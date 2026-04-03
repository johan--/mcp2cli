# 15 — JSON 输入支持

## 一、背景与动机

mcp2cli 通过 `--kebab-case` flags 传递参数，覆盖了大部分简单场景。但 MCP tool 的 `inputSchema` 中存在嵌套对象、数组等复杂类型（如 Jira 的 `additional_fields: {"priority": {"name": "High"}}`），无法用简单 flags 表达。

**设计原则：简单场景用 flags，复杂场景用 JSON 位置参数，两者可混合。**

## 二、方案：位置参数 JSON

采用**位置参数**方式传入 JSON，命令末尾直接跟 JSON 字符串，无需额外 flag 名，避免与 tool 参数名冲突：

```bash
# 位置参数：命令末尾直接跟 JSON
mcp2cli jira issue create '{"project_key":"INFRA","summary":"Fix bug","additional_fields":{"priority":{"name":"High"}}}'

# 混合使用：JSON 提供基础参数，flags 覆盖同名 key
mcp2cli jira issue create '{"project_key":"INFRA","summary":"Original"}' --summary "Overridden"
# 结果: {"project_key": "INFRA", "summary": "Overridden"}
```

### 2.1 识别规则

Resolver 在完成路径解析（找到叶子节点 `_tool`）后，扫描剩余 tokens：

- 以 `{` 开头的 token → 视为内联 JSON 字符串，`json.loads()` 解析为 dict
- 以 `--` 开头的 token → 正常 flag 解析
- 其他 → 报错（叶子命令不接受无名位置参数）

只允许一个 JSON 位置参数。JSON 中的 key 使用 **snake_case**（与 MCP inputSchema 一致），不做 kebab→snake 转换。

### 2.2 Flags 与 JSON 的合并

```python
def merge_params(json_params, flag_params):
    """浅合并，flags 优先覆盖 JSON。"""
    result = {**json_params, **flag_params}
    return result
```

- `--flags` > 位置参数 JSON（显式优先）
- 浅合并，不做深度递归（flags 无法表达嵌套，不会有嵌套冲突）

### 2.3 Flag 值的 JSON 自动解析

单个 flag 的值如果对应 inputSchema 中的 `object` 或 `array` 类型，自动执行 `json.loads()`：

```bash
# additional_fields 在 inputSchema 中是 object 类型 → 自动解析
mcp2cli jira issue create --project-key INFRA --additional-fields '{"priority":{"name":"High"}}'

# summary 在 inputSchema 中是 string 类型 → 保持原样
mcp2cli jira issue create --project-key INFRA --summary '{"not":"parsed"}'
```

## 三、解析流程

```
输入: mcp2cli jira issue create '{"project_key":"INFRA"}' --summary "Fix"

解析过程:
  1-4. (不变) 路径解析 → 找到 _tool: jira_create_issue
  5. 参数解析:
     a. 扫描剩余 tokens:
        - 以 { 开头 → json.loads() → json_params
        - 以 -- 开头 → flag 解析 → flag_params
        - 其他 → 报错
     b. merge: {**json_params, **flag_params}
     c. 校验合并结果 against inputSchema
  6. 转发到 daemon（不变）
```

## 四、错误处理

| 场景 | 错误信息 |
|------|----------|
| JSON 不合法 | `Error: invalid JSON argument: Expecting ',' delimiter ...` |
| 多个 JSON 位置参数 | `Error: only one JSON argument allowed` |
| JSON key 不在 inputSchema 中 | 与 flag 校验逻辑一致，列出可用参数 |
| 非 JSON 非 flag 的位置参数 | `Error: unexpected argument: xxx` |

## 五、`--help` 展示

叶子命令的 `--help` 增加 JSON 提示：

```
Usage: mcp2cli jira issue create [OPTIONS] [JSON]

Create a new Jira issue

Options:
  --project-key TEXT    The JIRA project key (required)
  --summary TEXT        Summary/title of the issue (required)
  --issue-type TEXT     Issue type: Task, Bug, Story, Epic
  ...

JSON Input:
  mcp2cli ... create '{"project_key":"INFRA","summary":"Fix bug"}'
  Flags override JSON:  ... create '{"project_key":"INFRA"}' --summary "Override"
```

## 六、SKILL.md 说明

通用说明区域添加：

```
For complex/nested params, pass JSON: `mcp2cli ... create '{"key":"value"}'`.
```
