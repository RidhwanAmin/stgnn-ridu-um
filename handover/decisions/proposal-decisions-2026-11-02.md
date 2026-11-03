# Proposal Defence: Decision Log, part 2 (2 November 2026)

Continues claude/proposal-defence-decisions.md. Where they differ, this file takes precedence.

## Item 6: Estimator, validation and data decisions ✅ DECIDED (2 November 2026)

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
