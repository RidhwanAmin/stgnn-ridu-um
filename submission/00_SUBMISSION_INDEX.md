# ESVEA Proposal Defence: Submission Index

**Candidate:** Ridhwan Amin Azhari Bin Zabidi (25118475), FCSIT, Universiti Malaya
**Supervisors:** Dr. Bryan Raj A/L Peter Jabaraj; Assoc. Prof. Ts. Dr. Ismail Bin Ahmedy
**Compiled:** 3 November 2026, updated after the independent review and the candidate's revision
**Repository branch:** `claude/nifty-meitner-605ymp` (RidhwanAmin/stgnn-ridu-um)

This index maps every markdown record, from the handover to the latest change, to the two submission deliverables: the proposal docx and the slide deck. `COMPILED_CONTEXT.md` holds the full text of every record in the order below. It is an archive for the candidate and supervisors, not a faculty submission (its handover records contain em dashes).

> **Pending supervisor reconfirmation: E1 (as revised after the independent review) and E11.** Both are applied in the docx and the deck. Details: `proposal/SUPERVISOR_RECONFIRMATION_E1_E11.md`.

---

## 1. Deliverables

| Deliverable | Location | Version | Status |
|---|---|---|---|
| Proposal (Word) | `proposal/Ridhwan_Research_Proposal_UM.docx` | Candidate's post-review revision, 3 Nov 2026 | Text identical to a fresh build of `proposal/source/content.txt`; 6,986 main-text words |
| Proposal, handover version (for comparison) | `proposal/Ridhwan_Research_Proposal_UM_handover_2026-11-03.docx` | Handover | Unchanged |
| Proposal source and build | `proposal/source/` (`content.txt`, `build.js`, `framework.png`, `arch.png`) | Post-review revision | `node build.js` (npm `docx`) |
| Slide deck (Claude Slides) | https://claude.ai/artifact/4RuYVim5WsRqG5aQLYJGas | Version id 1793687949-bd1f | 45 slides; shared with anyone with the link |
| Slide sources (full copy) | `slides/project/` | Same version | Version history; the deck is the source of truth |
| Research map page | `index.html` (+ `assets/`), https://claude.ai/artifact/1BnWNir54MvkSfH5uPfMiE | Version 9 (id 1793724829-12f9) | Matches the post-review proposal; 19 figures (8 interactive), including what is counted (PAC vs motion artefact, PAC vs AF; 24 hours to an ESVEA call) and a step-by-step dependency chain; E1 and E11 marked as awaiting confirmation; shared with anyone with the link |

---

## 2. Records in chronological order

| # | Stage | Record | Role | Feeds |
|---|---|---|---|---|
| 1 | Handover | `handover/00_HANDOVER.md` | State of the project at 3 Nov 2026 | Baseline |
| 2 | Handover | `handover/decisions/proposal-defence-decisions_part1.md` | Decision log, 20 Oct 2026 | Baseline |
| 3 | Handover | `handover/decisions/proposal-decisions-2026-11-02.md` | Decision log, 2 Nov 2026 | Decision 6g reversed by E1 |
| 4 | Handover | `handover/decisions/*` (audit plan, README, UM checklist) | Process | Housekeeping |
| 5 | Handover | `handover/checks/*.md` | Earlier checks; several superseded | Background |
| 6 | Handover | `handover/analyses/**/*.md` | RO1, simulation, Pulsewatch pre-check, Icentia11k clock time | §3.4, §4.2, Appendix C |
| 7 | Handover | `handover/review_paper/Review_Reference_Corrections.md` | Review paper corrections | Separate deliverable |
| 8 | Session | `index.html` | Research map page | Context |
| 9 | Review | `drafts/proposal_revisions_draft.md`, "Original review (verbatim)" | First review: 12 issues | E1 to E11 |
| 10 | Drafting | `drafts/proposal_revisions_draft.md` | Before/after text, budget, decisions (E1 partly superseded, see #20) | Docx and deck |
| 11 | Check | `drafts/Check_E11_Pilot_Rerun_Weight_0.5.md` | Pilot rerun instructions | E11 |
| 12 | Check | `drafts/Check_E2_Pulsewatch_Timestamps.md` | Timestamp check instructions | E2 |
| 13 | Verification | `drafts/Verification_Guo_H1_H2.md` | Guo, Bhurane, "first" claims | E4; §2.7 (optional) |
| 14 | Result | E11 rerun, recorded in draft E11 | Re-curated pilot values | E11 |
| 15 | Result | `drafts/Result_E2_Pulsewatch_Timestamps.md` | E2 pass | E2; trim T11 |
| 16 | Check | `drafts/Check_E11b_AF_Trial_Holdout_Subjects.md` | AF-only holdout check | E11 |
| 17 | Result | `drafts/Result_E11b_AF_Trial_Holdout_Subjects.md` | 8 (8); 5,483 | E11 |
| 18 | Applied | `slides/README.md` | Slide change history | Deck |
| 19 | Review | `drafts/Independent_Review_2026-11-03.md` | Independent review (C1 to C3, M1 to M4) and resolution | E1 revised; Table 3.4; §3.5, §3.9; abstract |
| 20 | Applied | `proposal/SUPERVISOR_RECONFIRMATION_E1_E11.md` | Current state of E1 and E11 for supervisors | E1, E11 |

---

## 3. Traceability: revision → docx → slides → records

Slide numbers are deck positions.

| ID | Source | Docx | Slides | Records | Status |
|---|---|---|---|---|---|
| **E1** (revised) | Review #1; independent review C1, C2 | §3.4 ¶2 and definitions; Eq. 3.1 π̂(m) = P(beat reported \| motion m, outside a gap); Eq. 3.2, 3.4 use π̂(mᵢ); §4.2; Appendix C; §3.6 pulse-deficit sweep | 14, 31, 42 | Draft E1 (superseded part), independent review, reconfirmation note | Applied; **supervisor reconfirmation pending** |
| C3 | Independent review | §3.5 (overnight whitepaper; Garmin's 24-hour confirmation; 24-hour logging in device verification); §3.9 fallback | 15, 19 | Independent review | Applied; written confirmation to file |
| M1 | Independent review | Table 3.4 row "Flags and silent loss" | 16 | Independent review | Applied |
| M2 | Independent review | none | 18 `preliminary-icentia`; research map page | Independent review | Applied |
| M4 | Independent review | Abstract: "one AF subject per cohort" | none | Independent review | Applied |
| E2 | Review #2 | §3.4 ¶1 | 14 | Draft E2; Check and Result E2 | Applied |
| E3 | #3 | §1.3 H2; Table 3.5; Table B.1 | 5, 13, 43 | Draft E3 | Applied |
| E4 | #4 | §3.4; §2.8; Guo et al. (2017) | 31, 42 | Draft E4; Verification | Applied |
| E5 | #5 | §3.6; Table 3.4 timing-noise row | 16, 19 | Draft E5 | Applied |
| E6 | #6 | §3.5 RQ3.4 | 15 | Draft E6 | Applied |
| E7 | #8 | §3.4; Table 3.2 | 14, 42 | Draft E7 | Applied |
| E8 | #9 | §3.4 ¶1 | 14 (notes) | Draft E8 | Decided; applied |
| E9 | #10 | §3.5; Appendix C | 15 | Draft E9 | Applied |
| E10 | #11 | Table 3.1; Table B.3 | none | Draft E10 | Applied |
| **E11** | #12; independent review M4 | Abstract; §4.1; Table 4.1; Table B.2 | 17 | Draft E11; Checks and Result E11b; reconfirmation note | Applied; **supervisor reconfirmation pending** |
| Trims | word limit | §1.1, §1.6, §2.1, §2.4, §3.4, §4.2, §5.1 | none | Draft trims | Applied |
| Refs | deck | none | 23, 24, 27, 28, 34, 36 to 39 | `slides/README.md` | Six slide-only sources removed (v49) |
| Page no. | deck | none | 31 | `slides/README.md` | Applied (v48) |
| H1 | housekeeping | §2.7 optional wording not applied | 9 | Verification | Open |
| H2 | housekeeping | Tables 2.1, 2.2 unchanged | 9, 10 | Verification | Closed |

---

## 4. Build checks (post-review revision, 3 November 2026)

| Check | Result |
|---|---|
| Docx text identical to a fresh build of `content.txt` | Yes |
| Main-text words, Chapter 1 to References | 6,986 (limit 7,000) |
| Words including the abstract | 7,326 (the handover was 7,270 under this rule, so the limit has been read as excluding the abstract) |
| Em dashes in the proposal | 0 |
| References | 67 |
| Equations 3.1 to 3.4 | One per line; the "\|" inside Equation 3.1 parses correctly in `build.js` |

---

## 5. Open before submission

1. Supervisor confirmation of **E1** (revised) and **E11**; approval of the final docx.
2. Garmin's 24-hour Enhanced BBI confirmation **in writing**; the proposal now refers to it.
3. Postgraduate Office: does the 7,000-word limit include the abstract (7,326 if so)?
4. Open the docx in Word and check layout, including the long Table 4.1 caption.
5. Optional: IEEE Xplore native search, then the §2.7 wording.
6. Ethics committee name; Pulsewatch permitted use in writing.
7. Remaining handover slide inconsistencies: `problem.html` wording, `gaps.html` gap wording, "et al." in reference slides.
8. Remove "Pending supervisor reconfirmation" lines from speaker notes after confirmation (the deck is shared by link).
9. Mock defence.
