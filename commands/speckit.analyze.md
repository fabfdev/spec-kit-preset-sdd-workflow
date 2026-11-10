---
description: Optional read-only consistency check of a feature's prd.md, techspec.md and tasks before implementation. One pass, one report, modifies nothing.
---

## User Input

```text
$ARGUMENTS
```

## Step 1 — Structure

Slug from `$ARGUMENTS` or the current `feature/[slug]` branch; read the files from that branch. Run `python3 .specify/presets/sdd-workflow/scripts/sdd.py validate [slug] --stage tasks`. Structural errors are CRITICAL findings.

## Step 2 — Read only the feature

Read `specs/[slug]/prd.md`, `techspec.md` (full size), the task document, and the MUST-level rules of `docs/core/sdd.md` if it exists. Do not read source code, other features or project config files.

## Step 3 — One pass

Check:
- **Coverage:** each RF/AC maps to a task that can actually prove it; no orphan tasks.
- **Consistency:** terminology, data model and scope agree across documents.
- **Architecture:** nothing contradicts a MUST in `sdd.md` (always CRITICAL).
- **Testability:** each AC is observable; each gate can fail when the AC is broken.
- **Order:** dependencies come before dependents.

Severity: CRITICAL (blocks baseline function or violates sdd.md), HIGH (conflict, scope violation, untestable AC), MEDIUM, LOW.

## Step 4 — Report inline

```markdown
## Analyze — [slug]
| ID | Severity | Location | Finding | Fix |
|----|----------|----------|---------|-----|
Verdict: BLOCKED (CRITICAL/HIGH present) | READY (warnings only)
```

For BLOCKED, name the command that fixes each finding (`/speckit.clarify`, `/speckit.plan`, `/speckit.tasks`). MEDIUM/LOW are warnings and do not block. Do not loop: run once and stop.

## Constraints

- Read-only: never write files, JSON or reports to disk.
