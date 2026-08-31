---
description: Create a technical specification (techspec) for a feature that already has a PRD. Translates requirements into technical decisions.
handoffs:
  - label: Clarify PRD first
    agent: speckit.clarify
    prompt: Clarify the PRD for this feature before planning.
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

If not specified in `$ARGUMENTS`, check the current git branch name for `feature/[slug]` and infer from it. If still unclear, ask the user.

Verify that `specs/[feature-slug]/prd.md` exists before proceeding.

## Step 1.5 — Verify the branch isn't checked out elsewhere

Run `git worktree list` (each line is `<path> <sha> [<branch>]`; do not pass `--porcelain` — command wrappers in some setups strip it) and check if `feature/[feature-slug]` appears as a `[<branch>]` in a worktree line.

- If it is, and its path differs from the current directory: stop and tell the user:
  ```
  This feature has a dedicated worktree at [path].
  Run this command from there instead of the current directory.
  ```
  Do not attempt `git checkout` — Git refuses to check out a branch that's already checked out in another worktree, so it would just fail.
- If no worktree holds this branch (feature predates the worktree convention, or its worktree was already removed by `/speckit.sdd-workflow.finish`): proceed with the checkout below.

```bash
git checkout feature/[feature-slug]
```

## Step 2 — Load mandatory context

Read before any generation:
1. `specs/[feature-slug]/prd.md` — full feature requirements
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
**PRD:** specs/[feature-slug]/prd.md

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

## Step 7 — Save and update the kanban entry

After approval:

1. Save to `specs/[feature-slug]/techspec.md`
2. In `docs/kanban/feature-[feature-slug].md` frontmatter, set `status: specced` and `updated:` to today's date. (If the file does not exist — feature predates the kanban convention — create it now following the schema in `docs/kanban/README.md`.)

## Step 8 — Commit

```bash
git add specs/[feature-slug]/techspec.md docs/kanban/feature-[feature-slug].md
git commit -m "docs: add techspec for [feature-slug]"
```

## Constraints

- **Explore the project first** — non-obvious dependencies are in the code
- **Present before saving** — explicit approval required
- **Focus on HOW** — techspec describes implementation; PRD describes what/why
- **Do not write code** — only specify interfaces, models, and sequence
- **Branch required** — checkout `feature/[feature-slug]` before saving any file
- **Commit required** — commit `techspec.md` and the kanban entry with `docs:` prefix
- **Kanban update required** — set `status: specced` in `docs/kanban/feature-[slug].md` after saving techspec
