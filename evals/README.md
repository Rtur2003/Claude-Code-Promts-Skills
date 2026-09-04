# Evals

Regression protection for the `find-prompt` routing table — the thing every review of this library (external audit, competitor research, and a follow-up critique of the eval's own first draft) flagged as the highest-value missing piece. The first version of this eval only checked "does the expected file exist" — real routing failure modes are broader than that, so the case set now covers five distinct behaviors.

## Categories

| File | Tests | Static check | Live check |
|---|---|---|---|
| `cases/basic-routing.jsonl` | One task, one clearly correct specialist — the common case | Expected file exists | Model picks the expected file |
| `cases/no-specialist.jsonl` | Trivial tasks (rename, typo, one-line fix) that should load **no** specialist — Tier 0 | Case declares `expected_tier: 0` | Model says `NONE`, doesn't over-route to a specialist for a one-line fix |
| `cases/multi-domain.jsonl` | Tasks that genuinely need Tier 2 (two independent specialists) or Tier 3 (orchestration) | Every named specialist file exists, tier is 2 or 3 | Model names every genuinely load-bearing specialist, not just one |
| `cases/ambiguous.jsonl` | Tasks with several defensible routes (e.g. "API is slow and intermittently 500s" could be debugging, performance, or monitoring) | 2+ acceptable specialists listed, all exist | Model's answer matches *any* of the acceptable routes — this category exists so a reasonable alternate answer doesn't count as a routing failure |
| `cases/conflict-precedence.jsonl` | Two loaded specialists disagree (e.g. Debugging wants to inspect env vars, Security says never print secrets) | Forbidden actions and a precedence rule are declared | Model's first concrete action doesn't contain any forbidden action — proves the precedence order in `agents/claude-agent-system-prompt.md` and `workflows/prompt-selector-guide.md#conflict-precedence` is actually followed, not just documented |

## Running it

```bash
python3 evals/run_routing_eval.py                        # all categories, static tier only
python3 evals/run_routing_eval.py --category no-specialist   # one category
ANTHROPIC_API_KEY=sk-... python3 evals/run_routing_eval.py --live   # static + live, all categories
```

Wired into CI (`.github/workflows/quality-gate.yml`, `routing-eval` job): the static tier runs on every PR unconditionally; the live tier runs only if the `ANTHROPIC_API_KEY` repository secret is configured (optional — CI stays green without it, you just lose live behavioral coverage).

## Why the categories matter (not just "add more cases")

A routing eval that only measures "picked the expected file" rewards over-routing and under-routing equally as long as *a* file gets picked — it can't tell "loaded exactly the right one specialist" apart from "loaded five specialists, one of which happened to be right." Splitting into categories makes each failure mode falsifiable on its own:

- **basic-routing** alone can't catch over-routing (a trivial task getting a specialist it doesn't need) — that's what **no-specialist** is for.
- **basic-routing** alone can't catch under-routing (a two-domain task getting only one specialist) — that's what **multi-domain** is for.
- Neither can catch "the model refused a defensible alternate route and called it wrong" — that's a bug in the *eval*, not the routing, which **ambiguous** exists to prevent.
- None of the above test whether the conflict-precedence *policy* (not just its existence in a prompt file) actually changes model behavior — **conflict-precedence** is the only category that runs an adversarial scenario and checks for an absence (no forbidden action appears) rather than a presence (the right file was named).

## Verified failure detection

Each static check was deliberately broken once, confirmed to fail with exit code 1 and a clear message, then reverted — the same discipline used for the deterministic-checks, doc-link-audit, and skill-audit skills. See the CHANGELOG entry for this eval addition for the specific breaks tested.

## When to add a case

Whenever a row is added to the `find-prompt` routing table, add a `basic-routing` case for it. If the change introduces a new tier-2/3 combination, a new ambiguous overlap, or a new conflict between two specialists, add a case to the matching category. A routing-table row or precedence claim with no eval case is a claim, not a tested fact.

## What this still does not cover

Prompt *quality* (whether the content of the routed-to file is any good — see `workflows/prompt-review-checklist.md` for that, a separate concern), and behavioral regression on a single prompt's own output quality over time (e.g. "did `security-audit-prompt.md` get worse at catching SQL injection after the last edit") — that would need per-prompt benchmark suites with scored test cases, which is a larger, separate undertaking than routing correctness.
