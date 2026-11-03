# Check E2: are Pulsewatch timestamps continuous across days?

**For:** Ridhwan (to run on your local Pulsewatch files)
**Why:** review issue #2. The epoch scale of the ST-GNN aggregates "across windows within the day", but Icentia11k segments are about 70 minutes long with no clock time. The draft E2 trains the epoch scale on pseudo-days. If Pulsewatch recordings carry real, continuous timestamps across days, the proposal can also say "real within-day ordering is tested on timestamped Pulsewatch recordings at window level" (optional E2 clause, +14 words).
**Draft text waiting on this:** the optional clause under E2a in `drafts/proposal_revisions_draft.md`.
**Time needed:** about 30 minutes.

---

## 1. What is already known

From `analyses/pulsewatch_retention/Pulsewatch_Beat_Retention_Data_Check.md`:

- `PPG_filt_csv` column 0 in the segment `.pt` files "looks like a UNIX millisecond timestamp with a 20 ms step".
- That was checked **within** segments only. Nobody has checked whether timestamps line up **across** segments and days for the same participant.
- `ECG_time_1_hr_this` is on a different scale, so the ECG clock cannot be used. Use the watch timestamps only.
- Raw watch files (`*_ppg_*.txt`, `*_accel_*.txt`) are in `synapse_data\raw_watch_8subj` for 8 subjects; it is not known whether they carry timestamps.

---

## 2. Questions to answer

| # | Question | Why it matters |
|---|---|---|
| Q1 | Do segment timestamps convert to plausible calendar dates (the study years, not 1970)? | Confirms they are real clock times |
| Q2 | Within one participant, do segments span several days, in time order, without overlaps? | Needed for day-level ordering |
| Q3 | What is the time zone? UNIX time is UTC; the study site is in Massachusetts (US Eastern) | Time-of-day blocks are wrong by 4 to 5 hours if the zone is wrong |
| Q4 | How are recordings spread over the 24 hours, in local time? | Shows whether daytime blocks (06–12, 12–18, 18–24) have any data |
| Q5 | Is it the same for labelled, excluded and no-label segments? | Labelled segments alone may be biased towards clean, low-motion time |

---

## 3. Script

Save as `build/check_pulsewatch_timestamps.py` (outside the data folder) and run with `python -I build/check_pulsewatch_timestamps.py <segment_pt_folder> <out_csv>`. Edit `SUBJECT_REGEX` to match your file names first.

```python
"""Check whether Pulsewatch segment timestamps are real and continuous across days."""
import re, sys, pathlib
import pandas as pd
import torch

SEG_DIR = pathlib.Path(sys.argv[1])        # e.g. synapse_data/untar/PPG_Elgendi_30sec_HR_ACC_pt
OUT_CSV = pathlib.Path(sys.argv[2])
SUBJECT_REGEX = r"^(\d{3})"               # EDIT: how the subject ID appears in the file name
TZ = "America/New_York"                    # study site time zone (check Q3)

rows = []
for f in sorted(SEG_DIR.rglob("*.pt")):
    m = re.search(SUBJECT_REGEX, f.name)
    if not m:
        continue
    try:
        d = torch.load(f, map_location="cpu", weights_only=False)
        t = d["PPG_filt_csv"][:, 0]
        t = t.numpy() if hasattr(t, "numpy") else t
    except Exception as e:
        rows.append({"file": f.name, "subject": m.group(1), "error": str(e)})
        continue
    rows.append({"file": f.name, "subject": m.group(1),
                 "t_start_ms": float(t[0]), "t_end_ms": float(t[-1]),
                 "n": len(t), "step_ms": float(pd.Series(t).diff().median())})

df = pd.DataFrame(rows)
df.to_csv(OUT_CSV, index=False)
ok = df.dropna(subset=["t_start_ms"]).copy()
ok["start_utc"] = pd.to_datetime(ok["t_start_ms"], unit="ms", utc=True)
ok["start_local"] = ok["start_utc"].dt.tz_convert(TZ)

print("Files read:", len(df), " errors:", df.get("error", pd.Series()).notna().sum())
print("Q1 date range (UTC):", ok["start_utc"].min(), "to", ok["start_utc"].max())

g = ok.sort_values("t_start_ms").groupby("subject")
summary = g.agg(segments=("file", "size"),
                first=("start_local", "min"), last=("start_local", "max"),
                days=("start_local", lambda s: s.dt.date.nunique()))
ok["gap_s"] = g["t_start_ms"].diff() / 1000
ok["prev_end"] = g["t_end_ms"].shift()
summary["overlaps"] = (ok["t_start_ms"] < ok["prev_end"]).groupby(ok["subject"]).sum()
summary["median_gap_s"] = ok.groupby("subject")["gap_s"].median()
print("\nQ2 per subject:\n", summary.to_string())

ok["block"] = pd.cut(ok["start_local"].dt.hour, [0, 6, 12, 18, 24], right=False,
                     labels=["00-06", "06-12", "12-18", "18-24"])
print("\nQ4 share of segments by local block:\n",
      ok["block"].value_counts(normalize=True).sort_index().round(3).to_string())
print("\nQ4 by subject:\n",
      pd.crosstab(ok["subject"], ok["block"], normalize="index").round(2).to_string())
```

**Q5:** join the output CSV with `03_Labels` (`table_file_name`, `final_AF_GT_20230921`) and repeat the Q4 table for labelled (codes 0, 1, 2), excluded (negative codes) and no-label segments. If excluded segments have no `.pt` files, use the raw `*_ppg_*.txt` files for those, if they contain a time column (check one file by eye first).

**Q3 (time zone):** look for a night-time dip in Q4. Watch wear and clean PPG should be highest at night in local time. If the busiest block is 04–10 UTC, the timestamps are UTC and the Eastern conversion is right. Also check the Pulsewatch Synapse wiki for a time-zone statement.

---

## 4. Decision rule

| Result | Decision |
|---|---|
| Q1 plausible dates **and** Q2 at least 5 subjects span 3 or more days, in order, with no overlaps **and** Q3 time zone settled | **Pass.** Add the optional E2 clause (+14 words; take them from the E8 removal alternative or another trim). |
| Dates plausible but only within single sessions, or time zone unclear | **Fail for E2.** Keep E2 as drafted (pseudo-days only). |
| Dates implausible (1970, or not in the study years) | **Fail.** Note it in the data check file; do not use Pulsewatch time of day anywhere. |

---

## 5. Fill in and send back

| Item | Result |
|---|---|
| Files read / errors | |
| Date range (UTC) | |
| Subjects spanning ≥ 3 days, in order, no overlaps | __ of __ |
| Median gap between segments | |
| Time zone (and how determined) | |
| Share of segments by block 00–06 / 06–12 / 12–18 / 18–24 (all) | |
| Same, labelled vs excluded vs no-label | |
| Decision (pass / fail) | |

## 6. Side benefit

If this passes, the Q4 table is real smartwatch coverage by time of day. That supports the RO3 fallback ("coverage modelled from Pulsewatch wear data", Section 3.9) and could check the night-weighted coverage assumption (Merschel & Reinhardt, 2022) used in Appendix C and RO4a.

## 7. Do not claim
- That Pulsewatch reflects Garmin coverage: it is a Samsung watch in a different population.
- Any time-of-day ectopy pattern from Pulsewatch: labels are 30-second windows with PAC and PVC merged.
