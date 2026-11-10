# Changelog

## 4.1.0

- No more git worktrees: `specify` creates `feature/[slug]` from the updated
  default branch in the main checkout (clean tree required). The other commands
  `git switch` to the feature branch; a branch still held by a legacy worktree is
  worked on in that worktree's path.
- The kanban `worktree:` field is no longer written; existing values are ignored.
- `sdd.py` is always resolved from the current checkout.

## 4.0.0

Lean rebuild from 2.0.0 that keeps the useful parts of 3.0.0 and drops what
made sessions expensive.

Kept from 3.0.0:
- PRD `**Size:** small | full`; small features keep up to 3 tasks inline in `prd.md`.
- RF/AC IDs and one consolidated `tasks.md` with a Checks table (no `N_task.md`).
- One commit per task (code, tests and tracking together), no per-commit prompt.
- `scripts/sdd.py validate` for structure, now also printing the next task.

Changed:
- `implement` runs exactly one task and stops, telling the user to `/clear`.
- `specify` asks its clarifying questions in one round; `clarify` is optional.
- `analyze` is a single read-only pass over the feature's documents and
  `sdd.md`; only CRITICAL/HIGH block. No fingerprints, JSON or fix loop.
- Gates: baseline once, narrow gate per task, full checks once before the PR.
  `sdd.py check` prints `PASS` or only the last 40 lines of a failure.
- Independent review is optional, before the PR, with only the diff and the ACs.
- Each command is self-contained and at most 3 KB (tested).

Removed: `references/workflow.md`, `scan`, `record-analysis`, `ready`, `prove`,
`finish` runtime gates, tree digests, `proofs.json`, `analysis-*.json`,
`execution.json`, `verification.json` and `usage.jsonl`. v3 files left in a
feature folder are ignored. The 4-column v3 Checks table is still accepted.

Requires Python 3.8+ and Spec Kit CLI 0.9.0+.
