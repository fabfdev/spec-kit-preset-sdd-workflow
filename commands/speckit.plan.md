---
description: Create the techspec (specs/[slug]/techspec.md) for a full-size feature with an approved PRD. Small features skip this step.
---

## User Input

```text
$ARGUMENTS
```

## Step 1 — Locate

Slug from `$ARGUMENTS` or the current `feature/[slug]` branch. If not on it, `git switch feature/[slug]` (dirty tree: ask to commit or stash first; branch held by a legacy worktree: work in that path). Require an approved `specs/[slug]/prd.md`. If it says `**Size:** small`, tell the user to run `/speckit.tasks` instead.

## Step 2 — Investigate

Read the PRD and the sections of `docs/core/sdd.md` relevant to this feature (stack, conventions, test framework). Explore only the modules this feature touches and one representative existing test. Look up library documentation only for an API that is new or uncertain here.

## Step 3 — Decide

Ask only unresolved technical decisions (module boundaries, data model, failure modes, test depth) in **one numbered round**, each with a recommendation. Find repository facts yourself.

## Step 4 — Draft

Focus on HOW, citing PRD IDs. Omit sections that do not apply.

```markdown
# Techspec — [Feature]
**PRD:** specs/[slug]/prd.md

## 1. Overview and affected modules
## 2. Data model
## 3. Interfaces (in the project's language)
## 4. Data flow and failure modes
## 5. Dependencies (justify each new one)
## 6. Testing strategy (unit / integration / e2e; real commands)
```

**Show the draft and wait for explicit approval.**

## Step 5 — Save and commit

Save `specs/[slug]/techspec.md`. In `docs/kanban/feature-[slug].md` set `status: specced` and `updated:`; keep other fields.

```bash
git add specs/[slug]/techspec.md docs/kanban/feature-[slug].md
git commit -m "docs: add techspec for [slug]"
```

Then: "Run `/clear`, then `/speckit.tasks [slug]`."

## Constraints

- No code; only interfaces, models and sequence.
- Respect MUST-level rules in `docs/core/sdd.md`.
