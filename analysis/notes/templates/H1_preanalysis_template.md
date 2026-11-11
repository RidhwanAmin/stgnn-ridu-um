# H1 pre-analysis note (copy to notes/<YYYY-MM-DD>_H1_preanalysis.md and commit BEFORE running s07_h1.py)

- Data: P1 (n = __, seed __, SHA-256 __), drawn on __ after the D1 note of __.
- Unit: patient. Outcome: retained / tallied PAC coupling intervals at the 20% percent-deviation threshold.
- Predictor: x = log(PACs per analysed hour). Patients with no PAC are excluded (count reported).
- Model: logit P(retained) = a + b x + u_j, u_j ~ N(0, sigma^2); ML with adaptive Gauss-Hermite quadrature.
- Test: two-sided Wald test of b = 0 at alpha 0.05; report b, 95% CI, odds ratio per doubling of PAC rate.
- H1 supported if the 95% CI for b excludes 0. Direction reported (section 4.2 suggests b > 0).
- Sensitivity (not confirmatory): thresholds 10, 15, 25, 30%; AF stretches excluded; adaptive filter.
- Deviations from this note will be reported as such.
