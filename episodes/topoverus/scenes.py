"""TopoVerus (Sun, Yang, Pei. NeurIPS 2026).

Scenes are rendered one by one, e.g.
    PYTHONPATH=. manim -ql episodes/topoverus/scenes.py Topo01Title
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
    Arrow, Circle, Create, DashedVMobject, RoundedRectangle, FadeIn, FadeOut, GrowArrow, Indicate, LaggedStart, Line,
    ReplacementTransform, SurroundingRectangle, Transform, VGroup, Write,
)

from manim.utils.exceptions import EndSceneEarlyException

from common import style as S
from common.components import (
    NarratedScene, T, badge, bar_chart, bullet_list, card, cite, code_panel, highlight_lines,
    pipeline, state_table, title_card,
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


LOOP = screen1("caseB-fig4-code-SCREEN.rs")
FIXED_RANGE = screen1("caseB-fig4-repair-target-SCREEN.rs")
# screen line numbers in caseB-fig4-code-SCREEN.rs (1-based)
L_ENSURES = (4, 5)
L_INIT = (7, 8)
L_LOOP = (9, 18)
L_BUG = (12, 14)
L_RANGE = 13
LOOP_FIXED = "\n".join(LOOP.splitlines()[:L_RANGE - 1] + FIXED_RANGE.splitlines() + LOOP.splitlines()[L_RANGE:])


def loop_panel(font_size=17, title="LeetCode 121 · max_profit"):
    return code_panel(LOOP, "rust", title=title, line_numbers=False, font_size=font_size)


# ------------------------------------------------------------------ 1. title card and question
class Topo01Title(TopoScene):
    def construct(self):
        tc = title_card(EP, extra="Yuechun Sun, Jun Yang, Kexin Pei · NeurIPS 2026")
        q = T("Can a model learn to write the counterexample itself?", size=S.BODY_SIZE, color=ACC)
        VGroup(tc, q.next_to(tc, DOWN, buff=0.6)).move_to(ORIGIN)
        with self.beat("Topo01Title-1"):
            self.play(FadeIn(tc, shift=UP * 0.2), run_time=1.2)
            self.play(FadeIn(q), run_time=0.8)


# ------------------------------------------------------------------ 2. hook: Case B fails with a one-line error
class Topo02Hook(TopoScene):
    def construct(self):
        panel = loop_panel(font_size=15).to_corner(UL, buff=0.3)
        err = term_box(screen1("caseB-fig4-verus-error.txt"), "Verus error", size=14)
        err.to_edge(RIGHT, buff=0.2).align_to(panel, UP).shift(DOWN * 0.6)
        c = cite("TopoVerus Fig. 4, p.9 (Case Study B, App. B p.17)")

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

        one = VGroup(T("TopoVerus", size=S.BODY_SIZE, weight="BOLD", color=ACC),
                     T("counterexample, rationale and repair in one pass", size=S.BODY_SIZE - 4, color=S.INK)
                     ).arrange(DOWN, buff=0.2).shift(UP * 1.2)
        quote = VGroup(T("“a counterexample is useful when conditioning on it", size=S.BODY_SIZE - 2),
                       T("helps the model produce a safe, verifier-passing proof”", size=S.BODY_SIZE - 2)
                       ).arrange(DOWN, buff=0.15)
        qc = card(quote.width + 0.8, quote.height + 0.6, edge=ACC)
        Q = VGroup(qc, quote.move_to(qc)).shift(DOWN * 1.0)
        c3 = cite("TopoVerus, Abstract p.1")
        with self.beat("Topo03Background-3"):
            self.play(FadeOut(g), FadeOut(cards), FadeOut(cx), FadeOut(c1), run_time=0.6)
            self.play(FadeIn(one, shift=UP * 0.1), FadeIn(c3), run_time=0.9)
            self.play(FadeIn(Q, shift=UP * 0.15), run_time=1.0)


# ------------------------------------------------------------------ 4. the one-trajectory output format
class Topo04Format(TopoScene):
    def construct(self):
        h = heading("One response, three sections")
        fmt = code_panel(screen1("appD-output-format.txt"), "text",
                         title="TopoVerus prompt, App. D.1", line_numbers=False, font_size=20)
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
            think = note("(preceded by a <think> block)", size=S.SMALL_SIZE).next_to(fmt, DOWN, buff=0.35)
            self.play(FadeIn(think), run_time=0.5)

        secs = screen("caseB-fig4-counterexample-SCREEN.txt")
        cx = code_panel(secs["counterexample"], "text", line_numbers=False, font_size=16, max_width=12.0,
                        title="TopoVerus counterexample · max_profit")
        cx[0].set_stroke(S.BAD)
        tgt = VGroup(*[T(l, size=S.SMALL_SIZE, color=ACC) for l in secs["repair target"].splitlines()]
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        VGroup(cx, tgt).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(DOWN * 0.1)
        c2 = cite("TopoVerus Fig. 4, p.9 (Case Study B, App. B p.17)")
        with self.beat("Topo04Format-3"):
            self.play(*[FadeOut(m) for m in (h, fmt, c1, think, *boxes)], run_time=0.6)
            self.play(FadeIn(cx, shift=UP * 0.2), FadeIn(c2), run_time=1.0)
            self.play(FadeIn(tgt), run_time=0.7)


# ------------------------------------------------------------------ 5. the counterexample, next to the code
class Topo05Counterexample(TopoScene):
    def construct(self):
        panel = loop_panel(font_size=15).to_corner(UL, buff=0.3)
        colx = (panel.get_right()[0] + 7.0) / 2
        st = state_table([("price", "[5, 3, 7]"), ("i", "0"), ("max_pro", "0"), ("min_price", "i32::MAX")],
                         title="[State] before the loop", size=S.SMALL_SIZE)
        st[0].set_stroke(S.BAD)
        st.move_to([colx, 0, 0]).to_edge(UP, buff=0.3)
        c = cite("TopoVerus Fig. 4, p.9 (Case Study B, App. B p.17)")
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
        trace = VGroup(T("price[2] - price[0]", size=S.SMALL_SIZE, mono=True),
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
        why = VGroup(note("before any day is processed:", size=S.SMALL_SIZE - 2),
                     note("only the empty prefix 0..i", size=S.SMALL_SIZE - 2)).arrange(DOWN, buff=0.08)
        why.next_to(viol, DOWN, buff=0.2).set_x(colx)
        with self.beat("Topo05Counterexample-3"):
            bad = highlight_lines(panel, *L_BUG, color=S.BAD)
            self.play(FadeIn(viol, shift=UP * 0.1), ReplacementTransform(bug, bad), run_time=0.8)
            self.play(FadeIn(why), run_time=0.6)
        with self.beat("Topo05Counterexample-4"):
            cause = VGroup(T("root cause:", size=S.SMALL_SIZE + 2, color=ACC, weight="BOLD"),
                           T("the quantifier range", size=S.SMALL_SIZE + 2, color=ACC, weight="BOLD")
                           ).arrange(DOWN, buff=0.08)
            cause.move_to(why)
            self.play(ReplacementTransform(why, cause), Indicate(bad, color=S.BAD), run_time=1.0)


# ------------------------------------------------------------------ 6. repair target
class Topo06Repair(TopoScene):
    def construct(self):
        panel = loop_panel(font_size=15).to_corner(UL, buff=0.3)
        colx = (panel.get_right()[0] + 7.0) / 2
        bad = highlight_lines(panel, *L_BUG, color=S.BAD)
        lines = screen("caseB-fig4-counterexample-SCREEN.txt")["repair target"]
        words = " ".join(lines.split())
        wrapped = ["The last invariant talks about", "all future days. It should only",
                   "summarize the processed prefix:", "0 <= j < k < i."]
        assert " ".join(wrapped) == words, words
        rat = VGroup(T("repair target", size=S.SMALL_SIZE - 2, color=ACC),
                     *[T(l, size=S.SMALL_SIZE - 2, mono=(i == 3), color=ACC if i == 3 else S.INK)
                       for i, l in enumerate(wrapped)]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        rc = card(rat.width + 0.5, rat.height + 0.45, edge=ACC)
        R = VGroup(rc, rat.move_to(rc))
        R.move_to([colx, 0, 0]).to_edge(UP, buff=0.6)
        c = cite("TopoVerus Fig. 4 p.9; §4.6 p.8; App. B p.17")
        with self.beat("Topo06Repair-1"):
            self.play(FadeIn(panel), FadeIn(bad), FadeIn(c), run_time=0.8)
            self.play(FadeIn(R, shift=LEFT * 0.2), run_time=1.0)

        twin = aligned_twin(panel, LOOP_FIXED, "rust", title="x", line_numbers=False, font_size=15)
        new_line = twin.lines[L_RANGE - 1]
        sub = VGroup(T("full array", size=S.SMALL_SIZE + 2, color=S.BAD),
                     T("→ processed prefix", size=S.SMALL_SIZE + 2, color=ACC)).arrange(DOWN, buff=0.12)
        sub.next_to(R, DOWN, buff=0.6).set_x(colx)
        with self.beat("Topo06Repair-2"):
            self.play(Transform(panel.lines[L_RANGE - 1], new_line), run_time=1.2)
            fixed = SurroundingRectangle(VGroup(*panel.lines[L_BUG[0] - 1:L_BUG[1]]), color=ACC, buff=0.06,
                                         stroke_width=3, corner_radius=0.05)
            self.play(ReplacementTransform(bad, fixed), FadeIn(sub), run_time=0.8)


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
             {"id": "gate", "label": "Safety gate", "sub": "Lynette: only proof code changed?", "pos": [3.0, 0.55],
              "w": 3.9, "h": 1.05, "color": S.WARN},
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
        c = cite("TopoVerus §3.2 and Eq. 2 p.5; §4.1 p.6–7")
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
        h = heading("Binary-search insertion: five invariants")
        inv = code_panel(screen1("binary-search-invariants-SCREEN.rs"), "rust",
                         title="search_insert · loop invariants", line_numbers=False, font_size=20)
        inv.next_to(h, DOWN, buff=0.35)
        c = cite("TopoVerus Fig. 1 p.3; Fig. 2 and §2.1 p.4")
        with self.beat("Topo08Order-1"):
            self.play(FadeIn(h), FadeIn(c), run_time=0.6)
            self.play(FadeIn(inv), run_time=0.9)
        with self.beat("Topo08Order-2"):
            b = highlight_lines(inv, 1, color=S.INFO)
            self.play(Create(b), run_time=0.6)
            b2 = highlight_lines(inv, 2, 3, color=S.INFO)
            self.play(ReplacementTransform(b, b2), run_time=0.7)
            b3 = highlight_lines(inv, 4, 5, color=ACC)
            self.play(ReplacementTransform(b2, b3), run_time=0.7)

        first3 = VGroup(*inv.lines[0:3])
        miss = note("missing", color=S.MUTED, size=S.SMALL_SIZE + 2).next_to(first3, RIGHT, buff=0.6)
        under = VGroup(T("Under-constrained counterexample (Fig. 2, top)", size=S.SMALL_SIZE + 2, color=S.BAD,
                         weight="BOLD"),
                       note("state high = 2, yet it checks i = 1", size=S.SMALL_SIZE + 2, color=S.INK),
                       note("mid = 0: a hallucinated value", size=S.SMALL_SIZE + 2, color=S.INK)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        uc = card(under.width + 0.6, under.height + 0.5, edge=S.BAD)
        U = VGroup(uc, under.move_to(uc)).next_to(inv, DOWN, buff=0.45)
        with self.beat("Topo08Order-3"):
            b5w = highlight_lines(inv, 5, color=S.BAD)
            self.play(first3.animate.set_opacity(0.2), FadeIn(miss), ReplacementTransform(b3, b5w), run_time=0.8)
            self.play(FadeIn(U, shift=UP * 0.15), run_time=0.8)

        st = state_table([("nums", "[1, 3, 5]"), ("target", "5"), ("high", "2"), ("low after 1 step", "2")],
                         title="Constrained (Fig. 2, bottom)", size=S.SMALL_SIZE)
        st[0].set_stroke(S.BAD)
        check = VGroup(T("I5 at i = 2:", size=S.SMALL_SIZE + 2, color=S.MUTED),
                       T("nums[2] > 5 ?", size=S.SMALL_SIZE + 4, mono=True),
                       T("nums[2] = 5   false", size=S.SMALL_SIZE + 4, mono=True, color=S.BAD)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        low = VGroup(st, check).arrange(RIGHT, buff=0.9).next_to(inv, DOWN, buff=0.3)
        with self.beat("Topo08Order-4"):
            self.play(FadeOut(U), FadeOut(miss), first3.animate.set_opacity(1), run_time=0.6)
            self.play(FadeIn(st, shift=UP * 0.1), run_time=0.9)
            self.play(FadeIn(check[0:2]), run_time=0.6)
            self.play(FadeIn(check[2]), run_time=0.5)

        fixed = aligned_twin(inv, screen1("binary-search-invariants-SCREEN.rs").rsplit("\n", 1)[0] + "\n"
                             + screen1("binary-search-I5-fixed-SCREEN.rs"), "rust",
                             title="search_insert · loop invariants", line_numbers=False, font_size=20)
        rep = T("high <= i  →  high < i", size=S.SMALL_SIZE + 4, mono=True, color=ACC)
        rep.next_to(check, DOWN, buff=0.4).align_to(check, LEFT)
        with self.beat("Topo08Order-5"):
            self.play(Transform(inv.lines[4], fixed.lines[4]), run_time=1.0)
            self.play(b5w.animate.set_color(ACC), FadeIn(rep), run_time=0.6)


# ------------------------------------------------------------------ 9. topological graph reward (graph as in Fig. 2)
def inv_node(label: str, color=ACC):
    t = T(label, size=S.BODY_SIZE - 4, weight="BOLD", mono=True)
    r = RoundedRectangle(width=0.95, height=0.6, corner_radius=0.1, stroke_color=color, stroke_width=3,
                         fill_color=S.PANEL, fill_opacity=1)
    return VGroup(r, t.move_to(r))


class Topo09GraphReward(TopoScene):
    def construct(self):
        h = heading("Topological Graph Reward  R_dep", color=ACC)
        n = {k: inv_node(k) for k in ("I1", "I2", "I3", "I4", "I5'")}
        n["I1"].move_to([-5.4, 1.5, 0])
        n["I2"].move_to([-3.75, 1.5, 0])
        n["I3"].move_to([-2.65, 1.5, 0])
        grp = DashedVMobject(SurroundingRectangle(VGroup(n["I2"], n["I3"]), buff=0.2, corner_radius=0.1,
                                                  color=S.INK, stroke_width=2), num_dashes=40)
        n["I4"].move_to([-0.4, 2.15, 0])
        n["I5'"].move_to([-0.4, 0.85, 0])
        ar = lambda a, b: Arrow(a, b, buff=0.05, color=S.INK, stroke_width=3, max_tip_length_to_length_ratio=0.25)
        a1 = ar(n["I1"].get_right(), grp.get_left())
        a4 = ar(grp.get_right(), n["I4"].get_left())
        a5 = ar(grp.get_right(), n["I5'"].get_left())
        graph = VGroup(a1, a4, a5, grp, *n.values())
        expl = note("edge a → b: a must be established before b can be inductively verified", size=S.SMALL_SIZE)
        expl.next_to(graph, DOWN, buff=0.3).align_to(n["I1"], LEFT)
        c = cite("TopoVerus §3.1 and Defs. 1–3 p.5–6; Fig. 2 p.4; Eq. 6 p.6; §2.1 p.4; §4.1 p.6")
        with self.beat("Topo09GraphReward-1"):
            self.play(FadeIn(h), FadeIn(c), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(m) for m in n.values()], lag_ratio=0.15), Create(grp), run_time=1.2)
            self.play(GrowArrow(a1), GrowArrow(a4), GrowArrow(a5), FadeIn(expl), run_time=1.0)

        def leg(col, txt):
            return VGroup(Circle(radius=0.09, color=col, fill_color=col, fill_opacity=1),
                          T(txt, size=S.SMALL_SIZE - 2, color=S.INK)).arrange(RIGHT, buff=0.12)
        legend = VGroup(leg(S.OK, "correct"), leg(S.BAD, "wrong"), leg(S.MUTED, "missing")).arrange(RIGHT, buff=0.4)
        legend.next_to(graph, RIGHT, buff=0.8).shift(UP * 0.7)
        top = VGroup(T("Fig. 2, top", size=S.SMALL_SIZE, color=S.MUTED),
                     T("I1–I3 missing, I5 wrong", size=S.SMALL_SIZE + 2)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        bot = VGroup(T("Fig. 2, bottom", size=S.SMALL_SIZE, color=S.MUTED),
                     T("I1–I4 in place, I5 wrong", size=S.SMALL_SIZE + 2)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        top.next_to(legend, DOWN, buff=0.35).align_to(legend, LEFT)
        bot.move_to(top, aligned_edge=UL)

        def paint(state):
            return [n[k][0].animate.set_stroke(col, opacity=1).set_fill(S.PANEL, opacity=1) for k, col in state.items()]
        with self.beat("Topo09GraphReward-2"):
            self.play(FadeOut(expl), FadeIn(legend), FadeIn(top),
                      *paint({"I1": S.MUTED, "I2": S.MUTED, "I3": S.MUTED, "I4": S.OK, "I5'": S.BAD}), run_time=1.0)
            self.play(*[n[k][1].animate.set_opacity(0.45) for k in ("I1", "I2", "I3")], run_time=0.5)
            self.play(ReplacementTransform(top, bot), *[n[k][1].animate.set_opacity(1) for k in ("I1", "I2", "I3")],
                      *paint({"I1": S.OK, "I2": S.OK, "I3": S.OK}), run_time=1.0)

        f = VGroup(T("R_dep = α × β", size=S.BODY_SIZE + 2, mono=True, weight="BOLD"),
                   VGroup(T("α", size=S.BODY_SIZE, color=ACC, mono=True),
                          note("coverage: reference invariants written / all", color=S.INK)).arrange(RIGHT, buff=0.25),
                   VGroup(T("β", size=S.BODY_SIZE, color=ACC, mono=True),
                          note("edge satisfaction: edges written in dependency order / edges", color=S.INK)
                          ).arrange(RIGHT, buff=0.25)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        f.next_to(graph, DOWN, buff=0.55).align_to(n["I1"], LEFT)
        with self.beat("Topo09GraphReward-3"):
            self.play(FadeIn(f[0]), run_time=0.7)
            self.play(FadeIn(f[1], shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(f[2], shift=UP * 0.1), run_time=0.6)

        q = VGroup(T("prerequisite facts first", size=S.BODY_SIZE - 2, color=ACC, weight="BOLD"),
                   T("→ counterexamples for dependent invariants", size=S.SMALL_SIZE + 2),
                   T("in a better-constrained proof state", size=S.SMALL_SIZE + 2)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        q.next_to(f, DOWN, buff=0.35).align_to(f, LEFT)
        with self.beat("Topo09GraphReward-4"):
            self.play(FadeIn(q, shift=UP * 0.1), run_time=0.9)
        tr = badge("training signal only", ACC)
        tr2 = note("at test time: no reference proof, no graph", size=S.SMALL_SIZE)
        T2 = VGroup(tr, tr2).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        T2.next_to(top, DOWN, buff=0.5).align_to(legend, LEFT)
        with self.beat("Topo09GraphReward-5"):
            self.play(FadeIn(T2), run_time=0.8)


# ------------------------------------------------------------------ 10. safety gate
class Topo10Safety(TopoScene):
    def construct(self):
        secs = screen("safety-gate-S3-SCREEN.rs")
        h = heading("Why a safety gate?")
        orig = code_panel(secs["screen text below: original"], "rust", title="original", line_numbers=False,
                          font_size=19)
        orig.next_to(h, DOWN, buff=0.35)
        c = cite("TopoVerus code: tests/test_trust.py:138-149; safety gate (Lynette): §3.2 p.5")
        with self.beat("Topo10Safety-1"):
            self.play(FadeIn(h), FadeIn(c), run_time=0.6)
            self.play(FadeIn(orig), run_time=0.9)
            b = highlight_lines(orig, 1, color=S.INFO)
            self.play(Create(b), run_time=0.6)
        fail = badge("Verus: verification failed", S.BAD)
        x2 = note("x = 2 → y = 1, but ensures r > 1", size=S.SMALL_SIZE)
        row1 = VGroup(fail, x2).arrange(RIGHT, buff=0.4).next_to(orig, DOWN, buff=0.25)
        with self.beat("Topo10Safety-2"):
            b2 = highlight_lines(orig, 2, color=S.WARN)
            self.play(ReplacementTransform(b, b2), run_time=0.6)
            self.play(FadeIn(x2), run_time=0.5)
            self.play(FadeIn(fail), run_time=0.5)

        cand = code_panel(secs["screen text below: original"], "rust", title="move the existing assume",
                          line_numbers=False, font_size=19)
        cand.next_to(row1, DOWN, buff=0.4)
        cand_fixed = aligned_twin(cand, secs["screen text below: candidate"], "rust",
                                  title="move the existing assume", line_numbers=False, font_size=19)
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


# ------------------------------------------------------------------ 12. limitations and takeaway
class Topo12Close(TopoScene):
    def construct(self):
        h = heading("Limitations")
        items = ["Curriculum targets loop invariants, not assertions",
                 "Counterexamples are not formally checked; traces can be imprecise",
                 "Systems code (VeruSAGE), Safe-Pass@1: Sonnet-4.5 75.5% vs TopoVerus 30.2%"]
        bl = bullet_list(items, size=S.BODY_SIZE - 2).move_to(UP * 0.2)
        if bl.width > 12.6:
            bl.scale_to_fit_width(12.6)
        c1 = cite("TopoVerus §6 Limitations p.10; Table 1 p.7")
        with self.beat("Topo12Close-1"):
            self.play(FadeIn(h), FadeIn(c1), run_time=0.6)
            for it in bl:
                self.play(FadeIn(it, shift=RIGHT * 0.1), run_time=0.7)

        t = T("TopoVerus", size=S.TITLE_SIZE, weight="BOLD", color=ACC)
        lines = VGroup(T("Name a concrete failing state before repairing.", size=S.BODY_SIZE),
                       T("Reward establishing prerequisite invariants first.", size=S.BODY_SIZE),
                       T("Diagnosis becomes a skill used in a single pass.", size=S.BODY_SIZE, color=ACC)
                       ).arrange(DOWN, buff=0.35)
        tk = VGroup(t, lines).arrange(DOWN, buff=0.7).move_to(ORIGIN)
        with self.beat("Topo12Close-2"):
            self.play(FadeOut(h), FadeOut(bl), FadeOut(c1), run_time=0.6)
            self.play(FadeIn(t), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in lines], lag_ratio=0.5), run_time=2.0)
