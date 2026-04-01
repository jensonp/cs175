from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path
from typing import Dict

from scheduler.docs import build_site
from scheduler.meta import make_meta_scheduler
from scheduler.policies import ConfidenceGatedEDFSPTPolicy, EDFPolicy, LeastSlackPolicy, SPTPolicy
from scheduler.simulator import compare_policies
from scheduler.workloads import make_bursty_workload

ROOT = Path(__file__).resolve().parents[2]


def _metrics_to_report_rows(results: Dict[str, Dict[str, float | int | str]]) -> str:
    rows = []
    for policy_name, metrics in results.items():
        rows.append(
            "<tr>"
            f"<th>{policy_name}</th>"
            f"<td>{metrics['missed_deadlines']}</td>"
            f"<td>{metrics['total_penalty']}</td>"
            f"<td>{metrics['average_lateness']:.2f}</td>"
            f"<td>{metrics['machine_utilization']:.2f}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def _write_report(results: Dict[str, Dict[str, float | int | str]], output_dir: Path) -> None:
    report = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Smoke experiment report</title>
    <style>
      body {{ font-family: sans-serif; margin: 32px; }}
      table {{ border-collapse: collapse; width: 100%; }}
      th, td {{ border: 1px solid #ccc; padding: 10px; text-align: left; }}
      th {{ background: #f2f2f2; }}
    </style>
  </head>
  <body>
    <h1>Smoke experiment report</h1>
    <table>
      <thead>
        <tr>
          <th>Policy</th>
          <th>Missed deadlines</th>
          <th>Total penalty</th>
          <th>Average lateness</th>
          <th>Utilization</th>
        </tr>
      </thead>
      <tbody>
        {_metrics_to_report_rows(results)}
      </tbody>
    </table>
  </body>
</html>
"""
    (output_dir / "report.html").write_text(report, encoding="utf-8")


def smoke(seed: int, num_jobs: int, num_machines: int, run_id: str) -> Path:
    workload = make_bursty_workload(num_jobs=num_jobs, seed=seed)
    experts = [EDFPolicy(), SPTPolicy(), LeastSlackPolicy(), ConfidenceGatedEDFSPTPolicy()]
    policies = [*experts, make_meta_scheduler(experts)]
    results = compare_policies(policies, workload, num_machines=num_machines)

    latest_dir = ROOT / "artifacts" / "site" / "latest"
    run_dir = ROOT / "artifacts" / "runs" / run_id
    latest_dir.mkdir(parents=True, exist_ok=True)
    run_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "run_id": run_id,
        "seed": seed,
        "num_jobs": num_jobs,
        "num_machines": num_machines,
        "workload": "bursty",
        "policies": results,
    }

    metrics_json = json.dumps(payload, indent=2) + "\n"
    (latest_dir / "metrics.json").write_text(metrics_json, encoding="utf-8")
    (run_dir / "metrics.json").write_text(metrics_json, encoding="utf-8")
    _write_report(results, latest_dir)
    _write_report(results, run_dir)

    build_site(ROOT / "site")
    return latest_dir


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="python -m scheduler.cli")
    subparsers = parser.add_subparsers(dest="command", required=True)

    smoke_parser = subparsers.add_parser("smoke", help="Run a small smoke experiment.")
    smoke_parser.add_argument("--seed", type=int, default=0)
    smoke_parser.add_argument("--num-jobs", type=int, default=18)
    smoke_parser.add_argument("--num-machines", type=int, default=2)
    smoke_parser.add_argument("--run-id", default="smoke-seed-0")

    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command == "smoke":
        smoke(
            seed=args.seed,
            num_jobs=args.num_jobs,
            num_machines=args.num_machines,
            run_id=args.run_id,
        )
        return 0
    raise ValueError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
