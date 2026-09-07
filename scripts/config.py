"""Shared configuration and SVG helpers for the ikkycodes profile artwork.

Every generated SVG pulls its colors / fonts / helpers from here so the whole
profile stays visually consistent: a dark, GitHub-compatible terminal aesthetic.

Design system tokens (global):
    Background      #0d1117
    Terminal panel  #161b22   /  #21262d (alt)
    Border          #30363d
    Primary text    #f0f6fc
    Secondary text  #8b949e
    Green accent    #39d353   /  #2ea043 (dim)
    Cyan accent     #58d6ff
"""

from __future__ import annotations

import html
from pathlib import Path

# ---------------------------------------------------------------------------
# Repository layout
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
DATA_DIR = REPO_ROOT / "data"
DATA_FILE = DATA_DIR / "contributions.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)

USERNAME = "ikkycodes"
GITHUB_URL = f"https://github.com/{USERNAME}"

# ---------------------------------------------------------------------------
# Design system
# ---------------------------------------------------------------------------

BG_COLOR = "#0d1117"
PANEL_COLOR = "#161b22"
PANEL_ALT = "#21262d"
BORDER_COLOR = "#30363d"
PRIMARY_TEXT = "#f0f6fc"
SECONDARY_TEXT = "#8b949e"
GREEN = "#39d353"
GREEN_DIM = "#2ea043"
CYAN = "#58d6ff"
MUTED = "#484f58"

FONT_MONO = "'SFMono-Regular','Cascadia Code','Consolas','Menlo','JetBrains Mono',monospace"

WIDTH = 820

# ---------------------------------------------------------------------------
# Primitives
# ---------------------------------------------------------------------------


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def rect(x, y, w, h, fill="none", stroke="none", rx=0, sw=1, dash=None, opacity=1.0) -> str:
    out = (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
        f'rx="{rx:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"'
    )
    if dash is not None:
        out += f' stroke-dasharray="{dash}"'
    if opacity != 1.0:
        out += f' opacity="{opacity:.2f}"'
    return out + "/>"


def text(x, y, content, size=14, fill=PRIMARY_TEXT, anchor="start", weight="normal",
         opacity=1.0, spacing=None) -> str:
    out = (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT_MONO}" font-size="{size}" '
        f'fill="{fill}" text-anchor="{anchor}" font-weight="{weight}"'
    )
    if spacing is not None:
        out += f' letter-spacing="{spacing}"'
    if opacity != 1.0:
        out += f' opacity="{opacity:.2f}"'
    return out + f">{esc(content)}</text>"


def fade(content: str, begin: float, dur: float = 0.35) -> str:
    """Fade a fragment in once, then freeze (SMIL, no loop)."""
    return (
        '<g opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" dur="{dur}s" '
        f'begin="{begin}s" fill="freeze"/>'
        f"{content}</g>"
    )


def panel(x, y, w, h, rx=12, fill=PANEL_COLOR, stroke=BORDER_COLOR) -> str:
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="{rx:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>')


def svg_open(height: int, width: int = WIDTH) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="{FONT_MONO}">'
        f'<rect width="{width}" height="{height}" fill="{BG_COLOR}"/>'
    )


def svg_close() -> str:
    return "</svg>"


def save(name: str, svg: str) -> Path:
    target = REPO_ROOT / name
    target.write_text(svg, encoding="utf-8")
    print(f"[save] {target.relative_to(REPO_ROOT)} ({len(svg)} bytes)")
    return target


# ---------------------------------------------------------------------------
# Typewriter reveal (SVG-native, clip-based — no JS)
# ---------------------------------------------------------------------------

_seq = {"n": 0}


def typed_text(x, y, content, begin, dur, size=15, fill=PRIMARY_TEXT, cursor=GREEN) -> str:
    """Reveal ``content`` left → right like a terminal type-in, then drop the cursor."""
    _seq["n"] += 1
    cid = f"clip-{_seq['n']}"
    width = len(content) * 0.6 * size  # monospace advance ≈ 0.6em
    clip = (
        f'<clipPath id="{cid}">'
        f'<rect x="{x:.1f}" y="{y - size:.1f}" width="0" height="{size * 1.8:.1f}">'
        f'<animate attributeName="width" from="0" to="{width:.1f}" dur="{dur}s" '
        f'begin="{begin}s" fill="freeze"/></rect></clipPath>'
    )
    label = (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT_MONO}" font-size="{size}" '
        f'fill="{fill}" clip-path="url(#{cid})">{esc(content)}</text>'
    )
    cursor_g = (
        f'<g opacity="0">'
        f'<animate attributeName="opacity" values="0;1;1;1;0;0" '
        f'keyTimes="0;0.05;0.35;0.45;0.75;1" dur="1s" '
        f'begin="{begin + dur + 0.1:.2f}s" fill="freeze"/>'
        f'<text x="{x + width + 7:.1f}" y="{y:.1f}" font-family="{FONT_MONO}" '
        f'font-size="{size}" fill="{cursor}">&#9608;</text>'
        f'</g>'
    )
    return clip + label + cursor_g