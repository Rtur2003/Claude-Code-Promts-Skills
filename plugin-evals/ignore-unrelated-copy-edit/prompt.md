---
description: Ensures capability-audit does not trigger for an unrelated local copy edit.
tags: [capability-audit, negative]
runs: 1
max_turns: 3
timeout_seconds: 120
allowed_tools: [Skill]
expected_outcome: Claude answers without invoking capability-audit.
---

Rewrite this sentence to be clearer: “The button was clicked by the user in order to submit the form.”
