---
description: Implement exactly one task of an approved plan, pass its gate, commit code, tests and tracking together, then stop so the user can /clear.
---

## User Input

```text
$ARGUMENTS
```

## Step 1 — Pick the task

Slug from `$ARGUMENTS` or the current `feature/[slug]` branch; work in its worktree. `SDD` = `python3 .specify/presets/sdd-workflow/scripts/sdd.py` (same path in the primary checkout if absent). Run `SDD validate [slug]`: it requires recorded approvals and prints the next task. Use the task in `$ARGUMENTS` if given.

Legacy plan with `N_task.md` files: implement from that file, run the project's tests directly instead of `SDD check`, and tick it in `tasks.md`.

## Step 2 — Load only what this task needs

Read the task section, the PRD criteria it cites, the techspec sections it touches and relevant conventions in `docs/core/sdd.md`. Open the task's Files and their direct collaborators. Do not reread whole documents you do not need.

## Step 3 — Baseline (first task only)

If no task is done yet: run `SDD check [slug] --baseline`. Report failures that existed before your change; do not fix unrelated code. Set kanban `status: in-progress`.

## Step 4 — Implement and gate

Implement the code and its tests. Run `SDD check [slug] --task Tn`. Fix and re-run; after 2 failed fix attempts, stop and report the failing output instead of looping.

## Step 5 — Commit

Set the task's `**Status:** done`. In `docs/kanban/feature-[slug].md` set `tasks_done` to the number of done tasks and `updated:`. One commit with explicit paths:

```bash
git add [code and test files] specs/[slug]/ docs/kanban/feature-[slug].md
git commit -m "feat: [concise description]"
```

## Step 6 — Last task only

Run `SDD check [slug] --final`. Ask whether the user wants an independent review; if yes, give one fresh subagent only `git diff [default-branch]...HEAD` and the PRD ACs, and fix valid findings. Write a PR body file, then:

```bash
git push -u origin feature/[slug]
gh pr create --title "feat: [feature]" --body-file [body-file]
```

Set kanban `status: in-review`, `pr: [url]`, commit `docs: [slug] in review` and push.

## Step 7 — Stop

Report the task, files and gate result, then: "Task Tn committed (K/N). Run `/clear`, then `/speckit.implement [slug]`." **Never start the next task in this session.**

## Constraints

- One task per invocation; test gate must pass before commit.
- Stay inside the task's scope; scope changes need the user.
