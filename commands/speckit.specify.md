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

## Step 2 — Check for duplicate slug in Notion

Load `.sdd-notion.json` from the project root and read `database_id`.

Use the Notion MCP to query the database filtering where the `Slug` property equals the derived slug.

If a page already exists with that slug:

```
A feature with slug "[slug]" already exists in Notion.
Status: [current status]
Notion page: [page URL]

Is this a new feature or a continuation of the existing one?
- New feature: choose a different slug.
- Continuation: navigate to the existing feature's worktree.
```

Wait for the user's response before proceeding.

If continuation, locate the existing worktree:

1. Read the `Worktree Path` property from the Notion page (if the property exists and is not empty).
2. Verify it still exists: run `git worktree list --porcelain` and confirm a `worktree [path]` entry is present.
3. If confirmed, `cd` into that path before continuing — the rest of this command (and any follow-up command) now operates inside the worktree.
4. If `Worktree Path` is empty (project set up before this property existed) or the path no longer matches a real worktree, fall back to: run `git worktree list --porcelain` and find the entry whose branch is `feature/[slug]`. If found, `cd` into it. If no worktree exists at all for this branch, tell the user the feature predates the worktree convention and continue in the current directory.

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

1. Check idempotency before creating anything: run `git worktree list --porcelain` and check for an entry whose branch is `feature/[feature-slug]`. Also check if the local branch already exists (`git branch --list feature/[feature-slug]`).
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

## Step 7 — Register in Notion

Use the Notion MCP to create a new page in the database (read `database_id` from `.sdd-notion.json`) with these properties:

- **Name**: [Feature Name]
- **Type**: Feature
- **Status**: Planned
- **Slug**: [feature-slug]
- **Branch**: feature/[feature-slug]
- **Worktree Path**: .worktrees/[feature-slug] (if this property doesn't exist on the database yet — project set up before this version — skip it silently)
- **Tasks Done**: 0
- **Tasks Total**: 0
- **Priority**: Medium (adjust if the user specified otherwise)

Then append the following content block to the newly created Notion page:

```
Spec path: specs/[feature-slug]/
```

## Step 8 — Commit

Run inside the worktree (`.worktrees/[feature-slug]/`):

```bash
git add specs/[feature-slug]/prd.md
git commit -m "docs: add PRD for [feature-slug]"
```

## Constraints

- **Notion check first** — always query Notion for duplicate slug before creating any folder
- **Questions first** — never skip to drafting
- **Present before saving** — explicit approval required
- **Focus on WHAT and WHY** — no technical implementation details
- **Worktree required** — always create `.worktrees/[slug]` with branch `feature/[slug]` after saving; never plain `git checkout -b` in the current directory
- **Idempotent worktree creation** — check for an existing worktree/branch before creating one; never fail on a re-run
- **Commit required** — commit only `prd.md` with `docs:` prefix
- **Notion registration required** — create Notion page after every approved PRD
