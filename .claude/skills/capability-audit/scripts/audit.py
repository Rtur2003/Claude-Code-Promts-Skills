#!/usr/bin/env python3
"""Read-only evidence collector for GitHub-hosted agent capabilities.

Usage:
  audit.py owner/repo [owner/repo ...]
  audit.py https://github.com/owner/repo --json

The script reads the repository's current default branch through the GitHub API.
It does not clone, install, execute repository code, or produce a trust verdict.
Exit codes: 0 = inspected, 1 = one or more candidates could not be inspected,
2 = invalid command usage.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field


API_ROOT = "https://api.github.com"
USER_AGENT = "claude-code-prompts-capability-audit/1.0"
MAX_TEXT_FILES = 80
TEXT_SUFFIXES = (
    ".md", ".json", ".yaml", ".yml", ".sh", ".py", ".js", ".mjs", ".cjs",
    ".ts", ".ps1", ".bat", ".cmd",
)
EXECUTABLE_PATTERNS = {
    "piped remote shell": re.compile(r"(?:curl|wget)[^\n|]{0,300}\|\s*(?:ba)?sh\b", re.I),
    "unversioned npx package": re.compile(r"\bnpx\s+(?:-y\s+)?(?![^\s]+@(?:\d|[a-f0-9]{7,40}\b))[^\s]+", re.I),
    "broad shell grant": re.compile(r"allowed-tools\s*:[^\n]*(?:\bBash\b|\bShell\b)(?!\([^\n)]*\))", re.I),
    "live-looking secret assignment": re.compile(
        r"(?:api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?(?!\$\{|<|your[-_ ]|example|test|dummy)[A-Za-z0-9_./+=-]{16,}",
        re.I,
    ),
}


@dataclass
class Finding:
    severity: str
    message: str
    evidence: str | None = None


@dataclass
class Report:
    repository: str
    url: str = ""
    default_branch: str = ""
    stars: int | None = None
    forks: int | None = None
    archived: bool | None = None
    pushed_at: str | None = None
    license: str | None = None
    open_issues: int | None = None
    files_scanned: int = 0
    surfaces: dict[str, list[str]] = field(default_factory=dict)
    findings: list[Finding] = field(default_factory=list)
    error: str | None = None


class GitHubClient:
    def __init__(self, token: str | None = None):
        self.headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": USER_AGENT,
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def json(self, path: str) -> object:
        request = urllib.request.Request(f"{API_ROOT}{path}", headers=self.headers)
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.load(response)

    def text_file(self, owner: str, repo: str, path: str, ref: str) -> str:
        encoded_path = "/".join(urllib.parse.quote(part, safe="") for part in path.split("/"))
        encoded_ref = urllib.parse.quote(ref, safe="")
        payload = self.json(f"/repos/{owner}/{repo}/contents/{encoded_path}?ref={encoded_ref}")
        if not isinstance(payload, dict):
            raise ValueError(f"unexpected content response for {path}")
        content = payload.get("content", "")
        if payload.get("encoding") != "base64" or not isinstance(content, str):
            raise ValueError(f"unsupported content encoding for {path}")
        return base64.b64decode(content).decode("utf-8", errors="replace")


def parse_repo(value: str) -> tuple[str, str]:
    value = value.strip()
    if value.startswith(("http://", "https://")):
        parsed = urllib.parse.urlparse(value)
        if parsed.netloc.lower() not in {"github.com", "www.github.com"}:
            raise ValueError("only github.com repository URLs are supported")
        parts = [part for part in parsed.path.split("/") if part]
    else:
        parts = [part for part in value.split("/") if part]
    if len(parts) < 2:
        raise ValueError("expected owner/repo or https://github.com/owner/repo")
    owner, repo = parts[0], parts[1]
    if repo.endswith(".git"):
        repo = repo[:-4]
    valid = re.compile(r"^[A-Za-z0-9_.-]+$")
    if not valid.fullmatch(owner) or not valid.fullmatch(repo):
        raise ValueError("repository owner/name contains unsupported characters")
    return owner, repo


def days_since(timestamp: str | None) -> int | None:
    if not timestamp:
        return None
    try:
        instant = dt.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return None
    return (dt.datetime.now(dt.timezone.utc) - instant).days


def classify_paths(paths: list[str]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {
        "plugin_manifests": [],
        "marketplaces": [],
        "skills": [],
        "mcp": [],
        "hooks": [],
        "executables": [],
        "tests": [],
        "ci": [],
        "security": [],
        "licenses": [],
    }
    for path in paths:
        lower = path.lower()
        name = lower.rsplit("/", 1)[-1]
        if lower.endswith(".claude-plugin/plugin.json"):
            groups["plugin_manifests"].append(path)
        if lower.endswith(".claude-plugin/marketplace.json"):
            groups["marketplaces"].append(path)
        if name == "skill.md":
            groups["skills"].append(path)
        if name == ".mcp.json" or "mcp" in name and name.endswith((".json", ".yaml", ".yml")):
            groups["mcp"].append(path)
        if "hook" in lower and name.endswith((".json", ".sh", ".py", ".js", ".ts", ".ps1")):
            groups["hooks"].append(path)
        if name.endswith((".sh", ".ps1", ".bat", ".cmd")) or "/bin/" in lower or "/scripts/" in lower:
            groups["executables"].append(path)
        if re.search(r"(^|/)(tests?|evals?)(/|$)", lower) or name.startswith("test_") or name.endswith((".test.js", ".test.ts", ".spec.js", ".spec.ts")):
            groups["tests"].append(path)
        if lower.startswith(".github/workflows/"):
            groups["ci"].append(path)
        if name in {"security.md", "security.txt"} or lower.startswith(".github/security"):
            groups["security"].append(path)
        if name.startswith(("license", "copying")):
            groups["licenses"].append(path)
    return {key: sorted(value) for key, value in groups.items() if value}


def inspect_candidate(client: GitHubClient, owner: str, repo: str) -> Report:
    full_name = f"{owner}/{repo}"
    report = Report(repository=full_name)
    try:
        meta = client.json(f"/repos/{owner}/{repo}")
        if not isinstance(meta, dict):
            raise ValueError("unexpected repository response")
        report.url = str(meta.get("html_url", ""))
        report.default_branch = str(meta.get("default_branch", ""))
        report.stars = meta.get("stargazers_count")
        report.forks = meta.get("forks_count")
        report.archived = meta.get("archived")
        report.pushed_at = meta.get("pushed_at")
        report.open_issues = meta.get("open_issues_count")
        license_data = meta.get("license") or {}
        report.license = license_data.get("spdx_id") if isinstance(license_data, dict) else None

        branch = urllib.parse.quote(report.default_branch, safe="")
        tree = client.json(f"/repos/{owner}/{repo}/git/trees/{branch}?recursive=1")
        if not isinstance(tree, dict):
            raise ValueError("unexpected tree response")
        entries = tree.get("tree", [])
        paths = [entry.get("path", "") for entry in entries if isinstance(entry, dict) and entry.get("type") == "blob"]
        paths = [path for path in paths if isinstance(path, str)]
        report.surfaces = classify_paths(paths)

        if report.archived:
            report.findings.append(Finding("high", "repository is archived"))
        age = days_since(report.pushed_at)
        if age is not None and age > 365:
            report.findings.append(Finding("medium", f"default repository activity is {age} days old"))
        if not report.license or report.license == "NOASSERTION":
            report.findings.append(Finding("high", "no machine-readable license was found"))
        if "security" not in report.surfaces:
            report.findings.append(Finding("info", "no SECURITY.md or repository security policy path was found"))
        if "tests" not in report.surfaces:
            report.findings.append(Finding("medium", "no test or eval path was detected"))
        if "ci" not in report.surfaces:
            report.findings.append(Finding("info", "no GitHub Actions workflow was detected"))

        priority_paths = []
        for key in ("plugin_manifests", "marketplaces", "skills", "mcp", "hooks", "executables"):
            priority_paths.extend(report.surfaces.get(key, []))
        seen = set()
        for path in priority_paths:
            if path in seen or len(seen) >= MAX_TEXT_FILES or not path.lower().endswith(TEXT_SUFFIXES):
                continue
            seen.add(path)
            try:
                content = client.text_file(owner, repo, path, report.default_branch)
            except (urllib.error.URLError, ValueError, json.JSONDecodeError) as exc:
                report.findings.append(Finding("info", "could not inspect a relevant text file", f"{path}: {exc}"))
                continue
            report.files_scanned += 1
            for label, pattern in EXECUTABLE_PATTERNS.items():
                if pattern.search(content):
                    severity = "high" if label in {"piped remote shell", "live-looking secret assignment"} else "medium"
                    report.findings.append(Finding(severity, label, path))

        if report.surfaces.get("mcp"):
            report.findings.append(Finding("info", "MCP configuration expands the runtime trust boundary", ", ".join(report.surfaces["mcp"][:5])))
        if report.surfaces.get("hooks"):
            report.findings.append(Finding("info", "hooks can run automatically on lifecycle events", ", ".join(report.surfaces["hooks"][:5])))
        if report.surfaces.get("executables"):
            report.findings.append(Finding("info", "repository includes executable or script surfaces", f"{len(report.surfaces['executables'])} path(s)"))
    except urllib.error.HTTPError as exc:
        report.error = f"GitHub API HTTP {exc.code}: {exc.reason}"
    except urllib.error.URLError as exc:
        report.error = f"network error: {exc.reason}"
    except (ValueError, json.JSONDecodeError) as exc:
        report.error = str(exc)
    return report


def print_markdown(reports: list[Report]) -> None:
    for report in reports:
        print(f"## {report.repository}")
        if report.error:
            print(f"\nERROR: {report.error}\n")
            continue
        age = days_since(report.pushed_at)
        activity = f"{report.pushed_at} ({age} days ago)" if age is not None else "unknown"
        print()
        print(f"- Repository: {report.url}")
        print(f"- Default branch inspected: `{report.default_branch}` (not an install pin)")
        print(f"- Activity: {activity}; archived={report.archived}")
        print(f"- License: {report.license or 'unknown'}")
        print(f"- Adoption signal: {report.stars} stars, {report.forks} forks (not scored as quality)")
        print(f"- Open issues: {report.open_issues}")
        print(f"- Relevant text files scanned: {report.files_scanned}")
        print("- Surfaces:")
        if report.surfaces:
            for name, paths in report.surfaces.items():
                preview = ", ".join(f"`{path}`" for path in paths[:6])
                suffix = f" (+{len(paths) - 6} more)" if len(paths) > 6 else ""
                print(f"  - {name}: {preview}{suffix}")
        else:
            print("  - none detected")
        print("- Findings:")
        if report.findings:
            for finding in report.findings:
                evidence = f" — {finding.evidence}" if finding.evidence else ""
                print(f"  - [{finding.severity.upper()}] {finding.message}{evidence}")
        else:
            print("  - No configured heuristic fired; this is not a safety verdict.")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repositories", nargs="+", help="owner/repo or a github.com repository URL")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of Markdown")
    parser.add_argument(
        "--token-env",
        metavar="NAME",
        help="read a GitHub token from this environment variable; never pass token values as arguments",
    )
    args = parser.parse_args()

    token = None
    if args.token_env:
        token = os.environ.get(args.token_env)
        if not token:
            print(f"error: environment variable {args.token_env!r} is not set", file=sys.stderr)
            return 2

    parsed = []
    for value in args.repositories:
        try:
            parsed.append(parse_repo(value))
        except ValueError as exc:
            print(f"error: {value}: {exc}", file=sys.stderr)
            return 2

    client = GitHubClient(token)
    reports = [inspect_candidate(client, owner, repo) for owner, repo in parsed]
    if args.json:
        print(json.dumps([asdict(report) for report in reports], indent=2, ensure_ascii=False))
    else:
        print_markdown(reports)
    return 1 if any(report.error for report in reports) else 0


if __name__ == "__main__":
    sys.exit(main())
