"""Beat matching and motion for pi_hat(m) on Pulsewatch, with the settings locked for the pre-check
(handover/analyses/pulsewatch_retention/Pulsewatch_Beat_Retention_Precheck_Config.md).

* one-to-one matching: each PPG peak matches at most one ECG beat within +/-100 ms of the lag-shifted
  beat, closest pairs first;
* beats within 1 s of the PPG segment edges are dropped;
* motion = SD of accelerometer magnitude (m/s^2) in a 2 s window centred on the beat;
* bins <0.05, 0.05-0.2, 0.2-0.5, 0.5-1, >=1 m/s^2;
* lag search -3 to +3 s in 0.02 s steps maximising matches (nearest-peak count for speed); ties broken by
  the smallest mean distance (this tie-break is new and must be checked against the pre-check script).
"""
from __future__ import annotations

import numpy as np

MOTION_BINS = np.array([0.0, 0.05, 0.2, 0.5, 1.0, np.inf])


def match_one_to_one(ecg_t: np.ndarray, ppg_t: np.ndarray, tol: float = 0.100) -> np.ndarray:
    """Return, for each ECG beat time, True if it is matched to a distinct PPG peak within tol seconds."""
    ecg_t, ppg_t = np.asarray(ecg_t, float), np.asarray(ppg_t, float)
    pairs = []
    if len(ppg_t):
        for i, t in enumerate(ecg_t):
            lo, hi = np.searchsorted(ppg_t, [t - tol, t + tol])
            for j in range(lo, hi):
                pairs.append((abs(ppg_t[j] - t), i, j))
    pairs.sort()
    used_e, used_p = set(), set()
    for _, i, j in pairs:
        if i not in used_e and j not in used_p:
            used_e.add(i)
            used_p.add(j)
    out = np.zeros(len(ecg_t), dtype=bool)
    out[list(used_e)] = True
    return out


def nearest_count(ecg_t, ppg_t, tol=0.100) -> int:
    if len(ppg_t) == 0:
        return 0
    idx = np.clip(np.searchsorted(ppg_t, ecg_t), 1, len(ppg_t) - 1)
    d = np.minimum(np.abs(ppg_t[idx] - ecg_t), np.abs(ppg_t[idx - 1] - ecg_t))
    return int((d <= tol).sum())


def best_lag(ecg_t, ppg_t, lo=-3.0, hi=3.0, step=0.02, tol=0.100) -> float:
    lags = np.round(np.arange(lo, hi + step / 2, step), 4)
    ecg_t, ppg_t = np.asarray(ecg_t, float), np.asarray(ppg_t, float)
    counts = np.array([nearest_count(ecg_t + L, ppg_t, tol) for L in lags])
    best = np.flatnonzero(counts == counts.max())
    if len(best) == 1:
        return float(lags[best[0]])
    # tie-break (the count is flat within +/- tol): smallest mean distance among matched beats
    return float(min(lags[best], key=lambda L: _mean_distance(ecg_t + L, ppg_t, tol)))


def _mean_distance(ecg_t, ppg_t, tol):
    idx = np.clip(np.searchsorted(ppg_t, ecg_t), 1, len(ppg_t) - 1)
    d = np.minimum(np.abs(ppg_t[idx] - ecg_t), np.abs(ppg_t[idx - 1] - ecg_t))
    d = d[d <= tol]
    return d.mean() if len(d) else np.inf


def motion_sd(acc_mag: np.ndarray, fs: float, beat_t: np.ndarray, window: float = 2.0) -> np.ndarray:
    half = int(round(window * fs / 2))
    idx = np.round(np.asarray(beat_t) * fs).astype(int)
    return np.array([np.std(acc_mag[max(0, i - half):i + half]) if 0 <= i < len(acc_mag) else np.nan for i in idx])


def motion_bin(m: np.ndarray) -> np.ndarray:
    return np.digitize(m, MOTION_BINS[1:-1])


def edge_mask(beat_t: np.ndarray, seg_len_s: float, edge: float = 1.0) -> np.ndarray:
    beat_t = np.asarray(beat_t)
    return (beat_t >= edge) & (beat_t <= seg_len_s - edge)
