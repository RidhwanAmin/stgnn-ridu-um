"""
Beat-retention feasibility test on RAW watch files, including segments excluded
from the labelled release. Read-only on all inputs. Prints and saves aggregates only.
Settings and pass rule: methodology/Pulsewatch_Beat_Retention_Precheck_Config.md

  * Peaks: one detector for every segment (signal_proc bandpass + Elgendi), because
    excluded segments have no .pt. Labelled segments are also scored with the
    authors' .pt peaks as a bridge to the earlier test.
  * Lag: fitted per session on alternating LABELLED segments only (-3..+3 s, 0.02 s
    steps), never on the segments being scored. Sessions need >=4 labelled segments.
  * Scored: remaining labelled segments and all other segments of those sessions.
  * Match: one-to-one within +-100 ms after lag, closest pairs first. Beats landing
    within 1 s of the PPG segment edges are dropped.
  * Interval (secondary): consecutive ECG beats matched to adjacent PPG peaks.
  * Motion: SD of ACC magnitude (m/s^2) in a 2 s window centred on the beat.
  * Control: the segment's own PPG and ACC, with ECG beats from a segment in a
    different session of the same subject (chance level under the same motion).
  * Session gate: labelled held-out match must exceed its control.
  * Skip counts are written before any scoring. No model is fitted.

Usage: python -B beat_retention_raw_test.py [--smoke]
"""
import collections
import csv
import io
import json
import multiprocessing
import os
import pickle
import random
import re
import sys
import tarfile
import zipfile

import numpy as np
import scipy.io as sio

ROOT = r"C:\Users\Cerdas UTP\Documents\ridhwan\synapse"
sys.path.insert(0, ROOT)
from pulsewatch.mat_table import read_aligned_mat
from signal_proc import bandpass_ppg, detect_ppg_peaks

RAW_DIR = os.path.join(ROOT, r"synapse_data\raw_watch_8subj")
ALIGNED = os.path.join(ROOT, r"synapse_data\ecg\Aligned_ECG_LinearInterp")
LABELS = os.path.join(ROOT, r"synapse_data\03_Labels")
PT_ROOT = os.path.join(ROOT, r"synapse_data\untar\PPG_Elgendi_30sec_HR_ACC_pt")
ECG_ROOTS = [os.path.join(ROOT, r"build\ecg_fresh\Filtered_ECG_Peaks"),
             os.path.join(ROOT, r"synapse_data\ecg\Filtered_ECG_Peaks")]
OUT = os.path.join(ROOT, r"build\beat_retention_raw_results.json")
OUT_SKIPS = os.path.join(ROOT, r"build\beat_retention_raw_skipcounts.json")
ALIGNED_SUFFIX = "_final_align_output_LinearInterp.mat"

UIDS = ["017", "044", "055", "075", "083", "098", "109", "110"]
SMOKE_UIDS = ["055", "083"]
FS_PPG, FS_ECG, SEG_LEN = 50, 250, 1500
TOL = 0.10
LAGS = np.arange(-3, 3.0001, 0.02)
MIN_LABELLED = 4
MAX_SESSIONS = 300
SEED = 11
N_BOOT = 2000
BIN_EDGES = [0, 0.05, 0.2, 0.5, 1.0, np.inf]
BIN_NAMES = ["<0.05", "0.05-0.2", "0.2-0.5", "0.5-1", ">=1"]
TOP_BINS = ["0.5-1", ">=1"]
MIN_BIN_BEATS, MIN_BIN_SUBJECTS, MIN_SUBJECT_BEATS = 500, 3, 50
GROUPS = ["labelled", "excluded", "noise_3", "no_label"]
BEAT, INTERVAL, PEAK = 0, 1, 2


class _Stub:
    def __init__(self, *a):
        pass


class _Unpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module.startswith("torch"):
            return lambda *a, **k: None
        return super().find_class(module, name)

    def persistent_load(self, pid):
        return _Stub()


def pt_peaks(uid, stem):
    path = os.path.join(PT_ROOT, uid, stem + "_ppg_pk_HR.pt")
    if not os.path.exists(path):
        return None
    z = zipfile.ZipFile(io.BytesIO(open(path, "rb").read()))
    name = [n for n in z.namelist() if n.endswith("data.pkl")][0]
    d = _Unpickler(io.BytesIO(z.read(name))).load()
    return np.sort(np.asarray(d["new_PPG_peak_loc_Elgendi"]).ravel().astype(float)) / FS_PPG


def load_labels(uid):
    out = {}
    with open(os.path.join(LABELS, f"{uid}_final_attemp_4_1_Dong.csv"), encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            try:
                out[re.sub(r"\.txt$", "", row["table_file_name"])] = int(float(row["final_AF_GT_20230921"]))
            except (ValueError, TypeError):
                pass
    return out


def group_of(code):
    if code is None:
        return "no_label"
    if code in (0, 1, 2):
        return "labelled"
    if code == 3:
        return "noise_3"
    return "excluded"


def read_signal(tar, member):
    """Return the data column of a raw watch .txt (1 column, or column 2 of 2-3)."""
    rows = [re.split(r"[,\s]+", l.strip()) for l in
            tar.extractfile(member).read().decode("latin1").splitlines() if l.strip()]
    ncol = collections.Counter(len(r) for r in rows).most_common(1)[0][0]
    col = 0 if ncol == 1 else 1
    return np.array([float(r[col]) for r in rows if len(r) == ncol], dtype=np.float64)


class EcgPeaks:
    def __init__(self):
        self.cache = {}

    def get(self, patch, hour):
        key = (patch, hour)
        if key not in self.cache:
            self.cache[key] = None
            for root in ECG_ROOTS:
                fn = os.path.join(root, patch, f"ECG_Billal_peak_1_hr_{patch}_seg_{hour:03d}.mat")
                if os.path.exists(fn):
                    self.cache[key] = np.asarray(sio.loadmat(fn)["Billal_ECG_peak_1_hr_this"]).ravel().astype(np.int64)
                    break
        return self.cache[key]


def nearest_hit(te, tp, lag):
    """Vectorised nearest-peak test, used only for the lag search."""
    if len(tp) == 0:
        return np.zeros(len(te), dtype=bool)
    q = te + lag
    j = np.searchsorted(tp, q)
    a = np.clip(j - 1, 0, len(tp) - 1)
    b = np.clip(j, 0, len(tp) - 1)
    return np.minimum(np.abs(q - tp[a]), np.abs(q - tp[b])) <= TOL


def fit_lag(pairs):
    scores = [np.mean([nearest_hit(te, tp, l).mean() for te, tp in pairs]) for l in LAGS]
    return float(LAGS[int(np.argmax(scores))])


def one_to_one(te, tp, lag):
    """Return, per ECG beat, the index of its matched PPG peak or -1. Closest pairs first."""
    out = np.full(len(te), -1, dtype=np.int64)
    if len(tp) == 0:
        return out
    q = te + lag
    lo = np.searchsorted(tp, q - TOL, side="left")
    hi = np.searchsorted(tp, q + TOL, side="right")
    cand = [(abs(q[k] - tp[p]), k, p) for k in range(len(q)) for p in range(lo[k], hi[k])]
    used = set()
    for _, k, p in sorted(cand):
        if out[k] < 0 and p not in used:
            out[k] = p
            used.add(p)
    return out


def motion_at(acc, t):
    i = int(round(t * FS_PPG))
    w = acc[max(0, i - FS_PPG):min(len(acc), i + FS_PPG)]
    return float(np.std(w)) if w.size >= FS_PPG else np.nan


def score(rec, sub, ses, grp, kind, te, tp, acc, lag):
    """Append (subject, session, group, kind, unit, motion, hit) rows."""
    m = one_to_one(te, tp, lag)
    t = te + lag
    ok = (t >= 1) & (t <= 29)
    for k in np.where(ok)[0]:
        rec.append((sub, ses, grp, kind, BEAT, motion_at(acc, t[k]), m[k] >= 0))
    for k in range(len(te) - 1):
        if ok[k] and ok[k + 1]:
            hit = m[k] >= 0 and m[k + 1] == m[k] + 1
            rec.append((sub, ses, grp, kind, INTERVAL, motion_at(acc, (t[k] + t[k + 1]) / 2), hit))
    claimed = set(m[m >= 0].tolist())
    for p, tt in enumerate(tp):
        if 1 <= tt <= 29:
            rec.append((sub, ses, grp, kind, PEAK, motion_at(acc, tt), p in claimed))


def load_subject(uid, rng, skips):
    """Phase 1: read and filter segments. No matching happens here."""
    labels = load_labels(uid)
    tar = tarfile.open(os.path.join(RAW_DIR, f"{uid}_final.tar"))
    ppg, acc = {}, {}
    for m in tar.getmembers():
        if not m.isfile():
            continue
        base = os.path.basename(m.name)
        if re.search(r"_ppg_\d+\.txt$", base):
            ppg[base[:-4]] = m
        elif re.search(r"_accel_\d+\.txt$", base):
            acc[base[:-4]] = m

    sessions = collections.defaultdict(list)
    for stem in sorted(ppg):
        sessions[stem.rsplit("_ppg_", 1)[0]].append(stem)
        skips["raw_segments|" + group_of(labels.get(stem))] += 1
    eligible = [s for s, v in sessions.items()
                if sum(group_of(labels.get(x)) == "labelled" for x in v) >= MIN_LABELLED]
    for s, v in sessions.items():
        if s not in set(eligible):
            for x in v:
                skips["session_under_4_labelled|" + group_of(labels.get(x))] += 1
    skips["sessions_total"] += len(sessions)
    skips["sessions_eligible"] += len(eligible)
    rng.shuffle(eligible)
    for s in eligible[MAX_SESSIONS:]:
        for x in sessions[s]:
            skips["session_over_cap|" + group_of(labels.get(x))] += 1

    ecg = EcgPeaks()
    loaded = []
    for s in eligible[:MAX_SESSIONS]:
        segs = []
        for stem in sessions[s]:
            grp = group_of(labels.get(stem))

            def skip(reason):
                skips[reason + "|" + grp] += 1

            path = os.path.join(ALIGNED, uid, stem + ALIGNED_SUFFIX)
            if not os.path.exists(path):
                skip("no_aligned_file")
                continue
            try:
                r = read_aligned_mat(path)
            except Exception:
                skip("aligned_unreadable")
                continue
            if not r.get("patch_id") or None in (r.get("start"), r.get("end"), r.get("hour")):
                skip("no_alignment_values")
                continue
            if r["start"] > r["end"]:
                skip("hour_straddle")
                continue
            if r.get("contain_empty"):
                skip("contain_empty")
                continue
            pk = ecg.get(r["patch_id"], r["hour"])
            if pk is None:
                skip("ecg_not_local")
                continue
            te = (pk[(pk >= r["start"]) & (pk <= r["end"])] - r["start"]) / FS_ECG
            acc_stem = stem.replace("_ppg_", "_accel_")
            if len(te) < 5:
                skip("under_5_ecg_beats")
                continue
            if acc_stem not in acc:
                skip("no_acc_file")
                continue
            try:
                x = read_signal(tar, ppg[stem])
                a = read_signal(tar, acc[acc_stem])
            except Exception:
                skip("raw_unreadable")
                continue
            if x.size != SEG_LEN or a.size != SEG_LEN:
                skip("not_1500_samples")
                continue
            tp = detect_ppg_peaks(bandpass_ppg(x)) / FS_PPG
            segs.append(dict(stem=stem, group=grp, te=te, tp=tp, acc=a.astype(np.float32)))
        if sum(g["group"] == "labelled" for g in segs) >= MIN_LABELLED:
            loaded.append(segs)
            skips["sessions_loaded"] += 1
            for g in segs:
                skips["kept|" + g["group"]] += 1
        else:
            skips["session_under_4_after_rules"] += 1
            for g in segs:
                skips["dropped_with_session|" + g["group"]] += 1
    return loaded


def score_subject(sub, uid, loaded, rng, rec, session_rows, bridge):
    """Phase 2: lag fit, matching and control."""
    for i, segs in enumerate(loaded):
        lab = [g for g in segs if g["group"] == "labelled"]
        fit, held = lab[0::2], lab[1::2]
        lag = fit_lag([(g["te"], g["tp"]) for g in fit])
        others = [g for j, o in enumerate(loaded) if j != i for g in o]
        if not others:
            continue

        pf = [(g["te"], pt_peaks(uid, g["stem"])) for g in fit]
        ph = [pt_peaks(uid, g["stem"]) for g in held]
        if all(p[1] is not None and len(p[1]) for p in pf) and all(p is not None and len(p) for p in ph):
            lag_pt = fit_lag(pf)
            for g, tp_pt in zip(held, ph):
                keep = (g["te"] >= 1) & (g["te"] <= 29)
                bridge[sub][0] += int(keep.sum())
                bridge[sub][1] += int((one_to_one(g["te"], g["tp"], lag)[keep] >= 0).sum())
                bridge[sub][2] += int((one_to_one(g["te"], tp_pt, lag_pt)[keep] >= 0).sum())

        ses = len(session_rows)
        start = len(rec)
        for g in held + [x for x in segs if x["group"] != "labelled"]:
            grp = GROUPS.index(g["group"])
            score(rec, sub, ses, grp, 0, g["te"], g["tp"], g["acc"], lag)
            score(rec, sub, ses, grp, 1, rng.choice(others)["te"], g["tp"], g["acc"], lag)
        rows = [r for r in rec[start:] if r[2] == 0 and r[4] == BEAT]
        real = [r[6] for r in rows if r[3] == 0]
        ctrl = [r[6] for r in rows if r[3] == 1]
        passed = bool(real and ctrl and np.mean(real) > np.mean(ctrl))
        session_rows.append((sub, lag, passed))


def bin_index(motion, edges):
    return np.clip(np.searchsorted(edges, motion, side="right") - 1, 0, len(edges) - 2)


def rate(hit):
    return float(np.mean(hit)) if len(hit) else float("nan")


def table(d, edges, names, label):
    """Print beat, interval and unmatched-peak results per bin for rows d."""
    print(f"  {label}")
    for b, name in enumerate(names):
        idx = bin_index(d["motion"], edges) == b
        def part(kind, unit):
            return d["hit"][idx & (d["kind"] == kind) & (d["unit"] == unit)]
        rb, cb, ri, ci, rp = part(0, BEAT), part(1, BEAT), part(0, INTERVAL), part(1, INTERVAL), part(0, PEAK)
        if len(rb):
            print("    %-16s beats=%-8d match=%.3f control=%.3f excess=%+.3f | intervals=%-8d kept=%.3f control=%.3f | PPG peaks unmatched=%.3f"
                  % (name, len(rb), rate(rb), rate(cb), rate(rb) - rate(cb), len(ri), rate(ri), rate(ci), 1 - rate(rp)))


def select(d, mask):
    return {k: v[mask] for k, v in d.items()}


def counts_by_subject_bin(d, n_sub):
    """Return arrays [subject, bin, (n_real, hit_real, n_ctrl, hit_ctrl)] for beats."""
    out = np.zeros((n_sub, len(BIN_NAMES), 4))
    beats = d["unit"] == BEAT
    bins = bin_index(d["motion"], np.array(BIN_EDGES))
    for s in range(n_sub):
        for b in range(len(BIN_NAMES)):
            m = beats & (d["subject"] == s) & (bins == b)
            r, c = m & (d["kind"] == 0), m & (d["kind"] == 1)
            out[s, b] = [r.sum(), d["hit"][r].sum(), c.sum(), d["hit"][c].sum()]
    return out


def excess(c):
    with np.errstate(invalid="ignore", divide="ignore"):
        return c[..., 1] / c[..., 0] - c[..., 3] / c[..., 2]


def evaluate(d, n_sub, bridge, label):
    """Apply the locked pass rule to rows d."""
    c = counts_by_subject_bin(d, n_sub)
    rng = np.random.default_rng(SEED)
    boots = rng.integers(0, n_sub, size=(N_BOOT, n_sub))
    res = dict(bins={})
    print(f"\n=== pass rule, {label} ===")
    for b, name in enumerate(BIN_NAMES):
        n_each = c[:, b, 0]
        enough = n_each.sum() >= MIN_BIN_BEATS and (n_each >= MIN_SUBJECT_BEATS).sum() >= MIN_BIN_SUBJECTS
        ex = excess(c[:, b].sum(0))
        sims = excess(c[boots, b].sum(1))
        lo, hi = np.nanpercentile(sims, [2.5, 97.5]) if np.isfinite(sims).any() else (np.nan, np.nan)
        res["bins"][name] = dict(beats=int(n_each.sum()), subjects_50plus=int((n_each >= MIN_SUBJECT_BEATS).sum()),
                                 enough=bool(enough), excess=float(ex), ci95=[float(lo), float(hi)])
        print("  %-9s beats=%-8d subjects>=50=%d enough=%-5s excess=%+.3f 95%% CI [%+.3f, %+.3f]"
              % (name, n_each.sum(), (n_each >= MIN_SUBJECT_BEATS).sum(), bool(enough), ex, lo, hi))
    top = [res["bins"][b] for b in TOP_BINS if res["bins"][b]["enough"]]
    c1 = bool(top) and all(t["ci95"][0] > 0 for t in top)

    falls = []
    for s in range(n_sub):
        elig = [b for b in range(len(BIN_NAMES)) if c[s, b, 0] >= MIN_SUBJECT_BEATS and c[s, b, 2] > 0]
        if len(elig) >= 2:
            lo_ex, hi_ex = excess(c[s, elig[0]]), excess(c[s, elig[-1]])
            falls.append(bool(hi_ex < lo_ex))
            print("  S%d lowest bin %s excess=%+.3f, highest bin %s excess=%+.3f"
                  % (s + 1, BIN_NAMES[elig[0]], lo_ex, BIN_NAMES[elig[-1]], hi_ex))
    c2 = len(falls) >= 3 and np.mean(falls) >= 2 / 3

    tot = np.sum(bridge, axis=0)
    pooled = abs(tot[1] - tot[2]) / tot[0] if tot[0] else float("nan")
    subj = {f"S{s + 1}": abs(b[1] - b[2]) / b[0] for s, b in enumerate(bridge) if b[0] >= MIN_SUBJECT_BEATS}
    c3 = bool(tot[0]) and pooled <= 0.05 and all(v <= 0.10 for v in subj.values())
    print("  bridge beats=%d project=%.3f authors=%.3f pooled_diff=%.3f per-subject max=%.3f"
          % (tot[0], tot[1] / max(tot[0], 1), tot[2] / max(tot[0], 1), pooled, max(subj.values()) if subj else float("nan")))
    print("  criterion 1 (above chance at high motion): %s" % c1)
    print("  criterion 2 (falls within subjects): %s (%d of %d subjects)" % (c2, sum(falls), len(falls)))
    print("  criterion 3 (detector comparable): %s" % c3)
    print("  PASS: %s" % (c1 and c2 and c3))
    res.update(c1=bool(c1), c2=bool(c2), c3=bool(c3), passed=bool(c1 and c2 and c3),
               falls=[int(sum(falls)), len(falls)], bridge=dict(beats=int(tot[0]), project=float(tot[1] / max(tot[0], 1)),
                                                               authors=float(tot[2] / max(tot[0], 1)), pooled_diff=float(pooled),
                                                               per_subject_diff=subj))
    return res


def main():
    smoke = "--smoke" in sys.argv[1:]
    uids = SMOKE_UIDS if smoke else UIDS
    rng = random.Random(SEED)

    skips = collections.Counter()
    data = {}
    for n, uid in enumerate(uids):
        data[uid] = load_subject(uid, rng, skips)
        print(f"loaded subject {n + 1}/{len(uids)}", flush=True)
    print("\nskip counts (before scoring):")
    for k, v in sorted(skips.items()):
        print("  %-42s %d" % (k, v))
    if not smoke:
        with open(OUT_SKIPS, "w") as f:
            json.dump(dict(sorted(skips.items())), f, indent=1)

    rec, session_rows = [], []
    bridge = [[0, 0, 0] for _ in uids]
    for n, uid in enumerate(uids):
        score_subject(n, uid, data[uid], rng, rec, session_rows, bridge)
        print(f"scored subject {n + 1}/{len(uids)}", flush=True)
    del data

    arr = np.array(rec, dtype=np.float64)
    del rec
    keep = np.isfinite(arr[:, 5])
    arr = arr[keep]
    d = dict(subject=arr[:, 0].astype(int), session=arr[:, 1].astype(int), group=arr[:, 2].astype(int),
             kind=arr[:, 3].astype(int), unit=arr[:, 4].astype(int), motion=arr[:, 5], hit=arr[:, 6].astype(bool))
    gate = np.array([r[2] for r in session_rows])
    gated = select(d, gate[d["session"]])
    print("\nsessions scored=%d passing gate=%d" % (len(session_rows), gate.sum()))
    for s in range(len(uids)):
        ls = [r[1] for r in session_rows if r[0] == s]
        ps = [r[2] for r in session_rows if r[0] == s]
        if ls:
            print("  S%d sessions=%d passing=%d lag IQR=[%.2f, %.2f]" % (s + 1, len(ls), sum(ps), *np.percentile(ls, [25, 75])))

    edges = np.array(BIN_EDGES)
    real_gated = gated["motion"][(gated["kind"] == 0) & (gated["unit"] == BEAT)]
    q = np.unique(np.percentile(real_gated, [0, 20, 40, 60, 80, 100]))
    q_edges = np.concatenate([[0], q[1:-1], [np.inf]])
    q_names = ["Q%d (%.3f-%.3f)" % (i + 1, q_edges[i], q_edges[i + 1]) for i in range(len(q_edges) - 1)]

    for name, sub in (("GATED sessions", gated), ("ALL sessions", d)):
        print(f"\n##### {name} #####")
        print(" fixed bins, m/s^2")
        table(sub, edges, BIN_NAMES, "all scored groups")
        for g, grp in enumerate(GROUPS):
            part = select(sub, sub["group"] == g)
            if len(part["hit"]):
                table(part, edges, BIN_NAMES, grp)
        print(" quintile bins (secondary)")
        table(sub, q_edges, q_names, "all scored groups")

    print("\n##### per subject, gated, beat excess by fixed bin #####")
    cg = counts_by_subject_bin(gated, len(uids))
    for s in range(len(uids)):
        print("  S%d " % (s + 1) + "  ".join("%s:%+.2f(n=%d)" % (BIN_NAMES[b], excess(cg[s, b]), cg[s, b, 0])
                                             for b in range(len(BIN_NAMES)) if cg[s, b, 0]))

    primary = evaluate(gated, len(uids), bridge, "PRIMARY: gated sessions")
    sensitivity = evaluate(d, len(uids), bridge, "sensitivity: all sessions")
    if not smoke:
        with open(OUT, "w") as f:
            json.dump(dict(primary=primary, sensitivity=sensitivity, sessions=len(session_rows),
                           sessions_gated=int(gate.sum())), f, indent=1)
        print("\nsaved", OUT)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
