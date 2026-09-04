#!/usr/bin/env bash
# Deterministic changelog generation from Conventional Commits. Requires git.
# Usage: generate.sh [from-ref] [to-ref]
#   from-ref defaults to the most recent tag (or the repo root commit if no tags exist)
#   to-ref defaults to HEAD
set -euo pipefail

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "error: not a git repository" >&2
  exit 2
fi

FROM="${1:-}"
TO="${2:-HEAD}"

if [ -z "$FROM" ]; then
  FROM="$(git describe --tags --abbrev=0 2>/dev/null || git rev-list --max-parents=0 HEAD | tail -1)"
fi

RANGE="${FROM}..${TO}"

# Tab-separated: hash, subject. Body is fetched separately per-commit for breaking-change detection.
COMMITS="$(git log "$RANGE" --no-merges --pretty=format:'%H%x09%s' 2>/dev/null || true)"

if [ -z "$COMMITS" ]; then
  echo "No commits in range $RANGE" >&2
  exit 0
fi

declare -A SECTIONS
SECTIONS[feat]="### Features"
SECTIONS[fix]="### Fixes"
SECTIONS[perf]="### Performance"
SECTIONS[refactor]="### Refactoring"
SECTIONS[docs]="### Documentation"
SECTIONS[test]="### Tests"
SECTIONS[build]="### Build"
SECTIONS[ci]="### CI"
SECTIONS[chore]="### Chore"
SECTIONS[other]="### Other"

TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

BREAKING_FILE="$TMPDIR/breaking.txt"
: > "$BREAKING_FILE"

while IFS=$'\t' read -r hash subject; do
  [ -z "$hash" ] && continue

  body="$(git log -1 --pretty=format:'%b' "$hash" 2>/dev/null || true)"

  # Conventional Commits: type(scope)!: subject  — the ! marks a breaking change,
  # as does a "BREAKING CHANGE:" footer in the body.
  if printf '%s' "$subject" | grep -Eq '^[a-z]+(\([^)]+\))?!:' || printf '%s' "$body" | grep -q '^BREAKING CHANGE:'; then
    printf '- %s (%s)\n' "$subject" "${hash:0:7}" >> "$BREAKING_FILE"
  fi

  type="$(printf '%s' "$subject" | sed -nE 's/^([a-z]+)(\([^)]+\))?!?:.*/\1/p')"
  scope="$(printf '%s' "$subject" | sed -nE 's/^[a-z]+\(([^)]+)\)!?:.*/\1/p')"
  desc="$(printf '%s' "$subject" | sed -E 's/^[a-z]+(\([^)]+\))?!?:[[:space:]]*//')"

  if [ -z "$type" ] || [ -z "${SECTIONS[$type]:-}" ]; then
    type="other"
    desc="$subject"
  fi

  if [ -n "$scope" ]; then
    printf '%s\t- **%s:** %s (%s)\n' "$type" "$scope" "$desc" "${hash:0:7}" >> "$TMPDIR/entries.tsv"
  else
    printf '%s\t- %s (%s)\n' "$type" "$desc" "${hash:0:7}" >> "$TMPDIR/entries.tsv"
  fi
done <<< "$COMMITS"

if [ -s "$BREAKING_FILE" ]; then
  echo "## BREAKING CHANGES"
  echo
  cat "$BREAKING_FILE"
  echo
fi

for type in feat fix perf refactor docs test build ci chore other; do
  if [ -f "$TMPDIR/entries.tsv" ] && grep -q "^${type}	" "$TMPDIR/entries.tsv"; then
    echo "${SECTIONS[$type]}"
    echo
    grep "^${type}	" "$TMPDIR/entries.tsv" | cut -f2-
    echo
  fi
done
