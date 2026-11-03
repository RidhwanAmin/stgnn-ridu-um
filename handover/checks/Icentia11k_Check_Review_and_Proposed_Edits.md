# Icentia11k clock-time check: independent review and proposed edits

Reviewed 2 November 2026 against the handoff folder (`claude_desktop_handoff/`), the current proposal source (Ridhwan_Research_Proposal_UM.docx) and the current slide deck. **Nothing has been edited.** Every edit in Part 3 waits for your approval.

Labels used throughout:
- **Confirmed:** I checked it against the cited file myself.
- **Inference:** my reasoning from confirmed facts; not checked against an external source.
- **Unverified:** stated in the handoff or elsewhere but not checked by me.
- **Decision:** a choice you need to make.

---

## Part 1. Independent check of the handoff

### Confirmed

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

### Where I disagree or add to the handoff

1. **Icentia11k cannot fit Equation 3.1 at all, not just its h-dependence.** The handoff (Still open, item 4) says Icentia11k "can't provide any dependence on block h". It also has no accelerometer (one signal per record, confirmed above), so it cannot provide the motion term m either. It can only inform retention by beat class, through the RO1 filter. *(Confirmed for the data; consequence is inference.)*
2. **"Summed to a true daily count" is wrong in the proposal itself.** Table 3.1 (RO2 row) and the validation-matrix slide say the Icentia11k ground truth is "ECG beat labels summed to a true daily count". With random, non-contiguous, untimed segments, the reference can only be a patient-level rate × 24, as `S_per_day_extrap` computes. *(Confirmed: proposal Table 3.1; script line 126.)*
3. **RO4a places coverage gaps "by time of day" on Icentia11k** (Table 3.4; RO4 slide). That cannot be done on untimed segments unless segments are assigned synthetic clock times. The handoff did not catch this because it had not seen the proposal. *(Confirmed: proposal Table 3.4.)*
4. **The ESVEA threshold in my earlier worked example was not the proposal's.** The proposal currently uses Binici's rate form (≥30/h) for the daily rate: Table 3.3 "ESVEA in rate form (Binici et al., 2010)" and the RO3 slide "≥30 per hour". The 480/day in `new_task.md` was my choice for the example, not taken from the proposal. *(Confirmed: proposal Table 3.3; slide ro3.)*
5. **Larsen is already cited in the proposal, slightly mis-summarised.** Section 3.5 says "PACs are afternoon-weighted (Larsen et al., 2016)". Figure 3 shows the highest block is 18–24 h, then 12–18 h, so "afternoon and evening" is accurate. *(Confirmed: figure image; proposal Section 3.5.)*
6. **Minor arithmetic note:** the handoff's "435" is right only with unrounded shares (see table above).

### Could not verify

- That **no** segment among about 541,794 has clock time: 68 headers were read. The encoder argument rests on `icentia11k_make_wfdb.py`, which is not in the folder. *(Unverified.)*
- The annotation check (400 `.atr` files): its script was not saved. *(Unverified.)*
- That segment numbers are not chronological, the 3- to 14-day recording length, and how the random selection was made. These are the authors' descriptions or the handoff's reading of the encoder. *(Unverified.)*
- I could not rerun any header check: this workspace's proxy blocks PhysioNet and its S3 mirror (HTTP 403).
- Larsen et al. 2016 volume and pages (18(10), 1573–1580): taken from the handoff; the DOI matches the proposal's reference. *(Unverified by me.)*
- The source of the 480/day definition: the proposal attributes "480 or more supraventricular beats per day, or runs of 10 to 29 seconds" to Haeusler et al. (2025). I have not re-read that paper in this check. *(Unverified in this check.)*

---

## Part 2. Resolving the "Still open" items

### Item 4. Equation 3.1: where is retention π̂ estimated?

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

### Item 5. Equation 3.3: how does the coverage gate work?

**What the proposal says (confirmed):** the gate checks only two blocks, "c(d, day) ≥ θ_day and c(d, night) ≥ θ_night", while Equation 3.2 sums over blocks h, which are never defined.

**Problem (inference):** with wₕ = Lₕ/24, every block h needs an observed rate. A day can pass a day/night gate while one 6-hour block has no coverage, which leaves r̂(d,h) undefined. So the claim in my earlier file that "no block's rate is guessed" is wrong under the current gate (the handoff was right to flag it).

**Proposed resolution (decision):**
- **Main estimate:** the gate requires minimum coverage in **every** block: c(d,h) ≥ θ for all h. Then Option A never needs to guess a rate.
- **Sensitivity analysis:** days that pass a day/night gate but leave a block below θ are kept, and thin blocks are filled by Option B (shrinkage towards gₕ). This gives Option B a defined job.
- **Trade-off:** a per-block gate makes "valid day" stricter, which lowers the RO3 primary outcome (proportion with at least 3 valid days). θ is set at device verification, so it can be modest (for example, at least 1 analysable hour per 6-hour block). The alternative is to keep the day/night gate and accept that the main estimate extrapolates within the day/night halves.

### Item 6. How is Icentia11k used as a reference?

**Confirmed:** Icentia11k gives, per patient, PAC count ÷ analysed hours (median 57.5 h; Table 4.3). It cannot be split into days or clock-time blocks.

**Proposed resolution (inference):**
- **RO2:** compare the model's estimate with the reference at **patient level**: pool the model's PAC estimates over all of a patient's segments, divide by analysed hours, × 24, and compare with the annotated rate × 24. The "daily-count MAE" metric becomes a patient-level rate error expressed per day.
- **RO4a:** for coverage gaps, assign each segment to one of the four blocks at random (consistent with the published random selection) and form pseudo-days of 24 h. Gap patterns are then applied by block, and the coverage gate is evaluated on pseudo-days. Reference ESVEA status comes from the patient-level rate.
- Day-to-day estimation and real time-of-day effects are tested only in RO3 (no ground truth) and stated as a limit.

### Item 7. Block definition

**Confirmed:** the proposal never defines blocks. The four 6-hour blocks appear only in my worked example and in the handoff's gₕ.

**Proposed resolution (decision):** four 6-hour blocks, 00–06, 06–12, 12–18 and 18–24 h. Night = 00–06; day = 06–24 (for the sensitivity gate). This matches gₕ as already calculated, so nothing needs recomputing.

### Item 2 (ESVEA threshold): 480/day or ≥30/h?

**Confirmed current state:** the proposal and slides use Binici's rate form, ≥30/h (720/day), for the daily rate (Table 3.3; slide ro3), and quote "66 ESVEA-positive" (Binici rate or run) for RO4a (Section 3.6; Section 4.2; slides ro4 and preliminary-icentia). My `new_task.md` example used 480/day.

**Options (decision):**

| | ≥480 per day (stroke cohorts; Haeusler et al., 2025, per the proposal) | ≥30 per hour (Binici et al., 2010) |
|---|---|---|
| Population | Acute ischaemic stroke (matches RO3) | General population |
| Fits Equation 3.2 output (a daily count) | Directly | Via × 24 (= 720/day) |
| RO4a positives in 298 | 67 | 54 |
| Change needed | Table 3.3, Section 3.6, Section 4.2 text, three slides | None beyond the run caveat below |

**My recommendation:** ≥480 per day as the primary rate criterion, ≥30 per hour as secondary. Report runs separately, because filtering removes 60.9% of PAC coupling intervals (Table 4.2), which breaks runs apart. The 480/day definition source must be re-checked against Haeusler et al. (2025) before submission. If you prefer to keep Binici as primary, only the run caveat and my worked example change.

### Item 1. Do the study's own Garmin recordings carry clock time?

**Unverified.** Equation 3.2 needs τ(d,h), so it is required. The device has not arrived (Section 3.5). **Proposed:** add "timestamps on every interval" to the device verification checklist (Section 3.5, milestone M1).

### Item 3. Value of κ in Option B

**Decision.** Proposed: κ = 1 hour (the same order as a minimum per-block coverage threshold), with a sweep κ ∈ {0.5, 1, 2, 4} h reported. This is a convention, not taken from a source.

### Items 8 to 11 (fixes to `new_task.md`)

- **8. r̄(d):** I agree with the handoff's fix, r̄(d) = Σₕ τ(d,h) r̂(d,h) / Σₕ τ(d,h) gₕ with Σₕ Lₕ gₕ / 24 = 1. If true block rates follow the shape gₕ, this recovers the scale from whichever blocks were observed, and it is defined when some τ(d,h) = 0. The gₕ values sum to 4.01 over four 6-hour blocks, so the normalisation holds to rounding. *(Checked algebraically.)*
- **9.** Included in the Section 3.4 text below.
- **10.** The worked example's 0.40/0.20/0.15/0.25 weights were hypothetical and do not match Figure 3; it is not used in the proposal, so no proposal edit is needed.
- **11.** gₕ now has a provisional cited source (Larsen et al., 2016, Figure 3), included below.

---

## Part 3. Exact edits proposed (not applied)

Edits assume the recommendations above: per-block gate, four 6-hour blocks, ≥480/day primary. Edits marked **[if 480/day]** are dropped if you keep Binici as primary.

### Proposal

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

### Slides

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

## Questions for you before I edit

1. **Pulsewatch:** does your release include accelerometer data and ECG beat timing? (Decides P3 and the Equation 3.1 wording.)
2. **Coverage gate:** per-block gate (recommended) or keep day/night?
3. **Blocks:** four 6-hour blocks, as above?
4. **ESVEA primary:** ≥480/day (recommended) or ≥30/h?
5. **κ:** 1 hour with a sweep, as proposed?
