"""Build Appendix D slides (D1-D5) for the defence deck, in the deck's own style."""
import math
from pathlib import Path

OUT = Path('/home/user/stgnn-ridu-um/slides/project/slides')
INK, MID, GREY, LIGHT, ACC = '#1a1a1a', '#4a4a4a', '#6b6b6b', '#d4d4d4', '#9b1c1c'
SEC = ('background:#ffffff;color:#1a1a1a;font-family:Arial, Helvetica, sans-serif;'
       'padding:88px 112px 120px;display:flex;flex-direction:column;gap:24px')
H2 = 'font-size:44px;font-weight:700;line-height:1.15'
P = 'font-size:24px;line-height:1.3'
SRC = 'font-size:24px;line-height:1.3;color:#6b6b6b'
TBL = 'width:100%;font-size:24px;color:#1a1a1a;border:1px solid #8a8a8a'


def f(v):
    return f'{v:.1f}'.rstrip('0').rstrip('.')


def write(sid, body, notes):
    html = f'<section id="{sid}" style="{SEC}">\n{body}\n<aside>{notes}</aside>\n</section>\n'
    (OUT / f'{sid}.html').write_text(html)
    print(sid, len(html))


# ------------------------------------------------------------------ D1
def pulse(t, t0, amp):
    d = (t - t0) * 1000
    if d < -80 or d > 520:
        return 0
    return amp * (math.exp(-((d - 90) / 48) ** 2) + 0.32 * math.exp(-((d - 250) / 55) ** 2))


def panel(x0, w, kind):
    T = 6.4
    px = lambda t: x0 + 10 + t / T * (w - 20)
    out = []
    if kind == 'pac':
        rr = [800, 805, 795, 800, 480, 1060, 800, 805]
        amp = [1, 1, 1, 1, .55, 1, 1, 1]
    elif kind == 'mot':
        rr = [800, 805, 795, 800, 800, 800, 800, 800]
        amp = [1] * 8
    else:
        rr = [620, 900, 540, 770, 1010, 580, 840, 470, 760]
        amp = [.8, 1, .62, .9, 1, .66, .92, .58, .86]
    t = 0.45
    beats = []
    for r, a in zip(rr, amp):
        t += r / 1000
        if t > T - 0.2:
            break
        beats.append((t, a))
    mot = (2.4, 5.0) if kind == 'mot' else None
    # rows
    ACC_Y, PPG_TOP, PPG_BASE, TK0, TK1, RR0, RR1 = 64, 100, 196, 214, 240, 262, 382
    if mot:
        out.append(f'<rect x="{f(px(mot[0]))}" y="44" width="{f(px(mot[1]) - px(mot[0]))}" height="344" rx="8" fill="#ececec"/>')
    if kind == 'pac':
        b4, b5 = beats[4][0], beats[5][0]
        out.append(f'<rect x="{f(px(b4 - .22))}" y="44" width="{f(px(b5 + .16) - px(b4 - .22))}" height="344" rx="8" fill="#f3e3e3"/>')
    # accelerometer
    d = []
    for i in range(121):
        tt = i / 120 * T
        a = 0.06
        if mot and mot[0] < tt < mot[1]:
            a = 1
        v = a * (math.sin(tt * 23) * .6 + math.sin(tt * 41 + 1) * .4)
        d.append(f'{"M" if i == 0 else "L"}{f(px(tt))},{f(ACC_Y - v * 13)}')
    out.append(f'<path d="{"".join(d)}" fill="none" stroke="{GREY}" stroke-width="2"/>')
    # PPG
    d = []
    for i in range(241):
        tt = i / 240 * T
        v = sum(pulse(tt, b, a) for b, a in beats)
        if mot and mot[0] < tt < mot[1]:
            v = v * .5 + .5 * math.sin(tt * 9.3) + .22 * math.sin(tt * 31 + 2)
        d.append(f'{"M" if i == 0 else "L"}{f(px(tt))},{f(PPG_BASE - v * 78)}')
    col = MID if kind == 'af' else (GREY if kind == 'mot' else INK)
    out.append(f'<path d="{"".join(d)}" fill="none" stroke="{col}" stroke-width="2.5" stroke-linejoin="round"/>')
    if kind == 'pac':
        b, a = beats[4]
        dd = []
        for i in range(31):
            tt = b - .08 + i / 30 * .55
            dd.append(f'{"M" if i == 0 else "L"}{f(px(tt))},{f(PPG_BASE - pulse(tt, b, a) * 78)}')
        out.append(f'<path d="{"".join(dd)}" fill="none" stroke="{ACC}" stroke-width="4"/>')
    # reported beats
    rep = []
    for i, (b, a) in enumerate(beats):
        if kind == 'mot' and i == 3:
            continue  # missed beat
        rep.append((b, i))
        if kind == 'mot' and i == 4:
            rep.append((b + .36, 'spur'))
    rep.sort(key=lambda r: r[0])
    y = lambda v: RR1 - (min(max(v, 300), 1700) - 300) / 1400 * (RR1 - RR0)
    out.append(f'<line x1="{f(x0 + 10)}" x2="{f(x0 + w - 10)}" y1="{f(y(800))}" y2="{f(y(800))}" stroke="{LIGHT}" stroke-width="2"/>')
    for k, (b, tag) in enumerate(rep):
        x = px(b)
        pac = kind == 'pac' and tag == 4
        flagged = (kind == 'pac' and tag == 4) or (kind == 'mot' and mot[0] < b < mot[1])
        out.append(f'<line x1="{f(x)}" x2="{f(x)}" y1="{TK0}" y2="{TK1}" stroke="{ACC if pac else (MID if kind == "af" else INK)}" stroke-width="{4 if pac else 3}"/>')
        if flagged:
            out.append(f'<circle cx="{f(x)}" cy="{TK0 - 9}" r="6" fill="none" stroke="{INK}" stroke-width="2"/>')
        if k == 0:
            continue
        iv = (b - rep[k - 1][0]) * 1000
        if kind == 'pac' and tag == 4:
            out.append(f'<circle cx="{f(x)}" cy="{f(y(iv))}" r="9" fill="{ACC}"/>')
        elif kind == 'pac' and tag == 5:
            out.append(f'<circle cx="{f(x)}" cy="{f(y(iv))}" r="8" fill="#ffffff" stroke="{ACC}" stroke-width="3"/>')
        elif kind == 'mot' and flagged:
            out.append(f'<circle cx="{f(x)}" cy="{f(y(iv))}" r="8" fill="#ffffff" stroke="{GREY}" stroke-width="3"/>')
        else:
            out.append(f'<circle cx="{f(x)}" cy="{f(y(iv))}" r="7" fill="{MID if kind == "af" else INK}"/>')
    lab = {'pac': 'Premature atrial beat', 'mot': 'Motion artefact', 'af': 'Atrial fibrillation'}[kind]
    out.append(f'<text x="{f(x0 + w / 2)}" y="30" font-size="26" font-weight="700" text-anchor="middle" fill="{INK}">{lab}</text>')
    if kind == 'pac':
        out.append(f'<text x="{f(px(beats[4][0]) - 16)}" y="{f(y(480) + 8)}" font-size="22" text-anchor="end" fill="{ACC}">early</text>')
        out.append(f'<text x="{f(px(beats[5][0]) + 4)}" y="{f(y(1060) - 14)}" font-size="22" text-anchor="middle" fill="{ACC}">pause</text>')
    if kind == 'mot':
        mg = [r for r in rep if r[1] == 4][0]
        out.append(f'<text x="{f(px(mg[0]))}" y="{f(y(1600) - 12)}" font-size="22" text-anchor="middle" fill="{MID}">missed beat</text>')
    return out


def d1():
    W, H = 1696, 400
    s = []
    for name, yy in [('Accelerometer', 70), ('Wrist pulse', 152), ('Beats reported', 233), ('Interval', 312), ('(800 ms line)', 340)]:
        s.append(f'<text x="0" y="{yy}" font-size="22" fill="{GREY}">{name}</text>')
    gx, pw, gap = 176, 492, 22
    for i, k in enumerate(['pac', 'mot', 'af']):
        s += panel(gx + i * (pw + gap), pw, k)
    svg = (f'<svg aria-label="Three schematic recordings side by side, each with the accelerometer, the wrist pulse, the beats the watch reports and the interval between beats. '
           f'Premature atrial beat: wrist still; one early, smaller pulse, then a longer pause, and the rhythm resumes. '
           f'Motion artefact: wrist moving; the pulse is distorted, one beat is missed so one interval is about twice normal, and a false peak splits another; these beats are flagged. '
           f'Atrial fibrillation: wrist still; every interval differs and there is no steady pace." width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
           + ''.join(s) + '</svg>')
    col = ('<div style="flex:1;display:flex;flex-direction:column;gap:8px;padding:18px;border:1px solid #8a8a8a">'
           '<h3 style="font-size:26px;font-weight:700">{h}</h3><p style="font-size:24px;line-height:1.3">{p}</p></div>')
    cols = ''.join([
        col.format(h='Counted', p='Wrist still. One early, smaller pulse, then a longer pause. The device may flag it as abnormally short. The model scores it as p̂ᵢ.'),
        col.format(h='Not a PAC', p='Wrist moving. Beats are missed or split and flagged as motion-affected. Flag and motion are inputs; silent loss is corrected by 1/π̂(m); a marked gap leaves observed time.'),
        col.format(h='A different finding', p='Every interval differs, with no steady pace, for minutes or more. In the pilot, AF vs PAC/PVC windows: AUROC 0.968 to 1.000 (Table 4.1).'),
    ])
    body = (f'<h2 style="{H2}">Appendix D1: What Is Counted: a PAC, Motion Artefact or AF</h2>\n{svg}\n'
            f'<div style="display:flex;flex-direction:row;gap:22px;padding-left:176px">{cols}</div>\n'
            f'<p style="{SRC}">Schematic waveforms, not device data. Open circle above a beat: device low-confidence flag. Flag semantics: §3.4 (Garmin, 2023); low-confidence beats at low motion are candidate rhythm events.</p>')
    notes = ('Held for questions, for panel members outside cardiology. Three things make beat intervals irregular and only one is counted. '
             'A PAC is one early, weaker beat followed by a longer pause, with the wrist still. Motion artefact happens while the wrist moves: '
             'the watch misses a beat, giving one long interval with no short one before it, or picks up a false peak; the Garmin flags these, '
             'and the accelerometer tells the model the wrist was moving. AF is irregular throughout, with no interval repeating; it is the '
             'arrhythmia that monitoring after stroke looks for, not an ectopic count. The flag is binary and marks both motion-affected beats '
             'and intervals judged abnormally short or long, so a PAC tends to be flagged too: that is why the flag is an input, not a deletion rule.')
    write('app-d1', body, notes)


# ------------------------------------------------------------------ D2
def d2():
    W, H = 1696, 640
    s = []
    # row 1: unit
    s.append(f'<text x="0" y="30" font-size="28" font-weight="700" fill="{INK}">The unit: one premature atrial beat</text>')
    xs = [20, 110, 200, 290, 350, 470, 560, 650, 740]
    for i, x in enumerate(xs):
        pac = i == 4
        s.append(f'<line x1="{x}" x2="{x}" y1="{56 if pac else 66}" y2="112" stroke="{ACC if pac else GREY}" stroke-width="{5 if pac else 4}"/>')
        if pac:
            s.append(f'<circle cx="{x}" cy="54" r="8" fill="{ACC}"/>')
    s.append(f'<line x1="0" x2="770" y1="112" y2="112" stroke="{LIGHT}" stroke-width="2"/>')
    s.append(f'<text x="350" y="144" font-size="24" text-anchor="middle" fill="{MID}">counts as 1</text>')
    s.append(f'<text x="840" y="80" font-size="24" fill="{MID}">Early, then a pause. Normal beats, AF beats and</text>')
    s.append(f'<text x="840" y="110" font-size="24" fill="{MID}">motion artefacts are not counted.</text>')
    # row 2: window
    s.append(f'<text x="0" y="206" font-size="28" font-weight="700" fill="{INK}">The window: 24 hours, about 100,000 beats (illustrative day: 620 PACs)</text>')
    block = [0.87, 0.63, 1.11, 1.40]
    var = [1.04, .95, 1.02, .98, 1.05, .96]
    w = [block[h // 6] * var[h % 6] for h in range(24)]
    c = [620 * v / sum(w) for v in w]
    L, R, B, T = 60, 1690, 400, 236
    bw = (R - L) / 24
    mx = 50
    for h, v in enumerate(c):
        x = L + h * bw + 3
        hh = v / mx * (B - T)
        s.append(f'<rect x="{f(x)}" y="{f(B - hh)}" width="{f(bw - 6)}" height="{f(hh)}" fill="{ACC}"/>')
    s.append(f'<line x1="{L}" x2="{R}" y1="{B}" y2="{B}" stroke="{GREY}" stroke-width="2"/>')
    for h in [0, 6, 12, 18, 24]:
        s.append(f'<text x="{f(L + h * bw)}" y="{B + 28}" font-size="22" text-anchor="middle" fill="{GREY}">{h:02d}:00</text>')
    s.append(f'<text x="{L - 8}" y="{T + 8}" font-size="22" text-anchor="end" fill="{GREY}">{mx}</text>')
    s.append(f'<text x="{L - 8}" y="{B}" font-size="22" text-anchor="end" fill="{GREY}">0</text>')
    s.append(f'<text x="{L + 6}" y="{T - 4}" font-size="22" fill="{GREY}">PACs per hour</text>')
    # usable strip (illustrative night-weighted coverage)
    cov = [.95, .95, .92, .92, .9, .85, .6, .55, .5, .45, .45, .45, .3, .25, .2, .25, .25, .3, .3, .3, .3, .35, .5, .8]
    for h, fv in enumerate(cov):
        g = int(235 - 190 * fv)
        s.append(f'<rect x="{f(L + h * bw)}" y="{B + 40}" width="{f(bw)}" height="16" fill="rgb({g},{g},{g})"/>')
    s.append(f'<text x="{L - 8}" y="{B + 54}" font-size="22" text-anchor="end" fill="{GREY}">usable</text>')
    # row 3: threshold
    s.append(f'<text x="0" y="520" font-size="28" font-weight="700" fill="{INK}">The threshold: ESVEA</text>')
    X0, X1, MAX, ly = 60, 1690, 1500, 588
    xx = lambda v: X0 + v / MAX * (X1 - X0)
    s.append(f'<rect x="{f(xx(480))}" y="{ly - 12}" width="{f(X1 - xx(480))}" height="24" fill="#f3e3e3"/>')
    s.append(f'<line x1="{X0}" x2="{X1}" y1="{ly}" y2="{ly}" stroke="{GREY}" stroke-width="2"/>')
    for v in [0, 250, 500, 750, 1000, 1250, 1500]:
        s.append(f'<line x1="{f(xx(v))}" x2="{f(xx(v))}" y1="{ly - 6}" y2="{ly + 6}" stroke="{GREY}" stroke-width="2"/>')
        s.append(f'<text x="{f(xx(v))}" y="{ly + 34}" font-size="22" text-anchor="middle" fill="{GREY}">{v}</text>')
    s.append(f'<line x1="{f(xx(480))}" x2="{f(xx(480))}" y1="{ly - 26}" y2="{ly + 16}" stroke="{ACC}" stroke-width="5"/>')
    s.append(f'<text x="{f(xx(480))}" y="{ly - 34}" font-size="24" font-weight="700" text-anchor="middle" fill="{ACC}">480</text>')
    s.append(f'<text x="{f(xx(1100))}" y="{ly - 22}" font-size="24" text-anchor="middle" fill="{ACC}">480 or more per 24 h: ESVEA</text>')
    s.append(f'<path d="M{f(xx(620))},{ly - 4} l-11,-20 h22 z" fill="{INK}"/>')
    s.append(f'<text x="{f(xx(620))}" y="{ly - 30}" font-size="22" text-anchor="middle" fill="{INK}">620</text>')
    svg = (f'<svg aria-label="Three rows. The unit: one premature atrial beat in a row of normal beats counts as one. The window: PACs per hour across an illustrative day of 620 PACs, higher in the afternoon and evening, with a strip showing that the watch is usable mostly at night. '
           f'The threshold: a scale from 0 to 1500 PACs per 24 hours with ESVEA at 480 or more; the illustrative day at 620 is ESVEA." width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
           + ''.join(s) + '</svg>')
    body = (f'<h2 style="{H2}">Appendix D2: From One Beat to an ESVEA Call</h2>\n{svg}\n'
            f'<p style="{P}">Primary ESVEA: 480 or more supraventricular beats per day (Haeusler et al., 2025); secondary: 30 or more per hour (Binici et al., 2010), equal to 720 per day; runs reported separately. Scaling analysable hours to a day is biased low, most on active days and in high-burden patients (§2.5), so Equation 3.2 divides each 6-hour block by its own observed hours.</p>\n'
            f'<p style="{SRC}">Hourly shape from the block ratios of Larsen et al. (2016): 0.87, 0.63, 1.11, 1.40. The usable strip is illustrative of night-weighted analysable time (Merschel &amp; Reinhardt, 2022).</p>')
    notes = ('Held for questions. Three steps from one beat to a decision. The unit is one premature atrial beat: early, then a pause. '
             'The window is 24 hours, about 100,000 beats; PACs are not spread evenly, they are lowest around 6 a.m. and highest in the afternoon and evening. '
             'The threshold is 480 or more supraventricular beats per day, the MonDAFIS criterion; 30 per hour, Binici, is secondary and equals 720 per day. '
             'The strip under the bars is the point of the whole estimator: the watch is usable mostly at night, when PACs are fewest, so multiplying what it sees up to 24 hours under-counts. '
             'That is why each 6-hour block is divided by its own observed hours. The hourly shape and the strip are illustrative, not study data.')
    write('app-d2', body, notes)


# ------------------------------------------------------------------ D3
def d3():
    rows = [
        ('H1', 'ectopy burden differs between patients (PACs per hour from ECG labels)',
         'the share of PAC intervals that survive the filter differs (each interval kept or removed)',
         'Mixed-effects logistic regression in new Icentia11k patients (P1)'),
        ('H2', 'the daily count comes from the two-scale ST-GNN with the flag as input, not the best non-graph baseline',
         'its mean absolute error against the ECG-derived daily-equivalent count is lower',
         'Paired subject-level bootstrap 95% CI; primary contrast'),
        ('H3', 'post-stroke survivors wear the Garmin under the 7-day protocol',
         'at least 75% give three or more valid days',
         'One-sided test against 50%, α 0.05, 90% power (about 34 analysed)'),
    ]
    tr = ''.join(f'<tr><td><b>{h}</b></td><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for h, a, b, c in rows)
    body = (f'<h2 style="{H2}">Appendix D3: Hypotheses as If–Then Statements</h2>\n'
            f'<table style="{TBL}">\n<tr><th style="width:6%;text-align:left"></th><th style="width:33%;text-align:left">If (what varies)</th><th style="width:33%;text-align:left">then (what will happen)</th><th style="width:28%;text-align:left">Test</th></tr>\n{tr}\n</table>\n'
            f'<div style="display:flex;flex-direction:row;gap:22px">'
            f'<div style="flex:1;display:flex;flex-direction:column;gap:8px;padding:18px;border:1px solid #8a8a8a"><h3 style="font-size:26px;font-weight:700">Direction of H1</h3><p style="{P}">H1 states a relationship without a direction. The preliminary data show one: at 20%, 78.5% of PAC intervals removed in ESVEA-negative patients against 60.0% in ESVEA-positive (§4.2).</p></div>'
            f'<div style="flex:1;display:flex;flex-direction:column;gap:8px;padding:18px;border:1px solid #8a8a8a"><h3 style="font-size:26px;font-weight:700">Why RQ4 has none</h3><p style="{P}">RQ4 asks how much classification changes and how far selections agree, not whether a predicted relation holds. Fewer than five AF events are expected in the cohort, so it is descriptive: reclassification, κ, sensitivity, specificity; κ and Jaccard against scores.</p></div>'
            f'</div>\n'
            f'<p style="{SRC}">Hypotheses as worded in §1.3; the If–Then form restates them and adds no claim.</p>')
    notes = ('Held for questions. If asked to state the hypotheses as predictions: each one names what varies and what will happen, and both sides are measured. '
             'H1: if burden differs, the share of PAC intervals surviving the filter differs; tested by mixed-effects logistic regression in patients not used in the preliminary analysis. '
             'H2: if the count comes from the flag-aware two-scale model rather than the best non-graph baseline, its error is lower; the single primary contrast. '
             'H3: if survivors wear the watch for 7 days, at least 75% give three valid days; a feasibility level against 50%, not a relation between two measured variables. '
             'RQ4 has no hypothesis because it asks how much, not whether, and too few AF events are expected to power one.')
    write('app-d3', body, notes)


# ------------------------------------------------------------------ D4
def d4():
    rows = [
        ('Icentia11k', 'Which beat is a PAC: ECG beat labels for about 11,000 patients', 'A wrist signal; clock time (untimed segments, so a patient-level rate × 24)', 'RO1 (P0, P1); RO2 training (P2); RO4a test (P3)'),
        ('Pulsewatch', 'How often a real beat reaches the watch at each motion level, π̂(m); waveform vs intervals', 'Garmin behaviour (transfer assumed); PACs alone (merged with PVCs)', 'RO1 morphology loss; RO2 frozen retention'),
        ('Garmin specification', 'Device rules: doubtful beats flagged, not deleted; gaps marked', 'Accuracy of any reading', 'RO2 inputs and gap handling; simulated training flags'),
        ('RO3 cohort (PPUM)', 'Real wear and coverage after stroke on the target device', 'Accuracy of any estimate (no concurrent ECG)', 'RO3 outcomes; RO4a coverage; RO4b selections'),
    ]
    tr = ''.join(f'<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in rows)
    steps = [('1', 'RO1 measures the loss', 'and decides that flagged beats stay as input'),
             ('2', 'RO2 builds and freezes', 'model, π̂(m) and gate at M4'),
             ('3', 'Only then P3 opens', 'for RO4a, so the test is not tuned'),
             ('4', 'RO3 runs in parallel', 'RO1, RO2 and RO4a do not wait for it')]
    st = ''.join(f'<div style="flex:1;display:flex;flex-direction:column;gap:6px;padding:16px;border:1px solid #8a8a8a"><p style="font-size:26px;font-weight:700;color:{ACC}">{n}</p><p style="font-size:24px;font-weight:700;line-height:1.2">{a}</p><p style="{P}">{b}</p></div>' for n, a, b in steps)
    body = (f'<h2 style="{H2}">Appendix D4: What Each Source Brings, and Why the Order Is Fixed</h2>\n'
            f'<table style="{TBL}">\n<tr><th style="width:17%;text-align:left">Source</th><th style="width:31%;text-align:left">Brings</th><th style="width:28%;text-align:left">Cannot show</th><th style="width:24%;text-align:left">Goes to</th></tr>\n{tr}\n</table>\n'
            f'<div style="display:flex;flex-direction:row;gap:18px">{st}</div>\n'
            f'<p style="{SRC}">Patient sets P0 to P3 are disjoint (Table B.3). Fallback (§3.9): without the cohort by semester 4, coverage is modelled from Pulsewatch wear and RO4b is deferred.</p>')
    notes = ('Held for questions. No single dataset has everything. Icentia11k has the answer key, which beat is a PAC, but no wrist signal and no clock. '
             'Pulsewatch links the wrist to the heart: it shows how often a real heartbeat reaches the watch at each motion level, but it is a Samsung watch and its labels merge PACs with PVCs. '
             'The Garmin specification fixes what a flag and a gap mean. The cohort has the right watch and the right patients but no ECG, so it shows delivery, not accuracy. '
             'The order follows: RO1 decides the design, RO2 is frozen at M4, only then is the held-out set P3 opened for RO4a, and RO3 runs alongside so the core does not wait for ethics or the device.')
    write('app-d4', body, notes)


# ------------------------------------------------------------------ D5
def d5():
    W, H = 1000, 560
    bins = ['<0.05', '0.05–0.2', '0.2–0.5', '0.5–1', '≥1']
    beats = ['55,684', '15,812', '5,342', '6,074', '4,468']
    match = [.849, .725, .516, .477, .407]
    ctrl = [.207, .224, .202, .204, .210]
    kept = [.766, .600, .335, .292, .220]
    kctl = [.076, .078, .055, .056, .054]
    L, R, T, B = 90, 760, 30, 460
    x = lambda i: L + i * (R - L) / 4
    y = lambda v: B - v * (B - T)
    s = []
    for v in [0, .25, .5, .75, 1]:
        s.append(f'<line x1="{L}" x2="{R}" y1="{f(y(v))}" y2="{f(y(v))}" stroke="#e4e4e4" stroke-width="2"/>')
        s.append(f'<text x="{L - 10}" y="{f(y(v) + 8)}" font-size="22" text-anchor="end" fill="{GREY}">{v:g}</text>')
    for i, b in enumerate(bins):
        s.append(f'<text x="{f(x(i))}" y="{B + 32}" font-size="22" text-anchor="middle" fill="{GREY}">{b}</text>')
    s.append(f'<text x="{f((L + R) / 2)}" y="{B + 66}" font-size="22" text-anchor="middle" fill="{GREY}">accelerometer motion (m/s²)</text>')
    s.append(f'<text transform="translate(24,{f((T + B) / 2)}) rotate(-90)" font-size="22" text-anchor="middle" fill="{GREY}">share matched or kept</text>')

    def line(vals, col, dash, lab, ly):
        pts = ' '.join(f'{f(x(i))},{f(y(v))}' for i, v in enumerate(vals))
        da = 'stroke-dasharray="10 8"' if dash else ''
        s.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="4" {da}/>')
        for i, v in enumerate(vals):
            s.append(f'<circle cx="{f(x(i))}" cy="{f(y(v))}" r="7" fill="{col if not dash else "#ffffff"}" stroke="{col}" stroke-width="3"/>')
        s.append(f'<text x="{R + 18}" y="{f(ly)}" font-size="22" fill="{INK}">{lab}</text>')
    line(match, INK, False, 'Beat match', y(match[-1]) + 8)
    line(kept, ACC, False, 'Intervals kept', y(kept[-1]) - 12)
    line(ctrl, INK, True, 'Beat control', y(ctrl[-1]) + 26)
    line(kctl, ACC, True, 'Interval control', y(kctl[-1]) + 8)
    s.append(f'<text x="{f(x(0) + 12)}" y="{f(y(match[0]) - 16)}" font-size="22" fill="{INK}">0.849</text>')
    s.append(f'<text x="{f(x(4) - 10)}" y="{f(y(match[4]) - 16)}" font-size="22" text-anchor="end" fill="{INK}">0.407</text>')
    svg = (f'<svg aria-label="Line chart across five motion bins from below 0.05 to 1 or more metres per second squared. Beat match falls from 0.849 to 0.407 while its chance control stays near 0.21. Intervals kept fall from 0.766 to 0.220 while their chance control stays near 0.06." width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
           + ''.join(s) + '</svg>')
    crit = [('1. Above chance at high motion', 'Met: excess +0.273 at 0.5–1, +0.197 at ≥1'),
            ('2. Consistent within subjects', 'Met: lower at the highest motion in 8 of 8'),
            ('3. Detectors comparable', 'Not met: 0.850 vs 0.752 on 58,121 beats')]
    tr = ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in crit)
    right = (f'<div style="flex:1;display:flex;flex-direction:column;gap:16px">'
             f'<table style="{TBL}"><tr><th style="width:52%;text-align:left">Criterion (locked before the run)</th><th style="width:48%;text-align:left">Result</th></tr>{tr}</table>'
             f'<p style="{P}"><b style="color:{ACC}">Not passed.</b> The motion effect is measurable; its absolute level depends on the peak detector. No retention value is claimed.</p>'
             f'<p style="{P}">The motion term stays, estimated on Pulsewatch in RO2 with a detector sensitivity analysis: Elgendi et al. (2013) on all segments as primary, the authors&#39; peaks as the alternative (§3.4).</p></div>')
    body = (f'<h2 style="{H2}">Appendix D5: Pulsewatch Beat-Retention Pre-check</h2>\n'
            f'<p style="{P}">8 subjects; beats matched to lag-shifted ECG R-peaks, by motion bin; sessions passing the quality gate. Each measure has its own chance control (dashed).</p>\n'
            f'<div style="display:flex;flex-direction:row;gap:32px;align-items:start">{svg}{right}</div>\n'
            f'<p style="{SRC}">Not a random sample and not an estimate of π̂(m). Beats per bin: {", ".join(beats)}. Run 2 November 2026; values from the pre-check record; the proposal reports the summary (§3.4).</p>')
    notes = ('Held for questions. Say the outcome first: the check did not pass under the rule locked before the run. Two criteria were met: beat matching stays well above its chance control even at high motion, '
             'and it falls with motion in every subject. The third failed: two peak detectors gave different absolute retention, 0.850 against 0.752, so the level depends on the detector. '
             'This test cannot say which detector is right. So no retention value is claimed; the motion term stays and is estimated in RO2 with a detector sensitivity analysis. '
             'The 8 subjects were chosen for the check, so this is not an estimate of the curve. The current lag method reached only 2.5% of excluded and 0.8% of no-label segments, so a label-free lag method is an RO2 task.')
    write('app-d5', body, notes)


d1(); d2(); d3(); d4(); d5()
