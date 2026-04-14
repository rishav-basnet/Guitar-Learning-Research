"""
Mean clean_ratio by session (learning progression), line chart.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = REPO_ROOT / "data" / "main-data.csv"
OUT_DIR = REPO_ROOT / "analysis" / "figures"
OUT_PATH = OUT_DIR / "learning_progression_clean_ratio.png"


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    by_session = df.groupby("session", as_index=False)["clean_ratio"].mean()

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(
        by_session["session"],
        by_session["clean_ratio"],
        marker="o",
        linewidth=2,
        markersize=8,
    )
    ax.set_xlabel("Session")
    ax.set_ylabel("Average clean_ratio")
    ax.set_title("Learning progression over sessions")
    ax.set_xticks(by_session["session"])
    ax.set_ylim(0, 1.05)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PATH, dpi=150)
    plt.close(fig)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
