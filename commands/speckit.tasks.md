---
description: Create one consolidated task plan with requirement traceability, executable gates and joint technical approval.
handoffs:
  - label: Analyze artifacts
    agent: speckit.analyze
    prompt: Analyze this approved plan before implementation.
---

## User Input

```text
$ARGUMENTS
```

## Step 1 — Load the execution contract

Resolve `.specify/presets/sdd-workflow/` in this checkout or the primary checkout
from `git worktree list`. Read `references/workflow.md` there (once per session;
reload after compaction/update). It defines formats, approvals, incremental review,
proofs and delivery. Use its `scripts/sdd.py` with `--root [active-worktree]`.
Read applicable project rules and only context relevant to this command.

## Step 2 — Resolve inputs

Use the feature's existing worktree and approved PRD. For full work require
`techspec.md`; for small work keep the plan in `prd.md`. Read affected interfaces,
test configuration and a representative existing test to discover conventions.

For existing v2 work, migrate `tasks.md` and each `N_task.md` into the consolidated
format in place: preserve task identities in titles/legacy references, subtasks,
acceptance criteria, completed state and relevant notes. Add stable T/AC IDs and
traceability. Preserve originals until the migration diff is checked and approved;
then archive/remove only files whose content was completely carried forward.
Never rerun completed implementation. Ask about missing behavior, not formatting.

## Step 3 — Build the task plan

Use the exact contract format: one ## Tn section per atomic deliverable, Status,
Requirements, Criteria, Depends on, Files and Gate; a Checks table with exactly one
row per criterion, plus Final gate and relevant technical references.
Put implementation and its meaningful tests together. Discover real commands from
project configuration/CI; choose narrow task gates and complete required final
checks. Capture dependencies explicitly; order by dependencies rather than a
blanket backend-before-frontend rule. No arbitrary maximum task count.

Full work uses only `tasks.md`; small work embeds these sections in `prd.md` and
promotes to full above three tasks or with architectural uncertainty. Include a
short context Inputs list for additional files to pass to analyze with --include.

## Step 4 — Validate and approve

Run `sdd.py validate [slug] --stage tasks`. Fix structural issues, then present
scope-preserving technical decisions, task breakdown and verification commands.
**Wait for approval of the technical plan and tasks together.** Record the actual
approval line; existing unchanged approval remains valid during mechanical fixes.
For small work already approved with its PRD, no second approval is needed.

## Step 5 — Commit and analyze

Recompute Kanban tasks_total and tasks_done from Status fields, set `ready` only
when implementation has not already started, preserve other state. Commit the
technical plan, consolidated tasks and tracking together with `docs:`. Run
`analyze` next; implementation requires its accepted result.

## Constraints

- One source of task truth; counters are derived, never blindly incremented.
- Every criterion has an executable check and an outcome the reviewer can judge.
- Approval authorizes sequential local implementation and commits.
