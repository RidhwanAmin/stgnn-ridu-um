"""Generate the HyperFrames project for the ESVEA research walkthrough.

Scenes are declared as data below; anchors are script words, timed by the
aligned narration (build/align.py). Run: python3 build/gen.py
"""
import json, re, subprocess, html
from pathlib import Path
from PIL import Image
from align import load, norm

ROOT = Path(__file__).resolve().parent.parent
NARR = json.loads((ROOT.parent / "narration.json").read_text())
TEXT = {d["id"][:2]: d["text"] for d in NARR}

W, H = 1920, 1080
STAGE = dict(x=120, y=262, w=1680, h=622)   # figure area; captions live below 930
LEAD = 0.45      # audio starts this far into each scene slot
TAIL = 0.85      # hold after the last word

def dur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True).stdout.strip()
    return float(out)

def esc(s):
    return html.escape(s, quote=True)

# ---------------------------------------------------------------- scene data
# event kinds: zoom(cx,cy,s) | reset | hl(rect=[x,y,w,h] in % of image) | pill(text, x, y in % of stage) | swap(i)
# 'at' is a script word (optionally "word#n" for the n-th occurrence), or a number of seconds.
S = [
 dict(n="01", chap="ESVEA after stroke", title="Counting atrial ectopy on a smartwatch", kind="intro"),
 dict(n="02", chap="Overview", title="Four questions, four objectives", imgs=["questions"], ev=[
   dict(at="First,", k="hl", rect=[0, 11.5, 100, 22.5]),
   dict(at="Second,", k="hl", rect=[0, 34.5, 100, 22.5]),
   dict(at="Third,", k="hl", rect=[0, 57.5, 100, 18]),
   dict(at="fourth,", k="hl", rect=[0, 76, 100, 22]),
   dict(at="primary", k="pill", text="ESVEA: ≥ 480 supraventricular beats per day", x=50, y=92),
 ]),
 dict(n="03", chap="Methodology", title="A chain of dependencies", imgs=["flow"], ev=[
   dict(at="Icentia11k,", k="hl", rect=[1, 9, 26, 15]), dict(at="Icentia11k,", k="zoom", cx=20, cy=25, s=1.6),
   dict(at="Pulsewatch,", k="hl", rect=[1, 31, 26, 15]), dict(at="Pulsewatch,", k="zoom", cx=20, cy=42, s=1.6),
   dict(at="Garmin", k="hl", rect=[1, 50, 26, 15]), dict(at="Garmin", k="zoom", cx=20, cy=58, s=1.6),
   dict(at="Objective", k="hl", rect=[38, 8, 26, 42]), dict(at="Objective", k="zoom", cx=50, cy=30, s=1.4),
   dict(at="frozen", k="hl", rect=[74, 31, 25, 17]), dict(at="frozen", k="zoom", cx=80, cy=40, s=1.5),
   dict(at="stroke", k="hl", rect=[1, 73, 63, 17]), dict(at="stroke", k="zoom", cx=35, cy=80, s=1.3),
   dict(at="If", k="reset"),
   dict(at="If", k="pill", text="Fallback: RO1, RO2 and RO4a do not need the cohort", x=50, y=93),
 ]),
 dict(n="04", chap="RO1 · Information loss", title="The filter that hides premature beats", imgs=["filter20", "filter10", "filter30"], ev=[
   dict(at="rejects", k="pill", text="reject if |RR − median of 5 accepted| > threshold", x=50, y=8),
   dict(at="premature", k="zoom", cx=30, cy=45, s=1.7),
   dict(at="In", k="reset"),
   dict(at="band", k="swap", i=1),
   dict(at="band", k="pill", text="threshold 10%", x=84, y=8),
   dict(at="crosses", k="swap", i=2),
   dict(at="crosses", k="pill", text="threshold 30%", x=84, y=8),
 ]),
 dict(n="05", chap="RO1 · Preliminary result", title="Filtering removes PACs, not normal beats", imgs=["rchart", "burden"], ev=[
   dict(at="twenty", k="hl", rect=[37, 6, 10, 84]),
   dict(at="sixty-one", k="pill", text="PAC coupling 60.9% removed", x=76, y=12),
   dict(at="nine", k="pill", text="normal intervals 8.8% removed", x=76, y=88),
   dict(at="burden:", k="swap", i=1),
   dict(at="smaller", k="pill", text="at 20%: ESVEA− 78.5% vs ESVEA+ 60.0% of PAC intervals", x=50, y=8),
   dict(at="Hypothesis", k="pill", text="H1: tested at patient level in new patients (set P1)", x=50, y=92),
 ]),
 dict(n="06", chap="RO2 · Architecture", title="Two scales: beats, then the day", imgs=["scale"], ev=[
   dict(at="beat", k="zoom", cx=50, cy=13, s=1.2),
   dict(at="attention", k="zoom", cx=50, cy=38, s=1.2),
   dict(at="epoch", k="zoom", cx=50, cy=64, s=1.2),
   dict(at="Because", k="zoom", cx=50, cy=89, s=1.2),
   dict(at="segments.", k="reset"),
 ]),
 dict(n="07", chap="RO2 · Beat graph", title="Two graphs inside every window", imgs=["graph", "graph_sel", "heatmaps"], ev=[
   dict(at="temporal", k="swap", i=1),
   dict(at="temporal", k="hl", rect=[0, 66, 100, 22]),
   dict(at="temporal", k="pill", text="Â_adj: banded temporal chain (below)", x=24, y=94),
   dict(at="similarity", k="hl", rect=[0, 2, 100, 50]),
   dict(at="similarity", k="pill", text="Â_sim: k nearest neighbours in feature space (above)", x=70, y=6),
   dict(at="Both", k="swap", i=2),
   dict(at="Both", k="pill", text="built once per window, reused in all L layers", x=50, y=94),
 ]),
 dict(n="08", chap="RO2 · Local block", title="One local layer, three branches", imgs=["step", "step_b"], ev=[
   dict(at="chain", k="hl", rect=[0, 0, 17, 100]),
   dict(at="own", k="hl", rect=[17, 0, 17, 100]),
   dict(at="similarity", k="hl", rect=[34, 0, 17, 100]),
   dict(at="normalised", k="hl", rect=[51, 0, 49, 100]),
   dict(at="because", k="swap", i=1),
   dict(at="because", k="pill", text="α = 0.3, β = 1.5: the similarity branch dominates", x=50, y=8),
   dict(at="Every", k="pill", text="RQ2.3: remove each component in turn", x=50, y=92),
 ]),
 dict(n="09", chap="RO2 · Observation model", title="Every loss goes to one place", imgs=["loss"], ev=[
   dict(at="Deleting", k="hl", rect=[21, 10, 18, 72]),
   dict(at="gaps", k="hl", rect=[57, 10, 20, 72]),
   dict(at="silently", k="hl", rect=[38, 10, 20, 72]),
   dict(at="silently", k="pill", text="weight 1 / π̂(m)", x=48, y=8),
   dict(at="wrist", k="hl", rect=[77, 10, 22, 72]),
   dict(at="wrist", k="pill", text="pulse deficit: measured in RO4a, not corrected", x=70, y=92),
 ]),
 dict(n="10", chap="Equations 3.1 and 3.2", title="From beat probabilities to a daily rate", kind="eqs", imgs=["eq1", "eq2", "eq3", "eq4"], ev=[
   dict(at="Equation", k="show", i=0),
   dict(at="Equation#2", k="show", i=1),
   dict(at="one", k="pill", text="each reported beat weighted by 1 / π̂(mᵢ)", x=50, y=50),
   dict(at="six-hour", k="pill", text="each 6-hour block divided by its own observed hours τ", x=50, y=62),
   dict(at="combined", k="pill", text="blocks combined by length: Lₕ / 24 = 1/4 each", x=50, y=74),
   dict(at="revised", k="pill", text="Equation 3.1 as revised: awaiting supervisor confirmation (E1)", x=50, y=86, warn=True),
 ]),
 dict(n="11", chap="Equations 3.2 and 3.3", title="A worked example", imgs=["calc"], ev=[
   dict(at="naive", k="zoom", cx=36, cy=47, s=1.9),
   dict(at="naive", k="hl", rect=[0, 44, 15, 6]),
   dict(at="Retention", k="hl", rect=[15, 44, 14, 6]),
   dict(at="Block", k="hl", rect=[29, 44, 14, 6]),
   dict(at="Block", k="pill", text="illustrative numbers: 83 → 93 → 130 per day", x=50, y=92),
   dict(at="Equation", k="hl", rect=[43, 44, 13, 6]),
   dict(at="abstains.", k="reset"),
 ]),
 dict(n="12", chap="Equation 3.4", title="Pool the week, not the day", imgs=["cov", "sim"], ev=[
   dict(at="two", k="hl", rect=[0, 23, 100, 11]),
   dict(at="seven", k="hl", rect=[0, 85, 100, 11]),
   dict(at="five", k="hl", rect=[0, 57, 100, 11]),
   dict(at="six", k="hl", rect=[0, 71, 100, 11]),
   dict(at="six", k="pill", text="valid by every block, not valid by day/night: abstains", x=50, y=6),
   dict(at="simulation", k="swap", i=1),
   dict(at="eighty-eight", k="pill", text="poor coverage: computable 87–88% pooled vs 81–82% per day", x=50, y=92),
 ]),
 dict(n="13", chap="Evaluation", title="Patients never cross sets", imgs=["part"], ev=[
   dict(at="preliminary", k="hl", rect=[24, 4, 24, 18]),
   dict(at="hypothesis", k="hl", rect=[24, 24, 24, 16]),
   dict(at="development,", k="hl", rect=[24, 45, 24, 24]),
   dict(at="held", k="hl", rect=[24, 70, 24, 20]),
   dict(at="frozen", k="hl", rect=[53, 45, 22, 21]),
   dict(at="primary", k="hl", rect=[78, 11, 21, 31]),
   dict(at="degraded", k="hl", rect=[78, 55, 21, 34]),
 ]),
 dict(n="14", chap="RO3 · Deployability", title="Seven days of wear after stroke", imgs=["ro3"], ev=[
   dict(at="seven", k="hl", rect=[0, 8, 100, 9]), dict(at="seven", k="zoom", cx=50, cy=13, s=1.45),
   dict(at="primary", k="hl", rect=[0, 47, 100, 6]), dict(at="primary", k="zoom", cx=50, cy=50, s=1.45),
   dict(at="traffic-light", k="hl", rect=[0, 65, 100, 7.5]), dict(at="traffic-light", k="zoom", cx=50, cy=66, s=1.45),
   dict(at="Device", k="hl", rect=[0, 1, 100, 7]), dict(at="Device", k="zoom", cx=50, cy=8, s=1.45),
   dict(at="personal", k="pill", text="24-hour logging: Garmin personal communication only", x=50, y=92, warn=True),
 ]),
 dict(n="15", chap="Preliminary · Pilot", title="Ranking transfers; the threshold does not", imgs=["auc", "recall"], ev=[
   dict(at="0.995", k="pill", text="AUROC ≥ 0.995 where non-AF windows existed", x=40, y=92),
   dict(at="operating", k="swap", i=1),
   dict(at="forty-five", k="hl", rect=[74, 28, 16, 60]),
   dict(at="forty-five", k="pill", text="MIMIC-III AF recall 45% at 0.393", x=50, y=8),
   dict(at="Each", k="pill", text="one AF subject per external cohort", x=50, y=8),
   dict(at="await", k="pill", text="pilot values awaiting supervisor confirmation (E11)", x=50, y=92, warn=True),
 ]),
 dict(n="16", chap="Preliminary · Pulsewatch", title="The retention check did not pass", kind="silent", imgs=["pre"], seconds=15.0, ev=[
   dict(at=1.2, k="pill", text="8 subjects, rule locked before the run", x=50, y=8),
   dict(at=4.2, k="hl", rect=[6, 8, 72, 32]),
   dict(at=4.2, k="pill", text="beat match 0.85 → 0.41 as motion rises, above chance", x=50, y=8),
   dict(at=8.0, k="pill", text="absolute retention depended on the peak detector", x=50, y=92),
   dict(at=11.2, k="pill", text="check not passed: no retention value is claimed", x=50, y=92, warn=True),
 ]),
 dict(n="17", chap="Closing", title="The contribution is the observation model", kind="close"),
]

# ---------------------------------------------------------------- helpers
def anchor_time(words, at, scene):
    if isinstance(at, (int, float)):
        return float(at)
    word, nth = (at.split("#") + ["1"])[:2]
    nth = int(nth)
    key = norm(word)
    c = 0
    for w in words:
        if norm(w["text"]) == key:
            c += 1
            if c == nth:
                return w["start"]
    raise SystemExit(f"anchor '{at}' not found in scene {scene}")

def fit(iw, ih, bw, bh):
    s = min(bw / iw, bh / ih)
    return iw * s, ih * s

def groups(words):
    """Caption groups of 4-6 words; break at sentence end, pause >= 0.15 s or 6 words."""
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        end_sent = w["text"][-1] in ".?!:;"
        pause = nxt is not None and nxt["start"] - w["end"] >= 0.15
        if len(cur) >= 6 or (len(cur) >= 3 and (end_sent or pause or w["text"].endswith(","))) or nxt is None:
            out.append(cur); cur = []
    return out

COMMON_CSS = """
#root{position:absolute;inset:0;font-family:'Lato',sans-serif;color:var(--color-ink)}
.chap{position:absolute;left:120px;top:80px;font-family:'IBM Plex Mono',monospace;font-size:28px;letter-spacing:.14em;text-transform:uppercase;color:var(--color-accent)}
.ttl{position:absolute;left:120px;top:122px;width:1680px;font-family:'EB Garamond',serif;font-weight:400;font-size:84px;line-height:1.05;color:var(--color-ink);letter-spacing:-.01em}
.ttl span{display:inline-block;margin-right:.24em}
.stage{position:absolute;left:%(x)dpx;top:%(y)dpx;width:%(w)dpx;height:%(h)dpx;overflow:hidden;border-radius:14px}
.cam{position:absolute;left:0;top:0;width:100%%;height:100%%;display:flex;align-items:center;justify-content:center}
.card{position:relative;background:#fff;border-radius:14px;box-shadow:0 18px 50px rgba(24,34,44,.12),0 0 0 1px rgba(24,34,44,.08);overflow:hidden}
.card img{position:absolute;left:0;top:0;width:100%%;height:100%%;object-fit:contain}
.hl{position:absolute;border:5px solid var(--color-accent);border-radius:12px;box-shadow:0 0 0 9999px rgba(246,247,245,.0),0 0 24px rgba(163,33,79,.35)}
.pill{position:absolute;left:0;width:100%%;text-align:center;pointer-events:none}
.pill b{display:inline-block;font-family:'IBM Plex Mono',monospace;font-weight:400;font-size:30px;line-height:1.3;color:var(--color-ink);background:#fff;border:2px solid var(--color-accent);border-left-width:10px;border-radius:10px;padding:10px 22px;box-shadow:0 10px 30px rgba(24,34,44,.14)}
.pill.warn b{border-color:#A86200;color:#6b3f00}
""" % STAGE

def scene_shell(sid, dur_s, css, body, js):
    return f"""<template>
  <style>
{COMMON_CSS}
{css}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1920" data-height="1080" data-start="0" data-duration="{dur_s:.2f}">
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{sid}"] = tl;
  </script>
</template>
"""

def title_html(sid, sc):
    words = sc["title"].split()
    spans = "".join(f'<span id="{sid}-t{i}">{esc(w)}</span>' for i, w in enumerate(words))
    return (f'    <div class="chap" id="{sid}-chap">{esc(sc["chap"])}</div>\n'
            f'    <h1 class="ttl" id="{sid}-ttl">{spans}</h1>\n'), len(words)

def title_js(sid, nwords, end):
    js = [f'    tl.fromTo("#{sid}-chap", {{opacity:0, filter:"blur(6px)"}}, {{opacity:1, filter:"blur(0px)", duration:0.25, ease:"power4.out"}}, 0.15);']
    for i in range(nwords):
        js.append(f'    tl.fromTo("#{sid}-t{i}", {{opacity:0, filter:"blur(6px)"}}, {{opacity:1, filter:"blur(0px)", duration:0.16, ease:"power4.out"}}, {0.3 + i*0.075:.3f});')
    js.append(f'    tl.to(["#{sid}-chap", "#{sid}-ttl"], {{opacity:0, filter:"blur(8px)", duration:0.22, ease:"power3.in"}}, {end-0.3:.2f});')
    return "\n".join(js)

def figure_scene(sc, words, dur_s):
    sid = "s" + sc["n"]
    t_html, nw = title_html(sid, sc)
    imgs = sc["imgs"]
    iw, ih = Image.open(ROOT / "assets/fig" / f"{imgs[0]}.png").size
    cw, ch = fit(iw, ih, STAGE["w"], STAGE["h"] - 40)
    body = [t_html, f'    <div class="stage" id="{sid}-stage">', f'      <div class="cam" id="{sid}-cam">',
            f'        <div class="card" id="{sid}-card" style="width:{cw:.0f}px;height:{ch:.0f}px">']
    for i, im in enumerate(imgs):
        body.append(f'          <img id="{sid}-img{i}" src="assets/fig/{im}.png" alt="">')
    evs = sorted([dict(e, t=anchor_time(words, e["at"], sid) + (0 if sc.get("kind") == "silent" else LEAD)) for e in sc["ev"]],
                 key=lambda e: e["t"])
    hls = [e for e in evs if e["k"] == "hl"]
    for j, e in enumerate(hls):
        x, y, w_, h_ = e["rect"]
        body.append(f'          <div class="hl" id="{sid}-hl{j}" style="left:{x}%;top:{y}%;width:{w_}%;height:{h_}%"></div>')
    body.append('        </div>\n      </div>')
    pills = [e for e in evs if e["k"] == "pill"]
    for j, e in enumerate(pills):
        cls = "pill warn" if e.get("warn") else "pill"
        body.append(f'      <div class="{cls}" id="{sid}-p{j}" style="top:calc({e["y"]}% - 28px)"><b>{esc(e["text"])}</b></div>')
    body.append('    </div>')

    js = [title_js(sid, nw, dur_s)]
    js.append(f'    tl.fromTo("#{sid}-card", {{opacity:0, y:40, filter:"blur(10px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.7, ease:"expo.out"}}, 0.55);')
    for i in range(1, len(imgs)):
        js.append(f'    tl.set("#{sid}-img{i}", {{opacity:0}}, 0);')
    # swaps
    cur = 0
    for e in evs:
        if e["k"] == "swap":
            js.append(f'    tl.to("#{sid}-img{cur}", {{opacity:0, filter:"blur(8px)", duration:0.2, ease:"power2.in"}}, {e["t"]:.2f});')
            js.append(f'    tl.fromTo("#{sid}-img{e["i"]}", {{opacity:0, filter:"blur(8px)"}}, {{opacity:1, filter:"blur(0px)", duration:0.3, ease:"power3.out"}}, {e["t"]+0.12:.2f});')
            cur = e["i"]
    # highlights: each lasts until the next highlight or a swap/reset, else to the end
    stops = sorted([e["t"] for e in evs if e["k"] in ("hl", "swap", "reset")] + [dur_s - 0.35])
    for j, e in enumerate(hls):
        nxt = next(t for t in stops if t > e["t"] + 0.01)
        js.append(f'    tl.fromTo("#{sid}-hl{j}", {{opacity:0, scale:1.06}}, {{opacity:1, scale:1, duration:0.35, ease:"expo.out"}}, {e["t"]:.2f});')
        js.append(f'    tl.to("#{sid}-hl{j}", {{opacity:0, duration:0.18, ease:"power2.in"}}, {max(nxt - 0.12, e["t"] + 0.4):.2f});')
    # pills: each lasts until the next pill in the same band (top/bottom) or the end
    for j, e in enumerate(pills):
        band = e["y"] < 50
        later = [p["t"] for p in pills[j+1:] if (p["y"] < 50) == band]
        later += [x["t"] for x in evs if x["k"] == "swap" and x["t"] > e["t"] + 0.01]
        end = min(later) if later else dur_s - 0.35
        js.append(f'    tl.fromTo("#{sid}-p{j} b", {{opacity:0, y:12, filter:"blur(6px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.4, ease:"expo.out"}}, {e["t"]:.2f});')
        js.append(f'    tl.to("#{sid}-p{j} b", {{opacity:0, filter:"blur(6px)", duration:0.18, ease:"power3.in"}}, {max(end - 0.12, e["t"] + 0.5):.2f});')
    # camera
    for e in evs:
        if e["k"] == "zoom":
            s = e["s"]
            x = -(e["cx"] / 100 - 0.5) * cw * s
            y = -(e["cy"] / 100 - 0.5) * ch * s
            mx = max((cw * s - STAGE["w"]) / 2, 0); my = max((ch * s - STAGE["h"]) / 2, 0)
            x = max(-mx, min(mx, x)); y = max(-my, min(my, y))
            js.append(f'    tl.to("#{sid}-cam", {{scale:{s}, x:{x:.0f}, y:{y:.0f}, duration:0.9, ease:"power2.inOut"}}, {e["t"]-0.15:.2f});')
        if e["k"] == "reset":
            js.append(f'    tl.to("#{sid}-cam", {{scale:1, x:0, y:0, duration:0.8, ease:"power2.inOut"}}, {e["t"]:.2f});')
    js.append(f'    tl.to("#{sid}-stage", {{opacity:0, filter:"blur(10px)", duration:0.25, ease:"power3.in"}}, {dur_s-0.3:.2f});')
    css = f"#{sid}-cam{{transform-origin:50% 50%}}"
    return scene_shell(sid, dur_s, css, "\n".join(body), "\n".join(js))

def eq_scene(sc, words, dur_s):
    sid = "s" + sc["n"]
    t_html, nw = title_html(sid, sc)
    body = [t_html, f'    <div class="stage" id="{sid}-stage">']
    evs = sorted([dict(e, t=anchor_time(words, e["at"], sid) + LEAD) for e in sc["ev"]], key=lambda e: e["t"])
    for i, im in enumerate(sc["imgs"][:2]):
        iw, ih = Image.open(ROOT / "assets/fig" / f"{im}.png").size
        w_ = 1560; h_ = w_ * ih / iw
        body.append(f'      <div class="card" id="{sid}-eq{i}" style="position:absolute;left:{(STAGE["w"]-w_)/2:.0f}px;top:{30 + i*(h_+40):.0f}px;width:{w_}px;height:{h_:.0f}px"><img src="assets/fig/{im}.png" alt=""></div>')
    pills = [e for e in evs if e["k"] == "pill"]
    for j, e in enumerate(pills):
        cls = "pill warn" if e.get("warn") else "pill"
        body.append(f'      <div class="{cls}" id="{sid}-p{j}" style="top:calc({e["y"]}% - 28px)"><b>{esc(e["text"])}</b></div>')
    body.append('    </div>')
    js = [title_js(sid, nw, dur_s)]
    for e in evs:
        if e["k"] == "show":
            js.append(f'    tl.fromTo("#{sid}-eq{e["i"]}", {{opacity:0, x:-40, filter:"blur(10px)"}}, {{opacity:1, x:0, filter:"blur(0px)", duration:0.6, ease:"expo.out"}}, {max(e["t"], 0.6):.2f});')
    for j, e in enumerate(pills):
        later = [p["t"] for p in pills[j+1:] if p["y"] == e["y"]]
        end = later[0] if later else dur_s - 0.35
        js.append(f'    tl.fromTo("#{sid}-p{j} b", {{opacity:0, y:12, filter:"blur(6px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.4, ease:"expo.out"}}, {e["t"]:.2f});')
        js.append(f'    tl.to("#{sid}-p{j} b", {{opacity:0, filter:"blur(6px)", duration:0.18, ease:"power3.in"}}, {max(end - 0.12, e["t"] + 0.5):.2f});')
    js.append(f'    tl.to("#{sid}-stage", {{opacity:0, filter:"blur(10px)", duration:0.25, ease:"power3.in"}}, {dur_s-0.3:.2f});')
    return scene_shell(sid, dur_s, "", "\n".join(body), "\n".join(js))

# ECG-like trace for the intro: RR series with one PAC (short) and its pause (long)
def ecg_path(x0, y0, width, beats):
    pts = []; x = x0
    for rr, pac in beats:
        step = rr * 0.30
        # baseline, P, QRS, T as a polyline (P absent on the PAC to mark it)
        seq = [(0, 0), (0.18, 0), (0.24, -10 if not pac else 0), (0.30, 0), (0.40, 0), (0.43, 14), (0.47, -120), (0.51, 34), (0.55, 0), (0.70, 0), (0.80, -22), (0.90, 0)]
        for fx, fy in seq:
            pts.append((x + fx * step, y0 + fy))
        x += step
        if x > x0 + width:
            break
    return "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts), x

def intro_scene(sc, words, dur_s):
    sid = "s01"
    T = lambda w, n=1: anchor_time(words, w + ("#%d" % n if n > 1 else ""), sid) + LEAD
    beats = [(800, 0)] * 5 + [(480, 1), (1120, 0)] + [(800, 0)] * 6
    d, xend = ecg_path(150, 420, 1620, beats)
    pac_x = 150 + sum(rr * 0.30 for rr, _ in beats[:5])
    body = f"""    <div class="chap" id="{sid}-chap">{esc(sc["chap"])}</div>
    <h1 class="ttl" id="{sid}-ttl" style="font-size:104px;top:118px">{''.join(f'<span id="{sid}-t{i}">{esc(w)}</span>' for i, w in enumerate(sc["title"].split()))}</h1>
    <svg id="{sid}-ecg" style="position:absolute;left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">
      <path id="{sid}-trace" d="{d}" fill="none" stroke="#18222C" stroke-width="4" stroke-linejoin="round"/>
      <rect id="{sid}-pacbox" x="{pac_x-18:.0f}" y="280" width="{480*0.30+60:.0f}" height="190" rx="12" fill="none" stroke="#A3214F" stroke-width="5"/>
      <text id="{sid}-paclbl" x="{pac_x+40:.0f}" y="270" font-family="IBM Plex Mono" font-size="28" fill="#A3214F" text-anchor="middle">PAC: early beat, then a long pause</text>
    </svg>
    <div id="{sid}-defs" style="position:absolute;left:120px;top:520px;width:1680px">
      <div class="pill" id="{sid}-p0" style="position:relative;text-align:left"><b>ESVEA: excessive supraventricular ectopic activity, ≥ 480 beats per day</b></div>
    </div>
    <div id="{sid}-row" style="position:absolute;left:120px;top:640px;width:1680px;display:flex;gap:28px">
      <div class="prob" id="{sid}-c0"><i>Thresholds</i>derived on Holter ECG, the resource being rationed</div>
      <div class="prob" id="{sid}-c1"><i>Smartwatch</i>beat intervals + a per-beat quality flag; error unknown</div>
      <div class="prob" id="{sid}-c2"><i>Problem 1</i>filtering removes ectopic beats preferentially</div>
      <div class="prob" id="{sid}-c3"><i>Problem 2</i>usable data weighted to night; PACs peak afternoon and evening</div>
    </div>"""
    css = f"""
#{sid}-row .prob{{flex:1;background:#fff;border-radius:14px;padding:22px 24px;font-size:28px;line-height:1.3;box-shadow:0 14px 40px rgba(24,34,44,.10),0 0 0 1px rgba(24,34,44,.08)}}
#{sid}-row .prob i{{display:block;font-style:normal;font-family:'IBM Plex Mono',monospace;font-size:28px;letter-spacing:.08em;text-transform:uppercase;color:var(--color-accent);margin-bottom:8px}}
"""
    L = 4000
    js = [title_js(sid, len(sc["title"].split()), dur_s),
          f'    tl.fromTo("#{sid}-trace", {{strokeDasharray:{L}, strokeDashoffset:{L}}}, {{strokeDashoffset:0, duration:3.2, ease:"none"}}, 0.6);',
          f'    tl.fromTo(["#{sid}-pacbox", "#{sid}-paclbl"], {{opacity:0}}, {{opacity:1, duration:0.35, ease:"expo.out"}}, {T("premature"):.2f});',
          f'    tl.fromTo("#{sid}-p0 b", {{opacity:0, y:12, filter:"blur(6px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.4, ease:"expo.out"}}, {T("ESVEA,"):.2f});']
    for i, (w, n) in enumerate([("Holter", 1), ("Smartwatches", 1), ("Filtering", 1), ("night,", 1)]):
        js.append(f'    tl.fromTo("#{sid}-c{i}", {{opacity:0, y:30, filter:"blur(8px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.55, ease:"expo.out"}}, {T(w, n):.2f});')
    js.append(f'    tl.to(["#{sid}-ecg", "#{sid}-defs", "#{sid}-row"], {{opacity:0, filter:"blur(10px)", duration:0.25, ease:"power3.in"}}, {dur_s-0.3:.2f});')
    return scene_shell(sid, dur_s, css, body, "\n".join(js))

def close_scene(sc, words, dur_s):
    sid = "s17"
    T = lambda w: anchor_time(words, w, sid) + LEAD
    t_html, nw = title_html(sid, sc)
    lim = [("simulated", "Error measured under simulated losses, not on a device"),
           ("deficit", "Pulse deficit: a measured bias, not corrected"),
           ("Samsung", "Samsung → Garmin transfer: an assumption")]
    con = [("flag", "The flag as evidence"), ("frozen", "A frozen retention correction"), ("coverage", "A coverage gate that knows when not to report")]
    body = [t_html, f'    <div id="{sid}-lim" style="position:absolute;left:120px;top:300px;width:1680px;display:flex;gap:24px">']
    for i, (_, t) in enumerate(lim):
        body.append(f'      <div class="lim" id="{sid}-l{i}">{esc(t)}</div>')
    body.append('    </div>')
    body.append(f'    <div id="{sid}-con" style="position:absolute;left:120px;top:500px;width:1680px;display:flex;gap:24px">')
    for i, (_, t) in enumerate(con):
        body.append(f'      <div class="con" id="{sid}-k{i}"><i>0{i+1}</i>{esc(t)}</div>')
    body.append('    </div>')
    body.append(f'    <div id="{sid}-last" style="position:absolute;left:120px;top:760px;width:1680px;font-family:\'EB Garamond\',serif;font-size:56px;font-style:italic">The graph architecture is a means, tested against baselines.</div>')
    css = f"""
#{sid}-lim .lim{{flex:1;font-size:28px;line-height:1.3;color:#5A6570;border-top:3px solid #D8DDDD;padding-top:14px}}
#{sid}-con .con{{flex:1;background:#fff;border-radius:14px;padding:26px 28px;font-size:38px;line-height:1.2;box-shadow:0 14px 40px rgba(24,34,44,.12),0 0 0 1px rgba(24,34,44,.08);border-left:10px solid var(--color-accent)}}
#{sid}-con .con i{{display:block;font-style:normal;font-family:'IBM Plex Mono',monospace;font-size:28px;color:var(--color-accent);margin-bottom:10px}}
"""
    js = [title_js(sid, nw, dur_s + 10)]  # title stays to the end
    for i, (w, _) in enumerate(lim):
        js.append(f'    tl.fromTo("#{sid}-l{i}", {{opacity:0, filter:"blur(6px)"}}, {{opacity:1, filter:"blur(0px)", duration:0.4, ease:"power4.out"}}, {T(w):.2f});')
    for i, (w, _) in enumerate(con):
        js.append(f'    tl.fromTo("#{sid}-k{i}", {{opacity:0, y:30, filter:"blur(8px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.55, ease:"expo.out"}}, {T(w):.2f});')
    js.append(f'    tl.fromTo("#{sid}-last", {{opacity:0, filter:"blur(8px)"}}, {{opacity:1, filter:"blur(0px)", duration:0.5, ease:"power4.out"}}, {T("graph"):.2f});')
    return scene_shell(sid, dur_s, css, "\n".join(body), "\n".join(js))

# ---------------------------------------------------------------- build
def main():
    comp = ROOT / "compositions"; comp.mkdir(exist_ok=True)
    t0 = 0.0
    hosts, audios, cap_groups, timeline = [], [], [], []
    for sc in S:
        sid = "s" + sc["n"]
        mp3 = ROOT / "assets/audio" / f"{sid}.mp3"
        if sc.get("kind") == "silent" or not mp3.exists():
            words, d = [], sc.get("seconds", 15.0)
            dur_s = d
        else:
            words = load(sid, TEXT[sc["n"]])
            if words is None:
                raise SystemExit(f"no transcript for {sid}")
            a = dur(mp3)
            dur_s = round(LEAD + a + TAIL, 2)
            audios.append(f'      <audio id="{sid}-vo" class="clip" src="assets/audio/{sid}.mp3" data-start="{t0 + LEAD:.2f}" data-duration="{a:.2f}" data-track-index="20" data-volume="1"></audio>')
            for g in groups(words):
                cap_groups.append((t0 + LEAD + g[0]["start"] - 0.05, t0 + LEAD + g[-1]["end"] + 0.08, " ".join(w["text"] for w in g)))
        kind = sc.get("kind")
        src = {"intro": intro_scene, "close": close_scene, "eqs": eq_scene}.get(kind, figure_scene)(sc, words, dur_s)
        (comp / f"{sid}.html").write_text(src)
        hosts.append(f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{t0:.2f}" data-duration="{dur_s:.2f}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>')
        timeline.append((sid, t0, dur_s, sc["title"]))
        t0 = round(t0 + dur_s, 2)
    total = t0

    # captions: one composition holding every group; no overlap between groups
    cap_groups.sort()
    fixed = []
    for i, (s, e, txt) in enumerate(cap_groups):
        if i + 1 < len(cap_groups):
            e = min(e, cap_groups[i + 1][0] - 0.02)
        fixed.append((s, e, txt))
    cb = [f'    <div class="cg" id="cap{i}"><span>{esc(t)}</span></div>' for i, (s, e, t) in enumerate(fixed)]
    cj = []
    for i, (s, e, t) in enumerate(fixed):
        cj.append(f'    tl.set("#cap{i}", {{visibility:"visible"}}, {s:.2f}); tl.fromTo("#cap{i}", {{opacity:0}}, {{opacity:1, duration:0.1}}, {s:.2f});')
        cj.append(f'    tl.to("#cap{i}", {{opacity:0, duration:0.1, ease:"power2.in"}}, {e-0.1:.2f}); tl.set("#cap{i}", {{opacity:0, visibility:"hidden"}}, {e:.2f});')
    cap_css = """
#root{position:absolute;inset:0}
.cg{position:absolute;left:0;bottom:62px;width:100%;text-align:center;visibility:hidden;opacity:0}
.cg span{display:inline-block;font-family:'Lato',sans-serif;font-weight:700;font-size:40px;line-height:1.25;color:#18222C;background:rgba(255,255,255,.88);padding:8px 20px;border-radius:10px;max-width:1500px}
"""
    (comp / "captions.html").write_text(f"""<template>
  <style>{cap_css}</style>
  <div id="root" data-composition-id="captions" data-width="1920" data-height="1080" data-start="0" data-duration="{total:.2f}" data-layout-allow-caption-zone>
{chr(10).join(cb)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join(cj)}
    window.__timelines["captions"] = tl;
  </script>
</template>
""")

    # chrome: progress line and scene counter, whole film
    chrome_marks = "".join(f'<i style="left:{120 + 1680*s/total:.1f}px"></i>' for _, s, _, _ in timeline[1:])
    counter = []
    for k, (sid, s, d, _) in enumerate(timeline):
        counter.append(f'    <div class="cnt" id="cnt{k}">{k+1:02d} / {len(timeline):02d}</div>')
    cjs = [f'    tl.fromTo("#bar", {{scaleX:0}}, {{scaleX:1, duration:{total:.2f}, ease:"none"}}, 0);']
    for k, (sid, s, d, _) in enumerate(timeline):
        cjs.append(f'    tl.set("#cnt{k}", {{opacity:1}}, {s:.2f}); tl.set("#cnt{k}", {{opacity:0}}, {s+d-0.01:.2f});')
    (comp / "chrome.html").write_text(f"""<template>
  <style>
#root{{position:absolute;inset:0}}
#track{{position:absolute;left:120px;top:48px;width:1680px;height:4px;background:#D8DDDD;border-radius:2px}}
#bar{{position:absolute;left:120px;top:48px;width:1680px;height:4px;background:#A3214F;border-radius:2px;transform-origin:0 50%}}
#marks i{{position:absolute;top:44px;width:2px;height:12px;background:#F6F7F5}}
.cnt{{position:absolute;right:120px;top:72px;font-family:'IBM Plex Mono',monospace;font-size:28px;color:#5A6570;opacity:0}}
  </style>
  <div id="root" data-composition-id="chrome" data-width="1920" data-height="1080" data-start="0" data-duration="{total:.2f}">
    <div id="track"></div><div id="bar"></div><div id="marks">{chrome_marks}</div>
{chr(10).join(counter)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join(cjs)}
    window.__timelines["chrome"] = tl;
  </script>
</template>
""")

    idx = f"""<!doctype html>
<html lang="en" data-composition-variables='[
  {{"id":"color-ground","type":"color","label":"Background","default":"#F6F7F5"}},
  {{"id":"color-ink","type":"color","label":"Text","default":"#18222C"}},
  {{"id":"color-accent","type":"color","label":"Accent","default":"#A3214F"}}
]'>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      :root {{ --color-ground:#F6F7F5; --color-ink:#18222C; --color-accent:#A3214F; }}
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ margin:0; width:1920px; height:1080px; overflow:hidden; background:var(--color-ground); }}
      #paper {{ position:absolute; inset:0; background-color:var(--color-ground);
        background-image:linear-gradient(rgba(163,33,79,.07) 1px, transparent 1px), linear-gradient(90deg, rgba(163,33,79,.07) 1px, transparent 1px);
        background-size:48px 48px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total:.2f}" data-width="1920" data-height="1080">
      <div id="paper"></div>
{chr(10).join(hosts)}
      <div id="chrome" data-composition-id="chrome" data-composition-src="compositions/chrome.html" data-start="0" data-duration="{total:.2f}" data-track-index="2" data-track-kind="graphics" data-width="1920" data-height="1080"></div>
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{total:.2f}" data-track-index="3" data-track-kind="captions" data-width="1920" data-height="1080"></div>
{chr(10).join(audios)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
    (ROOT / "index.html").write_text(idx)
    (ROOT / "build" / "timeline.json").write_text(json.dumps(timeline, indent=1))
    print("total", total, "s;", len(fixed), "caption groups")
    for sid, s, d, t in timeline:
        print(f"{sid} {s:7.2f} {d:6.2f}  {t}")

if __name__ == "__main__":
    main()
