#!/usr/bin/env python3
"""Deterministic structural audit for the prompt library."""

import argparse
import json
import re
import sys
from pathlib import Path


RETIRED_IDS = (
    "claude-3-",
    "claude-opus-4-1",
    "claude-sonnet-4-0",
    "gpt-4o",
)

VAGUE_PHRASES = (
    "consider the trade-offs",
    "ensure quality",
    "use best practices",
    "handle appropriately",
)


def findings_for(path: Path, repo_root: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    findings: list[str] = []

    if re.search(
        r"compatibility stub|archived prompt|use .*archive|^# Deprecated:",
        text,
        re.I | re.MULTILINE,
    ):
        return findings

    if "## Role" not in text:
        findings.append("missing ## Role")
    if not re.search(
        r"^## .*?(Protocol|Core Loop|Workflow|Process|Cycle)",
        text,
        re.MULTILINE,
    ):
        findings.append("missing protocol/## Phases section")
    if not re.search(
        r"^#{2,3} .*?(Phase|Phases|Protocol|Core Loop|Workflow|Process|Cycle|Loop|Steps)",
        text,
        re.MULTILINE,
    ):
        findings.append("missing ## Phase(s)")
    if "## Remember" not in text:
        findings.append("missing ## Remember")
    else:
        headings = re.findall(r"^## (.+)$", text, re.MULTILINE)
        if headings[-1] != "Remember":
            findings.append("## Remember is not the final ## heading")

    if "/agents/" in str(path).replace("\\", "/") and "/archive/" not in str(path):
        if "**Use this when:**" not in text:
            findings.append("agent prompt missing **Use this when:**")
        skip_match = re.search(r"\*\*Skip to:\*\*\s*(.+)", text)
        if not skip_match:
            findings.append("agent prompt missing **Skip to:**")
        elif len(re.findall(r"\[[^\]]+\]\([^)]+\)", skip_match.group(1))) < 3:
            findings.append("**Skip to:** should contain 3–5 real links")

    lower = text.lower()
    for phrase in VAGUE_PHRASES:
        if phrase in lower:
            findings.append(f"vague advice phrase: {phrase}")

    for line_number, line in enumerate(text.splitlines(), start=1):
        lower_line = line.lower()
        if "retired" in lower_line or "legacy" in lower_line:
            continue
        for model_id in RETIRED_IDS:
            if model_id in lower_line:
                findings.append(
                    f"line {line_number} presents retired model identifier: {model_id}"
                )

    if path.name not in {"claude-agent-system-prompt.md", "quick-reference-prompt.md"}:
        relative = path.relative_to(repo_root).as_posix()
        agent_index = (repo_root / "prompts/english/agents/INDEX.md").read_text(
            encoding="utf-8"
        )
        global_index = (repo_root / "prompts/english/INDEX.md").read_text(
            encoding="utf-8"
        )
        name = path.name
        if name not in agent_index and name not in global_index:
            findings.append(f"prompt is not named in either prompt index: {relative}")

    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="?", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    repo_root = target
    while not (repo_root / "prompts").exists() and repo_root != repo_root.parent:
        repo_root = repo_root.parent
    if not (repo_root / "prompts").exists():
        repo_root = target if target.is_dir() else target.parent

    if target.is_dir():
        candidates = []
        for relative_dir in (
            "agents",
            "project-types",
            "base",
        ):
            directory = target / relative_dir
            if directory.exists():
                candidates.extend(directory.rglob("*.md"))
        files = sorted(p for p in candidates if "/archive/" not in str(p))
    else:
        files = [target]
    results = {}
    for path in files:
        if path.name == "INDEX.md":
            continue
        local = findings_for(path, repo_root)
        if local:
            results[path.as_posix()] = local

    if args.json:
        print(json.dumps(results, indent=2))
    elif not results:
        print("clean: prompt structure, metadata, and catalog checks passed")
    else:
        for path, local in results.items():
            print(path)
            for finding in local:
                print(f"  - {finding}")

    return 1 if results else 0


if __name__ == "__main__":
    sys.exit(main())
