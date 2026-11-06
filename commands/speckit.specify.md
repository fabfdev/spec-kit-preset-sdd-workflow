---
description: Create an adaptive feature PRD, resolve scope decisions and record approval in an isolated worktree.
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

## Step 2 — Resolve the feature and existing work

Derive a kebab-case slug from the request. Search the current branch, Kanban and
`git worktree list` for existing work; read the live worktree's record first.
For an explicit continuation, reuse it and preserve state and approved decisions.
Ask only if new-versus-continuation is ambiguous. Never reset an existing record.
Follow project branch conventions; persist the actual branch and worktree path.

For new work, ensure `.worktrees/` is ignored, then create exactly one worktree
under the primary checkout: attach an existing branch without `-b`, or create a
new branch with `-b feature/[slug]`. Use explicit absolute working directories.
If a dirty existing record must move, copy its exact approved content into the
worktree with the file tool; preserve the original until safely committed.

## Step 3 — Scope and draft

Read relevant product rules and architecture sections. Infer small/full from
complexity using the contract; explain the choice in one sentence. Ask only
unanswered decisions about outcomes, boundaries and failure cases. Batch questions
whose answers are independent; persist answers as they arrive.

Write `specs/[slug]/prd.md`: problem, **Size**, RF definitions, AC definitions,
scenarios/errors, business rules, explicit scope boundaries and binding references.
For small work, include its atomic inline tasks, Checks and Final gate now.
For full work, defer technical plan/tasks until after scope approval.

## Step 4 — Validate and approve scope

Run `sdd.py validate [slug] --stage spec` (small: also `--stage tasks`). Repair
structural issues before presenting. Show the reviewable scope and, for small
work, its plan. **Wait for scope approval**, then record the user's words and date.
Save drafts freely; an approval must never be fabricated. A changed approved
outcome requires renewed approval; continuation alone does not.

## Step 5 — Track and commit

Create `docs/kanban/feature-[slug].md` only if absent, with YAML frontmatter:
name, type: feature, status: planned, slug, actual branch, worktree, priority:
medium unless specified, spec: specs/[slug]/, tasks_done: 0, tasks_total, pr,
created, updated. Quote strings that need YAML escaping. Body: `## Notes`.
On continuation update only fields changed by this invocation.

Commit the approved PRD and Kanban together with `docs:`. Small work proceeds to
`analyze`; full work proceeds to `plan`, then `tasks`, then `analyze`.

## Constraints

- Scope approval is a milestone; file writes are reversible drafts.
- Preserve IDs, existing worktree state and approvals when resuming.
- Small work still has explicit criteria, checks and independent final review.
