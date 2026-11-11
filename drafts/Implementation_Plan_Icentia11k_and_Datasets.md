# Implementation plan for the next phase: from the proof of concept to the first participant

Prepared 4 November 2026; extended 11 November 2026 with the readiness track for real-patient data acquisition (sections 10 to 12). The step-by-step Track 1 runbook to the end of S3, with the initial code in `analysis/`, is `drafts/Track1_Implementation_Runbook_S2_S3.md`. Source of truth: the proposal docx (`proposal/Ridhwan_Research_Proposal_UM.docx`). Where the proposal leaves a choice open, this plan marks it **Decision** and proposes a default; nothing here changes the proposal.

---

## 1. Where we are

The preliminary analysis (§4.2) was a proof of concept on 300 Icentia11k patients drawn with a fixed seed (298 analysed, median 57.5 h each). It used **beat annotations only**, computed RR intervals, ran one filter (percent-deviation, reference = median of the 5 preceding accepted intervals, 10% to 30%), and tallied removals by beat class and ESVEA status. It answered one narrow question: is the filtering loss large and burden-dependent? Yes (60.9% of PAC coupling intervals vs 8.8% of normal intervals removed at 20%; 78.5% vs 60.0% by ESVEA status).

That patient set is now **P0** (Table B.3) and is never reused for testing.

What is not yet built: the hypothesis test H1 in new patients, the full RO1 decomposition, the RO2 estimator, the flag and loss simulator, and the RO4a substitution test. Nor is anything yet in place for the cohort: the device has not been received, and no device verification, ethics submission, data pipeline for the Garmin or site arrangement exists.

The next phase therefore runs as **two tracks in parallel**, ending at the go/no-go gate in S4 when the first PPUM participant can be fitted with a watch:

| Track | Covers | Sections | Ends with |
|---|---|---|---|
| **1. Modelling (retrospective)** | Icentia11k and Pulsewatch: data pipeline, RO1 and H1, training simulator, RO2 build | 3 to 8 | M3 (RO1 paper, S3); M4 (model frozen, S4) |
| **2. Readiness for acquisition (prospective)** | Device, verification, Garmin data pipeline, protocol and ethics, PPUM site | 10 | M1 and M2 (S3); go/no-go gate (S4) |

The two tracks meet at three points (section 11): shared coverage and valid-day code, a dry run of the full estimator on real Garmin output, and the motion scale used by π̂(m). RO4a (section 9) follows M4 and is not part of the phase before acquisition.

---

## 2. Facts about Icentia11k that shape the implementation

| Fact | Consequence |
|---|---|
| About 11,000 patients; up to 50 segments of about 70 min at 250 Hz each, sampled at random from recordings of up to 14 days; some patients have fewer (p08975 has 20) | Hours per patient vary; every rate is per **analysed hour** |
| Segments carry **no clock time**, and segment numbers are not chronological | Never compute an interval across two segments; a "day" must be a pseudo-day built from a patient's segments; the reference is a patient-level rate × 24 |
| Beat labels N, S (PAC), V (PVC), Q (unclassifiable, about 24% of beats); rhythm labels in `aux_note` include AFIB and AFL | Exclude Q beats and intervals touching them; decide how AF stretches are handled (**Decision D3**) |
| RO1 and RO2 use beat annotations, not raw ECG (§3.7: "one GPU suffices, as RO2 uses beat annotations rather than raw signals") | Download annotation and header files only; the raw signal is not needed for the Icentia11k work |
| Licence CC BY-NC-SA 4.0 | Non-commercial; cite; derived tables shared under the same terms |

**Scale.** Icentia11k holds 2.77 billion labelled beats, of which about 0.68 billion are unclassifiable (Q), so roughly **2 billion intervals** remain for tallies once intervals touching Q are dropped (298 patients gave about 57 million). Stored as a compact table (interval in ms, beat classes, segment id), that is in the order of 10 to 20 GB on disk: manageable on one workstation, but it must be streamed, not loaded at once.

---

## 3. Patient sets first, before any new analysis

Table B.3 fixes four disjoint sets. Lock them before opening any data beyond P0.

| Set | Use | Size | Status |
|---|---|---|---|
| P0 | Preliminary RO1 | 300 sampled, 298 analysed (fixed seed) | Done; reuse the same seed and list |
| P1 | H1 test | "New random sample, size fixed before analysis" | **Decision D1**: size from a power simulation using P0 (below) |
| P2 | RO2 training, validation, test, split by subject | "Random sample, split lists recorded and released" | **Decision D2**: proposed default is all remaining patients, split 70/15/15 by patient |
| P3 | RO4a held-out test | About 300, untouched until M4 | Draw now, store the list, do not read its annotations until M4 |

How to lock them:
1. Draw P3, then P1, then P2 from the patients not in P0, each with its own recorded seed.
2. Save the four lists as plain text in the analysis repository with a SHA-256 hash of each, and commit before any analysis of P1, P2 or P3.
3. Make the data loader refuse to read a patient whose set does not match the analysis being run (a simple guard that prevents leakage by accident).

**D1, sizing P1.** Use P0 to estimate the burden effect on retention (per-patient retention at 20% against log PACs per hour), simulate the H1 model at candidate sizes, and pick the smallest size with 90% power at α 0.05. Fix the size in a dated note before drawing data, as was done for the Pulsewatch pre-check.

---

## 4. Stage A: the data pipeline (S2 to S3)

One pipeline, run once, produces the tables every later stage reads.

1. **Download** headers and beat annotations from PhysioNet (Icentia11k continuous ECG, v1.0) with `wfdb`; record the file list and checksums.
2. **Index**: one row per segment (patient, segment, length, number of beats by class, rhythm labels present).
3. **Beat table**, per patient, one row per beat: segment, sample index, beat class, rhythm context (inside AFIB or AFL or not).
4. **Interval table**: RR from consecutive beats **within a segment only**; tag each interval by the class of the beat that ends it (coupling interval) and starts it (pause after a PAC); drop intervals touching Q, and intervals outside 0.2 to 3.0 s, from the tallies (as the preliminary script did: the filter runs on all intervals, exclusions apply to the counts).
5. **Patient summary**: analysed hours; PACs, PVCs, normal beats; PACs per hour; reference daily-equivalent count (PACs per analysed hour × 24); ESVEA status by the primary definition (≥480 per day) and the secondary (≥30 per hour; rate or run as Binici et al., 2010, for comparability with §4.2); longest PAC run.
6. Write everything to columnar files (Parquet), one file per patient, so later stages stream patient by patient.

Checks before moving on: P0 summaries from the new pipeline must reproduce Table 4.2 and Table 4.3 exactly. If they do not, the difference is a pipeline bug, not a finding.

**D3, AF stretches.** Normal intervals in §4.2 included irregular rhythms such as AF (stated as a limitation). Proposed default: run every RO1 analysis twice, with AFIB/AFL stretches included and excluded, and report both; for RO2 training, exclude AF stretches from the PAC count target but keep them in the input so the model sees them.

---

## 5. Stage B: RO1 in full (S2 to S3; M3 RO1 paper)

| Part | Data | What to run | Output |
|---|---|---|---|
| RQ1.2 filtering loss | P0 for curves | Percent-deviation filter at 10% to 30% in 1-point steps; adaptive threshold of Lipponen and Tarvainen (2019) | Retention curves by beat class and by burden band |
| **H1** | **P1** | Mixed-effects logistic regression of PAC coupling-interval retention on burden (log PACs per hour), 20% threshold primary, other thresholds as sensitivity | Burden effect with 95% CI; direction reported (§4.2 already suggests higher retention at higher burden) |
| RQ1.3 origin loss | P1 | Premature-beat count (S+V) vs PAC-only count (S) per patient, by burden | Count discrepancy; Bland–Altman bias and limits |
| RQ1.1 morphology loss | Pulsewatch | Waveform model vs interval model on identical recordings (see §8) | Change in F1 and AUROC (DeLong; paired bootstrap) |

Implementation notes for H1:
- About a million PAC intervals cannot all enter one mixed model comfortably; aggregate to **retained / total PAC intervals per patient** and fit a binomial mixed model (patient random intercept). This is the same model in aggregated form and runs in seconds.
- Write the analysis script and the model formula into a dated, committed note **before** running it on P1.

RO1 also produces two numbers RO2 and RO4a need: retention by beat class and burden at each threshold (to calibrate the flag simulator and the RO4a severity sweep).

---

## 6. Stage C: the training simulator (S3)

Icentia11k has ECG intervals with true labels but none of the things a Garmin adds. The simulator turns a clean Icentia11k segment into a watch-like stream for training. It must follow §3.4 and Table 3.4 exactly, and it must be **separate** from the RO4a degradation code, so RO4a is not an in-distribution test (§3.6: "sampled independently of the training simulation").

| Element | Rule from the proposal | Implementation |
|---|---|---|
| Device flag (binary) | Marks motion-affected beats and any interval judged abnormally short or long (Garmin, 2023) | Flag = 1 if the interval deviates from a running reference by more than a threshold (calibrated from RO1), or if the beat falls in a motion episode |
| Motion | Retention depends on motion m; π̂(m) fitted on Pulsewatch | **Decision D4**: Icentia11k has no accelerometer, so motion traces must be simulated. Proposed default: sample motion episodes from Pulsewatch accelerometer magnitude (distribution of level and duration), placed at random in each segment |
| Silent loss | Unflagged beats missed at motion, rate from π̂(m) | Drop a beat with probability 1 − π̂(m); the two intervals around it merge into one, unflagged |
| Gaps | Marked by the device where it gives no beat | Remove stretches and record them as unobserved time τ, with a gap marker |
| Pulse deficit | Not simulated in training | Left to RO4a only (it is the bias RO4a measures) |
| Timing noise | PPG peak vs ECG R-peak offsets | Small jitter drawn from Pulsewatch offsets (optional in training; required in RO4a) |

Every simulated stream keeps the truth alongside it (which beats were PACs, which were dropped), so the targets stay exact.

---

## 7. Stage D: RO2, the estimator (S3 to S4; M4 freeze)

### 7.1 Data for training

- **P2** only, split by patient into train, validation and test (D2).
- **Pseudo-days**: group each patient's segments into 24-hour pseudo-days (about 20 segments each), assigning segments to the four 6-hour blocks at random, as decided after the clock-time check. A patient with 50 segments gives about two pseudo-days.
- **Windows**: within each segment, cut the reported beat stream into windows of N beats (**Decision D5**: N, k and depth L are open choices and are reported as sensitivity analyses).
- **Targets**: beat-level PAC label; window PAC count (auxiliary rate head); patient-level reference rate for evaluation.
- Class balance: any resampling only inside training folds; validation and test at natural prevalence (§3.7).

### 7.2 The model

Implemented in PyTorch and PyTorch Geometric, as Figure 3.2:
1. Per-beat features: interval, next interval, ratios to a local reference, flag, motion.
2. Per window: banded temporal-chain graph Â_adj and k-nearest-neighbour similarity graph Â_sim, built once and reused in all L local layers; gated local block; attention readout to one embedding per window.
3. Across a pseudo-day: interval block (graph convolution and a selective state-space layer) over window embeddings in order.
4. Heads: event head (beat PAC probability p̂ᵢ); rate head (auxiliary only).
5. Outside the network: temperature scaling of p̂ᵢ on validation patients; frozen π̂(m) from Pulsewatch; Equations 3.2 to 3.4; the coverage gate.

**D6, training losses.** Open in the proposal. Proposed default: weighted binary cross-entropy for the event head plus a count loss (for example Poisson) for the rate head, with the weight chosen on validation.

### 7.3 Comparisons (Table 3.2)

Run every model on the same simulated streams and splits, five seeds each:
- RQ2.1 baselines: logistic regression, SVM and random forest on RR features; RR plus morphology (Dias et al., 2021); Poincaré rule (Han et al., 2020); BiLSTM; GRU-D; transformer.
- RQ2.2: epoch graph vs summation, mean pooling and an LSTM over epochs.
- RQ2.3 ablations: remove chain edges, similarity edges, interval block, retention correction, coverage gate.
- RQ2.4: flag as filter vs input vs input with correction.

**H2** is the one primary contrast: daily-equivalent MAE of the two-scale ST-GNN with flag as input vs the best non-graph baseline on the P2 test patients, paired subject-level bootstrap 95% CI. Everything else is Holm-corrected. If H2 is rejected, the retention correction and gate are applied to the best baseline and the negative result is reported (§3.9).

### 7.4 Compute

The proposal states one GPU suffices. Practical setup: stream patient files, sample windows per epoch rather than iterating all 2 billion intervals, cache graphs per window. Budget roughly: data pipeline once (hours), each training run in hours, 5 seeds × all baselines and ablations in the order of weeks of GPU time, so schedule ablations to run unattended. **Decision D7**: confirm GPU access (faculty server or cloud credit) before S3.

### 7.5 Freeze at M4 (S4)

Freeze and hash: model weights, temperature, π̂(m), θ_block placeholder, simulator configuration, split lists, code commit. Only after this is P3 opened.

---

## 8. Other datasets: what is needed and when

| Dataset | Needed for | What to implement | When | Notes |
|---|---|---|---|---|
| **Pulsewatch** (Synapse syn23565056) | RQ1.1; π̂(m); timing-noise offsets; motion profiles for the simulator (D4); RO2 window-level external test; real day order for the epoch graph | (1) Waveform vs interval models on identical 30-s windows, PAC and PVC merged; (2) π̂(m): match PPG peaks to lag-corrected ECG R-peaks outside peak-free stretches, by motion bin, Elgendi et al. (2013) detector primary, authors' peaks as sensitivity; (3) a label-free lag method (the current one reached only 2.5% of excluded and 0.8% of no-label segments) | S2 to S3, before RO2 training | **Permitted use still to be confirmed in writing**: the main data risk |
| **Garmin specification** (Garmin, 2023) | Flag and gap rules for the simulator and the estimator | Encode as simulator rules (§6) | S3 | Confirm against the real export at device verification (M1) |
| **RO3 cohort** (PPUM, Garmin) | RO3; realistic coverage for RO4a; RO4b | No training. Inference with the frozen model only; coverage profile by block feeds RO4a | S4 to S6 | No ECG, so no accuracy claims |
| **Simband, MIMIC-III** | Pilot only (§4.1) | Not required for RO1, RO2 or RO4a. Optional: an external AF-vs-ectopy window check of the RO2 encoder | Optional | Fallback external sets |

---

## 9. Stage E: RO4a on P3 (S5 to S6)

1. Open P3. Compute each patient's reference status from ECG labels: daily-equivalent count (≥480 primary; ≥30 per hour secondary).
2. Build pseudo-days as in RO2, then degrade with the four operators of Table 3.4, **sampled independently of the training simulator**:
   - flags and silent loss (Garmin rules; Pulsewatch motion retention),
   - coverage gaps by block on pseudo-days (night-weighted pattern of Merschel and Reinhardt, 2022; replaced by the RO3 coverage profile when available),
   - pulse deficit (pulse lost below a coupling interval of about 55% of the sinus RR; swept around that value),
   - interval timing noise (Pulsewatch offsets; swept).
3. Run the frozen estimator; compute 24 · R̄ per patient and the ESVEA call.
4. Report reclassification rate, κ, sensitivity and specificity at the cut-off, with Wilson 95% CIs, **for each operator across its severity sweep** and for combinations. With about 67 of 300 expected at ≥480 per day, sensitivity is estimated within about ±8 percentage points.

---

## 10. Track 2: readiness for real-patient data acquisition (S2 to S4)

Nothing in the cohort can start until the device is verified (M1) and ethics is approved with the protocol registered (M2), both planned for S3 (Table 6.2). Recruitment and 7-day monitoring begin in S4 (Table 6.1). The steps below are in dependency order.

### R1. Device and data access (S2)

| Task | Why | Done when |
|---|---|---|
| Obtain the Garmin watches for verification | The device has not been received; every later step depends on it | Watches in hand, model and firmware recorded |
| Confirm Garmin Health SDK or API access and its licence terms | Enhanced beat-to-beat intervals, the per-beat confidence flag, gap markers and accelerometer data must be exportable for research | Written access confirmation |
| Obtain Garmin's 24-hour logging confirmation **in writing** | The proposal currently rests on a personal communication (§3.5) | Written confirmation filed |
| Set up study-managed, pseudonymous accounts | §3.8: export under study accounts, not participants' personal accounts, where possible | Accounts created, naming scheme fixed |

### R2. Device verification on non-participant wear (S2 to S3; gate M1)

§3.5 requires this before ethics submission. It answers whether the Garmin behaves as the model assumes, and it fixes the thresholds the protocol must state.

| Check | Question | Feeds |
|---|---|---|
| Export | Can the intervals, flag, gap marker and accelerometer be exported together, time-stamped? | R3 parser |
| Flag encoding | Is the flag binary per beat; does it mark abnormally short or long intervals as the specification says? | Training simulator (Stage C); Equation 3.2 inputs |
| Gap encoding | Are stretches with no beat marked as gaps, distinct from "not recording"? | Observed time τ; coverage gate |
| 24-hour logging | Are intervals recorded through the day, not only overnight? | Feasibility of day blocks; the whole RO3 design |
| 7-day battery | Does the watch last 7 days with intervals and accelerometer on, with one short daily charge? | Wear instructions; charging window |
| **Accelerometer scale** | In what units and at what rate does the Garmin report motion, and how does it map to the Pulsewatch motion bins used for π̂(m)? | Transfer of π̂(m) from Samsung to Garmin (section 11) |
| Coverage thresholds | What day and night coverage, and what per-block minimum θ_block (proposed about 1 h), are realistic? | Valid-day rule; Equation 3.3; protocol |

Output: a dated verification report and the threshold values written into the protocol. **This is M1.**

### R3. Garmin data pipeline (S3)

Built and tested on the verification data, so it is proven before any participant wears a watch.

1. Export from the study accounts to pseudonymised storage on university infrastructure (PDPA 2010).
2. Parse into the same beat-table layout as Icentia11k: one row per reported beat with interval, flag, gap marker, accelerometer motion and clock time.
3. Compute coverage per 6-hour block, the valid-day rule, and the per-block gate (Equation 3.3), using the **same code** as the RO2 estimator.
4. Log wear time and recording time separately (Table 3.3, adherence logging), so the study team can see during the week whether a participant's data are accumulating.

### R4. Protocol, documents and ethics (S2 to S3; gate M2)

| Document | Content fixed by the proposal |
|---|---|
| Study protocol | Eligibility (adults after ischaemic stroke or TIA, no known AF, after discharge); consecutive approach at PPUM; 7-day wear; valid-day rule and θ_block from R2; outcomes RQ3.1 to RQ3.5; progression criteria (red ≤50%, amber 51 to 74%, green ≥75%); sample (recruit about 40, analyse ≥34) |
| Participant information sheet and consent form | Written informed consent; statement that watch data are not reviewed in real time and the study is not clinical monitoring; rhythm concerns referred through usual care |
| Data management plan | Pseudonymisation at collection; university storage; PDPA 2010; study-managed accounts |
| Case report form for routine records | ESUS status; items for CHA₂DS₂-VASc, HAVOC, C₂HEST, AS5F and Brown ESUS-AF (ESUS subgroup only); left atrial volume index, P-wave duration and NT-proBNP (RO4b) |
| Screening log and wear log | Consecutive approach; wear and charging record |

Submit to the PPUM Medical Research Ethics Committee after M1; register the protocol before recruitment. **Approval plus registration is M2.**

### R5. Site readiness at PPUM (S3)

- Agree the recruitment pathway with the clinical team: where and when patients are approached after discharge.
- Device logistics: issue, fitting, charging instructions, return, cleaning, and replacement stock.
- Scheduled contacts during the 7 days (Table 3.6 mitigation for wear tolerance).
- A first-fit run-through with the study team on the full sequence, from consent to export, before the first participant.

---

## 11. Where the two tracks meet

| Meeting point | From track 1 | From track 2 | Why it matters before acquisition |
|---|---|---|---|
| **Coverage and valid-day code** | The coverage gate and Equation 3.3 in the estimator | The valid-day rule and θ_block in the protocol (R2, R4) | One implementation, so the protocol's definitions and the estimator's cannot drift apart |
| **Dry run on real Garmin output** | An interim RO2 model and the estimator pipeline | Verification wear data through the R3 pipeline | Proves a Garmin export can be read end to end, from intervals to a daily estimate, before patients are enrolled; the frozen model is not needed yet |
| **Motion scale for π̂(m)** | π̂(m) fitted on Pulsewatch accelerometer magnitude | Garmin accelerometer units and rate (R2) | π̂(m) is applied to Garmin motion; without a mapping between the two scales, the Samsung-to-Garmin transfer cannot be applied at all |
| **Fallback coverage model** | Coverage modelled from Pulsewatch wear data | Only needed if the gate fails | §3.9: if the cohort cannot start, RO3 becomes device verification with coverage modelled from Pulsewatch; it should exist before S4 so the fallback is immediate |

---

## 12. Go/no-go gate (start of S4)

| Condition | Evidence |
|---|---|
| Device verified (M1) | Verification report; thresholds in the protocol |
| 24-hour interval logging confirmed | R2 result and Garmin's written confirmation |
| Ethics approved and protocol registered (M2) | Approval letter; registration record |
| Garmin pipeline proven | R3 run on verification data; dry run of section 11 |
| Site ready | R5 run-through completed |

**Go:** recruitment and 7-day monitoring start in S4 (Table 6.1). **No-go** (ethics, the device or 24-hour logging not secured by S4): RO3 becomes a device-verification study with coverage modelled from Pulsewatch wear data, RO4a proceeds unchanged and RO4b is deferred (§3.9). RO1, RO2 and RO4a do not depend on the cohort.

---

## 13. Repository and reproducibility

```
analysis/
  configs/            one YAML per run (seed, set, thresholds, model sizes)
  splits/             P0.txt P1.txt P2_train.txt P2_val.txt P2_test.txt P3.txt + SHA256SUMS
  src/ingest/         download, index, beat and interval tables
  src/ro1/            filters, retention curves, H1 model, RQ1.3
  src/simulate/       training simulator (separate from degrade/)
  src/degrade/        RO4a operators
  src/model/          ST-GNN, baselines, estimator equations, gate
  src/pulsewatch/     RQ1.1, retention fit, lag method, timing offsets
  notes/              dated pre-analysis notes (H1 formula, P1 size, freeze record)
  results/            tables and figures, regenerated from code only
```

Rules: five seeds per model; every result regenerated from a config; the loader guard on patient sets; pre-analysis notes committed before each confirmatory test; code and split lists released on publication (§3.7).

---

## 14. Sequence against the schedule (Table 6.1)

| Semester | Track 1: modelling | Track 2: readiness for acquisition | Gate |
|---|---|---|---|
| S2 (now) | Lock P0 to P3; data pipeline; reproduce §4.2 on P0; D1 sizing note | R1 device and data access; start R2 verification; draft R4 documents; Pulsewatch permission | Tables 4.2 and 4.3 reproduced |
| S3 | H1 on P1; RQ1.2, RQ1.3; RQ1.1 and π̂(m) on Pulsewatch; simulator; RO2 build starts | Finish R2; R3 pipeline; ethics submission after M1; R5 site readiness; section 11 dry run | **M1** device verified; **M2** ethics and registration; M3 RO1 paper |
| S4 | RO2 baselines, ablations, H2; freeze | Go/no-go; first participants fitted | **Go/no-go**; **M4** model frozen, then P3 opens |
| S5 to S6 | RO4a on P3 | 7-day monitoring and analysis (RO3); RO4b | M6 recruitment complete (S5) |
| S6 to S7 | Writing | Writing | M7 submission |

---

## 15. Decisions to settle with the supervisors

| ID | Decision | Proposed default |
|---|---|---|
| D1 | Size of P1 | Smallest size giving 90% power for H1, from a simulation on P0 |
| D2 | Size and split of P2 | All remaining patients, 70/15/15 by patient |
| D3 | AF stretches | Report RO1 with and without; exclude from the RO2 count target, keep in the input |
| D4 | Motion for the training simulator | Sample motion episodes from Pulsewatch accelerometer data |
| D5 | Window length N, neighbours k, depth L | Choose on validation; report sensitivity |
| D6 | Training losses | Weighted cross-entropy (event) plus Poisson count loss (rate) |
| D7 | GPU access | Confirm a faculty server or cloud allocation before S3 |
| D8 | Who wears the watch for device verification, and whether that needs its own ethics approval | Study team and volunteers; confirm with the PPUM ethics office first |
| D9 | Where the protocol is registered | A public trial or study registry agreed with the supervisors |
| D10 | Language versions of the information sheet and consent form | As required by the PPUM ethics committee for the patient population |
| D11 | Mapping Garmin accelerometer output to the Pulsewatch motion scale | Fixed from the R2 accelerometer check before π̂(m) is applied |

None of D1 to D11 contradicts the proposal: each fills a choice the proposal leaves open (the research map's "Open design choices" list names N, k, L, the losses and the simulator specification).
