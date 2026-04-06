# Merge Request Commands

## create — Create a new merge request

```bash
mcp2cli gitlab mr create --source-branch feature/foo --target-branch main --title "Add new feature"
mcp2cli gitlab mr create --project-id mygroup/myrepo --source-branch feature/foo --target-branch main --title "Fix bug" --description "Fixes #123" --draft true
```

Required: `--title`, `--source-branch`, `--target-branch`

Also supports: `--project-id`, `--description`, `--target-project-id`, `--assignee-ids`, `--reviewer-ids`, `--labels`, `--draft`, `--allow-collaboration`, `--remove-source-branch`, `--squash`

## get — Get a merge request

```bash
mcp2cli gitlab mr get --merge-request-iid 42
mcp2cli gitlab mr get --project-id mygroup/myrepo --merge-request-iid 42
```

Also supports: `--project-id`, `--merge-request-iid`, `--source-branch`

## list — List merge requests

```bash
mcp2cli gitlab mr list
mcp2cli gitlab mr list --project-id mygroup/myrepo --state opened
mcp2cli gitlab mr list --assignee-username john --state opened --scope all
```

Also supports: `--project-id`, `--state` (opened/closed/locked/merged/all), `--scope` (created_by_me/assigned_to_me/all), `--assignee-id`, `--assignee-username`, `--author-id`, `--author-username`, `--reviewer-id`, `--reviewer-username`, `--labels`, `--milestone`, `--source-branch`, `--target-branch`, `--search`, `--order-by`, `--sort`, `--page`, `--per-page`

## update — Update a merge request

```bash
mcp2cli gitlab mr update --merge-request-iid 42 --title "Updated title"
mcp2cli gitlab mr update --project-id mygroup/myrepo --merge-request-iid 42 --state-event close
```

Also supports: `--project-id`, `--merge-request-iid`, `--source-branch`, `--title`, `--description`, `--target-branch`, `--assignee-ids`, `--reviewer-ids`, `--labels`, `--state-event` (close/reopen), `--remove-source-branch`, `--squash`, `--draft`

## merge — Merge a merge request

```bash
mcp2cli gitlab mr merge --merge-request-iid 42
mcp2cli gitlab mr merge --project-id mygroup/myrepo --merge-request-iid 42 --squash true --should-remove-source-branch true
```

Also supports: `--project-id`, `--merge-request-iid`, `--auto-merge`, `--merge-commit-message`, `--merge-when-pipeline-succeeds`, `--should-remove-source-branch`, `--squash`, `--squash-commit-message`

## approve — Approve a merge request

```bash
mcp2cli gitlab mr approve --merge-request-iid 42
```

Also supports: `--project-id`, `--merge-request-iid`, `--sha`, `--approval-password`

## unapprove — Unapprove a merge request

```bash
mcp2cli gitlab mr unapprove --merge-request-iid 42
```

Also supports: `--project-id`, `--merge-request-iid`

## approval-state — Get approval state

```bash
mcp2cli gitlab mr approval-state --merge-request-iid 42
```

Also supports: `--project-id`, `--merge-request-iid`

## conflicts — Get MR conflicts

```bash
mcp2cli gitlab mr conflicts --merge-request-iid 42
```

---

## Code Review Workflow

### diff changed-files — List changed files (step 1)

```bash
mcp2cli gitlab mr diff changed-files --merge-request-iid 42
mcp2cli gitlab mr diff changed-files --project-id mygroup/myrepo --merge-request-iid 42
```

Also supports: `--source-branch`, `--excluded-file-patterns`

### diff file — Get file diff (step 2)

```bash
mcp2cli gitlab mr diff file --merge-request-iid 42 --file-paths '["src/api/users.ts","src/model/user.go"]'
```

Required: `--file-paths`

Also supports: `--project-id`, `--merge-request-iid`, `--source-branch`, `--unidiff`

### diff get — Get all diffs

```bash
mcp2cli gitlab mr diff get --merge-request-iid 42
```

Also supports: `--project-id`, `--merge-request-iid`, `--source-branch`, `--view` (inline/parallel), `--excluded-file-patterns`

### diff list — List diffs with pagination

```bash
mcp2cli gitlab mr diff list --merge-request-iid 42 --page 1 --per-page 20
```

Also supports: `--project-id`, `--merge-request-iid`, `--source-branch`, `--page`, `--per-page`, `--unidiff`

Use `mcp2cli gitlab mr <action> --help` for full parameter details.
