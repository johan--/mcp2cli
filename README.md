# mcp2cli

Convert MCP servers into CLI commands and compact AI agent skills.

## Why

Take [zereight/gitlab-mcp](https://github.com/zereight/gitlab-mcp) — it exposes **122 tools** across 14 categories (merge requests, issues, pipelines, wikis, etc.). Every tool schema gets injected into your AI conversation context on every request. We measured this directly against the Claude API:

| Per-request input tokens | Before (raw MCP) | After (mcp2cli) |
|---|---|---|
| Your message | 20 | 20 |
| Tool definitions (122 tools) | 27,969 | — |
| Skill file (1 file) | — | ~800 |
| **Total** | **27,989** | **~820** |
| **Reduction** | | **~97%** |

After `mcp2cli convert`, your AI agent stops seeing 122 tool definitions. Instead, it reads one small skill file, and calls CLI commands like `mcp2cli gitlab mr create --project-id 123 --title "Fix bug"` to get the job done.

Beyond token savings, some projects maintain both a CLI and an MCP server in parallel (e.g. the GitLab MCP server vs. the `glab` CLI). Keeping two interfaces in sync is a maintenance burden and inevitably leads to feature drift. mcp2cli eliminates the need — one MCP server, one generated CLI, always consistent.

## Quick Start

```bash
pip install mcp2cli
```

If you already have an MCP server configured in Claude, Cursor, or Codex — one command is all you need:

```bash
mcp2cli convert gitlab-mcp
```

That's it. Your MCP server is now a CLI, and the compressed skill files are synced to your AI clients.

## How It Works

```
                        mcp2cli convert
                              |
          +-------------------+-------------------+
          |                   |                   |
     1. Extract          2. AI Generate       3. Sync
   server config       CLI tree + skill     to AI clients
  from Claude/Cursor    from MCP tools     Claude/Cursor/Codex
          |                   |                   |
          v                   v                   v
     servers.yaml        cli.yaml +          ~/.claude/skills/
                         SKILL.md            ~/.cursor/skills/

                     --- at runtime ---

    mcp2cli gitlab mr list --project-id 123
          |
          v
    +-----------+       MCP protocol       +------------+
    |  mcp2cli  | --------------------->   | MCP Server |
    |  daemon   | <---------------------   | (gitlab)   |
    +-----------+       JSON result        +------------+
```

The daemon starts automatically on first use and stops when idle. You don't need to manage it.

## What `convert` Does

```
mcp2cli convert gitlab-mcp
```

1. Reads your MCP server config from Claude (`~/.claude.json`) / Cursor (`~/.cursor/mcp.json`) / Codex (`~/.codex/config.toml`)
2. Connects to the MCP server, discovers all tools, and uses AI to generate:
   ```
   ~/.agents/mcp2cli/gitlab-mcp/
   ├── cli.yaml    # CLI mapping — tool → command tree
   └── SKILL.md    # Skill file — compressed cheat-sheet for AI agents
   ```
3. Syncs skill files to your AI clients and disables the raw MCP server:
   ```
   ~/.claude/skills/gitlab-mcp.md
   ~/.cursor/skills/gitlab-mcp.md
   ~/.codex/skills/gitlab-mcp.md
   ```

## Presets

Don't want to wait for AI generation (~2-3 min)? Use **presets** — pre-built CLI mappings + skill files shared by the community. Downloads in ~10 seconds.

```bash
mcp2cli preset list                       # Browse available presets
mcp2cli preset pull mcp-atlassian         # Download + sync to AI clients
mcp2cli preset pull mcp-atlassian@1.2.3   # Pin a specific version
mcp2cli preset push gitlab-mcp            # Share your result with others
```

Presets are also checked automatically during `convert` and `install` — if one exists, you'll be prompted to use it instead of waiting for AI generation.

Custom registry for private/team use:

```bash
mcp2cli preset registry set https://github.com/your-org/mcp2cli-presets
```

## Usage Examples

```bash
# List all configured MCP servers
mcp2cli list

# Convert a server (auto-detects config from all clients)
mcp2cli convert gitlab-mcp

# Use the generated CLI
mcp2cli gitlab mr list --project-id 123
mcp2cli gitlab issue create --title "Fix login bug" --project-id 123

# Update when the MCP server adds new tools
mcp2cli update gitlab-mcp

# Remove everything (CLI, skills, config)
mcp2cli remove gitlab-mcp
```

## Commands

| Command | Description |
|---------|-------------|
| `convert <server>` | Convert an MCP server to skill-based usage |
| `install <server>` | Install a new MCP server and generate skills |
| `update <server>` | Update tools and regenerate CLI + skills |
| `remove <server>` | Remove a server and all generated artifacts |
| `list` | List all configured MCP servers |
| `scan <server>` | Discover all tools from an MCP server |
| `tools <server>` | List tools or show tool details |
| `call <server> <tool>` | Call an MCP tool directly |
| `generate cli <server>` | (Re)generate the CLI command tree |
| `generate skill <server>` | (Re)generate skill files |
| `skill sync <server>` | Sync skill files to AI clients |
| `skill unsync <server>` | Remove synced skills and re-enable MCP server |
| `preset list [server]` | Browse available presets (local + remote) |
| `preset pull <name[@ver]>` | Download a preset, skip AI generation |
| `preset push <server>` | Push local preset to community registry |
| `validate <server>` | Validate CLI mapping and skill files |

## License

MIT
