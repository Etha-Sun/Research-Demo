# Research-Demo: from a failed proof to a trusted one

This is the source kit for a four-part explainer video series about Yuechun Sun's research on LLMs and formal
verification. Everything is code: storyboards, narration, Manim scenes and the source audit. The videos are rendered on
your own machine.

| # | Episode | Topic | Narration |
|---|---------|-------|-----------|
| 1 | **ExVerus** (ICML 2026) | Verus proof repair via counterexample reasoning; also opens the series | ~9 min |
| 2 | **TopoVerus** (NeurIPS 2026) | A model trained with RL to produce counterexamples and repairs; safety gate; topological graph reward | ~8 min |
| 3 | **Vero** (NeurIPS 2026) | Can AI agents build formally verified software repositories? Benchmark, checker, spec audit | ~8 min |
| 4 | **Vekto** (work in progress) | C-level equivalence proofs for SIMD kernel migrations (NEON/SSE → RVV/HVX) with QCP + Coq | ~9 min |

Through-line: **counterexamples connect a failed proof to its repair**, and **a proof is only as good as its spec and
its checker**. See `docs/SERIES.md`.

## Quick start (macOS / Linux)

```bash
git clone https://github.com/Etha-Sun/Research-Demo.git && cd Research-Demo
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt        # manim 0.19.1 (+ kokoro TTS, optional)
# Manim needs cairo/pango/ffmpeg:  macOS: brew install cairo pango ffmpeg pkg-config
#                                  Ubuntu: sudo apt install libcairo2-dev libpango1.0-dev ffmpeg

./render.sh exverus l none             # fast 480p silent preview of episode 1
./render.sh exverus h kokoro           # 1080p60 with local English voice + en/zh subtitles
./render.sh all h kokoro               # all four episodes
```

Outputs go to `out/<episode>.mp4` with `out/<episode>.en.srt` and `out/<episode>.zh.srt`. Options:

- `./render.sh EP Q ENGINE LANG`
  - Q: `l` (480p) / `m` / `h` (1080p60) / `k` (4K)
  - ENGINE: `kokoro` / `say` (macOS) / `none`
  - LANG: `en` (voice; zh becomes subtitles) or `zh` (Chinese voice)
- Nicer fonts: `export VIDEO_FONT_SANS="Inter" VIDEO_FONT_MONO="JetBrains Mono"`. For Chinese, any CJK font works,
  e.g. `PingFang SC`.
- To burn subtitles into the picture: `python tools/mux.py EP --burn`.
- To preview one scene: `PYTHONPATH=. manim -pql episodes/exverus/scenes.py ExV04Brs1Bug`.

## How the kit is organised

```
docs/SERIES.md            series arc, fixed recap/bridge lines, chosen examples, numbers policy
docs/PRODUCTION-SPEC.md   conventions every episode follows
docs/REVIEW.md            final fact-check / continuity review and open issues for the author
episodes/<ep>/            STORYBOARD.md, narration.json (en + zh), scenes.py, examples/, SOURCES.md
research/<ep>/            research briefs, verbatim code examples and cited claims (sources.json)
common/                   shared style (colours, fonts) and Manim components
tools/                    tts.py, sync_durations.py, mux.py, check_episode.py
verify/                   optional local Verus re-check of the on-screen Verus examples
papers/fetch.sh           downloads the three papers (PDFs are not committed)
repos/fetch.sh            shallow clones of the public code repos at the cited commits
```

**Editing workflow.**
1. Edit the narration in `episodes/<ep>/narration.json`.
2. Run `python tools/check_episode.py <ep>`.
3. Run `./render.sh <ep> l none` and review the preview.
4. Render at `h`.

Voice clips are cached per beat and only changed beats are re-synthesised. Scene timing follows the voice
automatically: `tts.py` → `sync_durations.py` → manim → `mux.py`.

**Working with Claude Code locally.** Open this folder in Claude Code and ask for changes scene by scene. A Manim agent
skill can help, but review third-party skills before installing them. `docs/PRODUCTION-SPEC.md` is the contract
they must follow.

## Source integrity

- Every on-screen number has a citation footnote, and every code panel is verbatim from the paper or repository.
  Trims are documented in the example file headers and in `SOURCES.md`.
- Where the papers' own numbers were inconsistent, the episode uses per-table values only (see `docs/SERIES.md`).
- Some examples were not re-run by us. The TopoVerus Case B repair is narrated as "the paper reports". `verify/` lets
  you check the Verus examples locally.
- Vekto is unpublished ongoing work; its episode labels results as established / in progress / not started.
