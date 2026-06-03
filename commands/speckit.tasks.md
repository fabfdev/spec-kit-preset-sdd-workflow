---
description: Break down a feature's PRD and techspec into implementation tasks. Requires approval of the high-level task list before generating any files.
handoffs:
  - label: Analyze artifacts first
    agent: speckit.analyze
    prompt: Analyze consistency between PRD, techspec, and tasks for this feature.
  - label: Implement Tasks
    agent: speckit.implement
    prompt: Implement task 1.
---

## User Input

```text
$ARGUMENTS
```

## Step 1 — Identify the feature

If not specified in `$ARGUMENTS`, check the current git branch name for `feature/NNN-[slug]` and infer from it. If still unclear, ask the user.

Verify that both files exist before proceeding:
- `specs/NNN-[feature-slug]/prd.md`
- `specs/NNN-[feature-slug]/techspec.md`

## Step 1.5 — Switch to the feature branch

```bash
git checkout feature/NNN-[feature-slug]
```

## Step 2 — Analyze PRD and techspec

Read both files and extract: requirements, main components, technical decisions, dependencies between parts.

## Step 3 — Present high-level task list for approval

**Required before generating any file.**

Present the proposed task list in this format:

```
## Proposed tasks for NNN-[feature-slug]

- [ ] 1.0 Task title
- [ ] 2.0 Task title
- [ ] 3.0 Task title

Do you approve this structure before I generate the individual files?
```

**Wait for explicit confirmation before proceeding.**

## Step 4 — Generate task files

After approval:

1. Create `specs/NNN-[feature-slug]/tasks.md` with the approved list
2. For each main task, create `specs/NNN-[feature-slug]/[N]_task.md` with this structure:

```markdown
# Task N.0 — [Title]

## Objective
[What this task accomplishes.]

## Subtasks
- [ ] N.1 [Subtask]
- [ ] N.2 [Subtask]
- [ ] N.3 Write tests for [scope]

## Acceptance Criteria
- [ ] [Verifiable criterion]
- [ ] [Verifiable criterion]

## Technical References
- Techspec section: [relevant section]
- Files to modify: [list]
```

## Step 5 — Update roadmap

After generating all files:

Update `docs/core/roadmap.md`: change status `specced` → `ready` and set task count `0/N`.

## Step 6 — Commit

```bash
git add specs/NNN-[feature-slug]/tasks.md specs/NNN-[feature-slug]/*_task.md docs/core/roadmap.md
git commit -m "docs: add tasks for NNN-[feature-slug]"
```

## Constraints

- **High-level list first** — never generate files without explicit approval
- **Maximum 10 tasks** — group logically
- **Do not write code** — only specify tasks and criteria
- **Logical order:** backend before frontend; both before E2E tests
- **Tests required:** each task must have test subtasks
- **Branch required** — checkout `feature/NNN-[feature-slug]` before generating any file
- **Commit required** — commit all task files + `roadmap.md` with `docs:` prefix
