#!/usr/bin/env python3
"""
Detect Markdown lines that often break GitHub rendering for $$ math blocks.

Checks include:
- text wrapped around $$...$$ on a single line (e.g., "Variables: $$ x $$")
- open/close $$ delimiters sharing a line with extra text
- odd number of $$ delimiters on a line
- unmatched multi-line $$ block delimiters
- $$ usage inside list/blockquote context (often fragile on GitHub)

Usage:
  python3 scripts/detect_dollar_math_violations.py path/to/file.md
  python3 scripts/detect_dollar_math_violations.py file1.md file2.md
  python3 scripts/detect_dollar_math_violations.py --glob "**/*.md"
"""

from __future__ import annotations

import argparse
import glob
import re
import sys
from dataclasses import dataclass
from pathlib import Path

SAME_LINE_BLOCK_RE = re.compile(r"\$\$([^\n]*?)\$\$")
LIST_OR_QUOTE_RE = re.compile(r"^\s{0,3}(?:[-+*]|\d+\.)\s+|^\s*>")
FENCE_RE = re.compile(r"^\s*(```|~~~)")


@dataclass
class Issue:
    file: Path
    line: int
    code: str
    message: str
    text: str


def find_issues(path: Path) -> list[Issue]:
    issues: list[Issue] = []
    lines = path.read_text(encoding="utf-8").splitlines()

    in_fence = False
    in_block_math = False
    open_block_line = 0

    for i, line in enumerate(lines, start=1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        if "$$" not in line:
            continue

        stripped = line.strip()
        delimiter_count = line.count("$$")

        # 1) Odd number of delimiters on line is fragile by itself.
        if delimiter_count % 2 == 1 and stripped != "$$":
            issues.append(
                Issue(
                    file=path,
                    line=i,
                    code="ODD_DELIMS_LINE",
                    message="Odd number of $$ delimiters on one line.",
                    text=line,
                )
            )

        # 2) Same-line $$...$$ blocks.
        for match in SAME_LINE_BLOCK_RE.finditer(line):
            left = line[: match.start()].strip()
            right = line[match.end() :].strip()
            inner = match.group(1).strip()

            # Text around $$...$$ usually should be inline $...$ instead.
            if left or right:
                issues.append(
                    Issue(
                        file=path,
                        line=i,
                        code="INLINE_BLOCK_WITH_TEXT",
                        message=(
                            "Text appears outside $$...$$ on the same line. "
                            "Use inline $...$ or move $$ block to its own lines."
                        ),
                        text=line,
                    )
                )

            # In list/quote contexts, inline is usually safer.
            if LIST_OR_QUOTE_RE.match(line):
                issues.append(
                    Issue(
                        file=path,
                        line=i,
                        code="LIST_CONTEXT_DOLLAR_BLOCK",
                        message=(
                            "$$...$$ used in list/quote context on one line. "
                            "Prefer inline $...$ or a non-indented block."
                        ),
                        text=line,
                    )
                )

            if not inner:
                issues.append(
                    Issue(
                        file=path,
                        line=i,
                        code="EMPTY_BLOCK",
                        message="Empty $$...$$ math block.",
                        text=line,
                    )
                )

        # 3) Delimiter-only block tracking for unmatched multi-line $$ blocks.
        # Only toggle state for pure delimiter lines, so this tracks true block usage.
        if stripped == "$$":
            if not in_block_math:
                in_block_math = True
                open_block_line = i
            else:
                in_block_math = False
                open_block_line = 0

        # 4) Lines that start/end with $$ but share extra text.
        starts = stripped.startswith("$$")
        ends = stripped.endswith("$$")
        only_delim_line = stripped == "$$"
        same_line_block = bool(SAME_LINE_BLOCK_RE.fullmatch(stripped))
        if not only_delim_line and not same_line_block:
            if starts and stripped != "$$":
                issues.append(
                    Issue(
                        file=path,
                        line=i,
                        code="OPEN_DELIM_WITH_TEXT",
                        message="Opening $$ shares a line with text/math content.",
                        text=line,
                    )
                )
            if ends and stripped != "$$":
                issues.append(
                    Issue(
                        file=path,
                        line=i,
                        code="CLOSE_DELIM_WITH_TEXT",
                        message="Closing $$ shares a line with text/math content.",
                        text=line,
                    )
                )

    if in_block_math:
        issues.append(
            Issue(
                file=path,
                line=open_block_line,
                code="UNMATCHED_BLOCK",
                message="Unmatched opening $$ block delimiter.",
                text=lines[open_block_line - 1] if 0 < open_block_line <= len(lines) else "$$",
            )
        )

    return issues


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detect likely $$ rendering violations in Markdown.")
    parser.add_argument("paths", nargs="*", help="Markdown files to inspect.")
    parser.add_argument(
        "--glob",
        dest="glob_pattern",
        help='Glob pattern (example: "**/*.md").',
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    candidates: list[Path] = []

    if args.glob_pattern:
        for p in glob.glob(args.glob_pattern, recursive=True):
            path = Path(p)
            if path.is_file():
                candidates.append(path)

    for p in args.paths:
        path = Path(p)
        if path.is_file():
            candidates.append(path)
        else:
            print(f"[skip] not a file: {path}")

    # De-duplicate while preserving order.
    seen: set[Path] = set()
    files: list[Path] = []
    for p in candidates:
        rp = p.resolve()
        if rp in seen:
            continue
        seen.add(rp)
        files.append(p)

    if not files:
        print("No input files. Pass files or --glob.")
        return 2

    total_issues = 0
    for file_path in files:
        issues = find_issues(file_path)
        if not issues:
            print(f"[ok] {file_path}")
            continue
        print(f"[issues] {file_path} ({len(issues)})")
        for issue in issues:
            print(f"  L{issue.line:>4}  {issue.code:<24} {issue.message}")
            print(f"        {issue.text.strip()}")
        total_issues += len(issues)

    print(f"\nTotal issues: {total_issues}")
    return 1 if total_issues else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
