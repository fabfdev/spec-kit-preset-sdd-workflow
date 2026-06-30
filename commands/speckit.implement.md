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

## Step 3 — Update Notion to In Progress (first task only)

Use the Notion MCP to query the database (read `database_id` from `.sdd-notion.json`) for the page where `Slug` = `[feature-slug]`.

If the page `Status` is `Ready`, update it to `In Progress`.

Skip this step if status is already `In Progress`.

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
2. **Commit immediately:**

```bash
git add specs/[feature-slug]/tasks.md
git commit -m "docs: mark task N.0 as done"
```

3. Use the Notion MCP to query the database for the page where `Slug` = `[feature-slug]` and update:
   - `Tasks Done` → K+1 (increment by 1)

**Never leave `tasks.md` modified without committing.**

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

After the PR is created, use the Notion MCP to update the feature page:
- `Status` → `In Review`
- `PR URL` → [URL returned by gh pr create]

## Step 10 — Report and wait for approval

```
Task N.0 committed.
Notion: [feature-slug] — K/N tasks completed. Status updated in Notion.

Next task: N+1.0 — [Title].
Can I proceed?
```

## Constraints

- **Mandatory context:** read `sdd.md` (if exists), `[N]_task.md`, and `techspec.md` before any code
- **Test gate:** tests passing before presenting to user
- **Human gate:** explicit approval before any commit
- **Two commits per task:** 1st commit = code; 2nd commit = `tasks.md`
- **Tracking always committed:** never leave `tasks.md` modified without committing
- **Notion update required:** increment Tasks Done after every task; set Status → In Review and PR URL on last task
- **No automatic advance:** wait for approval before the next task
