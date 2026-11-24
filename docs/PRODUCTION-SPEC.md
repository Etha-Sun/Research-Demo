# Production spec (for everyone who writes an episode)

This spec keeps the four episodes consistent. Read it before touching `episodes/<ep>/`.

## Files per episode

```
episodes/<ep>/
  STORYBOARD.md     scene-by-scene plan: purpose, visuals, on-screen code, narration (en + zh), sources
  narration.json    the beats; the single source of truth for voice and subtitles
  scenes.py         Manim scenes (one class per scene), using common/components.py
  examples/         code shown on screen, one file per snippet, header comment = exact source
  SOURCES.md        every number / quote / code snippet on screen -> paper page/table/figure or repo file:line
```

## Conventions

1. **Scene names are globally unique.** Prefix them with the episode, for example `ExV01Hook`, `Topo03Reward`,
   `Vero02Benchmark`, `Vek05Counterexample`. Manim writes every scene to `media/videos/scenes/<res>/<Scene>.mp4`,
   and the timeline file uses the same name.
2. **Scene order** is the key order of `"scenes"` in `narration.json`.
3. **Beats.** Every narration sentence or two is one beat: `{"id": "<scene>-<n>", "seconds": <estimate>, "en": "...", "zh": "..."}`.
   Estimate `seconds` as words/2.6 for English (about 155 words per minute) plus 0.5 s; `tools/sync_durations.py` replaces it with the
   real voice length. In `scenes.py`, wrap the animations of each beat in `with self.beat("<id>"):`. Every beat id in
   narration.json must be used exactly once, in order. Animations inside a beat must be shorter than the beat.
4. **Language.** English narration is the default voice. The Chinese text is a faithful translation for the subtitles or a
   Chinese voice track. Keep technical terms in English inside the Chinese text (Verus, loop invariant, counterexample,
   SIMD, QCP, Coq, verification condition).
5. **Length.** Each episode is 6 to 9 minutes of narration and has 8 to 12 scenes.
6. **Shape of an episode.**
   1. Series map with the current episode lit, plus a one-sentence recap of the previous episode. Episode 1 introduces
      the whole series.
   2. Hook: a concrete failure or question shown in code, not a definition.
   3. Background: only the concepts the episode needs.
   4. Motivated example, step by step, in real code.
   5. The method as an architecture diagram. The motivated example then flows through the diagram.
   6. Results with citations.
   7. Limitations: what the work does not claim.
   8. Bridge to the next episode, then the series map again.
7. **Code on screen.**
   - Show real code, verbatim from the paper or repository.
   - Trimming for the screen is allowed: drop unrelated lines and use `...`. Never change a line's meaning.
   - Record the exact source and every trim in the header of `examples/<file>` and in SOURCES.md.
   - At most about 18 lines and about 70 columns per panel at `CODE_FONT_SIZE`.
   - Use `highlight_lines` to point at what the narration is talking about at that moment.
8. **Numbers.** Every number on screen carries a `cite(...)` footnote, for example "ExVerus, Table 2" or
   "repo: build/.../APPROVAL-x24-rvv.json". No rounding that changes meaning. Do not compare numbers measured under
   different settings without saying so.
9. **Honesty.**
   - State the paper's claims at the strength the paper states them.
   - Vekto is ongoing work. Mark results as established, in progress, or assumption, and show its modelling
     assumptions (for example LP64 for HVX, fixed VLEN) on screen when the claim depends on them.
10. **Style.**
    - Use only `common/style.py` colours and `common/components.py` helpers. Add a helper to components.py only if two
      episodes need it.
    - The episode accent colour marks "this episode's idea". `OK`/`BAD`/`WARN` mean verified / failure or
      counterexample / assumption, in every episode.
    - No LaTeX. Use `Text` and `Code` only, so that local installs need no TeX.
    - Keep the 16:9 frame clean: one idea per screen, generous margins, no more than about 25 words of on-screen text
      besides code.
11. **Privacy.** No absolute server paths, host names, user names, keys or tokens. Use repository-relative paths.

## Checking (cheap, the server CPU is shared)

- `python -m py_compile episodes/<ep>/scenes.py`
- `python tools/check_episode.py <ep>`: checks the beat ids and scene names, and lists all citations.
- Optional: last-frame stills at low quality, one scene at a time:
  `PYTHONPATH=. manim -ql -s --media_dir /tmp/<ep>-media episodes/<ep>/scenes.py <Scene>`. Look at the PNG.
- Do not render full videos on the server. Full renders run on the user's machine via `./render.sh`.
