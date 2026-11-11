"""RQ1.3: origin-agnostic premature-beat count (S + V) against the PAC-only count (S), by burden."""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..config import ESVEA_PRIMARY_PER_DAY


def bland_altman(a: np.ndarray, b: np.ndarray) -> dict:
    d = np.asarray(a, float) - np.asarray(b, float)
    bias, sd = d.mean(), d.std(ddof=1)
    return {"bias": bias, "loa_low": bias - 1.96 * sd, "loa_high": bias + 1.96 * sd, "n": len(d)}


def origin_table(summary: pd.DataFrame) -> pd.DataFrame:
    """Per patient: daily-equivalent premature (S+V) and PAC-only (S) counts, and the ESVEA call each gives."""
    s = summary.copy()
    s["premature_per_day"] = (s["n_S"] + s["n_V"]) / s["hours"] * 24
    s["pac_per_day"] = s["n_S"] / s["hours"] * 24
    s["esvea_premature"] = s["premature_per_day"] >= ESVEA_PRIMARY_PER_DAY
    s["esvea_pac"] = s["pac_per_day"] >= ESVEA_PRIMARY_PER_DAY
    s["reclassified"] = s["esvea_premature"] != s["esvea_pac"]
    return s


def by_band(tab: pd.DataFrame, band_col: str = "burden_band") -> pd.DataFrame:
    rows = []
    for band, g in tab.groupby(band_col, observed=True):
        ba = bland_altman(np.log1p(g["premature_per_day"]), np.log1p(g["pac_per_day"]))
        rows.append({band_col: band, **ba, "reclassified": int(g["reclassified"].sum())})
    return pd.DataFrame(rows)
