# Guitar Skill Acquisition Study

## Overview

This project studies how chord transition performance (A ↔ E) changes under time pressure.

BPM controls speed, and mode controls how much time is available to switch chords. Performance is measured using clean_ratio (successful_trials / 4).

---

## Motivation

- I was learning guitar and wanted to know whether progress was actually happening, and how fast it showed up.
- Day-to-day practice felt inconsistent, so I wanted a fixed structure to measure performance instead of relying on intuition.
- Turning practice into a small experiment made improvement something I could observe, not just assume.

---

## Experiment Design

- Protocol video (same routine each session):  
  https://www.youtube.com/watch?v=WtXb90taPOY

- Each session follows the same grid:
  - 4 modes (difficulty levels)
  - 6 BPM levels: 60, 70, 80, 90, 100, 110
  - 4 trials per (mode, BPM)

- Mode (1–4): more strums per cycle → less time to switch chords  
- BPM: controls tempo and time pressure  

### Practice Protocol

Each session follows a timed strumming exercise:

- A 4-beat cycle is repeated at each BPM.
- The player alternates between A and E chords.

Modes define how much time is available to switch:

- Mode 1: strum once, switch during remaining beats  
- Mode 2: strum twice, switch in shorter window  
- Mode 3: strum three times, very limited switching time  
- Mode 4: strum continuously, minimal gap to switch  

For each (mode, BPM):
- 4 trials are performed
- Each trial is marked successful or not based on a clean, on-time chord change

Each session follows the exact same structure, allowing direct comparison across sessions.

---

## Dataset

Each row represents one block: a single (session, mode, BPM) combination.

- successful_trials: number of clean transitions (0–4)  
- clean_ratio: successful_trials / 4  

The dataset is stored in `data/main-data.csv` and is fully structured with no missing conditions.

---

## Analysis

- Session trend: average clean_ratio across all conditions per session  
- BPM vs performance: how tempo and difficulty affect performance  
- Threshold (≥ 0.75): highest BPM where performance remains mostly clean  

---

## Reproducibility

All derived tables used by figures are exported to `outputs/`.

- Regenerate analysis outputs:
  - `python analysis/main_analysis.py`
- Verify exported outputs are consistent with recomputation:
  - `python analysis/verify_consistency.py`

Figure scripts read from `outputs/*.csv` so calculations are centralized and reproducible.

---

## Key Insights

- Performance shows an overall upward trend across sessions  
- Learning is not linear, with plateaus and short regressions  
- Higher BPM generally reduces performance, especially in harder modes  
- Modes 3–4 consistently perform worse than modes 1–2  
- Performance varies noticeably across sessions, even under the same conditions  

---

## Reflection

Practice felt inconsistent, and the data confirmed that. Progress was visible overall, but individual sessions often moved in unexpected directions.

Recording performance made it easier to see patterns that would otherwise be missed or misremembered.

---

## Structure

- data/ — dataset  
- analysis/ — scripts and plots  
- docs/ — experiment details and data dictionary  

---

## Tools

Python, pandas, matplotlib

---

## Run the analysis

From the repository root, with a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python analysis/01_load_and_verify.py
python analysis/main_analysis.py
python analysis/verify_consistency.py
python analysis/02_learning_progression.py
python analysis/03_clean_ratio_vs_bpm.py
python analysis/04_max_bpm_threshold.py
```

Figures are written to `analysis/figures/`. The integrity script checks that `clean_ratio` matches `successful_trials / 4` on every row.

---

## Notes

This is a small, single-learner study. It is intended to explore patterns in practice rather than make general conclusions.