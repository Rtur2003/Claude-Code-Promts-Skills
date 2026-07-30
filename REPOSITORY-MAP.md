# Repository Map

Single-file navigation map for fast orientation before deep reading.

## Root

| Path | Purpose |
|---|---|
| `README.md` | Main catalog, usage entrypoint, portfolio standards |
| `QUICK-START.md` | Fast setup and minimal prompt selection |
| `USAGE.md` | Scenario-based prompt composition |
| `CONTRIBUTING.md` | Contribution and quality rules |
| `CHANGELOG.md` | Versioned documentation history |
| `CLAUDE.md` | Project memory and maintenance rules |
| `llms.txt` | LLM-friendly index |
| `prompts/english/` | Full prompt library (English only) |

## prompts/english

| Path | Purpose |
|---|---|
| `INDEX.md` | Global prompt index across all categories |
| `agents/` | Active specialist/system prompts |
| `agents/INDEX.md` | Active + archived agent catalog |
| `agents/archive/` | Archived prompts and merge rationale |
| `base/` | Foundation universal prompt |
| `project-types/` | Domain-specific prompts (web, API, ML, mobile, etc.) |
| `examples/` | Real usage scenarios |
| `workflows/` | Selection guides, review checklists, maintenance workflows |

## Recommended Reading Order

1. `REPOSITORY-MAP.md` (this file)
2. `README.md`
3. `prompts/english/INDEX.md`
4. `prompts/english/agents/claude-agent-system-prompt.md`
5. Add only one specialist prompt from `prompts/english/agents/INDEX.md` if needed

## Fast Lookup

- Need the default operational prompt: `prompts/english/agents/claude-agent-system-prompt.md`
- Need Claude Code setup/MCP workflow: `prompts/english/agents/claude-code-workflow-prompt.md`
- Need prompt composition examples: `prompts/english/examples/`
- Need governance criteria: `prompts/english/workflows/prompt-review-checklist.md`
