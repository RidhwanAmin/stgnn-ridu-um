"""Pseudo-days for Icentia11k (segments carry no clock time; clock-time check, 2 November 2026).

A patient's segments are shuffled with a recorded seed, grouped into pseudo-days of about 20 segments
(about 24 h), and each segment is assigned to one of the four 6-hour blocks at random, balanced within
a pseudo-day. Pseudo-days are a training device: the patient-level reference is rate x 24.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .config import N_BLOCKS


def assign(segments: list[int], seed: int, per_day: int = 20) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    segs = list(rng.permutation(segments))
    rows = []
    n_days = max(1, int(round(len(segs) / per_day)))
    for d, chunk in enumerate(np.array_split(np.array(segs), n_days)):
        blocks = np.resize(np.arange(N_BLOCKS), len(chunk))
        rng.shuffle(blocks)
        rows += [(int(s), d, int(b)) for s, b in zip(chunk, blocks)]
    return pd.DataFrame(rows, columns=["segment", "pseudo_day", "block"]).sort_values("segment", ignore_index=True)
