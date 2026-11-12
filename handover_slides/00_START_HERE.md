# Proposal defence slides: handover for refinement

Prepared 12 November 2026 for a new session that will refine the proposal defence deck in **writing and presentation**. The candidate is Ridhwan Amin Azhari Bin Zabidi (UM FCSIT). The supervisors are Dr Bryan Raj and Assoc. Prof. Ismail Ahmedy.

## 1. The deck

| Item | Value |
|---|---|
| Live deck (Claude Slides artifact) | https://claude.ai/artifact/4RuYVim5WsRqG5aQLYJGas (opened in Claude Code as artifact `1bc5a5b1-f55e-4d31-8fbb-6d3cc1f92d80`) |
| Version at handover | Version 57, id `1794385399-32f4`, 56 slides |
| Local copy of every slide | `deck/project/deck.json` (slide order) and `deck/project/slides/<id>.html` (one file per slide; speaker notes in `<aside>`) |
| Change history | `deck/VERSION_HISTORY.md` |
| Generators for scripted slides | `deck/build_prelim_next.py` (slide 19), `deck/build_appendix_d.py` (D1 to D5), `deck/build_appendix_e.py` (E1 to E4), `deck/build_appendix_e5.py` (E5). Edit the generator, not only the HTML, or a rebuild will undo the change |
| Structure | Slides 1 to 23: main talk. 24 to 30: references. 31 to 56: appendix (backup slides for questions) |

**How to edit and publish (in a Claude Code session with the Artifact tool):**
1. Read the live deck first, with `Artifact` `action: "read"` on the URL. It may have changed since this copy was made; build on what comes back.
2. Edit the slide HTML files.
3. Publish to the same `url` with `root` set to the folder that holds `project/` and `file_path` set to `project/deck.json`. List every changed slide in `files` as `"project/slides/<id>.html"`. To add a slide, add its id to `order` in `deck.json`.
4. Never publish a slide file you have not read in that session.

## 2. Rules

1. **The proposal docx is the source of truth** (`proposal/Ridhwan_Research_Proposal_UM.docx`; plain-text source `proposal/content.txt`). Every number, claim, objective wording and citation on a slide must match it. If the docx is internally inconsistent, flag the problem; do not "fix" the slide away from the docx.
2. **The deck is for the proposal defence.** It presents what will be done and why, with preliminary evidence. It is not a progress report. Implementation work that has started since (a Track 1 runbook and code; a G1 reproduction check) does **not** belong in the main talk. See section 4.
3. **Supervisor comments on the early deck are binding** (section 3). Do not undo them.
4. **House style:** APA 7th edition; **no em dashes**; "to our knowledge" on every first-of-its-kind claim; RO verbs as agreed (RO1 investigate, RO2 develop and evaluate, RO3 evaluate, RO4 evaluate and validate).
5. **Jargon glosses:** at first use in the main talk, technical terms carry a plain-language gloss of at most five words in parentheses, for example "beat intervals (time between heartbeats)". There are 52 of them, on slides 2 to 9, 12 to 17 and 19. Keep them, or shorten them, but do not drop them.
6. **Visual system** (keep it):
   - **Colours:** monochrome ink `#1a1a1a`, greys `#3a3a3a` to `#d4d4d4`, a single accent `#9b1c1c` for emphasis and limits.
   - **Type:** Arial. Main titles 52 px, appendix titles 44 px, body and tables 22 to 24 px.
   - **Layout:** section padding `88px 112px 140px` on main slides and `88px 112px 120px` on the appendix.
   - **Page number:** `<p style="position:absolute;right:112px;bottom:56px;width:200px;text-align:right;font-size:24px;color:#6b6b6b">N</p>` on slides 2 to 22 and on `app-eq`. Renumber if slides move.
7. **Technical limits:**
   - Inline SVG must be well-formed XML: escape `<` as `&lt;`, or the slide fails to load.
   - Do not use `<sub>`; use Unicode subscripts (π̂, R̄, θ_block).
   - Content must end above y = 940 on main slides and y = 960 on appendix slides. Check with `tools/render_slides.js` (an approximate preview) and on the live deck.
8. **Speaker notes are visible to anyone with the link.** Four slides (`ro1-ro2`, `preliminary`, `app-eq`, `app-b3`) still carry a "Pending supervisor reconfirmation" line about revisions E1 and E11 (see `proposal/SUPERVISOR_RECONFIRMATION_E1_E11.md`). Remove the line once the supervisors confirm.

## 3. Dr Bryan's comments on the early deck (verbatim, from `context/ESVEA_Proposal_Defence1_early_deck_with_comments.pptx`)

| Early slide | Comment | How the current deck answers it |
|---|---|---|
| 1 (cover) | "Make all the words bigger in font." | Cover fonts enlarged |
| 5 (objectives) | "Check the RO1. Suggest changing the word quantify to something like investigate or study." | RO1 "investigate". Note: slide 4 still says "quantify", matching §1.2 of the docx |
| 5 | "Maybe it's to analyze not determine" | RO3 wording uses "evaluate" / "analysing" |
| 5 | "Here use words like evaluation and validation" | RO4 "evaluate and validate" |
| 7 (literature table) | "Highlight the limits that you want to emphasize." | Limits in accent red on slides 7 and 8 |
| 7 | "include a column talking generally about advantages" | Advantages column on slides 7 and 8, with a common-thread line |
| 12 (method) | "Use these words in the RO3" / "Substitute and validate or something like that in RO4." | Slide 12 headers updated |
| 14 (RO1, RO2) | "make the picture bigger and the writing smaller" | Picture enlarged; text at 19 px. Check that it still reads well |

The comments also set the expected register: academic thesis style, precise verbs, and evidence-led tables.

## 4. Content that may not belong in a proposal defence (decide in the new session)

The deck gained slides while implementation planning was under way. Review these against rule 2:

| Slides | What they hold | Suggested treatment (for the candidate to decide) |
|---|---|---|
| 19 `prelim-next` | What each preliminary result decided, the next step, and gates (pipeline reproduction, M3, M4) | Keep the "what it decided in the design" idea, which links results to the method. Remove plan-level detail such as gates and pipeline reproduction, or fold the slide into 17 and 18 |
| 52 to 56 `app-e1` to `app-e5` | Implementation plan: stages A to E, patient sets P0 to P3, simulator, schedule and decisions D1 to D7, readiness track to the first participant | Not in the docx. Either drop the whole of Appendix E, or keep at most one backup slide (schedule and gates, consistent with Tables 6.1 and 6.2). If cut, also update the `app-divider` list, the speaker notes of `thanks` and `prelim-next` that point to E, and the E-related lines in `deck/VERSION_HISTORY.md` |
| 47 to 50 `app-d1` to `app-d4` | Explainers (what is counted; one beat to an ESVEA call; hypotheses as If–Then; data chain) | Backup material derived from Ch 3. Keep if useful for questions; check wording against the docx |
| 51 `app-d5` | Pulsewatch pre-check result (not passed; detector-dependent) | Keep as backup: it is cited in §3.4 |
| 18 `preliminary-icentia` | Table 4.2 | Leave as is. A reproduction run found the PVC 20% value is 69.9% on today's PhysioNet files against 70.0% in the docx. The supervisors decide whether Table 4.2 changes; until then the slide matches the docx |

Do not add new progress from the implementation (G1 results, code, runbook) to the deck.

## 5. Files in this package

| Path | What it is |
|---|---|
| `00_START_HERE.md` | This brief |
| `01_SLIDE_INVENTORY.md` | All 56 slides: id, title, section, docx source, word counts (slide and notes), flags |
| `02_REVIEW_GUIDE.md` | What to refine in writing and presentation, with checks |
| `deck/` | Local copy of the deck, version history, slide generators |
| `proposal/` | Proposal docx, its text source `content.txt`, Figures 3.1 (`framework.png`) and 3.2 (`arch.png`), the supervisor reconfirmation note |
| `context/` | Early deck with Dr Bryan's comments; UM FSKTM proposal-defence checklist; defence and proposal decision logs; the implementation plan (for awareness only, not for the slides) |
| `tools/render_slides.js` | Approximate preview and content-bottom check (needs Playwright) |
| `tools/check_svg.py` | Checks that every inline SVG parses |

Related live artifact (read-only context): the research map, https://claude.ai/artifact/1BnWNir54MvkSfH5uPfMiE. It is explanatory, not a source of truth; where it differs from the docx, the docx wins.

## 6. Prompt to paste into the new session

> You are refining my PhD proposal defence deck (Claude Slides artifact https://claude.ai/artifact/4RuYVim5WsRqG5aQLYJGas) in writing and presentation. Read `handover_slides/00_START_HERE.md`, `01_SLIDE_INVENTORY.md` and `02_REVIEW_GUIDE.md`. The proposal docx is the source of truth; the deck is for the proposal defence, not a progress report. First read the live deck with the Artifact tool. Then give me a review: for each main-talk slide, what to tighten in wording, layout and emphasis; and a recommendation for the slides flagged in section 4 of the brief. Do not publish changes until I approve the list. Keep Dr Bryan's comments, the glosses, the visual system and the page numbering rules.
