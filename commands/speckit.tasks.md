---
description: Break an approved PRD (and techspec) into one consolidated task plan with RF/AC traceability and executable gates. Approval before saving.
---

## User Input

```text
$ARGUMENTS
```

## Step 1 — Locate

Slug from `$ARGUMENTS` or the current `feature/[slug]` branch; work in its worktree (`git worktree list`, default format). Require an approved PRD; full size also requires `techspec.md`. Tool: `python3 .specify/presets/sdd-workflow/scripts/sdd.py` (if absent, the same path in the primary checkout — first line of `git worktree list`).

## Step 2 — Discover gates

Read the PRD, the techspec (full) and the project's test/lint/typecheck commands from manifests and CI. Choose a narrow gate per task and one complete final gate.

## Step 3 — Write the plan

Full: `specs/[slug]/tasks.md`. Small (≤3 tasks): append the same sections to `prd.md`; promote to full if it grows. One `## Tn` per atomic deliverable, code and its tests together, ordered by dependency:

```markdown
**Final gate:** `npm run lint && npm test`

## T1 — Persist drafts
**Status:** pending
**Requirements:** RF-01
**Criteria:** AC-01
**Depends on:** none
**Files:** `src/drafts.ts`, `src/drafts.test.ts`
**Gate:** `npm test -- drafts`

- Implement save and its tests, including the error cases in AC-01.

## Checks
| Criterion | Task | Proof command |
|-----------|------|---------------|
| AC-01 | T1 | `npm test -- drafts` |
```

Every RF and AC is covered by a task; the Checks table has exactly one row per AC. Run `sdd.py validate [slug] --stage tasks` and fix what it reports.

## Step 4 — Approve and commit

**Show the task list with gates and wait for explicit approval.** Then add `**Approved:** YYYY-MM-DD — user: "[their words]"` at the top of the task document. In `docs/kanban/feature-[slug].md` set `status: ready`, `tasks_total:`, `tasks_done: 0`, `updated:`.

```bash
git add specs/[slug]/ docs/kanban/feature-[slug].md
git commit -m "docs: add tasks for [slug]"
```

Then: "Run `/clear`, then `/speckit.implement [slug]`." (Optionally `/speckit.analyze [slug]` first.)

## Constraints

- No code. Each task has tests and a real gate command.
- Shell pipelines with `|` go in a project script, not in the Checks table.
