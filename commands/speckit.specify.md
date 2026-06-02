---
description: Create a feature-level PRD with clarifying questions and mandatory approval before saving.
handoffs:
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

## Step 2 — Clarifying questions

Ask the user the following before drafting anything:

- What specific problem does this feature solve?
- Which users are affected and what are their needs?
- What is the main functionality and use cases?
- What is explicitly **out of scope** for this feature?
- Are there dependencies on other features?

Do not skip this step even if the feature description seems complete — the questions capture scope constraints and edge cases.

## Step 3 — Draft the PRD

Using the answers, draft the feature PRD focused on the **WHAT and WHY** — no implementation details.

Structure:

```markdown
# PRD — [Feature Name]

**Version:** 1.0
**Date:** YYYY-MM-DD
**Status:** Draft

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

## Step 4 — Present for approval

Show the complete draft to the user and wait for explicit approval before saving anything.

**Do not save until the user approves.**

## Step 5 — Save and create branch

After approval:

1. Create directory `docs/tasks/prd-[feature-slug]/`
2. Save to `docs/tasks/prd-[feature-slug]/prd.md`
3. Create and switch to feature branch:

```bash
git checkout -b feature/prd-[feature-slug]
```

## Step 6 — Register in roadmap

Open `docs/core/roadmap.md` and add:

```
| [Readable Name] | prd-[feature-slug] | planning | 0/0 |
```

If `docs/core/roadmap.md` does not exist, create it with a header and this first entry.

## Step 7 — Commit

```bash
git add docs/tasks/prd-[feature-slug]/prd.md docs/core/roadmap.md
git commit -m "docs: add PRD for prd-[feature-slug]"
```

## Constraints

- **Questions first** — never skip to drafting
- **Present before saving** — explicit approval required
- **Focus on WHAT and WHY** — no technical implementation details
- **Branch required** — always create `feature/prd-[slug]` after saving
- **Commit required** — commit `prd.md` + `roadmap.md` on the feature branch with `docs:` prefix
