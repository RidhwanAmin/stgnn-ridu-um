"""Download headers and beat annotations for the patients in the given sets (P3 is refused).

  python scripts/s02_download.py P0 [--jobs 4]

--jobs runs that many patients in parallel (keep it small to stay polite to PhysioNet). The manifest
is written from the main thread, one patient at a time.

Re-runs are safe: patients already in the manifest are skipped without contacting PhysioNet. A patient
whose download still fails after the retries in `download_patient` (for example a lasting 502) is
reported and left out of the manifest; the other patients continue, and the script exits 1 at the end
listing the failed patients, so a re-run picks up only those.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor

from esvea import sets
from esvea.config import ICENTIA_RAW
from esvea.ingest.download import done_patients, download_patient, write_manifest


def _safe(pid):
    try:
        return download_patient(pid), None
    except Exception as e:                       # noqa: BLE001  reported below, patient left for a re-run
        return None, f"{type(e).__name__}: {e}"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("sets", nargs="+")
    ap.add_argument("--jobs", type=int, default=1)
    a = ap.parse_args()
    if "P3" in a.sets:
        raise SystemExit("P3 is not downloaded before M4")
    ICENTIA_RAW.mkdir(parents=True, exist_ok=True)
    manifest = ICENTIA_RAW / "MANIFEST.sha256"
    failed = []
    for n in a.sets:
        done = done_patients(manifest)
        ids = sets.read_set(n)
        todo = [p for p in ids if p not in done]
        print(n, f"{len(ids) - len(todo)} already in the manifest, {len(todo)} to download", flush=True)
        with ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
            for i, (pid, (paths, err)) in enumerate(zip(todo, ex.map(_safe, todo))):
                if err:
                    failed.append(pid)
                    print(n, i + 1, pid, "FAILED", err, flush=True)
                    continue
                write_manifest(paths, manifest)
                print(n, i + 1, pid, len(paths), flush=True)
    if failed:
        raise SystemExit(f"{len(failed)} patients failed (re-run to retry): {' '.join(failed)}")
