# Kappa simulation: choosing the shrinkage strength for the sensitivity analysis

**Purpose.** Test whether the Option B sensitivity analysis (thin 6-hour blocks shrunk towards a published diurnal profile, proposal Section 3.4) depends on the shrinkage strength κ, using simulated data built to behave like the future RO3 Garmin cohort. This chooses and justifies κ before the real data exist. It does **not** confirm κ for real Garmin data; that needs the RO3 masking check.

**Files**
| File | Content |
|---|---|
| `kappa_sim.py` | The simulator (Python; numpy, pandas, scipy). Run `python kappa_sim.py`; about 1 minute |
| `calibration.csv` | Simulated values against each published target |
| `kappa_results.csv` | Estimator performance for every scenario and κ |
| `run_output.txt` | Console output of the run reported here (seed 2026) |

No dataset is downloaded. The only Icentia11k inputs are summary numbers from the candidate's own RO1 run.

---

## 1. How the data are generated

Each simulated participant has 7 days × four 6-hour blocks (00–06, 06–12, 12–18, 18–24 h).

| # | Layer | Model | Numbers and source |
|---|---|---|---|
| 1 | PAC burden | Log-normal rate per participant | Spread from Icentia11k IQR 0.23 to 13.38 PACs/h (proposal Table 4.3); level calibrated so 25.3% have a true 7-day mean ≥480/day (Haeusler et al., 2025) |
| 2 | Time-of-day pattern | Larsen shape × individual deviation | Shape 0.87, 0.63, 1.11, 1.40 (Larsen et al., 2016, Figure 3, read by eye); individual deviation **unknown, swept** (log SD 0.2 or 0.5) |
| 3 | Day-to-day variation | Log-normal day factor with day-to-day persistence (AR(1)) | SD and persistence **calibrated** so one day and seven days detect high PAC frequency with 76.6% and 88.8% sensitivity against a 14-day reference (Måneheim et al., 2024) |
| 4 | PACs per block | Poisson, or clustered (negative binomial) | Clustering **unknown, swept** (none, or gamma shape 2) |
| 5 | Wear | Daily wear probability falling over time, with between-participant variation | 73% falling to 63% over 30 days (Ding et al., 2023); between-participant SD 1.0 on the logit scale (assumed) |
| 6 | Blocks worn on a worn day | Each block worn with a fixed probability | **Unknown, swept**: 0.95 ("typical") or 0.75 ("poor") |
| 7 | Charging | One hour removed from 06–12 each worn day | Protocol: one short daily charging window (Table 3.3); placement assumed |
| 8 | Usable signal | Beta-distributed usable fraction per block | 94% at night, 64% in the day, averaging 71.5% over 24 h (Merschel & Reinhardt, 2022) |
| 9 | Beat loss | Each PAC in usable time kept with probability 0.391 | PAC coupling intervals kept at the 20% filter: 100 − 60.9% (proposal Table 4.2) |

**Estimators (as planned in the proposal):**
- **Main (Option A):** Equation 3.2 with wₕ = 6/24, using only days where every block has ≥1 usable hour (Equation 3.3).
- **Option B, κ = 0.5, 1, 2, 4 h:** days meeting the day/night rule (≥2 h at night, ≥6 h in the day; assumed thresholds), with every block shrunk towards the profile: r̃ = (τ r̂ + κ gₕ r̄) / (τ + κ), r̄ = Σₕ τ r̂ / Σₕ τ gₕ.
- Each participant's estimate is the mean daily count over the days used; ESVEA if ≥480. Truth is the participant's true mean daily count over all 7 days.

**Deliberate simplifications:** retention (0.391) and PAC identification are treated as known exactly, so the simulation isolates coverage and κ. Real estimates will have additional error from both.

---

## 2. Calibration: does the simulator reproduce the published figures?

| Target | Source | Simulated (range across 8 scenarios) |
|---|---|---|
| 1-day sensitivity 76.6% | Måneheim et al. (2024) | 76.0 to 77.7% |
| 7-day sensitivity 88.8% | Måneheim et al. (2024) | 88.3 to 89.4% |
| ESVEA 25.3% | Haeusler et al. (2025) | 24.7 to 25.1% |
| Day-1 wear 73% | Ding et al. (2023) | 71.6 to 74.2% |
| Usable 71.5% over 24 h | Merschel & Reinhardt (2022) | 71.4 to 71.6% |
| Usable 94% at night | Merschel & Reinhardt (2022) | 93.9 to 94.2% |

All targets are reproduced within about 1.5 percentage points. Calibrated day-to-day variation is large (log SD 1.2 to 1.4) with strong persistence (0.8 to 0.9), which is what is needed to reproduce both Måneheim figures together.

---

## 3. Results

### κ makes almost no difference

| Coverage | Misclassified (Option B, all κ) | Median relative error (all κ) | Participants changing ESVEA class vs main estimate |
|---|---|---|---|
| Typical (blocks worn 95%) | 1.6 to 2.0% | 8.1 to 8.7% | **0.7 to 1.1%** |
| Poor (blocks worn 75%) | 3.1 to 3.7% | 14.5 to 15.5% | **2.5 to 3.0%** |

Within any one scenario, moving κ from 0.5 to 4 h changes misclassification by at most 0.2 percentage points and the median error by at most 0.4 points. Class changes stay well under the 10% robustness limit in every scenario.

**Conclusion: κ = 1 h, with 0.5 to 4 h reported, is supported. The sensitivity analysis is robust to κ.**

### A second finding: the per-block rule has a cost when coverage is poor

| Coverage | Main estimate computable | Main estimate median error | Option B computable | Option B median error | ≥3 per-block valid days | ≥3 day/night valid days |
|---|---|---|---|---|---|---|
| Typical | 98.4 to 98.9% | 9.7 to 10.4% | about 99% | 8.1 to 8.7% | 82 to 84% | 88 to 89% |
| Poor | 80.5 to 82.0% | 19.4 to 21.2% | about 95% | 14.5 to 15.5% | **20 to 21%** | 58 to 61% |

- With typical coverage, the main estimate and Option B are close.
- With poor coverage, the per-block rule discards many days. The main estimate then becomes **less** accurate than Option B, because large day-to-day variation makes using more days worth more than avoiding thin blocks. Only about one participant in five would have 3 per-block-valid days.

**What this means:** keep the per-block rule as the main estimate (it adds no outside assumption), but state that if device verification shows poor block coverage, Option B is the more informative estimate. This is a point to raise with your supervisors, not a change to make now.

---

### A third estimator: pooling each block across the participant's own days

For each block, total corrected PACs ÷ total usable hours across all day/night-valid days (minimum 1 usable hour per block across the week), then daily count = Σₕ 6 × block rate. It uses no outside profile.

| Coverage | Estimator | Computable | Misclassified | Median relative error |
|---|---|---|---|---|
| Typical | Main (per-block days) | 98.4 to 98.9% | 2.1 to 2.5% | 9.7 to 10.4% |
| Typical | Option B, κ = 1 h | 98.9 to 99.2% | 1.6 to 2.0% | 8.1 to 8.6% |
| Typical | **Pooled by block** | 98.5 to 98.9% | 1.8 to 2.1% | 8.4 to 8.8% |
| Poor | Main (per-block days) | 80.5 to 82.0% | 4.2 to 4.4% | 19.4 to 21.2% |
| Poor | Option B, κ = 1 h | 95.4 to 95.9% | 3.1 to 3.7% | 14.6 to 15.4% |
| Poor | **Pooled by block** | 87.1 to 88.3% | 2.7 to 3.3% | 13.9 to 15.1% |

Pooling matches Option B's accuracy without borrowing the Larsen profile, and is clearly better than the per-block-day estimate when coverage is poor. It is the recommended participant-level estimate; per-day values (per-block rule) remain for day-to-day stability, and Option B remains the sensitivity analysis.

## 4. Limits

- Every unknown is swept over two values only (individual shape, clustering, coverage). Other values are untested.
- The Måneheim target assumes their "high PAC frequency" corresponds to ≥480/day against a 14-day reference; their threshold and reference were not re-checked.
- The Larsen profile is used both to generate the data and in Option B. If real diurnal patterns differ more than the swept individual deviation, Option B would do worse than shown.
- Retention and PAC identification are perfect here. RO2 errors are not simulated.
- Thresholds for the day/night rule (2 h night, 6 h day) are assumed; the per-block minimum (1 h) is the proposed value, to be set at device verification.

---

## 5. Suggested text for the proposal (Section 3.4, after the sensitivity sentence)

> The shrinkage strength κ is set at 1 hour, with 0.5, 2 and 4 hours also reported. In a pre-specified simulation calibrated to published wear, signal-quality and ectopy data (Ding et al., 2023; Haeusler et al., 2025; Måneheim et al., 2024; Merschel & Reinhardt, 2022), varying κ across this range changed ESVEA class in at most 3% of simulated participants. κ is checked in the RO3 data by masking blocks on fully covered days.

About 75 words.
