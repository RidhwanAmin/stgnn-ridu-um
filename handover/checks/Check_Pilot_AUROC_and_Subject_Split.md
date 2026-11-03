# Check: exact pilot AUROC and subject-level split

**Why this matters:** Table 4.1 of the proposal reports the Pulsewatch result as "≈1.00 (AF vs PAC/PVC 0.986)".
- "≈1.00" hides the real value, and a near-perfect AUROC invites a leakage question. Chen et al. (2024) reached only 0.664 PAC/PVC sensitivity on the same Pulsewatch data.
- The proposal text does not state how the data were split. Only the pilot slide says "subject-level splits".

This is not a decision. It is a number your pilot already produced, and a fact about how the data were split. You only need to look both up, or recompute them, and confirm them.

**What to answer at the end:**
- **Q1.** The exact Pulsewatch AF-vs-rest AUROC, to three decimals, ideally with a 95% CI.
- **Q2.** The exact AF vs PAC/PVC AUROC (currently 0.986), with a 95% CI if possible.
- **Q3.** Do any subjects appear in both the training and the test sets? (The answer must be 0.)
- **Q4.** Were the decision threshold and the 0.986 value computed on validation and test subjects only, respectively?

**Time needed:** about 15 to 30 minutes on the computer with the pilot outputs.

---

## Step 1. Find the exact AUROC in your pilot outputs

Look in the pilot's output or log folder for a metrics file (`.json`, `.csv` or a training log) for the **Pulsewatch held-out test**. Note:
- AF-vs-rest AUROC, to three decimals
- AF vs PAC/PVC AUROC, to three decimals
- whether a 95% confidence interval was already computed

If you find both values with confidence intervals, skip to Step 3.

## Step 2. If only predictions were saved, recompute

You need a file of test-set predictions with one row per window: subject ID, true label, and the predicted AF probability. Adjust the file and column names below to match yours.

Save as `pilot_auroc_check.py` and run `python pilot_auroc_check.py`:

```python
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

d = pd.read_csv("pulsewatch_test_predictions.csv")   # columns: subject_id, label, p_af

def auroc(df, negatives=None):
    """AF vs rest, or AF vs a chosen negative class (e.g. 'PAC/PVC')."""
    if negatives is not None:
        df = df[df.label.isin(["AF", negatives])]
    return roc_auc_score(df.label == "AF", df.p_af)

def subject_ci(df, negatives=None, n=2000, seed=2026):
    """95% CI by resampling subjects (with replacement), not windows."""
    rng = np.random.default_rng(seed)
    subs = df.subject_id.unique()
    groups = {s: g for s, g in df.groupby("subject_id")}
    vals = []
    for _ in range(n):
        boot = pd.concat([groups[s] for s in rng.choice(subs, len(subs), replace=True)])
        sub = boot if negatives is None else boot[boot.label.isin(["AF", negatives])]
        if sub.label.eq("AF").nunique() == 2:
            vals.append(auroc(sub))
    return np.percentile(vals, [2.5, 97.5])

for name, neg in [("AF vs rest", None), ("AF vs PAC/PVC", "PAC/PVC")]:
    lo, hi = subject_ci(d, neg)
    print(f"{name}: AUROC {auroc(d, neg):.3f} (95% CI {lo:.3f} to {hi:.3f}); "
          f"subjects {d.subject_id.nunique()}, windows {len(d)}")
```

If `pip install scikit-learn pandas numpy` is needed, run it first. Use the label text your files actually use for the PAC/PVC class.

## Step 3. Confirm the split is by subject

Point these at your actual split files (train, validation and test subject lists):

```python
import pandas as pd
train = set(pd.read_csv("train_split.csv").subject_id)
val   = set(pd.read_csv("val_split.csv").subject_id)
test  = set(pd.read_csv("test_split.csv").subject_id)
print("train & test:", len(train & test))   # must be 0
print("val & test:  ", len(val & test))     # must be 0
print("train & val: ", len(train & val))    # should be 0
```

Also check, from your code or notes:
- the decision threshold was chosen on **validation** data, not on the test set (the pilot slide already says this)
- the 0.986 AF vs PAC/PVC value was computed on **test subjects only**
- no preprocessing statistic (normalisation, resampling) was fitted on test data

## Step 4. What each result means for the proposal

| What you find | Wording in Table 4.1 and Section 4.1 |
|---|---|
| No subject overlap; exact values available | State "subject-level split" in Section 4.1; replace "≈1.00" with the exact AUROC and its 95% CI, e.g. "0.998 (0.995 to 1.000)" |
| Value rounds to 1.000 | Report "1.000 (95% CI lower bound to 1.000)"; do not write "≈" |
| No confidence interval possible (no saved predictions) | Report the exact point value and state that the CI was not computed |
| Subjects overlap, or the split was by window | Rerun the pilot with a subject-level split before the defence. Otherwise remove the Pulsewatch AUROC and keep only the cross-device recall results |

**Word count:** stating the split and the exact values adds about 10 to 15 words to the main text, which fits in the remaining headroom (about 30 words under the 7,000 limit).

## Step 5. Send the result back

Paste into the chat:
1. Q1 and Q2: the two AUROC values, with confidence intervals if available
2. Q3: the overlap counts from Step 3
3. Q4: yes or no for the threshold and the test-only computation
4. The number of test subjects and windows

Claude will then update Table 4.1, Section 4.1 and the pilot slide (slide 17).

**Data protection:** share only the summary numbers, not prediction files or subject identifiers.
