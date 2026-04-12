# Data Dictionary

File: `data/main-data.csv`

Each row represents one block:
a single combination of session, mode, and BPM.

---

## Columns

### session
- Integer
- Identifies the practice session
- In this dataset, sessions increase sequentially over time

---

### day
- Integer
- Day index of practice
- Matches session in this dataset (1 session per day)

---

### mode
- Integer (1–4)
- Represents difficulty level

Higher mode → less time available to switch chords  
Lower mode → more time available  

---

### bpm
- Integer (60–110)
- Speed of the metronome

Higher BPM → faster tempo → less time per beat  

---

### successful_trials
- Integer (0–4)
- Number of clean chord transitions in that block

Each block contains exactly 4 trials

---

### clean_ratio
- Float (0.0 – 1.0)
- Computed as:

  successful_trials / 4

Represents consistency:
- 1.0 → all trials successful  
- 0.0 → no successful trials  

Values increase in steps of 0.25

---

## Notes

- The dataset is fully structured (no missing conditions)
- Each session contains the same 24 blocks (4 modes × 6 BPMs)
- This allows direct comparison across sessions