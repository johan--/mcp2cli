# mcp2cli install 设计文档

本文档是 [0.0-design-overview.md](0.0-design-overview.md) 第十一章 `mcp2cli install` 的展开设计。

## 一、功能概述

本章涉及两个命令：

- **`mcp2cli add`**：安装 MCP server 到物理机上
- **`mcp2cli install`**：一键全流程，内部调用 `add`，再通过 Step Pipeline 依次执行 scan → generate cli → generate skill

### mcp2cli add 流程

```
mcp2cli add mcp-atlassian
        │
        ▼
┌─ 1. AI 搜索安装信息 ────────────────────┐
│  调用 claude -p，搜索互联网获取：          │
│  - command (如 uvx, npx, node)          │
│  - args (如 ["mcp-atlassian"])          │
│  - env (如 JIRA_URL, JIRA_API_TOKEN)    │
│  - 哪些 env 需要用户填写                  │
└───────────────────┬─────────────────────┘
                    │
                    ▼
┌─ 2. 交互式补全 ────────────────────────┐
│  提示用户输入必需的 env 值：             │
│  JIRA_URL: https://xxx.atlassian.net   │
│  JIRA_API_TOKEN: ****                  │
└───────────────────┬─────────────────────┘
                    │
                    ▼
┌─ 3. 安装 MCP server package ──────────┐
│  根据 command 类型执行预安装：           │
│  uvx  → uvx install mcp-atlassian      │
│  npx  → npm install -g <package>       │
│  node → 检查路径/提示用户手动安装        │
│                                        │
│  失败处理：打印警告，继续写入配置         │
│  （AI 客户端首次启动时会自动安装）        │
└───────────────────┬─────────────────────┘
                    │
                    ▼
┌─ 4. 写入三个配置文件 ──────────────────┐
│  ~/.claude.json         ✓ 写入         │
│  ~/.cursor/mcp.json     ✓ 写入         │
│  ~/.codex/config.toml   ⊘ 已存在,跳过   │
└────────────────────────────────────────┘
```

### mcp2cli install 流程

```
mcp2cli install mcp-atlassian
        │
        ▼
┌─ 阶段 A: add ───────────────────────────┐
│  mcp2cli add mcp-atlassian              │
│  (AI 搜索 + 交互补全 + 安装 + 写配置)    │
└───────────────────┬─────────────────────┘
                    │ 成功
                    ▼
┌─ 阶段 B: Step Pipeline ────────────────┐
│                                        │
│  Step 1: scan                          │
│    mcp2cli scan mcp-atlassian          │
│    失败 → 警告 + 跳过后续步骤           │
│         │ 成功                          │
│         ▼                              │
│  Step 2: generate cli                  │
│    mcp2cli generate cli mcp-atlassian  │
│    失败 → 警告 + 跳过后续步骤           │
│         │ 成功                          │
│         ▼                              │
│  Step 3: generate skill                │
│    mcp2cli generate skill mcp-atlassian│
│    失败 → 警告                          │
│                                        │
└────────────────────────────────────────┘
```

## 二、命令接口

### 2.1 mcp2cli add（安装并注册 MCP server）

```bash
mcp2cli add <server-name> [OPTIONS]

Arguments:
  server-name          MCP server 名称（如 mcp-atlassian, playwright）

Options:
  --targets            写入哪些配置文件 (默认: claude,cursor,codex)
                       可选值: claude, cursor, codex, all
                       示例: --targets claude,cursor
  --env KEY=VALUE      预设 env 值，跳过交互式询问（可多次使用）
                       示例: --env JIRA_URL=https://xxx.atlassian.net
  --skip-install       跳过 package 安装步骤，只写配置文件
  --dry-run            只展示将要执行的操作，不实际修改文件
  --yes                跳过确认提示，直接执行
```

### 2.2 mcp2cli install（一键全流程）

```bash
mcp2cli install <server-name> [OPTIONS]

Arguments:
  server-name          MCP server 名称（如 mcp-atlassian, playwright）

Options:
  --targets            同 add，透传给 add 阶段
  --env KEY=VALUE      同 add，透传给 add 阶段
  --dry-run            只展示将要写入的内容，不实际修改文件（不执行 pipeline）
  --yes                跳过确认提示，直接执行
  --skip-generate      跳过 pipeline（等价于直接使用 mcp2cli add）
```

### 2.3 配置文件路径

| 目标 | 配置文件路径 | 格式 |
|------|-------------|------|
| Claude | `~/.claude.json` | JSON (`mcpServers` 字段) |
| Cursor | `~/.cursor/mcp.json` | JSON (`mcpServers` 字段) |
| Codex | `~/.codex/config.toml` | TOML (`[[mcp_servers]]` 表) |

## 三、AI 辅助安装（核心设计）

### 3.1 调用方式

使用 `claude -p` 搜索互联网，获取 MCP server 的安装配置信息：

```bash
claude -p "<install_prompt>" --output-format json
```

**关键设计：**

- AI 通过搜索 GitHub README、npm/PyPI 页面、官方文档等获取安装信息
- 输出结构化 JSON，由程序侧解析和处理

### 3.2 Install Prompt 模板

```
你是 MCP server 安装助手。用户需要安装名为 "{{SERVER_NAME}}" 的 MCP server。

请通过搜索互联网，找到该 MCP server 的安装和配置信息，然后输出一个 JSON 对象。

搜索策略：
1. 搜索 "{{SERVER_NAME}} MCP server" 或 "{{SERVER_NAME}} model context protocol"
2. 查看 GitHub 仓库的 README，找到 MCP 配置示例
3. 查看 npm / PyPI 包页面，确认包名和安装方式

输出格式（严格 JSON）：

```json
{
  "found": true,
  "server_name": "mcp-atlassian",
  "package_name": "mcp-atlassian",
  "package_registry": "pypi",
  "command": "uvx",
  "args": ["mcp-atlassian"],
  "env": {
    "JIRA_URL": {
      "description": "Your Jira instance URL",
      "example": "https://your-company.atlassian.net",
      "required": true,
      "sensitive": false
    },
    "JIRA_API_TOKEN": {
      "description": "Jira API token for authentication",
      "example": "",
      "required": true,
      "sensitive": true
    }
  },
  "source_url": "https://github.com/..."
}
```

字段说明：
- `found`: 是否找到该 MCP server
- `command`: 启动命令（常见: uvx, npx, node, python）
- `args`: 命令参数数组
- `env`: 环境变量定义
  - `required`: 是否必须提供
  - `sensitive`: 是否为敏感信息（如 API Token），用于决定是否在确认界面隐藏显示
- `source_url`: 信息来源 URL，供用户查验

如果找不到该 MCP server，返回：
```json
{
  "found": false,
  "error": "未找到名为 xxx 的 MCP server",
  "suggestions": ["类似名称的 server 列表"]
}
```

注意：
- 只输出 JSON，不要输出任何其他内容
- 优先使用官方文档中的配置格式
- command 优先使用 uvx (Python) 或 npx (Node.js) 等免安装运行器
```

### 3.3 AI 返回结果处理

```
AI 返回 JSON
    │
    ├── found: false
    │   → 输出错误信息 + suggestions
    │   → 退出
    │
    └── found: true
        │
        ▼
    解析 env 定义
        │
        ├── 检查 --env 参数预设值，匹配的直接填入
        │
        └── 剩余 required=true 且未预设的 env
            → 交互式询问用户
            → sensitive=true 的字段使用密码输入模式（不回显）
```

### 3.4 会话续接（信息不全时）

如果 AI 首次搜索信息不完整（如只找到 command 但不确定 env），通过 `--resume` 续接：

```bash
# 首次调用返回 session_id
claude -p "<install_prompt>" --output-format json ...
# → session_id: "abc-123"

# 信息不完整时，追加上下文续接
claude -p "之前的搜索结果缺少 env 配置信息，请尝试搜索 {{SERVER_NAME}} 的环境变量配置要求" \
  --output-format json \
  --resume abc-123
```

最多重试 2 次，仍不完整则使用已获取的信息继续（env 部分可能为空），提示用户后续手动补充。

## 四、配置文件写入

### 4.1 写入流程

```
对每个目标配置文件 (claude, cursor, codex):
    │
    ├── 文件不存在 → 创建文件并写入 server 定义
    │
    ├── 文件存在，server 已定义 → 跳过，打印提示
    │   "⊘ ~/.claude.json: mcp-atlassian already exists, skipped"
    │
    └── 文件存在，server 未定义 → 追加 server 定义
        "✓ ~/.claude.json: mcp-atlassian added"
```

### 4.2 Claude 配置写入 (`~/.claude.json`)

```json
{
  "mcpServers": {
    "mcp-atlassian": {
      "command": "uvx",
      "args": ["mcp-atlassian"],
      "env": {
        "JIRA_URL": "https://your-company.atlassian.net",
        "JIRA_API_TOKEN": "user_provided_token"
      }
    }
  }
}
```

**写入逻辑：**

```python
# 伪代码
config = json.load(claude_json_path) if exists else {}
servers = config.setdefault("mcpServers", {})
if server_name in servers:
    print(f"⊘ {path}: {server_name} already exists, skipped")
    return
servers[server_name] = {
    "command": command,
    "args": args,
    "env": env_values  # 只写入有值的 env
}
json.dump(config, claude_json_path, indent=2)
print(f"✓ {path}: {server_name} added")
```

### 4.3 Cursor 配置写入 (`~/.cursor/mcp.json`)

格式与 Claude 完全相同：

```json
{
  "mcpServers": {
    "mcp-atlassian": {
      "command": "uvx",
      "args": ["mcp-atlassian"],
      "env": {
        "JIRA_URL": "https://your-company.atlassian.net",
        "JIRA_API_TOKEN": "user_provided_token"
      }
    }
  }
}
```

### 4.4 Codex 配置写入 (`~/.codex/config.toml`)

TOML 格式不同于 JSON：

```toml
[[mcp_servers]]
name = "mcp-atlassian"
command = "uvx"
args = ["mcp-atlassian"]

[mcp_servers.env]
JIRA_URL = "https://your-company.atlassian.net"
JIRA_API_TOKEN = "user_provided_token"
```

**写入逻辑：**

```python
# 伪代码
config = toml.load(codex_toml_path) if exists else {}
servers = config.setdefault("mcp_servers", [])
for s in servers:
    if s.get("name") == server_name:
        print(f"⊘ {path}: {server_name} already exists, skipped")
        return
servers.append({
    "name": server_name,
    "command": command,
    "args": args,
    "env": env_values
})
toml.dump(config, codex_toml_path)
print(f"✓ {path}: {server_name} added")
```

### 4.5 写入前确认

默认在写入前展示预览，要求用户确认：

```
The following configuration will be written:

  Server: mcp-atlassian
  Command: uvx mcp-atlassian
  Environment:
    JIRA_URL = https://your-company.atlassian.net
    JIRA_API_TOKEN = ****  (sensitive)

  Targets:
    ~/.claude.json          → will add
    ~/.cursor/mcp.json      → will add
    ~/.codex/config.toml    → already exists, skip

  Source: https://github.com/sooperset/mcp-atlassian

Proceed? [Y/n]
```

使用 `--yes` 跳过此确认。使用 `--dry-run` 则只显示预览不执行。

## 五、Step Pipeline（install 专属）

`mcp2cli install` 在 `add` 完成后，通过 Step Pipeline 依次执行 scan → generate cli → generate skill。

### 5.1 Step 数据结构

```python
@dataclass
class Step:
    name: str           # 步骤名，用于日志和错误信息
    run: Callable       # 执行函数，返回 bool（是否成功）
    retry_cmd: str      # 失败时提示用户的手动重试命令
    depends_on: list[str] = field(default_factory=list)
    # depends_on 列表中任意一步失败，本步自动跳过
```

### 5.2 Pipeline 定义与 Runner

```python
pipeline: list[Step] = [
    Step(
        name="scan",
        run=lambda: run_scan(server_name),
        retry_cmd=f"mcp2cli scan {server_name}",
    ),
    Step(
        name="generate-cli",
        run=lambda: run_generate_cli(server_name),
        retry_cmd=f"mcp2cli generate cli {server_name}",
        depends_on=["scan"],        # scan 失败则跳过
    ),
    Step(
        name="generate-skill",
        run=lambda: run_generate_skill(server_name),
        retry_cmd=f"mcp2cli generate skill {server_name}",
        depends_on=["generate-cli"],
    ),
]

# Runner（无需 reduce/chain，for 循环 + 结构化 Step 即是最优平衡）
results: dict[str, bool] = {}
for step in pipeline:
    if any(not results.get(dep) for dep in step.depends_on):
        warn(f"Skipping {step.name}: dependency failed")
        results[step.name] = False
        continue

    ok = step.run()
    results[step.name] = ok
    if not ok:
        warn(f"{step.name} failed. Retry later: {step.retry_cmd}")
        # 不 break，让后续无依赖的步骤继续执行
```

**设计说明**：
- `depends_on` 让依赖关系声明在数据里而非散落在 if-else 中
- 每步失败只打警告，不中止 pipeline（除非后续步骤有依赖）
- Runner 不感知具体步骤内容，仅负责调度和错误收集

### 5.3 跳过 Pipeline

```bash
# 只写配置文件，等价于直接用 mcp2cli add
mcp2cli install mcp-atlassian --skip-generate
```

## 六、端到端示例

### 6.1 标准安装流程

```
$ mcp2cli install mcp-atlassian

🔍 Searching for mcp-atlassian installation info...
   Found: mcp-atlassian (PyPI)
   Source: https://github.com/sooperset/mcp-atlassian

📋 Environment variables required:
   JIRA_URL (Your Jira instance URL)
   > https://mycompany.atlassian.net

   JIRA_API_TOKEN (Jira API token, sensitive)
   > ********

   CONFLUENCE_URL (Your Confluence URL, optional)
   > (skip)

📝 Configuration preview:
   Server: mcp-atlassian
   Command: uvx mcp-atlassian
   Env: JIRA_URL, JIRA_API_TOKEN (2 values set)

   Targets:
     ~/.claude.json        → will add
     ~/.cursor/mcp.json    → will add
     ~/.codex/config.toml  → will add

   Proceed? [Y/n] y

✓ ~/.claude.json: mcp-atlassian added
✓ ~/.cursor/mcp.json: mcp-atlassian added
✓ ~/.codex/config.toml: mcp-atlassian added

🔧 Scanning mcp-atlassian...
   Found 65 tools. Written to ~/.agents/mcp2cli/tools/mcp-atlassian.json

🤖 Generating CLI command tree...
   mcp-atlassian
   ├── jira
   │   ├── issue (create, get, search, update, delete, transition)
   │   ├── sprint (create, update, list, issues)
   │   ├── board (list, issues)
   │   └── project (list, issues, components, versions)
   └── confluence
       ├── page (get, create, update, delete, move, children)
       ├── search
       ├── comment (list, add, reply)
       └── attachment (list, upload, download, delete)
   Coverage: 65/65 tools ✓
   Written to ~/.agents/mcp2cli/cli/mcp-atlassian.yaml

🧩 Generating skill definitions...
   Generated 12 skills for mcp-atlassian
   Written to ~/.agents/mcp2cli/skills/mcp-atlassian/

✅ Installation complete!
   Next steps:
   - Use CLI: mcp2cli mcp-atlassian jira issue create --help
   - Use skill: mcp2cli mcp-atlassian jira (in Claude Code)
```

### 6.2 已存在时跳过

```
$ mcp2cli install mcp-atlassian

🔍 Searching for mcp-atlassian installation info...
   Found: mcp-atlassian (PyPI)

📝 Configuration preview:
   Targets:
     ~/.claude.json        → already exists, skip
     ~/.cursor/mcp.json    → already exists, skip
     ~/.codex/config.toml  → will add

   Proceed? [Y/n] y

⊘ ~/.claude.json: mcp-atlassian already exists, skipped
⊘ ~/.cursor/mcp.json: mcp-atlassian already exists, skipped
✓ ~/.codex/config.toml: mcp-atlassian added

🔧 Scanning mcp-atlassian...
   ...
```

### 6.3 找不到 server

```
$ mcp2cli install mcp-jiraa

🔍 Searching for mcp-jiraa installation info...
   ✗ Could not find MCP server "mcp-jiraa"

   Did you mean:
     - mcp-atlassian (includes Jira + Confluence)

   You can also provide config manually:
     mcp2cli install mcp-jiraa --command uvx --args mcp-jiraa
```

### 6.4 预设 env 跳过交互

```
$ mcp2cli install mcp-atlassian \
    --env JIRA_URL=https://mycompany.atlassian.net \
    --env JIRA_API_TOKEN=my_token \
    --yes

🔍 Searching for mcp-atlassian installation info...
   Found: mcp-atlassian (PyPI)

✓ ~/.claude.json: mcp-atlassian added
✓ ~/.cursor/mcp.json: mcp-atlassian added
✓ ~/.codex/config.toml: mcp-atlassian added

🔧 Scanning mcp-atlassian... 65 tools found.
🤖 Generating CLI command tree... 65/65 tools ✓
🧩 Generating skill definitions... 12 skills ✓

✅ Installation complete!
```

### 6.5 Dry-run 模式

```
$ mcp2cli install mcp-atlassian --dry-run

🔍 Searching for mcp-atlassian installation info...
   Found: mcp-atlassian (PyPI)

📋 Environment variables required:
   JIRA_URL: > https://mycompany.atlassian.net
   JIRA_API_TOKEN: > ********

📝 [DRY RUN] Would write to:

   ~/.claude.json:
   {
     "mcpServers": {
       "mcp-atlassian": {
         "command": "uvx",
         "args": ["mcp-atlassian"],
         "env": { "JIRA_URL": "...", "JIRA_API_TOKEN": "..." }
       }
     }
   }

   ~/.cursor/mcp.json:
   (same as above)

   ~/.codex/config.toml:
   [[mcp_servers]]
   name = "mcp-atlassian"
   command = "uvx"
   args = ["mcp-atlassian"]
   ...

   No files were modified.
```

## 七、错误处理

| 场景 | 处理方式 |
|------|---------|
| AI 搜索无结果 | 展示 suggestions，提示用户手动指定 `--command` |
| AI 返回非法 JSON | 通过 `--resume` 重试 1 次，仍失败则报错退出 |
| 配置文件无写入权限 | 报错，提示用户检查文件权限 |
| scan 失败（server 无法启动） | 打印警告，提示手动重试，不阻断整体流程 |
| generate 失败 | 打印警告，提示手动重试 |
| 所有目标配置均已存在 | 提示全部跳过，询问是否要 `--force` 覆盖 |

## 八、代码实现位置

```
mcp2cli/
├── main.py                    # 新增 add / install 子命令
├── installer/
│   ├── __init__.py
│   ├── ai_search.py           # AI 搜索安装信息（claude -p 调用、prompt 构造、JSON 解析）
│   ├── config_writer.py       # 三配置文件写入（Claude/Cursor/Codex 各一个写入函数）
│   ├── interactive.py         # 交互式 env 输入（密码模式、可选跳过）
│   └── pipeline.py            # Step dataclass + pipeline runner
```

## 九、与现有模块的关系

```
mcp2cli add <server>           mcp2cli install <server>
    │                               │
    │                               ├─ 调用 add（复用上述所有模块）
    │                               │
    ├── installer/ai_search.py      └─ installer/pipeline.py  ← 新增
    │     调用 claude -p                  Step pipeline runner
    │
    ├── installer/config_writer.py
    │     读写 ~/.claude.json 等
    │
    └── installer/interactive.py
          getpass / input

pipeline 内部调用（已有模块）：
    scan        → scanner.py
    generate cli  → generator/cli_gen.py
    generate skill → generator/skill_gen.py
```
