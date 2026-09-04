#!/usr/bin/env bash
# PreToolUse hook (matcher: Write|Edit). Denies writing content that looks like a live credential.
# Reads the Claude Code hook JSON on stdin; emits a PreToolUse decision on stdout.
set -euo pipefail

payload="$(cat)"
content="$(printf '%s' "$payload" | jq -r '.tool_input.content // .tool_input.new_string // empty')"

if [ -z "$content" ]; then
  exit 0
fi

# Known credential shapes: AWS keys, GitHub tokens, PEM private keys, generic sk- style API keys.
if printf '%s' "$content" | grep -Eq \
  'AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{36,}|-----BEGIN[[:space:]][A-Z ]*PRIVATE KEY-----|\bsk-[A-Za-z0-9]{20,}\b'; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "This write contains what looks like a live credential (AWS key, GitHub token, private key, or API key). Use an environment variable or secret manager reference instead, or confirm with the user that this value is a placeholder."
    }
  }'
  exit 0
fi

exit 0
