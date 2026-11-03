# Check E11b: are all 8 AF-trial holdout subjects AF subjects?

**For:** Ridhwan (to run on your own machine, with the 3 November rerun code)
**Why:** the E11 draft writes the Table 4.1 row for the Pulsewatch AF-trial holdouts as "8; 5,483, all AF". If confirmed, it becomes "8 (8); 5,483", the same format as the other cohorts (for example "16 (1); 48,396").
**Draft text waiting on this:** E11d (Table 4.1 rows) in `drafts/proposal_revisions_draft.md`; the pilot table on the research map page (`index.html`); slide 17.
**Time needed:** about 10 minutes.

---

## 1. What "AF subject" means here

In Table 4.1, the number in brackets counts **subjects with at least one AF-labelled window in the evaluated test set**. It is not a clinical AF diagnosis. Use the same definition here, so the AF-trial row is counted like the other rows.

---

## 2. What the earlier output already shows

From `analyses/pilot_auroc/pilot_auroc_check.txt` (the earlier check, before the 3 November rerun):

```
Clinical:  subjects=16  windows=48396  AF=170  PAC/PVC=1779  AF subjects=1
Pooled (clinical + 4xx + 3xx):
           subjects=24  windows=53879  AF=5653  PAC/PVC=1779  AF subjects=9
```

Pooled minus clinical:

| | Pooled | Clinical | AF-trial holdouts |
|---|---:|---:|---:|
| Subjects | 24 | 16 | **8** |
| Subjects with any AF window | 9 | 1 | **8** |
| Windows | 53,879 | 48,396 | **5,483** |
| AF windows | 5,653 | 170 | **5,483** |
| PAC/PVC windows | 1,779 | 1,779 | **0** |

This already suggests that all 8 subjects are AF subjects and all 5,483 windows are AF. The check below confirms it on the **3 November rerun**, because only the external labels (Simband, MIMIC-III) were re-curated and these counts come from the earlier run.

---

## 3. Steps

### 3a. Use the rerun's test set
Open the script that produced the 3 November results (same v2 checkpoint, re-curated external labels, all v2 training and validation subjects excluded). Run the check **after** the test windows are loaded and filtered, so it sees exactly the windows that were scored.

### 3b. Add this snippet
Edit the column names to match your script (cohort, subject ID, window label).

```python
# Check E11b: AF-trial holdout subjects
t = test_df[test_df["cohort"].isin(["4xx", "3xx"])]        # EDIT: the AF-trial cohort codes

n_subj = t["subject"].nunique()
n_af_subj = t.loc[t["label"] == "AF", "subject"].nunique()  # EDIT: your AF label value
print("windows:", len(t))
print("subjects:", n_subj)
print("subjects with >=1 AF window:", n_af_subj)
print("windows by label:\n", t["label"].value_counts())
print("per subject:\n", t.groupby("subject")["label"].value_counts().unstack(fill_value=0))
```

### 3c. Check the cohort codes
Before reading the result, confirm which cohort codes make up the "AF trial holdouts" in the rerun (the earlier pooled block combined `4xx` and `3xx`). If the rerun's AF-trial group uses different codes, use those.

---

## 4. Pass rule

| Item | Expected | Result |
|---|---|---|
| Windows | 5,483 | 5,483 |
| Subjects | 8 | 8 |
| Subjects with ≥ 1 AF window | 8 | 8 |
| Labels present | AF only (no NSR, no PAC/PVC, no other) | AF only (2026-11-03, `build/results/pilot_e11b_af_trial_subjects.txt`): **Pass** |

**Pass:** all four match. The Table 4.1 row becomes `AF trial (Pulsewatch) | Wrist smartwatch PPG | 8 (8); 5,483 | …`.

**If it fails:**
- **Fewer than 8 subjects have an AF window:** write the true count, for example "8 (7); 5,483", and check why a subject with no AF windows is in an "AF trial" group.
- **Non-AF windows are present:** the AF-trial row can no longer say "Not computed" for AUROC. Compute AF vs rest (and AF vs PAC/PVC if any) with the same bootstrap settings, and send the numbers back.
- **Window count differs from 5,483:** stop and check the rerun's filters before changing any text. The recall figures (97% / 88%) were computed on 5,483 windows.

---

## 5. Optional: clinical diagnosis

Table 4.1 does not need it. If you want to say these are patients with diagnosed AF, check the Pulsewatch trial documentation (Dickson et al., 2021, protocol; Ding et al., 2023) for whether the `3xx` and `4xx` groups enrolled people with known AF. Do not write "diagnosed AF" in the proposal without that source.

---

## 6. How to send the result back

Reply with **one message** in exactly this structure. Copy the template, fill in every field, and keep the headings and their order. Write "none" rather than deleting a section. This is the same shape as your E2 and E11 results, so it can go straight into the draft.

````markdown
# Check E11b result: AF-trial holdout subjects

**Run:** YYYY-MM-DD HH:MM (+08:00)
**Script and data:** <script name>; 3 November rerun test set (v2 checkpoint, re-curated external labels)
**Rule:** Section 4 of the check file, unchanged / changed (if changed, say what and when)

## 1. Results
| Item | Expected | Result | Met? |
|---|---|---|---|
| Cohort codes used | 4xx, 3xx (confirm) | | |
| Windows | 5,483 | | |
| Subjects | 8 | | |
| Subjects with ≥ 1 AF window | 8 | | |
| Labels present | AF only | | |
| Any subject with zero AF windows | No | | |

## 2. Windows by label
| Label | Windows |
|---|---:|
| AF | |
| NSR | |
| PAC/PVC | |
| Other or noise | |
| **Total** | |

## 3. Per-subject counts (no subject IDs)
| Subject | AF windows | Non-AF windows |
|---|---:|---:|
| S1 | | |
| S2 | | |
| S3 | | |
| S4 | | |
| S5 | | |
| S6 | | |
| S7 | | |
| S8 | | |

## 4. Console output
```
<paste the raw printout here, with subject IDs replaced by S1 to S8>
```

## 5. Decision
Pass / Fail. If fail, which item failed and what you did (see Section 4 "If it fails").

## 6. Deviations from the instructions
none / list each change to the snippet, filters or cohort codes, and why.

## 7. Optional: clinical diagnosis source
none / the document and the sentence that says whether 3xx and 4xx enrolled people with known AF.
````

**Rules for the reply**
- Replace subject IDs with S1 to S8 everywhere, including the console output.
- Report numbers exactly as printed; do not round.
- If anything was seen before the run (for example, an earlier printout), say so under "Rule".
- If the window count is not 5,483, stop after Section 2 and send what you have.

## 7. What changes after a pass
- E11d in `proposal_revisions_draft.md`: "8; 5,483, all AF" → "8 (8); 5,483" (same word count).
- `index.html` pilot table: "8; 5,483 (all AF)" → "8 (8); 5,483".
- Slide 17 draft row: same change.
