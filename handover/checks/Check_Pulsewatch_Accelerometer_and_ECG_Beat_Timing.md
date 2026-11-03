# Check: Does Pulsewatch include accelerometer data and beat-level ECG timing?

**Why this matters:** Equation 3.1 estimates π̂, the chance that a real beat survives into the smartwatch interval series, as a function of motion. Estimating it needs three things recorded at the same time: the true beats (reference ECG), what the watch reported (PPG), and motion (accelerometer). Icentia11k has only the ECG, and the RO3 Garmin cohort has no ECG. Pulsewatch is the only dataset in the proposal that might have all three. Its contents decide how Section 3.4 and Equation 3.1 are written.

**What to answer at the end:**
- **Q1.** Does Pulsewatch include accelerometer data for the same periods as the PPG?
- **Q2.** Does the reference ECG come with beat-level timing (R-peak times or beat annotations), or at least the raw ECG signal from which beats can be detected? Or only 30-second window labels?
- **Q3.** Are the watch and ECG recordings time-aligned, so that a beat in the ECG can be matched to the same moment in the PPG?

**Time needed:** about 20 to 40 minutes, most of it browsing and downloading one sample file.

---

## Step 1. Start with the copy you already have

You used Pulsewatch in the pilot (proposal Section 4.1, Table 4.1: 48,396 segments), so part of the dataset is probably already on your computer.

1. Find the folder you used for the pilot.
2. List what is in it (file names, extensions, subfolders). On Windows, in PowerShell:
   ```powershell
   Get-ChildItem -Recurse "C:\path\to\pulsewatch" | Select-Object FullName, Length | Out-File pulsewatch_files.txt
   ```
   On macOS or Linux:
   ```bash
   find /path/to/pulsewatch -type f | head -200 > pulsewatch_files.txt
   ```
3. Look in `pulsewatch_files.txt` for names containing: `acc`, `accel`, `ACC`, `motion`, `imu`, `ecg`, `ECG`, `rpeak`, `r_peak`, `beat`, `annot`, `label`, `timestamp`, `time`.

If the pilot copy is only pre-cut 30-second PPG segments with labels, it may be a processed subset. Continue to Step 2 to check the full release.

## Step 2. Check the full release on Synapse

1. Sign in at https://www.synapse.org with the account that has Pulsewatch access.
2. Open the project: search for **syn23565056** (the ID in proposal Table B.2).
3. Read the project **Wiki** page first. It usually describes:
   - which signals are included (PPG channels, accelerometer, heart rate)
   - the reference device (ECG patch) and whether raw ECG is shared
   - the label format (per 30-second window, or per beat)
   - how watch and ECG recordings were synchronised
4. Open the **Files** tab and expand each folder. Note:
   - folder and file names
   - file types (`.csv`, `.mat`, `.h5`/`.hdf5`, `.json`, `.npy`, `.parquet`, `.txt`)
   - any README, data dictionary or codebook file. Download it if present.
5. Check the **Conditions for Use** or data use terms on the project. Confirm that the planned use (fitting a beat-loss model) is allowed under your access approval.

## Step 3. Inspect one sample file of each type

Download **one** small file of each type you found (one PPG file, one ECG file, one label file, one accelerometer file if separate). Put them in an empty folder, for example `pw_sample/`.

Save this script as `inspect_pulsewatch.py` **outside** that folder, then run it with the folder as the argument:

```bash
python inspect_pulsewatch.py pw_sample
```

```python
"""Print the structure of every file in a folder: columns, keys, shapes, first rows."""
import os, sys, json

folder = sys.argv[1]
KEYWORDS = ("acc", "imu", "motion", "ecg", "rpeak", "r_peak", "beat", "annot",
            "label", "time", "stamp", "ppg", "hr")

def flag(names):
    hits = [n for n in names if any(k in str(n).lower() for k in KEYWORDS)]
    return f"  matching keywords: {hits}" if hits else "  matching keywords: none"

for name in sorted(os.listdir(folder)):
    path = os.path.join(folder, name)
    ext = os.path.splitext(name)[1].lower()
    print(f"\n===== {name} ({os.path.getsize(path):,} bytes) =====")
    try:
        if ext in (".csv", ".txt", ".tsv"):
            import pandas as pd
            df = pd.read_csv(path, sep=None, engine="python", nrows=10)
            print("  columns:", list(df.columns)); print(flag(df.columns))
            print(df.head(5).to_string())
        elif ext == ".parquet":
            import pandas as pd
            df = pd.read_parquet(path)
            print("  shape:", df.shape, "columns:", list(df.columns)); print(flag(df.columns))
            print(df.head(5).to_string())
        elif ext == ".mat":
            try:
                from scipy.io import loadmat
                m = {k: v for k, v in loadmat(path).items() if not k.startswith("__")}
                for k, v in m.items():
                    print(f"  {k}: type={type(v).__name__} shape={getattr(v, 'shape', '')}")
                print(flag(m.keys()))
            except NotImplementedError:  # MATLAB v7.3 files are HDF5
                import h5py
                with h5py.File(path, "r") as f:
                    f.visititems(lambda n, o: print(f"  {n}: {getattr(o, 'shape', '')}"))
                    keys = []; f.visit(keys.append); print(flag(keys))
        elif ext in (".h5", ".hdf5"):
            import h5py
            with h5py.File(path, "r") as f:
                f.visititems(lambda n, o: print(f"  {n}: {getattr(o, 'shape', '')} {getattr(o, 'dtype', '')}"))
                keys = []; f.visit(keys.append); print(flag(keys))
                for k, v in f.attrs.items(): print(f"  attr {k} = {v}")
        elif ext == ".npy":
            import numpy as np
            a = np.load(path, allow_pickle=False); print("  shape:", a.shape, "dtype:", a.dtype)
        elif ext == ".json":
            with open(path) as fh: d = json.load(fh)
            keys = list(d.keys()) if isinstance(d, dict) else []
            print("  top-level keys:", keys[:50]); print(flag(keys))
        else:
            print("  (not inspected: unknown type)")
    except Exception as e:
        print("  could not read:", e)
```

If a package is missing, install it: `pip install pandas scipy h5py pyarrow`.

## Step 4. Read the output

### Q1. Accelerometer

| What you see | Answer |
|---|---|
| Columns or keys such as `acc_x`, `acc_y`, `acc_z`, `ACC`, `accel`, `imu`, at a regular sampling rate, covering the same period as the PPG | **Yes** |
| Only a motion summary (for example a single activity value per window) | **Partly**: usable as a coarse motion level per window, not per beat |
| No motion data anywhere, and the Wiki does not mention it | **No** |

### Q2. Beat-level ECG timing

| What you see | Answer |
|---|---|
| A list of R-peak times or beat annotations (sample indices or timestamps, possibly with beat types) | **Yes, annotated** |
| A raw ECG signal (a long array at, say, 125 to 500 Hz) but no beat list | **Yes, derivable**: beats can be detected with a standard R-peak detector (for example `neurokit2`), without beat types |
| Only labels per 30-second window (for example AF / PAC-PVC / normal / noise) and no ECG signal | **No** |

### Q3. Time alignment

| What you see | Answer |
|---|---|
| PPG and ECG share a timestamp column or start time, or the Wiki describes synchronisation | **Yes** |
| Segments are pre-cut and paired (same 30-s window for PPG and ECG) but with no absolute time | **Partly**: alignment within each window only; check the Wiki for how precise the pairing is |
| No shared time reference | **No** |

## Step 5. What each answer changes in the proposal

| Q1 accelerometer | Q2 beat timing | Q3 aligned | What Equation 3.1 and Section 3.4 can say |
|---|---|---|---|
| Yes | Yes (annotated or derivable) | Yes | Motion part of retention is **estimated** on Pulsewatch: for each ECG beat, whether it appears in the PPG interval series, modelled against accelerometer motion. Beat-class part comes from RO1 on Icentia11k. State that the two parts are combined multiplicatively and that Pulsewatch uses a different watch from Garmin. |
| Yes | Window labels only | Any | Motion effect can be estimated only at **window level** (share of beats lost per 30-s window against motion, using heart-rate-based expected beat counts). Weaker; state it as an approximation. |
| No | Any | Any | Motion part stays a **stated assumption** from the Garmin specification. Equation 3.1 drops the motion term in the main analysis, and motion enters only as a sensitivity analysis. Consider the concurrent-ECG substudy in RO3 (10 to 15 participants wearing an ECG patch with the watch) to estimate it directly. |

## Step 6. Send the result back

Paste into the chat:
1. The answers to Q1, Q2 and Q3 (Yes / Partly / No).
2. The relevant part of the `inspect_pulsewatch.py` output (column and key names, not the data values).
3. Any sentence from the Synapse Wiki describing signals, labels or synchronisation.

Claude will then write Equation 3.1, the retention paragraph in Section 3.4, Table 3.1 and Table B.2, and update the matching slides.

**Data protection:** share only file names, column names and descriptions in the chat. Do not paste participant data values or identifiers. The Pulsewatch data use terms and the UM AI guidelines may restrict uploading the data itself.
