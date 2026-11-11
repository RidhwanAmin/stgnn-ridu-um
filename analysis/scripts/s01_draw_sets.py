"""Draw and lock a patient set. Run once per set, in this order:
  python scripts/s01_draw_sets.py P3 --n 300 --seed <seed>     (S2 week 1; needs splits/P0.txt)
  python scripts/s01_draw_sets.py P1 --n <from D1 note> --seed <seed>
  python scripts/s01_draw_sets.py P2 --seed <seed>             (all remaining, 70/15/15)
Commit splits/ immediately after each run.
"""
import argparse

from esvea import sets

ap = argparse.ArgumentParser()
ap.add_argument("name", choices=["P3", "P1", "P2"])
ap.add_argument("--n", type=int)
ap.add_argument("--seed", type=int, required=True)
a = ap.parse_args()

all_ids = sets.fetch_patient_ids()
taken = set()
for n in sets.SET_FILES:
    try:
        taken |= set(sets.read_set(n))
    except FileNotFoundError:
        pass
if "P0" not in [n for n in sets.SET_FILES if (sets.SPLITS / f"{n}.txt").exists()]:
    raise SystemExit("splits/P0.txt is missing: copy the preliminary patient list first (see README)")
pool = [p for p in all_ids if p not in taken]
if a.name == "P2":
    for k, v in sets.split_p2(pool, a.seed).items():
        print(sets.write_set(k, v, a.seed), len(v))
else:
    print(sets.write_set(a.name, sets.draw(pool, a.n, a.seed), a.seed))
sets.verify()
