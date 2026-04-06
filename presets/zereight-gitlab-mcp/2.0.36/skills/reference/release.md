# Release Commands

## create — Create a new release

```bash
mcp2cli gitlab release create --tag-name v1.0.0
mcp2cli gitlab release create --project-id mygroup/myrepo --tag-name v1.0.0 --name "Release 1.0.0" --description "First stable release" --ref main
```

Required: `--tag-name`

Also supports: `--project-id`, `--name`, `--tag-message`, `--description`, `--ref`, `--milestones`, `--assets`, `--released-at`

## list — List releases

```bash
mcp2cli gitlab release list --project-id mygroup/myrepo
mcp2cli gitlab release list --project-id mygroup/myrepo --order-by released_at --sort desc
```

Also supports: `--project-id`, `--order-by` (released_at/created_at), `--sort` (asc/desc), `--include-html-description`, `--page`, `--per-page`

## get — Get a release by tag

```bash
mcp2cli gitlab release get --tag-name v1.0.0
mcp2cli gitlab release get --project-id mygroup/myrepo --tag-name v1.0.0
```

Required: `--tag-name`

Also supports: `--project-id`, `--include-html-description`

## update — Update an existing release

```bash
mcp2cli gitlab release update --tag-name v1.0.0 --name "Release 1.0.1" --description "Bugfix release"
```

Required: `--tag-name`

Also supports: `--project-id`, `--name`, `--description`, `--milestones`, `--released-at`

## delete — Delete a release (tag is preserved)

```bash
mcp2cli gitlab release delete --tag-name v1.0.0
```

Required: `--tag-name`

Also supports: `--project-id`

## evidence — Create release evidence

```bash
mcp2cli gitlab release evidence --tag-name v1.0.0
```

Required: `--tag-name`

Also supports: `--project-id`

## download-asset — Download release asset

```bash
mcp2cli gitlab release download-asset --tag-name v1.0.0 --direct-asset-path /binaries/linux-amd64
```

Also supports: `--project-id`, `--tag-name`

---

## deployment list — List deployments

```bash
mcp2cli gitlab deployment list --project-id mygroup/myrepo
mcp2cli gitlab deployment list --project-id mygroup/myrepo --environment production --status success
```

Also supports: `--project-id`, `--environment`, `--ref`, `--sha`, `--status`, `--updated-after`, `--updated-before`, `--order-by`, `--sort`, `--page`, `--per-page`

## deployment get — Get a deployment

```bash
mcp2cli gitlab deployment get --deployment-id 789
```

Also supports: `--project-id`, `--deployment-id`

---

## environment list — List environments

```bash
mcp2cli gitlab environment list --project-id mygroup/myrepo
mcp2cli gitlab environment list --project-id mygroup/myrepo --states available
```

Also supports: `--project-id`, `--name`, `--search`, `--states` (available/stopped), `--page`, `--per-page`

## environment get — Get an environment

```bash
mcp2cli gitlab environment get --environment-id 123
```

Also supports: `--project-id`, `--environment-id`

Use `mcp2cli gitlab release <action> --help` for full parameter details.
