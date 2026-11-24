"""Episode 2: TopoVerus (Sun, Yang, Pei. NeurIPS 2026).

Scenes are rendered one by one, e.g.
    PYTHONPATH=. manim -ql episodes/topoverus/scenes.py Topo01Map
On-screen code comes from episodes/topoverus/examples/ (each file's header gives the exact source and trims).
"""
from __future__ import annotations

import os
import re
from contextlib import contextmanager
from pathlib import Path

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UP, ORIGIN, UL, UR, DL, DR,
    Arrow, Circle, Create, FadeIn, FadeOut, GrowArrow, Indicate, LaggedStart, Line,
    ReplacementTransform, SurroundingRectangle, Transform, VGroup, Write,
)

from manim.utils.exceptions import EndSceneEarlyException

from common import style as S
from common.components import (
    NarratedScene, T, badge, bar_chart, bullet_list, card, cite, code_panel, highlight_lines,
    pipeline, series_map, state_table, title_card,
)

EP = "topoverus"
ACC = S.ACCENT[EP]
EX = Path(__file__).resolve().parent / "examples"


# ------------------------------------------------------------------ local helpers
def screen(name: str) -> dict[str, str]:
    """Sections of an examples/ file; a section starts at a line '// ---- <key> ----' or '# ---- <key> ----'.
    Everything before the first marker is the provenance header and is not shown."""
    secs, cur = {}, None
    for line in (EX / name).read_text(encoding="utf-8").splitlines():
        m = re.match(r"^(?://|#) ---- (.+?) ----\s*$", line)
        if m:
            cur = m.group(1)
            secs[cur] = []
            continue
        if cur is not None:
            secs[cur].append(line)
    return {k: "\n".join(v) for k, v in secs.items()}


def screen1(name: str) -> str:
    return next(iter(screen(name).values()))


def heading(text: str, color: str = S.INK) -> "T":
    h = T(text, size=S.HEADING_SIZE - 6, weight="BOLD", color=color)
    h.to_edge(UP, buff=0.45)
    return h


def note(text: str, color: str = S.MUTED, size: float = S.SMALL_SIZE) -> "T":
    return T(text, size=size, color=color)


def aligned_twin(panel, code: str, language: str, **kw):
    """A second code_panel whose code lines sit exactly on top of `panel`'s (for line-by-line Transforms)."""
    twin = code_panel(code, language, **kw)
    twin.code.scale(panel.code.height / twin.code.height)
    twin.shift(panel.code.get_corner(UL) - twin.code.get_corner(UL))
    return twin


def term_box(text: str, title: str, edge=S.BAD, size: float = 14):
    """Terminal-style output card (plain mono lines, no syntax colours) with a small title."""
    body = VGroup(*[T(l if l.strip() else " ", size=size, mono=True) for l in text.splitlines()])
    body.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    head = T(title, size=S.SMALL_SIZE - 2, color=S.MUTED, mono=True)
    inner = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    fr = card(inner.width + 0.4, inner.height + 0.35, edge=edge)
    fr.move_to(inner)
    return VGroup(fr, inner)


def strike(mob, color=S.BAD):
    return Line(mob.get_left() + LEFT * 0.05, mob.get_right() + RIGHT * 0.05, color=color, stroke_width=4)


class TopoScene(NarratedScene):
    """NarratedScene + a preview hook: with TOPO_STOP=<beat id> in the environment, the scene ends right after that
    beat, so `manim -s` saves a still of a mid-scene state. No effect on normal renders."""
    EPISODE = EP

    @contextmanager
    def beat(self, beat_id: str):
        with super().beat(beat_id) as b:
            yield b
        if os.environ.get("TOPO_STOP") == beat_id:
            raise EndSceneEarlyException()


LOOP = screen1("caseB-loop-SCREEN.rs")
FIXED_RANGE = screen1("caseB-repaired-line-SCREEN.rs")
LOOP_FIXED = "\n".join(LOOP.splitlines()[:13] + FIXED_RANGE.splitlines() + LOOP.splitlines()[15:])
# screen line numbers in caseB-loop-SCREEN.rs (1-based)
L_ENSURES = (4, 5)
L_INIT = (8, 9)
L_LOOP = (10, 19)
L_DELETED = 12
L_BUG = (14, 15)



def loop_panel(font_size=17, title="LeetCode 121 · buggy proof (Case B)"):
    return code_panel(LOOP, "rust", title=title, line_numbers=False, font_size=font_size)


# ------------------------------------------------------------------ 1. series map + recap
class Topo01Map(TopoScene):
    def construct(self):
        m = series_map(EP).shift(DOWN * 0.3)
        recap = T("Last time: a concrete counterexample beats a one-line verifier error",
                  size=S.SMALL_SIZE + 4, color=S.INK)
        recap.next_to(m, UP, buff=0.7)
        with self.beat("Topo01Map-1"):
            self.play(FadeIn(m, shift=UP * 0.2), run_time=1.2)
            self.play(FadeIn(recap, shift=DOWN * 0.1), run_time=0.8)
        with self.beat("Topo01Map-2"):
            self.play(FadeOut(m), FadeOut(recap), run_time=0.6)
            tc = title_card(EP, 2, extra="Yuechun Sun, Jun Yang, Kexin Pei · NeurIPS 2026")
            q = T("Can a model learn to produce the counterexample itself?", size=S.BODY_SIZE, color=ACC)
            VGroup(tc, q.next_to(tc, DOWN, buff=0.6)).move_to(ORIGIN)
            self.play(FadeIn(tc, shift=UP * 0.2), run_time=1.0)
            self.play(FadeIn(q), run_time=0.8)


# ------------------------------------------------------------------ 2. hook: Case B fails with a one-line error
class Topo02Hook(TopoScene):
    def construct(self):
        panel = loop_panel(font_size=15).to_corner(UL, buff=0.3)
        err = term_box(screen1("caseB-verifier-error.txt"), "Verus output", size=14)
        err.to_edge(RIGHT, buff=0.2).align_to(panel, UP).shift(DOWN * 0.6)
        c = cite("Case B: repo docs/case-studies/b-prefix-invariant (buggy.rs, verifier-error.txt); TopoVerus Fig. 4 p.9")

        with self.beat("Topo02Hook-1"):
            self.play(FadeIn(panel), FadeIn(c), run_time=1.0)
            box = highlight_lines(panel, *L_ENSURES, color=S.INFO)
            self.play(Create(box), run_time=0.6)
        with self.beat("Topo02Hook-2"):
            loopbox = highlight_lines(panel, *L_LOOP, color=S.MUTED)
            self.play(ReplacementTransform(box, loopbox), run_time=0.7)
            bug = highlight_lines(panel, *L_BUG, color=S.WARN)
            self.play(ReplacementTransform(loopbox, bug), run_time=0.7)
        with self.beat("Topo02Hook-3"):
            self.play(FadeIn(err, shift=UP * 0.2), run_time=0.8)
            bad = highlight_lines(panel, *L_BUG, color=S.BAD)
            arrow = Arrow(err.get_bottom() + LEFT * 1.5, bad.get_right() + RIGHT * 0.05, color=S.BAD,
                          stroke_width=3, buff=0.08, max_tip_length_to_length_ratio=0.12)
            self.play(ReplacementTransform(bug, bad), GrowArrow(arrow), run_time=0.8)
        with self.beat("Topo02Hook-4"):
            qs = VGroup(T("Which state", size=S.BODY_SIZE, color=ACC),
                        T("breaks it? Why?", size=S.BODY_SIZE, color=ACC)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            qs.next_to(err, DOWN, buff=2.2).align_to(err, LEFT).shift(RIGHT * 0.3)
            self.play(FadeIn(qs, shift=UP * 0.1), run_time=0.8)


# ------------------------------------------------------------------ 3. background: invariants and counterexamples
class Topo03Background(TopoScene):
    def construct(self):
        h = heading("Loop invariants and counterexamples")
        g = pipeline(
            [{"id": "pre", "label": "Before the loop", "sub": "invariant must hold", "pos": [-3.0, 1.6],
              "w": 4.2, "color": S.INFO},
             {"id": "body", "label": "Every iteration", "sub": "invariant is preserved", "pos": [3.0, 1.6],
              "w": 4.2, "color": S.INFO}],
            [{"from": "pre", "to": "body"}])
        with self.beat("Topo03Background-1"):
            self.play(FadeIn(h), run_time=0.6)
            self.play(FadeIn(g[0][0], shift=UP * 0.1), run_time=0.6)
            self.play(GrowArrow(g[1][0]), FadeIn(g[0][1], shift=UP * 0.1), run_time=0.8)

        parts = [("[State]", "σ", "where the obligation fails"),
                 ("[Execution Trace]", "τ", "what runs from σ"),
                 ("[Violation]", "ψ", "why, in plain words")]
        cards = VGroup()
        for name, sym, sub in parts:
            r = card(4.15, 1.5, edge=S.BAD)
            lab = VGroup(VGroup(T(name, size=S.BODY_SIZE - 6, weight="BOLD", mono=True),
                                T(sym, size=S.BODY_SIZE, color=S.BAD)).arrange(RIGHT, buff=0.25),
                         T(sub, size=S.SMALL_SIZE, color=S.MUTED)).arrange(DOWN, buff=0.15).move_to(r)
            cards.add(VGroup(r, lab))
        cards.arrange(RIGHT, buff=0.25).shift(DOWN * 1.0)
        cx = T("counterexample", size=S.SMALL_SIZE + 2, color=S.BAD).next_to(cards, UP, buff=0.2)
        c1 = cite("TopoVerus Eq. 1 and §3.1, p.4–5")
        with self.beat("Topo03Background-2"):
            self.play(FadeIn(cx), FadeIn(c1), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(k, shift=UP * 0.15) for k in cards], lag_ratio=0.4), run_time=1.8)

        ex = S.ACCENT["exverus"]
        left = VGroup(T("ExVerus", size=S.BODY_SIZE, weight="BOLD", color=ex),
                      T("search + validate", size=S.SMALL_SIZE + 2, color=S.INK),
                      T("at every repair", size=S.SMALL_SIZE + 2, color=S.MUTED)).arrange(DOWN, buff=0.15)
        right = VGroup(T("TopoVerus", size=S.BODY_SIZE, weight="BOLD", color=ACC),
                       T("learned in training", size=S.SMALL_SIZE + 2, color=S.INK),
                       T("one pass at repair time", size=S.SMALL_SIZE + 2, color=S.MUTED)).arrange(DOWN, buff=0.15)
        lc, rc = card(4.6, 2.0, edge=ex), card(4.6, 2.0, edge=ACC)
        L, R = VGroup(lc, left.move_to(lc)), VGroup(rc, right.move_to(rc))
        VGroup(L, R).arrange(RIGHT, buff=1.4).shift(UP * 0.6)
        arr = Arrow(L.get_right(), R.get_left(), buff=0.1, color=S.MUTED, stroke_width=3)
        c2 = cite("TopoVerus §1 ¶4–5, p.2")
        with self.beat("Topo03Background-3"):
            self.play(FadeOut(g), FadeOut(cards), FadeOut(cx), FadeOut(c1), run_time=0.6)
            self.play(FadeIn(L), FadeIn(c2), run_time=0.7)
            self.play(GrowArrow(arr), FadeIn(R, shift=LEFT * 0.2), run_time=0.9)

        quote = VGroup(T("“a counterexample is useful when conditioning on it", size=S.BODY_SIZE - 2),
                       T("helps the model produce a safe, verifier-passing proof”", size=S.BODY_SIZE - 2)
                       ).arrange(DOWN, buff=0.15)
        qc = card(quote.width + 0.8, quote.height + 0.6, edge=ACC)
        Q = VGroup(qc, quote.move_to(qc)).shift(DOWN * 2.1)
        c3 = cite("TopoVerus, Abstract p.1")
        sub = note("the model's counterexample is not checked by a solver", color=S.WARN, size=S.SMALL_SIZE + 2).next_to(Q, UP, buff=0.2)
        with self.beat("Topo03Background-4"):
            self.play(FadeOut(c2), FadeIn(sub), run_time=0.5)
            self.play(FadeIn(Q, shift=UP * 0.15), FadeIn(c3), run_time=1.0)


# ------------------------------------------------------------------ 4. the one-trajectory output format
class Topo04Format(TopoScene):
    def construct(self):
        h = heading("One response, three sections")
        fmt = code_panel(screen1("appD-output-format.txt"), "text",
                         title="TopoVerus prompt, App. D.1 (verbatim)", line_numbers=False, font_size=20)
        fmt.move_to(UP * 0.4)
        c1 = cite("TopoVerus App. D.1, p.21; App. D p.20")
        with self.beat("Topo04Format-1"):
            self.play(FadeIn(h), run_time=0.6)
            self.play(FadeIn(fmt), FadeIn(c1), run_time=0.9)
        with self.beat("Topo04Format-2"):
            boxes = []
            for ln, col in ((2, S.BAD), (3, S.INFO), (4, ACC)):
                row = fmt.lines[ln - 1]
                b = Line(row.get_corner(DL) + LEFT * 0.15, row.get_corner(UL) + LEFT * 0.15, color=col,
                         stroke_width=8)
                boxes.append(b)
                self.play(Create(b), row.animate.set_color(col), run_time=0.6)
            think = note("(a free <think> block may come first)", size=S.SMALL_SIZE).next_to(fmt, DOWN, buff=0.35)
            self.play(FadeIn(think), run_time=0.5)

        secs = screen("caseB-trajectory-filled-SCREEN.txt")
        p1 = code_panel(secs["panel 1: counterexample"], "text", line_numbers=False, font_size=14, max_width=7.2,
                        title="1 · counterexample")
        p2 = code_panel(secs["panel 2: reasoning"], "text", line_numbers=False, font_size=14, max_width=5.8,
                        title="2 · rationale")
        p3 = code_panel(secs["panel 3: rust"], "text", line_numbers=False, font_size=14, max_width=5.8,
                        title="3 · repaired proof")
        p1[0].set_stroke(S.BAD)
        p2[0].set_stroke(S.INFO)
        p3[0].set_stroke(ACC)
        right = VGroup(p2, p3).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        VGroup(p1, right).arrange(RIGHT, buff=0.5, aligned_edge=UP).move_to(DOWN * 0.25)
        a1 = Arrow([p1.get_right()[0], p2.get_center()[1], 0], p2.get_left(), buff=0.05, color=S.MUTED,
                   stroke_width=3)
        a2 = Arrow(p2.get_bottom(), p3.get_top(), buff=0.08, color=S.MUTED, stroke_width=3)
        sub = note("recorded TopoVerus output for Case B (released case study)", size=S.SMALL_SIZE)
        sub.to_edge(UP, buff=0.4)
        c2 = cite("repo: docs/case-studies/b-prefix-invariant/model-output.txt (trimmed; see SOURCES.md)")
        with self.beat("Topo04Format-3"):
            self.play(*[FadeOut(m) for m in (h, fmt, c1, think, *boxes)], run_time=0.6)
            self.play(FadeIn(sub), FadeIn(p1, shift=RIGHT * 0.2), FadeIn(c2), run_time=0.9)
            self.play(GrowArrow(a1), FadeIn(p2, shift=RIGHT * 0.2), run_time=0.7)
            self.play(GrowArrow(a2), FadeIn(p3, shift=DOWN * 0.2), run_time=0.7)


# ------------------------------------------------------------------ 5. the counterexample, next to the code
class Topo05Counterexample(TopoScene):
    def construct(self):
        panel = loop_panel(font_size=15).to_corner(UL, buff=0.3)
        colx = (panel.get_right()[0] + 7.0) / 2
        st = state_table([("prices", "[5, 3, 7]"), ("i", "0"), ("max_pro", "0"), ("min_price", "i32::MAX")],
                         title="[State] before the loop", size=S.SMALL_SIZE)
        st[0].set_stroke(S.BAD)
        st.move_to([colx, 0, 0]).to_edge(UP, buff=0.3)
        c = cite("Counterexample: repo docs/case-studies/b-prefix-invariant/model-output.txt:2-17; TopoVerus Fig. 4 p.9")
        with self.beat("Topo05Counterexample-1"):
            self.play(FadeIn(panel), FadeIn(c), run_time=0.8)
            init = highlight_lines(panel, *L_INIT, color=S.INFO)
            self.play(FadeIn(st, shift=LEFT * 0.2), Create(init), run_time=0.9)

        # the array with j and k pointers
        cells = VGroup()
        for v in (5, 3, 7):
            sq = card(0.7, 0.7)
            cells.add(VGroup(sq, T(str(v), size=S.BODY_SIZE - 2, mono=True).move_to(sq)))
        cells.arrange(RIGHT, buff=0.08)
        idx = VGroup(*[T(str(i), size=S.SMALL_SIZE - 4, color=S.MUTED, mono=True).next_to(cells[i], UP, buff=0.06)
                       for i in range(3)])
        jl = T("j", size=S.SMALL_SIZE, color=S.BAD, mono=True).next_to(cells[0], DOWN, buff=0.1)
        kl = T("k", size=S.SMALL_SIZE, color=S.BAD, mono=True).next_to(cells[2], DOWN, buff=0.1)
        arr = VGroup(cells, idx, jl, kl)
        arr.next_to(st, DOWN, buff=0.3).set_x(colx)
        trace = VGroup(T("prices[2] - prices[0]", size=S.SMALL_SIZE, mono=True),
                       T("= 7 - 5 = 2", size=S.SMALL_SIZE, mono=True)).arrange(DOWN, buff=0.1)
        trace.next_to(arr, DOWN, buff=0.25).set_x(colx)
        with self.beat("Topo05Counterexample-2"):
            bug = highlight_lines(panel, *L_BUG, color=S.WARN)
            self.play(ReplacementTransform(init, bug), FadeIn(cells), FadeIn(idx), run_time=0.9)
            self.play(FadeIn(jl, shift=UP * 0.1), FadeIn(kl, shift=UP * 0.1),
                      cells[0][0].animate.set_stroke(S.BAD), cells[2][0].animate.set_stroke(S.BAD), run_time=0.7)
            self.play(FadeIn(trace), run_time=0.8)

        viol = T("2 <= max_pro = 0 : false", size=S.SMALL_SIZE + 2, color=S.BAD, mono=True)
        viol.next_to(trace, DOWN, buff=0.3).set_x(colx)
        why = VGroup(note("range = the whole array,", size=S.SMALL_SIZE - 2),
                     note("but nothing is processed yet", size=S.SMALL_SIZE - 2)).arrange(DOWN, buff=0.08)
        why.next_to(viol, DOWN, buff=0.2).set_x(colx)
        with self.beat("Topo05Counterexample-3"):
            bad = highlight_lines(panel, *L_BUG, color=S.BAD)
            self.play(FadeIn(viol, shift=UP * 0.1), ReplacementTransform(bug, bad), run_time=0.8)
            self.play(FadeIn(why), run_time=0.6)
        with self.beat("Topo05Counterexample-4"):
            cause = VGroup(T("cause: quantifier range", size=S.SMALL_SIZE + 2, color=ACC, weight="BOLD"),
                           T("is too wide", size=S.SMALL_SIZE + 2, color=ACC, weight="BOLD")).arrange(DOWN, buff=0.08)
            cause.move_to(why)
            self.play(ReplacementTransform(why, cause), Indicate(bad, color=S.BAD), run_time=1.0)


# ------------------------------------------------------------------ 6. rationale and repaired line; honest status
class Topo06Repair(TopoScene):
    def construct(self):
        panel = loop_panel(font_size=15, title="max_profit · recorded repair (Case B)").to_corner(UL, buff=0.3)
        colx = (panel.get_right()[0] + 7.0) / 2
        bad = highlight_lines(panel, *L_BUG, color=S.BAD)
        rat = VGroup(T("rationale (recorded, item 2)", size=S.SMALL_SIZE - 2, color=S.INFO),
                     T("Change the invariant to", size=S.SMALL_SIZE - 2, mono=True),
                     T("forall|j: int, k: int|", size=S.SMALL_SIZE - 2, mono=True, color=ACC),
                     T("0 <= j < k < i ==> ...", size=S.SMALL_SIZE - 2, mono=True, color=ACC),
                     T("... At i=0, this is", size=S.SMALL_SIZE - 2, mono=True),
                     T("vacuously true ...", size=S.SMALL_SIZE - 2, mono=True)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        rc = card(rat.width + 0.5, rat.height + 0.45, edge=S.INFO)
        R = VGroup(rc, rat.move_to(rc))
        R.move_to([colx, 0, 0]).to_edge(UP, buff=0.3)
        c = cite("repo: docs/case-studies/b-prefix-invariant/model-output.txt:23, 29, 73; TopoVerus Fig. 4 p.9")
        with self.beat("Topo06Repair-1"):
            self.play(FadeIn(panel), FadeIn(bad), FadeIn(c), run_time=0.8)
            self.play(FadeIn(R, shift=LEFT * 0.2), run_time=1.0)

        twin = aligned_twin(panel, LOOP_FIXED, "rust", title="x", line_numbers=False, font_size=15)
        new_line = twin.lines[L_BUG[0] - 1]
        with self.beat("Topo06Repair-2"):
            self.play(Transform(panel.lines[L_BUG[0] - 1], new_line), run_time=1.2)
            fixed = SurroundingRectangle(VGroup(*panel.lines[L_BUG[0] - 1:L_BUG[1]]), color=ACC, buff=0.06,
                                         stroke_width=3, corner_radius=0.05)
            self.play(ReplacementTransform(bad, fixed), run_time=0.6)

        dl = panel.lines[L_DELETED - 1]
        st = strike(dl)
        dnote = VGroup(note("also deleted in", color=S.BAD, size=S.SMALL_SIZE),
                       note("the recorded output", color=S.BAD, size=S.SMALL_SIZE)).arrange(DOWN, buff=0.06)
        dnote.next_to(R, DOWN, buff=0.5).set_x(colx)
        darr = Arrow(dnote.get_left(), dl.get_right() + RIGHT * 0.1, buff=0.1, color=S.BAD, stroke_width=3,
                     max_tip_length_to_length_ratio=0.12)
        with self.beat("Topo06Repair-3"):
            self.play(Create(st), dl.animate.set_opacity(0.35), run_time=0.8)
            self.play(FadeIn(dnote), GrowArrow(darr), run_time=0.7)

        status = VGroup(badge("Verus on this repaired program: not reported", S.WARN),
                        note("The paper reports the counterexample and the repair target. We could not run Verus.",
                             size=S.SMALL_SIZE - 2)
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        status.next_to(panel, DOWN, buff=0.25).align_to(panel, LEFT)
        with self.beat("Topo06Repair-4"):
            self.play(FadeIn(status[0], shift=UP * 0.1), run_time=0.7)
            self.play(FadeIn(status[1]), run_time=0.7)


# ------------------------------------------------------------------ 7. training pipeline
class Topo07Pipeline(TopoScene):
    def construct(self):
        g = pipeline(
            [{"id": "base", "label": "QwQ-32B", "sub": "base model", "pos": [-5.3, 2.4], "w": 2.4, "h": 1.05,
              "color": S.MUTED},
             {"id": "sft", "label": "Counterexample SFT", "sub": "teacher writes the diagnosis", "pos": [-1.5, 2.4],
              "w": 3.6, "h": 1.05, "color": S.BAD},
             {"id": "grpo", "label": "GRPO", "sub": "8 responses per prompt", "pos": [3.0, 2.4], "w": 3.2,
              "h": 1.05, "color": S.INFO},
             {"id": "gate", "label": "Safety gate", "sub": "only proof annotations changed?", "pos": [3.0, 0.55],
              "w": 3.6, "h": 1.05, "color": S.WARN},
             {"id": "verus", "label": "Verus", "sub": "R_pass", "pos": [3.0, -1.3], "w": 3.2, "h": 1.05,
              "color": S.INFO},
             {"id": "graph", "label": "Topological Graph Reward", "sub": "R_dep: which invariants, in what order",
              "pos": [-2.2, 0.55], "w": 4.4, "h": 1.05, "color": ACC},
             {"id": "reward", "label": "Reward (Eq. 2)", "sub": "drives the GRPO update", "pos": [-2.2, -1.3],
              "w": 4.4, "h": 1.05, "color": S.INK}],
            [{"from": "base", "to": "sft"}, {"from": "sft", "to": "grpo"}, {"from": "grpo", "to": "gate"},
             {"from": "gate", "to": "verus"}, {"from": "verus", "to": "reward"}, {"from": "graph", "to": "reward"},
             {"from": "grpo", "to": "graph"}])
        B, E = g.by_id, g.edge_by_id
        c = cite("TopoVerus §3.2 p.5; §4.1 p.6–7 (461 trajectories, 249 programs, 8 rollouts); Eq. 2 p.5")
        with self.beat("Topo07Pipeline-1"):
            self.play(FadeIn(B["base"], shift=UP * 0.1), FadeIn(c), run_time=0.8)
        data = note("teacher: Sonnet 4.6 · 461 trajectories from 249 programs", size=S.SMALL_SIZE)
        data.next_to(B["sft"], UP, buff=0.18).shift(RIGHT * 0.6)
        with self.beat("Topo07Pipeline-2"):
            self.play(GrowArrow(E[("base", "sft")]), FadeIn(B["sft"], shift=RIGHT * 0.1), run_time=0.9)
            self.play(FadeIn(data), run_time=0.6)
        with self.beat("Topo07Pipeline-3"):
            self.play(GrowArrow(E[("sft", "grpo")]), FadeIn(B["grpo"], shift=RIGHT * 0.1), run_time=0.9)
            self.play(FadeIn(B["verus"]), run_time=0.6)
        unsafe = note("unsafe → reward 0", color=S.BAD, size=S.SMALL_SIZE + 2)
        unsafe.next_to(B["gate"], RIGHT, buff=0.15)
        if unsafe.get_right()[0] > 6.95:
            unsafe.next_to(B["gate"], DOWN, buff=0.08).shift(RIGHT * 2.2)
        with self.beat("Topo07Pipeline-4"):
            self.play(GrowArrow(E[("grpo", "gate")]), FadeIn(B["gate"]), run_time=0.8)
            self.play(GrowArrow(E[("gate", "verus")]), FadeIn(unsafe), run_time=0.7)
        eq = T("R = S_safe · [ G_format · ( R_pass + λ_dep · R_dep ) + λ_format · R_format ]",
               size=S.SMALL_SIZE, mono=True)
        eq.scale_to_fit_width(min(eq.width, 12.8)).move_to(DOWN * 2.75)
        with self.beat("Topo07Pipeline-5"):
            self.play(FadeIn(B["reward"]), GrowArrow(E[("verus", "reward")]), run_time=0.7)
            self.play(GrowArrow(E[("grpo", "graph")]), FadeIn(B["graph"], shift=DOWN * 0.1), run_time=0.8)
            self.play(GrowArrow(E[("graph", "reward")]), FadeIn(eq), run_time=0.8)
            self.play(B["graph"][0].animate.set_stroke(width=6), run_time=0.4)


# ------------------------------------------------------------------ 8. why order matters (binary search, Fig. 1-2)
class Topo08Order(TopoScene):
    def construct(self):
        tag = badge("illustrative example from the paper", S.INFO).to_edge(UP, buff=0.35)
        inv = code_panel(screen1("binary-search-invariants-SCREEN.rs"), "rust",
                         title="binary-search insertion: loop invariants", line_numbers=False, font_size=20)
        inv.next_to(tag, DOWN, buff=0.3)
        c = cite("TopoVerus Fig. 1 p.3, Fig. 2 and text p.4 (illustrative)")
        with self.beat("Topo08Order-1"):
            self.play(FadeIn(tag), FadeIn(c), run_time=0.6)
            self.play(FadeIn(inv), run_time=0.9)
        with self.beat("Topo08Order-2"):
            b = highlight_lines(inv, 1, color=S.INFO)
            self.play(Create(b), run_time=0.6)
            b2 = highlight_lines(inv, 2, 3, color=S.INFO)
            self.play(ReplacementTransform(b, b2), run_time=0.7)
            b3 = highlight_lines(inv, 4, 5, color=ACC)
            self.play(ReplacementTransform(b2, b3), run_time=0.7)

        first3 = VGroup(*inv.lines[0:3])
        miss = note("missing", color=S.BAD, size=S.SMALL_SIZE + 2).next_to(first3, RIGHT, buff=0.6)
        under = VGroup(T("Under-constrained counterexample (Fig. 2, top)", size=S.SMALL_SIZE + 2, color=S.BAD,
                         weight="BOLD"),
                       note("state high = 2, yet it checks i = 1", size=S.SMALL_SIZE + 2, color=S.INK),
                       note("mid = 0: a hallucinated value", size=S.SMALL_SIZE + 2, color=S.INK)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        uc = card(under.width + 0.6, under.height + 0.5, edge=S.BAD)
        U = VGroup(uc, under.move_to(uc)).next_to(inv, DOWN, buff=0.45)
        with self.beat("Topo08Order-3"):
            self.play(first3.animate.set_opacity(0.2), FadeIn(miss), FadeOut(b3), run_time=0.8)
            self.play(FadeIn(U, shift=UP * 0.15), run_time=0.8)

        st = state_table([("nums", "[1, 3, 5]"), ("target", "5"), ("high", "2"), ("low after 1 step", "2")],
                         title="Constrained (Fig. 2, bottom)")
        st[0].set_stroke(S.BAD)
        check = VGroup(T("I5 at i = 2:", size=S.SMALL_SIZE + 2, color=S.MUTED),
                       T("nums[2] > 5 ?", size=S.SMALL_SIZE + 4, mono=True),
                       T("nums[2] = 5   false", size=S.SMALL_SIZE + 4, mono=True, color=S.BAD)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        low = VGroup(st, check).arrange(RIGHT, buff=0.9).next_to(inv, DOWN, buff=0.4)
        with self.beat("Topo08Order-4"):
            self.play(FadeOut(U), FadeOut(miss), first3.animate.set_opacity(1), run_time=0.6)
            b5 = highlight_lines(inv, 5, color=S.BAD)
            self.play(FadeIn(st, shift=UP * 0.1), Create(b5), run_time=0.9)
            self.play(FadeIn(check[0:2]), run_time=0.6)
            self.play(FadeIn(check[2]), run_time=0.5)

        fixed = aligned_twin(inv, screen1("binary-search-invariants-SCREEN.rs").rsplit("\n", 1)[0] + "\n"
                             + screen1("binary-search-I5-fixed-SCREEN.rs"), "rust",
                             title="binary-search insertion: loop invariants", line_numbers=False, font_size=20)
        rep = T("high <= i  →  high < i", size=S.SMALL_SIZE + 4, mono=True, color=ACC)
        rep.next_to(check, DOWN, buff=0.4).align_to(check, LEFT)
        with self.beat("Topo08Order-5"):
            self.play(Transform(inv.lines[4], fixed.lines[4]), run_time=1.0)
            self.play(b5.animate.set_color(ACC), FadeIn(rep), run_time=0.6)


# ------------------------------------------------------------------ 9. topological graph reward
class Topo09GraphReward(TopoScene):
    def construct(self):
        h = heading("Topological Graph Reward  R_dep", color=ACC)
        pos = {"I1": [0, 1.5], "I2": [-1.3, 0.1], "I3": [1.3, 0.1], "I4": [-1.3, -1.4], "I5": [1.3, -1.4]}
        nodes = {}
        for k, p in pos.items():
            circ = Circle(radius=0.42, stroke_color=ACC, stroke_width=3, fill_color=S.PANEL, fill_opacity=1)
            nodes[k] = VGroup(circ, T(k, size=S.BODY_SIZE - 2, weight="BOLD", mono=True)).move_to([p[0], p[1], 0])
        edges = [("I1", "I2"), ("I1", "I3"), ("I2", "I4"), ("I3", "I4"), ("I2", "I5"), ("I3", "I5")]
        arrows = {}
        for a, b in edges:
            pa, pb = nodes[a].get_center(), nodes[b].get_center()
            d = (pb - pa) / np.linalg.norm(pb - pa)
            ln = np.linalg.norm(pb - pa) - 0.84
            arrows[(a, b)] = Arrow(pa + d * 0.42, pb - d * 0.42, buff=0.02, color=S.MUTED, stroke_width=3,
                                   max_tip_length_to_length_ratio=0.2 / ln)
        graph = VGroup(*arrows.values(), *nodes.values())
        graph.move_to(LEFT * 4.1 + DOWN * 0.2)
        reading = VGroup(note("edges: our reading of Fig. 2", color=S.WARN),
                         note("(illustrative example from the paper)", size=S.SMALL_SIZE - 2)
                         ).arrange(DOWN, buff=0.08).next_to(graph, DOWN, buff=0.35)
        expl = VGroup(note("edge a → b:", size=S.SMALL_SIZE, color=S.INK),
                      note("a must hold before b can be proven", size=S.SMALL_SIZE)).arrange(DOWN, buff=0.06)
        expl.next_to(graph, UP, buff=0.25)
        c = cite("TopoVerus Defs. 1–3 p.5–6; Eq. 6 p.6; graph not given at evaluation, §4.1 p.6")
        with self.beat("Topo09GraphReward-1"):
            self.play(FadeIn(h), FadeIn(c), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(n) for n in nodes.values()], lag_ratio=0.2), run_time=1.2)
            self.play(GrowArrow(arrows[("I1", "I2")]), FadeIn(expl), run_time=0.8)
        with self.beat("Topo09GraphReward-2"):
            self.play(LaggedStart(*[GrowArrow(arrows[e]) for e in edges[1:]], lag_ratio=0.25), run_time=1.6)
            self.play(FadeIn(reading), run_time=0.5)

        f = VGroup(T("R_dep = α × β", size=S.BODY_SIZE + 2, mono=True, weight="BOLD"),
                   VGroup(T("α", size=S.BODY_SIZE, color=ACC, mono=True),
                          note("coverage: reference invariants written / all", color=S.INK)).arrange(RIGHT, buff=0.25),
                   VGroup(T("β", size=S.BODY_SIZE, color=ACC, mono=True),
                          note("edge satisfaction: edges in order / edges", color=S.INK)).arrange(RIGHT, buff=0.25)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        f.move_to(RIGHT * 2.9 + UP * 1.9)
        with self.beat("Topo09GraphReward-3"):
            self.play(FadeIn(f[0]), run_time=0.7)
            self.play(FadeIn(f[1], shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(f[2], shift=UP * 0.1), run_time=0.6)

        rows = [("I1 I2 I3 I4 I5", "6/6", "1.0"), ("I4 I5 I1 I2 I3", "2/6", "0.33"), ("I5 I4 I3 I2 I1", "0/6", "0")]
        tbl = VGroup(VGroup(note("model writes", size=S.SMALL_SIZE), note("β", size=S.SMALL_SIZE),
                            note("R_dep", size=S.SMALL_SIZE)))
        for o, b, r in rows:
            tbl.add(VGroup(T(o, size=S.SMALL_SIZE + 2, mono=True), T(b, size=S.SMALL_SIZE + 2, mono=True),
                           T(r, size=S.SMALL_SIZE + 2, mono=True, color=ACC)))
        for row in tbl:
            row[1].shift(RIGHT * 0)
        # column layout
        xs = [0, 3.0, 4.3]
        for i, row in enumerate(tbl):
            for j, cell in enumerate(row):
                cell.move_to([xs[j], -i * 0.55, 0], aligned_edge=LEFT)
        tbl.next_to(f, DOWN, buff=0.45).align_to(f, LEFT)
        own = note("our computation (illustrative edge set, all α = 1)", color=S.WARN, size=S.SMALL_SIZE - 2)
        own.next_to(tbl, DOWN, buff=0.2).align_to(tbl, LEFT)
        with self.beat("Topo09GraphReward-4"):
            self.play(FadeIn(tbl[0]), FadeIn(own), run_time=0.6)
            for row in tbl[1:]:
                self.play(FadeIn(row, shift=UP * 0.1), run_time=0.6)
        tr = badge("training-time signal only", S.WARN)
        tr.next_to(own, DOWN, buff=0.3).align_to(tbl, LEFT)
        tr2 = note("evaluation: no reference proof, no graph", size=S.SMALL_SIZE).next_to(tr, DOWN, buff=0.15)
        tr2.align_to(tr, LEFT)
        with self.beat("Topo09GraphReward-5"):
            self.play(FadeIn(tr), FadeIn(tr2), run_time=0.8)


# ------------------------------------------------------------------ 10. safety gate
class Topo10Safety(TopoScene):
    def construct(self):
        secs = screen("safety-gate-S3-SCREEN.rs")
        tag = badge("test case from the released code", S.INFO).to_edge(UP, buff=0.35)
        orig = code_panel(secs["screen text below: original"], "rust", title="original", line_numbers=False,
                          font_size=19)
        orig.next_to(tag, DOWN, buff=0.35)
        c = cite("repo: tests/test_trust.py:138-149 · outcomes are the test's assertions; we did not run it")
        with self.beat("Topo10Safety-1"):
            self.play(FadeIn(tag), FadeIn(c), run_time=0.6)
            self.play(FadeIn(orig), run_time=0.9)
        fail = badge("Verus: verification failed", S.BAD)
        x2 = note("x = 2 → y = 1, but ensures r > 1", size=S.SMALL_SIZE)
        row1 = VGroup(fail, x2).arrange(RIGHT, buff=0.4).next_to(orig, DOWN, buff=0.25)
        with self.beat("Topo10Safety-2"):
            b = highlight_lines(orig, 1, color=S.INFO)
            self.play(Create(b), run_time=0.6)
            b2 = highlight_lines(orig, 2, color=S.WARN)
            self.play(ReplacementTransform(b, b2), run_time=0.6)
            self.play(FadeIn(x2), run_time=0.5)
            self.play(FadeIn(fail), run_time=0.5)

        cand = code_panel(secs["screen text below: original"], "rust", title="\"repair\": move the existing assume",
                          line_numbers=False, font_size=19)
        cand.next_to(row1, DOWN, buff=0.4)
        cand_fixed = aligned_twin(cand, secs["screen text below: candidate"], "rust",
                                  title="\"repair\": move the existing assume", line_numbers=False, font_size=19)
        ver = badge("Verus: verified", S.OK)
        ver.next_to(cand, DOWN, buff=0.25).align_to(row1, LEFT)
        with self.beat("Topo10Safety-3"):
            self.play(FadeOut(b2), FadeIn(cand, shift=UP * 0.1), run_time=0.8)
            self.play(Transform(cand.lines[1], cand_fixed.lines[1]), run_time=1.0)
            self.play(Create(highlight_lines(cand, 2, color=S.WARN)), FadeIn(ver), run_time=0.7)
        gate = badge("safety gate: unsafe → reward 0", S.BAD)
        gate.next_to(ver, RIGHT, buff=0.4)
        with self.beat("Topo10Safety-4"):
            self.play(FadeIn(gate, shift=LEFT * 0.1), run_time=0.8)
            self.play(Indicate(gate, color=S.BAD), run_time=0.8)


# ------------------------------------------------------------------ 11. results
class Topo11Results(TopoScene):
    def construct(self):
        h = heading("Safe-Pass on 471 problems, 7 Verus benchmarks")
        def chart(items, title):
            ch = bar_chart(items, highlight="TopoVerus", accent=ACC, width=3.6, max_value=100)
            t = T(title, size=S.BODY_SIZE - 2, weight="BOLD")
            return VGroup(t, ch).arrange(DOWN, buff=0.4)
        k1 = chart([("TopoVerus", 61.6), ("Sonnet-4.5", 55.9)], "Safe-Pass@1")
        k3 = chart([("TopoVerus", 72.2), ("Sonnet-4.5", 65.9)], "Safe-Pass@3")
        VGroup(k1, k3).arrange(RIGHT, buff=1.2).shift(UP * 0.5)
        c1 = cite("TopoVerus Table 1 p.7 and Table 4 p.18 (weighted = micro-average); §4.2 p.7")
        with self.beat("Topo11Results-1"):
            self.play(FadeIn(h), FadeIn(c1), run_time=0.6)
            self.play(FadeIn(k1, shift=UP * 0.1), FadeIn(k3, shift=UP * 0.1), run_time=1.2)
        d1 = T("+5.7", size=S.BODY_SIZE, color=ACC, weight="BOLD").next_to(k1, DOWN, buff=0.35)
        d3 = T("+6.3", size=S.BODY_SIZE, color=ACC, weight="BOLD").next_to(k3, DOWN, buff=0.35)
        setting = VGroup(note("baselines: iterative repair with verifier feedback"),
                         note("TopoVerus: 3 chains × 10 iterations")).arrange(DOWN, buff=0.1)
        setting.next_to(VGroup(d1, d3), DOWN, buff=0.45)
        with self.beat("Topo11Results-2"):
            self.play(FadeIn(d1), FadeIn(d3), run_time=0.7)
            self.play(FadeIn(setting), run_time=0.7)

        h2 = heading("Ablations (weighted Safe-Pass@1)")
        lad = bar_chart([("CoT-Init", 39.3), ("CTX-Init", 50.5), ("CTX-Binary", 53.7), ("CTX-Dep = TopoVerus", 61.6)],
                        highlight="CTX-Dep = TopoVerus", accent=ACC, width=4.6, max_value=100)
        lad.move_to(UP * 0.4).to_edge(LEFT, buff=0.6)
        xr = max(r.get_right()[0] for r in lad) + 0.35

        def bracket(r0, r1, big, small):
            y0, y1 = lad[r0].get_center()[1], lad[r1].get_center()[1]
            br = VGroup(Line([xr, y0, 0], [xr + 0.2, y0, 0]), Line([xr + 0.2, y0, 0], [xr + 0.2, y1, 0]),
                        Line([xr + 0.2, y1, 0], [xr, y1, 0])).set_stroke(ACC, 3)
            lab = VGroup(T(big, size=S.BODY_SIZE - 2, color=ACC, weight="BOLD"),
                         note(small, size=S.SMALL_SIZE)).arrange(RIGHT, buff=0.2)
            lab.next_to(br, RIGHT, buff=0.2)
            return VGroup(br, lab)

        a1 = bracket(0, 1, "+11.2", "counterexample format")
        a2 = bracket(2, 3, "+7.9", "graph reward vs pass/fail RL")
        c2 = cite("TopoVerus Table 1 and §4.2–4.3 p.7; Table 4 p.18")
        with self.beat("Topo11Results-3"):
            self.play(*[FadeOut(m) for m in (h, k1, k3, d1, d3, setting, c1)], run_time=0.6)
            self.play(FadeIn(h2), FadeIn(lad[0]), FadeIn(lad[1]), FadeIn(c2), run_time=0.8)
            self.play(FadeIn(a1), run_time=0.6)
            self.play(FadeIn(lad[2]), FadeIn(lad[3]), run_time=0.8)
            self.play(FadeIn(a2), run_time=0.6)

        h3 = heading("Does it write invariants in dependency order?")
        beta = bar_chart([("CTX-Binary", 43.8), ("CTX-Dep", 95.8)], highlight="CTX-Dep", accent=ACC, width=6.0,
                         max_value=100)
        bt = T("edge satisfaction β", size=S.BODY_SIZE - 2, weight="BOLD")
        B = VGroup(bt, beta).arrange(DOWN, buff=0.4).shift(UP * 0.3)
        cov = note("coverage α: CTX-Binary 98.6%, CTX-Dep 98.5% (almost unchanged)", size=S.SMALL_SIZE + 2).next_to(B, DOWN, buff=0.6)
        c3 = cite("TopoVerus Table 7 p.20 (24 paired tasks accepted by Verus; post-hoc analysis)")
        with self.beat("Topo11Results-4"):
            self.play(*[FadeOut(m) for m in (h2, lad, a1, a2, c2)], run_time=0.6)
            self.play(FadeIn(h3), FadeIn(B), FadeIn(c3), run_time=1.0)
            self.play(FadeIn(cov), run_time=0.6)


# ------------------------------------------------------------------ 12. limitations, bridge, series map
class Topo12Close(TopoScene):
    def construct(self):
        h = heading("What TopoVerus does not claim")
        items = ["Curriculum targets loop invariants only",
                 "Counterexamples are not formally checked",
                 "Systems code (VeruSAGE), Safe-Pass@1: Sonnet-4.5 75.5% vs TopoVerus 30.2%"]
        bl = bullet_list(items, size=S.BODY_SIZE - 2).move_to(UP * 0.2)
        if bl.width > 12.6:
            bl.scale_to_fit_width(12.6)
        c1 = cite("TopoVerus §6 Limitations p.10; Table 1 p.7")
        with self.beat("Topo12Close-1"):
            self.play(FadeIn(h), FadeIn(c1), run_time=0.6)
            self.play(FadeIn(bl[0], shift=RIGHT * 0.1), run_time=0.7)
        with self.beat("Topo12Close-2"):
            self.play(FadeIn(bl[1], shift=RIGHT * 0.1), run_time=0.7)
        with self.beat("Topo12Close-3"):
            self.play(FadeIn(bl[2], shift=RIGHT * 0.1), run_time=0.7)

        m = series_map("vero").shift(DOWN * 0.3)
        q = T("Next: can agents build verified repositories?", size=S.BODY_SIZE - 2, color=S.ACCENT["vero"])
        q.next_to(m, UP, buff=0.7)
        with self.beat("Topo12Close-4"):
            self.play(FadeOut(h), FadeOut(bl), FadeOut(c1), run_time=0.6)
            self.play(FadeIn(m, shift=UP * 0.2), run_time=1.2)
            self.play(FadeIn(q), run_time=0.8)
