# Pipeline Commands

## create — Create a pipeline

```bash
mcp2cli gitlab pipeline create --ref main
mcp2cli gitlab pipeline create --project-id mygroup/myrepo --ref feature/foo --variables '[{"key":"ENV","value":"staging"}]'
```

Required: `--ref`

Also supports: `--project-id`, `--variables`, `--inputs`

## list — List pipelines

```bash
mcp2cli gitlab pipeline list --project-id mygroup/myrepo
mcp2cli gitlab pipeline list --project-id mygroup/myrepo --status failed --ref main
```

Also supports: `--project-id`, `--scope` (running/pending/finished/branches/tags), `--status`, `--ref`, `--sha`, `--yaml-errors`, `--username`, `--updated-after`, `--updated-before`, `--order-by`, `--sort`, `--page`, `--per-page`

## get — Get pipeline details

```bash
mcp2cli gitlab pipeline get --pipeline-id 12345
mcp2cli gitlab pipeline get --project-id mygroup/myrepo --pipeline-id 12345
```

Also supports: `--project-id`, `--pipeline-id`

## retry — Retry a failed pipeline

```bash
mcp2cli gitlab pipeline retry --pipeline-id 12345
```

Also supports: `--project-id`, `--pipeline-id`

## cancel — Cancel a running pipeline

```bash
mcp2cli gitlab pipeline cancel --pipeline-id 12345
```

Also supports: `--project-id`, `--pipeline-id`

---

## pipeline job list — List jobs in a pipeline

```bash
mcp2cli gitlab pipeline job list --pipeline-id 12345
```

Also supports: `--project-id`, `--pipeline-id`, `--scope`

## pipeline job list-triggers — List trigger jobs

```bash
mcp2cli gitlab pipeline job list-triggers --pipeline-id 12345
```

## pipeline job get — Get a specific job

```bash
mcp2cli gitlab pipeline job get --job-id 67890
```

Also supports: `--project-id`, `--job-id`

## pipeline job output — Get job output log

```bash
mcp2cli gitlab pipeline job output --job-id 67890
```

Also supports: `--project-id`, `--job-id`

## pipeline job play — Play a manual job

```bash
mcp2cli gitlab pipeline job play --job-id 67890
```

Also supports: `--project-id`, `--job-id`, `--job-variables-attributes`

## pipeline job retry — Retry a failed job

```bash
mcp2cli gitlab pipeline job retry --job-id 67890
```

## pipeline job cancel — Cancel a running job

```bash
mcp2cli gitlab pipeline job cancel --job-id 67890
```

Also supports: `--project-id`, `--job-id`, `--force`

---

## pipeline artifact list — List job artifacts

```bash
mcp2cli gitlab pipeline artifact list --job-id 67890
mcp2cli gitlab pipeline artifact list --job-id 67890 --path reports/ --recursive true
```

Also supports: `--project-id`, `--job-id`, `--path`, `--recursive`

## pipeline artifact download — Download artifact archive

```bash
mcp2cli gitlab pipeline artifact download --job-id 67890 --local-path ./artifacts
```

Also supports: `--project-id`, `--job-id`, `--local-path`

## pipeline artifact get-file — Get a specific artifact file

```bash
mcp2cli gitlab pipeline artifact get-file --job-id 67890 --artifact-path reports/coverage.xml
```

Required: `--artifact-path`

Also supports: `--project-id`, `--job-id`

Use `mcp2cli gitlab pipeline <action> --help` for full parameter details.
