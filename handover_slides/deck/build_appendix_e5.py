"""Build Appendix E5: the readiness track from now to the first PPUM participant, drawn beside the
modelling track, with the points where they meet and the S4 go/no-go gate. Deck style as Appendix E."""
from build_appendix_e import OUT, INK, MID, GREY, LIGHT, ACC, H2, SRC, esc, text, lines, write  # noqa: F401

W, H = 1696, 480
L, C2, C3, G = 300, 300, 820, 1330   # label column; S2 start; S3 start; gate (start of S4)
s = []
for x0, x1, t, fill in [(C2, C3, 'S2 (now)', '#f0f0f0'), (C3, G, 'S3', '#ffffff'), (G, W, 'S4', '#f0f0f0')]:
    s.append(f'<rect x="{x0}" y="0" width="{x1 - x0}" height="40" fill="{fill}" stroke="{LIGHT}"/>')
    s.append(text((x0 + x1) / 2, 28, t, 22, INK, 'middle', '700'))

# track 1: modelling (one row of chained steps)
s.append(text(0, 84, 'Track 1: modelling', 22, INK, 'start', '700'))
s.append(text(0, 108, 'Icentia11k, Pulsewatch', 20, GREY))
for x0, x1, t in [(C2 + 4, 560, 'Pipeline; §4.2 reproduced'), (566, 940, 'RO1, H1 on P1; π̂(m)'), (946, G - 6, 'Simulator; RO2 build')]:
    s.append(f'<rect x="{x0}" y="62" width="{x1 - x0}" height="44" fill="{MID}"/>')
    s.append(text((x0 + x1) / 2, 91, t, 20, '#ffffff', 'middle', '700'))

# track 2: readiness rows
s.append(text(0, 172, 'Track 2: readiness', 22, INK, 'start', '700'))
s.append(text(0, 196, 'Garmin, ethics, PPUM', 20, GREY))
rows = [('R1 Device and data access', C2 + 4, 640, 'Watches; SDK; 24-h logging in writing'),
        ('R2 Device verification', 560, 1010, 'Export, flag, gaps, 24 h, battery, motion'),
        ('R3 Garmin data pipeline', 900, G - 6, 'Export to beat table, coverage'),
        ('R4 Protocol and ethics', 600, 1250, 'Protocol, consent, CRF; MREC after M1'),
        ('R5 PPUM site readiness', 1010, G - 6, 'Pathway, devices, run')]
for i, (lab, x0, x1, t) in enumerate(rows):
    y = 222 + i * 50
    s.append(text(0, y + 28, lab, 20, INK))
    s.append(f'<rect x="{x0}" y="{y + 6}" width="{x1 - x0}" height="34" fill="{INK}"/>')
    s.append(text(x0 + 12, y + 30, t, 19, '#ffffff'))
# milestones on R2 and R4
for x, y, t in [(1010, 222 + 50, 'M1'), (1250, 222 + 150, 'M2')]:
    s.append(f'<path d="M{x},{y + 4} l-14,19 l14,19 l14,-19 z" fill="{ACC}"/>')
    s.append(text(x, y + 30, t, 15, '#ffffff', 'middle', '700'))

# meeting points: numbered red circles on connectors between the tracks
for n, x, y2 in [(3, 720, 272), (1, 1060, 322), (2, 1200, 322)]:
    s.append(f'<line x1="{x}" x2="{x}" y1="106" y2="{y2 + 6}" stroke="{ACC}" stroke-width="3" stroke-dasharray="6 5"/>')
    s.append(f'<circle cx="{x}" cy="140" r="17" fill="#ffffff" stroke="{ACC}" stroke-width="3"/>')
    s.append(text(x, 148, str(n), 20, ACC, 'middle', '700'))

# go/no-go gate at the start of S4
s.append(f'<line x1="{G}" x2="{G}" y1="44" y2="{H}" stroke="{ACC}" stroke-width="3" stroke-dasharray="8 6"/>')
s.append(f'<path d="M{G},150 l-22,26 l22,26 l22,-26 z" fill="{ACC}"/>')
s.append(text(G + 34, 170, 'Go/no-go', 22, ACC, 'start', '700'))
s.append(f'<rect x="{G + 24}" y="210" width="{W - G - 26}" height="110" fill="#ffffff" stroke="{INK}" stroke-width="2"/>')
s.append(lines(G + 40, 240, ['Go: first participant', 'fitted; 7-day wear;', 'RO3 monitoring starts'], 20, INK, 27))
s.append(f'<rect x="{G + 24}" y="336" width="{W - G - 26}" height="138" fill="#ffffff" stroke="{ACC}" stroke-width="2"/>')
s.append(lines(G + 40, 366, ['No-go: RO3 becomes', 'device verification', '(coverage from', 'Pulsewatch); RO4b deferred'], 20, ACC, 27))

svg = (f'<svg aria-label="Two tracks from semester 2 to the start of semester 4. Track 1, modelling: data pipeline reproducing section 4.2, then RO1 and H1 with the motion retention curve, then the simulator and RO2 build. '
       'Track 2, readiness: R1 device and data access in S2; R2 device verification from S2 into S3, ending in M1; R3 Garmin data pipeline in S3; R4 protocol and ethics from S2 to S3, submitted after M1 and ending in M2; R5 site readiness in S3. '
       'Three meeting points link the tracks: 1 shared coverage and valid-day code, 2 a dry run on real Garmin output, 3 the motion scale for the retention curve. '
       'At the start of S4 a go/no-go gate: go means the first participant is fitted for 7-day wear; no-go means RO3 becomes a device-verification study with coverage modelled from Pulsewatch and RO4b is deferred." '
       f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + ''.join(s) + '</svg>')

meet = [('1', 'Coverage and valid-day code', 'Coverage gate in the estimator (Eq. 3.3)', 'Valid-day rule and θ_block in the protocol', 'One implementation, so the two cannot drift; the P0 pipeline (§4.2) is its base'),
        ('2', 'Dry run on real Garmin output', 'Interim RO2 model and estimator', 'Verification wear through the R3 pipeline', 'Pilot (slide 17): thresholds do not transfer across devices, so test the real export early'),
        ('3', 'Motion scale for π̂(m)', 'π̂(m) fitted on Pulsewatch motion', 'Garmin accelerometer units and rate (R2)', 'Pre-check (D5): motion effect measurable; without a scale map, π̂(m) cannot be applied')]
tr = ''.join(f'<tr><td><b style="color:{ACC}">{a}</b> <b>{b}</b></td><td>{c}</td><td>{d}</td><td>{e}</td></tr>' for a, b, c, d, e in meet)
table = ('<table style="width:100%;font-size:21px;color:#1a1a1a;border:1px solid #8a8a8a">'
         '<tr><th style="width:21%;text-align:left">Where the tracks meet</th><th style="width:23%;text-align:left">Modelling brings</th>'
         '<th style="width:23%;text-align:left">Readiness brings</th><th style="width:33%;text-align:left">Why, from completed work</th></tr>'
         f'{tr}</table>')

body = (f'<h2 style="{H2}">Appendix E5: Readiness Track, From Now to the First Participant</h2>\n{svg}\n{table}\n'
        f'<p style="{SRC}">From §3.5, §3.8, §3.9, Tables 6.1 and 6.2. Task detail: implementation plan, sections 10 to 12.</p>')
notes = ('Held for questions, for example: what happens before the first patient wears a watch? Two tracks run in parallel until the start of S4. '
         'The readiness track starts with the device itself: we do not have it yet, so R1 is obtaining the watches, Garmin Health SDK access, and Garmin’s 24-hour logging confirmation in writing, since the proposal currently cites a personal communication. '
         'R2 is the device verification §3.5 requires before ethics: export, flag and gap encoding, 24-hour logging, 7-day battery, and one item added here, the accelerometer scale, because π̂(m) is fitted on Samsung motion and has to be mapped to Garmin units. Verification ends at M1 and fixes the thresholds the protocol states. '
         'R3 builds the Garmin pipeline on that verification data, so it is proven before any participant. R4 is the protocol, consent, case report form and the MREC submission after M1, ending at M2 with registration. R5 is site readiness at PPUM. '
         'The tracks meet three times: shared coverage code, a dry run of the estimator on real Garmin output, and the motion scale. '
         'At the start of S4: go, and recruitment starts; no-go, and §3.9 applies: RO3 becomes device verification with coverage modelled from Pulsewatch, RO4a is unchanged and RO4b is deferred. RO1, RO2 and RO4a never wait for the cohort.')
write('app-e5', body, notes)
