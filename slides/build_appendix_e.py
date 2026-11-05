"""Build Appendix E slides (E1-E4): the implementation plan from the Icentia11k proof of concept
to the full analyses, drawn against work already completed. Deck style as Appendix D."""
from pathlib import Path

OUT = Path(__file__).resolve().parent / 'project' / 'slides'
INK, MID, GREY, LIGHT, ACC = '#1a1a1a', '#4a4a4a', '#6b6b6b', '#d4d4d4', '#9b1c1c'
SEC = ('background:#ffffff;color:#1a1a1a;font-family:Arial, Helvetica, sans-serif;'
       'padding:88px 112px 120px;display:flex;flex-direction:column;gap:22px')
H2 = 'font-size:44px;font-weight:700;line-height:1.15'
P = 'font-size:24px;line-height:1.3'
SRC = 'font-size:24px;line-height:1.3;color:#6b6b6b'
TBL = 'width:100%;font-size:24px;color:#1a1a1a;border:1px solid #8a8a8a'


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def write(sid, body, notes):
    html = f'<section id="{sid}" style="{SEC}">\n{body}\n<aside>{notes}</aside>\n</section>\n'
    (OUT / f'{sid}.html').write_text(html)
    print(sid, len(html))


def text(x, y, s, size=22, fill=INK, anchor='start', weight='400'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{esc(s)}</text>'


def lines(x, y, rows, size=22, fill=INK, gap=27, anchor='start', weight='400'):
    return ''.join(text(x, y + i * gap, r, size, fill, anchor, weight) for i, r in enumerate(rows))


# ------------------------------------------------------------------ E1: done -> planned
def e1():
    W, H = 1696, 620
    s = []
    done = [
        ('P0 preliminary RO1', ['298 patients; Tables 4.2, 4.3', 'loss large, burden-dependent']),
        ('Clock-time check', ['segments untimed', 'pseudo-days; rate × 24']),
        ('Pulsewatch pre-check', ['motion effect measurable;', 'level detector-dependent']),
        ('Cross-device pilot', ['ranking transferred;', 'threshold did not']),
        ('Appendix C simulation', ['pooling by block (Eq. 3.4)', 'robust to poor coverage']),
    ]
    stages = [
        ('A', 'Data pipeline', ['beat and interval tables', 'for 11,000 patients'], 'Every later stage reads it;', 'must match Tables 4.2, 4.3'),
        ('B', 'RO1 in full; H1 on P1', ['filter curves; H1;', 'origin and morphology loss'], 'H1 must be tested on', 'patients not used before'),
        ('C', 'Training simulator', ['flags, motion, silent loss', 'and gaps on ECG intervals'], 'Labels exist only on ECG;', 'model needs watch-like input'),
        ('D', 'RO2: train and freeze', ['P2; baselines, ablations;', 'H2; frozen at M4'], 'Freeze before P3, so RO4a', 'is an honest test'),
        ('E', 'RO4a on P3', ['degrade, re-estimate,', 'compare with ECG truth'], 'Only place substitution', 'meets ECG truth'),
    ]
    links = [(0, 0), (0, 1), (0, 2), (0, 4), (1, 0), (1, 3), (2, 2), (2, 3), (3, 3), (3, 4), (4, 3), (4, 4)]
    bw, gap = 316, 29
    x = lambda i: i * (bw + gap)
    # row titles
    s.append(text(0, 22, 'Completed (proof of concept and checks)', 24, MID, weight='700'))

    for a, b in links:  # connectors first, under the boxes
        x1, x2 = x(a) + bw / 2, x(b) + bw / 2
        s.append(f'<path d="M{x1},{170} C{x1},{235} {x2},{235} {x2},{318}" fill="none" stroke="#b5b5b5" stroke-width="2"/>')
    s.append(f'<rect x="0" y="278" width="330" height="32" fill="#ffffff"/>')
    s.append(text(0, 302, 'Planned stages (not started)', 24, MID, weight='700'))
    for i, (t, d) in enumerate(done):
        s.append(f'<rect x="{x(i)}" y="40" width="{bw}" height="130" fill="{INK}"/>')
        s.append(text(x(i) + 16, 76, t, 24, '#ffffff', weight='700'))
        s.append(lines(x(i) + 16, 110, d, 22, '#ffffff'))
    for i, (k, t, d, w1, w2) in enumerate(stages):
        s.append(f'<rect x="{x(i)}" y="318" width="{bw}" height="290" fill="#ffffff" stroke="{INK}" stroke-width="2" stroke-dasharray="10 6"/>')
        s.append(text(x(i) + 16, 356, f'{k}  {t}', 24, INK, weight='700'))
        s.append(lines(x(i) + 16, 392, d, 20, MID))
        s.append(f'<line x1="{x(i) + 16}" x2="{x(i) + bw - 16}" y1="462" y2="462" stroke="{LIGHT}" stroke-width="2"/>')
        s.append(text(x(i) + 16, 494, 'Why', 22, ACC, weight='700'))
        s.append(lines(x(i) + 16, 526, [w1, w2], 20, INK))
    svg = (f'<svg aria-label="Two rows. Top: five completed pieces of work, filled boxes: the P0 preliminary RO1 analysis, the clock-time check, the Pulsewatch pre-check, the cross-device pilot and the Appendix C simulation. '
           f'Bottom: five planned stages, dashed boxes, A data pipeline, B RO1 in full with H1 on P1, C training simulator, D RO2 train compare and freeze, E RO4a on P3, each with why it is needed. '
           f'Lines link each completed piece to the stages it feeds." width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + ''.join(s) + '</svg>')
    body = (f'<h2 style="{H2}">Appendix E1: From Proof of Concept to the Full Analyses</h2>\n{svg}\n'
            f'<p style="{SRC}">Filled: done. Dashed: planned, not started. Each line shows what a completed result fixes in a later stage: for example, P0 sets the size of P1, calibrates the simulator and showed RO4a has enough ESVEA-positive patients (67 of 298).</p>')
    notes = ('Held for questions, if asked how the preliminary work becomes the thesis. The top row is done; the bottom row is the plan, not yet started. '
             'Read the lines: the P0 analysis is a proof of concept, not the H1 test, so H1 needs new patients (stage B), and P0 also calibrates the training simulator (C) and showed RO4a will have enough ESVEA-positive patients (E). '
             'The clock-time check is why every interval stays inside a segment (A) and why training uses pseudo-days and a patient-level rate (D). '
             'The Pulsewatch pre-check is why π̂(m) enters the simulator (C) and is frozen with a detector sensitivity analysis (D). '
             'The pilot showed the interval representation carries rhythm information but that a threshold does not transfer, which is why scores are calibrated and the substitution is tested under device losses. '
             'The Appendix C simulation fixed pooling by block, which the estimator and RO4a coverage operator use.')
    write('app-e1', body, notes)


# ------------------------------------------------------------------ E2: patient sets and data volume
def e2():
    W, H = 1696, 600
    s = []
    s.append(text(0, 26, 'Icentia11k, about 11,000 patients, split into four sets that never overlap (Table B.3)', 24, INK, weight='700'))
    X0, X1 = 0, 1696
    tot = 11000
    segs = [('P0', 300, INK, 'done'), ('P1', 550, '#ffffff', 'D1'), ('P2', 9850, '#ececec', 'D2'), ('P3', 300, ACC, 'locked')]
    x = X0
    for name, n, col, st in segs:
        w = (X1 - X0) * n / tot
        dash = ' stroke-dasharray="8 5"' if st == 'D1' else ''
        s.append(f'<rect x="{x:.1f}" y="48" width="{w:.1f}" height="64" fill="{col}" stroke="{INK}" stroke-width="2"{dash}/>')
        x += w
    W_ = X1 - X0
    labels = [  # (segment centre in patients, label x, anchor, title, lines)
        (150, 0, 'start', 'P0  300, preliminary RO1', ['done (298 analysed);', 'never reused for testing']),
        (575, 380, 'start', 'P1  H1 test', ['new patients; size from a', 'power simulation on P0 (D1)']),
        (5775, 820, 'start', 'P2  RO2 development', ['remaining patients, split by', 'patient: train, val., test (D2)']),
        (10850, X1, 'end', 'P3  about 300, RO4a', ['drawn now, not read until', 'the model is frozen (M4)']),
    ]
    for c, lx_, anchor, t, d in labels:
        cx = W_ * c / tot
        s.append(f'<path d="M{cx:.1f},112 L{cx:.1f},124 L{lx_ if anchor == "start" else lx_:.1f},124 L{lx_:.1f},136" fill="none" stroke="{GREY}" stroke-width="2"/>')
        s.append(text(lx_, 160, t, 22, INK, anchor, '700'))
        s.append(lines(lx_, 188, d, 22, MID, 26, anchor))
    s.append(text(0, 262, 'Guards: set lists and checksums committed before analysis; the loader refuses a patient from the wrong set. P1 width not to scale.', 22, GREY))
    # data volume, log scale
    s.append(text(0, 330, 'What to download: beat labels, not the ECG waveform', 24, INK, weight='700'))
    import math
    rows = [('Raw ECG, all patients', 1100, 'about 1.1 TB (PhysioNet)', False),
            ('Raw ECG, 298 patients (P0)', 31, 'about 31 GB', False),
            ('Beat labels, all patients', 6, 'about 6 GB (2.77 billion beats)', True),
            ('Beat labels, 298 patients', 0.2, 'about 0.2 GB', True)]
    L, R = 420, 1500
    lx = lambda gb: L + (math.log10(gb) - math.log10(0.1)) / (math.log10(2000) - math.log10(0.1)) * (R - L)
    for i, (t, gb, lab, use) in enumerate(rows):
        y = 356 + i * 56
        s.append(text(0, y + 28, t, 22, INK))
        s.append(f'<rect x="{L}" y="{y + 6}" width="{lx(gb) - L:.1f}" height="32" fill="{ACC if use else "#bdbdbd"}"/>')
        s.append(text(lx(gb) + 12, y + 30, lab, 22, INK))
    for gb, t in [(0.1, '0.1 GB'), (1, '1 GB'), (10, '10 GB'), (100, '100 GB'), (1000, '1 TB')]:
        s.append(f'<line x1="{lx(gb):.1f}" x2="{lx(gb):.1f}" y1="352" y2="584" stroke="{LIGHT}" stroke-width="1.5"/>')
        s.append(text(lx(gb), 600, t, 20, GREY, 'middle'))
    svg = (f'<svg aria-label="Top: a bar of about 11,000 Icentia11k patients split into P0, 300 patients, done; P1, the H1 test, size to be set by a power simulation; P2, the remaining patients for RO2; and P3, about 300 patients held out until the model is frozen. '
           f'Bottom: data sizes on a log scale. Raw ECG is about 1.1 TB for all patients and 31 GB for the 298 preliminary patients; beat labels, which are all the analysis needs, are about 6 GB for all patients and 0.2 GB for 298." width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + ''.join(s) + '</svg>')
    body = (f'<h2 style="{H2}">Appendix E2: Patient Sets and Data Volume</h2>\n{svg}\n'
            f'<p style="{P}"><b>Why:</b> separate sets keep each claim honest (H1 on patients it was not formed on; RO4a on patients the model never saw). Labels only, because RO1 and RO2 read beat annotations, not the waveform (§3.7); the full dataset then fits one workstation if streamed patient by patient.</p>\n'
            f'<p style="{SRC}">Sizes estimated from PhysioNet figures (1.1 TB; 541,794 segments of 1,048,577 int16 samples; 2,774,054,987 labelled beats) and the P0 run (median 57.5 h per patient).</p>')
    notes = ('Held for questions. The four sets come from Table B.3. P0 is the 300 patients of the preliminary analysis; it formed the H1 idea, so H1 is tested on new patients, P1, whose size is fixed by a power simulation on P0 before any data are read. '
             'P2 is everything else, split by patient. P3, about 300, is drawn now and stays unopened until the model, π̂(m) and the gate are frozen at M4. '
             'The lower panel answers the storage question: the waveform is 1.1 TB, but the study needs only the beat labels, about 6 GB for all patients and 0.2 GB for the 298 already analysed. Sizes are estimates from the PhysioNet page and the P0 run.')
    write('app-e2', body, notes)


# ------------------------------------------------------------------ E3: simulator vs RO4a degradation
def e3():
    W, H = 1696, 470
    s = []
    # three tracks of beats
    beats = [0, 1, 2, 3, 3.6, 5.0, 6, 7, 8, 9, 10, 11, 12, 13, 13.6, 15, 16, 17, 18, 19]
    pac = {4, 14}
    X = lambda b: 230 + b * 66
    tracks = [('1  Icentia11k (ECG)', 60), ('2  Simulated watch', 190), ('3  Truth kept', 330)]
    for t, y in tracks:
        s.append(text(0, y + 8, t, 22, INK, weight='700'))
        s.append(f'<line x1="220" x2="1520" y1="{y + 30}" y2="{y + 30}" stroke="{LIGHT}" stroke-width="2"/>')
    # motion band and gap on track 2
    s.append(f'<rect x="{X(6.5)}" y="168" width="{X(10.5) - X(6.5)}" height="68" fill="#ececec"/>')
    s.append(text(X(8.5), 162, 'motion episode', 20, MID, 'middle'))
    s.append(f'<rect x="{X(15.6)}" y="168" width="{X(17.6) - X(15.6)}" height="68" fill="#ffffff" stroke="{GREY}" stroke-width="2" stroke-dasharray="6 5"/>')
    s.append(text(X(16.6), 162, 'gap: unobserved time', 20, MID, 'middle'))
    for i, b in enumerate(beats):
        p = i in pac
        col = ACC if p else INK
        s.append(f'<line x1="{X(b)}" x2="{X(b)}" y1="{60 + (6 if p else 12)}" y2="90" stroke="{col}" stroke-width="{5 if p else 3}"/>')
        dropped = (i == 9)          # silent loss at motion
        gap = 15.6 < b < 17.6
        if not dropped and not gap:
            flag = p or (6.5 < b < 10.5)
            s.append(f'<line x1="{X(b)}" x2="{X(b)}" y1="{190 + (6 if p else 12)}" y2="220" stroke="{col}" stroke-width="{5 if p else 3}"/>')
            if flag:
                s.append(f'<circle cx="{X(b)}" cy="{186}" r="6" fill="none" stroke="{INK}" stroke-width="2"/>')
        if dropped:
            s.append(f'<line x1="{X(b) - 8}" x2="{X(b) + 8}" y1="{198}" y2="{214}" stroke="{ACC}" stroke-width="3"/><line x1="{X(b) + 8}" x2="{X(b) - 8}" y1="198" y2="214" stroke="{ACC}" stroke-width="3"/>')
        lab = 'PAC' if p else ('missed' if dropped else ('in gap' if gap else ''))
        s.append(f'<line x1="{X(b)}" x2="{X(b)}" y1="{330 + (6 if p else 12)}" y2="360" stroke="{col if not (dropped or gap) else "#9a9a9a"}" stroke-width="{5 if p else 3}"/>')
        if lab and lab != 'in gap':
            s.append(text(X(b), 390, lab, 20, ACC if p else MID, 'middle'))
    s.append(text(X(16.6), 390, 'in gap', 20, MID, 'middle'))
    s.append(text(0, 448, 'Open circle: simulated low-confidence flag. Cross: beat dropped without a flag (silent loss, probability 1 − π̂(m)).', 22, GREY))
    svg = (f'<svg aria-label="Three beat tracks over the same stretch. Track 1: Icentia11k ECG beats with two PACs marked. Track 2: the simulated watch stream: during a motion episode beats are flagged and one is dropped silently; a gap removes a stretch as unobserved time; the PACs are flagged. Track 3: the truth kept alongside, with every beat, the PACs, the missed beat and the beats inside the gap marked." width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + ''.join(s) + '</svg>')
    rows = [('Device flag', 'Garmin rules: motion-affected, abnormally short or long', 'Thresholds from the P0 filter results (Table 4.2)'),
            ('Motion', 'Drives flags and silent loss', '<b>Open (D4):</b> Icentia11k has no accelerometer; sample episodes from Pulsewatch'),
            ('Silent loss', 'Drop with probability 1 − π̂(m)', 'π̂(m) from Pulsewatch; the pre-check showed the motion effect is measurable'),
            ('Gaps', 'Unobserved time, by block on pseudo-days', 'Clock-time check: segments untimed, so blocks are assigned at random')]
    tr = ''.join(f'<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>' for a, b, c in rows)
    body = (f'<h2 style="{H2}">Appendix E3: The Training Simulator (Stage C)</h2>\n{svg}\n'
            f'<table style="{TBL}"><tr><th style="width:15%;text-align:left">Operator</th><th style="width:37%;text-align:left">Rule</th><th style="width:48%;text-align:left">Calibrated from completed work</th></tr>{tr}</table>\n'
            f'<p style="{P}"><b>Why:</b> Icentia11k has the labels but none of the watch&#39;s losses; the model must learn from watch-like input with exact targets. RO4a later uses a <b>separate</b> degradation, sampled independently and adding pulse deficit and timing noise, so it is not tested on its own training losses.</p>')
    notes = ('Held for questions, if asked how a model trained on ECG can work on a watch. Icentia11k gives true labels for every beat but no flags, motion or gaps. '
             'The simulator adds them following the Garmin specification: beats in motion episodes are flagged, some are dropped without a flag at a rate set by π̂(m), and stretches are removed as gaps. '
             'The truth is kept alongside, so the training targets stay exact. Each rule is calibrated from work already done: the P0 filter results set the flag thresholds, the Pulsewatch pre-check showed the motion effect can be measured, and the clock-time check is why blocks are assigned at random on pseudo-days. '
             'Motion itself is the open choice D4: Icentia11k has no accelerometer, so motion episodes would be sampled from Pulsewatch. '
             'RO4a does not reuse this code; its degradation is sampled independently and adds pulse deficit and timing noise.')
    write('app-e3', body, notes)


# ------------------------------------------------------------------ E4: schedule, gates, decisions
def e4():
    W, H = 1696, 450
    s = []
    sems = ['S2', 'S3', 'S4', 'S5', 'S6', 'S7']
    L, R = 380, 1696
    cw = (R - L) / 6
    for i, t in enumerate(sems):
        s.append(f'<rect x="{L + i * cw:.1f}" y="0" width="{cw:.1f}" height="40" fill="{"#f0f0f0" if i % 2 == 0 else "#ffffff"}"/>')
        s.append(text(L + i * cw + cw / 2, 28, t + (' (now)' if t == 'S2' else ''), 22, INK, 'middle', '700'))
    rows = [('A  Data pipeline', 0, 1, None),
            ('B  RO1 in full; H1 on P1', 0, 2, None),
            ('Pulsewatch: RQ1.1, π̂(m), lag', 0, 2, None),
            ('C  Training simulator', 1, 2, None),
            ('D  RO2 train, compare, freeze', 1, 3, None),
            ('E  RO4a on P3', 3, 5, None),
            ('RO3 cohort (context)', 0, 5, 'grey')]
    for i, (t, a, b, g) in enumerate(rows):
        y = 56 + i * 50
        s.append(text(0, y + 26, t, 22, GREY if g else INK))
        s.append(f'<rect x="{L + a * cw + 6:.1f}" y="{y + 6}" width="{(b - a) * cw - 12:.1f}" height="28" fill="{"#c9c9c9" if g else INK}"/>')
    gates = [(0.95, 'Tables 4.2, 4.3 reproduced', 'end'), (1.9, 'M3 RO1 paper', 'start'), (2.95, 'M4 freeze; P3 opens', 'start')]
    for xi, t, anchor in gates:
        x = L + xi * cw
        s.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="44" y2="410" stroke="{ACC}" stroke-width="3" stroke-dasharray="8 6"/>')
        s.append(f'<path d="M{x:.1f},{416} l-11,14 l11,14 l11,-14 z" fill="{ACC}"/>')
        s.append(text(x - 18 if anchor == 'end' else x + 18, 438, t, 22, ACC, anchor, '700'))
    svg = (f'<svg aria-label="Schedule from semester 2 to 7. Data pipeline in S2; RO1 in full with H1 in S2 and S3; Pulsewatch work in S2 and S3; training simulator in S3; RO2 in S3 and S4; RO4a in S5 and S6; the RO3 cohort runs alongside from S2 to S6. Gates: Tables 4.2 and 4.3 reproduced by the pipeline at the end of S2; M3 RO1 paper in S3; M4 model frozen in S4, after which P3 opens." width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + ''.join(s) + '</svg>')
    dec = [('D1', 'Size of P1', 'Power simulation on P0', 'S2'),
           ('D2', 'P2 split', 'Remaining patients, 70/15/15 by patient', 'S2'),
           ('D3', 'AF stretches', 'RO1 with and without; out of the RO2 count target', 'S2'),
           ('D4', 'Motion for training', 'Sample episodes from Pulsewatch', 'S3'),
           ('D5', 'N, k, L', 'Chosen on validation; reported as sensitivity', 'S3'),
           ('D6', 'Training losses', 'Weighted cross-entropy plus Poisson count', 'S3'),
           ('D7', 'GPU access', 'Faculty server or cloud allocation', 'S2')]
    half = [dec[:4], dec[4:]]
    cells = ''
    for part in half:
        tr = ''.join(f'<tr><td><b>{a}</b> {b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in part)
        cells += (f'<table style="flex:1;font-size:24px;color:#1a1a1a;border:1px solid #8a8a8a"><tr><th style="width:34%;text-align:left">Decision</th><th style="width:52%;text-align:left">Proposed default</th><th style="width:14%;text-align:left">By</th></tr>{tr}</table>')
    body = (f'<h2 style="{H2}">Appendix E4: Schedule, Gates and Open Decisions</h2>\n{svg}\n'
            f'<div style="display:flex;flex-direction:row;gap:24px;align-items:start">{cells}</div>\n'
            f'<p style="{SRC}">Semesters and milestones from Tables 6.1 and 6.2. Defaults fill choices the proposal leaves open; each is to be agreed with the supervisors.</p>')
    notes = ('Held for questions. The order follows Table 6.1. First gate, end of this semester: the new pipeline must reproduce Tables 4.2 and 4.3 exactly, so the full run starts from a verified base. '
             'RO1 and the Pulsewatch work run in S2 and S3 because RO2 needs their outputs: the retention curves and π̂(m). The simulator comes before RO2 training. '
             'M4 in S4 is the hard gate: the model, π̂(m) and the gate are frozen, and only then is P3 opened for RO4a in S5 and S6. The cohort runs alongside and feeds RO4a coverage when available. '
             'The seven decisions are choices the proposal leaves open; the proposed defaults are for agreement with the supervisors, and D4, motion for training, is the largest.')
    write('app-e4', body, notes)


e1(); e2(); e3(); e4()
