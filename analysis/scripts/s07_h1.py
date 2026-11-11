"""H1 on P1. Refuses to run unless the pre-analysis note is committed (notes/*H1_preanalysis.md)."""
import json
import subprocess

import numpy as np
import pandas as pd

from esvea.config import NOTES, RESULTS
from esvea.io import iter_intervals, load_summary
from esvea.ro1 import glmm
from esvea.ro1.retention import apply_filter, removal_counts

notes = sorted(NOTES.glob("*H1_preanalysis.md"))
if not notes or subprocess.run(["git", "ls-files", "--error-unmatch", str(notes[-1])], capture_output=True).returncode:
    raise SystemExit("Commit notes/<date>_H1_preanalysis.md before running H1")
s = load_summary(["P1"], "h1").set_index("patient")
out = {}
for thr in (0.10, 0.15, 0.20, 0.25, 0.30):
    for af in ("include", "exclude"):
        rows = []
        for pid, ivs in iter_intervals(["P1"], "h1"):
            rc = removal_counts(ivs, apply_filter(ivs, thr), af).set_index("category")
            if "pac_coupling" in rc.index and s.loc[pid, "n_S"] > 0:
                n = int(rc.loc["pac_coupling", "n"])
                rows.append((n - int(rc.loc["pac_coupling", "removed"]), n, np.log(s.loc[pid, "pac_per_hour"])))
        d = pd.DataFrame(rows, columns=["k", "n", "x"])
        f = glmm.fit(d.k, d.n, d.x)
        out[f"{thr:.2f}_{af}"] = {**f.__dict__, "odds_ratio_per_doubling": float(np.exp(f.b * np.log(2))), "n_patients": len(d)}
RESULTS.mkdir(exist_ok=True)
(RESULTS / "h1_P1.json").write_text(json.dumps(out, indent=2, default=float))
print(json.dumps(out["0.20_include"], indent=2, default=float))
