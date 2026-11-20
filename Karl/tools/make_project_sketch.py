"""Draws Karl/project_sketch.png: the chain Sun -> L1 -> Earth -> Kp -> impacts.

Run from the repo root:  uv run python Karl/tools/make_project_sketch.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

OUT = Path(__file__).resolve().parent.parent / "project_sketch.png"

# (x center, title, body, color)
STEPS = [
    (1.2, "1  SUN", "Eruption:\nflare (light)\nCME (plasma cloud)\nfast solar wind", "#f4a261"),
    (4.0, "2  SPACE", "Charged particles +\nmagnetic field\n300–800 km/s\n(storm: >1000 km/s)", "#e9c46a"),
    (6.8, "3  L1 SATELLITE", "DSCOVR / ACE\nmeasures every minute:\nBz, speed, density", "#8ecae6"),
    (9.6, "4  EARTH", "Magnetosphere\nBz < 0 → field opens\n→ energy flows in", "#90be6d"),
    (12.4, "5  GROUND", "Magnetometers\n→ K → Kp (0–9)\n→ NOAA G-scale", "#b5a7d6"),
]
Y, W, H = 4.6, 2.3, 2.2

fig, ax = plt.subplots(figsize=(16, 9), dpi=130)
ax.set(xlim=(0, 14), ylim=(0, 9))
ax.axis("off")
fig.patch.set_facecolor("white")

ax.text(7, 8.55, "SolarSentinel – from the Sun to a storm warning", ha="center", fontsize=22, weight="bold")
ax.text(7, 8.05, "Goal: predict Kp every few minutes instead of every 3 hours", ha="center", fontsize=13, color="#444")

for x, title, body, color in STEPS:
    ax.add_patch(FancyBboxPatch((x - W / 2, Y - H / 2), W, H, boxstyle="round,pad=0.05",
                                fc=color, ec="#333", lw=1.5))
    ax.text(x, Y + 0.72, title, ha="center", fontsize=12.5, weight="bold")
    ax.text(x, Y - 0.25, body, ha="center", va="center", fontsize=10.5, linespacing=1.4)

# arrows between boxes, with travel time and distance above
LINKS = ["~150 million km\nlight: ~8 min\nCME: 1–3 days", "same particles\nkeep flying",
         "~1.5 million km\n30–90 min", "minutes"]
for (x1, *_), (x2, *_), label in zip(STEPS, STEPS[1:], LINKS):
    ax.add_patch(FancyArrowPatch((x1 + W / 2 + 0.05, Y), (x2 - W / 2 - 0.05, Y),
                                 arrowstyle="-|>", mutation_scale=22, lw=2, color="#333"))
    ax.text((x1 + x2) / 2, Y + 1.5, label, ha="center", fontsize=9.5, color="#222")

# the SolarSentinel window between L1 and Earth
ax.add_patch(Rectangle((6.8 - W / 2 - 0.15, Y - H / 2 - 0.85), 9.6 - 6.8 + W + 0.3, H + 1.0,
                       fill=False, ec="#d62828", lw=2.5, ls="--"))
ax.text(8.2, Y - H / 2 - 0.65, "SolarSentinel works here: 30–90 min warning time\n"
        "warning time = 1.5 million km ÷ solar wind speed", ha="center", fontsize=10.5,
        color="#d62828", weight="bold")

# impacts table at the bottom
ax.text(7, 1.95, "What a strong storm does", ha="center", fontsize=13, weight="bold")
ROWS = [
    ("Kp 5–7  (G1–G3)", "aurora in the north, small grid fluctuations, GPS errors, satellite drag", "#f6bd60"),
    ("Kp 8  (G4 severe)", "voltage problems in the grid, GPS off for hours, HF radio disturbed", "#f28482"),
    ("Kp 9  (G5 extreme)", "grid collapse possible (Québec 1989), transformer damage, GPS off for days,\n"
                           "satellites sink, aurora over all of Germany (May 2024)", "#d62828"),
]
for i, (kp, text, color) in enumerate(ROWS):
    y = 1.45 - i * 0.55
    ax.add_patch(FancyBboxPatch((0.4, y - 0.2), 2.6, 0.4, boxstyle="round,pad=0.03", fc=color, ec="none"))
    ax.text(1.7, y, kp, ha="center", va="center", fontsize=10.5, weight="bold", color="white" if i == 2 else "black")
    ax.text(3.2, y, text, va="center", fontsize=10.2)

fig.savefig(OUT, bbox_inches="tight", facecolor="white")
print("saved", OUT)
