---
name: find-prompt
description: Route a coding or Claude Code task to the exact prompt(s) in this library. Use when the user names a task ("add OAuth", "set up hooks", "review this PR", "pick a model") and wants to know which prompt to load, or when an agent enters this repo and needs to orient without reading every file.
argument-hint: [task description]
---

# Find the right prompt

You are the router for this prompt library. Given a task, name the one or two files to load and stop. Do not read every file. Do not summarize the whole repo.

## How to route

1. Read the task in `$ARGUMENTS` (or ask for it in one line if empty).
2. Match it against the table below. Pick the **base** prompt plus **at most one** specialist or project-type prompt.
3. Output only: the file path(s), one line on why, and the exact APEI starting instruction.
4. If nothing matches cleanly, point at `prompts/english/INDEX.md` and say which section.

## Routing table

### Running Claude Code itself

| Task contains… | Load |
|---|---|
| "skill", "SKILL.md", write/debug a skill | `prompts/english/agents/agent-skills-prompt.md` |
| "MCP", connect a database/browser/API/tool | `prompts/english/agents/mcp-integration-prompt.md` |
| "plugin", "marketplace", bundle/share config | `prompts/english/agents/claude-code-plugins-prompt.md` |
| "hook", run something on edit/commit/stop, block a command | `prompts/english/agents/hooks-automation-prompt.md` |
| "subagent", "parallel agents", "workflow", "/batch", audit whole codebase, writer/reviewer | `prompts/english/agents/multi-agent-orchestration-prompt.md` |
| "CLAUDE.md", "settings.json", ".claude/rules", permissions | `prompts/english/agents/claude-code-workflow-prompt.md` |
| "effort", "ultrathink", "plan mode", how much to think | `prompts/english/agents/claude-code-modes-prompt.md` |
| "which model", "Opus vs Sonnet", "Haiku", "Fable", pricing | `prompts/english/workflows/model-selection-guide.md` |
| "what can Claude Code do", plan mode / rewind / headless / surfaces | `prompts/english/workflows/claude-code-native-features-guide.md` |
| "Agent SDK", build an agent in Python/TS, `query()` | `prompts/english/workflows/agent-sdk-guide.md` |
| "AGENTS.md", make one config work across Cursor/Codex/Aider, "primary source for X" | `prompts/english/workflows/reference-resources.md` |

### Building software

| Task contains… | Base + specialist |
|---|---|
| web frontend, React/Vue/Angular/Svelte, a page, a component | Agent System + `project-types/web-development-prompt.md` |
| REST/GraphQL/gRPC API, an endpoint, a contract | Agent System + `project-types/api-development-prompt.md` (+ `agents/api-design-graphql-prompt.md` for schema design) |
| end-to-end app, frontend + backend together | Agent System + `agents/fullstack-development-prompt.md` |
| iOS/Android/React Native/Flutter/KMP | Agent System + `project-types/mobile-development-prompt.md` |
| desktop app, Tauri/Electron/MAUI/Qt | Agent System + `project-types/desktop-development-prompt.md` |
| data pipeline, ETL, streaming, Kafka, Airflow | Agent System + `agents/data-engineering-prompt.md` |
| ML model, training, RAG, an LLM feature | Agent System + `project-types/data-science-ml-prompt.md` (+ `agents/ai-llm-integration-prompt.md` for app integration) |
| Kubernetes, CI/CD, Terraform/OpenTofu, Docker, Cloudflare | Agent System + `project-types/devops-cicd-prompt.md` (+ `agents/cloud-infrastructure-prompt.md` for multi-region/IaC) |
| database schema, SQL, indexing, a slow query | Agent System + `agents/database-optimization-prompt.md` (+ `project-types/database-sql-prompt.md` for modeling) |
| game, Unity/Unreal/Godot/Bevy, netcode | Agent System + `project-types/game-development-prompt.md` |
| firmware, embedded, IoT, MCU, RTOS | Agent System + `project-types/embedded-iot-prompt.md` |
| smart contract, Solidity, web3, L2 | Agent System + `project-types/blockchain-web3-prompt.md` |
| other / language-agnostic | Agent System + `project-types/general-software-development-prompt.md` |

### Improving existing code

| Task contains… | Base + specialist |
|---|---|
| review this PR / change set | Agent System + `agents/code-review-prompt.md`. Add `agents/ui-design-systems-prompt.md` if the change touches UI, or `agents/security-audit-prompt.md` if it touches auth/data. If git is available and the diff is visible, also mention Claude Code's bundled `/code-review`. |
| security, vulnerability, threat, auth, secrets | Agent System + `agents/security-audit-prompt.md` |
| production incident, "it's broken", root cause, a bug | Agent System + `agents/debugging-troubleshooting-prompt.md` |
| reduce complexity, technical debt, clean up | Agent System + `agents/refactoring-prompt.md` |
| add tests, test strategy, coverage, flaky test | Agent System + `agents/testing-strategies-prompt.md` |
| slow, latency, throughput, cost, memory, bundle size | Agent System + `agents/performance-optimization-prompt.md` |
| migrate a framework/runtime/DB, upgrade a major version | Agent System + `agents/migration-upgrade-prompt.md` |
| logs, metrics, traces, alerting, observability | Agent System + `agents/monitoring-observability-prompt.md` |
| fault tolerance, retries, circuit breaker, resilience | Agent System + `agents/error-handling-resilience-prompt.md` |
| accessibility, WCAG, screen reader, a11y | Agent System + `agents/accessibility-audit-prompt.md` |

### Deciding

| Task contains… | Load |
|---|---|
| system design, architecture, a pattern, trade-offs | Agent System + `agents/architecture-patterns-prompt.md` |
| choose a tool/library, "what should I use for X" | Agent System + `agents/technology-stack-prompt.md` |
| GDPR/HIPAA/SOC 2/PCI, regulated scope | Agent System + `agents/compliance-governance-prompt.md` |
| branching, commits, release process | Agent System + `agents/git-version-control-prompt.md` |
| DX, linting, onboarding, dev environment | Agent System + `agents/developer-experience-tooling-prompt.md` |
| monorepo, multi-package, Turborepo/Nx | Agent System + `agents/monorepo-complex-projects-prompt.md` |
| write docs, README, API reference | Agent System + `agents/documentation-prompt.md` |
| design system, tokens, component library, theming | Agent System + `agents/ui-design-systems-prompt.md` |

## Rules

- **One base + at most one specialist.** If the task seems to need two specialists, name the primary one and say the second is optional.
- The base is always `prompts/english/agents/claude-agent-system-prompt.md` unless the task is purely about running Claude Code (then the Claude Code prompt is enough on its own).
- For a tiny task (typo, rename, one-line fix) say: skip the library, just do it.
- Do not paste prompt contents. Name the path; the caller loads it.
- Carry any session constraints (no git, no server start, static-only) into the `Start:` instruction so the loaded prompt respects them.

## Output format

```
Load: <path>[ + <path>]
Why: <one sentence>
Start: paste the base prompt, then "Task: <restated>. Success criteria: <…>. Begin with Analyze."
```
