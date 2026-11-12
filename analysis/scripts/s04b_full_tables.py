"""G1 follow-up: compare EVERY cell of proposal Tables 4.2 and 4.3 on P0 (new value vs docx value).

Analysable rule (coded, not a list): a patient needs at least one non-Q beat (excludes p08269, p10564).
Outputs results/p0_full_tables.csv and results/p0_full_tables.json. Exit 0 only if every cell matches.
"""
import json

import numpy as np
import pandas as pd

from esvea.config import RESULTS
from esvea.io import iter_intervals, load_summary
from esvea.ro1.retention import apply_filter, removal_counts

DOCX_42 = {  # category: (n, 10%, 20%, 30%, 20% ESVEA-neg, 20% ESVEA-pos), shares in %
    "pac_coupling": (867745, 81.5, 60.9, 37.4, 78.5, 60.0),
    "pause_after_pac": (864826, 74.9, 54.5, 37.3, 50.1, 54.8),
    "pvc_coupling": (405273, 85.4, 70.0, 46.5, 65.4, 77.9),
    "normal": (55206675, 20.1, 8.8, 6.2, 8.1, 11.5),
}
DOCX_43 = {
    "n_patients": 298, "hours_median": 57.5, "hours_q1": 55.5, "hours_q3": 58.1,
    "pac_h_median": 1.35, "pac_h_q1": 0.23, "pac_h_q3": 13.38,
    "n_30h": 54, "pct_30h": 18.1, "n_480d": 67, "pct_480d": 22.5,
    "n_run20": 25, "pct_run20": 8.4, "n_binici": 66, "pct_binici": 22.1,
}

s = load_summary(["P0"], "reproduce_p0")
s["analysable"] = (s.n_N + s.n_S + s.n_V) > 0
print("not analysable:", s.loc[~s.analysable, "patient"].tolist())
s = s[s.analysable].reset_index(drop=True)
keep_ids = set(s.patient)
esvea = s.set_index("patient")["esvea_binici_rate_or_run"]

parts = []
for pid, ivs in iter_intervals(["P0"], "reproduce_p0"):
    if pid not in keep_ids:
        continue
    for thr in (0.10, 0.20, 0.30):
        rc = removal_counts(ivs, apply_filter(ivs, thr))
        rc["patient"], rc["threshold"], rc["esvea"] = pid, thr, bool(esvea[pid])
        parts.append(rc)
rc = pd.concat(parts, ignore_index=True)

rows = []
for cat, (n_doc, *shares_doc) in DOCX_42.items():
    d = rc[rc.category == cat]
    n_new = int(d[np.isclose(d.threshold, 0.20)]["n"].sum())
    rows.append(("4.2", cat, "n", n_new, n_doc))
    for thr, doc in zip((0.10, 0.20, 0.30), shares_doc[:3]):
        t = d[np.isclose(d.threshold, thr)]
        rows.append(("4.2", cat, f"{int(thr * 100)}%", round(100 * t.removed.sum() / t.n.sum(), 1), doc))
    t = d[np.isclose(d.threshold, 0.20)]
    for flag, doc in ((False, shares_doc[3]), (True, shares_doc[4])):
        g = t[t.esvea == flag]
        rows.append(("4.2", cat, f"20% ESVEA {'pos' if flag else 'neg'}", round(100 * g.removed.sum() / g.n.sum(), 1), doc))

N = len(s)
new43 = {
    "n_patients": N,
    "hours_median": round(s.hours.median(), 1), "hours_q1": round(s.hours.quantile(0.25), 1),
    "hours_q3": round(s.hours.quantile(0.75), 1),
    "pac_h_median": round(s.pac_per_hour.median(), 2), "pac_h_q1": round(s.pac_per_hour.quantile(0.25), 2),
    "pac_h_q3": round(s.pac_per_hour.quantile(0.75), 2),
    "n_30h": int(s.esvea_secondary.sum()), "pct_30h": round(100 * s.esvea_secondary.mean(), 1),
    "n_480d": int(s.esvea_primary.sum()), "pct_480d": round(100 * s.esvea_primary.mean(), 1),
    "n_run20": int((s.longest_pac_run >= 20).sum()), "pct_run20": round(100 * (s.longest_pac_run >= 20).mean(), 1),
    "n_binici": int(s.esvea_binici_rate_or_run.sum()), "pct_binici": round(100 * s.esvea_binici_rate_or_run.mean(), 1),
}
rows += [("4.3", "", k, new43[k], v) for k, v in DOCX_43.items()]

out = pd.DataFrame(rows, columns=["table", "row", "column", "new", "docx"])
out["equal"] = [bool(a == b) for a, b in zip(out.new, out.docx)]  # exact: values are already rounded to the printed precision
RESULTS.mkdir(exist_ok=True)
out.to_csv(RESULTS / "p0_full_tables.csv", index=False)
(RESULTS / "p0_full_tables.json").write_text(json.dumps(
    {"cells": len(out), "equal": int(out.equal.sum()), "differ": out[~out.equal].to_dict("records")}, indent=2, default=str))
print(out.to_string(index=False))
print(f"\n{out.equal.sum()} of {len(out)} cells equal")
raise SystemExit(0 if out.equal.all() else 1)
