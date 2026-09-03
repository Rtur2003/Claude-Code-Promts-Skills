# Archived Agent Prompts

> Historical prompts moved out of the active catalog to reduce overlap and improve prompt selection speed.

## Archive Policy

A prompt is archived when at least one of these is true:
- It duplicates guidance already covered by `claude-agent-system-prompt.md`.
- A newer specialist prompt provides better, more complete coverage.
- It adds selection friction without clear incremental outcome value.

## Keep / Merge / Archive Decisions

| Prompt | Status | Merged Into | Reason |
|--------|--------|-------------|--------|
| Error Analysis | Archive | Debugging & Troubleshooting + Agent System | Overlaps with production debugging flow and root-cause loop |
| Project Workflow | Archive | Agent System + Technology Stack + Full-Stack Development | Lifecycle planning is now covered by core + stack-specific prompts |
| Integration Guardian | Archive | Code Review + Testing + Monitoring & Observability | Cross-cutting integrity checks are distributed in stronger specialist prompts |
| Claude Code Token Optimization | Archive | Claude Code Thinking & Planning + Claude Code Workflow + Model Selection Guide | Token and effort strategy is now covered by effort levels, context discipline, and model choice |
| Prompt Chaining | Archive | Agent System + Multi-Agent Orchestration | Multi-step planning is handled by the core loop, subagents, and dynamic workflows |

## Access Archived Content

Archived files remain available for reference:
- [Error Analysis](error-analysis-prompt.md)
- [Project Workflow](project-workflow-prompt.md)
- [Integration Guardian](integration-guardian-prompt.md)
- [Claude Code Token Optimization](claude-code-token-optimization-prompt.md)
- [Prompt Chaining](prompt-chaining-prompt.md)
