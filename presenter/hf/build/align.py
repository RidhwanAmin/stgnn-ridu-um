"""Align the narration script (exact wording) to Whisper word timings.

Whisper mishears domain terms, so captions and anchors use the script's words;
times come from Whisper via a difflib alignment, with unmatched script words
interpolated between their matched neighbours.
"""
import difflib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def align(script_text, whisper_words):
    sw = script_text.split()
    a = [norm(w) for w in sw]
    b = [norm(w["text"]) for w in whisper_words]
    t = [None] * len(sw)
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            ww = whisper_words[blk.b + k]
            t[blk.a + k] = (ww["start"], ww["end"])
    # interpolate gaps
    n = len(sw)
    end_all = whisper_words[-1]["end"] if whisper_words else 1.0
    i = 0
    while i < n:
        if t[i] is None:
            j = i
            while j < n and t[j] is None:
                j += 1
            s0 = t[i - 1][1] if i > 0 else 0.0
            s1 = t[j][0] if j < n else end_all
            span = max(s1 - s0, 0.05)
            cnt = j - i
            for k in range(cnt):
                t[i + k] = (s0 + span * k / cnt, s0 + span * (k + 1) / cnt)
            i = j
        else:
            i += 1
    return [{"text": w, "start": round(s, 3), "end": round(e, 3)} for w, (s, e) in zip(sw, t)]


def load(scene_id, script_text):
    p = ROOT / "words" / f"{scene_id}.json"
    if not p.exists():
        return None
    d = json.loads(p.read_text())
    ww = d["words"] if isinstance(d, dict) else d
    return align(script_text, ww)
