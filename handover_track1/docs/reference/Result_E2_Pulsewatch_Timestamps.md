# Check E2: Pulsewatch timestamps across days

**Purpose:** decide whether the proposal can add the optional E2 clause saying real within-day ordering is tested on timestamped Pulsewatch recordings. The request is in `Check_E2_Pulsewatch_Timestamps.md`.

**Decision (3 November 2026): pass.** The optional clause can be added, but it should not call the timestamps UTC. Use file-name time as local time, not the conversion in the request's script.

**Timing of the rule:** the definitions below were written after a read-only sample of 11,735 files had been seen, and before the full run. They are not fully blind.

## Results to send back

| Item | Result |
|---|---|
| Files read / errors | 167,205 / 0 |
| Date range | 2019 to 2021 (years only) |
| Subjects spanning ≥ 3 days, in order, no overlaps | **64 of 108** (68 span ≥ 3 days) |
| Median gap between segments | 30.0 s; about 10 minutes between session starts (median across subjects) |
| Time zone | US Eastern local time in the file names, shown by the daylight-saving pattern and the hourly profile. No written statement found |
| Blocks 00–06 / 06–12 / 12–18 / 18–24, all `.pt` | Pooled 43.2 / 15.9 / 15.5 / 25.3%; mean of subjects 28.9 / 20.2 / 30.6 / 20.3% |
| Labelled, all subjects (pooled) | 43.3 / 15.8 / 15.5 / 25.4% |
| Excluded, all subjects (pooled) | 16.8 / 22.3 / 33.7 / 27.3% |
| No-label, 8 subjects (pooled) | 20.4 / 24.3 / 29.2 / 26.0% |
| Decision | **Pass** |

## Pass rule

The request's rule stands. These definitions make it computable.

| Item | Definition | Result | Met? |
|---|---|---|---|
| Q1 | At least 99% of readable files in the published study years, 2019–2021 | 100% | Yes |
| Q2 | At least 5 subjects span 3 or more local days, with zero order violations and zero overlaps above 2 s | 64 subjects | Yes |
| Q3 | At least 95% of segments match the US Eastern calendar offset within 5 s; US beats UK in weeks where the calendars differ; the name-clock profile peaks at night | 99.1%; 97.2% vs 2.6% on 6,710 segments; busiest hour 01:00 | Yes |

## Why the request's time conversion was not used

The request treats column 0 of `PPG_filt_csv` as UTC and converts it to `America/New_York`. The data does not support that:

- **Offset:** epoch minus file-name time, after removing segment index × 30 s, is 0 h in winter and −1 h in summer. True UTC against Eastern local time would be +5 h and +4 h.
- **Night test:** the request expects the busiest period at 04–10 UTC if the column is UTC. On the epoch column, 04–10 is among the quieter periods and the peak is 23:00–03:00.
- **Effect of converting:** the 00–06 share falls from 43.2% to 19.1%, and the 18–24 share rises from 25.3% to 45.2%. Night-time recording would look like evening recording.

The most likely reading is that the file name holds Eastern local time and the epoch sits at a fixed UTC−5 all year. How the release built that column is not documented, so this is an inference.

### Supporting evidence

- **In-clinic cohort:** all 188 `3xx` segments fall in 06–18 on the name clock (33.5% and 66.5%), as expected for in-clinic recording.
- **`statics` files, 8 subjects (added after the first full run, not part of the rule):**
  - These files have their own epoch in the name. Shifted by −5 h in winter or −4 h in summer, they almost never fall inside a session (0.0% and 0.1%).
  - Neighbouring shifts give 81–91% on the side towards later times. That edge sits at the Eastern UTC offset, which fits `statics` being true UTC and written between sessions.
  - My first explanation, that they are written just before a session starts, was wrong: none fall within 60 s of a session start at those shifts.
  - This is indirect evidence, and the season split itself uses the US calendar.

## Other findings

- **Labelled time is not wear time:** 43.3% of labelled segments fall in 00–06, against 16.8% of excluded ones. Labelled data favours quiet night hours.
- **Pooled shares favour heavy subjects:** the 00–06 share is 43.2% pooled and 28.9% as a mean of subjects.
- **Within-day ordering:** the median subject has labelled data in at least 2 blocks on 74% of their days, and spans 5 days. This is descriptive and not part of the rule.
- **Raw recordings, 8 subjects:** pooled 22.9 / 22.3 / 28.6 / 26.3%; mean of subjects 18.2 / 21.6 / 40.0 / 20.1%. This is the closest available measure of recording time, from subjects who were not randomly chosen.

## Limits

1. **Clock exceptions:** 1,540 segments (0.9%), from 36 subjects and 302 sessions, do not match the US calendar. One subject accounts for 37% of them. 353 January segments sit at +1 h, unexplained.
2. **Order and overlap:** 4 of the 68 subjects spanning 3 days fail the strict rule. There are 10 across-session order violations and 168 overlaps above 2 s (391 strict). There are no within-session order violations.
3. **Subjects below 3 days:** 40 of 108 subjects do not span 3 days in labelled `.pt` data, including the brief in-clinic `3xx` recordings.
4. **Excluded coverage:** excluded segments come from 68 clinical subjects and 1 `4xx` subject (11 segments), so the labelled vs excluded contrast describes clinical subjects. No-label data covers 6 of the 8 raw-tar subjects.
5. **Study years:** the 2019–2021 source is the randomised trial, enrolling September 2019 to August 2021. All clinical and `3xx` files fall within that enrolment period plus 44 days of follow-up, but only 38.0% of `4xx` files do. The `4xx` files stay within 2019–2021, and no separate published dates for that cohort were checked.
6. **Travel:** a participant who travelled outside Eastern time cannot be detected.

## Counts reconcile

- 403,022 label rows give 394,019 unique names: 166,279 labelled, 224,444 excluded, 392 code 3 and 2,904 kept-label conflicts or missing `.pt` (537 + 2,367).
- The labelled count matches the project's 166,279 de-duplicated set.
- In the 8 raw-tar subjects, no-label is 74,192, plus 53 files with long-index names not counted, which gives the earlier test's 74,245.
- Excluded is 12,533 here against 12,532 in the earlier test. Group totals exceed the raw file count by one, which suggests one excluded name has no raw file. This was not traced to a specific file.

## Do not claim

- That the timestamps are UTC.
- That labelled shares show wear or coverage. Use the 8-subject raw table, with its limits, for the RO3 fallback or any check of night-weighted coverage.
- That Pulsewatch reflects Garmin coverage. It is a Samsung watch in a different population.
- Any time-of-day ectopy pattern. Labels are 30-second windows with PAC and PVC merged.

## Files

- Script: `build/check_pulsewatch_timestamps.py`
- Aggregates: `build/pulsewatch_timestamps_summary.json`
- Exact times, local only and not to be shared: `build/pulsewatch_timestamps_segments.csv`, `build/pulsewatch_timestamps_segments_smoke.csv`

## Sources for study dates

- Dickson et al., *Cardiovasc Digit Health J* 2021, PMID 35265913 (protocol, 14- and 44-day follow-up)
- Ding et al., *JMIR Cardio* 2023;7:e45137 (enrolment dates, UMass Memorial, Massachusetts)
- The Pulsewatch Synapse wiki gives no time-zone statement.
