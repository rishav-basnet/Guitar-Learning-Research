"""
clean_ratio vs BPM: one line per mode, mean clean_ratio across sessions.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
BPM_MODE_PATH = REPO_ROOT / "outputs" / "bpm_mode_accuracy.csv"
OUT_DIR = REPO_ROOT / "analysis" / "figures"
OUT_PATH = OUT_DIR / "clean_ratio_vs_bpm_by_mode.png"

mode_colors = {
    1: "#8FD3FE",
    2: "#FFE08A",
    3: "#C3B1E1",
    4: "#FF9B85",
}


def main() -> None:
    if not BPM_MODE_PATH.exists():
        raise FileNotFoundError(
            f"Missing {BPM_MODE_PATH}. Run: python analysis/main_analysis.py"
        )

    by_mode_bpm = pd.read_csv(BPM_MODE_PATH).sort_values(["mode", "bpm"])
    modes = sorted(int(mode) for mode in by_mode_bpm["mode"].unique())
    bpms = sorted(int(bpm) for bpm in by_mode_bpm["bpm"].unique())

    bpm_means = []
    for bpm in bpms:
        vals = by_mode_bpm.loc[by_mode_bpm["bpm"] == bpm, "accuracy"]
        bpm_means.append((bpm, float(vals.mean())))

    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    fig.patch.set_alpha(0)
    ax.set_facecolor("#0b1111")
    for mode in modes:
        mode_data = by_mode_bpm[by_mode_bpm["mode"] == mode]

        if mode_data.empty:
            print(f"Skipping Mode {mode}: no rows after aggregation")
            continue

        ax.plot(
            mode_data["bpm"],
            mode_data["accuracy"],
            marker="o",
            linewidth=2.5,
            markersize=7,
            color=mode_colors[mode],
            label=f"Mode {mode}",
        )
        ax.scatter(
            mode_data["bpm"],
            mode_data["accuracy"],
            s=40,
            color=mode_colors[mode],
            zorder=4,
        )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(colors="#cfcfcf")
    ax.xaxis.label.set_color("#d8d8d8")
    ax.yaxis.label.set_color("#d8d8d8")

    ax.set_xlabel("Speed (beats per minute)")
    ax.set_ylabel("Accuracy (successful transitions)")
    ax.set_xticks(bpms)
    ax.set_ylim(0, 1.05)
    ax.axhline(y=0.75, linestyle="--", color="#8e8e8e", alpha=0.3)

    best_bpm, best_y = max(bpm_means, key=lambda row: row[1])
    ax.scatter(best_bpm, best_y, s=80, color="#6BFFA7", zorder=5)
    ax.annotate(
        "Best-performing BPM range",
        xy=(best_bpm, best_y),
        xytext=(best_bpm + 4, min(best_y + 0.14, 0.98)),
        arrowprops=dict(arrowstyle="->", color="#6BFFA7"),
        color="#6BFFA7",
        fontsize=9,
    )

    high_bpm = max(bpms)
    high_y = next(mean for bpm, mean in bpm_means if bpm == high_bpm)
    ax.scatter(high_bpm, high_y, s=80, color="#6BFFA7", zorder=5)
    ax.annotate(
        "Accuracy generally drops at higher speeds, especially in harder modes",
        xy=(high_bpm, high_y),
        xytext=(high_bpm - 18, max(high_y - 0.18, 0.1)),
        arrowprops=dict(arrowstyle="->", color="#6BFFA7"),
        color="#6BFFA7",
        fontsize=9,
    )

    ax.legend(title="Mode", framealpha=0.9)
    grid_color = (0, 1, 170 / 255, 0.08)
    ax.grid(True, linestyle="--", alpha=0.15, color=grid_color)
    fig.tight_layout()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PATH, dpi=150, transparent=True)
    plt.close(fig)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
