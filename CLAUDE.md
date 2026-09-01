# CLAUDE.md — spec-kit-preset-sdd-workflow

## What this repo is

An **authoring repo for a spec-kit preset**. It is not an application. It ships
`commands/*.md` — prompt templates that spec-kit installs into a *target*
project as slash commands (`/speckit.specify`, `/speckit.plan`, …), replacing
spec-kit's core commands with the opinionated SDD workflow described in
`README.md`.

- `preset.yml` — manifest: which template replaces which core command, plus `version`.
- `commands/*.md` — the templates themselves. Each is a full prompt with numbered
  steps, fenced `bash` blocks showing exact commands, and a `## Constraints` block.
- Nothing here (including this file) is installed into the target project. Only
  `commands/*.md` ship. Guidance for the *end user's* agent must live inside the
  templates.

Sibling repo: `../spec-kit-extension-sdd-workflow` (the extension layer —
product PRD, SDD, bug/tech-debt, worktree lifecycle). Keep conventions in sync.

## Editing the command templates

- **Match the house style**: numbered steps, imperative voice, human approval
  gates called out in bold, a `## Constraints` recap at the end.
- **Every template must work with or without a CLI wrapper installed.** Users
  commonly run [rtk](https://github.com/rtk-ai/rtk) (a `PreToolUse` Bash hook
  that rewrites `git`, `gh`, `ls`, `grep`, … to compact equivalents). Write shell
  that survives that rewrite:
  - **No `git ... --porcelain` for output the template parses.** rtk's
    `rtk git worktree` drops `--porcelain` and reformats. Parse the default
    `git worktree list` format instead: `<path> <sha> [<branch>]`, one line each,
    first line = main worktree. This works identically with and without rtk.
  - **No command substitution (`$(...)`, backticks), no process substitution,
    no file redirects (`> f`, `>> f`), no heredocs (`<< EOF`)** in a fenced
    `bash` block. Any of these makes rtk pass the command through unrewritten
    (and they make the step harder to reason about). Break the work into
    discrete commands; use the agent's file-writing tool to create file bodies
    (e.g. a PR body file for `gh pr create --body-file`), not `>`.
  - `gh ... --json`, `gh pr merge`, `gh pr create`, `git add/commit`,
    `git worktree add` are all safe — rtk either passes them through or emits a
    faithful confirmation line.
- **Tracking is local (since v2.0.0).** Status and history live in
  `docs/kanban/feature-[slug].md` — YAML frontmatter for the structured fields
  (`status`, `slug`, `branch`, `worktree`, `priority`, `tasks_done`,
  `tasks_total`, `pr`, `created`, `updated`), markdown body for notes. The file
  is committed with the feature, so `git log` is the audit trail. The schema is
  documented in `docs/kanban/README.md`, created by the extension's `setup`; the
  preset commands create `docs/kanban/` on demand so they also work without the
  extension. No Notion, no MCP, no `.sdd-notion.json` anywhere in the workflow.
- **Reference-doc reads**: steps that load `sdd.md` / `prd.md` / `techspec.md`
  for context can use `rtk read <file>` (via Bash) for a first survey pass when
  rtk is present, but the agent should fall back to its native file-read tool
  when it needs exact text to edit. Keep this as the end user's judgment call;
  do not hard-code `rtk` invocations into a template.

## Versioning

Bump `version` in `preset.yml` on any change to `commands/*.md` or the manifest,
and update the `v<version>` tag in the README install snippets to match.
