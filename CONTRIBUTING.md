# Contributing

## Scope

This repository is **English-only** and **Markdown-only**.

## How to Contribute

| Type | Description |
|------|-------------|
| New prompts | Agent, project-type, or workflow prompts |
| Improvements | Better structure, clarity, outcome quality |
| Examples | Real-world APEI walkthroughs |
| Maintenance | Link fixes, catalog cleanup, archive actions |

## Prompt Quality Standard

Every prompt must contain:
- `## Role` (one or two sentences)
- A protocol section — `## Protocol: <ACRONYM>` or `## <Name> Protocol`
- Phase sections (`## Phase 1: …`, or a single `## Phases`) with `- [ ]` checklists or ordered steps
- `## Remember` (final section)

**Agent prompts** (`prompts/english/agents/`) also need, right under the `> **subtitle**` line:
- A `**Use this when:**` line — the concrete situation this prompt is for
- A `**Skip to:**` list of 3–5 anchor links that resolve to real headings in the file

Project-type prompts (`prompts/english/project-types/`) may keep their `## Overview` opener; the `## Role` and protocol sections are still required.

The routing table in `.claude/skills/find-prompt/SKILL.md` must have a row for every prompt.

### No Vague Advice Rule

Every recommendation should end with a concrete:
- decision, or
- tool, or
- validation step.

### Currency Rule

- Verify Claude Code features, commands, and model IDs against `code.claude.com/docs` and `platform.claude.com/docs` — never from memory.
- Do not reference retired models (`claude-3-*`, `claude-opus-4-1`, `claude-sonnet-4-0`, `gpt-4o`) as current.
- State framework versions only after checking the current stable release.

Use this measurable checklist for prompt reviews:
- [Prompt Review Checklist](prompts/english/workflows/prompt-review-checklist.md)

## Archive Workflow

If a prompt is low-value or overlapping:
1. Classify as keep / merge / archive
2. Move to `prompts/english/agents/archive/`
3. Update active indexes and README
4. Add rationale to archive index

## Required PR Checklist

Copy this checklist into your PR description and complete all items:

- [ ] Markdown renders correctly
- [ ] No spelling or grammar errors
- [ ] Internal relative links resolve
- [ ] Hypothetical example paths are plain code literals (not Markdown links)
- [ ] Catalog/index entries are updated (`README.md`, both INDEX files, `prompts/english/workflows/INDEX.md`, `project-types/INDEX.md`)
- [ ] `llms.txt` and `REPOSITORY-MAP.md` updated when adding/removing/renaming a prompt
- [ ] New prompts have the `Use this when` / `Skip to` header and a `~token` estimate in the agent catalog
- [ ] No vague advice language; no model/version claims stated from memory
- [ ] Prompt changes pass `Role / Protocol / Phases / Remember` review checklist
- [ ] Navigation consistency checked across `README.md`, `prompts/english/INDEX.md`, `prompts/english/agents/INDEX.md`, `prompts/english/workflows/INDEX.md`, and `llms.txt`
- [ ] Markdown lint passed: `npx markdownlint-cli2 '**/*.md'`

Optional local checks:

```bash
grep -r '\[.*\](.*\.md)' prompts/ | head
npx markdownlint-cli2 '**/*.md'
```

## Commit Message Style

```text
feat: add new prompt
fix: correct catalog link
docs: improve usage guidance
update: archive overlapping prompt
```
