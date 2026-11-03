# Narrated walkthrough video (HyperFrames)

A 9 min 10 s, 1920×1080, 30 fps explainer of the research, built from the research map
(https://claude.ai/artifact/1BnWNir54MvkSfH5uPfMiE, version 8) with
[HyperFrames](https://hyperframes.heygen.com) and ElevenLabs narration.

| Item | Where |
|---|---|
| Narration script (17 scenes) | `narration.json` |
| HyperFrames project | `hf/` (`index.html`, `compositions/`, `assets/`) |
| Scene generator | `hf/build/gen.py` (scene data, anchors, camera moves, captions); `hf/build/align.py` (script-to-Whisper alignment) |
| Figures | `hf/assets/fig/` — 2× captures of the research-map figures (`cap.js` style capture, light theme) |
| Narration audio | `hf/assets/audio/sNN.mp3` — ElevenLabs `eleven_v4`, voice "Astro – calm & steady for learning" (American) |
| Word timings | `hf/words/sNN.json` — local Whisper `small.en` |
| Rendered video | `hf/renders/ESVEA_research_walkthrough.mp4` (not committed; too large for git) |

## Rebuild

```bash
cd presenter/hf
python3 build/gen.py
npx hyperframes@0.9.7 check --json
npx hyperframes@0.9.7 render --quality delivery -o renders/ESVEA_research_walkthrough.mp4
```

## Known gaps

- **Scene 16 (Pulsewatch pre-check) has no narration.** The ElevenLabs account reached its
  40,000-credit quota before that clip was generated. The scene plays as a 15 s on-screen text
  card. To fix: generate the scene 16 line from `narration.json` with the same voice, save it as
  `hf/assets/audio/s16.mp3`, transcribe it
  (`npx hyperframes@0.9.7 transcribe assets/audio/s16.mp3 --model small.en`, copy
  `assets/audio/transcript.json` to `words/s16.json`), remove `kind="silent"` and the numeric
  anchors from scene 16 in `build/gen.py`, then rebuild and render.
- No music bed: the HeyGen music catalog needs `npx hyperframes auth login`.
- Captions use the script's exact words, timed by aligning to Whisper's word times; a few
  interpolated words (numbers spoken as words) can be off by a fraction of a second.
- Figure highlights mark regions by hand-set percentages of each captured figure; recapture the
  figures and recheck the boxes if the research map layout changes.
