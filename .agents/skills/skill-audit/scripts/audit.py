#!/usr/bin/env python3
"""Deterministic audit of a Claude Code skills directory: frontmatter validity,
description quality heuristics (SDO), body size, and name collisions across scopes.

Usage: audit.py [skills_dir ...]
  With no args, checks the conventional locations that exist:
    .claude/skills/, ~/.claude/skills/, and any --plugin-dir path is NOT auto-discovered
    (pass plugin skill dirs explicitly as extra args).
Exit code: 0 = no issues, 1 = issues found, 2 = usage error.
"""
import sys
import os
import re
import glob

FRONTMATTER_RE = re.compile(r'\A---\n(.*?)\n---\n', re.DOTALL)
WORKFLOW_WORDS = [
    'first', 'then', 'next', 'finally', 'step 1', 'step one',
    'dispatches', 'runs', 'writes then', 'reviews then',
]


def parse_frontmatter(text):
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if ':' in line and not line.strip().startswith('#'):
            key, _, val = line.partition(':')
            fm[key.strip()] = val.strip().strip('"\'')
    return fm


def find_skill_dirs(roots):
    found = []
    for root in roots:
        if not os.path.isdir(root):
            continue
        for entry in sorted(os.listdir(root)):
            skill_md = os.path.join(root, entry, 'SKILL.md')
            if os.path.isfile(skill_md):
                found.append(skill_md)
    return found


def check_description_quality(name, description):
    issues = []
    if not description:
        issues.append(f"{name}: missing 'description' field")
        return issues
    if len(description) > 1024:
        issues.append(f"{name}: description is {len(description)} chars, over the 1024-char spec limit")
    lower = description.lower()
    if not re.match(r'^use (when|for|this|before|after|during|as|to)\b', lower):
        issues.append(f"{name}: description doesn't open with a trigger phrase ('Use when...', 'Use before...', etc.) — SDO best practice leads with the trigger, not what the skill does")
    hits = [w for w in WORKFLOW_WORDS if w in lower]
    if hits:
        issues.append(f"{name}: description contains workflow-summary language ({', '.join(hits)}) — a description that summarizes process invites the model to act on the summary instead of reading the skill body")
    if description.strip().startswith('I ') or ' I ' in description[:20]:
        issues.append(f"{name}: description appears first-person; write in third person (it's injected into the system prompt)")
    return issues


def main():
    args = sys.argv[1:]
    if not args:
        home = os.path.expanduser('~')
        roots = [os.path.join('.claude', 'skills'), os.path.join(home, '.claude', 'skills')]
    else:
        roots = args

    skill_files = find_skill_dirs(roots)
    if not skill_files:
        print(f"No SKILL.md files found under: {', '.join(roots)}")
        return 0

    issues = []
    names_seen = {}
    total_words = {}

    for path in skill_files:
        with open(path, encoding='utf-8') as f:
            text = f.read()

        fm = parse_frontmatter(text)
        dirname = os.path.basename(os.path.dirname(path))

        if fm is None:
            issues.append(f"{path}: no valid YAML frontmatter (must start with '---' on line 1)")
            continue

        name = fm.get('name', dirname)
        if 'name' in fm and fm['name'] != dirname:
            issues.append(f"{path}: frontmatter name '{fm['name']}' differs from directory name '{dirname}' — the command comes from the directory name for personal/project skills, this is likely a copy-paste leftover")

        if not re.match(r'^[a-zA-Z0-9-]+$', name):
            issues.append(f"{path}: name '{name}' contains characters other than letters/numbers/hyphens")

        issues.extend(check_description_quality(path, fm.get('description', '')))

        body = text[FRONTMATTER_RE.match(text).end():] if FRONTMATTER_RE.match(text) else text
        word_count = len(body.split())
        total_words[path] = word_count
        if word_count > 2000:
            issues.append(f"{path}: body is ~{word_count} words (roughly {word_count // 4} tokens) — well over the ~500-line / ~2000-token guideline; move detail to a reference file loaded on demand")

        key = name.lower()
        names_seen.setdefault(key, []).append(path)

    for name, paths in names_seen.items():
        if len(paths) > 1:
            issues.append(f"name collision '{name}': defined in {len(paths)} places: {', '.join(paths)} — the one with higher scope precedence silently wins; the others never trigger")

    print(f"Scanned {len(skill_files)} skill(s) under: {', '.join(r for r in roots if os.path.isdir(r))}")
    print()

    if issues:
        print(f"FINDINGS ({len(issues)}):")
        for i in issues:
            print(f"  - {i}")
        return 1

    print("clean: frontmatter valid, descriptions follow SDO conventions, no name collisions, no oversized bodies")
    return 0


if __name__ == '__main__':
    sys.exit(main())
