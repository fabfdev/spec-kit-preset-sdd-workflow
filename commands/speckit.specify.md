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
- Continuation: navigate to the existing feature's PRD at specs/[slug]/prd.md.
```

Wait for the user's response before proceeding.

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

## Step 6 — Save and create branch

After approval:

1. Create directory `specs/[feature-slug]/`
2. Save to `specs/[feature-slug]/prd.md`
3. Create and switch to feature branch:

```bash
git checkout -b feature/[feature-slug]
```

## Step 7 — Register in Notion

Use the Notion MCP to create a new page in the database (read `database_id` from `.sdd-notion.json`) with these properties:

- **Name**: [Feature Name]
- **Type**: Feature
- **Status**: Planned
- **Slug**: [feature-slug]
- **Branch**: feature/[feature-slug]
- **Tasks Done**: 0
- **Tasks Total**: 0
- **Priority**: Medium (adjust if the user specified otherwise)

Then append the following content block to the newly created Notion page:

```
Spec path: specs/[feature-slug]/
```

## Step 8 — Commit

```bash
git add specs/[feature-slug]/prd.md
git commit -m "docs: add PRD for [feature-slug]"
```

## Constraints

- **Notion check first** — always query Notion for duplicate slug before creating any folder
- **Questions first** — never skip to drafting
- **Present before saving** — explicit approval required
- **Focus on WHAT and WHY** — no technical implementation details
- **Branch required** — always create `feature/[slug]` after saving
- **Commit required** — commit only `prd.md` with `docs:` prefix
- **Notion registration required** — create Notion page after every approved PRD
