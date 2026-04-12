"""
clean_ratio vs BPM: one line per mode, mean clean_ratio across sessions.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = REPO_ROOT / "data" / "main-data.csv"
OUT_DIR = REPO_ROOT / "analysis" / "figures"
OUT_PATH = OUT_DIR / "clean_ratio_vs_bpm_by_mode.png"


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    by_mode_bpm = (
        df.groupby(["mode", "bpm"], as_index=False)["clean_ratio"].mean().sort_values(
            ["mode", "bpm"]
        )
    )

    fig, ax = plt.subplots(figsize=(8, 4.5))
    for mode in sorted(by_mode_bpm["mode"].unique()):
        sub = by_mode_bpm[by_mode_bpm["mode"] == mode]
        ax.plot(
            sub["bpm"],
            sub["clean_ratio"],
            marker="o",
            linewidth=2,
            markersize=7,
            label=f"Mode {mode}",
        )

    ax.set_xlabel("BPM")
    ax.set_ylabel("clean_ratio")
    ax.set_title("clean_ratio vs BPM by mode (mean across sessions)")
    ax.set_xticks(sorted(df["bpm"].unique()))
    ax.set_ylim(0, 1.05)
    ax.legend(title="Mode", framealpha=0.95)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PATH, dpi=150)
    plt.close(fig)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
