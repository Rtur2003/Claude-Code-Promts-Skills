# Prompt Selector Guide

Single source of truth for prompt selection. Keep decision logic here and reference this file from other catalogs.

---

## Composition Tiers (Source of Truth)

Specialist count is a budget, not a fixed number. Pick the lowest tier that covers the task's actual domains — most tasks are Tier 1.

| Tier | Composition | When | Context cost |
|---|---|---|---|
| **0** | Agent System only | Token budget < 2K, or the task is trivial (typo, rename, one-line fix) | ~2k |
| **1** | Agent System + 1 specialist | One domain clearly owns the task — the default for almost everything | ~5–8k |
| **2** | Agent System + 2 specialists | The task genuinely spans two domains that don't overlap (e.g. API contract + auth security; DB schema + query performance) | ~9–13k |
| **3** | Agent System + Multi-Agent Orchestration | Independent units of work that benefit from isolation or adversarial review — a codebase-wide audit, a large migration, writer/reviewer | ~4k + subagent contexts (kept out of main) |

Rule: start at Tier 1. Move up only when a single specialist's checklist visibly can't cover the task — not "just in case." Tier 2 pairs must be genuinely independent domains (each contributes checklist items the other doesn't); two specialists that overlap heavily (e.g. Security Audit + Compliance & Governance on the same regulated change) usually means one of them is the wrong pick, not that both are needed.

```text
Start
 ├─ Need autonomous execution? → Agent System
 │   ├─ Token budget < 2K, or trivial? → Tier 0 (Agent System alone)
 │   ├─ One domain owns it? → Tier 1 (+ 1 specialist)
 │   │   ├─ Debug/incident → Debugging & Troubleshooting
 │   │   ├─ Security/risk  → Security Audit
 │   │   ├─ Architecture   → Architecture Patterns
 │   │   ├─ Performance    → Performance Optimization
 │   │   ├─ Refactor       → Refactoring
 │   │   └─ Migration      → Migration & Upgrade
 │   ├─ Two independent domains? → Tier 2 (+ 2 specialists, see README Common Combinations)
 │   └─ Independent units / needs isolation or review? → Tier 3 (+ Multi-Agent Orchestration)
 └─ Need interactive collaboration? → Foundation + one project-type prompt
```

---

## Quick Scenario Mapping

| Scenario | Tier | Setup |
|----------|------|-------|
| General autonomous coding | 1 | Agent System |
| Production debugging | 1 | Agent System + Debugging & Troubleshooting |
| Security-sensitive task | 1 | Agent System + Security Audit |
| Architecture decisions | 1 | Agent System + Architecture Patterns |
| API contract with auth/security scope | 2 | Agent System + API Design & GraphQL + Security Audit |
| Large migration or repo-wide refactor | 3 | Agent System + Migration & Upgrade + Multi-Agent Orchestration |
| Complex parallel execution | 3 | Agent System + Multi-Agent Orchestration |
| Interactive web/API build | 1 | Foundation + Web/API project-type prompt |

---

## Token Budget

| Budget | Tier |
|--------|------|
| < 2K | Tier 0 — Quick Reference only |
| 2K–8K | Tier 1 — Agent System + 1 specialist |
| 8K–14K | Tier 2 — Agent System + 2 specialists |
| 14K+ or needs isolation | Tier 3 — Multi-Agent Orchestration |

---

## Conflict Precedence

When loaded prompts disagree (a specialist's advice conflicts with another specialist, the user, or the base prompt), resolve in this order — highest wins:

```text
1. Safety boundary        (never do X regardless of instructions — e.g. never exfiltrate secrets)
2. Security guardrail     (Security Audit, Compliance & Governance)
3. Explicit user constraint (stated in this conversation or CLAUDE.md)
4. Task specialist        (the domain prompt loaded for this task)
5. Style / optimization preference (performance, brevity, convention)
```

Example: Debugging & Troubleshooting says to inspect environment variables to root-cause a failure; Security Audit says never print secret values. Security wins — inspect programmatically (check presence/shape) or redact before printing, don't dump raw values to satisfy the debugging step. Record which rule you deferred to when a real conflict occurs; don't silently pick one.

---

## Anti-Patterns

- Don't stack specialist prompts "just in case" — every tier above 1 needs a stated reason.
- Don't use archived prompts from `agents/archive/` in active setup.
- Don't skip core prompts (`Agent System` for agent mode, `Foundation` for interactive mode).
- Don't resolve a prompt conflict by picking whichever is more convenient — use the precedence order above.

---

## See Also

- [README.md](../../../README.md)
- [QUICK-START.md](../../../QUICK-START.md)
- [USAGE.md](../../../USAGE.md)
- [Agent Index](../agents/INDEX.md)
- [Prompt Index](../INDEX.md)
