# Pulsewatch beat-retention pre-confirmation: data and configuration

**Purpose:** record the data, settings and pass rule for a small test on raw watch files. The test decides whether the motion term in Equation 3.1 looks workable before committing to the full download of about 338 GB.

**Status:** settings and pass rule locked on 2 November 2026, before any result from this test was seen. Report any later change as made after seeing the results.

**Related files:**
- Earlier data check and draft proposal text: `methodology/Pulsewatch_Beat_Retention_Data_Check.md`
- Test script: `build/beat_retention_raw_test.py`
- Results, once run: `build/beat_retention_raw_results.json`

## Why this test is needed

The earlier check used labelled segments only. About half of the label rows are code −1, which the setup notes describe as mostly >5 s motion noise or unadjudicated, and those segments have no `.pt` files. That leaves high motion under-represented, so retention at high motion could look too good.

This test adds the raw watch files, so excluded segments can be scored too.

## Data

### Size

| Item | This test | Full release | Share |
|---|---:|---:|---:|
| Raw watch files (`01_Clinical_Trial`) | 10.35 GB, 8 tars | 109.32 GB, 101 tars | 9.5% |
| ECG R-peak files (`10_Filtered_ECG_Peaks`) | 9.63 GB, 10 patches, 1,130 hour files | 228.37 GB, 157 tars | 4.2% |
| Subjects with ECG | 8 | 71 | 11% |

The raw tars go in a new folder, `synapse_data\raw_watch_8subj`. The ECG files are already local, and no existing data is changed. The download is MD5-checked against the Drive.

### Subjects

The labelled counts come from `synapse_data\ecg\coverage_report.txt`.

| Subject | NSR | AF | PAC/PVC | Raw tar (GB) | Local ECG patches | On Drive, not local |
|---|---:|---:|---:|---:|---|---|
| 017 | 0 | 170 | 0 | 0.24 | B | A |
| 044 | 738 | 0 | 0 | 0.34 | A | |
| 055 | 80 | 0 | 0 | 0.01 | A | B |
| 075 | 196 | 13 | 2,110 | 1.43 | A | |
| 083 | 78 | 0 | 0 | 0.18 | A | |
| 098 | 82 | 0 | 0 | 3.14 | A, B | |
| 109 | 615 | 0 | 0 | 0.25 | A | |
| 110 | 12 | 1 | 261 | 4.74 | A, B | |
| **Total** | **1,801** | **184** | **2,371** | **10.35** (unrounded) | 10 patches | 2 patches |

That is 4,356 labelled segments, plus the excluded segments the raw tars add. The final segment and beat counts come from the run. Segments on patches `017A` and `055B` are skipped and counted, because those patches are not local.

### Segment groups

| Group | Label code | Use |
|---|---|---|
| `labelled` | 0, 1, 2 | Lag fit and scoring |
| `excluded` | Negative codes | Scoring only |
| `noise_3` | 3 | Scoring only, reported separately |
| `no_label` | No row in `03_Labels` | Scoring only, reported separately |

## Configuration

These settings are coded in `build/beat_retention_raw_test.py`.

### Signals

| Setting | Value |
|---|---|
| PPG source | Raw `*_ppg_*.txt` from the tars, 50 Hz, 1,500 samples |
| ACC source | Paired raw `*_accel_*.txt`, 50 Hz, 1,500 samples, magnitude |
| PPG filter | `signal_proc.bandpass_ppg`: 0.5–8 Hz, order 3, zero-phase |
| PPG peaks | `signal_proc.detect_ppg_peaks`: Elgendi-style, windows 0.111 s and 0.667 s, β 0.02, 0.30 s refractory |
| ECG beats | `Billal_ECG_peak_1_hr_this`, 250 Hz, from `build\ecg_fresh` and `synapse_data\ecg` |
| Alignment | Authors' per-segment tables in `Aligned_ECG_LinearInterp`, read with `pulsewatch.mat_table`, plus the session lag below |

Excluded segments have no `.pt` peaks, so one detector is used for every segment. As a bridge to the earlier test, held-out labelled segments are also scored with the authors' `new_PPG_peak_loc_Elgendi` peaks.

### Sessions and lag

| Setting | Value |
|---|---|
| Session definition | Shared filename prefix before `_ppg_` |
| Eligible session | At least 4 labelled segments after the segment rules |
| Sampling | Up to 300 random sessions per subject, seed 11 |
| Lag search | −3 to +3 s in 0.02 s steps, maximising beat match |
| Lag fit data | Alternating labelled segments only |
| Scored segments | The other labelled segments and all non-labelled segments in the session |

The lag never comes from a segment being scored, and never from a noisy one.

### Segment rules

A segment is skipped and counted if any of these apply:
- No alignment file, an unreadable one, or no alignment values in it
- `contain_empty` is set
- It crosses an hour boundary (`start_idx > end_idx`)
- Its ECG patch or hour file is not local
- Fewer than 5 ECG beats, or no paired accelerometer file
- The PPG or ACC file cannot be read or does not have 1,500 samples

### Scoring

| Setting | Value |
|---|---|
| Beat match | One-to-one: each PPG peak can match only one ECG beat, within ±100 ms of the lag-shifted beat, closest pairs first. The lag search itself uses nearest-peak matching for speed |
| Unmatched PPG peaks | Reported per motion bin |
| Interval retention (secondary) | Two consecutive ECG beats matched to two adjacent PPG peaks, with motion taken at the interval midpoint |
| Edge rule | Beats within 1 s of the PPG segment edges dropped |
| Motion measure | SD of ACC magnitude in a 2 s window centred on the beat |
| Motion units | m/s², checked on 40 files per subject: median level about 9.5–10.1, which is gravity |
| Motion bins (m/s²) | <0.05, 0.05–0.2, 0.2–0.5, 0.5–1, ≥1; quintile bins also reported as secondary |
| Skip counts | Written by reason and segment group to `build/beat_retention_raw_skipcounts.json` before any scoring |
| Control | The segment's own PPG and ACC, with ECG beats from a random segment in another session of the subject |
| Excess | Match minus control, in the same bin |
| Quality gate | A session passes if its held-out labelled match beats its control |
| Reporting | With and without the gate, pooled and per subject |
| Model | None fitted |

The control here differs from the earlier test, which refitted a lag on mismatched sessions. Control values are therefore not directly comparable between the two tests.

## What this test can and cannot show

**It can show:**
- Whether beat matching beats chance in excluded, high-motion segments
- Whether retention falls as motion rises within subjects
- Whether the larger download looks worthwhile

**It cannot show:**
- **A population estimate of π̂:** these 8 subjects were not randomly chosen, because the local ECG was fetched for AF subjects plus a few NSR subjects.
- **Rhythm-specific effects:** AF comes almost entirely from subject 017, and PAC/PVC mostly from subjects 075 and 110.
- **Garmin performance:** this is an offline detector on Samsung signals.
- **Whether a failed match is the PPG's fault:** motion can also corrupt the ECG, and the test cannot separate the two.
- **Validity in fully rejected sessions:** the lag needs at least 4 labelled segments, so sessions with fewer are left out, and these may be the noisiest ones.

## Proposed pass rule

Treat the test as a pass only if all three hold. "Enough beats" means at least 500 beats in a bin, from at least 3 subjects each contributing at least 50 beats.

1. **Above chance at high motion:** the lower bound of a 95% interval on excess over control, bootstrapped by subject, is above zero in every top bin with enough beats.
2. **Consistent within subjects:** at least two-thirds of subjects with 2 or more eligible bins show lower excess in their highest eligible bin than in their lowest.
3. **Detector comparable:** the absolute difference in match rate from the authors' `.pt` peaks, on the same held-out labelled beats, is at most 0.05 pooled and at most 0.10 in every subject.

### Details added to make the rule computable

These were not specified in the review and were fixed before the run:

- **Primary analysis:** sessions passing the quality gate, all scored segment groups together, one-to-one beat match. All-session results are reported as a sensitivity check.
- **Top bins:** 0.5–1 and ≥1 m/s². If neither has enough beats, criterion 1 is not met.
- **Eligible bin for criterion 2:** at least 50 beats from that subject. If fewer than 3 subjects have 2 or more eligible bins, criterion 2 is not met.
- **Criterion 3:** uses all sessions and beats at least 1 s from the segment edges, with each detector's own fitted lag. The per-subject limit applies to subjects with at least 50 such beats.
- **Bootstrap:** 2,000 resamples of subjects, seed 11. With 8 subjects this interval is coarse.

## What each outcome means

| Outcome | Proposal wording | Next step |
|---|---|---|
| **Pass** | Cite as feasibility evidence for estimating the motion term; no π̂ value | Download the remaining data when you're ready to fit the model |
| **Fail** | Motion term stays a stated assumption, with motion as a sensitivity analysis | The RO3 concurrent-ECG substudy provides the estimate |

Either way, the RO3 substudy stays, because it is the only direct estimate on Garmin.

This table is kept as written before the run. The test did not pass, and the decision actually taken departs from the Fail row: see "Contradiction and decision" below.

## Result (run 2 November 2026)

**Outcome: not passed under the locked rule.** Criteria 1 and 2 were met and criterion 3 was not. The rule was not changed after the run.

| Criterion | Result | Met? |
|---|---|---|
| 1. Above chance at high motion | Excess +0.273 (95% CI +0.180 to +0.336) at 0.5–1 m/s²; +0.197 (+0.122 to +0.254) at ≥1 m/s² | Yes |
| 2. Consistent within subjects | Excess lower in the highest bin for 8 of 8 subjects (7 of 8 across all sessions) | Yes |
| 3. Detector comparable | Project 0.850, authors' peaks 0.752, on 58,121 beats: pooled difference 0.097 (limit 0.05), largest subject difference 0.146 (limit 0.10) | **No** |

Sessions passing the gate, all scored segment groups:

| Motion (m/s²) | Beats | Match | Control | Excess | Intervals kept | Interval control | PPG peaks unmatched |
|---|---:|---:|---:|---:|---:|---:|---:|
| <0.05 | 55,684 | 0.849 | 0.207 | +0.642 | 0.766 | 0.076 | 0.096 |
| 0.05–0.2 | 15,812 | 0.725 | 0.224 | +0.501 | 0.600 | 0.078 | 0.179 |
| 0.2–0.5 | 5,342 | 0.516 | 0.202 | +0.315 | 0.335 | 0.055 | 0.347 |
| 0.5–1 | 6,074 | 0.477 | 0.204 | +0.273 | 0.292 | 0.056 | 0.392 |
| ≥1 | 4,468 | 0.407 | 0.210 | +0.197 | 0.220 | 0.054 | 0.472 |

**Reach of the test:**
- 472 of 9,145 sessions were scored (463 passed the gate).
- 319 of 12,532 excluded segments (2.5%) and 607 of 74,245 no-label segments (0.8%) were scored. Almost all the others were in sessions with too few labelled segments to fit a lag.
- The high-motion result therefore covers segments next to clean ones, not the noisiest sessions.

**Other points:**
- **Near-chance subjects:** S6 is near chance at every motion level (excess +0.02 at <0.05 m/s²), so its "fall" in criterion 2 is not meaningful. S3 reaches +0.005 at ≥1 m/s².
- **Unequal weight:** S4 contributes 29,324 of the 55,684 beats in the lowest bin and has a wide session-lag spread.
- **Detector difference:** this test cannot say which detector is more accurate. It shows only that absolute retention depends on the detector.
- **ECG quality:** motion may also corrupt the ECG, and this test does not separate the two causes.
- **Skipped patches:** no segment was skipped for non-local ECG. The eligible sessions all had their ECG on local patches.
- **Order of runs:** a smoke run on 2 subjects (S3 and S5) printed results before the full run. The rule was locked before that run and nothing changed afterwards.

Outputs: `build/beat_retention_raw_results.json`, `build/beat_retention_raw_skipcounts.json`.

## Contradiction and decision (2 November 2026)

This decision was made after seeing the results.

### The contradiction

| Source | What it says about a failed test |
|---|---|
| "What each outcome means" in this file | The motion term stays a stated assumption, with motion as a sensitivity analysis, and the RO3 substudy provides the estimate |
| The review of settings and pass rule | The data check alone is enough to rewrite Equation 3.1 and Section 3.4, and "either way the proposal stands" |

The two were written before the run and did not anticipate a partial result, where the motion criteria were met and the detector criterion was not.

### The decision

**The motion term stays in the plan, to be estimated on Pulsewatch during RO2. The test is not described as passed.** This is a looser reading of the failure than the Fail row, and the proposal must say the detector criterion was not met.

**Why:**
- Criteria 1 and 2 support a motion effect that can be measured.
- Criterion 3 questions the absolute level of retention, not whether the motion effect exists.
- The data needed for the estimate exists.

**Not changed:** the pass rule, the recorded outcome (not passed) and the original outcome table.

### What this adds to the RO2 plan

1. **Detector sensitivity analysis:** name the detector used for π̂ and report results with an alternative, because absolute retention differed by 0.097 between detectors.
2. **Lag method independent of labelled segments:** the current method reached only 2.5% of excluded segments and 0.8% of no-label segments.
3. **RO3 concurrent-ECG substudy stays:** it is the only direct estimate on Garmin.

No π̂ value is reported from this test.

### Sentence for the proposal

> A pre-specified check in 8 subjects found beat matching above chance at high motion and falling as motion rose, but absolute retention depended on the peak detector (0.850 vs 0.752), so the estimate will be reported with a detector sensitivity analysis.

### Still open

- The proposal has not been updated. Its path and approval for the rewrite are still needed.
- The lag method in item 2 has not been designed or tested, so it may not reach the noisiest sessions either.

## Decisions recorded

- Settings approved with four changes: one-to-one matching, a units check with quintile bins, interval-level retention, and skip counts recorded before scoring.
- Pass rule approved with tightened definitions.
- This test is enough for the proposal stage and is not strictly required. The full 338 GB download waits until after the defence, for fitting π̂ during RO2.
