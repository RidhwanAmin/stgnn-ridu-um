"""Gate G1: the new pipeline must reproduce Tables 4.2 and 4.3 on P0 (to the printed precision).

Section 4.2 analysed 298 of the 300 sampled patients. The rule that dropped two patients must be taken from
the preliminary script and implemented as a column `analysable` in the summary table (see
runbook T2). Implemented 12 Nov 2026 as `ingest.tables.is_analysable`: at least one non-Q beat.
Writes results/p0_per_patient.csv for a patient-by-patient comparison with the preliminary outputs.
"""
import json

import numpy as np
import pandas as pd

from esvea.config import RESULTS
from esvea.io import iter_intervals, load_summary
from esvea.ro1.retention import P0_TARGETS, apply_filter, removal_counts

s = load_summary(["P0"], "reproduce_p0")
dropped = []
if "analysable" in s.columns:
    dropped = s.loc[~s.analysable, "patient"].tolist()
    print("not analysable:", dropped)
    s = s[s.analysable].reset_index(drop=True)
parts = []
for pid, ivs in iter_intervals(["P0"], "reproduce_p0"):
    if pid not in set(s.patient):
        continue
    rc = removal_counts(ivs, apply_filter(ivs, 0.20))
    rc["patient"] = pid
    parts.append(rc)
rc = pd.concat(parts).merge(s[["patient", "esvea_binici_rate_or_run"]], on="patient")
RESULTS.mkdir(exist_ok=True)
per = rc.pivot_table(index="patient", columns="category", values=["n", "removed"], aggfunc="sum", fill_value=0)
per.columns = [f"{a}_{b}" for a, b in per.columns]
s.set_index("patient").join(per).to_csv(RESULTS / "p0_per_patient.csv")
pool = rc.groupby("category")[["n", "removed"]].sum()
share = (pool.removed / pool.n).round(3).to_dict()
pac = rc[rc.category == "pac_coupling"].groupby("esvea_binici_rate_or_run")[["n", "removed"]].sum()


def share_in(status):
    if status not in pac.index or pac.loc[status, "n"] == 0:
        return float("nan")
    return round(float(pac.loc[status, "removed"] / pac.loc[status, "n"]), 3)


got = {
    "n_patients": int(s.shape[0]),
    "removed_pac_coupling": share.get("pac_coupling"), "removed_pause_after_pac": share.get("pause_after_pac"),
    "removed_pvc_coupling": share.get("pvc_coupling"), "removed_normal": share.get("normal"),
    "removed_pac_esvea_neg": share_in(False), "removed_pac_esvea_pos": share_in(True),
    "n_esvea_480": int(s.esvea_primary.sum()), "n_esvea_30h": int(s.esvea_secondary.sum()),
    "n_esvea_binici": int(s.esvea_binici_rate_or_run.sum()),
    "median_hours": round(float(s.hours.median()), 1), "median_pac_per_hour": round(float(s.pac_per_hour.median()), 2),
}
diff = {k: (got[k], v) for k, v in P0_TARGETS.items() if not np.isclose(got[k], v, atol=1e-9)}
(RESULTS / "p0_reproduction.json").write_text(json.dumps({"got": got, "target": P0_TARGETS, "diff": diff,
                                                               "not_analysable": dropped}, indent=2))
print(json.dumps(diff or "REPRODUCED", indent=2))
raise SystemExit(1 if diff else 0)
