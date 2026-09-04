#!/usr/bin/env python3
"""Eval runner for find-prompt routing accuracy.

Two tiers, run in order:
  1. STATIC (always runs, no API key needed): every case's expected_specialist file
     must actually exist under prompts/english/. Catches the routing table pointing
     at a renamed/deleted/typo'd file — the failure mode that actually happens when
     a prompt is renamed and the SKILL.md routing table isn't updated to match.
  2. LIVE (only if ANTHROPIC_API_KEY is set): sends each case's task to a real model
     with the find-prompt routing table as context and checks whether the model
     picks the expected file. This is the actual trigger-accuracy measurement;
     tier 1 alone cannot catch "routes to a file that exists but is the wrong one."

Usage: run_routing_eval.py [--live]
  --live forces the live tier even without checking for cases marked skip;
  without it, live tier still runs automatically if ANTHROPIC_API_KEY is set.
Exit code: 0 = all cases pass, 1 = failures, 2 = usage/setup error.
"""
import sys
import os
import json
import argparse

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PROMPTS_ROOT = os.path.join(REPO_ROOT, 'prompts', 'english')
CASES_FILE = os.path.join(os.path.dirname(__file__), 'cases', 'find-prompt-routing.jsonl')
ROUTING_TABLE_FILE = os.path.join(REPO_ROOT, '.claude', 'skills', 'find-prompt', 'SKILL.md')


def load_cases():
    cases = []
    with open(CASES_FILE, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                cases.append(json.loads(line))
    return cases


def static_check(cases):
    """Tier 1: does the expected file actually exist?"""
    failures = []
    for c in cases:
        path = os.path.join(PROMPTS_ROOT, c['expected_specialist'])
        if not os.path.isfile(path):
            failures.append(f"{c['id']}: expected_specialist '{c['expected_specialist']}' does not exist at {path}")
    return failures


def live_check(cases):
    """Tier 2: does a real model route each task to the expected file?"""
    try:
        import anthropic
    except ImportError:
        print("SKIP live tier: 'anthropic' package not installed (pip install anthropic)")
        return [], 0

    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("SKIP live tier: ANTHROPIC_API_KEY not set")
        return [], 0

    with open(ROUTING_TABLE_FILE, encoding='utf-8') as f:
        routing_table = f.read()

    client = anthropic.Anthropic(api_key=api_key)
    failures = []
    checked = 0

    for c in cases:
        prompt = (
            f"You are given a routing table (below) that maps tasks to prompt files. "
            f"Given the task, reply with ONLY the file path from the table that best matches — "
            f"no explanation, no other text.\n\n"
            f"ROUTING TABLE:\n{routing_table}\n\n"
            f"TASK: {c['task']}\n\n"
            f"FILE PATH:"
        )
        try:
            response = client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=100,
                messages=[{"role": "user", "content": prompt}],
            )
            answer = response.content[0].text.strip()
        except Exception as e:
            failures.append(f"{c['id']}: API call failed: {e}")
            continue

        checked += 1
        expected = c['expected_specialist']
        if expected not in answer:
            failures.append(f"{c['id']}: task '{c['task'][:60]}...' expected '{expected}', model said '{answer[:100]}'")

    return failures, checked


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--live', action='store_true', help='Force the live tier (still needs ANTHROPIC_API_KEY)')
    args = parser.parse_args()

    if not os.path.isfile(CASES_FILE):
        print(f"error: cases file not found: {CASES_FILE}", file=sys.stderr)
        return 2

    cases = load_cases()
    print(f"Loaded {len(cases)} routing test cases")
    print()

    print("=== Tier 1: static (routing table -> file exists) ===")
    static_failures = static_check(cases)
    if static_failures:
        print(f"FAIL ({len(static_failures)}):")
        for f in static_failures:
            print(f"  - {f}")
    else:
        print(f"PASS: all {len(cases)} expected_specialist paths exist")
    print()

    print("=== Tier 2: live (task -> model picks expected file) ===")
    live_failures, checked = live_check(cases)
    if checked:
        if live_failures:
            print(f"FAIL ({len(live_failures)}/{checked}):")
            for f in live_failures:
                print(f"  - {f}")
        else:
            print(f"PASS: model routed correctly on all {checked} cases")
    print()

    total_failures = len(static_failures) + len(live_failures)
    if total_failures:
        print(f"RESULT: {total_failures} failure(s)")
        return 1
    print("RESULT: all checks passed")
    return 0


if __name__ == '__main__':
    sys.exit(main())
