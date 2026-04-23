#!/usr/bin/env python3
"""
Fix Markdown math patterns that often fail on GitHub rendering.

Main fixes:
1) Embedded block math on one line, e.g.
     Variables: $$ X = \{A, B, C, D\}. $$
   becomes
     Variables: $X = \{A, B, C, D\}.$

2) Standalone one-line block math, e.g.
     $$ X = Y $$
   becomes
     $$
     X = Y
     $$

Usage:
  python3 scripts/fix_markdown_math.py file1.md file2.md
  python3 scripts/fix_markdown_math.py --write file1.md
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SAME_LINE_BLOCK = re.compile(r"\$\$([^\n]*?)\$\$")


def _has_text_outside_blocks(line: str) -> bool:
    outside = SAME_LINE_BLOCK.sub("", line)
    return bool(outside.strip())


def _fix_line(line: str) -> tuple[str, int]:
    """
    Returns (new_line, replacement_count_for_line).
    """
    if "$$" not in line:
        return line, 0
    if line.count("$$") % 2 != 0:
        # Leave unmatched delimiters untouched.
        return line, 0
    if not SAME_LINE_BLOCK.search(line):
        return line, 0

    replacements = 0

    # Case 1: Text exists outside $$...$$ on this line.
    # Convert same-line $$...$$ to inline $...$.
    if _has_text_outside_blocks(line):
        def _inline_sub(match: re.Match[str]) -> str:
            nonlocal replacements
            replacements += 1
            inner = match.group(1).strip()
            return f"${inner}$"

        return SAME_LINE_BLOCK.sub(_inline_sub, line), replacements

    # Case 2: Entire line is exactly one same-line block.
    stripped = line.strip()
    full = SAME_LINE_BLOCK.fullmatch(stripped)
    if full:
        inner = full.group(1).strip()
        indent = line[: len(line) - len(line.lstrip(" \t"))]
        replacements += 1
        return f"{indent}$$\n{indent}{inner}\n{indent}$$", replacements

    # Otherwise leave unchanged.
    return line, 0


def fix_text(text: str) -> tuple[str, int]:
    had_trailing_newline = text.endswith("\n")
    lines = text.splitlines()
    out_lines: list[str] = []
    total = 0

    for line in lines:
        fixed, count = _fix_line(line)
        out_lines.append(fixed)
        total += count

    out_text = "\n".join(out_lines)
    if had_trailing_newline:
        out_text += "\n"
    return out_text, total


def process_file(path: Path, write: bool) -> int:
    original = path.read_text(encoding="utf-8")
    fixed, replacements = fix_text(original)
    if replacements == 0:
        return 0
    if write:
        path.write_text(fixed, encoding="utf-8")
    return replacements


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Fix GitHub-unfriendly Markdown math patterns.")
    parser.add_argument("paths", nargs="+", help="Markdown files to process.")
    parser.add_argument("--write", action="store_true", help="Write changes in-place.")
    args = parser.parse_args(argv)

    total_replacements = 0
    changed_files = 0

    for raw_path in args.paths:
        path = Path(raw_path)
        if not path.exists():
            print(f"[skip] not found: {path}")
            continue
        if path.is_dir():
            print(f"[skip] directory: {path}")
            continue

        replacements = process_file(path, write=args.write)
        if replacements:
            changed_files += 1
            total_replacements += replacements
            action = "updated" if args.write else "would update"
            print(f"[{action}] {path} ({replacements} replacement(s))")
        else:
            print(f"[ok] {path} (no changes)")

    mode = "write" if args.write else "dry-run"
    print(
        f"Done ({mode}). Files changed: {changed_files}. "
        f"Total replacements: {total_replacements}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
