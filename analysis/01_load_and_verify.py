"""
Step 1: Load main-data.csv, inspect, and verify integrity.

Design note: the CSV uses `successful_trials` (0–4) for what you called clean_cycles;
`clean_ratio` is successful_trials / 4. Modes are integers 1–4 (see docs/data_dictionary.md).
"""

from pathlib import Path

import pandas as pd

# Paths (run from repo root: python analysis/01_load_and_verify.py)
REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = REPO_ROOT / "data" / "main-data.csv"

TOTAL_CYCLES = 4
EXPECTED_BPMS = {60, 70, 80, 90, 100, 110}
EXPECTED_MODES = {1, 2, 3, 4}
ROWS_PER_SESSION = len(EXPECTED_MODES) * len(EXPECTED_BPMS)  # 24


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def basic_inspection(df: pd.DataFrame) -> None:
    print("=== Shape ===")
    print(df.shape)
    print()

    print("=== dtypes ===")
    print(df.dtypes)
    print()

    print("=== head() ===")
    print(df.head(12).to_string())
    print()

    print("=== summary (numeric) ===")
    print(df.describe(include="all").T.to_string())
    print()

    # Optional quick check: spot weird clustering or unrealistic spikes
    print("=== successful_trials value_counts() (quick check) ===")
    if "successful_trials" in df.columns:
        print(df["successful_trials"].value_counts().sort_index().to_string())
    print()

    print("=== value counts: session, mode, bpm ===")
    print("sessions:", sorted(int(x) for x in df["session"].unique()))
    print("modes:", sorted(int(x) for x in df["mode"].unique()))
    print("bpms:", sorted(int(x) for x in df["bpm"].unique()))
    print()


def verify_integrity(df: pd.DataFrame) -> list[str]:
    """Return list of failure messages; empty means all checks passed."""
    errors: list[str] = []

    required = ["session", "day", "mode", "bpm", "successful_trials", "clean_ratio"]
    missing_cols = [c for c in required if c not in df.columns]
    if missing_cols:
        errors.append(f"Missing columns: {missing_cols}")
        return errors

    if df.isna().any().any():
        na_cols = df.columns[df.isna().any()].tolist()
        errors.append(f"Missing values in columns: {na_cols}")

    ratio_ok = (df["clean_ratio"] - (df["successful_trials"] / TOTAL_CYCLES)).abs() < 1e-9
    if not ratio_ok.all():
        bad = df.loc[~ratio_ok, required]
        errors.append(
            "clean_ratio != successful_trials / 4 for some rows:\n"
            + bad.to_string()
        )

    trials_range = df["successful_trials"].between(0, TOTAL_CYCLES)
    if not trials_range.all():
        errors.append(
            "successful_trials outside [0, 4]:\n"
            + df.loc[~trials_range, required].to_string()
        )

    unexpected_bpm = ~df["bpm"].isin(EXPECTED_BPMS)
    if unexpected_bpm.any():
        errors.append("Unexpected bpm values:\n" + df.loc[unexpected_bpm, "bpm"].unique().tolist().__repr__())

    unexpected_mode = ~df["mode"].isin(EXPECTED_MODES)
    if unexpected_mode.any():
        errors.append("Unexpected mode values:\n" + df.loc[unexpected_mode, "mode"].unique().tolist().__repr__())

    counts = df.groupby("session").size()
    bad_counts = counts[counts != ROWS_PER_SESSION]
    if not bad_counts.empty:
        errors.append(
            "Sessions without exactly 24 rows (mode × BPM grid):\n"
            + bad_counts.to_string()
        )

    return errors


def main() -> None:
    df = load_data()
    basic_inspection(df)

    print("=== Integrity checks ===")
    errs = verify_integrity(df)
    if errs:
        print("FAILED:")
        for e in errs:
            print(e)
            print()
        raise SystemExit(1)
    print("All integrity checks passed.")
    print()

    print(
        """=== Suggested next steps (no modeling yet) ===

Visualization
- Line plots: clean_ratio vs bpm, faceted by mode, colored or faceted by session (learning).
- Session index on x-axis: mean clean_ratio per session, overall and split by mode.
- Heatmaps: rows = session, cols = (mode, bpm) or session × bpm within one mode.

Feature engineering (keep interpretable)
- block_pass: 1 if clean_ratio >= 0.75 (see data_dictionary).
- session-centered metrics: cumulative mean clean_ratio, or change from session 1.
- Optional: time pressure index as ordered bpm (60=1 … 110=6) for monotonic trend plots.

Analysis
- Compare distributions of clean_ratio by mode and by bpm (e.g. side-by-side box/strip plots).
- Within-subject trends: same participant trajectory over session (you have one series per design—describe as n=7 sessions).
- Pre-register simple questions: e.g. "does later session shift the bpm–performance curve?"
- Report non-monotonicity explicitly: count reversals, show raw points—not only smooth fits.

"""
    )


if __name__ == "__main__":
    main()
