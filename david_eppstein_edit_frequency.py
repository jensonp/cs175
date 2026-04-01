#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import requests


API_URL = "https://en.wikipedia.org/w/api.php"
USER = "David Eppstein"
USER_AGENT = "CodexEditFrequencyGraph/1.0 (https://openai.com)"
OUT_DIR = Path(__file__).resolve().parent
CSV_PATH = OUT_DIR / "david_eppstein_edit_frequency_monthly.csv"
PNG_PATH = OUT_DIR / "david_eppstein_edit_frequency_monthly.png"


def fetch_monthly_counts(username: str) -> Counter[datetime]:
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    params = {
        "action": "query",
        "list": "usercontribs",
        "ucuser": username,
        "uclimit": "max",
        "ucprop": "timestamp",
        "ucdir": "newer",
        "format": "json",
        "formatversion": "2",
        "maxlag": "5",
    }

    counts: Counter[datetime] = Counter()
    fetched = 0
    request_count = 0

    while True:
        response = session.get(API_URL, params=params, timeout=30)
        response.raise_for_status()
        payload = response.json()

        if "error" in payload:
            raise RuntimeError(f"MediaWiki API error: {payload['error']}")

        contribs = payload.get("query", {}).get("usercontribs", [])
        for contrib in contribs:
            ts = datetime.strptime(contrib["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
            month_bucket = datetime(ts.year, ts.month, 1)
            counts[month_bucket] += 1

        fetched += len(contribs)
        request_count += 1
        print(
            f"\rFetched {fetched:,} contributions in {request_count} requests...",
            end="",
            file=sys.stderr,
            flush=True,
        )

        if "continue" not in payload:
            break

        for key, value in payload["continue"].items():
            params[key] = value
        time.sleep(0.05)

    print(file=sys.stderr)
    return counts


def write_csv(counts: Counter[datetime], output_path: Path) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["month", "edit_count"])
        for month in sorted(counts):
            writer.writerow([month.strftime("%Y-%m-%d"), counts[month]])


def render_plot(counts: Counter[datetime], output_path: Path) -> None:
    months = sorted(counts)
    values = [counts[month] for month in months]

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(months, values, color="#184e77", linewidth=1.8)
    ax.fill_between(months, values, color="#1d7874", alpha=0.2)

    ax.set_title("David Eppstein English Wikipedia Edit Frequency by Month")
    ax.set_xlabel("Date")
    ax.set_ylabel("Edits per Month")

    ax.xaxis.set_major_locator(mdates.YearLocator(base=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    fig.autofmt_xdate()

    peak_month = max(months, key=counts.get)
    peak_value = counts[peak_month]
    ax.annotate(
        f"Peak: {peak_value} edits\n{peak_month.strftime('%b %Y')}",
        xy=(peak_month, peak_value),
        xytext=(20, 20),
        textcoords="offset points",
        arrowprops={"arrowstyle": "->", "color": "#555555"},
        fontsize=10,
    )

    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)


def main() -> int:
    counts = fetch_monthly_counts(USER)
    write_csv(counts, CSV_PATH)
    render_plot(counts, PNG_PATH)

    total = sum(counts.values())
    first_month = min(counts)
    last_month = max(counts)
    peak_month = max(counts, key=counts.get)

    print(f"CSV written to: {CSV_PATH}")
    print(f"PNG written to: {PNG_PATH}")
    print(f"Total edits processed: {total:,}")
    print(f"First month: {first_month:%Y-%m}")
    print(f"Latest month: {last_month:%Y-%m}")
    print(f"Peak month: {peak_month:%Y-%m} ({counts[peak_month]:,} edits)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
