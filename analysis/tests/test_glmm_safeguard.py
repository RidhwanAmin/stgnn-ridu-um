"""Regression tests for the safeguarded mode search in glmm (D1 fix, 13 Nov 2026)."""
from functools import lru_cache

import numpy as np
from scipy import special

from esvea.ro1 import glmm


@lru_cache(maxsize=None)
def p0_like():
    """275 patients shaped like the P0 D1 data (heavy-tailed interval counts, log PACs/h spread about 2.7),
    plus a patient like p01525 (97 of 123 retained) placed at an extreme linear predictor."""
    rng = np.random.default_rng(13)
    x = rng.normal(1.0, 2.7, 274)
    n = np.round(np.exp(rng.uniform(0, np.log(60000), 274))).astype(int)
    k, n, x = glmm.simulate(274, -1.9, 0.12, 1.27, x, n, rng)
    return (np.append(k, 97).astype(float), np.append(n, 123).astype(float), np.append(x, -6.0))


def test_mode_solves_score_at_extremes():
    for s2 in (0.05, 1.6, 25.0):
        for lin in np.linspace(-15, 15, 31):
            for k, n in ((97, 123), (0, 500), (500, 500), (1, 1), (51815, 62857)):
                u = glmm._mode(np.array([lin]), s2, np.array([k]), np.array([n]))
                g = k - n * special.expit(lin + u) - u / s2
                assert np.all(np.isfinite(u))
                assert abs(g[0]) < 1e-6 * max(1.0, n)


def test_likelihood_continuous_at_optimum():
    k, n, x = p0_like()
    f = glmm.fit(k, n, x)
    th = np.array([f.a, f.b, np.log(f.sigma)])
    base = glmm._negloglik(th, k, n, x)
    for i in range(3):
        for h in (1e-6, 1e-4):
            e = np.eye(3)[i] * h
            up, down = glmm._negloglik(th + e, k, n, x) - base, glmm._negloglik(th - e, k, n, x) - base
            assert -1e-6 < up < 1.0 and -1e-6 < down < 1.0      # no jump on either side
            assert abs(up - down) < 0.05 * max(abs(up), 1e-6) + 1e-6 or max(up, down) < 1e-6


def test_wald_se_agrees_with_profile():
    k, n, x = p0_like()
    f = glmm.fit(k, n, x)
    lo, hi = glmm.profile_ci_b(k, n, x, f)
    assert lo < f.b < hi
    assert 0.7 < (f.ci_b[1] - f.ci_b[0]) / (hi - lo) < 1.3
    assert f.se_b > 0.005                                    # the bug gave about 0.00002


def test_handles_k_zero_and_k_equal_n():
    rng = np.random.default_rng(4)
    x = rng.normal(0, 1.5, 120)
    n = rng.integers(1, 3000, 120)
    k, n, x = glmm.simulate(120, 0.0, 0.3, 1.0, x, n, rng)
    k[:5], k[5:10] = 0, n[5:10]
    f = glmm.fit(k, n, x)
    assert f.converged and np.isfinite([f.a, f.b, f.sigma, f.se_b]).all()
    assert np.isfinite(glmm._negloglik([f.a, f.b, np.log(f.sigma)], k, n, x))


def test_same_optimum_from_three_starts():
    k, n, x = p0_like()
    fits = [glmm.fit(k, n, x, start=s) for s in (None, [0.5, -0.3, np.log(3.0)], [-4.0, 0.5, np.log(0.2)])]
    nll = [glmm._negloglik([f.a, f.b, np.log(f.sigma)], k, n, x) for f in fits]
    assert max(f.b for f in fits) - min(f.b for f in fits) < 2e-3
    assert max(nll) - min(nll) < 1e-3


def test_false_positive_rate_at_null():
    k0, n0, x0 = p0_like()
    rng = np.random.default_rng(7)
    rej = sum(glmm.fit(*glmm.simulate(100, -1.9, 0.0, 1.27, x0, n0, rng)).p_b < 0.05 for _ in range(200))
    assert 0.02 <= rej / 200 <= 0.09                          # nominal 0.05; the bug gave 0.58
