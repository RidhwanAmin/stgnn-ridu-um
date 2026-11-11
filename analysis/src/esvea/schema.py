"""The reported-beat table: one format for simulated Icentia11k streams, Pulsewatch-derived streams and,
later, the Garmin export (Track 2, R3 parser target). The estimator reads only this format.

Column            type     meaning
patient           str      pseudonymous id
day               int      calendar day index (Garmin) or pseudo-day (Icentia11k)
block             int      0..3 for 00-06, 06-12, 12-18, 18-24 local time
t                 float    seconds from the start of the day
rr                float    interval ending at this beat, seconds; NaN after a gap or at a start
flag              bool     device low-confidence flag (binary per beat)
motion            float    SD of accelerometer magnitude, m/s^2, 2-s window centred on the beat
gap_before        bool     a device gap marker lies between the previous reported beat and this one
Coverage table (one row per patient, day, block): observed_h = block time minus marked gaps and non-wear.
"""
from __future__ import annotations

import pandas as pd

BEAT_COLUMNS = {"patient": "object", "day": "int64", "block": "int64", "t": "float64", "rr": "float64",
                "flag": "bool", "motion": "float64", "gap_before": "bool"}
COVERAGE_COLUMNS = {"patient": "object", "day": "int64", "block": "int64", "observed_h": "float64"}


def validate(df: pd.DataFrame, columns: dict[str, str]) -> pd.DataFrame:
    missing = set(columns) - set(df.columns)
    if missing:
        raise ValueError(f"missing columns: {sorted(missing)}")
    out = df[list(columns)].astype(columns)
    if "block" in out and not out["block"].between(0, 3).all():
        raise ValueError("block must be 0..3")
    if "observed_h" in out and not out["observed_h"].between(0, 6).all():
        raise ValueError("observed_h must be within 0..6 h")
    return out
