# Inputs required

## From the preliminary project (needed in W1; G1 cannot run without them)

| # | Item | Goes to | Used for |
|---|---|---|---|
| 1 | P0 patient list (300 ids) and the seed used to draw it | `analysis/splits/P0.txt` (seed in the header line) | Locking P0; drawing P1 to P3 from the rest |
| 2 | Preliminary RO1 script and its three result CSVs (`analyses/ro1_icentia11k/`) | `analysis/legacy/ro1_preliminary/` | G1: filter warm-up rule, categories, exclusions, hours |
| 3 | Pulsewatch pre-check scripts: `build/beat_retention_raw_test.py`, `signal_proc.py` (with `bandpass_ppg`, `detect_ppg_peaks`), `pulsewatch.mat_table` reader | `analysis/legacy/pulsewatch_precheck/` | B7 and B8: lag search, matching, Elgendi detector, file readers |
| 4 | Pre-check outputs: `beat_retention_raw_results.json`, `beat_retention_raw_skipcounts.json` | `analysis/legacy/pulsewatch_precheck/` | Baseline for B8 |
| 5 | Local Pulsewatch data already downloaded (`synapse_data/` with the 8 pre-check subjects and ECG patches) | Under `ESVEA_DATA/pulsewatch/` | B6 to B10 |

## To request (written replies)

| # | Item | From | Needed by |
|---|---|---|---|
| 6 | Permission to use Pulsewatch for the thesis and publications | Pulsewatch custodians via Synapse syn23565056 | W6 (critical path) |
| 7 | University storage (about 350 GB) | University IT or faculty | W2 |
| 8 | GPU allocation (D7) | Faculty server or cloud | Request by W4; needed by W24 |
| 9 | UM academic calendar 2026/2027 | UM | W1 (confirm week dates) |

## Decisions to agree with the supervisors (defaults in the runbook, section 6)

D1 rule (W4), D2 split (W5), D3 AF stretches (W6), lag pass rule (W8), π̂(m) model form (W14), D4 motion (W20), D5 N, k, L and D6 losses (W28), D7 GPU (W4), target conference and journal (W12).
