"""Stage A: beat, interval and summary tables (Parquet) for the patients in the given sets."""
import argparse

import pandas as pd

from esvea import sets
from esvea.config import ICENTIA_RAW, ICENTIA_TABLES
from esvea.ingest.tables import build_patient, write_patient

ap = argparse.ArgumentParser()
ap.add_argument("sets", nargs="+")
a = ap.parse_args()
rows = []
for n in a.sets:
    for pid in sets.read_set(n):
        beats, ivs, summ = build_patient(pid, ICENTIA_RAW)
        write_patient(pid, beats, ivs, ICENTIA_TABLES)
        rows.append({**summ, "set": n})
        print(pid, f"{summ['hours']:.1f} h", summ["n_S"], "PACs")
new = pd.DataFrame(rows)
p = ICENTIA_TABLES / "summary.parquet"
if p.exists():
    old = pd.read_parquet(p)
    new = pd.concat([old[~old.patient.isin(new.patient)], new], ignore_index=True)
new.to_parquet(p, index=False)
