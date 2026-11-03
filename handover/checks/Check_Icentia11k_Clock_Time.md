# Check: Do Icentia11k segments carry clock time?

**Why this matters:** Equation 3.2 in the proposal uses time-of-day weights (wₕ) "estimated from the diurnal PAC profile in Icentia11k". That only works if each Icentia11k segment carries a clock time. If it does not, wₕ must be redefined (for example, block length ÷ 24), and the proposal must say the Icentia11k reference daily count is itself extrapolated.

**What you need:** the same computer and Python setup you used for `icentia_ro1_prelim.py` (Python 3 with the `wfdb` package) and an internet connection. No full download is needed; the script reads only small header files from PhysioNet.

---

## Step 1. Check that wfdb is installed

Open a terminal (Command Prompt / PowerShell on Windows, Terminal on macOS) and run:

```bash
python -c "import wfdb; print(wfdb.__version__)"
```

If you see a version number, continue. If you get `ModuleNotFoundError`, install it:

```bash
pip install wfdb
```

## Step 2. Create the check script

Create a new file named `check_icentia_time.py` in the same folder as your RO1 script, and paste this in:

```python
import wfdb

# Patients to check (first patient of three different folders)
patients = [0, 1000, 5000]

for pid in patients:
    pdir = f"icentia11k-continuous-ecg/1.0/p{pid // 1000:02d}/p{pid:05d}"
    print(f"\n=== Patient p{pid:05d} ===")
    for s in range(3):  # first three segments
        seg = f"p{pid:05d}_s{s:02d}"
        try:
            h = wfdb.rdheader(seg, pn_dir=pdir)
            minutes = round(h.sig_len / h.fs / 60, 1)
            print(f"{seg} | date: {h.base_date} | time: {h.base_time} | "
                  f"fs: {h.fs} Hz | length: {minutes} min | comments: {h.comments}")
        except Exception as e:
            print(f"{seg} | could not read header: {e}")
```

## Step 3. Run it

```bash
python check_icentia_time.py
```

It should finish in under a minute.

## Step 4. Read the output

| What you see | Meaning | What to change in the proposal |
|---|---|---|
| `date: None` and `time: None` for every segment | Segments carry **no clock time** | Redefine wₕ as block length ÷ 24 (or use a published diurnal PAC profile from another source); state that the Icentia11k daily count is extrapolated from non-contiguous segments; Icentia11k cannot be used to place coverage gaps by time of day |
| Date and time are filled in | Clock time exists | Check Step 5 to see whether segments are contiguous |
| `length` is about 70 min per segment | Confirms each patient's ~57.5 h is many separate ~70-min segments, not one continuous recording | Describe the segment structure in Section 3.2 |
| `comments` contains text | May hold timing or recording notes | Copy it and send it to Claude |

## Step 5. Only if clock time exists: check contiguity

For one patient, note the `time` and `length` of `s00`, then the `time` of `s01`.

- If `s01` starts where `s00` ends (start time + length), the segments are contiguous.
- If there is a gap, the segments are sampled from the full recording, and a daily count must still be extrapolated.

## Step 6. Confirm with the official description

1. Open https://physionet.org/content/icentia11k-continuous-ecg/1.0/
2. Press Ctrl+F (Cmd+F on macOS) and search for: `time`, `segment`, `contiguous`, `random`.
3. Note any sentence describing how segments were taken from each patient's recording (up to about two weeks long), and whether timestamps were kept or removed.

## Step 7. Send the result back

Copy the full terminal output from Step 3 and any relevant sentence from Step 6, and paste them into the chat. Claude will then update Equation 3.2, Section 3.2, Section 3.4 and the matching slides.

---

# Decision: how should Equation 3.2 define wₕ?

**Recommendation:** define wₕ as block length ÷ 24 in the main estimate, and run a published diurnal PAC profile only as a sensitivity analysis. The main estimate then adds no outside assumption.

## Current equation (as submitted)

$$
\hat R(d) = \sum_h w_h \cdot \frac{\sum_{i \in A(d,h)} \hat p_i / \hat\pi(m_i, h)}{\tau(d,h)}, \qquad \sum_h w_h = 1 \tag{3.2}
$$

Plain text: R̂(d) = Σₕ wₕ · [ Σᵢ∈A(d,h) p̂ᵢ / π̂(mᵢ, h) ] / τ(d,h), with Σₕ wₕ = 1

- The bracketed term divided by τ(d,h) is the **observed hourly PAC rate in block h** after retention weighting. Call it r̂(d,h).
- The proposal currently says wₕ is "estimated from the diurnal PAC profile in Icentia11k".

## The problem with profile weights

r̂(d,h) already contains that day's diurnal variation: if PACs are more frequent at night, the night rate is already higher. Multiplying it by a weight that is also larger at night counts the diurnal pattern twice and inflates the daily count.

## Option A (recommended): weights are block durations

$$
w_h = \frac{L_h}{24}, \qquad \hat R(d) = \sum_h \frac{L_h}{24}\,\hat r(d,h), \qquad \text{daily count} = 24\,\hat R(d) = \sum_h L_h\,\hat r(d,h)
$$

Plain text: wₕ = Lₕ / 24, where Lₕ is the length of block h in hours. The daily count is Σₕ Lₕ · r̂(d,h): each block's rate times its length.

- Needs no external data and no clock time in Icentia11k.
- Every block counts in proportion to the time it covers, which is what a Holter 24-hour count does.
- The coverage gate (Equation 3.3) already refuses days whose day or night blocks are too thinly observed, so no block's rate is guessed.

## Option B (sensitivity analysis only): a published profile fills thin blocks

The profile is used to shrink rates in blocks with low coverage, not as a weight:

$$
\tilde r(d,h) = \frac{\tau(d,h)\,\hat r(d,h) + \kappa\, g_h\, \bar r(d)}{\tau(d,h) + \kappa}, \qquad \text{daily count}_B = \sum_h L_h\,\tilde r(d,h)
$$

Plain text: r̃(d,h) = [ τ(d,h) · r̂(d,h) + κ · gₕ · r̄(d) ] / [ τ(d,h) + κ ]

- gₕ is the published relative PAC rate in block h (average 1 across the day).
- r̄(d) is that day's duration-weighted mean rate.
- κ (hours) sets how strongly thin blocks are pulled towards the profile.
- A well-observed block keeps its own rate; a thinly observed block borrows the published shape.
- Report how many patients change ESVEA class between Option A and Option B.

## Worked example: why the choice matters near the threshold

Four 6-hour blocks, retention-weighted hourly PAC rates observed on one day:

| Block | Night 00–06 | Morning 06–12 | Afternoon 12–18 | Evening 18–24 |
|---|---|---|---|---|
| Observed rate r̂ (PACs/h) | 30 | 12 | 10 | 20 |

- **Option A (wₕ = 6/24 = 0.25 each):** 24 × (0.25 × 30 + 0.25 × 12 + 0.25 × 10 + 0.25 × 20) = **432 PACs/day**, ESVEA negative at 480/day.
- **Current wording, profile weights** (e.g. 0.40, 0.20, 0.15, 0.25): 24 × (12 + 2.4 + 1.5 + 5) = **502 PACs/day**, ESVEA positive.

The same data change class only because the night pattern was counted twice. That is why the main estimate should use Option A.

## How the Icentia11k check affects this

| Result of Steps 3 to 6 | Main estimate | Sensitivity analysis |
|---|---|---|
| No clock time | Option A (unchanged) | Profile gₕ must come from a published 24-hour Holter study (source to be chosen and cited) |
| Clock time exists | Option A (unchanged) | gₕ can be estimated from Icentia11k, using patients not used for RO2 training or RO4a testing |

Either way, Option A stays the main estimate. The Icentia11k result only decides where the sensitivity profile comes from.

## Proposed replacement text for Section 3.4

> Here wₕ = Lₕ/24, where Lₕ is the length of block h in hours, so the daily count 24 · R̂(d) = Σₕ Lₕ · r̂(d,h) weights each block by the time it covers, as a 24-hour Holter count does; c is the analysable coverage of each block, and the thresholds θ are fixed in the registered protocol. In a sensitivity analysis, rates in thinly observed blocks are shrunk towards a published diurnal PAC profile, and the number of participants whose ESVEA class changes is reported.

**Note:** this settles wₕ only. Equation 3.1 still needs the separate fix from the review: retention π̂ should also depend on beat class (or p̂ᵢ), because PAC intervals were retained at 39% against 91% for normal intervals (Section 4.2).
