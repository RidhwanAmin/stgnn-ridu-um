# Check E11: rerun the cross-device pilot at score weight 0.5

**Status: DONE (3 November 2026).** Rule locked 2026-11-03 12:40 (+08:00), before any new-data result was computed; not blind, because legacy and clinical results had already been seen. External labels were re-curated and all v2 training and validation subjects excluded; the earlier Simband and MIMIC-III values are withdrawn. Results and the drafted text are in E11 of `proposal_revisions_draft.md`. The tables below are kept as the original instructions.

**For:** Ridhwan (to run on your own machine; the pilot code, checkpoints and data are not in the handover)
**Why:** review issue #12. Table 4.1 reports the pilot at score weight 0.9, and that weight was chosen from a sweep on the held-out cohorts, so the test data informed it. Reporting the untuned weight 0.5 as primary, with 0.9 as a sensitivity result, removes that criticism.
**Draft text waiting on this:** E11 in `drafts/proposal_revisions_draft.md` (Section 4.1, Table 4.1, abstract, slide 17).
**Time needed:** about 30 to 60 minutes, mostly bootstrap run time.

---

## 1. Lock the rule before running

Write the date and time here before you run anything. Do not change the rule after seeing results; if you must, record it as a post-hoc change.

| Rule | Value |
|---|---|
| Primary weight | **w = 0.5**, reported whatever the result |
| Sensitivity weight | w = 0.9 (current Table 4.1) |
| Thresholds | Unchanged: Youden 0.393 and 95% specificity 0.505, set on validation subjects. **Do not re-tune.** |
| Mode | Evaluation mode (dropout off). The earlier 0.986 came from dropout left on. |
| CIs | Subject-level bootstrap, 2,000 resamples, same seed as `pilot_auroc_check.txt` |
| Splits | Same 92/17/36 subject split, zero overlap (as already verified) |
| Locked on | ____ (date, time) |

---

## 2. What you already have

From `analyses/pilot_auroc/pilot_auroc_check.txt` and the handover:

| Cohort | Comparison | w = 0.5 | w = 0.9 | w = 1.0 |
|---|---|---|---|---|
| Pulsewatch clinical | AF vs rest | 1.000 (1.000 to 1.000) | 0.997 (0.996 to 0.998) | 0.985 (0.980 to 0.990) |
| Pulsewatch clinical | AF vs PAC/PVC | 0.998 (0.997 to 1.000) | 0.981 (0.949 to 0.998) | 0.952 (0.869 to 0.996) |
| Simband | AF vs rest | 0.891 (CI not in handover) | 0.951 (0.654 to 0.995) | ? |
| Simband | AF vs PAC/PVC | **missing** | 0.944 (0.543 to 1.000) | ? |
| MIMIC-III | AF vs rest | **missing** | 0.998 (0.856 to 1.000) | ? |
| MIMIC-III | AF vs PAC/PVC | **missing** | 0.973 (indicative) | ? |

**Note on recall.** The w = 1.0 values (0.985 and 0.952) are the same AUROCs the proposal gives for the "gfeat-head score" used for recall. So recall appears to be computed on the w = 1.0 score, which does not depend on the weight. Step 3c confirms this. If it holds, the recall column (and the abstract's "88% to 100%") does not change.

---

## 3. Steps

### 3a. Find the script
The script that wrote `pilot_auroc_check.txt` is on your machine, next to `ckpt/log_plus_v2.txt` (the output names that log file). It already loops over weights 0.5, 0.9 and 1.0 for the Pulsewatch cohorts.

### 3b. Extend it to the external cohorts
For each held-out cohort (**Pulsewatch clinical, Simband, MIMIC-III**) and each weight (**0.5, 0.9, 1.0**), compute:
1. AF vs rest AUROC with the 95% subject-bootstrap CI.
2. AF vs PAC/PVC AUROC with the 95% subject-bootstrap CI.
3. The number of bootstrap resamples skipped (a resample is skipped when it has no AF or no comparison subject). Clinical skipped 701 of 2,000 before, because it has one AF subject.

If a CI cannot be estimated (for example MIMIC-III AF vs PAC/PVC, 3 subjects), write "not estimable", as now.

### 3c. Confirm which score recall uses
Print, for each cohort, the recall at threshold 0.393 and at 0.505, and state which score it was computed on (gfeat-head, w = 1.0, or the blended score). If recall changes with w, compute it at w = 0.5 too.

### 3d. Pulsewatch AF trial holdouts
Recall only, as in Table 4.1 (5,483 windows; currently 97% / 100%). Rerun only if 3c shows recall depends on w.

---

## 4. Fill in and send back

| Cohort | Subjects (AF); windows | AF vs rest, w = 0.5 | AF vs PAC/PVC, w = 0.5 | AF vs rest, w = 0.9 | AF vs PAC/PVC, w = 0.9 | Skipped resamples (0.5) | Recall (score used) |
|---|---|---|---|---|---|---|---|
| Pulsewatch clinical | 16 (1); 48,396 | | | 0.997 (0.996 to 0.998) | 0.981 (0.949 to 0.998) | | |
| Simband | 9 (3); 66 | | | 0.951 (0.654 to 0.995) | 0.944 (0.543 to 1.000) | | |
| MIMIC-III | 3 (1); 705 | | | 0.998 (0.856 to 1.000) | 0.973 (indicative) | | |
| Pulsewatch AF trial holdouts | 5,483 windows | not computed | not computed | not computed | not computed | | |

Also paste the raw console output, so the numbers can be traced.

---

## 5. What happens with the result

- **Table 4.1** is rebuilt at w = 0.5. The caption changes to "score weight 0.5" (E11b).
- **Section 4.1** gets the E11a sentence. If the Simband value differs from 0.891, the sentence is updated.
- **Abstract:** check "AF recall between 88% and 100%" against step 3c.
- **Slide 17** (`preliminary.html`): the weight note and the table.
- **Research map page** (`index.html`): the pilot table.

**If w = 0.5 looks worse on Simband:** report it anyway. Simband has 9 subjects and a lower bound of 0.654 already, and the proposal calls the pilot "promising pilot evidence, not proof". An untuned, slightly lower number is easier to defend than a tuned, higher one.

## 6. Do not claim
- That the pilot is "zero-shot": training included AF from the other cohorts.
- Anything about counting: the pilot classifies windows.
- That w = 0.9 is better: it was chosen on the test cohorts.
