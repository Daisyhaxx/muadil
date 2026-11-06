"""İki oyuncunun mevki içi percentile radarı (PNG)."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

# Doğrulanmış kategorik palet, açık tema (slot 1 / slot 2)
QUERY_COLOR = "#2a78d6"
CANDIDATE_COLOR = "#eb6834"
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
FONT = ["Segoe UI", "DejaVu Sans", "sans-serif"]


def _place_axis_labels(ax, angles: np.ndarray, labels: list[str]) -> None:
    """Etiketleri dairenin dışına, bulunduğu tarafa doğru hizalı koyar (sağdakiler sola yaslı vb.)."""
    for angle, text in zip(angles, labels):
        x, y = np.sin(angle), np.cos(angle)  # saat yönünde, tepeden başlayan açı
        ha = "left" if x > 0.1 else "right" if x < -0.1 else "center"
        va = "bottom" if y > 0.1 else "top" if y < -0.1 else "center"
        ax.text(angle, 108, text, ha=ha, va=va, color=INK_SECONDARY, fontsize=9, clip_on=False)


def save_radar(
    labels: list[str],
    query_pct: np.ndarray,
    candidate_pct: np.ndarray,
    names: tuple[str, str],
    title: str,
    path: Path,
    note: str = "",
) -> None:
    """Oyunculardan birinde verisi olmayan eksen (NaN, örn. TFF'de xG) çizilmez, altta not edilir."""
    present = ~(np.isnan(query_pct) | np.isnan(candidate_pct))
    missing = [lab for lab, ok in zip(labels, present) if not ok]
    labels = [lab for lab, ok in zip(labels, present) if ok]
    query_pct, candidate_pct = query_pct[present], candidate_pct[present]
    subtitle = "Mevki içi percentile (0–100), 90 dakika başına"
    if note:
        subtitle += f" · {note}"
    if missing:
        subtitle += f" · veri yok: {', '.join(missing)}"

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    closed = np.append(angles, angles[0])

    with plt.rc_context({"font.family": FONT}):
        fig, ax = plt.subplots(figsize=(8, 8.4), subplot_kw={"polar": True}, facecolor=SURFACE)
        ax.set_facecolor(SURFACE)
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)

        for values, color, name in ((query_pct, QUERY_COLOR, names[0]),
                                    (candidate_pct, CANDIDATE_COLOR, names[1])):
            ring = np.append(values, values[0]) * 100
            ax.fill(closed, ring, color=color, alpha=0.12, linewidth=0)
            ax.plot(closed, ring, color=color, linewidth=2, label=name)
            ax.scatter(angles, values * 100, color=color, s=22, zorder=3,
                       edgecolors=SURFACE, linewidths=1.5)

        ax.set_ylim(0, 100)
        ax.set_yticks([25, 50, 75, 100])
        ax.set_yticklabels(["25", "50", "75", ""], color=MUTED, fontsize=8)
        ax.set_rlabel_position(180 / len(labels))  # ilk iki eksenin arası, çizgiye binmesin
        ax.set_xticks(angles)
        ax.set_xticklabels([])
        _place_axis_labels(ax, angles, labels)
        ax.grid(color=GRID, linewidth=0.8)
        ax.spines["polar"].set_color(GRID)

        fig.suptitle(title, x=0.06, y=0.98, ha="left", color=INK, fontsize=13)
        fig.text(0.06, 0.945, subtitle, ha="left", color=MUTED, fontsize=9)
        ax.legend(loc="upper right", bbox_to_anchor=(1.12, 1.13), frameon=False,
                  labelcolor=INK, fontsize=10)
        fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=SURFACE)
        plt.close(fig)
