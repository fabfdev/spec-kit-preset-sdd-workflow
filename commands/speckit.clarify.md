---
description: Optional. Revisit an existing feature PRD with up to 5 targeted questions and encode the answers into prd.md. specify already clarifies new PRDs.
---

## User Input

```text
$ARGUMENTS
```

## Step 1 — Locate

Slug from `$ARGUMENTS` or the current `feature/[slug]` branch. Work in the feature's worktree: if `git worktree list` (default format) shows the branch at another path, stop and tell the user to run from there. Require `specs/[slug]/prd.md`; otherwise point to `/speckit.specify`.

## Step 2 — Scan

Read the PRD (and `docs/core/prd.md` only if a question may already be answered there). Look for untestable requirements, RFs without ACs, missing edge/error cases, unquantified rules, vague out of scope, open questions that block planning. Do not print the scan.

## Step 3 — Ask

Ask at most 5 questions **in one numbered round**, only those whose answer changes design, tasks or testability. Give a recommended answer for each. Zero questions is valid — say the PRD is ready.

## Step 4 — Update and commit

Patch only the affected sections; keep existing headings and IDs, add new RF/AC IDs at the end. If scope or acceptance outcomes changed, the previous approval is void: **show the diff and wait for approval**, then refresh the `**Approved:**` line with the user's words.

```bash
git add specs/[slug]/prd.md
git commit -m "docs: clarify PRD for [slug]"
```

## Constraints

- Read-only until the user approves the change.
- Never restructure the PRD or renumber IDs.
