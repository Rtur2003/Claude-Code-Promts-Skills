# Cross-Agent Skills

Adapters and mirrored deterministic skills for agent hosts that discover `.agents/skills/`.

- [Find Prompt](find-prompt/SKILL.md) — delegates to the canonical Claude routing table
- [Capability Audit](capability-audit/SKILL.md) — delegates to the canonical read-only GitHub inspector
- [Deterministic Checks](deterministic-checks/SKILL.md)
- [Changelog from Commits](changelog-from-commits/SKILL.md)
- [Documentation Link Audit](doc-link-audit/SKILL.md)
- [Skill Audit](skill-audit/SKILL.md)

The canonical Claude Code implementations live in [`.claude/skills/`](../../.claude/skills/). Do not maintain a second routing table here.
