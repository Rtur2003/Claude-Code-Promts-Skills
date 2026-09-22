---
description: Activates the capability audit for a low-adoption Claude Code plugin candidate.
tags: [capability-audit, smoke]
runs: 1
max_turns: 3
timeout_seconds: 120
allowed_tools: [Skill]
expected_outcome: Claude invokes capability-audit before recommending installation.
---

This Claude Code plugin has only a few stars, but its narrow feature looks useful. Evaluate https://github.com/WasayAbid/agent-trace-triage before I install it. Do not treat popularity as the decision.
