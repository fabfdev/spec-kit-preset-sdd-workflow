---
description: Implement one task at a time. Runs tests before presenting to the user. Requires explicit validation before committing. Two commits per task — code first, tracking files second.
---

## User Input

```text
$ARGUMENTS
```

## Step 1 — Identify the task

If not specified in `$ARGUMENTS`, check the current git branch name for `feature/[slug]` and infer the feature from it. Then ask which task number to implement.

Target file: `specs/[feature-slug]/[N]_task.md`

## Step 2 — Load mandatory context

Read before writing any code:
1. `specs/[feature-slug]/[N]_task.md` — requirements, subtasks, acceptance criteria
2. `specs/[feature-slug]/techspec.md` — technical decisions for the feature
3. `docs/core/sdd.md` — base architecture, conventions, project structure (if it exists)

**Do not skip this step.** The `sdd.md` contains critical naming conventions, import patterns, and structural rules.

## Step 3 — Mark the kanban entry In Progress (first task only)

In `docs/kanban/feature-[feature-slug].md` frontmatter: if `status` is `ready`, set it to `in-progress` and bump `updated:` to today.

Skip this step if `status` is already `in-progress`. Commit this change together with the tracking commit in Step 8.

## Step 4 — Implement the task

Follow the requirements and subtasks from `[N]_task.md`. For each subtask:
1. Implement the code
2. Mark `- [x]` in `[N]_task.md` (real-time progress)

Follow conventions from `docs/core/sdd.md` if it exists.

## Step 5 — Test gate

After implementing all subtasks, run the project's tests.

Identify the test framework in use (check `package.json`, `pyproject.toml`, or config files) and run:
- Unit tests
- Integration tests (if applicable)
- Typecheck and lint (if configured)

**If any test fails:** fix it before proceeding. Never present code with failing tests.

## Step 6 — Present for user validation

```
Task N.0 implemented. Here is what was done:

[Summary of modified files and resulting behavior]

Tests: ✓ passing

Can you validate so I can commit?
```

**Wait for explicit validation. Do not commit without approval.**

## Step 7 — Implementation commit (after approval)

Commit **only the code files** — do not include `tasks.md`:

```bash
git add [task code files]
git commit -m "feat: [concise description]"
```

Use the appropriate conventional prefix (`feat:`, `fix:`, `refactor:`, etc.).

## Step 8 — Update tracking and commit separately

1. Mark `- [x]` for the task in `specs/[feature-slug]/tasks.md`
2. In `docs/kanban/feature-[feature-slug].md` frontmatter: set `tasks_done:` to K+1, bump `updated:` to today, and apply the Step 3 `status: in-progress` change if it hasn't been committed yet.
3. **Commit immediately:**

```bash
git add specs/[feature-slug]/tasks.md docs/kanban/feature-[feature-slug].md
git commit -m "docs: mark task N.0 as done"
```

**Never leave `tasks.md` or the kanban entry modified without committing.**

## Step 9 — Create PR (last task only)

If this is the last task of the feature:

```bash
gh pr create \
  --title "feat: [feature name]" \
  --body "## What was implemented
[Description]

## How to test
[Steps to validate manually]"
```

After the PR is created, in `docs/kanban/feature-[feature-slug].md` frontmatter set:
- `status: in-review`
- `pr:` [URL returned by gh pr create]
- `updated:` today

Commit it:

```bash
git add docs/kanban/feature-[feature-slug].md
git commit -m "docs: [feature-slug] in review"
```

## Step 10 — Report and wait for approval

```
Task N.0 committed.
Kanban: [feature-slug] — K/N tasks completed. docs/kanban/feature-[feature-slug].md updated.

Next task: N+1.0 — [Title].
Can I proceed?
```

## Constraints

- **Mandatory context:** read `sdd.md` (if exists), `[N]_task.md`, and `techspec.md` before any code
- **Test gate:** tests passing before presenting to user
- **Human gate:** explicit approval before any commit
- **Two commits per task:** 1st commit = code; 2nd commit = `tasks.md` + kanban entry
- **Tracking always committed:** never leave `tasks.md` or the kanban entry modified without committing
- **Kanban update required:** bump `tasks_done` after every task; set `status: in-review` and `pr:` on the last task
- **No automatic advance:** wait for approval before the next task
