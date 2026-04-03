# 14. Update 命令设计 (`mcp2cli update`)

本文档是 [0.0-design-overview.md](0.0-design-overview.md) update 章节的详细设计，描述 `mcp2cli update` 命令的检测流程、版本对比策略和批量更新机制。

## 14.1 命令概述

```bash
# 更新单个 server：重新 scan → 对比变化 → 按需 generate cli --merge + generate skill
mcp2cli update mcp-atlassian

# 批量更新所有已转换的 server
mcp2cli update --all

# 选项
mcp2cli update mcp-atlassian --yes       # 跳过确认提示，直接执行
mcp2cli update mcp-atlassian --dry-run   # 只预览变化，不写入
mcp2cli update --all --yes               # 批量无交互更新
```

`mcp2cli update` 是 `install`/`convert` 完成后的增量维护命令，专门处理 MCP server 升级的场景：新增 tool、删除 tool、版本号更新。

## 14.2 前置条件

`update` 仅对已完成 scan 的 server 有效：

| 条件 | 行为 |
|------|------|
| `tools/<server>.json` 不存在 | 报错：`mcp-atlassian has not been scanned. Run 'mcp2cli convert mcp-atlassian' first.` |
| `cli/<server>.yaml` 不存在 | 警告：CLI tree 不存在，将在 scan 后重新生成（非 --merge 模式） |
| server 不在 `servers.yaml` | 报错：`mcp-atlassian is not registered. Run 'mcp2cli convert' or 'mcp2cli install' first.` |

## 14.3 单 Server 更新流程

```
mcp2cli update <server>
            │
            ▼
  ┌─ 1. 前置检查 ─────────────────────────────────┐
  │  验证 tools/<server>.json 和 servers.yaml 存在  │
  │  读取旧版本信息：                               │
  │    old_version    ← tools/<server>.json[version] │
  │    old_tool_names ← tools/<server>.json[tools[].name] │
  └──────────────────────┬────────────────────────┘
                         │
                         ▼
  ┌─ 2. 重新 Scan ────────────────────────────────┐
  │  连接 MCP server → list_tools                 │
  │  获取：                                        │
  │    new_version    ← serverInfo.version         │
  │    new_tools      ← tool 列表（含 inputSchema）│
  │  失败 → 报错退出，保留旧 tools JSON 不变        │
  └──────────────────────┬────────────────────────┘
                         │
                         ▼
  ┌─ 3. 对比变化 ─────────────────────────────────┐
  │  计算差异：                                    │
  │    version_changed = (new_version != old_version) │
  │    added_tools     = new_tool_names - old_tool_names │
  │    removed_tools   = old_tool_names - new_tool_names │
  │    schema_changed  = any tool's inputSchema differs │
  │                                               │
  │  无任何变化（version、tool 列表、schema 均相同）│
  │  → 打印 "mcp-atlassian is up-to-date" 退出    │
  └──────────────────────┬────────────────────────┘
                         │
                         ▼（有变化）
  ┌─ 4. 展示变化摘要 ─────────────────────────────┐
  │  version: 1.2.3 → 1.3.0                       │
  │  tools: 65 → 68                               │
  │    + jira_bulk_create_issues                  │
  │    + jira_get_bulk_issue_property             │
  │    + confluence_move_page                     │
  │    schema changes: jira_create_issue (2 params)│
  │                                               │
  │  未指定 --yes → 交互确认 "Continue? [Y/n]"    │
  │  指定 --yes  → 直接继续                        │
  │  --dry-run   → 到此退出，不执行后续步骤         │
  └──────────────────────┬────────────────────────┘
                         │
                         ▼（用户确认/--yes）
  ┌─ 5. 写入新 tools JSON ──────────────────────────┐
  │  覆盖写入 tools/<server>.json                  │
  │  更新 version、scanned_at、tools 数组           │
  └──────────────────────┬────────────────────────┘
                         │
                         ▼
  ┌─ 6. 更新 CLI 命令树 ────────────────────────────┐
  │  若 cli/<server>.yaml 存在：                   │
  │    mcp2cli generate cli <server> --merge       │
  │    （AI 仅处理新增/删除 tool，保留已有映射）    │
  │  若 cli/<server>.yaml 不存在：                 │
  │    mcp2cli generate cli <server>               │
  │    （全量重新生成）                             │
  └──────────────────────┬────────────────────────┘
                         │
                         ▼
  ┌─ 7. 更新 Skill 文件 ────────────────────────────┐
  │  mcp2cli generate skill <server>               │
  │  （通过 source_cli_hash 自动判断增量/跳过）     │
  └──────────────────────┬────────────────────────┘
                         │
                         ▼
  ┌─ 8. Skill Sync ─────────────────────────────────┐
  │  mcp2cli skill sync <server>                   │
  │  将更新后的 skill 复制到各客户端目录             │
  │  （仅在 generate skill 实际写入了变更时执行）   │
  └──────────────────────┬────────────────────────┘
                         │
                         ▼
  ┌─ 9. 输出更新摘要 ─────────────────────────────┐
  │  ✓ tools scanned: 65 → 68 (+3 -0)             │
  │  ✓ CLI tree: 3 new mappings added, 65 preserved│
  │  ✓ SKILL.md: updated (395 tokens)             │
  │  ✓ Skill synced to: claude, cursor, codex      │
  │  Done! mcp-atlassian updated: 1.2.3 → 1.3.0   │
  └────────────────────────────────────────────────┘
```

## 14.4 版本对比策略

| 情况 | 判定 | 处理 |
|------|------|------|
| version 相同，tool 列表相同，schema 相同 | 无变化 | 打印 up-to-date，退出 |
| version 不同，tool 无变化 | 有更新 | 仅更新 tools JSON 中的 version；跳过 generate cli/skill |
| version 相同，tool 有新增/删除 | 有更新 | 执行 generate cli --merge + generate skill |
| version 不同，tool 有新增/删除 | 有更新 | 执行完整更新流程 |
| version 为 null（server 不报版本） | 只看 tool 差异 | tool 无差异则视为无变化 |
| schema 有变化，tool 无增删 | 有变化 | 更新 tools JSON，不触发 generate cli（命令树结构未变）；generate skill 通过 source_cli_hash 判断是否需要更新 |

**注意**：`source_cli_hash` 跟踪的是 `cli/<server>.yaml` 内容的变化，而非 tool schema。因此 schema 变化但 CLI 树无变化时，`generate skill` 不会被触发（通过 hash 跳过），schema 细节仍通过 `--help` 从 tools JSON 实时读取。

## 14.5 批量更新 (`--all`)

```
mcp2cli update --all [--yes] [--dry-run]
            │
            ▼
  ┌─ 1. 读取 servers.yaml ────────────────────────┐
  │  获取所有已注册的 server 列表                  │
  │  过滤：仅处理已有 tools/<server>.json 的 server │
  └──────────────────────┬────────────────────────┘
                         │
                         ▼
  ┌─ 2. 并发 Scan ────────────────────────────────┐
  │  并发连接所有 server（默认最多 4 个并发）       │
  │  单个 server 连接失败 → 记录错误，继续其他      │
  └──────────────────────┬────────────────────────┘
                         │
                         ▼
  ┌─ 3. 汇总变化报告 ─────────────────────────────┐
  │  NAME             STATUS         CHANGES      │
  │  mcp-atlassian    needs update   +3 tools, v↑ │
  │  playwright       up-to-date     -             │
  │  mcp-github       needs update   -2 tools      │
  │  mcp-slack        error          connection failed │
  │                                               │
  │  3 servers scanned, 2 need update, 1 error    │
  │                                               │
  │  未指定 --yes → 确认 "Update 2 servers? [Y/n]"│
  │  --dry-run → 到此退出                          │
  └──────────────────────┬────────────────────────┘
                         │
                         ▼（用户确认/--yes）
  ┌─ 4. 顺序执行各 server 的更新 ──────────────────┐
  │  按 needs-update 列表顺序逐一执行              │
  │  每个 server 的 generate cli/skill 顺序执行    │
  │  单个失败 → 打印错误，继续下一个               │
  └──────────────────────┬────────────────────────┘
                         │
                         ▼
  ┌─ 5. 最终汇总 ─────────────────────────────────┐
  │  ✓ mcp-atlassian: updated (1.2.3 → 1.3.0)    │
  │  ✓ mcp-github: updated (-2 tools)             │
  │  ✗ mcp-slack: connection failed               │
  │  2/2 updates completed (1 error)              │
  └────────────────────────────────────────────────┘
```

## 14.6 自动版本变化提示（可选配置）

通过 `~/.agents/mcp2cli/config.yaml` 开启：

```yaml
# ~/.agents/mcp2cli/config.yaml
auto_update_check: true   # 每次 CLI 调用时后台检测版本变化（默认 false）
```

开启后，daemon 在每次与 MCP server 建立连接时，将 serverInfo.version 与 `tools/<server>.json` 中记录的 version 对比。版本不一致时，在命令执行完毕后附加提示：

```
[mcp-atlassian] Server updated: 1.2.3 → 1.3.0. Run 'mcp2cli update mcp-atlassian' to regenerate CLI and skill.
```

- 提示仅输出一次（记录到 `~/.agents/mcp2cli/update_hints.yaml`，已提示的 server+version 对不重复提示）
- 不阻塞命令执行，检测在 daemon 侧完成

## 14.7 CLI 参数设计

```bash
mcp2cli update <server> [OPTIONS]
mcp2cli update --all [OPTIONS]

Arguments:
  <server>            要更新的 MCP server 名称（与 --all 互斥）

Options:
  --all               更新所有已注册的 server
  --yes, -y           跳过确认提示，直接执行
  --dry-run           只扫描并预览变化，不写入任何文件
  --concurrency N     --all 模式下的并发 scan 数（默认 4）
```

## 14.8 输出示例

### 单 server 有更新

```
$ mcp2cli update mcp-atlassian
Scanning mcp-atlassian...

Changes detected:
  version: 1.2.3 → 1.3.0
  tools: 65 → 68
    + jira_bulk_create_issues
    + jira_get_bulk_issue_property
    + confluence_move_page

Continue? [Y/n] y
✓ tools/mcp-atlassian.json updated
✓ CLI tree: 3 new commands merged, 65 preserved
✓ SKILL.md: updated (395 tokens, +3 commands)
✓ Skill synced to: claude, cursor, codex
Done! mcp-atlassian updated: 1.2.3 → 1.3.0
```

### 单 server 无变化

```
$ mcp2cli update mcp-atlassian
Scanning mcp-atlassian...
mcp-atlassian is up-to-date (version 1.2.3, 65 tools). Nothing to do.
```

### --dry-run

```
$ mcp2cli update mcp-atlassian --dry-run
Scanning mcp-atlassian...

Changes detected (dry-run, no files written):
  version: 1.2.3 → 1.3.0
  tools: 65 → 68
    + jira_bulk_create_issues
    + jira_get_bulk_issue_property
    + confluence_move_page

Run without --dry-run to apply.
```

### --all 批量

```
$ mcp2cli update --all
Scanning 3 servers (concurrency: 4)...
  mcp-atlassian ... needs update (+3 tools, 1.2.3 → 1.3.0)
  playwright    ... up-to-date
  mcp-github    ... needs update (-2 tools)

Update 2 servers? [Y/n] y

[1/2] Updating mcp-atlassian...
  ✓ tools updated
  ✓ CLI tree merged
  ✓ SKILL.md updated

[2/2] Updating mcp-github...
  ✓ tools updated
  ✓ CLI tree merged
  ✓ SKILL.md updated

Done! 2/2 servers updated.
```

## 14.9 与其他命令的关系

| 命令 | 和 update 的关系 |
|------|-----------------|
| `mcp2cli scan <server>` | update 内部调用 scan 获取最新 tool 列表，但 scan 不做对比、不触发 generate |
| `mcp2cli generate cli --merge` | update 在检测到 tool 增删时自动调用 |
| `mcp2cli generate skill` | update 在 CLI YAML 变化后自动调用（增量模式） |
| `mcp2cli skill sync` | update 在 generate skill 实际写入变更后自动调用，将更新同步到各客户端 |
| `mcp2cli convert` | 首次转换命令，update 是转换后的维护命令 |
| `mcp2cli install` | 首次安装命令，update 是安装后的维护命令 |

## 14.10 文件布局

`update` 命令不新增文件，复用已有布局：

```
mcp2cli/
└── mcp2cli/
    ├── main.py                       # 新增 update 命令入口
    └── updater/                      # 新增模块
        ├── __init__.py
        ├── diff.py                   # tool 列表差异计算（version/names/schema 对比）
        └── pipeline.py               # update pipeline（scan → diff → generate → skill sync → summary）
```

`updater/diff.py` 导出：

```python
@dataclass
class ToolsDiff:
    version_changed: bool
    old_version: str | None
    new_version: str | None
    added_tools: list[str]
    removed_tools: list[str]
    schema_changed_tools: list[str]

    @property
    def has_any_change(self) -> bool: ...
    @property
    def needs_cli_regen(self) -> bool:
        """tool 增删时需要 generate cli --merge"""
        return bool(self.added_tools or self.removed_tools)
```
