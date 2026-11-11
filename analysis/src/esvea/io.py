"""Load the Stage A tables for a set of patients through the guard."""
from __future__ import annotations

import pandas as pd

from .config import ICENTIA_TABLES
from .sets import Guard, read_set


def load_summary(set_names: list[str], analysis: str) -> pd.DataFrame:
    g = Guard(analysis)
    s = pd.read_parquet(ICENTIA_TABLES / "summary.parquet")
    ids = [g.check(p) for n in set_names for p in read_set(n)]
    return s[s.patient.isin(ids)].reset_index(drop=True)


def iter_intervals(set_names: list[str], analysis: str):
    g = Guard(analysis)
    for n in set_names:
        for pid in read_set(n):
            yield g.check(pid), pd.read_parquet(ICENTIA_TABLES / "intervals" / f"{pid}.parquet")
