# Project, Group & Namespace Commands

## project get — Get project details

```bash
mcp2cli gitlab project get --project-id mygroup/myrepo
mcp2cli gitlab project get --project-id 12345
```

Also supports: `--project-id`

## project list — List accessible projects

```bash
mcp2cli gitlab project list
mcp2cli gitlab project list --search my-project --owned true --membership true
```

Also supports: `--search`, `--search-namespaces`, `--owned`, `--membership`, `--simple`, `--archived`, `--visibility` (public/internal/private), `--order-by`, `--sort`, `--with-issues-enabled`, `--with-merge-requests-enabled`, `--min-access-level`, `--page`, `--per-page`

## project members — List project members

```bash
mcp2cli gitlab project members --project-id mygroup/myrepo
mcp2cli gitlab project members --project-id mygroup/myrepo --query "john" --include-inheritance true
```

Required: `--project-id`

Also supports: `--query`, `--user-ids`, `--skip-users`, `--include-inheritance`, `--per-page`, `--page`

---

## group projects — List projects in a group

```bash
mcp2cli gitlab group projects --group-id mygroup
mcp2cli gitlab group projects --group-id mygroup --include-subgroups true --search backend
```

Also supports: `--group-id`, `--include-subgroups`, `--search`, `--page`, `--per-page`

## group iterations — List group iterations

```bash
mcp2cli gitlab group iterations --group-id mygroup
mcp2cli gitlab group iterations --group-id mygroup --state current
```

Also supports: `--group-id`, `--state` (opened/upcoming/current/closed/all), `--search`, `--include-ancestors`, `--include-descendants`, `--updated-before`, `--updated-after`, `--page`, `--per-page`

---

## namespace list — List accessible namespaces

```bash
mcp2cli gitlab namespace list
```

## namespace get — Get a namespace

```bash
mcp2cli gitlab namespace get --namespace-id mygroup
```

## namespace verify — Verify a namespace exists

```bash
mcp2cli gitlab namespace verify --namespace-id mygroup
```

---

## user list — List GitLab users

```bash
mcp2cli gitlab user list
```

Use `mcp2cli gitlab project <action> --help` or `mcp2cli gitlab group <action> --help` for full parameter details.
