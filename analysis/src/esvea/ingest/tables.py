"""Beat, interval and patient-summary tables from Icentia11k annotations (plan, Stage A).

Rules carried over from the preliminary analysis (section 4.2):
* intervals are formed only between consecutive beats of the same segment (segments are untimed and
  not in chronological order, so no interval crosses a segment boundary);
* every interval goes through the filter, but tallies exclude intervals touching a Q beat and
  intervals outside 0.2 to 3.0 s (strict on both ends);
* rate = PACs per analysed hour.

Aligned 12 Nov 2026 with legacy/ro1_preliminary/incentia_ro1_prelim.py (G1):
* segments are read in order s00, s01, ... up to s49 and reading stops at the first missing segment;
  a patient without s00 is not analysable;
* a segment with fewer than 2 beats contributes nothing; a segment with fewer than 8 beats
  (REF_WINDOW + 3) contributes beats and hours but no tallied intervals;
* analysed hours of a segment = time from its first to its last non-Q beat (not the record length);
* a patient is analysable if it has at least one non-Q (N, S or V) beat in the segments read
  (G1 decision, 12 Nov 2026: a coded rule, not a list; on P0 it excludes p08269 and p10564, which
  contain only Q beats).
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import wfdb

from ..config import AF_RHYTHMS, BEAT_SYMBOLS, BINICI_RUN_BEATS, ESVEA_PRIMARY_PER_DAY, \
    ESVEA_SECONDARY_PER_HOUR, FS, RR_MAX_S, RR_MIN_S

MAX_SEGMENTS = 50                 # legacy MAX_SEGMENTS
MIN_BEATS_FOR_INTERVALS = 8       # legacy REF_WINDOW + 3


def is_analysable(summ: dict) -> bool:
    """G1 decision rule: at least one non-Q beat (N, S or V)."""
    return bool(summ["n_N"] + summ["n_S"] + summ["n_V"] > 0)


def beats_from_annotation(sample: np.ndarray, symbol: list[str], aux: list[str]) -> pd.DataFrame:
    """Keep beat symbols; carry the rhythm context from '+' markers ('(N', '(AFIB', '(AFL')."""
    rhythm, rows = "(N", []
    for s, sym, note in zip(sample, symbol, aux):
        if sym == "+":
            rhythm = (note or rhythm).strip("\x00") or rhythm
            continue
        if sym in BEAT_SYMBOLS:
            rows.append((int(s), sym, rhythm in AF_RHYTHMS))
    return pd.DataFrame(rows, columns=["sample", "cls", "in_af"])


def read_segment(record_path: Path) -> tuple[pd.DataFrame, float]:
    """record_path without extension, e.g. raw/p00/p00000/p00000_s00. Returns beats and hours."""
    ann = wfdb.rdann(str(record_path), "atr")
    hdr = wfdb.rdheader(str(record_path))
    beats = beats_from_annotation(ann.sample, ann.symbol, ann.aux_note)
    return beats, hdr.sig_len / hdr.fs / 3600.0


def intervals_from_beats(beats: pd.DataFrame, fs: int = FS) -> pd.DataFrame:
    """One row per interval within a segment, tagged by the classes of its start and end beats."""
    if len(beats) < 2:
        return pd.DataFrame(columns=["rr_s", "start_cls", "end_cls", "in_af", "tally"])
    s = beats["sample"].to_numpy()
    c = beats["cls"].to_numpy()
    af = beats["in_af"].to_numpy()
    rr = np.diff(s) / fs
    out = pd.DataFrame({"rr_s": rr, "start_cls": c[:-1], "end_cls": c[1:], "in_af": af[:-1] | af[1:]})
    out["tally"] = (out.start_cls != "Q") & (out.end_cls != "Q") & (out.rr_s > RR_MIN_S) & (out.rr_s < RR_MAX_S)
    if len(beats) < MIN_BEATS_FOR_INTERVALS:        # legacy: segment too short for the filter reference
        out["tally"] = False
    return out


def analysed_hours(beats: pd.DataFrame, fs: int = FS) -> float:
    """Legacy definition: first to last classified (non-Q) beat of the segment."""
    s = beats.loc[beats["cls"] != "Q", "sample"].to_numpy()
    return float(s[-1] - s[0]) / fs / 3600.0 if len(s) > 1 else 0.0


def interval_category(df: pd.DataFrame) -> pd.Series:
    """Categories used in Tables 4.2 and RO1: PAC coupling, pause after PAC, PVC coupling, normal."""
    cat = pd.Series("other", index=df.index, dtype="object")
    cat[(df.start_cls == "N") & (df.end_cls == "N")] = "normal"
    cat[df.end_cls == "V"] = "pvc_coupling"
    cat[df.start_cls == "S"] = "pause_after_pac"
    cat[df.end_cls == "S"] = "pac_coupling"      # wins over pause for S-S pairs (a run)
    return cat


def longest_run(cls: np.ndarray, symbol: str = "S") -> int:
    best = cur = 0
    for c in cls:
        cur = cur + 1 if c == symbol else 0
        best = max(best, cur)
    return best


def build_patient(pid: str, raw_root: Path) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Read every segment of one patient. Returns (beats, intervals, summary dict)."""
    pdir = raw_root / pid[:3] / pid
    beat_parts, int_parts, hours, rec_hours, run = [], [], 0.0, 0.0, 0
    for seg in range(MAX_SEGMENTS):
        rec = pdir / f"{pid}_s{seg:02d}"
        if not rec.with_suffix(".hea").exists() or not rec.with_suffix(".atr").exists():
            break                                    # legacy: stop at the first missing segment
        b, h = read_segment(rec)
        if len(b) < 2:
            continue
        hours += analysed_hours(b)
        rec_hours += h
        run = max(run, longest_run(b["cls"].to_numpy()))
        b.insert(0, "segment", seg)
        iv = intervals_from_beats(b)
        iv.insert(0, "segment", seg)
        beat_parts.append(b)
        int_parts.append(iv)
    if not beat_parts:
        beats = pd.DataFrame(columns=["segment", "sample", "cls", "in_af"])
        ivs = pd.DataFrame(columns=["segment", "rr_s", "start_cls", "end_cls", "in_af", "tally", "category"])
    else:
        beats = pd.concat(beat_parts, ignore_index=True)
        ivs = pd.concat(int_parts, ignore_index=True)
        ivs["category"] = interval_category(ivs)
    summ = summarise(pid, beats, hours, run)
    summ["record_hours"] = rec_hours
    summ["analysable"] = is_analysable(summ)
    return beats, ivs, summ


def summarise(pid: str, beats: pd.DataFrame, hours: float, longest_s_run: int) -> dict:
    n = beats["cls"].value_counts()
    pac = int(n.get("S", 0))
    rate = pac / hours if hours else np.nan
    daily = rate * 24
    return {
        "patient": pid, "hours": hours, "n_segments": int(beats["segment"].nunique()),
        "n_N": int(n.get("N", 0)), "n_S": pac, "n_V": int(n.get("V", 0)), "n_Q": int(n.get("Q", 0)),
        "pac_per_hour": rate, "pac_per_day": daily, "longest_pac_run": longest_s_run,
        "esvea_primary": bool(daily >= ESVEA_PRIMARY_PER_DAY),
        "esvea_secondary": bool(rate >= ESVEA_SECONDARY_PER_HOUR),
        "esvea_binici_rate_or_run": bool(rate >= ESVEA_SECONDARY_PER_HOUR or longest_s_run >= BINICI_RUN_BEATS),
    }


def write_patient(pid: str, beats: pd.DataFrame, ivs: pd.DataFrame, out: Path) -> None:
    for name, df in (("beats", beats), ("intervals", ivs)):
        d = out / name
        d.mkdir(parents=True, exist_ok=True)
        df.to_parquet(d / f"{pid}.parquet", index=False)
