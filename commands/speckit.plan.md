---
description: Draft technical decisions for full work; resolve only new decisions before task-plan approval.
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

## Step 2 — Identify the feature

Resolve slug and actual branch from arguments/current worktree/Kanban. Require an
approved `prd.md`. Work in the associated worktree; never check out a branch held
elsewhere. For small work with no architectural uncertainty, keep decisions inline
and proceed to analyze; promote to full if exploration changes that assessment.

## Step 3 — Investigate and draft

Read the PRD, relevant SDD sections and affected interfaces/source. Discover test
commands from manifests and CI. Research current primary library documentation
only when a new/uncertain API or decision requires it; reuse confirmed context.
Ask only unresolved technical decisions. Write `techspec.md` with affected modules,
requirement IDs, interfaces, data changes, failure modes, dependencies and testing
strategy. Omit irrelevant sections. Retain binding source/design references.

When invoked to fix analysis findings, patch the named sections and impacted
contracts; preserve other decisions. An approved decision change invalidates task
approval and requires new approval. Do not rerun the whole interview.

## Step 4 — Save and continue

Save the technical draft, set Kanban status to `specced` without resetting counters
or PR data, and continue to `tasks`. **Technical decisions and tasks are approved
together there.** Commit the plan with that milestone rather than introducing a
separate approval and commit here.

## Constraints

- Respect applicable project architecture constraints and binding designs.
- Use relevant context and narrow corrections; avoid redundant research.
- Implementation waits for approved scope and the consolidated plan.
