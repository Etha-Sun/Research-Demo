# Revision brief (author feedback 2026-11-23)

Revise ONE video in episodes/<ep>/ (narration.json, scenes.py, STORYBOARD.md, SOURCES.md, examples/). First read
docs/SERIES.md and docs/PRODUCTION-SPEC.md — both were rewritten for this round.

The author's feedback, verbatim:
"不用标 our reading... 这种也太防御性了。我觉得vero和vekto就是两个工作，可以不用加太多联系的，我们尽量做到四个视频是相对独立的吧。以论文为主，用我们arxiv的版本"
(= Don't add labels like "our reading…", that is too defensive. Vero and Vekto are two separate works, no need for
many connections; make the four videos relatively independent. Paper first, use our arXiv version.)

Do:
1. Make the video self-contained:
   - Remove the series map, the series intro, recaps of other episodes and bridges to other episodes. Remove every
     mention of, and analogy to, the other three works (ExVerus/TopoVerus/Vero/Vekto), unless the paper itself cites
     that work as related work. Even then, keep it to one plain sentence at most.
   - Remove "Episode N" wording; `title_card(EP, extra=...)` no longer shows a number.
   - Open with the title card (authors · venue) and a concrete hook. End with this work's own takeaway.
2. Remove defensive labels and hedges, both on screen and in narration: "our reading of …", "illustrative",
   "not shown in the paper", "the paper reports…" used as a hedge, "test case from the released code", WARN badges
   about what we did not run, "unpublished · treat as status report", and similar.
   - Present the paper's figures and examples the way the paper presents them, with an ordinary citation footnote
     (for example "Fig. 2", "App. B").
   - Keep all facts true: do not claim anything the paper does not claim. If the paper presents a repair as the model's
     output, show it as the model's output; do not add verdicts the paper does not give.
3. Paper first (arXiv version in papers/<ep>.pdf; text via `.venv/bin/python -c "import pypdf…"`):
   - Where released code and paper differ, use the paper.
   - Prefer the paper's own figures and examples over repo-only material. Replace repo-only material with the paper's
     equivalent if the paper has one; otherwise keep it, presented plainly.
   - Vekto has no paper: use the repository's approved results; keep modelling assumptions only where a claim depends
     on them, stated as facts, not hedges.
4. Keep the beat mechanism consistent: `.venv/bin/python tools/check_episode.py <ep>` must print OK, and
   `py_compile` must pass. Update the zh text to match the en text (technical terms stay in English). Update
   STORYBOARD.md and SOURCES.md to match.
5. Target length: about 5–7 minutes of narration. Cut the series and hedge material first, then trim repetition. Keep
   the motivated example and the architecture diagram complete.
6. Check every scene you changed with a last-frame still, one at a time:
   `PYTHONPATH=. nice -n 19 .venv/bin/manim -ql -s --media_dir /tmp/<ep>-rev episodes/<ep>/scenes.py <Scene>`.
   Open the PNG and fix layout problems. Never run more than one manim at a time, and do not render full videos.
7. Write only inside episodes/<ep>/. Append a short "Revision 2026-11-23" section to STORYBOARD.md listing what
   changed.

Finish with a ≤150-word summary: scenes, minutes, what was removed or changed.
