---
description: Resolve remaining PRD decisions in grouped rounds and patch affected sections.
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

## Step 2 — Identify and inspect

Resolve the feature from arguments, current branch or its Kanban record. Require
`specs/[slug]/prd.md`. Operate in its existing worktree with an explicit cwd.
Read the PRD and relevant project constraints; inspect code for facts yourself.
Check testability, error/empty states, business rules, binding sources, scope and
external failure modes. Ask only questions whose answers materially affect work.

## Step 3 — Resolve and persist

Ask all currently independent questions in one round, with recommendations; wait
for the answers before asking dependent questions. Zero questions is valid.
Patch answers into the affected PRD sections immediately. Keep IDs and unrelated
text stable. Require scope approval only for changed outcomes/decisions and record
it truthfully; clear the previous approval while such a change is unapproved.
Mechanical clarifications within approved decisions need no extra commit gate.

## Step 4 — Validate and commit

Run `sdd.py validate [slug] --stage spec`, show the concise diff, and commit the
changed PRD with `docs:` once required scope approval is recorded. Existing analysis
will detect its hash change. Continue to plan/tasks for full work or analyze for
small work; do not regenerate an unchanged plan.

## Constraints

- Find facts in the project; ask the user for unresolved decisions.
- Preserve approved scope unless a new approval changes it.
- Fix affected sections, rather than rewriting the document.
