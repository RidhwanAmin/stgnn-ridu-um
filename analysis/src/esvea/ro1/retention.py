"""RQ1.2: removal (1 - retention) by interval category, burden band and threshold."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .filters import percent_deviation_by_segment

# Section 4.2 values the new pipeline must reproduce on P0 at the 20% threshold.
P0_TARGETS = {
    "n_patients": 298,
    "removed_pac_coupling": 0.609,
    "removed_pause_after_pac": 0.545,
    "removed_pvc_coupling": 0.700,
    "removed_normal": 0.088,
    "removed_pac_esvea_neg": 0.785,     # ESVEA by Binici rate or run
    "removed_pac_esvea_pos": 0.600,
    "n_esvea_480": 67, "n_esvea_30h": 54, "n_esvea_binici": 66,
    "median_hours": 57.5, "median_pac_per_hour": 1.35,
}

# Proposed burden bands for curves (PACs per hour); quintiles are reported as well.
BURDEN_BANDS = [0, 1, 10, 30, np.inf]
BAND_LABELS = ["<1/h", "1-10/h", "10-30/h", ">=30/h"]


def apply_filter(ivs: pd.DataFrame, threshold: float) -> np.ndarray:
    return percent_deviation_by_segment(ivs["rr_s"].to_numpy(), ivs["segment"].to_numpy(), threshold)


def category_masks(ivs: pd.DataFrame) -> dict[str, np.ndarray]:
    """Table 4.2 categories as in the preliminary script: each is its own mask and they overlap.
    An S-S interval counts as PAC coupling and as pause after PAC; an S-V interval counts as PVC
    coupling and as pause after PAC (legacy/ro1_preliminary/incentia_ro1_prelim.py, aligned for G1)."""
    st, en = ivs["start_cls"].to_numpy(), ivs["end_cls"].to_numpy()
    return {
        "pac_coupling": en == "S",
        "pause_after_pac": st == "S",
        "pvc_coupling": en == "V",
        "normal": (st == "N") & (en == "N"),
    }


def removal_counts(ivs: pd.DataFrame, keep: np.ndarray, af: str = "include") -> pd.DataFrame:
    """Per category: n tallied, n removed. af in {'include', 'exclude'} (Decision D3)."""
    m = ivs["tally"].to_numpy().astype(bool)
    if af == "exclude":
        m &= ~ivs["in_af"].to_numpy().astype(bool)
    removed = ~np.asarray(keep, dtype=bool)
    rows = [{"category": c, "n": int((m & mk).sum()), "removed": int((m & mk & removed).sum())}
            for c, mk in category_masks(ivs).items()]
    return pd.DataFrame(rows)


def patient_threshold_sweep(pid: str, ivs: pd.DataFrame, thresholds=np.arange(0.10, 0.301, 0.01),
                            af: str = "include") -> pd.DataFrame:
    rows = []
    for t in thresholds:
        rc = removal_counts(ivs, apply_filter(ivs, float(t)), af)
        rc.insert(0, "threshold", round(float(t), 2))
        rc.insert(0, "patient", pid)
        rows.append(rc)
    return pd.concat(rows, ignore_index=True)


def pooled_removal(sweep: pd.DataFrame, by: list[str] | None = None) -> pd.DataFrame:
    """Pooled share removed (sum removed / sum n), as in Table 4.2."""
    keys = ["threshold", "category"] + (by or [])
    g = sweep.groupby(keys)[["n", "removed"]].sum().reset_index()
    g["share_removed"] = g["removed"] / g["n"]
    return g


def add_burden_band(summary: pd.DataFrame) -> pd.DataFrame:
    s = summary.copy()
    s["burden_band"] = pd.cut(s["pac_per_hour"], BURDEN_BANDS, labels=BAND_LABELS, right=False)
    s["burden_quintile"] = pd.qcut(s["pac_per_hour"].rank(method="first"), 5, labels=False) + 1
    return s


def patient_bootstrap_ci(sweep: pd.DataFrame, category: str, threshold: float, n_boot: int = 2000,
                         seed: int = 2026) -> tuple[float, float, float]:
    """Pooled removal with a 95% CI from resampling patients."""
    d = sweep[(sweep.category == category) & np.isclose(sweep.threshold, threshold)]
    n, r = d["n"].to_numpy(), d["removed"].to_numpy()
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(d), size=(n_boot, len(d)))
    boots = r[idx].sum(1) / n[idx].sum(1)
    return r.sum() / n.sum(), *np.percentile(boots, [2.5, 97.5])
