"""Paths and constants shared by every stage. Data never live in git: set ESVEA_DATA."""
from __future__ import annotations

import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]          # analysis/
DATA = Path(os.environ.get("ESVEA_DATA", REPO / "data"))
ICENTIA_RAW = DATA / "icentia11k" / "raw"            # .hea and .atr only
ICENTIA_TABLES = DATA / "icentia11k" / "tables"      # one Parquet file per patient and table
PULSEWATCH = DATA / "pulsewatch"
SPLITS = REPO / "splits"
NOTES = REPO / "notes"
RESULTS = REPO / "results"

ICENTIA_DB = "icentia11k-continuous-ecg"
ICENTIA_VERSION = "1.0"
FS = 250                                   # Hz, Icentia11k
RR_MIN_S, RR_MAX_S = 0.2, 3.0              # tallies exclude intervals outside this range (as in section 4.2)
BEAT_SYMBOLS = ("N", "S", "V", "Q")        # '+' is a rhythm-change marker, not a beat
AF_RHYTHMS = ("(AFIB", "(AFL")

BLOCK_HOURS = 6.0                          # L_h in Equations 3.2 and 3.4
N_BLOCKS = 4                               # 00-06, 06-12, 12-18, 18-24
ESVEA_PRIMARY_PER_DAY = 480                # Haeusler et al. (2025)
ESVEA_SECONDARY_PER_HOUR = 30              # Binici et al. (2010)
BINICI_RUN_BEATS = 20                      # run criterion used for the "rate or run" comparison with section 4.2
LARSEN_PROFILE = (0.87, 0.63, 1.11, 1.40)  # sensitivity analysis only (provisional reading of Larsen 2016 Fig. 3)
