# Claude Code Native Features Guide

> **Plan Mode & Permissions** | **Checkpoints & Context** | **Surfaces & Commands**

**Use this when:** you need to know what a current Claude Code build can do — how to plan before editing, control permissions, rewind, run headless, manage context, or move a session between devices.
**Skip to:** [Protocol](#protocol-drive) · [Plan mode](#plan-mode) · [Permission modes](#permission-modes) · [Sandboxing](#sandboxing) · [Checkpoints & rewind](#checkpoints--rewind) · [Context management](#context-management) · [Background & headless](#background-tasks--headless-mode) · [Sessions](#sessions--continuity) · [Output styles & statusline](#output-styles--statusline) · [Surfaces](#surfaces) · [Command surface](#command-surface) · [Remember](#remember)

## Role

You use Claude Code's native features deliberately: plan before editing uncertain changes, keep permissions tight but unobtrusive, rewind instead of over-planning, keep context clean, and move work between terminal, desktop, web, and phone without re-explaining it.

## Protocol: DRIVE

```
D → DECIDE    — Plan mode for uncertain/multi-file changes; skip it for one-line diffs
R → RESTRICT  — Set the permission mode and allowlist for the risk level
I → ISOLATE   — Subagents for research; /clear between unrelated tasks
V → VERIFY    — Give Claude a check it can run; /rewind if a risky try fails
E → EXTEND    — Headless for CI; background tasks for long commands; teleport between devices
```

---

## Plan mode

Claude reads, explores, and writes a plan, but does not edit source.

- Enter: `Shift+Tab` until the bar shows `⏸ plan mode on`, or `claude --permission-mode plan`, or `/plan` to prefix one prompt.
- `Ctrl+G` opens the plan in your editor to edit it directly before Claude proceeds.
- On approval you choose: use auto mode, manually approve edits, or keep planning.
- Approving generates a session title.

**Use plan mode when** the approach is uncertain, the change touches multiple files, or you are unfamiliar with the code. **Skip it** when you could describe the diff in one sentence.

The four-phase workflow: **explore** (plan mode, read the relevant code) → **plan** (ask for a written plan) → **implement** (approve, let Claude code against the plan) → **commit** (descriptive message + PR).

---

## Permission modes

| Mode | Config value | Runs without asking |
|---|---|---|
| **Manual** | `default` | Reads only |
| **Accept edits** | `acceptEdits` | Reads + file edits + common FS commands within the working dir |
| **Plan** | `plan` | Reads + classifier-approved commands |
| **Auto** | `auto` | Everything, with a background safety classifier |
| **Don't ask** | `dontAsk` | Only pre-approved tools |
| **Bypass** | `bypassPermissions` | Everything — isolated containers/VMs only |

- `Shift+Tab` cycles Manual → Accept edits → Plan, with Auto and Bypass slotted in where available.
- **Auto mode is the default starting mode on Pro / Max / Team plans** in the terminal and VS Code. Enterprise seats and Console API keys start in Manual. `-p` and the Agent SDK start in Manual.
- **`"auto"` and `"bypassPermissions"` in project or local settings are ignored** — they must be in `~/.claude/settings.json` or managed settings. `defaultMode: "bypassPermissions"` in project/local settings is also ignored.

### How auto mode works

A separate classifier model reviews actions before they run and blocks anything that escalates beyond your request, targets unrecognized infrastructure, or looks driven by hostile content Claude read. It also screens inter-agent messages and critical-path removals (`rm -rf /`, `rm -rf ~`).

Blocked by default: `curl | bash`, sending sensitive data off-origin, production deploys/migrations, mass cloud-storage deletion, granting IAM/repo permissions, force push, `git reset --hard`, `git clean -fd`, `git stash drop`, amending pushed commits, `terraform/pulumi/cdk destroy`, writing to secret managers, toggling production feature flags, printing live credentials, writing to Claude Code's own transcripts, repointing API base URLs or git remotes to third-party hosts.

Allowed: local file ops in the working dir, installing declared dependencies, reading `.env` and sending creds to the matching API, read-only HTTP, pushing to any branch of the repo you are working in.

`claude auto-mode defaults` prints the full rule lists. The `/permissions` **Auto mode** tab views and edits classifier rules.

### Permission rules

`/permissions` or `settings.json` `allow` / `deny` / `ask` arrays:

```json
{
  "permissions": {
    "allow": ["Bash(npm run test:*)", "Bash(git commit *)", "Read(src/**)"],
    "deny": ["Read(**/.env)", "Edit(migrations/**)"],
    "ask": ["Bash(git push *)"]
  }
}
```

- **Deny rules block in every mode**, including `bypassPermissions`.
- Allow rules have no effect in `bypassPermissions`.
- Parameter matching: `Agent(model:opus)`, `Read(**/.env)`, `Skill(deploy *)`, `mcp__github`.
- `/fewer-permission-prompts` scans your transcripts and proposes an allowlist.

---

## Sandboxing

`/sandbox` or `sandbox.enabled` — OS-level filesystem and network isolation on macOS / Linux / WSL2. Auto-allow mode lets sandboxed commands run without asking, independent of the classifier, and works in Manual mode. Sandbox network requests route through the classifier.

`--restricted` (`CLAUDE_CODE_RESTRICTED=1`) removes code-execution tools and `WebFetch`, confines file tools to the working dir, refuses `bypassPermissions`, and ignores user/project/local settings.

---

## Checkpoints & rewind

- Every prompt creates a checkpoint. Claude snapshots files before each change.
- `Esc Esc` or `/rewind` opens the menu: restore conversation only, code only, both, or **Summarize from here** / **Summarize up to here** (partial compaction).
- Checkpoints are saved with the conversation — close the terminal, resume later, still rewind.
- **Checkpoints only track changes made through Claude's file-editing tools.** Bash and external-process changes are not captured. This is not a git replacement.

Tell Claude to try something risky; if it fails, rewind and try another approach. That beats over-planning every move.

---

## Context management

The context window holds the whole conversation — every message, file read, and command output. Performance degrades as it fills.

| Tool | Use |
|---|---|
| `/clear` | Reset context between unrelated tasks. After two failed corrections on one issue, `/clear` and write a better prompt. |
| `/compact <instructions>` | Controlled summarization: `/compact focus on the API changes` |
| `/rewind` → Summarize | Compact only part of the conversation |
| `/btw <question>` | Ask a side question whose answer never enters history |
| Subagents | Research and verification in a separate context that returns only a summary |
| `/context` | See what loads at startup and what each file read costs |
| CLAUDE.md compaction note | `When compacting, always preserve the list of modified files and test commands` |

Project-root CLAUDE.md is re-read from disk and re-injected after `/compact`. Nested and path-scoped rules reload as matching files are touched. Conversation-only instructions are lost — add them to CLAUDE.md to persist.

---

## Background tasks & headless mode

### Background tasks

`Ctrl+B`, or pass `run_in_background` to a Bash call — the command runs async and returns a task ID immediately. Claude polls its output via `Monitor` and streams new lines into context. `/tasks` lists them. `/background` (`/bg`) detaches the whole session. `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` disables.

### Headless / print mode

```bash
claude -p "explain what this project does"
claude -p "list all API endpoints" --output-format json
claude -p "analyze this log" --output-format stream-json --verbose
claude --permission-mode auto -p "fix all lint errors"
tail -200 app.log | claude -p "flag any anomalies"
```

- Still creates a resumable session unless `--no-session-persistence`.
- `json` returns one object with a `result` field; `stream-json` prints one object per line starting with an init event.
- `--allowedTools "Edit,Bash(git commit *)"` scopes an unattended run.
- Use for CI, pre-commit hooks, and fan-out loops. See [multi-agent-orchestration-prompt](../agents/multi-agent-orchestration-prompt.md) for `/batch` and loop patterns.

---

## Sessions & continuity

| Command | Effect |
|---|---|
| `claude --continue` | Resume the last session |
| `claude --resume` | Pick from a list |
| `/rename <name>` | Name a session; treat sessions like branches (`oauth-migration`) |
| `/branch [name]` | Fork the conversation to try a different direction |
| `/fork [prompt]` | Copy the conversation into a new background session (keeps the prompt cache) |
| `/cd <path>` | Move the session to a new working directory without rebuilding the prompt cache |
| `/add-dir <path>` | Grant file access to another directory |
| `claude --teleport` | Pull a web session into this terminal |
| `claude --cloud` | Push the current session to the cloud, continue on mobile |

`ANTHROPIC_DEFAULT_MODEL` sets the model new sessions start on.

---

## Output styles & statusline

- **Output styles** (`/output-style`, or the Output style row in `/config`): change how Claude formats responses. Built-in **Concise** leads with the result and skips preamble; work is just as thorough. **Proactive** favors autonomous behavior. Custom project and plugin styles are supported.
- **Statusline** (`statusLine` in `settings.json`, or `/statusline`): an external script that emits the status line — model, cwd, context usage, cost. Recommended for tracking context continuously. `subagentStatusLine` for subagents.

---

## Cost control

Claude Code's cost can run away in agentic loops — the most common community complaint in 2026. Guardrails:

- Watch `/context` (fill level) and `/usage` (spend) on long runs.
- Cap unattended runs: `--max-turns`, a `/goal` that stops on a condition, a size guideline for dynamic workflows.
- Test a fan-out on one directory before the whole repo.
- A `Stop` hook that logs session token cost to CSV makes spend visible over time.
- Pin `effortLevel` in settings so a product-side default change doesn't silently move it.

The Pro plan ($20/mo) hits its ceiling fast under heavy agent use; sustained agentic work needs Max.

---

## Surfaces

| Surface | Use |
|---|---|
| **Terminal** | The full CLI; daily interactive use |
| **VS Code / JetBrains** | Inline diffs, `@`-mentions, plan review; model + effort in the footer |
| **Desktop app** | Parallel sessions each in a worktree, visual diffs, scheduled tasks, an iOS Simulator pane, a built-in browser |
| **Claude Code on the web** (`claude.ai/code`) | Cloud sessions on Anthropic infra; long tasks you check back on; repos you don't have locally |
| **Mobile** (Claude app) | Start, monitor, steer tasks from a phone |
| **Remote Control** | Continue a local session from a phone or browser |
| **Slack** | `@Claude` a bug report, get a PR back |
| **Chrome** | Debug live web apps; automate form filling |
| **GitHub Actions** (`anthropics/claude-code-action`) | PR review, issue triage, `@claude` mentions in CI |
| **Routines** | Scheduled cloud agents (`/schedule`); each run is a fresh remote session |
| **Agent SDK** | Claude Code as a library — see [agent-sdk-guide](agent-sdk-guide.md) |

Every surface shares the same engine, so CLAUDE.md, settings, and MCP servers carry across.

For how Claude Code compares to Cursor, Codex, Aider, and Cline — and how to make one config serve all of them via `AGENTS.md` — see [reference-resources.md](reference-resources.md).

---

## Command surface

Grouped. Bundled skills marked **[S]**.

**Session & context:** `/clear` `/resume` `/branch` `/fork` `/compact` `/context` `/export` `/rewind` `/btw` `/cd` `/add-dir`

**Model & performance:** `/model` `/effort` `/fast` `/advisor`

**Quality:** `/code-review` **[S]** (`--fix`, `--comment`, `ultra`) `/security-review` **[S]** `/verify` **[S]** `/debug` **[S]** `/simplify`

**Parallel & workflows:** `/batch` **[S]** `/background` `/tasks` `/loop` **[S]** `/deep-research` `/goal` `/subtask` `/workflows`

**Setup & config:** `/init` `/memory` `/mcp` `/permissions` `/hooks` `/agents` `/skills` `/plugin` `/config` `/doctor` **[S]** `/statusline` `/output-style` `/theme` `/keybindings`

**Usage:** `/usage` `/cost` `/status` `/insights` `/context`

**Cross-device:** `/remote-control` `/teleport` `/desktop` `/mobile` `/list-agents` `/autofix-pr`

**Reference:** `/claude-api` **[S]** `/help` `/powerup` `/import` (from Codex/Gemini)

Custom commands: `.claude/commands/*.md` (flat) or `.claude/skills/<name>/SKILL.md` (directory). Both support `$ARGUMENTS`, `$0`/`$1`, named `arguments:`, `` !`cmd` `` injection, `@file` refs. See [agent-skills-prompt](../agents/agent-skills-prompt.md).

---

## Remember

> **Plan mode for uncertain changes, `/clear` between tasks, `/rewind` instead of over-planning, and always give Claude a check it can run.**

Priorities:
1. Match the permission mode to the risk, then allowlist the safe commands so you stop clicking
2. Keep context clean — subagents for research, `/clear` between unrelated work
3. Give Claude verification (tests, build, screenshot); review its evidence, not just its claim
4. Move work between surfaces instead of re-explaining it
