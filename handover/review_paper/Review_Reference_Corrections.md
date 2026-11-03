# Review paper: reference verification and corrections

All 79 references were checked against PubMed, Consensus and Wiley Scholar Gateway (plus publisher pages for computing venues). All 79 exist. The items below need changes.

## Claims not supported by the source (fix first)
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

## Outcome or design framing
- 39 Axford and 40 Kim JT: the outcome is a composite (recurrence or death; stroke, MI or death), not recurrence alone. 48 Kim 2023: composite MACE.
- 51 Ke: case-control design (recurrent vs first-ever admissions), not a cohort.
- 36 Wang: 0.887 to 0.946 is not labelled as test AUC; report "ROC analysis (10-fold CV 0.777 to 0.959)", single centre.
- 23 Mittag: inclusion was limited to studies reporting performance above 0.95, so pooled performance is inflated by selection.
- 74 Hu: detects prevalent CVD (cross-sectional), not prediction. 78 Fang: 6-month functional outcome, not recurrence.
- 58 and 59 Holmes: same 863-patient cohort; do not count as independent evidence.
- 21 Alhakeem: "early stroke prediction" rather than "first stroke".

## Metadata
- 1: author is Habibi, M. A.; Acta Neurol Belg 2025;125(3):609 to 624.
- 6 Ababneh: add 21(7):910 to 922. 13 Webb: 2018;49(1):62 to 67. 15: add 5(3):335 to 343.
- 22 Olawade and 23 Mittag: volume 249 and 207 are likely issue-year 2025 and 2026; use one convention.
- 33: add 73(4):1679 to 1693. 35 Vodencarevic: add 53(7):2299 to 2306; "double nested CV".
- 50: author "Zhou, Q."; n = 625. 51: author "Ke, L.". 55 Yu: 2025 in print (Int J Stroke 20(4):411 to 418).
- 68: single author Altwajre, B. A. N. (2025); weak venue, consider replacing.
- 70 Haule: confirm year and volume (article 109610). 73: first author Tabassum, I. 77 Lacson: use 2019 consistently.
- In-text: the Pulsewatch cohort is not "106 survivors" (see ref 33).

## Source-internal inconsistencies (avoid quoting)
- 54: AS5F 0.69 in the abstract vs 0.68 in the text. 57 Choi: "14.4%" does not equal 58/352 (16.5%). 60 Ding: SUS 65 in the abstract vs 62.8 in the text. 52 Zhang: prospective CI in the abstract is a typo.
