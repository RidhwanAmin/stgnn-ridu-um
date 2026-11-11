import numpy as np

from esvea.ro1 import glmm


def test_recovers_slope():
    rng = np.random.default_rng(1)
    x = rng.normal(0, 1.5, 400)
    n = rng.integers(50, 3000, 400)
    k, n, x = glmm.simulate(400, 0.3, 0.25, 0.6, x, n, rng)
    f = glmm.fit(k, n, x)
    assert f.converged
    assert f.ci_b[0] < 0.25 < f.ci_b[1]
    assert abs(f.sigma - 0.6) < 0.15


def test_null_slope_rarely_significant():
    rng = np.random.default_rng(2)
    xs, ns = rng.normal(0, 1.5, 300), rng.integers(50, 2000, 300)
    hits = sum(glmm.fit(*glmm.simulate(150, 0.0, 0.0, 0.5, xs, ns, rng)).p_b < 0.05 for _ in range(40))
    assert hits <= 6
