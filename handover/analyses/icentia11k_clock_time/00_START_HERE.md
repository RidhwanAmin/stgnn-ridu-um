# Icentia11k clock-time check: start here

Handoff for confirming the answer to `core/new_task.md`. Prepared 2026-11-02 from the `icentia-verification` project.

**To the reader:** treat "confirmed" below as checked against the listed file or source, and everything under "Still open" as unverified. The proposal and slides are not in this folder and have not been read or edited.

## The answer

**The released Icentia11k segments carry no clock time.** The "no clock time" row of Step 4 applies, so:

1. wₕ can't be "estimated from the diurnal PAC profile in Icentia11k", as Equation 3.2 currently says.
2. wₕ becomes block length ÷ 24 in the main estimate (Option A).
3. The proposal must say the Icentia11k daily count is extrapolated from non-contiguous segments, and that Icentia11k can't place coverage gaps by time of day.
4. The sensitivity profile gₕ has to come from outside Icentia11k. The provisional source is Larsen et al. 2016, Figure 3.

## Answers to each step in `new_task.md`

| Step | Result | Evidence |
|---|---|---|
| 1. wfdb installed | Yes, version 4.3.1 | Run in the project environment; no file |
| 2. Create the script | Done, code as given in the task | `evidence/check_icentia_time.py` |
| 3. Run it | 9 of 9 segments read | `evidence/check_icentia_time_output.txt` |
| 4. Read the output | `date: None`, `time: None`, 250 Hz, 69.9 min, `comments: []` on all 9, so no clock time and about 70-min segments | `evidence/check_icentia_time_output.txt` |
| 5. Contiguity | Can't be run because there are no timestamps. The published random selection means segments are a sample of each recording | `core/icentia_time_check_findings.md`, "Step 5: contiguity" |
| 6. Official description | "we randomly select 50 of the segments". It doesn't say whether timestamps were kept or removed | `core/icentia_time_check_findings.md`, "Step 6: official description" |
| 7. Update the proposal | **Not done:** the proposal and slides haven't been supplied | See "Still open" |

## Supporting evidence for "no clock time"

- **Wider sample:** 59 of 60 randomly chosen headers were read, and none has a time field or comment line. The other was a 404 because p08975 has only 20 segments (`evidence/check_icentia_time_wide_output.txt`).
- **Authors' encoder:** `icentia11k_make_wfdb.py` (github.com/shawntan/icentia-ecg, `physionet/`) writes no `base_time` or `base_date`. It isn't copied here.
- **Annotations:** 400 of the 14,758 local `.atr` files hold only rhythm labels in `aux_note`. This was a one-off check, and its script wasn't saved.

## Decision on Equation 3.2

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

## Confirmed numbers

| Claim | Result | File |
|---|---|---|
| Worked example | Option A gives 432 PACs/day; profile weights give 501.6, rounded to 502 | Recalculated from `core/new_task.md` |
| PAC retention 39%, normal 91% | 60.9% and 8.8% removed at the 20% threshold | `core/tableA_removed_by_class.csv` |
| Same rates with Figure 3 shares as weights | 435 PACs/day, so the 502 depends on the example's hypothetical weights | `core/icentia_time_check_findings.md`, "gₕ from Larsen Figure 3" |
| ESVEA counts | 67 patients at ≥480/day, 54 at ≥30/h, out of 298 | `core/tableB_esvea_prevalence.csv` |

## Still open

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

## Where to find things

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

## Notes on the files

- **Paths:** these are copies. `core/icentia_time_check_findings.md` still uses the original project paths, so `results/<name>` there means the file of that name in `core/` or `evidence/` here.
- **Spelling:** the script's real name is `incentia_ro1_prelim.py`, although `new_task.md` writes `icentia_ro1_prelim.py`. It's the same script.
- **Rerunning:** the check scripts need Python with `wfdb` and internet access. `incentia_ro1_prelim.py` needs the annotation files, which aren't included, or it can stream them slowly from PhysioNet.
- **Not included:** the proposal, the slides and the Larsen PDF.
