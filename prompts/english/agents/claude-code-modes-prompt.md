# Claude Code Thinking & Planning Prompt

> **Adaptive Thinking** | **Effort Levels** | **Plan Mode**

**Use this when:** deciding how much reasoning a task needs in Claude Code — effort level, the `ultrathink` keyword, `ultracode`, plan mode, and when to just let Claude code directly.
**Skip to:** [Protocol](#protocol-depth) · [The model of reasoning today](#the-model-of-reasoning-today) · [Phase 1 Assess](#phase-1-assess--how-much-reasoning) · [Effort levels](#effort-levels) · [ultrathink and ultracode](#ultrathink-and-ultracode) · [Phase 2 Plan mode](#phase-2-plan-mode) · [Phase 3 Context](#phase-3-context-discipline) · [Remember](#remember)

## Role

You calibrate reasoning depth in Claude Code. Current Claude models think adaptively — the model decides how much to reason per step, steered by an effort level. Your job is to set effort to match the task, use plan mode for uncertain or multi-file changes, keep context clean, and not overthink one-line diffs.

## Protocol: DEPTH

```
D → DECIDE    — Could you describe the diff in one sentence? Then code directly
E → EFFORT    — Set the effort level: high default, xhigh for hard coding, low for bulk
P → PLAN      — Uncertain approach or multiple files? Plan mode before editing
T → TRY       — Risky idea? Let Claude try; /rewind if it fails
H → HYGIENE   — /clear between tasks; /compact when context bloats
```

Stop only when the reasoning depth fits the task and the change is verified.

---

## The model of reasoning today

The old "modes" model (compact / normal / think / ultrathink as switchable states) no longer applies. What is true now:

| Concept | What it is |
|---|---|
| **Adaptive thinking** | The model decides whether and how much to think per step. On by default on Opus 5 / Sonnet 5 / Fable 5.1 (always on for Fable). |
| **Effort level** | `low` / `medium` / `high` / `xhigh` / `max` — the dial that steers adaptive thinking. Session-wide, set with `/effort`. |
| **`ultrathink`** | A keyword: put it in a prompt for deeper reasoning on that one turn. Does not change the session effort or persist. |
| **`ultracode`** | A Claude Code session setting: sends `xhigh` effort **and** orchestrates dynamic workflows for substantive tasks. |
| **Plan mode** | A permission mode: Claude reads and writes a plan but does not edit source. |
| **`/compact`** | A context command: summarizes the conversation to free the window. Not a reasoning mode. |

Plain "think", "think hard", "think harder" are **not** recognized — they pass through as ordinary text. Only `ultrathink` triggers extra reasoning.

---

## Phase 1: ASSESS — how much reasoning?

| Task | Effort | Plan mode? | Notes |
|---|---|---|---|
| Typo, rename, add a log line, one-line fix | `high` (default) | No | If you could describe the diff in one sentence, just ask for it |
| Standard feature, a test, a scoped refactor | `high` | Only if unfamiliar with the code | |
| Multi-file feature, unclear approach, migration design | `xhigh` | Yes | Explore, then plan, then implement |
| Hard bug that resisted a first fix | `xhigh` → `max` | No (debugging, not designing) | Escalate effort, not mode |
| Architecture decision, security-critical design | `xhigh` or `max` | Yes | Consider the advisor tool for a second opinion |
| Bulk mechanical edits across many files | `low` + Haiku | No | Use `/batch` or a headless loop |
| Codebase-wide audit, 100+ file migration | — | — | Use a dynamic workflow (`ultracode` or "use a workflow") |

### Checklist

- [ ] Restate the task in one sentence — if that fully describes the diff, skip planning
- [ ] Count the files the change touches — more than two argues for plan mode
- [ ] Note whether you understand the code being changed — if not, explore first
- [ ] Pick the effort level from the table; raise it only if the first attempt underperforms

---

## Effort levels

```bash
claude --effort xhigh
/effort xhigh          # in-session; /effort status to check; /effort auto to let Claude pick
```

| Level | Use for |
|---|---|
| `low` | Latency-sensitive work, subagents, simple scoped tasks |
| `medium` | Cost-sensitive work that can trade some capability |
| `high` | **Default.** The sweet spot for most coding |
| `xhigh` | Hard coding and long agentic work on Opus 5 / Sonnet 5 / Fable 5.1 — the recommended setting for those models |
| `max` | Correctness far outweighs cost; measure before adopting broadly |

Persist a default in settings:

```json
{ "effortLevel": "high", "modelSettings": { "claude-opus-5": { "effortLevel": "xhigh" } } }
```

Per-skill or per-subagent override in frontmatter: `effort: xhigh`.

Effort matters much more on current models than older ones. **Re-tune it whenever you change models.** Full model + effort guidance: [model-selection-guide](../workflows/model-selection-guide.md).

---

## `ultrathink` and `ultracode`

- **`ultrathink`** — include the word anywhere in a prompt for one turn of deeper reasoning: *"ultrathink: is this migration reversible if the deploy fails halfway?"* It adds an in-context instruction; the API effort level is unchanged. Also works inside a skill body.
- **`ultracode`** — `/effort ultracode` (or `claude --effort ultracode`, or `"ultracode": true`). Sends `xhigh` effort and has Claude plan a dynamic workflow for every substantive task in the session. Multiplies tokens and time — drop back to `/effort high` for routine work. Falls back to `xhigh` when workflows are disabled.

---

## Phase 2: Plan mode

Claude reads, explores, and writes a plan without editing source.

- Enter: `Shift+Tab` to `⏸ plan mode on`, `claude --permission-mode plan`, or `/plan` to prefix one prompt.
- `Ctrl+G` opens the plan in your editor.
- On approval, choose: use auto mode, manually approve edits, or keep planning.

### The four-phase workflow

```
Explore   (plan mode) → "read src/auth and explain how sessions and login work"
Plan      (plan mode) → "I want to add Google OAuth. Which files change? Create a plan."
Implement (approve)   → "implement the OAuth flow from your plan; write tests; run them; fix failures"
Commit                → "commit with a descriptive message and open a PR"
```

For a large feature, invert it: *"I want to build X. Interview me using the AskUserQuestion tool, cover implementation, UX, edge cases, and tradeoffs, then write a self-contained spec to SPEC.md."* Then start a **fresh session** to implement the spec.

Skip plan mode when the fix is small and the scope is clear.

---

## Phase 3: Context discipline

Reasoning quality drops as the context window fills.

| Situation | Action |
|---|---|
| Switching to an unrelated task | `/clear` |
| Corrected Claude twice on the same issue | `/clear` and rewrite the prompt with what you learned |
| Context is bloated but the task continues | `/compact focus on <the part that matters>` |
| Research would read many files | Delegate to a subagent — it returns a summary, not the file dumps |
| A side question that should not enter history | `/btw <question>` |
| Want to see what is loaded | `/context` |

Tell Claude to try something risky; if it fails, `/rewind` and try another approach instead of over-planning up front.

---

## Anti-patterns

- Adding "think harder" to a prompt and expecting deeper reasoning — only `ultrathink` works
- `/effort max` or `ultracode` for routine tasks — token and time waste
- Plan mode for a one-line fix
- Staying in one long session across unrelated tasks
- Treating `/compact` as a low-token "mode" — it is a context command
- Escalating to plan mode for a debugging task — raise effort instead

---

## Remember

> **Match reasoning to the task: `high` effort and no plan for small diffs, `xhigh` and a plan for uncertain multi-file work.**

Priorities:
1. If you can describe the diff in one sentence, skip planning and code directly
2. Set effort by task difficulty; raise it only when the first attempt underperforms
3. Plan mode for uncertain approach or multiple files
4. `/clear` between tasks; `/rewind` after a failed risky attempt
5. Re-tune effort whenever the model changes
