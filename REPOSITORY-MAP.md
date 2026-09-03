# Repository Map

30-second orientation. Resolve your task to one file, open it, act. Do not read the whole repo.

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

## How to use the library

1. Start with **Agent System** (`prompts/english/agents/claude-agent-system-prompt.md`).
2. Add **one** specialist or project-type prompt only if the task clearly needs it.
3. For Claude Code setup, add the relevant operation prompt (Skills / MCP / Hooks / Workflow).
4. Validate every output against explicit success criteria before adding more prompts.

Selection tree: `prompts/english/workflows/prompt-selector-guide.md`.
