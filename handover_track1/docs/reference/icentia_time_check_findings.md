# Icentia11k clock-time check: findings

Checked 2026-11-02, following `new_task.md`.

**Result: the released Icentia11k segments carry no clock time.** Time-of-day weights (wₕ) can't be estimated from this dataset. The Icentia11k daily count is extrapolated from sampled segments.

## Context and current status

**The question.** Equation 3.2 in the proposal estimates a daily PAC count, R̂(d), by weighting hourly rates from each time-of-day block with weights wₕ. The proposal says wₕ is "estimated from the diurnal PAC profile in Icentia11k", which needs every Icentia11k segment to carry a clock time. `new_task.md` sets out the check and the decision that follows from it.

| Item | Status |
|---|---|
| Do released Icentia11k segments carry clock time? | Answered: no, on every header sampled, in the authors' encoder and in the annotations |
| Main estimate for wₕ | Decided: wₕ = Lₕ/24 (Option A in `new_task.md`) |
| Sensitivity analysis | Decided: shrink thin blocks towards a published profile (Option B). Its definition of r̄(d) still needs fixing |
| Source of gₕ | Provisional: Larsen et al. 2016 Figure 3, with values read by eye |
| Proposal and slides | Not edited: the files haven't been supplied |

Everything that could not be confirmed is listed in the last section, "Still missing or unconfirmed".

## Step 3 output

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

## Step 6: official description

PhysioNet, Data Description (https://physionet.org/content/icentia11k-continuous-ecg/1.0/). The CinC 2021 paper uses almost the same words:

> From this, we randomly select 50 of the segments and their respective labels from the list of segments. The goal here is to reduce the size of the dataset while maintaining a fair representation of each patient.

Neither the page nor the paper says whether timestamps were kept or removed, and neither uses the word "contiguous".

## Supporting evidence

| Check | Result |
|---|---|
| Wider sample, `check_icentia_time_wide.py` (seed 2026): one random segment from each of 60 random patients | 59 read, and every record line has only 4 fields (name, signals, rate, samples), with no comment lines. The other one was p08975_s36, HTTP 404: `RECORDS` for that patient lists only 20 segments (s00-s19) |
| Raw header, p00000_s00 | `p00000_s00 1 250 1048577`, then a signal line |
| Authors' encoder, `icentia11k_make_wfdb.py` (shawntan/icentia-ecg) | `wrsamp` and `wrann` are called without `base_time` or `base_date` |
| Annotations: 400 random files from `icentia_atr/` (one-off check, script not saved) | `aux_note` holds only rhythm labels: `(N`, `(AFIB`, `(AFL`, `)`, `(N)`, `(AFIB)`, plus `None` |

## Step 5: contiguity

This can't be tested because there are no timestamps. The random selection means a patient's segments are a sample of the recording, not one continuous stretch. Some selected segments could still happen to be adjacent, and the data can't show which.

## Limits

- This describes the released files. It doesn't show whether Icentia's source data has timestamps.
- Nothing states that segment numbers follow time order. The encoder numbers them in the order they appear in the source file, so s00, s01 and so on shouldn't be treated as chronological.
- Not every patient has 50 segments (p08975 has 20), so hours per patient vary.

## What this means for the proposal

Not yet applied, because the proposal and slides aren't on this machine.

- **Equation 3.2:** decided in `new_task.md`. The main estimate uses wₕ = Lₕ/24 (Option A). The sensitivity analysis shrinks thin blocks towards a published profile (Option B), because the "no clock time" row of its decision table applies. The provisional source for gₕ is Larsen et al. 2016 Figure 3 (see "gₕ from Larsen Figure 3").
- **Section 3.2:** describe up to 50 randomly selected segments of about 70 minutes per patient, from 3-14 day recordings, with no clock time.
- **Section 3.4:** state that the Icentia11k daily count is extrapolated from non-contiguous segments, and that Icentia11k can't place coverage gaps by time of day. `S_per_day_extrap` in `incentia_ro1_prelim.py` is already computed as S per hour × 24.
- **Slides:** apply the same wording.

## Review of the decision section in `new_task.md`

Confirmed:
- The worked example: Option A gives 432 PACs/day; profile weights give 501.6, rounded to 502.
- The 39% and 91% retention figures in the closing note: at the 20% threshold, `results/tableA_removed_by_class.csv` shows 60.9% of PAC coupling intervals and 8.8% of normal intervals removed.

Open points:
1. **Replacement text:** it leaves out what Step 4 requires, namely that the Icentia11k daily count is extrapolated and that the dataset can't place coverage gaps by time of day.
2. **"No clock time in Icentia11k":** this holds for the weights only. Without clock time, Icentia11k segments can't be assigned to a day d or a block h, so R̂(d), τ(d,h), r̂(d,h) and any h-dependence in π̂(m,h) can't be computed from it. Its reference is a patient-level rate × 24, as in `S_per_day_extrap`. Where π̂ is estimated needs checking against Equation 3.1, and how Icentia11k is compared with the R̂(d) daily count needs stating.
3. **Option B definition of r̄(d):** a duration-weighted mean needs a rate in every block, so it's undefined when τ(d,h) = 0, and it includes the thin blocks being corrected. Suggested: r̄(d) = Σₕ τ(d,h) r̂(d,h) / Σₕ τ(d,h) gₕ, with gₕ normalised so that Σₕ Lₕ gₕ / 24 = 1. If the true rates follow the profile shape, this recovers their scale regardless of which blocks were observed.
4. **"No block's rate is guessed":** this overstates the gate. A block that passes is still extrapolated from its observed part. Option B also only has work to do if thin blocks can pass the gate. Check against Equation 3.3.

## Literature search for gₕ (2026-11-02)

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

### gₕ from Larsen Figure 3

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

### Limits to state in the proposal

- Source of the values: they were read by eye from a figure, and they are medians rather than the mean rates that gₕ ideally represents. The authors chose not to report means [1].
- Who it represents: 66 community participants with ≥30 PACs/h (≥720/day), and none of them are in your 480–720/day range. In the full cohort, which was mostly people with fewer PACs, no pattern was visible [1].
- Precision: a 3 PACs/h reading error across a whole block moves gₕ by about 0.04 at most. Sampling noise is probably larger, as neighbouring hours jump from 118 to 73.
- Text versus figure: the paper's conclusion says PACs fall during the evening, but Figure 3 keeps them high until 23–00. Cite the figure for this.

### Suggested wording for the proposal

> In a sensitivity analysis, rates in thinly observed blocks are shrunk towards a published diurnal profile. Relative block rates (gₕ = 0.87, 0.63, 1.11 and 1.40 for 00–06, 06–12, 12–18 and 18–24) were derived from values read from the published figure of median hourly PAC counts in participants with frequent PACs in the Copenhagen Holter Study (n = 66; Larsen et al., 2016). The number of participants whose ESVEA class changes is reported.

[1] Larsen BS, Kumarathurai P, Nielsen OW, Sajadieh A. The circadian variation of premature atrial contractions. Europace. 2016;18(10):1573–1580. https://doi.org/10.1093/europace/euv389

## Still missing or unconfirmed

### Needs the proposal or slides (not seen)

Everything below comes from the excerpts in `new_task.md`. The proposal itself hasn't been read.

| Item | Why it matters |
|---|---|
| Equation 3.1, and where π̂(m,h) is estimated | If π̂ depends on block h and is estimated from Icentia11k, it can't be computed without clock time |
| Equation 3.3, the coverage gate | Decides whether "no block's rate is guessed" holds, and whether thin blocks can reach Option B at all |
| How Icentia11k is used as a reference, including RO2 and RO4a | R̂(d) is a per-day, per-block count, while Icentia11k gives only a patient-level rate × 24. The comparison needs to be stated |
| The block definition | gₕ above assumes four 6-hour blocks, which appear only in the worked example. Other blocks mean recalculating gₕ from the hourly readings |
| Which ESVEA threshold the proposal uses | See "ESVEA threshold" below |
| Current wording of Sections 3.2, 3.4 and 4.2, and the slides | Needed to make the edits. The 39% and 91% figures were checked against `results/`, not against Section 4.2 |

### Needs an answer from you

- **Clock time in the study's own recordings:** inferred from τ(d,h) in Equation 3.2, not confirmed. Without it, gₕ can't be checked against the study's own data.
- **κ in Option B:** no value has been proposed, and the sensitivity analysis can't run without one.
- **Option B's r̄(d):** the suggested fix in "Review of the decision section" hasn't been accepted or applied.
- **Worked example:** its weights aren't yet labelled as hypothetical in `new_task.md`.

### ESVEA threshold

- `new_task.md` and the worked example classify at 480 PACs/day. `incentia_ro1_prelim.py` also tests ≥30 S/h and uses 30/h, not 480/day, in `esvea_any`.
- These differ: 30/h × 24 = 720/day, which is the equivalence Larsen uses. In `results/tableB_esvea_prevalence.csv`, 67 patients meet ≥480/day and 54 meet ≥30/h.
- The source for the 480/day cut-off wasn't checked in this work. The script's docstring attributes it to Binici et al. 2010, but that paper wasn't read.

### Icentia11k

| Not confirmed | What was actually checked |
|---|---|
| That no segment in the dataset has a clock time | 68 headers read (9 + 59) out of about 541,794 segments. The encoder supports the result for all of them, assuming it is the script that produced the released files |
| Whether Icentia's source data has timestamps | Neither the description nor the paper says. The step that produced the encoder's input files wasn't available. Only the authors could answer this |
| Whether segment numbers follow time order | Not stated anywhere |
| Whether random selection was even across day and night | Only "randomly select" is stated. No method is given, and it can't be tested without clock time |
| Annotation check across all files | 400 of the 14,758 local `.atr` files, by a one-off check whose script wasn't saved |

The 3-14 day recording length and the sampling statement are the authors' descriptions and weren't independently verified.

### gₕ and the literature

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

### Not done

- Sections 3.2 and 3.4 of the proposal, Equation 3.2 and the slides haven't been edited.
- `new_task.md` still has the "must come from a published 24-hour Holter study" row with its source marked "to be chosen and cited", and none of the open points above have been applied to it.
