---
description: Routes a consequential comparison request to the evidence-driven research prompt.
tags: [routing, research, smoke]
runs: 1
max_turns: 5
timeout_seconds: 180
allowed_tools: [Skill, Read, Glob, Grep]
expected_outcome: Claude invokes find-prompt and identifies evidence-driven-research-prompt.md.
---

Compare two unfamiliar home air-quality monitors for a family with asthma. I care about sensor accuracy, replaceable parts, privacy, and evidence beyond affiliate reviews. Use the right prompt from this library and tell me how you would research the decision.
