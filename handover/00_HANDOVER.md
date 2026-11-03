# Handover: ESVEA smartwatch PhD proposal (state as of 3 November 2026)

Read this first. It replaces the long conversation history. Everything here was true at handover; anything marked **open** still needs action.

---

## 1. Who, what, where

| Item | Detail |
|---|---|
| Candidate | Ridhwan Amin Azhari Bin Zabidi, matric 25118475, PhD (by research) |
| Institution | Faculty of Computer Science and Information Technology (FSKTM/FCSIT), Universiti Malaya |
| Supervisors | Dr. Bryan Raj A/L Peter Jabaraj; Assoc. Prof. Ts. Dr. Ismail Bin Ahmedy |
| Thesis title | Estimating Atrial Ectopy Burden from Smartwatch Beat Intervals: A Two-Scale Spatio-Temporal Graph Neural Network and Its Feasibility in Post-Stroke Survivors |
| Stage | Proposal defence. Started Semester 2, 2025/2026 (= S1). Now S2. Thesis submission 8 May 2029 (= S7) |
| Deliverables | (1) Word proposal `proposal/Ridhwan_Research_Proposal_UM.docx`; (2) Claude Slides deck (artifact URL in Section 9); (3) the candidate's review paper (`review_paper/`) |
| House rules | APA 7th edition. **Never use em dashes.** Main text 3,000 to 7,000 words. Line and page numbers required. Report and slides must be consistent |
| User style | Direct, action-oriented, prefers execution over clarification. Wants decisions explained simply when asked, and markdown instruction files when they must check something themselves |

---

## 2. File map (this zip)

| Folder / file | What it is |
|---|---|
| `00_HANDOVER.md` | This document |
| `proposal/Ridhwan_Research_Proposal_UM.docx` / `.pdf` | **Latest proposal** (43 pages, main text about 6,980 words) |
| `proposal/source/content.txt` | Proposal source in custom markup (Section 10) |
| `proposal/source/build.js` | docx-js build script (A4, Times New Roman 12, double spacing, continuous line numbers) |
| `proposal/source/framework.png`, `arch.png` | Figure 3.1 (conceptual framework), Figure 3.2 (architecture) |
| `slides/deck.json`, `slides/slides/*.html` | Local source of the Claude Slides deck (45 slides) |
| `review_paper/` | Latest verified review paper (v2) and reference-correction notes |
| `analyses/ro1_icentia11k/` | RO1 preliminary script and its three result CSVs |
| `analyses/kappa_simulation/` | Simulation used to justify the pooled estimate and λ (README explains every layer) |
| `analyses/pulsewatch_retention/` | The candidate's Pulsewatch data check and pre-check config (the config holds the test result and decision) |
| `analyses/pilot_auroc/pilot_auroc_check.txt` | Output of the subject-level AUROC recheck |
| `analyses/icentia11k_clock_time/` | Evidence that Icentia11k segments carry no clock time |
| `checks/` | Instruction files written for the candidate, and review notes (some now superseded: see Section 8) |
| `decisions/` | Decision logs, the audit plan, UM requirements, the FSKTM checklist |

---

## 3. The study in one page

**Problem.** Atrial ectopy burden (ESVEA) selects post-stroke survivors for prolonged rhythm monitoring, but every threshold comes from Holter ECG, the scarce resource being allocated. Smartwatches report beat intervals with a per-beat quality flag, but the error of a smartwatch-derived daily ectopic-beat count is unknown, filtering removes ectopic beats preferentially, and analysable data are night-weighted while PACs peak in the afternoon and evening.

**Aim (reworded after independent review).** To establish whether smartwatch beat intervals, analysed with an estimator that models signal quality and unobserved time, can yield a daily atrial ectopy estimate whose error is characterised against ECG labels under simulated smartwatch losses and whose coverage after stroke is adequate, as a step towards comparison with ECG-derived ESVEA thresholds.

| RQ | RO |
|---|---|
| RQ1: How much ectopy information is lost when a PPG waveform is reduced to a quality-filtered beat-interval series? | RO1: Investigate the loss, separating absent pulse morphology from beat rejection |
| RQ2: Can a two-scale beat-interval ST-GNN using per-beat quality flags as input estimate atrial ectopy rate more accurately than sequence-based baselines? | RO2: Develop and evaluate the two-scale ST-GNN (beat-graph and epoch-graph) |
| RQ3: Can a 7-day smartwatch protocol in post-stroke survivors yield enough analysable and stable data for a per-day ESVEA classification? | RO3: Evaluate deployability (yield, threshold computability, day-to-day stability) against progression criteria |
| RQ4: Does substituting a smartwatch estimate for the ECG count change ESVEA classification, and how do wearable-based selections compare with clinical scores? | RO4: (a) reclassification under simulated device losses (Icentia11k, held-out patients); (b) agreement with score-based selections (cohort, descriptive) |

**Hypotheses.**
- **H1:** in Icentia11k patients not used in the preliminary analysis, PAC retention after filtering varies with ectopy burden, so no single correction factor restores the count. This replaced an earlier H1 that was true by construction.
- **H2:** on subject-wise held-out data, the ST-GNN with the flag as input has lower daily-count MAE than the best non-graph baseline.
- **H3:** at least 75% of participants yield three or more valid days (null 50% or below).
- RQ4 is descriptive.

**Design.** Three retrospective secondary-data analyses (RO1, RO2, RO4a) and one prospective observational cohort (RO3, RO4b).

| Data | Role | Key facts |
|---|---|---|
| Icentia11k (PhysioNet, CC BY-NC-SA 4.0) | ECG beat-label truth for RO1, RO2, RO4a | Up to 50 random ~70-min segments per patient, **no clock time**, ~24% beats unclassifiable. Reference = patient-level rate × 24, not a true day |
| Pulsewatch (Synapse syn23565056, folder syn64402376) | RO1 morphology loss; motion part of retention; window-level transfer test | Samsung watch PPG 50 Hz, accelerometer magnitude only, ECG R-peaks 250 Hz for clinical-trial subjects (no beat types), 30-s labels with PAC and PVC merged. Alignment not beat-accurate: per-session lag needed. No explicit licence found; permitted use to be confirmed with the data contact |
| Simband, MIMIC-III | Pilot external cohorts | Small subject counts |
| RO3 cohort | Feasibility, RO4b | Adults after ischaemic stroke or TIA without known AF, consecutive, at **PPUM (University of Malaya Medical Centre)**; recruit ~40, analyse ≥34; 7 days continuous Garmin wear (Enhanced BBI, binary confidence flag, gap markers, accelerometer). **No concurrent ECG, no ECG-patch substudy** (Bryan confirmed) |

**ESVEA definition.** Primary: ≥480 supraventricular beats per day (Haeusler et al., 2025, MonDAFIS, verified on PubMed). Secondary: ≥30 per hour (Binici et al., 2010). Runs are reported separately, because filtering breaks them.

---

## 4. Deep-learning architecture (proposal Section 3.4, Figure 3.2)

**Two-scale spatio-temporal graph neural network (ST-GNN) on beat-interval sequences.**

**(a) Inputs**
- Event features X ∈ R^{T×D} for T beats.
- Per-beat reliability r ∈ R^T, from the device quality flag.

**(b) Windowing and graphs**
- The stream is split into M windows of N beats: X^(w) ∈ R^{N×D}.
- Two static graphs are built per window and used in all layers:
  - **Â_adj:** banded temporal-chain adjacency.
  - **Â_sim:** k-nearest-neighbour similarity adjacency.

**(c) Encoders**
- **Local block × L.** From hidden state H ∈ R^{N×F}, three branches:
  - temporal-chain aggregation Â_adj H W_a, scaled by a learned chain gate α^(l)
  - self-feature preservation H W_s
  - similarity aggregation Â_sim H W_b, scaled by a learned similarity gate β^(l)

  The three are summed, then Norm and ReLU.
- **Attention readout:** gives one embedding per window.
- **Interval block × L (epoch scale, across windows within the day):** interval graph convolution, then a selective state-space layer, then norm and residual. Output Z ∈ R^{M×F}.

**(d) Heads**
- **Event head:** beat-level PAC probability p̂ᵢ.
- **Rate head:** window-level rate.
- **Frozen reliability correction:** fitted separately; this pathway bypasses both encoders, so its effect can be isolated by ablation.
- **Coverage gate:** decides whether a value is reported.
- Output: estimated rate ρ̂ ∈ R^M and a mask.

**Quality flag as evidence.** The Garmin flag marks both motion beats and abnormally short or long intervals, so a premature beat tends to be flagged. The flag is therefore input, not a deletion rule, and the accelerometer separates motion from rhythm events.

**Equations (proposal 3.1 to 3.4)**
- (3.1) π̂ₖ(m) = π̂_class(k) · π̂_motion(m), for class k ∈ {PAC, other} at motion m.
  - The class part comes from RO1 on Icentia11k: PAC coupling intervals kept 39.1% and normal intervals 91.2% at the 20% filter.
  - The motion part comes from Pulsewatch.
  - The product is an **assumption**.
  - There is no time-of-day term.
- (3.2) R̂(d) = Σₕ (Lₕ/24) · [Σᵢ∈A(d,h) p̂ᵢ / π̂_PAC(mᵢ)] / τ(d,h). The blocks h are 00–06, 06–12, 12–18 and 18–24 h, each Lₕ = 6 h. The daily count is 24·R̂(d).
- (3.3) Report R̂(d) only if coverage c(d,h) ≥ θ_block for every block. θ_block is set at device verification, proposed ~1 h.
- (3.4) R̄ = Σₕ (Lₕ/24) · [Σ_d∈V Σᵢ p̂ᵢ/π̂_PAC(mᵢ)] / Σ_d∈V τ(d,h): the participant count **pooled by block** over valid days V.
  - Requires ≥1 analysable hour per block across the week.
  - **ESVEA status uses 24·R̄.**
  - Per-day values are for stability.
- Sensitivity analysis: block rates shrunk towards the Larsen et al. (2016) Figure 3 profile (0.87, 0.63, 1.11, 1.40) with strength λ = 1 h (0.5, 2, 4 h also reported). λ, not κ, avoids clashing with Cohen's κ.
- Valid day for the RO3 primary outcome uses the looser day/night rule (night ≥ ~2 h, day ≥ ~6 h, assumed).

**Baselines and ablations (Table 3.2)**
- RQ2.1 graph vs non-graph: LR, SVM and RF on RR features; Poincaré rule; BiLSTM; GRU-D; transformer.
- RQ2.2 epoch-graph vs summation, mean pooling and LSTM over epochs.
- RQ2.3 ablations: chain edges, similarity edges, interval block, retention correction, coverage gate.
- RQ2.4 flag as filter vs input vs input with correction.

**Analysis plan (Table 3.5)**
- RO2: one primary contrast (H2) by paired subject-level bootstrap; other contrasts with Holm correction; seeds averaged.
- RO1: DeLong test, paired bootstrap, and a mixed-effects logistic regression of PAC retention on burden (H1).
- RO3: one-sided test vs 50%, Wilson CI, ICC(2,1).
- RO4a: reclassification, sensitivity and specificity, κ with Wilson CIs across a severity sweep.
- RO4b: Cohen κ, Jaccard, "equal monitoring capacity" (each method selects as many as the wearable calls ESVEA-positive), and atrial substrate (LA volume index, P-wave duration, NT-proBNP).

**RO4a design**
- Icentia11k patients **held out from RO1 calibration and RO2 training**.
- Three degradation operators:
  - beat rejection, from RO1
  - coverage gaps by block on pseudo-days, because segments are untimed
  - pulse deficit, below a coupling interval of ~55% of RR (Zheng et al., 2008), swept around that value
- Sampled independently of the training simulation; the frozen RO2 model re-estimates.

**Training flags on Icentia11k** are simulated from the Garmin specification and the RO1 results (a stated assumption).

**Implementation:** Python, PyTorch, PyTorch Geometric, one GPU, five seeds, versioned configs, code released on publication, RO3 protocol registered.

---

## 5. Results so far

### 5.1 RO1 preliminary (Icentia11k, 298 of 300 sampled patients, median 57.5 h each)
- Percent-deviation filter (median of 5 preceding accepted intervals). Removal at the 20% threshold:
  - PAC coupling intervals: **60.9%**
  - pause after PAC: 54.5%
  - PVC coupling: 70.0%
  - normal intervals: **8.8%**
- By ESVEA status (Binici rate or run), PAC removal at 20%: 78.5% in ESVEA-negative vs 60.0% in ESVEA-positive patients, so loss depends on burden.
- Prevalence:
  - ≥480/day (extrapolated): **67 (22.5%)**
  - ≥30/h: 54 (18.1%)
  - Binici rate or run: 66 (22.1%)
  - median 1.35 PACs/h (IQR 0.23 to 13.38)
- Files: `analyses/ro1_icentia11k/`.

### 5.2 Cross-device pilot (beat-graph rhythm classifier; evaluation mode, score weight 0.9, CIs resample subjects)

| Cohort | Subjects (AF subjects); windows | AF vs rest | AF vs PAC/PVC | Recall (gfeat-head score) |
|---|---|---|---|---|
| Pulsewatch clinical | 16 (1); 48,396 | 0.997 (0.996 to 0.998) | 0.981 (0.949 to 0.998) | 100% |
| Simband | 9 (3); 66 | 0.951 (0.654 to 0.995) | 0.944 (0.543 to 1.000) | 88% |
| MIMIC-III | 3 (1); 705 | 0.998 (0.856 to 1.000) | 0.973, indicative (CI not estimable) | 99% |
| Pulsewatch AF trial holdouts | 5,483 windows | Not computed | Not computed | 97% / 100% |

Disclosures that must stay with these numbers:
- **Splits:** subject-level with zero overlap (92/17/36 subjects across training, validation and test).
- **Thresholds:** set once on validation subjects, 5 of 17 of them external; no per-device tuning. Thresholds 0.393 (Youden) and 0.505 (95% specificity).
- **The 0.9 weight** was chosen from a sweep on these held-out cohorts, which is optimistic. Simband gains most (0.891 at 0.5 to 0.951).
- **Pulsewatch AF:** all 170 AF windows come from one subject, and 2 of 10 PAC/PVC subjects supply 95% of PAC/PVC windows.
- **Recall** uses the gfeat-head score, whose AUROCs are lower: 0.985, and 0.952 for AF vs PAC/PVC.
- **"Zero-shot" is not used:** training included AF from the other cohorts.
- **Superseded values:** an earlier logged 0.986 was computed with dropout on. An older Simband CI of 0.81 to 0.97 resampled windows.
- **Overall:** treat the external results as promising pilot evidence, not proof of cross-device performance.

### 5.3 Pulsewatch beat-retention pre-check (8 subjects): **NOT PASSED** under the locked rule
- Criterion 1, above chance at high motion: **met**. Excess was +0.273 (95% CI +0.180 to +0.336) at 0.5–1 m/s², and +0.197 (+0.122 to +0.254) at ≥1 m/s².
- Criterion 2, falls with motion within subjects: **met** (8/8; one subject near chance).
- Criterion 3, detector comparable: **not met**. Project detector 0.850 vs authors' peaks 0.752; pooled gap 0.097 (limit 0.05), largest subject gap 0.146 (limit 0.10).
- **Decision (made after results):**
  - The motion term stays, to be estimated on Pulsewatch in RO2.
  - The estimate is reported with a detector sensitivity analysis.
  - Primary detector: an Elgendi et al. (2013) systolic-peak implementation on all segments; the authors' peaks are the alternative on labelled segments.
  - A lag method independent of labelled segments is to be developed in RO2. The current one reached only 2.5% of excluded and 0.8% of no-label segments.
- **Never claim:** a π̂ value; that the test passed; that either detector is more accurate; that missed matches are the PPG's fault; anything AF-specific; data-use permission.

### 5.4 Simulation for the participant-level estimate (`analyses/kappa_simulation/`)
- **Calibration:** matched to Måneheim et al. (2024) 1-day and 7-day sensitivities (76.6%, 88.8%), ESVEA 25.3%, Ding et al. (2023) wear, and Merschel & Reinhardt (2022) usable time (71.5%, >94% at night).
- **Result:** pooling by block is as accurate as shrinkage and better than averaging only fully covered days under poor coverage. With poor coverage, median error is ~14% vs ~20%, and misclassification 2.7–3.3% vs 4.2–4.4%. λ from 0.5 to 4 h changes ESVEA class in ≤3% of participants.
- **Limits:**
  - retention and PAC identification treated as perfect
  - each unknown swept at two values
  - the Måneheim threshold mapping is assumed

### 5.5 Icentia11k clock time
- Headers read: 9 of 9, plus 59 of 60 random headers. None has a date, time or comments, and segments are 69.9 min.
- Hence: no time-of-day analysis on Icentia11k; patient-level reference rate; pseudo-days in RO4a.

---

## 6. Caveats the panel will probe (and the agreed answers)

1. **No real-device error measurement.** No objective has concurrent ECG on the Garmin. The answer: error is characterised on ECG-labelled data under simulated losses (RO2, RO4a), and transfer from Pulsewatch (Samsung) to the Garmin is a stated assumption. Direct Garmin validation is future work.
2. **Simulation optimism.** Icentia11k intervals are ECG RR, not PPG. Garmin PPG agrees only moderately with ECG for short-term variability after stroke (Theurl et al., 2023).
3. **The retention product is an assumption.** Pulsewatch R-peaks carry no beat types.
4. **Pilot evidence is thin.** One AF subject on Pulsewatch, Simband's lower bound 0.654, and three MIMIC subjects.
5. **The pre-check failed its detector criterion.** Absolute retention depends on the detector.
6. **The Icentia11k reference is extrapolated** from random, untimed segments.
7. **Device not yet received;** export, flags and battery are unconfirmed. A fallback applies if ethics or the device is not secured by S4: RO3 becomes a device-verification study, RO4a proceeds, and RO4b is deferred.
8. **The "first" claims** are qualified "to our knowledge" and "in these databases" (PubMed, Consensus, Wiley; October 2026). A targeted IEEE Xplore and arXiv search would close the gap.
9. **Pulsewatch licence:** no explicit licence; the access form asks only for citation.

---

## 7. Plan for the real research (Table 6.1; S1 = Sem 2 2025/26, S7 = Sem 2 2028/29)

| Semester | Work |
|---|---|
| S1–S2 | Literature review, proposal (defence now, S2) |
| S2–S3 | RO1: morphology loss on Pulsewatch (waveform vs interval model on identical recordings); filtering loss on Icentia11k (percent-deviation and adaptive Lipponen & Tarvainen filters, threshold sweep); premature vs PAC-only count by burden; H1 on new patients |
| S2–S4 | Device verification (export, timestamps, flags, gaps, battery, set θ thresholds); PPUM ethics; recruitment |
| S3–S4 | RO2: build ST-GNN; baselines and ablations; fit retention (class from RO1, motion from Pulsewatch with lag correction and detector sensitivity); freeze model before RO4a |
| S4–S6 | RO3: 7-day monitoring and analysis |
| S4 | Candidature defence |
| S5–S6 | RO4a on held-out Icentia11k; RO4b in cohort |
| S6–S7 | Thesis writing; submission 8 May 2029 |

**Milestones**
- M1 device verified (S3)
- M2 ethics approved and protocol registered (S3)
- M3 RO1 paper submitted (S3)
- M4 RO2 model frozen (S4)
- M5 candidature defence (S4)
- M6 recruitment complete (S5)
- M7 thesis submitted (S7, 8 May 2029)

**Papers:** RO1 (S3), RO2 (S5), RO3 (S6), a pilot conference paper (S3). UM requires at least one indexed publication accepted before graduation.

**Immediate post-defence research tasks**
- Download the full Pulsewatch release (~338 GB).
- Design the lag method that doesn't need labelled segments.
- Select the held-out Icentia11k patients for H1 and RO4a, and fix the split lists.
- Specify the training-flag simulator.
- Confirm Garmin Health SDK access.

---

## 8. Open items

**Candidate / supervisors**
1. Supervisor approval of the final docx. Many changes since they last saw it: aim, ESVEA criterion, estimator, pilot numbers, schedule.
2. AI-use declaration and upload consent under the UM AI policy (Senate, 20 November 2025). Ask Bryan.
3. Postgraduate Office, in writing:
   - deadline: semester 2 vs 3, and one vs two weeks before the defence
   - number of copies; PDF or Word
   - whether tables count toward the 7,000 words (currently ~6,980, so there's no room if they do)
   - whether the IAS line-number rule applies
4. Confirm the formal ethics committee name. The text says "PPUM Medical Research Ethics Committee"; it may be "UMMC MREC".
5. Confirm the semester mapping is acceptable. S3 is crowded (device, ethics, RO1 paper); check that a candidature defence in S4 fits FSKTM rules.
6. Pulsewatch permitted use: get written confirmation from the data contact (Dong Han).
7. Name the funder and the Garmin SDK timeline, if they can be disclosed.
8. Open the docx in Word and check the layout. All checks so far used LibreOffice.
9. Mock defence (likely questions: Section 6).

**Superseded documents (do not follow)**
- `checks/Pulsewatch_Precheck_Review.md` and the candidate's Pulsewatch files still say the RO3 ECG-patch substudy "stays". **It was ruled out by Bryan.**
- `checks/Icentia11k_Check_Review_and_Proposed_Edits.md`, `Check_Icentia11k_Clock_Time.md` and `Check_Kappa_Shrinkage_Strength.md` predate the final decisions:
  - pooled estimate (Equation 3.4)
  - λ instead of κ
  - ESVEA at 480/day
  - Equation 3.1 as a product

  The proposal text is authoritative.

**Known slide inconsistencies still to tidy (minor, not yet fixed)**
- `problem.html` still says "the resource the selection rations" (the proposal now says "the scarce resource being allocated").
- `gaps.html` uses the longer gap wording, while the proposal's Table 2.1 is shortened. Its speaker notes quote Bhurane 93.96%.
- `app-b3.html` says "Stage 1 fits the retention curve where censoring is observable", which is outdated. It should say class from RO1 × motion from Pulsewatch with lag correction.
- `app-a3.html` and `refs-1.html` still list sources removed from the proposal (Holmes, Robinson, Bacevičius, Jing). This is harmless for slides but inconsistent.
- The reference slides use "et al.", while the proposal uses full APA author lists.

**Claim to confirm:** Table 2.1 "PAC/PVC sensitivity 83% to 94% (Han et al., 2026; Bhurane et al., 2026)". The gaps-slide notes attribute 93.96% to Bhurane et al. and warn it is not directly comparable (subject independence not reported); Table 2.2 gives Bhurane accuracy 98.0%. Confirm that 93.96% is Bhurane's PAC/PVC sensitivity.

---

## 9. Slide deck

- **Claude Slides artifact:** https://claude.ai/artifact/4RuYVim5WsRqG5aQLYJGas (private to the user; latest published version 34).
- **To edit:**
  - Read the published file first (`Artifact` action `read` with `path`); a publish of a file not read in the session is refused.
  - Edit `project/slides/<id>.html`.
  - Publish with `file_path` = `deck.json`, `root` = the folder containing `project/`, and a `files` map of the changed slides.
- **Format:**
  - 1920×1080.
  - Speaker notes in `<aside>`.
  - Slide numbers are `<p style="position:absolute;right:112px;bottom:56px...">N</p>`.
  - The architecture image in `ro1-ro2.html` is an artifact blob (`/_blob/...`), not in this zip. The same image is `proposal/source/arch.png`.
- **Order (22 main slides + 7 reference slides + appendix):**
  1. cover
  2. bg-esvea
  3. bg-monitoring
  4. problem
  5. rq-ro
  6. scope-significance
  7. lit-selection
  8. lit-ppg
  9. gaps
  10. closest
  11. framework
  12. method-overview
  13. validation-matrix
  14. ro1-ro2
  15. ro3
  16. ro4
  17. preliminary
  18. preliminary-icentia
  19. risks
  20. ethics-data
  21. contributions
  22. thanks

  Then refs-1 to refs-7, app-divider, app-eq, app-a1 to a8, app-b1 to b3, app-c1 to c3.
- **Presentation:** 15 to 20 min, plus 10 to 20 min Q&A.
- **Bryan's earlier comments (all applied):**
  - bigger cover text
  - RO1/RO3/RO4 wording
  - an "Advantages" column and bold limits in the literature table
  - Phase headings "Investigate information loss" and "Substitute and validate"
  - a larger architecture image on slide 14

---

## 10. How to edit and rebuild the proposal

- **Source:** `proposal/source/content.txt`. Markup:
  - `# ` chapter heading, `## ` section heading
  - `TABLE|caption`, then `W|widths`, then rows separated by ` | `, then `ENDTABLE`
  - `FIGURE|file|width_cm|caption`
  - `EQ|equation|number`
  - `REF|reference`
  - `PAGEBREAK`, `ABSTRACT`
  - `*italic*`, `**bold**`
- **Build:** `node build.js` in the folder holding `content.txt`, the figures and `build.js` (needs the npm `docx` package). Then convert to PDF with LibreOffice to check the layout.
- **Word-count rule used:** all lines before `# REFERENCES`, excluding TABLE/W/FIGURE/EQ/ENDTABLE/PAGEBREAK lines (so table rows count, captions don't). Keep ≤ 7,000; currently ~6,980, **so any addition needs a trim**.
- **Checks after every edit:**
  - zero em dashes (U+2014)
  - every reference cited and every citation referenced
  - Equation 3.1 fits on one line
  - Tables 3.1, 3.3, 3.4 and B.2 stay consistent with Section 3.4

---

## 11. Review paper (separate deliverable)

- **Latest:** `review_paper/RBME_Review_Stroke_Recurrence_ML_DL_v2_verified.docx`. It's the version with affiliations: 69 studies, 42 recurrence, 4 of 42 externally validated, calibration in 17, 2 of 18 signal studies quantified data loss.
- **Corrections made:**
  - Chen 2024 is subject-independent, not subject-dependent.
  - PRERISK c-index 0.885 with patient-level 5-fold CV.
  - García-Terriza: composite outcome, 500 patients, 34 events, window-level CV.
- **Still unverifiable:** whether the Vodencarevic nested-CV folds were grouped by patient. The text says "double nested cross-validation".
- **In the proposal** it's cited as: Amin, R., Raj, B., & Ahmedy, I. (2026). *From static prediction to continuous monitoring: A taxonomy-based systematic review…* [Unpublished manuscript]. FCSIT, Universiti Malaya.
