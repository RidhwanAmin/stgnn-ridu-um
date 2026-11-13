"""Download Icentia11k headers and beat annotations only (no signal files), with a checksum manifest.

About 6 GB for all 11,000 patients; about 0.2 GB for 300. The raw signal (1.1 TB) is not needed for
RO1 or RO2 (section 3.7).
"""
from __future__ import annotations

import hashlib
import threading
import time
import urllib.request
from pathlib import Path

import wfdb
from wfdb.io._url import NetFileNotFoundError

from ..config import ICENTIA_DB, ICENTIA_RAW, ICENTIA_VERSION


_missing_lock = threading.Lock()


def patient_dir(pid: str) -> str:
    return f"{pid[:3]}/{pid}"


def segment_names(pid: str) -> list[str]:
    url = f"https://physionet.org/files/{ICENTIA_DB}/{ICENTIA_VERSION}/{patient_dir(pid)}/RECORDS"
    return urllib.request.urlopen(url, timeout=60).read().decode().split()


def _retry(fn, tries: int = 5, wait: float = 10.0):
    """PhysioNet returns occasional 502/503 errors; retry with a growing pause. 404s are not retried."""
    for k in range(tries):
        try:
            return fn()
        except NetFileNotFoundError:
            raise
        except Exception:
            if k == tries - 1:
                raise
            time.sleep(wait * (k + 1))


def download_patient(pid: str, out: Path = ICENTIA_RAW, overwrite: bool = False) -> list[Path]:
    """Download .hea and .atr for every listed segment. Some listed segments have no .atr on
    PhysioNet (e.g. p04240_s49): those files are skipped and logged in MISSING.txt. The table builder
    stops at the first segment without both files, as the preliminary script did."""
    segs = _retry(lambda: segment_names(pid))
    files = [f"{patient_dir(pid)}/{s}.{ext}" for s in segs for ext in ("hea", "atr")]
    try:
        _retry(lambda: wfdb.dl_files(ICENTIA_DB, str(out), files, keep_subdirs=True, overwrite=overwrite))
        return [out / f for f in files]
    except NetFileNotFoundError:
        pass
    got, missing = [], []
    for f in files:                                   # fall back to one file at a time
        try:
            _retry(lambda f=f: wfdb.dl_files(ICENTIA_DB, str(out), [f], keep_subdirs=True, overwrite=overwrite))
            got.append(out / f)
        except NetFileNotFoundError:
            missing.append(f)
    with _missing_lock, (out / "MISSING.txt").open("a") as fh:
        fh.writelines(f"{m}\n" for m in missing)
    return got


def done_patients(manifest: Path) -> set[str]:
    """Patients already in the manifest. A patient's lines are written only after its download returned,
    so these are complete and are skipped on a re-run (no repeat requests to PhysioNet)."""
    if not manifest.exists():
        return set()
    out = set()
    for line in manifest.read_text().splitlines():
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            out.add(Path(parts[1].strip()).parts[1])     # p00/p00008/p00008_s00.hea -> p00008
    return out


def write_manifest(paths: list[Path], manifest: Path) -> None:
    """Append 'sha256  relative/path' lines so the download can be re-verified later."""
    with manifest.open("a") as fh:
        for p in paths:
            fh.write(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(manifest.parent)}\n")
