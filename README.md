# Claude Code Prompts

Production-ready prompt library for Claude AI and coding agents, built on the **APEI cycle**: Analyze → Plan → Execute → Iterate.

**Repository default is English-only and remains enforced to keep quality, tone, and contribution standards consistent across all prompts.**

---

## Start Here

0. Open **[REPOSITORY-MAP.md](REPOSITORY-MAP.md)** for one-file navigation.
1. Use **Agent System** as the core prompt.
2. Add **one** specialist prompt only when the task clearly needs it.
3. Validate outputs against explicit success criteria.

### Top 5 Outcome Scenarios

| Scenario | Prompt Setup |
|----------|--------------|
| General autonomous coding | Agent System |
| Debugging production issues | Agent System + Debugging & Troubleshooting |
| Security-sensitive changes | Agent System + Security Audit |
| Architecture decisions | Agent System + Architecture Patterns |
| Complex multi-agent execution | Agent System + Multi-Agent Orchestration |

---

## One Decision Tree + Token Budget

Use the single-source selector here: [Prompt Selector Guide](prompts/english/workflows/prompt-selector-guide.md).

Rule: start minimal, then add exactly one specialist only if quality gates fail.

---

## Active Agent Portfolio (Outcome-First)

> `claude-agent-system-prompt.md` is the operational source of truth.

| Prompt | Use when | Do not use when | File |
|--------|----------|-----------------|------|
| Agent System ⭐ | Any autonomous task | You only need a tiny cheat sheet | [View](prompts/english/agents/claude-agent-system-prompt.md) |
| Quick Reference | Token budget is extremely tight | You need deep specialist logic | [View](prompts/english/agents/agent-quick-reference.md) |
| Code Review | Reviewing a PR/change set | Writing new feature code from scratch | [View](prompts/english/agents/code-review-prompt.md) |
| Security Audit | Threat/risk exposure is possible | Task has no security relevance | [View](prompts/english/agents/security-audit-prompt.md) |
| Refactoring | Improving maintainability safely | Incident response under active outage | [View](prompts/english/agents/refactoring-prompt.md) |
| Testing | Building or fixing test strategy | You only need non-test docs | [View](prompts/english/agents/testing-strategies-prompt.md) |
| Documentation | Producing technical docs | You need runtime diagnosis | [View](prompts/english/agents/documentation-prompt.md) |
| Performance | Latency/throughput/cost bottlenecks | Problem is primarily correctness | [View](prompts/english/agents/performance-optimization-prompt.md) |
| Git & VCS | Workflow, branching, commit hygiene | App logic decisions | [View](prompts/english/agents/git-version-control-prompt.md) |
| Accessibility Audit | WCAG and accessibility compliance | Backend-only infrastructure change | [View](prompts/english/agents/accessibility-audit-prompt.md) |
| Migration & Upgrade | Framework/runtime/DB migrations | Greenfield implementation | [View](prompts/english/agents/migration-upgrade-prompt.md) |
| Monitoring & Observability | Logs, metrics, traces, alerts | Pure UI copy/content task | [View](prompts/english/agents/monitoring-observability-prompt.md) |
| Debugging & Troubleshooting | Root-cause and incident diagnostics | You are designing architecture from zero | [View](prompts/english/agents/debugging-troubleshooting-prompt.md) |
| Claude Code Modes ⭐ | Managing /think and planning depth | Non-Claude environments only | [View](prompts/english/agents/claude-code-modes-prompt.md) |
| Claude Code Workflow | CLAUDE.md, hooks, permissions, MCP | You only need algorithm design | [View](prompts/english/agents/claude-code-workflow-prompt.md) |
| Technology Stack ⭐ | Selecting tools/libraries | Stack is fixed and approved | [View](prompts/english/agents/technology-stack-prompt.md) |
| Architecture Patterns | System design and trade-offs | Small local bug fix | [View](prompts/english/agents/architecture-patterns-prompt.md) |
| Full-Stack Development | End-to-end app delivery | Single-layer scoped work | [View](prompts/english/agents/fullstack-development-prompt.md) |
| AI & LLM Integration | RAG/agents/model integration | No AI component exists | [View](prompts/english/agents/ai-llm-integration-prompt.md) |
| API Design & GraphQL | API contract/schema design | UI-only styling task | [View](prompts/english/agents/api-design-graphql-prompt.md) |
| Cloud & Infrastructure | IaC/K8s/multi-region/cost | Local script-only changes | [View](prompts/english/agents/cloud-infrastructure-prompt.md) |
| Data Engineering | Pipelines/streaming/data quality | CRUD app without data platform scope | [View](prompts/english/agents/data-engineering-prompt.md) |
| Compliance & Governance | Regulated/security governance scope | Prototype with no compliance requirements | [View](prompts/english/agents/compliance-governance-prompt.md) |
| Multi-Agent Orchestration | Parallel agent coordination | Single-agent linear task | [View](prompts/english/agents/multi-agent-orchestration-prompt.md) |
| Monorepo & Complex Projects | Multi-package cross-cutting work | Small standalone repository | [View](prompts/english/agents/monorepo-complex-projects-prompt.md) |
| Error Handling & Resilience | Fault tolerance and degradation | Static content editing only | [View](prompts/english/agents/error-handling-resilience-prompt.md) |
| Developer Experience & Tooling | Linting/hooks/onboarding/DX | Feature logic changes only | [View](prompts/english/agents/developer-experience-tooling-prompt.md) |
| Database Design & Optimization | Schema/index/query tuning | No persistent data layer exists | [View](prompts/english/agents/database-optimization-prompt.md) |
| UI/UX & Design Systems | Design tokens/components/theming | API/backend-only task | [View](prompts/english/agents/ui-design-systems-prompt.md) |

---

## Archived (Merged) Prompts

These were removed from the active catalog to reduce overlap:

- Error Analysis
- Project Workflow
- Integration Guardian
- Claude Code Token Optimization
- Prompt Chaining

See [Archive Index](prompts/english/agents/archive/INDEX.md).

---

## Quality Gate (Repository Standard)

Every active prompt must include:
- `## Role`
- `## Protocol / Core Loop`
- `## Phases`
- `## Remember` (final section)

And must follow **No Vague Advice**:
- each recommendation must end with a concrete decision, tool, or validation step.

Use the measurable review checklist: [Prompt Review Checklist](prompts/english/workflows/prompt-review-checklist.md)

---

## 90-Day Improvement Cycle

- Monthly: usage, token, and link hygiene review
- Quarterly: keep/merge/archive portfolio review and active catalog cleanup

Guide: [Portfolio Maintenance Guide](prompts/english/workflows/portfolio-maintenance-guide.md)

---

## Repository Structure

```text
prompts/
└── english/
    ├── agents/          # Active agent prompts
    │   └── archive/     # Archived prompts removed from active catalog
    ├── base/            # Foundation prompt
    ├── project-types/   # Domain-specific prompts
    ├── examples/        # Real-world usage examples
    └── workflows/       # Setup, selection, troubleshooting, maintenance
```

## Resources

- [QUICK-START.md](QUICK-START.md)
- [USAGE.md](USAGE.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [CHANGELOG.md](CHANGELOG.md)
- [llms.txt](llms.txt)
- [Agent Index](prompts/english/agents/INDEX.md)
- [Prompt Index](prompts/english/INDEX.md)
- [Repository Map](REPOSITORY-MAP.md)
- [Prompt Selector Guide](prompts/english/workflows/prompt-selector-guide.md)
- [Prompt Review Checklist](prompts/english/workflows/prompt-review-checklist.md)
