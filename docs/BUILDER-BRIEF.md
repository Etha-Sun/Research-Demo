# Brief for episode builders

You build ONE episode of a four-part explainer video series as code (Manim Community 0.19.1), not as a rendered video.
Project root: build/research-demo/ (below, paths are relative to it).

Read first, fully: docs/SERIES.md (arc, fixed recap/bridge lines, chosen motivated examples, numbers policy),
docs/PRODUCTION-SPEC.md (file layout, conventions, checks), common/style.py and common/components.py (use these helpers;
look at their docstrings), and your episode's research/<ep>/BRIEF.md, research/<ep>/sources.json and research/<ep>/examples/.
Paper PDF: papers/<ep>.pdf (Vekto has no paper; its sources are repo files cited in the brief — read-only).

Produce in episodes/<ep>/:
1. STORYBOARD.md — 8–12 scenes; per scene: purpose, what is on screen (layout sketch in words), code panels with exact
   example file + lines, narration (en+zh), citations, duration estimate.
2. narration.json — beats per the spec (en voice, zh faithful translation; ~6–9 min total).
3. scenes.py — one NarratedScene subclass per scene (EPISODE = "<ep>", globally unique prefixed names), every beat used
   exactly once and in order. Professional pacing: build diagrams step by step, highlight the code line being discussed,
   transform the failing line into the fixed line, show the counterexample as a state_table next to the code, cite every
   number. Clear and uncluttered.
4. examples/ — the exact code shown on screen (copy from research/<ep>/examples, keep the source header).
5. SOURCES.md — every on-screen number/quote/code → source locator.

Rules:
- Never invent code, numbers or results. If the research brief marks something [inferred]/unverified/discrepant, follow
  docs/SERIES.md; if still unclear, leave it off screen and note it in STORYBOARD.md "Open issues".
- Do not claim a program "verifies" unless the paper (or repo record) says so; phrase as "the paper reports …".
- Write only inside episodes/<ep>/. If components.py lacks something you need, implement it locally in your scenes.py
  (note it in STORYBOARD.md "Open issues" so the supervisor can lift it into common/).
- CPU is shared: no full renders. Check with: `cd build/research-demo && .venv/bin/python -m py_compile episodes/<ep>/scenes.py`,
  `.venv/bin/python tools/check_episode.py <ep>` (must print OK), and last-frame stills of EVERY scene at low quality, one
  at a time: `PYTHONPATH=. nice -n 19 .venv/bin/manim -ql -s --media_dir /tmp/<ep>-media episodes/<ep>/scenes.py <Scene>`
  — then open the PNG with the Read tool and fix overlaps, text running off the frame, unreadable code. For scenes whose
  important moment is mid-scene, temporarily check with `-s -n <k>` (or render a still of a mid state) as needed.
  Note: -s skips animations quickly, so cost is small; never run more than one manim at a time.
- No absolute paths, host names, user names or tokens in deliverables.
- Finish with a ≤200-word summary: scenes, total narration minutes, open issues.
