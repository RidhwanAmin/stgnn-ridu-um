# Pulsewatch beat-retention pre-check: review of settings, pass rule and proposal-stage need

Reviewed 2 November 2026 against `Pulsewatch_Beat_Retention_Precheck_Config.md` (pasted). The test has not been run; no results are reviewed here.

**Short answer:** yes to all three questions, with four changes to the settings and tighter definitions for the pass rule. The config file also answers the earlier Pulsewatch question: the data has everything Equation 3.1 needs.

## What the config confirms about Pulsewatch

| Question (from `Check_Pulsewatch_Accelerometer_and_ECG_Beat_Timing.md`) | Answer | Evidence in the config |
|---|---|---|
| Q1. Accelerometer data | **Yes** | Raw `*_accel_*.txt`, 50 Hz, paired with each PPG segment |
| Q2. Beat-level ECG timing | **Yes, annotated** | R-peak files `Billal_ECG_peak_1_hr_this`, 250 Hz |
| Q3. Time alignment | **Yes** | Authors' per-segment tables `Aligned_ECG_LinearInterp`, plus a lag fitted per recording session |

So Pulsewatch can support the motion part of Equation 3.1, with the stated limit that it is a Samsung watch, not Garmin.

---

## 1. Settings: approve, with four changes

| # | Change | Why |
|---|---|---|
| a | **Match one-to-one:** each PPG peak can match only one ECG beat. Also report unmatched PPG peaks per motion bin | Motion makes the detector produce extra peaks. Without one-to-one matching, spurious peaks inflate "retention" at high motion, which is exactly the bias the test is meant to rule out. The control corrects for chance, but not for one peak counted twice |
| b | **Check the accelerometer units** (m/s² or g) on one file before running, and also report bins by motion quintile | The fixed bins (<0.05 to ≥1 m/s²) are wrong if the units are g, and the top bins may be empty. Quintile bins always have data |
| c | **Add interval-level retention as a secondary result:** both beats of an interval matched consecutively | Equation 3.1 concerns intervals in the series, not single beats. One missed beat removes two intervals |
| d | **Record the segment-skip counts by reason before scoring** | So the share of data lost to each skip rule is visible and fixed in advance |

**Already sound, no change:**
- Lag fitted only on held-out labelled segments, never on a scored or noisy one
- The 1-second edge rule
- A control drawn from another session of the same subject
- Reporting with and without the quality gate, pooled and per subject
- No model fitted
- A fixed seed

---

## 2. Pass rule thresholds: approve, with the definitions tightened

| Criterion | Proposed | Recommended wording |
|---|---|---|
| "Enough beats" | ≥500 beats per motion bin from ≥3 subjects | ≥500 beats per bin, from ≥3 subjects **each contributing ≥50 beats**, so one subject cannot dominate a bin |
| 1. Above chance at high motion | Excess over control above zero | **Lower bound of a 95% interval, bootstrapped by subject, above zero** in every top bin with enough beats. Beats within a subject are not independent, so a point estimate above zero is not enough |
| 2. Consistent within subjects | "Most subjects" show excess falling as motion rises | **At least two-thirds of subjects** with ≥2 eligible bins show lower excess in their highest eligible bin than in their lowest |
| 3. Detector comparable | Within 0.05 of the authors' `.pt` peaks | **Absolute difference in match rate ≤0.05, pooled, on the same held-out labelled beats, and ≤0.10 in every subject** |

Write these into the config file and date it before any result is seen. Report any later change as made after seeing the results.

---

## 3. Is this test alone enough for the proposal stage? Yes, and it is not strictly required

- **The proposal only has to show the motion term can be estimated.** The data check already shows that: accelerometer data, R-peaks and alignment all exist. That alone is enough to rewrite Equation 3.1 and Section 3.4 now.
- **The test adds evidence that it works:** matching beats chance at high motion, and retention falls as motion rises.
  - **If it passes before submission:** one sentence in the proposal, cited as feasibility evidence, with no π̂ value.
  - **If it is not run in time:** describe it as planned. Either way the proposal stands.
- **Do not download the full 338 GB before the defence.** That is for fitting π̂ during RO2, after the defence.
- **The RO3 concurrent-ECG substudy stays** whatever the result, because it is the only direct estimate on Garmin.

**Word-count constraint:** the main text is at about 6,980 of 7,000 words, so a test result can get one sentence at most.

---

## Next step on the proposal (awaiting approval)

Rewrite Equation 3.1 so retention depends on:
- **beat class**, from RO1 on Icentia11k (PAC 39% against normal 91% at the 20% filter), and
- **motion**, from Pulsewatch (ECG R-peaks matched to PPG peaks against accelerometer motion),

with no time-of-day term, because no dataset with true beats also has clock time and motion together. Then update the retention sentence in Section 3.4, and trim about 100 words from Chapter 2 to stay under 7,000.
