"""Fetch REAL contribution data from GitHub for the profile heatmap.

Source : https://github.com/users/{USERNAME}/contributions
Parses the contribution SVG cells (dates / counts / levels) and writes a
processed, anonymized aggregate to  data/contributions.json.

Stats are ALWAYS computed from the fetched data — never hardcoded.
If the fetch fails, an error marker is written and the script exits non-zero
so the workflow stops before generating any fake numbers.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date, datetime, timedelta

import requests
from bs4 import BeautifulSoup

from config import DATA_FILE, USERNAME

URL = f"https://github.com/users/{USERNAME}/contributions"
HEADERS = {"User-Agent": "ikkycodes-profile-art/1.0 (github profile readme generator)"}


def parse_count(tip_text: str) -> int:
    """'4 contributions on ...' -> 4;  'No contributions on ...' / missing -> 0."""
    match = re.search(r"(\d+)\s+contributions?", tip_text or "")
    return int(match.group(1)) if match else 0


def fetch_cells() -> tuple[list[dict], int]:
    resp = requests.get(URL, timeout=25, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    cells: list[dict] = []
    seen: set[str] = set()
    for node in soup.select("td[data-date]"):
        date_attr = node.get("data-date")
        if not date_attr or date_attr in seen:
            continue
        seen.add(date_attr)
        tip = node.find_next_sibling("tool-tip")
        tip_text = tip.get_text() if tip else ""
        cells.append(
            {
                "date": date_attr,
                "count": parse_count(tip_text),
                "level": int(node.get("data-level") or 0),
            }
        )
    if not cells:
        raise ValueError("no contribution cells parsed from the response")

    # GitHub's own page-level total: "21 contributions in the last year"
    total = sum(c["count"] for c in cells)
    headline = re.search(r"(\d+)\s+contributions\s+in\s+the\s+last\s+year", resp.text)
    if headline:
        total = int(headline.group(1))
    return cells, total


def compute_stats(cells: list[dict]) -> dict:
    cells.sort(key=lambda c: c["date"])
    counts = {c["date"]: c["count"] for c in cells}
    dates = sorted(counts)

    total = sum(counts.values())
    last_day = date.fromisoformat(dates[-1])

    # current streak: consecutive days with >0 commits ending at the graph end
    current_streak = 0
    cursor = last_day
    while counts.get(cursor.isoformat(), 0) > 0:
        current_streak += 1
        cursor -= timedelta(days=1)

    # longest streak
    longest_streak, run = 0, 0
    for ds in dates:
        if counts[ds] > 0:
            run += 1
            longest_streak = max(longest_streak, run)
        else:
            run = 0

    # most active day
    best = max(cells, key=lambda c: c["count"])

    # monthly totals (non-zero months)
    monthly: dict[str, int] = {}
    for c in cells:
        if c["count"] == 0:
            continue
        month = c["date"][:7]
        monthly[month] = monthly.get(month, 0) + c["count"]
    monthly_totals = [{"month": m, "count": monthly[m]} for m in sorted(monthly)]

    return {
        "username": USERNAME,
        "source": URL,
        "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "total_contributions": total,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "most_active_day": {"date": best["date"], "count": best["count"]},
        "monthly_totals": monthly_totals,
        "first_day": dates[0],
        "last_day": last_day.isoformat(),
        "days": cells,
    }


def main() -> None:
    try:
        cells, total = fetch_cells()
        stats = compute_stats(cells)
        stats["total_contributions"] = total  # keep GitHub's own headline total
        DATA_FILE.write_text(json.dumps(stats, indent=2), encoding="utf-8")
        print(
            f"[fetch] {USERNAME}: total={total} "
            f"streak={stats['current_streak']} "
            f"longest={stats['longest_streak']} "
            f"best={stats['most_active_day']['date']} "
            f"({len(cells)} days) -> {DATA_FILE}"
        )
    except Exception as exc:  # noqa: BLE001 - any failure must abort cleanly
        marker = {
            "error": str(exc),
            "username": USERNAME,
            "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "note": "Contribution fetch failed. No fake numbers were generated.",
        }
        DATA_FILE.write_text(json.dumps(marker, indent=2), encoding="utf-8")
        print(f"[fetch] FAILED: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()