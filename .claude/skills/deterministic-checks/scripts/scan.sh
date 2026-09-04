#!/usr/bin/env bash
# Language-agnostic, zero-model-cost repo scan. No dependencies beyond grep/find (git optional).
# Exit code: 0 = clean, 1 = findings reported (stdout), 2 = usage error.
set -euo pipefail

ROOT="${1:-.}"
cd "$ROOT"

FOUND=0
report() { printf '%s\n' "$1"; FOUND=1; }

# Respect .gitignore when git is available; otherwise scan everything under ROOT.
# Excludes this script's own directory (its source contains the patterns it looks for)
# and any path matching *.example.* / *fixtures* / *test-data* — extend via SCAN_EXCLUDE
# (a grep -Ev pattern) for docs directories with intentional example markers.
list_files() {
  if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    git ls-files --cached --others --exclude-standard
  else
    find . -type f \
      -not -path '*/node_modules/*' -not -path '*/.git/*' \
      -not -path '*/dist/*' -not -path '*/build/*' -not -path '*/vendor/*'
  fi | grep -Ev '(^|/)\.claude/skills/deterministic-checks/scripts/'
}

FILES="$(list_files)"
if [ -n "${SCAN_EXCLUDE:-}" ]; then
  FILES="$(printf '%s\n' "$FILES" | grep -Ev "$SCAN_EXCLUDE" || true)"
fi

# 1. Unresolved merge conflict markers
CONFLICTS="$(printf '%s\n' "$FILES" | xargs -r grep -lE '^(<<<<<<<|=======|>>>>>>>)( |$)' 2>/dev/null || true)"
if [ -n "$CONFLICTS" ]; then
  report "CONFLICT MARKERS:"
  printf '%s\n' "$CONFLICTS" | sed 's/^/  /'
fi

# 2. Live-looking credentials (same patterns as hooks/scripts/block-secret-writes.sh)
SECRETS="$(printf '%s\n' "$FILES" | xargs -r grep -lE \
  'AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{36,}|-----BEGIN[[:space:]][A-Z ]*PRIVATE KEY-----|\bsk-[A-Za-z0-9]{20,}\b' \
  2>/dev/null || true)"
if [ -n "$SECRETS" ]; then
  report "POSSIBLE CREDENTIALS:"
  printf '%s\n' "$SECRETS" | sed 's/^/  /'
fi

# 3. Debug leftovers commonly forgotten before commit
DEBUG="$(printf '%s\n' "$FILES" | grep -E '\.(js|jsx|ts|tsx|py|go|rb)$' | xargs -r grep -lnE \
  '\bconsole\.(log|debug)\(|^\s*print\((\"|'"'"')DEBUG|\bdebugger;|\bpdb\.set_trace\(\)|\bbinding\.pry\b' \
  2>/dev/null || true)"
if [ -n "$DEBUG" ]; then
  report "DEBUG LEFTOVERS:"
  printf '%s\n' "$DEBUG" | sed 's/^/  /'
fi

# 4. Untracked TODO/FIXME with no ticket reference (heuristic: no #NNN or [A-Z]+-[0-9]+ nearby)
UNTRACKED_TODOS="$(printf '%s\n' "$FILES" | xargs -r grep -nE '(TODO|FIXME|XXX)(:|\s)' 2>/dev/null \
  | grep -vE '(TODO|FIXME|XXX)[^\n]*(#[0-9]+|[A-Z]{2,}-[0-9]+)' || true)"
if [ -n "$UNTRACKED_TODOS" ]; then
  report "UNTRACKED TODO/FIXME (no ticket ref):"
  printf '%s\n' "$UNTRACKED_TODOS" | sed 's/^/  /' | head -30
fi

# 5. Large files that likely don't belong in git (>5MB, excluding common binary/lockfile allowlist)
LARGE="$(printf '%s\n' "$FILES" | while IFS= read -r f; do
  [ -f "$f" ] || continue
  case "$f" in *.lock|*package-lock.json|*.min.js) continue ;; esac
  size=$(wc -c < "$f" 2>/dev/null || echo 0)
  if [ "$size" -gt 5242880 ]; then
    printf '%s (%s bytes)\n' "$f" "$size"
  fi
done)"
if [ -n "$LARGE" ]; then
  report "LARGE FILES (>5MB):"
  printf '%s\n' "$LARGE" | sed 's/^/  /'
fi

if [ "$FOUND" -eq 0 ]; then
  echo "clean: no conflict markers, credentials, debug leftovers, untracked TODOs, or oversized files found"
  exit 0
fi

exit 1
