# Branch & Commit Commands

## branch create — Create a new branch

```bash
mcp2cli gitlab branch create --branch feature/my-feature --ref main
mcp2cli gitlab branch create --project-id mygroup/myrepo --branch hotfix/bug-123 --ref main
```

Required: `--branch`

Also supports: `--project-id`, `--ref`

## branch diff — Get diffs between branches

```bash
mcp2cli gitlab branch diff --from main --to feature/my-feature
mcp2cli gitlab branch diff --project-id mygroup/myrepo --from main --to develop --straight true
```

Required: `--from`, `--to`

Also supports: `--project-id`, `--straight`, `--excluded-file-patterns`

---

## commit list — List commits

```bash
mcp2cli gitlab commit list --project-id mygroup/myrepo
mcp2cli gitlab commit list --project-id mygroup/myrepo --ref-name main --since "2024-01-01T00:00:00Z" --per-page 50
```

Also supports: `--project-id`, `--ref-name`, `--since`, `--until`, `--path`, `--author`, `--all`, `--with-stats`, `--first-parent`, `--order`, `--trailers`, `--page`, `--per-page`

## commit get — Get a specific commit

```bash
mcp2cli gitlab commit get --sha abc1234def567890
mcp2cli gitlab commit get --project-id mygroup/myrepo --sha abc1234 --stats true
```

Required: `--sha`

Also supports: `--project-id`, `--stats`

## commit diff — Get commit diff

```bash
mcp2cli gitlab commit diff --sha abc1234def567890
mcp2cli gitlab commit diff --project-id mygroup/myrepo --sha abc1234 --full-diff true
```

Required: `--sha`

Also supports: `--project-id`, `--full-diff`

Use `mcp2cli gitlab branch <action> --help` or `mcp2cli gitlab commit <action> --help` for full details.
