# Track 1 implementation runbook: S2 to the end of S3

Prepared 11 November 2026. Companion to `drafts/Implementation_Plan_Icentia11k_and_Datasets.md` (the overview) and to the initial code in `analysis/` (see `analysis/README.md`). The proposal docx remains the source of truth and the slides are unchanged. Anything the proposal does not fix is marked **[Proposed]** and is for agreement with the supervisors.

**Scope.** Track 1 only: Icentia11k, Pulsewatch, RO1 in full, the training simulator and the start of RO2, up to the end of S3. The last section lists what Track 1 must hand to Track 2 (device, ethics, Garmin pipeline) before the S4 go/no-go gate.

**End state at the end of S3:**
1. RO1 complete: RQ1.1, RQ1.2, RQ1.3 and H1. The RO1 paper is submitted (M3), and so is the conference paper on the preliminary results.
2. π̂(m) is estimated on Pulsewatch with a detector sensitivity analysis, together with the motion, timing-offset and wear-coverage profiles.
3. The training simulator is calibrated and validated.
4. RO2 runs end to end on P2 with an interim model and the first baselines. It is not frozen; the freeze (M4) comes in S4.
5. The Track 2 handover pack is complete.

---

## 1. Calendar

Table 6.1 defines S1 as Semester 2, 2025/2026, so **S2 is Semester 1, 2026/2027** and **S3 is Semester 2, 2026/2027**. The week dates below are planning dates. Check them against the UM academic calendar and move the week numbers if the semester boundaries differ.

| Weeks | Dates (Monday) | Period |
|---|---|---|
| W1 to W15 | 16 Nov 2026 to 22 Feb 2027 | Rest of S2 |
| W16 to W41 | 1 Mar 2027 to 23 Aug 2027 | S3 (including the mid-year break) |
| W42 to W46 | 30 Aug 2027 to 27 Sep 2027 | Buffer before S4 and the go/no-go gate |

Key dates: W4 = 7 Dec 2026; W8 = 4 Jan 2027; W12 = 1 Feb 2027; W20 = 29 Mar 2027; W24 = 26 Apr 2027; W28 = 24 May 2027; W32 = 21 Jun 2027; W36 = 19 Jul 2027; W40 = 16 Aug 2027.

The proposal defence date is not fixed here. Panel corrections take priority in the two weeks after it and push the weeks below back by up to two weeks.

---

## 2. Week-by-week schedule

| Weeks | Icentia11k and RO1 | Pulsewatch | Simulator and RO2 | Writing | Gate |
|---|---|---|---|---|---|
| W1 to W2 | T0 setup; T1 P0 import, P3 drawn; T2 P0 download and tables | T8a permission request; storage | | | P3 sealed |
| W3 to W4 | T2 reproduction gate; T3 D1 power note | T8a download starts | | | **G1** Tables 4.2 and 4.3 reproduced |
| W5 to W8 | T1 P1, P2 drawn; T4 download and tables for P1, P2 | T8a download | | | **G2** all sets locked |
| W6 to W10 | T5 RQ1.2 curves (P0, P1), adaptive filter | T8b lag method design | | | |
| W8 to W11 | T6 H1 note, H1 run, sensitivity; T7 RQ1.3 | T8b lag method | | | **G3** H1 result |
| W12 to W15 | RO1 tables final | T8b lag validated; T8c π̂(m) starts | | T9 outlines (both papers) | **G4** lag method passes |
| W16 to W22 | | T8c π̂(m) and detector sensitivity; T8d profiles | T10 simulator calibration starts | T9 conference paper drafted | **G5** π̂(m) candidate |
| W16 to W26 | | T8e RQ1.1 models | T10 simulator validated (W26) | | **G6** RQ1.1 result; simulator validated |
| W24 to W34 | | | T11 RO2 data loader, graphs, model, training loop | T9 RO1 paper drafted (W20 to W28), supervisor review (W28 to W32) | |
| W30 to W38 | | | T11 baselines and first ST-GNN runs | **M3** RO1 paper submitted (target W34) | |
| W36 to W41 | | | T11 interim model end to end; T12 handover pack | | **G7** handover pack complete |
| W42 to W46 | Buffer | Buffer | Buffer; GPU queue for S4 ablations | | Ready for S4 |

The critical path runs: **Pulsewatch permission → full download → lag method → π̂(m) → simulator → RO2 training.** RO1 on Icentia11k is not on it. If the Pulsewatch permission has not arrived by W6, raise it with the supervisors at once (risk table, section 3.9).

---

## 3. Conventions for every work package

- **Code:** `analysis/`, Python 3.10 or later, run as `pip install -e ".[dev,adaptive]"`. Data live outside git under `ESVEA_DATA` on university storage (PDPA 2010).
- **Configs:** `analysis/configs/default.yaml`. A changed setting needs a dated note in `analysis/notes/`.
- **Pre-analysis notes:** every confirmatory test (D1, H1, π̂(m) primary analysis, H2 later) has a note committed before the data are opened. The H1 script refuses to run without its note.
- **Seeds:** models use 11 to 15; bootstraps use 2026, with 2,000 resamples by patient or subject.
- **Patient-set guard:** `esvea.sets.Guard`. Each analysis may read only its allowed sets, and P3 stays closed until `notes/M4_freeze_record.md` exists.
- **Done means:** the "done when" test passes, results regenerate from code, and the commit is pushed.

---

## 4. Work packages

### T0. Setup (W1 to W2)

| Item | Steps | Done when |
|---|---|---|
| Environment | Clone the repository; `pip install -e ".[dev,adaptive]"`; `pytest -q` and `pytest -q -m network` | 25 tests pass; the network test reads p00000_s00 |
| Storage | Request university storage. Allow about 10 GB for Icentia11k labels and tables, and **about 340 GB for Pulsewatch** (raw watch 109 GB plus ECG peaks 228 GB) | `ESVEA_DATA` set; quota confirmed |
| GPU (D7) | Ask for a faculty GPU server or cloud allocation, needed from W24 | Written allocation |
| Pulsewatch permission | Email the Pulsewatch data custodians through Synapse (syn23565056), asking for written confirmation of permitted use for a PhD thesis and publications | Written reply filed in `analysis/notes/` |
| Existing code | Copy into the repository, read-only under `analysis/legacy/`, the preliminary RO1 script and P0 list, and the Pulsewatch pre-check script (`beat_retention_raw_test.py`, `signal_proc.py`). They are the reference for T2 and T8 | Files committed with their origin noted |

### T1. Lock the patient sets (W1 to W5)

| Step | Command | Done when |
|---|---|---|
| 1. Import P0 | Write `analysis/splits/P0.txt` from the preliminary list, with the seed in the header; then `python -c "from esvea import sets; sets._update_sums(sets.SPLITS)"` | 300 ids; hash committed |
| 2. Draw P3 (W1) | `python scripts/s01_draw_sets.py P3 --n 300 --seed <new seed>` | Committed. P3 is never downloaded before M4 (`s02_download.py` refuses it) |
| 3. Draw P1 (W4, after T3) | `python scripts/s01_draw_sets.py P1 --n <size from D1 note> --seed <seed>` | Committed after the D1 note |
| 4. Draw P2 (W5) | `python scripts/s01_draw_sets.py P2 --seed <seed>` | `P2_train`, `P2_val`, `P2_test` committed (70/15/15 by patient, D2 [Proposed]) |
| Check | `sets.verify()` runs inside every guard | No overlap; no hash change |

### T2. Stage A pipeline on P0 and the reproduction gate (W1 to W4)

**Steps:**
1. Run `python scripts/s02_download.py P0`. This fetches headers and beat annotations only (about 0.2 GB) and writes SHA-256 lines to `raw/MANIFEST.sha256`.
2. Run `python scripts/s03_build_tables.py P0`. It writes per-patient Parquet beat and interval tables and `summary.parquet`. A smoke run on p00001 took 17 s for 50 segments and found 58.3 h, 54 PACs and 26% Q beats.
3. Run `python scripts/s04_reproduce_p0.py`. It compares against Tables 4.2 and 4.3: 298 patients; removal at 20% of 60.9% (PAC coupling), 54.5% (pause after PAC), 70.0% (PVC coupling) and 8.8% (normal); 78.5% vs 60.0% PAC removal by Binici ESVEA status; 67, 54 and 66 ESVEA-positive; median 57.5 h and 1.35 PACs/h.

**If it does not reproduce**, check these in order, against `analysis/legacy/`:
- the filter warm-up rule (`ro1/filters.percent_deviation`);
- whether the filter runs per segment;
- the category definitions (an S beat followed by S counts as PAC coupling);
- Q exclusion and the 0.2 to 3.0 s range;
- how "analysed hours" is defined;
- which two of the 300 patients were dropped, and why.

Fix the code, never the targets.

**Done when (G1):** `s04_reproduce_p0.py` exits 0 and `results/p0_reproduction.json` is committed.

### T3. D1: the size of P1 (W3 to W4)

- Run `python scripts/s05_power_d1.py`. It fits the H1 model on P0, simulates candidate P1 sizes of 50 to 300, and writes a dated note.
- **[Proposed] rule:** the smallest size with at least 90% power at **half** the P0 effect. The P0 estimate is optimistic because P0 also generated the hypothesis.
- **Done when:** the note `notes/<date>_D1_P1_size.md` is committed before P1 is drawn.

### T4. Download and tables for P1 and P2 (W5 to W8)

- Commands: `python scripts/s02_download.py P1 P2_train P2_val P2_test`, then `python scripts/s03_build_tables.py` with the same sets.
- **Time:** about 17 s per patient for about 10,400 patients, roughly 49 h serial. Split the set lists into 8 parallel jobs (about 6 h), keeping requests polite to PhysioNet.
- **Size:** about 6 GB of labels plus about 10 to 20 GB of tables.
- **Done when (G2):** the manifest is complete, `summary.parquet` has every P0 to P2 patient, and a re-run reports no checksum change.

### T5. RQ1.2 retention curves (W6 to W12)

**Steps:**
1. Run `python scripts/s06_ro1_curves.py P0 P1 --adaptive`. This covers thresholds 10 to 30% in 1-point steps, AF stretches included and excluded (D3), and the Lipponen and Tarvainen adaptive filter.
2. Burden bands **[Proposed]**: <1, 1 to 10, 10 to 30 and ≥30 PACs/h, plus quintiles. Pooled removal per band uses patient-bootstrap 95% CIs (`retention.patient_bootstrap_ci`).
3. Check the adaptive filter on synthetic series (`tests/test_filters.py`). Then confirm on 5 real P0 patients that NeuroKit2's index convention flags the interval ending at the flagged beat.

**Outputs:**
- Retention curves by class (PAC coupling, pause after PAC, PVC coupling, normal) × threshold × band.
- Adaptive-filter removal by class.

These feed RO2 (the flag threshold in the simulator) and RO4a (the severity sweep).

**Done when:** figures and tables regenerate from `results/ro1_sweep_*.parquet`, and the 20% P0 row equals Table 4.2.

### T6. H1 on P1 (W8 to W11)

1. Copy `notes/templates/H1_preanalysis_template.md` to `notes/<date>_H1_preanalysis.md`, fill it in and commit it.
2. Run `python scripts/s07_h1.py`. The model is a binomial GLMM on per-patient retained and tallied PAC coupling intervals, with log PACs/h as predictor and a patient random intercept, fitted by maximum likelihood with adaptive Gauss-Hermite quadrature. It reports b, its 95% CI, the odds ratio per doubling and the p-value. The 20% threshold is primary; 10, 15, 25 and 30% and AF-excluded fits are sensitivity analyses.
3. Run the model check on P1: compare observed and fitted retention by burden decile. As a robustness check **[Proposed]**, refit with a quadratic term in x.

**Done when (G3):** `results/h1_P1.json` is committed, and the result is written into the RO1 paper's results section as supported or not supported.

The fit was checked on simulated data: it recovers b = 0.25 (estimate 0.251, 95% CI 0.203 to 0.299) and σ = 0.6 (estimate 0.61).

### T7. RQ1.3 origin loss (W10 to W11)

- Run `python scripts/s08_rq13.py`. It reports, per patient, premature (S+V) and PAC-only (S) daily-equivalent counts, the ESVEA call from each, Bland–Altman bias and limits on log(1 + count) by burden band, and the number reclassified.
- **Done when:** the table and Bland–Altman figure are committed. The RO1 paper reports how many P1 patients change ESVEA class if PVCs are counted as PACs.

### T8. Pulsewatch (W1 to W26)

**T8a. Permission and download (W1 to W10).** After written permission, download the remaining raw watch tars (101 in all) and the ECG R-peak tars (157). MD5-check each against Synapse. The 8 pre-check subjects are already local.
- **Done when:** all 71 subjects with ECG are local and checked, and skip counts by reason are recorded before any scoring.

**T8b. Lag method that does not need labelled segments (W6 to W15).** The current method reached only 2.5% of excluded and 0.8% of no-label segments.
- **[Proposed] method:** for each session, search the lag (−3 to +3 s in 0.02 s steps) on PPG peaks and ECG beats from **all** segments in the session, using only beats at low motion (<0.05 m/s²) to fit the lag. This uses `pulsewatch.matching.best_lag` with its mean-distance tie-break; check the tie-break against the pre-check script.
- **Validation:** on sessions where the labelled-segment lag also exists, compare the two.
- **[Proposed] pass rule, fixed in a note before running:** agreement within ±0.04 s in at least 90% of those sessions, and coverage of at least 50% of excluded segments.
- **Done when (G4):** the note and the result are committed.

**T8c. π̂(m) with the detector sensitivity analysis (W12 to W22).** Matching is one-to-one within ±100 ms, after the lag. Beats within 1 s of segment edges are dropped. Motion is the SD of accelerometer magnitude in a 2 s window, in m/s² (units checked against gravity). The bins are those of the pre-check.
- **Primary detector:** Elgendi et al. (2013) on all segments. **Alternative:** the authors' released peaks.
- **Model [Proposed]:** logistic regression of "beat reported" on a natural spline of motion (3 knots), with a subject random intercept. Fit on 70% of subjects and check calibration on the other 30%, outside peak-free stretches (the Garmin gap analogue).
- **Report:** the curve, the per-bin table, and the curve from each detector, with the difference.
- **Done when (G5):** a π̂(m) candidate is saved as a versioned file in `results/pi_hat/`, with both detectors. It is not frozen until M4.

**T8d. Profiles for the simulator and RO4a (W18 to W22)** (`src/esvea/pulsewatch/`):
- **Motion episodes:** distribution of level and duration above 0.2 m/s², for D4.
- **Timing offsets:** PPG peak minus lag-corrected R-peak, for jitter.
- **Peak-free stretches:** duration and relation to motion, for the gap model.
- **Wear coverage per 6-hour block:** from file-name times, local US Eastern (Check E2). This is the Track 2 fallback coverage model.
- **Done when:** each profile is saved as a table plus a fitted parametric summary.

**T8e. RQ1.1 morphology loss (W16 to W26).** Pulsewatch 30-s windows with labels NSR, AF and PAC/PVC (merged), on identical windows for both models.
- **[Proposed] waveform model:** a 1D CNN on the 50 Hz PPG (1,500 samples).
- **[Proposed] interval model:** the same capacity class on the interval sequence from detected peaks (a GRU or 1D CNN on RR).
- **Splits:** subject-wise 5-fold cross-validation with identical folds for both models, and five seeds.
- **Metrics:** macro F1, PAC/PVC-class F1 and AUROC, compared by DeLong's test and a paired subject bootstrap.
- **Done when (G6):** the RQ1.1 table and a note on what the difference means are committed.

### T9. Papers (W12 to W34)

| Paper | Content | Steps | Target |
|---|---|---|---|
| Conference paper on the preliminary results (section 6) | Pilot (Table 4.1) and filtering loss on P0 (Table 4.2) | Outline W12; draft W16 to W20; supervisors W20 to W22 | Venue and deadline agreed with the supervisors **[Proposed]**; check the call before W12 |
| RO1 journal paper (M3) | RQ1.1, RQ1.2, RQ1.3, H1 | Outline W12; results frozen W26; draft W20 to W28; supervisors W28 to W32; submit by W34 | Indexed journal agreed with the supervisors (UM requires one indexed acceptance before graduation) |

### T10. Training simulator: calibrate and validate (W16 to W26)

The code is in `analysis/src/esvea/simulate/stream.py`. All its parameters are placeholders now.

| Parameter | Calibrated from |
|---|---|
| Flag deviation threshold | RO1 (T5): the threshold whose removal pattern matches Garmin's "abnormally short or long" rule; 20% primary, swept 10 to 30% |
| Motion episodes | T8d (D4) |
| Silent loss | π̂(m) candidate (T8c) |
| Gap rate and durations | T8d peak-free stretches |
| Jitter | T8d timing offsets; off in training by default |

**[Proposed] validation checks, fixed in a note first:**
1. The flagged fraction rises with motion, as on Pulsewatch.
2. PAC beats are flagged more often than normal beats at low motion.
3. The PAC accounting holds: reported = true − silent − in gap (the unit test).
4. `simulate/` does not import `degrade/` (the unit test).

The comparison with real Garmin flags and gaps waits for device verification (Track 2, meeting point 2).

**Done when (G6):** the validation report is committed and the configuration is versioned.

### T11. RO2 build start (W24 to W41)

| Step | Weeks | Content | Done when |
|---|---|---|---|
| Data loader | W24 to W28 | P2 pseudo-days (`pseudodays.assign`); simulated reported-beat streams in the `schema.py` format; windows of N beats (D5 [Proposed] start: N = 64, k = 8, L = 2) | Loader yields batches for one patient in under 1 s; a unit test on shapes passes |
| Graphs and model | W26 to W32 | Banded chain graph and k-NN similarity graph per window; gated local block; attention readout; interval block over windows; event and rate heads (PyTorch Geometric) | Overfits one batch to near-zero loss |
| Estimator outside the network | W28 to W30 | Temperature scaling on P2_val; `estimator/equations.py` (already tested) applied to model outputs | Recovers a known daily count on simulated streams with p = truth |
| First baselines | W30 to W36 | Logistic regression, SVM and random forest on RR features; BiLSTM; transformer (D6 losses [Proposed]: weighted cross-entropy plus Poisson) | Daily-equivalent MAE on P2_val for each |
| Interim ST-GNN | W34 to W40 | One configuration, three seeds, on P2_train and P2_val; **P2_test untouched until the S4 comparisons** | Interim MAE reported; checkpoint saved |
| Dry-run package | W38 to W41 | One command takes a reported-beat table and coverage table and outputs daily and pooled counts with the ESVEA call | Runs on a simulated stream; ready for Garmin verification data |

### T12. Handover pack to Track 2 (W36 to W41)

See section 5. **Done when (G7):** every row in section 5 has its file committed and a one-paragraph README.

---

## 5. What Track 1 must hand to Track 2

| # | Item | Where it lives | Used by Track 2 for | Ready by |
|---|---|---|---|---|
| 1 | Coverage, valid-day rule, per-block gate, Equations 3.2 to 3.4 | `analysis/src/esvea/estimator/equations.py` (done, tested) | R3 imports it; R2 replaces the placeholder thresholds in `CoverageRule` | Now; thresholds after M1 |
| 2 | Reported-beat and coverage table format | `analysis/src/esvea/schema.py` (done) | Target format for the Garmin parser (R3) | Now |
| 3 | Motion definition and scale | `pulsewatch/matching.py`: SD of accelerometer magnitude, m/s², 2 s window; bins | R2 accelerometer check: what Garmin must provide and how it is mapped (D11) | Now; mapping after R2 |
| 4 | π̂(m) candidate with detector sensitivity | `results/pi_hat/` | Applied to Garmin motion in the dry run | W22 |
| 5 | Simulator flag and gap rules, with the quantities to compare | `simulate/stream.py`; the T10 report | R2 compares real Garmin flag fraction vs motion, gap durations and interval distribution against these | W26 |
| 6 | Interim model and dry-run command | T11 dry-run package | Meeting point 2: verification wear through R3 to a daily estimate | W41 |
| 7 | Fallback coverage model | T8d wear coverage per block from Pulsewatch | §3.9 fallback if the cohort cannot start | W22 |
| 8 | Day/night valid-day thresholds for the protocol | Placeholders: night ≥2 h, day ≥6 h, θ_block 1 h; data from T8d | R2 sets the final values; R4 writes them into the protocol | Draft W22; final after M1 |

---

## 6. Decisions due in this period

| ID | Decision | Default | Decide by |
|---|---|---|---|
| D1 | Size of P1 | Power at half the P0 effect, ≥90% | W4 |
| D2 | P2 split | All remaining, 70/15/15 by patient | W5 |
| D3 | AF stretches | RO1 both ways; excluded from the RO2 count target, kept in input | W6 |
| D4 | Motion for training | Episodes sampled from Pulsewatch (T8d) | W20 |
| D5 | N, k, L | Start 64, 8, 2; tuned on P2_val; sensitivity in S4 | W28 |
| D6 | Losses | Weighted cross-entropy plus Poisson count | W28 |
| D7 | GPU | Faculty server or cloud | W4 (needed W24) |
| New | Lag-method pass rule | ±0.04 s in ≥90% of sessions; ≥50% of excluded segments reached | W8 |
| New | π̂(m) model form | Motion spline with a subject random intercept | W14 |

---

## 7. Risks inside Track 1

| Risk | Early sign | Response |
|---|---|---|
| P0 does not reproduce | G1 fails at W4 | Align with the legacy script before anything else; do not draw P1 until G1 passes |
| Pulsewatch permission delayed | No reply by W6 | Supervisors contact the custodians; RO1 Icentia11k work continues; T8 and T10 slip, so RO2 starts on placeholder simulator values |
| Lag method fails its rule | G4 fails | Use labelled-segment lags only and report the limited reach as a limitation of π̂(m) |
| Detector disagreement persists | T8c difference ≥0.05 | Report both curves; carry both into RO2 as a sensitivity analysis (already planned) |
| GPU not available | No allocation by W16 | Run the baselines on CPU; reduce the interim ST-GNN to one seed |
| Icentia11k download throttled | T4 slower than 10 h | Spread over nights; download only P1 first, then P2 |

---

## 8. Initial code delivered with this runbook

`analysis/` (25 unit tests passing; one network test reads a real segment; a smoke run built tables for p00001 from PhysioNet):

| Module | State |
|---|---|
| `sets.py`: draw, SHA-256 lock, guard, P3 closed until M4 | Ready |
| `ingest/download.py`, `ingest/tables.py` | Ready; tested on a real patient |
| `ro1/filters.py`: percent deviation; adaptive via NeuroKit2 | Ready; the warm-up rule is checked at G1 |
| `ro1/retention.py`, `ro1/origin.py` | Ready |
| `ro1/glmm.py`: H1 model with adaptive quadrature; power simulation | Ready; recovers simulated parameters |
| `estimator/equations.py`, `schema.py` | Ready; shared with Track 2 |
| `pseudodays.py` | Ready |
| `pulsewatch/matching.py` | Ready for T8b and T8c; the readers for Pulsewatch files are still to be written (T8a) |
| `simulate/stream.py` | First version with placeholder parameters (T10) |
| `degrade/` | Empty by design until S5 |
| Not yet started | Pulsewatch file readers, π̂(m) fit, RQ1.1 models, RO2 model and baselines (T8, T11) |
