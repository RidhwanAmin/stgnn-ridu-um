# Patient sets (Table B.3)

Written once by `scripts/s01_draw_sets.py`, hashed in `SHA256SUMS`, committed immediately. Never edited.

1. `P0.txt`: copy the 300 patient ids of the preliminary analysis (section 4.2) from the preliminary
   project, with its seed in the header line `# P0; n=300; seed=<seed>`, then run
   `python -c "from esvea import sets; sets._update_sums(sets.SPLITS)"` and commit.
2. `P3.txt`: 300 patients, drawn first and sealed until `notes/M4_freeze_record.md` exists.
3. `P1.txt`: size from the dated D1 note.
4. `P2_train.txt`, `P2_val.txt`, `P2_test.txt`: every remaining patient, 70/15/15 by patient.
