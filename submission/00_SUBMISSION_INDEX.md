# ESVEA Proposal Defence: Submission Index

**Candidate:** Ridhwan Amin Azhari Bin Zabidi (25118475), FCSIT, Universiti Malaya
**Supervisors:** Dr. Bryan Raj A/L Peter Jabaraj; Assoc. Prof. Ts. Dr. Ismail Bin Ahmedy
**Compiled:** 3 November 2026
**Repository branch:** `claude/nifty-meitner-605ymp` (RidhwanAmin/stgnn-ridu-um)

This index maps every markdown record, from the handover to the latest change, to the two submission deliverables: the proposal docx and the slide deck. `COMPILED_CONTEXT.md` holds the full text of every record in the order below.

> **Pending supervisor reconfirmation: E1 and E11.** Both are applied in the docx and the deck. Revert using the "Current" text in `drafts/proposal_revisions_draft.md` if either is not confirmed. Details: `proposal/SUPERVISOR_RECONFIRMATION_E1_E11.md`.

---

## 1. Deliverables

| Deliverable | Location | Version | Status |
|---|---|---|---|
| Proposal (Word) | `proposal/Ridhwan_Research_Proposal_UM.docx` | Rebuilt 3 Nov 2026 from `proposal/source/content.txt` | All approved revisions applied; 6,983 main-text words; 45 pages (LibreOffice render; check in Word) |
| Proposal, handover version (for comparison) | `proposal/Ridhwan_Research_Proposal_UM_handover_2026-11-03.docx` | Handover | Unchanged |
| Proposal source and build | `proposal/source/` (`content.txt`, `build.js`, `framework.png`, `arch.png`) | 3 Nov 2026 | `node build.js` (npm `docx`) |
| Slide deck (Claude Slides) | https://claude.ai/artifact/4RuYVim5WsRqG5aQLYJGas | Version 49 | 45 slides; 20 changed this session |
| Changed slide sources (copies) | `slides/project/slides/` | v44, v46, v48, v49 | For version history; the deck is the source of truth |
| Research map page | `index.html` (+ `assets/`), https://claude.ai/artifact/1BnWNir54MvkSfH5uPfMiE | Version 3 | Methodology and architecture context; pilot table updated |

---

## 2. Records in chronological order

| # | Stage | Record | Role | Feeds |
|---|---|---|---|---|
| 1 | Handover | `handover/00_HANDOVER.md` | State of the project at 3 Nov 2026 | Baseline for everything below |
| 2 | Handover | `handover/decisions/proposal-defence-decisions_part1.md` | Decision log, 20 Oct 2026 (RO4 framing) | Baseline |
| 3 | Handover | `handover/decisions/proposal-decisions-2026-11-02.md` | Decision log, 2 Nov 2026 (items 6a to 6k) | Decision **6g is reversed by E1** |
| 4 | Handover | `handover/decisions/proposal-audit-plan.md`, `README.md`, `UM_FSKTM_PhD_Proposal_Defence_Checklist.md` | Audit plan, index, UM checklist | Housekeeping |
| 5 | Handover | `handover/checks/*.md` (6 files) | Earlier checks; several superseded (see handover §8) | Background only |
| 6 | Handover | `handover/analyses/**/*.md` (5 files) | RO1, simulation, Pulsewatch pre-check, Icentia11k clock-time evidence | Appendix C, Sections 3.4, 4.2 |
| 7 | Handover | `handover/review_paper/Review_Reference_Corrections.md` | Review paper corrections | Separate deliverable |
| 8 | Session | `index.html` | Research map: methodology and ST-GNN architecture | Context page |
| 9 | Review | `drafts/proposal_revisions_draft.md` → "Original review (verbatim)" | Defence review: 12 issues, feasibility, housekeeping | E1 to E11, trims |
| 10 | Drafting | `drafts/proposal_revisions_draft.md` | Before/after text, word budget, issue map, slide drafts, decisions | **Docx and deck** |
| 11 | Check | `drafts/Check_E11_Pilot_Rerun_Weight_0.5.md` | Instructions: pilot rerun at weight 0.5 | E11 |
| 12 | Check | `drafts/Check_E2_Pulsewatch_Timestamps.md` | Instructions: Pulsewatch timestamp continuity | E2 |
| 13 | Verification | `drafts/Verification_Guo_H1_H2.md` | Guo et al. (2017) verified; Bhurane 93.96% confirmed; "first" claims hold | E4 reference; Section 2.7 (optional) |
| 14 | Result | E11 rerun (re-curated labels), recorded in draft E11 | New pilot values; legacy values withdrawn | E11 |
| 15 | Result | `drafts/Result_E2_Pulsewatch_Timestamps.md` | E2 pass (file-name local time; not UTC) | E2 clause, trim T11 |
| 16 | Check | `drafts/Check_E11b_AF_Trial_Holdout_Subjects.md` | Instructions and reply template | E11 Table 4.1 row |
| 17 | Result | `drafts/Result_E11b_AF_Trial_Holdout_Subjects.md` | 8 (8); 5,483, all AF; row renamed "Pulsewatch AF-only holdouts" | E11 |
| 18 | Applied | `proposal/SUPERVISOR_RECONFIRMATION_E1_E11.md` | What still needs supervisor confirmation | E1, E11 |
| 19 | Applied | `slides/README.md` | Which slides changed, by deck version | Deck v44, v46, v48 |

---

## 3. Traceability: revision → docx → slides → records

Slide numbers are deck positions (the viewer's numbering).

| ID | Review issue | Docx (sections, tables, equations) | Slides | Records | Status |
|---|---|---|---|---|---|
| **E1** | #1 | §3.4 ¶2 and definitions; Eq. 3.1, 3.2, 3.4; §4.2; Appendix C; Garmin reference (2023) | 14 `ro1-ro2`; 31 `app-eq`; 42 `app-b3` (redrawn v46) | Draft E1; Garmin whitepaper (cited); reconfirmation note | Applied; **supervisor reconfirmation pending** |
| E2 | #2 | §3.4 ¶1 (pseudo-days; Pulsewatch order across days) | 14 `ro1-ro2` | Draft E2; Check E2; Result E2 | Applied |
| E3 | #3 | §1.3 H2; Table 3.5; Table B.1 (new row) | 5 `rq-ro`; 13 `validation-matrix`; 43 `app-c1` | Draft E3 | Applied |
| E4 | #4 | §3.4 ¶2; §2.8; Guo et al. (2017) reference | 31 `app-eq` (notes); 42 `app-b3` | Draft E4; Verification | Applied |
| E5 | #5 | §3.6; Table 3.4 (new row) | 16 `ro4`; 19 `risks` | Draft E5 | Applied |
| E6 | #6 | §3.5 (RQ3.4) | 15 `ro3` | Draft E6 | Applied |
| E7 | #8 | §3.4 ¶2; Table 3.2 (RQ2.3) | 14 `ro1-ro2` (notes); 42 `app-b3` | Draft E7 | Applied |
| E8 | #9 | §3.4 ¶1 (rate head) | 14 `ro1-ro2` (notes) | Draft E8 | Decided (keep as auxiliary); applied |
| E9 | #10 | §3.5 (key secondary); Appendix C | 15 `ro3` | Draft E9 | Applied |
| E10 | #11 | Table 3.1 (RO4a); Table B.3 (new) | none | Draft E10 | Applied |
| **E11** | #12 | Abstract; §4.1; Table 4.1 and caption; Table B.2 | 17 `preliminary` | Draft E11; Check E11; Check and Result E11b; reconfirmation note | Applied; **supervisor reconfirmation pending** |
| T1, T3 to T8, T11 | word limit | §3.4, §5.1, §2.4, §2.1, §1.1, §3.4, §4.2, §1.6 (Kapsecker, Montanaro, Ye, Abedi references removed; PPV defined in §2.6) | none | Draft trims | Applied |
| T2 | word limit | Merged into E11 (§4.1 ¶2) | none | Draft | Superseded |
| Title | #7 | No change (prepared answer) | none | Draft §4 | Decided |
| H1 | housekeeping | Optional §2.7 wording not applied (needs IEEE Xplore native search) | 9 `gaps` unchanged | Verification | Open |
| H2 | housekeeping | Tables 2.1, 2.2 unchanged (93.96% confirmed) | 9 `gaps`, 10 `closest` unchanged | Verification | Closed |
| Page no. | deck | none | 31 `app-eq` printed number 30 → 31 (v48) | `slides/README.md` | Applied |
| Refs | deck | none (proposal already excludes them) | 23 `refs-1`, 24 `refs-2`, 27 `refs-5`, 28 `refs-6`; 34 `app-a3`, 36 `app-a5`, 37 `app-a6`, 38 `app-a7`, 39 `app-a8` (v49) | `slides/README.md` | Applied: six slide-only sources removed |

---

## 4. Deck version history (this session)

| Version | Change | Slides |
|---|---|---|
| 44 | Approved revisions E1 to E11 | 5, 13, 14, 15, 16, 17, 19, 31, 42 (caption), 43 |
| 46 | `app-b3` redrawn: stage cards, loss-routing table, schematic retention curves (no fitted values) | 42 |
| 48 | `app-eq` printed page number corrected | 31 |
| 49 | Removed six sources not in the proposal (Aguilar 2021, Bacevičius 2022, Gruwez 2024, Sun 2024, Väliaho 2019, Zahid 2023): reference entries and the appendix rows citing them | 23, 24, 27, 28, 34, 36 to 39 |

Speaker notes on slides 14, 17, 31 and 42 carry a "Pending supervisor reconfirmation" line. Remove it after confirmation.

---

## 5. Build checks (docx, 3 November 2026)

| Check | Result |
|---|---|
| Main-text words (Chapter 1 to References; table rows counted) | 6,983 (limit 7,000) |
| Em dashes | 0 |
| Every reference cited, every citation referenced | Yes |
| Equation 3.1 on one line | Yes (LibreOffice render) |
| Pages | 45 (handover: 43) |

---

## 6. Open before submission

1. Supervisor confirmation of **E1** and **E11**; general approval of the final docx.
2. Open the docx in Word and check layout, including the long Table 4.1 caption.
3. Optional: IEEE Xplore native search, then the §2.7 wording (+5 words).
4. Garmin's 24/7 Enhanced BBI confirmation in writing.
5. Ethics committee name (PPUM MREC or UMMC MREC); Pulsewatch permitted use in writing; Postgraduate Office word-count rule.
6. Remaining handover slide inconsistencies not in scope this session: `problem.html` wording, `gaps.html` gap wording, "et al." in reference slides.
7. Mock defence.
