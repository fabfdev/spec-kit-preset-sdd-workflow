---
description: Create a technical specification (techspec) for a feature that already has a PRD. Translates requirements into technical decisions.
handoffs:
  - label: Create Tasks
    agent: speckit.tasks
    prompt: Create the implementation tasks for this feature.
---

## User Input

```text
$ARGUMENTS
```

## Step 0 — Load architecture context (if available)

Before any generation, check if `docs/core/sdd.md` exists and read it if it does.

Extract and record:
- **Language/stack** → use in interface examples (do not use another language)
- **Test framework** → use in the testing section (omit layers marked "não aplicável")
- **Observability** → use in the monitoring section (omit the section if "não aplicável")

If `docs/core/sdd.md` does not exist, proceed — the techspec will cover stack decisions for this feature.

## Step 1 — Identify the feature

If not specified in `$ARGUMENTS`, ask the user which feature to generate the techspec for.

Verify that `docs/tasks/prd-[feature]/prd.md` exists before proceeding.

## Step 1.5 — Switch to the feature branch

```bash
git checkout feature/prd-[feature-slug]
```

## Step 2 — Load mandatory context

Read before any generation:
1. `docs/tasks/[feature]/prd.md` — full feature requirements
2. `docs/core/sdd.md` — base architecture, stack, conventions (if it exists)
3. Relevant source files from the project (explore current structure to understand existing patterns)

## Step 3 — Research (when needed)

For technical decisions involving libraries or patterns, search the current documentation for the relevant libraries and look for similar implementations in reference projects before making recommendations.

## Step 4 — Clarifying questions

Ask the user about:
- Module boundaries and positioning within the domain
- Data flow: inputs, outputs, transformations
- External dependencies and failure modes
- Testing strategy priority

## Step 5 — Draft the techspec

Focus on the **HOW** — translate PRD requirements into technical decisions.

Structure:

```markdown
# Techspec — [Feature Name]

**Version:** 1.0
**Date:** YYYY-MM-DD
**PRD:** [link to prd.md]

## 1. Overview
[Technical summary of what will be built.]

## 2. Architecture
[How this feature fits into the existing architecture. Affected modules.]

## 3. Data Model
[New or modified entities, fields, relationships.]

## 4. Interfaces
[Function signatures, API contracts, component props — in the project's language.]

## 5. Data Flow
[Sequence of operations from input to output.]

## 6. External Dependencies
[New libraries or services. Justification for each.]

## 7. Testing Strategy
[Unit: what to test and how.
Integration: what to test and how (or N/A).
E2E: what to test and how (or N/A).]

## 8. Monitoring
[Logs, metrics, alerts — or N/A if not applicable.]

## 9. Open Questions
[Unresolved technical decisions — max 3.]
```

## Step 6 — Present for approval

Show the complete draft to the user and wait for explicit approval before saving.

**Do not save until the user approves.**

## Step 7 — Save and update roadmap

After approval:
1. Save to `docs/tasks/[feature]/techspec.md`
2. Update `docs/core/roadmap.md`: change status `planning` → `specced`

## Step 8 — Commit

```bash
git add docs/tasks/[feature]/techspec.md docs/core/roadmap.md
git commit -m "docs: add techspec for [feature]"
```

## Constraints

- **Explore the project first** — non-obvious dependencies are in the code
- **Present before saving** — explicit approval required
- **Focus on HOW** — techspec describes implementation; PRD describes what/why
- **Do not write code** — only specify interfaces, models, and sequence
- **Branch required** — checkout `feature/prd-[feature]` before saving any file
- **Commit required** — commit `techspec.md` + `roadmap.md` with `docs:` prefix
