---
description: Identify underspecified areas in the feature PRD by asking up to 5 targeted clarification questions and encoding answers back into prd.md. Run after /speckit.specify and before /speckit.plan.
handoffs:
  - label: Create Techspec
    agent: speckit.plan
    prompt: Create the techspec for this feature.
---

## User Input

```text
$ARGUMENTS
```

## Step 0 — Load project context

Before proceeding, check if these files exist and read them if they do:

- `docs/core/prd.md` — product vision, personas, business rules. Skip questions already answered here.
- `docs/core/sdd.md` — architecture, stack, conventions. Skip questions already answered here.

## Step 1 — Identify the feature

If not specified in `$ARGUMENTS`, check the current git branch name for `feature/NNN-[slug]` and infer from it. If still unclear, ask the user.

Locate `specs/NNN-[feature-slug]/prd.md`. If it doesn't exist, stop and instruct the user to run `/speckit.specify` first.

## Step 2 — Switch to the feature branch

```bash
git checkout feature/NNN-[feature-slug]
```

## Step 3 — Scan the PRD for ambiguity

Read `specs/NNN-[feature-slug]/prd.md` in full.

Run an internal ambiguity scan across these categories. For each, mark internally: **Clear / Partial / Missing**.

- **Functional scope**: Are requirements testable? Any vague verbs ("handle", "manage", "support") without measurable criteria?
- **Out of scope**: Is it explicit enough to prevent scope creep during techspec?
- **User scenarios**: Are edge cases, error states, and empty states covered?
- **Business rules**: Are constraints quantified, or left open to interpretation?
- **Dependencies**: Are external systems and their failure modes described?
- **Open questions**: Does `## 8. Open Questions` have items that block planning?

Do not output the raw scan. Use it internally to prioritize questions.

## Step 4 — Generate up to 5 targeted questions

Select at most 5 questions where the answer would materially change the techspec or implementation.

A question qualifies if its answer affects:
- Architecture or data modeling decisions
- Task decomposition or ordering
- Acceptance criteria testability
- UX behavior or error handling strategy

Skip questions about stylistic preferences. Skip questions already answered in `docs/core/prd.md` or `docs/core/sdd.md`. If the PRD is already complete, asking 0–2 questions is valid.

## Step 5 — Interactive questioning (one at a time)

Present **EXACTLY ONE question at a time**. Wait for the user's answer before presenting the next.

For questions with discrete options:
- Show 2–4 mutually exclusive options
- Recommend the best option with a one-sentence reason
- Format: `**Recommended:** Option [X] — [reason]`
- Let the user accept the recommendation or choose another

For open-ended questions:
- Suggest an answer based on best practices and project context
- Format: `**Suggested:** [answer] — [reason]`
- Let the user accept or provide their own answer

## Step 6 — Update prd.md with clarifications

After all questions are answered:

1. Incorporate answers into the relevant sections of `specs/NNN-[feature-slug]/prd.md`
2. Resolve items in `## 8. Open Questions` — remove resolved ones or mark them answered
3. Add new content only where needed — do not restructure the entire PRD
4. If a clarification expands scope, add entries to `## 3. Functional Requirements` (RF-XX) and `## 4. User Scenarios`

## Step 7 — Present diff and ask for approval

Show a summary of every section changed and what was added or removed. Wait for explicit approval before committing.

**Do not commit without approval.**

## Step 8 — Commit

```bash
git add specs/NNN-[feature-slug]/prd.md
git commit -m "docs: clarify PRD for NNN-[feature-slug]"
```

## Constraints

- **One question at a time** — never dump all questions at once
- **Max 5 questions** — if the PRD is already complete, fewer is better; zero is valid
- **Update, don't restructure** — preserve existing section headings and requirement IDs (RF-01, etc.)
- **Approval required** — show what changed before committing
- **Read-only until approved** — do not modify prd.md until the user approves
- **Branch required** — checkout `feature/NNN-[slug]` before any file write
