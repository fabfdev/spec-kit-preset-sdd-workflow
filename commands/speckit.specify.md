---
description: Create a feature-level PRD with clarifying questions and mandatory approval before saving. Feature folder is named by slug only (specs/[slug]/).
handoffs:
  - label: Clarify PRD
    agent: speckit.clarify
    prompt: Clarify the PRD for this feature.
  - label: Create Techspec
    agent: speckit.plan
    prompt: Create the techspec for this feature.
---

## User Input

```text
$ARGUMENTS
```

## Step 0 — Load project context (if available)

Before asking any questions, check if these files exist and read them if they do:

- `docs/core/prd.md` — product vision, personas, business rules. If present, do not ask about information already documented here.
- `docs/core/sdd.md`, section `## Contexto do Projeto` — project type and stack. If present, do not ask about information already documented here.

If neither file exists, proceed normally — all necessary context will be gathered through clarifying questions.

## Step 1 — Identify the feature

If the feature is not clear from `$ARGUMENTS`, ask the user which feature they want to document.

Derive the feature slug (lowercase, hyphenated, e.g. `user-authentication`).

## Step 2 — Check for duplicate slug

A feature is a duplicate if either of these is true:

- `docs/kanban/feature-[slug].md` already exists.
- `git worktree list` (each line is `<path> <sha> [<branch>]`) has a line whose `[<branch>]` is `[feature/[slug]]`.

If a duplicate is found:

```
A feature with slug "[slug]" already exists.
Status: [status: from docs/kanban/feature-[slug].md, or "branch exists, no kanban file"]
Kanban entry: docs/kanban/feature-[slug].md

Is this a new feature or a continuation of the existing one?
- New feature: choose a different slug.
- Continuation: navigate to the existing feature's worktree.
```

Wait for the user's response before proceeding.

If continuation, locate the existing worktree:

1. Read the `worktree:` field from `docs/kanban/feature-[slug].md` frontmatter (if the file exists and the field is not empty).
2. Verify it still exists: run `git worktree list` and confirm a line starting with that path is present. Each line is `<path> <sha> [<branch>]`; do not pass `--porcelain` (command wrappers in some setups strip it — the default format carries everything this command needs).
3. If confirmed, `cd` into that path before continuing — the rest of this command (and any follow-up command) now operates inside the worktree.
4. If the `worktree:` field is empty or the path no longer matches a real worktree, fall back to: run `git worktree list` and find the line whose `[<branch>]` is `[feature/[slug]]`. If found, `cd` into its path. If no worktree exists at all for this branch, tell the user the feature predates the worktree convention and continue in the current directory.

## Step 3 — Clarifying questions

Ask the user the following before drafting anything:

- What specific problem does this feature solve?
- Which users are affected and what are their needs?
- What is the main functionality and use cases?
- What is explicitly **out of scope** for this feature?
- Are there dependencies on other features?

Do not skip this step even if the feature description seems complete — the questions capture scope constraints and edge cases.

## Step 4 — Draft the PRD

Using the answers, draft the feature PRD focused on the **WHAT and WHY** — no implementation details.

Structure:

```markdown
# PRD — [Feature Name]

**Version:** 1.0
**Date:** YYYY-MM-DD
**Status:** Draft
**Spec:** specs/[feature-slug]/

## 1. Overview
[Problem the feature solves and why it matters.]

## 2. Objectives
[What success looks like for this feature.]

## 3. Functional Requirements
- RF-01: [Requirement]
- RF-02: [Requirement]

## 4. User Scenarios
[Main user flows — step by step.]

## 5. Out of Scope
[What this feature explicitly does NOT cover.]

## 6. Business Rules
[Constraints and rules that govern this feature.]

## 7. Dependencies
[Other features or systems this depends on.]

## 8. Open Questions
[Anything still unresolved — max 3.]
```

## Step 5 — Present for approval

Show the complete draft to the user and wait for explicit approval before saving anything.

**Do not save until the user approves.**

## Step 6 — Create worktree and save

After approval:

1. Check idempotency before creating anything: run `git worktree list` (each line is `<path> <sha> [<branch>]`) and check for a line whose `[<branch>]` is `[feature/[feature-slug]]`. Also check if the local branch already exists (`git branch --list feature/[feature-slug]`).
   - If a worktree already exists for this branch: `cd` into it and skip straight to substep 4 below (do not create a new worktree).
   - If the branch exists but has no worktree: `git worktree add .worktrees/[feature-slug] feature/[feature-slug]` (no `-b` — attach the existing branch instead of creating a new one).
   - If neither exists: proceed normally with substep 2.
2. Ensure `.worktrees/` is listed in the project's `.gitignore`. If the file doesn't have it, add the line and commit that change on its own (`chore: ignore .worktrees/`) before continuing.
3. Create the isolated worktree with a new branch:

```bash
git worktree add .worktrees/[feature-slug] -b feature/[feature-slug]
```

4. Create directory `.worktrees/[feature-slug]/specs/[feature-slug]/`
5. Save to `.worktrees/[feature-slug]/specs/[feature-slug]/prd.md`
6. Tell the user:

```
Worktree created at .worktrees/[feature-slug]/
You can continue here (this session just moved into it), or open a new Claude Code session pointed at that path to work on it in parallel with something else.
```

## Step 7 — Register in docs/kanban/

Everything below runs inside the worktree (`.worktrees/[feature-slug]/`).

Create `docs/kanban/` if it does not exist. Then write `docs/kanban/feature-[feature-slug].md`:

```markdown
---
name: [Feature Name]
type: feature
status: planned
slug: [feature-slug]
branch: feature/[feature-slug]
worktree: .worktrees/[feature-slug]
priority: medium
spec: specs/[feature-slug]/
tasks_done: 0
tasks_total: 0
pr:
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
---

## Notes

[Optional freeform context. Leave empty if nothing to add.]
```

Set `priority` to `low` / `medium` / `high` per what the user specified (default `medium`). Use today's date for `created` and `updated`.

## Step 8 — Commit

Run inside the worktree (`.worktrees/[feature-slug]/`):

```bash
git add specs/[feature-slug]/prd.md docs/kanban/feature-[feature-slug].md
git commit -m "docs: add PRD for [feature-slug]"
```

## Constraints

- **Duplicate check first** — check `docs/kanban/feature-[slug].md` and `git worktree list` for the branch before creating any folder
- **Questions first** — never skip to drafting
- **Present before saving** — explicit approval required
- **Focus on WHAT and WHY** — no technical implementation details
- **Worktree required** — always create `.worktrees/[slug]` with branch `feature/[slug]` after saving; never plain `git checkout -b` in the current directory
- **Idempotent worktree creation** — check for an existing worktree/branch before creating one; never fail on a re-run
- **Commit required** — commit `prd.md` and the `docs/kanban/` entry together with `docs:` prefix
- **Kanban entry required** — create `docs/kanban/feature-[slug].md` (status `planned`) after every approved PRD
