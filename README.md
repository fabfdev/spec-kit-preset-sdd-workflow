# spec-kit-preset-sdd-workflow

A [Spec Kit](https://github.com/github/spec-kit) preset that replaces the four core workflow commands with an opinionated **Spec-Driven Development (SDD)** workflow.

---

## Background

### What is Spec Kit?

[Spec Kit](https://github.com/github/spec-kit) is an open-source toolkit that implements Spec-Driven Development. It installs slash commands (e.g. `/speckit.specify`, `/speckit.plan`) into your AI coding agent — Claude, Copilot, Cursor, and 30+ others — and guides the agent through a structured workflow from requirements to implementation.

Spec Kit has no AI logic of its own. The commands are Markdown prompt files that tell the agent what to do step by step.

### What is a preset?

A preset overrides Spec Kit's default command files at install time. When you install this preset, your agent's `speckit.specify`, `speckit.plan`, `speckit.tasks`, and `speckit.implement` commands are replaced with the versions defined here — without touching Spec Kit's CLI or core infrastructure.

### Why this preset?

Spec Kit's default commands are intentionally minimal. This preset layers an opinionated workflow on top:

- **Mandatory human approval gates** — nothing is saved or committed without explicit user confirmation
- **Conventional commits** — `feat:`, `fix:`, `docs:`, `refactor:` prefixes enforced at every step
- **Roadmap tracking** — `docs/core/roadmap.md` is updated automatically at each phase transition
- **Two-commit discipline per task** — implementation code first, tracking files second, always separate
- **Graceful degradation** — works without `docs/core/prd.md` and `docs/core/sdd.md`; uses them when present to avoid redundant questions

---

## Commands

This preset replaces the following Spec Kit core commands:

| Command | Replaces | What it does |
|---------|----------|--------------|
| `speckit.specify` | `speckit.specify` | Creates a feature-level PRD in `docs/tasks/prd-[feature]/prd.md` with clarifying questions and approval gate |
| `speckit.plan` | `speckit.plan` | Creates a techspec in `docs/tasks/prd-[feature]/techspec.md` translating PRD requirements into technical decisions |
| `speckit.tasks` | `speckit.tasks` | Breaks down PRD + techspec into task files with high-level approval before generating any file |
| `speckit.implement` | `speckit.implement` | Implements one task at a time with test gate, human validation, and two-commit tracking |

---

## Installation

### Prerequisites

- [Spec Kit CLI](https://github.com/github/spec-kit) installed (`uv tool install specify-cli ...`)
- A project initialized with `specify init`

### Install the preset

```bash
specify preset add sdd-workflow \
  --from https://github.com/fabfdev/spec-kit-preset-sdd-workflow/archive/refs/tags/v1.0.0.zip
```

### Full project setup (recommended)

For the complete workflow including product PRD, SDD architecture document, and bug tracking, also install the companion extension:

```bash
specify extension add sdd-workflow \
  --from https://github.com/fabfdev/spec-kit-extension-sdd-workflow/archive/refs/tags/v1.0.0.zip
```

Then initialize the project structure:

```
/speckit.sdd-workflow.setup
```

---

## Workflow

Once installed, the full development lifecycle looks like this:

```
[Project inception — run once]
/speckit.sdd-workflow.product-prd   → docs/core/prd.md
/speckit.sdd-workflow.sdd           → docs/core/sdd.md

[Feature cycle — repeat per feature]
/speckit.specify                    → docs/tasks/prd-[feature]/prd.md
/speckit.plan                       → docs/tasks/prd-[feature]/techspec.md
/speckit.tasks                      → docs/tasks/prd-[feature]/tasks.md + N_task.md files
/speckit.implement                  → code + commits (one task at a time)

[Maintenance]
/speckit.sdd-workflow.fix-bug       → docs/health/bugs/BUG-XXX.md + bugfix branch + PR
```

### Roadmap status lifecycle

```
planning → specced → ready → in_progress → completed
```

| Transition | Triggered by |
|------------|-------------|
| `planning` | `/speckit.specify` |
| `specced` | `/speckit.plan` |
| `ready` | `/speckit.tasks` |
| `in_progress` | `/speckit.implement` (first task) |
| `completed` | `/speckit.implement` (last task) |

---

## File structure generated

```
docs/
  core/
    roadmap.md          ← macro feature tracking (auto-updated)
    prd.md              ← product PRD (from companion extension)
    sdd.md              ← architecture doc (from companion extension)
  tasks/
    prd-[feature]/
      prd.md
      techspec.md
      tasks.md
      1_task.md
      2_task.md
      ...
  health/
    bugs/               ← BUG-XXX documents
    debt/               ← TD-XXX documents
```

---

## Creating a new version

When you update command files in this repo, follow these steps to publish a new version:

### 1. Make your changes

Edit files in `commands/` as needed.

### 2. Update the version in `preset.yml`

```yaml
preset:
  version: "1.1.0"  # bump according to semver
```

Use semantic versioning:
- **Patch** (`1.0.x`) — wording fixes, minor clarifications
- **Minor** (`1.x.0`) — new behavior added, backwards compatible
- **Major** (`x.0.0`) — breaking changes to the workflow

### 3. Commit

```bash
git add .
git commit -m "chore: bump preset to v1.1.0"
```

### 4. Push

```bash
git push
```

### 5. Create the release

```bash
gh release create v1.1.0 \
  --repo fabfdev/spec-kit-preset-sdd-workflow \
  --title "v1.1.0" \
  --target main \
  --notes "Describe what changed."
```

### 6. Update projects

In each project using this preset, update the `--from` URL to the new version:

```bash
specify preset remove sdd-workflow
specify preset add sdd-workflow \
  --from https://github.com/fabfdev/spec-kit-preset-sdd-workflow/archive/refs/tags/v1.1.0.zip
```

---

## Companion extension

This preset pairs with [`spec-kit-extension-sdd-workflow`](https://github.com/fabfdev/spec-kit-extension-sdd-workflow), which adds the commands that Spec Kit doesn't cover:

- `/speckit.sdd-workflow.setup` — initializes the project directory structure
- `/speckit.sdd-workflow.product-prd` — creates the product-level PRD
- `/speckit.sdd-workflow.sdd` — creates the Software Design Document
- `/speckit.sdd-workflow.fix-bug` — registers and fixes bugs with full tracking

---

## License

MIT
