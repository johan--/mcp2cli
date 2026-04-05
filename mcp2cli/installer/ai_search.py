"""AI-powered search for MCP server installation info."""

from __future__ import annotations

import json

import click

from mcp2cli.config.models import AISearchCandidate, AISearchResult
from mcp2cli.generator.llm_backend import get_backend

INSTALL_PROMPT_TEMPLATE = """你是 MCP server 安装助手。用户需要安装名为 "{server_name}" 的 MCP server。

请通过搜索互联网，找到最相关的 MCP server（最多 3 个候选），按推荐度从高到低排列，然后输出一个 JSON 对象。

搜索策略：
0. 必须使用 WebSearch 工具搜索，不要使用浏览器工具
1. 搜索 "{server_name} MCP server" 或 "{server_name} model context protocol"
2. 查看 GitHub 仓库，获取 star 数量、是否为官方仓库、README 中的 MCP 配置示例
3. 查看 npm / PyPI 包页面，确认包名和安装方式
4. 优先推荐：官方仓库 > star 数量多 > 维护活跃

输出格式（严格 JSON）：

```json
{{
  "found": true,
  "candidates": [
    {{
      "server_name": "{server_name}",
      "package_name": "package-name",
      "package_registry": "npm",
      "command": "npx",
      "args": ["-y", "{server_name}"],
      "env": {{
        "ENV_VAR_NAME": {{
          "description": "Description of this env var",
          "example": "https://example.com",
          "required": true,
          "sensitive": false
        }}
      }},
      "source_url": "https://github.com/...",
      "github_stars": "8.2k",
      "is_official": true,
      "description": "One-line description of what this MCP server does"
    }}
  ]
}}
```

字段说明：
- `candidates`: 候选列表，按推荐度排序，最多 3 个；若只找到 1 个也放入数组
- `github_stars`: GitHub star 数，格式如 "8.2k" 或 "430"，找不到填 ""
- `is_official`: 是否为官方/原作者发布的仓库
- `description`: 简短描述（英文，一句话）
- `command`: 启动命令（常见: uvx, npx, node, python）
- `env.required`: 是否必须提供
- `env.sensitive`: 是否为敏感信息（如 API Token）

如果找不到该 MCP server，返回：
```json
{{
  "found": false,
  "error": "Could not find MCP server named {server_name}",
  "suggestions": ["similar-server-name-1", "similar-server-name-2"]
}}
```

注意：
- 只输出 JSON，不要输出任何其他内容
- 优先使用官方文档中的配置格式
- command 优先使用 uvx (Python) 或 npx (Node.js) 等免安装运行器"""


def ai_search_server(server_name: str) -> AISearchResult | None:
    """Use AI to search for MCP server installation info.

    Returns AISearchResult or None on failure.
    """
    click.echo(f"🔍 Searching for {server_name} installation info...")

    backend = get_backend()
    prompt = INSTALL_PROMPT_TEMPLATE.format(server_name=server_name)

    result = backend.invoke(
        prompt,
        command_name="install search",
        server_name=server_name,
        show_progress=True,
        progress_message=f"Searching for {server_name}...",
        allowed_tools=["WebSearch"],
    )

    if result.is_error:
        click.echo(f"AI search failed: {result.result}", err=True)
        return None

    # Parse the JSON from LLM result
    text = result.result.strip()
    parsed = _extract_json(text)
    if parsed is None:
        # Retry once with session
        if result.session_id:
            click.echo("  Retrying AI search (invalid JSON)...")
            retry_result = backend.resume(
                result.session_id,
                "你的上一次输出不是合法的 JSON。请只输出 JSON 对象，不要输出任何其他文字。",
            )
            if not retry_result.is_error:
                parsed = _extract_json(retry_result.result.strip())

    if parsed is None:
        click.echo("Error: Could not parse AI search result as JSON.", err=True)
        return None

    search_result = AISearchResult.from_dict(parsed)

    if not search_result.found:
        click.echo(f"  ✗ Could not find MCP server \"{server_name}\"")
        if search_result.error:
            click.echo(f"  {search_result.error}")
        if search_result.suggestions:
            click.echo(f"  Did you mean: {', '.join(search_result.suggestions)}")
        backend.clear_session("install search", server_name)
        return search_result

    # Select from candidates (or auto-select if only one)
    candidate = _select_candidate(server_name, search_result.candidates)
    if candidate is None:
        backend.clear_session("install search", server_name)
        return None

    # Populate top-level fields from the selected candidate
    search_result.server_name = candidate.server_name
    search_result.package_name = candidate.package_name
    search_result.package_registry = candidate.package_registry
    search_result.command = candidate.command
    search_result.args = candidate.args
    search_result.env = candidate.env
    search_result.source_url = candidate.source_url

    if search_result.source_url:
        click.echo(f"  Source: {search_result.source_url}")

    backend.clear_session("install search", server_name)
    return search_result


def _select_candidate(
    server_name: str,
    candidates: list[AISearchCandidate],
) -> AISearchCandidate | None:
    """Show candidate list and let user pick one. Returns selected candidate or None."""
    if not candidates:
        click.echo(f"  ✗ No candidates found for \"{server_name}\"", err=True)
        return None

    if len(candidates) == 1:
        c = candidates[0]
        click.echo(f"  Found: {c.server_name} ({c.package_registry})")
        return c

    # Multiple candidates — show selection table
    click.echo(f"\nFound {len(candidates)} MCP servers matching \"{server_name}\". Please select one:\n")

    col_name = max((len(c.package_name or c.server_name) for c in candidates), default=4)
    col_name = max(col_name, 4)

    rows = []
    for i, c in enumerate(candidates, start=1):
        name = c.package_name or c.server_name
        stars = f"★ {c.github_stars}" if c.github_stars else "—"
        status = "✓ Official" if c.is_official else "Community"
        desc = c.description or ""
        suffix = " (Recommended)" if i == 1 else ""
        rows.append((i, name, stars, status, desc + suffix, c.source_url or ""))

    header = f"  {'#':>2}  {'Name':<{col_name}}  {'Stars':<7}  {'Status':<10}  Description"
    click.echo(header)
    click.echo("  " + "─" * (len(header) - 2))

    for i, name, stars, status, desc, url in rows:
        click.echo(f"  {i:>2}  {name:<{col_name}}  {stars:<7}  {status:<10}  {desc}")
        if url:
            click.echo(f"      {'':>{col_name}}             {url}")

    click.echo("")
    raw = click.prompt(
        f"  Enter number [1-{len(candidates)}]",
        default="1",
        show_default=True,
    ).strip()

    try:
        choice = int(raw)
        if 1 <= choice <= len(candidates):
            selected = candidates[choice - 1]
            click.echo(f"  Selected: {selected.package_name or selected.server_name}")
            return selected
    except ValueError:
        pass

    click.echo("  Invalid selection, using first result.")
    return candidates[0]


def _extract_json(text: str) -> dict | None:
    """Try to extract JSON from text that may contain markdown fences."""
    # Direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try extracting from ```json ... ```
    import re
    match = re.search(r"```(?:json)?\s*\n(.*?)```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # Try finding { ... } block
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass

    return None
