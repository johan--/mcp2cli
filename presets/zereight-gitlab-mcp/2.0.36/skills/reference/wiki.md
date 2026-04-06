# Wiki Commands

## wiki list — List project wiki pages

```bash
mcp2cli gitlab wiki list --project-id mygroup/myrepo
mcp2cli gitlab wiki list --project-id mygroup/myrepo --with-content true
```

Also supports: `--project-id`, `--with-content`, `--page`, `--per-page`

## wiki get — Get a wiki page

```bash
mcp2cli gitlab wiki get --slug my-page --project-id mygroup/myrepo
```

Required: `--slug`

Also supports: `--project-id`

## wiki create — Create a wiki page

```bash
mcp2cli gitlab wiki create --project-id mygroup/myrepo --title "My Page" --content "# Welcome\nContent here"
```

Required: `--title`, `--content`

Also supports: `--project-id`, `--format`

## wiki update — Update a wiki page

```bash
mcp2cli gitlab wiki update --slug my-page --project-id mygroup/myrepo --content "# Updated\nNew content" --title "Updated Page"
```

Required: `--slug`

Also supports: `--project-id`, `--title`, `--content`, `--format`

## wiki delete — Delete a wiki page

```bash
mcp2cli gitlab wiki delete --slug my-page --project-id mygroup/myrepo
```

Required: `--slug`

Also supports: `--project-id`

---

## group wiki list — List group wiki pages

```bash
mcp2cli gitlab group wiki list --group-id mygroup
```

Also supports: `--group-id`, `--with-content`, `--page`, `--per-page`

## group wiki get — Get a group wiki page

```bash
mcp2cli gitlab group wiki get --slug my-page --group-id mygroup
```

Required: `--slug`

Also supports: `--group-id`

## group wiki create — Create a group wiki page

```bash
mcp2cli gitlab group wiki create --group-id mygroup --title "Group Page" --content "# Welcome"
```

Required: `--title`, `--content`

Also supports: `--group-id`, `--format`

## group wiki update — Update a group wiki page

```bash
mcp2cli gitlab group wiki update --slug my-page --group-id mygroup --content "Updated content"
```

Required: `--slug`

## group wiki delete — Delete a group wiki page

```bash
mcp2cli gitlab group wiki delete --slug my-page --group-id mygroup
```

Required: `--slug`

Use `mcp2cli gitlab wiki <action> --help` or `mcp2cli gitlab group wiki <action> --help` for full details.
