"""Download headers and beat annotations for the patients in the given sets (P3 is refused)."""
import argparse

from esvea import sets
from esvea.config import ICENTIA_RAW
from esvea.ingest.download import download_patient, write_manifest

ap = argparse.ArgumentParser()
ap.add_argument("sets", nargs="+")
a = ap.parse_args()
if "P3" in a.sets:
    raise SystemExit("P3 is not downloaded before M4")
ICENTIA_RAW.mkdir(parents=True, exist_ok=True)
for n in a.sets:
    for i, pid in enumerate(sets.read_set(n)):
        paths = download_patient(pid)
        write_manifest(paths, ICENTIA_RAW / "MANIFEST.sha256")
        print(n, i + 1, pid, len(paths))
