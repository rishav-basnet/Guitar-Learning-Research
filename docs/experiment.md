# Guitar skill acquisition experiment — design reference

This document is the **single source of truth** for experiment design and analysis intent.  
Block-level measurements live in **`data/main-data.csv`**; column definitions are in **`docs/data_dictionary.md`**.

---

## Purpose

Measure how **performance changes under increasing time constraints** when learning **repeated chord transitions between A major and E major** (same pair throughout).

---

## Hierarchy

| Level | Definition |
|--------|------------|
| **Session** | Completing the full practice video once (full run-through of the protocol for that day). |
| **Condition** | A combination of **mode** (time-constraint level) **and** **BPM**. |
| **Block** | **4** repeated trials under the **same** condition. |
| **Trial** | One **4-beat cycle** plus the **chord transition** into the next cycle (transition must be ready **before** the next beat 1). |

---

## Trial definition

Each trial:

- **Beats 1–4:** strumming pattern depends on **mode** (see below).
- **Transition:** A ↔ E must be **clean, on time**, with **rhythm maintained**, completed **before** the next beat 1.

**Success:** clean chord, on time, rhythm held.  
**Failure:** delay, buzzing, wrong fingering, or rhythm break.

---

## Modes (decreasing available transition time)

| Mode | Strumming | Time available to change |
|------|-----------|---------------------------|
| **1** (easiest) | Strum on beat 1 only | Beats 2–4 + gap before next cycle |
| **2** | Strums on beats 1 and 2 | Beats 3–4 + gap |
| **3** | Strums on beats 1, 2, 3 | Beat 4 + gap |
| **4** (hardest) | Strums on all four beats | Gap only (between beat 4 and next beat 1) |

---

## BPM levels

Each mode is tested at: **60, 70, 80, 90, 100, 110** BPM.

---

## Repetitions and blocks

- For each **(mode, BPM)** condition: perform **4 trials** → one **block**.
- **Recorded per block** (not per trial): number of **successful trials** out of 4.

**Derived per block:**

- `clean_ratio = successful_trials / 4` (equivalently `clean_cycles / 4` if using that column name).

**Intended row semantics (one row per block):**

- Identifiers: session, calendar day, mode, BPM  
- Counts: successful trials in the block (0–4)  
- Derived: `clean_ratio`

---

## Core performance metric

**Performance threshold (per session and mode):**

- **Highest BPM** at which `clean_ratio ≥ 0.75` for that block.

(Interpret with care: only six discrete BPMs are tested; ceiling effects at 110 BPM are possible.)

---

## Research focus

- Skill acquisition under **time pressure**
- **Learning curves** across sessions
- Relationship between **speed (BPM)** and **accuracy (`clean_ratio`)**
- Effect of **narrowing transition window** (mode 1 → 4) on performance

---

## Fixed constraints

- **Same chord pair:** A major ↔ E major only.
- **Same protocol** every session (document any unavoidable deviation when it happens).
- **Same scoring criteria** for success/failure throughout the study.

### Design cautions (for analysis)

- **Coarse blocks:** 4 trials ⇒ `clean_ratio` ∈ {0, 0.25, 0.5, 0.75, 1.0}; summarize trends over **many blocks/sessions**, not single rows in isolation.
- **Order effects:** if condition order is fixed within a session, consider logging order or counterbalancing.
- **N = 1 learner:** findings describe **this** learning trajectory; generalization requires more participants.

---

## Repository layout (intent)

| Path | Role |
|------|------|
| `data/main-data.csv` | Canonical block-level dataset (`docs/data_dictionary.md`) |
| `docs/experiment.md` | This file — protocol and definitions |
| `docs/data_dictionary.md` | Column specs and integrity notes for `main-data.csv` |
| `notebooks/` | EDA, visualization, modeling |
| `src/` | Optional: reusable load/feature/plot code |
