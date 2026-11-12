"""Interval rejection rules used in RQ1.2.

percent_deviation: the deployed-style rule used in section 4.2 (Karlsson et al., 2012): an interval is
accepted if it deviates from the median of the last five accepted intervals by at most the threshold.
The filter runs per segment and restarts at each segment.

Warm-up rule (checked 12 Nov 2026 against legacy/ro1_preliminary/incentia_ro1_prelim.py,
`deviation_filter`): the first `ref_n` intervals of a segment are accepted unconditionally and form
the reference; testing starts at interval `ref_n`. The filter runs on every interval of the segment,
including intervals that touch a Q beat or fall outside 0.2 to 3.0 s.

adaptive_lipponen_tarvainen: Lipponen and Tarvainen (2019), through NeuroKit2's 'Kubios' method.
Verify the index convention (interval i ends at peak i) on the unit test before using results.
"""
from __future__ import annotations

from collections import deque

import numpy as np


def percent_deviation(rr: np.ndarray, threshold: float, ref_n: int = 5) -> np.ndarray:
    """Return a boolean array: True where the interval is accepted."""
    rr = np.asarray(rr, dtype=float)
    keep = np.zeros(len(rr), dtype=bool)
    ref: deque[float] = deque(maxlen=ref_n)
    for i, x in enumerate(rr):
        if i < ref_n:                     # warm-up: first ref_n intervals accepted untested (legacy rule)
            keep[i] = True
            ref.append(x)
            continue
        m = float(np.median(ref))
        # same floating-point expression as the legacy script: RR values are multiples of 4 ms, so
        # deviations of exactly the threshold are common and |x-m| <= t*m rounds differently
        if not (abs(x - m) / m > threshold):
            keep[i] = True
            ref.append(x)
    return keep


def percent_deviation_by_segment(rr: np.ndarray, segment: np.ndarray, threshold: float) -> np.ndarray:
    keep = np.zeros(len(rr), dtype=bool)
    seg = np.asarray(segment)
    for s in np.unique(seg):
        idx = np.flatnonzero(seg == s)
        keep[idx] = percent_deviation(rr[idx], threshold)
    return keep


def adaptive_lipponen_tarvainen(rr: np.ndarray, fs: int = 250) -> np.ndarray:
    """Accepted mask from the Lipponen-Tarvainen detector (ectopic, long/short, missed, extra beats)."""
    import neurokit2 as nk  # optional dependency: pip install .[adaptive]

    rr = np.asarray(rr, dtype=float)
    peaks = np.concatenate([[0], np.cumsum(np.round(rr * fs))]).astype(int)
    info, _ = nk.signal_fixpeaks(peaks, sampling_rate=fs, method="Kubios", iterative=False, show=False)
    bad_peaks = set()
    for k in ("ectopic", "missed", "extra", "longshort"):
        bad_peaks.update(int(i) for i in np.atleast_1d(info.get(k, [])))
    keep = np.ones(len(rr), dtype=bool)
    for p in bad_peaks:                   # peak p closes interval p-1 (peaks has one more element than rr)
        if 1 <= p <= len(rr):
            keep[p - 1] = False
    return keep
