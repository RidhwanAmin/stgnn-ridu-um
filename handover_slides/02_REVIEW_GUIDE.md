# Review guide: refining writing and presentation

The deck's content has been checked against the docx several times (see `deck/VERSION_HISTORY.md`). The next round is about **how it reads and how it presents**. Work in this order.

## 1. Facts to start from

| Measure | Current state |
|---|---|
| Main talk | 23 slides (1 to 23); speaker notes time it at about **26 minutes** (sum of the "About N minutes" cues) |
| Time limit | **Not confirmed.** The FSKTM checklist (`context/UM_FSKTM_PhD_Proposal_Defence_Checklist.md`, item 35) asks the candidate to confirm the presentation and Q&A durations. Get this first; it decides how much must go |
| Visible words per main slide | Mean about 189; slide 5 has 330, slide 4 has 247, slide 3 has 223 (see `01_SLIDE_INVENTORY.md`) |
| Balance | Background and problem (slides 2 to 6) take about 7 minutes; methodology and evaluation (11 to 16) about 7.5 minutes. The checklist warns against background dominating |
| Appendix | 26 backup slides (A1 to A8, B1 to B3, C1 to C3, D1 to D5, E1 to E5) plus equations |

## 2. Writing

| Check | What good looks like |
|---|---|
| One message per slide | The title states the claim or question; the body supports it. A reader of titles alone can follow the argument |
| Density | Roughly 60 to 120 visible words on a text slide; tables carry evidence, so prose around them stays short. Move detail into speaker notes or the appendix, not into smaller type |
| Register | Academic thesis style (Dr Bryan): precise verbs (investigate, develop, evaluate, validate); no hype; hedged claims ("to our knowledge"); numbers with their source |
| Consistency with the docx | Objective and research-question wording verbatim from Table 1.1; H1 to H3 as stated in §1.2; numbers from Tables 4.1 to 4.3 and Ch 3 |
| Glosses | Five words or fewer, at first use only; do not repeat a gloss on later slides |
| Known docx-level wording issues | Do not "fix" these on the slides; raise them with the candidate: "quantify" on slide 4 (matches §1.2) against "investigate" in RO1; RQ2 "sequence-based baselines" against H2 "best non-graph baseline"; RQ3 per-day wording against the pooled estimate in §3.4; H1 has no stated direction (it is two-sided by design) |
| Speaker notes | Each note opens with the time cue, then the two or three things to say; anticipated questions marked "If asked". Remove the "Pending supervisor reconfirmation" lines once confirmed |

## 3. Presentation

| Check | What good looks like |
|---|---|
| Readability at distance | Body text no smaller than 22 px (slide 14 has 19 px text beside the enlarged figure: check it projects legibly; its figure also ends at y = 952, 12 px past the main-slide limit, which predates this handover) |
| Emphasis | Accent `#9b1c1c` only for the one thing per slide the panel must remember (limits, the gap, the key number) |
| Figures | Figure 3.1 (framework) and Figure 3.2 (architecture) as large as the slide allows; each figure explained in the notes |
| Flow | Checklist sequence (FSKTM section 14): title, context, problem, significance, literature, gap, aim and objectives, contribution, framework, methodology, technical detail, evaluation, ethics and risks, outcomes, timeline, conclusion |
| Closing | The last content slide leaves one clear statement of the contribution (checklist: "the final slide leaves the panel with a clear statement") |
| Two-minute version | The candidate can tell the whole proposal from slides 4, 5, 9, 11 and 22 alone; if not, sharpen those titles |
| Backup slides | Each appendix slide answers one likely question; the notes say which question |

## 4. Scope decisions to settle first

1. Confirm the time limit (section 1).
2. Decide slide 19 `prelim-next` and Appendix E (brief, section 4). Cutting Appendix E removes 5 slides; slide 19 can lose its gate strip and keep the "what each result decided" table.
3. Then trim the main talk to the time limit, starting with background (slides 2 and 3) and literature (7 and 8), not methodology.

## 5. Checks before every publish

1. `python tools/check_svg.py deck/project/slides`: prints `ok`.
2. `node tools/render_slides.js deck/project/slides /tmp/preview <changed ids>`: every slide `ok` (content bottom ≤ 940 main, ≤ 960 appendix). Look at the PNGs.
3. Page numbers on slides 2 to 22 and `app-eq` match their positions after any insert or removal.
4. No em dash (Unicode U+2014) in any changed file: `grep -c $'\u2014'` returns 0.
5. After publishing, open the live deck and look at each changed slide; record the new version id in `deck/VERSION_HISTORY.md`.
