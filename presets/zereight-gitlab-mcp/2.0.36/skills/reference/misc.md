# Miscellaneous Commands

## event list — List user events

```bash
mcp2cli gitlab event list
mcp2cli gitlab event list --target-type issue --after 2026-01-01 --before 2026-04-01
```

Also supports: `--action`, `--target-type` (epic/issue/merge_request/milestone/note/project/snippet/user), `--before`, `--after`, `--scope`, `--sort` (asc/desc), `--page`, `--per-page`

## event project-events — Get events for a project

```bash
mcp2cli gitlab event project-events --project-id mygroup/myrepo
```

Also supports: `--project-id`, `--action`, `--target-type`, `--before`, `--after`, `--sort`, `--page`, `--per-page`

---

## misc create-note — Create a note on issue or MR

```bash
mcp2cli gitlab misc create-note --noteable-type issue --noteable-iid 123 --body "This is a note"
```

Required: `--noteable-type` (issue/merge_request), `--body`

Also supports: `--project-id`, `--noteable-iid`

## misc upload-markdown — Upload file for markdown

```bash
mcp2cli gitlab misc upload-markdown --project-id mygroup/myrepo --file-path ./diagram.png
```

Required: `--project-id`, `--file-path`

## misc download-attachment — Download an attachment

```bash
mcp2cli gitlab misc download-attachment --project-id mygroup/myrepo --secret abc123def456 --filename diagram.png
```

Required: `--project-id`, `--secret`, `--filename`

Also supports: `--local-path`

Use `mcp2cli gitlab misc <action> --help` or `mcp2cli gitlab event <action> --help` for full details.
