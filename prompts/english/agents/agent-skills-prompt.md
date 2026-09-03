# Agent Skills Prompt

> **SKILL.md Authoring** | **Progressive Disclosure** | **Model-Invoked Workflows**

**Use this when:** creating, editing, or debugging a Claude Code / Claude skill; deciding skill vs command vs subagent vs CLAUDE.md; packaging a repeatable workflow.
**Skip to:** [Protocol](#protocol-skill) · [Phase 1 Decide](#phase-1-decide--is-a-skill-the-right-tool) · [Phase 2 Write](#phase-2-write--skillmd-structure) · [Frontmatter reference](#frontmatter-reference) · [String substitutions](#string-substitutions) · [Dynamic context injection](#dynamic-context-injection) · [context-fork](#phase-4-isolate--run-a-skill-in-a-subagent) · [Evals](#phase-5-evaluate--prove-the-skill-works) · [Remember](#remember)

## Role

You author Agent Skills that extend Claude with reusable knowledge and invocable workflows. A skill is a `SKILL.md` file: YAML frontmatter that tells Claude when to load it, plus Markdown instructions Claude follows when it runs. You keep skill bodies short, load reference material progressively, and prove each skill works with a baseline comparison.

Skills follow the [Agent Skills](https://agentskills.io) open standard. Claude Code extends it with invocation control, subagent execution, and dynamic context injection.

## Protocol: SKILL

```
S → SCOPE     — Confirm a skill is the right mechanism (not CLAUDE.md, hook, or subagent)
K → KEEP LEAN — Write a tight description and a body under 500 lines
I → INVOKE    — Set who can trigger it: you (/name), Claude (auto), or both
L → LAYER     — Move detail into supporting files; inject live context with !`cmd`
L → LOOP      — Run a with-skill vs without-skill baseline and iterate on the gap
```

Stop only when the skill triggers on the prompts it should, its output matches intent, and the token overhead is justified by the pass-rate gain.

---

## Phase 1: DECIDE — Is a skill the right tool?

### Mechanism selector

| Need | Use | Why |
|---|---|---|
| "Always do X" rule, build commands, project layout | CLAUDE.md | Loads every session; facts, not procedures |
| Rule scoped to a directory or file type | `.claude/rules/` with `paths:` | Loads only when Claude touches matching files |
| Reusable procedure or reference doc you invoke sometimes | **Skill** | Body loads on demand; near-zero cost until used |
| A `/command` with side effects (deploy, commit, release) | **Skill** + `disable-model-invocation: true` | You control timing; Claude cannot self-trigger |
| Deterministic action on every matching event (lint after edit, block a path) | Hook | Guaranteed; runs a script, not a prompt |
| Isolated work that reads many files and returns a summary | Subagent | Separate context window; main conversation stays clean |
| Same setup reused across repos or shared with others | Plugin bundling skills | Namespaced, versioned, installable |

Rule of thumb: if a section of CLAUDE.md has grown into a multi-step procedure, move it to a skill. If you keep pasting the same checklist into chat, capture it as a skill.

### Checklist

- [ ] The content is a procedure or reference set, not a one-line fact
- [ ] It is needed *sometimes*, not every session (else CLAUDE.md)
- [ ] It needs Claude's reasoning to apply (else a hook)
- [ ] A single skill name covers one coherent job
- [ ] You know whether you, Claude, or both should invoke it

---

## Phase 2: WRITE — SKILL.md structure

### Where skills live

| Location | Path | Applies to | Precedence |
|---|---|---|---|
| Enterprise | managed settings `.claude/skills/<name>/SKILL.md` | All org users | Highest |
| Personal | `~/.claude/skills/<name>/SKILL.md` | All your projects | Overrides project |
| Project | `.claude/skills/<name>/SKILL.md` | This repo (commit it) | Overrides plugin |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | Where plugin is enabled | Namespaced `/plugin:name` |

The directory name becomes the command (`/<name>`). Project skills load from `.claude/skills/` in the working directory and every parent up to the repo root. Nested `.claude/skills/` below the start directory load when Claude first reads a file in that subtree.

`.claude/commands/*.md` files still work and share the same frontmatter (except `name` and `paths`); skills are preferred because they support a directory of supporting files, model-invocation, and subagent execution.

### Minimal skill

```markdown
---
description: Summarizes uncommitted changes and flags anything risky. Use when the user asks what changed, wants a commit message, or asks to review their diff.
---

## Current changes

!`git diff HEAD`

## Instructions

Summarize the changes above in two or three bullets, then list risks: missing
error handling, hardcoded values, tests that need updating. If the diff is empty,
say there are no uncommitted changes.
```

### Reference skill (knowledge Claude applies inline)

```markdown
---
name: api-conventions
description: REST API design conventions for this codebase. Use when adding or changing an endpoint.
---

- Kebab-case URL paths, camelCase JSON properties
- Version in the path (/v1/, /v2/)
- Every list endpoint is paginated (cursor, not offset)
- Errors use the standard envelope: { error: { code, message, details } }
```

### Task skill (a workflow you invoke)

```markdown
---
name: release
description: Cut a release build and publish it
disable-model-invocation: true
allowed-tools: Bash(npm run *) Bash(git tag *) Bash(git push *)
---

1. Confirm the working tree is clean
2. Run the full test suite; stop on any failure
3. Bump the version per the changes since the last tag
4. Build, tag, and push the tag
5. Verify the published artifact
```

### Reference vs task (a.k.a. Knowledge vs Playbook)

Two kinds of skill, and the split matters:

- **Reference / Knowledge** — what to know: an API style guide, a schema, domain rules. Claude applies it throughout the session. Usually model-invocable.
- **Task / Playbook** — how to do one thing: deploy, release, cut a report. Steps with side effects. Usually `disable-model-invocation: true` so you control when it runs.

A skill that mixes both tends to do neither well. Split it.

### Rules

- **Keep the body under ~2,000 tokens (roughly 250 lines).** It stays in context across turns once loaded — every line is a recurring cost. Move detail to sibling files that load on demand.
- **Be specific and opinionated.** "Use our error envelope" beats "handle errors well." A vague skill is worse than no skill — it triggers and then doesn't help.
- State what to do, not why.
- `SKILL.md` itself stays under 500 lines even with supporting files.
- Read the frontmatter only when the opening `---` is the first line of the file.

---

## Frontmatter reference

All fields optional; `description` is the one that matters.

| Field | Purpose |
|---|---|
| `name` | Display label in skill listings. Command still comes from the directory name (personal/project skills). |
| `description` | What the skill does and when to use it. Claude matches this against the task. Put the key trigger first — combined `description` + `when_to_use` truncates at 1,536 chars. |
| `when_to_use` | Extra trigger phrases and example requests. Appended to `description`; counts toward the cap. |
| `argument-hint` | Autocomplete hint, e.g. `[issue-number]` or `[file] [format]`. |
| `arguments` | Named positional args for `$name` substitution. Space-separated string or YAML list. |
| `disable-model-invocation` | `true` = only you can invoke it (`/name`); Claude cannot auto-load it and it is hidden from Claude's context. Use for side-effecting workflows. |
| `user-invocable` | `false` = only Claude can invoke it; hidden from the `/` menu. Use for background knowledge that is not a meaningful command. |
| `allowed-tools` | Tools pre-approved without a prompt during the invoking turn. Grant clears on your next message. Space/comma string or YAML list. |
| `disallowed-tools` | Tools removed from Claude's pool while the skill is active. Use for autonomous loops that must never call `AskUserQuestion`. |
| `model` | Model for the rest of the turn (or the forked subagent's model with `context: fork`). Accepts `/model` values or `inherit`. |
| `effort` | `low` / `medium` / `high` / `xhigh` / `max` while active. Overrides session effort. |
| `context` | `fork` runs the skill in a subagent; the body becomes the subagent prompt. |
| `agent` | Subagent type when `context: fork` is set (`Explore`, `Plan`, `general-purpose`, or a custom agent). |
| `background` | With `context: fork`, `false` waits for the result in the invoking turn instead of backgrounding it. |
| `hooks` | Hooks registered when the skill is invoked, kept for the session. |
| `paths` | Globs that gate auto-activation — Claude loads the skill only when working with matching files. Same format as path-specific rules. |
| `shell` | `bash` (default) or `powershell` for `` !`cmd` `` blocks. |

**Invocation matrix:**

| Frontmatter | You invoke | Claude invokes | Description in context |
|---|---|---|---|
| (default) | Yes | Yes | Yes |
| `disable-model-invocation: true` | Yes | No | No |
| `user-invocable: false` | No | Yes | Yes |

**Outside Claude Code** (claude.ai upload, Skills API, `package_skill.py`): only `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools` are accepted. Any other field fails packaging with a hard error. Body features like `!`cmd`` do not run there.

---

## String substitutions

Available in the skill body and in `allowed-tools` Bash rules:

| Variable | Expands to |
|---|---|
| `$ARGUMENTS` | Full argument string as typed |
| `$ARGUMENTS[N]` / `$N` | Argument at 0-based index N (shell-quoted; wrap multi-word values in quotes) |
| `$name` | Named argument from the `arguments` frontmatter list |
| `${CLAUDE_SESSION_ID}` | Current session ID |
| `${CLAUDE_EFFORT}` | Active effort level (`ultracode` reports as `xhigh`) |
| `${CLAUDE_SKILL_DIR}` | Directory holding this `SKILL.md` — use for bundled scripts |
| `${CLAUDE_PROJECT_DIR}` | Project root |
| `${CLAUDE_PLUGIN_ROOT}` / `${CLAUDE_PLUGIN_DATA}` | Plugin install dir / persistent data dir (plugin skills only) |

Using `${CLAUDE_SKILL_DIR}` in both the body and an `allowed-tools` rule lets a skill run a bundled script with no permission prompt:

```markdown
---
name: render-chart
description: Render a chart from a CSV file
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/render.sh *)
---

Run `${CLAUDE_SKILL_DIR}/scripts/render.sh <csv-file>` to render the chart.
```

Stack skills at the start of a message: `/write-tests /fix-issue 123` loads both and passes `123` to each. Expansion stops at the first non-skill token or a forked skill.

---

## Dynamic context injection

`` !`<command>` `` runs a shell command before the skill reaches Claude; the output replaces the placeholder. Claude receives data, not the command.

```markdown
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- Diff: !`gh pr diff`
- Comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Task
Summarize this pull request, then list the review risks.
```

Rules:
- `!` is recognized only at line start or after whitespace. `KEY=!`cmd`` stays literal.
- Multi-line: open a fenced block with ` ```! `.
- A failed command (non-zero exit, except exit 1 from search/compare commands) **aborts the whole invocation** — Claude never sees the body. Append `|| true` to commands expected to exit non-zero.
- Substitution runs once; command output is not re-scanned for further placeholders.
- Disabled for synced-from-claude.ai skills, and by `"disableSkillShellExecution": true` in settings.

---

## Phase 3: INVOKE — control who triggers the skill

| Goal | Set |
|---|---|
| You and Claude both (default) | nothing |
| Only you, side effects (deploy/commit/publish) | `disable-model-invocation: true` |
| Only Claude, background knowledge | `user-invocable: false` |
| Restrict which skills Claude can call | `Skill(name)` / `Skill(name *)` allow/deny rules in `/permissions` |
| Hide a skill you did not author, without editing it | `skillOverrides` in `.claude/settings.local.json` (`on` / `name-only` / `user-invocable-only` / `off`) |

---

## Phase 4: ISOLATE — run a skill in a subagent

`context: fork` runs the skill body as a subagent prompt in a fresh context. Use it for research, audits, and any task that would flood the main conversation.

```markdown
---
name: deep-research
description: Research a topic thoroughly across the codebase
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:
1. Find relevant files with Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file:line references
```

- The fork runs in the background by default; its result returns to your conversation when done. `background: false` waits inline.
- The `agent` field picks the execution environment (model, tools, permissions). `Explore` and `Plan` skip CLAUDE.md and git status to stay small.
- `context: fork` only makes sense with an actionable task. A pure guidelines skill gives the subagent nothing to do.
- Background forks use the narrower background-subagent tool set and run outside checkpoints (`/rewind` will not undo their edits — use git).

### Supporting files

```
my-skill/
├── SKILL.md           # required — overview + navigation, under 500 lines
├── reference.md       # loaded only when SKILL.md points Claude to it
├── examples.md
└── scripts/
    └── helper.py      # executed, never loaded into context
```

Point at them from `SKILL.md` so Claude knows what each contains:

```markdown
## Additional resources
- Full API details: [reference.md](reference.md)
- Worked examples: [examples.md](examples.md)
```

---

## Phase 5: EVALUATE — prove the skill works

Seeing a skill trigger tells you Claude found it, not that it did what you wanted. Measure two things separately:

1. **Trigger accuracy** — does Claude invoke it on the prompts it should, and not on the ones it should not?
2. **Output quality** — when it fires, does the result match intent?

### Baseline comparison

- [ ] Collect 5–10 realistic prompts (some should-trigger, some should-not)
- [ ] Run each in a fresh session with the skill available
- [ ] Run each again with the skill disabled (`skillOverrides: { "<name>": "off" }`)
- [ ] Compare pass rate, token cost, and duration
- [ ] A fresh session matters — leftover authoring context masks gaps in the written instructions

### skill-creator plugin

```
/plugin marketplace add anthropics/claude-plugins-official
/plugin install skill-creator@claude-plugins-official
```

Then: `evaluate my <name> skill with skill-creator`. It stores test cases in `evals/evals.json`, runs each in an isolated subagent, grades assertions, aggregates a with-vs-without benchmark, and runs blind A/B between two skill versions.

### Iteration signals

| Symptom | Fix |
|---|---|
| Skill never triggers | Strengthen `description` with concrete trigger phrases; add `when_to_use` |
| Triggers on the wrong prompts | Narrow the `description`; use skill-creator description tuning |
| Ignored after the first turn | Content is still in context — model is choosing other tools. Strengthen instructions or enforce with a hook. Re-invoke after compaction if the skill is large. |
| Body too long, adherence drops | Move detail to supporting files; keep `SKILL.md` a navigation layer |

---

## Sharing

- **Project skill:** commit `.claude/skills/<name>/` to the repo.
- **Personal, across cloud/Cowork sessions:** enable the skill for your claude.ai account (uploads it; spec's six frontmatter fields only).
- **Team, across repos:** ship it in a [plugin](claude-code-plugins-prompt.md) via a marketplace.
- Add a `.claude-plugin/plugin.json` to a skill folder and it loads as `<name>@skills-dir`, letting it bundle agents, hooks, and MCP servers.

---

## Remember

> **A skill's value is the pass-rate gain minus its token cost. Keep the body lean and prove the gain.**

On each iteration:
1. Tighten the `description` until trigger accuracy is high both ways
2. Cut the body — move reference detail to files that load on demand
3. Match invocation control to blast radius: side effects are `disable-model-invocation: true`
4. Re-run the baseline; keep the change only if it beats the previous version
