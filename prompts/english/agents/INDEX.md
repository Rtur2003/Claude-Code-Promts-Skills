# Agent Prompts Index

> Outcome-first catalog for autonomous AI coding agents.

## Core Rule

Start with [Agent System](claude-agent-system-prompt.md). Add specialists by tier — 1 for a single-domain task (default), 2 for two genuinely independent domains, Multi-Agent Orchestration when units of work need isolation.

Composition tiers + conflict precedence: [../workflows/prompt-selector-guide.md](../workflows/prompt-selector-guide.md)

## Route by task

| Task | Prompt |
|---|---|
| Any autonomous coding task | [Agent System](claude-agent-system-prompt.md) |
| Write or debug a Claude skill | [Agent Skills](agent-skills-prompt.md) |
| Connect Claude to a DB / browser / API via MCP | [MCP Integration](mcp-integration-prompt.md) |
| Package skills/agents/hooks into a plugin | [Claude Code Plugins](claude-code-plugins-prompt.md) |
| Parallel agents, workflows, audits, writer/reviewer | [Multi-Agent Orchestration](multi-agent-orchestration-prompt.md) |
| Automate on a lifecycle event (lint, block, gate) | [Hooks & Automation](hooks-automation-prompt.md) |
| Set up CLAUDE.md, rules, settings, permissions | [Claude Code Workflow](claude-code-workflow-prompt.md) |
| Calibrate thinking depth / effort / plan mode | [Claude Code Thinking & Planning](claude-code-modes-prompt.md) |
| Pick a model / effort level | [../workflows/model-selection-guide.md](../workflows/model-selection-guide.md) |
| Know what a current Claude Code build does | [../workflows/claude-code-native-features-guide.md](../workflows/claude-code-native-features-guide.md) |
| Build an agent on the Agent SDK | [../workflows/agent-sdk-guide.md](../workflows/agent-sdk-guide.md) |
| Review a PR / change set | [Code Review](code-review-prompt.md) |
| Security exposure is possible | [Security Audit](security-audit-prompt.md) |
| Root-cause a production incident | [Debugging & Troubleshooting](debugging-troubleshooting-prompt.md) |
| Design system architecture | [Architecture Patterns](architecture-patterns-prompt.md) |
| Choose tools / libraries | [Technology Stack](technology-stack-prompt.md) |
| Build or fix a test strategy | [Testing Strategies](testing-strategies-prompt.md) |

## Active Catalog (Keep)

### Claude Code operation

| Prompt | Use when | Do not use when | ~Tokens | File |
|--------|----------|-----------------|---------|------|
| Agent System ⭐ | Any autonomous task | You only need minimal guidance | 2k | [View](claude-agent-system-prompt.md) |
| Quick Reference | Token budget is extremely tight | You need specialist depth | 1k | [View](agent-quick-reference.md) |
| Agent Skills ⭐ | Writing / debugging a Claude skill | No skill authoring involved | 4k | [View](agent-skills-prompt.md) |
| MCP Integration ⭐ | Connecting Claude to an external system | No external system involved | 3k | [View](mcp-integration-prompt.md) |
| Claude Code Plugins | Bundling skills/agents/hooks to share | Nothing to package or distribute | 3k | [View](claude-code-plugins-prompt.md) |
| Multi-Agent Orchestration ⭐ | Parallel agents, workflows, audits, review | Single-agent linear work | 4k | [View](multi-agent-orchestration-prompt.md) |
| Hooks & Automation | Enforcing something on a lifecycle event | Advisory guidance is enough | 3k | [View](hooks-automation-prompt.md) |
| Claude Code Workflow | CLAUDE.md/rules/settings/permissions | No Claude Code setup task | 3k | [View](claude-code-workflow-prompt.md) |
| Claude Code Thinking & Planning ⭐ | Calibrating effort / plan mode | Non-Claude context only | 2k | [View](claude-code-modes-prompt.md) |

### Development specialists

| Prompt | Use when | Do not use when | ~Tokens | File |
|--------|----------|-----------------|---------|------|
| Code Review | Reviewing a PR/change set | Writing a feature from scratch | 2k | [View](code-review-prompt.md) |
| Security Audit | Security risk is material | No threat model is in scope | 3k | [View](security-audit-prompt.md) |
| Refactoring | Reducing complexity safely | Active production incident | 3k | [View](refactoring-prompt.md) |
| Testing | Building test strategy and coverage | You only need docs | 6k | [View](testing-strategies-prompt.md) |
| Documentation | Producing high-quality docs | Root-cause debugging task | 3k | [View](documentation-prompt.md) |
| Performance | Throughput/latency/cost bottlenecks | Core issue is correctness | 5k | [View](performance-optimization-prompt.md) |
| Git & VCS | Branching/commit/release hygiene | App architecture decision | 3k | [View](git-version-control-prompt.md) |
| Accessibility Audit | Accessibility and WCAG compliance | Backend-only systems task | 4k | [View](accessibility-audit-prompt.md) |
| Migration & Upgrade | Framework/runtime/DB migration | Greenfield build | 3k | [View](migration-upgrade-prompt.md) |
| Monitoring & Observability | Logs/metrics/traces/alerts | Pure content update | 4k | [View](monitoring-observability-prompt.md) |
| Debugging & Troubleshooting | Incident/root-cause diagnostics | Net-new architecture design | 4k | [View](debugging-troubleshooting-prompt.md) |
| Technology Stack ⭐ | Tool/library selection | Stack already fixed | 3k | [View](technology-stack-prompt.md) |
| Architecture Patterns | Architecture and trade-off design | Small local fix | 5k | [View](architecture-patterns-prompt.md) |
| Full-Stack Development | End-to-end web app delivery | Narrow scoped layer-only task | 4k | [View](fullstack-development-prompt.md) |
| AI & LLM Integration | RAG/vector/agent integration | No AI component exists | 4k | [View](ai-llm-integration-prompt.md) |
| API Design & GraphQL | API contracts/schema decisions | UI-only work | 5k | [View](api-design-graphql-prompt.md) |
| Cloud & Infrastructure | IaC/K8s/multi-region operations | Pure local utility task | 4k | [View](cloud-infrastructure-prompt.md) |
| Data Engineering | Pipelines/streaming/data quality | Standard app CRUD only | 5k | [View](data-engineering-prompt.md) |
| Compliance & Governance | Regulated scope and controls | Non-regulated prototype | 4k | [View](compliance-governance-prompt.md) |
| Monorepo & Complex Projects | Multi-package coordination | Small standalone repo | 4k | [View](monorepo-complex-projects-prompt.md) |
| Error Handling & Resilience | Fault tolerance and reliability | Static content updates | 5k | [View](error-handling-resilience-prompt.md) |
| Developer Experience & Tooling | Lint/hooks/dev workflow standards | Core feature implementation | 4k | [View](developer-experience-tooling-prompt.md) |
| Database Design & Optimization | Schema/index/query optimization | No data layer scope | 4k | [View](database-optimization-prompt.md) |
| UI/UX & Design Systems | Component systems/theming/a11y UI | Backend-only task | 5k | [View](ui-design-systems-prompt.md) |

## Archived (Merge/Archive)

| Prompt | Status | Merged Into | File |
|--------|--------|-------------|------|
| Error Analysis | Archive | Debugging & Troubleshooting + Agent System | [View](archive/error-analysis-prompt.md) |
| Project Workflow | Archive | Agent System + Technology Stack + Full-Stack Development | [View](archive/project-workflow-prompt.md) |
| Integration Guardian | Archive | Code Review + Testing + Monitoring & Observability | [View](archive/integration-guardian-prompt.md) |
| Claude Code Token Optimization | Archive | Claude Code Modes + Claude Code Workflow | [View](archive/claude-code-token-optimization-prompt.md) |
| Prompt Chaining | Archive | Agent System + Multi-Agent Orchestration | [View](archive/prompt-chaining-prompt.md) |

See full rationale in [Archive Index](archive/INDEX.md).
