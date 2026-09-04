# Evals

Regression protection for the `find-prompt` routing table — the thing every audit of this library (external and internal) flagged as the highest-value missing piece: nothing proved the routing table actually routes correctly.

## What's here

- `cases/find-prompt-routing.jsonl` — 20 realistic tasks, one drawn from most rows of the routing table in `.claude/skills/find-prompt/SKILL.md`, each with the file that row should resolve to.
- `run_routing_eval.py` — runs two tiers:
  1. **Static** (always runs, no dependencies): confirms every case's `expected_specialist` file actually exists. This is the failure mode that happens in practice — a prompt gets renamed or archived and the routing table isn't updated to match. Catches it deterministically, in under a second, with no API cost.
  2. **Live** (runs only if `ANTHROPIC_API_KEY` is set): sends each task to `claude-haiku-4-5` with the routing table as context and checks whether the model's answer matches the expected file. This is the actual trigger-accuracy measurement — static tier alone can't catch "routes to a file that exists but is the wrong one."

## Running it

```bash
python3 evals/run_routing_eval.py              # static tier only
ANTHROPIC_API_KEY=sk-... python3 evals/run_routing_eval.py --live   # both tiers
```

Wired into CI (`.github/workflows/quality-gate.yml`, `routing-eval` job): the static tier runs on every PR unconditionally; the live tier runs only if the `ANTHROPIC_API_KEY` repository secret is configured (it's optional — CI stays green without it, you just lose live routing-accuracy coverage).

## When to add a case

Whenever a row is added to the `find-prompt` routing table, add one realistic task here that should hit it — that's what turns "the table says X routes to Y" into "we've verified X actually routes to Y." A routing-table row with no eval case is a claim, not a tested fact.

## What this does not cover

This tests routing accuracy only — whether the right file gets picked. It does not test prompt *quality* (whether the content of that file is any good), and it does not test the composition-tier logic (whether the right *number* of specialists gets loaded) or the conflict-precedence rule. Those would need scenario-based evals with a human or model grading the output against a rubric, which is a larger undertaking than this file-existence-plus-routing check — a reasonable next addition, not something this eval claims to already do.
