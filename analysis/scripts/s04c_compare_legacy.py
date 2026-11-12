"""Compare legacy incentia_ro1_prelim.analyse_patient with the new esvea pipeline, per patient.
Usage: python compare_legacy.py <analysis_dir> <raw_root> pid [pid ...]"""
import importlib.util, sys, warnings
from pathlib import Path
warnings.filterwarnings("ignore")

analysis, raw = Path(sys.argv[1]), Path(sys.argv[2])
spec = importlib.util.spec_from_file_location("legacy", analysis / "legacy/ro1_preliminary/incentia_ro1_prelim.py")
leg = importlib.util.module_from_spec(spec); spec.loader.exec_module(leg)
from esvea.ingest.tables import build_patient
from esvea.ro1.retention import apply_filter, removal_counts

names = {"coupling interval ending at PAC (S)": "pac_coupling", "pause after PAC (S)": "pause_after_pac",
         "coupling interval ending at PVC (V)": "pvc_coupling", "normal-to-normal (N to N)": "normal"}
bad = 0
for p in sys.argv[3:]:
    pid = int(p.lstrip("p"))
    S, R = leg.analyse_patient(pid, str(raw))
    _, ivs, s = build_patient(f"p{pid:05d}", raw)
    for thr in (0.10, 0.20, 0.30):
        rc = removal_counts(ivs, apply_filter(ivs, thr)).set_index("category")
        for r in R:
            if r["threshold_pct"] == round(thr * 100):
                c = names[r["interval"]]
                if (rc.loc[c, "n"], rc.loc[c, "removed"]) != (r["n"], r["rejected"]):
                    bad += 1; print("DIFF", p, thr, c, (r["n"], r["rejected"]), tuple(rc.loc[c]))
    checks = {"hours": (S["hours"], s["hours"]), "n_S": (S["n_S"], s["n_S"]), "run": (S["longest_S_run"], s["longest_pac_run"]),
              "binici": (S["esvea_any"], s["esvea_binici_rate_or_run"])}
    for k, (a, b) in checks.items():
        if abs(float(a) - float(b)) > 1e-9:
            bad += 1; print("DIFF", p, k, a, b)
    print(p, f"hours {s['hours']:.3f}", f"S {s['n_S']}", "ok" if not bad else "")
print("TOTAL DIFFS", bad)
