"""D1: size of P1 from a power simulation on P0. Writes a dated note to commit BEFORE drawing P1."""
import datetime as dt

import numpy as np
import pandas as pd

from esvea.config import NOTES
from esvea.io import iter_intervals, load_summary
from esvea.ro1 import glmm
from esvea.ro1.retention import apply_filter, removal_counts

s = load_summary(["P0"], "power_d1").set_index("patient")
rows = []
for pid, ivs in iter_intervals(["P0"], "power_d1"):
    rc = removal_counts(ivs, apply_filter(ivs, 0.20)).set_index("category")
    if "pac_coupling" in rc.index and rc.loc["pac_coupling", "n"] > 0 and s.loc[pid, "n_S"] > 0:
        n = int(rc.loc["pac_coupling", "n"])
        rows.append((pid, n - int(rc.loc["pac_coupling", "removed"]), n, np.log(s.loc[pid, "pac_per_hour"])))
d = pd.DataFrame(rows, columns=["patient", "k", "n", "x"])
f = glmm.fit(d.k, d.n, d.x)
sizes = [50, 75, 100, 150, 200, 300]
# Power for half the P0 effect as well: the P0 effect is an optimistic planning value.
pw_full = glmm.power(sizes, f.a, f.b, f.sigma, d.x.to_numpy(), d.n.to_numpy(), n_sim=500)
pw_half = glmm.power(sizes, f.a, f.b / 2, f.sigma, d.x.to_numpy(), d.n.to_numpy(), n_sim=500)
choice = glmm.smallest_size(pw_half) or max(sizes)
note = NOTES / f"{dt.date.today()}_D1_P1_size.md"
note.write_text(f"""# D1: size of P1 (written before P1 is drawn)

P0 fit (20% threshold, PAC coupling retention on log PACs/h, patient random intercept): b = {f.b:.3f}
(95% CI {f.ci_b[0]:.3f} to {f.ci_b[1]:.3f}), sigma = {f.sigma:.3f}, n patients = {len(d)}.

Power (500 simulations each, alpha 0.05, two-sided):

| P1 size | power at P0 effect | power at half the P0 effect |
|---|---|---|
""" + "".join(f"| {m} | {pw_full[m]:.2f} | {pw_half[m]:.2f} |\n" for m in sizes) + f"""
Rule: smallest size with >= 0.90 power at HALF the P0 effect. **P1 size = {choice}.**
Seed for drawing P1: to be recorded in splits/P1.txt.
""")
print(note.read_text())
