# Track 1 analysis code (initial version, November 2026)

Icentia11k pipeline, RO1 (RQ1.2, H1, RQ1.3), the estimator equations (3.1 to 3.4) and coverage rules, the
Pulsewatch matching utilities and a first training simulator. The plan this code serves is
`drafts/Track1_Implementation_Runbook_S2_S3.md`.

## Setup

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev,adaptive]"
export ESVEA_DATA=/path/to/university/storage/esvea   # data never go in git
pytest -q                     # unit tests (no network)
pytest -q -m network          # one real Icentia11k segment from PhysioNet
```

## Order of runs (S2)

| Step | Command | Gate |
|---|---|---|
| 1 | copy `splits/P0.txt` (see `splits/README.md`) | committed |
| 2 | `python scripts/s01_draw_sets.py P3 --n 300 --seed <seed>` | committed; P3 sealed |
| 3 | `python scripts/s02_download.py P0` then `python scripts/s03_build_tables.py P0` | 298 patients built |
| 4 | `python scripts/s04_reproduce_p0.py` | exits 0: Tables 4.2 and 4.3 reproduced |
| 5 | `python scripts/s05_power_d1.py` | D1 note committed |
| 6 | `python scripts/s01_draw_sets.py P1 --n <D1> --seed <seed>`; then `P2` | committed |
| 7 | `s02_download.py P1 P2_train P2_val P2_test`; `s03_build_tables.py ...` | manifest written |
| 8 | `python scripts/s06_ro1_curves.py P0 P1 --adaptive` | curves |
| 9 | commit `notes/<date>_H1_preanalysis.md`; `python scripts/s07_h1.py` | H1 result |
| 10 | `python scripts/s08_rq13.py` | RQ1.3 table |

## Layout

```
src/esvea/config.py          paths and constants
src/esvea/sets.py            P0-P3 drawing, SHA-256 lock, loader guard (P3 closed until M4)
src/esvea/ingest/            PhysioNet download (.hea/.atr only); beat, interval, summary tables
src/esvea/ro1/               filters (percent deviation; Lipponen-Tarvainen via NeuroKit2), retention, H1 GLMM + power, RQ1.3
src/esvea/estimator/         Equations 3.2-3.4, gate, valid day, shrinkage sensitivity (shared with Track 2)
src/esvea/schema.py          reported-beat and coverage table format (Garmin parser target)
src/esvea/pseudodays.py      pseudo-days for untimed Icentia11k segments
src/esvea/pulsewatch/        one-to-one matching, lag search, motion SD and bins (pre-check settings)
src/esvea/simulate/          training simulator (placeholder parameters until calibrated)
src/esvea/degrade/           empty until S5; must stay separate from simulate/
```

## Known assumptions to check first

* `ro1/filters.percent_deviation`: warm-up rule; must reproduce section 4.2 on P0 or be aligned with the preliminary script.
* `pulsewatch/matching.best_lag`: tie-break by mean distance is new; compare with the pre-check script.
* `simulate/stream.py`: every parameter is a placeholder until calibrated (runbook T10).
