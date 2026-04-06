# MR Notes, Discussions & Draft Notes

## mr note create — Add a note to a MR

```bash
mcp2cli gitlab mr note create --merge-request-iid 42 --body "LGTM!"
```

Required: `--body`

Also supports: `--project-id`, `--merge-request-iid`

## mr note list — List notes on a MR

```bash
mcp2cli gitlab mr note list --merge-request-iid 42
```

Also supports: `--project-id`, `--merge-request-iid`, `--sort`, `--order-by`, `--per-page`, `--page`

## mr note get — Get a specific note

```bash
mcp2cli gitlab mr note get --merge-request-iid 42 --note-id 123
```

## mr note update — Update a note

```bash
mcp2cli gitlab mr note update --merge-request-iid 42 --note-id 123 --body "Updated comment"
```

Required: `--body`

## mr note delete — Delete a note

```bash
mcp2cli gitlab mr note delete --merge-request-iid 42 --note-id 123
```

---

## mr discussion list — List discussions on a MR

```bash
mcp2cli gitlab mr discussion list --merge-request-iid 42
```

Also supports: `--project-id`, `--merge-request-iid`, `--page`, `--per-page`

## mr discussion create-thread — Create a discussion thread

```bash
mcp2cli gitlab mr discussion create-thread --merge-request-iid 42 --body "Please fix this"
```

Required: `--body`

Also supports: `--project-id`, `--merge-request-iid`, `--position`, `--created-at`

## mr discussion resolve-thread — Resolve a thread

```bash
mcp2cli gitlab mr discussion resolve-thread --merge-request-iid 42 --discussion-id abc123 --resolved true
```

Also supports: `--project-id`, `--merge-request-iid`, `--discussion-id`, `--resolved`

## mr discussion add-note — Add note to a discussion

```bash
mcp2cli gitlab mr discussion add-note --merge-request-iid 42 --discussion-id abc123 --body "Follow-up comment"
```

Required: `--body`

## mr discussion update-note — Update a discussion note

```bash
mcp2cli gitlab mr discussion update-note --merge-request-iid 42 --discussion-id abc123 --note-id 456 --body "Updated"
```

## mr discussion delete-note — Delete a discussion note

```bash
mcp2cli gitlab mr discussion delete-note --merge-request-iid 42 --discussion-id abc123 --note-id 456
```

---

## mr draft-note create — Create a draft note

```bash
mcp2cli gitlab mr draft-note create --merge-request-iid 42 --body "Draft comment"
```

Required: `--body`

Also supports: `--project-id`, `--merge-request-iid`, `--in-reply-to-discussion-id`, `--position`, `--resolve-discussion`

## mr draft-note list — List draft notes

```bash
mcp2cli gitlab mr draft-note list --merge-request-iid 42
```

## mr draft-note publish — Publish a draft note

```bash
mcp2cli gitlab mr draft-note publish --merge-request-iid 42 --draft-note-id 789
```

## mr draft-note bulk-publish — Publish all draft notes

```bash
mcp2cli gitlab mr draft-note bulk-publish --merge-request-iid 42
```

Use `mcp2cli gitlab mr <action> --help` for full parameter details.
