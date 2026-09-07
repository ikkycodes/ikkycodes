"""Generate info-card.svg - a clean professional profile panel (SMIL only).

Shows "AI/ML Engineer" as the brand block - no personal name, no fake
terminal commands, no photos/portraits. Each row reveals sequentially then freezes.
"""

from config import (
    BORDER_COLOR, CYAN, GREEN, GREEN_DIM, MUTED, PANEL_ALT, PANEL_COLOR,
    PRIMARY_TEXT, SECONDARY_TEXT, fade, panel, rect, save, svg_close,
    svg_open, text,
)


W =820
H =460

PANEL_X, PANEL_Y, PANEL_W, PANEL_H =40,26,W -80,400


ROWS = [
    ("Name", "Ikjyot Singh"),
    ("Education", "B.Tech Computer Science"),
    ("University", "Sri Guru Granth Sahib World"),
    ("Focus", "ML \u2022 GenAI \u2022 MLOps"),
    ("Python", "NumPy \u2022 Pandas"),
    ("ML", "Scikit-learn"),
    ("AI", "TensorFlow \u2022 Keras"),
    ("GenAI", "LLMs \u2022 RAG \u2022 Embeddings"),
    ("Backend", "FastAPI \u2022 Streamlit"),
    ("DevOps", "Docker \u2022 Git \u2022 GitHub"),
]

LABEL_X =340
VALUE_X =470
ROW_STEP =25
ROW_START =116


def brand_panel() -> str:
    gx, gy, gw, gh =72,96,210,270
    grid = (
        '<pattern id="grid" width="14" height="14" patternUnits="userSpaceOnUse">'
        + f'<path d="M 14 0 L 0 0 0 14" fill="none" stroke="{PANEL_ALT}" stroke-width="1"/>'
        + '</pattern>'
    )
    out = grid
    out += f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" rx="12" fill="{PANEL_COLOR}" stroke="{BORDER_COLOR}" stroke-width="1"/>'
    out += f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" rx="12" fill="url(#grid)" opacity="0.6"/>'

    # brand - AI/ML Engineer
    out += fade(text(gx + gw / 2, 152,"AI/ML", size=40, fill=CYAN, anchor="middle", weight="bold"),0.5,0.5)
    out += fade(text(gx + gw /  2,186, "ENGINEER", size=20, fill=GREEN, anchor="middle", weight="bold", spacing="3"),1.0,0.4)

    # divider
    out += fade(f'<line x1="{gx + 24}" y1="212" x2="{gx + gw -  24}" y2="212" stroke="{BORDER_COLOR}" stroke-width="1"/>',1.3,0.3)

    # focus chips - clean labels
    out += fade(text(gx + gw /  2,238, "ML \u2022 GenAI \u2022 MLOps", size=12, fill=SECONDARY_TEXT, anchor="middle"),1.6,0.35)
    out += fade(text(gx + gw /2,261, "PYTHON \u2022 TENSORFLOW", size=12, fill=SECONDARY_TEXT, anchor="middle"),1.9,0.35)

    # circuit accents
    out += fade(
        f'<circle cx="{gx + 40}" cy="318" r="3" fill="{GREEN_DIM}"/>'
        + f'<circle cx="{gx + 170}" cy="318" r="3" fill="{CYAN}"/>'
        + f'<line x1="{gx + 46}" y1="318" x2="{gx + 164}" y2="318" stroke="{BORDER_COLOR}" stroke-width="1"/>',
        2.8,0.4,
    )
    return out


def build() -> None:
    parts = [svg_open(H)]

    # panel frame + header
    parts.append(panel(PANEL_X,PANEL_Y,PANEL_W,PANEL_H))
    parts.append(fade(text(PANEL_X +32,60, "PROFILE", size=16, fill=CYAN, weight="bold", spacing="3"),0.2,0.4))
    parts.append(fade(text(PANEL_X + PANEL_W -32,60, "ikky@github", size=12, fill=SECONDARY_TEXT, anchor="end"),0.45,0.35))
    parts.append(
        fade(f'<line x1="{PANEL_X +32}" y1="86" x2="{PANEL_X + PANEL_W -32}" y2="86" '
             f'stroke="{BORDER_COLOR}" stroke-width="1"/>',0.7,0.3)
    )

    # left brand block
    parts.append(brand_panel())

    # info rows - sequential reveal
    t =1.2
    for i,(label,value) in enumerate(ROWS):
        y = ROW_START + i * ROW_STEP
        row = (
            text(LABEL_X,y,label,size=14,fill=CYAN)
            + text(VALUE_X,y,value,size=14,fill=PRIMARY_TEXT)
        )
        parts.append(fade(row,t,0.32))
        t +=0.26

    # goal line
    parts.append(
        fade(f'<line x1="{LABEL_X}" y1="372" x2="{PANEL_X + PANEL_W -32}" y2="372" '
             f'stroke="{BORDER_COLOR}" stroke-width="1"/>',t,0.3)
    )
    goal = (
        text(LABEL_X,400, "Goal", size=14, fill=GREEN)
        + text(VALUE_X,400, "Build real-world AI systems", size=14, fill=PRIMARY_TEXT, weight="bold")
    )
    parts.append(fade(goal,t +0.25,0.4))

    parts.append(svg_close())
    save("info-card.svg","".join(parts))


if __name__ == "__main__":
    build()