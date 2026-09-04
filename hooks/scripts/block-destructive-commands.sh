#!/usr/bin/env bash
# PreToolUse hook (matcher: Bash). Denies commands that are hard to reverse.
# Reads the Claude Code hook JSON on stdin; emits a PreToolUse decision on stdout.
set -euo pipefail

payload="$(cat)"
command="$(printf '%s' "$payload" | jq -r '.tool_input.command // empty')"

if [ -z "$command" ]; then
  exit 0
fi

deny() {
  jq -n --arg reason "$1" '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: $reason
    }
  }'
  exit 0
}

# Recursive/forced delete of a root-ish or home-ish path
if printf '%s' "$command" | grep -Eq '\brm\s+(-[a-zA-Z]*r[a-zA-Z]*f[a-zA-Z]*|-[a-zA-Z]*f[a-zA-Z]*r[a-zA-Z]*)\s+(/|~|\$HOME|\.\.?/?\s*$)'; then
  deny "rm -rf against a root-like or home-like path is blocked. Scope the path explicitly and re-run if intended."
fi

# History-rewriting / force-push git operations
if printf '%s' "$command" | grep -Eq '\bgit\s+push\s+(--force|(-f)\b)|\bgit\s+reset\s+--hard\b|\bgit\s+clean\s+-[a-zA-Z]*f'; then
  deny "This git command discards or overwrites history/work (force-push, reset --hard, or clean -f). Confirm with the user before running it manually."
fi

# Destructive database / infra commands
if printf '%s' "$command" | grep -Eiq '\bDROP\s+(DATABASE|TABLE)\b|\bterraform\s+destroy\b|\bkubectl\s+delete\s+(namespace|--all)\b'; then
  deny "This command permanently destroys data or infrastructure. Confirm with the user before running it manually."
fi

exit 0
