#!/usr/bin/env python3
"""
Preliminary RO1 analysis on Icentia11k (beat annotations only, no signal download).

Produces, for a random subset of patients:
  1. Retention by beat class under a percent-deviation RR filter (Karlsson et al., 2012 style)
     at several thresholds: share of intervals around PAC (S), PVC (V) and normal (N) beats removed.
  2. ESVEA prevalence: patients meeting >=30 S beats/hour, >=480 S beats/day (rate extrapolated),
     or any run of >=20 consecutive S beats (Binici et al., 2010).

Icentia11k beat symbols: N normal, S PAC (supraventricular), V PVC, Q unclassifiable.
Q beats, and intervals touching a Q beat, are excluded from all truth counts.

Usage
  pip install wfdb numpy pandas
  # stream annotations from PhysioNet (no full download needed):
  python icentia_ro1_prelim.py --n-patients 300 --out results
  # or point at a local copy of the dataset:
  python icentia_ro1_prelim.py --local-root /data/icentia11k --n-patients 300 --out results
  # check the code without network:
  python icentia_ro1_prelim.py --selftest
"""
import argparse, os, random, sys
import numpy as np
import pandas as pd

FS = 250                      # Icentia11k sampling rate (Hz)
PN_DIR = "icentia11k-continuous-ecg/1.0"
N_PATIENTS_TOTAL = 11000
MAX_SEGMENTS = 50
THRESHOLDS = [0.10, 0.15, 0.20, 0.25, 0.30]
REF_WINDOW = 5                # accepted intervals used as the reference


def record_dir(pid):
    return f"p{pid // 1000:02d}/p{pid:05d}"


def load_segment(pid, seg, local_root=None):
    import wfdb
    name = f"p{pid:05d}_s{seg:02d}"
    try:
        if local_root:
            ann = wfdb.rdann(os.path.join(local_root, record_dir(pid), name), "atr")
        else:
            ann = wfdb.rdann(name, "atr", pn_dir=f"{PN_DIR}/{record_dir(pid)}")
    except Exception:
        return None
    samples = np.asarray(ann.sample)
    symbols = np.asarray(ann.symbol)
    keep = np.isin(symbols, ["N", "S", "V", "Q"])
    return samples[keep], symbols[keep]


def deviation_filter(rr, thr):
    """Return boolean array: True = interval rejected.
    Reference = median of the last REF_WINDOW accepted intervals."""
    rejected = np.zeros(len(rr), dtype=bool)
    accepted = []
    for i, x in enumerate(rr):
        if len(accepted) < REF_WINDOW:
            accepted.append(x)
            continue
        ref = np.median(accepted[-REF_WINDOW:])
        if abs(x - ref) / ref > thr:
            rejected[i] = True
        else:
            accepted.append(x)
    return rejected


def analyse_segment(samples, symbols):
    """Per-interval table. Interval i ends at beat i+1.
    'role' = class of the beat ending the interval (coupling interval),
    'post' = class of the beat starting it (captures the compensatory pause)."""
    if len(samples) < REF_WINDOW + 3:
        return None
    rr = np.diff(samples) / FS
    end_sym = symbols[1:]
    start_sym = symbols[:-1]
    valid = (end_sym != "Q") & (start_sym != "Q") & (rr > 0.2) & (rr < 3.0)
    out = {"end": end_sym, "start": start_sym, "valid": valid}
    for thr in THRESHOLDS:
        out[f"rej_{int(thr*100)}"] = deviation_filter(rr, thr)
    return pd.DataFrame(out)


def longest_s_run(symbols):
    best = cur = 0
    for s in symbols:
        cur = cur + 1 if s == "S" else 0
        best = max(best, cur)
    return best


def analyse_patient(pid, local_root=None, loader=None):
    loader = loader or load_segment
    tables, n = [], {"N": 0, "S": 0, "V": 0, "Q": 0}
    hours, run = 0.0, 0
    for seg in range(MAX_SEGMENTS):
        res = loader(pid, seg, local_root)
        if res is None:
            if seg == 0:
                return None
            break
        samples, symbols = res
        if len(samples) < 2:
            continue
        for k in n:
            n[k] += int((symbols == k).sum())
        classified = symbols != "Q"
        if classified.sum() > 1:
            hours += (samples[classified][-1] - samples[classified][0]) / FS / 3600
        run = max(run, longest_s_run(symbols))
        t = analyse_segment(samples, symbols)
        if t is not None:
            tables.append(t)
    if not tables or hours <= 0:
        return None
    df = pd.concat(tables, ignore_index=True)
    df = df[df.valid]
    s_per_h = n["S"] / hours
    summary = {
        "pid": pid, "hours": hours, **{f"n_{k}": v for k, v in n.items()},
        "q_fraction": n["Q"] / max(1, sum(n.values())),
        "S_per_hour": s_per_h, "S_per_day_extrap": s_per_h * 24,
        "longest_S_run": run,
        "esvea_rate30": s_per_h >= 30,
        "esvea_day480": s_per_h * 24 >= 480,
        "esvea_run20": run >= 20,
    }
    summary["esvea_any"] = summary["esvea_rate30"] or summary["esvea_run20"]
    retention = []
    for thr in THRESHOLDS:
        col = f"rej_{int(thr*100)}"
        for label, mask in [
            ("coupling interval ending at PAC (S)", df.end == "S"),
            ("pause after PAC (S)", df.start == "S"),
            ("coupling interval ending at PVC (V)", df.end == "V"),
            ("normal-to-normal (N to N)", (df.end == "N") & (df.start == "N")),
        ]:
            sub = df[mask]
            retention.append({"pid": pid, "threshold_pct": int(thr*100), "interval": label,
                              "n": len(sub), "rejected": int(sub[col].sum())})
    return summary, retention


def run(pids, local_root, out, loader=None):
    os.makedirs(out, exist_ok=True)
    summaries, rets = [], []
    for i, pid in enumerate(pids, 1):
        r = analyse_patient(pid, local_root, loader)
        if r is None:
            print(f"[{i}/{len(pids)}] p{pid:05d}: not found, skipped", file=sys.stderr)
            continue
        summaries.append(r[0]); rets.extend(r[1])
        print(f"[{i}/{len(pids)}] p{pid:05d}: {r[0]['hours']:.1f} h, S/h {r[0]['S_per_hour']:.1f}", file=sys.stderr)
    S = pd.DataFrame(summaries); R = pd.DataFrame(rets)
    S.to_csv(os.path.join(out, "patients.csv"), index=False)
    R.to_csv(os.path.join(out, "retention_by_patient.csv"), index=False)

    # Table A: pooled share of intervals removed, by class and threshold
    A = R.groupby(["threshold_pct", "interval"])[["n", "rejected"]].sum().reset_index()
    A["removed_pct"] = 100 * A.rejected / A.n.clip(lower=1)
    A.to_csv(os.path.join(out, "tableA_removed_by_class.csv"), index=False)
    # Table A by ESVEA status (does filtering remove more in high-burden patients?)
    R2 = R.merge(S[["pid", "esvea_any"]], on="pid")
    A2 = R2.groupby(["threshold_pct", "esvea_any", "interval"])[["n", "rejected"]].sum().reset_index()
    A2["removed_pct"] = 100 * A2.rejected / A2.n.clip(lower=1)
    A2.to_csv(os.path.join(out, "tableA2_removed_by_esvea.csv"), index=False)

    # Table B: ESVEA prevalence
    n = len(S)
    def pct(c): return f"{int(S[c].sum())} ({100*S[c].mean():.1f}%)"
    B = pd.DataFrame([
        ["Patients analysed", str(n)],
        ["Median monitored hours (IQR)", f"{S.hours.median():.1f} ({S.hours.quantile(.25):.1f} to {S.hours.quantile(.75):.1f})"],
        ["Median unclassifiable beat fraction", f"{100*S.q_fraction.median():.1f}%"],
        ["Median PAC per hour (IQR)", f"{S.S_per_hour.median():.2f} ({S.S_per_hour.quantile(.25):.2f} to {S.S_per_hour.quantile(.75):.2f})"],
        [">= 30 PAC per hour", pct("esvea_rate30")],
        [">= 480 PAC per day (extrapolated)", pct("esvea_day480")],
        ["Any run of >= 20 PACs", pct("esvea_run20")],
        ["ESVEA (Binici: rate or run)", pct("esvea_any")],
    ], columns=["Measure", "Value"])
    B.to_csv(os.path.join(out, "tableB_esvea_prevalence.csv"), index=False)

    print("\n=== Table A: intervals removed by the deviation filter (pooled) ===")
    print(A.pivot(index="interval", columns="threshold_pct", values="removed_pct").round(1).to_string())
    print("\n=== Table B: ESVEA prevalence ===")
    print(B.to_string(index=False))
    print(f"\nCSV files written to {os.path.abspath(out)}")


def selftest():
    """Synthetic patients: sinus rhythm with injected PACs (short coupling, compensatory pause)."""
    rng = np.random.default_rng(0)
    def loader(pid, seg, _root):
        if seg >= 3:
            return None
        n = 4000
        rr = rng.normal(0.85, 0.03, n)
        sym = np.array(["N"] * n, dtype=object)
        pac_rate = 0.002 if pid % 2 else 0.03
        for i in range(10, n - 2):
            if rng.random() < pac_rate:
                sym[i] = "S"; rr[i - 1] *= 0.65; rr[i] *= 1.25
        sym[rng.random(n) < 0.02] = "Q"
        samples = np.concatenate([[0], np.cumsum(rr)]) * FS
        return samples[:-1].astype(int), sym
    run([1, 2, 3, 4], None, "selftest_out", loader)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--n-patients", type=int, default=300)
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--local-root", default=None, help="local Icentia11k root containing p00/, p01/, ...")
    ap.add_argument("--out", default="ro1_prelim_results")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest(); sys.exit(0)
    pids = random.Random(a.seed).sample(range(N_PATIENTS_TOTAL), a.n_patients)
    run(sorted(pids), a.local_root, a.out)