import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "figure.facecolor": "white",
})

# --- solar vertical SHM, phase fixed by present position ---
P = 60.0              # Myr
t_cross = -2.7        # last midplane crossing (Myr; negative = past)
z0 = 20.0             # present height, pc
omega = 2 * np.pi / P
A = z0 / np.sin(omega * (0.0 - t_cross))   # ~72 pc

age = np.linspace(540, 0, 4000)

def z_of_age(a):
    t = -np.asarray(a)                      # t = 0 now, past is negative
    return A * np.sin(omega * (t - t_cross))

def vz_of_age(a):
    t = -np.asarray(a)
    return A * omega * np.cos(omega * (t - t_cross))  # pc / Myr

z = z_of_age(age)

# biodiversity schematic: peaks at 40, 100, 160, ... Ma
D = np.cos(2 * np.pi * (age - 40.0) / P)

events = [
    ("O–S", 444.0),
    ("Late Dev.", 372.0),
    ("P–T", 252.0),
    ("Tr–J", 201.0),
    ("K–Pg", 66.0),
]

fig = plt.figure(figsize=(15.2, 10.2))

# ========== Panel 1: biodiversity ==========
ax1 = fig.add_subplot(2, 1, 1)

# declining halves: peak (40 + 60k) -> trough (10 + 60k) as time runs forward
for k in range(-1, 12):
    peak = 40 + 60 * k
    trough = 10 + 60 * k
    a_left = max(trough, 0)
    a_right = min(peak, 540)
    if a_right > a_left:
        ax1.axvspan(a_left, a_right, color="#f4c1c1", alpha=0.45, zorder=0)

ax1.plot(age, D, color="#1f4e8c", lw=2.15, zorder=3, label="60 Myr biodiversity cycle")
ax1.axhline(0, color="#888888", lw=0.8, ls=":")

for name, a in events:
    d = np.cos(2 * np.pi * (a - 40.0) / P)
    ax1.axvline(a, color="#b33", lw=0.9, ls="--", alpha=0.7, zorder=2)
    ax1.scatter([a], [d], marker="v", s=90, c="#c0392b", zorder=5,
                edgecolors="white", linewidths=0.6)
    va = "bottom" if d < 0.15 else "top"
    ytxt = d + (0.18 if d < 0.15 else -0.18)
    ax1.annotate(
        f"{name}\n({a:.0f} Ma)", xy=(a, d), xytext=(a, ytxt),
        ha="center", va=va, fontsize=8, color="#8b1e1e", fontweight="bold",
    )

ax1.set_xlim(540, 0)
ax1.set_ylim(-1.35, 1.55)
ax1.set_ylabel("Normalized marine genus diversity\n(60 Myr cyclic component)")
ax1.set_title(
    "60 Myr biodiversity cycle and the Big Five  —  "
    "with reconstructed solar height on the same clock",
    pad=8,
)
ax1.legend(loc="upper left", framealpha=0.92, fontsize=9)
ax1.text(
    0.99, 0.06,
    "Declining phase shaded   |   period = 60 Myr (Rohde & Muller–style schematic)",
    transform=ax1.transAxes, ha="right", va="bottom", fontsize=8, color="#666",
)
ax1.set_xticks([540, 500, 450, 400, 350, 300, 250, 200, 150, 100, 50, 0])

# ========== Panel 2: solar z ==========
ax2 = fig.add_subplot(2, 1, 2, sharex=ax1)

ax2.axhspan(-25, 25, color="#4a90d9", alpha=0.16, zorder=0)
ax2.axhline(0, color="#2c6fbb", lw=1.15, zorder=1)
ax2.plot(age, z, color="#e6b800", lw=2.15, zorder=3,
         label="Sun vertical path  z(t)  (schematic SHM)")

ax2.scatter([0], [z0], s=130, c="#ff5533", zorder=6,
            edgecolors="white", linewidths=1.0)
ax2.annotate(
    "NOW\n+20 pc, moving north", xy=(0, z0), xytext=(28, 58),
    fontsize=8, color="#c4451d",
    arrowprops=dict(arrowstyle="->", color="#c4451d", lw=1.1), ha="left",
)

ax2.scatter([2.7], [0], s=36, c="white", edgecolors="#333", zorder=5, linewidths=0.8)
ax2.annotate(
    "last plane\ncrossing\n2.7 Ma", xy=(2.7, 0), xytext=(55, -78),
    fontsize=7.5, color="#444",
    arrowprops=dict(arrowstyle="->", color="#888", lw=0.9), ha="center",
)

for name, a in events:
    za = float(z_of_age(a))
    vza = float(vz_of_age(a))
    ax2.axvline(a, color="#b33", lw=0.9, ls="--", alpha=0.7, zorder=2)
    ax2.scatter([a], [za], marker="o", s=70, c="#c0392b", zorder=5,
                edgecolors="white", linewidths=0.7)
    side = "S" if za < 0 else "N"
    going = "↑" if vza > 0 else "↓"
    ax2.annotate(
        f"{name}\n{za:.0f} pc {side} {going}",
        xy=(a, za), xytext=(a, za - 22),
        ha="center", va="top", fontsize=7.5, color="#7a1f1f",
    )

ax2.set_xlim(540, 0)
ax2.set_ylim(-110, 100)
ax2.set_xlabel("Age (million years ago)")
ax2.set_ylabel("Sun height  z  (parsecs)\nabove / below midplane")
ax2.legend(loc="upper left", framealpha=0.92, fontsize=9)
ax2.grid(True, alpha=0.25)
ax2.text(
    0.99, 0.04,
    f"P = 60 Myr   |   amplitude ≈ {A:.0f} pc   |   "
    "phase fixed by present z ≈ +20 pc, W > 0\n"
    "Schematic sine, not a full Galactic-potential orbit",
    transform=ax2.transAxes, ha="right", va="bottom", fontsize=8, color="#555",
)

periods = [
    (541, 485.4, "#f3e9c6", "Cam"),
    (485.4, 443.8, "#d4b36a", "Ord"),
    (443.8, 419.2, "#c6e3b5", "Sil"),
    (419.2, 358.9, "#d19b5b", "Dev"),
    (358.9, 298.9, "#67a87a", "Carb"),
    (298.9, 251.9, "#d9898a", "Perm"),
    (251.9, 201.3, "#b39bc9", "Trias"),
    (201.3, 145.0, "#7eb6d6", "Jura"),
    (145.0, 66.0, "#6aa84f", "Cret"),
    (66.0, 23.0, "#f0b429", "Pg"),
    (23.0, 0.0, "#ffe599", "N"),
]
ymin, ymax = -110, -96
for a0, a1, c, lab in periods:
    ax2.add_patch(plt.Rectangle(
        (a1, ymin), a0 - a1, ymax - ymin,
        facecolor=c, edgecolor="white", lw=0.4, zorder=4, clip_on=True,
    ))
    mid = 0.5 * (a0 + a1)
    if a0 - a1 > 18:
        ax2.text(mid, 0.5 * (ymin + ymax), lab, ha="center", va="center",
                 fontsize=7.5, color="#222", zorder=5)

plt.tight_layout(h_pad=1.6)
plt.savefig("combined_sun_biodiversity.png", dpi=160, bbox_inches="tight",
            facecolor="white")
plt.show()
