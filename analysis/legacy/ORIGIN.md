# Legacy code and results (read-only reference for T2 and T8)

Copied 12 November 2026 (checklist item A3). Do not edit these files; they are the reference the new
pipeline is checked against. SHA-256 of each file is in `SHA256SUMS` next to this note.

## ro1_preliminary/ (input 2)

| File | Copied from |
|---|---|
| `incentia_ro1_prelim.py` | `Desktop/claude_desktop_handoff/core/incentia_ro1_prelim.py` |
| `tableA_removed_by_class.csv` | `Desktop/claude_desktop_handoff/core/` |
| `tableB_esvea_prevalence.csv` | `Desktop/claude_desktop_handoff/core/` |
| `tableA2_removed_by_esvea.csv` | `Desktop/claude_desktop_handoff/evidence/` |

The per-patient outputs of that run (`patients.csv`, `retention_by_patient.csv`) were not found on
this machine, so the exact list of 298 analysed patients is not available from the legacy side.

## pulsewatch_precheck/ (inputs 3 and 4)

| File | Copied from |
|---|---|
| `beat_retention_raw_test.py` | `synapse/build/beat_retention_raw_test.py` |
| `signal_proc.py` | `synapse/build/signal_proc.py` (contains `bandpass_ppg`, `detect_ppg_peaks`) |
| `mat_table.py` | `synapse/pulsewatch/mat_table.py` (the `pulsewatch.mat_table` reader) |
| `beat_retention_raw_results.json` | `synapse/build/` |
| `beat_retention_raw_skipcounts.json` | `synapse/build/` |

## P0 list (input 1)

No stored P0 id list was found. The preliminary script draws its patients as
`sorted(random.Random(seed).sample(range(11000), 300))` with default `--seed 2026` and
`--n-patients 300`. `splits/P0.txt` was regenerated from that rule with seed 2026. This assumes the
preliminary run used the defaults; G1 (exact reproduction of Tables 4.2 and 4.3) is the check.
