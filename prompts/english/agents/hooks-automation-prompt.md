# Hooks & Automation Prompt

> **Lifecycle Events** | **Deterministic Guardrails** | **settings.json Schema**

**Use this when:** you need something to happen every time at a specific point in Claude Code's loop — format after an edit, block a command, run a check before a turn ends, log which instructions loaded, enforce a model policy.
**Skip to:** [Protocol](#protocol-hook) · [Hook vs skill vs CLAUDE.md](#hook-vs-skill-vs-claudemd) · [Phase 1 Pick an event](#phase-1-pick-an-event) · [Event reference](#event-reference) · [Phase 2 Config](#phase-2-config--settingsjson-schema) · [Handler types](#handler-types) · [Decision output](#decision-output) · [Recipes](#recipes) · [Remember](#remember)

## Role

You write Claude Code hooks. A hook runs your script, HTTP request, MCP tool call, prompt, or subagent when Claude Code reaches a lifecycle event. Unlike CLAUDE.md and skills, which are advisory, a hook is deterministic — it always fires on its event. Use hooks for the rules that must hold every time.

## Protocol: HOOK

```
H → HOLD?     — Is this a rule that must be guaranteed? (else CLAUDE.md or a skill)
O → OCCASION  — Pick the exact lifecycle event
O → OPERATION — Pick the handler type: command, http, prompt, mcp_tool, agent
K → KEY       — Set the matcher (and if: for command-pattern conditions)
```

Stop only when the hook fires on exactly the events you intend, its decision output is correct, and it does not slow every turn.

---

## Hook vs skill vs CLAUDE.md

| | Hook | Skill | CLAUDE.md |
|---|---|---|---|
| Runs | A command / request / prompt / subagent | Instructions Claude reads and applies | Text Claude reads at session start |
| Trigger | A lifecycle event — guaranteed | You type `/name`, or Claude matches the description | Every session |
| Determinism | Always fires | Claude decides how to apply it | Advisory only |
| Context cost | Zero unless it returns output | Description each session; body when used | Every request |
| Best for | Lint after edit, block `rm -rf`, test-gate a turn, log, notify | Workflows needing reasoning, reference material | "Always do X" facts, conventions |

**Put guardrails in hooks.** "Never edit `.env`" in CLAUDE.md is a request. A `PreToolUse` hook that denies the edit is enforcement. If a rule must hold every time, it is a hook.

---

## Phase 1: PICK AN EVENT

| Goal | Event |
|---|---|
| Format / lint after Claude edits a file | `PostToolUse` matcher `Write\|Edit` |
| Block a dangerous command | `PreToolUse` matcher `Bash` with `if: Bash(rm *)` |
| Run tests before the turn is allowed to end | `Stop` |
| Add context when the user submits a prompt | `UserPromptSubmit` |
| Set up env / print a reminder at session start | `SessionStart` matcher `startup\|resume\|clear` |
| Clean up at session end | `SessionEnd` |
| Enforce which model can be used | `PreModelSwitch` |
| Log which CLAUDE.md / rules loaded (debugging) | `InstructionsLoaded` |
| React to a watched file changing on disk | `FileChanged` matcher `.env` |
| Replace default git worktree behavior | `WorktreeCreate` / `WorktreeRemove` |
| Verify a subagent's result before it returns | `SubagentStop` |

---

## Event reference

Grouped by area. "Block" = the event can stop or reverse the action.

### Session

| Event | Trigger | Block | Notes |
|---|---|---|---|
| `SessionStart` | Session begins or resumes | No | Matcher `startup\|resume\|clear\|compact\|fork`. Resume hooks receive session staleness + estimated re-cache cost. |
| `SessionEnd` | Session terminates | No | Matcher `clear\|resume\|logout\|prompt_input_exit\|other`. ~1.5s budget. |
| `Setup` | `--init` / `--init-only` / `--maintenance` runs | Yes | One-time setup logic. |

### Per turn

| Event | Trigger | Block | Notes |
|---|---|---|---|
| `UserPromptSubmit` | User submits a prompt | Yes | Block the prompt, add `additionalContext`, or rewrite via `updatedInput`. |
| `UserPromptExpansion` | A slash command expands | Yes | Block the expansion. |
| `Stop` | Claude finishes responding | Yes | Block to keep the conversation going; add context; `updatedOutput`. Overridden after 8 consecutive blocks. |
| `StopFailure` | Turn ended by an API error | No | Output ignored except `terminalSequence`. |

### Tool execution

| Event | Trigger | Block | Notes |
|---|---|---|---|
| `PreToolUse` | Before a tool runs | Yes | `permissionDecision: allow\|deny`; modify `updatedInput`; supports `if:` command-pattern conditions. |
| `PostToolUse` | After a tool succeeds | No (exit 2 shows stderr to Claude) | Lint, validate output, add context. |
| `PostToolUseFailure` | After a tool fails | No | Log failures; surface stderr to Claude. |
| `PostToolBatch` | After a parallel tool batch resolves | Yes | Stop the loop before the next model call. |
| `PermissionRequest` | A tool needs a permission decision | No | Provide a verdict via `decision: allow\|deny`. |
| `PermissionDenied` | Auto mode denied a tool call | No | Suggest a retry via `hookSpecificOutput.retry: true`. |

### Subagents & tasks

| Event | Trigger | Block |
|---|---|---|
| `SubagentStart` | A subagent is spawned | No |
| `SubagentStop` | A subagent finishes | Yes — prevent it stopping |
| `TaskCreated` | A task is created via TaskCreate | Yes — rolls back creation |
| `TaskCompleted` | A task is marked completed | Yes — prevents completion |
| `TeammateIdle` | An agent-team teammate goes idle | Yes — keep it working |

### Config, model, files

| Event | Trigger | Block | Notes |
|---|---|---|---|
| `ConfigChange` | A settings file changes | Yes (except `policy_settings`) | Matcher `user_settings\|project_settings\|local_settings\|policy_settings\|skills`. |
| `InstructionsLoaded` | CLAUDE.md / rules load | No | Matcher `session_start\|nested_traversal\|path_glob_match\|include\|compact`. Best tool for debugging what loaded. |
| `PreModelSwitch` | Before a model change | Yes | Enforce a model policy. |
| `PostModelSwitch` | After a model change | No | Matcher = model names/patterns. `switch_reason: user_requested\|auto_recovery\|resume`. |
| `FileChanged` | A watched file changes on disk | No | Matcher = literal filenames. |
| `DirectoryAdded` / `CwdChanged` | A dir is added / cwd changes | No | `CwdChanged` for direnv-style env sync. |
| `WorktreeCreate` / `WorktreeRemove` | Worktree lifecycle | Yes | Replace default git behavior. |

### Compaction, display, MCP

| Event | Trigger | Block |
|---|---|---|
| `PreCompact` / `PostCompact` | Before / after context compaction | `PreCompact` yes |
| `Notification` | Claude Code sends a notification | No |
| `MessageDisplay` | An assistant message streams | No |
| `Elicitation` / `ElicitationResult` | An MCP server requests / returns user input | No |

---

## Phase 2: CONFIG — settings.json schema

Hooks live in `settings.json` (user / project / local), a plugin's `hooks/hooks.json`, or skill/agent frontmatter.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(rm *)",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-rm.sh",
            "timeout": 30,
            "statusMessage": "Checking for destructive commands..."
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "prettier", "args": ["--write", "${tool_input.file_path}"], "async": true }
        ]
      }
    ]
  }
}
```

### Matcher patterns

| Matcher | Evaluation |
|---|---|
| `"*"` or omitted | Every occurrence |
| `Bash`, `Edit\|Write` | Exact tool name / list |
| `mcp__memory__.*`, `^Notebook` | Regex, unanchored |

Tool events match on `tool_name`. Session events match on how the session started (`startup`, `resume`, `clear`). `Notification` matches the notification type (`permission_prompt`, `agent_completed`).

### Hook scope & precedence

| Location | Scope |
|---|---|
| `~/.claude/settings.json` | All your projects |
| `.claude/settings.json` | This project (commit it) |
| `.claude/settings.local.json` | This project, not committed |
| plugin `hooks/hooks.json` | While the plugin is enabled |
| skill / agent frontmatter `hooks:` | While that skill/agent is active |
| managed settings | Org-wide |

Hooks **merge** — every registered hook fires for its matching event regardless of source. `disableAllHooks: true` turns them all off.

---

## Handler types

| `type` | Runs | Config |
|---|---|---|
| `command` | A shell command; JSON on stdin, decision via exit code + stdout | `command`, `args` (exec form, no shell), `timeout`, `async`, `shell` (`bash`/`powershell`) |
| `http` | POST to a URL with the hook JSON as the body | `url`, `headers`, `allowedEnvVars`, `timeout` |
| `mcp_tool` | A tool on a connected MCP server; output treated like stdout | `server`, `tool`, `input` (supports `${tool_input.field}`) |
| `prompt` | A single-turn evaluation by a Claude model | `prompt` (supports `$ARGUMENTS`), `model`, `timeout` |
| `agent` | A subagent with Read/Grep/Glob to verify a condition (experimental) | `prompt`, `timeout` |

### Hook input (stdin JSON, common fields)

```json
{
  "session_id": "...",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/working/dir",
  "permission_mode": "default|plan|auto|acceptEdits|bypassPermissions",
  "hook_event_name": "PreToolUse",
  "effort": { "level": "low|medium|high|xhigh|max" },
  "tool_name": "Bash",
  "tool_input": { "command": "..." }
}
```

Subagent hooks also get `agent_id` and `agent_type`.

---

## Decision output

Exit code:
- **0** — success; JSON on stdout is honored if valid
- **2** — block the action (overrides the JSON `permissionDecision`)
- other — non-blocking error on most events

JSON on stdout:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny",
    "permissionDecisionReason": "why",
    "additionalContext": "info for Claude",
    "updatedInput": { "command": "modified command" },
    "retry": true
  },
  "systemMessage": "shown to Claude",
  "terminalSequence": ""
}
```

---

## Recipes

### Format after every edit

```json
{ "hooks": { "PostToolUse": [ { "matcher": "Write|Edit",
  "hooks": [ { "type": "command", "command": "prettier", "args": ["--write", "${tool_input.file_path}"], "async": true } ] } ] } }
```

### Block writes to a protected directory

```json
{ "hooks": { "PreToolUse": [ { "matcher": "Write|Edit", "hooks": [
  { "type": "command", "if": "Edit(migrations/**)", "command": ".claude/hooks/deny.sh" } ] } ] } }
```

`deny.sh`:

```bash
#!/bin/bash
jq -n '{ hookSpecificOutput: { hookEventName: "PreToolUse",
  permissionDecision: "deny", permissionDecisionReason: "migrations are hand-authored" } }'
```

### Test-gate the end of a turn

```json
{ "hooks": { "Stop": [ { "hooks": [
  { "type": "command", "command": "npm test --silent || echo '{\"decision\":\"block\",\"reason\":\"tests failing\"}'" } ] } ] } }
```

### Block a model switch away from policy

```json
{ "hooks": { "PreModelSwitch": [ { "hooks": [
  { "type": "command", "command": ".claude/hooks/enforce-model.sh" } ] } ] } }
```

### Debug which instructions loaded

```json
{ "hooks": { "InstructionsLoaded": [ { "hooks": [
  { "type": "command", "command": "jq -c . >> .claude/instructions.log" } ] } ] } }
```

### Community recipe set

The hooks power users share most often:

| Hook | Event | Purpose |
|---|---|---|
| Format on edit | `PostToolUse` `Write\|Edit` | Prettier / Ruff / `cargo fmt` on the edited file (`async: true`) |
| Test the matching file | `PostToolUse` `Write\|Edit` | Run the test file that covers the edited source |
| Block dangerous bash | `PreToolUse` `Bash` | Deny `rm -rf`, `dd if=`, `git reset --hard`, force push |
| Secret scanner | `PreToolUse` `Write\|Edit` | Block an edit whose content matches `sk-`, `AKIA`, `BEGIN [A-Z ]*PRIVATE KEY` |
| Cost tracker | `Stop` | Append session token spend to a CSV — the most-requested hook in 2026, because agent loops can run 10x over budget |
| Sub-agent ROI | `SubagentStop` | Log each subagent's duration and token count |
| Issue-ID linker | `PostToolUse` `Bash(git commit *)` | Prepend the ticket ID parsed from the branch name to the commit message |
| PR description generator | `Stop` | Draft a PR title and body from the session transcript |
| Long-task notifier | `Notification` matcher `permission_prompt\|idle_prompt` | OS notification / Slack webhook when Claude needs you or finishes |

Watch `/context` and `/usage` on long unattended runs, and cap fan-outs — test on one directory before the whole repo.

Claude can write any of these for you: *"write a hook that runs eslint --fix after every file edit"*, *"write a Stop hook that logs this session's token cost to costs.csv"*.

---

## Remember

> **A hook is the only advisory-free layer. If a rule must hold every time, it is a hook — not a CLAUDE.md line.**

Before adding a hook:
1. It enforces something that must be guaranteed, not merely encouraged
2. It fires on exactly the right event and matcher
3. Its decision output (exit code + JSON) is correct for that event
4. It does not add latency to every turn (`async: true` for fire-and-forget)
