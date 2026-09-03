# Reference Resources

> **Anthropic Canon** | **Cross-Tool Interop** | **What Else to Read**

**Use this when:** you want the authoritative source behind a recommendation in this library, or you need to make one config work across Claude Code, Cursor, Codex, and Aider.
**Skip to:** [Anthropic canon](#anthropic-canon) · [Cross-tool config](#cross-tool-config-agentsmd) · [Community catalogs](#community-catalogs) · [Adjacent tools](#adjacent-coding-agents) · [Remember](#remember)

## Role

You point people at the primary source instead of paraphrasing it. Every prompt in this library derives from the material below — when a recommendation is questioned, cite the source, don't re-argue it.

## Protocol: CITE

```
C → CHECK   — Is there an official Anthropic doc or engineering post for this? Link it
I → INTEROP — Does the user run more than one coding agent? Point them at AGENTS.md
T → TRIM    — Link the one resource that answers the question, not a reading list
E → EXAMINE — Community catalogs are unvetted; treat star counts as noise, patterns as signal
```

---

## Anthropic canon

The material this library is built on. Verify any Claude Code or model claim here before stating it.

| Resource | What it is | URL |
|---|---|---|
| Claude Code docs | The product reference — commands, hooks, MCP, skills, plugins, permissions | `code.claude.com/docs` |
| Claude Code changelog | Per-version feature and fix log | `code.claude.com/docs/en/changelog` + `github.com/anthropics/claude-code/blob/main/CHANGELOG.md` |
| Claude Code best practices | The workflow guidance (verification, explore-plan-code, context management, failure patterns) | `code.claude.com/docs/en/best-practices` |
| Models overview | Current model IDs, context windows, pricing, retirement dates | `platform.claude.com/docs/en/models/overview` |
| Model deprecations | Lifecycle status and retirement commitments | `platform.claude.com/docs/en/about-claude/model-deprecations` |
| Choosing a model | Which model and effort level for which work | `platform.claude.com/docs/en/about-claude/models/choosing-a-model` |
| **Building Effective Agents** | The five composable patterns: prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer | `anthropic.com/research/building-effective-agents` |
| Effective context engineering for AI agents | Why context is the scarce resource and how to manage it | `anthropic.com/engineering` (context-engineering post) |
| Writing effective tools for AI agents | Tool-definition design; why tool schemas and chained results both cost context | `anthropic.com/engineering/writing-tools-for-agents` |
| Code execution with MCP | Have the agent write code that calls MCP tools instead of threading every raw result through context | `anthropic.com/engineering` (code-execution-with-mcp post) |
| Claude Cookbook | 80+ runnable recipes — tool use, agents, evals, RAG, multimodal, skills | `platform.claude.com/cookbook` |
| Anthropic courses | Structured curriculum on building agents, evals, multi-agent systems | `github.com/anthropics/courses` |
| Prompt engineering interactive tutorial | Runnable lessons from basics to advanced | `github.com/anthropics/prompt-eng-interactive-tutorial` |
| anthropics/skills | The official Agent Skills library and `package_skill.py` | `github.com/anthropics/skills` |
| Agent Skills spec | The open standard skills follow (`agentskills.io`) | `agentskills.io` |
| Agent SDK docs | Claude Code as a library — `@anthropic-ai/claude-agent-sdk`, `claude-agent-sdk` | `code.claude.com/docs/en/agent-sdk/overview` |
| `/claude-api` bundled skill | In-session API reference: model IDs, pricing, params, migration | run `/claude-api` in Claude Code |

---

## Cross-tool config (AGENTS.md)

In 2026 the major coding-agent vendors (Google, OpenAI, Sourcegraph, Cursor, Factory, and others) converged on **`AGENTS.md`** as a shared, tool-neutral instructions file. Claude Code reads `CLAUDE.md`, not `AGENTS.md` — but you can make one file serve every tool.

**If your repo already has `AGENTS.md`:**

```markdown
# CLAUDE.md
@AGENTS.md

## Claude Code

Use plan mode for changes under src/billing/.
```

Claude loads the imported `AGENTS.md` at session start, then appends the Claude-specific lines. A symlink also works (`ln -s AGENTS.md CLAUDE.md`) when you have no Claude-specific content; on Windows use the import.

**If you're standardizing a repo for multiple agents:** put the shared instructions in `AGENTS.md`, keep each tool's file (`CLAUDE.md`, `.cursor/rules/`, Devin Knowledge) as a thin wrapper that imports it plus its own extras. `/init` with `CLAUDE_CODE_NEW_INIT=1` reads `AGENTS.md`, Cursor rules, and Copilot instructions; `/import` brings another agent's full config (MCP servers, commands, subagents, skills) into Claude Code.

---

## Community catalogs

Unvetted, community-maintained. Useful for discovery; verify anything before adopting it. Ignore star counts.

| Catalog | Covers |
|---|---|
| `PatrickJS/awesome-cursorrules` | 250+ stack-specific rule files — a good source of per-stack conventions to adapt into `.claude/rules/` |
| `x1xhlol/system-prompts-and-models-of-ai-tools` | Published system prompts of ~28 coding agents — reference for how other tools are steered |
| `rohitg00/awesome-claude-code-toolkit`, `jqueryscript/awesome-claude-code`, `hesreallyhim/awesome-claude-code` | Curated skills, subagents, hooks, MCP servers, plugins |
| `appcypher/awesome-mcp-servers`, `wong2/awesome-mcp-servers` | MCP server directories (also `claude.ai/directory` for reviewed connectors) |
| `humanlayer/12-factor-agents` | Architecture principles: production agents blend deterministic code with strategic LLM decision points, not a pure agentic loop |

**Spec-driven development frameworks** (heavier than this library's "interview → SPEC.md → fresh session" flow): GitHub `spec-kit`, BMAD-METHOD, Kiro, Tessl. Use one when a team needs an enforced spec → design → tasks → implementation pipeline.

---

## Adjacent coding agents

Where each still wins over Claude Code, per practitioners in 2026. Useful when advising a team on tooling, not just when using Claude Code.

| Tool | Wins when |
|---|---|
| **Claude Code** | Terminal-first workflow, 1M-context whole-codebase reasoning, deepest reasoning, architecture-level work |
| **Cursor** | You want an IDE not a CLI; mixing Claude + GPT + Gemini in one tool; visual side-by-side review |
| **Codex** (OpenAI) | Async PR delivery — long-running tasks in the cloud; team already on ChatGPT |
| **Aider** | Refusing vendor lock-in; git-first; transparent per-call cost control; BYO API key; measurably lower token use on some tasks |
| **Cline / Roo Code** | Lightweight VS Code extension, multi-model, free tier |

Claude Code's cost can run away in agentic loops. Watch `/context` and `/usage`, cap unattended runs, and test a fan-out on one directory before the whole repo.

---

## Remember

> **Cite the primary source. This library paraphrases Anthropic's material so you can act fast — but the docs are the authority, and they change.**

1. Before stating a model ID, version, or Claude Code feature, check the doc — never from memory
2. If the user runs more than one agent, `AGENTS.md` + a thin `CLAUDE.md` wrapper beats maintaining parallel configs
3. Community catalogs are for discovery; the star count is noise
