---
description: Validate cross-artifact consistency between prd.md, techspec.md, and tasks.md before implementation. Read-only — produces a structured report, modifies nothing. Run after /speckit.tasks and before /speckit.implement.
---

## User Input

```text
$ARGUMENTS
```

## Goal

Identify inconsistencies, coverage gaps, and underspecified areas across the three core feature artifacts before implementation begins. This command must run only after `/speckit.tasks` has produced a complete `tasks.md`.

**STRICTLY READ-ONLY**: do not modify any file. Output a structured analysis report only.

## Step 1 — Identify the feature

If not specified in `$ARGUMENTS`, check the current git branch name for `feature/[slug]` and infer from it. If still unclear, ask the user.

Verify that all three files exist:
- `specs/[feature-slug]/prd.md`
- `specs/[feature-slug]/techspec.md`
- `specs/[feature-slug]/tasks.md`

If any are missing, stop and tell the user which command to run first.

## Step 2 — Load architecture authority

If `docs/core/sdd.md` exists, read it in full. Extract:
- Stack constraints (language, frameworks, forbidden libraries)
- Naming conventions and structural rules
- Test requirements per layer
- Any MUST-level architecture decisions

`docs/core/sdd.md` is the authority for this project. Conflicts with it are automatically **CRITICAL**.

## Step 3 — Load the three artifacts

**From `prd.md`:**
- Functional requirements (RF-XX)
- User scenarios
- Out of scope declarations
- Business rules
- Open questions

**From `techspec.md`:**
- Architecture and stack decisions
- Data model (entities, fields, relationships)
- Interfaces and contracts
- Testing strategy
- External dependencies

**From `tasks.md`:**
- Task IDs and titles
- Task order and grouping
- Referenced files and components

## Step 4 — Run detection passes

### A. Coverage gaps
- Every RF-XX in `prd.md` must have at least one associated task
- Every task must trace back to a requirement in `prd.md` or a decision in `techspec.md`
- Flag: orphaned tasks (no requirement), uncovered requirements (no task)

### B. Inconsistencies
- **Terminology drift**: same concept named differently across the three files
- **Stack conflict**: techspec uses a library or pattern not aligned with `sdd.md`
- **Scope violation**: techspec or tasks cover something explicitly out of scope in `prd.md`
- **Data model conflict**: entity in `techspec.md` not mentioned in `prd.md`, or vice versa

### C. Underspecification
- Requirements with no measurable acceptance criterion
- Tasks with no clear Definition of Done
- Open questions in `prd.md` that the techspec did not address

### D. sdd.md alignment
- Does the techspec violate any MUST-level constraint from `sdd.md`?
- Are naming conventions and structural rules from `sdd.md` reflected in the task files?

### E. Task ordering
- Are foundational tasks before dependent tasks?
- Is testing included in the task list?
- Are backend tasks before frontend tasks (where applicable)?

## Step 5 — Assign severity

- **CRITICAL**: Violates a MUST in `sdd.md`; uncovered requirement that blocks baseline functionality; blocking inconsistency between artifacts
- **HIGH**: Duplicate or conflicting requirement; ambiguous acceptance criterion; scope violation; terminology drift affecting data model
- **MEDIUM**: Underspecified edge case; missing non-functional coverage; open question not addressed by techspec
- **LOW**: Minor wording inconsistency; low-risk redundancy; style improvement

## Step 6 — Produce the analysis report

Output a Markdown report inline. Do not write it to any file.

```markdown
## Analyze Report — [feature-slug]

### Findings

| ID | Category | Severity | Location | Summary | Recommendation |
|----|----------|----------|----------|---------|----------------|
| C1 | Coverage | CRITICAL | prd.md RF-03 | No task covers RF-03 | Add task for ... |
| I1 | Inconsistency | HIGH | techspec.md / sdd.md | Uses library X forbidden by sdd.md | Replace with Y |

### Coverage Summary

| Requirement | Has Task? | Task IDs |
|-------------|-----------|----------|
| RF-01       | ✅        | 1.0, 2.0 |
| RF-02       | ❌        | —        |

### Metrics
- Total requirements: N
- Total tasks: N
- Coverage: N%
- Critical issues: N
- High issues: N
- Medium/Low issues: N
```

## Step 7 — Next actions

End the report with a clear recommendation:

- **If CRITICAL issues exist:** do not proceed to `/speckit.implement`. List which commands to re-run (e.g., `/speckit.specify` to update the PRD, `/speckit.plan` to update the techspec).
- **If only MEDIUM/LOW issues:** the user may proceed to `/speckit.implement`. List improvements as optional suggestions.
- **If no issues:** confirm all artifacts are consistent and ready for implementation.

## Constraints

- **Read-only** — never modify any file under any circumstances
- **sdd.md is authoritative** — conflicts with it are always CRITICAL, not negotiable
- **Feature-scoped** — only analyze the specified feature's artifacts
- **No remediation** — report findings only; remediation happens via the appropriate commands
