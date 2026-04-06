# Milestone Commands

## create — Create a milestone

```bash
mcp2cli gitlab milestone create --title "v2.0 Release"
mcp2cli gitlab milestone create --project-id mygroup/myrepo --title "Q1 Sprint" --due-date "2026-03-31" --start-date "2026-01-01"
```

Required: `--title`

Also supports: `--project-id`, `--description`, `--due-date`, `--start-date`

## list — List milestones

```bash
mcp2cli gitlab milestone list --project-id mygroup/myrepo
mcp2cli gitlab milestone list --project-id mygroup/myrepo --state active
```

Also supports: `--project-id`, `--state` (active/closed), `--iids`, `--title`, `--search`, `--include-ancestors`, `--updated-before`, `--updated-after`, `--page`, `--per-page`

## get — Get a milestone

```bash
mcp2cli gitlab milestone get --milestone-id 42
mcp2cli gitlab milestone get --project-id mygroup/myrepo --milestone-id 42
```

Also supports: `--project-id`, `--milestone-id`

## update — Update a milestone

```bash
mcp2cli gitlab milestone update --milestone-id 42 --title "New Title" --state-event close
```

Also supports: `--project-id`, `--milestone-id`, `--title`, `--description`, `--due-date`, `--start-date`, `--state-event` (close/activate)

## delete — Delete a milestone

```bash
mcp2cli gitlab milestone delete --milestone-id 42
```

Also supports: `--project-id`, `--milestone-id`

## issues — Get issues for a milestone

```bash
mcp2cli gitlab milestone issues --milestone-id 42
```

Also supports: `--project-id`, `--milestone-id`

## mrs — Get MRs for a milestone

```bash
mcp2cli gitlab milestone mrs --milestone-id 42
```

Also supports: `--project-id`, `--milestone-id`

## promote — Promote milestone to group level

```bash
mcp2cli gitlab milestone promote --milestone-id 42
```

Also supports: `--project-id`, `--milestone-id`

## burndown — Get burndown events

```bash
mcp2cli gitlab milestone burndown --milestone-id 42
```

Also supports: `--project-id`, `--milestone-id`

Use `mcp2cli gitlab milestone <action> --help` for full parameter details.
