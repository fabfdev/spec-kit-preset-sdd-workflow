---
description: Implement one task at a time. Runs tests before presenting to the user. Requires explicit validation before committing. Two commits per task — code first, tracking files second.
---

## User Input

```text
$ARGUMENTS
```

## Step 1 — Identify the task

If not specified in `$ARGUMENTS`, ask:
- Which feature (directory slug under `docs/tasks/`)
- Which task number

Target file: `docs/tasks/[feature]/[N]_task.md`

## Step 2 — Load mandatory context

Read before writing any code:
1. `docs/tasks/[feature]/[N]_task.md` — requirements, subtasks, acceptance criteria
2. `docs/tasks/[feature]/techspec.md` — technical decisions for the feature
3. `docs/core/sdd.md` — base architecture, conventions, project structure (if it exists)

**Do not skip this step.** The `sdd.md` contains critical naming conventions, import patterns, and structural rules.

## Step 3 — Update roadmap to `in_progress` (first task only)

If the feature status in `docs/core/roadmap.md` is `ready`, update it to `in_progress`.

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

Commit **only the code files** — do not include `tasks.md` or `roadmap.md`:

```bash
git add [task code files]
git commit -m "feat: [concise description]"
```

Use the appropriate conventional prefix (`feat:`, `fix:`, `refactor:`, etc.).

## Step 8 — Update tracking and commit separately

1. Mark `- [x]` for the task in `docs/tasks/[feature]/tasks.md`
2. Increment the counter in `docs/core/roadmap.md`
3. If this is the last task, update the status to `completed`
4. **Commit immediately:**

```bash
git add docs/tasks/[feature]/tasks.md docs/core/roadmap.md
git commit -m "docs: mark task N.0 as done and update roadmap to (K+1)/N"
```

**Never leave `tasks.md` or `roadmap.md` modified without committing.**

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

## Step 10 — Report and wait for approval

```
Task N.0 committed.
Roadmap: [Feature] — K/N tasks completed.

Next task: N+1.0 — [Title].
Can I proceed?
```

## Constraints

- **Mandatory context:** read `sdd.md` (if exists), `[N]_task.md`, and `techspec.md` before any code
- **Test gate:** tests passing before presenting to user
- **Human gate:** explicit approval before any commit
- **Two commits per task:** 1st commit = code; 2nd commit = `tasks.md` + `roadmap.md`
- **Tracking always committed:** never leave `tasks.md` or `roadmap.md` modified without committing
- **No automatic advance:** wait for approval before the next task
