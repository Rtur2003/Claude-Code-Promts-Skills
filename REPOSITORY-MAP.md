# Repository Map

30-second orientation. Resolve your task to one file, open it, act. Do not read the whole repo.

**Running Claude Code in this repo?** Invoke `/find-prompt <your task>` — it routes any task to the exact prompt(s) to load, in one step. Skill lives at `.claude/skills/find-prompt/`. Four more real, tested skills ship alongside it in `.claude/skills/` — `deterministic-checks`, `changelog-from-commits`, `doc-link-audit`, `skill-audit` — each a script, not a prompt describing one.

## What this repo is

A prompt library for Claude coding agents. Pure Markdown. English only. Built on the APEI cycle (Analyze -> Plan -> Execute -> Iterate). Every prompt follows `## Role` -> `## Protocol` -> `## Phases` -> `## Remember` and ends every recommendation with a concrete decision, tool, or check.

## Fast lookup

| I need... | Open |
|---|---|
| The default operational prompt | `prompts/english/agents/claude-agent-system-prompt.md` |
| To route any task to the right prompt | `prompts/english/INDEX.md` |
| To pick a Claude model / effort level | `prompts/english/workflows/model-selection-guide.md` |
| To know what current Claude Code can do | `prompts/english/workflows/claude-code-native-features-guide.md` |
| To write a skill / set up MCP / build a plugin / write hooks | `prompts/english/agents/` (`agent-skills`, `mcp-integration`, `claude-code-plugins`, `hooks-automation`) |
| To run parallel agents or a dynamic workflow | `prompts/english/agents/multi-agent-orchestration-prompt.md` |
| To build a specific kind of app | `prompts/english/project-types/` |
| To improve existing code (review, debug, refactor, test, perf) | `prompts/english/agents/` specialist prompts |
| Composition examples | `prompts/english/examples/` |
| The Anthropic docs/blog sources + AGENTS.md interop + tool comparison | `prompts/english/workflows/reference-resources.md` |
| Governance / contribution rules | `CONTRIBUTING.md`, `prompts/english/workflows/prompt-review-checklist.md` |

## Directory layout

| Path | Contents |
|---|---|
| `README.md` | Catalog, portfolio table, common combinations |
| `prompts/english/INDEX.md` | Global task -> file router |
| `prompts/english/agents/` | 35 active prompts: the Agent System, Claude Code operation (Skills, MCP, Plugins, Subagents+Workflows, Hooks, Workflow, Thinking), and development specialists |
| `prompts/english/agents/INDEX.md` | Agent catalog with token counts and a task router |
| `prompts/english/agents/archive/` | Archived prompts + merge rationale |
| `prompts/english/base/` | Foundation prompt (universal best practices) |
| `prompts/english/project-types/` | 11 domain prompts (web, API, mobile, desktop, data/ML, DevOps, DB, game, embedded, blockchain, general) |
| `prompts/english/examples/` | Real usage walkthroughs |
| `prompts/english/workflows/` | Model selection, native features, Agent SDK, APEI, setup, selection, troubleshooting, maintenance |
| `prompts/english/workflows/INDEX.md` | Workflow guide catalog |
| `llms.txt` | Full LLM router index |
| `CHANGELOG.md` | Version history |
| `CLAUDE.md` | Project memory for anyone working on this repo |
| `.claude-plugin/plugin.json` | Plugin manifest — makes this repo `claude --plugin-dir`-installable |
| `hooks/` | Working `PreToolUse` scripts wired via `hooks/hooks.json` (block destructive commands, block secret writes) |
| `.claude/skills/` | 5 real skills: `find-prompt` (routing), `deterministic-checks`, `changelog-from-commits`, `doc-link-audit`, `skill-audit` — each ships an actual script |
| `evals/` | Routing-accuracy regression tests for `find-prompt` — 20 cases, static + live tiers, run in CI |
| `.github/workflows/quality-gate.yml` | CI: markdownlint, link audit, skill audit, deterministic-checks, plugin validation, routing eval — every PR |

## How to use the library

1. Start with **Agent System** (`prompts/english/agents/claude-agent-system-prompt.md`).
2. Add specialists by tier — 1 for a single-domain task (default), 2 only for two genuinely independent domains, Multi-Agent Orchestration for isolation/review work.
3. For Claude Code setup, add the relevant operation prompt (Skills / MCP / Hooks / Workflow).
4. Validate every output against explicit success criteria before adding more prompts.

Composition tiers + conflict precedence: `prompts/english/workflows/prompt-selector-guide.md`.
