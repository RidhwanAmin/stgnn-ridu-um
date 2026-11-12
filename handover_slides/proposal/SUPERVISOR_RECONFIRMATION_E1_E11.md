# Items needing supervisor reconfirmation: E1 and E11

**Status:** applied to `proposal/source/content.txt`, `proposal/Ridhwan_Research_Proposal_UM.docx` and the slide deck on 3 November 2026, with the candidate's approval. **Both items still need confirmation from Dr. Bryan Raj and Assoc. Prof. Dr. Ismail Ahmedy.** If either is not confirmed, revert using the "Current" text in `drafts/proposal_revisions_draft.md` (sections E1 and E11) and rebuild.

The handover version of the docx is kept as `proposal/Ridhwan_Research_Proposal_UM_handover_2026-11-03.docx` for comparison.

---

## E1: retention corrects only silent device loss

**Why confirmation is needed:** it reverses logged decision 6g (`decisions/proposal-decisions-2026-11-02.md`), which set Equation 3.1 as class retention from RO1 multiplied by motion retention from Pulsewatch.

**What changed** (revised after independent review, 3 November 2026)
- **Equation 3.1** is now π̂(m) = P(beat reported | motion m, outside a gap). Retention depends on motion only and is fitted on Pulsewatch.
- **Pulsewatch gap analogue:** π̂(m) is fitted outside stretches with no detected peak, matching the Garmin gap rule found in device verification. Otherwise beats that the Garmin would turn into a gap (already removed from τ) would be corrected a second time.
- **Pulse deficit is no longer in Equation 3.1.** A premature beat with no wrist pulse leaves no reported beat with a similar coupling interval, so inverse-probability weighting cannot restore it (a positivity failure). It is now a bias quantified by the RO4a pulse-deficit sweep.
- **Equations 3.2 and 3.4** use π̂(mᵢ).
- **Section 3.4** says gaps enter the observed time, the flag is an input and adds no weight, and the reliability pathway corrects only silent loss at motion.
- **Table 3.4:** "Beat rejection (deletion by the device)" is replaced by "Flags and silent loss", consistent with the Garmin flagging rather than deleting.
- **Section 4.2:** RO1's filter results support keeping flagged beats as input (RQ2.4).
- **Appendix C** notes that its 0.391 beat retention is pessimistic for a device that flags rather than deletes.

**Evidence:** the Garmin Enhanced BBI whitepaper (Garmin, 2023; already cited). It says abnormally short or long beats are kept and marked low confidence, and that extreme motion or poor signal produces a marked gap.

**Points for supervisors to weigh**
1. RO1's role changes. Its filter results justify flag-as-input rather than supplying a term in Equation 3.1. RO1 is paper 1 (milestone M3).
2. Pulse deficit is measured, not corrected. A merged-interval output that predicts hidden PACs in long intervals is possible RO2 work, but it is not proposed.
3. The evidence is a vendor document (one subject, one night, Venu 2 Plus, 2023). Device verification must confirm flag and gap behaviour on the study device.
4. 24-hour Enhanced BBI recording rests on Garmin's statement to the candidate; the public whitepaper describes overnight intervals. Section 3.5 mentions Garmin's confirmation without a citation, adds 24-hour logging to device verification, and adds it to the Section 3.9 fallback. **Keep Garmin's confirmation in writing.**

---

## E11: pilot results rewritten (Section 4.1, Table 4.1, abstract)

**Why confirmation is needed:** it changes a headline number the supervisors have seen, and withdraws earlier values.

**What changed**
- **Withdrawn:** the Simband and MIMIC-III values 0.891, 0.951, 0.944, 0.998 and 0.973, which used legacy external labels.
- **New results:** re-curated external labels, all v2 training and validation subjects excluded, same checkpoint, evaluation mode. AUROCs at the untuned score weight 0.5; recall at the validation thresholds (gfeat-head score), not re-tuned.
- **Test set:** 33 subjects (16 Pulsewatch clinical, 8 Pulsewatch AF-only holdouts, 6 Simband, 3 MIMIC-III).
- **Abstract:** "AF recall between 88% and 100% … without per-device threshold tuning" becomes "ranked AF above other rhythms well (AUROC 0.995 or higher where non-AF windows existed, one AF subject per cohort), but AF recall at a threshold fixed on validation subjects ranged from 45% to 100% across devices".
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

## Other applied revisions (for information only)

E2 (pseudo-days and Pulsewatch ordering), E3 (daily-equivalent count), E4 (no double counting; calibrated p̂; Guo et al., 2017 added), E5 (interval timing-noise operator), E6 (Garmin flag vs motion check), E7 (coverage gate as reporting rule), E8 (rate head as auxiliary target), E9 (pooled computability as key secondary), E10 (Table B.3, disjoint patient sets), and the trims T1, T3 to T8 and T11. Full before-and-after text is in `drafts/proposal_revisions_draft.md`.

**Build checks (3 November 2026):**
- main text 6,986 words, Chapter 1 to References (limit 7,000)
- zero em dashes
- every reference cited and every citation referenced
- Equations 3.1 to 3.4 each on one line
- 45 pages (LibreOffice render; Word not yet checked)
