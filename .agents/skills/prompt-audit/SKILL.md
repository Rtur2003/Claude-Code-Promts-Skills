---
name: prompt-audit
description: Use before adding or publishing a prompt — when you need deterministic structure and catalog checks for prompt headings, agent metadata, stale model IDs, and vague-advice language.
---

# Prompt Audit

This adapter delegates to the canonical Claude implementation at [`.claude/skills/prompt-audit/SKILL.md`](../../../.claude/skills/prompt-audit/SKILL.md).

Run the canonical audit from the repository root:

```bash
python3 .claude/skills/prompt-audit/scripts/audit.py prompts/english
```

Use `--json` for machine-readable output.
