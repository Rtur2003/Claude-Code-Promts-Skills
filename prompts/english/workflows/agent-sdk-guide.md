# Agent SDK Guide

> **Claude Code as a Library** | **TypeScript & Python** | **query() Loop**

**Use this when:** building a production agent that plans its own steps and calls tools — in your own process, in Python or TypeScript — instead of driving Claude Code from a terminal.
**Skip to:** [Protocol](#protocol-build) · [Which tool](#which-tool) · [Install](#install) · [Minimal agent](#minimal-agent) · [Options](#options) · [Loading .claude config](#loading-claude-config) · [Permissions](#permissions) · [Deployment](#deployment) · [Remember](#remember)

## Role

You build agents on the Claude Agent SDK — the same agent loop, built-in tools, and context management that power Claude Code, as a library you call from `query()`. You scope tools tightly, pick a permission mode that matches how much oversight you want, and load `.claude/` config so the agent behaves like a Claude Code session.

## Protocol: BUILD

```
B → BOUNDARY  — Agent SDK, CLI subprocess, Client SDK, or Managed Agents?
U → USE query — One entry point: query(prompt, options) returns an async iterator
I → INSTRUCT  — systemPrompt, or the claude_code preset + .claude/ config
L → LIMIT     — allowedTools + permissionMode scope what runs without approval
D → DEPLOY    — Docker / cloud / CI; API key auth, never claude.ai login
```

---

## Which tool

| Building | Use |
|---|---|
| An agent without writing the tool loop yourself, in Python or TypeScript | **Agent SDK** |
| Interactive development, one-off terminal tasks | **Claude Code CLI** |
| An agent loop in another language | **CLI as a subprocess**: `claude -p --output-format json` |
| Direct Messages API calls, your own tool loop | **Client SDK** (`anthropic` / `@anthropic-ai/sdk`) |
| Long-running async agents without managing your own sandbox | **Managed Agents** (hosted REST API; Anthropic runs the loop and the sandbox) |

The SDK gives you Claude Code's built-in tools (Read/Write/Edit/Bash/Glob/Grep/WebSearch/WebFetch), agent loop, context management, hooks, subagents, MCP, permissions, sessions, and skills/commands/memory loaded from `.claude/` and `~/.claude/`.

The "Claude Code SDK" was renamed the **Claude Agent SDK**.

---

## Install

**TypeScript** (`@anthropic-ai/claude-agent-sdk`), Node 18+:

```bash
npm init -y
npm pkg set type=module
npm install @anthropic-ai/claude-agent-sdk
npm install --save-dev tsx
```

**Python** (`claude-agent-sdk`), Python 3.10+:

```bash
uv init && uv add claude-agent-sdk
# or: python3 -m venv .venv && source .venv/bin/activate && pip install claude-agent-sdk
```

Both SDKs bundle a native Claude Code binary — no separate install needed in most cases. (Exceptions: a pip source-dist install, or `npm ci --omit=optional`.)

**Auth** — set `ANTHROPIC_API_KEY` in the shell that runs the agent. The SDK does not load `.env` files; load them yourself. Third-party providers: `CLAUDE_CODE_USE_BEDROCK=1`, `CLAUDE_CODE_USE_VERTEX=1`, `CLAUDE_CODE_USE_FOUNDRY=1`, or `CLAUDE_CODE_USE_ANTHROPIC_AWS=1`. **claude.ai login is not permitted for third-party SDK products** — use API keys.

---

## Minimal agent

**Python:**

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage

async def main():
    async for message in query(
        prompt="Review utils.py for bugs that would cause crashes. Fix any you find.",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Glob"],
            permission_mode="acceptEdits",
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")

asyncio.run(main())
```

**TypeScript:**

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Review utils.py for bugs that would cause crashes. Fix any you find.",
  options: {
    allowedTools: ["Read", "Edit", "Glob"],
    permissionMode: "acceptEdits",
  },
})) {
  if (message.type === "assistant" && message.message?.content) {
    for (const block of message.message.content) {
      if ("text" in block) console.log(block.text);
    }
  } else if (message.type === "result") {
    console.log(`Done: ${message.subtype}`);
  }
}
```

Run: `npx tsx agent.ts` / `uv run agent.py`. The loop yields Claude's reasoning, tool calls, tool results, then the final outcome. The SDK handles orchestration, tool execution, context management, and retries.

For background jobs and CI, collect all messages instead of streaming — see the SDK's streaming-vs-single-turn docs.

---

## Options

| Option | Purpose |
|---|---|
| `allowedTools` / `allowed_tools` | Pre-approve these tools. Common sets: `["Read","Glob","Grep"]` read-only, `["Read","Edit","Glob"]` modify code, `["Read","Edit","Bash","Glob","Grep"]` full automation. |
| `permissionMode` / `permission_mode` | `default`, `acceptEdits`, `plan`, `bypassPermissions`. |
| `systemPrompt` / `system_prompt` | Custom system prompt, or `{ preset: "claude_code" }` to use Claude Code's. |
| `mcpServers` / `mcp_servers` | MCP server config (inline or from `.mcp.json`). |
| `add_dirs` / `additionalDirectories` | Extra directories; also loads their `.claude/skills/` and `.claude/commands/`. |
| `settingSources` / `setting_sources` | Which settings layers to load — include `project` to load `.claude/` skills, commands, subagents. |
| `model`, `effort` | Model and effort level. |
| `maxTurns` | Cap the agent loop. |
| `hooks` | Intercept tool calls, add context, block actions. |
| `canUseTool` (TS) | A callback that approves or denies each tool call. |

Add web search: `allowedTools: [...,"WebSearch"]`. Custom tools: define an in-process MCP server. Structured output: request validated JSON from the workflow.

---

## Loading .claude config

The SDK loads project instructions, skills, hooks, subagents, and memory from `.claude/` and `~/.claude/` the same way Claude Code does — **when the `project` setting source is enabled** (the default). If you pass `settingSources` / `setting_sources` explicitly, include `project`.

- **System prompt:** `{ preset: "claude_code" }` uses Claude Code's system prompt; a string replaces it entirely; `{ preset: "claude_code", append: "..." }` extends it.
- **Skills:** control which the agent can invoke with the skills option.
- **Subagents:** define inline or load from `.claude/agents/`.
- **Plugins:** load by local path.
- **Sessions:** persist conversation history; resume or fork later; mirror transcripts to S3/Redis/your backend.

---

## Permissions

The SDK evaluates the active `permissionMode` together with your allow/deny rules in a fixed order. For anything beyond a trusted sandbox, do not use `bypassPermissions` — scope `allowedTools` and use `default` or `acceptEdits`, or supply a `canUseTool` callback / `PermissionRequest` hook that approves each call against your own policy.

| Tools granted | Agent can |
|---|---|
| `Read`, `Glob`, `Grep` | Read-only analysis |
| `Read`, `Edit`, `Glob` | Analyze and modify code |
| `Read`, `Edit`, `Bash`, `Glob`, `Grep` | Full automation |

---

## Deployment

- **Hosting:** Docker, cloud, CI/CD. The SDK docs have a hosting guide and a secure-deployment guide.
- **Observability:** export traces, metrics, and events via OpenTelemetry; track cost and token usage per session.
- **Checkpointing:** track file changes and restore files to a previous state.
- **Tool search:** scale to thousands of tools with deferred loading.
- **Branding for partners:** "Claude Agent" or "Powered by Claude" is allowed; "Claude Code" / "Claude Code Agent" and Claude Code visual mimicry are not.

Example agents: `github.com/anthropics/claude-agent-sdk-demos` (email assistant, research agent, and more).

---

## Remember

> **The SDK is Claude Code's loop as a library. Scope the tools, pick the permission mode, and load `.claude/` config so the agent behaves like a real session.**

Before shipping:
1. `allowedTools` is the minimum set the task needs
2. `permissionMode` is not `bypassPermissions` outside an isolated sandbox
3. Auth is an API key, never claude.ai login
4. Cost tracking and OpenTelemetry are wired before production traffic
