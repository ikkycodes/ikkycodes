"""Render contrib-heatmap.svg — a GitHub-style contribution matrix (SMIL only).

Grid:   53 weeks × 7 days, rounded cells, palette #161b22 → #39d353
Stats:  TOTAL / CURRENT STREAK / LONGEST STREAK / MOST ACTIVE DAY — all real,
        loaded from data/contributions.json (produced by fetch_contributions.py).
Anim:   staggered diagonal reveal (opacity + tiny slide), plays once, freezes.
"""

from __future__ import annotations

import json
import sys
from datetime import date, timedelta

from config import (
    BORDER_COLOR, CYAN, GREEN, MUTED, PRIMARY_TEXT, SECONDARY_TEXT,
    DATA_FILE as data_file, save, svg_close, svg_open, text,
)

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
MONTHS = [
    "", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]

CELL = 11          # cell size (px)
GAP = 3            # gap between cells (px)
STRIDE = CELL + GAP
COLS = 53          # weeks
ROWS = 7           # days
LOOKBACK = 371     # ~ GitHub's one-year window

GRAPH_X = 48
GRAPH_Y = 114


def load_data() -> dict:
    if not data_file.exists():
        print("[heatmap] no data/contributions.json — run fetch_contributions.py first")
        sys.exit(1)
    payload = json.loads(data_file.read_text(encoding="utf-8"))
    if "error" in payload:
        print(f"[heatmap] skip: contribution fetch previously failed ({payload['error']})")
        sys.exit(0)
    return payload


def month_labels(start: date, end: date) -> str:
    out = ""
    seen: set[str] = set()
    for col in range(COLS):
        first = start + timedelta(days=col * 7)
        if first > end:
            break
        tag = MONTHS[first.month]
        if tag and tag not in seen:
            seen.add(tag)
            out += text(GRAPH_X + col * STRIDE, 106, tag, size=11, fill=SECONDARY_TEXT)
        # a month only starts once
        prev = first - timedelta(days=7)
        if prev >= start and prev.month == first.month:
            seen.discard(tag)
    return out


def build() -> None:
    payload = load_data()
    days: list[dict] = payload["days"]
    counts = {d["date"]: d["count"] for d in days}
    levels = {d["date"]: d["level"] for d in days}

    total = payload["total_contributions"]
    streak = payload["current_streak"]
    longest = payload["longest_streak"]
    best = payload["most_active_day"]

    end = date.fromisoformat(payload["last_day"])
    start = end - timedelta(days=LOOKBACK - 1)
    start -= timedelta(days=start.weekday() + 1)  # align to Sunday

    width = GRAPH_X + COLS * STRIDE + 24
    height = 286

    parts = [svg_open(height, width)]

    # ---- header ------------------------------------------------------------
    parts.append(text(GRAPH_X, 34, "CONTRIBUTION MATRIX", size=15, fill=PRIMARY_TEXT, weight="bold",
                      spacing="1"))
    # (clean header — no terminal prompt clutter)
    parts.append(text(GRAPH_X, 60, f"TOTAL  {total:,}", size=16, fill=GREEN, weight="bold"))
    parts.append(text(GRAPH_X + 240, 60, f"STREAK  {streak}d", size=14, fill=CYAN))
    parts.append(text(GRAPH_X, 82, f"LONGEST  {longest}d", size=13, fill=SECONDARY_TEXT))
    parts.append(text(GRAPH_X + 240, 82, f"BEST  {best['date']}  ·  {best['count']} commits",
                      size=13, fill=SECONDARY_TEXT))

    # ---- month labels + grid -----------------------------------------------
    parts.append(month_labels(start, end))

    diagonal: list[list[str]] = [[] for _ in range(ROWS + COLS - 1)]
    for col in range(COLS):
        for row in range(ROWS):
            day = start + timedelta(days=col * 7 + row)
            if day > end:
                continue
            ds = day.isoformat()
            level = levels.get(ds, 0) if ds in counts else 0
            level = max(0, min(4, level))
            fill = PALETTE[level]
            x = GRAPH_X + col * STRIDE
            y = GRAPH_Y + row * STRIDE
            diagonal[col + row].append(
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="{fill}"/>'
            )

    for d, rects in enumerate(diagonal):
        if not rects:
            continue
        delay = d * 0.016
        parts.append(
            '<g opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.45s" '
            f'begin="{delay:.3f}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 4" to="0 0" '
            f'dur="0.45s" begin="{delay:.3f}s" fill="freeze"/>'
            f'{"".join(rects)}</g>'
        )

    # ---- legend ------------------------------------------------------------
    leg_x = width - 260
    parts.append(text(leg_x, 254, "Less", size=11, fill=SECONDARY_TEXT, anchor="end"))
    for i, color in enumerate(PALETTE):
        x = leg_x + 44 + i * (CELL + GAP)
        parts.append(f'<rect x="{x}" y="245" width="{CELL}" height="{CELL}" rx="3" fill="{color}"/>')
    parts.append(text(leg_x + 44 + 5 * (CELL + GAP), 254, "More", size=11, fill=SECONDARY_TEXT))

    # ---- caption -----------------------------------------------------------
    parts.append(text(GRAPH_X, 274, "REAL DATA · github.com/users/ikkycodes/contributions · "
                                    "refreshed weekly via GitHub Actions",
                      size=10, fill=MUTED))

    parts.append(svg_close())
    save("contrib-heatmap.svg", "".join(parts))


if __name__ == "__main__":
    build()