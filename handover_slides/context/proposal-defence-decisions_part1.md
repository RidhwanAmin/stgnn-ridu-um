# Proposal Defence — Decision Log

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

## Item 1 — RO4 framing ✅ DECIDED

### Problem
The original RQ4.2 claimed *substitution* for the Holter-derived ectopy term and measured it with net reclassification improvement (NRI). NRI is defined over events and non-events, so it requires an observed outcome or reference classification (Pencina et al., 2014). The prospective cohort has neither: no concurrent ECG (a stated design boundary) and no AF follow-up.

### Options considered
| Option | Description | Outcome |
|---|---|---|
| A | Holter on a subset of the cohort | Rejected as primary — reverses the "no concurrent ECG" boundary; kept as optional add-on (see Next steps) |
| B | AF follow-up as outcome | Rejected — expected AF ≈ 9% at 24 months (from Haeusler et al., 2025: ESVEA 25.3%, AF 18.5% vs 5.9%) → ~3 events at n = 30 |
| **C** | **Split RO4: retrospective substitution on Icentia11k + prospective comparative selection** | **Selected** |
| D | Drop substitution; comparative selection only | Rejected — weakest contribution |

### Final wording
**RQ4.** Does substituting a smartwatch-derived ectopy estimate for the ECG-derived count change patients' ESVEA classification, and how do wearable-based selections compare with clinical risk scores?

**RO4.** To determine
- **(a)** the reclassification of ESVEA status when ECG-derived counts are replaced by estimates from simulated smartwatch intervals, degraded by quality-based rejection, coverage gaps and pulse deficit calibrated from measured data; and
- **(b)** the agreement and composition of wearable-based versus score-based selections in post-stroke survivors.

### Design
| | RO4a — Substitution | RO4b — Comparative selection |
|---|---|---|
| Data | Icentia11k, degraded to Garmin-like output | RO3 cohort + routine records |
| Truth | ECG beat labels | None required (agreement only) |
| Metrics | Reclassification rate; κ at ESVEA cut-off; sensitivity/specificity of wearable ESVEA across degradation severities | Cohen's κ; Jaccard overlap; profile of discordant patients; association with atrial substrate markers |
| Removed | NRI on PROACTIA | — |

### Degradation model (amendment from revalidation)
| Operator | What it simulates | Calibrated from |
|---|---|---|
| Interval rejection | Quality-based beat filtering | RO1 results |
| Coverage gaps | Non-wear, charging, unusable PPG | Gruwez et al. (2021); Aguilar et al. (2025); RO3 cohort once collected |
| **Pulse deficit (beat merging)** | Premature beat produces no detectable wrist pulse → short + long interval seen as one long interval | Pulsewatch paired PPG–ECG; fallback: published PVC pulse-deficit evidence |

Results reported across a severity sweep for each operator, not a single setting.

### Evidence from revalidation (Consensus, PubMed, Scholar Gateway)
| Claim | Finding | Source |
|---|---|---|
| Simulating wearable monitoring from continuous records is accepted method | Smartwatch algorithms simulated on implantable-monitor data (CIRCA-DOSE, n = 346), daytime wear; >90% sensitivity with 24-h wear | Aguilar et al. (2025); also Aguilar et al. (2021), Quer et al. (2020), Ziegler et al. (2006) |
| Garmin PPG intervals degrade beat-level variability | Garmin vívoactive 4 vs ECG in 129 ischaemic stroke patients: near-perfect global agreement, rMSSD only moderate (ρc = 0.66) | Theurl et al. (2023) |
| Pulse deficit is real | PVCs with and without observable PPG pulse; PVC pulse may be too weak to detect | Sološenko et al. (2015); Argüello Prada et al. (2026); Kovoor et al. (2021) |
| PAC-specific pulse deficit | Evidence thin — named as a gap, addressed by calibration | — |
| NRI requires an outcome | Defined over events/non-events | Pencina et al. (2014) |
| Gap 1 still holds | Smartwatch AF burden widely validated; no study reports a smartwatch-derived daily PAC count | Zuo et al. (2026); Poh et al. (2023); Anagnostopoulos et al. (2025) |

### Slides affected
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

### Next steps to lock item 1
- [ ] Confirm Icentia11k annotation procedure (adjudicated vs technician-reviewed) — Tan et al. (2019) / PhysioNet record
- [ ] Confirm Pulsewatch access includes reference ECG alongside PPG
- [ ] Ask supervisors whether a hospital collaborator runs routine Holter on post-stroke patients (optional paired subset)

---

## Item 2 — RO3 numbers ⏳ OPEN

| Sub-decision | Options | Recommendation |
|---|---|---|
| Sample size | n = 30, or supervisor-specified | n = 30, justified by precision of coverage proportion (Wilson 95% CI half-width ≈ ±17% at 50%) |
| Monitoring duration | (a) 4 calendar days, ≥3 days at ≥95% coverage; (b) 7 days | Decide; current deck conflicts ("72 h over 4 days" vs "3 days") |
| Site | Named site or explicit placeholder | — |

Note from revalidation: Huntelaar et al. (2024) found 92.5% of cryptogenic stroke candidates ineligible and halted enrolment — argues for broad eligibility, not a cryptogenic-only cohort.

## Item 3 — Presentation slot length ⏳ OPEN

| Slot | Main deck |
|---|---|
| 25–30 min (assumed) | ~28 slides |
| 15–20 min | ~18 slides; more moved to appendix |

## Item 4 — Output format ⏳ OPEN

| Option | Notes |
|---|---|
| Claude Slides (recommended) | Editable; downloads as .pptx or PDF |
| PowerPoint file | If editing continues in PowerPoint or UM requires a template |

## Item 5 — Literature depth ⏳ OPEN

| Option | Notes |
|---|---|
| Verify + extend (recommended) | Check existing citations and add 2025–2026 work |
| Verify only | Check existing citations only |

---

## References (item 1)
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
