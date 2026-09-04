#!/usr/bin/env python3
"""Deterministic Markdown link checker: internal file links, heading anchors, and orphan pages.
External http(s) links are listed but not fetched by default (see --check-external).

Usage: check_links.py [root_dir] [--check-external] [--exclude PATTERN]
Exit code: 0 = no broken links, 1 = broken links found, 2 = usage error.
"""
import sys
import re
import os
import argparse
import urllib.request
import urllib.error

LINK_RE = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')
HEADING_RE = re.compile(r'^(#{1,6})\s+(.+?)\s*#*$', re.MULTILINE)
FENCED_BLOCK_RE = re.compile(r'^```[^\n]*\n.*?^```[ \t]*$', re.DOTALL | re.MULTILINE)
# Double-backtick spans (`` `code with a literal backtick` ``) allow single backticks
# INSIDE the span by design — that's the entire reason to use them — so the inner
# content must be matched non-greedily across any character, not excluding backtick.
# Must run before the single-backtick pattern, else the outer `` `` `` pair is missed
# and an inner single backtick gets mistaken for a span boundary.
INLINE_CODE_DOUBLE_RE = re.compile(r'``.+?``')
INLINE_CODE_RE = re.compile(r'`[^`\n]+`')


def strip_code(content: str) -> str:
    """Blank out fenced code blocks and inline code spans (preserving line count/offsets)
    so a [text](target) shown as a code EXAMPLE isn't checked as a real link."""
    def blank(m):
        return re.sub(r'[^\n]', ' ', m.group(0))
    content = FENCED_BLOCK_RE.sub(blank, content)
    content = INLINE_CODE_DOUBLE_RE.sub(blank, content)
    content = INLINE_CODE_RE.sub(blank, content)
    return content


def slugify(heading: str) -> str:
    # GitHub-style heading slug: lowercase, strip punctuation (not spaces/hyphens),
    # then map each whitespace run of length 1 to one hyphen WITHOUT collapsing —
    # "DECIDE — Is" (em-dash stripped, both surrounding spaces survive) must become
    # "decide--is" (double hyphen), matching GitHub's actual algorithm.
    s = heading.strip().lower()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'\s', '-', s)
    return s


def find_markdown_files(root, exclude_pattern=None):
    exclude_re = re.compile(exclude_pattern) if exclude_pattern else None
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ('.git', 'node_modules', 'dist', 'build', 'vendor')]
        for fn in filenames:
            if fn.endswith('.md'):
                path = os.path.join(dirpath, fn)
                # --exclude patterns are written with forward slashes; normalize before
                # matching so this works identically on Windows (os.path.join uses \).
                if exclude_re and exclude_re.search(path.replace(os.sep, '/')):
                    continue
                yield path


def extract_headings(content):
    return {slugify(h) for _, h in HEADING_RE.findall(content)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', nargs='?', default='.')
    parser.add_argument('--check-external', action='store_true',
                         help='Also HEAD-request http(s) links (slow, requires network; best-effort)')
    parser.add_argument('--exclude', default=None, help='regex of paths to skip')
    args = parser.parse_args()

    root = os.path.abspath(args.root)
    files = list(find_markdown_files(root, args.exclude))
    file_set = {os.path.relpath(f, root).replace('\\', '/') for f in files}

    headings_by_file = {}
    for f in files:
        with open(f, encoding='utf-8') as fh:
            headings_by_file[f] = extract_headings(fh.read())

    broken = []
    external = []
    referenced = set()

    for f in files:
        with open(f, encoding='utf-8') as fh:
            content = fh.read()
        rel_f = os.path.relpath(f, root).replace('\\', '/')
        for _text, target in LINK_RE.findall(strip_code(content)):
            target = target.strip()
            if target.startswith('http://') or target.startswith('https://'):
                external.append((rel_f, target))
                continue
            if target.startswith('mailto:') or target.startswith('#') and target == '#':
                continue

            anchor = None
            path_part = target
            if '#' in target:
                path_part, anchor = target.split('#', 1)

            if path_part == '':
                # Same-file anchor link
                target_file = f
            else:
                target_file = os.path.normpath(os.path.join(os.path.dirname(f), path_part))

            if path_part != '':
                if os.path.isdir(target_file):
                    continue  # a link to a directory (e.g. "examples/") is valid Markdown
                if not os.path.isfile(target_file):
                    broken.append((rel_f, target, 'file not found'))
                    continue
                rel_target = os.path.relpath(target_file, root).replace('\\', '/')
                referenced.add(rel_target)

            if anchor:
                target_headings = headings_by_file.get(target_file, headings_by_file.get(f, set()))
                if target_file not in headings_by_file:
                    # target file exists but wasn't a .md we indexed (shouldn't normally happen)
                    continue
                if slugify(anchor) not in headings_by_file[target_file]:
                    broken.append((rel_f, target, f'anchor #{anchor} not found in {os.path.relpath(target_file, root)}'))

    orphans = sorted(file_set - referenced - {os.path.relpath(f, root).replace('\\', '/')
                                               for f in files if os.path.basename(f).upper() in
                                               ('README.MD', 'INDEX.MD', 'CHANGELOG.MD', 'CONTRIBUTING.MD',
                                                'LICENSE.MD', 'CLAUDE.MD', 'QUICK-START.MD', 'USAGE.MD',
                                                'REPOSITORY-MAP.MD')})

    if broken:
        print(f"BROKEN LINKS ({len(broken)}):")
        for src, target, reason in broken:
            print(f"  {src} -> {target}  [{reason}]")
        print()

    if orphans:
        print(f"ORPHAN PAGES ({len(orphans)}, no other .md file links to them):")
        for o in orphans:
            print(f"  {o}")
        print()

    if args.check_external and external:
        print(f"EXTERNAL LINKS ({len(external)} found, checking...):")
        seen = set()
        for src, url in external:
            if url in seen:
                continue
            seen.add(url)
            try:
                req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'doc-link-audit/1.0'})
                urllib.request.urlopen(req, timeout=5)
            except urllib.error.HTTPError as e:
                if e.code >= 400:
                    broken.append((src, url, f'HTTP {e.code}'))
                    print(f"  BROKEN: {url}  [HTTP {e.code}]")
            except Exception as e:
                print(f"  UNVERIFIED: {url}  [{type(e).__name__}: {e}]")
        print()
    elif external:
        print(f"EXTERNAL LINKS ({len(external)} found, not checked - pass --check-external to verify)")
        print()

    if not broken and not orphans:
        print(f"clean: {len(files)} files, all internal links and anchors resolve, no orphan pages")
        return 0

    return 1


if __name__ == '__main__':
    sys.exit(main())
