"""Build main-talk slide 19 'prelim-next': what the preliminary work decided and what comes next."""
from pathlib import Path

OUT = Path(__file__).resolve().parent / 'project' / 'slides'
INK, MID, GREY, LIGHT, ACC = '#1a1a1a', '#4a4a4a', '#6b6b6b', '#d4d4d4', '#9b1c1c'
SEC = ('background:#ffffff;color:#1a1a1a;font-family:Arial, Helvetica, sans-serif;'
       'padding:88px 112px 140px;display:flex;flex-direction:column;gap:22px')

rows = [
    ('Filtering loss, 298 Icentia11k patients (slide 18)',
     'Flagged beats stay as model input; the loss rates calibrate the training simulator',
     'H1 tested on new patients (P1); RO1 in full, S2 to S3'),
    ('Cross-device pilot, 33 held-out subjects (slide 17)',
     'Interval graphs carry rhythm information, but a fixed threshold does not transfer: scores are calibrated, and substitution is tested under device losses',
     'RO2 on the Icentia11k development set (P2), S3 to S4'),
    ('Pulsewatch retention pre-check, 8 subjects',
     '<b>Not passed:</b> the motion effect is measurable, but its level depends on the peak detector; no retention value is claimed',
     'π̂(m) estimated in RO2 with a detector sensitivity analysis, before M4'),
    ('Icentia11k clock-time check',
     'Segments are untimed: training uses pseudo-days, and the reference is a patient-level rate × 24',
     'Built into RO2 training'),
]
tr = ''.join(f'<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>' for a, b, c in rows)
table = ('<table style="width:100%;font-size:24px;color:#1a1a1a;border:1px solid #8a8a8a">'
         '<tr><th style="width:27%;text-align:left">Completed</th><th style="width:43%;text-align:left">What it decided in the design</th><th style="width:30%;text-align:left">Next step</th></tr>'
         f'{tr}</table>')

# gate strip
W, H = 1696, 210
sems = ['S2 (now)', 'S3', 'S4', 'S5', 'S6', 'S7']
L, R = 0, W
cw = (R - L) / 6
s = []
SY = 100  # semester row top
for i, t in enumerate(sems):
    s.append(f'<rect x="{L + i * cw:.1f}" y="{SY}" width="{cw:.1f}" height="40" fill="{"#f0f0f0" if i % 2 == 0 else "#ffffff"}" stroke="{LIGHT}" stroke-width="1"/>')
    s.append(f'<text x="{L + i * cw + cw / 2:.1f}" y="{SY + 28}" font-size="22" font-weight="700" text-anchor="middle" fill="{INK}">{t}</text>')
s.append(f'<rect x="{L + 3 * cw + 4:.1f}" y="{SY + 48}" width="{2 * cw - 8:.1f}" height="16" fill="{MID}"/>')
s.append(f'<text x="{L + 4 * cw:.1f}" y="{SY + 96}" font-size="22" text-anchor="middle" fill="{MID}">RO4a on the held-out set P3</text>')
gates = [(1.0, 'Pipeline reproduces Tables 4.2, 4.3', 22),
         (2.0, 'M3: RO1 paper', 64),
         (3.0, 'M4: model frozen; P3 opens', 22)]
for xi, t, ty in gates:
    x = L + xi * cw
    s.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{ty + 12}" y2="{SY + 44}" stroke="{ACC}" stroke-width="3" stroke-dasharray="6 5"/>')
    s.append(f'<path d="M{x:.1f},{ty - 12} l-11,12 l11,12 l11,-12 z" fill="{ACC}"/>')
    s.append(f'<text x="{x + 18:.1f}" y="{ty + 8}" font-size="22" font-weight="700" fill="{ACC}">{t}</text>')
svg = (f'<svg aria-label="Semesters S2 to S7 with three gates: by the end of S2 the full pipeline reproduces Tables 4.2 and 4.3; in S3, M3, the RO1 paper; in S4, M4, the model is frozen and only then does the held-out set P3 open; RO4a runs on P3 in S5 and S6." width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + ''.join(s) + '</svg>')

notes = ('About 1 minute. This slide connects the preliminary work to the study. Each row is something already done, what it fixed in the design, and where it is tested next. '
         'The filtering result is why flagged beats stay as input, but it formed H1, so H1 is tested on patients not used before. '
         'The pilot shows interval graphs carry rhythm information, and that a threshold set on one device does not hold on another, which is why probabilities are calibrated and substitution is tested under device losses rather than assumed. '
         'Say the pre-check plainly: it did not pass its locked rule; the motion effect is real, but its level depended on the peak detector, so no retention value is claimed and RO2 estimates it with a detector sensitivity analysis. '
         'The clock-time check is why training uses pseudo-days. Then the gates: the full pipeline must first reproduce Tables 4.2 and 4.3; the model is frozen at M4 before the held-out patients are opened. '
         'Detail for questions: Appendix E1 to E5 (plan and readiness), D5 (pre-check).')

body = (f'<h2 style="font-size:52px;font-weight:700;line-height:1.15">Preliminary Findings (3): From Results to the Full Study</h2>\n'
        f'{table}\n{svg}\n'
        f'<p style="position:absolute;right:112px;bottom:56px;width:200px;text-align:right;font-size:24px;color:#6b6b6b">19</p>')
html = f'<section id="prelim-next" style="{SEC}">\n{body}\n<aside>{notes}</aside>\n</section>\n'
(OUT / 'prelim-next.html').write_text(html)
print(len(html))
