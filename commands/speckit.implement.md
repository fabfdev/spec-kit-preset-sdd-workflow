---
description: Execute approved tasks continuously with one atomic commit per task and one independent final review.
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

## Step 2 — Start or resume

Resolve the existing feature worktree and slug. Read the approved PRD and current
task document (tasks.md for full; PRD for small), relevant techspec/SDD sections and
applicable project rules. Reconcile Git, task statuses and Handoff; skip done tasks.
Migrate legacy N_task.md through tasks first. Respect an explicitly requested task
range; otherwise execute all remaining tasks sequentially.

Before the first code edit run `sdd.py ready [slug]` and project baseline checks.
On resumption keep a valid execution.json plan; if definitions changed, analyze
and run ready again before continuing. A changed decision needs fresh approval.
Set Kanban to `in-progress`; preserve other state and existing PR metadata.

## Step 3 — Implement, gate and commit each task

Follow the contract's Execute cycle. Read the current task and impacted contracts,
state approach briefly, implement the code and outcome-based tests, then run
`sdd.py gate [slug] --task Tn`. Fix failures before proceeding. Mark Status done,
recompute counters and commit implementation, tests and tracking together with a
Conventional Commit. Use explicit file paths. Continue to the next available task
without another permission question. Stop on scope decisions or unresolved checks.

## Step 4 — Verify the completed feature

Run required user journeys/visual checks and `sdd.py prove [slug]`. Dispatch one
fresh independent reviewer with the bounded context defined in the contract;
record its actual identity and per-AC evidence in verification.json. Fix all valid
findings, commit the fixes, rerun affected proofs and verify the corrections and
impacts. Keep the reviewer findings and annotate closures with commits/evidence.
Run `sdd.py finish [slug]`. Failures keep the feature incomplete; report remaining
blockers instead of starting another full audit loop.

## Step 5 — Deliver

Commit the review/proof records and report behavior, checks and reviewer outcome.
If push/PR delivery is authorized in this session, push first, reuse/create a PR
with --body-file, then save in-review + URL, commit the metadata and push again.
Otherwise leave a verified local result and request only missing remote authority.
Human merge/cleanup uses the extension's finish command. Record phase usage and
interventions when available; use null for unavailable token counts.

## Constraints

- Scope and plan approval replace per-task commit/advance prompts.
- One task commit includes code, tests and tracking; metadata-only delivery commits
  are allowed for final evidence and PR linkage.
- One independent review per completed feature; all valid findings must close.
