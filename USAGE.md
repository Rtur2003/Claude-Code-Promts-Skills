# Usage Guide

## Selection Rules

1. Start with [REPOSITORY-MAP.md](REPOSITORY-MAP.md) for fast orientation.
2. Start with **Agent System**.
3. Add **one** specialist prompt if required.
4. Validate with explicit success criteria before adding more prompts.

## Common Scenarios

| Scenario | Prompt Setup |
|----------|--------------|
| General autonomous development | Agent System |
| Production debugging / incident | Agent System + Debugging & Troubleshooting |
| Security audit | Agent System + Security Audit |
| Code review | Agent System + Code Review |
| Architecture design | Agent System + Architecture Patterns |
| Tooling choice | Agent System + Technology Stack |
| Performance optimization | Agent System + Performance |
| Multi-agent execution / dynamic workflows | Agent System + Multi-Agent Orchestration |
| Thinking depth / effort / plan mode | Agent System + Claude Code Thinking & Planning |
| Pick a model or effort level | Model Selection Guide |
| Claude Code setup/config | Agent System + Claude Code Workflow |
| Write a Claude skill | Agent Skills |
| Connect an external system (MCP) | MCP Integration |
| Build/distribute a plugin | Claude Code Plugins |
| Automate on a lifecycle event | Hooks & Automation |
| Build an agent on the Agent SDK | Agent SDK Guide |
| Interactive app/API work | Foundation + one project-type prompt |

## Copy-Paste Setup

### Agent mode

```text
[Paste Agent System prompt]
Task: <your task>
Success criteria: <measurable outcomes>
Constraints: <scope, time, risk>
```

### Interactive mode

```text
[Paste Foundation prompt + project-type prompt]
Task: <your task>
Start with Analyze phase.
```

## Quality Gate Before Completion

- Requirements met
- Validation passed
- Risks addressed or explicitly documented

## Portfolio Governance

Use the 90-day governance process to keep the prompt set lean:
- [Portfolio Maintenance Guide](prompts/english/workflows/portfolio-maintenance-guide.md)
- [Prompt Review Checklist](prompts/english/workflows/prompt-review-checklist.md)

## Outcome-First Task Briefs

For short, high-signal task specs, use:
- [Task-to-Outcome Scenario Pack](prompts/english/examples/task-outcome-scenarios-example.md)
