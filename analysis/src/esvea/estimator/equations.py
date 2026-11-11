"""Equations 3.1 to 3.4 and the coverage rules, outside the network (section 3.4).

This module is the single implementation of coverage, the valid-day rule and the per-block gate. The
Garmin pipeline in Track 2 (R3) must import it rather than re-implement it (meeting point 1).

Inputs per beat: day d, block h (0..3 for 00-06, 06-12, 12-18, 18-24), calibrated PAC probability p_i,
retention pi_hat(m_i). Inputs per day and block: observed (analysable) hours tau(d, h).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from ..config import BLOCK_HOURS, ESVEA_PRIMARY_PER_DAY, LARSEN_PROFILE, N_BLOCKS


@dataclass(frozen=True)
class CoverageRule:
    """Thresholds are fixed at device verification (M1). Defaults are the assumed values used in the
    Appendix C simulation and the proposed per-block minimum; replace them from the R2 report."""
    night_blocks: tuple[int, ...] = (0,)
    day_blocks: tuple[int, ...] = (1, 2, 3)
    min_night_hours: float = 2.0
    min_day_hours: float = 6.0
    theta_block: float = 1.0            # Equation 3.3, proposed about 1 h
    pooled_min_block_hours: float = 1.0  # Equation 3.4: at least 1 analysable hour per block across the week


def block_sums(beats: pd.DataFrame) -> pd.DataFrame:
    """S(d, h) = sum of p_i / pi_hat(m_i) over reported beats (numerator of Equations 3.2 and 3.4)."""
    w = beats["p"].to_numpy() / beats["pi_hat"].to_numpy()
    return (beats.assign(w=w).groupby(["day", "block"])["w"].sum()
            .unstack(fill_value=0.0).reindex(columns=range(N_BLOCKS), fill_value=0.0))


def daily_rate(S: pd.DataFrame, tau: pd.DataFrame) -> pd.Series:
    """Equation 3.2: R_hat(d) per hour; NaN where any block has tau = 0."""
    L = BLOCK_HOURS
    with np.errstate(divide="ignore", invalid="ignore"):
        r = (S / tau.replace(0, np.nan))
    return (L / 24.0 * r).sum(axis=1, min_count=N_BLOCKS)


def gate(tau: pd.DataFrame, rule: CoverageRule = CoverageRule()) -> pd.Series:
    """Equation 3.3: a daily value is reported only if every block meets theta_block."""
    return (tau >= rule.theta_block).all(axis=1)


def valid_days(tau: pd.DataFrame, rule: CoverageRule = CoverageRule()) -> pd.Series:
    """Valid day: minimum coverage in both a night block and the day blocks (assumed thresholds)."""
    night = tau[list(rule.night_blocks)].sum(axis=1) >= rule.min_night_hours
    day = tau[list(rule.day_blocks)].sum(axis=1) >= rule.min_day_hours
    return night & day


def pooled_rate(S: pd.DataFrame, tau: pd.DataFrame, rule: CoverageRule = CoverageRule()) -> float:
    """Equation 3.4: R_bar per hour over valid days; NaN if any block has < 1 h across those days."""
    v = valid_days(tau, rule)
    s_h, t_h = S[v].sum(axis=0), tau[v].sum(axis=0)
    if (t_h < rule.pooled_min_block_hours).any():
        return float("nan")
    return float((BLOCK_HOURS / 24.0 * s_h / t_h).sum())


def shrunk_pooled_rate(S: pd.DataFrame, tau: pd.DataFrame, lam: float = 1.0,
                       profile=LARSEN_PROFILE, rule: CoverageRule = CoverageRule()) -> float:
    """Sensitivity analysis: block rates shrunk towards the diurnal profile with strength lambda (hours).
    r_tilde_h = (tau_h r_h + lam g_h r_bar) / (tau_h + lam), r_bar = sum tau_h r_h / sum tau_h g_h."""
    v = valid_days(tau, rule)
    s_h, t_h = S[v].sum(axis=0).to_numpy(), tau[v].sum(axis=0).to_numpy()
    g = np.asarray(profile, float)
    if t_h.sum() == 0:
        return float("nan")
    r_bar = s_h.sum() / (t_h * g).sum()
    r_tilde = (s_h + lam * g * r_bar) / (t_h + lam)
    return float((BLOCK_HOURS / 24.0 * r_tilde).sum())


def esvea_call(rate_per_hour: float, cutoff_per_day: float = ESVEA_PRIMARY_PER_DAY) -> bool | None:
    if not np.isfinite(rate_per_hour):
        return None
    return bool(24.0 * rate_per_hour >= cutoff_per_day)
