"""Download headers and beat annotations for the patients in the given sets (P3 is refused).

  python scripts/s02_download.py P0 [--jobs 4]

--jobs runs that many patients in parallel (keep it small to stay polite to PhysioNet). The manifest
is written from the main thread, one patient at a time.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor

from esvea import sets
from esvea.config import ICENTIA_RAW
from esvea.ingest.download import download_patient, write_manifest

ap = argparse.ArgumentParser()
ap.add_argument("sets", nargs="+")
ap.add_argument("--jobs", type=int, default=1)
a = ap.parse_args()
if "P3" in a.sets:
    raise SystemExit("P3 is not downloaded before M4")
ICENTIA_RAW.mkdir(parents=True, exist_ok=True)
for n in a.sets:
    ids = sets.read_set(n)
    with ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
        for i, (pid, paths) in enumerate(zip(ids, ex.map(download_patient, ids))):
            write_manifest(paths, ICENTIA_RAW / "MANIFEST.sha256")
            print(n, i + 1, pid, len(paths), flush=True)
