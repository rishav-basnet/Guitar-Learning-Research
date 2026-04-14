"""
Verify that exported CSV outputs match fresh recomputation.
"""

from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal

from main_analysis import OUTPUTS_DIR, run_analysis


def _read_output(name: str) -> pd.DataFrame:
    path = OUTPUTS_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Missing output file: {path}")
    return pd.read_csv(path)


def _normalize(df: pd.DataFrame, sort_cols: list[str]) -> pd.DataFrame:
    normalized = df.sort_values(sort_cols).reset_index(drop=True).copy()
    return normalized


def main() -> None:
    recomputed = run_analysis()

    expected_pairs = [
        ("session_summary.csv", "session_summary", ["session"]),
        ("bpm_mode_accuracy.csv", "bpm_mode", ["mode", "bpm"]),
        ("threshold_summary.csv", "threshold_summary", ["mode"]),
        ("highest_bpm_threshold.csv", "highest_bpm", ["session", "mode"]),
    ]

    for filename, key, sort_cols in expected_pairs:
        actual = _read_output(filename)
        expected = recomputed[key]
        actual_norm = _normalize(actual, sort_cols)
        expected_norm = _normalize(expected, sort_cols)
        assert_frame_equal(actual_norm, expected_norm, check_dtype=False, atol=1e-12)
        print(f"OK: {filename}")

    print("All outputs are consistent with recomputed analysis.")


if __name__ == "__main__":
    main()
