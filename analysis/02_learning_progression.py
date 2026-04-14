"""
Mean clean_ratio by session (learning progression), line chart.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
SESSION_SUMMARY_PATH = REPO_ROOT / "outputs" / "session_summary.csv"
OUT_DIR = REPO_ROOT / "analysis" / "figures"
OUT_PATH = OUT_DIR / "learning_progression_clean_ratio.png"


def main() -> None:
    if not SESSION_SUMMARY_PATH.exists():
        raise FileNotFoundError(
            f"Missing {SESSION_SUMMARY_PATH}. Run: python analysis/main_analysis.py"
        )

    by_session = pd.read_csv(SESSION_SUMMARY_PATH).sort_values("session")
    y_by_session = by_session.set_index("session")["accuracy"]

    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    fig.patch.set_alpha(0)
    ax.set_facecolor("#0b1111")
    ax.plot(
        by_session["session"],
        by_session["accuracy"],
        marker="o",
        linewidth=2.5,
        markersize=8,
        color="#8FD3FE",
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(colors="#cfcfcf")
    ax.xaxis.label.set_color("#d8d8d8")
    ax.yaxis.label.set_color("#d8d8d8")

    ax.set_xlabel("Session")
    ax.set_ylabel("Accuracy (successful transitions)")
    ax.set_xticks(by_session["session"])
    ax.set_ylim(0, 1.05)
    ax.axhline(y=0.75, linestyle="--", color="#8e8e8e", alpha=0.3)

    jump_session = 4 if 4 in y_by_session.index else int(by_session["session"].iloc[0])
    jump_y = float(y_by_session.loc[jump_session])
    ax.scatter(jump_session, jump_y, s=80, color="#6BFFA7", zorder=5)
    ax.annotate(
        "Largest improvement jump",
        xy=(jump_session, jump_y),
        xytext=(jump_session - 1.2, min(jump_y + 0.17, 0.98)),
        arrowprops=dict(arrowstyle="->", color="#6BFFA7"),
        color="#6BFFA7",
        fontsize=9,
    )

    last_session = int(by_session["session"].iloc[-1])
    last_y = float(by_session["accuracy"].iloc[-1])
    ax.scatter(last_session, last_y, s=80, color="#6BFFA7", zorder=5)
    ax.annotate(
        "Performance plateau",
        xy=(last_session, last_y),
        xytext=(last_session - 2.1, max(last_y - 0.22, 0.15)),
        arrowprops=dict(arrowstyle="->", color="#6BFFA7"),
        color="#6BFFA7",
        fontsize=9,
    )

    grid_color = (0, 1, 170 / 255, 0.08)
    ax.grid(True, linestyle="--", alpha=0.15, color=grid_color)
    fig.tight_layout()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PATH, dpi=150, transparent=True)
    plt.close(fig)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
