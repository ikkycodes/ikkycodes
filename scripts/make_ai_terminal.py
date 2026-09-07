"""Generate ai-terminal.svg — a play-once terminal boot animation (SMIL only).

Flow:  BOOT → INITIALIZATION → MODULE LOADING → STATUS COMPLETE
Runs exactly once, then freezes on the final frame. No JavaScript, no loops.

This is a static portfolio visual — it does not imply any live system.
"""

from config import (
    BORDER_COLOR, GREEN, MUTED, PANEL_ALT, PRIMARY_TEXT, SECONDARY_TEXT,
    fade, panel, rect, save, svg_close, svg_open, text, typed_text,
)

MODULES = [
    "Loading Python runtime...",
    "Loading ML modules...",
    "Loading data pipeline...",
    "Loading deep learning stack...",
    "Initializing LLM interface...",
    "Initializing RAG pipeline...",
    "Connecting vector database...",
    "Loading deployment layer...",
]

W = 820
H = 428
LEFT = 64
BAR_X = LEFT + 16
BAR_W = 600
CHECK_X = W - 88


def progress_bar(begin: float) -> str:
    track = (
        f'<rect x="{BAR_X:.1f}" y="150" width="{BAR_W:.1f}" height="9" rx="4.5" '
        f'fill="{PANEL_ALT}" stroke="{BORDER_COLOR}" stroke-width="1"/>'
    )
    fill = (
        f'<rect x="{BAR_X:.1f}" y="150" width="0" height="9" rx="4.5" fill="{GREEN}">'
        f'<animate attributeName="width" from="0" to="{BAR_W:.1f}" dur="1.0s" '
        f'begin="{begin:.2f}s" fill="freeze" calcMode="linear"/></rect>'
    )
    number = fade(text(BAR_X + BAR_W + 14, 159, "100%", size=12, fill=GREEN), begin, 0.2)
    return track + fill + number


def build() -> None:
    parts = [svg_open(H)]

    # ---- window chrome -----------------------------------------------------
    parts.append(panel(40, 24, W - 80, H - 48))
    for i, color in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(rect(60 + i * 22, 43, 10, 10, fill=color, rx=10))
    parts.append(text(W / 2, 55, "initialize_ai.sh — ikky@github", size=12, fill=MUTED, anchor="middle"))
    parts.append(rect(40, 68, W - 80, 1, fill=BORDER_COLOR))

    # ---- 1) BOOT -----------------------------------------------------------
    parts.append(typed_text(LEFT, 100, "ikky@github ~ $ ./initialize_ai.sh",
                            begin=0.3, dur=0.9, size=15, fill=PRIMARY_TEXT, cursor=GREEN))

    # ---- 2) INITIALIZATION -------------------------------------------------
    parts.append(fade(text(LEFT, 130, "> Initializing AI environment...", size=14, fill=SECONDARY_TEXT),
                      1.5, 0.4))
    parts.append(progress_bar(2.0))

    # ---- 3) MODULE LOADING -------------------------------------------------
    t = 3.3
    for i, module in enumerate(MODULES):
        y = 196 + i * 22
        label = text(LEFT, y, f"> {module}", size=14, fill=SECONDARY_TEXT)
        check = text(CHECK_X, y, "✓", size=14, fill=GREEN)
        parts.append(fade(label, t))
        parts.append(fade(check, t + 0.35, 0.25))
        t += 0.42

    # ---- 4) STATUS COMPLETE ------------------------------------------------
    status = (
        text(W / 2, 376, "SYSTEM STATUS:", size=16, fill=SECONDARY_TEXT, anchor="middle")
        + text(W / 2 + 118, 376, "ONLINE", size=16, fill=GREEN, anchor="start", weight="bold")
    )
    parts.append(fade(status, t + 0.15, 0.5))

    parts.append(svg_close())
    save("ai-terminal.svg", "".join(parts))


if __name__ == "__main__":
    build()