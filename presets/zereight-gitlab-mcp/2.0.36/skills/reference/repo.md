# Repository Commands

## search — Search for GitLab projects

```bash
mcp2cli gitlab repo search --search my-project
mcp2cli gitlab repo search --search "backend service" --per-page 50
```

Also supports: `--page`, `--per-page`

## create — Create a new repository

```bash
mcp2cli gitlab repo create --name my-repo
mcp2cli gitlab repo create --name my-repo --description "My new project" --visibility private
```

Also supports: `--description`, `--visibility` (private/internal/public), `--initialize-with-readme`

## fork — Fork a repository

```bash
mcp2cli gitlab repo fork --project-id mygroup/myrepo
mcp2cli gitlab repo fork --project-id mygroup/myrepo --namespace my-namespace
```

Also supports: `--namespace`

## tree — Get repository file tree

```bash
mcp2cli gitlab repo tree --project-id mygroup/myrepo
mcp2cli gitlab repo tree --project-id mygroup/myrepo --path src/ --ref main --recursive true
```

Also supports: `--path`, `--ref`, `--recursive`, `--per-page`, `--page-token`, `--pagination`

## file get — Get file contents

```bash
mcp2cli gitlab repo file get --project-id mygroup/myrepo --file-path src/main.py
mcp2cli gitlab repo file get --project-id mygroup/myrepo --file-path README.md --ref develop
```

Also supports: `--ref`

## file create-or-update — Create or update a file

```bash
mcp2cli gitlab repo file create-or-update --project-id mygroup/myrepo --file-path src/new.py --content "print('hello')" --commit-message "Add new file" --branch main
```

Required: `--file-path`, `--content`, `--commit-message`, `--branch`

Also supports: `--project-id`, `--previous-path`, `--last-commit-id`, `--commit-id`

## file push — Push multiple files

```bash
mcp2cli gitlab repo file push --project-id mygroup/myrepo --branch main --files '[{"file_path":"a.txt","content":"hello"}]' --commit-message "Add files"
```

Required: `--branch`, `--files`, `--commit-message`

Also supports: `--project-id`

Use `mcp2cli gitlab repo <action> --help` for full parameter details.
