"""H1 model and the D1 power simulation.

Aggregated form of the H1 model (plan, section 5): for patient j, k_j of n_j PAC coupling intervals are
retained at the threshold, and
    logit P(retained) = a + b * x_j + u_j,   u_j ~ N(0, sigma^2),   x_j = log(PACs per hour).
With one row per patient the random intercept absorbs between-patient overdispersion. The integral over
u_j is done by adaptive Gauss-Hermite quadrature; the fit is maximum likelihood with a Wald 95% CI for b.
H1 is supported if the CI for b excludes 0 (two-sided; direction reported).

Fix of 13 Nov 2026 (approved in the D1 step): the per-patient mode of u is found by a safeguarded
search. The score g(u) = k - n*expit(lin + u) - u/sigma^2 is strictly decreasing in u, so its root is
unique and lies in [sigma^2*(k - n) - 1, sigma^2*k + 1]; a Newton step is accepted only inside the
current bracket, otherwise the bracket is bisected. The earlier undamped Newton search from u = 0
diverged for one P0 patient (97 of 123 retained) just below the optimum, which made the likelihood
jump by about 10,500 and gave a false Wald SE for b. The model and the quadrature are unchanged.
profile_ci_b gives a profile-likelihood CI for b, reported beside the Wald CI.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import optimize, special, stats

_GH_X, _GH_W = np.polynomial.hermite.hermgauss(15)


def _mode(lin, s2, k, n, max_iter: int = 200, tol: float = 1e-12):
    """Mode of u for each patient: the root of g(u) = k - n*expit(lin + u) - u/s2 (strictly decreasing).
    Safeguarded Newton: a Newton step is taken only if it stays inside the bracket [lo, hi] that holds
    the root; otherwise the bracket is bisected. Cannot diverge."""
    lin, k, n = (np.asarray(v, dtype=float) for v in (lin, k, n))
    lo = s2 * (k - n) - 1.0                                 # g(lo) > 0
    hi = s2 * k + 1.0                                       # g(hi) < 0
    u = np.clip(np.zeros_like(lin), lo, hi)
    for _ in range(max_iter):
        p = special.expit(lin + u)
        g1 = k - n * p - u / s2
        lo = np.where(g1 > 0, u, lo)
        hi = np.where(g1 > 0, hi, u)
        g2 = -n * p * (1 - p) - 1 / s2
        newton = u - g1 / g2
        u_new = np.where((newton > lo) & (newton < hi), newton, 0.5 * (lo + hi))
        if np.max(np.abs(u_new - u)) < tol:
            return u_new
        u = u_new
    return u


def _negloglik(theta, k, n, x):
    """Adaptive Gauss-Hermite quadrature: nodes centred on each patient's mode of u, scaled by its
    curvature. Plain quadrature fails here because counts of thousands make the integrand very peaked."""
    a, b, log_s = theta
    s2 = np.exp(2 * log_s)
    lin = a + b * x
    u = _mode(lin, s2, k, n)
    p = special.expit(lin + u)
    sd = 1 / np.sqrt(n * p * (1 - p) + 1 / s2)
    nodes = u[:, None] + np.sqrt(2.0) * sd[:, None] * _GH_X[None, :]
    eta = lin[:, None] + nodes
    g = (k[:, None] * -np.logaddexp(0.0, -eta) + (n - k)[:, None] * -np.logaddexp(0.0, eta)
         - nodes ** 2 / (2 * s2) - 0.5 * np.log(2 * np.pi * s2))
    ll = np.log(np.sqrt(2.0) * sd) + special.logsumexp(g + _GH_X[None, :] ** 2, b=_GH_W[None, :], axis=1)
    const = special.gammaln(n + 1) - special.gammaln(k + 1) - special.gammaln(n - k + 1)
    return -(ll + const).sum()


@dataclass
class Fit:
    a: float
    b: float
    sigma: float
    se_b: float
    ci_b: tuple[float, float]
    p_b: float
    converged: bool


def fit(k, n, x, start=None) -> Fit:
    """Maximum likelihood fit. start: optional (a, b, log sigma); default logit of the pooled rate, 0, log 0.5."""
    k, n, x = (np.asarray(v, dtype=float) for v in (k, n, x))
    if start is None:
        p0 = np.clip(k.sum() / n.sum(), 1e-3, 1 - 1e-3)
        start = np.array([np.log(p0 / (1 - p0)), 0.0, np.log(0.5)])
    res = optimize.minimize(_negloglik, np.asarray(start, dtype=float), args=(k, n, x), method="Nelder-Mead",
                           options={"xatol": 1e-7, "fatol": 1e-7, "maxiter": 4000})
    hess = _numeric_hessian(lambda t: _negloglik(t, k, n, x), res.x)
    cov = np.linalg.pinv(hess)
    se_b = float(np.sqrt(max(cov[1, 1], 0.0)))
    b = float(res.x[1])
    z = stats.norm.ppf(0.975)
    p = float(2 * stats.norm.sf(abs(b / se_b))) if se_b > 0 else np.nan
    return Fit(float(res.x[0]), b, float(np.exp(res.x[2])), se_b, (b - z * se_b, b + z * se_b), p, bool(res.success))


def profile_ci_b(k, n, x, f: Fit | None = None, level: float = 0.95) -> tuple[float, float]:
    """Profile-likelihood CI for b: the b values where twice the rise in the negative log-likelihood,
    re-maximised over a and log sigma, equals the chi-square(1) quantile."""
    k, n, x = (np.asarray(v, dtype=float) for v in (k, n, x))
    f = f or fit(k, n, x)
    crit = stats.chi2.ppf(level, 1)
    best = _negloglik([f.a, f.b, np.log(f.sigma)], k, n, x)
    start = np.array([f.a, np.log(f.sigma)])

    def rise(b):
        r = optimize.minimize(lambda t: _negloglik([t[0], b, t[1]], k, n, x), start, method="Nelder-Mead",
                              options={"xatol": 1e-8, "fatol": 1e-8, "maxiter": 4000})
        return 2 * (r.fun - best) - crit

    ends = []
    for sign in (-1, 1):
        step = max(f.se_b, 1e-3)
        for _ in range(40):
            if rise(f.b + sign * step) > 0:
                break
            step *= 2
        else:
            raise RuntimeError("profile CI bound not found")
        ends.append(optimize.brentq(rise, f.b, f.b + sign * step, xtol=1e-5))
    return float(ends[0]), float(ends[1])


def _numeric_hessian(f, x, h=1e-3):
    x = np.asarray(x, float)
    H = np.zeros((len(x), len(x)))
    for i in range(len(x)):
        for j in range(i, len(x)):
            ei, ej = np.eye(len(x))[i] * h, np.eye(len(x))[j] * h
            H[i, j] = H[j, i] = (f(x + ei + ej) - f(x + ei - ej) - f(x - ei + ej) + f(x - ei - ej)) / (4 * h * h)
    return H


def simulate(n_patients: int, a: float, b: float, sigma: float, x_pool: np.ndarray, n_pool: np.ndarray,
             rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Resample (x, n) pairs from P0 and draw retained counts from the fitted model."""
    idx = rng.integers(0, len(x_pool), n_patients)
    x, n = x_pool[idx], n_pool[idx].astype(int)
    eta = a + b * x + rng.normal(0, sigma, n_patients)
    k = rng.binomial(n, special.expit(eta))
    return k, n, x


def power(sizes, a, b, sigma, x_pool, n_pool, n_sim: int = 1000, alpha: float = 0.05, seed: int = 2026) -> dict:
    """Share of simulations in which the 95% CI for b excludes 0, for each candidate size of P1."""
    rng = np.random.default_rng(seed)
    out = {}
    for m in sizes:
        hits = 0
        for _ in range(n_sim):
            k, n, x = simulate(m, a, b, sigma, x_pool, n_pool, rng)
            f = fit(k, n, x)
            hits += int(f.p_b < alpha)
        out[int(m)] = hits / n_sim
    return out


def smallest_size(power_by_size: dict, target: float = 0.90) -> int | None:
    ok = [m for m, p in sorted(power_by_size.items()) if p >= target]
    return ok[0] if ok else None
