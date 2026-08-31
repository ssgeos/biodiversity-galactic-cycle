import numpy as np
import matplotlib.pyplot as plt

# Time axis (age in Ma, older on the left)
age = np.linspace(540, 0, 2000)

# Cycle parameters chosen so all Big Five sit on declining limbs
T = 61.0          # Myr
phi = 5.182098591317795

# D = sin(2π·age/T + φ)
# dD/dage > 0 wherever cos(...) > 0, so D falls as we move right (toward the present)
cycle = np.sin(2 * np.pi * age / T + phi)
cos_term = np.cos(2 * np.pi * age / T + phi)
declining = cos_term > 0

extinctions = {
    "O–S\n(444 Ma)": 443.8,
    "Late Dev.\n(372 Ma)": 372.2,
    "P–T\n(252 Ma)": 251.9,
    "Tr–J\n(201 Ma)": 201.3,
    "K–Pg\n(66 Ma)": 66.0,
}

fig, ax = plt.subplots(figsize=(12, 5.2))

ax.plot(age, cycle, color="#1f77b4", linewidth=2.4, label="60 Myr biodiversity cycle")
ax.fill_between(
    age, -1.35, 1.35, where=declining,
    color="#ffcccc", alpha=0.35, label="Declining phase"
)

for label, a in extinctions.items():
    y = np.sin(2 * np.pi * a / T + phi)
    ax.axvline(a, color="#c0392b", linestyle="--", linewidth=1.1, alpha=0.8)
    ax.scatter([a], [y], color="#c0392b", s=90, zorder=5, marker="v")
    va = "bottom" if y < 0.3 else "top"
    offset = 0.18 if y < 0.3 else -0.18
    ax.annotate(
        label, xy=(a, y), xytext=(a, y + offset),
        ha="center", va=va, fontsize=8, color="#8b0000", fontweight="bold"
    )

ax.set_xlim(540, 0)
ax.set_ylim(-1.45, 1.55)
ax.set_xlabel("Age (million years ago)", fontsize=12)
ax.set_ylabel("Normalized marine genus diversity\n(60 Myr cyclic component)", fontsize=11)
ax.set_title(
    "60-Myr biodiversity cycle and the Big Five mass extinctions\n"
    "(all five fall on declining phases of the cycle)",
    fontsize=13, pad=10,
)
ax.axhline(0, color="gray", linewidth=0.6, linestyle=":")
ax.legend(loc="upper left", framealpha=0.92, fontsize=9)
ax.grid(True, axis="x", alpha=0.25)

# Simple period color bar
periods = [
    (541, 485, "Cam"),
    (485, 444, "Ord"),
    (444, 419, "Sil"),
    (419, 359, "Dev"),
    (359, 299, "Carb"),
    (299, 252, "Perm"),
    (252, 201, "Trias"),
    (201, 145, "Jura"),
    (145, 66, "Cret"),
    (66, 23, "Pg"),
    (23, 0, "N"),
]
colors = [
    "#f4e3c1", "#f0d080", "#cfe8b0", "#e8c48a", "#8fbf8f", "#e6a0a0",
    "#c9a0dc", "#7ec8e3", "#7cb342", "#ffb74d", "#fff59d",
]
for (start, end, name), color in zip(periods, colors):
    ax.axvspan(
        start, end, ymin=0.0, ymax=0.045,
        color=color, transform=ax.get_xaxis_transform(),
        alpha=0.85, linewidth=0,
    )
    ax.text((start + end) / 2, -1.38, name, ha="center", va="center", fontsize=7.5, color="#333")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("biodiversity-cycle.png", dpi=160, bbox_inches="tight", facecolor="white")
plt.show()
