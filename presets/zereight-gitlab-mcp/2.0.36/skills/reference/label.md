# Label Commands

## list — List project labels

```bash
mcp2cli gitlab label list --project-id mygroup/myrepo
mcp2cli gitlab label list --project-id mygroup/myrepo --search bug --with-counts true
```

Also supports: `--project-id`, `--with-counts`, `--include-ancestor-groups`, `--search`

## get — Get a label

```bash
mcp2cli gitlab label get --label-id bug --project-id mygroup/myrepo
```

Also supports: `--project-id`, `--label-id`, `--include-ancestor-groups`

## create — Create a label

```bash
mcp2cli gitlab label create --project-id mygroup/myrepo --name "bug" --color "#e11d48"
```

Required: `--name`, `--color`

Also supports: `--project-id`, `--description`, `--priority`

## update — Update a label

```bash
mcp2cli gitlab label update --project-id mygroup/myrepo --label-id bug --new-name "Bug" --color "#dc2626"
```

Also supports: `--project-id`, `--label-id`, `--new-name`, `--color`, `--description`, `--priority`

## delete — Delete a label

```bash
mcp2cli gitlab label delete --project-id mygroup/myrepo --label-id bug
```

Also supports: `--project-id`, `--label-id`

Use `mcp2cli gitlab label <action> --help` for full parameter details.
