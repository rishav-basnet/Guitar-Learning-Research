# Data dictionary — `data/main-data.csv`

Canonical **block-level** dataset for the A ↔ E chord transition experiment. One row = one **block** (4 trials at a given session, day, mode, and BPM).

See **`docs/experiment.md`** for protocol definitions (session, condition, block, trial, modes, BPM grid).

---

## File

| Property | Value |
|----------|--------|
| Path | `data/main-data.csv` |
| Rows (current) | 168 (excluding header) |
| Sessions | 7 (IDs 1–7) |
| Rows per session | 24 (= 4 modes × 6 BPMs) |

---

## Columns

| Column | Type | Allowed values | Description |
|--------|------|----------------|-------------|
| `session` | int | ≥ 1 | Session index (full practice video run-through). |
| `day` | int | ≥ 1 | Day index aligned with session in this file (1:1 with `session` for current data). |
| `mode` | int | 1–4 | Time-constraint level (strumming density); 4 = hardest. |
| `bpm` | int | 60, 70, 80, 90, 100, 110 | Metronome tempo for that condition. |
| `successful_trials` | int | 0–4 | Count of successful trials in the block (out of 4). |
| `clean_ratio` | float | 0, 0.25, 0.5, 0.75, 1.0 | `successful_trials / 4`. |

---

## Derived metrics (compute in analysis, not stored)

- **`block_pass`:** 1 if `clean_ratio >= 0.75`, else 0.
- **Performance threshold (per session, per mode):** maximum `bpm` such that `clean_ratio >= 0.75` (if none, undefined or 0 per convention—document choice in notebooks).

---

## Integrity checks (automated)

These hold for the current file:

- `clean_ratio == successful_trials / 4` for every row.
- `successful_trials` in `[0, 4]`.
- `bpm` in `{60, 70, 80, 90, 100, 110}`.
- `mode` in `{1, 2, 3, 4}`.
- Exactly **24** rows per `session`.

---

## Other files in `data/`

| File | Note |
|------|------|
| `practice_log.csv` | Early placeholder with a different schema; **not** the analysis dataset. Use **`main-data.csv`** for all analysis unless migrated intentionally. |

When adding new exports (e.g. raw notes, session timestamps), prefer `data/raw/` vs `data/processed/` and extend this dictionary.
