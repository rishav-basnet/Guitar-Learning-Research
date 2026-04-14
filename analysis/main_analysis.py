"""
Central analysis pipeline.

Computes all derived statistics once and exports them to /outputs.
"""

from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = REPO_ROOT / "outputs"
DATA_CANDIDATES = [
    REPO_ROOT / "data" / "main_data.csv",
    REPO_ROOT / "data" / "main-data.csv",
]
THRESHOLD = 0.75


def load_data() -> pd.DataFrame:
    for path in DATA_CANDIDATES:
        if path.exists():
            df = pd.read_csv(path)
            break
    else:
        raise FileNotFoundError(
            "Could not find data/main_data.csv or data/main-data.csv"
        )

    if "accuracy" not in df.columns:
        if "clean_ratio" in df.columns:
            df["accuracy"] = df["clean_ratio"]
        else:
            raise KeyError("Dataset requires either 'accuracy' or 'clean_ratio' column")

    return df


def run_analysis() -> dict[str, pd.DataFrame]:
    df = load_data()
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    # A) Session trend
    session_summary = (
        df.groupby("session", as_index=False)["accuracy"].mean().sort_values("session")
    )
    session_summary.to_csv(OUTPUTS_DIR / "session_summary.csv", index=False)

    # B) Mode + BPM accuracy
    bpm_mode = (
        df.groupby(["mode", "bpm"], as_index=False)["accuracy"]
        .mean()
        .sort_values(["mode", "bpm"])
    )
    bpm_mode.to_csv(OUTPUTS_DIR / "bpm_mode_accuracy.csv", index=False)

    # C) Threshold attainment (>= 0.75)
    threshold_df = df.copy()
    threshold_df["threshold_met"] = threshold_df["accuracy"] >= THRESHOLD
    threshold_summary = (
        threshold_df.groupby("mode", as_index=False)["threshold_met"]
        .mean()
        .sort_values("mode")
    )
    threshold_summary.to_csv(OUTPUTS_DIR / "threshold_summary.csv", index=False)

    # D) Highest BPM maintaining >= 0.75
    filtered = threshold_df[threshold_df["accuracy"] >= THRESHOLD]
    highest_bpm = (
        filtered.groupby(["session", "mode"], as_index=False)["bpm"]
        .max()
        .sort_values(["session", "mode"])
    )
    highest_bpm.to_csv(OUTPUTS_DIR / "highest_bpm_threshold.csv", index=False)

    # Validation checks
    assert (
        session_summary["accuracy"].iloc[-1] > session_summary["accuracy"].iloc[0]
    ), "Expected late-session accuracy to exceed early-session accuracy"
    assert (
        threshold_summary["threshold_met"].max() <= 1.0
    ), "threshold_met values should be within [0, 1]"

    return {
        "session_summary": session_summary,
        "bpm_mode": bpm_mode,
        "threshold_summary": threshold_summary,
        "highest_bpm": highest_bpm,
    }


def main() -> None:
    outputs = run_analysis()
    for name, frame in outputs.items():
        print(f"{name}: {len(frame)} rows")
    print(f"Wrote outputs to: {OUTPUTS_DIR}")


if __name__ == "__main__":
    main()
