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
SESSION_SUMMARY_PATH = REPO_ROOT / "outputs" / "session_summary.csv"
HIGHEST_BPM_PATH = REPO_ROOT / "outputs" / "highest_bpm_threshold.csv"
OUT_DIR = REPO_ROOT / "analysis" / "figures"
OUT_PATH = OUT_DIR / "max_bpm_clean_ratio_ge_075.png"

THRESHOLD = 0.75
mode_colors = {
    1: "#8FD3FE",
    2: "#FFE08A",
    3: "#C3B1E1",
    4: "#FF9B85",
}


def main() -> None:
    if not SESSION_SUMMARY_PATH.exists() or not HIGHEST_BPM_PATH.exists():
        raise FileNotFoundError(
            "Missing outputs files. Run: python analysis/main_analysis.py"
        )

    sessions = (
        pd.read_csv(SESSION_SUMMARY_PATH)["session"].drop_duplicates().sort_values().tolist()
    )
    max_bpm_df = pd.read_csv(HIGHEST_BPM_PATH).sort_values(["session", "mode"])
    max_bpm_table = max_bpm_df.pivot(index="session", columns="mode", values="bpm")
    modes_in_data = sorted(int(mode) for mode in max_bpm_df["mode"].unique())
    print("Modes in dataset:", modes_in_data)

    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    fig.patch.set_alpha(0)
    ax.set_facecolor("#0b1111")
    modes = sorted(mode_colors.keys())
    for mode in modes:
        mode_data = max_bpm_df[max_bpm_df["mode"] == mode][["session", "bpm"]]
        mode_full = pd.DataFrame({"session": sessions}).merge(
            mode_data, on="session", how="left"
        )

        ax.plot(
            mode_full["session"],
            mode_full["bpm"],
            marker="o",
            linewidth=2.5,
            markersize=7,
            color=mode_colors[mode],
            label=f"Mode {mode}",
        )
        ax.scatter(
            mode_full["session"],
            mode_full["bpm"],
            s=40,
            color=mode_colors[mode],
            zorder=4,
        )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(colors="#cfcfcf")
    ax.xaxis.label.set_color("#d8d8d8")
    ax.yaxis.label.set_color("#d8d8d8")

    ax.set_xlabel("Session")
    ax.set_ylabel("Maximum sustainable speed (beats per minute)")
    ax.set_xticks(sessions)
    ax.set_ylim(55, 115)
    ax.set_yticks([60, 70, 80, 90, 100, 110])
    ax.axhline(y=90, linestyle="--", color="#8e8e8e", alpha=0.3)

    first_reach_rows = max_bpm_table.dropna(how="all")
    if not first_reach_rows.empty:
        first_session = int(first_reach_rows.index[0])
        first_row = max_bpm_table.loc[first_session]
        first_value = float(first_row.max(skipna=True))
        ax.scatter(first_session, first_value, s=80, color="#6BFFA7", zorder=5)
        ax.annotate(
            "Threshold first reached",
            xy=(first_session, first_value),
            xytext=(first_session + 0.6, min(first_value + 8, 112)),
            arrowprops=dict(arrowstyle="->", color="#6BFFA7"),
            color="#6BFFA7",
            fontsize=9,
        )

    max_bpm_non_na = max_bpm_df.dropna(subset=["bpm"]).set_index(["session", "mode"])["bpm"]
    if not max_bpm_non_na.empty:
        best_session, _best_mode = max_bpm_non_na.idxmax()
        best_value = float(max_bpm_non_na.max())
        ax.scatter(best_session, best_value, s=80, color="#6BFFA7", zorder=5)
        ax.annotate(
            "Highest sustained BPM",
            xy=(best_session, best_value),
            xytext=(best_session - 2.0, max(best_value - 10, 58)),
            arrowprops=dict(arrowstyle="->", color="#6BFFA7"),
            color="#6BFFA7",
            fontsize=9,
        )

    ax.legend(title="Mode", framealpha=0.95)
    grid_color = (0, 1, 170 / 255, 0.08)
    ax.grid(True, linestyle="--", alpha=0.15, color=grid_color)
    fig.tight_layout()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PATH, dpi=150, transparent=True)
    plt.close(fig)
    print(f"Wrote {OUT_PATH}")
    expected_pairs = len(sessions) * len(mode_colors)
    n_missing = expected_pairs - len(max_bpm_df)
    if n_missing:
        print(
            f"Note: {n_missing} (session, mode) pairs had no row with "
            f"accuracy >= {THRESHOLD:g} (plotted as gaps)."
        )


if __name__ == "__main__":
    main()
