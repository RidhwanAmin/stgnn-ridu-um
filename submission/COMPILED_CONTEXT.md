# ESVEA Proposal Defence: Compiled Context

Every markdown record from the handover to the latest change, in order. The mapping to the docx and slide deck is in `00_SUBMISSION_INDEX.md`. Handover records marked superseded in `00_HANDOVER.md` §8 are kept for the record; the proposal text is authoritative.

> Pending supervisor reconfirmation: E1 and E11 (see Part D).

## Contents

- **Part A. Handover (state at 3 November 2026)**
  - 1. `handover/00_HANDOVER.md`
  - 2. `handover/decisions/README.md`
  - 3. `handover/decisions/proposal-defence-decisions_part1.md`
  - 4. `handover/decisions/proposal-decisions-2026-11-02.md`
  - 5. `handover/decisions/proposal-audit-plan.md`
  - 6. `handover/decisions/UM_FSKTM_PhD_Proposal_Defence_Checklist.md`
  - 7. `handover/checks/Check_Icentia11k_Clock_Time.md`
  - 8. `handover/checks/Check_Kappa_Shrinkage_Strength.md`
  - 9. `handover/checks/Check_Pilot_AUROC_and_Subject_Split.md`
  - 10. `handover/checks/Check_Pulsewatch_Accelerometer_and_ECG_Beat_Timing.md`
  - 11. `handover/checks/Icentia11k_Check_Review_and_Proposed_Edits.md`
  - 12. `handover/checks/Pulsewatch_Precheck_Review.md`
  - 13. `handover/analyses/icentia11k_clock_time/00_START_HERE.md`
  - 14. `handover/analyses/icentia11k_clock_time/icentia_time_check_findings.md`
  - 15. `handover/analyses/kappa_simulation/README_kappa_simulation.md`
  - 16. `handover/analyses/pulsewatch_retention/Pulsewatch_Beat_Retention_Data_Check.md`
  - 17. `handover/analyses/pulsewatch_retention/Pulsewatch_Beat_Retention_Precheck_Config.md`
  - 18. `handover/review_paper/Review_Reference_Corrections.md`
- **Part B. Review and revision drafts**
  - 19. `drafts/proposal_revisions_draft.md`
- **Part C. Checks, verification and results**
  - 20. `drafts/Check_E11_Pilot_Rerun_Weight_0.5.md`
  - 21. `drafts/Check_E2_Pulsewatch_Timestamps.md`
  - 22. `drafts/Verification_Guo_H1_H2.md`
  - 23. `drafts/Result_E2_Pulsewatch_Timestamps.md`
  - 24. `drafts/Check_E11b_AF_Trial_Holdout_Subjects.md`
  - 25. `drafts/Result_E11b_AF_Trial_Holdout_Subjects.md`
- **Part D. Applied to the deliverables**
  - 26. `proposal/SUPERVISOR_RECONFIRMATION_E1_E11.md`
  - 27. `slides/README.md`


---

# Part A. Handover (state at 3 November 2026)


## 1. `handover/00_HANDOVER.md`

### Handover: ESVEA smartwatch PhD proposal (state as of 3 November 2026)

Read this first. It replaces the long conversation history. Everything here was true at handover; anything marked **open** still needs action.

---

#### 1. Who, what, where

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

#### 2. File map (this zip)

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

#### 3. The study in one page

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

#### 4. Deep-learning architecture (proposal Section 3.4, Figure 3.2)

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

#### 5. Results so far

##### 5.1 RO1 preliminary (Icentia11k, 298 of 300 sampled patients, median 57.5 h each)
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

##### 5.2 Cross-device pilot (beat-graph rhythm classifier; evaluation mode, score weight 0.9, CIs resample subjects)

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

##### 5.3 Pulsewatch beat-retention pre-check (8 subjects): **NOT PASSED** under the locked rule
- Criterion 1, above chance at high motion: **met**. Excess was +0.273 (95% CI +0.180 to +0.336) at 0.5–1 m/s², and +0.197 (+0.122 to +0.254) at ≥1 m/s².
- Criterion 2, falls with motion within subjects: **met** (8/8; one subject near chance).
- Criterion 3, detector comparable: **not met**. Project detector 0.850 vs authors' peaks 0.752; pooled gap 0.097 (limit 0.05), largest subject gap 0.146 (limit 0.10).
- **Decision (made after results):**
  - The motion term stays, to be estimated on Pulsewatch in RO2.
  - The estimate is reported with a detector sensitivity analysis.
  - Primary detector: an Elgendi et al. (2013) systolic-peak implementation on all segments; the authors' peaks are the alternative on labelled segments.
  - A lag method independent of labelled segments is to be developed in RO2. The current one reached only 2.5% of excluded and 0.8% of no-label segments.
- **Never claim:** a π̂ value; that the test passed; that either detector is more accurate; that missed matches are the PPG's fault; anything AF-specific; data-use permission.

##### 5.4 Simulation for the participant-level estimate (`analyses/kappa_simulation/`)
- **Calibration:** matched to Måneheim et al. (2024) 1-day and 7-day sensitivities (76.6%, 88.8%), ESVEA 25.3%, Ding et al. (2023) wear, and Merschel & Reinhardt (2022) usable time (71.5%, >94% at night).
- **Result:** pooling by block is as accurate as shrinkage and better than averaging only fully covered days under poor coverage. With poor coverage, median error is ~14% vs ~20%, and misclassification 2.7–3.3% vs 4.2–4.4%. λ from 0.5 to 4 h changes ESVEA class in ≤3% of participants.
- **Limits:**
  - retention and PAC identification treated as perfect
  - each unknown swept at two values
  - the Måneheim threshold mapping is assumed

##### 5.5 Icentia11k clock time
- Headers read: 9 of 9, plus 59 of 60 random headers. None has a date, time or comments, and segments are 69.9 min.
- Hence: no time-of-day analysis on Icentia11k; patient-level reference rate; pseudo-days in RO4a.

---

#### 6. Caveats the panel will probe (and the agreed answers)

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

#### 7. Plan for the real research (Table 6.1; S1 = Sem 2 2025/26, S7 = Sem 2 2028/29)

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

#### 8. Open items

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

#### 9. Slide deck

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

#### 10. How to edit and rebuild the proposal

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

#### 11. Review paper (separate deliverable)

- **Latest:** `review_paper/RBME_Review_Stroke_Recurrence_ML_DL_v2_verified.docx`. It's the version with affiliations: 69 studies, 42 recurrence, 4 of 42 externally validated, calibration in 17, 2 of 18 signal studies quantified data loss.
- **Corrections made:**
  - Chen 2024 is subject-independent, not subject-dependent.
  - PRERISK c-index 0.885 with patient-level 5-fold CV.
  - García-Terriza: composite outcome, 500 patients, 34 events, window-level CV.
- **Still unverifiable:** whether the Vodencarevic nested-CV folds were grouped by patient. The text says "double nested cross-validation".
- **In the proposal** it's cited as: Amin, R., Raj, B., & Ahmedy, I. (2026). *From static prediction to continuous monitoring: A taxonomy-based systematic review…* [Unpublished manuscript]. FCSIT, Universiti Malaya.


## 2. `handover/decisions/README.md`

### Decision documents

Live versions are in the claude.ai Project "research-proposal":
- claude/proposal-defence-decisions.md (part 1, 20 October 2026; copy here as proposal-defence-decisions_part1.md, may be an earlier upload)
- claude/proposal-decisions-2026-11-02.md (part 2; takes precedence where they differ)
- claude/proposal-audit-plan.md
- claude/um-proposal-defence-report-requirements.md (UM IAS and FSKTM rules: 3,000 to 7,000 words, line and page numbers, A4, Times New Roman 12, double spacing, left margin 4 cm, APA 7, panel weights)
- claude/review-reference-corrections.md

Where any of these conflict with the proposal docx, the proposal is authoritative (it carries the latest decisions).


## 3. `handover/decisions/proposal-defence-decisions_part1.md`

### Proposal Defence — Decision Log

**Thesis:** Estimating Atrial Ectopy Burden from Smartwatch Beat Intervals: A Two-Scale Spatio-Temporal Graph Neural Network and Its Feasibility in Post-Stroke Survivors
**Candidate:** Ridhwan Amin (25118475) · Universiti Malaya, FCSIT
**Purpose:** Record each structural decision before the deck is rebuilt.
**Last updated:** 20 October 2026

| # | Decision | Status |
|---|---|---|
| 1 | RO4 framing | **Decided: Option C + pulse-deficit amendment** |
| 2 | RO3 numbers (n, duration, site) | Open |
| 3 | Presentation slot length | Open |
| 4 | Output format | Open |
| 5 | Literature depth | Open |

---

#### Item 1 — RO4 framing ✅ DECIDED

##### Problem
The original RQ4.2 claimed *substitution* for the Holter-derived ectopy term and measured it with net reclassification improvement (NRI). NRI is defined over events and non-events, so it requires an observed outcome or reference classification (Pencina et al., 2014). The prospective cohort has neither: no concurrent ECG (a stated design boundary) and no AF follow-up.

##### Options considered
| Option | Description | Outcome |
|---|---|---|
| A | Holter on a subset of the cohort | Rejected as primary — reverses the "no concurrent ECG" boundary; kept as optional add-on (see Next steps) |
| B | AF follow-up as outcome | Rejected — expected AF ≈ 9% at 24 months (from Haeusler et al., 2025: ESVEA 25.3%, AF 18.5% vs 5.9%) → ~3 events at n = 30 |
| **C** | **Split RO4: retrospective substitution on Icentia11k + prospective comparative selection** | **Selected** |
| D | Drop substitution; comparative selection only | Rejected — weakest contribution |

##### Final wording
**RQ4.** Does substituting a smartwatch-derived ectopy estimate for the ECG-derived count change patients' ESVEA classification, and how do wearable-based selections compare with clinical risk scores?

**RO4.** To determine
- **(a)** the reclassification of ESVEA status when ECG-derived counts are replaced by estimates from simulated smartwatch intervals, degraded by quality-based rejection, coverage gaps and pulse deficit calibrated from measured data; and
- **(b)** the agreement and composition of wearable-based versus score-based selections in post-stroke survivors.

##### Design
| | RO4a — Substitution | RO4b — Comparative selection |
|---|---|---|
| Data | Icentia11k, degraded to Garmin-like output | RO3 cohort + routine records |
| Truth | ECG beat labels | None required (agreement only) |
| Metrics | Reclassification rate; κ at ESVEA cut-off; sensitivity/specificity of wearable ESVEA across degradation severities | Cohen's κ; Jaccard overlap; profile of discordant patients; association with atrial substrate markers |
| Removed | NRI on PROACTIA | — |

##### Degradation model (amendment from revalidation)
| Operator | What it simulates | Calibrated from |
|---|---|---|
| Interval rejection | Quality-based beat filtering | RO1 results |
| Coverage gaps | Non-wear, charging, unusable PPG | Gruwez et al. (2021); Aguilar et al. (2025); RO3 cohort once collected |
| **Pulse deficit (beat merging)** | Premature beat produces no detectable wrist pulse → short + long interval seen as one long interval | Pulsewatch paired PPG–ECG; fallback: published PVC pulse-deficit evidence |

Results reported across a severity sweep for each operator, not a single setting.

##### Evidence from revalidation (Consensus, PubMed, Scholar Gateway)
| Claim | Finding | Source |
|---|---|---|
| Simulating wearable monitoring from continuous records is accepted method | Smartwatch algorithms simulated on implantable-monitor data (CIRCA-DOSE, n = 346), daytime wear; >90% sensitivity with 24-h wear | Aguilar et al. (2025); also Aguilar et al. (2021), Quer et al. (2020), Ziegler et al. (2006) |
| Garmin PPG intervals degrade beat-level variability | Garmin vívoactive 4 vs ECG in 129 ischaemic stroke patients: near-perfect global agreement, rMSSD only moderate (ρc = 0.66) | Theurl et al. (2023) |
| Pulse deficit is real | PVCs with and without observable PPG pulse; PVC pulse may be too weak to detect | Sološenko et al. (2015); Argüello Prada et al. (2026); Kovoor et al. (2021) |
| PAC-specific pulse deficit | Evidence thin — named as a gap, addressed by calibration | — |
| NRI requires an outcome | Defined over events/non-events | Pencina et al. (2014) |
| Gap 1 still holds | Smartwatch AF burden widely validated; no study reports a smartwatch-derived daily PAC count | Zuo et al. (2026); Poh et al. (2023); Anagnostopoulos et al. (2025) |

##### Slides affected
| Slide | Change |
|---|---|
| RQ ↔ RO | New RQ4/RO4 wording |
| Scope & Delimitations | Add: substitution tested by simulation, not concurrent ECG |
| Literature tables | Add Aguilar et al. (2025); add Theurl et al. (2023) |
| Gap 4 | Reword to "reclassification under realistic device losses" |
| RO4 design | Two-part table + three-operator degradation model |
| Validation matrix (new) | RO4a truth = Icentia11k labels; RO4b agreement only |
| Data Analysis Plan | Remove NRI; add reclassification rate, κ, sensitivity/specificity across severities |
| Risks (new) | Simulation optimism → calibrated operators + severity sweep |
| Contributions | Reword RO4 bullet |

##### Next steps to lock item 1
- [ ] Confirm Icentia11k annotation procedure (adjudicated vs technician-reviewed) — Tan et al. (2019) / PhysioNet record
- [ ] Confirm Pulsewatch access includes reference ECG alongside PPG
- [ ] Ask supervisors whether a hospital collaborator runs routine Holter on post-stroke patients (optional paired subset)

---

#### Item 2 — RO3 numbers ⏳ OPEN

| Sub-decision | Options | Recommendation |
|---|---|---|
| Sample size | n = 30, or supervisor-specified | n = 30, justified by precision of coverage proportion (Wilson 95% CI half-width ≈ ±17% at 50%) |
| Monitoring duration | (a) 4 calendar days, ≥3 days at ≥95% coverage; (b) 7 days | Decide; current deck conflicts ("72 h over 4 days" vs "3 days") |
| Site | Named site or explicit placeholder | — |

Note from revalidation: Huntelaar et al. (2024) found 92.5% of cryptogenic stroke candidates ineligible and halted enrolment — argues for broad eligibility, not a cryptogenic-only cohort.

#### Item 3 — Presentation slot length ⏳ OPEN

| Slot | Main deck |
|---|---|
| 25–30 min (assumed) | ~28 slides |
| 15–20 min | ~18 slides; more moved to appendix |

#### Item 4 — Output format ⏳ OPEN

| Option | Notes |
|---|---|
| Claude Slides (recommended) | Editable; downloads as .pptx or PDF |
| PowerPoint file | If editing continues in PowerPoint or UM requires a template |

#### Item 5 — Literature depth ⏳ OPEN

| Option | Notes |
|---|---|
| Verify + extend (recommended) | Check existing citations and add 2025–2026 work |
| Verify only | Check existing citations only |

---

#### References (item 1)
- Aguilar, M., et al. (2021). *Circulation*. https://doi.org/10.1161/circulationaha.121.056109
- Aguilar, M., et al. (2025). *Europace*. https://doi.org/10.1093/europace/euaf280
- Anagnostopoulos, I., et al. (2025). *J Cardiovasc Dev Dis*. https://doi.org/10.3390/jcdd12040122
- Argüello Prada, E. J., et al. (2026). *Biomed Signal Process Control*. https://doi.org/10.1016/j.bspc.2026.110638
- Bulut, M. G., et al. (2025). *PLOS ONE*. https://doi.org/10.1371/journal.pone.0314154
- Haeusler, K. G., et al. (2025). *J Am Heart Assoc*. https://doi.org/10.1161/JAHA.123.034512
- Huntelaar, M., et al. (2024). *Front Stroke*. https://doi.org/10.3389/fstro.2024.1496003
- Kovoor, J., et al. (2021). *HeartRhythm Case Rep*. https://doi.org/10.1016/j.hrcr.2021.05.015
- Pencina, K. M., Pencina, M. J., & D'Agostino, R. B. (2014). *Stat Med*, 33(28), 4975–4987. https://doi.org/10.1002/sim.6286
- Poh, M., et al. (2023). *J Am Heart Assoc*. https://doi.org/10.1161/jaha.123.030543
- Quer, G., et al. (2020). *Europace*. https://doi.org/10.1093/europace/euaa186
- Sološenko, A., et al. (2015). *IEEE Trans Biomed Circuits Syst*. https://doi.org/10.1109/tbcas.2015.2477437
- Tan, S., et al. (2019). *arXiv*. https://doi.org/10.48550/arxiv.1910.09570
- Theurl, F., et al. (2023). *Eur Heart J Digit Health*. https://doi.org/10.1093/ehjdh/ztad022
- Ziegler, P., et al. (2006). *Heart Rhythm*. https://doi.org/10.1016/j.hrthm.2006.07.030
- Zuo, S., et al. (2026). *JACC Clin Electrophysiol*. https://doi.org/10.1016/j.jacep.2026.03.036


## 4. `handover/decisions/proposal-decisions-2026-11-02.md`

### Proposal Defence: Decision Log, part 2 (2 November 2026)

Continues claude/proposal-defence-decisions.md. Where they differ, this file takes precedence.

#### Item 6: Estimator, validation and data decisions ✅ DECIDED (2 November 2026)

These supersede earlier entries where they differ (notably item 2a's primary ESVEA rate form, and item 1's optional Holter subset).

| # | Decision | Basis |
|---|---|---|
| 6a | **No concurrent ECG in RO3, including no ECG-patch substudy** (confirmed by Dr. Bryan Raj). Retention on the Garmin is not estimated directly; transfer from Pulsewatch (Samsung) is a stated assumption | Supervisor decision |
| 6b | **Aim reworded:** error characterised against ECG labels under simulated smartwatch losses, coverage adequate after stroke, "as a step towards" comparison with ECG thresholds. Real-device error is a stated limitation | Independent review, Critical 1 |
| 6c | **ESVEA primary criterion ≥480 supraventricular beats per day** (Haeusler et al., 2025, MonDAFIS, stroke cohort); ≥30 per hour (Binici et al., 2010) secondary; runs reported separately | Definition checked on PubMed |
| 6d | **Four 6-hour blocks** (00–06, 06–12, 12–18, 18–24 h); block weights wₕ = Lₕ/24 (Equation 3.2), not a diurnal profile | Icentia11k segments carry no clock time |
| 6e | **Coverage:** day/night rule for RO3 valid days (primary outcome unchanged); per-block rule before a daily count is reported (Equation 3.3) | Avoids empty-block bias |
| 6f | **ESVEA status from the participant count pooled by block across valid days** (Equation 3.4); per-day values for stability; shrinkage towards Larsen et al. (2016) profile as sensitivity, λ = 1 h (0.5 to 4 h) | Calibrated simulation (Appendix C) |
| 6g | **Equation 3.1:** π̂ₖ(m) = π̂_class(k) · π̂_motion(m); class from RO1 (Icentia11k), motion from Pulsewatch with per-session lag; product is an assumption | Pulsewatch data check |
| 6h | **Pulsewatch retention pre-check: not passed** under the locked rule (criteria 1 and 2 met; detector criterion not met: 0.850 vs 0.752). Motion term kept for RO2 with a detector sensitivity analysis (project Elgendi-style detector primary, authors' peaks alternative) and a lag method not dependent on labelled segments, to be developed in RO2. No π̂ value claimed | Pulsewatch_Beat_Retention_Precheck_Config.md |
| 6i | **RO4a uses Icentia11k patients held out from RO1 calibration and RO2 training**; test degradations sampled independently of the training simulation | Independent review, Critical 2 |
| 6j | **H1 replaced:** PAC retention after filtering varies with burden in new Icentia11k patients (mixed-effects logistic regression) | Old H1 true by construction |
| 6k | **RO2 analysis:** one primary contrast (H2) by paired subject-level bootstrap; other contrasts with Holm correction | Review |

**Still open:** thesis submission date for the schedule; exact pilot AUROC and subject-split confirmation (Check_Pilot_AUROC_and_Subject_Split.md); recruitment site; Pulsewatch permitted use to be confirmed with the data contact.


## 5. `handover/decisions/proposal-audit-plan.md`

### Proposal audit against the UM FSKTM Proposal Defence checklist, and revision plan

Audit date: 30 October 2026. Audited file: the current research proposal (34 pages, about 6,990 words including tables). No changes have been made yet.

#### Step 1. Revalidation of the checklist

| Checklist claim | Status | Evidence |
|---|---|---|
| Conduct of Candidature Seminars: PhD by research presents "not later than the second semester"; 4 copies; 3,000 to 7,000 words; two weeks before | Confirmed | FSKTM PDF (24.conduct-of-candidature-seminars.pdf) |
| Application Guideline: "not later than third semester"; report one week before; Active (AK) status; supervisor approval | Confirmed | FSKTM PDF (5- Application-Guideline-PD-CD.pdf) |
| The two documents conflict; neither carries a date or version | Confirmed | Neither PDF shows a date |
| Eight required report contents (Section 1.3) | Confirmed, word for word | Conduct of Candidature Seminars |
| "Not an official UM marking rubric" | Correct, but incomplete | An official IAS panel evaluation form exists: title and abstract 5, introduction 25, literature 25, methods 20, summary 5, style and references 10, communication 10; pass mark 65. Use it to weight effort. |
| Presentation duration "communicated by FSKTM" | Incomplete | The IAS guideline (2025) gives 15 to 20 min presentation plus 10 to 20 min Q&A, line and page numbers, and a softcopy to ias_seminar@um.edu.my two weeks ahead |
| Generative-AI use "according to current UM/FSKTM guidance" (13.3) | Needs updating | UM AI Policy and Guidelines (Senate approved 20 November 2025, effective Session 2025/2026 Sem 2): formal AI-use declaration (Appendix 2(b)) for theses, dissertations and research reports; cross-check AI outputs against original sources; and Section 7(5): no uploading of a thesis, dissertation or research report to a public AI platform before Senate finalises assessment, except with written supervisor consent. The policy does not mention proposals explicitly, so ask the supervisor whether a declaration is needed and whether current AI-assisted drafting is covered by their consent. |

Verdict: the checklist is accurate. Three additions are needed: the IAS panel weights, the IAS presentation format, and the November 2025 UM AI policy.

#### Step 2. Audit findings

Ratings follow the checklist: Critical, Major, Minor, or Keep (meets the item; no revision).

##### Keep without revision
- Required content areas (1.3): all eight present.
- Title (2.1): names the problem, method, population and device; promises no results.
- Problem statement (3): all five links present (current practice, limitation, evidence, consequence, need), with a documented search behind "not quantified".
- Literature synthesis (4.2): grouped by theme (selector, scores, wearable detection, coverage, models), not paper by paper.
- Framework figures (7): conceptual framework and architecture are numbered, captioned, explained, and the novelty boxes are marked.
- Validation design (8.5, 9.1 to 9.4): validation matrix with "cannot claim" column, strong baselines, ablations, subject-wise splits, PROBAST+AI reporting, calibration, severity sweep.
- Preliminary findings (1.3): real results (Icentia11k) plus a clearly limited pilot.
- Clinical restraint (10): ectopy framed as a selector, no anticoagulation or recurrence claims.

##### Critical
| # | Checklist item | Finding | Planned revision |
|---|---|---|---|
| C1 | 6.1, 6.3 Originality vs closest prior work | No section names the 3 to 5 closest studies and states what this thesis adds beyond each. Novelty is spread across significance and gaps. This is the panel's most likely attack. | Add a short "Closest prior work and contribution" subsection with a table: Han 2026 (Pulsewatch Bi-GRU), Chen 2024 (Pulsewatch DenseNet; PAC/PVC sensitivity 0.664, falling to 0.143 and 0.373 externally), Bhurane 2026, Schoels 2025 (beat intervals, ectopy interpolated away), Siejko 2025 (daily PVC burden from an implanted monitor). Columns: what it does, what remains, what this study adds. Then name each contribution by type: methodological (quality flag as evidence with retention weighting), empirical/measurement (error profile of a daily count; filtering loss), feasibility evidence (RO3). |
| C2 | 13.1 No contradictions; 13.2 accurate citations | The proposal cites the candidate's review with superseded figures ("30 studies, 20 recurrence, calibration in 5 of 30"). The verified review now reports 69 studies, 42 recurrence, 18 signal-based, calibration in 17, external validation in 4 of 42. The citation also lacks the title and third author. | Update Section 2.1, Section 3.7 and the reference to: Amin, R., Raj, B., & Ahmedy, I. (2026). From static prediction to continuous monitoring: A taxonomy-based systematic review... Note: the review's own abstract still says the in-hospital signal study had "unreported validation"; its body now says composite outcome with window-level cross-validation. Fix the review abstract too so both documents agree. |
| C3 | 11.1, 11.2 Feasibility of RO3 | Recruitment site is still "to be confirmed" and the device is not yet received. Both are stated, but there is no fallback that preserves a research question if RO3 cannot run. | Add a fallback: if recruitment or the device fails, RO3 becomes a device-verification study plus coverage analysis of Pulsewatch wear data, and RO4b is dropped while RO4a stands. Ask the supervisor to fix the site before submission (an admin action, not writing). |

##### Major
| # | Checklist item | Finding | Planned revision |
|---|---|---|---|
| M1 | 5.1 One overarching aim | No aim statement; only four objectives. | Add one aim sentence at the start of 1.3 and in the abstract. |
| M2 | 5.3 Hypotheses | None stated, although RQ1 to RQ3 are testable. | Add three hypotheses under Table 1.1: H1 filtering removes PAC intervals disproportionately (already supported by Section 4.2); H2 the ST-GNN gives lower daily-count error than the best non-graph baseline; H3 at least 75% of participants yield 3 valid days. |
| M3 | 8.3 Precision of the method | No equations. The estimator is described only in prose. | Add 2 or 3 numbered equations: the retention-weighted daily rate (inverse-probability weighting of retained beats), the retention model as a function of motion and time of day, and the coverage-gate rule. |
| M4 | 12 Value if the method does not improve | Not stated. | Add 2 sentences: RO1, RO3 and the retention correction stand on their own; a negative RQ2.1 result (graph no better) is reported as evidence for simpler models. |
| M5 | 8.2 Data access and licences | Licences and access status are not stated. Icentia11k is CC BY-NC-SA 4.0 (non-commercial). Pulsewatch access route (Synapse) and approval status are not stated. | Add a small data table: dataset, owner, access route, licence, status, fallback. You need to confirm the Pulsewatch access status. |
| M6 | 8.4, 9.6 Environment and reproducibility | No software, compute, seeds, versions or code-sharing plan. | Add one paragraph: Python and PyTorch Geometric, GPU source, fixed seeds and versioned configs, code released on publication, RO3 protocol pre-registered. Note that RO2 uses beat annotations, not the 1.1 TB raw signals, so storage is modest. |
| M7 | 10 Ethics | No protocol for incidental findings (a watch may show possible AF or high ectopy in a participant). No description of the device data route (Garmin cloud vs direct export). No AI-use declaration. | Add: incidental findings are not reviewed in real time and participants are told so; any device AF alert follows usual care with notice to the treating physician; data route keeps identifiable data off consumer accounts where possible; AI-use declaration per the UM November 2025 policy if the supervisor confirms it applies. |
| M8 | 11.2 Risk prioritisation | The risk table has no likelihood or impact. | Add likelihood and impact columns (High, Medium, Low). |
| M9 | 11.3 Measurable milestones | The schedule lists tasks, not milestones. | Add milestones: M1 device verified, M2 ethics approved, M3 RO1 paper submitted, M4 first 20 participants, M5 RO2 model frozen, M6 candidature defence. |
| M10 | 4.3, 5.4 Comparison and traceability matrices | Tables 2.1 and 2.2 are partial matrices. There is no single objective, method, data, evaluation and deliverable traceability table. | Merge Tables 3.1 and 3.5 into one traceability matrix with a "deliverable" column. Put a fuller literature comparison matrix in an appendix. |

##### Minor
| # | Finding | Planned revision |
|---|---|---|
| m1 | Abbreviations: ESUS never defined; PPV used in 2.1 before definition; PAC used in the abstract before definition; ST-GNN not redefined in the body; "RR" means both risk ratio and RR interval; ICC and MAE undefined. | Define at first use; replace "risk ratio [RR]" with plain words. |
| m2 | Yang et al. (2022): HR 2.91 is for AF in stroke patients; the null result is recurrent ischaemic stroke or TIA. | Align wording with the verified review. |
| m3 | Grey literature (Vargova accepted abstract, Garmin white paper, conference abstracts) is not labelled as such in the text. | Add one sentence in 2.7 noting which sources are abstracts or technical documents. |
| m4 | "First" claims in the abstract and 5.1. | Qualify with "to our knowledge, based on the documented search". |
| m5 | Deliverables vs contributions (12). | One line separating deliverables (code, protocol, dataset of RO3 summaries) from contributions. |
| m6 | Repeated seeds and hyperparameter sensitivity not mentioned (9.3, 9.4). | Add to the analysis plan. |

##### Slides (checklist 14)
The deck already covers 14 of the 16 suggested slides. Planned changes:
- Add a "Closest prior work and contribution" slide before the framework (mirrors C1).
- Add a short "Ethics and data access" slide (M5, M7), or fold it into risks.
- Update every slide that cites review figures (C2), and keep the deck consistent with all report changes (FCSIT requires consistency).
- End on a one-line contribution statement.

#### Step 3. Word-count strategy
The report is at about 6,990 of 7,000 words counting tables. The revisions add roughly 900 to 1,000 words. Plan:
1. Ask the Postgraduate Office whether tables, references and appendices count (admin action A2).
2. Regardless, move the full literature matrix and the closest-prior-work detail to appendices, keep the main text tables short, and trim about 300 words from Chapter 2 and Section 1.1 background.
3. Target: main text at or under 7,000 words including tables; appendices outside the count if confirmed.

#### Step 4. Actions only you can do (not writing)
| # | Action | Checklist |
|---|---|---|
| A1 | Confirm which deadline applies (semester 2 vs 3; two weeks vs one week), number of copies, and submission channel, in writing | 1.2 |
| A2 | Confirm what the 3,000 to 7,000 words include | 1.2 |
| A3 | Confirm recruitment site with supervisors | 11.1 |
| A4 | Confirm Pulsewatch data access status | 8.2 |
| A5 | Ask the supervisor about the AI-use declaration and the upload restriction in the UM November 2025 AI Guidelines | 10, 13.3 |
| A6 | Active (AK) status, application form, supervisor approval, evidence folder | 1.1, 1.4 |
| A7 | Mock defence and the examiner questions in Section 15 | 14, 15 |

#### Step 5. Implementation order (after approval)
1. C2 and m1 to m4 (accuracy fixes).
2. C1, M1, M2, M4 (argument: aim, hypotheses, novelty, value of negative results).
3. M3, M5, M6, M7, M10 (methods precision and governance).
4. C3, M8, M9 (feasibility, risks, milestones).
5. Word-count pass, rebuild, render check.
6. Slide updates for consistency.

#### Sources
- FSKTM Conduct of Candidature Seminars: https://fsktm.um.edu.my/fsktm/doc/postgraduate/24.conduct-of-candidature-seminars.pdf
- FSKTM Application Guideline: https://fsktm.um.edu.my/fsktm/doc/postgraduate/5-%20Application-Guideline-PD-CD.pdf
- UM Policy and Guidelines on AI (IAS compilation, Final V3): https://ias.um.edu.my/Student%20Affairs/Guideline/Compilation%20Policy%20%26%20GP%20AI%20-%20Final%20V3.pdf
- UM announcement of the AI policy: https://spm.um.edu.my/2026/03/15/universiti-malaya-releases-policy-and-guidelines-on-the-use-of-artificial-intelligence-in-teaching-and-learning/

#### Implementation status (30 October 2026)
All writing items C1 to C3, M1 to M10 and m1 to m6 were implemented in the proposal (main text about 6,975 words including tables; Appendix A literature matrix and Appendix B definitions and data sources added). Slides updated: aim and hypotheses, closest prior work, risks with likelihood and fallback, ethics and data access, appendix equations, contribution statement, seventh references slide. Review abstract and conclusion aligned with the corrected García-Terriza description. Actions A1 to A7 remain with the candidate.


## 6. `handover/decisions/UM_FSKTM_PhD_Proposal_Defence_Checklist.md`

### UM FSKTM PhD Proposal Defence — Detailed Readiness Checklist

**Institution:** Universiti Malaya (UM)  
**Faculty:** Faculty of Computer Science and Information Technology (FSKTM)  
**Assessment:** PhD by Research — Proposal Defence  
**Checklist prepared:** 30 October 2026  
**Purpose:** A practical self-audit of the research proposal, technical quality, defence presentation and administrative preparation.

> **Important status note:** This is a preparation and quality-assurance checklist, not an official UM marking rubric. The faculty's published documents should be checked before submission. In particular, the FSKTM website currently hosts two Proposal Defence documents with different deadlines and submission lead times. See **Section 1.2** and confirm the applicable requirement with the FSKTM Postgraduate Office and supervisor.

---

#### How to use this checklist

- Tick an item only after checking the actual proposal, evidence, or administrative record.
- Use **N/A** for requirements that genuinely do not apply to the research design. Do not use N/A simply because an item has not yet been addressed.
- Classify unresolved items as:
  - **Critical:** could undermine the validity, originality, ethics, feasibility, or approval of the proposal.
  - **Major:** materially weakens the research argument or defence readiness.
  - **Minor:** mainly a clarity, presentation, or document-quality issue.
- The technical sections are deliberately written for Computer Science research. Adapt the algorithm, data, system, evaluation and reproducibility checks to the actual research paradigm; not every item applies to every PhD.

#### 1. UM / FSKTM administrative and submission checks

These are process checks, not judgements of research quality.

##### 1.1 Candidate and application status

- [ ] I am registered as an **active (AK)** candidate in the semester in which the Proposal Defence will be held.
- [ ] My candidature details, programme, research mode and semester count are correct in the university system.
- [ ] I have discussed the intended Proposal Defence date with my supervisor(s).
- [ ] I have obtained the supervisor's approval/permission before applying.
- [ ] I know the current faculty process for applying, including the required form, report format, submission channel and person responsible.
- [ ] I have confirmed whether the presentation will be physical, online or hybrid, and the applicable arrangements.
- [ ] I know the presentation duration, question-and-answer duration and any slide/report requirements communicated by FSKTM.

##### 1.2 Verify the deadline and report-submission rules — documents differ

The FSKTM website lists both of the following documents:

| Published document | Proposal Defence timing for a PhD by research | Report submission requirement stated | Practical treatment |
|---|---|---|---|
| **Conduct of Candidature Seminars** (linked from the FSKTM Guidelines and Policies page) | Not later than the **second semester** for doctoral candidates by research | **Four copies** of a complete proposal report, **3,000–7,000 words**, submitted at least **two weeks** before the presentation | Treat this as an important current faculty-published reference, but confirm applicability to your cohort and programme. |
| **Guidelines for Application of the Proposal Defence, Confirmation Defence, Candidature Defence and Thesis Seminar** | Not later than the **third semester** for PhD candidates | Proposal Defence report submitted at least **one week** before the presentation | This document appears older and conflicts with the other published document. Do not rely on it without confirmation. |

**Action required before submission:**

- [ ] I have asked the FSKTM Postgraduate Office which semester deadline applies to my intake/cohort and research-mode registration.
- [ ] I have confirmed the required number of copies (printed and/or electronic).
- [ ] I have confirmed the applicable word-count range and what is excluded from the count (e.g. references, appendices, tables and figures).
- [ ] I have confirmed the submission deadline and whether it is measured in calendar days or working days.
- [ ] I have retained written confirmation (email or official notice) of the requirements.

**Do not assume that the third-semester / one-week rule overrides the second-semester / two-week rule.** The faculty should clarify which document governs your case. The general UM candidature-seminar document may also be relevant, but the faculty should confirm how it applies to your cohort.

##### 1.3 Proposal report content listed in the FSKTM-hosted seminar guideline

Check that the proposal report covers each of these published content areas:

- [ ] Introduction, statement of the problem and scope of the research.
- [ ] Research objectives.
- [ ] Summary of the literature review.
- [ ] Conceptual framework, or summary of experimental methods / research design and required equipment, as appropriate.
- [ ] Importance and relevance of the study.
- [ ] Preliminary findings or pilot test, **if available**. If no preliminary findings exist, state that clearly rather than implying results.
- [ ] Proposed work schedule based on the intended thesis-submission date.
- [ ] Brief bibliography.

The detailed academic checklist in Sections 2–8 expands these broad items for a Computer Science PhD proposal.

##### 1.4 Administrative evidence folder

- [ ] Latest supervisor-approved proposal file is saved separately from earlier drafts.
- [ ] Required application form(s) are complete and signed where necessary.
- [ ] Supervisor approval is documented.
- [ ] Submission email/portal receipt is saved.
- [ ] Faculty instructions, presentation notice and any assessor instructions are saved.
- [ ] A copy of the exact submitted report and slides is retained.

---

#### 2. Title, abstract, background and research scope

##### 2.1 Research title

- [ ] The title identifies the main research problem or phenomenon.
- [ ] The title identifies the principal method, system, population, domain or context where necessary.
- [ ] The title is specific enough to distinguish the research from a broad topic area.
- [ ] The title does not promise outcomes that the proposed method or evidence cannot support.
- [ ] Key terms in the title are used consistently throughout the proposal.
- [ ] The title has been discussed with the supervisor and checked against any faculty approval process.

**Quality test:** A reader should be able to infer the subject, scope and broad research approach from the title without reading the entire proposal.

##### 2.2 Abstract or proposal summary

- [ ] The research area and context are introduced briefly.
- [ ] The specific problem is stated, not merely the general topic.
- [ ] The research gap is summarised.
- [ ] The aim and principal objectives are stated.
- [ ] The proposed research approach is described at a level appropriate for an abstract.
- [ ] The expected contribution is identified without claiming results that have not yet been obtained.
- [ ] The abstract is consistent with the title, objectives, scope and methodology.

##### 2.3 Background and motivation

- [ ] The background moves logically from the broad domain to the specific problem.
- [ ] Important claims are supported by reliable academic or authoritative sources.
- [ ] The context is supported by relevant facts, studies, datasets, technical constraints or documented practice.
- [ ] The motivation explains why the problem matters scientifically or technically.
- [ ] The proposal distinguishes practical motivation from the academic research problem.
- [ ] The background does not become an extended general introduction unrelated to the objectives.

##### 2.4 Scope and boundaries

- [ ] The application/domain context is defined.
- [ ] The target users, population, systems, devices or environments are specified, where relevant.
- [ ] The data types, modalities, variables or system components in scope are identified.
- [ ] The geographical, temporal, technical or operational boundaries are stated where relevant.
- [ ] The proposal states what is deliberately outside the scope.
- [ ] Assumptions and dependencies are made explicit.
- [ ] The scope is achievable within the permitted candidature period and available resources.

**Quality test:** An examiner should be able to state what the project will and will not attempt to solve.

---

#### 3. Problem statement and research justification

- [ ] The problem is written as a specific research problem, not only as a broad societal or industrial challenge.
- [ ] The problem is supported by evidence from the literature, empirical observations, datasets, standards or credible reports.
- [ ] The proposal identifies who or what is affected by the problem.
- [ ] The consequences of the problem are explained (e.g. reduced accuracy, poor generalisation, latency, high resource use, low reliability, usability limitations or theoretical uncertainty).
- [ ] The current state of the art is described accurately.
- [ ] The limitations of existing methods are specific and supported by cited studies or measured evidence.
- [ ] The proposal distinguishes a limitation in prior research from a limitation in the researcher's own proposed design.
- [ ] The problem statement leads logically to the research gap.
- [ ] The problem is sufficiently important and researchable for doctoral-level work.
- [ ] The proposal does not rely on unsupported claims such as “no studies have investigated this” without a documented search and clear qualification.

##### Problem-statement structure to test

A strong problem statement usually makes the following chain explicit:

1. **Current situation:** What is known or currently done?
2. **Specific limitation:** What remains inadequate, unresolved or poorly understood?
3. **Evidence:** Which studies, measurements or observations demonstrate the limitation?
4. **Consequence:** Why does the limitation matter?
5. **Research need:** What must be investigated to address it?

- [ ] All five parts can be identified in the written problem statement.

---

#### 4. Literature review, synthesis and research gap

##### 4.1 Literature coverage

- [ ] The review includes seminal or foundational work where necessary.
- [ ] The review includes recent, relevant work up to the proposal's literature-search cut-off date.
- [ ] Sources include relevant peer-reviewed journals and reputable conference proceedings for the research field.
- [ ] Important methods, benchmarks, datasets and evaluation practices in the field are covered.
- [ ] Sources are relevant to the exact problem, not included only because they use a similar keyword.
- [ ] Relevant conflicting findings or competing approaches are acknowledged.
- [ ] The review distinguishes peer-reviewed publications from preprints, technical reports, documentation and other grey literature.
- [ ] The proposal avoids relying heavily on vendor marketing material or unverified online claims for academic arguments.

##### 4.2 Critical synthesis

- [ ] Studies are grouped into meaningful themes, method families, research questions or generations of approaches.
- [ ] The proposal explains how approaches differ, rather than listing papers one by one.
- [ ] Strengths and limitations are compared using consistent criteria.
- [ ] The assumptions and experimental settings of prior studies are considered when comparing their results.
- [ ] The proposal identifies contradictions, trade-offs or unresolved methodological issues.
- [ ] The review explains why existing solutions do not fully address the stated research problem.
- [ ] The review leads directly to the proposed research questions and methodology.

##### 4.3 Literature comparison matrix

- [ ] A comparison matrix has been prepared, even if it is placed in an appendix or working document.
- [ ] The matrix includes the most relevant studies rather than an arbitrary large sample.
- [ ] It records, where applicable: objective/problem, method, data/domain, experimental setting, baseline, metrics, principal findings, limitations and relevance to the proposed study.
- [ ] Performance numbers are compared only where datasets, splits, metrics and experimental settings are sufficiently comparable.
- [ ] The proposal does not claim that one method is superior solely because it reports a higher score under a different setup.

##### 4.4 Research gap

- [ ] The gap is stated explicitly in one or more concise paragraphs.
- [ ] The gap follows from the literature synthesis and is not introduced as an unsupported opinion.
- [ ] The gap is specific: methodological, theoretical, empirical, computational, contextual, data-related, evaluation-related or another clearly defined type.
- [ ] The gap is not merely “few studies have used this algorithm in this country/domain” unless the context produces a meaningful research question.
- [ ] The gap is not simply the absence of a software implementation or platform.
- [ ] The proposal explains why the gap has not already been resolved by existing approaches, where this can be reasonably established.
- [ ] The proposed objectives and methods directly address the gap.

**Quality test:** If the research-gap paragraph were removed, would the proposal still look like an ordinary application of existing techniques? If yes, strengthen the gap and its link to the intended contribution.

---

#### 5. Research aim, objectives, questions and hypotheses

##### 5.1 Research aim

- [ ] There is one clear overarching aim.
- [ ] The aim describes the intended research outcome, not a list of implementation activities.
- [ ] The aim is consistent with the title, problem statement, gap and scope.

##### 5.2 Research objectives

For each objective:

- [ ] It begins with a clear action verb (e.g. analyse, characterise, design, develop, formulate, evaluate, validate or compare).
- [ ] It addresses a defined part of the problem or research gap.
- [ ] It specifies an achievable research outcome.
- [ ] It can be addressed by a planned method.
- [ ] It has an identifiable form of evidence or evaluation.
- [ ] It is not merely an administrative or project-management task.
- [ ] It is neither so broad that it cannot be evaluated nor so narrow that it is only a minor implementation step.
- [ ] The objectives collectively achieve the overall aim without major gaps or unnecessary overlap.

##### 5.3 Research questions and hypotheses

- [ ] Each research question maps to at least one objective.
- [ ] Each question is answerable using the proposed data and methods.
- [ ] Each question is stated precisely enough to guide the study.
- [ ] Hypotheses are included where appropriate and are testable.
- [ ] The proposal explains the variables, expected relationships or comparison being tested, where relevant.
- [ ] The proposal avoids presenting a desired result as if it were a research question.

##### 5.4 Objective-to-method-to-evidence traceability matrix

Complete a matrix like this for every objective:

| Objective | Research question / hypothesis | Method or work package | Data / materials | Evaluation or analysis | Evidence of completion |
|---|---|---|---|---|---|
| RO1: [insert] | RQ1: [insert] | [insert] | [insert] | [insert] | [insert] |
| RO2: [insert] | RQ2: [insert] | [insert] | [insert] | [insert] | [insert] |
| RO3: [insert] | RQ3: [insert] | [insert] | [insert] | [insert] | [insert] |

- [ ] No objective is left without a method.
- [ ] No major method is included without a clear research purpose.
- [ ] Every research question can be answered using the stated evaluation or analysis.
- [ ] The expected contribution can be traced back to one or more objectives.

---

#### 6. Originality, novelty and expected contribution

This is one of the most important intellectual checks for a PhD proposal.

##### 6.1 Explain what is original

- [ ] The proposal identifies the proposed original contribution(s) explicitly.
- [ ] Each contribution is distinguished from the use, integration or implementation of existing techniques.
- [ ] The proposal explains what is new relative to the closest prior studies, not only relative to a broad collection of papers.
- [ ] The contribution is supported by the literature comparison and research-gap analysis.
- [ ] The claimed novelty is proportionate to the evidence available at proposal stage.
- [ ] The proposal distinguishes **expected contribution** from **proven contribution**; anticipated outcomes are not written as completed findings.

##### 6.2 Possible contribution types in Computer Science

Select and justify the contribution types relevant to the project:

- [ ] **Algorithmic/methodological:** a new algorithm, learning mechanism, optimisation method, inference strategy, software method or materially improved procedure.
- [ ] **Theoretical:** a formal model, proof, complexity result, analytical insight or principled explanation.
- [ ] **Architectural/systems:** a novel system architecture, protocol, resource-management method or systems design supported by research questions and rigorous evaluation.
- [ ] **Empirical:** new evidence that changes or sharpens understanding of a technical phenomenon, including carefully designed comparative or reproducibility studies.
- [ ] **Data/benchmark:** a genuinely useful dataset, benchmark, evaluation protocol or data resource with clear research value, documentation and governance.
- [ ] **Human-centred / HCI:** new evidence or design knowledge established through an appropriate research method and evaluation, not merely a user-interface build.
- [ ] **Applied/domain contribution:** a new technical insight arising from a domain-specific challenge, not only the deployment of an existing tool in a new setting.

##### 6.3 Novelty stress test

- [ ] I can name the three to five closest studies to my proposed work.
- [ ] I can explain, for each closest study, what it does and what remains unresolved.
- [ ] I can state precisely what my research will add beyond those studies.
- [ ] I can explain why the contribution matters to the relevant Computer Science research community.
- [ ] I can explain how the proposed experiments or analysis will provide evidence for the contribution.

**Warning:** Combining established algorithms, applying an existing architecture to another dataset, building a platform around an existing model, or reporting a small performance increase does not automatically establish PhD-level novelty. Such elements may be useful, but the proposal must articulate the new knowledge, method, theory or evidence they are intended to produce.

---

#### 7. Conceptual, theoretical or technical framework

- [ ] The proposal includes a conceptual, theoretical, algorithmic or system framework appropriate to the research paradigm.
- [ ] The framework identifies the main components, variables, entities or modules.
- [ ] Relationships, dependencies and information flows are shown clearly.
- [ ] Inputs, outputs, assumptions and boundaries are explained.
- [ ] The framework is linked to the research objectives and questions.
- [ ] The diagram is legible, numbered, captioned and explained in the text.
- [ ] The framework does not imply that the system has already been implemented or validated if it is only proposed.
- [ ] Any mathematical notation is defined and used consistently.

For a computational or machine-learning framework:

- [ ] The data flow from acquisition to preprocessing, modelling, inference and evaluation is clear.
- [ ] The role of each model/component is justified.
- [ ] Training, validation and testing stages are distinguished.
- [ ] Any feedback loop, optimisation process, adaptation mechanism or online component is defined.
- [ ] The framework identifies where the proposed novelty occurs, rather than presenting only a generic pipeline.

---

#### 8. Research methodology and technical design

The methodology must show not only what tools will be used, but why the research design can answer the research questions and support the claimed contribution.

##### 8.1 Overall research design

- [ ] The research paradigm/design is identified (e.g. experimental, design science, theoretical, empirical, mixed method, systems research or another justified approach).
- [ ] The sequence of research phases is explained.
- [ ] Each phase maps to an objective and deliverable.
- [ ] The design explains how evidence will be collected and analysed.
- [ ] The methodology distinguishes research activities from routine development tasks.
- [ ] The choice of method is justified against plausible alternatives.
- [ ] The design includes a way to detect failure, negative results or unexpected outcomes.

##### 8.2 Data, datasets and sampling

Where data are used:

- [ ] Each dataset or data source is named and described.
- [ ] The source, owner, access conditions, licence and intended use are identified.
- [ ] The target population, unit of analysis, sampling frame and inclusion/exclusion criteria are stated where relevant.
- [ ] The expected sample size or dataset volume is justified.
- [ ] Data collection procedures, instrumentation and collection conditions are described.
- [ ] Labels, annotations, ground truth or reference standards are defined.
- [ ] Data quality issues are anticipated (missing values, noise, class imbalance, drift, duplicates, outliers, measurement error and inconsistent formats).
- [ ] Data preprocessing and exclusion rules are documented and will be applied consistently.
- [ ] Potential selection bias, survivorship bias, sampling bias and dataset leakage are considered.
- [ ] The split strategy is appropriate to the data structure (e.g. subject-wise, group-wise, temporal, site-wise or random split as justified).
- [ ] Data access has been confirmed, or a realistic access plan and fallback dataset/source are documented.

##### 8.3 Algorithm, model or system design

- [ ] The proposed method is described with enough detail to understand its operation.
- [ ] The role of every important component is explained.
- [ ] The design decisions are justified using theory, literature or preliminary evidence.
- [ ] The proposal identifies which components are existing and which are proposed as novel.
- [ ] Mathematical formulation, pseudocode, architecture diagrams or specifications are included where they improve precision.
- [ ] Important parameters, constraints and assumptions are identified.
- [ ] Computational complexity, memory use, latency, scalability or other resource constraints are considered where relevant.
- [ ] Alternative designs and trade-offs are discussed.
- [ ] Failure modes and limitations are considered.

##### 8.4 Implementation or experimental environment

- [ ] Programming languages, libraries, frameworks, simulators, platforms and tools are identified where relevant.
- [ ] Hardware, processor, GPU, memory, storage, network or sensor requirements are identified where relevant.
- [ ] The experimental environment can realistically be accessed for the duration of the research.
- [ ] Software/library versions and configuration details will be recorded.
- [ ] Any dependencies on third-party APIs, commercial platforms, cloud services or proprietary tools are identified.
- [ ] There is a contingency plan for unavailable or discontinued tools, datasets or services.
- [ ] The proposal does not mistake a tool choice (e.g. Python, PyTorch, TensorFlow or a cloud platform) for a research contribution.

##### 8.5 Validation and verification

- [ ] The proposal explains how the proposed method/system will be checked for correctness.
- [ ] Verification tests are distinguished from empirical validation of research claims.
- [ ] Evaluation procedures are specified before results are observed, where feasible.
- [ ] The validation is designed to answer the research questions, not merely to demonstrate that the software runs.
- [ ] Appropriate baselines, controls, reference methods or comparison conditions are included.
- [ ] The proposal explains how alternative explanations for observed results will be considered.

---

#### 9. Computer Science-specific evaluation checklist

Use the subsections relevant to the research. A PhD does not need every metric listed below; it needs a defensible evaluation strategy suited to its research questions and contribution.

##### 9.1 Baselines and comparisons

- [ ] The baseline methods are relevant, credible and sufficiently strong.
- [ ] Classical, standard and state-of-the-art approaches are considered where appropriate.
- [ ] Baselines are implemented or configured fairly.
- [ ] The same data splits and evaluation conditions are used for comparable methods.
- [ ] Hyperparameter tuning and computational budgets are treated consistently or differences are reported.
- [ ] The proposal explains why each baseline is included.
- [ ] The evaluation does not rely solely on comparison with a weak or outdated method.

##### 9.2 Metrics

- [ ] Every metric is defined and justified.
- [ ] Metrics match the task and research question.
- [ ] The proposal explains what each metric captures and what it fails to capture.
- [ ] Metrics are not selected solely because they produce favourable results.
- [ ] For imbalanced classification, appropriate measures (e.g. precision, recall, specificity, F1, PR-AUC, ROC-AUC, balanced accuracy or calibration) are considered rather than accuracy alone.
- [ ] For regression, suitable error measures and residual analysis are considered.
- [ ] For ranking/retrieval, suitable ranking or retrieval metrics are identified.
- [ ] For systems research, relevant performance measures (e.g. latency, throughput, resource utilisation, energy, reliability, scalability or cost) are included.
- [ ] For human-centred research, instruments, task outcomes and qualitative analysis are justified.
- [ ] Clinical, safety-critical or high-impact claims use suitable validation endpoints and avoid unsupported diagnostic or causal claims.

##### 9.3 Statistical and experimental rigour

- [ ] The experimental unit is clearly defined.
- [ ] Repeated runs, random seeds, folds or repeated measurements are planned where needed.
- [ ] The rationale for sample size, number of runs or number of folds is explained.
- [ ] Variability and uncertainty will be reported (e.g. confidence intervals, standard deviations or suitable uncertainty measures).
- [ ] Appropriate statistical tests or estimation procedures are identified where relevant.
- [ ] Assumptions of statistical tests will be checked.
- [ ] Multiple comparisons, dependence between observations and small-sample limitations are considered.
- [ ] Effect size or practical significance is considered, not only statistical significance.
- [ ] The proposal explains how missing or failed runs and outliers will be handled.

##### 9.4 Ablation, sensitivity and component analysis

- [ ] The proposal includes ablation experiments where the contribution involves multiple components.
- [ ] Each proposed novel component can be evaluated separately where feasible.
- [ ] Sensitivity to important hyperparameters or design choices is considered.
- [ ] The contribution can be distinguished from gains caused by more data, larger models, extra compute or different preprocessing.
- [ ] There is a plan to investigate why a method succeeds or fails, not only whether a score increases.

##### 9.5 Generalisation, robustness and external validity

- [ ] The proposal identifies the conditions under which the method is expected to work.
- [ ] Generalisation beyond a single random split or narrow dataset is considered.
- [ ] Cross-subject, cross-site, cross-device, cross-domain, temporal or external validation is considered where relevant.
- [ ] Robustness to noise, missing data, distribution shift, adversarial conditions or operational variation is considered where relevant.
- [ ] The proposal distinguishes interpolation within the evaluation dataset from generalisation to new settings.
- [ ] Limitations on generalisability will be reported honestly.

##### 9.6 Reproducibility and reporting

- [ ] The proposed pipeline can be reproduced from documented data, code, configurations and experimental procedures, subject to access and privacy restrictions.
- [ ] Data splits and preprocessing steps will be recorded.
- [ ] Model parameters, training settings, random seeds and software versions will be recorded where relevant.
- [ ] Code/data sharing plans are stated, or reasons for restrictions are explained.
- [ ] The proposal includes a plan to document negative, null or failed results.
- [ ] The reporting plan is sufficient for another researcher to understand and assess the work.

##### 9.7 Additional checks by research type

**Machine learning / AI / data science**

- [ ] Train/validation/test separation prevents leakage.
- [ ] Preprocessing is fitted only on the training data where appropriate.
- [ ] Class imbalance, label quality and data provenance are addressed.
- [ ] Baselines and tuning are fair.
- [ ] Calibration, uncertainty, interpretability or fairness are considered if relevant to the research claims.
- [ ] Model size, inference cost, memory and latency are measured if deployment or efficiency is part of the claim.

**Software engineering / information systems**

- [ ] The research artefact is distinguished from the knowledge contribution.
- [ ] The design/evaluation method is explicit (e.g. design science, controlled experiment, case study, field study or empirical analysis).
- [ ] Requirements, stakeholders and context are justified where relevant.
- [ ] Evaluation measures more than functional completion or user satisfaction if the research claim is broader.
- [ ] Threats to validity and context-specific limitations are discussed.

**Computer systems / networks / cybersecurity**

- [ ] Workloads, traffic, threat models, topologies or deployment conditions are specified.
- [ ] Performance and security baselines are appropriate.
- [ ] Scalability, reliability, fault conditions and resource constraints are evaluated where relevant.
- [ ] Experimental environments and assumptions reflect the intended use case.
- [ ] Security testing is authorised, bounded and ethically conducted.

**Theory / algorithms**

- [ ] Definitions, assumptions and notation are precise.
- [ ] Claims are stated in a form that can be proved or analysed.
- [ ] The proof or analytical strategy is outlined.
- [ ] Complexity bounds, correctness properties or formal guarantees are identified where appropriate.
- [ ] The proposal explains the significance of the theoretical result.

---

#### 10. Research ethics, privacy, security and responsible research

- [ ] The proposal identifies whether human participants, patient/clinical data, personal data, sensitive data, animals, confidential industry data or other regulated material are involved.
- [ ] Required ethics approval or institutional permission has been identified.
- [ ] The proposal does not assume that data being publicly available automatically removes all ethical, privacy or licence obligations.
- [ ] Consent, recruitment and participant information procedures are addressed where relevant.
- [ ] Data minimisation, anonymisation/pseudonymisation, storage, retention, access control and deletion are addressed where relevant.
- [ ] Risks to participants, institutions, systems or the public are considered.
- [ ] Security and access controls are proportionate to the data and system risks.
- [ ] Dataset licences, software licences and intellectual property conditions are respected.
- [ ] Any generative-AI assistance is handled in accordance with current UM/FSKTM guidance and any required declaration; authorship, citations and factual responsibility remain the researcher's responsibility.
- [ ] Potential bias, fairness, accessibility, explainability or misuse risks are considered where relevant.
- [ ] The proposal avoids overstating clinical, legal, safety or policy implications beyond the study's design and evidence.

---

#### 11. Feasibility, resources, risks and work plan

##### 11.1 Feasibility

- [ ] The project can be completed within the applicable candidature period.
- [ ] The expected scope is appropriate for one doctoral project.
- [ ] Data, participants, equipment, software, compute and facilities are available or there is a credible access plan.
- [ ] Costs and recurring expenses have been estimated where relevant.
- [ ] Dependencies on external collaborators, vendors or approvals are identified.
- [ ] The research plan allows time for analysis, writing, publication and revision, not only implementation.

##### 11.2 Risks and fallback plans

- [ ] Key technical, data, access, recruitment, ethics, compute and timeline risks are listed.
- [ ] Each major risk has a likelihood/impact assessment or equivalent prioritisation.
- [ ] A mitigation or contingency plan is stated for each high-impact risk.
- [ ] Alternative datasets, methods, recruitment routes or tools are considered where feasible.
- [ ] The fallback plan preserves a meaningful research question and does not silently remove the central contribution.

##### 11.3 Gantt chart and milestones

- [ ] The timeline is aligned with the official candidature dates and intended thesis-submission date.
- [ ] Milestones are measurable (e.g. literature synthesis completed, protocol approved, dataset ready, method formulated, experiments completed, analysis completed, papers submitted, thesis chapters drafted).
- [ ] Dependencies and approval lead times are represented.
- [ ] Data collection, implementation, experimentation, analysis, writing and revision have realistic durations.
- [ ] Time is reserved for failed experiments, rework, supervisor feedback and examiner corrections.
- [ ] Publication targets are realistic and do not replace the core thesis plan.
- [ ] The schedule is consistent with the proposed objectives and methods.

---

#### 12. Expected outcomes, significance and limitations

- [ ] Expected technical or scientific outcomes are listed clearly.
- [ ] Each expected outcome maps to an objective.
- [ ] The proposal distinguishes deliverables (e.g. software, dataset, prototype, model) from research contributions (e.g. new method, evidence, theory or design knowledge).
- [ ] The theoretical significance is explained where relevant.
- [ ] The methodological or technical significance is explained.
- [ ] Practical or societal relevance is described without exaggeration.
- [ ] The intended beneficiaries or research communities are identified where appropriate.
- [ ] Known limitations and constraints are acknowledged.
- [ ] The proposal explains how the study will remain valuable if the expected performance improvement is not achieved.

---

#### 13. Document quality, citations and academic integrity

##### 13.1 Structure and readability

- [ ] The report follows the current faculty/university template or formatting instructions, if prescribed.
- [ ] Headings and numbering are consistent.
- [ ] Figures, tables, algorithms and equations are numbered and cited in the text.
- [ ] Figure and table captions explain their content adequately.
- [ ] All abbreviations are defined at first use.
- [ ] Symbols and terminology are used consistently.
- [ ] The writing is clear, formal and grammatically sound.
- [ ] Paragraphs have a clear purpose and logical flow.
- [ ] There are no contradictory statements between the abstract, objectives, methodology, expected contributions and timeline.
- [ ] Appendices contain supporting material rather than essential arguments omitted from the main proposal.

##### 13.2 References

- [ ] Every in-text citation appears in the reference list.
- [ ] Every reference-list entry is cited in the report, unless the required style says otherwise.
- [ ] Bibliographic details, author names, titles, years, venue names and DOI/URLs are accurate.
- [ ] Sources can be located and verified.
- [ ] Direct quotations are marked and referenced appropriately.
- [ ] The required citation style is used consistently.
- [ ] Important claims are supported by primary research where possible.
- [ ] Reference-manager metadata and imported citations have been checked manually.

##### 13.3 Similarity and AI use

- [ ] The proposal has been checked for unattributed copying and improper paraphrasing.
- [ ] Similarity results have been interpreted carefully; a similarity percentage alone does not establish whether plagiarism has occurred.
- [ ] Reused text, figures, instruments or datasets are cited and permitted.
- [ ] AI-generated references, quotations, data, code or technical claims have been independently verified.
- [ ] Any required declaration of generative-AI use has been completed according to current UM/FSKTM policy.
- [ ] The researcher can explain and defend every technical and academic claim in the proposal.

---

#### 14. Proposal Defence presentation checklist

Adjust the slide count to the actual presentation duration and faculty instructions. The following is a suggested sequence, not an official required slide template.

- [ ] **1. Title:** title, candidate, programme, supervisor(s) and date.
- [ ] **2. Research context:** concise background and domain.
- [ ] **3. Problem:** the specific research problem and supporting evidence.
- [ ] **4. Motivation and significance:** why the issue matters.
- [ ] **5. Literature synthesis:** key research streams and closest approaches.
- [ ] **6. Research gap:** specific unresolved issue(s).
- [ ] **7. Aim, objectives and questions:** clear mapping.
- [ ] **8. Proposed contribution:** what is new and why it matters.
- [ ] **9. Framework:** conceptual, theoretical, algorithmic or system overview.
- [ ] **10. Methodology:** research phases and how each objective will be addressed.
- [ ] **11. Technical detail:** key algorithm, model, architecture, equations or design choices.
- [ ] **12. Evaluation:** datasets, baselines, metrics, experiments and analysis.
- [ ] **13. Ethics, feasibility and risks:** relevant approvals, resources and contingencies.
- [ ] **14. Expected outcomes and limitations:** realistic and traceable to objectives.
- [ ] **15. Timeline:** milestones and thesis plan.
- [ ] **16. Conclusion:** problem, gap, contribution and proposed validation in one coherent summary.

##### Presentation delivery

- [ ] The presentation fits the time limit set by FSKTM.
- [ ] Slides are readable from a distance and not overloaded with paragraphs.
- [ ] Technical diagrams and equations are legible and explained.
- [ ] Each figure has a clear purpose and source where required.
- [ ] The research gap and contribution are easy to identify.
- [ ] The methodology and evaluation receive enough time; the presentation is not dominated by background.
- [ ] A short version of the proposal can be explained in two minutes.
- [ ] A complete backup copy of the slides and supporting material is available.
- [ ] Screen sharing, audio, pointer, fonts, videos and software demonstrations have been tested if applicable.
- [ ] The final slide leaves the panel with a clear statement of the proposed contribution.

---

#### 15. Examiner-style questions to rehearse

Prepare concise answers supported by the proposal, citations, equations, evidence or a clear research plan.

##### Research problem and motivation

- [ ] What exactly is the research problem?
- [ ] What evidence demonstrates that the problem exists?
- [ ] Why is this a Computer Science research problem rather than only an implementation or domain problem?
- [ ] Who or what benefits if the problem is addressed?
- [ ] What is outside the scope of the research, and why?

##### Literature and gap

- [ ] What are the closest three studies to your proposed research?
- [ ] What are the strongest existing approaches?
- [ ] What specific limitations remain unresolved?
- [ ] How did you identify and validate the research gap?
- [ ] What would an expert in the field say is already known about this problem?

##### Novelty and contribution

- [ ] What is the single most important original contribution?
- [ ] How is it different from existing methods or systems?
- [ ] Is the contribution more than combining existing algorithms or applying them to a new dataset?
- [ ] What new knowledge will exist after the thesis that does not exist now?
- [ ] What evidence would convince the research community that the contribution is valid?

##### Methodology and technical choices

- [ ] Why is this research design appropriate?
- [ ] Why did you select this method, algorithm, architecture or framework?
- [ ] What are the strongest alternatives, and why were they not selected?
- [ ] What assumptions does the method make?
- [ ] What happens if those assumptions are violated?
- [ ] How will the proposed method be verified and validated?

##### Data and evaluation

- [ ] Why are the selected datasets or participants suitable?
- [ ] How will you prevent data leakage and bias?
- [ ] Why are the baselines and metrics appropriate?
- [ ] How will you show that an observed improvement is meaningful and not due to chance, data differences or extra computation?
- [ ] How will you test generalisation and robustness?
- [ ] What will you conclude if the method performs no better than the baseline?

##### Feasibility and impact

- [ ] Can the proposed work be completed within the candidature period?
- [ ] Are data, approvals, hardware, software and funding realistically available?
- [ ] What are the three biggest risks, and what are the fallback plans?
- [ ] What is the expected theoretical, methodological or technical contribution?
- [ ] What are the most important limitations of the proposed study?

---

#### 16. Final go / no-go review

A proposal should not be considered ready merely because every chapter exists. Use the following gates before asking the supervisor to approve submission.

##### Critical gates

- [ ] The problem is specific, evidenced and researchable.
- [ ] The research gap is explicit and defensible.
- [ ] The originality claim is clear and supported by comparison with closest prior work.
- [ ] Objectives, research questions, methods and evaluation are aligned.
- [ ] The methodology can answer the research questions.
- [ ] Data, ethics, access, compute and other essential resources are realistically addressed.
- [ ] The proposed scope and timeline are feasible.
- [ ] I can explain and defend the proposal's central contribution.

##### Major quality gates

- [ ] Literature review is analytical rather than descriptive.
- [ ] Baselines and evaluation measures are appropriate.
- [ ] Experimental design addresses validity, robustness and reproducibility where relevant.
- [ ] Expected contributions are distinguishable from implementation deliverables.
- [ ] Limitations and fallback plans are credible.
- [ ] The presentation communicates the research argument clearly.

##### Final administrative gate

- [ ] Supervisor approval is obtained.
- [ ] The applicable semester deadline, report word count, number of copies and submission lead time have been confirmed with FSKTM.
- [ ] Current submission instructions and forms have been followed.
- [ ] The final report and slides have been submitted through the prescribed channel and by the confirmed deadline.

**Readiness recommendation:** If any critical gate is unchecked, address it before submission or explicitly discuss it with the supervisor. A minor formatting issue can usually be corrected quickly; an unclear research gap, weak novelty claim or methodology that cannot test the objectives requires substantive revision.

---

#### 17. Official UM / FSKTM references

The links below are official UM / FSKTM pages or documents. Check them again immediately before submitting because faculty instructions and programme documents can change.

1. **FSKTM — Guidelines and Policies**  
   https://fsktm.um.edu.my/guidelines-and-policies  
   Includes links to supervision policy, Conduct of Candidature Seminars, plagiarism guidance, postgraduate publication guidance, thesis preparation guidance and the Proposal Defence application guideline.

2. **FSKTM — Conduct of Candidature Seminars (PDF)**  
   https://fsktm.um.edu.my/fsktm/doc/postgraduate/24.conduct-of-candidature-seminars.pdf  
   The linked document states the Proposal Defence timing and report requirements, including the 3,000–7,000-word report and two-week submission lead time. Confirm its applicability to your cohort with the Postgraduate Office.

3. **FSKTM — Application Guideline for Proposal Defence, Confirmation Defence, Candidature Defence and Thesis Seminar (PDF)**  
   https://fsktm.um.edu.my/fsktm/doc/postgraduate/5-%20Application-Guideline-PD-CD.pdf  
   This document contains the active-status and supervisor-approval requirements, but its timing and report-submission lead time differ from the Conduct of Candidature Seminars document. Confirm which version applies.

4. **FSKTM — Postgraduate Handbook**  
   https://fsktm.um.edu.my/postgraduate-handbook  
   Check the handbook for the applicable academic session, programme and candidature requirements.

5. **FSKTM — Rules and Regulations**  
   https://fsktm.um.edu.my/rules-and-regulations  
   Includes the Universiti Malaya Doctoral Degree Rules 2024 and related regulations.

6. **FSKTM — PhD Programme**  
   https://fsktm.um.edu.my/doctor-of-philosophy-ph-d.html  
   Provides programme information, including the research-mode nature of the PhD and Research Methodology course information.

7. **FSKTM — Postgraduate Office / Contact Information**  
   https://fsktm.um.edu.my/postgraduate  
   Use the current contact details on this page to confirm administrative requirements.

---

#### 18. Personal action tracker

| Priority | Issue / action | Evidence needed | Person responsible | Target date | Status |
|---|---|---|---|---|---|
| Critical | Confirm applicable Proposal Defence semester deadline | Written confirmation from FSKTM | Candidate / Postgraduate Office | [date] | Not started |
| Critical | Confirm word count, number of copies and submission lead time | Written confirmation / current notice | Candidate / Postgraduate Office | [date] | Not started |
| Critical | Validate research gap and closest prior studies | Literature comparison matrix | Candidate / Supervisor | [date] | Not started |
| Critical | Align objectives, methods and evaluation | Completed traceability matrix | Candidate / Supervisor | [date] | Not started |
| Major | Strengthen baseline and evaluation design | Experimental plan | Candidate | [date] | Not started |
| Major | Review ethics, data access and resource feasibility | Approval/access plan | Candidate / Supervisor | [date] | Not started |
| Major | Complete presentation and mock defence | Slide deck and rehearsal notes | Candidate | [date] | Not started |

**Suggested final supervisor discussion:** Ask your supervisor to review the critical gates first—problem, gap, originality, objective-method alignment, evaluation validity and feasibility—before spending time on minor formatting changes.


## 7. `handover/checks/Check_Icentia11k_Clock_Time.md`

### Check: Do Icentia11k segments carry clock time?

**Why this matters:** Equation 3.2 in the proposal uses time-of-day weights (wₕ) "estimated from the diurnal PAC profile in Icentia11k". That only works if each Icentia11k segment carries a clock time. If it does not, wₕ must be redefined (for example, block length ÷ 24), and the proposal must say the Icentia11k reference daily count is itself extrapolated.

**What you need:** the same computer and Python setup you used for `icentia_ro1_prelim.py` (Python 3 with the `wfdb` package) and an internet connection. No full download is needed; the script reads only small header files from PhysioNet.

---

#### Step 1. Check that wfdb is installed

Open a terminal (Command Prompt / PowerShell on Windows, Terminal on macOS) and run:

```bash
python -c "import wfdb; print(wfdb.__version__)"
```

If you see a version number, continue. If you get `ModuleNotFoundError`, install it:

```bash
pip install wfdb
```

#### Step 2. Create the check script

Create a new file named `check_icentia_time.py` in the same folder as your RO1 script, and paste this in:

```python
import wfdb

# Patients to check (first patient of three different folders)
patients = [0, 1000, 5000]

for pid in patients:
    pdir = f"icentia11k-continuous-ecg/1.0/p{pid // 1000:02d}/p{pid:05d}"
    print(f"\n=== Patient p{pid:05d} ===")
    for s in range(3):  # first three segments
        seg = f"p{pid:05d}_s{s:02d}"
        try:
            h = wfdb.rdheader(seg, pn_dir=pdir)
            minutes = round(h.sig_len / h.fs / 60, 1)
            print(f"{seg} | date: {h.base_date} | time: {h.base_time} | "
                  f"fs: {h.fs} Hz | length: {minutes} min | comments: {h.comments}")
        except Exception as e:
            print(f"{seg} | could not read header: {e}")
```

#### Step 3. Run it

```bash
python check_icentia_time.py
```

It should finish in under a minute.

#### Step 4. Read the output

| What you see | Meaning | What to change in the proposal |
|---|---|---|
| `date: None` and `time: None` for every segment | Segments carry **no clock time** | Redefine wₕ as block length ÷ 24 (or use a published diurnal PAC profile from another source); state that the Icentia11k daily count is extrapolated from non-contiguous segments; Icentia11k cannot be used to place coverage gaps by time of day |
| Date and time are filled in | Clock time exists | Check Step 5 to see whether segments are contiguous |
| `length` is about 70 min per segment | Confirms each patient's ~57.5 h is many separate ~70-min segments, not one continuous recording | Describe the segment structure in Section 3.2 |
| `comments` contains text | May hold timing or recording notes | Copy it and send it to Claude |

#### Step 5. Only if clock time exists: check contiguity

For one patient, note the `time` and `length` of `s00`, then the `time` of `s01`.

- If `s01` starts where `s00` ends (start time + length), the segments are contiguous.
- If there is a gap, the segments are sampled from the full recording, and a daily count must still be extrapolated.

#### Step 6. Confirm with the official description

1. Open https://physionet.org/content/icentia11k-continuous-ecg/1.0/
2. Press Ctrl+F (Cmd+F on macOS) and search for: `time`, `segment`, `contiguous`, `random`.
3. Note any sentence describing how segments were taken from each patient's recording (up to about two weeks long), and whether timestamps were kept or removed.

#### Step 7. Send the result back

Copy the full terminal output from Step 3 and any relevant sentence from Step 6, and paste them into the chat. Claude will then update Equation 3.2, Section 3.2, Section 3.4 and the matching slides.

---

### Decision: how should Equation 3.2 define wₕ?

**Recommendation:** define wₕ as block length ÷ 24 in the main estimate, and run a published diurnal PAC profile only as a sensitivity analysis. The main estimate then adds no outside assumption.

#### Current equation (as submitted)

$$
\hat R(d) = \sum_h w_h \cdot \frac{\sum_{i \in A(d,h)} \hat p_i / \hat\pi(m_i, h)}{\tau(d,h)}, \qquad \sum_h w_h = 1 \tag{3.2}
$$

Plain text: R̂(d) = Σₕ wₕ · [ Σᵢ∈A(d,h) p̂ᵢ / π̂(mᵢ, h) ] / τ(d,h), with Σₕ wₕ = 1

- The bracketed term divided by τ(d,h) is the **observed hourly PAC rate in block h** after retention weighting. Call it r̂(d,h).
- The proposal currently says wₕ is "estimated from the diurnal PAC profile in Icentia11k".

#### The problem with profile weights

r̂(d,h) already contains that day's diurnal variation: if PACs are more frequent at night, the night rate is already higher. Multiplying it by a weight that is also larger at night counts the diurnal pattern twice and inflates the daily count.

#### Option A (recommended): weights are block durations

$$
w_h = \frac{L_h}{24}, \qquad \hat R(d) = \sum_h \frac{L_h}{24}\,\hat r(d,h), \qquad \text{daily count} = 24\,\hat R(d) = \sum_h L_h\,\hat r(d,h)
$$

Plain text: wₕ = Lₕ / 24, where Lₕ is the length of block h in hours. The daily count is Σₕ Lₕ · r̂(d,h): each block's rate times its length.

- Needs no external data and no clock time in Icentia11k.
- Every block counts in proportion to the time it covers, which is what a Holter 24-hour count does.
- The coverage gate (Equation 3.3) already refuses days whose day or night blocks are too thinly observed, so no block's rate is guessed.

#### Option B (sensitivity analysis only): a published profile fills thin blocks

The profile is used to shrink rates in blocks with low coverage, not as a weight:

$$
\tilde r(d,h) = \frac{\tau(d,h)\,\hat r(d,h) + \kappa\, g_h\, \bar r(d)}{\tau(d,h) + \kappa}, \qquad \text{daily count}_B = \sum_h L_h\,\tilde r(d,h)
$$

Plain text: r̃(d,h) = [ τ(d,h) · r̂(d,h) + κ · gₕ · r̄(d) ] / [ τ(d,h) + κ ]

- gₕ is the published relative PAC rate in block h (average 1 across the day).
- r̄(d) is that day's duration-weighted mean rate.
- κ (hours) sets how strongly thin blocks are pulled towards the profile.
- A well-observed block keeps its own rate; a thinly observed block borrows the published shape.
- Report how many patients change ESVEA class between Option A and Option B.

#### Worked example: why the choice matters near the threshold

Four 6-hour blocks, retention-weighted hourly PAC rates observed on one day:

| Block | Night 00–06 | Morning 06–12 | Afternoon 12–18 | Evening 18–24 |
|---|---|---|---|---|
| Observed rate r̂ (PACs/h) | 30 | 12 | 10 | 20 |

- **Option A (wₕ = 6/24 = 0.25 each):** 24 × (0.25 × 30 + 0.25 × 12 + 0.25 × 10 + 0.25 × 20) = **432 PACs/day**, ESVEA negative at 480/day.
- **Current wording, profile weights** (e.g. 0.40, 0.20, 0.15, 0.25): 24 × (12 + 2.4 + 1.5 + 5) = **502 PACs/day**, ESVEA positive.

The same data change class only because the night pattern was counted twice. That is why the main estimate should use Option A.

#### How the Icentia11k check affects this

| Result of Steps 3 to 6 | Main estimate | Sensitivity analysis |
|---|---|---|
| No clock time | Option A (unchanged) | Profile gₕ must come from a published 24-hour Holter study (source to be chosen and cited) |
| Clock time exists | Option A (unchanged) | gₕ can be estimated from Icentia11k, using patients not used for RO2 training or RO4a testing |

Either way, Option A stays the main estimate. The Icentia11k result only decides where the sensitivity profile comes from.

#### Proposed replacement text for Section 3.4

> Here wₕ = Lₕ/24, where Lₕ is the length of block h in hours, so the daily count 24 · R̂(d) = Σₕ Lₕ · r̂(d,h) weights each block by the time it covers, as a 24-hour Holter count does; c is the analysable coverage of each block, and the thresholds θ are fixed in the registered protocol. In a sensitivity analysis, rates in thinly observed blocks are shrunk towards a published diurnal PAC profile, and the number of participants whose ESVEA class changes is reported.

**Note:** this settles wₕ only. Equation 3.1 still needs the separate fix from the review: retention π̂ should also depend on beat class (or p̂ᵢ), because PAC intervals were retained at 39% against 91% for normal intervals (Section 4.2).


## 8. `handover/checks/Check_Kappa_Shrinkage_Strength.md`

### Check: κ = 1 hour, with a range tested

**Short answer:** κ cannot be confirmed by looking it up, because no paper reports it. It is a tuning constant in our own sensitivity analysis. There is enough information now to **pre-specify** it (κ = 1 h, sweep 0.5 to 4 h) and justify that choice in the proposal. It can only be **checked against data** once the RO3 Garmin recordings exist. Nothing needs to be confirmed before submission.

---

#### 1. What κ does

In the sensitivity analysis (Option B), the rate in a thinly covered 6-hour block is pulled towards the published diurnal profile:

$$
\tilde r(d,h) = \frac{\tau(d,h)\,\hat r(d,h) + \kappa\, g_h\, \bar r(d)}{\tau(d,h) + \kappa}
$$

- τ(d,h): hours of usable data in block h on day d
- r̂(d,h): the observed rate in that block
- gₕ · r̄(d): the rate the Larsen et al. (2016) profile predicts for that block, scaled to the day
- **κ: how many hours of "virtual" observation the profile is worth**

The profile's share of the final block rate is κ / (τ + κ):

| Observed hours in the block (τ) | κ = 0.5 h | **κ = 1 h** | κ = 2 h | κ = 4 h |
|---|---|---|---|---|
| 0.5 | 50% | **67%** | 80% | 89% |
| 1 | 33% | **50%** | 67% | 80% |
| 2 | 20% | **33%** | 50% | 67% |
| 3 | 14% | **25%** | 40% | 57% |
| 6 (full block) | 8% | **14%** | 25% | 40% |

#### 2. Why κ = 1 hour as the central value

1. **It ties to the per-block minimum.** If θ_block (set at device verification) is about 1 hour, a block exactly at the minimum is weighted half data, half profile. Blocks below the minimum lean on the profile; blocks well above it are mostly data.
2. **It respects how weak the profile is.** gₕ comes from medians read by eye from one figure, in 66 community participants with ≥30 PACs/h (Larsen et al., 2016, Figure 3). A small κ stops that uncertain shape from dominating well-observed blocks.
3. **It matches the sampling noise.** At the Icentia11k median of 1.35 PACs per hour (proposal Table 4.3), one observed hour holds about one PAC, so a block with under an hour of data says little on its own. That is where the profile should matter most, and κ = 1 h does exactly that.
4. **The range brackets plausible choices.** 0.5 h (data-led) to 4 h (profile-led) covers both extremes, so if ESVEA classes barely change across the sweep, the result does not depend on κ.

These are reasons for a convention, not evidence from a source. Say so in the proposal.

#### 3. What to pre-specify in the protocol

| Item | Value |
|---|---|
| Central κ | 1 hour |
| Sweep | 0.5, 1, 2 and 4 hours |
| Reported for each κ | Number and percentage of participants whose ESVEA class (≥480/day) changes against the main estimate; median absolute change in daily count |
| Robustness rule | Conclusions are called robust if class changes stay under a stated limit (for example under 10% of participants) across the whole sweep |

#### 4. How to check κ against data later (RO3, after the cohort)

These need the Garmin recordings, so they are planned analyses, not pre-submission tasks.

**Check A: masking test (recommended).**
1. Take days on which **every** 6-hour block is well covered (for example at least 4 hours each).
2. For each such day, artificially cut one block down to 0.5 h, 1 h or 2 h of data, chosen at random.
3. Re-estimate the daily count with each κ in the sweep.
4. Compare with the count from the full, unmasked day.
5. The κ with the smallest error is the data-supported value. Report it beside the pre-specified κ = 1 h.

**Check B: method of moments (optional, more statistical).**
In a gamma–Poisson model, κ equals the profile-predicted block rate divided by the between-day variance of the true block rate. On fully covered days, estimate:
- the mean block rate, from the counts
- the between-day variance, as the total variance of block rates minus the Poisson part (rate ÷ hours)

Then κ ≈ mean ÷ between-day variance. If it is far from 1 h, report the estimated value as an extra sensitivity setting.

#### 5. Text to add to the proposal (Section 3.4, after the sensitivity sentence)

> The shrinkage strength κ is set at 1 hour, so a block observed for 1 hour is weighted equally between its own rate and the profile; results are reported for κ of 0.5, 1, 2 and 4 hours, and κ is checked in the RO3 data by masking blocks on fully covered days.

About 50 words. This sentence is added only if Option B (the sensitivity analysis) goes into Section 3.4, which waits on the Pulsewatch check and your approval of Equations 3.1 and 3.2.

#### 6. What you need to do now

Nothing to look up. Decide only:
1. **Accept κ = 1 h and the 0.5 to 4 h sweep?** (Recommended.)
2. **The robustness limit:** what share of participants changing ESVEA class would you treat as "not robust"? 10% is a reasonable default; your supervisors may prefer another.


## 9. `handover/checks/Check_Pilot_AUROC_and_Subject_Split.md`

### Check: exact pilot AUROC and subject-level split

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

#### Step 1. Find the exact AUROC in your pilot outputs

Look in the pilot's output or log folder for a metrics file (`.json`, `.csv` or a training log) for the **Pulsewatch held-out test**. Note:
- AF-vs-rest AUROC, to three decimals
- AF vs PAC/PVC AUROC, to three decimals
- whether a 95% confidence interval was already computed

If you find both values with confidence intervals, skip to Step 3.

#### Step 2. If only predictions were saved, recompute

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

#### Step 3. Confirm the split is by subject

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

#### Step 4. What each result means for the proposal

| What you find | Wording in Table 4.1 and Section 4.1 |
|---|---|
| No subject overlap; exact values available | State "subject-level split" in Section 4.1; replace "≈1.00" with the exact AUROC and its 95% CI, e.g. "0.998 (0.995 to 1.000)" |
| Value rounds to 1.000 | Report "1.000 (95% CI lower bound to 1.000)"; do not write "≈" |
| No confidence interval possible (no saved predictions) | Report the exact point value and state that the CI was not computed |
| Subjects overlap, or the split was by window | Rerun the pilot with a subject-level split before the defence. Otherwise remove the Pulsewatch AUROC and keep only the cross-device recall results |

**Word count:** stating the split and the exact values adds about 10 to 15 words to the main text, which fits in the remaining headroom (about 30 words under the 7,000 limit).

#### Step 5. Send the result back

Paste into the chat:
1. Q1 and Q2: the two AUROC values, with confidence intervals if available
2. Q3: the overlap counts from Step 3
3. Q4: yes or no for the threshold and the test-only computation
4. The number of test subjects and windows

Claude will then update Table 4.1, Section 4.1 and the pilot slide (slide 17).

**Data protection:** share only the summary numbers, not prediction files or subject identifiers.


## 10. `handover/checks/Check_Pulsewatch_Accelerometer_and_ECG_Beat_Timing.md`

### Check: Does Pulsewatch include accelerometer data and beat-level ECG timing?

**Why this matters:** Equation 3.1 estimates π̂, the chance that a real beat survives into the smartwatch interval series, as a function of motion. Estimating it needs three things recorded at the same time: the true beats (reference ECG), what the watch reported (PPG), and motion (accelerometer). Icentia11k has only the ECG, and the RO3 Garmin cohort has no ECG. Pulsewatch is the only dataset in the proposal that might have all three. Its contents decide how Section 3.4 and Equation 3.1 are written.

**What to answer at the end:**
- **Q1.** Does Pulsewatch include accelerometer data for the same periods as the PPG?
- **Q2.** Does the reference ECG come with beat-level timing (R-peak times or beat annotations), or at least the raw ECG signal from which beats can be detected? Or only 30-second window labels?
- **Q3.** Are the watch and ECG recordings time-aligned, so that a beat in the ECG can be matched to the same moment in the PPG?

**Time needed:** about 20 to 40 minutes, most of it browsing and downloading one sample file.

---

#### Step 1. Start with the copy you already have

You used Pulsewatch in the pilot (proposal Section 4.1, Table 4.1: 48,396 segments), so part of the dataset is probably already on your computer.

1. Find the folder you used for the pilot.
2. List what is in it (file names, extensions, subfolders). On Windows, in PowerShell:
   ```powershell
   Get-ChildItem -Recurse "C:\path\to\pulsewatch" | Select-Object FullName, Length | Out-File pulsewatch_files.txt
   ```
   On macOS or Linux:
   ```bash
   find /path/to/pulsewatch -type f | head -200 > pulsewatch_files.txt
   ```
3. Look in `pulsewatch_files.txt` for names containing: `acc`, `accel`, `ACC`, `motion`, `imu`, `ecg`, `ECG`, `rpeak`, `r_peak`, `beat`, `annot`, `label`, `timestamp`, `time`.

If the pilot copy is only pre-cut 30-second PPG segments with labels, it may be a processed subset. Continue to Step 2 to check the full release.

#### Step 2. Check the full release on Synapse

1. Sign in at https://www.synapse.org with the account that has Pulsewatch access.
2. Open the project: search for **syn23565056** (the ID in proposal Table B.2).
3. Read the project **Wiki** page first. It usually describes:
   - which signals are included (PPG channels, accelerometer, heart rate)
   - the reference device (ECG patch) and whether raw ECG is shared
   - the label format (per 30-second window, or per beat)
   - how watch and ECG recordings were synchronised
4. Open the **Files** tab and expand each folder. Note:
   - folder and file names
   - file types (`.csv`, `.mat`, `.h5`/`.hdf5`, `.json`, `.npy`, `.parquet`, `.txt`)
   - any README, data dictionary or codebook file. Download it if present.
5. Check the **Conditions for Use** or data use terms on the project. Confirm that the planned use (fitting a beat-loss model) is allowed under your access approval.

#### Step 3. Inspect one sample file of each type

Download **one** small file of each type you found (one PPG file, one ECG file, one label file, one accelerometer file if separate). Put them in an empty folder, for example `pw_sample/`.

Save this script as `inspect_pulsewatch.py` **outside** that folder, then run it with the folder as the argument:

```bash
python inspect_pulsewatch.py pw_sample
```

```python
"""Print the structure of every file in a folder: columns, keys, shapes, first rows."""
import os, sys, json

folder = sys.argv[1]
KEYWORDS = ("acc", "imu", "motion", "ecg", "rpeak", "r_peak", "beat", "annot",
            "label", "time", "stamp", "ppg", "hr")

def flag(names):
    hits = [n for n in names if any(k in str(n).lower() for k in KEYWORDS)]
    return f"  matching keywords: {hits}" if hits else "  matching keywords: none"

for name in sorted(os.listdir(folder)):
    path = os.path.join(folder, name)
    ext = os.path.splitext(name)[1].lower()
    print(f"\n===== {name} ({os.path.getsize(path):,} bytes) =====")
    try:
        if ext in (".csv", ".txt", ".tsv"):
            import pandas as pd
            df = pd.read_csv(path, sep=None, engine="python", nrows=10)
            print("  columns:", list(df.columns)); print(flag(df.columns))
            print(df.head(5).to_string())
        elif ext == ".parquet":
            import pandas as pd
            df = pd.read_parquet(path)
            print("  shape:", df.shape, "columns:", list(df.columns)); print(flag(df.columns))
            print(df.head(5).to_string())
        elif ext == ".mat":
            try:
                from scipy.io import loadmat
                m = {k: v for k, v in loadmat(path).items() if not k.startswith("__")}
                for k, v in m.items():
                    print(f"  {k}: type={type(v).__name__} shape={getattr(v, 'shape', '')}")
                print(flag(m.keys()))
            except NotImplementedError:  # MATLAB v7.3 files are HDF5
                import h5py
                with h5py.File(path, "r") as f:
                    f.visititems(lambda n, o: print(f"  {n}: {getattr(o, 'shape', '')}"))
                    keys = []; f.visit(keys.append); print(flag(keys))
        elif ext in (".h5", ".hdf5"):
            import h5py
            with h5py.File(path, "r") as f:
                f.visititems(lambda n, o: print(f"  {n}: {getattr(o, 'shape', '')} {getattr(o, 'dtype', '')}"))
                keys = []; f.visit(keys.append); print(flag(keys))
                for k, v in f.attrs.items(): print(f"  attr {k} = {v}")
        elif ext == ".npy":
            import numpy as np
            a = np.load(path, allow_pickle=False); print("  shape:", a.shape, "dtype:", a.dtype)
        elif ext == ".json":
            with open(path) as fh: d = json.load(fh)
            keys = list(d.keys()) if isinstance(d, dict) else []
            print("  top-level keys:", keys[:50]); print(flag(keys))
        else:
            print("  (not inspected: unknown type)")
    except Exception as e:
        print("  could not read:", e)
```

If a package is missing, install it: `pip install pandas scipy h5py pyarrow`.

#### Step 4. Read the output

##### Q1. Accelerometer

| What you see | Answer |
|---|---|
| Columns or keys such as `acc_x`, `acc_y`, `acc_z`, `ACC`, `accel`, `imu`, at a regular sampling rate, covering the same period as the PPG | **Yes** |
| Only a motion summary (for example a single activity value per window) | **Partly**: usable as a coarse motion level per window, not per beat |
| No motion data anywhere, and the Wiki does not mention it | **No** |

##### Q2. Beat-level ECG timing

| What you see | Answer |
|---|---|
| A list of R-peak times or beat annotations (sample indices or timestamps, possibly with beat types) | **Yes, annotated** |
| A raw ECG signal (a long array at, say, 125 to 500 Hz) but no beat list | **Yes, derivable**: beats can be detected with a standard R-peak detector (for example `neurokit2`), without beat types |
| Only labels per 30-second window (for example AF / PAC-PVC / normal / noise) and no ECG signal | **No** |

##### Q3. Time alignment

| What you see | Answer |
|---|---|
| PPG and ECG share a timestamp column or start time, or the Wiki describes synchronisation | **Yes** |
| Segments are pre-cut and paired (same 30-s window for PPG and ECG) but with no absolute time | **Partly**: alignment within each window only; check the Wiki for how precise the pairing is |
| No shared time reference | **No** |

#### Step 5. What each answer changes in the proposal

| Q1 accelerometer | Q2 beat timing | Q3 aligned | What Equation 3.1 and Section 3.4 can say |
|---|---|---|---|
| Yes | Yes (annotated or derivable) | Yes | Motion part of retention is **estimated** on Pulsewatch: for each ECG beat, whether it appears in the PPG interval series, modelled against accelerometer motion. Beat-class part comes from RO1 on Icentia11k. State that the two parts are combined multiplicatively and that Pulsewatch uses a different watch from Garmin. |
| Yes | Window labels only | Any | Motion effect can be estimated only at **window level** (share of beats lost per 30-s window against motion, using heart-rate-based expected beat counts). Weaker; state it as an approximation. |
| No | Any | Any | Motion part stays a **stated assumption** from the Garmin specification. Equation 3.1 drops the motion term in the main analysis, and motion enters only as a sensitivity analysis. Consider the concurrent-ECG substudy in RO3 (10 to 15 participants wearing an ECG patch with the watch) to estimate it directly. |

#### Step 6. Send the result back

Paste into the chat:
1. The answers to Q1, Q2 and Q3 (Yes / Partly / No).
2. The relevant part of the `inspect_pulsewatch.py` output (column and key names, not the data values).
3. Any sentence from the Synapse Wiki describing signals, labels or synchronisation.

Claude will then write Equation 3.1, the retention paragraph in Section 3.4, Table 3.1 and Table B.2, and update the matching slides.

**Data protection:** share only file names, column names and descriptions in the chat. Do not paste participant data values or identifiers. The Pulsewatch data use terms and the UM AI guidelines may restrict uploading the data itself.


## 11. `handover/checks/Icentia11k_Check_Review_and_Proposed_Edits.md`

### Icentia11k clock-time check: independent review and proposed edits

Reviewed 2 November 2026 against the handoff folder (`claude_desktop_handoff/`), the current proposal source (Ridhwan_Research_Proposal_UM.docx) and the current slide deck. **Nothing has been edited.** Every edit in Part 3 waits for your approval.

Labels used throughout:
- **Confirmed:** I checked it against the cited file myself.
- **Inference:** my reasoning from confirmed facts; not checked against an external source.
- **Unverified:** stated in the handoff or elsewhere but not checked by me.
- **Decision:** a choice you need to make.

---

#### Part 1. Independent check of the handoff

##### Confirmed

| Claim | My check | Source |
|---|---|---|
| Released segments carry no clock time | All 9 headers show `date: None`, `time: None`, `comments: []` | `evidence/check_icentia_time_output.txt` |
| Segments are about 70 min at 250 Hz | Raw header `p00000_s00 1 250 1048577`: 1,048,577 ÷ 250 ÷ 60 = 69.9 min | `core/icentia_time_check_findings.md`, "Supporting evidence" |
| Each record has **one signal only** (ECG) | Second field of the record line is `1` | same raw header |
| Wider sample: 59 of 60 read, none with a time field | The script flags any record line with other than 4 fields or more than 2 lines; output reports 0 | `evidence/check_icentia_time_wide.py` and `_output.txt` |
| PAC retention 39%, normal 91% at the 20% threshold | 100 − 60.94 = 39.1%; 100 − 8.76 = 91.2% | `core/tableA_removed_by_class.csv`; proposal Table 4.2 |
| 67 patients at ≥480/day; 54 at ≥30/h; 66 by Binici rate or run | Matches | `core/tableB_esvea_prevalence.csv`; proposal Table 4.3 |
| `esvea_any` = (≥30/h) OR (run ≥20); 480/day is `S_per_hour × 24` | Matches lines 126 to 132 | `core/incentia_ro1_prelim.py` |
| Worked example: 432 vs 501.6 PACs/day | Recalculated | `core/new_task.md` |
| gₕ = 0.87, 0.63, 1.11, 1.40 | Recalculated from the 24 hourly readings: block means 66.7, 48.2, 85.2, 107.2; overall mean 76.8 | `core/icentia_time_check_findings.md` |
| Same rates with Figure 3 shares give about 435/day | 435.4 with unrounded shares (439.7 if the rounded shares 0.22/0.16/0.28/0.35 are used, because they sum to 1.01) | same |
| Hourly readings match Figure 3 | Compared by eye with the image; I agree within a few PACs/h (lowest 06–07, peaks at 15–16 and 20–21) | `evidence/larsen_2016_figure3.png` |

##### Where I disagree or add to the handoff

1. **Icentia11k cannot fit Equation 3.1 at all, not just its h-dependence.** The handoff (Still open, item 4) says Icentia11k "can't provide any dependence on block h". It also has no accelerometer (one signal per record, confirmed above), so it cannot provide the motion term m either. It can only inform retention by beat class, through the RO1 filter. *(Confirmed for the data; consequence is inference.)*
2. **"Summed to a true daily count" is wrong in the proposal itself.** Table 3.1 (RO2 row) and the validation-matrix slide say the Icentia11k ground truth is "ECG beat labels summed to a true daily count". With random, non-contiguous, untimed segments, the reference can only be a patient-level rate × 24, as `S_per_day_extrap` computes. *(Confirmed: proposal Table 3.1; script line 126.)*
3. **RO4a places coverage gaps "by time of day" on Icentia11k** (Table 3.4; RO4 slide). That cannot be done on untimed segments unless segments are assigned synthetic clock times. The handoff did not catch this because it had not seen the proposal. *(Confirmed: proposal Table 3.4.)*
4. **The ESVEA threshold in my earlier worked example was not the proposal's.** The proposal currently uses Binici's rate form (≥30/h) for the daily rate: Table 3.3 "ESVEA in rate form (Binici et al., 2010)" and the RO3 slide "≥30 per hour". The 480/day in `new_task.md` was my choice for the example, not taken from the proposal. *(Confirmed: proposal Table 3.3; slide ro3.)*
5. **Larsen is already cited in the proposal, slightly mis-summarised.** Section 3.5 says "PACs are afternoon-weighted (Larsen et al., 2016)". Figure 3 shows the highest block is 18–24 h, then 12–18 h, so "afternoon and evening" is accurate. *(Confirmed: figure image; proposal Section 3.5.)*
6. **Minor arithmetic note:** the handoff's "435" is right only with unrounded shares (see table above).

##### Could not verify

- That **no** segment among about 541,794 has clock time: 68 headers were read. The encoder argument rests on `icentia11k_make_wfdb.py`, which is not in the folder. *(Unverified.)*
- The annotation check (400 `.atr` files): its script was not saved. *(Unverified.)*
- That segment numbers are not chronological, the 3- to 14-day recording length, and how the random selection was made. These are the authors' descriptions or the handoff's reading of the encoder. *(Unverified.)*
- I could not rerun any header check: this workspace's proxy blocks PhysioNet and its S3 mirror (HTTP 403).
- Larsen et al. 2016 volume and pages (18(10), 1573–1580): taken from the handoff; the DOI matches the proposal's reference. *(Unverified by me.)*
- The source of the 480/day definition: the proposal attributes "480 or more supraventricular beats per day, or runs of 10 to 29 seconds" to Haeusler et al. (2025). I have not re-read that paper in this check. *(Unverified in this check.)*

---

#### Part 2. Resolving the "Still open" items

##### Item 4. Equation 3.1: where is retention π̂ estimated?

**What the proposal says (confirmed, Section 3.4):** retention "is fitted where censoring is observable, frozen, and used to reweight surviving beats", and π̂ depends on motion m and block h. Training flags on Icentia11k "are simulated from this specification and the RO1 results".

**Problems:**
- No dataset in the proposal has all of: true beats, device output, motion and clock time. Icentia11k has true beats only. The RO3 cohort has device output, motion and (probably) clock time, but no true beats. *(Inference from Table 3.1 and Table B.2.)*
- π̂ ignores beat class, although Table 4.2 shows PACs retained at 39% against 91% for normal beats. This was the review's Critical item 3. *(Confirmed.)*

**Proposed resolution (inference; needs your confirmation of Pulsewatch contents):**
- Make retention depend on beat class and motion, and drop h: π̂ₖ(m) for class k ∈ {PAC, other}.
- Beat-class component: from Icentia11k and RO1 (filter removal by class, Table 4.2).
- Motion component: from Pulsewatch, where the reference patch ECG shows which beats the PPG interval series lost, against accelerometer motion. This requires Pulsewatch to release accelerometer data with the PPG (Han et al. 2026 used "PPG, accelerometer and heart rate", proposal Table 2.2) and ECG beat times. Pulsewatch labels merge PACs and PVCs, so the motion term would be fitted for all beats, not PACs alone.
- State the assumption that the two components combine multiplicatively.

**Question for you:** does your Pulsewatch release include accelerometer data and ECG beat-level timing (not only 30-s window labels)? If not, the motion term must stay a stated assumption from the Garmin specification.

##### Item 5. Equation 3.3: how does the coverage gate work?

**What the proposal says (confirmed):** the gate checks only two blocks, "c(d, day) ≥ θ_day and c(d, night) ≥ θ_night", while Equation 3.2 sums over blocks h, which are never defined.

**Problem (inference):** with wₕ = Lₕ/24, every block h needs an observed rate. A day can pass a day/night gate while one 6-hour block has no coverage, which leaves r̂(d,h) undefined. So the claim in my earlier file that "no block's rate is guessed" is wrong under the current gate (the handoff was right to flag it).

**Proposed resolution (decision):**
- **Main estimate:** the gate requires minimum coverage in **every** block: c(d,h) ≥ θ for all h. Then Option A never needs to guess a rate.
- **Sensitivity analysis:** days that pass a day/night gate but leave a block below θ are kept, and thin blocks are filled by Option B (shrinkage towards gₕ). This gives Option B a defined job.
- **Trade-off:** a per-block gate makes "valid day" stricter, which lowers the RO3 primary outcome (proportion with at least 3 valid days). θ is set at device verification, so it can be modest (for example, at least 1 analysable hour per 6-hour block). The alternative is to keep the day/night gate and accept that the main estimate extrapolates within the day/night halves.

##### Item 6. How is Icentia11k used as a reference?

**Confirmed:** Icentia11k gives, per patient, PAC count ÷ analysed hours (median 57.5 h; Table 4.3). It cannot be split into days or clock-time blocks.

**Proposed resolution (inference):**
- **RO2:** compare the model's estimate with the reference at **patient level**: pool the model's PAC estimates over all of a patient's segments, divide by analysed hours, × 24, and compare with the annotated rate × 24. The "daily-count MAE" metric becomes a patient-level rate error expressed per day.
- **RO4a:** for coverage gaps, assign each segment to one of the four blocks at random (consistent with the published random selection) and form pseudo-days of 24 h. Gap patterns are then applied by block, and the coverage gate is evaluated on pseudo-days. Reference ESVEA status comes from the patient-level rate.
- Day-to-day estimation and real time-of-day effects are tested only in RO3 (no ground truth) and stated as a limit.

##### Item 7. Block definition

**Confirmed:** the proposal never defines blocks. The four 6-hour blocks appear only in my worked example and in the handoff's gₕ.

**Proposed resolution (decision):** four 6-hour blocks, 00–06, 06–12, 12–18 and 18–24 h. Night = 00–06; day = 06–24 (for the sensitivity gate). This matches gₕ as already calculated, so nothing needs recomputing.

##### Item 2 (ESVEA threshold): 480/day or ≥30/h?

**Confirmed current state:** the proposal and slides use Binici's rate form, ≥30/h (720/day), for the daily rate (Table 3.3; slide ro3), and quote "66 ESVEA-positive" (Binici rate or run) for RO4a (Section 3.6; Section 4.2; slides ro4 and preliminary-icentia). My `new_task.md` example used 480/day.

**Options (decision):**

| | ≥480 per day (stroke cohorts; Haeusler et al., 2025, per the proposal) | ≥30 per hour (Binici et al., 2010) |
|---|---|---|
| Population | Acute ischaemic stroke (matches RO3) | General population |
| Fits Equation 3.2 output (a daily count) | Directly | Via × 24 (= 720/day) |
| RO4a positives in 298 | 67 | 54 |
| Change needed | Table 3.3, Section 3.6, Section 4.2 text, three slides | None beyond the run caveat below |

**My recommendation:** ≥480 per day as the primary rate criterion, ≥30 per hour as secondary. Report runs separately, because filtering removes 60.9% of PAC coupling intervals (Table 4.2), which breaks runs apart. The 480/day definition source must be re-checked against Haeusler et al. (2025) before submission. If you prefer to keep Binici as primary, only the run caveat and my worked example change.

##### Item 1. Do the study's own Garmin recordings carry clock time?

**Unverified.** Equation 3.2 needs τ(d,h), so it is required. The device has not arrived (Section 3.5). **Proposed:** add "timestamps on every interval" to the device verification checklist (Section 3.5, milestone M1).

##### Item 3. Value of κ in Option B

**Decision.** Proposed: κ = 1 hour (the same order as a minimum per-block coverage threshold), with a sweep κ ∈ {0.5, 1, 2, 4} h reported. This is a convention, not taken from a source.

##### Items 8 to 11 (fixes to `new_task.md`)

- **8. r̄(d):** I agree with the handoff's fix, r̄(d) = Σₕ τ(d,h) r̂(d,h) / Σₕ τ(d,h) gₕ with Σₕ Lₕ gₕ / 24 = 1. If true block rates follow the shape gₕ, this recovers the scale from whichever blocks were observed, and it is defined when some τ(d,h) = 0. The gₕ values sum to 4.01 over four 6-hour blocks, so the normalisation holds to rounding. *(Checked algebraically.)*
- **9.** Included in the Section 3.4 text below.
- **10.** The worked example's 0.40/0.20/0.15/0.25 weights were hypothetical and do not match Figure 3; it is not used in the proposal, so no proposal edit is needed.
- **11.** gₕ now has a provisional cited source (Larsen et al., 2016, Figure 3), included below.

---

#### Part 3. Exact edits proposed (not applied)

Edits assume the recommendations above: per-block gate, four 6-hour blocks, ≥480/day primary. Edits marked **[if 480/day]** are dropped if you keep Binici as primary.

##### Proposal

**P1. Section 3.2, first paragraph.** After "…about 24% are unclassifiable and excluded (Tan et al., 2019)." insert:
> For each patient it releases up to 50 segments of about 70 minutes, selected at random from a recording of up to 14 days; the segments carry no clock time, so Icentia11k supports patient-level ectopy rates but not day-level or time-of-day analysis.

**P2. Table 3.1.**
- RO2, Ground truth: "ECG beat labels summed to a true daily count; Pulsewatch window labels" → "ECG beat labels giving a patient-level reference rate (PACs per analysed hour × 24); Pulsewatch window labels"
- RO4a, Ground truth: "ECG beat labels giving true ESVEA status" → "ECG beat labels giving reference ESVEA status from the patient-level rate"

**P3. Section 3.4, second paragraph.**
- "retention (Equation 3.1) is fitted where censoring is observable, frozen, and used to reweight surviving beats (Equation 3.2)" → "retention (Equation 3.1) is estimated by beat class from the RO1 filtering results and by motion from Pulsewatch, where the reference ECG shows which beats were lost, then frozen and used to reweight surviving beats (Equation 3.2)" *(depends on your Pulsewatch answer)*

**P4. Equations and the paragraph before them.**
- Lead-in: "…let A(d,h) be the retained beats, p̂ᵢ the predicted probability that beat i is a PAC, mᵢ its accelerometer motion, and τ(d,h) the observed hours in the block." → "…for day d and block h (00–06, 06–12, 12–18 and 18–24 h, each of length Lₕ = 6 h), let A(d,h) be the retained beats, p̂ᵢ the predicted probability that beat i is a PAC, mᵢ its accelerometer motion, and τ(d,h) the observed hours in the block."
- Equation 3.1 → `π̂ₖ(m) = P̂(beat of class k retained with high confidence | motion m),  k ∈ {PAC, other}`
- Equation 3.2 → `R̂(d) = Σₕ (Lₕ / 24) · r̂(d,h),  where r̂(d,h) = [ Σᵢ∈A(d,h) p̂ᵢ / π̂_PAC(mᵢ) ] / τ(d,h)`
- Equation 3.3 → `report R̂(d) only if c(d,h) ≥ θ for every block h`

**P5. Paragraph after the equations.** Replace "Here wₕ are time-of-day weights estimated from the diurnal PAC profile in Icentia11k, c is the analysable coverage of each block, and the thresholds θ are fixed in the registered protocol. The daily count is 24 · R̂(d)." with:
> Here r̂(d,h) is the retention-weighted PAC rate in block h, c(d,h) is the analysable coverage of the block, and θ is fixed in the registered protocol after device verification. The daily count, 24 · R̂(d) = Σₕ Lₕ · r̂(d,h), weights each block by the time it covers, as a 24-hour Holter count does, and needs no external diurnal profile. In a sensitivity analysis, days with day and night coverage but a block below θ are kept, and thin-block rates are shrunk towards a published diurnal profile (relative rates 0.87, 0.63, 1.11 and 1.40 for the four blocks, read from the published figure of median hourly PACs in 66 participants with frequent PACs; Larsen et al., 2016); the number of participants whose ESVEA class changes is reported. Because Icentia11k segments carry no clock time, RO2 compares estimates with the patient-level reference rate, and RO4a assigns segments to blocks at random to form pseudo-days.

**P6. Table 3.3.**
- Valid day: "Pre-specified minimum analysable coverage in both a daytime and a night-time block" → "Pre-specified minimum analysable coverage in each of the four 6-hour blocks"
- Daily rate: "Time-of-day weighted rate (Equation 3.2); ESVEA in rate form (Binici et al., 2010)" → **[if 480/day]** "Block-duration weighted rate (Equation 3.2); ESVEA rate criterion of 480 or more supraventricular beats per day (Haeusler et al., 2025), with 30 or more per hour (Binici et al., 2010) as secondary"

**P7. Section 3.5, device verification sentence.** "…will confirm export, flag and gap encoding, all-day logging and 7-day battery life…" → "…will confirm export, interval timestamps, flag and gap encoding, all-day logging and 7-day battery life…"; and "Valid days need coverage in both a day and a night block because analysable time is night-weighted while PACs are afternoon-weighted" → "Valid days need coverage in every 6-hour block because analysable time is night-weighted while PACs peak in the afternoon and evening".

**P8. Table 3.4, Coverage gaps row.** "Non-wear, charging and unusable PPG, placed by time of day" → "Non-wear, charging and unusable PPG, placed by block on pseudo-days (Icentia11k segments are untimed)"

**P9. Section 3.6, RO4a sentence [if 480/day].** "Preliminary analysis found 66 of 298 Icentia11k patients ESVEA-positive (Section 4.2)" → "Preliminary analysis found 67 of 298 Icentia11k patients at or above 480 PACs per day (54 at 30 or more per hour; Section 4.2)"

**P10. Section 4.2, last paragraph [if 480/day].** "Sixty-six patients (22.1%) met ESVEA (Table 4.3)… its value is that RO4a has 66 positive and 232 negative cases." → "Sixty-seven patients (22.5%) met the primary 480-per-day criterion and 66 (22.1%) met Binici's rate-or-run definition (Table 4.3)… its value is that RO4a has 67 positive and 231 negative cases at the primary criterion."

**P11. Table B.1.**
- Coverage: "…reported separately for daytime and night-time blocks" → "…reported for each 6-hour block"
- Valid day: "A day meeting the pre-specified minimum coverage in both the daytime and the night-time block" → "A day meeting the pre-specified minimum coverage in every 6-hour block"
- Ectopy rate: "Ectopic beats per hour, weighted by time of day; extrapolated to 24 hours for comparison with per-day thresholds" → "Retention-weighted ectopic beats per observed hour in each 6-hour block, combined by block length into a daily count"

**P12. Reference.** Larsen 2016 → "Larsen, B. S., et al. (2016). The circadian variation of premature atrial contractions. *Europace, 18*(10), 1573–1580. https://doi.org/10.1093/europace/euv389" *(volume and pages from the handoff; verify)*

##### Slides

| Slide | Current | Proposed |
|---|---|---|
| app-eq (Appendix: Equations) | Equations 3.1 to 3.3 and the line "wₕ: time-of-day weights from the diurnal PAC profile in Icentia11k" | Same three equations as P4; replace the wₕ line with "Blocks h: 00–06, 06–12, 12–18, 18–24 h (Lₕ = 6 h); daily count = Σₕ Lₕ · r̂(d,h); sensitivity: thin blocks shrunk towards Larsen et al. (2016) profile"; update speaker notes to match |
| validation-matrix | RO2 ground truth "ECG beat labels, summed to a true daily count" | "ECG beat labels, patient-level reference rate (Icentia11k segments are untimed)" |
| ro3 | Valid day "…in both a daytime and a night-time block"; Daily rate "Time-of-day weighted estimate; ESVEA in rate form (≥30 per hour; Binici et al., 2010)"; notes "…weighted by time of day rather than scaled by 24" | Valid day "…in each 6-hour block"; Daily rate **[if 480/day]** "Block-length weighted estimate; ESVEA ≥480 per day (Haeusler et al., 2025), ≥30 per hour secondary"; notes "…each block is weighted by its length, so night-weighted coverage does not bias the daily rate" |
| ro4 | Coverage gaps "Night-weighted pattern (Merschel & Reinhardt, 2022); RO3 cohort" | Add "applied by block on pseudo-days (untimed segments)" |
| preliminary-icentia **[if 480/day]** | "RO4a is viable: 66 of 298 (22.1%) met ESVEA" | "RO4a is viable: 67 of 298 (22.5%) ≥480 per day; 66 by Binici rate or run" |
| app-c3 (definitions) | Coverage, Valid day, Ectopy rate as in Table B.1 | Same changes as P11 |

**Word count:** these edits add about 180 words to the main text (currently about 6,700 by my count), so it stays under 7,000.

---

#### Questions for you before I edit

1. **Pulsewatch:** does your release include accelerometer data and ECG beat timing? (Decides P3 and the Equation 3.1 wording.)
2. **Coverage gate:** per-block gate (recommended) or keep day/night?
3. **Blocks:** four 6-hour blocks, as above?
4. **ESVEA primary:** ≥480/day (recommended) or ≥30/h?
5. **κ:** 1 hour with a sweep, as proposed?


## 12. `handover/checks/Pulsewatch_Precheck_Review.md`

### Pulsewatch beat-retention pre-check: review of settings, pass rule and proposal-stage need

Reviewed 2 November 2026 against `Pulsewatch_Beat_Retention_Precheck_Config.md` (pasted). The test has not been run; no results are reviewed here.

**Short answer:** yes to all three questions, with four changes to the settings and tighter definitions for the pass rule. The config file also answers the earlier Pulsewatch question: the data has everything Equation 3.1 needs.

#### What the config confirms about Pulsewatch

| Question (from `Check_Pulsewatch_Accelerometer_and_ECG_Beat_Timing.md`) | Answer | Evidence in the config |
|---|---|---|
| Q1. Accelerometer data | **Yes** | Raw `*_accel_*.txt`, 50 Hz, paired with each PPG segment |
| Q2. Beat-level ECG timing | **Yes, annotated** | R-peak files `Billal_ECG_peak_1_hr_this`, 250 Hz |
| Q3. Time alignment | **Yes** | Authors' per-segment tables `Aligned_ECG_LinearInterp`, plus a lag fitted per recording session |

So Pulsewatch can support the motion part of Equation 3.1, with the stated limit that it is a Samsung watch, not Garmin.

---

#### 1. Settings: approve, with four changes

| # | Change | Why |
|---|---|---|
| a | **Match one-to-one:** each PPG peak can match only one ECG beat. Also report unmatched PPG peaks per motion bin | Motion makes the detector produce extra peaks. Without one-to-one matching, spurious peaks inflate "retention" at high motion, which is exactly the bias the test is meant to rule out. The control corrects for chance, but not for one peak counted twice |
| b | **Check the accelerometer units** (m/s² or g) on one file before running, and also report bins by motion quintile | The fixed bins (<0.05 to ≥1 m/s²) are wrong if the units are g, and the top bins may be empty. Quintile bins always have data |
| c | **Add interval-level retention as a secondary result:** both beats of an interval matched consecutively | Equation 3.1 concerns intervals in the series, not single beats. One missed beat removes two intervals |
| d | **Record the segment-skip counts by reason before scoring** | So the share of data lost to each skip rule is visible and fixed in advance |

**Already sound, no change:**
- Lag fitted only on held-out labelled segments, never on a scored or noisy one
- The 1-second edge rule
- A control drawn from another session of the same subject
- Reporting with and without the quality gate, pooled and per subject
- No model fitted
- A fixed seed

---

#### 2. Pass rule thresholds: approve, with the definitions tightened

| Criterion | Proposed | Recommended wording |
|---|---|---|
| "Enough beats" | ≥500 beats per motion bin from ≥3 subjects | ≥500 beats per bin, from ≥3 subjects **each contributing ≥50 beats**, so one subject cannot dominate a bin |
| 1. Above chance at high motion | Excess over control above zero | **Lower bound of a 95% interval, bootstrapped by subject, above zero** in every top bin with enough beats. Beats within a subject are not independent, so a point estimate above zero is not enough |
| 2. Consistent within subjects | "Most subjects" show excess falling as motion rises | **At least two-thirds of subjects** with ≥2 eligible bins show lower excess in their highest eligible bin than in their lowest |
| 3. Detector comparable | Within 0.05 of the authors' `.pt` peaks | **Absolute difference in match rate ≤0.05, pooled, on the same held-out labelled beats, and ≤0.10 in every subject** |

Write these into the config file and date it before any result is seen. Report any later change as made after seeing the results.

---

#### 3. Is this test alone enough for the proposal stage? Yes, and it is not strictly required

- **The proposal only has to show the motion term can be estimated.** The data check already shows that: accelerometer data, R-peaks and alignment all exist. That alone is enough to rewrite Equation 3.1 and Section 3.4 now.
- **The test adds evidence that it works:** matching beats chance at high motion, and retention falls as motion rises.
  - **If it passes before submission:** one sentence in the proposal, cited as feasibility evidence, with no π̂ value.
  - **If it is not run in time:** describe it as planned. Either way the proposal stands.
- **Do not download the full 338 GB before the defence.** That is for fitting π̂ during RO2, after the defence.
- **The RO3 concurrent-ECG substudy stays** whatever the result, because it is the only direct estimate on Garmin.

**Word-count constraint:** the main text is at about 6,980 of 7,000 words, so a test result can get one sentence at most.

---

#### Next step on the proposal (awaiting approval)

Rewrite Equation 3.1 so retention depends on:
- **beat class**, from RO1 on Icentia11k (PAC 39% against normal 91% at the 20% filter), and
- **motion**, from Pulsewatch (ECG R-peaks matched to PPG peaks against accelerometer motion),

with no time-of-day term, because no dataset with true beats also has clock time and motion together. Then update the retention sentence in Section 3.4, and trim about 100 words from Chapter 2 to stay under 7,000.


## 13. `handover/analyses/icentia11k_clock_time/00_START_HERE.md`

### Icentia11k clock-time check: start here

Handoff for confirming the answer to `core/new_task.md`. Prepared 2026-11-02 from the `icentia-verification` project.

**To the reader:** treat "confirmed" below as checked against the listed file or source, and everything under "Still open" as unverified. The proposal and slides are not in this folder and have not been read or edited.

#### The answer

**The released Icentia11k segments carry no clock time.** The "no clock time" row of Step 4 applies, so:

1. wₕ can't be "estimated from the diurnal PAC profile in Icentia11k", as Equation 3.2 currently says.
2. wₕ becomes block length ÷ 24 in the main estimate (Option A).
3. The proposal must say the Icentia11k daily count is extrapolated from non-contiguous segments, and that Icentia11k can't place coverage gaps by time of day.
4. The sensitivity profile gₕ has to come from outside Icentia11k. The provisional source is Larsen et al. 2016, Figure 3.

#### Answers to each step in `new_task.md`

| Step | Result | Evidence |
|---|---|---|
| 1. wfdb installed | Yes, version 4.3.1 | Run in the project environment; no file |
| 2. Create the script | Done, code as given in the task | `evidence/check_icentia_time.py` |
| 3. Run it | 9 of 9 segments read | `evidence/check_icentia_time_output.txt` |
| 4. Read the output | `date: None`, `time: None`, 250 Hz, 69.9 min, `comments: []` on all 9, so no clock time and about 70-min segments | `evidence/check_icentia_time_output.txt` |
| 5. Contiguity | Can't be run because there are no timestamps. The published random selection means segments are a sample of each recording | `core/icentia_time_check_findings.md`, "Step 5: contiguity" |
| 6. Official description | "we randomly select 50 of the segments". It doesn't say whether timestamps were kept or removed | `core/icentia_time_check_findings.md`, "Step 6: official description" |
| 7. Update the proposal | **Not done:** the proposal and slides haven't been supplied | See "Still open" |

#### Supporting evidence for "no clock time"

- **Wider sample:** 59 of 60 randomly chosen headers were read, and none has a time field or comment line. The other was a 404 because p08975 has only 20 segments (`evidence/check_icentia_time_wide_output.txt`).
- **Authors' encoder:** `icentia11k_make_wfdb.py` (github.com/shawntan/icentia-ecg, `physionet/`) writes no `base_time` or `base_date`. It isn't copied here.
- **Annotations:** 400 of the 14,758 local `.atr` files hold only rhythm labels in `aux_note`. This was a one-off check, and its script wasn't saved.

#### Decision on Equation 3.2

From the decision section of `core/new_task.md`:

| Part | Decision |
|---|---|
| Main estimate | Option A: wₕ = Lₕ/24, so the daily count is Σₕ Lₕ · r̂(d,h) |
| Sensitivity analysis | Option B: shrink thinly observed blocks towards gₕ, and report who changes ESVEA class |
| Why not profile weights | r̂(d,h) already contains the day/night pattern, so weighting by a profile counts it twice |

**gₕ from Larsen Figure 3** (`evidence/larsen_2016_figure3.png`), read by eye and provisional:

| Block | Mean of hourly medians (PACs/h) | gₕ |
|---|---|---|
| Night 00–06 | 66.7 | 0.87 |
| Morning 06–12 | 48.2 | 0.63 |
| Afternoon 12–18 | 85.2 | 1.11 |
| Evening 18–24 | 107.2 | 1.40 |

Citation: Larsen BS, Kumarathurai P, Nielsen OW, Sajadieh A. Europace 2016;18(10):1573–1580. https://doi.org/10.1093/europace/euv389

#### Confirmed numbers

| Claim | Result | File |
|---|---|---|
| Worked example | Option A gives 432 PACs/day; profile weights give 501.6, rounded to 502 | Recalculated from `core/new_task.md` |
| PAC retention 39%, normal 91% | 60.9% and 8.8% removed at the 20% threshold | `core/tableA_removed_by_class.csv` |
| Same rates with Figure 3 shares as weights | 435 PACs/day, so the 502 depends on the example's hypothetical weights | `core/icentia_time_check_findings.md`, "gₕ from Larsen Figure 3" |
| ESVEA counts | 67 patients at ≥480/day, 54 at ≥30/h, out of 298 | `core/tableB_esvea_prevalence.csv` |

#### Still open

Full list: `core/icentia_time_check_findings.md`, "Still missing or unconfirmed".

**Questions to settle**
1. Do the study's own recordings have clock time? This is only inferred from τ(d,h) in Equation 3.2.
2. Which ESVEA threshold does the proposal use: 480/day or ≥30/h (720/day)? The worked example uses 480/day, while `esvea_any` in the script uses ≥30/h. The source for 480/day is unconfirmed.
3. What value of κ should Option B use?

**Needs the proposal**
4. Where is π̂(m,h) estimated (Equation 3.1)? Icentia11k can't provide any dependence on block h.
5. How does the coverage gate work (Equation 3.3)? This decides whether "no block's rate is guessed" holds and whether thin blocks can reach Option B.
6. How is Icentia11k compared with R̂(d)? It gives only a patient-level rate × 24.
7. Are the blocks really four 6-hour periods? They appear only in the worked example, and other blocks would mean recalculating gₕ.

**Suggested fixes not yet applied to `new_task.md`**
8. Replace Option B's r̄(d), which is undefined when τ(d,h) = 0: r̄(d) = Σₕ τ(d,h) r̂(d,h) / Σₕ τ(d,h) gₕ, with Σₕ Lₕ gₕ / 24 = 1.
9. Add the Icentia11k statements from Step 4 to the replacement text for Section 3.4.
10. Label the worked example's weights as hypothetical. Its pattern doesn't match Figure 3.
11. Update the "must come from a published 24-hour Holter study" row, whose source is still "to be chosen and cited".

**Could not verify**
- Whether Icentia's source data has timestamps, whether segment numbers follow time order, and how the random selection was done.
- The exact values behind Figure 3, the shape based on means, and whether it applies to 480–720/day or to the study's population.
- Whether the UK Biobank preprint reports PAC timing (DOI 10.64898/2026.02.23.26346310; the full text returned HTTP 403).

#### Where to find things

| Looking for | File | Search for |
|---|---|---|
| The task and the decision options | `core/new_task.md` | `Step 4`, `Option A`, `Option B`, `Proposed replacement text` |
| Full findings and context | `core/icentia_time_check_findings.md` | `Context and current status` |
| Everything unconfirmed | `core/icentia_time_check_findings.md` | `Still missing or unconfirmed` |
| Review of the decision section | `core/icentia_time_check_findings.md` | `Review of the decision section` |
| Literature search | `core/icentia_time_check_findings.md` | `Literature search for` |
| gₕ derivation and hourly readings | `core/icentia_time_check_findings.md` | `gₕ from Larsen Figure 3` |
| Limits and draft proposal wording | `core/icentia_time_check_findings.md` | `Limits to state in the proposal`, `Suggested wording` |
| ESVEA definitions and daily extrapolation | `core/incentia_ro1_prelim.py` | `esvea_any`, `esvea_day480`, `S_per_day_extrap` |
| Removal by beat class | `core/tableA_removed_by_class.csv` | `threshold_pct` = 20 |
| ESVEA prevalence | `core/tableB_esvea_prevalence.csv` | `>= 480` |
| Removal split by ESVEA status | `evidence/tableA2_removed_by_esvea.csv` | `esvea_any` |
| Step 3 script and output | `evidence/check_icentia_time.py`, `evidence/check_icentia_time_output.txt` | `date: None` |
| Wider header check | `evidence/check_icentia_time_wide.py`, `evidence/check_icentia_time_wide_output.txt` | `read 59 of 60` |
| Source figure for gₕ | `evidence/larsen_2016_figure3.png` | Teal line, left axis |

#### Notes on the files

- **Paths:** these are copies. `core/icentia_time_check_findings.md` still uses the original project paths, so `results/<name>` there means the file of that name in `core/` or `evidence/` here.
- **Spelling:** the script's real name is `incentia_ro1_prelim.py`, although `new_task.md` writes `icentia_ro1_prelim.py`. It's the same script.
- **Rerunning:** the check scripts need Python with `wfdb` and internet access. `incentia_ro1_prelim.py` needs the annotation files, which aren't included, or it can stream them slowly from PhysioNet.
- **Not included:** the proposal, the slides and the Larsen PDF.


## 14. `handover/analyses/icentia11k_clock_time/icentia_time_check_findings.md`

### Icentia11k clock-time check: findings

Checked 2026-11-02, following `new_task.md`.

**Result: the released Icentia11k segments carry no clock time.** Time-of-day weights (wₕ) can't be estimated from this dataset. The Icentia11k daily count is extrapolated from sampled segments.

#### Context and current status

**The question.** Equation 3.2 in the proposal estimates a daily PAC count, R̂(d), by weighting hourly rates from each time-of-day block with weights wₕ. The proposal says wₕ is "estimated from the diurnal PAC profile in Icentia11k", which needs every Icentia11k segment to carry a clock time. `new_task.md` sets out the check and the decision that follows from it.

| Item | Status |
|---|---|
| Do released Icentia11k segments carry clock time? | Answered: no, on every header sampled, in the authors' encoder and in the annotations |
| Main estimate for wₕ | Decided: wₕ = Lₕ/24 (Option A in `new_task.md`) |
| Sensitivity analysis | Decided: shrink thin blocks towards a published profile (Option B). Its definition of r̄(d) still needs fixing |
| Source of gₕ | Provisional: Larsen et al. 2016 Figure 3, with values read by eye |
| Proposal and slides | Not edited: the files haven't been supplied |

Everything that could not be confirmed is listed in the last section, "Still missing or unconfirmed".

#### Step 3 output

Saved in `results/check_icentia_time_output.txt`.

```
=== Patient p00000 ===
p00000_s00 | date: None | time: None | fs: 250 Hz | length: 69.9 min | comments: []
p00000_s01 | date: None | time: None | fs: 250 Hz | length: 69.9 min | comments: []
p00000_s02 | date: None | time: None | fs: 250 Hz | length: 69.9 min | comments: []

=== Patient p01000 ===
p01000_s00 | date: None | time: None | fs: 250 Hz | length: 69.9 min | comments: []
p01000_s01 | date: None | time: None | fs: 250 Hz | length: 69.9 min | comments: []
p01000_s02 | date: None | time: None | fs: 250 Hz | length: 69.9 min | comments: []

=== Patient p05000 ===
p05000_s00 | date: None | time: None | fs: 250 Hz | length: 69.9 min | comments: []
p05000_s01 | date: None | time: None | fs: 250 Hz | length: 69.9 min | comments: []
p05000_s02 | date: None | time: None | fs: 250 Hz | length: 69.9 min | comments: []
```

#### Step 6: official description

PhysioNet, Data Description (https://physionet.org/content/icentia11k-continuous-ecg/1.0/). The CinC 2021 paper uses almost the same words:

> From this, we randomly select 50 of the segments and their respective labels from the list of segments. The goal here is to reduce the size of the dataset while maintaining a fair representation of each patient.

Neither the page nor the paper says whether timestamps were kept or removed, and neither uses the word "contiguous".

#### Supporting evidence

| Check | Result |
|---|---|
| Wider sample, `check_icentia_time_wide.py` (seed 2026): one random segment from each of 60 random patients | 59 read, and every record line has only 4 fields (name, signals, rate, samples), with no comment lines. The other one was p08975_s36, HTTP 404: `RECORDS` for that patient lists only 20 segments (s00-s19) |
| Raw header, p00000_s00 | `p00000_s00 1 250 1048577`, then a signal line |
| Authors' encoder, `icentia11k_make_wfdb.py` (shawntan/icentia-ecg) | `wrsamp` and `wrann` are called without `base_time` or `base_date` |
| Annotations: 400 random files from `icentia_atr/` (one-off check, script not saved) | `aux_note` holds only rhythm labels: `(N`, `(AFIB`, `(AFL`, `)`, `(N)`, `(AFIB)`, plus `None` |

#### Step 5: contiguity

This can't be tested because there are no timestamps. The random selection means a patient's segments are a sample of the recording, not one continuous stretch. Some selected segments could still happen to be adjacent, and the data can't show which.

#### Limits

- This describes the released files. It doesn't show whether Icentia's source data has timestamps.
- Nothing states that segment numbers follow time order. The encoder numbers them in the order they appear in the source file, so s00, s01 and so on shouldn't be treated as chronological.
- Not every patient has 50 segments (p08975 has 20), so hours per patient vary.

#### What this means for the proposal

Not yet applied, because the proposal and slides aren't on this machine.

- **Equation 3.2:** decided in `new_task.md`. The main estimate uses wₕ = Lₕ/24 (Option A). The sensitivity analysis shrinks thin blocks towards a published profile (Option B), because the "no clock time" row of its decision table applies. The provisional source for gₕ is Larsen et al. 2016 Figure 3 (see "gₕ from Larsen Figure 3").
- **Section 3.2:** describe up to 50 randomly selected segments of about 70 minutes per patient, from 3-14 day recordings, with no clock time.
- **Section 3.4:** state that the Icentia11k daily count is extrapolated from non-contiguous segments, and that Icentia11k can't place coverage gaps by time of day. `S_per_day_extrap` in `incentia_ro1_prelim.py` is already computed as S per hour × 24.
- **Slides:** apply the same wording.

#### Review of the decision section in `new_task.md`

Confirmed:
- The worked example: Option A gives 432 PACs/day; profile weights give 501.6, rounded to 502.
- The 39% and 91% retention figures in the closing note: at the 20% threshold, `results/tableA_removed_by_class.csv` shows 60.9% of PAC coupling intervals and 8.8% of normal intervals removed.

Open points:
1. **Replacement text:** it leaves out what Step 4 requires, namely that the Icentia11k daily count is extrapolated and that the dataset can't place coverage gaps by time of day.
2. **"No clock time in Icentia11k":** this holds for the weights only. Without clock time, Icentia11k segments can't be assigned to a day d or a block h, so R̂(d), τ(d,h), r̂(d,h) and any h-dependence in π̂(m,h) can't be computed from it. Its reference is a patient-level rate × 24, as in `S_per_day_extrap`. Where π̂ is estimated needs checking against Equation 3.1, and how Icentia11k is compared with the R̂(d) daily count needs stating.
3. **Option B definition of r̄(d):** a duration-weighted mean needs a rate in every block, so it's undefined when τ(d,h) = 0, and it includes the thin blocks being corrected. Suggested: r̄(d) = Σₕ τ(d,h) r̂(d,h) / Σₕ τ(d,h) gₕ, with gₕ normalised so that Σₕ Lₕ gₕ / 24 = 1. If the true rates follow the profile shape, this recovers their scale regardless of which blocks were observed.
4. **"No block's rate is guessed":** this overstates the gate. A block that passes is still extrapolated from its observed part. Option B also only has work to do if thin blocks can pass the gate. Check against Equation 3.3.

#### Literature search for gₕ (2026-11-02)

Searched PubMed (two queries, 100 records screened by keyword on title and abstract) and Consensus (three queries, top 20 each).

**Result: no study found publishes block or hourly PAC rates in numbers that could be used directly as gₕ.**

| Source | What it offers | Limits |
|---|---|---|
| Larsen et al., Europace 2016, DOI 10.1093/europace/euv389 (full text read) | Best match. Copenhagen Holter Study, 638 subjects, up to 48 h. In the 66 with ≥30 PACs/h, Figure 3 shows the lowest value at 06-07 and the highest at 15-16 and 20-21 | Hourly medians appear only in Figure 3 (read by eye, see below). Means not reported ("the statistical validity would be questionable"). No pattern in all subjects or in those below 30 PACs/h. Community cohort without known heart disease |
| Brooks et al., Heart Rhythm 2012, DOI 10.1016/j.hrthm.2012.03.062 (abstract) | In paroxysmal AF: "distinct increase in ectopy burden after 7 PM and elevation throughout the night" | 49 patients. Shares Larsen's high evening, but not necessarily the rest of the shape (abstract only) |
| Ribera et al., Gerontology 1989, DOI 10.1159/000213015 (abstract) | Supraventricular ectopy "mainly diurnal" | 50 subjects, no rates in the abstract |
| De Scalzi et al. 1984, PMID 6208073 (abstract) | Individual rhythms in 8 of 16 subjects, peak times from 04:24 to 18:12 | Very small; peak times vary widely |
| UK Biobank monitoring preprint, DOI 10.64898/2026.02.23.26346310 (abstract only) | 27,658 participants, 14-day patches, reports circadian patterns | Abstract covers AF and ventricular ectopy timing, not PACs. Full text returned HTTP 403, so not checked |

Not established: whether the UK Biobank paper reports PAC timing.

##### gₕ from Larsen Figure 3

Hourly values were read by eye from the median PACs/h line (left axis, linear, 00-01 to 23-00, n = 66): 78, 63, 82, 67, 60, 50, 33, 47, 56, 45, 46, 62, 71, 81, 88, 118, 73, 80, 104, 104, 120, 106, 116, 93.

| Block | Mean of hourly medians (PACs/h) | gₕ (block ÷ 76.8) |
|---|---|---|
| Night 00-06 | 66.7 | 0.87 |
| Morning 06-12 | 48.2 | 0.63 |
| Afternoon 12-18 | 85.2 | 1.11 |
| Evening 18-24 | 107.2 | 1.40 |

Limits:
- These are estimates of medians, from 66 community participants with ≥30 PACs/h. They are not published numbers or mean rates.
- A 3 PACs/h reading error across a whole block moves gₕ by about 0.04 at most. Sampling noise isn't quantified and is probably larger: neighbouring hours jump from 118 to 73.
- The paper's conclusion says PACs fall during the evening, but Figure 3 keeps them high until 23-00. The values above follow the figure.

**Implications:**
- gₕ can now come from a published source, as `new_task.md` requires, if it is described as read from Figure 3.
- Equation 3.2 needs τ(d,h), so the study's own recordings should have clock time (to confirm). If so, estimating gₕ from days with complete coverage is a useful second check on a shape that comes from only 66 people.
- The worked example has its highest rate at night and its lowest in the afternoon, while Figure 3 is highest in the evening and lowest in the morning. Its 0.40, 0.20, 0.15, 0.25 weights are hypothetical: using Figure 3 shares (0.22, 0.16, 0.28, 0.35) on the same rates gives 435 PACs/day, not 502. Double counting is still a sound objection, but label the example as hypothetical.

##### Limits to state in the proposal

- Source of the values: they were read by eye from a figure, and they are medians rather than the mean rates that gₕ ideally represents. The authors chose not to report means [1].
- Who it represents: 66 community participants with ≥30 PACs/h (≥720/day), and none of them are in your 480–720/day range. In the full cohort, which was mostly people with fewer PACs, no pattern was visible [1].
- Precision: a 3 PACs/h reading error across a whole block moves gₕ by about 0.04 at most. Sampling noise is probably larger, as neighbouring hours jump from 118 to 73.
- Text versus figure: the paper's conclusion says PACs fall during the evening, but Figure 3 keeps them high until 23–00. Cite the figure for this.

##### Suggested wording for the proposal

> In a sensitivity analysis, rates in thinly observed blocks are shrunk towards a published diurnal profile. Relative block rates (gₕ = 0.87, 0.63, 1.11 and 1.40 for 00–06, 06–12, 12–18 and 18–24) were derived from values read from the published figure of median hourly PAC counts in participants with frequent PACs in the Copenhagen Holter Study (n = 66; Larsen et al., 2016). The number of participants whose ESVEA class changes is reported.

[1] Larsen BS, Kumarathurai P, Nielsen OW, Sajadieh A. The circadian variation of premature atrial contractions. Europace. 2016;18(10):1573–1580. https://doi.org/10.1093/europace/euv389

#### Still missing or unconfirmed

##### Needs the proposal or slides (not seen)

Everything below comes from the excerpts in `new_task.md`. The proposal itself hasn't been read.

| Item | Why it matters |
|---|---|
| Equation 3.1, and where π̂(m,h) is estimated | If π̂ depends on block h and is estimated from Icentia11k, it can't be computed without clock time |
| Equation 3.3, the coverage gate | Decides whether "no block's rate is guessed" holds, and whether thin blocks can reach Option B at all |
| How Icentia11k is used as a reference, including RO2 and RO4a | R̂(d) is a per-day, per-block count, while Icentia11k gives only a patient-level rate × 24. The comparison needs to be stated |
| The block definition | gₕ above assumes four 6-hour blocks, which appear only in the worked example. Other blocks mean recalculating gₕ from the hourly readings |
| Which ESVEA threshold the proposal uses | See "ESVEA threshold" below |
| Current wording of Sections 3.2, 3.4 and 4.2, and the slides | Needed to make the edits. The 39% and 91% figures were checked against `results/`, not against Section 4.2 |

##### Needs an answer from you

- **Clock time in the study's own recordings:** inferred from τ(d,h) in Equation 3.2, not confirmed. Without it, gₕ can't be checked against the study's own data.
- **κ in Option B:** no value has been proposed, and the sensitivity analysis can't run without one.
- **Option B's r̄(d):** the suggested fix in "Review of the decision section" hasn't been accepted or applied.
- **Worked example:** its weights aren't yet labelled as hypothetical in `new_task.md`.

##### ESVEA threshold

- `new_task.md` and the worked example classify at 480 PACs/day. `incentia_ro1_prelim.py` also tests ≥30 S/h and uses 30/h, not 480/day, in `esvea_any`.
- These differ: 30/h × 24 = 720/day, which is the equivalence Larsen uses. In `results/tableB_esvea_prevalence.csv`, 67 patients meet ≥480/day and 54 meet ≥30/h.
- The source for the 480/day cut-off wasn't checked in this work. The script's docstring attributes it to Binici et al. 2010, but that paper wasn't read.

##### Icentia11k

| Not confirmed | What was actually checked |
|---|---|
| That no segment in the dataset has a clock time | 68 headers read (9 + 59) out of about 541,794 segments. The encoder supports the result for all of them, assuming it is the script that produced the released files |
| Whether Icentia's source data has timestamps | Neither the description nor the paper says. The step that produced the encoder's input files wasn't available. Only the authors could answer this |
| Whether segment numbers follow time order | Not stated anywhere |
| Whether random selection was even across day and night | Only "randomly select" is stated. No method is given, and it can't be tested without clock time |
| Annotation check across all files | 400 of the 14,758 local `.atr` files, by a one-off check whose script wasn't saved |

The 3-14 day recording length and the sampling statement are the authors' descriptions and weren't independently verified.

##### gₕ and the literature

| Not confirmed | Detail |
|---|---|
| The exact values behind Figure 3 | Read by eye and compared with the figure by eye. No digitising software was used and the authors weren't contacted |
| The shape based on mean rates | The authors say means looked similar but didn't report them. gₕ is built from medians, and a mean of hourly medians isn't a true block rate |
| Whether the shape applies near the threshold | Figure 3 covers only ≥30 PACs/h. No separate result exists for 480-720/day |
| Whether the shape applies to the study's population | Larsen's cohort is a community sample aged 55-75 without known heart disease, recorded in 1998-2000. The study population wasn't checked against it |
| Sampling uncertainty in gₕ | Not quantified. No confidence intervals are available from the figure |
| Whether PAC timing appears in the UK Biobank preprint | The abstract doesn't mention it, and the full text returned HTTP 403. This is the largest dataset found |
| Brooks 2012 and the other small studies | Abstracts only, so their figures and tables weren't seen |
| Sources not retrieved | Mikulecký et al. 2008 (cited by Larsen, 37 healthy men) and the Manolis et al. 2024 review |
| That no better source exists | PubMed abstracts were screened by keyword, and only the top 20 results of each Consensus query were seen. Papers reporting timing only in full text could have been missed |

##### Not done

- Sections 3.2 and 3.4 of the proposal, Equation 3.2 and the slides haven't been edited.
- `new_task.md` still has the "must come from a published 24-hour Holter study" row with its source marked "to be chosen and cited", and none of the open points above have been applied to it.


## 15. `handover/analyses/kappa_simulation/README_kappa_simulation.md`

### Kappa simulation: choosing the shrinkage strength for the sensitivity analysis

**Purpose.** Test whether the Option B sensitivity analysis (thin 6-hour blocks shrunk towards a published diurnal profile, proposal Section 3.4) depends on the shrinkage strength κ, using simulated data built to behave like the future RO3 Garmin cohort. This chooses and justifies κ before the real data exist. It does **not** confirm κ for real Garmin data; that needs the RO3 masking check.

**Files**
| File | Content |
|---|---|
| `kappa_sim.py` | The simulator (Python; numpy, pandas, scipy). Run `python kappa_sim.py`; about 1 minute |
| `calibration.csv` | Simulated values against each published target |
| `kappa_results.csv` | Estimator performance for every scenario and κ |
| `run_output.txt` | Console output of the run reported here (seed 2026) |

No dataset is downloaded. The only Icentia11k inputs are summary numbers from the candidate's own RO1 run.

---

#### 1. How the data are generated

Each simulated participant has 7 days × four 6-hour blocks (00–06, 06–12, 12–18, 18–24 h).

| # | Layer | Model | Numbers and source |
|---|---|---|---|
| 1 | PAC burden | Log-normal rate per participant | Spread from Icentia11k IQR 0.23 to 13.38 PACs/h (proposal Table 4.3); level calibrated so 25.3% have a true 7-day mean ≥480/day (Haeusler et al., 2025) |
| 2 | Time-of-day pattern | Larsen shape × individual deviation | Shape 0.87, 0.63, 1.11, 1.40 (Larsen et al., 2016, Figure 3, read by eye); individual deviation **unknown, swept** (log SD 0.2 or 0.5) |
| 3 | Day-to-day variation | Log-normal day factor with day-to-day persistence (AR(1)) | SD and persistence **calibrated** so one day and seven days detect high PAC frequency with 76.6% and 88.8% sensitivity against a 14-day reference (Måneheim et al., 2024) |
| 4 | PACs per block | Poisson, or clustered (negative binomial) | Clustering **unknown, swept** (none, or gamma shape 2) |
| 5 | Wear | Daily wear probability falling over time, with between-participant variation | 73% falling to 63% over 30 days (Ding et al., 2023); between-participant SD 1.0 on the logit scale (assumed) |
| 6 | Blocks worn on a worn day | Each block worn with a fixed probability | **Unknown, swept**: 0.95 ("typical") or 0.75 ("poor") |
| 7 | Charging | One hour removed from 06–12 each worn day | Protocol: one short daily charging window (Table 3.3); placement assumed |
| 8 | Usable signal | Beta-distributed usable fraction per block | 94% at night, 64% in the day, averaging 71.5% over 24 h (Merschel & Reinhardt, 2022) |
| 9 | Beat loss | Each PAC in usable time kept with probability 0.391 | PAC coupling intervals kept at the 20% filter: 100 − 60.9% (proposal Table 4.2) |

**Estimators (as planned in the proposal):**
- **Main (Option A):** Equation 3.2 with wₕ = 6/24, using only days where every block has ≥1 usable hour (Equation 3.3).
- **Option B, κ = 0.5, 1, 2, 4 h:** days meeting the day/night rule (≥2 h at night, ≥6 h in the day; assumed thresholds), with every block shrunk towards the profile: r̃ = (τ r̂ + κ gₕ r̄) / (τ + κ), r̄ = Σₕ τ r̂ / Σₕ τ gₕ.
- Each participant's estimate is the mean daily count over the days used; ESVEA if ≥480. Truth is the participant's true mean daily count over all 7 days.

**Deliberate simplifications:** retention (0.391) and PAC identification are treated as known exactly, so the simulation isolates coverage and κ. Real estimates will have additional error from both.

---

#### 2. Calibration: does the simulator reproduce the published figures?

| Target | Source | Simulated (range across 8 scenarios) |
|---|---|---|
| 1-day sensitivity 76.6% | Måneheim et al. (2024) | 76.0 to 77.7% |
| 7-day sensitivity 88.8% | Måneheim et al. (2024) | 88.3 to 89.4% |
| ESVEA 25.3% | Haeusler et al. (2025) | 24.7 to 25.1% |
| Day-1 wear 73% | Ding et al. (2023) | 71.6 to 74.2% |
| Usable 71.5% over 24 h | Merschel & Reinhardt (2022) | 71.4 to 71.6% |
| Usable 94% at night | Merschel & Reinhardt (2022) | 93.9 to 94.2% |

All targets are reproduced within about 1.5 percentage points. Calibrated day-to-day variation is large (log SD 1.2 to 1.4) with strong persistence (0.8 to 0.9), which is what is needed to reproduce both Måneheim figures together.

---

#### 3. Results

##### κ makes almost no difference

| Coverage | Misclassified (Option B, all κ) | Median relative error (all κ) | Participants changing ESVEA class vs main estimate |
|---|---|---|---|
| Typical (blocks worn 95%) | 1.6 to 2.0% | 8.1 to 8.7% | **0.7 to 1.1%** |
| Poor (blocks worn 75%) | 3.1 to 3.7% | 14.5 to 15.5% | **2.5 to 3.0%** |

Within any one scenario, moving κ from 0.5 to 4 h changes misclassification by at most 0.2 percentage points and the median error by at most 0.4 points. Class changes stay well under the 10% robustness limit in every scenario.

**Conclusion: κ = 1 h, with 0.5 to 4 h reported, is supported. The sensitivity analysis is robust to κ.**

##### A second finding: the per-block rule has a cost when coverage is poor

| Coverage | Main estimate computable | Main estimate median error | Option B computable | Option B median error | ≥3 per-block valid days | ≥3 day/night valid days |
|---|---|---|---|---|---|---|
| Typical | 98.4 to 98.9% | 9.7 to 10.4% | about 99% | 8.1 to 8.7% | 82 to 84% | 88 to 89% |
| Poor | 80.5 to 82.0% | 19.4 to 21.2% | about 95% | 14.5 to 15.5% | **20 to 21%** | 58 to 61% |

- With typical coverage, the main estimate and Option B are close.
- With poor coverage, the per-block rule discards many days. The main estimate then becomes **less** accurate than Option B, because large day-to-day variation makes using more days worth more than avoiding thin blocks. Only about one participant in five would have 3 per-block-valid days.

**What this means:** keep the per-block rule as the main estimate (it adds no outside assumption), but state that if device verification shows poor block coverage, Option B is the more informative estimate. This is a point to raise with your supervisors, not a change to make now.

---

##### A third estimator: pooling each block across the participant's own days

For each block, total corrected PACs ÷ total usable hours across all day/night-valid days (minimum 1 usable hour per block across the week), then daily count = Σₕ 6 × block rate. It uses no outside profile.

| Coverage | Estimator | Computable | Misclassified | Median relative error |
|---|---|---|---|---|
| Typical | Main (per-block days) | 98.4 to 98.9% | 2.1 to 2.5% | 9.7 to 10.4% |
| Typical | Option B, κ = 1 h | 98.9 to 99.2% | 1.6 to 2.0% | 8.1 to 8.6% |
| Typical | **Pooled by block** | 98.5 to 98.9% | 1.8 to 2.1% | 8.4 to 8.8% |
| Poor | Main (per-block days) | 80.5 to 82.0% | 4.2 to 4.4% | 19.4 to 21.2% |
| Poor | Option B, κ = 1 h | 95.4 to 95.9% | 3.1 to 3.7% | 14.6 to 15.4% |
| Poor | **Pooled by block** | 87.1 to 88.3% | 2.7 to 3.3% | 13.9 to 15.1% |

Pooling matches Option B's accuracy without borrowing the Larsen profile, and is clearly better than the per-block-day estimate when coverage is poor. It is the recommended participant-level estimate; per-day values (per-block rule) remain for day-to-day stability, and Option B remains the sensitivity analysis.

#### 4. Limits

- Every unknown is swept over two values only (individual shape, clustering, coverage). Other values are untested.
- The Måneheim target assumes their "high PAC frequency" corresponds to ≥480/day against a 14-day reference; their threshold and reference were not re-checked.
- The Larsen profile is used both to generate the data and in Option B. If real diurnal patterns differ more than the swept individual deviation, Option B would do worse than shown.
- Retention and PAC identification are perfect here. RO2 errors are not simulated.
- Thresholds for the day/night rule (2 h night, 6 h day) are assumed; the per-block minimum (1 h) is the proposed value, to be set at device verification.

---

#### 5. Suggested text for the proposal (Section 3.4, after the sensitivity sentence)

> The shrinkage strength κ is set at 1 hour, with 0.5, 2 and 4 hours also reported. In a pre-specified simulation calibrated to published wear, signal-quality and ectopy data (Ding et al., 2023; Haeusler et al., 2025; Måneheim et al., 2024; Merschel & Reinhardt, 2022), varying κ across this range changed ESVEA class in at most 3% of simulated participants. κ is checked in the RO3 data by masking blocks on fully covered days.

About 75 words.


## 16. `handover/analyses/pulsewatch_retention/Pulsewatch_Beat_Retention_Data_Check.md`

### Pulsewatch beat-retention data check

**Purpose:** decide how Equation 3.1 and Section 3.4 of the proposal are written. Equation 3.1 estimates π̂, the chance that a real beat survives into the smartwatch interval series, as a function of motion.

**Status:** feasibility check on local files only. No model was fitted, and the numbers below are not parameter estimates. The proposal text was not available when this was drafted, so the draft wording and table entries still need fitting to it.

**Update, 2 November 2026:** a later test on raw watch files did not pass its locked rule, and the draft text below predates it. The test result and the decision taken are in `methodology/Pulsewatch_Beat_Retention_Precheck_Config.md`, which takes precedence where the two differ.

#### Answers

| Question | Answer | Basis |
|---|---|---|
| **Q1.** Accelerometer for the same periods as the PPG? | **Yes, magnitude only** | 50 Hz, 1,500 samples per 30-s segment, paired with each PPG segment. The release documents the tri-axial signal as converted to magnitude, so 3-axis data is not available. |
| **Q2.** Beat-level ECG timing? | **Yes, for clinical subjects only** | R-peak sample indices at 250 Hz. They are detector output and carry no beat types. |
| **Q3.** Watch and ECG time-aligned? | **Partly** | The released alignment is not accurate to the beat. A lag fitted per session recovers beat matching in most patches, but not all. |

**Effect on the proposal's decision table:** closest to the row "Yes / Yes / Yes", where the motion part is estimated on Pulsewatch. That holds only with per-session lag correction and the limits listed below.

#### Files and keys

| Source | Location | Contents |
|---|---|---|
| Segment `.pt` (Elgendi set) | `synapse_data\untar\PPG_Elgendi_30sec_HR_ACC_pt` | `PPG_filt_csv` (1500, 2), `ACC_raw_csv` (1500, 2), `PPG_filt_Elgendi`, `PPG_peak_loc_Elgendi_4_2013`, `HR_Elgendi_4_2013`, `new_PPG_peak_loc_Elgendi`, `new_HR_PPG_Elgendi` |
| Segment `.pt` (WEPD set) | `synapse_data\untar\PPG_filt_30sec_HR_pt` | `PPG_filt_csv`, `PPG_filt_WEPD`, `PPG_peak_loc_WEPD`, `PPG_HR_WEPD`, `new_PPG_peak_loc`, `new_HR_PPG` (no ACC) |
| ECG hour files | `build\ecg_fresh\Filtered_ECG_Peaks`, `synapse_data\ecg\Filtered_ECG_Peaks` | `Billal_ECG_filt_1_hr_this` (900000, 1), `Billal_ECG_peak_1_hr_this`, `Billal_ECG_HR_1_hr_this`, `ECG_time_1_hr_this` (900000, 1) |
| Alignment index | `synapse_data\ecg\aligned_index.csv` | `seg_name`, `patch_id`, `hour_idx`, `start_idx`, `end_idx`, `contain_empty`, `pad_front`, `pad_end`, `fs_ecg`; 140,099 rows, all clinical |
| Labels | `synapse_data\03_Labels` | `table_file_name`, `final_AF_GT_20230921`; one label per 30-s segment |

**Local ECG coverage:** 10 patches from 8 subjects (1,130 hour files). The release describes clinical-trial ECG beyond this, which has not been downloaded.

**Clocks:** `PPG_filt_csv` column 0 looks like a UNIX millisecond timestamp with a 20 ms step. `ECG_time_1_hr_this` is on a much smaller scale, so these two columns cannot be compared directly as clocks. Alignment has to go through `aligned_index.csv`.

#### Evidence

| Check | Result |
|---|---|
| Session-fitted lag, held-out segments | Median ECG-beat match 0.867, PPG-peak precision 0.871 |
| Mismatched-session control, same method | Median 0.222 |
| Single fixed lag across all patches (separate run, 916 segments) | Median 0.151, below its control of 0.233 |
| Match by motion tertile | Mean 0.932 / 0.731 / 0.715 (low / mid / high) |

The motion tertiles are pooled across subjects and use segment-level ACC SD, so they are confounded by subject and do not show a motion effect.

##### Per-patch results (session-fitted lag)

| Patch | Held-out segments | Sessions | Match (median) | Control (median) | Session lag IQR (s) |
|---|---:|---:|---:|---:|---|
| 017B | 43 | 11 | 0.756 | 0.236 | −0.05 to 0.26 |
| 044A | 158 | 40 | 0.970 | 0.224 | −0.12 to 0.26 |
| 055A | 28 | 7 | 0.964 | 0.219 | −0.57 to −0.02 |
| 075A | 171 | 40 | 0.649 | 0.203 | −2.10 to 2.23 |
| 083A | 23 | 6 | 0.900 | 0.230 | 0.19 to 0.24 |
| 098B | 28 | 7 | 0.277 | 0.281 | −0.33 to 0.53 |
| 109A | 176 | 40 | 0.914 | 0.208 | −0.20 to 0.52 |
| 110A | 6 | 2 | 0.675 | 0.289 | −0.43 to 0.14 |
| 110B | 30 | 9 | 0.863 | 0.246 | 0.18 to 1.60 |

Patch 098B is no better than chance. Patch 110A has too few segments to interpret. Patch 098A produced no sessions for this test.

##### Method

The analysis ran as an inline read-only script that was not saved, so this description is the record of it.

- **Sample:** segments in `aligned_index.csv` with a `.pt` file and an ECG hour file, grouped into sessions by filename prefix. Sessions needed at least 6 usable segments, with up to 40 randomly chosen sessions per patch. Result: 663 held-out segments, 162 sessions, 9 patches, 8 subjects.
- **Beats:** ECG times from `Billal_ECG_peak_1_hr_this` within `start_idx` to `end_idx`. PPG times from `new_PPG_peak_loc_Elgendi` at 50 Hz.
- **Lag fit:** within each session, the lag was searched from −3 to +3 s in 0.02 s steps to maximise match on alternating segments, then scored on the remaining segments.
- **Match:** an ECG beat counts as matched if a PPG peak lies within ±100 ms after applying the lag. Precision applies the same test from PPG peaks to ECG beats.
- **Control:** the same lag fit and scoring, pairing a session's ECG with PPG from a different session of the same patch.

#### Limits

1. **Offline detector:** the PPG peaks come from an offline Elgendi detector on filtered PPG, not from intervals reported by the watch. π̂ is therefore detector retention on Samsung watches, and applying it to Garmin needs a stated transport assumption.
2. **Motion selection:** 215,428 of 403,022 label rows are code −1, which the local setup notes describe as mostly >5 s motion noise or unadjudicated. `.pt` files exist only for labelled segments. In the one subject with raw files on disk, there are 566 raw PPG files and 78 `.pt` files. Local data under-represents high motion, so π̂ would be biased upward at high motion unless the raw `.txt` files are obtained.
3. **Rhythm coverage:** the ECG is clinical-only, and only about 184 AF segments have ECG (subjects 017, 075 and 110). The 3xx and 4xx cohorts have none, so the motion term cannot be estimated separately in AF.
4. **Beat types:** `Solo.Beats.txt` is in the raw ECG folder that project rules prohibit. Beat-class retention stays with RO1 on Icentia11k.
5. **Sample size:** 8 subjects support a feasibility claim, not a parameter estimate.

#### Draft proposal text

##### Equation 3.1

$$\hat{\pi}(c, m) = \pi_{\text{class}}(c) \times \pi_{\text{motion}}(m) \tag{3.1}$$

where the motion component is estimated on Pulsewatch with a mixed-effects logistic model:

$$\text{logit}\,P(R_{ijk} = 1 \mid m_{ijk}) = \alpha + u_i + v_{ij} + \beta\, m_{ijk}$$

- $R_{ijk} = 1$ if ECG beat $k$ in session $j$ of subject $i$ has a PPG peak within tolerance after session-lag correction.
- $m_{ijk}$ is the SD of accelerometer magnitude in a window around the beat. The window length is still to be specified.
- $u_i$ and $v_{ij}$ are subject and session random intercepts.
- $\pi_{\text{class}}(c)$ is the beat-class retention from RO1 on Icentia11k.

The multiplicative form assumes that beat class and motion act independently on retention. This is an assumption, and Pulsewatch cannot test it because the usable ECG files carry no beat types.

##### Section 3.4 retention paragraph

> The motion component of beat retention will be estimated on Pulsewatch, the only dataset in this proposal with concurrent reference ECG, wrist PPG and accelerometer recordings. For each ECG R-peak, retention is defined as the presence of a PPG peak within a set tolerance, modelled against accelerometer magnitude with subject and session random effects. A feasibility check on 8 clinical subjects showed that the released alignment is not accurate to the beat: a single fixed lag performed no better than mismatched segments (median match 0.151 vs 0.233). A lag fitted within each recording session restored matching on held-out segments (median 0.867 vs 0.222). Lag correction is therefore part of the method. A session is retained only if its held-out match exceeds a mismatched-session control, and the number of sessions dropped will be reported.
>
> Five limits apply. First, PPG peaks come from an offline detector on Samsung watch signals rather than from device-reported intervals, so applying the estimate to the Garmin cohort rests on a transport assumption. Second, segments labelled as excluded, which are mostly motion-corrupted or unadjudicated, are absent from the processed release; analysis restricted to it would overstate retention at high motion, so the raw watch files are required for the final estimate. Third, reference ECG is available only for clinical-trial subjects and covers about 184 AF segments, so the motion effect cannot be estimated separately in AF. Fourth, the usable ECG files carry no beat types, so the beat-class component comes from RO1 on Icentia11k and the two components are combined multiplicatively by assumption. Fifth, the feasibility result comes from a small subset of subjects and is not a parameter estimate. The concurrent-ECG substudy in RO3 (10 to 15 participants wearing an ECG patch with the watch) is retained because it provides the only direct estimate on the Garmin device.

##### Table 3.1: Pulsewatch entry

| Field | Entry |
|---|---|
| Role | Estimates the motion component of beat retention, $\pi_{\text{motion}}(m)$ |
| Signals used | Wrist PPG (50 Hz), accelerometer magnitude (50 Hz), reference ECG R-peaks (250 Hz) |
| Subjects used | Clinical-trial cohort only |
| Device | Samsung Gear S3 / Galaxy Watch 3, Cardea SOLO ECG patch |
| Alignment | Released alignment plus per-session lag correction |
| Main limits | Offline peak detector; high-motion segments need raw files; few AF segments with ECG |

##### Table B.2: Pulsewatch entry

| Field | Entry |
|---|---|
| Identifier | Synapse project `syn23565056`, dataset folder `syn64402376` ("Pulsewatch2025"); download through the authors' Google Drive after a Google Form request |
| Accelerometer | Yes, magnitude only (not 3-axis) |
| Beat-level ECG | R-peak indices for clinical subjects; no beat types in the filtered files |
| Labels | 30-s adjudicated labels (NSR, AF, PAC/PVC) |
| Time alignment | Partial; per-session lag correction required |

#### Recommendation

Keep the RO3 concurrent-ECG substudy. Pulsewatch can provide a motion-retention estimate on Samsung hardware, but only the substudy measures retention directly on Garmin.

#### Open items

- **Data use terms:** no explicit licence or permitted-use statement was found, so permission for a beat-loss model is inferred, not stated. The Google Form's only commitment is to cite the authors' papers, and it also asks for the planned use. The Synapse API lists 0 access requirements for both `syn23565056` and `syn64402376`. The Drive folder was not checked for a licence file. To do: check that any planned use submitted on the form covers this work, ask the dataset contact (Dong Han) for written confirmation, and check the UM AI guidelines separately.
- **Further data, needing separate approval:** the remaining `Filtered_ECG_Peaks` patches and the raw `01_Clinical_Trial` watch files. A rough estimate for all ECG patches is 150 to 230 GB, extrapolated from local patch sizes and not checked against the Drive.
- **Model fit:** should wait for that data.


## 17. `handover/analyses/pulsewatch_retention/Pulsewatch_Beat_Retention_Precheck_Config.md`

### Pulsewatch beat-retention pre-confirmation: data and configuration

**Purpose:** record the data, settings and pass rule for a small test on raw watch files. The test decides whether the motion term in Equation 3.1 looks workable before committing to the full download of about 338 GB.

**Status:** settings and pass rule locked on 2 November 2026, before any result from this test was seen. Report any later change as made after seeing the results.

**Related files:**
- Earlier data check and draft proposal text: `methodology/Pulsewatch_Beat_Retention_Data_Check.md`
- Test script: `build/beat_retention_raw_test.py`
- Results, once run: `build/beat_retention_raw_results.json`

#### Why this test is needed

The earlier check used labelled segments only. About half of the label rows are code −1, which the setup notes describe as mostly >5 s motion noise or unadjudicated, and those segments have no `.pt` files. That leaves high motion under-represented, so retention at high motion could look too good.

This test adds the raw watch files, so excluded segments can be scored too.

#### Data

##### Size

| Item | This test | Full release | Share |
|---|---:|---:|---:|
| Raw watch files (`01_Clinical_Trial`) | 10.35 GB, 8 tars | 109.32 GB, 101 tars | 9.5% |
| ECG R-peak files (`10_Filtered_ECG_Peaks`) | 9.63 GB, 10 patches, 1,130 hour files | 228.37 GB, 157 tars | 4.2% |
| Subjects with ECG | 8 | 71 | 11% |

The raw tars go in a new folder, `synapse_data\raw_watch_8subj`. The ECG files are already local, and no existing data is changed. The download is MD5-checked against the Drive.

##### Subjects

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

##### Segment groups

| Group | Label code | Use |
|---|---|---|
| `labelled` | 0, 1, 2 | Lag fit and scoring |
| `excluded` | Negative codes | Scoring only |
| `noise_3` | 3 | Scoring only, reported separately |
| `no_label` | No row in `03_Labels` | Scoring only, reported separately |

#### Configuration

These settings are coded in `build/beat_retention_raw_test.py`.

##### Signals

| Setting | Value |
|---|---|
| PPG source | Raw `*_ppg_*.txt` from the tars, 50 Hz, 1,500 samples |
| ACC source | Paired raw `*_accel_*.txt`, 50 Hz, 1,500 samples, magnitude |
| PPG filter | `signal_proc.bandpass_ppg`: 0.5–8 Hz, order 3, zero-phase |
| PPG peaks | `signal_proc.detect_ppg_peaks`: Elgendi-style, windows 0.111 s and 0.667 s, β 0.02, 0.30 s refractory |
| ECG beats | `Billal_ECG_peak_1_hr_this`, 250 Hz, from `build\ecg_fresh` and `synapse_data\ecg` |
| Alignment | Authors' per-segment tables in `Aligned_ECG_LinearInterp`, read with `pulsewatch.mat_table`, plus the session lag below |

Excluded segments have no `.pt` peaks, so one detector is used for every segment. As a bridge to the earlier test, held-out labelled segments are also scored with the authors' `new_PPG_peak_loc_Elgendi` peaks.

##### Sessions and lag

| Setting | Value |
|---|---|
| Session definition | Shared filename prefix before `_ppg_` |
| Eligible session | At least 4 labelled segments after the segment rules |
| Sampling | Up to 300 random sessions per subject, seed 11 |
| Lag search | −3 to +3 s in 0.02 s steps, maximising beat match |
| Lag fit data | Alternating labelled segments only |
| Scored segments | The other labelled segments and all non-labelled segments in the session |

The lag never comes from a segment being scored, and never from a noisy one.

##### Segment rules

A segment is skipped and counted if any of these apply:
- No alignment file, an unreadable one, or no alignment values in it
- `contain_empty` is set
- It crosses an hour boundary (`start_idx > end_idx`)
- Its ECG patch or hour file is not local
- Fewer than 5 ECG beats, or no paired accelerometer file
- The PPG or ACC file cannot be read or does not have 1,500 samples

##### Scoring

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

#### What this test can and cannot show

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

#### Proposed pass rule

Treat the test as a pass only if all three hold. "Enough beats" means at least 500 beats in a bin, from at least 3 subjects each contributing at least 50 beats.

1. **Above chance at high motion:** the lower bound of a 95% interval on excess over control, bootstrapped by subject, is above zero in every top bin with enough beats.
2. **Consistent within subjects:** at least two-thirds of subjects with 2 or more eligible bins show lower excess in their highest eligible bin than in their lowest.
3. **Detector comparable:** the absolute difference in match rate from the authors' `.pt` peaks, on the same held-out labelled beats, is at most 0.05 pooled and at most 0.10 in every subject.

##### Details added to make the rule computable

These were not specified in the review and were fixed before the run:

- **Primary analysis:** sessions passing the quality gate, all scored segment groups together, one-to-one beat match. All-session results are reported as a sensitivity check.
- **Top bins:** 0.5–1 and ≥1 m/s². If neither has enough beats, criterion 1 is not met.
- **Eligible bin for criterion 2:** at least 50 beats from that subject. If fewer than 3 subjects have 2 or more eligible bins, criterion 2 is not met.
- **Criterion 3:** uses all sessions and beats at least 1 s from the segment edges, with each detector's own fitted lag. The per-subject limit applies to subjects with at least 50 such beats.
- **Bootstrap:** 2,000 resamples of subjects, seed 11. With 8 subjects this interval is coarse.

#### What each outcome means

| Outcome | Proposal wording | Next step |
|---|---|---|
| **Pass** | Cite as feasibility evidence for estimating the motion term; no π̂ value | Download the remaining data when you're ready to fit the model |
| **Fail** | Motion term stays a stated assumption, with motion as a sensitivity analysis | The RO3 concurrent-ECG substudy provides the estimate |

Either way, the RO3 substudy stays, because it is the only direct estimate on Garmin.

This table is kept as written before the run. The test did not pass, and the decision actually taken departs from the Fail row: see "Contradiction and decision" below.

#### Result (run 2 November 2026)

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

#### Contradiction and decision (2 November 2026)

This decision was made after seeing the results.

##### The contradiction

| Source | What it says about a failed test |
|---|---|
| "What each outcome means" in this file | The motion term stays a stated assumption, with motion as a sensitivity analysis, and the RO3 substudy provides the estimate |
| The review of settings and pass rule | The data check alone is enough to rewrite Equation 3.1 and Section 3.4, and "either way the proposal stands" |

The two were written before the run and did not anticipate a partial result, where the motion criteria were met and the detector criterion was not.

##### The decision

**The motion term stays in the plan, to be estimated on Pulsewatch during RO2. The test is not described as passed.** This is a looser reading of the failure than the Fail row, and the proposal must say the detector criterion was not met.

**Why:**
- Criteria 1 and 2 support a motion effect that can be measured.
- Criterion 3 questions the absolute level of retention, not whether the motion effect exists.
- The data needed for the estimate exists.

**Not changed:** the pass rule, the recorded outcome (not passed) and the original outcome table.

##### What this adds to the RO2 plan

1. **Detector sensitivity analysis:** name the detector used for π̂ and report results with an alternative, because absolute retention differed by 0.097 between detectors.
2. **Lag method independent of labelled segments:** the current method reached only 2.5% of excluded segments and 0.8% of no-label segments.
3. **RO3 concurrent-ECG substudy stays:** it is the only direct estimate on Garmin.

No π̂ value is reported from this test.

##### Sentence for the proposal

> A pre-specified check in 8 subjects found beat matching above chance at high motion and falling as motion rose, but absolute retention depended on the peak detector (0.850 vs 0.752), so the estimate will be reported with a detector sensitivity analysis.

##### Still open

- The proposal has not been updated. Its path and approval for the rewrite are still needed.
- The lag method in item 2 has not been designed or tested, so it may not reach the noisiest sessions either.

#### Decisions recorded

- Settings approved with four changes: one-to-one matching, a units check with quintile bins, interval-level retention, and skip counts recorded before scoring.
- Pass rule approved with tightened definitions.
- This test is enough for the proposal stage and is not strictly required. The full 338 GB download waits until after the defence, for fitting π̂ during RO2.


## 18. `handover/review_paper/Review_Reference_Corrections.md`

### Review paper: reference verification and corrections

All 79 references were checked against PubMed, Consensus and Wiley Scholar Gateway (plus publisher pages for computing venues). All 79 exist. The items below need changes.

#### Claims not supported by the source (fix first)
| Ref | Issue | Suggested correction |
|---|---|---|
| 1 Habibi | No comparison with classical statistics in the paper | Report the pooled AUC 0.82 (0.78 to 0.85) across 12 studies only |
| 18 Goh | "Pools three or fewer studies" is wrong | 24 studies; AF-after-stroke subgroup of 3 studies, mean AUROC 0.75 |
| 19 Kawamura | No meta-analysis | 19 studies (3 post-stroke); 37% externally validated; 0% of models shared |
| 32 Huntelaar | Exclusion reason (rule-based filter) is wrong | FibriCheck is described by its authors as deep-learning based. Exclude because no model was developed or evaluated and the aim was AF yield, not recurrence |
| 33 Han 2026 | Cohort and "not reported in abstract" are wrong | 72 stroke/TIA survivors (Pulsewatch) + 34 AF-trial patients; abstract reports PAC/PVC sensitivity 83% and AF accuracy 97.31% |
| 37 Alsalman | CV description wrong | SMOTE applied within training folds of stratified 10-fold CV; test folds unresampled; no external validation |
| 54 Schoels | 0.88 attributed to Bayesian fusion | Tree ensemble 0.88 (Bayesian fusion 0.89) in CV; 0.80 internal hold-out for new AF; 0.79 external vs AS5F 0.68 to 0.69 |
| 56 Jeon | Development cohort is not "non-stroke" | 44,085 sinus-rhythm ECGs from 12,666 patients with and without AF; combined 0.906 model not independently validated; "left atrial diameter" |
| 59 Holmes WP287 | Overstates superiority | AI-ECG 0.690 beat CHA2DS2-VASc (0.597) but not CHARGE-AF (0.651, p = 0.233); authors call all three suboptimal |
| 61 Lin & Luo | No recurrent network is proposed | Delete "recurrent": transformer (TransformerJM) or convolutional encoder |

#### Outcome or design framing
- 39 Axford and 40 Kim JT: the outcome is a composite (recurrence or death; stroke, MI or death), not recurrence alone. 48 Kim 2023: composite MACE.
- 51 Ke: case-control design (recurrent vs first-ever admissions), not a cohort.
- 36 Wang: 0.887 to 0.946 is not labelled as test AUC; report "ROC analysis (10-fold CV 0.777 to 0.959)", single centre.
- 23 Mittag: inclusion was limited to studies reporting performance above 0.95, so pooled performance is inflated by selection.
- 74 Hu: detects prevalent CVD (cross-sectional), not prediction. 78 Fang: 6-month functional outcome, not recurrence.
- 58 and 59 Holmes: same 863-patient cohort; do not count as independent evidence.
- 21 Alhakeem: "early stroke prediction" rather than "first stroke".

#### Metadata
- 1: author is Habibi, M. A.; Acta Neurol Belg 2025;125(3):609 to 624.
- 6 Ababneh: add 21(7):910 to 922. 13 Webb: 2018;49(1):62 to 67. 15: add 5(3):335 to 343.
- 22 Olawade and 23 Mittag: volume 249 and 207 are likely issue-year 2025 and 2026; use one convention.
- 33: add 73(4):1679 to 1693. 35 Vodencarevic: add 53(7):2299 to 2306; "double nested CV".
- 50: author "Zhou, Q."; n = 625. 51: author "Ke, L.". 55 Yu: 2025 in print (Int J Stroke 20(4):411 to 418).
- 68: single author Altwajre, B. A. N. (2025); weak venue, consider replacing.
- 70 Haule: confirm year and volume (article 109610). 73: first author Tabassum, I. 77 Lacson: use 2019 consistently.
- In-text: the Pulsewatch cohort is not "106 survivors" (see ref 33).

#### Source-internal inconsistencies (avoid quoting)
- 54: AS5F 0.69 in the abstract vs 0.68 in the text. 57 Choi: "14.4%" does not equal 58/352 (16.5%). 60 Ding: SUS 65 in the abstract vs 62.8 in the text. 52 Zhang: prospective CI in the abstract is a typo.


---

# Part B. Review and revision drafts


## 19. `drafts/proposal_revisions_draft.md`

### Draft revisions for the proposal defence (not yet applied)

**Status:** approved by the candidate and **applied on 3 November 2026** to `proposal/source/content.txt`, `proposal/Ridhwan_Research_Proposal_UM.docx` and the slide deck (version 44). E1 and E11 still need supervisor reconfirmation: see `proposal/SUPERVISOR_RECONFIRMATION_E1_E11.md`.
**Base version:** handover of 3 November 2026 (`content.txt`, 45-slide deck, version 34).
**House rules followed:** APA 7th edition; no em dashes; main text kept at or under 7,000 words.

---

#### 0. Summary

| ID | Review issue | Problem | Where | Main-text words |
|---|---|---|---|---:|
| E1 | #1 | Equation 3.1 ignores the burden dependence that Section 4.2 reports (revised: Garmin flags, not deletes) | 3.4 text, Eq. 3.1, 3.2, 3.4; 4.2 | +40 |
| E2 | #2 | The epoch scale has no day-long training data on Icentia11k | 3.4 para 1 | +45 |
| E3 | #3 | "Daily-count MAE" is not daily on Icentia11k | H2, Table 3.5, Table B.1 | +8 |
| E4 | #4 | Flag-as-input plus inverse weighting can count a beat twice; p̂ must be calibrated | 3.4 text, 2.8 | +35 |
| E5 | #5 | No PPG timing-noise operator in RO4a | 3.6, Table 3.4 | +21 |
| E6 | #6 | No Garmin-side check of the motion term | 3.5 | +11 |
| E7 | #8 | Coverage gate described as a model component | 3.4, Table 3.2 | +12 |
| E8 | #9 | Role of the rate head undefined | 3.4 para 1 | +19 |
| E9 | #10 | RO3 primary can pass while ESVEA is rarely computable | 3.5, Appendix C | +14 |
| E10 | #11 | Icentia11k patient sets not shown as disjoint | Table 3.1, new Table B.3 | +2 |
| E11 | #12 | Pilot weight 0.9 chosen on test cohorts; legacy external labels withdrawn | Abstract, 4.1, Table 4.1 | -8 |
| | | **Subtotal before trims** | | **+199** |
| T1, T3 to T8, T11 | (word limit) | Trims (T2 merged into E11c) | 1.1, 1.6, 2.1, 2.4, 3.4, 4.2, 5.1 | -177 |
| | | **Net change** (current main text 6,958; limit 7,000) | | **+22 → 6,980** |

All eight trims (T1, T3 to T8, T11) are needed to stay under the limit. T5 also adds 3 words where PPV is next defined (Section 2.6), giving about 6,983. If supervisors reject a trim, a different trim is needed: E8 is decided (rate head kept), so its removal alternative is no longer the fallback.

Word counts follow the handover rule: Chapter 1 to the start of References, table rows counted, captions, equations and appendices not counted.

##### Decisions (approved by the candidate, 3 November 2026)
All drafted revisions (E1 to E11, trims T1, T3 to T8 and T11) are approved by the candidate for now. Nothing has yet been applied to `content.txt`, the docx or the slide deck.

| Item | Candidate | Supervisors |
|---|---|---|
| E1, retention corrects only silent loss (replaces decision 6g) | Approved | **Ask** before applying: reverses a logged decision and changes RO1's role |
| E11, pilot rewritten (threshold did not transfer; legacy values withdrawn; abstract recall 45% to 100%) | Approved | **Ask** before the defence: changes a headline number they have seen |
| E4, no double counting; calibrated p̂ | Approved | Inform |
| E8, rate head kept as auxiliary target | Approved | Inform |
| E2, E3, E5 to E7, E9, E10, trims | Approved | Inform (part of the final docx they approve) |
| Title kept, prepared answer | Approved | Inform |
---

#### Review issues and where each is addressed

This section keeps the review that prompted these drafts, word for word, so each issue can be traced to its revision. Issue numbers match the review; draft IDs (E1 to E11, T1 to T8) match the sections below.

##### Issue map

| # | Review issue | Priority | Addressed by | Status |
|---|---|---|---|---|
| 1 | Equation 3.1 contradicts the preliminary finding on burden | Critical | E1, revised after the Garmin whitepaper: retention corrects only silent loss; RO1 filter loss moves to RQ2.4 | Approved by candidate; ask supervisors |
| 2 | Epoch-scale encoder has no day-long training data | Critical | E2: option b (pseudo-days) plus option c (Pulsewatch windows in real order across days) | Approved by candidate; Pulsewatch timestamp check passed 3 November 2026 |
| 3 | "Daily-count MAE" is not daily | Critical | E3 | Approved by candidate |
| 4 | Flag as input plus inverse weighting can double-count; p̂ must be calibrated | Critical | E4 | Approved by candidate; Guo et al. (2017) reference verified against PMLR (see `Verification_Guo_H1_H2.md`) |
| 5 | No PPG timing-noise operator | Important | E5 | Approved by candidate; jitter spread to be measured on Pulsewatch |
| 6 | Motion term is the weakest link | Important | E6 | Approved by candidate |
| 7 | Title does not match the claimed contribution | Important | Section 4, prepared answer (title kept) | Answer drafted; no text change |
| 8 | Coverage gate is not a model component | Important | E7 | Approved by candidate |
| 9 | Role of the rate head undefined | Important | E8: keep as an auxiliary target | Decided (option A); supervisors informed |
| 10 | RO3 primary can pass while ESVEA stays uncomputable | Important | E9 (key secondary, not co-primary, to keep H3 and the sample size unchanged) | Approved by candidate |
| 11 | Patient partitions should appear in one place | Important | E10 (Table 3.1 pointer and new Table B.3) | Approved by candidate; set sizes and seeds when splits are drawn |
| 12 | Pilot weight chosen on the test cohorts | Important | E11, rewritten with the 3 November rerun (re-curated labels, w = 0.5) | Approved by candidate; ask supervisors (legacy values withdrawn) |
| F1 | Device not arrived; S3 crowded | Feasibility | Not drafted: one fallback slide, from Section 3.9 last paragraph | Open |
| F2 | Scope: which RO to drop first | Feasibility | Not drafted: prepared answer is RO4b, as Section 3.9 already defers it in the fallback | Open |
| H1 | "First" claims: IEEE Xplore and arXiv search | Housekeeping | `Verification_Guo_H1_H2.md` | Both claims hold; run IEEE Xplore's native search before naming it in Section 2.7 (optional +5 words) |
| H2 | Bhurane 93.96% | Housekeeping | `Verification_Guo_H1_H2.md` | Confirmed from the IEEE Xplore abstract (PAC/PVC sensitivity 93.96%; split not reported) |
| H3 | Supervisor approval of the final docx | Housekeeping | Decisions list in Section 0 | Open |
| H4 | Ethics committee name | Housekeeping | Section 3 checklist | Open |
| H5 | Pulsewatch permitted use | Housekeeping | Section 3 checklist | Open |
| H6 | Whether tables count towards 7,000 words | Housekeeping | Word budget in Section 0 (measured 6,958 before edits, about 6,983 after) | Open |
| H7 | Slide inconsistencies, especially `app-b3.html` | Housekeeping | Section 2 slide table (app-b3 row) | Partly drafted |
| H8 | Mock defence | Housekeeping | Section 4 prepared answers | Open |

Note on the word count: the review quoted "about 6,980" from the handover; counting `content.txt` with the handover rule gives 6,958, which is the base used in this draft.

##### Original review (verbatim)

> A panel reading closely will find each of them in Section 3.4 and Chapter 4. After those come some tightening and a few housekeeping items.
>
> **Critical: fix these in the proposal text**
>
> **1. Equation 3.1 contradicts your own preliminary finding.**
>
> * Section 4.2 shows PAC removal depends on burden (78.5% in ESVEA-negative patients vs 60.0% in ESVEA-positive), and concludes that "a single correction factor cannot restore the count."
> * Equation 3.1 then uses one fixed class retention (39.1%) multiplied by a motion term, with no burden or context term.
> * A sharp examiner will put those two sentences side by side.
> * Fix: either make π̂ depend on local ectopy density (for example, the PAC share of the preceding reference window, which is the mechanism you describe), or state plainly that the network handles burden dependence and the frozen π̂ only corrects device-side loss. H1 then becomes the justification for that design, rather than a finding the equation ignores.
>
> **2. The epoch-scale encoder has no day-long training data.**
>
> * The interval block runs "across windows within the day." Icentia11k gives at most 50 random 70-minute segments per patient with no clock time.
> * Nothing contiguous lasts longer than about 70 minutes. So RQ2.2 (epoch-graph vs summation for the daily rate) has no day-level sequence to train on and no day-level truth to test against.
> * Fix: say explicitly what the second scale trains on. Options:
>    * (a) Windows within a 70-minute segment, so the "epoch" scale is sub-hour.
>    * (b) Pseudo-days stitched from segments, as RO4a already uses. If you choose this, say the diurnal structure is synthetic.
>    * (c) Pulsewatch multi-day sessions for the epoch scale, at window level.
> * Without this, the second scale's evaluation is undefined.
>
> **3. "Daily-count MAE" is not daily.**
>
> * The RO2 reference is a patient-level rate × 24 from random segments. H2's metric name promises something the data can't measure.
> * Fix: rename it "patient-level daily-equivalent rate MAE", or similar, in H2, Table 3.5 and the slides. It's a cheap change that removes an easy attack.
>
> **4. "Flag as input" and inverse-probability reweighting can double-count.**
>
> * If flagged beats are kept and fed to the model, which beats were not "retained"? Equation 3.2 reweights by 1/π̂ as if beats had been deleted.
> * Fix: add one paragraph separating two kinds of loss:
>    * Device-side, unrecoverable: beats the watch never reports, gaps, pulse deficit. These are the only losses π̂ should correct.
>    * Analysis-side: flagged beats. The model sees these, so they should not be reweighted.
> * Also say that p̂ᵢ must be calibrated (for example, temperature-scaled on validation subjects) before summing. A supraventricular PPV of 36.8% (Dias et al.) shows how summed probabilities inflate a count.
>
> **Important: strengthen these**
>
> 5. There is no PPG timing-noise operator. RO4a degrades ECG RR intervals by rejection, gaps and pulse deficit, but not by the jitter of PPG peak timing, which is the main ECG-to-PPG difference (Theurl: rMSSD agreement only moderate). You already have paired PPG peaks and lag-corrected ECG R-peaks from the Pulsewatch pre-check, so you can estimate the jitter distribution and add it as a fourth operator. This is the most defensible answer to "your simulation is optimistic."
> 6. The motion term is the weakest link. It comes from a Samsung signal and an offline detector, and the pre-check failed its detector criterion. Add a Garmin-side check that needs no ECG: in RO3, plot the flagged-beat fraction against accelerometer motion. That doesn't validate π̂, but it shows whether the Garmin's loss-versus-motion curve has the same shape as Pulsewatch's.
> 7. The title doesn't match the claimed contribution. The title leads with the ST-GNN, but Section 2.8 says "the graph architecture is a means, not a claimed contribution." Expect "so why is it in the title?" Either reframe the title around the coverage-aware estimator, or prepare a one-sentence answer.
> 8. The coverage gate isn't really a model component. Equation 3.3 is a threshold rule, not a learned layer, yet it sits in the architecture figure and in the ablation list. Call it a reporting rule. Ablating it then means comparing abstention against always reporting.
> 9. The role of the rate head is undefined. Equations 3.2 and 3.4 use only the event head's p̂ᵢ. State what the rate head is for (an auxiliary loss? a cross-check?) or drop it.
> 10. The RO3 primary outcome can pass while ESVEA stays uncomputable.
>    * Your own simulation shows the problem. With poor coverage, about 60% of participants have three or more day/night-valid days, but only about 20% have three or more days valid under the per-block rule.
>    * H3 could therefore go green while ESVEA is rarely computable.
>    * Make "pooled ESVEA computable (≥1 h per block across the week)" a co-primary outcome or a pre-specified key secondary.
> 11. Patient partitions should appear in one diagram. Icentia11k is used for:
>    * the RO1 preliminary sample (298 patients)
>    * the H1 new patients
>    * RO2 train, validation and test
>    * RO4a held-out
>
>    Show all four as disjoint sets. Examiners check this for leakage, and right now it is spread across several sentences.
> 12. The pilot weight was chosen on the test cohorts. Report w = 0.5 as primary, since its thresholds weren't touched by test data, and give 0.9 as a sensitivity result. Clinical held-out AUROCs at w = 0.5 are actually higher (1.000 and 0.998). Only Simband drops, to 0.891, so you lose little and remove a criticism.
>
> **Feasibility questions to prepare for**
>
> * The device hasn't arrived and S3 is crowded (device verification, ethics, RO1 paper). Have the fallback ready as a single slide.
> * Scope: four ROs, three datasets and a prospective cohort. Be ready to say which RO you would drop first. The proposal's own logic points to RO4b.
>
> **Housekeeping before submission**
>
> * "First" claims: run the targeted IEEE Xplore and arXiv search. "No GNN applied to PPG or inter-beat intervals" is the claim most likely to be false outside PubMed, Consensus and Wiley.
> * Bhurane 93.96%: confirm it is the PAC/PVC sensitivity cited in Table 2.1, or drop it.
> * Supervisor approval: get it on the final docx, since a lot has changed since they last saw it.
> * Ethics committee name: confirm whether it is PPUM MREC or UMMC MREC.
> * Pulsewatch: get written confirmation of permitted use.
> * Postgraduate Office: ask in writing whether tables count toward the 7,000 words. You are at about 6,980, so the fixes above need trims elsewhere.
> * Slide inconsistencies from the handover: fix these, especially `app-b3.html`, which still describes the old "Stage 1 fits the retention curve" approach.
> * Mock defence: run one using the caveats list.
>
> Points 1 to 4 are the ones most likely to cause trouble on the day, and each can be fixed in roughly 50 to 150 words in Section 3.4. I can draft the replacement text within the word limit, and turn this list into a shareable checklist page for your supervisors.

---

#### 1. Proposal text (Chapter 1 to Chapter 4)

##### E1 · Retention corrects only silent device loss (Section 3.4)

*Responds to review issue #1 (see the issue register below the summary).*

**Revised on 3 November 2026 after checking the Garmin whitepaper** (Garmin, n.d., the source already cited in the proposal; see "Evidence" below). The earlier E1 made class retention depend on burden. That is no longer needed: the Garmin does not delete abnormal beats, so RO1's filter loss is not a device loss.

**Evidence (Garmin Enhanced BBI whitepaper, November 2023):**
- Abnormally short or long beats are kept and marked low confidence: the device marks "as low confidence any beats that are thought to be unlikely due to being abnormally short or abnormally long".
- Motion above a first threshold: beat kept, marked low confidence.
- Motion above a higher threshold, or extremely poor signal: no beat is given and "the time series will indicate a gap".
- Outlier removal is left to the researcher.
- Garmin has confirmed to the candidate that Enhanced BBI is recorded 24/7. The public whitepaper says it "is measured during the user's sleep interval", so keep Garmin's confirmation in writing and cite it as a personal communication if asked.

**Consequences for the method:**

| Loss | Visible in the export? | Handled by |
|---|---|---|
| Premature beat kept with a low-confidence flag | Yes, flagged | Model input (no correction) |
| Extreme motion or poor signal | Yes, marked gap | Observed time τ(d,h) and the coverage gate |
| Premature beat with no wrist pulse (pulse deficit), merged into one long interval | No | Retention π̂ (Equation 3.1) |
| Beat missed at moderate motion without a gap | No | Retention π̂ (Equation 3.1) |
| Flagged beats deleted by the analyst | Only if the analyst deletes them | RO1 filter results; the "flag as filter" regime of RQ2.4 |

The RO1 burden effect (78.5% vs 60.0% of PAC coupling intervals removed) applies only when flagged beats are deleted. Keeping the flag as input avoids it, so RO1 becomes the evidence for that design rather than a term in Equation 3.1. This removes the contradiction in review issue #1.

###### E1a · Section 3.4, paragraph 2, sentence on Equation 3.1 [main]
**Current**
> The flag enters the model as an input, and a separate reliability pathway bypasses both encoders: retention (Equation 3.1) combines beat-class retention from the RO1 filtering results with motion retention estimated on Pulsewatch, which pairs wrist PPG and accelerometer magnitude with reference ECG R-peaks; their product is an assumption, because those R-peaks carry no beat types.

**Proposed**
> The flag enters the model as an input, and a separate reliability pathway bypasses both encoders. As the Garmin flags abnormal beats and marks a gap where it gives none (Garmin, n.d.), gaps enter the observed time and the pathway corrects only silent loss: retention (Equation 3.1) combines pulse retention by coupling interval (Zheng et al., 2008) with motion retention estimated on Pulsewatch, which pairs wrist PPG and accelerometer magnitude with reference ECG R-peaks; their product is an assumption.

###### E1b · Section 3.4, definitions paragraph [main]
**Current**
> Formally, for day d and time-of-day block h, let A(d,h) be the retained beats, π̂ₖ(m) the probability that a beat of class k ∈ {PAC, other} is retained at motion m, p̂ᵢ the predicted probability that beat i is a PAC, mᵢ its accelerometer motion, and τ(d,h) the observed hours in the block. The retention model, daily rate, coverage gate and participant-level rate are:

**Proposed**
> Formally, for day d and time-of-day block h, let A(d,h) be the beats the device reports, π̂ₖ(m, q) the probability that a beat of class k ∈ {PAC, other} is reported at motion m and coupling ratio q, p̂ᵢ the calibrated probability that beat i is a PAC, mᵢ and qᵢ its motion and coupling interval as a share of the preceding interval, and τ(d,h) the observed hours in the block. The retention model, daily rate, coverage gate and participant-level rate are:

###### E1c · Equations (not counted)
```
EQ|π̂ₖ(m, q) = π̂_pulse(k, q) · π̂_motion(m)|3.1
EQ|R̂(d) = Σₕ (Lₕ / 24) · [ Σᵢ∈A(d,h) p̂ᵢ / π̂_PAC(mᵢ, qᵢ) ] / τ(d,h)|3.2
EQ|report R̂(d) only if c(d, h) ≥ θ_block for every block h|3.3
EQ|R̄ = Σₕ (Lₕ / 24) · [ Σ_d∈V Σᵢ∈A(d,h) p̂ᵢ / π̂_PAC(mᵢ, qᵢ) ] / Σ_d∈V τ(d,h)|3.4
```
π̂_pulse(other, q) = 1. The coupling ratio is written q because c(d, h) already denotes coverage and κ denotes Cohen's kappa. Check after the build that Equation 3.1 fits on one line.

###### E1d · Section 4.2, paragraph after Table 4.2 [main]
**Current**
> A single correction factor therefore cannot restore the count, which supports learning retention as a function of context in RO2.

**Proposed**
> A single correction factor therefore cannot restore the count after deletion, which supports keeping flagged beats as input (RQ2.4).

###### E1e · Appendix C, after the first paragraph (not counted)
> Beat loss was set to the 20% filter retention of 0.391, which is pessimistic for a device that flags abnormal beats rather than deleting them (Garmin, n.d.); results therefore isolate coverage under heavy beat loss.

###### E1f · Reference update (housekeeping)
The proposal's `REF|Garmin. (n.d.). *Garmin Enhanced BBI* [White paper]` is the same document. Its cover is dated November 2023 and its full title is "Garmin Enhanced BBI: An example night". Consider changing to `Garmin. (2023). *Garmin Enhanced BBI: An example night* [White paper]. Garmin Health. https://www8.garmin.com/garminhealth/news/Garmin-Enhanced-BBI_Final.pdf` and updating in-text citations from (Garmin, n.d.) to (Garmin, 2023).

**Risks to state if asked:**
- The pulse-deficit term uses the same published coupling-interval threshold (Zheng et al., 2008) as the RO4a pulse-deficit operator. Report RO4a across the operator's severity sweep so the test is not just checking the model's own assumption.
- The whitepaper is a vendor document (one subject, one night, Venu 2 Plus). Device verification confirms flag and gap behaviour on the study device and firmware.

**Superseded options (kept for the record):** the first E1 draft made class retention depend on local PAC share; its alternative left Equation 3.1 unchanged and relied on the network. Both assumed the device deletes abnormal beats, which the whitepaper contradicts.

---

##### E2 · What the epoch scale trains on (Section 3.4, paragraph 1)

*Responds to review issue #2 (see the issue register below the summary).*

The interval block runs "across windows to aggregate the day", but Icentia11k segments last about 70 minutes and carry no clock time, so there is no real day to train or test on.

###### E2a · Section 3.4, paragraph 1 [main]
**Current**
> At the epoch scale, an interval block of graph convolution and a selective state-space layer operates across windows to aggregate the day.

**Proposed**
> At the epoch scale, an interval block of graph convolution and a selective state-space layer operates across windows to aggregate the day. As Icentia11k segments are untimed, it trains there on pseudo-days built from each patient's segments, learning aggregation under gaps rather than a diurnal pattern; RQ2.2 is judged against the patient-level rate, and on Pulsewatch windows in real order across days, timed by file-name local time.

**Check E2 passed (3 November 2026)**, so the Pulsewatch clause is included (+14 words). Full results: `Result_E2_Pulsewatch_Timestamps.md`.
- **Pass:** Q1, 100% of files fall in 2019 to 2021; Q2, 64 of 108 subjects span 3 or more local days in order with no overlaps; Q3, 99.1% of segments match the US Eastern calendar offset, and the busiest hour is 01:00.
- **Not fully blind:** the pass definitions were written after seeing a sample of 11,735 files, before the full run.
- **Time base:** file-name time, read as US Eastern local time. Column 0 of `PPG_filt_csv` is **not** UTC; it appears to sit at a fixed UTC−5. Converting it as UTC would wrongly drop the 00–06 share from 43.2% to 19.1%.
- **Limits:** 0.9% of segments do not match the US calendar (including 353 unexplained January segments); 40 of 108 subjects do not span 3 days in labelled data; excluded segments come almost entirely from clinical subjects; 4xx cohort dates were not checked against a separate publication; travel outside Eastern time cannot be detected.
- **Coverage figures for later use (not in the proposal text):** only the 8-subject raw recording shares may be used for the RO3 fallback or Appendix C. They are pooled 22.9 / 22.3 / 28.6 / 26.3% and mean of subjects 18.2 / 21.6 / 40.0 / 20.1% across 00–06 / 06–12 / 12–18 / 18–24, from subjects who were not randomly chosen. Labelled shares (43.3% in 00–06) favour quiet night hours and must not be described as wear or coverage.
- **Do not claim:** that the timestamps are UTC; that Pulsewatch reflects Garmin coverage; any time-of-day ectopy pattern.

---

##### E3 · Rename the H2 metric

*Responds to review issue #3 (see the issue register below the summary).*

###### E3a · Section 1.3, H2 [main]
**Current**
> H2: on subject-wise held-out data, the two-scale ST-GNN with the quality flag as input has a lower daily-count mean absolute error than the best non-graph baseline.

**Proposed**
> H2: on subject-wise held-out data, the two-scale ST-GNN with the quality flag as input has a lower mean absolute error of the daily-equivalent count (Table B.1) than the best non-graph baseline.

###### E3b · Table 3.5, RO2 row, "Primary metrics" cell [main]
**Current**
> Beat level: PAC sensitivity, PPV, F1, precision-recall AUC. Day level: daily-count mean absolute error; calibration slope and intercept across burden levels

**Proposed**
> Beat level: PAC sensitivity, PPV, F1, precision-recall AUC. Patient level: mean absolute error of the daily-equivalent count; calibration slope and intercept across burden levels

###### E3c · Table B.1, new row after "Ectopy rate" (not counted)
```
Daily-equivalent count | 24 times a patient-level rate of ectopic beats per analysable hour; used on Icentia11k, whose segments are untimed, in place of a true daily count
```

---

##### E4 · No double counting, and calibrated probabilities (Section 3.4 and 2.8)

*Responds to review issue #4 (see the issue register below the summary).*

###### E4a · Section 3.4, paragraph 2, sentence after E1a [main, new sentence]
**Current**
> (none)

**Proposed**
> Flagged beats stay in the input unweighted, so no beat is corrected twice.

###### E4b · Section 3.4, paragraph 2 [main]
**Current**
> Retention is frozen and reweights surviving beats (Equation 3.2); time of day acts only through motion and coverage.

**Proposed**
> Retention is frozen and reweights reported beats (Equation 3.2); time of day acts only through motion and coverage. Because Equation 3.2 sums probabilities, p̂ᵢ is calibrated on validation subjects by temperature scaling (Guo et al., 2017).

###### E4c · Section 2.8, contributions paragraph [main]
**Current**
> Methodologically, the study treats the quality flag as evidence: a frozen retention model reweights retained beats, and a coverage gate decides when a daily value can be reported (Section 3.4, Equations 3.1 to 3.4).

**Proposed**
> Methodologically, the study treats the quality flag as evidence: a frozen retention model corrects for beats the device never reports, and a coverage gate decides when a daily value can be reported (Section 3.4, Equations 3.1 to 3.4).

###### E4d · New reference (APA 7; verified against the PMLR record on 3 November 2026)
```
REF|Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. In D. Precup & Y. W. Teh (Eds.), *Proceedings of the 34th International Conference on Machine Learning* (Vol. 70, pp. 1321–1330). PMLR.
```

**Note for the defence.** The Garmin whitepaper states that abnormal beats are flagged, not deleted (see E1), so double counting can arise only if the analysis both deletes flagged beats and reweights by 1/π̂. RQ2.4 ("flag as filter vs input vs input with correction") tests exactly that.

---

##### E5 · Fourth degradation operator: PPG timing noise (Section 3.6)

*Responds to review issue #5 (see the issue register below the summary).*

The strongest answer to "your simulation is optimistic because Icentia11k is ECG RR" is to inject the timing error between PPG peaks and ECG R-peaks, measured on the paired Pulsewatch data you already have.

###### E5a · Section 3.6, paragraph 1 [main]
**Current**
> Three degradation operators are applied, each calibrated from measured data (Table 3.4) and sampled independently of the training simulation, and results are reported across a severity sweep for each operator.

**Proposed**
> Four degradation operators are applied, each calibrated from measured data (Table 3.4) and sampled independently of the training simulation, and results are reported across a severity sweep for each operator.

###### E5b · Table 3.4, new row after "Pulse deficit" [main, table row]
**Current**
> (none)

**Proposed**
> Interval timing noise | PPG peak timing that differs from the ECG R-peak | PPG to R-peak offsets on Pulsewatch, swept

---

##### E6 · Garmin-side check of the motion term (Section 3.5)

*Responds to review issue #6 (see the issue register below the summary).*

###### E6a · Section 3.5, secondary questions sentence [main]
**Current**
> Secondary questions cover yield (RQ3.1), computability of the daily ESVEA denominator (RQ3.2), day-to-day stability (RQ3.3), activity (RQ3.4) and the ESVEA proportion as a plausibility check (Haeusler et al., 2025; Teare et al., 2014) (RQ3.5).

**Proposed**
> Secondary questions cover yield (RQ3.1), computability of the daily ESVEA denominator (RQ3.2), day-to-day stability (RQ3.3), activity, including whether the flagged-beat fraction rises with motion as on Pulsewatch (RQ3.4), and the ESVEA proportion as a plausibility check (Haeusler et al., 2025; Teare et al., 2014) (RQ3.5).

---

##### E7 · Coverage gate is a reporting rule

*Responds to review issue #8 (see the issue register below the summary).*

###### E7a · Section 3.4, paragraph 2, last sentence [main]
**Current**
> A coverage gate decides whether a daily value is reported at all (Equation 3.3).

**Proposed**
> A coverage gate, a fixed reporting rule rather than a learned layer, decides whether a daily value is reported at all (Equation 3.3).

###### E7b · Table 3.2, RQ2.3 row, "Models benchmarked" cell [main]
**Current**
> Remove chain edges, similarity edges, interval block, retention correction, coverage gate

**Proposed**
> Remove chain edges, similarity edges, interval block, retention correction; coverage gate vs always reporting

---

##### E8 · Role of the rate head (Section 3.4, paragraph 1)

*Responds to review issue #9 (see the issue register below the summary).*

###### E8a · Section 3.4, paragraph 1, last sentence [main]
**Current**
> An event head and a rate head produce beat-level and window-level estimates.

**Proposed**
> An event head gives the beat PAC probabilities used in Equations 3.2 to 3.4; a rate head, an auxiliary target for the window PAC count, is not used in reported estimates.

**Decision (3 November 2026): option A, keep the rate head as an auxiliary target.** Figure 3.2 and slide 14 stay as they are. In RO2, report how the rate head compares with the summed p̂; if the ablations show it adds nothing, drop it then. Supervisors are informed in the decisions note.

**Not chosen (kept for the record), removal:** "An event head gives the beat-level PAC probabilities used in Equations 3.2 to 3.4." Then redraw Figure 3.2 without the rate head and drop it from the slides.

---

##### E9 · Make pooled computability a key secondary outcome (Section 3.5)

*Responds to review issue #10 (see the issue register below the summary).*

Appendix C shows that under poor coverage 58% to 61% of simulated participants had three or more day/night-valid days, but only 20% to 21% had three or more days meeting the per-block rule. H3 could go green while per-day ESVEA is rarely computable.

###### E9a · Section 3.5, end of the paragraph on valid days [main, new sentence]
**Current**
> (none; follows "...the share of valid days meeting it answers RQ3.2.")

**Proposed**
> Computability of the pooled count (Equation 3.4) is a key secondary outcome (Appendix C).

###### E9b · Appendix C, final paragraph, new sentence (not counted)
> Under poor coverage, 58% to 61% of simulated participants had three or more day/night-valid days, but only 20% to 21% had three or more days meeting the per-block rule; the pooled count remained computable in 87% to 88%.

---

##### E10 · Disjoint Icentia11k patient sets

*Responds to review issue #11 (see the issue register below the summary).*

###### E10a · Table 3.1, RO4a row, "Data" cell [main, table row]
**Current**
> Held-out Icentia11k patients degraded to smartwatch-like intervals

**Proposed**
> Held-out Icentia11k patients (Table B.3) degraded to smartwatch-like intervals

###### E10b · New Table B.3 (appendix, not counted)
```
TABLE|Table B.3: Disjoint sets of Icentia11k patients
W|18|42|40
Set | Use | Size and selection
P0 | Preliminary RO1 analysis (Section 4.2) | 298 analysed of 300 sampled with a fixed seed
P1 | H1 test of burden-dependent retention | New random sample, size fixed before analysis
P2 | RO2 training, validation and test, split by subject | Random sample, split lists recorded and released
P3 | RO4a held-out substitution test | About 300, untouched until the RO2 model is frozen (milestone M4)
ENDTABLE
```
Fix the P1 to P3 sizes and seeds when the split lists are drawn (post-defence task in the handover).

---

##### E11 · Report the pilot with re-curated labels and the untuned weight (Section 4.1, abstract)

*Responds to review issue #12 (see the issue register below the summary).*

**Rerun received 3 November 2026** (`Check_E11_Pilot_Rerun_Weight_0.5.md`). Rule locked 2026-11-03 12:40 (+08:00), before any new-data result was computed. The lock was not blind: legacy and Pulsewatch clinical results had already been seen.

**Withdrawn:** the Simband and MIMIC-III values 0.891, 0.951, 0.944, 0.998 and 0.973. They used legacy external labels. The replacements use re-curated labels, with all of v2's training and validation subjects excluded; same v2 checkpoint, evaluation mode, no retraining.

**New results**

| Cohort | Subjects (AF); windows | AF vs rest, w = 0.5 | AF vs PAC/PVC, w = 0.5 | AF vs rest, w = 0.9 | AF vs PAC/PVC, w = 0.9 |
|---|---|---|---|---|---|
| Pulsewatch clinical | 16 (1); 48,396 | 1.000 (1.000 to 1.000) | 0.998 (0.997 to 1.000) | 0.997 (0.996 to 0.998) | 0.981 (0.949 to 0.998) |
| Simband | 6 (1); 46 | 0.995 (0.989 to 1.000) | 0.968 (not estimable) | 0.995 (0.970 to 1.000) | 0.994 (not estimable) |
| MIMIC-III | 3 (1); 1,215 | 0.995 (0.993 to 0.997) | 1.000 (not estimable) | 0.994 (0.991 to 0.996) | 1.000 (not estimable) |

Skipped resamples of 2,000: clinical 701, Simband 669, MIMIC-III 676.

| Cohort | AF windows | AF recall, 0.393 / 0.505 | NSR false alarms, 0.393 / 0.505 | PAC/PVC false alarms, 0.393 / 0.505 |
|---|---|---|---|---|
| Pulsewatch clinical | 170 | 100% / 95% | 8.9% / 5.3% | 18.3% / 9.8% |
| Pulsewatch AF-only holdouts (3 AF trial, 5 in-clinic) | 5,483 | 97% / 88% | no NSR windows | no PAC/PVC windows |
| Simband | 12 | 100% / 92% | 14.3% / 9.5% | 15.4% / 0.0% |
| MIMIC-III | 292 | 45% / 15% | 0.2% / 0.0% | 0.0% / 0.0% |

Operating points use the gfeat-head score, which does not depend on w. Thresholds were not re-tuned.

**What the results say**
- **Ranking transferred; the operating point did not.** AF vs rest AUROC was 0.995 or higher in every cohort with non-AF windows. At the validation threshold 0.393, AF recall still ranged from 45% (MIMIC-III) to 100%. A threshold set on mostly Pulsewatch validation subjects (12 of 17) did not carry over to ICU fingertip PPG.
- **Ectopy drives false AF alarms.** PAC/PVC windows gave 18.3% false alarms on Pulsewatch at 0.393, against 8.9% for NSR. This is direct support for the thesis motivation.
- **One AF subject per external cohort, and on Pulsewatch clinical.** The intervals reflect variation between windows of that subject, not between AF patients.
- **AF-only holdouts (Check E11b).** 8 of 8 subjects have AF windows and all 5,483 windows are AF. Three subjects supply 99% of the windows, so the 97% and 88% recall figures reflect three people. The group is not independent evidence (in-clinic test subjects were drawn only from subjects with AF; the AF-trial subjects are a fixed list) and gives no false-alarm estimate.
- **Not untouched.** Weight 0.5 removes the weight tuning, but v2's design was iterated while these holdouts were inspected.
- **Not zero-shot.** Training included AF windows from other subjects in these cohorts.

**Consequence for the method (defence point, no text change).** The MIMIC-III result shows that a probability scale learned on one device can shift on another while ranking holds. E4 calibrates p̂ by temperature scaling on validation subjects, but Equation 3.2 sums p̂, so a shift of this kind on the Garmin would bias the count even with good discrimination. Say so if asked, and point to RO4a and the stated Pulsewatch-to-Garmin transfer assumption.

###### E11a · Abstract (not counted in the main text)
**Current**
> In pilot work, a beat-graph representation kept AF recall between 88% and 100% across four held-out PPG cohorts without per-device threshold tuning, and in 298 Icentia11k patients a 20% deviation filter removed 60.9% of PAC coupling intervals against 8.8% of normal intervals.

**Proposed**
> In pilot work on 33 held-out subjects from four PPG cohorts, a beat-graph classifier ranked AF above other rhythms well (AUROC 0.995 or higher where non-AF windows existed), but AF recall at a threshold fixed on validation subjects ranged from 45% to 100% across devices, and in 298 Icentia11k patients a 20% deviation filter removed 60.9% of PAC coupling intervals against 8.8% of normal intervals.

###### E11b · Section 4.1, paragraph 1 [main]
**Current**
> A beat-graph ST-GNN on the same interval representation classified rhythm from wearable PPG in four held-out cohorts (Table 4.1). Splits were by subject, with no subject shared between training, validation and test. Thresholds were set once on validation subjects (5 of 17 from external cohorts) and not tuned per device; the score weighting of 0.9 was chosen from a sweep on held-out cohorts, so the test data are not fully untouched.

**Proposed**
> A beat-graph ST-GNN on the same interval representation classified rhythm from PPG in 33 held-out subjects: 16 Pulsewatch clinical, 8 Pulsewatch AF-only holdouts, 6 Simband and 3 MIMIC-III (Table 4.1). No subject was shared between training, validation and test, and external labels were re-curated. Thresholds were set once on validation subjects (5 of 17 external) and not re-tuned. AUROCs use the untuned weight of 0.5, but the design was iterated while these holdouts were inspected.

###### E11c · Section 4.1, paragraph 2 [main] (replaces T2)
**Current**
> On Pulsewatch, AF separated from PAC/PVC windows, but all 170 AF windows came from one subject and two of ten PAC/PVC subjects supplied 95% of PAC/PVC windows, so between-patient variation is not captured. External results are promising pilot evidence, not proof of cross-device performance: Simband's lower bound is 0.654, MIMIC-III has three subjects, and the 0.9 weight favours them. Recall uses the gfeat-head score, whose AUROCs are lower (0.985 AF vs rest; 0.952 AF vs PAC/PVC). The pilot did not isolate the graph's contribution (RQ2.1, RQ2.3) and labels are per-window rhythm classes, so it shows feasibility of the representation, not of counting.

**Proposed**
> Ranking transferred but operating points did not: AF vs rest AUROC was at least 0.995 wherever non-AF windows existed, yet recall at the 0.393 threshold fell to 45% on MIMIC-III. PAC/PVC windows raised false AF alarms on Pulsewatch (18.3% against 8.9% for sinus rhythm). Each cohort except the AF-only holdouts had one AF subject, so intervals reflect variation between windows, not AF patients. The graph's contribution was not isolated and labels are per-window, so the pilot shows feasibility of the representation, not of counting.

###### E11d · Table 4.1 rows [main, table rows]
**Current**
> Held-out cohort | Device | Subjects (AF subjects); windows | AF vs rest AUROC | AF vs PAC/PVC AUROC | Recall, gfeat-head score
> Clinical (Pulsewatch) | Wrist smartwatch PPG | 16 (1); 48,396 | 0.997 (0.996 to 0.998) | 0.981 (0.949 to 0.998) | 100%
> Simband | Wrist PPG, motion-affected | 9 (3); 66 | 0.951 (0.654 to 0.995) | 0.944 (0.543 to 1.000) | 88%
> MIMIC-III | ICU fingertip PPG | 3 (1); 705 | 0.998 (0.856 to 1.000) | 0.973, indicative (CI not estimable) | 99%
> Pulsewatch AF trial holdouts | Wrist smartwatch PPG | 5,483 windows | Not computed | Not computed | 97% / 100%

**Proposed**
> Held-out cohort | Device | Subjects (AF); windows | AF vs rest AUROC | AF vs PAC/PVC AUROC | AF recall, 0.393 / 0.505
> Clinical (Pulsewatch) | Wrist smartwatch PPG | 16 (1); 48,396 | 1.000 (1.000 to 1.000) | 0.998 (0.997 to 1.000) | 100% / 95%
> Pulsewatch AF-only holdouts | Wrist smartwatch PPG | 8 (8); 5,483 | Not computed | Not computed | 97% / 88%
> Simband | Wrist PPG, motion-affected | 6 (1); 46 | 0.995 (0.989 to 1.000) | 0.968, CI not estimable | 100% / 92%
> MIMIC-III | ICU fingertip PPG | 3 (1); 1,215 | 0.995 (0.993 to 0.997) | 1.000, CI not estimable | 45% / 15%

Use `W|17|17|16|17|17|16` (six columns, as now). Confirmed by Check E11b (3 November 2026, `Result_E11b_AF_Trial_Holdout_Subjects.md`): 8 of 8 subjects have AF windows and all 5,483 windows are AF. The row is labelled "Pulsewatch AF-only holdouts" because it holds 3 AF-trial (4xx) and 5 in-clinic (3xx) subjects; "AF trial" would be inaccurate, and the internal codes would mean nothing to a reader.

###### E11e · Table 4.1 caption (not counted)
> Table 4.1: Pilot results in 33 held-out subjects (evaluation mode; re-curated external labels). AUROCs use score weight 0.5, with 95% CIs from 2,000 subject resamples (skipped: clinical 701, Simband 669, MIMIC-III 676). Recall and false alarms use the gfeat-head score, which does not depend on the weight, at thresholds set on validation subjects. False alarms at 0.393 / 0.505, sinus rhythm: clinical 8.9% / 5.3%, Simband 14.3% / 9.5%, MIMIC-III 0.2% / 0.0%; PAC/PVC: clinical 18.3% / 9.8%, Simband 15.4% / 0.0%, MIMIC-III 0.0% / 0.0%. At weight 0.9, AF vs rest AUROC was 0.997, 0.995 and 0.994. The Pulsewatch AF-only holdouts are 3 AF-trial and 5 in-clinic subjects with AF windows only, so only recall can be estimated; three subjects supply 5,430 of their 5,483 windows.

**Also update outside Chapter 4**
- Table B.2, Simband and MIMIC-III row, "Status" cell: "Used in pilot work" → "Used in pilot work (re-curated labels)". Not counted (appendix).
- Remove any statement, in text, slides or speaker notes, that one threshold transfers across devices or matches a per-device optimum.

---

##### Trims to stay within 7,000 words

###### T1 · Section 3.4, paragraph 2, lag sentence [main]
**Current**
> The released alignment is not accurate to the beat, so a lag is fitted per recording session; the current lag method needs labelled segments, and a method that does not is to be developed in RO2.

**Proposed**
> A per-session lag corrects the released alignment, which is not beat-accurate; a lag method not needing labelled segments is developed in RO2.

###### T2 · Superseded
Merged into E11c, which rewrites the same paragraph with the new pilot results.

###### T3 · Section 5.1 [main]
**Current**
> The deliverables are the estimator code, split lists and a registered protocol; the contributions are the method and evidence set out in Section 2.8.

**Proposed**
> (delete)

###### T4 · Section 2.4 [main]
**Current**
> An Icentia11k autoencoder detected premature beats (sensitivity 0.87) without reporting PACs separately (Kapsecker & Jonas, 2025).

**Proposed**
> (delete; also remove the Kapsecker & Jonas, 2025 reference, which is cited only here)

###### T5 · Section 2.1, paragraph 2 [main]
**Current**
> Static recurrence models have plateaued at AUROC 0.68 to 0.80 (Montanaro et al., 2026; Ye et al., 2025) and decay with horizon (Abedi et al., 2021). In a Malaysian registry, an AUROC of 0.943 coexisted with a positive predictive value (PPV) of 40.2% (Alsalman et al., 2026).

**Proposed**
> (delete; remove the Montanaro, Ye and Abedi references, which are cited only here; Alsalman et al. stays cited in Section 3.7; define "positive predictive value (PPV)" at its next use in Section 2.6)

T5 slightly weakens the positioning against the review paper; the review is still cited in the first paragraph of Section 2.1.

###### T6 · Section 1.1, paragraph 2 [main]
**Current**
> Detecting AF moves a patient from antiplatelet therapy to anticoagulation, which reduces ischaemic stroke in device-detected AF (risk ratio 0.68) at the cost of more major bleeding (risk ratio 1.62) (McIntyre et al., 2024), with a larger absolute benefit in patients with a prior stroke or TIA (Shoamanesh et al., 2025).

**Proposed**
> Detecting AF moves a patient from antiplatelet therapy to anticoagulation, with a larger absolute benefit after stroke or TIA (McIntyre et al., 2024; Shoamanesh et al., 2025).

Keep the risk ratios (0.68; 1.62) in the speaker notes for slide 2.

###### T7 · Section 3.4, paragraph 2, detector sentence [main]
**Current**
> The primary detector is an implementation of the Elgendi et al. (2013) systolic-peak algorithm applied to all segments, with the authors' released peaks as the alternative on labelled segments; transfer from Samsung signals to the Garmin is a stated assumption.

**Proposed**
> The primary detector implements Elgendi et al. (2013) on all segments, with the authors' released peaks as the alternative; transfer from Samsung to Garmin signals is a stated assumption.

###### T8 · Section 4.2, final paragraph, opening [main]
**Current**
> Sixty-seven patients (22.5%) met the primary criterion of 480 or more PACs per day, and 66 (22.1%) met the rate-or-run definition of Binici et al. (2010) (Table 4.3). Icentia11k is a general ambulatory population, so this is not a stroke estimate;

**Proposed**
> Icentia11k is a general ambulatory population (Table 4.3), so this is not a stroke estimate;

The deleted figures remain in Table 4.3 and in Section 3.6.



###### T11 · Section 1.6 [main]
**Current**
> Key terms (beat-interval series, per-beat quality flag, coverage, valid day, ectopy rate and pulse deficit) are defined in Appendix B (Table B.1).

**Proposed**
> Appendix B (Table B.1) defines key terms.

Offsets the E2 Pulsewatch clause. The list repeats the rows of Table B.1.

---

#### 2. Slide drafts (deck not changed)

Slide numbers follow the handover order. Only text is given; keep the existing HTML styling.

| Slide | File | Current | Proposed |
|---|---|---|---|
| 5 | `rq-ro.html` | **H2** the ST-GNN beats the best non-graph baseline on daily-count error | **H2** the ST-GNN beats the best non-graph baseline on daily-equivalent count error |
| 13 | `validation-matrix.html` | RO2 metric: Daily-count MAE; Bland–Altman bias and limits | RO2 metric: MAE of the daily-equivalent count (24 × patient rate); Bland–Altman bias and limits |
| 14 | `ro1-ro2.html` | Quality flag enters as input; retention by beat class (RO1) and motion (Pulsewatch, lag-corrected); coverage gate (Equations 3.1 to 3.4, appendix) | Quality flag enters as input; retention corrects only silent loss: pulse deficit by coupling interval and motion (Pulsewatch, lag-corrected); Garmin flags abnormal beats and marks gaps; coverage gate is a reporting rule (Equations 3.1 to 3.4) |
| 14 | `ro1-ro2.html` (new bullet) | (none) | Epoch scale trained on pseudo-days on Icentia11k (segments untimed); real day order tested on Pulsewatch |
| 15 | `ro3.html` (under primary outcome) | (none) | Key secondary: pooled ESVEA count computable (≥1 h per block across the week) |
| 16 | `ro4.html` (new table row) | (none) | Interval timing noise · PPG peak vs ECG R-peak offsets measured on Pulsewatch; swept |
| 17 | `preliminary.html` (table) | Simband 9 (3); 66 · 0.951 · 0.944 · 88%; MIMIC-III 3 (1); 705 · 0.998 · 0.973 · 99%; AF trial 97% / 100% | Use the E11d table: Simband 6 (1); 46 · 0.995 · 0.968 · 100% / 92%; MIMIC-III 3 (1); 1,215 · 0.995 · 1.000 · 45% / 15%; Pulsewatch AF-only holdouts 8 (8); 5,483 · 97% / 88%; clinical 1.000 · 0.998 · 100% / 95% |
| 17 | `preliminary.html` (note) | Evaluation mode, score weight 0.9 throughout | Evaluation mode; AUROCs at score weight 0.5 (untuned); recall at validation thresholds 0.393 / 0.505 (gfeat-head score); re-curated external labels; test set 33 subjects |
| 17 | `preliminary.html` (bullets) | Thresholds set once on validation subjects (5 of 17 external), with no per-device tuning; the 0.9 score weight was chosen from a sweep on held-out cohorts, so test data are not fully untouched. External results are promising pilot evidence, not proof of cross-device performance. | Ranking transferred (AUROC ≥ 0.995 where non-AF windows existed); the operating point did not (AF recall 45% on MIMIC-III at 0.393). PAC/PVC windows raised false AF alarms (18.3% vs 8.9% sinus, Pulsewatch). One AF subject per cohort except the AF-only holdouts, whose recall reflects three people (99% of windows). Design iterated while viewing these holdouts: not untouched. |
| 17 | `preliminary.html` (speaker notes) | "All cohorts are now at the documented weight 0.9 … Simband gains most (0.891 at weight 0.5 to 0.951) … An older Simband interval of 0.81 to 0.97 …" | Replace with: legacy Simband and MIMIC-III values withdrawn (legacy labels); rerun with re-curated labels and all v2 training and validation subjects excluded; weight 0.5 reported; the threshold did not transfer to MIMIC-III; not zero-shot, because training included AF from other subjects in these cohorts. |
| 19 | `risks.html` | RO4a simulation optimistic (ECG RR, not PPG) · Calibrated operators; severity sweep; stated limitation | RO4a simulation optimistic (ECG RR, not PPG) · Four calibrated operators incl. PPG timing noise; severity sweep; stated limitation |
| App | `app-eq.html` | (3.1) π̂ₖ(m) = π̂_class(k) · π̂_motion(m) | (3.1) π̂ₖ(m, q) = π̂_pulse(k, q) · π̂_motion(m); and π̂_PAC(mᵢ, qᵢ) in (3.2) and (3.4) |
| App | `app-eq.html` (definitions line) | A(d,h): retained beats … m_i: accelerometer motion | A(d,h): beats the device reports; p̂ᵢ: calibrated PAC probability; mᵢ: motion; qᵢ: coupling interval ÷ preceding interval. Gaps go to τ, flagged beats stay as input |
| App | `app-c1.html` | Day level: MAE of the daily count; agreement with the patient-level reference | Patient level: MAE of the daily-equivalent count; calibration across burden |
| App | `app-b3.html` | Stage 1 fits the retention curve where censoring is observable; Stage 2 weights each surviving beat by 1/π(r); Stage 3 calibrates the coverage gate that decides whether … | Stage 1 fits retention for silent loss: pulse deficit by coupling interval × motion from Pulsewatch (lag-corrected); Stage 2 weights each reported beat by 1/π̂; Stage 3 applies the coverage gate, a fixed reporting rule. (Also a known handover inconsistency; the figure on this slide may need redrawing.) |

**Speaker note to add on `app-eq.html`:**
> If asked about double counting: the reliability pathway corrects only beats the watch never reports. Reported beats, flagged or not, stay in the model's input and are not reweighted. Beat probabilities are temperature-scaled on validation subjects before they are summed, because a sum of uncalibrated probabilities inflates the count.

**Speaker note to add on `ro1-ro2.html`:**
> If asked how the epoch graph learns a day from 70-minute segments: on Icentia11k it trains on pseudo-days built from each patient's own segments, so it learns aggregation under gaps, not a diurnal pattern. Real day order is tested on Pulsewatch at window level, and the day-level evidence comes from RO3.

---

#### 3. Consistency checks after applying

- [ ] Zero em dashes (U+2014) in `content.txt` and changed slides.
- [ ] Guo et al. (2017) added to References (details verified); Kapsecker & Jonas (2025) removed (and Montanaro, Ye, Abedi if T5 is used).
- [ ] Equation 3.1 fits on one line in the docx.
- [ ] Tables 3.1, 3.3, 3.4 and B.2 still consistent with Section 3.4 (handover rule); Table 3.1 RO2 "Cannot claim" unchanged.
- [ ] Figure 3.2 caption still accurate (rate head kept, per E8).
- [ ] Abstract recall range rechecked after the E11 rerun.
- [ ] Main-text word count ≤ 7,000 using the handover rule.
- [ ] Research map page (`index.html`) updated to match whatever is applied.

**Housekeeping from the review (H1 to H8)**
- [x] H1: targeted search done (`Verification_Guo_H1_H2.md`); both claims hold. Remaining: run IEEE Xplore's native search (Section 3.4 of that file).
- [x] H2: Bhurane et al. (2026) 93.96% confirmed as PAC/PVC sensitivity (IEEE Xplore abstract).
- [ ] H3: supervisor approval of the final docx.
- [ ] H4: confirm the ethics committee name (PPUM MREC or UMMC MREC).
- [ ] H5: written confirmation of Pulsewatch permitted use from the data contact.
- [ ] H6: Postgraduate Office, in writing: do tables count towards 7,000 words?
- [ ] H7: remaining handover slide inconsistencies (`problem.html`, `gaps.html`, `app-a3.html`, `refs-1.html`) besides `app-b3.html`.
- [ ] H8: mock defence using the caveats list and Section 4 answers.
- [ ] F1: one fallback slide (device or ethics not secured by S4).

---

#### 4. Prepared answers (not for the manuscript)

**"The title leads with the ST-GNN, but you say the graph is not a contribution. Why?"**
> The title names the method I build and test. The contribution I claim is the observation model around it: retention correction, coverage-aware rates and the gate. The graph is the encoder I expect to work best on beat intervals, and RQ2.1 and RQ2.3 test that expectation against non-graph baselines. If it loses, the observation model is still evaluated on the best baseline and the negative result is reported.

**"What does your thesis prove without concurrent ECG on the Garmin?"**
> Three things. First, how much ectopy is lost from waveform to filtered intervals (RO1). Second, the error of the estimator against ECG labels under calibrated, swept device losses, including PPG timing noise (RO2, RO4a). Third, whether a 7-day protocol gives enough coverage after stroke to compute the estimate (RO3). Error on the Garmin itself needs concurrent ECG, and I state that as the next study.

**"Your retention pre-check failed. Why keep the motion term?"**
> It failed only on the detector criterion. Matching was above chance at high motion and fell with motion in 8 of 8 subjects. Absolute retention depends on the detector, so I report the motion term with a detector sensitivity analysis and claim no retention value. RO3 adds a Garmin-side check of whether flagging rises with motion in the same way.

**"Four ROs and a prospective cohort is a lot. What goes first?" (review F2)**
> RO4b. It is descriptive, has no ground truth, and depends on the cohort. RO1, RO2 and RO4a use existing data and carry the methodological contribution, and the fallback in Section 3.9 already defers RO4b if the device or ethics slips.


---

# Part C. Checks, verification and results


## 20. `drafts/Check_E11_Pilot_Rerun_Weight_0.5.md`

### Check E11: rerun the cross-device pilot at score weight 0.5

**Status: DONE (3 November 2026).** AF-only holdout subjects confirmed by Check E11b (`Result_E11b_AF_Trial_Holdout_Subjects.md`). Rule locked 2026-11-03 12:40 (+08:00), before any new-data result was computed; not blind, because legacy and clinical results had already been seen. External labels were re-curated and all v2 training and validation subjects excluded; the earlier Simband and MIMIC-III values are withdrawn. Results and the drafted text are in E11 of `proposal_revisions_draft.md`. The tables below are kept as the original instructions.

**For:** Ridhwan (to run on your own machine; the pilot code, checkpoints and data are not in the handover)
**Why:** review issue #12. Table 4.1 reports the pilot at score weight 0.9, and that weight was chosen from a sweep on the held-out cohorts, so the test data informed it. Reporting the untuned weight 0.5 as primary, with 0.9 as a sensitivity result, removes that criticism.
**Draft text waiting on this:** E11 in `drafts/proposal_revisions_draft.md` (Section 4.1, Table 4.1, abstract, slide 17).
**Time needed:** about 30 to 60 minutes, mostly bootstrap run time.

---

#### 1. Lock the rule before running

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

#### 2. What you already have

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

#### 3. Steps

##### 3a. Find the script
The script that wrote `pilot_auroc_check.txt` is on your machine, next to `ckpt/log_plus_v2.txt` (the output names that log file). It already loops over weights 0.5, 0.9 and 1.0 for the Pulsewatch cohorts.

##### 3b. Extend it to the external cohorts
For each held-out cohort (**Pulsewatch clinical, Simband, MIMIC-III**) and each weight (**0.5, 0.9, 1.0**), compute:
1. AF vs rest AUROC with the 95% subject-bootstrap CI.
2. AF vs PAC/PVC AUROC with the 95% subject-bootstrap CI.
3. The number of bootstrap resamples skipped (a resample is skipped when it has no AF or no comparison subject). Clinical skipped 701 of 2,000 before, because it has one AF subject.

If a CI cannot be estimated (for example MIMIC-III AF vs PAC/PVC, 3 subjects), write "not estimable", as now.

##### 3c. Confirm which score recall uses
Print, for each cohort, the recall at threshold 0.393 and at 0.505, and state which score it was computed on (gfeat-head, w = 1.0, or the blended score). If recall changes with w, compute it at w = 0.5 too.

##### 3d. Pulsewatch AF trial holdouts
Recall only, as in Table 4.1 (5,483 windows; currently 97% / 100%). Rerun only if 3c shows recall depends on w.

---

#### 4. Fill in and send back

| Cohort | Subjects (AF); windows | AF vs rest, w = 0.5 | AF vs PAC/PVC, w = 0.5 | AF vs rest, w = 0.9 | AF vs PAC/PVC, w = 0.9 | Skipped resamples (0.5) | Recall (score used) |
|---|---|---|---|---|---|---|---|
| Pulsewatch clinical | 16 (1); 48,396 | | | 0.997 (0.996 to 0.998) | 0.981 (0.949 to 0.998) | | |
| Simband | 9 (3); 66 | | | 0.951 (0.654 to 0.995) | 0.944 (0.543 to 1.000) | | |
| MIMIC-III | 3 (1); 705 | | | 0.998 (0.856 to 1.000) | 0.973 (indicative) | | |
| Pulsewatch AF trial holdouts | 5,483 windows | not computed | not computed | not computed | not computed | | |

Also paste the raw console output, so the numbers can be traced.

---

#### 5. What happens with the result

- **Table 4.1** is rebuilt at w = 0.5. The caption changes to "score weight 0.5" (E11b).
- **Section 4.1** gets the E11a sentence. If the Simband value differs from 0.891, the sentence is updated.
- **Abstract:** check "AF recall between 88% and 100%" against step 3c.
- **Slide 17** (`preliminary.html`): the weight note and the table.
- **Research map page** (`index.html`): the pilot table.

**If w = 0.5 looks worse on Simband:** report it anyway. Simband has 9 subjects and a lower bound of 0.654 already, and the proposal calls the pilot "promising pilot evidence, not proof". An untuned, slightly lower number is easier to defend than a tuned, higher one.

#### 6. Do not claim
- That the pilot is "zero-shot": training included AF from the other cohorts.
- Anything about counting: the pilot classifies windows.
- That w = 0.9 is better: it was chosen on the test cohorts.


## 21. `drafts/Check_E2_Pulsewatch_Timestamps.md`

### Check E2: are Pulsewatch timestamps continuous across days?

**Status: DONE, PASS (3 November 2026).** Results in `Result_E2_Pulsewatch_Timestamps.md`. Note: the script below treats column 0 as UTC; the check found it is not (it sits at a fixed UTC−5), so local time was taken from the file name plus segment index × 30 s, and the order check was replaced. The instructions below are kept as originally written.

**For:** Ridhwan (to run on your local Pulsewatch files)
**Why:** review issue #2. The epoch scale of the ST-GNN aggregates "across windows within the day", but Icentia11k segments are about 70 minutes long with no clock time. The draft E2 trains the epoch scale on pseudo-days. If Pulsewatch recordings carry real, continuous timestamps across days, the proposal can also say "real within-day ordering is tested on timestamped Pulsewatch recordings at window level" (optional E2 clause, +14 words).
**Draft text waiting on this:** the optional clause under E2a in `drafts/proposal_revisions_draft.md`.
**Time needed:** about 30 minutes.

---

#### 1. What is already known

From `analyses/pulsewatch_retention/Pulsewatch_Beat_Retention_Data_Check.md`:

- `PPG_filt_csv` column 0 in the segment `.pt` files "looks like a UNIX millisecond timestamp with a 20 ms step".
- That was checked **within** segments only. Nobody has checked whether timestamps line up **across** segments and days for the same participant.
- `ECG_time_1_hr_this` is on a different scale, so the ECG clock cannot be used. Use the watch timestamps only.
- Raw watch files (`*_ppg_*.txt`, `*_accel_*.txt`) are in `synapse_data\raw_watch_8subj` for 8 subjects; it is not known whether they carry timestamps.

---

#### 2. Questions to answer

| # | Question | Why it matters |
|---|---|---|
| Q1 | Do segment timestamps convert to plausible calendar dates (the study years, not 1970)? | Confirms they are real clock times |
| Q2 | Within one participant, do segments span several days, in time order, without overlaps? | Needed for day-level ordering |
| Q3 | What is the time zone? UNIX time is UTC; the study site is in Massachusetts (US Eastern) | Time-of-day blocks are wrong by 4 to 5 hours if the zone is wrong |
| Q4 | How are recordings spread over the 24 hours, in local time? | Shows whether daytime blocks (06–12, 12–18, 18–24) have any data |
| Q5 | Is it the same for labelled, excluded and no-label segments? | Labelled segments alone may be biased towards clean, low-motion time |

---

#### 3. Script

Save as `build/check_pulsewatch_timestamps.py` (outside the data folder) and run with `python -I build/check_pulsewatch_timestamps.py <segment_pt_folder> <out_csv>`. Edit `SUBJECT_REGEX` to match your file names first.

```python
"""Check whether Pulsewatch segment timestamps are real and continuous across days."""
import re, sys, pathlib
import pandas as pd
import torch

SEG_DIR = pathlib.Path(sys.argv[1])        # e.g. synapse_data/untar/PPG_Elgendi_30sec_HR_ACC_pt
OUT_CSV = pathlib.Path(sys.argv[2])
SUBJECT_REGEX = r"^(\d{3})"               # EDIT: how the subject ID appears in the file name
TZ = "America/New_York"                    # study site time zone (check Q3)

rows = []
for f in sorted(SEG_DIR.rglob("*.pt")):
    m = re.search(SUBJECT_REGEX, f.name)
    if not m:
        continue
    try:
        d = torch.load(f, map_location="cpu", weights_only=False)
        t = d["PPG_filt_csv"][:, 0]
        t = t.numpy() if hasattr(t, "numpy") else t
    except Exception as e:
        rows.append({"file": f.name, "subject": m.group(1), "error": str(e)})
        continue
    rows.append({"file": f.name, "subject": m.group(1),
                 "t_start_ms": float(t[0]), "t_end_ms": float(t[-1]),
                 "n": len(t), "step_ms": float(pd.Series(t).diff().median())})

df = pd.DataFrame(rows)
df.to_csv(OUT_CSV, index=False)
ok = df.dropna(subset=["t_start_ms"]).copy()
ok["start_utc"] = pd.to_datetime(ok["t_start_ms"], unit="ms", utc=True)
ok["start_local"] = ok["start_utc"].dt.tz_convert(TZ)

print("Files read:", len(df), " errors:", df.get("error", pd.Series()).notna().sum())
print("Q1 date range (UTC):", ok["start_utc"].min(), "to", ok["start_utc"].max())

g = ok.sort_values("t_start_ms").groupby("subject")
summary = g.agg(segments=("file", "size"),
                first=("start_local", "min"), last=("start_local", "max"),
                days=("start_local", lambda s: s.dt.date.nunique()))
ok["gap_s"] = g["t_start_ms"].diff() / 1000
ok["prev_end"] = g["t_end_ms"].shift()
summary["overlaps"] = (ok["t_start_ms"] < ok["prev_end"]).groupby(ok["subject"]).sum()
summary["median_gap_s"] = ok.groupby("subject")["gap_s"].median()
print("\nQ2 per subject:\n", summary.to_string())

ok["block"] = pd.cut(ok["start_local"].dt.hour, [0, 6, 12, 18, 24], right=False,
                     labels=["00-06", "06-12", "12-18", "18-24"])
print("\nQ4 share of segments by local block:\n",
      ok["block"].value_counts(normalize=True).sort_index().round(3).to_string())
print("\nQ4 by subject:\n",
      pd.crosstab(ok["subject"], ok["block"], normalize="index").round(2).to_string())
```

**Q5:** join the output CSV with `03_Labels` (`table_file_name`, `final_AF_GT_20230921`) and repeat the Q4 table for labelled (codes 0, 1, 2), excluded (negative codes) and no-label segments. If excluded segments have no `.pt` files, use the raw `*_ppg_*.txt` files for those, if they contain a time column (check one file by eye first).

**Q3 (time zone):** look for a night-time dip in Q4. Watch wear and clean PPG should be highest at night in local time. If the busiest block is 04–10 UTC, the timestamps are UTC and the Eastern conversion is right. Also check the Pulsewatch Synapse wiki for a time-zone statement.

---

#### 4. Decision rule

| Result | Decision |
|---|---|
| Q1 plausible dates **and** Q2 at least 5 subjects span 3 or more days, in order, with no overlaps **and** Q3 time zone settled | **Pass.** Add the optional E2 clause (+14 words; take them from the E8 removal alternative or another trim). |
| Dates plausible but only within single sessions, or time zone unclear | **Fail for E2.** Keep E2 as drafted (pseudo-days only). |
| Dates implausible (1970, or not in the study years) | **Fail.** Note it in the data check file; do not use Pulsewatch time of day anywhere. |

---

#### 5. Fill in and send back

| Item | Result |
|---|---|
| Files read / errors | |
| Date range (UTC) | |
| Subjects spanning ≥ 3 days, in order, no overlaps | __ of __ |
| Median gap between segments | |
| Time zone (and how determined) | |
| Share of segments by block 00–06 / 06–12 / 12–18 / 18–24 (all) | |
| Same, labelled vs excluded vs no-label | |
| Decision (pass / fail) | |

#### 6. Side benefit

If this passes, the Q4 table is real smartwatch coverage by time of day. That supports the RO3 fallback ("coverage modelled from Pulsewatch wear data", Section 3.9) and could check the night-weighted coverage assumption (Merschel & Reinhardt, 2022) used in Appendix C and RO4a.

#### 7. Do not claim
- That Pulsewatch reflects Garmin coverage: it is a Samsung watch in a different population.
- Any time-of-day ectopy pattern from Pulsewatch: labels are 30-second windows with PAC and PVC merged.


## 22. `drafts/Verification_Guo_H1_H2.md`

### Verification results: Guo et al. (2017), "first" claims (H1), Bhurane 93.96% (H2)

**Run:** 3 November 2026, using Firecrawl (web search, page scrape, research paper index covering PubMed, bioRxiv, medRxiv and arXiv) and Consensus.
**Feeds:** `drafts/proposal_revisions_draft.md` (E4d reference; issue map rows H1 and H2).

---

#### 1. Guo et al. (2017): verified

Source: the PMLR proceedings page, https://proceedings.mlr.press/v70/guo17a.html

| Field | PMLR record | Draft E4d |
|---|---|---|
| Authors | Chuan Guo, Geoff Pleiss, Yu Sun, Kilian Q. Weinberger | Same |
| Proceedings | Proceedings of the 34th International Conference on Machine Learning | Same |
| Editors | Doina Precup, Yee Whye Teh | Same |
| Series and volume | Proceedings of Machine Learning Research, Vol. 70 | Same |
| Pages | **1321–1330** | Same |
| Year | 2017 | Same |

**Status:** the E4d reference is correct as drafted. Optionally add the URL at the end:

```
REF|Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. In D. Precup & Y. W. Teh (Eds.), *Proceedings of the 34th International Conference on Machine Learning* (Vol. 70, pp. 1321–1330). PMLR. https://proceedings.mlr.press/v70/guo17a.html
```

The paper also supports the E4 wording: temperature scaling is "a single-parameter variant of Platt Scaling" and "surprisingly effective at calibrating predictions".

---

#### 2. Bhurane et al. (2026), 93.96%: confirmed

Source: the IEEE Xplore abstract, https://ieeexplore.ieee.org/document/11517622 (DOI 10.1109/CSPA68262.2026.11517622). The full text was not accessed.

What the abstract says:
- **Data:** the NIH-funded Pulsewatch dataset, "106 subjects recorded in real-life settings for 14 days"; raw single-channel PPG only.
- **Model:** "Tiny-ResNet" with 23,727 trainable parameters.
- **Results on the test set:** overall accuracy **98.00%**. For the PAC/PVC class: **sensitivity 93.96%**, specificity 98.80%, F1 92%. For AF: sensitivity 99.20%, specificity 99.00%.
- **Split:** the abstract does not say whether testing was subject-independent.

**Consequences:**
- Table 2.1 "PAC/PVC sensitivity 83% to 94% (Han et al., 2026; Bhurane et al., 2026)" is correct. The 94% is Bhurane's 93.96%, rounded.
- Table 2.2 "accuracy 98.0%" is correct.
- Keep the existing caveat in the `gaps.html` speaker notes: the split is not reported, so 93.96% is not directly comparable with Han et al.'s 83% on 72 held-out subjects.
- Table 2.2 says "full text not accessed". That is still true; the confirmation comes from the abstract.
- The abstract's "recorded … for 14 days" supports the Pulsewatch multi-day premise behind the optional E2 clause. Timestamp continuity still needs `Check_E2_Pulsewatch_Timestamps.md`.

---

#### 3. "First" claims (H1)

The proposal makes two novelty claims (Section 2.7, abstract and Section 5.1):

- **Claim A:** no smartwatch or PPG-derived daily PAC count validated against ECG.
- **Claim B:** "in these databases, no graph neural network applied to PPG or inter-beat-interval series for arrhythmia".

##### What was searched

| Source | Queries (summary) |
|---|---|
| arXiv | Firecrawl web search restricted to `site:arxiv.org`: GNN with PPG, inter-beat interval or RR interval and atrial fibrillation; the Firecrawl research index (includes arXiv) with three framings |
| IEEE Xplore | Firecrawl web search restricted to `site:ieeexplore.ieee.org`: GNN, photoplethysmography and arrhythmia; plus the Bhurane record |
| PubMed, bioRxiv, medRxiv | Firecrawl research index: GNN on PPG or IBI for arrhythmia; graph or visibility-graph methods on pulse-interval series; PPG or smartwatch PAC burden against Holter |
| Consensus | GNN with PPG or RR intervals for AF or premature beats; smartwatch PPG PAC burden against Holter |

**Limit:** IEEE Xplore was searched through a web index restricted to its domain, not through IEEE Xplore's own search engine. Before the proposal names IEEE Xplore as a searched database, run the native search yourself (Section 3.4).

##### Claim A, daily PAC count: holds

No study was found that reports a smartwatch- or PPG-derived **PAC** count or burden validated against ECG. Every count-level validation found is for **AF burden**:
- Poh et al. (2023), Verily watch against a 14-day Zio patch: R² = 0.986.
- Zhao et al. (2024): R² = 0.996.
- Zuo et al. (2026), 728 patients: r = 0.999. This study is already cited.
- Pan et al. (2025), Amazfit against a 7-day Holter: ICC 0.976.
- Anagnostopoulos et al. (2025): a meta-analysis of six AF-burden studies.

The nearest PAC work:
- **Kwon et al. (2019)** used a "PAC indicator" to estimate the share of PPG samples containing PACs (29.79% of post-cardioversion samples). That is a sample-level flag, not a validated count against ECG.
- **Han et al. (2020, 2026)** and **Bhurane et al. (2026)** classify windows only.

**Useful for the defence:** count-level validation is established for AF burden but not for PAC burden. That makes the gap concrete. Optionally, one AF-burden study could be cited in Section 2.4 as the analogue, but that costs words.

**Garmin-specific find:** Chang et al. (2022, *American Heart Journal*) ran 24-hour simultaneous Garmin smartwatch PPG with Holter ECG in 200 participants for AF detection. It is a Garmin precedent for continuous ambulatory recording. Consider it for Section 3.5 or the device answers.

##### Claim B, GNN on PPG or IBI for arrhythmia: holds, keep it scoped

No study was found that applies a GNN to **PPG or inter-beat-interval series for arrhythmia**. Graph methods nearby, which an examiner might raise:

| Work | What it does | Why it does not break Claim B |
|---|---|---|
| ECG-GraphNet (2025, *Heart Rhythm O2*); visibility-graph GCN (arXiv 2404.15367); CNN-GNN-BiLSTM (2025, *Med Eng Phys*, "inter-beat relationships"); several others | GNNs on **ECG** beats or leads, N/S/V classification | ECG, not PPG or IBI. The visibility-graph GCN notes the S (supraventricular) class stays hard inter-patient, which supports the proposal's motivation |
| CiGNN (IEEE) | GNN on wearable PPG for **blood pressure** | PPG, but not arrhythmia. This is why the claim must keep "for arrhythmia" |
| Rivera-Juzga et al. (2025, *Comput Biol Med*; Lip co-author) | GNN predicting **new AF after stroke** from clinical data | Not signals. But it is the closest GNN work in the same clinical space |
| Visibility-graph analysis of RR series (e.g., Entropy 2023) | Graph features of heartbeat series, no GNN | Feature engineering, not a GNN |
| MGNN (2022) | Despite the name, a multiscale grouped **CNN** on RR intervals | Not a graph network |

**Recommendations:**
1. Keep Claim B worded as "for arrhythmia" and "to our knowledge".
2. **Prepare for Rivera-Juzga et al. (2025).** If asked "hasn't a GNN already been used for AF after stroke?", answer: "Yes, on clinical variables to predict AF. This study applies a graph network to beat intervals from a wearable to estimate ectopy, a different input and a different target." Cite it only if the word budget allows.
3. The visibility-graph GCN paper reports S-class difficulty, which supports the existing EPMoghaddam et al. (2024) point that graphs are tested, not assumed.

##### 3.4 Run IEEE Xplore's own search (10 minutes) before naming it

Use https://ieeexplore.ieee.org/search/advanced with these queries, all years:
1. `("graph neural network" OR "graph convolutional" OR "graph attention") AND (photoplethysmograph* OR PPG OR "inter-beat interval" OR "pulse interval") AND (arrhythmia OR "atrial fibrillation" OR premature OR ectopic)`
2. `(smartwatch OR wearable OR photoplethysmograph*) AND ("premature atrial" OR "atrial ectopy" OR "supraventricular ectopic") AND (burden OR count OR "per day" OR "24-hour")`

Record the date and the number of hits screened. If nothing breaks either claim, the Section 2.7 sentence can name IEEE Xplore and arXiv (see 3.5).

##### 3.5 Optional wording for Section 2.7 (+5 words)

**Current**
> Searches of PubMed, Consensus and Wiley Scholar Gateway in October 2026 found no smartwatch or PPG-derived daily PAC count validated against ECG, and, in these databases, no graph neural network applied to PPG or inter-beat-interval series for arrhythmia (Table 2.1).

**Proposed** (only after step 3.4)
> Searches of PubMed, Consensus, Wiley Scholar Gateway, IEEE Xplore and arXiv in October and November 2026 found no smartwatch or PPG-derived daily PAC count validated against ECG, and, in these databases, no graph neural network applied to PPG or inter-beat-interval series for arrhythmia (Table 2.1).

Word budget: the main draft is at about 6,983 (after E11, E11b and E2), so +5 gives about 6,988, still under 7,000.

---

#### Sources

- Guo et al. (2017), PMLR: https://proceedings.mlr.press/v70/guo17a.html
- Bhurane et al. (2026), IEEE Xplore: https://ieeexplore.ieee.org/document/11517622
- Poh et al. (2023), JAHA: https://doi.org/10.1161/jaha.123.030543
- Zhao et al. (2024), PACE: https://doi.org/10.1111/pace.14951
- Zuo et al. (2026), JACC Clin EP: https://doi.org/10.1016/j.jacep.2026.03.036
- Pan et al. (2025), Digital Health: https://doi.org/10.1177/20552076251314105
- Anagnostopoulos et al. (2025), JCDD: https://doi.org/10.3390/jcdd12040122
- Kwon et al. (2019), JMIR mHealth uHealth: https://doi.org/10.2196/12770
- Chang et al. (2022), Am Heart J: https://doi.org/10.1016/j.ahj.2022.02.002
- ECG-GraphNet (2025), Heart Rhythm O2: https://doi.org/10.1016/j.hroo.2025.05.012
- Visibility-graph GCN (2024), arXiv: https://arxiv.org/abs/2404.15367
- CNN-GNN-BiLSTM (2025), Med Eng Phys: https://doi.org/10.1016/j.medengphy.2025.104418
- Rivera-Juzga et al. (2025), Comput Biol Med: https://doi.org/10.1016/j.compbiomed.2025.111095
- CiGNN, IEEE: https://ieeexplore.ieee.org/iel7/6221020/10521573/10472032.pdf


## 23. `drafts/Result_E2_Pulsewatch_Timestamps.md`

### Check E2: Pulsewatch timestamps across days

**Purpose:** decide whether the proposal can add the optional E2 clause saying real within-day ordering is tested on timestamped Pulsewatch recordings. The request is in `Check_E2_Pulsewatch_Timestamps.md`.

**Decision (3 November 2026): pass.** The optional clause can be added, but it should not call the timestamps UTC. Use file-name time as local time, not the conversion in the request's script.

**Timing of the rule:** the definitions below were written after a read-only sample of 11,735 files had been seen, and before the full run. They are not fully blind.

#### Results to send back

| Item | Result |
|---|---|
| Files read / errors | 167,205 / 0 |
| Date range | 2019 to 2021 (years only) |
| Subjects spanning ≥ 3 days, in order, no overlaps | **64 of 108** (68 span ≥ 3 days) |
| Median gap between segments | 30.0 s; about 10 minutes between session starts (median across subjects) |
| Time zone | US Eastern local time in the file names, shown by the daylight-saving pattern and the hourly profile. No written statement found |
| Blocks 00–06 / 06–12 / 12–18 / 18–24, all `.pt` | Pooled 43.2 / 15.9 / 15.5 / 25.3%; mean of subjects 28.9 / 20.2 / 30.6 / 20.3% |
| Labelled, all subjects (pooled) | 43.3 / 15.8 / 15.5 / 25.4% |
| Excluded, all subjects (pooled) | 16.8 / 22.3 / 33.7 / 27.3% |
| No-label, 8 subjects (pooled) | 20.4 / 24.3 / 29.2 / 26.0% |
| Decision | **Pass** |

#### Pass rule

The request's rule stands. These definitions make it computable.

| Item | Definition | Result | Met? |
|---|---|---|---|
| Q1 | At least 99% of readable files in the published study years, 2019–2021 | 100% | Yes |
| Q2 | At least 5 subjects span 3 or more local days, with zero order violations and zero overlaps above 2 s | 64 subjects | Yes |
| Q3 | At least 95% of segments match the US Eastern calendar offset within 5 s; US beats UK in weeks where the calendars differ; the name-clock profile peaks at night | 99.1%; 97.2% vs 2.6% on 6,710 segments; busiest hour 01:00 | Yes |

#### Why the request's time conversion was not used

The request treats column 0 of `PPG_filt_csv` as UTC and converts it to `America/New_York`. The data does not support that:

- **Offset:** epoch minus file-name time, after removing segment index × 30 s, is 0 h in winter and −1 h in summer. True UTC against Eastern local time would be +5 h and +4 h.
- **Night test:** the request expects the busiest period at 04–10 UTC if the column is UTC. On the epoch column, 04–10 is among the quieter periods and the peak is 23:00–03:00.
- **Effect of converting:** the 00–06 share falls from 43.2% to 19.1%, and the 18–24 share rises from 25.3% to 45.2%. Night-time recording would look like evening recording.

The most likely reading is that the file name holds Eastern local time and the epoch sits at a fixed UTC−5 all year. How the release built that column is not documented, so this is an inference.

##### Supporting evidence

- **In-clinic cohort:** all 188 `3xx` segments fall in 06–18 on the name clock (33.5% and 66.5%), as expected for in-clinic recording.
- **`statics` files, 8 subjects (added after the first full run, not part of the rule):**
  - These files have their own epoch in the name. Shifted by −5 h in winter or −4 h in summer, they almost never fall inside a session (0.0% and 0.1%).
  - Neighbouring shifts give 81–91% on the side towards later times. That edge sits at the Eastern UTC offset, which fits `statics` being true UTC and written between sessions.
  - My first explanation, that they are written just before a session starts, was wrong: none fall within 60 s of a session start at those shifts.
  - This is indirect evidence, and the season split itself uses the US calendar.

#### Other findings

- **Labelled time is not wear time:** 43.3% of labelled segments fall in 00–06, against 16.8% of excluded ones. Labelled data favours quiet night hours.
- **Pooled shares favour heavy subjects:** the 00–06 share is 43.2% pooled and 28.9% as a mean of subjects.
- **Within-day ordering:** the median subject has labelled data in at least 2 blocks on 74% of their days, and spans 5 days. This is descriptive and not part of the rule.
- **Raw recordings, 8 subjects:** pooled 22.9 / 22.3 / 28.6 / 26.3%; mean of subjects 18.2 / 21.6 / 40.0 / 20.1%. This is the closest available measure of recording time, from subjects who were not randomly chosen.

#### Limits

1. **Clock exceptions:** 1,540 segments (0.9%), from 36 subjects and 302 sessions, do not match the US calendar. One subject accounts for 37% of them. 353 January segments sit at +1 h, unexplained.
2. **Order and overlap:** 4 of the 68 subjects spanning 3 days fail the strict rule. There are 10 across-session order violations and 168 overlaps above 2 s (391 strict). There are no within-session order violations.
3. **Subjects below 3 days:** 40 of 108 subjects do not span 3 days in labelled `.pt` data, including the brief in-clinic `3xx` recordings.
4. **Excluded coverage:** excluded segments come from 68 clinical subjects and 1 `4xx` subject (11 segments), so the labelled vs excluded contrast describes clinical subjects. No-label data covers 6 of the 8 raw-tar subjects.
5. **Study years:** the 2019–2021 source is the randomised trial, enrolling September 2019 to August 2021. All clinical and `3xx` files fall within that enrolment period plus 44 days of follow-up, but only 38.0% of `4xx` files do. The `4xx` files stay within 2019–2021, and no separate published dates for that cohort were checked.
6. **Travel:** a participant who travelled outside Eastern time cannot be detected.

#### Counts reconcile

- 403,022 label rows give 394,019 unique names: 166,279 labelled, 224,444 excluded, 392 code 3 and 2,904 kept-label conflicts or missing `.pt` (537 + 2,367).
- The labelled count matches the project's 166,279 de-duplicated set.
- In the 8 raw-tar subjects, no-label is 74,192, plus 53 files with long-index names not counted, which gives the earlier test's 74,245.
- Excluded is 12,533 here against 12,532 in the earlier test. Group totals exceed the raw file count by one, which suggests one excluded name has no raw file. This was not traced to a specific file.

#### Do not claim

- That the timestamps are UTC.
- That labelled shares show wear or coverage. Use the 8-subject raw table, with its limits, for the RO3 fallback or any check of night-weighted coverage.
- That Pulsewatch reflects Garmin coverage. It is a Samsung watch in a different population.
- Any time-of-day ectopy pattern. Labels are 30-second windows with PAC and PVC merged.

#### Files

- Script: `build/check_pulsewatch_timestamps.py`
- Aggregates: `build/pulsewatch_timestamps_summary.json`
- Exact times, local only and not to be shared: `build/pulsewatch_timestamps_segments.csv`, `build/pulsewatch_timestamps_segments_smoke.csv`

#### Sources for study dates

- Dickson et al., *Cardiovasc Digit Health J* 2021, PMID 35265913 (protocol, 14- and 44-day follow-up)
- Ding et al., *JMIR Cardio* 2023;7:e45137 (enrolment dates, UMass Memorial, Massachusetts)
- The Pulsewatch Synapse wiki gives no time-zone statement.


## 24. `drafts/Check_E11b_AF_Trial_Holdout_Subjects.md`

### Check E11b: are all 8 AF-trial holdout subjects AF subjects?

**For:** Ridhwan (to run on your own machine, with the 3 November rerun code)
**Why:** the E11 draft writes the Table 4.1 row for the Pulsewatch AF-trial holdouts as "8; 5,483, all AF". If confirmed, it becomes "8 (8); 5,483", the same format as the other cohorts (for example "16 (1); 48,396").
**Draft text waiting on this:** E11d (Table 4.1 rows) in `drafts/proposal_revisions_draft.md`; the pilot table on the research map page (`index.html`); slide 17.
**Time needed:** about 10 minutes.

---

#### 1. What "AF subject" means here

In Table 4.1, the number in brackets counts **subjects with at least one AF-labelled window in the evaluated test set**. It is not a clinical AF diagnosis. Use the same definition here, so the AF-trial row is counted like the other rows.

---

#### 2. What the earlier output already shows

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

#### 3. Steps

##### 3a. Use the rerun's test set
Open the script that produced the 3 November results (same v2 checkpoint, re-curated external labels, all v2 training and validation subjects excluded). Run the check **after** the test windows are loaded and filtered, so it sees exactly the windows that were scored.

##### 3b. Add this snippet
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

##### 3c. Check the cohort codes
Before reading the result, confirm which cohort codes make up the "AF trial holdouts" in the rerun (the earlier pooled block combined `4xx` and `3xx`). If the rerun's AF-trial group uses different codes, use those.

---

#### 4. Pass rule

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

#### 5. Optional: clinical diagnosis

Table 4.1 does not need it. If you want to say these are patients with diagnosed AF, check the Pulsewatch trial documentation (Dickson et al., 2021, protocol; Ding et al., 2023) for whether the `3xx` and `4xx` groups enrolled people with known AF. Do not write "diagnosed AF" in the proposal without that source.

---

#### 6. How to send the result back

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

#### 7. What changes after a pass
- E11d in `proposal_revisions_draft.md`: "8; 5,483, all AF" → "8 (8); 5,483" (same word count).
- `index.html` pilot table: "8; 5,483 (all AF)" → "8 (8); 5,483".
- Slide 17 draft row: same change.


## 25. `drafts/Result_E11b_AF_Trial_Holdout_Subjects.md`

### Check E11b result: AF-trial holdout subjects

**Run:** 2026-11-03 13:29 (+08:00)
**Script and data:** `build/check_e11b_af_trial_subjects.py`; 3 November rerun test set (v2 checkpoint, re-curated external labels)
**Rule:** Section 4 of the check file, unchanged. Seen before the run: window, subject and label totals (2 and 3 November). Per-subject counts had not been computed.

#### 1. Results
| Item | Expected | Result | Met? |
|---|---|---|---|
| Cohort codes used | 4xx, 3xx (confirm) | 3xx, 4xx | Yes |
| Windows | 5,483 | 5483 | Yes |
| Subjects | 8 | 8 | Yes |
| Subjects with ≥ 1 AF window | 8 | 8 | Yes |
| Labels present | AF only | AF only | Yes |
| Any subject with zero AF windows | No | No (0 subjects) | Yes |

#### 2. Windows by label
| Label | Windows |
|---|---:|
| AF | 5483 |
| NSR | 0 |
| PAC/PVC | 0 |
| Other or noise | 0 |
| **Total** | 5483 |

#### 3. Per-subject counts (no subject IDs)
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

#### 4. Console output (summary)
Asserts passed: labels match the scored windows; holdouts identical under legacy and new external labels; 0 overlap with v2 training or validation subjects. Raw label audit: 5,483 distinct segments, 0 dropped for missing or conflicting labels, 0 unanimous labels absent from the evaluated set. DECISION: PASS. Full printout in the candidate's message of 3 November 2026.

#### 5. Decision
Pass. All four items met.

#### 6. Deviations from the instructions
- The pandas snippet was replaced with equivalent logic (the code has no `test_df`; labels are integers 0 NSR, 1 AF, 2 PAC/PVC).
- Added a split by cohort code, cohort codes beside S1 to S8, and a count of segments dropped from the raw label files.
- Added asserts on label match, holdout identity under both external sources, and no overlap with v2 training or validation.

#### 7. Optional: clinical diagnosis source
none

#### Limits (from the candidate)
- Not independent evidence: 3xx test subjects are drawn only from subjects with AF, and the 4xx subjects are a fixed list.
- Recall only: with no non-AF windows, this row gives no false-alarm estimate.
- Concentration: S1 to S3 supply 5,430 of 5,483 windows (99%), so the 97% and 88% recall figures reflect three people.
- Row label: 3 subjects are AF trial (4xx) and 5 are in-clinic (3xx), so "AF trial" is inaccurate. Table 4.1 uses "Pulsewatch AF-only holdouts".


---

# Part D. Applied to the deliverables


## 26. `proposal/SUPERVISOR_RECONFIRMATION_E1_E11.md`

### Items needing supervisor reconfirmation: E1 and E11

**Status:** applied to `proposal/source/content.txt`, `proposal/Ridhwan_Research_Proposal_UM.docx` and the slide deck on 3 November 2026, with the candidate's approval. **Both items still need confirmation from Dr. Bryan Raj and Assoc. Prof. Dr. Ismail Ahmedy.** If either is not confirmed, revert using the "Current" text in `drafts/proposal_revisions_draft.md` (sections E1 and E11) and rebuild.

The handover version of the docx is kept as `proposal/Ridhwan_Research_Proposal_UM_handover_2026-11-03.docx` for comparison.

---

#### E1: retention corrects only silent device loss

**Why confirmation is needed:** it reverses logged decision 6g (`decisions/proposal-decisions-2026-11-02.md`), which set Equation 3.1 as class retention from RO1 multiplied by motion retention from Pulsewatch.

**What changed**
- **Equation 3.1** is now π̂ₖ(m, q) = π̂_pulse(k, q) · π̂_motion(m). Pulse retention depends on the coupling ratio q (Zheng et al., 2008); motion retention still comes from Pulsewatch.
- **Equations 3.2 and 3.4** use π̂_PAC(mᵢ, qᵢ).
- **Section 3.4** says gaps enter the observed time, flagged beats stay in the input unweighted, and the reliability pathway corrects only silent loss.
- **Section 4.2:** RO1's filter results now support keeping flagged beats as input (RQ2.4), instead of "learning retention as a function of context".
- **Appendix C** notes that its 0.391 beat retention is pessimistic for a device that flags rather than deletes.

**Evidence:** the Garmin Enhanced BBI whitepaper (Garmin, 2023; already cited). It says abnormally short or long beats are kept and marked low confidence, and that extreme motion or poor signal produces a marked gap.

**Points for supervisors to weigh**
1. RO1's role changes. Its filter results justify flag-as-input rather than supplying a term in Equation 3.1. RO1 is paper 1 (milestone M3).
2. The pulse-deficit term uses the same published threshold as the RO4a pulse-deficit degradation. The safeguard is reporting RO4a across the operator's full severity sweep.
3. The evidence is a vendor document (one subject, one night, Venu 2 Plus, 2023). Device verification must confirm flag and gap behaviour on the study device.
4. Enhanced BBI recording 24/7 was confirmed by Garmin to the candidate. The public whitepaper says sleep only, so keep Garmin's confirmation in writing.

---

#### E11: pilot results rewritten (Section 4.1, Table 4.1, abstract)

**Why confirmation is needed:** it changes a headline number the supervisors have seen, and withdraws earlier values.

**What changed**
- **Withdrawn:** the Simband and MIMIC-III values 0.891, 0.951, 0.944, 0.998 and 0.973, which used legacy external labels.
- **New results:** re-curated external labels, all v2 training and validation subjects excluded, same checkpoint, evaluation mode. AUROCs at the untuned score weight 0.5; recall at the validation thresholds (gfeat-head score), not re-tuned.
- **Test set:** 33 subjects (16 Pulsewatch clinical, 8 Pulsewatch AF-only holdouts, 6 Simband, 3 MIMIC-III).
- **Abstract:** "AF recall between 88% and 100% … without per-device threshold tuning" becomes "ranked AF above other rhythms well (AUROC 0.995 or higher where non-AF windows existed), but AF recall at a threshold fixed on validation subjects ranged from 45% to 100% across devices".
- **Section 4.1 now states:**
  - ranking transferred but operating points did not (MIMIC-III recall 45%)
  - PAC/PVC windows raised false AF alarms (18.3% vs 8.9% sinus rhythm)
  - one AF subject per cohort except the AF-only holdouts
  - the design was iterated while the holdouts were inspected, so they are not untouched
- **Table 4.1:** the row "Pulsewatch AF-only holdouts" holds 3 AF-trial and 5 in-clinic subjects, 8 (8); 5,483, confirmed by Check E11b.

**Points for supervisors to weigh**
1. The rule was locked at 2026-11-03 12:40 (+08:00), before new-data results, but not blind: legacy and clinical results had been seen.
2. MIMIC-III shows that a probability scale can shift across devices while ranking holds. Equation 3.2 sums probabilities, so the same shift on the Garmin would bias the count. This is a prepared defence answer, not proposal text.
3. In the AF-only holdouts, three subjects supply 99% of windows, so the 97% and 88% recall figures reflect three people.

---

#### Other applied revisions (for information only)

E2 (pseudo-days and Pulsewatch ordering), E3 (daily-equivalent count), E4 (no double counting; calibrated p̂; Guo et al., 2017 added), E5 (interval timing-noise operator), E6 (Garmin flag vs motion check), E7 (coverage gate as reporting rule), E8 (rate head as auxiliary target), E9 (pooled computability as key secondary), E10 (Table B.3, disjoint patient sets), and the trims T1, T3 to T8 and T11. Full before-and-after text is in `drafts/proposal_revisions_draft.md`.

**Build checks (3 November 2026):**
- main text 6,983 words (limit 7,000)
- zero em dashes
- every reference cited and every citation referenced
- Equation 3.1 on one line
- 45 pages (LibreOffice render; Word not yet checked)


## 27. `slides/README.md`

### Slide sources (changed slides only)

Copies of the 10 slides changed on 3 November 2026 in the Claude Slides deck https://claude.ai/artifact/4RuYVim5WsRqG5aQLYJGas (version 44; `app-b3` redrawn in version 46; `app-eq` page number corrected from 30 to 31 in version 48; six sources not in the proposal removed in version 49), plus the unchanged `deck.json` index. The deck itself is the source of truth; these copies are for version history.

Changed: `rq-ro` (5), `validation-matrix` (13), `ro1-ro2` (14), `ro3` (15), `ro4` (16), `preliminary` (17), `risks` (19), `app-eq`, `app-c1`, `app-b3`.

Speaker notes on `ro1-ro2`, `app-eq` and `app-b3` (E1) and `preliminary` (E11) carry a "Pending supervisor reconfirmation" line. Remove it once supervisors confirm (see `proposal/SUPERVISOR_RECONFIRMATION_E1_E11.md`).

`app-b3`: the two old images (which illustrated the superseded three-stage retention approach) were replaced in version 46 by native slide content: three stage cards, a "where each loss goes" table, and two schematic retention curves labelled "shapes only; no fitted values".

Version 49: removed six sources that are not in the proposal's reference list, both the reference entries and the appendix rows citing them: Aguilar et al. (2021) from `app-a5` and `refs-1`; Bacevičius et al. (2022) from `app-a3` and `refs-1`; Väliaho et al. (2019) and Gruwez et al. (2024) from `app-a6`, `refs-6` and `refs-2`; Zahid et al. (2023) from `app-a7` and `refs-6`; Sun et al. (2024) from `app-a8` and `refs-5`. The four references removed from the proposal this session (Kapsecker, Montanaro, Ye, Abedi) were never on the slides.
