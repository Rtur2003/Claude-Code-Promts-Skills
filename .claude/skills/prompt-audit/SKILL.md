---
name: prompt-audit
description: Use before adding or publishing a prompt — when you need a deterministic audit of required headings, agent metadata, catalog registration, retired model references, and vague-advice language in this prompt library.
allowed-tools: Bash(python ${CLAUDE_SKILL_DIR}/scripts/audit.py *) Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/audit.py *)
---

# Prompt Audit

## Purpose

Audit prompt files against this repository's measurable contribution standard. The bundled script does not judge prompt quality semantically; it detects structural omissions and patterns that commonly cause catalog drift or stale guidance.

## Workflow

1. Audit the active prompt set:

   ```bash
   python ${CLAUDE_SKILL_DIR}/scripts/audit.py ../../prompts/english
   ```

2. Audit one file while editing:

   ```bash
   python ${CLAUDE_SKILL_DIR}/scripts/audit.py ../../prompts/english/agents/your-prompt.md
   ```

3. Pass `--json` when another tool or CI job needs machine-readable results.
4. Fix every finding that is in scope. A clean report means only that configured structural checks passed.

## Checks

| Check | Failure condition |
|---|---|
| Required headings | A prompt is missing `## Role`, a protocol heading, `## Phases`, or `## Remember` |
| Final Remember section | `## Remember` is not the final Markdown heading |
| Agent metadata | An active agent prompt omits `Use this when:` or a 3–5 item `Skip to:` list |
| Catalog registration | A prompt is not referenced by the agent/global prompt index |
| Retired model claims | An active prompt presents a retired model ID outside a clearly marked retirement section |
| Vague advice | A recommendation uses one of the configured generic filler phrases without a concrete tool, decision, or validation step nearby |

## Interpretation

- Structural failures are blocking.
- A `Skip to:` link may resolve to the same file only when it points to a real heading.
- A clean audit does not prove technical accuracy. Verify framework versions and Claude features against the official Claude documentation:
  - [Claude Code docs](https://code.claude.com/docs)
  - [Claude Platform docs](https://platform.claude.com/docs)

## Additional resources

- [Prompt Review Checklist](../../../prompts/english/workflows/prompt-review-checklist.md)
- [Contributing Rules](../../../CONTRIBUTING.md)
- [Agent Skills prompt](../../../prompts/english/agents/agent-skills-prompt.md)

## Remember

> A prompt is ready for publication only when its structure, navigation, and current claims can be checked by another person or tool.
