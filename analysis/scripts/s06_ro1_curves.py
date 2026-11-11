"""RQ1.2: threshold sweep 10-30% (1-point steps), AF included and excluded, plus the adaptive filter."""
import argparse

import pandas as pd

from esvea.config import RESULTS
from esvea.io import iter_intervals
from esvea.ro1.filters import adaptive_lipponen_tarvainen
from esvea.ro1.retention import patient_threshold_sweep, removal_counts

ap = argparse.ArgumentParser()
ap.add_argument("sets", nargs="+")
ap.add_argument("--adaptive", action="store_true")
a = ap.parse_args()
sw, ad = [], []
for pid, ivs in iter_intervals(a.sets, "ro1_curves"):
    for af in ("include", "exclude"):
        sw.append(patient_threshold_sweep(pid, ivs, af=af).assign(af=af))
    if a.adaptive:
        keep = ivs.groupby("segment", group_keys=False)["rr_s"].apply(lambda r: pd.Series(adaptive_lipponen_tarvainen(r.to_numpy()), index=r.index))
        ad.append(removal_counts(ivs, keep.sort_index().to_numpy()).assign(patient=pid))
RESULTS.mkdir(exist_ok=True)
tag = "_".join(a.sets)
pd.concat(sw).to_parquet(RESULTS / f"ro1_sweep_{tag}.parquet", index=False)
if ad:
    pd.concat(ad).to_parquet(RESULTS / f"ro1_adaptive_{tag}.parquet", index=False)
