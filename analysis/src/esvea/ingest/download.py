"""Download Icentia11k headers and beat annotations only (no signal files), with a checksum manifest.

About 6 GB for all 11,000 patients; about 0.2 GB for 300. The raw signal (1.1 TB) is not needed for
RO1 or RO2 (section 3.7).
"""
from __future__ import annotations

import hashlib
import urllib.request
from pathlib import Path

import wfdb

from ..config import ICENTIA_DB, ICENTIA_RAW, ICENTIA_VERSION


def patient_dir(pid: str) -> str:
    return f"{pid[:3]}/{pid}"


def segment_names(pid: str) -> list[str]:
    url = f"https://physionet.org/files/{ICENTIA_DB}/{ICENTIA_VERSION}/{patient_dir(pid)}/RECORDS"
    return urllib.request.urlopen(url, timeout=60).read().decode().split()


def download_patient(pid: str, out: Path = ICENTIA_RAW, overwrite: bool = False) -> list[Path]:
    segs = segment_names(pid)
    files = [f"{patient_dir(pid)}/{s}.{ext}" for s in segs for ext in ("hea", "atr")]
    wfdb.dl_files(ICENTIA_DB, str(out), files, keep_subdirs=True, overwrite=overwrite)
    return [out / f for f in files]


def write_manifest(paths: list[Path], manifest: Path) -> None:
    """Append 'sha256  relative/path' lines so the download can be re-verified later."""
    with manifest.open("a") as fh:
        for p in paths:
            fh.write(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(manifest.parent)}\n")
