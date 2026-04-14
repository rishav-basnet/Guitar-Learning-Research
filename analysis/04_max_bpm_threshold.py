"""
Per (session, mode): max BPM with clean_ratio >= 0.75; line plot by mode vs session.

If no row meets the threshold for a (session, mode), the value is NaN (line breaks).
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = REPO_ROOT / "data" / "main-data.csv"
OUT_DIR = REPO_ROOT / "analysis" / "figures"
OUT_PATH = OUT_DIR / "max_bpm_clean_ratio_ge_075.png"

THRESHOLD = 0.75


def max_bpm_per_session_mode(df: pd.DataFrame) -> pd.Series:
    sessions = sorted(df["session"].unique())
    modes = sorted(df["mode"].unique())
    full_idx = pd.MultiIndex.from_product(
        [sessions, modes], names=["session", "mode"]
    )
    passed = df[df["clean_ratio"] >= THRESHOLD]
    max_bpm = passed.groupby(["session", "mode"])["bpm"].max()
    return max_bpm.reindex(full_idx)


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    max_bpm = max_bpm_per_session_mode(df)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    sessions = sorted(df["session"].unique())

    for mode in sorted(df["mode"].unique()):
        y = max_bpm.xs(mode, level="mode").reindex(sessions)
        ax.plot(
            sessions,
            y,
            marker="o",
            linewidth=2,
            markersize=7,
            label=f"Mode {mode}",
        )

    ax.set_xlabel("Session")
    ax.set_ylabel("Max BPM (clean_ratio ≥ 0.75)")
    ax.set_title(
        f"Maximum BPM meeting clean_ratio ≥ {THRESHOLD:g}, by session and mode"
    )
    ax.set_xticks(sessions)
    ax.set_ylim(55, 115)
    ax.set_yticks(sorted(df["bpm"].unique()))
    ax.legend(title="Mode", framealpha=0.95)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PATH, dpi=150)
    plt.close(fig)
    print(f"Wrote {OUT_PATH}")

    n_missing = int(max_bpm.isna().sum())
    if n_missing:
        print(
            f"Note: {n_missing} (session, mode) pairs had no row with "
            f"clean_ratio >= {THRESHOLD:g} (plotted as gaps)."
        )


if __name__ == "__main__":
    main()
