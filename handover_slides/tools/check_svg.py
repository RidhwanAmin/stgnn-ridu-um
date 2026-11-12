"""Every inline <svg> in the deck must parse as XML (a raw '<' in text breaks the slide). Usage: python check_svg.py <slides_dir>"""
import re, sys, pathlib, xml.dom.minidom as m
bad = 0
for f in sorted(pathlib.Path(sys.argv[1]).glob("*.html")):
    for s in re.findall(r"<svg.*?</svg>", f.read_text(), re.S):
        try: m.parseString(s)
        except Exception as e: bad += 1; print(f.name, e)
print("ok" if not bad else f"{bad} broken svg")
