"""Gate for Stage A: the new pipeline must reproduce Tables 4.2 and 4.3 on P0 (to the printed precision)."""
import json

import numpy as np
import pandas as pd

from esvea.config import RESULTS
from esvea.io import iter_intervals, load_summary
from esvea.ro1.retention import P0_TARGETS, apply_filter, removal_counts

s = load_summary(["P0"], "reproduce_p0")
parts = []
for pid, ivs in iter_intervals(["P0"], "reproduce_p0"):
    if pid not in set(s.patient):
        continue
    rc = removal_counts(ivs, apply_filter(ivs, 0.20))
    rc["patient"] = pid
    parts.append(rc)
rc = pd.concat(parts).merge(s[["patient", "esvea_binici_rate_or_run"]], on="patient")
pool = rc.groupby("category")[["n", "removed"]].sum()
share = (pool.removed / pool.n).round(3).to_dict()
pac = rc[rc.category == "pac_coupling"].groupby("esvea_binici_rate_or_run")[["n", "removed"]].sum()
got = {
    "n_patients": int(s.shape[0]),
    "removed_pac_coupling": share.get("pac_coupling"), "removed_pause_after_pac": share.get("pause_after_pac"),
    "removed_pvc_coupling": share.get("pvc_coupling"), "removed_normal": share.get("normal"),
    "removed_pac_esvea_neg": round(float(pac.loc[False, "removed"] / pac.loc[False, "n"]), 3),
    "removed_pac_esvea_pos": round(float(pac.loc[True, "removed"] / pac.loc[True, "n"]), 3),
    "n_esvea_480": int(s.esvea_primary.sum()), "n_esvea_30h": int(s.esvea_secondary.sum()),
    "n_esvea_binici": int(s.esvea_binici_rate_or_run.sum()),
    "median_hours": round(float(s.hours.median()), 1), "median_pac_per_hour": round(float(s.pac_per_hour.median()), 2),
}
diff = {k: (got[k], v) for k, v in P0_TARGETS.items() if not np.isclose(got[k], v, atol=1e-9)}
RESULTS.mkdir(exist_ok=True)
(RESULTS / "p0_reproduction.json").write_text(json.dumps({"got": got, "target": P0_TARGETS, "diff": diff}, indent=2))
print(json.dumps(diff or "REPRODUCED", indent=2))
raise SystemExit(1 if diff else 0)
