# Draft revisions for the proposal defence (not yet applied)

**Status:** draft for review with supervisors. Nothing here has been applied to `proposal/source/content.txt`, the docx or the slide deck.
**Base version:** handover of 3 November 2026 (`content.txt`, 45-slide deck, version 34).
**House rules followed:** APA 7th edition; no em dashes; main text kept at or under 7,000 words.

---

## 0. Summary

| ID | Problem | Where | Main-text words |
|---|---|---|---:|
| E1 | Equation 3.1 ignores the burden dependence that Section 4.2 reports | 3.4 text, Eq. 3.1, 3.2, 3.4 | +33 |
| E2 | The epoch scale has no day-long training data on Icentia11k | 3.4 para 1 | +31 |
| E3 | "Daily-count MAE" is not daily on Icentia11k | H2, Table 3.5, Table B.1 | +8 |
| E4 | Flag-as-input plus inverse weighting can count a beat twice; p̂ must be calibrated | 3.4 text, 2.8 | +49 |
| E5 | No PPG timing-noise operator in RO4a | 3.6, Table 3.4 | +21 |
| E6 | No Garmin-side check of the motion term | 3.5 | +11 |
| E7 | Coverage gate described as a model component | 3.4, Table 3.2 | +12 |
| E8 | Role of the rate head undefined | 3.4 para 1 | +19 |
| E9 | RO3 primary can pass while ESVEA is rarely computable | 3.5, Appendix C | +26 |
| E10 | Icentia11k patient sets not shown as disjoint | Table 3.1, new Table B.3 | +2 |
| E11 | Pilot weight 0.9 chosen on test cohorts | 4.1, Table 4.1 | +12 |
| | **Subtotal before trims** | | **+224** |
| T1 to T8 | Trims | 1.1, 2.1, 2.4, 3.4, 4.1, 4.2, 5.1 | -189 |
| | **Net change** (current main text 6,958; limit 7,000) | | **+35 → 6,993** |

All eight trims are needed to stay under the limit. T5 also adds 3 words where PPV is next defined (Section 2.6), giving about 6,996. If supervisors reject a trim, the fallback is the E8 removal alternative (saves 19 words).

Word counts follow the handover rule: Chapter 1 to the start of References, table rows counted, captions, equations and appendices not counted.

### Decisions needed from supervisors before applying
1. **E1:** burden-dependent retention in Equation 3.1 (recommended), or leave Equation 3.1 as it is and state that the network absorbs burden dependence (alternative text given).
2. **E8:** keep the rate head as an auxiliary target (recommended), or remove it and redraw Figure 3.2.
3. **E11:** needs a rerun of the pilot at score weight 0.5 for Simband (AF vs PAC/PVC) and MIMIC-III before Table 4.1 can be filled.
4. **E2:** confirm that Pulsewatch timestamps hold across days within a participant (the data check found UNIX millisecond timestamps within segments only).
5. **Title:** keep it, and use the prepared answer in Section 4.

---

## 1. Proposal text (Chapter 1 to Chapter 4)

### E1 · Burden-dependent retention (Section 3.4)

RO1 found PAC coupling-interval removal of 78.5% in ESVEA-negative patients against 60.0% in ESVEA-positive patients, and Section 4.2 concludes that "a single correction factor therefore cannot restore the count". Equation 3.1 then applies one fixed class retention. The fix makes class retention a function of the local ectopic share, which is the mechanism Section 4.2 gives (frequent PACs enter the running reference of the five preceding accepted intervals).

#### E1a · Section 3.4, paragraph 2, sentence on Equation 3.1 [main]
**Current**
> The flag enters the model as an input, and a separate reliability pathway bypasses both encoders: retention (Equation 3.1) combines beat-class retention from the RO1 filtering results with motion retention estimated on Pulsewatch, which pairs wrist PPG and accelerometer magnitude with reference ECG R-peaks; their product is an assumption, because those R-peaks carry no beat types.

**Proposed**
> The flag enters the model as an input, and a separate reliability pathway bypasses both encoders: retention (Equation 3.1) combines class retention from the RO1 filtering results, as a function of local PAC share, because loss fell as burden rose (Section 4.2), with motion retention estimated on Pulsewatch, which pairs wrist PPG and accelerometer magnitude with reference ECG R-peaks; their product is an assumption, because those R-peaks carry no beat types.

#### E1b · Section 3.4, definitions paragraph [main]
**Current**
> Formally, for day d and time-of-day block h, let A(d,h) be the retained beats, π̂ₖ(m) the probability that a beat of class k ∈ {PAC, other} is retained at motion m, p̂ᵢ the predicted probability that beat i is a PAC, mᵢ its accelerometer motion, and τ(d,h) the observed hours in the block. The retention model, daily rate, coverage gate and participant-level rate are:

**Proposed**
> Formally, for day d and time-of-day block h, let A(d,h) be the beats the device reports, π̂ₖ(m, e) the probability that a beat of class k ∈ {PAC, other} is reported at motion m and local ectopic share e, p̂ᵢ the calibrated probability that beat i is a PAC, mᵢ and eᵢ its motion and the PAC share of its five preceding intervals, and τ(d,h) the observed hours in the block. The retention model, daily rate, coverage gate and participant-level rate are:

#### E1c · Equations (not counted)
```
EQ|π̂ₖ(m, e) = π̂_class(k, e) · π̂_motion(m)|3.1
EQ|R̂(d) = Σₕ (Lₕ / 24) · [ Σᵢ∈A(d,h) p̂ᵢ / π̂_PAC(mᵢ, eᵢ) ] / τ(d,h)|3.2
EQ|report R̂(d) only if c(d, h) ≥ θ_block for every block h|3.3
EQ|R̄ = Σₕ (Lₕ / 24) · [ Σ_d∈V Σᵢ∈A(d,h) p̂ᵢ / π̂_PAC(mᵢ, eᵢ) ] / Σ_d∈V τ(d,h)|3.4
```
Check after the build that Equation 3.1 still fits on one line (handover rule).

#### E1d · Appendix C, after the first paragraph (not counted)
> Retention was fixed at 0.391 and did not vary with burden, so the simulation does not test the burden-dependent retention of Equation 3.1.

**Alternative to E1a to E1c if supervisors prefer not to change Equation 3.1** (use instead of E1a; about +25 words):
> Retention corrects only the average loss by beat class and motion; the dependence of loss on ectopy burden found in Section 4.2 is left to the network, which sees each beat's context, and is tested by H1.

---

### E2 · What the epoch scale trains on (Section 3.4, paragraph 1)

The interval block runs "across windows to aggregate the day", but Icentia11k segments last about 70 minutes and carry no clock time, so there is no real day to train or test on.

#### E2a · Section 3.4, paragraph 1 [main]
**Current**
> At the epoch scale, an interval block of graph convolution and a selective state-space layer operates across windows to aggregate the day.

**Proposed**
> At the epoch scale, an interval block of graph convolution and a selective state-space layer operates across windows to aggregate the day. As Icentia11k segments are untimed, it trains there on pseudo-days built from each patient's segments, learning aggregation under gaps rather than a diurnal pattern; RQ2.2 is judged against the patient-level rate.

**Optional addition if word count allows (+14):** "Real within-day ordering is tested on timestamped Pulsewatch recordings at window level." Verify first that Pulsewatch timestamps are continuous across days within a participant.

---

### E3 · Rename the H2 metric

#### E3a · Section 1.3, H2 [main]
**Current**
> H2: on subject-wise held-out data, the two-scale ST-GNN with the quality flag as input has a lower daily-count mean absolute error than the best non-graph baseline.

**Proposed**
> H2: on subject-wise held-out data, the two-scale ST-GNN with the quality flag as input has a lower mean absolute error of the daily-equivalent count (Table B.1) than the best non-graph baseline.

#### E3b · Table 3.5, RO2 row, "Primary metrics" cell [main]
**Current**
> Beat level: PAC sensitivity, PPV, F1, precision-recall AUC. Day level: daily-count mean absolute error; calibration slope and intercept across burden levels

**Proposed**
> Beat level: PAC sensitivity, PPV, F1, precision-recall AUC. Patient level: mean absolute error of the daily-equivalent count; calibration slope and intercept across burden levels

#### E3c · Table B.1, new row after "Ectopy rate" (not counted)
```
Daily-equivalent count | 24 times a patient-level rate of ectopic beats per analysable hour; used on Icentia11k, whose segments are untimed, in place of a true daily count
```

---

### E4 · No double counting, and calibrated probabilities (Section 3.4 and 2.8)

#### E4a · Section 3.4, paragraph 2, sentence after E1a [main, new sentence]
**Current**
> (none)

**Proposed**
> It corrects only beats the watch never reports, not flagged beats it reports; whether the Garmin deletes or only flags rejected beats is confirmed at device verification.

#### E4b · Section 3.4, paragraph 2 [main]
**Current**
> Retention is frozen and reweights surviving beats (Equation 3.2); time of day acts only through motion and coverage.

**Proposed**
> Retention is frozen and reweights reported beats (Equation 3.2); time of day acts only through motion and coverage. Because Equation 3.2 sums probabilities, p̂ᵢ is calibrated on validation subjects by temperature scaling (Guo et al., 2017).

#### E4c · Section 2.8, contributions paragraph [main]
**Current**
> Methodologically, the study treats the quality flag as evidence: a frozen retention model reweights retained beats, and a coverage gate decides when a daily value can be reported (Section 3.4, Equations 3.1 to 3.4).

**Proposed**
> Methodologically, the study treats the quality flag as evidence: a frozen retention model corrects for beats the device never reports, and a coverage gate decides when a daily value can be reported (Section 3.4, Equations 3.1 to 3.4).

#### E4d · New reference (APA 7; check the page range against the PMLR record before adding)
```
REF|Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. In D. Precup & Y. W. Teh (Eds.), *Proceedings of the 34th International Conference on Machine Learning* (Vol. 70, pp. 1321–1330). PMLR.
```

**Note for the defence.** If device verification shows the Garmin only flags and never deletes, the class part of Equation 3.1 applies only to pulse deficit and gaps, and RQ2.4 ("flag as filter vs input vs input with correction") becomes the main test of whether correction is needed at all. Say this if asked.

---

### E5 · Fourth degradation operator: PPG timing noise (Section 3.6)

The strongest answer to "your simulation is optimistic because Icentia11k is ECG RR" is to inject the timing error between PPG peaks and ECG R-peaks, measured on the paired Pulsewatch data you already have.

#### E5a · Section 3.6, paragraph 1 [main]
**Current**
> Three degradation operators are applied, each calibrated from measured data (Table 3.4) and sampled independently of the training simulation, and results are reported across a severity sweep for each operator.

**Proposed**
> Four degradation operators are applied, each calibrated from measured data (Table 3.4) and sampled independently of the training simulation, and results are reported across a severity sweep for each operator.

#### E5b · Table 3.4, new row after "Pulse deficit" [main, table row]
**Current**
> (none)

**Proposed**
> Interval timing noise | PPG peak timing that differs from the ECG R-peak | PPG to R-peak offsets on Pulsewatch, swept

---

### E6 · Garmin-side check of the motion term (Section 3.5)

#### E6a · Section 3.5, secondary questions sentence [main]
**Current**
> Secondary questions cover yield (RQ3.1), computability of the daily ESVEA denominator (RQ3.2), day-to-day stability (RQ3.3), activity (RQ3.4) and the ESVEA proportion as a plausibility check (Haeusler et al., 2025; Teare et al., 2014) (RQ3.5).

**Proposed**
> Secondary questions cover yield (RQ3.1), computability of the daily ESVEA denominator (RQ3.2), day-to-day stability (RQ3.3), activity, including whether the flagged-beat fraction rises with motion as on Pulsewatch (RQ3.4), and the ESVEA proportion as a plausibility check (Haeusler et al., 2025; Teare et al., 2014) (RQ3.5).

---

### E7 · Coverage gate is a reporting rule

#### E7a · Section 3.4, paragraph 2, last sentence [main]
**Current**
> A coverage gate decides whether a daily value is reported at all (Equation 3.3).

**Proposed**
> A coverage gate, a fixed reporting rule rather than a learned layer, decides whether a daily value is reported at all (Equation 3.3).

#### E7b · Table 3.2, RQ2.3 row, "Models benchmarked" cell [main]
**Current**
> Remove chain edges, similarity edges, interval block, retention correction, coverage gate

**Proposed**
> Remove chain edges, similarity edges, interval block, retention correction; coverage gate vs always reporting

---

### E8 · Role of the rate head (Section 3.4, paragraph 1)

#### E8a · Section 3.4, paragraph 1, last sentence [main]
**Current**
> An event head and a rate head produce beat-level and window-level estimates.

**Proposed**
> An event head gives the beat PAC probabilities used in Equations 3.2 to 3.4; a rate head, an auxiliary target for the window PAC count, is not used in reported estimates.

**Alternative (if the rate head is removed):** "An event head gives the beat-level PAC probabilities used in Equations 3.2 to 3.4." Then redraw Figure 3.2 without the rate head and drop it from the slides.

---

### E9 · Make pooled computability a key secondary outcome (Section 3.5)

Appendix C shows that under poor coverage 58% to 61% of simulated participants had three or more day/night-valid days, but only 20% to 21% had three or more days meeting the per-block rule. H3 could go green while per-day ESVEA is rarely computable.

#### E9a · Section 3.5, end of the paragraph on valid days [main, new sentence]
**Current**
> (none; follows "...the share of valid days meeting it answers RQ3.2.")

**Proposed**
> Computability of the pooled count (Equation 3.4) is a key secondary outcome, as simulated poor coverage left far fewer per-block than day/night valid days (Appendix C).

#### E9b · Appendix C, final paragraph, new sentence (not counted)
> Under poor coverage, 58% to 61% of simulated participants had three or more day/night-valid days, but only 20% to 21% had three or more days meeting the per-block rule; the pooled count remained computable in 87% to 88%.

---

### E10 · Disjoint Icentia11k patient sets

#### E10a · Table 3.1, RO4a row, "Data" cell [main, table row]
**Current**
> Held-out Icentia11k patients degraded to smartwatch-like intervals

**Proposed**
> Held-out Icentia11k patients (Table B.3) degraded to smartwatch-like intervals

#### E10b · New Table B.3 (appendix, not counted)
```
TABLE|Table B.3: Disjoint sets of Icentia11k patients
W|18|42|40
Set | Use | Size and selection
P0 | Preliminary RO1 analysis (Section 4.2); class retention π̂_class(k, e) | 298 analysed of 300 sampled with a fixed seed
P1 | H1 test of burden-dependent retention | New random sample, size fixed before analysis
P2 | RO2 training, validation and test, split by subject | Random sample, split lists recorded and released
P3 | RO4a held-out substitution test | About 300, untouched until the RO2 model is frozen (milestone M4)
ENDTABLE
```
Fix the P1 to P3 sizes and seeds when the split lists are drawn (post-defence task in the handover).

---

### E11 · Report the pilot at the untuned weight (Section 4.1)

**Blocked on a rerun.** The handover has weight 0.5 values only for the Pulsewatch clinical cohort (AF vs rest 1.000; AF vs PAC/PVC 0.998) and Simband AF vs rest (0.891). Rerun `pilot_auroc_check` at weight 0.5 for Simband AF vs PAC/PVC, MIMIC-III and recall, then fill Table 4.1.

#### E11a · Section 4.1, paragraph 1 [main]
**Current**
> Thresholds were set once on validation subjects (5 of 17 from external cohorts) and not tuned per device; the score weighting of 0.9 was chosen from a sweep on held-out cohorts, so the test data are not fully untouched.

**Proposed**
> Thresholds were set once on validation subjects (5 of 17 from external cohorts) and not tuned per device. Table 4.1 uses the original score weighting of 0.5; the weighting of 0.9, chosen from a sweep on held-out cohorts and therefore optimistic, raised Simband AF vs rest AUROC from 0.891 to 0.951.

#### E11b · Table 4.1 caption (not counted)
> Table 4.1: Pilot results on held-out cohorts (evaluation mode, score weight 0.5; 95% CIs resample subjects)

Table 4.1 cells: replace with weight 0.5 values after the rerun. The abstract's "AF recall between 88% and 100%" must be checked against the new recall values.

---

### Trims to stay within 7,000 words

#### T1 · Section 3.4, paragraph 2, lag sentence [main]
**Current**
> The released alignment is not accurate to the beat, so a lag is fitted per recording session; the current lag method needs labelled segments, and a method that does not is to be developed in RO2.

**Proposed**
> A per-session lag corrects the released alignment, which is not beat-accurate; a lag method not needing labelled segments is developed in RO2.

#### T2 · Section 4.1, final paragraph [main]
**Current**
> On Pulsewatch, AF separated from PAC/PVC windows, but all 170 AF windows came from one subject and two of ten PAC/PVC subjects supplied 95% of PAC/PVC windows, so between-patient variation is not captured. External results are promising pilot evidence, not proof of cross-device performance: Simband's lower bound is 0.654, MIMIC-III has three subjects, and the 0.9 weight favours them. Recall uses the gfeat-head score, whose AUROCs are lower (0.985 AF vs rest; 0.952 AF vs PAC/PVC). The pilot did not isolate the graph's contribution (RQ2.1, RQ2.3) and labels are per-window rhythm classes, so it shows feasibility of the representation, not of counting.

**Proposed**
> On Pulsewatch, all 170 AF windows came from one subject and two of ten PAC/PVC subjects supplied 95% of PAC/PVC windows, so between-patient variation is not captured. External results are pilot evidence, not proof of cross-device performance: Simband's lower bound is 0.654 and MIMIC-III has three subjects. Recall uses the gfeat-head score. Labels are per-window rhythm classes and the graph's contribution was not isolated, so the pilot shows feasibility of the representation, not of counting.

Note: T2 drops the gfeat-head AUROCs (0.985; 0.952). Keep them in the speaker notes for slide 17.

#### T3 · Section 5.1 [main]
**Current**
> The deliverables are the estimator code, split lists and a registered protocol; the contributions are the method and evidence set out in Section 2.8.

**Proposed**
> (delete)

#### T4 · Section 2.4 [main]
**Current**
> An Icentia11k autoencoder detected premature beats (sensitivity 0.87) without reporting PACs separately (Kapsecker & Jonas, 2025).

**Proposed**
> (delete; also remove the Kapsecker & Jonas, 2025 reference, which is cited only here)

#### T5 · Section 2.1, paragraph 2 [main]
**Current**
> Static recurrence models have plateaued at AUROC 0.68 to 0.80 (Montanaro et al., 2026; Ye et al., 2025) and decay with horizon (Abedi et al., 2021). In a Malaysian registry, an AUROC of 0.943 coexisted with a positive predictive value (PPV) of 40.2% (Alsalman et al., 2026).

**Proposed**
> (delete; remove the Montanaro, Ye and Abedi references, which are cited only here; Alsalman et al. stays cited in Section 3.7; define "positive predictive value (PPV)" at its next use in Section 2.6)

T5 slightly weakens the positioning against the review paper; the review is still cited in the first paragraph of Section 2.1.

#### T6 · Section 1.1, paragraph 2 [main]
**Current**
> Detecting AF moves a patient from antiplatelet therapy to anticoagulation, which reduces ischaemic stroke in device-detected AF (risk ratio 0.68) at the cost of more major bleeding (risk ratio 1.62) (McIntyre et al., 2024), with a larger absolute benefit in patients with a prior stroke or TIA (Shoamanesh et al., 2025).

**Proposed**
> Detecting AF moves a patient from antiplatelet therapy to anticoagulation, with a larger absolute benefit after stroke or TIA (McIntyre et al., 2024; Shoamanesh et al., 2025).

Keep the risk ratios (0.68; 1.62) in the speaker notes for slide 2.

#### T7 · Section 3.4, paragraph 2, detector sentence [main]
**Current**
> The primary detector is an implementation of the Elgendi et al. (2013) systolic-peak algorithm applied to all segments, with the authors' released peaks as the alternative on labelled segments; transfer from Samsung signals to the Garmin is a stated assumption.

**Proposed**
> The primary detector implements Elgendi et al. (2013) on all segments, with the authors' released peaks as the alternative; transfer from Samsung to Garmin signals is a stated assumption.

#### T8 · Section 4.2, final paragraph, opening [main]
**Current**
> Sixty-seven patients (22.5%) met the primary criterion of 480 or more PACs per day, and 66 (22.1%) met the rate-or-run definition of Binici et al. (2010) (Table 4.3). Icentia11k is a general ambulatory population, so this is not a stroke estimate;

**Proposed**
> Icentia11k is a general ambulatory population (Table 4.3), so this is not a stroke estimate;

The deleted figures remain in Table 4.3 and in Section 3.6.

---

## 2. Slide drafts (deck not changed)

Slide numbers follow the handover order. Only text is given; keep the existing HTML styling.

| Slide | File | Current | Proposed |
|---|---|---|---|
| 5 | `rq-ro.html` | **H2** the ST-GNN beats the best non-graph baseline on daily-count error | **H2** the ST-GNN beats the best non-graph baseline on daily-equivalent count error |
| 13 | `validation-matrix.html` | RO2 metric: Daily-count MAE; Bland–Altman bias and limits | RO2 metric: MAE of the daily-equivalent count (24 × patient rate); Bland–Altman bias and limits |
| 14 | `ro1-ro2.html` | Quality flag enters as input; retention by beat class (RO1) and motion (Pulsewatch, lag-corrected); coverage gate (Equations 3.1 to 3.4, appendix) | Quality flag enters as input; retention by beat class and local ectopic share (RO1) and motion (Pulsewatch, lag-corrected) corrects only unreported beats; coverage gate is a reporting rule (Equations 3.1 to 3.4) |
| 14 | `ro1-ro2.html` (new bullet) | (none) | Epoch scale trained on pseudo-days on Icentia11k (segments untimed); real day order tested on Pulsewatch |
| 15 | `ro3.html` (under primary outcome) | (none) | Key secondary: pooled ESVEA count computable (≥1 h per block across the week) |
| 16 | `ro4.html` (new table row) | (none) | Interval timing noise · PPG peak vs ECG R-peak offsets measured on Pulsewatch; swept |
| 17 | `preliminary.html` | Evaluation mode, score weight 0.9 throughout | Evaluation mode, score weight 0.5 (untuned); 0.9 reported as sensitivity |
| 17 | `preliminary.html` | the 0.9 score weight was chosen from a sweep on held-out cohorts, so test data are not fully untouched | the 0.9 weight, chosen on held-out cohorts, is shown only as a sensitivity result (Simband 0.891 → 0.951) |
| 19 | `risks.html` | RO4a simulation optimistic (ECG RR, not PPG) · Calibrated operators; severity sweep; stated limitation | RO4a simulation optimistic (ECG RR, not PPG) · Four calibrated operators incl. PPG timing noise; severity sweep; stated limitation |
| App | `app-eq.html` | (3.1) π̂ₖ(m) = π̂_class(k) · π̂_motion(m) | (3.1) π̂ₖ(m, e) = π̂_class(k, e) · π̂_motion(m); and π̂_PAC(mᵢ, eᵢ) in (3.2) and (3.4) |
| App | `app-eq.html` (definitions line) | A(d,h): retained beats … m_i: accelerometer motion | A(d,h): beats the device reports; p̂ᵢ: calibrated PAC probability; mᵢ: motion; eᵢ: PAC share of the 5 preceding intervals |
| App | `app-c1.html` | Day level: MAE of the daily count; agreement with the patient-level reference | Patient level: MAE of the daily-equivalent count; calibration across burden |
| App | `app-b3.html` | Stage 1 fits the retention curve where censoring is observable; Stage 2 weights each surviving beat by 1/π(r); Stage 3 calibrates the coverage gate that decides whether … | Stage 1 fits retention: beat class and local ectopic share from RO1 × motion from Pulsewatch (lag-corrected); Stage 2 weights each reported beat by 1/π̂; Stage 3 applies the coverage gate, a fixed reporting rule. (Also a known handover inconsistency; the figure on this slide may need redrawing.) |

**Speaker note to add on `app-eq.html`:**
> If asked about double counting: the reliability pathway corrects only beats the watch never reports. Reported beats, flagged or not, stay in the model's input and are not reweighted. Beat probabilities are temperature-scaled on validation subjects before they are summed, because a sum of uncalibrated probabilities inflates the count.

**Speaker note to add on `ro1-ro2.html`:**
> If asked how the epoch graph learns a day from 70-minute segments: on Icentia11k it trains on pseudo-days built from each patient's own segments, so it learns aggregation under gaps, not a diurnal pattern. Real day order is tested on Pulsewatch at window level, and the day-level evidence comes from RO3.

---

## 3. Consistency checks after applying

- [ ] Zero em dashes (U+2014) in `content.txt` and changed slides.
- [ ] Guo et al. (2017) added to References; Kapsecker & Jonas (2025) removed (and Montanaro, Ye, Abedi if T5 is used).
- [ ] Equation 3.1 fits on one line in the docx.
- [ ] Tables 3.1, 3.3, 3.4 and B.2 still consistent with Section 3.4 (handover rule); Table 3.1 RO2 "Cannot claim" unchanged.
- [ ] Figure 3.2 caption still accurate (rate head kept or removed per E8).
- [ ] Abstract recall range rechecked after the E11 rerun.
- [ ] Main-text word count ≤ 7,000 using the handover rule.
- [ ] Research map page (`index.html`) updated to match whatever is applied.

---

## 4. Prepared answers (not for the manuscript)

**"The title leads with the ST-GNN, but you say the graph is not a contribution. Why?"**
> The title names the method I build and test. The contribution I claim is the observation model around it: retention correction, coverage-aware rates and the gate. The graph is the encoder I expect to work best on beat intervals, and RQ2.1 and RQ2.3 test that expectation against non-graph baselines. If it loses, the observation model is still evaluated on the best baseline and the negative result is reported.

**"What does your thesis prove without concurrent ECG on the Garmin?"**
> Three things. First, how much ectopy is lost from waveform to filtered intervals (RO1). Second, the error of the estimator against ECG labels under calibrated, swept device losses, including PPG timing noise (RO2, RO4a). Third, whether a 7-day protocol gives enough coverage after stroke to compute the estimate (RO3). Error on the Garmin itself needs concurrent ECG, and I state that as the next study.

**"Your retention pre-check failed. Why keep the motion term?"**
> It failed only on the detector criterion. Matching was above chance at high motion and fell with motion in 8 of 8 subjects. Absolute retention depends on the detector, so I report the motion term with a detector sensitivity analysis and claim no retention value. RO3 adds a Garmin-side check of whether flagging rises with motion in the same way.
