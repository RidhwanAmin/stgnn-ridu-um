# Track 1 handover: start here

Handover from the planning session (cloud, repository `RidhwanAmin/stgnn-ridu-um`, branch `claude/nifty-meitner-605ymp`) to the local implementation session, 12 November 2026.

## 1. What this session is for

Carry out **Track 1** of the ESVEA PhD study from now (S2, week W1 = 16 Nov 2026) to the end of S3 (W41, 23 Aug 2027): the Icentia11k pipeline, RO1 in full (RQ1.1, RQ1.2, RQ1.3, H1), Pulsewatch work (lag method, π̂(m), profiles), the training simulator, the start of RO2, two papers, and the handover pack for Track 2 (device, ethics, Garmin pipeline).

Out of scope here: the slides (they are the research proposal and are not revised), the proposal text, and Track 2 itself.

## 2. Rules

1. **The proposal docx is the source of truth** (`docs/Ridhwan_Research_Proposal_UM.docx`). Where it leaves a choice open, the runbook marks it **[Proposed]**; these need supervisor agreement and must not be presented as settled.
2. **No em dashes** in any written document (house rule).
3. **Pre-analysis notes are committed before data are opened** for every confirmatory step (D1, H1, lag rule, π̂(m) model, simulator checks). Deviations are reported as deviations.
4. **P3 (about 300 Icentia11k patients) stays closed** until the M4 freeze in S4. The code enforces this; do not work around it.
5. **Fix the code, never the targets:** if P0 does not reproduce Tables 4.2 and 4.3, the pipeline is wrong.
6. Data never go in git: set `ESVEA_DATA` to university storage (PDPA 2010).

## 3. Files in this package

`analysis/` sits next to `handover_track1/` (at the repository root, or at the root of the zip).

| File | What it is |
|---|---|
| `00_START_HERE.md` | This brief |
| `01_COMPLETION_CHECKLIST.md` | Every item to complete, the expected result, the "done when" test, and a status column to keep up to date |
| `02_INPUTS_REQUIRED.md` | Documents to bring in from the preliminary project and to request, with where each goes |
| `docs/Track1_Implementation_Runbook_S2_S3.md` | The full week-by-week plan (work packages T0 to T12, gates G1 to G7, commands) |
| `docs/Implementation_Plan_Icentia11k_and_Datasets.md` | Overview of both tracks (Track 1 and Track 2) and decisions D1 to D11 |
| `docs/Ridhwan_Research_Proposal_UM.docx` | The proposal (source of truth) |
| `docs/reference/` | Pulsewatch pre-check configuration and result, Icentia11k clock-time findings, kappa simulation README |
| `analysis/` | Initial code: `esvea` package, numbered scripts, 25 unit tests (see `analysis/README.md`) |
| `Track1_Handover_Package.zip` | Everything above in one file: `handover_track1/` plus `analysis/` at the zip root. Unzip it into the local working folder |

## 4. State at handover

| Done | Not done |
|---|---|
| Plan and runbook written | Nothing has been run on P0, P1 or P2 |
| `analysis/` package: patient-set lock and guard; Icentia11k download and tables; filters; retention; H1 model and power simulation; RQ1.3; Equations 3.2 to 3.4 and coverage rules; reported-beat schema; pseudo-days; Pulsewatch matching; first simulator | P0 list not yet imported (it is in the preliminary project) |
| 25 unit tests pass; one real patient (p00001) built from PhysioNet in 17 s | Pulsewatch file readers, π̂(m) fit, RQ1.1 models, RO2 model and baselines |

Two assumptions in the code must be checked first: the warm-up rule of the percent-deviation filter (`ro1/filters.py`) and the tie-break in the lag search (`pulsewatch/matching.py`). Both are checked against the legacy scripts listed in `02_INPUTS_REQUIRED.md`.

## 5. First three steps

1. Set up: `cd analysis && python -m venv .venv && . .venv/bin/activate && pip install -e ".[dev,adaptive]" && pytest -q` (expect 25 passed).
2. Bring in inputs 1 to 4 from `02_INPUTS_REQUIRED.md` (P0 list and seed; preliminary RO1 script; Pulsewatch pre-check scripts and results).
3. Run gate G1 (runbook T2): download and build P0, then `python scripts/s04_reproduce_p0.py` must exit 0.

## 6. Prompt to paste into the local session

> You are continuing Track 1 of my ESVEA PhD study. Read `handover_track1/00_START_HERE.md`, then `01_COMPLETION_CHECKLIST.md`, `02_INPUTS_REQUIRED.md` and `docs/Track1_Implementation_Runbook_S2_S3.md`. The proposal docx is the source of truth; do not edit the slides or the proposal. Start with the first three steps in section 5. Work through the checklist in order, update its status column as items are completed, record every confirmatory pre-analysis note before running the analysis, and stop to ask me before any decision marked [Proposed] or any deviation from the runbook. Report each gate (G1 to G7) with its evidence file.
