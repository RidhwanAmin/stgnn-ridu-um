# Pulsewatch beat-retention data check

**Purpose:** decide how Equation 3.1 and Section 3.4 of the proposal are written. Equation 3.1 estimates π̂, the chance that a real beat survives into the smartwatch interval series, as a function of motion.

**Status:** feasibility check on local files only. No model was fitted, and the numbers below are not parameter estimates. The proposal text was not available when this was drafted, so the draft wording and table entries still need fitting to it.

**Update, 2 November 2026:** a later test on raw watch files did not pass its locked rule, and the draft text below predates it. The test result and the decision taken are in `methodology/Pulsewatch_Beat_Retention_Precheck_Config.md`, which takes precedence where the two differ.

## Answers

| Question | Answer | Basis |
|---|---|---|
| **Q1.** Accelerometer for the same periods as the PPG? | **Yes, magnitude only** | 50 Hz, 1,500 samples per 30-s segment, paired with each PPG segment. The release documents the tri-axial signal as converted to magnitude, so 3-axis data is not available. |
| **Q2.** Beat-level ECG timing? | **Yes, for clinical subjects only** | R-peak sample indices at 250 Hz. They are detector output and carry no beat types. |
| **Q3.** Watch and ECG time-aligned? | **Partly** | The released alignment is not accurate to the beat. A lag fitted per session recovers beat matching in most patches, but not all. |

**Effect on the proposal's decision table:** closest to the row "Yes / Yes / Yes", where the motion part is estimated on Pulsewatch. That holds only with per-session lag correction and the limits listed below.

## Files and keys

| Source | Location | Contents |
|---|---|---|
| Segment `.pt` (Elgendi set) | `synapse_data\untar\PPG_Elgendi_30sec_HR_ACC_pt` | `PPG_filt_csv` (1500, 2), `ACC_raw_csv` (1500, 2), `PPG_filt_Elgendi`, `PPG_peak_loc_Elgendi_4_2013`, `HR_Elgendi_4_2013`, `new_PPG_peak_loc_Elgendi`, `new_HR_PPG_Elgendi` |
| Segment `.pt` (WEPD set) | `synapse_data\untar\PPG_filt_30sec_HR_pt` | `PPG_filt_csv`, `PPG_filt_WEPD`, `PPG_peak_loc_WEPD`, `PPG_HR_WEPD`, `new_PPG_peak_loc`, `new_HR_PPG` (no ACC) |
| ECG hour files | `build\ecg_fresh\Filtered_ECG_Peaks`, `synapse_data\ecg\Filtered_ECG_Peaks` | `Billal_ECG_filt_1_hr_this` (900000, 1), `Billal_ECG_peak_1_hr_this`, `Billal_ECG_HR_1_hr_this`, `ECG_time_1_hr_this` (900000, 1) |
| Alignment index | `synapse_data\ecg\aligned_index.csv` | `seg_name`, `patch_id`, `hour_idx`, `start_idx`, `end_idx`, `contain_empty`, `pad_front`, `pad_end`, `fs_ecg`; 140,099 rows, all clinical |
| Labels | `synapse_data\03_Labels` | `table_file_name`, `final_AF_GT_20230921`; one label per 30-s segment |

**Local ECG coverage:** 10 patches from 8 subjects (1,130 hour files). The release describes clinical-trial ECG beyond this, which has not been downloaded.

**Clocks:** `PPG_filt_csv` column 0 looks like a UNIX millisecond timestamp with a 20 ms step. `ECG_time_1_hr_this` is on a much smaller scale, so these two columns cannot be compared directly as clocks. Alignment has to go through `aligned_index.csv`.

## Evidence

| Check | Result |
|---|---|
| Session-fitted lag, held-out segments | Median ECG-beat match 0.867, PPG-peak precision 0.871 |
| Mismatched-session control, same method | Median 0.222 |
| Single fixed lag across all patches (separate run, 916 segments) | Median 0.151, below its control of 0.233 |
| Match by motion tertile | Mean 0.932 / 0.731 / 0.715 (low / mid / high) |

The motion tertiles are pooled across subjects and use segment-level ACC SD, so they are confounded by subject and do not show a motion effect.

### Per-patch results (session-fitted lag)

| Patch | Held-out segments | Sessions | Match (median) | Control (median) | Session lag IQR (s) |
|---|---:|---:|---:|---:|---|
| 017B | 43 | 11 | 0.756 | 0.236 | −0.05 to 0.26 |
| 044A | 158 | 40 | 0.970 | 0.224 | −0.12 to 0.26 |
| 055A | 28 | 7 | 0.964 | 0.219 | −0.57 to −0.02 |
| 075A | 171 | 40 | 0.649 | 0.203 | −2.10 to 2.23 |
| 083A | 23 | 6 | 0.900 | 0.230 | 0.19 to 0.24 |
| 098B | 28 | 7 | 0.277 | 0.281 | −0.33 to 0.53 |
| 109A | 176 | 40 | 0.914 | 0.208 | −0.20 to 0.52 |
| 110A | 6 | 2 | 0.675 | 0.289 | −0.43 to 0.14 |
| 110B | 30 | 9 | 0.863 | 0.246 | 0.18 to 1.60 |

Patch 098B is no better than chance. Patch 110A has too few segments to interpret. Patch 098A produced no sessions for this test.

### Method

The analysis ran as an inline read-only script that was not saved, so this description is the record of it.

- **Sample:** segments in `aligned_index.csv` with a `.pt` file and an ECG hour file, grouped into sessions by filename prefix. Sessions needed at least 6 usable segments, with up to 40 randomly chosen sessions per patch. Result: 663 held-out segments, 162 sessions, 9 patches, 8 subjects.
- **Beats:** ECG times from `Billal_ECG_peak_1_hr_this` within `start_idx` to `end_idx`. PPG times from `new_PPG_peak_loc_Elgendi` at 50 Hz.
- **Lag fit:** within each session, the lag was searched from −3 to +3 s in 0.02 s steps to maximise match on alternating segments, then scored on the remaining segments.
- **Match:** an ECG beat counts as matched if a PPG peak lies within ±100 ms after applying the lag. Precision applies the same test from PPG peaks to ECG beats.
- **Control:** the same lag fit and scoring, pairing a session's ECG with PPG from a different session of the same patch.

## Limits

1. **Offline detector:** the PPG peaks come from an offline Elgendi detector on filtered PPG, not from intervals reported by the watch. π̂ is therefore detector retention on Samsung watches, and applying it to Garmin needs a stated transport assumption.
2. **Motion selection:** 215,428 of 403,022 label rows are code −1, which the local setup notes describe as mostly >5 s motion noise or unadjudicated. `.pt` files exist only for labelled segments. In the one subject with raw files on disk, there are 566 raw PPG files and 78 `.pt` files. Local data under-represents high motion, so π̂ would be biased upward at high motion unless the raw `.txt` files are obtained.
3. **Rhythm coverage:** the ECG is clinical-only, and only about 184 AF segments have ECG (subjects 017, 075 and 110). The 3xx and 4xx cohorts have none, so the motion term cannot be estimated separately in AF.
4. **Beat types:** `Solo.Beats.txt` is in the raw ECG folder that project rules prohibit. Beat-class retention stays with RO1 on Icentia11k.
5. **Sample size:** 8 subjects support a feasibility claim, not a parameter estimate.

## Draft proposal text

### Equation 3.1

$$\hat{\pi}(c, m) = \pi_{\text{class}}(c) \times \pi_{\text{motion}}(m) \tag{3.1}$$

where the motion component is estimated on Pulsewatch with a mixed-effects logistic model:

$$\text{logit}\,P(R_{ijk} = 1 \mid m_{ijk}) = \alpha + u_i + v_{ij} + \beta\, m_{ijk}$$

- $R_{ijk} = 1$ if ECG beat $k$ in session $j$ of subject $i$ has a PPG peak within tolerance after session-lag correction.
- $m_{ijk}$ is the SD of accelerometer magnitude in a window around the beat. The window length is still to be specified.
- $u_i$ and $v_{ij}$ are subject and session random intercepts.
- $\pi_{\text{class}}(c)$ is the beat-class retention from RO1 on Icentia11k.

The multiplicative form assumes that beat class and motion act independently on retention. This is an assumption, and Pulsewatch cannot test it because the usable ECG files carry no beat types.

### Section 3.4 retention paragraph

> The motion component of beat retention will be estimated on Pulsewatch, the only dataset in this proposal with concurrent reference ECG, wrist PPG and accelerometer recordings. For each ECG R-peak, retention is defined as the presence of a PPG peak within a set tolerance, modelled against accelerometer magnitude with subject and session random effects. A feasibility check on 8 clinical subjects showed that the released alignment is not accurate to the beat: a single fixed lag performed no better than mismatched segments (median match 0.151 vs 0.233). A lag fitted within each recording session restored matching on held-out segments (median 0.867 vs 0.222). Lag correction is therefore part of the method. A session is retained only if its held-out match exceeds a mismatched-session control, and the number of sessions dropped will be reported.
>
> Five limits apply. First, PPG peaks come from an offline detector on Samsung watch signals rather than from device-reported intervals, so applying the estimate to the Garmin cohort rests on a transport assumption. Second, segments labelled as excluded, which are mostly motion-corrupted or unadjudicated, are absent from the processed release; analysis restricted to it would overstate retention at high motion, so the raw watch files are required for the final estimate. Third, reference ECG is available only for clinical-trial subjects and covers about 184 AF segments, so the motion effect cannot be estimated separately in AF. Fourth, the usable ECG files carry no beat types, so the beat-class component comes from RO1 on Icentia11k and the two components are combined multiplicatively by assumption. Fifth, the feasibility result comes from a small subset of subjects and is not a parameter estimate. The concurrent-ECG substudy in RO3 (10 to 15 participants wearing an ECG patch with the watch) is retained because it provides the only direct estimate on the Garmin device.

### Table 3.1: Pulsewatch entry

| Field | Entry |
|---|---|
| Role | Estimates the motion component of beat retention, $\pi_{\text{motion}}(m)$ |
| Signals used | Wrist PPG (50 Hz), accelerometer magnitude (50 Hz), reference ECG R-peaks (250 Hz) |
| Subjects used | Clinical-trial cohort only |
| Device | Samsung Gear S3 / Galaxy Watch 3, Cardea SOLO ECG patch |
| Alignment | Released alignment plus per-session lag correction |
| Main limits | Offline peak detector; high-motion segments need raw files; few AF segments with ECG |

### Table B.2: Pulsewatch entry

| Field | Entry |
|---|---|
| Identifier | Synapse project `syn23565056`, dataset folder `syn64402376` ("Pulsewatch2025"); download through the authors' Google Drive after a Google Form request |
| Accelerometer | Yes, magnitude only (not 3-axis) |
| Beat-level ECG | R-peak indices for clinical subjects; no beat types in the filtered files |
| Labels | 30-s adjudicated labels (NSR, AF, PAC/PVC) |
| Time alignment | Partial; per-session lag correction required |

## Recommendation

Keep the RO3 concurrent-ECG substudy. Pulsewatch can provide a motion-retention estimate on Samsung hardware, but only the substudy measures retention directly on Garmin.

## Open items

- **Data use terms:** no explicit licence or permitted-use statement was found, so permission for a beat-loss model is inferred, not stated. The Google Form's only commitment is to cite the authors' papers, and it also asks for the planned use. The Synapse API lists 0 access requirements for both `syn23565056` and `syn64402376`. The Drive folder was not checked for a licence file. To do: check that any planned use submitted on the form covers this work, ask the dataset contact (Dong Han) for written confirmation, and check the UM AI guidelines separately.
- **Further data, needing separate approval:** the remaining `Filtered_ECG_Peaks` patches and the raw `01_Clinical_Trial` watch files. A rough estimate for all ECG patches is 150 to 230 GB, extrapolated from local patch sizes and not checked against the Drive.
- **Model fit:** should wait for that data.
