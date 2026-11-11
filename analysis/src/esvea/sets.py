"""Patient sets P0 to P3 (Table B.3): drawing, locking with SHA-256, and the loader guard.

Order of drawing (plan, section 3): P3 first and sealed; P1 once its size is fixed by the D1 power note;
P2 is every remaining patient, split 70/15/15 by patient (Decision D2, proposed default).
"""
from __future__ import annotations

import hashlib
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .config import ICENTIA_DB, ICENTIA_VERSION, SPLITS

SET_FILES = ("P0", "P1", "P2_train", "P2_val", "P2_test", "P3")

# Which sets each analysis may read. The guard refuses anything else.
ALLOWED = {
    "reproduce_p0": {"P0"},
    "power_d1": {"P0"},
    "ro1_curves": {"P0", "P1"},
    "h1": {"P1"},
    "rq13": {"P1"},
    "ro2_train": {"P2_train"},
    "ro2_val": {"P2_val"},
    "ro2_test": {"P2_test"},
    "ro4a": {"P3"},              # only after the M4 freeze record exists
}


def fetch_patient_ids(cache: Path | None = None) -> list[str]:
    """All 11,000 patient ids (p00000 ... p10999) from the PhysioNet RECORDS file."""
    cache = cache or SPLITS / "_all_patients.txt"
    if cache.exists():
        return cache.read_text().split()
    url = f"https://physionet.org/files/{ICENTIA_DB}/{ICENTIA_VERSION}/RECORDS"
    lines = urllib.request.urlopen(url, timeout=60).read().decode().split()
    ids = sorted(line.strip("/").split("/")[-1] for line in lines)
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text("\n".join(ids) + "\n")
    return ids


def draw(pool: list[str], n: int, seed: int) -> list[str]:
    """Draw n ids without replacement from a sorted pool with a recorded seed."""
    pool = sorted(pool)
    if n > len(pool):
        raise ValueError(f"asked for {n} from a pool of {len(pool)}")
    rng = np.random.default_rng(seed)
    return sorted(rng.choice(pool, size=n, replace=False).tolist())


def split_p2(pool: list[str], seed: int, fractions=(0.70, 0.15, 0.15)) -> dict[str, list[str]]:
    pool = sorted(pool)
    rng = np.random.default_rng(seed)
    order = rng.permutation(len(pool))
    n_tr = int(round(fractions[0] * len(pool)))
    n_va = int(round(fractions[1] * len(pool)))
    pick = [pool[i] for i in order]
    return {"P2_train": sorted(pick[:n_tr]), "P2_val": sorted(pick[n_tr:n_tr + n_va]),
            "P2_test": sorted(pick[n_tr + n_va:])}


def write_set(name: str, ids: list[str], seed: int | None, splits: Path = SPLITS) -> Path:
    if name not in SET_FILES:
        raise ValueError(name)
    p = splits / f"{name}.txt"
    if p.exists():
        raise FileExistsError(f"{p} exists: sets are written once and never redrawn")
    header = f"# {name}; n={len(ids)}; seed={seed}\n"
    p.write_text(header + "\n".join(ids) + "\n")
    _update_sums(splits)
    return p


def read_set(name: str, splits: Path = SPLITS) -> list[str]:
    p = splits / f"{name}.txt"
    return [x for x in p.read_text().split("\n") if x and not x.startswith("#")]


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _update_sums(splits: Path) -> None:
    lines = [f"{_sha(splits / f'{n}.txt')}  {n}.txt" for n in SET_FILES if (splits / f"{n}.txt").exists()]
    (splits / "SHA256SUMS").write_text("\n".join(lines) + "\n")


def verify(splits: Path = SPLITS) -> None:
    """Raise if any committed list changed after locking, or if two sets overlap."""
    sums = splits / "SHA256SUMS"
    for line in sums.read_text().split("\n"):
        if not line.strip():
            continue
        h, name = line.split()
        if _sha(splits / name) != h:
            raise RuntimeError(f"{name} changed after it was locked")
    seen: dict[str, str] = {}
    for n in SET_FILES:
        if (splits / f"{n}.txt").exists():
            for pid in read_set(n, splits):
                if pid in seen:
                    raise RuntimeError(f"{pid} is in both {seen[pid]} and {n}")
                seen[pid] = n


@dataclass
class Guard:
    """Refuses to load a patient whose set is not allowed for the analysis being run."""
    analysis: str
    splits: Path = SPLITS

    def __post_init__(self):
        verify(self.splits)
        allowed = ALLOWED[self.analysis]
        if self.analysis == "ro4a" and not (self.splits.parent / "notes" / "M4_freeze_record.md").exists():
            raise PermissionError("P3 stays closed until notes/M4_freeze_record.md exists")
        self.ids = {pid for n in allowed for pid in read_set(n, self.splits)}

    def check(self, pid: str) -> str:
        if pid not in self.ids:
            raise PermissionError(f"{pid} is not in the sets allowed for '{self.analysis}'")
        return pid
