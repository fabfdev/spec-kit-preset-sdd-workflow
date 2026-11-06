---
description: Incrementally review approved artifacts, persist findings, and correct affected sections until every valid finding is closed.
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

## Step 2 — Scan

Resolve the feature's worktree and slug. Full work requires PRD, techspec and
consolidated tasks; small work requires PRD with inline tasks. Migrate v2 tasks
using `tasks` first. Run `sdd.py scan [slug]`, adding --include for relevant source,
rules, dependency/configuration and binding design files beyond declared inputs.
Use --full for missing confidence or broad impact. The script writes only analysis
metadata; scan itself does not approve semantic correctness.

## Step 3 — Semantic review

Follow the contract's full/delta/unchanged rules. Read only changed sections and
their impacts on a delta; verify all required inputs are accounted for. Check RF
and AC coverage, data/interface consistency, dependency order, test adequacy,
applicable MUST constraints, binding designs and scope. New input dependencies
must be added with --include and rescanned before accepting the result.

Persist a compact cumulative `analysis-review.json` with snapshot, reviewed keys
and all findings. Each finding needs evidence, location and consequence. Address
CRITICAL/HIGH/MEDIUM/LOW alike. Dismiss only false positives or out-of-scope items
with a reason; do not invent extra requirements or report stylistic preferences
as defects. An unchanged valid accepted analysis is reusable.

## Step 4 — Patch and verify

For scope-preserving fixes, edit affected sections automatically and check their
impacts. Preserve stable IDs and prior decisions. If a fix changes approved scope
or architecture, invalidate that approval and ask only the new decision; wait.
After changes run scan again, review the delta and retain closure evidence and
prior finding IDs. Stop incomplete after two unsuccessful automatic correction
rounds, or on a decision blocker. Do not regenerate all documents.

## Step 5 — Accept

Run `sdd.py record-analysis [slug]`; it rejects stale, incomplete or unresolved
reports. Commit corrected artifacts and the cumulative analysis metadata in one
`docs:` commit, then report only new/resolved findings and readiness. Any pending
valid finding blocks implementation. Keep the pending review draft on blockers.

## Constraints

- Analysis may save reports and apply narrow mechanical corrections.
- All valid findings must close; absence of findings is not a guarantee of no bugs.
- Scripts validate structure and freshness; semantic judgement remains required.
