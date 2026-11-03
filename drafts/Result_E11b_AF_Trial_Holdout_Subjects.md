# Check E11b result: AF-trial holdout subjects

**Run:** 2026-11-03 13:29 (+08:00)
**Script and data:** `build/check_e11b_af_trial_subjects.py`; 3 November rerun test set (v2 checkpoint, re-curated external labels)
**Rule:** Section 4 of the check file, unchanged. Seen before the run: window, subject and label totals (2 and 3 November). Per-subject counts had not been computed.

## 1. Results
| Item | Expected | Result | Met? |
|---|---|---|---|
| Cohort codes used | 4xx, 3xx (confirm) | 3xx, 4xx | Yes |
| Windows | 5,483 | 5483 | Yes |
| Subjects | 8 | 8 | Yes |
| Subjects with ≥ 1 AF window | 8 | 8 | Yes |
| Labels present | AF only | AF only | Yes |
| Any subject with zero AF windows | No | No (0 subjects) | Yes |

## 2. Windows by label
| Label | Windows |
|---|---:|
| AF | 5483 |
| NSR | 0 |
| PAC/PVC | 0 |
| Other or noise | 0 |
| **Total** | 5483 |

## 3. Per-subject counts (no subject IDs)
| Subject | Cohort | AF windows | Non-AF windows |
|---|---|---:|---:|
| S1 | 4xx | 2016 | 0 |
| S2 | 4xx | 1955 | 0 |
| S3 | 4xx | 1459 | 0 |
| S4 | 3xx | 17 | 0 |
| S5 | 3xx | 13 | 0 |
| S6 | 3xx | 11 | 0 |
| S7 | 3xx | 6 | 0 |
| S8 | 3xx | 6 | 0 |

By cohort: 3xx (in-clinic) 5 subjects, 53 windows; 4xx (AF trial) 3 subjects, 5,430 windows.

## 4. Console output (summary)
Asserts passed: labels match the scored windows; holdouts identical under legacy and new external labels; 0 overlap with v2 training or validation subjects. Raw label audit: 5,483 distinct segments, 0 dropped for missing or conflicting labels, 0 unanimous labels absent from the evaluated set. DECISION: PASS. Full printout in the candidate's message of 3 November 2026.

## 5. Decision
Pass. All four items met.

## 6. Deviations from the instructions
- The pandas snippet was replaced with equivalent logic (the code has no `test_df`; labels are integers 0 NSR, 1 AF, 2 PAC/PVC).
- Added a split by cohort code, cohort codes beside S1 to S8, and a count of segments dropped from the raw label files.
- Added asserts on label match, holdout identity under both external sources, and no overlap with v2 training or validation.

## 7. Optional: clinical diagnosis source
none

## Limits (from the candidate)
- Not independent evidence: 3xx test subjects are drawn only from subjects with AF, and the 4xx subjects are a fixed list.
- Recall only: with no non-AF windows, this row gives no false-alarm estimate.
- Concentration: S1 to S3 supply 5,430 of 5,483 windows (99%), so the 97% and 88% recall figures reflect three people.
- Row label: 3 subjects are AF trial (4xx) and 5 are in-clinic (3xx), so "AF trial" is inaccurate. Table 4.1 uses "Pulsewatch AF-only holdouts".
