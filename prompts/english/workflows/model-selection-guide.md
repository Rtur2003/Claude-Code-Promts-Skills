# Model Selection Guide

> **Current Lineup** | **Effort Levels** | **Plan vs Execute vs Bulk**

**Use this when:** choosing a Claude model or effort level for a coding task, in Claude Code or the Agent SDK, or migrating code off a retired model.
**Skip to:** [Protocol](#protocol-select) · [Current models](#current-models-september-2026) · [Which model for which task](#which-model-for-which-task) · [Effort levels](#effort-levels) · [Claude Code model config](#claude-code-model-config) · [Retired models](#retired-and-legacy-models) · [API changes](#api-behavior-changes-on-current-models) · [Remember](#remember)

## Role

You pick the model and effort level that deliver the task at the lowest cost. Default to Opus 5 for hard agentic coding, Sonnet 5 for everyday work, Haiku 4.5 for bulk, Fable 5.1 only when Opus 5 at high effort still falls short. Judge cost per completed task, not per request.

## Protocol: SELECT

```
S → SCOPE     — How hard is the task? Planning, execution, or bulk mechanical work?
E → ELECT     — Pick the model tier for that scope
L → LEVEL     — Set effort: high is the default; xhigh for hard coding; low for subagents
E → ECONOMIZE — Cheaper model at lower effort often beats a pricier one at higher effort
C → CHECK     — Measure on real requests before locking a default
T → TUNE      — Re-tune effort when you change models; it matters more on current models
```

Stop only when the model and effort produce correct output and you have measured the cost per finished task, not per API call.

---

## Current models (September 2026)

| Model | API ID | Context | Max output | $/MTok in | $/MTok out | Knowledge cutoff |
|---|---|---|---|---|---|---|
| **Claude Opus 5** | `claude-opus-5` | 1M | 128K | $5 | $25 | May 2026 |
| **Claude Sonnet 5** | `claude-sonnet-5` | 1M | 128K | $2 | $10 | Jan 2026 |
| **Claude Haiku 4.5** | `claude-haiku-4-5` | 200K | 64K | $1 | $5 | Feb 2025 |
| **Claude Fable 5.1** | `claude-fable-5-1` | 1M | 128K | $10 | $50 | Jun 2026 |

- All four take text + image input, produce text, support vision, tool use, and multilingual work.
- Batch API is 50% off. Prompt-cache reads cost 10% of base input price (Fable 5.1 cache reads: $0.25/MTok).
- Aliases in Claude Code: `opus`, `sonnet`, `haiku`, `fable`, `best` (latest Fable where available, else Opus), `opusplan` (Opus for planning, auto-switches to Sonnet for execution), `opus[1m]` / `sonnet[1m]` (explicit 1M window).
- Legacy but still callable: Opus 4.5–4.8, Sonnet 4.5/4.6, Fable 5. No updates; retirement dates assigned.
- Haiku 4.5 is **not** a "5" model — it is the current small model. There is no Haiku 5 as of September 2026.

Verify current IDs and pricing at `platform.claude.com/docs/en/models/overview` before pinning anything.

---

## Which model for which task

| Task | Model | Effort | Why |
|---|---|---|---|
| Architecture decision, multi-file feature, hard debugging | **Opus 5** | `high` or `xhigh` | Default for complex agentic coding; checks its own work |
| Everyday feature work, small-to-medium changes, code review | **Sonnet 5** | `high` | Best speed/intelligence balance at 1/2.5 of Opus 5's price |
| Bulk mechanical edits, mass migration, test running, subagent research | **Haiku 4.5** | (no effort param) | Fastest, cheapest; fine for scoped work |
| A task where Opus 5 at `xhigh` still fails your evals; a long autonomous run | **Fable 5.1** | `high` (thinking always on) | Most capable; 2x Opus 5 price and different API behavior |
| A session that plans then implements | **`opusplan`** alias | — | Opus plans, Sonnet executes automatically |

Rules of thumb:
- **Start with Sonnet 5.** Move up to Opus 5 when Sonnet's output needs repeated correction on the same task.
- **A cascade is rarely worth it.** "The most capable model at lower effort" usually beats a multi-model routing scheme, and a cascade forfeits cross-model prompt-cache reuse.
- **Subagents and `Explore` default to lower effort** and can be pinned to Haiku. Use `CLAUDE_CODE_SUBAGENT_MODEL` for a default, `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` to override every subagent's frontmatter.
- **Fable 5.1 runs can take many minutes** on one hard request — plan for timeouts, stream output, show progress.

---

## Effort levels

Effort controls adaptive reasoning — how much the model thinks per step. It replaced fixed thinking budgets.

| Level | Use for |
|---|---|
| `low` | Latency-sensitive or non-intelligence-critical work; subagents; simple tasks |
| `medium` | Cost-sensitive work that can trade some capability |
| `high` | **Default.** Balances tokens and capability; the sweet spot for most coding |
| `xhigh` | The recommended setting for hard coding and long agentic work on Opus 5 / Sonnet 5 / Fable 5.1; higher token cost |
| `max` | Correctness far outweighs cost; test before adopting broadly |

- **Default is `high`** on all current API models (equivalent to omitting the parameter).
- Haiku 4.5 and Sonnet 4.5 **do not support effort**.
- Effort matters far more on current models than on prior generations. **Re-tune effort whenever you switch models.**
- `ultrathink` anywhere in a prompt requests deeper reasoning for that one turn without changing the session effort or persisting.
- `ultracode` (Claude Code session setting, not an API effort level) sends `xhigh` and orchestrates dynamic workflows for substantive tasks.

Setting effort:

```bash
claude --effort xhigh
/effort xhigh          # in-session
```

```json
// settings.json
{ "effortLevel": "high", "modelSettings": { "claude-opus-5": { "effortLevel": "xhigh" } } }
```

```yaml
# skill or subagent frontmatter
effort: xhigh
```

---

## Claude Code model config

Resolution order (first match wins):

1. `/model <alias|id>` in-session, or `/model` to open the picker
2. `claude --model <alias|id>` at startup
3. `ANTHROPIC_MODEL` environment variable
4. `model` in `~/.claude/settings.json`
5. `ANTHROPIC_DEFAULT_MODEL` (the fallback default; persists after a `/model` override)

```json
{
  "model": "opus",
  "fallbackModel": ["claude-sonnet-5", "claude-haiku-4-5"],
  "env": { "CLAUDE_CODE_SUBAGENT_MODEL": "haiku" }
}
```

- `fallbackModel` — up to three models tried in order when the primary is overloaded.
- **Fast mode** (`/fast`, Opus/Fable) — the same model with faster output, not a downgrade. In Claude Code, `/fast` pairs an Opus/Fable planner with a Sonnet executor.
- **Advisor tool** (`--advisor <model>`, `advisorModel` in managed settings) — pairs your main model with a stronger one you can consult mid-session for hard decisions.
- **Enterprise controls:** `availableModels` + `enforceAvailableModels` restrict the picker; `modelPricing` supplies contracted rates for `/usage`; `modelPicker` curates the `/model` list.

### Context and compaction

- 1M-token context on Opus 5 / Sonnet 5 / Fable 5.1 ≈ 555k words on the current tokenizer.
- Run `/context` to see what loads at session start and what each file read costs.
- `/compact <instructions>` for controlled summarization; auto-compaction triggers near the limit.
- The 1M window is not free — performance still degrades as it fills. Manage context with `/clear` between tasks and subagents for research.

---

## Retired and legacy models

**Retired — API calls fail. Remove every reference:**

| Model | Retired |
|---|---|
| `claude-opus-4-1-*` (Opus 4.1) | Aug 5, 2026 |
| `claude-opus-4-20250514` (Opus 4) | Jun 15, 2026 |
| `claude-sonnet-4-20250514` (Sonnet 4) | Jun 15, 2026 |
| `claude-3-7-sonnet-*` (Sonnet 3.7) | Feb 19, 2026 |
| `claude-3-5-sonnet-*`, `claude-3-5-haiku-*` | 2025–Feb 2026 |
| `claude-3-opus-*`, `claude-3-haiku-*` | Jan–Apr 2026 |
| Claude 2.x | Jul 2025 |

The entire Claude 3.x family is retired. Original Claude 4.0 and 4.1 (Opus 4, Sonnet 4, Opus 4.1) are retired.

**Legacy — still callable, no updates, retirement dates assigned:** Opus 4.5 / 4.6 / 4.7 / 4.8, Sonnet 4.5 / 4.6, Fable 5.

Migrate code with the `/claude-api migrate` bundled skill.

---

## API behavior changes on current models

If you write code against the Messages API (not just Claude Code), these differ from Claude 3.x / 4.0:

| Change | Detail |
|---|---|
| **`budget_tokens` removed** | `thinking: {type: "enabled", budget_tokens: N}` returns 400 on Fable 5/5.1, Opus 5/4.7/4.8, Sonnet 5. Use `thinking: {type: "adaptive"}` or omit it, and set `effort`. |
| **`temperature` / `top_p` / `top_k` deprecated** | A non-default value returns 400 on Opus 4.7+. Steer with prompting. |
| **No assistant prefill** | Prefilling the assistant turn returns 400 on current models. Use structured outputs or system-prompt instructions. |
| **Thinking display defaults to omitted** | Set `thinking: {type: "adaptive", display: "summarized"}` if you stream reasoning. Raw chain-of-thought is never returned. |
| **`refusal` stop reason** | Safety classifiers can decline (HTTP 200, `stop_reason: "refusal"`). Enable server-side `fallbacks`. |
| **Parse tool inputs as JSON** | Use `json.loads()` / `JSON.parse()` — never raw string matching; escaping varies. |
| **Effort is GA** | `output_config: {effort: "..."}`, no beta header. |

---

## Remember

> **Judge cost per completed task, not per request. A cheaper model that needs three turns is not cheaper.**

Selection order:
1. Default to Sonnet 5 at `high`
2. Move to Opus 5 when Sonnet needs repeated correction on the same task
3. Raise effort to `xhigh` for hard coding before reaching for Fable 5.1
4. Pin subagents to Haiku 4.5 for bulk and research
5. Re-tune effort every time you change models
