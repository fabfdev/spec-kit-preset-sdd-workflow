---
description: Create a feature PRD (specs/[slug]/prd.md) with one round of clarifying questions, approval before saving, a feature branch and a kanban entry.
---

## User Input

```text
$ARGUMENTS
```

## Step 1 — Context and slug

Read `docs/core/prd.md` and the `## Contexto do Projeto` section of `docs/core/sdd.md` if they exist; never ask what they already answer. Derive a kebab-case slug.

Duplicate if `docs/kanban/feature-[slug].md` exists or `git branch --list feature/[slug]` prints it. Then ask: new feature (pick another slug) or continuation (switch to that branch).

## Step 2 — One round of questions

Ask everything in **one numbered round**, each with your recommended answer: problem, affected users, main use cases, out of scope, dependencies, plus up to 5 ambiguities that would change the design (edge cases, error states, measurable rules). Skip what the description already settles.

## Step 3 — Draft

WHAT and WHY only. Choose `small` (≤3 obvious tasks, no new architecture, integration or data/security risk) or `full`.

```markdown
# PRD — [Feature]
**Size:** small | full
**Date:** YYYY-MM-DD

## 1. Problem and objectives
## 2. Requirements
- RF-01: [requirement]
- AC-01 (RF-01): When [situation], the system shall [observable outcome].
## 3. User scenarios (incl. edge and error cases)
## 4. Business rules
## 5. Out of scope
## 6. Dependencies
```

Every RF needs at least one AC. **Show the draft and wait for explicit approval.** Then add under the title: `**Approved:** YYYY-MM-DD — user: "[their words]"`.

## Step 4 — Branch and save

The working tree must be clean; otherwise ask the user to commit or stash first. Branch from the up-to-date default branch (if the branch already exists, just `git switch feature/[slug]`):

```bash
git switch [default-branch]
git pull --ff-only
git switch -c feature/[slug]
```

Save `specs/[slug]/prd.md` and `docs/kanban/feature-[slug].md`:

```markdown
---
name: [Feature]
type: feature
status: planned
slug: [slug]
branch: feature/[slug]
priority: medium
spec: specs/[slug]/
tasks_done: 0
tasks_total: 0
pr:
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

```bash
git add specs/[slug]/prd.md docs/kanban/feature-[slug].md
git commit -m "docs: add PRD for [slug]"
```

## Step 5 — Hand off

"Run `/clear`, then `/speckit.plan [slug]` (full) or `/speckit.tasks [slug]` (small)."

## Constraints

- Questions in one round; approval before saving; no implementation details.
- Never commit feature work on the default branch; re-runs must be idempotent.
