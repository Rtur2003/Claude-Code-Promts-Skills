# AGENTS.md

## Project Overview
- **Name**: Claude Code Prompts
- **Type**: Prompt library (Markdown-first) plus tested scripts bundled as Claude Code and cross-agent skills (`.claude/skills/`, `.agents/skills/`) and safety hooks
- **Purpose**: Production-ready system prompts for Claude Code, with cross-agent discovery through `AGENTS.md`, `.agents/skills/`, and `llms.txt`
- **Core Methodology**: APEI cycle — Analyze → Plan → Execute → Iterate
- **License**: MIT
- **Language**: English only

## Routing skill

`.claude/skills/find-prompt/SKILL.md` is the canonical routing table. `.agents/skills/find-prompt/SKILL.md` is a thin cross-agent adapter. Keep the canonical table, indexes, `llms.txt`, and eval cases in sync whenever a prompt is added, removed, or renamed.

## Repository Structure

```
├── AGENTS.md              # This file — project memory
├── README.md              # Main catalog, portfolio table, common combinations
├── REPOSITORY-MAP.md      # 30-second orientation, task -> file lookup
├── QUICK-START.md         # 30-second setup guide
├── USAGE.md               # Scenario-based prompt composition
├── CONTRIBUTING.md        # Contribution guidelines
├── CHANGELOG.md           # Version history (current: 2.2.0)
├── llms.txt               # Full LLM router index
├── .claude-plugin/
│   ├── plugin.json        # Claude Code plugin manifest
│   └── marketplace.json   # Installable marketplace catalog
├── hooks/
│   ├── hooks.json          # PreToolUse wiring
│   └── scripts/            # block-destructive-commands.sh, block-secret-writes.sh
├── .claude/skills/        # 6 Claude Code skills
│   ├── find-prompt/
│   ├── deterministic-checks/
│   ├── changelog-from-commits/
│   ├── doc-link-audit/
│   ├── skill-audit/
│   └── capability-audit/
├── .agents/skills/        # Cross-agent adapters / mirrored deterministic skills
├── evals/                  # find-prompt routing-accuracy regression tests (static + live tiers)
├── .github/workflows/
│   └── quality-gate.yml    # CI: lint, link audit, skill audit, deterministic-checks, plugin validate, routing eval
└── prompts/
    └── english/
        ├── INDEX.md           # Global task -> file router
        ├── agents/            # Active agent prompts + compatibility stubs
        │   ├── INDEX.md       #   catalog with token counts + task router
        │   └── archive/       # Archived prompts removed from active catalog
        ├── base/              # Foundation prompt (universal best practices)
        ├── project-types/     # Domain-specific prompts (11 files)
        ├── examples/          # Real-world usage examples
        └── workflows/         # Model selection, native features, Agent SDK,
            └── INDEX.md       #   APEI, selection, troubleshooting, setup, maintenance
```

### Claude Code operation prompts (agents/)

The library covers the current Claude Code / Claude ecosystem. Keep these accurate against `code.claude.com/docs` and `platform.claude.com/docs`:

- `agent-skills-prompt.md` — SKILL.md authoring
- `mcp-integration-prompt.md` — MCP servers, scopes, auth, injection safety
- `claude-code-plugins-prompt.md` — plugin.json, marketplaces
- `multi-agent-orchestration-prompt.md` — native subagents + dynamic workflows
- `hooks-automation-prompt.md` — hook events and settings.json schema
- `claude-code-workflow-prompt.md` — CLAUDE.md, rules, settings, permissions
- `claude-code-modes-prompt.md` — adaptive thinking, effort, plan mode
- `workflows/model-selection-guide.md` — model lineup and effort
- `workflows/claude-code-native-features-guide.md` — the current feature surface
- `workflows/agent-sdk-guide.md` — the Claude Agent SDK

## File Naming Conventions

| Type | Format | Example |
|------|--------|---------|
| Prompts | `kebab-case-prompt.md` | `code-review-prompt.md` |
| Guides | `kebab-case-guide.md` | `iterative-development-guide.md` |
| Index files | `INDEX.md` | `INDEX.md` |

## Prompt Structure Standards

Every prompt follows this template:

```markdown
# Prompt Title

> **Key Feature 1** | **Key Feature 2** | **Key Feature 3**

## Role
[Define what this prompt does]

## Protocol / Core Loop
[Main workflow — often uses a protocol acronym]

## Phases
[Phase details with templates and checklists]

## Remember
[Key takeaways — always the final section]
```

Key elements:
- **Protocol acronym**: Each prompt defines a memorable acronym for its core loop
- **Phases**: Detailed steps with Markdown templates and `- [ ]` checklists
- **Tables**: Used for options, comparisons, and structured data
- **Code blocks**: Used for command examples, templates, and diagrams
- **Remember section**: Closing callout with priority rules (always last)

## Markdown Style Guide

- Use `#` for title, `##` for major sections, `###` for subsections
- Tables for structured data (catalogs, options, comparisons)
- `> **bold text**` for callout/subtitle lines under the title
- Fenced code blocks with language tags where applicable
- `- [ ]` checklists inside phases
- `---` horizontal rules to separate major sections
- Keep prompts concise — include token count in catalog tables
- Use `⭐` emoji only for recommended/primary prompts in catalogs

## Build & Development

No build system for the prompts themselves. The bundled skill/hook scripts under `.claude/skills/*/scripts/` and `hooks/scripts/` are standalone (bash/Python, no install step, no dependency beyond what's noted in each `SKILL.md`).

- **Install**: `git clone` the repo, or `claude --plugin-dir <path>` to try it as a plugin
- **Validate links**: `python3 .claude/skills/doc-link-audit/scripts/check_links.py .` — real link/anchor checker, not a grep spot-check
- **Validate formatting**: Open `.md` files in a Markdown previewer
- **Lint**: `npx markdownlint-cli2 '**/*.md'`
- **Pre-commit scan**: `bash .claude/skills/deterministic-checks/scripts/scan.sh .`
- **Skill quality check**: `python3 .claude/skills/skill-audit/scripts/audit.py .claude/skills`
- **Plugin checks**: `claude plugin validate .claude-plugin/plugin.json` and `claude plugin validate .claude-plugin/marketplace.json`

## Bundled skills and scripts

`.claude/skills/` ships 6 skills: `find-prompt`, 4 deterministic repository checks, and `capability-audit`. `.agents/skills/` exposes the library to other agent hosts without maintaining a second routing table. `hooks/` ships 2 `PreToolUse` safety scripts. Keep the catalogs, adapters, routing cases, and scripts synchronized; test scripts against real input before documenting them as working.

## Common Tasks

### Add a new agent prompt
1. Create `prompts/english/agents/your-topic-prompt.md` using the template above; open with a "Use this when" line and a "Skip to" anchor list
2. Update `prompts/english/agents/INDEX.md` — the task router and the catalog table (with a ~token estimate)
3. Update `prompts/english/INDEX.md` task router
4. Add a row to `.claude/skills/find-prompt/SKILL.md` and a routing eval case
5. Add entry to the portfolio table and, if it is a recurring pairing, the Common Combinations table in `README.md`
6. Add a line to `llms.txt` and `REPOSITORY-MAP.md`

### Add a new project-type prompt
1. Create `prompts/english/project-types/your-domain-prompt.md`
2. Update `prompts/english/INDEX.md`
3. Add entry to the Foundation & Project Prompts table in `README.md`
4. Add relevant combinations to the Common Combinations table in `README.md`

### Add a usage example
1. Create a new file in `prompts/english/examples/`
2. Show real-world prompt usage with context and expected output

### Update documentation
1. Edit the relevant `.md` file
2. Ensure all relative links still resolve
3. Keep `CHANGELOG.md` updated for notable changes

### Archive overlapping prompts
1. Classify prompt as keep / merge / archive
2. Move archived prompt to `prompts/english/agents/archive/`
3. Add archive rationale in `prompts/english/agents/archive/INDEX.md`
4. Update active catalogs (`README.md`, `prompts/english/agents/INDEX.md`, `prompts/english/INDEX.md`)

## Quality Checklist

Before submitting changes:
- [ ] Content is accurate and follows best practices
- [ ] Markdown renders correctly (check headers, tables, code blocks)
- [ ] No spelling or grammar errors
- [ ] INDEX files updated if adding/removing prompts
- [ ] All relative links resolve to existing files
- [ ] Follows existing naming conventions (`kebab-case-prompt.md`)
- [ ] New prompts include Role, Protocol, Phases, and Remember sections
- [ ] README.md catalog tables updated if adding new prompts
- [ ] Recommendations are concrete (no vague advice)

## Commit Messages

```
feat: add security audit prompt       # New features
fix: correct typo in API prompt        # Fixes
docs: improve README examples          # Documentation
update: enhance code review checklist  # Updates
```

## Things to Avoid

- Don't add non-English content — this repo is English only
- Don't add code beyond the bundled skill/hook scripts (`.claude/skills/*/scripts/`, `hooks/scripts/`) — the prompt content itself stays pure Markdown; a script added there must ship inside a skill with a `SKILL.md` documenting it, be dependency-free or note its dependency explicitly, and be tested against real input before being documented as working
- Don't deviate from the APEI methodology in prompt design
- Don't remove the Remember section from prompts
- Don't use absolute URLs for internal links — use relative paths
- Don't cite Claude Code features, commands, or model IDs from memory — verify against `code.claude.com/docs` / `platform.claude.com/docs`
- Don't reference retired models (`claude-3-*`, `claude-opus-4-1`, `claude-sonnet-4-0`, `gpt-4o`) as current
- Don't add filler or AI-cliché phrasing; every sentence carries information
