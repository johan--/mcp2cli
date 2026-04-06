---
name: zereight-gitlab-mcp
description: Manage GitLab repos, MRs, issues, pipelines, deployments, and releases via CLI. Use when user needs to create/search repos, review/merge MRs, manage issues, or run pipelines.
source_version: "2.0.36"
source_cli_hash: "362ae121"
generated_at: "2026-04-06T04:47:10.508590+00:00"
---

# zereight-gitlab-mcp (via mcp2cli)

Manage GitLab repos, merge requests, issues, pipelines, and releases via CLI.

## Shortcuts

- `mcp2cli gitlab <cmd>`

## Commands

### Repository
| Command | Description | Example | Ref |
|---|---|---|---|
| `gitlab repo search` | Search repos | `mcp2cli gitlab repo search --search my-project` | [ref](reference/repo.md) |
| `gitlab repo create` | Create repo | `mcp2cli gitlab repo create --name my-repo` | [ref](reference/repo.md) |
| `gitlab repo tree` | List files/dirs | | [ref](reference/repo.md) |
| `gitlab repo file get` | Get file contents | `mcp2cli gitlab repo file get --project-id grp/repo --file-path src/main.py` | [ref](reference/repo.md) |
| `gitlab repo file create-or-update` | Create/update file | | [ref](reference/repo.md) |
| `gitlab repo file push` | Push files | | [ref](reference/repo.md) |

### Branch & Commit
| Command | Description | Example | Ref |
|---|---|---|---|
| `gitlab branch create` | Create branch | `mcp2cli gitlab branch create --branch feat/x --ref main` | [ref](reference/branch-commit.md) |
| `gitlab branch diff` | Diff branches | `mcp2cli gitlab branch diff --from main --to feat/x` | [ref](reference/branch-commit.md) |
| `gitlab commit list` | List commits | | [ref](reference/branch-commit.md) |
| `gitlab commit get` | Get commit | `mcp2cli gitlab commit get --sha abc1234` | [ref](reference/branch-commit.md) |
| `gitlab commit diff` | Commit diff | | [ref](reference/branch-commit.md) |

### Merge Request
| Command | Description | Example | Ref |
|---|---|---|---|
| `gitlab mr create` | Create MR | `mcp2cli gitlab mr create --source-branch feat/x --target-branch main --title "Add X"` | [ref](reference/mr.md) |
| `gitlab mr get` | Get MR | `mcp2cli gitlab mr get --merge-request-iid 42` | [ref](reference/mr.md) |
| `gitlab mr list` | List MRs | `mcp2cli gitlab mr list --state opened` | [ref](reference/mr.md) |
| `gitlab mr update` | Update MR | | [ref](reference/mr.md) |
| `gitlab mr merge` | Merge MR | `mcp2cli gitlab mr merge --merge-request-iid 42` | [ref](reference/mr.md) |
| `gitlab mr approve` | Approve MR | | [ref](reference/mr.md) |
| `gitlab mr diff changed-files` | Changed files (review) | | [ref](reference/mr.md) |
| `gitlab mr diff file` | File diff (review) | | [ref](reference/mr.md) |

### Issue
| Command | Description | Example | Ref |
|---|---|---|---|
| `gitlab issue create` | Create issue | `mcp2cli gitlab issue create --title "Fix bug"` | [ref](reference/issue.md) |
| `gitlab issue get` | Get issue | `mcp2cli gitlab issue get --issue-iid 123` | [ref](reference/issue.md) |
| `gitlab issue list` | List issues | `mcp2cli gitlab issue list --state opened --scope all` | [ref](reference/issue.md) |
| `gitlab issue my` | My issues | `mcp2cli gitlab issue my` | [ref](reference/issue.md) |
| `gitlab issue update` | Update issue | | [ref](reference/issue.md) |
| `gitlab issue delete` | Delete issue | | [ref](reference/issue.md) |

### Project & Group
| Command | Description | Example | Ref |
|---|---|---|---|
| `gitlab project get` | Get project | `mcp2cli gitlab project get --project-id grp/repo` | [ref](reference/project.md) |
| `gitlab project list` | List projects | | [ref](reference/project.md) |
| `gitlab project members` | List members | | [ref](reference/project.md) |
| `gitlab group projects` | Group projects | | [ref](reference/project.md) |

### Pipeline
| Command | Description | Example | Ref |
|---|---|---|---|
| `gitlab pipeline create` | Create pipeline | `mcp2cli gitlab pipeline create --ref main` | [ref](reference/pipeline.md) |
| `gitlab pipeline list` | List pipelines | | [ref](reference/pipeline.md) |
| `gitlab pipeline get` | Get pipeline | | [ref](reference/pipeline.md) |
| `gitlab pipeline retry` | Retry pipeline | | [ref](reference/pipeline.md) |
| `gitlab pipeline cancel` | Cancel pipeline | | [ref](reference/pipeline.md) |
| `gitlab pipeline job list` | List jobs | | [ref](reference/pipeline.md) |
| `gitlab pipeline job output` | Job output log | | [ref](reference/pipeline.md) |

### Release & Milestone
| Command | Description | Example | Ref |
|---|---|---|---|
| `gitlab release create` | Create release | `mcp2cli gitlab release create --tag-name v1.0.0` | [ref](reference/release.md) |
| `gitlab release list` | List releases | | [ref](reference/release.md) |
| `gitlab release get` | Get release | | [ref](reference/release.md) |
| `gitlab milestone create` | Create milestone | | [ref](reference/milestone.md) |
| `gitlab milestone list` | List milestones | | [ref](reference/milestone.md) |

## Discover Parameters

    mcp2cli gitlab mr create --help

> Ref links → detailed params. Also: [wiki](reference/wiki.md), [label](reference/label.md), [mr-notes](reference/mr-notes.md), [misc](reference/misc.md)

## User Notes

> **MUST READ** [users/SKILL.md](users/SKILL.md) for custom workflows and tips.
> See [users/workflows.md](users/workflows.md) for multi-step workflow examples.
> Not overwritten by updates.
