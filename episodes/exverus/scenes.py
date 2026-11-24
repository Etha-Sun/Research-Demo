"""Episode 1 -- ExVerus: Verus proof repair via counterexample reasoning.

Scenes are listed in narration.json order. Every number on screen carries a cite(...) footnote.
On-screen code is loaded from episodes/exverus/examples/ (the part below the "on screen below" marker).
"""
from __future__ import annotations

from pathlib import Path

from manim import (
    DOWN, LEFT, RIGHT, UP, ORIGIN, UR, UL,
    Arrow, Create, FadeIn, FadeOut, FadeTransform, GrowArrow, Indicate, LaggedStart,
    Group, Line, Rectangle, SurroundingRectangle, VGroup, Write, CurvedArrow,
)

from common import style as S
from common.components import (
    NarratedScene, T, badge, bullet_list, card, cite, code_panel, highlight_lines,
    pipeline, pulse_path, series_map, state_table, title_card,
)

EP = "exverus"
ACC = S.ACCENT[EP]
EXAMPLES = Path(__file__).resolve().parent / "examples"
MARK = "---- on screen below ----"

CITE_PAPER = "ExVerus (Yang, Sun, Wu, Caridad, Yuan, Yao, Lu, Pei), ICML 2026"


def ex(name: str) -> str:
    """On-screen part of an example file (everything after the marker line)."""
    lines = (EXAMPLES / name).read_text(encoding="utf-8").splitlines()
    k = next(i for i, l in enumerate(lines) if MARK in l)
    return "\n".join(lines[k + 1:])


def heading(text: str, color: str = S.INK) -> "T":
    h = T(text, size=S.HEADING_SIZE, weight="BOLD", color=color)
    if h.width > 13.0:
        h.scale_to_fit_width(13.0)
    h.to_edge(UP, buff=0.45)
    return h


def label_under(mob, text, color=S.MUTED, size=S.SMALL_SIZE, buff=0.18):
    return T(text, size=size, color=color).next_to(mob, DOWN, buff=buff)


def grouped_bars(groups, series, colors, max_value=100.0, width=5.2, size=S.SMALL_SIZE):
    """Local helper: grouped horizontal bars.

    groups: [(group_label, [v_series0, v_series1, ...])]; series: names; colors: one per series.
    (components.bar_chart draws one series only; see STORYBOARD 'Open issues'.)
    """
    rows = VGroup()
    bar_h, gap = 0.26, 0.05
    y = 0.0
    for gl, vals in groups:
        g = VGroup()
        lab = T(gl, size=size + 2, color=S.INK, weight="BOLD")
        bars = VGroup()
        for j, v in enumerate(vals):
            r = Rectangle(width=max(0.02, width * v / max_value), height=bar_h, stroke_width=0,
                          fill_color=colors[j], fill_opacity=1)
            r.move_to([0, y - j * (bar_h + gap), 0], aligned_edge=LEFT)
            val = T(f"{v:.1f}", size=size, color=S.INK if j == 0 else S.MUTED).next_to(r, RIGHT, buff=0.12)
            bars.add(VGroup(r, val))
        lab.next_to(bars, LEFT, buff=0.35)
        lab.align_to([-0.35, 0, 0], RIGHT)
        g.add(lab, bars)
        rows.add(g)
        y -= len(vals) * (bar_h + gap) + 0.38
    legend = VGroup()
    for name, col in zip(series, colors):
        sw = Rectangle(width=0.3, height=0.2, stroke_width=0, fill_color=col, fill_opacity=1)
        legend.add(VGroup(sw, T(name, size=size, color=S.INK)).arrange(RIGHT, buff=0.12))
    legend.arrange(RIGHT, buff=0.5)
    legend.next_to(rows, UP, buff=0.4)
    return VGroup(legend, rows)


def range_row(label, lo, hi, color, width=7.0, max_value=100.0, size=S.SMALL_SIZE + 2):
    """Local helper: a bar spanning [lo, hi] on a 0..max axis (for 'between x and y' ranges)."""
    axis = Line([0, 0, 0], [width, 0, 0], color=S.PANEL_EDGE, stroke_width=2)
    span = Rectangle(width=width * (hi - lo) / max_value, height=0.36, stroke_width=0, fill_color=color, fill_opacity=1)
    span.move_to([width * (lo + hi) / 2 / max_value, 0, 0])
    lab = T(label, size=size, color=S.INK).next_to(axis, LEFT, buff=0.3)
    vals = T(f"{lo:g}–{hi:g}%", size=size, color=color).next_to(span, RIGHT, buff=0.15)
    return VGroup(lab, axis, span, vals)


# =====================================================================================================
class ExV01SeriesIntro(NarratedScene):
    EPISODE = EP

    def construct(self):
        with self.beat("exv01-1"):
            m = series_map(None)
            self.play(FadeIn(m[0], lag_ratio=0.2), run_time=2.0)
            self.play(LaggedStart(*[GrowArrow(a) for a in m[1]], lag_ratio=0.3), run_time=1.2)
            levels = ["one loop invariant", "a model that\nlearns to repair", "whole repositories",
                      "optimised SIMD\nkernels"]
            tops = VGroup()
            for tile, lv in zip(m[0], levels):
                t = T(lv, size=S.SMALL_SIZE - 2, color=S.MUTED).next_to(tile, UP, buff=0.25)
                tops.add(t)
                self.play(Indicate(tile, scale_factor=1.06, color=S.INK), FadeIn(t), run_time=0.9)
            m.add(tops)
        with self.beat("exv01-2"):
            self.play(FadeIn(m[2], shift=UP * 0.1), run_time=1.0)
            ev = VGroup(badge("counterexamples = evidence", S.BAD), badge("verifier re-check = trust", S.OK))
            ev.arrange(RIGHT, buff=0.6).next_to(m[2], DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in ev], lag_ratio=0.5), run_time=1.6)
        with self.beat("exv01-3"):
            self.play(FadeOut(VGroup(m, ev)), run_time=0.6)
            name = T("Yuechun Sun", size=S.HEADING_SIZE + 4, weight="BOLD")
            rows = VGroup(
                T("Senior undergraduate, School of the Gifted Young, USTC", size=S.BODY_SIZE - 2),
                T("Data Science and Big Data Technology", size=S.BODY_SIZE - 4, color=S.MUTED),
                T("Advisors: Prof. Kexin Pei (UChicago), Prof. Alvin Cheung (UC Berkeley)", size=S.BODY_SIZE - 4),
                T("Interests: language models and formal verification", size=S.BODY_SIZE - 4, color=ACC),
            ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
            inner = VGroup(name, rows).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
            fr = card(inner.width + 1.0, inner.height + 0.9)
            fr.move_to(inner)
            author = VGroup(fr, inner)
            c = cite("Author homepage (fetched 2026-11-23)")
            self.play(FadeIn(fr), Write(name), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.35), FadeIn(c),
                      run_time=2.0)
        with self.beat("exv01-4"):
            self.play(FadeOut(VGroup(author, c)), run_time=0.6)
            m1 = series_map(EP).scale(0.62).to_edge(UP, buff=0.35)
            tc = title_card(EP, 1, extra="Yang, Sun, Wu, Caridad, Yuan, Yao, Lu, Pei  ·  ICML 2026")
            tc.next_to(m1, DOWN, buff=0.9)
            self.play(FadeIn(m1), run_time=0.8)
            self.play(Indicate(m1[0][0], color=ACC, scale_factor=1.08), run_time=0.8)
            self.play(FadeIn(tc, shift=UP * 0.2), run_time=1.2)


# =====================================================================================================
class ExV02ColdOpen(NarratedScene):
    EPISODE = EP

    def construct(self):
        with self.beat("exv02-1"):
            code = code_panel(ex("findmax_buggy_screen.rs"), "rust", title="findmax  (VerusBench)",
                              font_size=19, max_width=7.3, max_height=6.4)
            code.to_edge(LEFT, buff=0.35).shift(DOWN * 0.1)
            c = cite("ExVerus (Yang et al., ICML 2026), Fig. 1 (p.3); requires/ensures, decreases trimmed")
            self.play(FadeIn(code, shift=UP * 0.2), FadeIn(c), run_time=1.4)
            inv = highlight_lines(code, 8, 11, color=S.INFO)
            self.play(Create(inv), run_time=0.8)
        with self.beat("exv02-2"):
            bad = highlight_lines(code, 11, color=S.BAD)
            err = VGroup(T("error:", size=S.SMALL_SIZE, color=S.BAD, weight="BOLD", mono=True),
                         T("invariant not satisfied", size=S.SMALL_SIZE, color=S.BAD, mono=True),
                         T("at end of loop body", size=S.SMALL_SIZE, color=S.BAD, mono=True)
                         ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            err.next_to(code, RIGHT, buff=0.5).align_to(code, UP).shift(DOWN * 0.4)
            q = T("where — but why?", size=S.BODY_SIZE, color=S.MUTED).next_to(err, DOWN, buff=0.5, aligned_edge=LEFT)
            self.play(FadeOut(inv), Create(bad), run_time=0.8)
            self.play(FadeIn(err, shift=LEFT * 0.2), run_time=0.8)
            self.play(FadeIn(q), run_time=0.6)
        with self.beat("exv02-3"):
            self.play(FadeOut(VGroup(err, q)), run_time=0.5)
            raw = code_panel(ex("findmax_verus_raw_model.txt"), "text",
                             title="Verus's own model (Z3)", font_size=15, line_numbers=False, max_width=5.2)
            raw.next_to(code, RIGHT, buff=0.3).align_to(code, UP)
            facts = VGroup(badge("7,083-line SMT query", S.MUTED), badge("answer: unknown", S.BAD))
            facts.arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(raw, DOWN, buff=0.3).align_to(raw, LEFT)
            c2 = cite("ExVerus (Yang et al., ICML 2026), Fig. 1 (p.3), §2.2 (p.3–4)")
            self.play(FadeIn(raw, shift=LEFT * 0.2), FadeTransform(c, c2), run_time=1.2)
            self.play(Create(SurroundingRectangle(raw.lines[0], color=S.BAD, buff=0.05)), run_time=0.6)
            self.play(Create(SurroundingRectangle(raw.lines[3], color=S.WARN, buff=0.05)),
                      Create(SurroundingRectangle(raw.lines[7], color=S.WARN, buff=0.05)),
                      Create(SurroundingRectangle(raw.lines[9], color=S.WARN, buff=0.05)), run_time=0.8)
            self.play(FadeIn(facts), run_time=0.8)
        with self.beat("exv02-4"):
            raw_group = Group(*[m for m in self.mobjects if m not in (code, bad, c2)])
            tab = state_table([("nums", "vec![-1, -1]"), ("i", "1"), ("max", "0")],
                              title="ExVerus: CEX_1")
            tab[0].set_stroke(color=S.BAD)
            tab.next_to(code, RIGHT, buff=0.5).align_to(code, UP).shift(DOWN * 0.3)
            sat = badge("Status: SAT", S.OK).next_to(tab, DOWN, buff=0.35, aligned_edge=LEFT)
            self.play(FadeOut(raw_group, shift=RIGHT * 0.2), run_time=0.6)
            self.play(FadeIn(tab, shift=LEFT * 0.2), FadeIn(sat), run_time=1.0)
            maxrow = SurroundingRectangle(VGroup(tab[1][1][0][2], tab[1][1][1][2]), color=S.BAD, buff=0.08)
            note = T("0 is not in [-1, -1]", size=S.BODY_SIZE - 2, color=S.BAD).next_to(sat, DOWN, buff=0.4,
                                                                                         aligned_edge=LEFT)
            self.play(Create(maxrow), FadeIn(note), run_time=1.0)
        with self.beat("exv02-5"):
            self.play(*[FadeOut(m) for m in self.mobjects if m is not c2], run_time=0.6)
            a = T("one-line error", size=S.BODY_SIZE, color=S.MUTED)
            b = T("concrete counterexamples", size=S.BODY_SIZE, color=S.BAD)
            d = T("repaired proof", size=S.BODY_SIZE, color=ACC)
            row = VGroup(a, b, d).arrange(RIGHT, buff=1.0)
            ar = VGroup(Arrow(a.get_right(), b.get_left(), buff=0.15, color=S.MUTED),
                        Arrow(b.get_right(), d.get_left(), buff=0.15, color=S.MUTED))
            self.play(FadeOut(c2), FadeIn(a), run_time=0.6)
            self.play(GrowArrow(ar[0]), FadeIn(b), run_time=0.8)
            self.play(GrowArrow(ar[1]), FadeIn(d), run_time=0.8)


# =====================================================================================================
class ExV03Background(NarratedScene):
    EPISODE = EP

    def construct(self):
        with self.beat("exv03-1"):
            h = heading("Verus in one slide")
            kws = VGroup(
                VGroup(T("requires", size=S.BODY_SIZE, mono=True, color=ACC),
                       T("holds on entry", size=S.SMALL_SIZE, color=S.MUTED)).arrange(DOWN, buff=0.15),
                VGroup(T("ensures", size=S.BODY_SIZE, mono=True, color=ACC),
                       T("holds on return", size=S.SMALL_SIZE, color=S.MUTED)).arrange(DOWN, buff=0.15),
                VGroup(T("invariant", size=S.BODY_SIZE, mono=True, color=ACC),
                       T("holds on every loop pass", size=S.SMALL_SIZE, color=S.MUTED)).arrange(DOWN, buff=0.15),
            )
            boxes = VGroup(*[VGroup(card(3.9, 1.4), k) for k in kws])
            for b in boxes:
                b[1].move_to(b[0])
            boxes.arrange(RIGHT, buff=0.4).next_to(h, DOWN, buff=0.7)
            self.play(FadeIn(h), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.15) for b in boxes], lag_ratio=0.35), run_time=1.6)
        with self.beat("exv03-2"):
            chk = VGroup(T("① before the loop", size=S.BODY_SIZE - 2),
                         T("② after one iteration", size=S.BODY_SIZE - 2)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            chk.next_to(boxes, DOWN, buff=1.2).to_edge(LEFT, buff=1.2)
            vc = VGroup(card(3.4, 1.1, edge=S.INFO), T("verification\ncondition", size=S.SMALL_SIZE + 2))
            vc[1].move_to(vc[0])
            z3 = VGroup(card(2.4, 1.1, edge=S.INFO), T("Z3 (SMT)", size=S.BODY_SIZE - 2, weight="BOLD"))
            z3[1].move_to(z3[0])
            vc.next_to(chk, RIGHT, buff=1.0)
            z3.next_to(vc, RIGHT, buff=1.0)
            a1 = Arrow(chk.get_right(), vc.get_left(), buff=0.1, color=S.MUTED)
            a2 = Arrow(vc.get_right(), z3.get_left(), buff=0.1, color=S.MUTED)
            self.play(FadeIn(chk, shift=RIGHT * 0.2), run_time=0.8)
            self.play(GrowArrow(a1), FadeIn(vc), run_time=0.8)
            self.play(GrowArrow(a2), FadeIn(z3), run_time=0.8)
        with self.beat("exv03-3"):
            self.play(FadeOut(VGroup(boxes, chk, vc, z3, a1, a2)), run_time=0.6)
            h2 = heading("Counterexample")
            d = VGroup(T("obligation   A  ⟹  C", size=S.BODY_SIZE + 4, mono=True),
                       T("counterexample σ:   σ ⊨ A ∧ ¬C", size=S.BODY_SIZE + 4, mono=True, color=S.BAD)
                       ).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(UP * 0.4)
            gu = T("with forall / exists, the solver often answers: unknown", size=S.BODY_SIZE - 2, color=S.MUTED)
            gu.next_to(d, DOWN, buff=0.8)
            c = cite("ExVerus (Yang et al., ICML 2026), Def. 2.1 (p.4); §2.2 (p.3)")
            self.play(FadeTransform(h, h2), FadeIn(d[0]), FadeIn(c), run_time=1.0)
            self.play(FadeIn(d[1], shift=UP * 0.1), run_time=0.8)
            self.play(FadeIn(gu), run_time=0.8)
        with self.beat("exv03-4"):
            self.play(FadeOut(VGroup(d, gu)), run_time=0.5)
            h3 = heading("ExVerus: a source-level Z3Py query")
            code = code_panel(ex("findmax_z3py_screen.py"), "python", title="written by the LLM for findmax",
                              font_size=17, max_width=7.8, max_height=5.6)
            code.next_to(h3, DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
            c2 = cite("ExVerus (Yang et al., ICML 2026), Fig. 1 (p.3); blank lines trimmed")
            self.play(FadeTransform(h2, h3), FadeTransform(c, c2), FadeIn(code, shift=UP * 0.2), run_time=1.2)
            hl = highlight_lines(code, 3, color=S.WARN)
            note = VGroup(T("length fixed to 2", size=S.BODY_SIZE, color=S.WARN),
                          T("→ no quantifiers", size=S.BODY_SIZE, color=S.WARN),
                          T("program's own names:", size=S.SMALL_SIZE + 2, color=S.MUTED),
                          T("nums, i, max", size=S.SMALL_SIZE + 2, mono=True, color=S.MUTED),
                          ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            note.next_to(code, RIGHT, buff=0.5).align_to(code, UP).shift(DOWN * 0.2)
            self.play(Create(hl), FadeIn(note[:2], shift=LEFT * 0.2), run_time=1.0)
            self.play(FadeIn(note[2:]), run_time=0.6)
        with self.beat("exv03-5"):
            out = state_table([("nums", "vec![-1, -1]"), ("i", "1"), ("max", "0")], title="SAT → CEX_1")
            out.next_to(note, DOWN, buff=0.5, aligned_edge=LEFT)
            tr = badge("not trusted until Verus checks", S.WARN).next_to(out, DOWN, buff=0.3, aligned_edge=LEFT)
            self.play(FadeIn(out, shift=UP * 0.15), run_time=0.8)
            self.play(FadeIn(tr), run_time=0.6)


# =====================================================================================================
def brs1_panel(fixed: bool = False):
    p = code_panel(ex("brs1_loop_fixed_screen.rs" if fixed else "brs1_loop_screen.rs"), "rust",
                   title="brs1, second loop  (VerusBench Diffy/brs1)", font_size=19, max_width=8.2, max_height=6.4)
    p.to_edge(LEFT, buff=0.4).shift(DOWN * 0.2)
    return p




class ExV04Brs1Bug(NarratedScene):
    EPISODE = EP

    def construct(self):
        with self.beat("exv04-1"):
            code = brs1_panel()
            c = cite("ExVerus (Yang et al., ICML 2026), Fig. 3 (p.13); first loop and correct invariants trimmed")
            self.play(FadeIn(code, shift=UP * 0.2), FadeIn(c), run_time=1.4)
            body = highlight_lines(code, 10, 14, color=S.INFO)
            self.play(Create(body), run_time=0.8)
            reset = highlight_lines(code, 11, color=S.INFO)
            tag = T("reset only when i == 0", size=S.SMALL_SIZE + 2, color=S.INFO)
            tag.next_to(code, RIGHT, buff=0.4).match_y(reset)
            self.play(FadeTransform(body, reset), FadeIn(tag), run_time=1.0)
        with self.beat("exv04-2"):
            inv = highlight_lines(code, 7, color=S.WARN)
            claim = T("LLM's invariant:  sum[0] <= i", size=S.BODY_SIZE - 2, color=S.WARN)
            claim.next_to(code, RIGHT, buff=0.4).match_y(inv)
            self.play(FadeOut(reset), FadeOut(tag), Create(inv), run_time=0.8)
            self.play(FadeIn(claim, shift=LEFT * 0.2), run_time=0.8)
        with self.beat("exv04-3"):
            bad = highlight_lines(code, 7, color=S.BAD)
            err = VGroup(T("error:", size=S.SMALL_SIZE + 2, color=S.BAD, weight="BOLD", mono=True),
                         T("invariant not satisfied", size=S.SMALL_SIZE + 2, color=S.BAD, mono=True),
                         T("before loop", size=S.SMALL_SIZE + 2, color=S.BAD, mono=True)
                         ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            err.next_to(code, RIGHT, buff=0.4).match_y(bad)
            av = VGroup(T("AutoVerus: 16 attempts", size=S.BODY_SIZE - 2, color=S.MUTED),
                        T("on this error, task failed", size=S.BODY_SIZE - 2, color=S.MUTED)
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            av.next_to(err, DOWN, buff=0.7, aligned_edge=LEFT)
            c2 = cite("ExVerus (Yang et al., ICML 2026), Fig. 3, App. A.1 (p.13)")
            self.play(FadeTransform(inv, bad), FadeTransform(claim, err), run_time=1.0)
            self.play(FadeIn(av), FadeTransform(c, c2), run_time=0.8)


# =====================================================================================================
class ExV05Brs1Cex(NarratedScene):
    EPISODE = EP

    def construct(self):
        code = brs1_panel()
        bad = highlight_lines(code, 7, color=S.BAD)
        c = cite("ExVerus (Yang et al., ICML 2026), Fig. 3 (p.13): counterexamples, validation program")
        self.add(code, bad, c)
        with self.beat("exv05-1"):
            t1 = state_table([("a", "vec![1, 1]"), ("sum", "vec![1]"), ("i", "0"), ("N", "2")], title="CEX_1")
            t2 = state_table([("a", "vec![1, 1]"), ("sum", "vec![2]"), ("i", "0"), ("N", "2")], title="CEX_2")
            for t in (t1, t2):
                t[0].set_stroke(color=S.BAD)
            tabs = VGroup(t1, t2).arrange(DOWN, buff=0.3).scale(0.85)
            tabs.next_to(code, RIGHT, buff=0.35).align_to(code, UP)
            self.play(FadeIn(t1, shift=LEFT * 0.2), run_time=0.9)
            self.play(FadeIn(t2, shift=LEFT * 0.2), run_time=0.9)
        with self.beat("exv05-2"):
            ev = VGroup(T("sum[0] <= i", size=S.BODY_SIZE, mono=True),
                        T("1 <= 0", size=S.BODY_SIZE, mono=True, color=S.BAD),
                        T("false", size=S.BODY_SIZE, weight="BOLD", color=S.BAD)).arrange(DOWN, buff=0.25)
            ev.move_to(t2).align_to(t2, LEFT).shift(RIGHT * 0.2)
            kv = t1[1][1]  # (keys, vals); rows: a, sum, i, N
            self.play(FadeOut(t2), run_time=0.5)
            self.play(Indicate(VGroup(kv[0][1], kv[1][1]), color=S.BAD),
                      Indicate(VGroup(kv[0][2], kv[1][2]), color=S.BAD), run_time=1.0)
            self.play(FadeIn(ev[0]), run_time=0.5)
            self.play(FadeTransform(ev[0].copy(), ev[1]), run_time=0.8)
            self.play(FadeIn(ev[2]), run_time=0.5)
        with self.beat("exv05-3"):
            self.play(FadeOut(VGroup(code, bad, ev)), run_time=0.6)
            self.play(t1.animate.scale(1 / 0.85).to_edge(RIGHT, buff=0.5).to_edge(UP, buff=0.9), run_time=0.8)
            h = harness_panel(False)
            h.to_edge(LEFT, buff=0.4).shift(DOWN * 0.1)
            self.play(FadeIn(h, shift=UP * 0.2), run_time=1.0)
            inj = highlight_lines(h, 2, 5, color=S.INFO)
            injl = T("CEX_1 injected", size=S.SMALL_SIZE + 2, color=S.INFO).next_to(t1, DOWN, buff=0.3)
            self.play(Create(inj), FadeIn(injl), run_time=0.8)
            asr = highlight_lines(h, 7, 11, color=S.MUTED)
            asl = T("invariants → assertions", size=S.SMALL_SIZE + 2, color=S.MUTED).next_to(injl, DOWN, buff=0.3)
            self.play(Create(asr), FadeIn(asl), run_time=0.8)
            self.no_llm = badge("no LLM in this step", S.INFO).next_to(asl, DOWN, buff=0.4)
            self.play(FadeIn(self.no_llm), run_time=0.6)
        with self.beat("exv05-4"):
            fail = highlight_lines(h, 11, color=S.BAD)
            v = VGroup(badge("assertion fails", S.BAD), badge("CEX_1 validated", S.BAD)).arrange(RIGHT, buff=0.4)
            v.next_to(h, DOWN, buff=0.35)
            self.play(FadeOut(asr), FadeOut(inj), Create(fail), run_time=0.8)
            self.play(FadeIn(v[0]), run_time=0.6)
            self.play(FadeIn(v[1]), run_time=0.6)


def harness_panel(blocking: bool):
    return code_panel(ex("brs1_harness_blocking_screen.rs" if blocking else "brs1_harness_screen.rs"), "rust",
                      title="validation program (loop extracted)", font_size=16, max_width=8.6, max_height=5.6)


# =====================================================================================================
class ExV06Triage(NarratedScene):
    EPISODE = EP

    def construct(self):
        with self.beat("exv06-1"):
            h = heading("Triage: is the counterexample reachable?")
            left = VGroup(T("reachable", size=S.BODY_SIZE + 4, weight="BOLD", color=S.BAD),
                          T("a real run can produce it", size=S.SMALL_SIZE + 2, color=S.MUTED)
                          ).arrange(DOWN, buff=0.2)
            right = VGroup(T("spurious", size=S.BODY_SIZE + 4, weight="BOLD", color=S.WARN),
                           T("no run ever reaches it", size=S.SMALL_SIZE + 2, color=S.MUTED)
                           ).arrange(DOWN, buff=0.2)
            cols = VGroup(VGroup(card(5.2, 2.0, edge=S.BAD), left), VGroup(card(5.2, 2.0, edge=S.WARN), right))
            for g in cols:
                g[1].move_to(g[0])
            cols.arrange(RIGHT, buff=0.8).next_to(h, DOWN, buff=0.7)
            self.play(FadeIn(h), run_time=0.6)
            self.play(FadeIn(cols[0], shift=UP * 0.15), run_time=0.8)
            self.play(FadeIn(cols[1], shift=UP * 0.15), run_time=0.8)
        with self.beat("exv06-2"):
            v1 = VGroup(T("invariant is wrong", size=S.BODY_SIZE - 2),
                        T("wrong_fact → replace", size=S.BODY_SIZE - 2, mono=True, color=S.BAD)
                        ).arrange(DOWN, buff=0.2).next_to(cols[0], DOWN, buff=0.45)
            v2 = VGroup(T("invariant too weak", size=S.BODY_SIZE - 2),
                        T("too_weak → strengthen", size=S.BODY_SIZE - 2, mono=True, color=S.WARN)
                        ).arrange(DOWN, buff=0.2).next_to(cols[1], DOWN, buff=0.45)
            c = cite("ExVerus (Yang et al., ICML 2026), §3.2 (p.5)")
            self.play(FadeIn(v1, shift=UP * 0.1), FadeIn(c), run_time=0.8)
            self.play(FadeIn(v2, shift=UP * 0.1), run_time=0.8)
        with self.beat("exv06-3"):
            keep = VGroup(cols, v1, v2)
            h2 = heading("Triage for brs1")
            self.play(FadeOut(keep), FadeTransform(h, h2), run_time=0.8)
            js = code_panel(ex("brs1_triage.json"), "json", title="brs1: LLM diagnosis", font_size=19,
                            line_numbers=False, max_width=8.2)
            js.to_edge(LEFT, buff=0.4).shift(DOWN * 0.2)
            c2 = cite("ExVerus (Yang et al., ICML 2026), Fig. 3 (p.13); rationale wrapped for screen")
            self.play(FadeIn(js, shift=UP * 0.2), FadeTransform(c, c2), run_time=1.0)
            self.play(Create(highlight_lines(js, 2, color=S.BAD)), run_time=0.6)
            self.play(Create(highlight_lines(js, 4, 5, color=S.BAD)), run_time=0.8)
            res = VGroup(T("brs1", size=S.BODY_SIZE - 2, weight="BOLD"),
                         T("reachable", size=S.SMALL_SIZE + 2, color=S.BAD),
                         T("wrong_fact → replace", size=S.SMALL_SIZE + 2, mono=True, color=S.BAD)
                         ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            resc = VGroup(card(4.4, res.height + 0.5, edge=S.BAD), res)
            res.move_to(resc[0])
            resc.next_to(js, RIGHT, buff=0.4).align_to(js, UP)
            self.play(FadeIn(resc, shift=LEFT * 0.15), run_time=0.8)
        with self.beat("exv06-4"):
            fm = VGroup(T("findmax (cold open)", size=S.BODY_SIZE - 2, weight="BOLD"),
                        T("max = 0 never occurs", size=S.SMALL_SIZE + 2, color=S.MUTED),
                        T("for [-1, -1]: spurious", size=S.SMALL_SIZE + 2, color=S.WARN),
                        T("too_weak → strengthen", size=S.SMALL_SIZE + 2, mono=True, color=S.WARN)
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            fmc = VGroup(card(4.4, fm.height + 0.5, edge=S.WARN), fm)
            fm.move_to(fmc[0])
            fmc.next_to(resc, DOWN, buff=0.4).align_to(resc, LEFT)
            c3 = cite("ExVerus (Yang et al., ICML 2026), Fig. 3 (p.13); findmax: Fig. 8 (p.23)")
            self.play(FadeIn(fmc, shift=UP * 0.15), FadeTransform(c2, c3), run_time=1.0)


# =====================================================================================================
class ExV07Repair(NarratedScene):
    EPISODE = EP

    def construct(self):
        with self.beat("exv07-1"):
            h = heading("Mutate: five candidate proofs (replace mutator)")
            pat = badge("shared by all CEXs:  i = 0  and  sum[0] > 0", S.BAD).next_to(h, DOWN, buff=0.4)
            cands = VGroup()
            for k in range(1, 6):
                shown = k == 1
                lab = VGroup(T(f"mutant_{k}", size=S.SMALL_SIZE + 2, mono=True, weight="BOLD",
                               color=S.INK if shown else S.MUTED),
                             T("i > 0 ==> sum[0] <= i as i32" if shown else "not shown in the paper",
                               size=S.SMALL_SIZE - 2, mono=shown, color=ACC if shown else S.MUTED)
                             ).arrange(DOWN, buff=0.12)
                bx = card(max(2.3, lab.width + 0.3), 1.1, edge=ACC if shown else S.PANEL_EDGE)
                lab.move_to(bx)
                cands.add(VGroup(bx, lab))
            cands.arrange(RIGHT, buff=0.22).next_to(pat, DOWN, buff=0.6)
            if cands.width > 13.4:
                cands.scale_to_fit_width(13.4)
            c = cite("ExVerus (Yang et al., ICML 2026), §4.1 (p.6: 5 mutants); Fig. 3 and App. A.1 (p.13)")
            self.play(FadeIn(h), FadeIn(c), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.15) for x in cands], lag_ratio=0.2), run_time=1.6)
            self.play(FadeIn(pat), run_time=0.7)
        with self.beat("exv07-2"):
            rk = T("rank = # validated counterexamples blocked", size=S.BODY_SIZE, color=S.INFO)
            rk.next_to(cands, DOWN, buff=0.6)
            blk = T("blocked: CEX no longer triggers the failure", size=S.SMALL_SIZE + 2, color=S.MUTED)
            blk.next_to(rk, DOWN, buff=0.25)
            top = badge("mutant_1 blocks all CEXs  (paper, p.13)", ACC).next_to(blk, DOWN, buff=0.4)
            pdr = T("idea from PDR / IC3", size=S.SMALL_SIZE, color=S.MUTED).next_to(top, DOWN, buff=0.3)
            c2 = cite("ExVerus (Yang et al., ICML 2026), p.6 'Mutant ranking'; App. A.1 (p.13)")
            self.play(FadeIn(rk), FadeTransform(c, c2), run_time=0.8)
            self.play(FadeIn(blk), run_time=0.6)
            self.play(FadeIn(top), Indicate(cands[0], color=ACC), FadeIn(pdr), run_time=1.0)
        with self.beat("exv07-3"):
            self.play(*[FadeOut(m) for m in self.mobjects if m is not c2], run_time=0.6)
            code = brs1_panel()
            bad = highlight_lines(code, 7, color=S.BAD)
            self.play(FadeIn(code), Create(bad), run_time=0.8)
            fixed = brs1_panel(fixed=True)
            diff = code_panel(ex("brs1_patch.diff"), "diff", title="patch of mutant_1", font_size=17,
                              line_numbers=False, max_width=6.75 - code.get_right()[0] - 0.4 - 0.3)
            diff.next_to(code, RIGHT, buff=0.4).align_to(code, UP)
            self.play(FadeIn(diff, shift=LEFT * 0.2), run_time=0.8)
            good = highlight_lines(fixed, 7, color=S.OK)
            self.play(FadeTransform(code.lines[6], fixed.lines[6]), FadeTransform(bad, good), run_time=1.4)
            self.code, self.good, self.diff = code, good, diff
            self.fixed_line = fixed.lines[6]
        with self.beat("exv07-4"):
            self.play(FadeOut(VGroup(self.code, self.good, self.diff, self.fixed_line)), run_time=0.6)
            hb = harness_panel(False)
            hb.to_edge(LEFT, buff=0.4).shift(UP * 0.3)
            h = harness_panel(True).move_to(hb)
            cx = state_table([("a", "vec![1, 1]"), ("sum", "vec![1]"), ("i", "0"), ("N", "2")], title="CEX_1")
            cx[0].set_stroke(color=S.BAD)
            cx.scale(0.85).next_to(hb, RIGHT, buff=0.35).align_to(hb, UP)
            self.play(FadeIn(hb, shift=UP * 0.2), FadeIn(cx), run_time=0.8)
            red = highlight_lines(hb, 11, color=S.BAD)
            self.play(Create(red), run_time=0.5)
            ok = highlight_lines(h, 11, color=S.OK)
            self.play(FadeTransform(hb.lines[10], h.lines[10]), FadeTransform(red, ok), run_time=1.2)
            okb = badge("assertion passes: CEX_1 blocked", S.OK).next_to(hb, DOWN, buff=0.3)
            self.play(FadeIn(okb), run_time=0.6)
            self.cx = cx
        with self.beat("exv07-5"):
            rep = VGroup(T("paper reports:", size=S.SMALL_SIZE + 2, color=S.MUTED),
                         T("mutant_1 blocks all CEXs", size=S.SMALL_SIZE + 2, color=S.OK, weight="BOLD"),
                         T("and passes Verus", size=S.SMALL_SIZE + 2, color=S.OK, weight="BOLD"),
                         T("reference proof:", size=S.SMALL_SIZE + 2, color=S.MUTED),
                         T("same guard  i > 0 ==>", size=S.SMALL_SIZE + 2, color=S.INK, mono=True),
                         ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            rep[3].shift(DOWN * 0.2)
            rep[4].shift(DOWN * 0.2)
            repc = VGroup(card(rep.width + 0.5, rep.height + 0.5, edge=S.OK), rep)
            rep.move_to(repc[0])
            avail = 6.85 - self.cx.get_left()[0]
            if repc.width > avail:
                repc.scale_to_fit_width(avail)
            repc.next_to(self.cx, DOWN, buff=0.35).align_to(self.cx, LEFT)
            c3 = cite("ExVerus (Yang et al., ICML 2026), App. A.1 (p.13); repo cleaned-verusbench/Diffy/verified/brs1.rs:35")
            self.play(FadeIn(repc, shift=UP * 0.1), FadeTransform(c2, c3), run_time=1.0)


# =====================================================================================================
ARCH_NODES = [
    {"id": "proof", "label": "Proof + Verus", "sub": "LLM draft, error", "pos": [-5.25, 1.6], "color": S.MUTED,
     "w": 2.7},
    {"id": "gen", "label": "Generate", "sub": "LLM → Z3Py → CEXs", "pos": [-1.75, 1.6], "color": ACC, "w": 2.7},
    {"id": "val", "label": "Validate", "sub": "Verus, extracted loop", "pos": [1.75, 1.6], "color": S.OK, "w": 2.7},
    {"id": "tri", "label": "Triage", "sub": "wrong_fact / too_weak", "pos": [5.25, 1.6], "color": ACC, "w": 2.7},
    {"id": "mut", "label": "Mutate & rank", "sub": "5 candidates, # CEX blocked", "pos": [5.25, -1.3],
     "color": ACC, "w": 2.7},
    {"id": "ver", "label": "Verus", "sub": "check candidates", "pos": [1.75, -1.3], "color": S.OK, "w": 2.7},
    {"id": "done", "label": "Verified", "sub": "proof accepted", "pos": [-5.25, -1.3], "color": S.OK, "w": 2.7},
]
ARCH_EDGES = [
    {"from": "proof", "to": "gen", "label": ""},
    {"from": "gen", "to": "val", "label": ""},
    {"from": "val", "to": "tri", "label": ""},
    {"from": "tri", "to": "mut", "label": ""},
    {"from": "mut", "to": "ver", "label": ""},
    {"from": "ver", "to": "done", "label": ""},
]


class ExV08Architecture(NarratedScene):
    EPISODE = EP

    def construct(self):
        g = pipeline(ARCH_NODES, ARCH_EDGES)
        orig = {k: v[0].get_stroke_color() for k, v in g.by_id.items()}
        h = heading("ExVerus pipeline")
        c = cite("ExVerus (Yang et al., ICML 2026), Fig. 2 (p.4), Alg. 1–3 (p.19), §4.1 (p.6), §4.3 (p.7)")

        def elab(a, b, text, color=S.MUTED, side=UP):
            return T(text, size=S.SMALL_SIZE - 2, color=color).next_to(g.edge_by_id[(a, b)], side, buff=0.1)

        labs = {
            "error": elab("proof", "gen", "error"),
            "cex": elab("gen", "val", "CEXs"),
            "valid": elab("val", "tri", "valid"),
            "verdict": elab("tri", "mut", "verdict", side=RIGHT),
            "best": elab("mut", "ver", "best", side=DOWN),
            "pass": elab("ver", "done", "pass", color=S.OK),
        }
        retry = T("≤ 10 CEXs; retry if not SAT", size=S.SMALL_SIZE - 4, color=S.MUTED)
        retry.next_to(g.by_id["gen"], DOWN, buff=0.12)
        loop = CurvedArrow(g.by_id["ver"].get_corner(UL) + RIGHT * 0.3, g.by_id["proof"].get_bottom() + DOWN * 0.05,
                           angle=-0.35, color=S.WARN, stroke_width=3)
        loop_lab = T("still failing:\nnext iteration (max 10)", size=S.SMALL_SIZE - 4, color=S.WARN)
        loop_lab.move_to([0, 0.05, 0]).to_edge(LEFT, buff=0.5)

        def show(node_id, edge=None, extra=()):
            anims = [FadeIn(g.by_id[node_id], shift=UP * 0.1)]
            if edge:
                anims.append(GrowArrow(g.edge_by_id[edge]))
            anims += [FadeIn(x) for x in extra]
            self.play(*anims, run_time=0.8)

        with self.beat("exv08-1"):
            self.play(FadeIn(h), FadeIn(c), run_time=0.6)
            show("proof")
        with self.beat("exv08-2"):
            show("gen", ("proof", "gen"), [labs["error"]])
            self.play(FadeIn(retry), run_time=0.5)
        with self.beat("exv08-3"):
            show("val", ("gen", "val"), [labs["cex"]])
            show("tri", ("val", "tri"), [labs["valid"]])
        with self.beat("exv08-4"):
            show("mut", ("tri", "mut"), [labs["verdict"]])
            show("ver", ("mut", "ver"), [labs["best"]])
            show("done", ("ver", "done"), [labs["pass"]])
            self.play(Create(loop), FadeIn(loop_lab), run_time=1.0)
        cap = None

        def step(node_id, text, color=S.INFO):
            nonlocal cap
            new = T(text, size=S.BODY_SIZE - 4, color=color, mono=True)
            new.move_to([0, -2.85, 0])
            if cap is None:
                self.play(FadeIn(new), run_time=0.3)
            else:
                self.play(FadeTransform(cap, new), run_time=0.3)
            cap = new
            pulse_path(self, g, [node_id], color=color, run_time=0.35)
            self.play(g.by_id[node_id][0].animate.set_stroke(color=orig[node_id]), run_time=0.2)

        with self.beat("exv08-5"):
            step("proof", "brs1: sum[0] <= i as i32  fails before loop", S.BAD)
            step("gen", "CEX_1: sum = vec![1], i = 0", S.BAD)
            step("val", "assertion fails → CEX_1 validated", S.BAD)
        with self.beat("exv08-6"):
            step("tri", "verdict: wrong_fact", S.WARN)
            step("mut", "mutant_1: i > 0 ==> sum[0] <= i as i32", ACC)
            step("ver", "blocks all CEXs (paper, p.13)", S.OK)
            step("done", "paper reports: passes Verus", S.OK)
        with self.beat("exv08-7"):
            llm = VGroup(*[g.by_id[i] for i in ("gen", "tri", "mut")])
            ver = VGroup(*[g.by_id[i] for i in ("val", "ver")])
            t1 = T("LLM proposes", size=S.SMALL_SIZE + 2, color=ACC)
            t2 = T("only Verus decides", size=S.SMALL_SIZE + 2, color=S.OK, weight="BOLD")
            lg = VGroup(t1, t2).arrange(RIGHT, buff=0.8).move_to([0, -2.85, 0])
            self.play(FadeOut(cap), run_time=0.3)
            self.play(*[Indicate(b, color=ACC, scale_factor=1.04) for b in llm], FadeIn(t1), run_time=1.0)
            self.play(*[b[0].animate.set_stroke(color=S.OK, width=6) for b in ver], FadeIn(t2), run_time=1.0)


# =====================================================================================================
class ExV09Results(NarratedScene):
    EPISODE = EP

    def construct(self):
        with self.beat("exv09-1"):
            h = heading("Success rate (%), Claude Sonnet 4.5")
            ch = grouped_bars([("VerusBench", [88.4, 75.3, 83.6]), ("DafnyBench", [95.5, 95.5, 95.5]),
                               ("LCBench", [28.6, 14.3, 25.0]), ("HumanEval", [41.2, 27.9, 29.4])],
                              ["ExVerus", "AutoVerus", "Iterative Refinement"], [ACC, S.INFO, S.MUTED],
                              width=6.0)
            ch.next_to(h, DOWN, buff=0.35)
            ch.shift(RIGHT * 0.6)
            c = cite("ExVerus (Yang et al., ICML 2026), Table 1 (p.7), Claude-Sonnet-4.5")
            self.play(FadeIn(h), FadeIn(c), FadeIn(ch[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in ch[1]], lag_ratio=0.3), run_time=2.0)
        with self.beat("exv09-2"):
            hard = SurroundingRectangle(VGroup(ch[1][2], ch[1][3]), color=S.WARN, buff=0.12)
            note = T("harder benchmarks:\nbelow 50%", size=S.SMALL_SIZE + 2, color=S.WARN)
            note.next_to(hard, RIGHT, buff=0.3)
            self.play(Indicate(ch[1][0], color=ACC), Indicate(ch[1][2], color=ACC), Indicate(ch[1][3], color=ACC),
                      run_time=1.2)
            self.play(Create(hard), FadeIn(note), run_time=0.8)
        with self.beat("exv09-3"):
            self.play(FadeOut(VGroup(ch, hard, note)), run_time=0.6)
            h2 = heading("VerusBench (%), DeepSeek-V3.1")
            ch2 = grouped_bars([("VerusBench", [71.9, 24.7, 60.3])],
                               ["ExVerus", "AutoVerus", "Iterative Refinement"], [ACC, S.INFO, S.MUTED],
                               width=7.0)
            ch2.scale(1.2).move_to(ORIGIN).shift(RIGHT * 0.6)
            c2 = cite("ExVerus (Yang et al., ICML 2026), Table 1 (p.7), DeepSeek-V3.1")
            self.play(FadeTransform(h, h2), FadeTransform(c, c2), FadeIn(ch2[0]), run_time=0.8)
            self.play(FadeIn(ch2[1], shift=RIGHT * 0.2), run_time=1.0)
        with self.beat("exv09-4"):
            self.play(FadeOut(ch2), run_time=0.6)
            h3 = heading("ObfsBench: 266 obfuscated tasks, DeepSeek-V3.1")
            r1 = range_row("ExVerus", 73.9, 86.5, ACC)
            r2 = range_row("AutoVerus", 24.7, 36.5, S.INFO)
            r1.shift(UP * 0.9)
            rows = VGroup(r1, r2)
            rows.shift(LEFT * 3.0 + DOWN * 0.3)  # both axes start at the same x (0% line)
            ticks = VGroup()
            for v in (0, 50, 100):
                x = r2[1].get_left()[0] + 7.0 * v / 100
                ticks.add(T(f"{v}%", size=S.SMALL_SIZE - 2, color=S.MUTED).move_to([x, r2[1].get_y() - 0.45, 0]))
            sub = T("range over 6 obfuscation strategies", size=S.SMALL_SIZE + 2, color=S.MUTED)
            sub.next_to(ticks, DOWN, buff=0.5)
            c3 = cite("ExVerus (Yang et al., ICML 2026), Table 2 (p.7); ObfsBench size p.6")
            self.play(FadeTransform(h2, h3), FadeTransform(c2, c3), run_time=0.8)
            self.play(FadeIn(VGroup(r1[0], r1[1], r2[0], r2[1], ticks)), run_time=0.6)
            self.play(GrowFromLeft(r1[2]), FadeIn(r1[3]), run_time=0.8)
            self.play(GrowFromLeft(r2[2]), FadeIn(r2[3]), FadeIn(sub), run_time=0.8)


def GrowFromLeft(m):
    from manim import GrowFromEdge
    return GrowFromEdge(m, LEFT)


# =====================================================================================================
class ExV10Evidence(NarratedScene):
    EPISODE = EP

    def construct(self):
        with self.beat("exv10-1"):
            h = heading("Ablation: ObfsBench, DeepSeek-V3.1 (%)")
            ch = grouped_bars([("ObfsBench", [81.6, 65.4])], ["ExVerus", "ExVerus_NO_MUT (CEXs to LLM, no validation)"],
                              [ACC, S.MUTED], width=7.0)
            ch.scale(1.2).move_to(ORIGIN).shift(RIGHT * 0.6)
            c = cite("ExVerus (Yang et al., ICML 2026), Table 4 (p.8)")
            self.play(FadeIn(h), FadeIn(c), FadeIn(ch[0]), run_time=0.8)
            self.play(FadeIn(ch[1], shift=RIGHT * 0.2), run_time=1.0)
        with self.beat("exv10-2"):
            self.play(FadeOut(ch), run_time=0.6)
            h2 = heading("Does blocking predict success?  (one CEX per repair)")
            a = VGroup(T("mutants that block the CEX", size=S.BODY_SIZE - 2),
                       T("70.78%", size=S.TITLE_SIZE, color=S.OK, weight="BOLD"),
                       T("172 / 243 verify", size=S.BODY_SIZE - 2, color=S.OK)
                       ).arrange(DOWN, buff=0.25)
            b = VGroup(T("mutants that block none", size=S.BODY_SIZE - 2),
                       T("24.84%", size=S.TITLE_SIZE, color=S.MUTED, weight="BOLD"),
                       T("38 / 153 verify", size=S.BODY_SIZE - 2, color=S.MUTED)
                       ).arrange(DOWN, buff=0.25)
            ca = VGroup(card(5.6, 2.9, edge=S.OK), a)
            cb = VGroup(card(5.6, 2.9), b)
            a.move_to(ca[0])
            b.move_to(cb[0])
            pair = VGroup(ca, cb).arrange(RIGHT, buff=0.6).move_to(DOWN * 0.2)
            c2 = cite("ExVerus (Yang et al., ICML 2026), §4.3 (p.8), ExVerus_ONE_CEX")
            self.play(FadeTransform(h, h2), FadeTransform(c, c2), run_time=0.8)
            self.play(FadeIn(ca, shift=UP * 0.15), run_time=0.8)
            self.play(FadeIn(cb, shift=UP * 0.15), run_time=0.8)
        with self.beat("exv10-3"):
            self.play(FadeOut(pair), run_time=0.6)
            h3 = heading("Cost and time per task")
            hdr = ["model", "", "ExVerus", "AutoVerus"]
            rows = [["DeepSeek-V3.1", "cost", "$0.04", "$0.17"], ["", "time", "720.3 s", "2989.1 s"],
                    ["GPT-4o", "cost", "$0.42", "$0.69"], ["", "time", "250.0 s", "233.9 s"]]
            xs = [-4.2, -1.6, 1.0, 3.8]
            tab = VGroup()
            for j, t in enumerate(hdr):
                tab.add(T(t, size=S.SMALL_SIZE + 2, color=S.MUTED).move_to([xs[j], 1.6, 0]))
            for i, r in enumerate(rows):
                y = 0.8 - i * 0.75 - (0.3 if i >= 2 else 0)
                for j, t in enumerate(r):
                    col = ACC if j == 2 else (S.INK if j != 1 else S.MUTED)
                    tab.add(T(t, size=S.BODY_SIZE - 2, color=col, mono=j >= 2).move_to([xs[j], y, 0]))
            sep = Line([-5.6, -0.47, 0], [5.0, -0.47, 0], color=S.PANEL_EDGE, stroke_width=2)
            top = Line([-5.6, 1.25, 0], [5.0, 1.25, 0], color=S.PANEL_EDGE, stroke_width=2)
            note = T("cost depends on the model", size=S.SMALL_SIZE + 2, color=S.WARN).move_to([0, -2.9, 0])
            c3 = cite("ExVerus (Yang et al., ICML 2026), Table 3 (p.8)")
            self.play(FadeTransform(h2, h3), FadeTransform(c2, c3), FadeIn(tab[:4]), Create(top), run_time=0.8)
            self.play(FadeIn(tab[4:12]), run_time=0.8)
            self.play(Create(sep), FadeIn(tab[12:]), run_time=0.8)
            self.play(FadeIn(note), run_time=0.5)


# =====================================================================================================
class ExV11Limits(NarratedScene):
    EPISODE = EP

    def construct(self):
        h = heading("What the paper does not claim")
        items = [
            ("Validation covers only loop-invariant errors", "§3.1 (p.5), §5 (p.8)"),
            ("Other errors: counterexamples are unvalidated hints", "§5 (p.8)"),
            ("CEX generation can fail or be wrong; only Verus is trusted", "p.2, p.5"),
            ("Passing Verus ≠ the spec matches the user's intent", "Impact Statement (p.9)"),
            ("Weaker on tasks needing asserts / proof blocks (GPT-4o)", "Table 5 (p.23)"),
            ("Verus version change lowered the AutoVerus baseline", "App. H.4 (p.22)"),
        ]
        rows = VGroup()
        for text, loc in items:
            rows.add(VGroup(T("•  " + text, size=S.BODY_SIZE - 4), T(loc, size=S.CITE_SIZE + 2, color=S.MUTED)
                            ).arrange(DOWN, aligned_edge=LEFT, buff=0.08))
        pairs = []
        for k in range(0, 6, 2):
            pr = VGroup(rows[k], rows[k + 1]).arrange(DOWN, aligned_edge=LEFT, buff=0.6)
            pr.move_to(DOWN * 0.2)
            pairs.append(pr)
        c = cite("ExVerus (Yang, Sun, Wu, Caridad, Yuan, Yao, Lu, Pei), ICML 2026")

        def show(n):
            if n == 0:
                self.play(FadeIn(h), FadeIn(c), run_time=0.6)
            else:
                self.play(FadeOut(pairs[n - 1], shift=UP * 0.2), run_time=0.5)
            self.play(FadeIn(pairs[n][0], shift=RIGHT * 0.2), run_time=0.7)
            self.play(FadeIn(pairs[n][1], shift=RIGHT * 0.2), run_time=0.7)

        with self.beat("exv11-1"):
            show(0)
        with self.beat("exv11-2"):
            show(1)
        with self.beat("exv11-3"):
            show(2)


# =====================================================================================================
class ExV12Bridge(NarratedScene):
    EPISODE = EP

    def construct(self):
        with self.beat("exv12-1"):
            a = T("failed proof", size=S.BODY_SIZE, color=S.MUTED)
            b = T("counterexamples", size=S.BODY_SIZE, color=S.BAD)
            d = T("repair ranked by CEXs blocked", size=S.BODY_SIZE, color=ACC)
            e = T("Verus re-check", size=S.BODY_SIZE, color=S.OK)
            row = VGroup(a, b, d, e).arrange(RIGHT, buff=0.8).scale_to_fit_width(12.8)
            ars = VGroup(*[Arrow(row[i].get_right(), row[i + 1].get_left(), buff=0.12, color=S.MUTED)
                           for i in range(3)])
            self.play(FadeIn(a), run_time=0.5)
            for i in range(3):
                self.play(GrowArrow(ars[i]), FadeIn(row[i + 1]), run_time=0.6)
        with self.beat("exv12-2"):
            self.play(FadeOut(VGroup(row, ars)), run_time=0.6)
            q = VGroup(T("ExVerus searches for a counterexample at every repair.", size=S.BODY_SIZE, color=S.MUTED),
                       T("What if the model could learn to produce it itself?", size=S.BODY_SIZE + 2, color=S.INK)
                       ).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.9)
            nxt = T("Next: TopoVerus", size=S.SMALL_SIZE + 2, color=S.ACCENT["topoverus"])
            m = series_map("topoverus").move_to(DOWN * 0.6)
            self.play(FadeIn(q), run_time=0.8)
            self.play(FadeIn(m), run_time=1.0)
            nxt.next_to(m, DOWN, buff=0.5)
            self.play(Indicate(m[0][1], color=S.ACCENT["topoverus"], scale_factor=1.08), FadeIn(nxt), run_time=1.0)
