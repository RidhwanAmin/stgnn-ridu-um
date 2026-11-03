# Independent review of the submission package (3 November 2026)

**Source:** an independent agent, given the 3 November package by the candidate.
**Outcome:** the candidate revised `proposal/source/content.txt`, the docx, the reconfirmation note, the slide deck and the research map page, and these were committed to the repository the same day.

---

## Resolution of each finding

| Finding | Verified by the drafting agent | Resolution (candidate's revision) |
|---|---|---|
| **C1** Pulse-deficit term cannot correct (positivity failure) | Agreed | Option 1: pulse deficit removed from Equation 3.1, now π̂(m) = P(beat reported \| motion m, outside a gap); pulse deficit is a bias quantified by the RO4a sweep. Equations 3.2 and 3.4 use π̂(mᵢ) |
| **C2** Motion term may double-correct gap time | Agreed | π̂(m) fitted on Pulsewatch outside stretches with no detected peak, mirroring the Garmin gap rule |
| **C3** 24-hour recording rests on an unpublished statement | Agreed | §3.5 states that the whitepaper describes overnight intervals and cites Garmin's confirmation of 24-hour logging; 24-hour interval logging added to device verification and to the §3.9 fallback. Written confirmation still to be filed |
| **M1** Table 3.4 models the Garmin as deleting beats | Agreed | Row replaced: "Flags and silent loss \| Low-confidence flags on abnormal and motion-affected beats; unflagged beats missed at motion \| Garmin (2023) specification; Pulsewatch motion retention"; RO4 slide updated |
| **M2** Stale Equation 3.1 on slide 18 and the research page | Agreed | `preliminary-icentia` (slide 18) and the research map page updated |
| **M3** Word count over under the handover rule | **Not reproduced.** Counting "all lines before # REFERENCES" gives 7,270 at handover and 7,318 before the revision, so the handover's stated "~6,980" matches the Chapter 1 rule (6,958 at handover). The review's 7,027 and 6,981 could not be reproduced | Main text 6,986 (Chapter 1 to References). With the abstract: 7,326. Whether the abstract counts remains a Postgraduate Office question |
| **M4** Abstract overstates the pilot | Agreed | Abstract adds "one AF subject per cohort" |
| Minor 1 "unweighted" wording | Agreed | §3.4 now says the flag adds no weight |
| Minor 2 π̂_pulse(other, q) = 1 | Agreed | Moot after C1 |
| Minor 3 to 5, 7 | Agreed | Kept as defence points or open items |
| Minor 6 em dashes in COMPILED_CONTEXT.md | Agreed | The compiled file is an archive, not a faculty submission |

---

## Review text (verbatim)

> # Independent review: ESVEA submission package (3 November 2026)
>
> **Scope:** the 3 November package (proposal docx and source, the 11 changed slides, the research map page, the drafts and check records), compared with the handover version of the same day.
>
> **Method:**
> - Line-by-line diff of `content.txt` against the handover source.
> - Rebuilt the docx from the package source.
> - Recounted words, references and em dashes, and re-rendered the equations.
> - Cross-checked the pilot numbers against the check records and the earlier `pilot_auroc_check.txt`.
> - Searched the full deck (handover copies plus the changed slides) and the research map page for stale content.
>
> **Verdict:** most revisions are sound and well documented, and E11 in particular is a clear improvement in honesty. But **E1 has two technical problems** that a methods examiner can find. Three consistency errors that E1 created remain in the docx and slides. The word count passes only under one of the two counting rules in use.
>
> ## What I checked and found correct
>
> | Check | Result |
> |---|---|
> | Package docx matches a fresh build of `content.txt` | Yes (identical text) |
> | Pages | 45 |
> | Em dashes in the proposal | 0 |
> | References | 67, all cited; no citation without a reference |
> | Equations 3.1 to 3.4 render one per line | Yes |
> | Table 4.1 clinical values at weight 0.5 (1.000; 0.998, 0.997 to 1.000) | Match the earlier independent output (`pilot_auroc_check.txt`, w = 0.5 rows) |
> | Abstract pilot sentence vs Table 4.1 | Consistent: AUROC ≥0.995 in all three cohorts with non-AF windows; recall at 0.393 ranges 45% to 100% |
> | E2, E3, E5 to E10 | Text matches the drafts; no internal contradiction found |
> | Guo et al. (2017) reference | Correct APA form for a PMLR proceedings paper |
> | Removed references (Abedi, Kapsecker, Montanaro, Ye) | Not cited anywhere in the text, and absent from the slides |
>
> ## Critical
>
> ### C1. The pulse-deficit term in Equation 3.1 cannot correct anything as specified (positivity failure)
>
> - **What the text says:** retention "combines pulse retention by coupling interval (Zheng et al., 2008)", and each reported beat is weighted by 1/π̂_PAC(mᵢ, qᵢ). The app-b3 notes say π̂_pulse uses "the published threshold of about 55% of the sinus RR".
> - **The problem:** inverse-probability weighting recovers lost units only if units with the same covariates are sometimes observed.
>   - If pulse loss follows a threshold, a PAC with q below about 0.55 is never reported, so no reported beat carries q below 0.55, and nothing gets up-weighted to stand in for those PACs.
>   - Every reported PAC has q above the threshold, where π̂_pulse is about 1, so the weight does nothing.
>   - With a smooth curve, PACs near the threshold get large, unstable weights, and those below it are still unrecoverable.
>   - In both cases the pulse-deficit PACs are not restored.
> - **What a lost PAC leaves behind:** one long merged interval, with a following beat that is reported normally. That is information, but Equation 3.2 doesn't use it.
> - **Fix (pick one):**
>   1. **Drop π̂_pulse from Equation 3.1** (π̂ₖ(m) = π̂_motion(m)). Treat pulse deficit as a bias that RO4a quantifies across its severity sweep, and state that it can't be corrected by weighting. About −15 words.
>   2. **Add a merged-interval output to the event head:** the probability that an observed long interval hides a PAC. Train it on Icentia11k with simulated pulse deficit, and add Σ of those probabilities to the count. This is more ambitious, needs one more sentence (about +25 words), and RO4a must then use a pulse-deficit setting the model was not trained on (see C2).
> - **My recommendation:** option 1 for the proposal, and mention option 2 as RO2 future work in the defence. Either way, Equations 3.1, 3.2 and 3.4, the definitions paragraph, the app-eq and app-b3 slides, and the reconfirmation note all change.
>
> ### C2. The motion term may double-correct beats that the Garmin turns into gaps
>
> - **The E1 premise:** the Garmin reports a gap under strong motion, and those gaps leave the observed time τ.
> - **The problem:** π̂_motion is fitted on Pulsewatch, where an offline detector on Samsung PPG silently misses beats at high motion; there is no gap marker.
>   - At the motion levels where the Garmin would produce a gap, Pulsewatch's misses count as "silent loss" in π̂_motion.
>   - On the Garmin, that time is already removed from τ.
>   - Applied to Garmin data, π̂_motion then up-weights beats in moderate-motion time for losses that were really gap time. The count is corrected twice in the same direction.
> - **Fix:** define a gap analogue on Pulsewatch before fitting π̂_motion. For example, any stretch longer than a set duration with no detected peak, or with a signal-quality index below a threshold, is a gap. Fit π̂_motion only on non-gap time. One sentence in Section 3.4 (about +20 words).
> - **The RO3 check helps but doesn't settle it:** E6 (flagged-beat fraction against motion) compares shapes, not this gap boundary.
>
> ### C3. The 24-hour recording that RO3 depends on rests on an unpublished statement, and the cited source says the opposite
>
> - **The conflict:** the proposal cites Garmin (2023) for the device (Table 3.3, Section 3.5), and the reconfirmation note quotes that same whitepaper as saying Enhanced BBI "is measured during the user's sleep interval". The 7-day continuous protocol, the day blocks and the per-block coverage rule all need 24-hour recording.
> - **Why it matters:** a panel member who opens the cited whitepaper will find it contradicts the design.
> - **Fix:**
>   - Cite Garmin's confirmation in Section 3.5 as a personal communication. In APA 7 that's in text only, for example "(Garmin Health, personal communication, [date])", at about +8 words.
>   - Make "24-hour Enhanced BBI logging" an explicit item of the device verification. The text already says "all-day logging".
>   - Add a sentence to the Section 3.9 fallback for the case where 24-hour logging is unavailable.
>   - Get the written confirmation before submission.
>
> ## Major
>
> ### M1. Table 3.4 and the RO4 slide still model the Garmin as deleting beats, which contradicts E1
> - Table 3.4: "Beat rejection | Quality-based deletion of intervals by the device | RO1 filtering results". The RO4 slide shows the same row.
> - E1's whole premise is that the Garmin flags abnormal beats rather than deleting them.
> - **Fix:** replace it with "Flag assignment | Low-confidence flags on abnormal and motion-affected beats, as the Garmin marks them | RO1 filter thresholds; Garmin (2023)". Keep deletion only as the "flag as filter" regime of RQ2.4, which Section 3.4 already covers.
>
> ### M2. Two places still describe the old Equation 3.1
> - **`preliminary-icentia.html` (deck slide 18):** "one correction factor cannot restore the count: retention must be learned (RO2)". Section 4.2 now says this "supports keeping flagged beats as input (RQ2.4)". The slide wasn't in the changed set.
> - **Research map page (`index.html`, version 3):** still shows π̂ₖ(m) = π̂_class(k) · π̂_motion(m), "RO1 … supplies the class part of the retention model", and "→ π̂_class(k)".
> - **Fix:** update both to the E1 wording, or to the C1-fixed wording once that's decided.
>
> ### M3. The word count is over the limit under the handover's own rule
> - **Handover rule:** "all lines before # REFERENCES", which includes the abstract. That gives **7,027**.
> - **Package rule:** Chapter 1 to References, which excludes the abstract. That gives 6,983. The draft note calls this "the handover rule", but the handover counted the abstract (6,981 at handover under that rule).
> - **The change:** the revisions added about 45 words net under a consistent rule.
> - **Fix:** until the Postgraduate Office confirms whether the abstract counts, trim about 40 words so both rules pass. Candidates:
>   - the long Table 4.1 row labels
>   - "so intervals reflect variation between windows, not AF patients" (the caption already says it)
>   - the second clause of the E2 sentence
>
>   C1 option 1 would also save about 15 words.
>
> ### M4. The abstract overstates the pilot
> - **What it says:** "ranked AF above other rhythms well (AUROC 0.995 or higher …)".
> - **The problem:** every cohort with a computable AUROC has **one AF subject**, which Section 4.1 and the Table 4.1 caption disclose but the abstract doesn't.
> - **Fix:** add "(one AF subject per cohort)" after the AUROC clause. That's +5 words; the abstract is outside the package's count, but inside the handover's (see M3).
>
> ## Minor
>
> 1. **"Flagged beats stay in the input unweighted"** (Section 3.4). Equation 3.2 weights every reported beat, flagged or not, by 1/π̂_PAC(m, q). The intended meaning is that the flag itself carries no weight. Suggest "Flagged beats stay in the input and are not reweighted for being flagged, so no beat is corrected twice."
> 2. **π̂_pulse(other, q) = 1** appears on the app-eq slide but not in the proposal. Add it, or it becomes moot under C1 option 1.
> 3. **Temperature scaling (E4):** calibration on validation subjects from the training domain won't fix a device-level scale shift, as MIMIC-III shows. The draft keeps this as a defence point, which is fine. Consider naming a Pulsewatch window-level recalibration check as the RO2 response.
> 4. **Table 4.1 caption** is about 150 words. It's legal, but heavy for a table caption. Consider moving the false-alarm figures into two extra table columns or a short note row.
> 5. **H1's role changed.** It now justifies flag-as-input rather than feeding Equation 3.1. Check that Table 3.5 (RO1 deliverable, "retention curves") still reads correctly.
> 6. **COMPILED_CONTEXT.md contains 26 em dashes** from the handover records. That's fine as an archive, but don't submit it to the faculty.
> 7. **Handover slide inconsistencies** still open, as the package already notes: `problem.html`, `gaps.html`, and the `app-a3` and `refs-1` sources removed earlier.
>
> ## On the two supervisor-reconfirmation items
>
> - **E11 (pilot): ready to show the supervisors as is**, after the abstract fix in M4. It is more honest than the handover version and internally consistent. The "rule locked but not blind" and "design iterated while inspecting holdouts" disclosures are correct to keep.
> - **E1 (retention): don't ask the supervisors to confirm it in its current form.** The premise (the Garmin flags rather than deletes) is good and well sourced. But the equation built on it has the C1 positivity problem and the C2 gap double-count, and two stale descriptions remain (M1, M2). Fix C1 and C2 first, then send E1 for reconfirmation together with C3's 24-hour evidence.
>
> ## Suggested order
> 1. Decide C1 (option 1 recommended), then add the C2 sentence and the C3 personal-communication citation.
> 2. Fix M1 (Table 3.4 and the RO4 slide) and M2 (slide 18 and the research map page).
> 3. Trim to pass both word-count rules (M3); add the abstract caveat (M4).
> 4. Rebuild and recheck: words under both rules, em dashes, references, equations on one line.
> 5. Send E1 (revised) and E11 to the supervisors.
