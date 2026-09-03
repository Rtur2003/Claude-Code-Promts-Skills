# Multi-Agent Orchestration Prompt

> **Native Subagents** | **Dynamic Workflows** | **Adversarial Review**

**Use this when:** a task needs more than one agent — parallel research, an isolated worker, a codebase-wide audit or migration, a writer/reviewer split, or an unattended run that verifies its own output.
**Skip to:** [Protocol](#protocol-delegate) · [Five patterns](#the-five-composable-patterns) · [Pick a mechanism](#pick-a-mechanism) · [Phase 1 Subagents](#phase-1-subagents--isolated-workers) · [Phase 2 Workflows](#phase-2-dynamic-workflows--scripted-orchestration) · [Phase 3 Fan-out](#phase-3-fan-out--batch-and-headless-loops) · [Phase 4 Review](#phase-4-adversarial-review) · [Parallel humans](#parallel-human-driven-sessions) · [Remember](#remember)

## Role

You coordinate multiple agents on one task. Claude Code gives you four mechanisms: **subagents** (isolated workers Claude spawns), **dynamic workflows** (a script that orchestrates many subagents), **`/batch`** (fan-out with one PR per unit), and **parallel human-driven sessions** (worktrees, agent view, agent teams, cross-session messaging). You pick by who holds the plan and how much coordination the task needs, keep intermediate work out of the main context, and never let the agent that did the work be the one that grades it.

## Protocol: DELEGATE

```
D → DECOMPOSE  — Split the task into independent units
E → ELECT      — Pick the mechanism: subagent, workflow, /batch, or parallel sessions
L → LAUNCH     — Spawn with the right agent type, model, and tool scope
E → EXCHANGE   — Pass findings by summary, not by full transcript
G → GATE       — A fresh agent verifies each result against the spec
A → ASSEMBLE   — Merge; resolve conflicts by Security > Correctness > Convention
T → TRIM       — Keep only conclusions in the main context
E → EVALUATE   — Did isolation and parallelism actually pay off?
```

Stop only when every unit is verified by an agent that did not build it, and the merged result passes the task's own check.

---

## The five composable patterns

Anthropic's "Building Effective Agents" defines five patterns. Most multi-agent work is one of these — name the pattern before you build:

| Pattern | Shape | Use for |
|---|---|---|
| **Prompt chaining** | Step A's output feeds step B | A task with clean sequential subtasks (outline → draft → polish) |
| **Routing** | Classify the input, send it to a specialized handler | Distinct request types that need different handling |
| **Parallelization** | Run independent subtasks at once, aggregate | Sectioning work, or voting for confidence |
| **Orchestrator-workers** | A lead decides the subtasks dynamically and delegates | Work where the subtasks aren't known up front |
| **Evaluator-optimizer** | One agent produces, another critiques, loop | Output that measurably improves with a review round |

**Challenge-and-converge:** for a hard bug or a contested decision, run three agents on the same question and tell each to challenge the others' findings. A single agent stops at the first plausible cause; three that argue converge on the real one.

**Keep the deterministic parts deterministic.** Production agent systems blend fixed code with strategic LLM decision points — they are not one big agentic loop. If a step can be a script, make it a script (a hook, a dynamic-workflow line), and spend the model's judgment where it actually matters.

---

## Pick a mechanism

| | Subagent | Dynamic workflow | `/batch` | Parallel sessions |
|---|---|---|---|---|
| **What it is** | A worker Claude spawns for a turn | A JavaScript script Claude writes and a runtime executes | A bundled skill that splits a change across 5–30 subagents | Full Claude Code sessions you run and check |
| **Who plans** | Claude, turn by turn | The script | The `/batch` skill | You |
| **Results live in** | Claude's context (a summary) | Script variables (out of context) | One PR per unit | Each session |
| **Scale** | A few per turn | Dozens to hundreds of agents | 5–30 units, one PR each | A handful |
| **Use for** | Research, one isolated worker, a review | Codebase audit, large migration, cross-checked research | Repo-wide refactor or migration you want as PRs | Long independent workstreams, writer/reviewer |
| **Invoke** | "use a subagent to…", `@agent-name`, `/subtask` | "use a workflow to…", `ultracode`, `/deep-research` | `/batch <instruction>` | `git worktree`, `claude agents`, `--worktree` |

Rule: reach for the lightest one that fits. A subagent for a focused question. A workflow when the job outgrows a handful of subagents or you want findings cross-checked. `/batch` when you want the output as reviewable PRs. Parallel sessions when the streams are long-lived and you want to steer each.

---

## Phase 1: SUBAGENTS — isolated workers

A subagent runs in its own context window with its own system prompt and tool set, and returns a summary. Use it for work that would flood the main conversation with file contents or search output you will not reference again.

### Definition file

`.claude/agents/<name>.md`:

```markdown
---
name: security-reviewer
description: Reviews a diff for injection, auth, secrets, and unsafe data handling. Use after a feature touches auth or user input.
tools: Read, Grep, Glob, Bash
model: opus
permissionMode: plan
skills: [security-checklist]
memory: project
---
You are a senior security engineer. Review only the diff you are given.
For each finding: the file:line, the vulnerability class, an exploit sketch, and a fix.
Flag only issues that affect correctness or the stated requirements.
```

| Field | Use |
|---|---|
| `name`, `description` | Required. `description` drives auto-delegation — write concrete triggers. |
| `tools` | Allowlist. Omit to inherit the full subagent tool set. |
| `disallowedTools` | Denylist (inherit minus these). |
| `model` | `sonnet` / `opus` / `haiku` / `fable` / `inherit`. Cheap model for bulk or scoped work. |
| `permissionMode` | `default` / `acceptEdits` / `auto` / `plan` / `bypassPermissions`. |
| `skills` | Skills preloaded in full at launch as reference material. |
| `memory` | `user` / `project` / `local` — the subagent keeps its own auto memory. |
| `isolation: worktree` | Run in an isolated git worktree so edits do not collide. |
| `maxTurns`, `background`, `hooks` | Turn cap; force background; register session hooks. |

**Scope precedence** (highest first): managed settings → `--agents` CLI → `.claude/agents/` → `~/.claude/agents/` → plugin `agents/`.

### Built-in subagents

| Agent | Model | Tools | Use |
|---|---|---|---|
| **Explore** | Inherits (capped at Opus) | Read-only | Fast codebase search; skips CLAUDE.md and git status |
| **Plan** | Inherits | Read-only | Research before plan mode |
| **general-purpose** | Configurable | All subagent tools | Multi-step tasks needing exploration and action |

### Invoking

```
Use a subagent to investigate how token refresh works and whether we have OAuth utilities to reuse.
@"security-reviewer" review the diff on this branch.
/subtask draft unit tests for the parser changes so far
```

- `/subtask` (and a `context: fork` skill) creates a **fork** — a subagent that inherits the full conversation and prompt cache, runs in the background, keeps its tool calls out of the main context.
- Non-teammate spawns default to background in interactive sessions; permission prompts surface in the main session.
- Subagents can nest up to 3 levels deep.
- Model selection order: per-invocation `model` → frontmatter `model` → `CLAUDE_CODE_SUBAGENT_MODEL` env → main model. `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` overrides frontmatter.

### What a subagent receives

Its own system prompt, the task message, the CLAUDE.md hierarchy (except Explore/Plan), a git status snapshot, preloaded skills, the sibling roster. **Not**: conversation history (except forks), output style, the main conversation's auto memory.

### Common patterns

```
Research auth, database, and API modules in parallel using three separate subagents.
Use a subagent to run the test suite and report only the failing tests with their errors.
Use the code-reviewer subagent to find issues, then the optimizer subagent to fix them.
```

---

## Phase 2: DYNAMIC WORKFLOWS — scripted orchestration

A dynamic workflow is a JavaScript script Claude writes that orchestrates many subagents in the background while your session stays responsive. The script holds the loop, the branching, and the intermediate results, so the main context sees only the final answer.

### When a workflow beats subagents

- The job needs more agents than one conversation can coordinate (audit a whole codebase, migrate 500 files).
- You want the orchestration as a script you can read and rerun.
- You want findings **cross-checked** before you see them — independent agents adversarially review each other's output, or a plan is drafted from several angles and weighed.

### Starting one

```
use a workflow to audit every route handler under src/routes/ for missing auth checks, and adversarially verify each finding before reporting it

ultracode: migrate every component under src/components/ from JavaScript to TypeScript, each file in its own isolated copy

/deep-research What changed in the Node.js permission model between v20 and v22?
```

- `ultracode` in a typed prompt triggers one workflow for that task without changing session effort. `/effort ultracode` makes Claude plan a workflow for every substantive task in the session.
- Claude Code shows the planned phases and asks to approve before the run starts.
- `/workflows` opens the progress view — phases, agent counts, token totals; drill into any agent.
- Save a run's script with `s` in `/workflows` → `.claude/workflows/<name>.js` (project) or `~/.claude/workflows/` (personal). It then runs as `/<name>`.

### Script shape

```javascript
export const meta = {
  name: 'audit-routes',
  description: 'Audit every route handler for missing auth checks',
}

const found = await agent('List every .ts file under src/routes/.', {
  schema: { type: 'object', required: ['files'],
    properties: { files: { type: 'array', items: { type: 'string' } } } },
})

const audits = await pipeline(found.files, file =>
  agent(`Audit ${file} for missing authentication checks.`, { label: file }),
)

return audits.filter(Boolean)
```

`agent()` spawns one subagent, `pipeline()` runs one per list item, `parallel()` runs a set at once. Plain JavaScript with top-level `await`; no `import()`, no filesystem or shell from the script itself (agents do that). Limits: 16 concurrent agents, 4,096 items per `pipeline`/`parallel`, 1,000 agents per run.

Run `/workflow-authoring` before editing a saved script — it loads the reference Claude works from.

### Cost

A workflow spawns many agents; a run can use far more tokens than working the task in conversation. Test on a slice first (one directory, a narrow question). Set `workflowSizeGuideline` (`small` <5, `medium` <15, `large` <50) in `/config`. A run over 25 agents or 1.5M projected tokens shows a `Large workflow` warning.

---

## Phase 3: FAN-OUT — `/batch` and headless loops

### `/batch`

```
/batch migrate every file that imports the old logger to the new one
```

In a git repo, `/batch` splits the change across 5–30 subagents, each working in its own worktree, each opening a pull request. Built for migrations, audits, and cross-file refactors where you want the output as reviewable PRs.

### Headless loop

```bash
# 1. produce the list
claude -p "list all Python 2 files that need migrating, save to files.txt"

# 2. one invocation per file
for file in $(cat files.txt); do
  claude -p "Migrate $file from Python 2 to Python 3. Return OK or FAIL." \
    --allowedTools "Edit,Bash(git commit *)"
done
```

Refine the prompt on the first 2–3 files, then run the full set. `--allowedTools` scopes what each unattended invocation can do. Pipe structured output into your own tooling with `--output-format json`.

---

## Phase 4: ADVERSARIAL REVIEW

The longer an agent works unattended, the more an independent check matters. A reviewer in a fresh context sees only the diff and the criteria — not the reasoning that produced the change — so it grades the result on its own terms.

```
Use a subagent to review the rate-limiter diff against PLAN.md. Check that every
requirement is implemented, the listed edge cases have tests, and nothing outside
scope changed. Report gaps that affect correctness or the requirements — not style.
```

- `/code-review` runs a bundled correctness review in a fresh subagent and returns findings to the session.
- The **writer / reviewer** split: session A implements, session B reviews in a clean context (no bias toward code it just wrote), A addresses the feedback.
- The **test-first** split: one agent writes tests, another writes code to pass them.

**Caveat:** a reviewer told to find gaps will report some even when the work is sound. Chasing every finding leads to over-engineering — extra abstraction, defensive code, tests for impossible cases. Tell the reviewer to flag only gaps that affect correctness or the stated requirements; treat the rest as optional.

---

## Parallel human-driven sessions

When workstreams are long-lived and you want to steer each:

| Tool | Use |
|---|---|
| **git worktrees** (`--worktree`, `EnterWorktree`) | Isolated checkouts so edits do not collide |
| **`claude agents`** (agent view) | Dispatch background sessions, watch them from one screen; shows GitHub `#N` / GitLab `!N` |
| **Cross-session messaging** | `@`-mention another session by name; Claude delivers a finding directly (`SendMessage`) |
| **Agent teams** (experimental, off by default) | A team lead with shared tasks, messaging, pipeline or peer-review structure |
| **Desktop app / Claude Code on web** | Manage multiple sessions visually, each in its own worktree |

**Contract-first discipline** still applies across sessions: define shared types and API contracts before parallel implementation; give each session non-overlapping file ownership; merge shared types first, then backend, then frontend, then tests.

### Conflict resolution

| Conflict | Resolution |
|---|---|
| Two agents define a type differently | One shared definition |
| Both edit the same file | One agent per file; coordinator merges |
| Convention clash | Defer to project CLAUDE.md |
| Dependency version clash | Pick the version that satisfies both; pin it |
| Logic clash (different rules for one field) | Coordinator decides; record the decision |

Priority order: **Security > Correctness > Convention > Preference.** Record every non-obvious resolution where the next session will see it.

---

## Anti-patterns

- Multiple agents editing the same file at once
- Overlapping agent scopes with no owner per file
- Passing full conversation transcripts between agents instead of summaries
- Skipping the merge/integration verification step
- The agent that wrote the code also being the one that reviews it
- A workflow launched at full repo scope before testing it on one directory
- `ultracode` on every routine task — it multiplies tokens and time

---

## Remember

> **Isolation is the point: keep each worker's noise out of the main context, and never grade your own work.**

Orchestration priorities:
1. Decompose into independent units before spawning anything
2. Pick the lightest mechanism that fits — subagent before workflow before parallel sessions
3. Pass findings as summaries, not transcripts
4. A fresh agent verifies each result against the spec
5. Merge by Security > Correctness > Convention; record every resolution
