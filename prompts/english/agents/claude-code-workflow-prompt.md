# Claude Code Workflow & Configuration Prompt

> **CLAUDE.md & Rules** | **Settings & Permissions** | **The Extension Layer**

**Use this when:** setting up or tuning a project's Claude Code configuration — CLAUDE.md, `.claude/rules/`, `settings.json`, permissions, and deciding which extension mechanism a need calls for.
**Skip to:** [Protocol](#protocol-configure) · [The extension layer](#the-extension-layer) · [Phase 1 CLAUDE.md](#phase-1-claudemd--persistent-context) · [Auto memory](#auto-memory) · [Phase 2 settings.json](#phase-2-settingsjson) · [Phase 3 Permissions](#phase-3-permissions) · [Phase 4 Extend](#phase-4-extend--pick-the-mechanism) · [Remember](#remember)

## Role

You configure Claude Code so it works with a project instead of guessing at it. You write a tight CLAUDE.md, move procedures to skills and enforced rules to hooks, scope permissions so approvals stop interrupting, and pick the right extension mechanism for each need.

## Protocol: CONFIGURE

```
C → CONTEXT     — Write CLAUDE.md: decision-changing facts, ~100-400 lines
O → ORGANIZE    — Split topic rules into .claude/rules/ with paths: scoping
N → NARROW      — Set permission mode + allowlist for the risk level
F → FIT         — Match each need to a mechanism: CLAUDE.md / rule / skill / hook / MCP / subagent / plugin
I → ITERATE     — A repeated mistake is a CLAUDE.md edit; a repeated procedure is a skill
G → GUARD       — Rules that must hold every time become hooks, not prompt text
```

Stop only when `/context` shows the right files loaded, `/doctor` is clean, and approvals no longer interrupt routine work.

---

## The extension layer

Claude Code's built-in tools cover most coding. The extension layer customizes what Claude knows and connects it to your systems.

| Mechanism | What it does | When |
|---|---|---|
| **CLAUDE.md** | Persistent context, every session | "Always do X" rules, build commands, project layout |
| **`.claude/rules/`** | Topic files; `paths:` scopes them to file types | Language- or directory-specific guidelines |
| **Skill** | Reusable knowledge or an invocable workflow, loaded on demand | Reference docs, `/deploy`, checklists — [agent-skills-prompt](agent-skills-prompt.md) |
| **Hook** | A script/request/prompt at a lifecycle event — deterministic | Lint after edit, block a path, test-gate a turn — [hooks-automation-prompt](hooks-automation-prompt.md) |
| **MCP** | Connect to an external system | DB, browser, issue tracker — [mcp-integration-prompt](mcp-integration-prompt.md) |
| **Subagent** | Isolated worker returning a summary | Research, review, parallel work — [multi-agent-orchestration-prompt](multi-agent-orchestration-prompt.md) |
| **Plugin** | Bundle skills + agents + hooks + MCP, versioned | Reuse across repos, share with a team — [claude-code-plugins-prompt](claude-code-plugins-prompt.md) |

Build the setup over time. Each need has a trigger:

| Trigger | Add |
|---|---|
| Claude gets a convention wrong twice | A line in CLAUDE.md |
| You keep typing the same prompt to start a task | A user-invocable skill |
| You paste the same multi-step procedure a third time | A skill |
| You keep copying data from a tab Claude can't see | An MCP server |
| A side task floods the conversation with output | Route it through a subagent |
| Something must happen every time with no exceptions | A hook |
| A second repo needs the same setup | A plugin |

---

## Phase 1: CLAUDE.md — persistent context

CLAUDE.md is read at the start of every session and stays in context. It costs tokens on every request, so it holds only what Claude cannot infer from the code.

### Locations, in load order (broad to specific)

| Scope | Location |
|---|---|
| Managed policy | macOS `/Library/Application Support/ClaudeCode/CLAUDE.md`; Linux/WSL `/etc/claude-code/CLAUDE.md`; Windows `C:\Program Files\ClaudeCode\CLAUDE.md` |
| User | `~/.claude/CLAUDE.md` |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` (commit it) |
| Local (gitignored) | `./CLAUDE.local.md` |

All discovered files are concatenated, not overridden. Nested CLAUDE.md in subdirectories load on demand when Claude reads files there.

### What to include

| Include | Exclude |
|---|---|
| Bash commands Claude can't guess | Anything Claude can read from the code |
| Code style that differs from defaults | Standard language conventions |
| Test runner and testing instructions | API docs (link instead) |
| Branch naming, PR conventions | Information that changes frequently |
| Architectural decisions specific to this project | File-by-file descriptions |
| Environment quirks (required env vars) | "Write clean code" |

Test every line: *"Would removing this cause Claude to make a mistake?"* If not, cut it. A bloated CLAUDE.md causes Claude to ignore the rules that matter.

### Template

```markdown
# CLAUDE.md

## Stack
- Next.js 16 (App Router), React 19, TypeScript
- Tailwind v4, shadcn/ui
- Prisma ORM, PostgreSQL

## Commands
- Dev: pnpm dev
- Test: pnpm test  (prefer a single test file over the whole suite)
- Lint: pnpm lint
- Typecheck: pnpm typecheck

## Conventions
- Server Components by default; 'use client' only when needed
- API handlers in app/api/; Prisma schema in prisma/schema.prisma
- Conventional Commits

## Gotchas
- The seed script requires a running local Redis
- Do not edit prisma/migrations/ by hand
```

- **Imports:** `@path/to/file` pulls another file in (recursive, 4 hops max). Backtick-wrap a path to keep it literal. Imported files load at launch — they organize, they don't save context.
- **`AGENTS.md` interop:** Claude Code reads `CLAUDE.md`, not `AGENTS.md` — but `AGENTS.md` is the cross-tool standard the major vendors converged on in 2026. If your repo has one, make `CLAUDE.md` a thin wrapper: `@AGENTS.md` on the first line, then Claude-specific lines below. A symlink works when you have nothing Claude-specific. `/init` (with `CLAUDE_CODE_NEW_INIT=1`) and `/import` also read `AGENTS.md`, Cursor rules, and Copilot instructions. See [../workflows/reference-resources.md](../workflows/reference-resources.md).
- **HTML comments** (`<!-- ... -->`) are stripped before injection — free space for maintainer notes.
- **Size:** the community consensus is **100–400 lines** — under 100 usually means missing context, over 400 means split per-package or move detail to rules. Treat it as a config file: commit it, review changes in PRs. `/doctor` proposes trims. Files over 4 MiB are skipped.
- **Include only rules that change the agent's decisions** — not style rules (the linter owns those), not pasted code, not one-off task instructions.
- `/init` generates a starter CLAUDE.md (suggests improvements if one exists). `/memory` opens the files for editing.

### `.claude/rules/`

Split large instruction sets into topic files under `.claude/rules/`. Rules without `paths:` load every session at the same priority as `.claude/CLAUDE.md`. Rules with `paths:` load only when Claude touches matching files:

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API rules
- Every endpoint validates input
- Errors use the standard envelope
- Include OpenAPI comments
```

This keeps CLAUDE.md short and scopes guidance to where it applies.

### Auto memory

On by default. Claude writes its own notes across sessions — your preferences (`user`), corrections you give (`feedback`), ongoing work (`project`), where to find external info (`reference`) — at `~/.claude/projects/<project>/memory/`. It skips anything derivable from the code or already in CLAUDE.md. `/memory` browses it; `autoMemoryEnabled: false` or `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` turns it off. Saying "remember that…" saves to auto memory; "add this to CLAUDE.md" targets the file.

---

## Phase 2: settings.json

Layers, highest precedence first: managed policy → `.claude/settings.local.json` (not committed) → `.claude/settings.json` (committed) → `~/.claude/settings.json`.

```json
{
  "model": "opus",
  "effortLevel": "high",
  "permissions": {
    "allow": ["Bash(pnpm test:*)", "Bash(pnpm lint)", "Bash(git commit *)", "Read(src/**)"],
    "deny": ["Read(**/.env)", "Edit(prisma/migrations/**)"],
    "ask": ["Bash(git push *)"]
  },
  "env": { "CLAUDE_CODE_SUBAGENT_MODEL": "haiku" },
  "hooks": {
    "PostToolUse": [
      { "matcher": "Write|Edit",
        "hooks": [ { "type": "command", "command": "pnpm exec prettier --write", "args": ["${tool_input.file_path}"], "async": true } ] }
    ]
  },
  "statusLine": { "type": "command", "command": ".claude/statusline.sh" },
  "outputStyle": "Concise",
  "enabledPlugins": ["acme-tools@acme"],
  "autoMemoryEnabled": true
}
```

- `"auto"` / `"bypassPermissions"` as a `defaultMode` are **ignored** in project/local settings — they must be in `~/.claude/settings.json` or managed settings.
- `/config key=value` sets any key from the prompt. `/hooks` browses configured hooks.

---

## Phase 3: Permissions

| Mode | Runs without asking | Use |
|---|---|---|
| Manual (`default`) | Reads only | Sensitive work, reviewing every action |
| `acceptEdits` | Reads + edits + common FS commands in the working dir | Iterating on code you review after |
| `plan` | Reads + classifier-approved commands | Exploring before changing |
| `auto` | Everything, with a background safety classifier | Long tasks; default on Pro/Max/Team |
| `bypassPermissions` | Everything | Isolated containers only |

`Shift+Tab` cycles the modes. Cut interruptions two ways: **allowlist** the specific safe commands (`/permissions` or the `allow` array), and **sandbox** (`/sandbox`) so isolated commands run without asking. Deny rules block in every mode. `/fewer-permission-prompts` proposes an allowlist from your transcripts.

Full detail: [claude-code-native-features-guide](../workflows/claude-code-native-features-guide.md).

---

## Phase 4: Extend — pick the mechanism

| Need | Mechanism | Why |
|---|---|---|
| A convention Claude keeps getting wrong | CLAUDE.md line (or a hook if it must be enforced) | Advisory context vs guaranteed enforcement |
| Guidance only for `*.tsx` files | `.claude/rules/` with `paths:` | Loads only when relevant |
| A deployment runbook | Skill (`disable-model-invocation: true`) | Loads on demand; you control timing |
| Your API style guide | Skill (reference) | Full text off the context budget until needed |
| Format after every edit | `PostToolUse` hook | Deterministic |
| Block edits to `migrations/` | `PreToolUse` hook | A CLAUDE.md rule is a request, not a guarantee |
| Query the production DB | MCP server (read-only DSN) | Purpose-built tools, auth handled |
| Research that reads 30 files | Subagent | Keeps the main context clean |
| The whole setup, reused in another repo | Plugin | One installable, versioned unit |

Layering when the same feature exists at multiple levels: CLAUDE.md files are additive; skills and subagents override by name (managed > user > project); MCP servers override local > project > user; hooks all fire.

---

## Troubleshooting

| Issue | Fix |
|---|---|
| Claude ignores a CLAUDE.md rule | File is too long — prune it; or the rule is ambiguous — make it concrete; or convert it to a hook |
| CLAUDE.md not loaded | `/context` → check **Memory files**; confirm it is in a loaded location |
| Instruction lost after `/compact` | It was conversation-only — add it to CLAUDE.md; project-root CLAUDE.md survives compaction |
| Hook not running | `/hooks` to check config; `claude --debug` for the hook debug log |
| MCP server not connecting | `claude mcp get <name>` for the error; see [mcp-integration-prompt](mcp-integration-prompt.md) |
| Too many approval prompts | Allowlist safe commands; enable sandboxing; consider auto mode |
| Config not taking effect | `/doctor`, or `claude --debug` |

---

## Remember

> **CLAUDE.md holds what Claude can't infer. Everything procedural moves to a skill; everything enforced moves to a hook.**

Configuration priorities:
1. Write a CLAUDE.md in the 100-400 line range; test every line against "would removing this cause a mistake?"
2. Scope topic guidance with `.claude/rules/` `paths:` so it loads only when relevant
3. Allowlist safe commands so approvals stop interrupting
4. A repeated mistake is a CLAUDE.md edit; a repeated procedure is a skill; an enforced rule is a hook
