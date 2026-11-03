# Check: κ = 1 hour, with a range tested

**Short answer:** κ cannot be confirmed by looking it up, because no paper reports it. It is a tuning constant in our own sensitivity analysis. There is enough information now to **pre-specify** it (κ = 1 h, sweep 0.5 to 4 h) and justify that choice in the proposal. It can only be **checked against data** once the RO3 Garmin recordings exist. Nothing needs to be confirmed before submission.

---

## 1. What κ does

In the sensitivity analysis (Option B), the rate in a thinly covered 6-hour block is pulled towards the published diurnal profile:

$$
\tilde r(d,h) = \frac{\tau(d,h)\,\hat r(d,h) + \kappa\, g_h\, \bar r(d)}{\tau(d,h) + \kappa}
$$

- τ(d,h): hours of usable data in block h on day d
- r̂(d,h): the observed rate in that block
- gₕ · r̄(d): the rate the Larsen et al. (2016) profile predicts for that block, scaled to the day
- **κ: how many hours of "virtual" observation the profile is worth**

The profile's share of the final block rate is κ / (τ + κ):

| Observed hours in the block (τ) | κ = 0.5 h | **κ = 1 h** | κ = 2 h | κ = 4 h |
|---|---|---|---|---|
| 0.5 | 50% | **67%** | 80% | 89% |
| 1 | 33% | **50%** | 67% | 80% |
| 2 | 20% | **33%** | 50% | 67% |
| 3 | 14% | **25%** | 40% | 57% |
| 6 (full block) | 8% | **14%** | 25% | 40% |

## 2. Why κ = 1 hour as the central value

1. **It ties to the per-block minimum.** If θ_block (set at device verification) is about 1 hour, a block exactly at the minimum is weighted half data, half profile. Blocks below the minimum lean on the profile; blocks well above it are mostly data.
2. **It respects how weak the profile is.** gₕ comes from medians read by eye from one figure, in 66 community participants with ≥30 PACs/h (Larsen et al., 2016, Figure 3). A small κ stops that uncertain shape from dominating well-observed blocks.
3. **It matches the sampling noise.** At the Icentia11k median of 1.35 PACs per hour (proposal Table 4.3), one observed hour holds about one PAC, so a block with under an hour of data says little on its own. That is where the profile should matter most, and κ = 1 h does exactly that.
4. **The range brackets plausible choices.** 0.5 h (data-led) to 4 h (profile-led) covers both extremes, so if ESVEA classes barely change across the sweep, the result does not depend on κ.

These are reasons for a convention, not evidence from a source. Say so in the proposal.

## 3. What to pre-specify in the protocol

| Item | Value |
|---|---|
| Central κ | 1 hour |
| Sweep | 0.5, 1, 2 and 4 hours |
| Reported for each κ | Number and percentage of participants whose ESVEA class (≥480/day) changes against the main estimate; median absolute change in daily count |
| Robustness rule | Conclusions are called robust if class changes stay under a stated limit (for example under 10% of participants) across the whole sweep |

## 4. How to check κ against data later (RO3, after the cohort)

These need the Garmin recordings, so they are planned analyses, not pre-submission tasks.

**Check A: masking test (recommended).**
1. Take days on which **every** 6-hour block is well covered (for example at least 4 hours each).
2. For each such day, artificially cut one block down to 0.5 h, 1 h or 2 h of data, chosen at random.
3. Re-estimate the daily count with each κ in the sweep.
4. Compare with the count from the full, unmasked day.
5. The κ with the smallest error is the data-supported value. Report it beside the pre-specified κ = 1 h.

**Check B: method of moments (optional, more statistical).**
In a gamma–Poisson model, κ equals the profile-predicted block rate divided by the between-day variance of the true block rate. On fully covered days, estimate:
- the mean block rate, from the counts
- the between-day variance, as the total variance of block rates minus the Poisson part (rate ÷ hours)

Then κ ≈ mean ÷ between-day variance. If it is far from 1 h, report the estimated value as an extra sensitivity setting.

## 5. Text to add to the proposal (Section 3.4, after the sensitivity sentence)

> The shrinkage strength κ is set at 1 hour, so a block observed for 1 hour is weighted equally between its own rate and the profile; results are reported for κ of 0.5, 1, 2 and 4 hours, and κ is checked in the RO3 data by masking blocks on fully covered days.

About 50 words. This sentence is added only if Option B (the sensitivity analysis) goes into Section 3.4, which waits on the Pulsewatch check and your approval of Equations 3.1 and 3.2.

## 6. What you need to do now

Nothing to look up. Decide only:
1. **Accept κ = 1 h and the 0.5 to 4 h sweep?** (Recommended.)
2. **The robustness limit:** what share of participants changing ESVEA class would you treat as "not robust"? 10% is a reasonable default; your supervisors may prefer another.
