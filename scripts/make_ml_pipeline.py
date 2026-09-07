"""Generate ml-pipeline.svg — a clean ML engineering pipeline visual (SMIL only).

Chain:  CODE → DATA → PREPROCESSING → FEATURES → MODEL → EVALUATION → DEPLOYMENT
Emphasized signal path:  DATA → PREPROCESSING → MODEL → EVALUATION → DEPLOYMENT

A subtle indicator travels the emphasized path once, then everything freezes.
"""

from config import (
    BORDER_COLOR, CYAN, GREEN, GREEN_DIM, MUTED, PANEL_COLOR, PANEL_ALT,
    PRIMARY_TEXT, SECONDARY_TEXT, fade, panel, rect, save, svg_close,
    svg_open, text,
)

W = 820
H = 640

BOX_X = 310
BOX_W = 200
BOX_H = 48
SPINE_X = BOX_X + BOX_W + 30          # right-side signal spine
STEP = 78
START_Y = 92

# (y, index, label, is_primary)
STAGES = [
    (START_Y + 0 * STEP, "01", "CODE", False),
    (START_Y + 1 * STEP, "02", "DATA", True),
    (START_Y + 2 * STEP, "03", "PREPROCESSING", True),
    (START_Y + 3 * STEP, "04", "FEATURES", False),
    (START_Y + 4 * STEP, "05", "MODEL", True),
    (START_Y + 5 * STEP, "06", "EVALUATION", True),
    (START_Y + 6 * STEP, "07", "DEPLOYMENT", True),
]

# Emphasis activation timeline (seconds, play once)
ACTIVATIONS = [
    ("DATA", 1.0),
    ("PREPROCESSING", 2.2),
    ("MODEL", 3.4),
    ("EVALUATION", 4.6),
    ("DEPLOYMENT", 5.8),
]
END_BEGIN = 7.0


def arrow(y_top: float, y_bot: float, active: bool) -> str:
    """Thin connector line + arrowhead between two boxes."""
    cx = BOX_X + BOX_W / 2
    y_mid = (y_top + y_bot) / 2
    stroke = CYAN if active else BORDER_COLOR
    line = (
        f'<line x1="{cx:.1f}" y1="{y_top:.1f}" x2="{cx:.1f}" y2="{y_bot - 8:.1f}" '
        f'stroke="{stroke}" stroke-width="1.5"/>'
    )
    head = (
        f'<polygon points="{cx - 4:.1f},{y_bot - 8:.1f} {cx + 4:.1f},{y_bot - 8:.1f} '
        f'{cx:.1f},{y_bot:.1f}" fill="{stroke}"/>'
    )
    return line + head


def box(y: float, index: str, label: str, primary: bool) -> str:
    fill = PANEL_COLOR if primary else PANEL_ALT
    stroke = GREEN_DIM if primary else BORDER_COLOR
    fg = PRIMARY_TEXT if primary else SECONDARY_TEXT
    idx_color = GREEN if primary else MUTED

    glow = ""
    if primary:
        t = dict(ACTIVATIONS)[label]
        glow = (
            f'<rect x="{BOX_X - 4:.1f}" y="{y - 4:.1f}" width="{BOX_W + 8:.1f}" '
            f'height="{BOX_H + 8:.1f}" rx="11" fill="none" stroke="{CYAN}" stroke-width="1.5" opacity="0">'
            f'<animate attributeName="opacity" values="0;0.55;0" dur="0.9s" '
            f'begin="{t:.1f}s" fill="freeze"/></rect>'
        )
        flash = (
            f'<rect x="{BOX_X:.1f}" y="{y:.1f}" width="{BOX_W:.1f}" height="{BOX_H:.1f}" '
            f'rx="8" fill="none" stroke="{GREEN_DIM}" stroke-width="1.5">'
            f'<animate attributeName="stroke" values="{GREEN_DIM};{CYAN};{GREEN_DIM}" '
            f'dur="0.9s" begin="{t:.1f}s" fill="freeze"/></rect>'
        )
    else:
        flash = ""

    body = (
        f'<rect x="{BOX_X:.1f}" y="{y:.1f}" width="{BOX_W:.1f}" height="{BOX_H:.1f}" '
        f'rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
    )
    idx = text(BOX_X - 22, y + BOX_H / 2 + 5, index, size=12, fill=idx_color, anchor="end")
    label_t = text(BOX_X + BOX_W / 2, y + BOX_H / 2 + 5, label, size=15, fill=fg, anchor="middle", weight="bold")
    return glow + body + flash + idx + label_t


def spine() -> str:
    """Right-side signal spine connecting the five primary stages."""
    ys = [y + BOX_H / 2 for y, _, _, p in STAGES if p]
    line = (
        f'<line x1="{SPINE_X:.1f}" y1="{ys[0]:.1f}" x2="{SPINE_X:.1f}" y2="{ys[-1]:.1f}" '
        f'stroke="{PANEL_ALT}" stroke-width="2"/>'
    )
    nodes = ""
    for y, _, label, p in STAGES:
        if not p:
            continue
        cy = y + BOX_H / 2
        nodes += (
            f'<line x1="{BOX_X + BOX_W:.1f}" y1="{cy:.1f}" x2="{SPINE_X:.1f}" y2="{cy:.1f}" '
            f'stroke="{PANEL_ALT}" stroke-width="1.5"/>'
        )
        nodes += f'<circle cx="{SPINE_X:.1f}" cy="{cy:.1f}" r="3" fill="{GREEN_DIM}"/>'
    return line + nodes


def traveler() -> str:
    """Glowing indicator that hops DATA → PREP → MODEL → EVAL → DEPLOY once."""
    centers = [y + BOX_H / 2 for y, _, label, p in STAGES if p]
    d0, d1, d2, d3, d4 = centers
    values = f"{d0};{d0};{d1};{d1};{d2};{d2};{d3};{d3};{d4};{d4}"
    key_times = "0;0.12;0.18;0.30;0.36;0.48;0.54;0.66;0.74;1"
    return (
        f'<circle cx="{SPINE_X:.1f}" cy="{d0:.1f}" r="4" fill="{CYAN}" opacity="0">'
        f'<animate attributeName="opacity" values="0;0.95;0.95;0" keyTimes="0;0.05;0.9;1" '
        f'dur="6.8s" begin="1.0s" fill="freeze"/>'
        f'<animate attributeName="cy" values="{values}" keyTimes="{key_times}" '
        f'dur="6.8s" begin="1.0s" fill="freeze" calcMode="linear"/>'
        f'</circle>'
    )


def build() -> None:
    parts = [svg_open(H)]

    # panel frame
    parts.append(panel(30, 30, W - 60, H - 60))
    parts.append(text(60, 56, "ml_pipeline.run()", size=13, fill=SECONDARY_TEXT))
    parts.append(fade(text(60, 56, "ml_pipeline.run()", size=13, fill=SECONDARY_TEXT), 0.2, 0.3))

    # status readout (top right)
    parts.append(text(W - 60, 56, "STATUS: IDLE", size=13, fill=MUTED, anchor="end"))
    parts.append(fade(text(W - 60, 56, "STATUS: READY", size=13, fill=GREEN, anchor="end", weight="bold"),
                      END_BEGIN, 0.5))

    # arrows between consecutive boxes
    for (y_top, _, _, _), (y_bot, _, _, _) in zip(STAGES, STAGES[1:]):
        parts.append(arrow(y_top + BOX_H, y_bot, active=False))

    # boxes
    for y, index, label, primary in STAGES:
        parts.append(box(y, index, label, primary))

    # signal spine + traveling indicator
    parts.append(spine())
    parts.append(traveler())

    parts.append(svg_close())
    save("ml-pipeline.svg", "".join(parts))


if __name__ == "__main__":
    build()