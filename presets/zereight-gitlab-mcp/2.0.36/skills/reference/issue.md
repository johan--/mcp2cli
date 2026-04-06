# Issue Commands

## create — Create a new issue

```bash
mcp2cli gitlab issue create --title "Fix memory leak"
mcp2cli gitlab issue create --project-id mygroup/myrepo --title "Add login feature" --description "User should be able to login" --labels '["backend","feature"]'
```

Required: `--title`

Also supports: `--project-id`, `--description`, `--assignee-ids`, `--labels`, `--milestone-id`, `--issue-type` (issue/incident/test_case/task), `--weight`

## get — Get issue by IID

```bash
mcp2cli gitlab issue get --issue-iid 123
mcp2cli gitlab issue get --project-id mygroup/myrepo --issue-iid 123
```

Also supports: `--project-id`, `--issue-iid`

## list — List issues

```bash
mcp2cli gitlab issue list --project-id mygroup/myrepo
mcp2cli gitlab issue list --project-id mygroup/myrepo --state opened --scope all --labels '["bug"]'
```

Also supports: `--project-id`, `--state` (opened/closed/all), `--scope` (created_by_me/assigned_to_me/all), `--assignee-id`, `--assignee-username`, `--author-id`, `--author-username`, `--labels`, `--milestone`, `--issue-type`, `--search`, `--created-after`, `--created-before`, `--updated-after`, `--updated-before`, `--page`, `--per-page`

## my — My assigned issues

```bash
mcp2cli gitlab issue my
mcp2cli gitlab issue my --state opened --labels '["urgent"]'
```

Also supports: `--project-id`, `--state`, `--labels`, `--milestone`, `--search`, `--created-after`, `--created-before`, `--updated-after`, `--updated-before`, `--per-page`, `--page`

## update — Update an issue

```bash
mcp2cli gitlab issue update --issue-iid 123 --title "Updated title"
mcp2cli gitlab issue update --project-id mygroup/myrepo --issue-iid 123 --state-event close
```

Also supports: `--project-id`, `--issue-iid`, `--title`, `--description`, `--assignee-ids`, `--labels`, `--milestone-id`, `--state-event` (close/reopen), `--due-date`, `--weight`, `--issue-type`, `--confidential`, `--discussion-locked`

## delete — Delete an issue

```bash
mcp2cli gitlab issue delete --issue-iid 123
```

Also supports: `--project-id`, `--issue-iid`

---

## issue note create — Add a note to an issue

```bash
mcp2cli gitlab issue note create --issue-iid 123 --body "This is a comment"
```

## issue note update — Update an issue note

```bash
mcp2cli gitlab issue note update --issue-iid 123 --note-id 456 --body "Updated comment"
```

## issue discussion list — List discussions on an issue

```bash
mcp2cli gitlab issue discussion list --issue-iid 123
```

---

## issue link create — Create an issue link

```bash
mcp2cli gitlab issue link create --issue-iid 123 --target-issue-iid 456 --link-type "relates_to"
```

Also supports: `--project-id`, `--issue-iid`, `--target-project-id`, `--target-issue-iid`, `--link-type` (relates_to/blocks/is_blocked_by)

## issue link list — List issue links

```bash
mcp2cli gitlab issue link list --issue-iid 123
```

## issue link delete — Delete an issue link

```bash
mcp2cli gitlab issue link delete --issue-iid 123 --issue-link-id 789
```

Use `mcp2cli gitlab issue <action> --help` for full parameter details.
