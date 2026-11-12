# Track 1 completion checklist (S2 to the end of S3)

Keep the **Status** column current: `Not started`, `In progress`, `Done (date, commit)`, or `Blocked (reason)`. Weeks: W1 = 16 Nov 2026, W16 = 1 Mar 2027, W41 = 23 Aug 2027 (confirm against the UM calendar). Details for each item are in the runbook section given in brackets.

## Gates

| Gate | Week | Passes when | Evidence | Status |
|---|---|---|---|---|
| G1 | W4 | New pipeline reproduces Tables 4.2 and 4.3 on P0 exactly | `results/p0_reproduction.json`, script exits 0 | Not passed (locked rule); proceeding by decision of 12 Nov 2026, see `analysis/notes/2026-11-12_G1_decision.md` |
| G2 | W8 | P0, P1, P2 (train, val, test) and P3 locked; P1 and P2 downloaded and built | `splits/SHA256SUMS`; `raw/MANIFEST.sha256`; `summary.parquet` | Not started |
| G3 | W11 | H1 result on P1 | `results/h1_P1.json` + committed pre-analysis note | Not started |
| G4 | W15 | New lag method passes its pre-set rule | Lag note + result | Not started |
| G5 | W22 | π̂(m) candidate with both peak detectors | `results/pi_hat/` | Not started |
| G6 | W26 | RQ1.1 result; simulator validated | RQ1.1 table; simulator validation report | Not started |
| G7 | W41 | Track 2 handover pack complete (8 items, section D) | Files + README per item | Not started |

## A. Setup and data (T0 to T4)

| # | Item | Week | Expected result | Done when | Status |
|---|---|---|---|---|---|
| A1 | Environment (T0) | W1 | `pytest -q`: 25 passed; `pytest -m network` reads p00000_s00 | Both pass on the local machine | Done (12 Nov 2026, commit "A1"): 25 passed and network test passed on Python 3.14.3, wfdb 4.3.1; now 28 with three legacy-rule tests |
| A2 | Storage (T0) | W2 | About 10 GB for Icentia11k labels and tables; about 340 GB for Pulsewatch | `ESVEA_DATA` set; quota confirmed in writing | In progress: interim local `Documents/ridhwan/ESVEA_DATA` (outside git); university quota not yet requested; P0 raw labels took about 0.6 GB, not 0.2 GB |
| A3 | Legacy code imported (T0) | W1 | Preliminary RO1 script, P0 list, Pulsewatch pre-check scripts under `analysis/legacy/` | Committed with origin noted | Done (12 Nov 2026, commit "A3"): `legacy/ORIGIN.md` + `legacy/SHA256SUMS`; legacy per-patient CSVs (`patients.csv`, `retention_by_patient.csv`) not found |
| A4 | P0 imported (T1) | W1 | `splits/P0.txt`: 300 ids, seed in header, hash in `SHA256SUMS` | Committed | Done (12 Nov 2026, commit "A4"): regenerated from the legacy draw rule `sorted(random.Random(2026).sample(range(11000), 300))` (no stored list found) |
| A5 | P3 drawn and sealed (T1) | W1 | 300 ids, disjoint from P0; never downloaded before M4 | Committed; `s02_download.py P3` refuses | Done (13 Nov 2026, commit "A5"): 300 ids, seed 20261113 (rule: date of the draw as YYYYMMDD); 0 overlap with P0; `s02_download.py P3` exits 1 ("P3 is not downloaded before M4"); `Guard('ro4a')` refuses until `notes/M4_freeze_record.md` exists |
| A6 | P0 built (T2) | W2 | 300 patients downloaded (about 0.2 GB); 298 analysable | Tables and summary written | Done (12 Nov 2026, commit "A6"): 300 downloaded, 29,519 files (about 0.6 GB), checksums in `results/p0_raw_MANIFEST.sha256`; 3 .atr files absent on PhysioNet (`results/p0_raw_MISSING.txt`); 298 analysable (p08269 and p10564 contain only Q beats) |
| A7 | **P0 reproduction (T2, G1)** | W4 | See section E, all values equal | `s04_reproduce_p0.py` exits 0 | Not passed (locked rule); proceeding by decision of 12 Nov 2026, see `analysis/notes/2026-11-12_G1_decision.md` |
| A8 | D1 power note (T3) | W4 | P1 size = smallest with ≥90% power at half the P0 effect [Proposed rule] | `notes/<date>_D1_P1_size.md` committed **before** P1 is drawn | Done (13 Nov 2026, commit "A8"): `notes/2026-11-13_D1_P1_size.md`; P1 size = 900 (power 0.914 at half the P0 effect; false-positive rate 0.040 at 900); first run invalid (glmm SE bug, fixed in 2bd3374) and discarded; size confirmed 13 Nov 2026 |
| A9 | P1 drawn (T1) | W4 | Size from A8; disjoint | Committed | Done (13 Nov 2026, commit "A9"): 900 ids, seed 20261113 (rule: date of the draw as YYYYMMDD); 0 overlap with P0 and P3; `sets.verify()` passes |
| A10 | P2 drawn (T1) | W5 | All remaining patients, split 70/15/15 by patient (D2 [Proposed]) | Three lists committed | Not started |
| A11 | P1 and P2 built (T4) | W5 to W8 | About 10,400 patients; about 49 h serial, about 6 h in 8 jobs; about 6 GB labels | Manifest complete; re-run reports no checksum change | Not started |

## B. RO1 (T5 to T8e)

| # | Item | Week | Expected result | Done when | Status |
|---|---|---|---|---|---|
| B1 | RQ1.2 curves (T5) | W6 to W12 | Removal by class (PAC coupling, pause after PAC, PVC coupling, normal) × threshold 10 to 30% × burden band (<1, 1 to 10, 10 to 30, ≥30 PACs/h [Proposed]), AF included and excluded (D3); patient-bootstrap 95% CIs | 20% P0 row equals Table 4.2; figures regenerate from `results/ro1_sweep_*.parquet` | Not started |
| B2 | Adaptive filter (T5) | W8 | Lipponen and Tarvainen removal by class; index convention confirmed on 5 real patients | Table committed | Not started |
| B3 | H1 pre-analysis note (T6) | W8 | From `notes/templates/H1_preanalysis_template.md` | Committed before B4 | Not started |
| B4 | **H1 on P1 (T6, G3)** | W9 to W11 | Slope b (log PACs/h) with 95% CI, odds ratio per doubling, p; 20% primary; 10, 15, 25, 30% and AF-excluded as sensitivity. Direction expected b > 0 (higher retention at higher burden, as in section 4.2), but the test is two-sided | `results/h1_P1.json`; stated as supported or not | Not started |
| B5 | RQ1.3 (T7) | W10 to W11 | Per patient S+V vs S daily-equivalent counts; Bland–Altman bias and limits by band; number of P1 patients reclassified for ESVEA | Table and figure committed | Not started |
| B6 | Pulsewatch permission and download (T8a) | W1 to W10 | Written permission; all 71 subjects with ECG local and MD5-checked | Skip counts recorded before scoring | Not started |
| B7 | **Lag method (T8b, G4)** | W6 to W15 | Lag fitted from all segments of a session using low-motion beats; agreement ±0.04 s with the labelled lag in ≥90% of sessions; ≥50% of excluded segments reached [Proposed rule; fix in a note first]. Current method reaches 2.5% and 0.8% | Note + result committed | Not started |
| B8 | **π̂(m) (T8c, G5)** | W12 to W22 | Retention falls with motion (pre-check: match 0.849 at <0.05 m/s² to 0.407 at ≥1 m/s² in 8 subjects); curves from Elgendi (primary) and authors' peaks, with the difference (pre-check 0.850 vs 0.752). Model [Proposed]: motion spline + subject random intercept, 70/30 subject split | Versioned file in `results/pi_hat/`; not frozen until M4 | Not started |
| B9 | Profiles (T8d) | W18 to W22 | Motion episodes (level, duration); timing offsets; peak-free stretches; wear coverage per 6-hour block (Check E2 pooled 43.2 / 15.9 / 15.5 / 25.3%) | Tables + parametric summaries saved | Not started |
| B10 | **RQ1.1 (T8e, G6)** | W16 to W26 | Waveform model vs interval model on identical 30-s windows (NSR, AF, PAC/PVC merged); subject-wise 5-fold, five seeds; macro F1, PAC/PVC F1, AUROC; DeLong and paired subject bootstrap | Table + interpretation note | Not started |

## C. Simulator, RO2 start and papers (T9 to T11)

| # | Item | Week | Expected result | Done when | Status |
|---|---|---|---|---|---|
| C1 | Simulator calibration (T10) | W16 to W26 | Flag threshold from B1; motion from B9 (D4); silent loss from B8; gaps from B9; jitter off in training | Config versioned | Not started |
| C2 | **Simulator validation (T10, G6)** | W26 | Flagged fraction rises with motion; PACs flagged more than normal beats at low motion; PAC accounting holds; `simulate/` never imports `degrade/` | Validation report committed | Not started |
| C3 | RO2 data loader (T11) | W24 to W28 | P2 pseudo-days; windows of N beats (D5 start N 64, k 8, L 2 [Proposed]) | One patient batched in under 1 s; shape test passes | Not started |
| C4 | Graphs and model (T11) | W26 to W32 | Chain + k-NN graphs; gated local block; attention readout; interval block; event and rate heads | Overfits one batch | Not started |
| C5 | Estimator on model outputs (T11) | W28 to W30 | Temperature scaling on P2_val; Equations 3.2 to 3.4 | Recovers a known daily count when p equals truth | Not started |
| C6 | First baselines (T11) | W30 to W36 | Logistic regression, SVM, random forest on RR features; BiLSTM; transformer (D6 losses [Proposed]) | Daily-equivalent MAE on P2_val for each | Not started |
| C7 | Interim ST-GNN (T11) | W34 to W40 | One configuration, three seeds; **P2_test untouched** | Interim MAE + checkpoint | Not started |
| C8 | Conference paper, preliminary results (T9) | W12 to W22 | Pilot (Table 4.1) + filtering loss (Table 4.2) | Draft to supervisors | Not started |
| C9 | **RO1 journal paper, M3 (T9)** | W12 to W34 | RQ1.1, RQ1.2, RQ1.3, H1 | Submitted by W34 | Not started |

## D. Handover pack to Track 2 (T12, G7, by W41)

| # | Item | Ready now? | Expected content | Status |
|---|---|---|---|---|
| D1 | Coverage and Equations 3.2 to 3.4 | Yes (`estimator/equations.py`) | Track 2 imports it; thresholds replaced after device verification | Ready |
| D2 | Reported-beat and coverage format | Yes (`schema.py`) | Target format for the Garmin parser | Ready |
| D3 | Motion definition | Yes (`pulsewatch/matching.py`) | SD of accelerometer magnitude, m/s², 2 s window; bins; what Garmin must provide | Ready |
| D4 | π̂(m) candidate | After B8 (W22) | Both detectors | Not started |
| D5 | Simulator flag and gap rules + quantities to compare with real Garmin data | After C2 (W26) | Flag fraction vs motion; gap durations; interval distribution | Not started |
| D6 | Interim model + dry-run command | After C7 (W41) | One command: reported-beat table → daily and pooled counts + ESVEA call | Not started |
| D7 | Fallback coverage model | After B9 (W22) | Pulsewatch wear coverage per block (section 3.9 fallback) | Not started |
| D8 | Draft valid-day thresholds | Draft W22 | Placeholders night ≥2 h, day ≥6 h, θ_block 1 h; final after device verification | Not started |

## E. Reference values for G1 (section 4.2, 20% threshold)

| Quantity | Expected |
|---|---|
| Patients analysed | 298 of 300 |
| PAC coupling intervals removed | 60.9% |
| Pause after PAC removed | 54.5% |
| PVC coupling removed | 70.0% |
| Normal intervals removed | 8.8% |
| PAC removal, ESVEA-negative vs positive (Binici rate or run) | 78.5% vs 60.0% |
| ESVEA ≥480/day; ≥30/h; Binici rate or run | 67 (22.5%); 54 (18.1%); 66 (22.1%) |
| Median analysed hours; median PACs/h | 57.5 h; 1.35 (IQR 0.23 to 13.38) |
