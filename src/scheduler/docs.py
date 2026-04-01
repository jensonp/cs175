from __future__ import annotations

import argparse
import json
import shutil
from collections.abc import Sequence
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS_DIR = ROOT / "docs"
ARTIFACT_SITE_DIR = ROOT / "artifacts" / "site" / "latest"


def _write_placeholder(target_dir: Path) -> None:
    target_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = target_dir / "metrics.json"
    report_path = target_dir / "report.html"

    if not metrics_path.exists():
        metrics_path.write_text(
            json.dumps(
                {
                    "status": "placeholder",
                    "message": "Run the smoke command to generate the latest metrics.",
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    if not report_path.exists():
        report_path.write_text(
            """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Pending experiment report</title>
  </head>
  <body>
    <h1>Pending experiment report</h1>
    <p>Run the smoke command to generate an HTML summary.</p>
  </body>
</html>
""",
            encoding="utf-8",
        )


def build_site(output: Path, strict: bool = False) -> None:
    if strict and not DOCS_DIR.exists():
        raise FileNotFoundError("docs/ directory is required")

    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(DOCS_DIR, output)

    generated_dir = output / "generated" / "latest"
    if ARTIFACT_SITE_DIR.exists():
        shutil.copytree(ARTIFACT_SITE_DIR, generated_dir, dirs_exist_ok=True)
    else:
        _write_placeholder(generated_dir)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="python -m scheduler.docs")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build", help="Build the static docs site.")
    build_parser.add_argument("--output", default="site")
    build_parser.add_argument("--strict", action="store_true")

    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command == "build":
        build_site(ROOT / args.output, strict=args.strict)
        return 0
    raise ValueError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
