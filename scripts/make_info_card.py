"""Generate info-card.svg — a Neofetch-style terminal profile card (SMIL only).

Each line reveals sequentially, then the card freezes. No personal photos,
no portraits, no JavaScript.
"""

from config import (
    BORDER_COLOR, CYAN, GREEN, GREEN_DIM, MUTED, PANEL_ALT, PANEL_COLOR,
    PRIMARY_TEXT, SECONDARY_TEXT, fade, panel, rect, save, svg_close,
    svg_open, text,
)

W = 820
H = 470

PANEL_X, PANEL_Y, PANEL_W, PANEL_H = 40, 26, W - 80, 400

# (label, value) rows — Neofetch layout
ROWS = [
    ("Name", "Ikjyot Singh"),
    ("Role", "AI/ML Engineer"),
    ("Education", "B.Tech Computer Science"),
    ("University", "Sri Guru Granth Sahib World"),
    ("Focus", "ML • GenAI • MLOps"),
    ("Python", "NumPy • Pandas"),
    ("ML", "Scikit-learn"),
    ("AI", "TensorFlow • Keras"),
    ("GenAI", "LLMs • RAG • Embeddings"),
    ("Backend", "FastAPI • Streamlit"),
    ("DevOps", "Docker • Git • GitHub"),
]

LABEL_X = 340
VALUE_X = 470
ROW_STEP = 24
ROW_START = 112


def glyph_panel() -> str:
    """Abstract terminal glyph block (no photo, no portrait)."""
    gx, gy, gw, gh = 72, 96, 210, 280
    grid = (
        '<pattern id="grid" width="14" height="14" patternUnits="userSpaceOnUse">'
        f'<path d="M 14 0 L 0 0 0 14" fill="none" stroke="{PANEL_ALT}" stroke-width="1"/>'
        "</pattern>"
    )
    out = grid
    out += f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" rx="10" fill="{PANEL_COLOR}" stroke="{BORDER_COLOR}" stroke-width="1"/>'
    out += f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" rx="10" fill="url(#grid)" opacity="0.6"/>'

    # big monogram
    out += fade(text(gx + gw / 2, 150, "ikky", size=34, fill=GREEN, anchor="middle", weight="bold"), 0.5, 0.5)
    out += fade(text(gx + gw / 2, 176, "AI/ML ENGINEER", size=12, fill=CYAN, anchor="middle", spacing="2"), 1.0, 0.4)

    # divider
    out += fade(f'<line x1="{gx + 24}" y1="196" x2="{gx + gw - 24}" y2="196" stroke="{BORDER_COLOR}" stroke-width="1"/>', 1.3, 0.3)

    # mini terminal
    out += fade(text(gx + 20, 224, "$ whoami", size=13, fill=SECONDARY_TEXT), 1.6, 0.35)
    out += fade(text(gx + 20, 246, "> Ikjyot Singh", size=13, fill=PRIMARY_TEXT), 1.9, 0.35)
    out += fade(text(gx + 20, 268, "$ pwd", size=13, fill=SECONDARY_TEXT), 2.2, 0.35)
    out += fade(text(gx + 20, 290, "> ~/ai-ml/engineer", size=13, fill=PRIMARY_TEXT), 2.5, 0.35)

    # circuit accents
    out += fade(
        f'<circle cx="{gx + 40}" cy="318" r="3" fill="{GREEN_DIM}"/>'
        f'<circle cx="{gx + 170}" cy="318" r="3" fill="{CYAN}"/>'
        f'<line x1="{gx + 46}" y1="318" x2="{gx + 164}" y2="318" stroke="{BORDER_COLOR}" stroke-width="1"/>',
        2.8, 0.4,
    )
    return out


def build() -> None:
    parts = [svg_open(H)]

    # panel frame + header
    parts.append(panel(PANEL_X, PANEL_Y, PANEL_W, PANEL_H))
    parts.append(fade(text(PANEL_X + 32, 60, "ikky@github", size=16, fill=GREEN, weight="bold"), 0.2, 0.4))
    parts.append(fade(text(PANEL_X + 32, 78, "whoami — profile", size=12, fill=MUTED), 0.45, 0.35))
    parts.append(
        fade(f'<line x1="{PANEL_X + 32}" y1="90" x2="{PANEL_X + PANEL_W - 32}" y2="90" '
             f'stroke="{BORDER_COLOR}" stroke-width="1"/>', 0.7, 0.3)
    )

    # left glyph panel
    parts.append(glyph_panel())

    # info rows — sequential reveal
    t = 1.2
    for i, (label, value) in enumerate(ROWS):
        y = ROW_START + i * ROW_STEP
        row = (
            text(LABEL_X, y, label, size=14, fill=CYAN)
            + text(VALUE_X, y, value, size=14, fill=PRIMARY_TEXT)
        )
        parts.append(fade(row, t, 0.32))
        t += 0.26

    # goal line
    parts.append(
        fade(f'<line x1="{LABEL_X}" y1="392" x2="{PANEL_X + PANEL_W - 32}" y2="392" '
             f'stroke="{BORDER_COLOR}" stroke-width="1"/>', t, 0.3)
    )
    goal = (
        text(LABEL_X, 414, "Goal", size=14, fill=GREEN)
        + text(VALUE_X, 414, "Build real-world AI systems", size=14, fill=PRIMARY_TEXT, weight="bold")
    )
    parts.append(fade(goal, t + 0.25, 0.4))

    parts.append(svg_close())
    save("info-card.svg", "".join(parts))


if __name__ == "__main__":
    build()