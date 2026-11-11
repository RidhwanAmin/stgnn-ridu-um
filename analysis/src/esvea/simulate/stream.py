"""Turn a clean Icentia11k segment into a watch-like beat stream for RO2 training (Table 3.4, section 3.4).

Rules (Garmin, 2023, and the proposal): the binary flag marks motion-affected beats and intervals judged
abnormally short or long; the device marks a gap where it gives no beat; beats can also be lost silently
at motion (probability 1 - pi_hat(m)), merging two intervals into one unflagged interval. Pulse deficit is
NOT simulated in training (it is the bias RO4a measures). Timing jitter is optional in training.

Every parameter below is a placeholder until calibrated: motion episodes and jitter from Pulsewatch (D4),
flag threshold from RO1, pi_hat(m) from the Pulsewatch fit, gap statistics from Pulsewatch peak-free
stretches, then checked against Garmin verification data (meeting point 2).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np
import pandas as pd


@dataclass
class SimConfig:
    flag_threshold: float = 0.20                 # deviation from running reference (calibrate from RO1)
    flag_motion_level: float = 0.5               # m/s^2: beats at or above are flagged as motion-affected
    baseline_motion: tuple[float, float] = (0.02, 0.01)       # mean, sd of resting motion SD (m/s^2)
    episode_rate_per_hour: float = 4.0
    episode_levels: np.ndarray = field(default_factory=lambda: np.array([0.1, 0.3, 0.7, 1.5]))
    episode_durations_s: np.ndarray = field(default_factory=lambda: np.array([10, 30, 60, 180]))
    gap_rate_per_hour: float = 1.0
    gap_durations_s: np.ndarray = field(default_factory=lambda: np.array([5, 15, 60]))
    gap_motion_boost: float = 3.0                # gaps more likely during motion episodes
    jitter_sd_s: float = 0.0                     # 0 in training by default; Pulsewatch offsets in RO4a
    ref_n: int = 5


def default_pi_hat(m: np.ndarray) -> np.ndarray:
    """Placeholder retention curve, shaped like the pre-check (match falls with motion). NOT a fitted value."""
    return np.clip(0.95 - 0.35 * np.log1p(np.asarray(m) / 0.2), 0.3, 0.95)


def motion_trace(duration_s: float, cfg: SimConfig, rng: np.random.Generator, fs: float = 4.0):
    t = np.arange(0, duration_s, 1 / fs)
    m = np.abs(rng.normal(*cfg.baseline_motion, size=len(t)))
    n_ep = rng.poisson(cfg.episode_rate_per_hour * duration_s / 3600)
    for _ in range(n_ep):
        start = rng.uniform(0, duration_s)
        dur = rng.choice(cfg.episode_durations_s)
        m[(t >= start) & (t < start + dur)] = rng.choice(cfg.episode_levels) * rng.lognormal(0, 0.3)
    return t, m


def gap_intervals(duration_s, t_m, m, cfg: SimConfig, rng) -> list[tuple[float, float]]:
    n = rng.poisson(cfg.gap_rate_per_hour * duration_s / 3600)
    if n == 0:
        return []
    w = 1 + cfg.gap_motion_boost * (m >= cfg.flag_motion_level)
    starts = rng.choice(t_m, size=n, p=w / w.sum())
    return [(float(s), float(s + rng.choice(cfg.gap_durations_s))) for s in starts]


def simulate_segment(beat_t: np.ndarray, beat_cls: np.ndarray, duration_s: float, cfg: SimConfig,
                     rng: np.random.Generator, pi_hat: Callable[[np.ndarray], np.ndarray] = default_pi_hat):
    """Return (reported beats DataFrame, truth dict). Times in seconds from segment start."""
    beat_t = np.asarray(beat_t, float)
    beat_cls = np.asarray(beat_cls)
    t_m, m_trace = motion_trace(duration_s, cfg, rng)
    m = np.interp(beat_t, t_m, m_trace)
    gaps = gap_intervals(duration_s, t_m, m_trace, cfg, rng)
    in_gap = np.zeros(len(beat_t), dtype=bool)
    for a, b in gaps:
        in_gap |= (beat_t >= a) & (beat_t < b)
    silent = (~in_gap) & (rng.random(len(beat_t)) > pi_hat(m))
    keep = ~in_gap & ~silent
    t_rep = beat_t[keep] + (rng.normal(0, cfg.jitter_sd_s, keep.sum()) if cfg.jitter_sd_s > 0 else 0.0)
    rr = np.diff(t_rep, prepend=np.nan)
    gap_before = np.zeros(keep.sum(), dtype=bool)
    idx_keep = np.flatnonzero(keep)
    for k in range(1, len(idx_keep)):
        gap_before[k] = in_gap[idx_keep[k - 1] + 1: idx_keep[k]].any()
    rr[gap_before] = np.nan                         # no interval is formed across a marked gap
    flag = np.zeros(len(rr), dtype=bool)
    ref: list[float] = []
    for i, x in enumerate(rr):
        if not np.isfinite(x):
            ref = []
            continue
        if ref:
            med = float(np.median(ref[-cfg.ref_n:]))
            flag[i] = abs(x - med) > cfg.flag_threshold * med
        if not flag[i]:
            ref.append(x)
    flag |= m[keep] >= cfg.flag_motion_level
    gap_time = sum(min(b, duration_s) - a for a, b in _merge(gaps) if a < duration_s)
    reported = pd.DataFrame({"t": t_rep, "rr": rr, "flag": flag, "motion": m[keep], "gap_before": gap_before,
                             "is_pac": beat_cls[keep] == "S"})
    truth = {"n_pac_true": int((beat_cls == "S").sum()), "n_pac_silent": int(((beat_cls == "S") & silent).sum()),
             "n_pac_in_gap": int(((beat_cls == "S") & in_gap).sum()), "observed_s": duration_s - gap_time,
             "gaps": gaps}
    return reported, truth


def _merge(iv):
    out = []
    for a, b in sorted(iv):
        if out and a <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out
