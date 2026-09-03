# Quick Start

## Start Rule (Do This First)

**Start minimal, then add one specialist only if quality gates fail.**

Before selection, read [REPOSITORY-MAP.md](REPOSITORY-MAP.md) for one-file navigation.

---

## 30-Second Copy-Paste Start

### Autonomous Agent Tasks

```text
[Paste Agent System prompt]
Task: <what you need done>
Success criteria: <measurable outcomes>
Constraints: <scope/risk/time>
```

### Interactive Session Tasks

```text
[Paste Foundation prompt + one project-type prompt]
Task: <what you need done>
Start with Analyze.
```

---

## 1) Base Setup

| Situation | Prompt Setup |
|-----------|--------------|
| Any autonomous coding task | **Agent System** ⭐ |
| Tight token budget | **Quick Reference** |
| Claude Code setup (CLAUDE.md, permissions) | Agent System + **Claude Code Workflow** |
| Write a skill / set up MCP / build a plugin / write hooks | **Agent Skills** / **MCP Integration** / **Claude Code Plugins** / **Hooks & Automation** |
| Pick a model or effort level | **Model Selection Guide** |
| Production debugging | Agent System + **Debugging & Troubleshooting** |
| Security-sensitive task | Agent System + **Security Audit** |

Decision tree source: [Prompt Selector Guide](prompts/english/workflows/prompt-selector-guide.md)
Modern Claude Code coverage: [REPOSITORY-MAP.md](REPOSITORY-MAP.md) fast lookup, or [prompts/english/INDEX.md](prompts/english/INDEX.md) task router.

## 2) Add One Specialist Only If Needed

Need criteria: add a specialist only when Agent System alone cannot provide domain-specific protocols for your task.

| Need | Add |
|------|-----|
| Architecture decisions | Architecture Patterns |
| Tool/library selection | Technology Stack |
| Multi-agent parallel flow | Multi-Agent Orchestration |
| Performance bottlenecks | Performance Optimization |
| Reliability hardening | Error Handling & Resilience |

## 3) Typical Flows

### A) General implementation flow

1. Agent System
2. Define measurable success criteria
3. Add one specialist only if blocked

### B) Production debugging flow

1. Agent System + Debugging & Troubleshooting
2. Reproduce issue
3. Validate fix with explicit checks

### C) Security review flow

1. Agent System + Security Audit
2. Enumerate threats and findings
3. Apply remediations and verify risk reduction

## 4) Use APEI Loop

```text
ANALYZE → PLAN → EXECUTE → ITERATE
```

## 5) Token Budget

| Budget | Setup |
|--------|-------|
| < 2K | Quick Reference only |
| 2K–8K | Agent System |
| 8K+ | Agent System + 1 specialist |

## 6) Catalogs

- [Active Agent Index](prompts/english/agents/INDEX.md)
- [Archived Prompt Index](prompts/english/agents/archive/INDEX.md)
- [Global Prompt Index](prompts/english/INDEX.md)
- [LLM Index](llms.txt)
- [Repository Map](REPOSITORY-MAP.md)
