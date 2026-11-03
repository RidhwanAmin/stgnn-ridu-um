# Proposal audit against the UM FSKTM Proposal Defence checklist, and revision plan

Audit date: 30 October 2026. Audited file: the current research proposal (34 pages, about 6,990 words including tables). No changes have been made yet.

## Step 1. Revalidation of the checklist

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

## Step 2. Audit findings

Ratings follow the checklist: Critical, Major, Minor, or Keep (meets the item; no revision).

### Keep without revision
- Required content areas (1.3): all eight present.
- Title (2.1): names the problem, method, population and device; promises no results.
- Problem statement (3): all five links present (current practice, limitation, evidence, consequence, need), with a documented search behind "not quantified".
- Literature synthesis (4.2): grouped by theme (selector, scores, wearable detection, coverage, models), not paper by paper.
- Framework figures (7): conceptual framework and architecture are numbered, captioned, explained, and the novelty boxes are marked.
- Validation design (8.5, 9.1 to 9.4): validation matrix with "cannot claim" column, strong baselines, ablations, subject-wise splits, PROBAST+AI reporting, calibration, severity sweep.
- Preliminary findings (1.3): real results (Icentia11k) plus a clearly limited pilot.
- Clinical restraint (10): ectopy framed as a selector, no anticoagulation or recurrence claims.

### Critical
| # | Checklist item | Finding | Planned revision |
|---|---|---|---|
| C1 | 6.1, 6.3 Originality vs closest prior work | No section names the 3 to 5 closest studies and states what this thesis adds beyond each. Novelty is spread across significance and gaps. This is the panel's most likely attack. | Add a short "Closest prior work and contribution" subsection with a table: Han 2026 (Pulsewatch Bi-GRU), Chen 2024 (Pulsewatch DenseNet; PAC/PVC sensitivity 0.664, falling to 0.143 and 0.373 externally), Bhurane 2026, Schoels 2025 (beat intervals, ectopy interpolated away), Siejko 2025 (daily PVC burden from an implanted monitor). Columns: what it does, what remains, what this study adds. Then name each contribution by type: methodological (quality flag as evidence with retention weighting), empirical/measurement (error profile of a daily count; filtering loss), feasibility evidence (RO3). |
| C2 | 13.1 No contradictions; 13.2 accurate citations | The proposal cites the candidate's review with superseded figures ("30 studies, 20 recurrence, calibration in 5 of 30"). The verified review now reports 69 studies, 42 recurrence, 18 signal-based, calibration in 17, external validation in 4 of 42. The citation also lacks the title and third author. | Update Section 2.1, Section 3.7 and the reference to: Amin, R., Raj, B., & Ahmedy, I. (2026). From static prediction to continuous monitoring: A taxonomy-based systematic review... Note: the review's own abstract still says the in-hospital signal study had "unreported validation"; its body now says composite outcome with window-level cross-validation. Fix the review abstract too so both documents agree. |
| C3 | 11.1, 11.2 Feasibility of RO3 | Recruitment site is still "to be confirmed" and the device is not yet received. Both are stated, but there is no fallback that preserves a research question if RO3 cannot run. | Add a fallback: if recruitment or the device fails, RO3 becomes a device-verification study plus coverage analysis of Pulsewatch wear data, and RO4b is dropped while RO4a stands. Ask the supervisor to fix the site before submission (an admin action, not writing). |

### Major
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

### Minor
| # | Finding | Planned revision |
|---|---|---|
| m1 | Abbreviations: ESUS never defined; PPV used in 2.1 before definition; PAC used in the abstract before definition; ST-GNN not redefined in the body; "RR" means both risk ratio and RR interval; ICC and MAE undefined. | Define at first use; replace "risk ratio [RR]" with plain words. |
| m2 | Yang et al. (2022): HR 2.91 is for AF in stroke patients; the null result is recurrent ischaemic stroke or TIA. | Align wording with the verified review. |
| m3 | Grey literature (Vargova accepted abstract, Garmin white paper, conference abstracts) is not labelled as such in the text. | Add one sentence in 2.7 noting which sources are abstracts or technical documents. |
| m4 | "First" claims in the abstract and 5.1. | Qualify with "to our knowledge, based on the documented search". |
| m5 | Deliverables vs contributions (12). | One line separating deliverables (code, protocol, dataset of RO3 summaries) from contributions. |
| m6 | Repeated seeds and hyperparameter sensitivity not mentioned (9.3, 9.4). | Add to the analysis plan. |

### Slides (checklist 14)
The deck already covers 14 of the 16 suggested slides. Planned changes:
- Add a "Closest prior work and contribution" slide before the framework (mirrors C1).
- Add a short "Ethics and data access" slide (M5, M7), or fold it into risks.
- Update every slide that cites review figures (C2), and keep the deck consistent with all report changes (FCSIT requires consistency).
- End on a one-line contribution statement.

## Step 3. Word-count strategy
The report is at about 6,990 of 7,000 words counting tables. The revisions add roughly 900 to 1,000 words. Plan:
1. Ask the Postgraduate Office whether tables, references and appendices count (admin action A2).
2. Regardless, move the full literature matrix and the closest-prior-work detail to appendices, keep the main text tables short, and trim about 300 words from Chapter 2 and Section 1.1 background.
3. Target: main text at or under 7,000 words including tables; appendices outside the count if confirmed.

## Step 4. Actions only you can do (not writing)
| # | Action | Checklist |
|---|---|---|
| A1 | Confirm which deadline applies (semester 2 vs 3; two weeks vs one week), number of copies, and submission channel, in writing | 1.2 |
| A2 | Confirm what the 3,000 to 7,000 words include | 1.2 |
| A3 | Confirm recruitment site with supervisors | 11.1 |
| A4 | Confirm Pulsewatch data access status | 8.2 |
| A5 | Ask the supervisor about the AI-use declaration and the upload restriction in the UM November 2025 AI Guidelines | 10, 13.3 |
| A6 | Active (AK) status, application form, supervisor approval, evidence folder | 1.1, 1.4 |
| A7 | Mock defence and the examiner questions in Section 15 | 14, 15 |

## Step 5. Implementation order (after approval)
1. C2 and m1 to m4 (accuracy fixes).
2. C1, M1, M2, M4 (argument: aim, hypotheses, novelty, value of negative results).
3. M3, M5, M6, M7, M10 (methods precision and governance).
4. C3, M8, M9 (feasibility, risks, milestones).
5. Word-count pass, rebuild, render check.
6. Slide updates for consistency.

## Sources
- FSKTM Conduct of Candidature Seminars: https://fsktm.um.edu.my/fsktm/doc/postgraduate/24.conduct-of-candidature-seminars.pdf
- FSKTM Application Guideline: https://fsktm.um.edu.my/fsktm/doc/postgraduate/5-%20Application-Guideline-PD-CD.pdf
- UM Policy and Guidelines on AI (IAS compilation, Final V3): https://ias.um.edu.my/Student%20Affairs/Guideline/Compilation%20Policy%20%26%20GP%20AI%20-%20Final%20V3.pdf
- UM announcement of the AI policy: https://spm.um.edu.my/2026/03/15/universiti-malaya-releases-policy-and-guidelines-on-the-use-of-artificial-intelligence-in-teaching-and-learning/

## Implementation status (30 October 2026)
All writing items C1 to C3, M1 to M10 and m1 to m6 were implemented in the proposal (main text about 6,975 words including tables; Appendix A literature matrix and Appendix B definitions and data sources added). Slides updated: aim and hypotheses, closest prior work, risks with likelihood and fallback, ethics and data access, appendix equations, contribution statement, seventh references slide. Review abstract and conclusion aligned with the corrected García-Terriza description. Actions A1 to A7 remain with the candidate.
