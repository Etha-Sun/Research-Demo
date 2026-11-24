"""Episode 4: Vekto (work in progress). Manim Community 0.19.

Scenes Vek01Open .. Vek12Close. Narration: episodes/vekto/narration.json.
On-screen code: episodes/vekto/examples/ (each file's header names the exact repo source and the trims).
Local helpers (not in common/components.py): example(), heading(), chip_row(), lane_box(), gate_row(), status_row(), tag().
"""
from __future__ import annotations

from pathlib import Path

from manim import (
    DOWN, LEFT, RIGHT, UP, ORIGIN, UL, UR,
    Arrow, Create, FadeIn, FadeOut, GrowArrow, LaggedStart, Line, ReplacementTransform, Square,
    SurroundingRectangle, Transform, VGroup, Indicate,
)

from common import style as S
from common.components import (
    NarratedScene, T, badge, bullet_list, card, cite, code_panel, highlight_lines, pipeline, series_map,
    state_table, title_card,
)

EP = "vekto"
ACC = S.ACCENT[EP]
EX = Path(__file__).resolve().parent / "examples"


# ------------------------------------------------------------------ local helpers
def example(name: str, part: int | None = None) -> str:
    """Screen text of examples/<name> without its source header.

    .c files: header = everything up to the first line ending in '*/'.
    .v file : header = up to the first '*)'; the body is split at '(* panel k' lines, `part` selects one.
    .diff   : lines starting with '#' are header.
    """
    lines = (EX / name).read_text(encoding="utf-8").splitlines()
    if name.endswith(".diff"):
        return "\n".join(l for l in lines if not l.startswith("#"))
    end = ".*)" if name.endswith(".v") else "*/"
    i = next(k for k, l in enumerate(lines) if l.rstrip().endswith(end[-2:]))
    body = lines[i + 1:]
    if part is None:
        return "\n".join(body)
    parts, cur = [], None
    for l in body:
        if l.startswith("(* panel"):
            cur = []
            parts.append(cur)
        elif cur is not None:
            cur.append(l)
    return "\n".join(parts[part - 1])


def heading(text: str, color: str = S.INK) -> VGroup:
    h = T(text, size=S.HEADING_SIZE - 6, weight="BOLD", color=color)
    h.to_edge(UP, buff=0.4)
    return h


def tag(text: str, color: str = S.WARN, size: float = S.SMALL_SIZE) -> VGroup:
    return badge(text, color).scale(size / S.SMALL_SIZE)


def lane_box(label: str, color: str = S.PANEL_EDGE, w: float = 1.35, h: float = 0.7, text_color: str = S.INK) -> VGroup:
    r = card(w, h, edge=color)
    t = T(label, size=S.SMALL_SIZE + 2, color=text_color, mono=True)
    if t.width > w - 0.15:
        t.scale_to_fit_width(w - 0.15)
    t.move_to(r)
    return VGroup(r, t)


def lane_row(labels, color=S.PANEL_EDGE, w=1.35) -> VGroup:
    return VGroup(*[lane_box(l, color, w) for l in labels]).arrange(RIGHT, buff=0.08)


def gate_row(name: str, desc: str) -> VGroup:
    box = Square(side_length=0.28, stroke_color=S.MUTED, stroke_width=2)
    n = T(name, size=S.SMALL_SIZE - 1, weight="BOLD", mono=True)
    d = T(desc, size=S.SMALL_SIZE - 2, color=S.MUTED)
    g = VGroup(box, n, d)
    n.next_to(box, RIGHT, buff=0.2)
    d.next_to(box, RIGHT, buff=2.7)
    return g


def status_row(key: str, what: str, statuses, detail: str) -> VGroup:
    """One experiment row: key, description + detail line, status badges right-aligned (stacked)."""
    k = T(key, size=S.BODY_SIZE + 2, weight="BOLD", color=ACC)
    w = T(what, size=S.SMALL_SIZE + 2)
    dt = T(detail, size=S.SMALL_SIZE - 2, color=S.MUTED)
    txt = VGroup(w, dt).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    bs = VGroup(*[badge(t, c) for t, c in statuses]).arrange(DOWN, aligned_edge=RIGHT, buff=0.1)
    k.move_to([-6.3, 0, 0], aligned_edge=LEFT)
    txt.move_to([-5.4, 0, 0], aligned_edge=LEFT)
    bs.move_to([6.75, 0, 0], aligned_edge=RIGHT)
    return VGroup(k, txt, bs)


# ================================================================== 1. open
class Vek01Open(NarratedScene):
    EPISODE = EP

    def construct(self):
        with self.beat("Vek01Open-1"):
            tc = title_card(EP, 4, extra="work in progress · unpublished")
            self.play(FadeIn(tc, shift=UP * 0.2), run_time=1.2)
        with self.beat("Vek01Open-2"):
            m = series_map(EP).shift(DOWN * 0.3)
            recap = T("We have seen counterexamples drive proof repair,\n"
                      "and that a proof is only as good as its spec and its checker.",
                      size=S.BODY_SIZE - 2, color=S.MUTED, line_spacing=1.2).to_edge(UP, buff=0.9)
            self.play(FadeOut(tc), run_time=0.6)
            self.play(FadeIn(m), run_time=1.0)
            self.play(FadeIn(recap, shift=DOWN * 0.1), run_time=0.8)
        with self.beat("Vek01Open-3"):
            q1 = T("Ported to another instruction set,", size=S.BODY_SIZE + 4)
            q2 = T("does an optimised kernel still compute the same thing?", size=S.BODY_SIZE + 4, color=ACC)
            q3 = T("Which assumptions does the answer rely on?", size=S.BODY_SIZE + 4, color=S.WARN)
            q = VGroup(q1, q2, q3).arrange(DOWN, buff=0.35)
            self.play(FadeOut(m), FadeOut(recap), run_time=0.6)
            self.play(FadeIn(q1), FadeIn(q2), run_time=1.0)
            self.play(FadeIn(q3, shift=UP * 0.1), run_time=0.8)


# ================================================================== 2. hook
class Vek02Hook(NarratedScene):
    EPISODE = EP

    def construct(self):
        h = heading("f32-vmax: one input, two outputs")
        a = code_panel(example("01_vmax_neon_A_core.c"), "c", title="A · original NEON (XNNPACK, via SALTy-rn)",
                       max_width=8.3)
        b = code_panel(example("02_vmax_rvv_Bopt_core.c"), "c", title="Bopt · LLM-optimised RVV",
                       max_width=8.3)
        a.to_edge(LEFT, buff=0.45).shift(UP * 1.25)
        b.to_edge(LEFT, buff=0.45).shift(DOWN * 1.55)
        b.align_to(a, LEFT)
        with self.beat("Vek02Hook-1"):
            self.play(FadeIn(h), run_time=0.6)
            self.play(FadeIn(a, shift=RIGHT * 0.2), run_time=1.0)
            self.play(Create(ha := highlight_lines(a, 4, color=S.INFO)), run_time=0.6)
        with self.beat("Vek02Hook-2"):
            self.play(FadeIn(b, shift=RIGHT * 0.2), run_time=1.0)
            self.play(Create(hb := highlight_lines(b, 4, color=S.INFO)), run_time=0.6)
        with self.beat("Vek02Hook-3"):
            inp = state_table([("a[0]", "0x7fc12345  NaN"), ("b[0]", "0x3f800000  1.0")], title="input, n = 1")
            inp.move_to([4.6, 1.5, 0])
            self.play(FadeIn(inp, shift=LEFT * 0.2), run_time=0.9)
        with self.beat("Vek02Hook-4"):
            out = state_table([("A", "0x7fc12345  NaN"), ("Bopt", "0x3f800000  1.0")], title="output[0]",
                              val_color=S.BAD)
            out.next_to(inp, DOWN, buff=0.35).align_to(inp, LEFT)
            neq = badge("A ≠ Bopt", S.BAD).next_to(out, DOWN, buff=0.3)
            self.play(FadeIn(out, shift=LEFT * 0.2), ha.animate.set_color(S.BAD), hb.animate.set_color(S.BAD),
                      run_time=1.0)
            self.play(FadeIn(neq, scale=1.2), run_time=0.6)
        with self.beat("Vek02Hook-5"):
            note = T("QEMU at VLEN 128 / 256 / 512\ninputs swapped: same difference", size=S.SMALL_SIZE - 2,
                     color=S.MUTED, line_spacing=1.1).next_to(neq, DOWN, buff=0.25)
            note.set_x(neq.get_x())
            c = cite("repo: research/project-plan-20261102/final-minmax-reproduction/README.zh-CN.md; "
                     "research/bugs/divergences/DIV-001")
            self.play(FadeIn(note), FadeIn(c), run_time=0.8)


# ================================================================== 3. lanes
class Vek03Lanes(NarratedScene):
    EPISODE = EP

    def construct(self):
        h = heading("SIMD: one instruction, many lanes")
        ra = lane_row(["NaN", "a1", "a2", "a3"])
        rb = lane_row(["1.0", "b1", "b2", "b3"])
        la = T("va", size=S.BODY_SIZE, mono=True, color=S.MUTED)
        lb = T("vb", size=S.BODY_SIZE, mono=True, color=S.MUTED)
        ra.move_to([-2.4, 1.9, 0])
        rb.move_to([-2.4, 1.0, 0])
        la.next_to(ra, LEFT, buff=0.3)
        lb.next_to(rb, LEFT, buff=0.3)
        lanes_lab = VGroup(*[T(f"lane {i}", size=S.CITE_SIZE, color=S.MUTED).next_to(ra[i], UP, buff=0.1)
                             for i in range(4)])
        neon = T("NEON: fixed 128-bit\nregister = 4 × f32", size=S.SMALL_SIZE, color=S.MUTED, line_spacing=1.1)
        neon.next_to(VGroup(ra, rb), RIGHT, buff=0.5)
        with self.beat("Vek03Lanes-1"):
            self.play(FadeIn(h), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(x) for x in ra], lag_ratio=0.15), FadeIn(la), FadeIn(lanes_lab),
                      run_time=1.2)
            self.play(FadeIn(rb), FadeIn(lb), FadeIn(neon), run_time=0.8)
        with self.beat("Vek03Lanes-2"):
            op = T("vacc = vmaxq_f32(va, vb);", size=S.SMALL_SIZE + 2, mono=True, color=S.INFO)
            ro = lane_row(["?", "max", "max", "max"], color=S.INFO)
            ro.next_to(rb, DOWN, buff=0.75).align_to(ra, LEFT)
            op.next_to(VGroup(rb, ro), RIGHT, buff=0.5)
            lo = T("vacc", size=S.BODY_SIZE, mono=True, color=S.MUTED).next_to(ro, LEFT, buff=0.3)
            arrows = VGroup(*[Arrow(rb[i].get_bottom(), ro[i].get_top(), buff=0.05, stroke_width=2,
                                    color=S.MUTED, max_tip_length_to_length_ratio=0.12) for i in range(4)])
            self.play(FadeIn(op), run_time=0.6)
            self.play(LaggedStart(*[GrowArrow(x) for x in arrows], lag_ratio=0.15), run_time=0.9)
            self.play(LaggedStart(*[FadeIn(x) for x in ro], lag_ratio=0.15), FadeIn(lo), run_time=0.9)
        with self.beat("Vek03Lanes-3"):
            rv = lane_row([""] * 8, color=ACC, w=0.7)
            rv.move_to([-0.9, -2.55, 0])
            rvl = T("RVV: VLEN bits, set by the chip", size=S.SMALL_SIZE, color=S.MUTED).next_to(rv, RIGHT, buff=0.3)
            rvv = T("vl = vsetvl(n)", size=S.SMALL_SIZE, mono=True, color=ACC).next_to(rv, UP, buff=0.12)
            rvv.align_to(rv, LEFT)
            self.play(FadeIn(rv), FadeIn(rvl), run_time=0.9)
            self.play(FadeIn(rvv), Indicate(rv, color=ACC, scale_factor=1.03), run_time=1.0)
        with self.beat("Vek03Lanes-4"):
            self.play(FadeOut(VGroup(rv, rvl, rvv)), run_time=0.5)
            dim = VGroup(*[g[i] for g in (ra, rb, ro) for i in (1, 2, 3)], arrows[1:], lanes_lab[1:])
            self.play(dim.animate.set_opacity(0.25), ra[0][0].animate.set_stroke(S.BAD, 4),
                      rb[0][0].animate.set_stroke(S.BAD, 4), run_time=0.8)
            outA = lane_box("NaN", S.BAD)
            outB = lane_box("1.0", S.BAD)
            la2 = T("A, NEON FMAX", size=S.SMALL_SIZE, color=S.INK)
            lb2 = T("Bopt, RVV vfmax", size=S.SMALL_SIZE, color=S.INK)
            pair = VGroup(VGroup(outA, la2).arrange(RIGHT, buff=0.25),
                          VGroup(outB, lb2).arrange(RIGHT, buff=0.25)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            pair.next_to(ro[0], DOWN, buff=0.45).align_to(ro[0], LEFT)
            self.play(ReplacementTransform(ro[0].copy(), pair), run_time=1.0)


# ================================================================== 4. resolve
class Vek04Resolve(NarratedScene):
    EPISODE = EP

    def construct(self):
        h = heading("Why they differ, and what Vekto does with it")
        with self.beat("Vek04Resolve-1"):
            pn = code_panel(example("03_fmax_lane_models.v", 1), "coq", title="NEON FMAX · NeonLib.v", max_width=9.6)
            pr = code_panel(example("03_fmax_lane_models.v", 2), "coq", title="RVV vfmax · RvvModel.v", max_width=9.6)
            VGroup(pn, pr).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(LEFT, buff=0.45).shift(DOWN * 0.25)
            ln = T("Arm FMAX:\nNaN propagates", size=S.SMALL_SIZE + 2, color=S.INFO, line_spacing=1.1)
            lr = T("maximumNumber:\none NaN is ignored", size=S.SMALL_SIZE + 2, color=S.INFO, line_spacing=1.1)
            ln.next_to(pn, RIGHT, buff=0.4)
            lr.next_to(pr, RIGHT, buff=0.4)
            c = cite("repo: build/e2e3-workers-20261106/intrinsics-v1.7.3/neon/NeonLib.v:87-89,105-107; rvv/RvvModel.v:62-64")
            self.play(FadeIn(h), FadeIn(pn), FadeIn(c), run_time=0.9)
            self.play(Create(highlight_lines(pn, 3, 6, color=S.INFO)), FadeIn(ln), run_time=0.8)
            self.play(FadeIn(pr), run_time=0.7)
            self.play(Create(highlight_lines(pr, 2, 3, color=S.INFO)), FadeIn(lr), run_time=0.8)
        with self.beat("Vek04Resolve-2"):
            self.play(*[FadeOut(m) for m in self.mobjects if m is not h], run_time=0.6)
            t = T("Counterexample triage (L1)", size=S.BODY_SIZE, color=S.MUTED).next_to(h, DOWN, buff=0.45)
            r1 = VGroup(T("Can the input occur?", size=S.BODY_SIZE - 2),
                        T("yes: no NaN check on the XNNPACK call path", size=S.SMALL_SIZE + 2, color=S.MUTED)
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            r2 = VGroup(T("Which side deviates?", size=S.BODY_SIZE - 2),
                        T("no reference: min/max NaN behaviour not guaranteed (XNNPACK #441)",
                          size=S.SMALL_SIZE + 2, color=S.MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            rows = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(t, DOWN, buff=0.4)
            rows.set_x(0)
            t.align_to(rows, LEFT)
            c = cite("repo: research/project-plan-20261102/LESSONS.zh-CN.md (L1, L3); "
                     "research/bugs/divergences/DIV-001-f32-vmax-nan.zh-CN.md")
            self.play(FadeIn(t), FadeIn(c), run_time=0.6)
            self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.8)
            self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.8)
        with self.beat("Vek04Resolve-3"):
            m1 = badge("main result:  A ≠ Bopt   (DIV-001)", S.BAD).scale(1.25)
            m1.next_to(rows, DOWN, buff=0.6).align_to(rows, LEFT)
            self.play(FadeIn(m1, shift=UP * 0.1), run_time=0.8)
        with self.beat("Vek04Resolve-4"):
            m2 = badge("conditional:  A ≡ Bopt under C-001 (no NaN inputs)", S.WARN).scale(1.25)
            m2.next_to(m1, DOWN, buff=0.3).align_to(m1, LEFT)
            n2 = T("counted separately · recorded as passed + rechecked · early evidence not re-runnable here",
                   size=S.SMALL_SIZE - 2, color=S.MUTED).next_to(m2, DOWN, buff=0.15).align_to(m2, LEFT)
            c2 = cite("repo: research/project-plan-20261102/CONDITIONS.zh-CN.md row C-001; SUMMARY-20261111.zh-CN.md §2")
            self.play(FadeIn(m2, shift=UP * 0.1), run_time=0.8)
            self.play(FadeIn(n2), Transform(c, c2), run_time=0.6)
        with self.beat("Vek04Resolve-5"):
            self.play(*[FadeOut(m) for m in self.mobjects if m is not h], run_time=0.6)
            rep_src = example("04_vmax_bopt_nan_repair.c")
            one = code_panel(rep_src.splitlines()[0], "c", title="Bopt", max_width=12.6)
            full = code_panel(rep_src, "c", title="Bopt, NaN-repaired (candidate)", max_width=12.6)
            full.move_to([0, 0.9, 0])
            one.move_to(full).align_to(full, UP)
            self.play(FadeIn(one), run_time=0.6)
            self.play(ReplacementTransform(one, full), run_time=1.2)
            hl = highlight_lines(full, 2, 5, color=S.WARN)
            cost = T("+18.8 % cycles", size=S.HEADING_SIZE, weight="BOLD", color=S.WARN)
            sub = T("geometric mean over 7 sizes, Saturn RTL · tested, not proved", size=S.SMALL_SIZE,
                    color=S.MUTED)
            VGroup(cost, sub).arrange(DOWN, buff=0.15).next_to(full, DOWN, buff=0.5)
            c3 = cite("repo: research/project-plan-20261102/vmax-performance/REPORT.zh-CN.md (结论); repair.patch")
            self.play(Create(hl), run_time=0.6)
            self.play(FadeIn(cost, scale=1.1), FadeIn(sub), FadeIn(c3), run_time=0.9)


# ================================================================== 5. testing
class Vek05Testing(NarratedScene):
    EPISODE = EP

    def construct(self):
        h = heading("Why passing checks are not enough")

        def row(num, text, note):
            n = T(num, size=S.BODY_SIZE, weight="BOLD", color=S.BAD)
            t = T(text, size=S.SMALL_SIZE + 3)
            s = T(note, size=S.CITE_SIZE, color=S.MUTED)
            body = VGroup(t, s).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            return VGroup(n, body).arrange(RIGHT, buff=0.35, aligned_edge=UP)

        r1 = row("1", "Test buffers replace NaN with 0: the NaN assertion never fires",
                 "research/bugs/xnnpack/XNN-005-f32-vexp-nan-clamp/README.zh-CN.md (supplement)")
        r2 = row("2", "QEMU keeps RVV tail lanes unchanged: a tail-lane bug stays hidden",
                 "research/bugs/xnnpack/XNN-003-s8u8-rminmax-rvv-tail-agnostic/README.zh-CN.md:20")
        r3 = row("3", "An earlier bounded checker said VERIFIED: its NEON model ignored NaN",
                 "research/project-plan-20261102/final-minmax-reproduction/README.zh-CN.md")
        rows = VGroup(r1, r2, r3).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(h, DOWN, buff=0.5)
        rows.set_x(0)
        with self.beat("Vek05Testing-1"):
            self.play(FadeIn(h), run_time=0.6)
        with self.beat("Vek05Testing-2"):
            self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.8)
        with self.beat("Vek05Testing-3"):
            self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.8)
        with self.beat("Vek05Testing-4"):
            self.play(FadeIn(r3, shift=UP * 0.1), run_time=0.8)
            d = code_panel(example("05_bounded_checker_patch.diff"), "diff",
                           title="patch to the checker's NEON model",
                           font_size=S.CODE_FONT_SIZE - 2, max_width=9.0, max_height=2.4)
            d.next_to(rows, DOWN, buff=0.35).to_edge(LEFT, buff=0.5)
            v = badge("VERIFIED", S.MUTED)
            x = badge("COUNTEREXAMPLE", S.BAD)
            VGroup(v, x).arrange(DOWN, buff=0.3).to_edge(RIGHT, buff=0.5).set_y(d.get_y())
            strike = Line(v.get_left(), v.get_right(), color=S.BAD, stroke_width=3)
            self.play(FadeIn(v), run_time=0.5)
            self.play(FadeIn(d), run_time=0.8)
            self.play(Create(strike), FadeIn(x, shift=UP * 0.1), run_time=0.8)
        with self.beat("Vek05Testing-5"):
            self.play(*[FadeOut(m) for m in self.mobjects if m is not h], run_time=0.6)
            goal = VGroup(
                T("Goal", size=S.SMALL_SIZE, color=ACC, weight="BOLD"),
                T("“establish equivalence for all inputs permitted", size=S.BODY_SIZE + 2),
                T("by the preconditions in the spec”", size=S.BODY_SIZE + 2),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(UP * 0.5)
            vero = T("Vero's lesson: the model and the spec decide what a verdict means",
                     size=S.SMALL_SIZE + 2, color=S.ACCENT["vero"]).next_to(goal, DOWN, buff=0.7)
            c = cite("repo: research/project-plan-20261102/intro-bullets/v2-preconditions.md ¶3 (Intro V2, draft)")
            self.play(FadeIn(goal), FadeIn(c), run_time=1.0)
            self.play(FadeIn(vero, shift=UP * 0.1), run_time=0.8)


# ================================================================== 6. level
class Vek06Level(NarratedScene):
    EPISODE = EP

    def construct(self):
        h = heading("Where should the proof live?")

        def col(title, sub, edge=S.PANEL_EDGE):
            r = card(3.9, 1.5, edge=edge)
            g = VGroup(T(title, size=S.BODY_SIZE - 2, weight="BOLD"), T(sub, size=S.SMALL_SIZE, color=S.MUTED))
            g.arrange(DOWN, buff=0.12)
            if g.width > 3.6:
                g.scale_to_fit_width(3.6)
            g.move_to(r)
            return VGroup(r, g)

        cols = VGroup(col("Assembly / ISA", "Sail, Islaris"), col("Compiler IR", "Alive2, Rake"),
                      col("C + intrinsic contracts", "Vekto")).arrange(RIGHT, buff=0.4).shift(UP * 1.1)
        c = cite("repo: research/project-plan-20261102/intro-bullets/v2-preconditions.md ¶4–5 (Intro V2, draft)")
        with self.beat("Vek06Level-1"):
            self.play(FadeIn(h), FadeIn(c), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.15) for x in cols], lag_ratio=0.3), run_time=1.4)
        with self.beat("Vek06Level-2"):
            pts = bullet_list(["separate NEON / RVV models", "+ a correspondence", "+ exceptions, privileged mode"],
                              size=S.SMALL_SIZE - 2, color=S.WARN, buff=0.15)
            pts.next_to(cols[0], DOWN, buff=0.4).align_to(cols[0], LEFT).shift(RIGHT * 0.15)
            self.play(cols[0][0].animate.set_stroke(S.WARN, 3), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.3), run_time=1.4)
        with self.beat("Vek06Level-3"):
            pc = bullet_list(["each intrinsic: a C definition", "numbers + memory behaviour",
                              "reviewed against ISA docs"], size=S.SMALL_SIZE - 2, color=ACC, buff=0.15)
            pc.next_to(cols[2], DOWN, buff=0.4).align_to(cols[2], LEFT)
            self.play(cols[2][0].animate.set_stroke(ACC, 5), cols[0].animate.set_opacity(0.45),
                      pts.animate.set_opacity(0.45), cols[1].animate.set_opacity(0.45), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(p) for p in pc], lag_ratio=0.3), run_time=1.2)


# ================================================================== 7. pipeline
class Vek07Pipeline(NarratedScene):
    EPISODE = EP

    def construct(self):
        y0, yt, yb, yc = 0.55, 2.4, -1.2, -2.65
        nodes = [
            {"id": "impl", "label": "impl/", "sub": "original A, B", "pos": [-5.75, y0], "w": 2.2, "h": 0.95},
            {"id": "rule", "label": "rule tool", "sub": "deterministic rewrite", "pos": [-3.05, y0], "w": 2.3, "h": 0.95},
            {"id": "qcp", "label": "QCP", "sub": "symbolic execution", "pos": [-0.35, y0], "w": 2.3, "h": 0.95},
            {"id": "vcs", "label": "VCs", "sub": "verification conditions", "pos": [2.3, y0], "w": 2.3, "h": 0.95},
            {"id": "coq", "label": "Coq", "sub": "proofs by agents", "pos": [5.25, y0], "w": 2.3, "h": 0.95},
            {"id": "lib", "label": "intrinsic contracts", "sub": "one shared library", "pos": [-0.35, yt],
             "w": 2.9, "h": 0.95},
            {"id": "diff", "label": "differential tests", "sub": "native x86 · QEMU", "pos": [3.3, yt],
             "w": 2.9, "h": 0.95},
            {"id": "spec", "label": "spec.c", "sub": "equivalent(): human-reviewed", "pos": [-0.35, yb],
             "w": 2.9, "h": 0.95, "color": ACC},
            {"id": "gates", "label": "check.py", "sub": "12 gates → APPROVAL", "pos": [5.25, yb], "w": 2.3,
             "h": 0.95, "color": S.OK},
            {"id": "cex", "label": "counterexample", "sub": "replayed on originals", "pos": [3.45, yc], "w": 2.8,
             "h": 0.95, "color": S.BAD},
            {"id": "tri", "label": "L1/L3 triage", "sub": "condition · fix · divergence", "pos": [-0.35, yc],
             "w": 2.9, "h": 0.95, "color": S.WARN},
        ]
        edges = [
            {"from": "impl", "to": "rule"}, {"from": "rule", "to": "qcp"}, {"from": "qcp", "to": "vcs"},
            {"from": "vcs", "to": "coq"}, {"from": "lib", "to": "qcp"}, {"from": "diff", "to": "lib"},
            {"from": "spec", "to": "qcp"}, {"from": "coq", "to": "gates"},
            {"from": "vcs", "to": "cex", "color": S.BAD}, {"from": "cex", "to": "tri", "color": S.BAD},
            {"from": "tri", "to": "spec", "color": S.WARN},
        ]
        g = pipeline(nodes, edges)
        B, E = g.by_id, g.edge_by_id
        c = cite("repo: tools/rvv_ptr_lower/README.zh-CN.md; intrinsics-v1.7.3/INTRINSICS-COMMON.zh-CN.md")

        def show(*ids, edges_=()):
            anims = [FadeIn(B[i], shift=UP * 0.1) for i in ids]
            self.play(*anims, run_time=0.7)
            if edges_:
                self.play(*[GrowArrow(E[e]) for e in edges_], run_time=0.6)

        with self.beat("Vek07Pipeline-1"):
            self.play(FadeIn(heading("The Vekto pipeline")), FadeIn(c), run_time=0.5)
            show("impl")
        with self.beat("Vek07Pipeline-2"):
            show("rule", edges_=[("impl", "rule")])
            note = T("vector statements only · no LLM, no hand edits · unknown construct = reject",
                     size=S.CITE_SIZE + 1, color=S.MUTED).next_to(B["rule"], UP, buff=0.2)
            note.align_to(B["impl"], LEFT)
            self.play(FadeIn(note), run_time=0.6)
        with self.beat("Vek07Pipeline-3"):
            self.play(FadeOut(note), run_time=0.3)
            show("qcp", "vcs", "coq", edges_=[("rule", "qcp"), ("qcp", "vcs"), ("vcs", "coq")])
        with self.beat("Vek07Pipeline-4"):
            show("lib", "diff", edges_=[("diff", "lib"), ("lib", "qcp")])
        with self.beat("Vek07Pipeline-5"):
            show("spec", edges_=[("spec", "qcp")])
            self.play(Indicate(B["spec"], color=ACC, scale_factor=1.05), run_time=0.8)
        with self.beat("Vek07Pipeline-6"):
            show("gates", edges_=[("coq", "gates")])
        with self.beat("Vek07Pipeline-7"):
            show("cex", edges_=[("vcs", "cex")])
            show("tri", edges_=[("cex", "tri"), ("tri", "spec")])
            for i, col in (("vcs", S.BAD), ("cex", S.BAD), ("tri", S.WARN), ("spec", ACC)):
                self.play(B[i][0].animate.set_stroke(color=col, width=6), run_time=0.35)
                self.play(B[i][0].animate.set_stroke(width=2), run_time=0.2)


# ================================================================== 8. gates
GATES = [
    ("g1 identity", "sources byte-identical to upstream"),
    ("g2 lowering", "rule tool regenerates the rewrite"),
    ("g3 pins", "library, tool, Coq copies pinned"),
    ("g4 libs", "Coq libraries built from scratch"),
    ("g5 units", "QCP symbolic execution"),
    ("g6 proofs", "every VC Qed · axiom whitelist"),
    ("g7 equivalence", "equivalent() proved"),
    ("g8 contracts", "contract text equal everywhere"),
    ("g9 b1", "no vacuous goals (QCP-B1)"),
    ("g10 witness", "precondition satisfiable"),
    ("g11 closure", "every callee proved or pinned"),
    ("g12 difftests", "libraries + original kernels tested"),
]


def gate_grid() -> VGroup:
    rows = VGroup(*[gate_row(n, d) for n, d in GATES])
    left = VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
    right = VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
    VGroup(left, right).arrange(RIGHT, buff=0.6, aligned_edge=UP)
    return rows


class Vek08Gates(NarratedScene):
    EPISODE = EP

    def construct(self):
        h = heading("check.py: twelve gates, from an empty directory")
        rows = gate_grid()
        rows.next_to(h, DOWN, buff=0.75).set_x(0)
        if rows.width > 13.2:
            rows.scale_to_fit_width(13.2)
        c = cite("repo: build/e2e3-workers-20261106/w36-e2-transposec/work/pkg24/proof/check.py, docstring lines 4–17")

        def group(idx, color):
            sel = VGroup(*[rows[i] for i in idx])
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in sel], lag_ratio=0.2), run_time=0.9)
            box = SurroundingRectangle(sel, color=color, buff=0.12, corner_radius=0.08, stroke_width=2)
            self.play(Create(box), run_time=0.5)
            return box

        with self.beat("Vek08Gates-1"):
            self.play(FadeIn(h), FadeIn(c), run_time=0.6)
            b = group([0, 1, 2, 3], S.INFO)
        with self.beat("Vek08Gates-2"):
            self.play(FadeOut(b), run_time=0.3)
            b = group([4, 5, 6], S.INFO)
        with self.beat("Vek08Gates-3"):
            self.play(FadeOut(b), run_time=0.3)
            b = group([7, 8], ACC)
        with self.beat("Vek08Gates-4"):
            self.play(FadeOut(b), run_time=0.3)
            b = group([9, 10], ACC)
        with self.beat("Vek08Gates-5"):
            self.play(FadeOut(b), run_time=0.3)
            b = group([11], S.INFO)
            self.play(FadeOut(b), run_time=0.4)


# ================================================================== 9. walk-through
class Vek09Walk(NarratedScene):
    EPISODE = EP

    def construct(self):
        h = heading("Walk-through: x24-transposec, SSSE3 → RVV")
        src = code_panel(example("06_x24_source_ssse3.c"), "c",
                         title="source · XNNPACK SSSE3 (byte-identical)", max_width=9.2,
                         max_height=5.6)
        src.to_edge(LEFT, buff=0.45).shift(DOWN * 0.35)
        with self.beat("Vek09Walk-1"):
            self.play(FadeIn(h), run_time=0.5)
            self.play(FadeIn(src, shift=RIGHT * 0.2), run_time=1.0)
            c = cite("repo: build/e2e3-workers-20261106/w36-e2-transposec/work/pkg24/impl/")
            self.play(FadeIn(c), run_time=0.4)
        with self.beat("Vek09Walk-2"):
            h1 = highlight_lines(src, 2, 5, color=S.INFO)
            self.play(Create(h1), run_time=0.6)
            h2 = highlight_lines(src, 7, 9, color=S.INFO)
            self.play(ReplacementTransform(h1, h2), run_time=0.7)
            oob = tag("XNN_OOB_READS:\n16-byte loads\nmay over-read", S.WARN)
            oob.next_to(src, RIGHT, buff=0.3).set_y(highlight_lines(src, 2, 5).get_y())
            h3 = highlight_lines(src, 2, 5, color=S.WARN)
            self.play(ReplacementTransform(h2, h3), FadeIn(oob), run_time=0.8)
        with self.beat("Vek09Walk-3"):
            tgt = code_panel(example("07_x24_target_rvv.c"), "c", title="target · new RVV code (frozen)",
                             max_width=11.2, max_height=5.3)
            tgt.next_to(h, DOWN, buff=0.3).set_x(0)
            self.play(FadeOut(VGroup(src, h3, oob)), run_time=0.5)
            self.play(FadeIn(tgt, shift=RIGHT * 0.2), run_time=0.9)
            k1 = highlight_lines(tgt, 6, color=ACC)
            self.play(Create(k1), run_time=0.5)
            k2 = highlight_lines(tgt, 7, 8, color=ACC)
            self.play(ReplacementTransform(k1, k2), run_time=0.6)
            note = T("one column per pass; the strided segment load does the transpose", size=S.SMALL_SIZE,
                     color=ACC).next_to(tgt, DOWN, buff=0.2)
            self.play(FadeIn(note), run_time=0.5)
        with self.beat("Vek09Walk-4"):
            spec = code_panel(example("08_x24_spec_equivalent.c"), "c", title="spec.c · equivalent()  (trimmed)",
                              max_width=11.6, max_height=3.9)
            spec.next_to(h, DOWN, buff=0.3).set_x(0)
            self.play(FadeOut(VGroup(tgt, k2, note)), run_time=0.5)
            self.play(FadeIn(spec, shift=UP * 0.2), run_time=0.9)
            s1 = highlight_lines(spec, 12, 13, color=S.INFO)
            self.play(Create(s1), run_time=0.5)
        with self.beat("Vek09Walk-5"):
            t1, t2, t3 = tag("C-022  block ≥ 1×1"), tag("C-024  no address wrap"), tag("C-033  input window")
            tags = VGroup(t1, t2, t3).arrange(RIGHT, buff=0.35).next_to(spec, DOWN, buff=0.25)
            a1 = highlight_lines(spec, 5, color=S.WARN)
            a2 = highlight_lines(spec, 6, 7, color=S.WARN)
            a3 = highlight_lines(spec, 8, color=S.WARN)
            self.play(ReplacementTransform(s1, a1), FadeIn(t1), run_time=0.8)
            self.play(ReplacementTransform(a1, a2), FadeIn(t2), run_time=0.8)
            self.play(ReplacementTransform(a2, a3), FadeIn(t3), run_time=0.8)
            c2 = cite("repo: build/e2e3-workers-20261106/w36-e2-transposec/work/pkg24/spec.c; CONDITIONS.zh-CN.md")
            self.play(Transform(c, c2), run_time=0.4)
        with self.beat("Vek09Walk-6"):
            o = highlight_lines(spec, 10, color=ACC)
            to = tag("outputs_related: equal on every byte a transpose writes", ACC)
            to.next_to(tags, DOWN, buff=0.15)
            self.play(ReplacementTransform(a3, o), FadeIn(to), run_time=0.8)


# ================================================================== 10. results
class Vek10Results(NarratedScene):
    EPISODE = EP

    def construct(self):
        h = heading("x24-transposec: supervisor recheck")
        c = cite("repo: build/e2e3-workers-20261106/w36-e2-transposec/APPROVAL-x24-rvv.json; "
                 "rechecks/w36x24/run/status.json")
        with self.beat("Vek10Results-1"):
            chips = VGroup(*[badge(f"g{i}", S.OK) for i in range(1, 13)]).arrange(RIGHT, buff=0.18)
            chips.next_to(h, DOWN, buff=0.55)
            res = T("RESULT: PASS   ·   12 / 12 gates   ·   5,990 s", size=S.BODY_SIZE, weight="BOLD", color=S.OK)
            res.next_to(chips, DOWN, buff=0.35)
            self.play(FadeIn(h), FadeIn(c), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(x, scale=1.2) for x in chips], lag_ratio=0.08), run_time=1.4)
            self.play(FadeIn(res), run_time=0.6)

        def tile(num, lab):
            n = T(num, size=S.TITLE_SIZE, weight="BOLD", color=S.INK)
            l = T(lab, size=S.SMALL_SIZE, color=S.MUTED)
            g = VGroup(n, l).arrange(DOWN, buff=0.12)
            r = card(g.width + 0.7, g.height + 0.45)
            r.move_to(g)
            return VGroup(r, g)

        with self.beat("Vek10Results-2"):
            t1 = tile("435", "x86 VCs, all Qed")
            t2 = tile("22 per VLEN", "RVV VCs at VLEN 128 / 256 / 512")
            tiles = VGroup(t1, t2).arrange(RIGHT, buff=0.6).next_to(res, DOWN, buff=0.5)
            self.play(FadeIn(t1, shift=UP * 0.1), run_time=0.7)
            self.play(FadeIn(t2, shift=UP * 0.1), run_time=0.7)
        with self.beat("Vek10Results-3"):
            self.play(FadeOut(tiles), run_time=0.4)
            a = bullet_list(["fixed VLEN 128 / 256 / 512 bits, not arbitrary VLEN",
                             "C-022 block ≥ 1×1   ·   C-024 no address wrap",
                             "C-031 window ≤ INT64_MAX   ·   C-033 input window (XNN_OOB_READS)"],
                            size=S.SMALL_SIZE + 2, color=S.WARN, buff=0.2)
            lab = T("assumptions", size=S.SMALL_SIZE, color=S.WARN, weight="BOLD")
            blk = VGroup(lab, a).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(res, DOWN, buff=0.45)
            blk.set_x(0)
            self.play(FadeIn(lab), LaggedStart(*[FadeIn(x) for x in a], lag_ratio=0.35), run_time=1.6)
        with self.beat("Vek10Results-4"):
            g = bullet_list(["G-004 partial correctness only",
                             "G-002 intrinsics = reviewed contracts + differential tests, no formal ISA proof",
                             "modelling: 6 const tables 16-byte aligned · assert() off (NDEBUG)"],
                            size=S.SMALL_SIZE + 2, color=S.WARN, buff=0.2)
            g.next_to(blk, DOWN, buff=0.25).align_to(blk, LEFT)
            c2 = cite("repo: APPROVAL-x24-rvv.json (conditions); research/project-plan-20261102/CONDITIONS.zh-CN.md G-rows")
            self.play(FadeIn(g), Transform(c, c2), run_time=0.9)
        with self.beat("Vek10Results-5"):
            e = T("out-of-domain edge cases: 14 of 25 differ (e.g. block_width = 0), excluded by C-022",
                  size=S.SMALL_SIZE + 1, color=S.BAD)
            e.next_to(g, DOWN, buff=0.35).align_to(blk, LEFT)
            if e.width > 13:
                e.scale_to_fit_width(13)
            self.play(FadeIn(e, shift=UP * 0.1), run_time=0.8)


# ================================================================== 11. status
class Vek11Status(NarratedScene):
    EPISODE = EP

    def construct(self):
        h = heading("Experiments E1–E4, status as of 2026-11-23")
        rows = [
            status_row("E1", "original NEON A vs LLM-optimised RVV Bopt (35 pairs)", [("IN PROGRESS", S.WARN)],
                       "17 approval records in the current batch; most: main result A ≠ Bopt"),
            status_row("E2", "translate x86 ops that RVV / HVX lack, and prove it",
                       [("ESTABLISHED: 24", S.OK), ("IN PROGRESS", S.WARN)],
                       "24 approved migrations (supervisor log); x64 → HVX in progress"),
            status_row("E3", "cross-check independent XNNPACK implementations",
                       [("ESTABLISHED: 15", S.OK), ("IN PROGRESS", S.WARN)],
                       "as of 11-11: 14 pairs approved, 1 proved not equivalent, 3 not started"),
            status_row("E4", "one application-level program (softmax candidate)", [("NOT STARTED", S.MUTED)],
                       "no program-level result yet"),
        ]
        for i, r in enumerate(rows):
            r.shift(UP * (1.85 - i * 1.35))
        cites = [
            "repo: build/e1-codex-20261111/c*/APPROVAL*.json (17 files); EXPERIMENT-DESIGN.zh-CN.md (E1)",
            "repo: research/project-plan-20261102/DECISIONS-FOR-REVIEW.zh-CN.md, 11-23 04:05 and 14:20 entries",
            "repo: research/project-plan-20261102/SUMMARY-20261111.zh-CN.md §2.2",
            "repo: research/project-plan-20261102/SUMMARY-20261111.zh-CN.md §2; EXPERIMENT-DESIGN.zh-CN.md (E4)",
        ]
        c = cite(cites[0])

        def reveal(i):
            if i == 0:
                self.play(FadeIn(h), FadeIn(c), FadeIn(rows[0], shift=UP * 0.1), run_time=0.9)
            else:
                self.play(FadeIn(rows[i], shift=UP * 0.1), Transform(c, cite(cites[i])), run_time=0.9)

        with self.beat("Vek11Status-1"):
            reveal(0)
        with self.beat("Vek11Status-2"):
            reveal(1)
        with self.beat("Vek11Status-3"):
            reveal(2)
        with self.beat("Vek11Status-4"):
            reveal(3)


# ================================================================== 12. close
class Vek12Close(NarratedScene):
    EPISODE = EP

    def construct(self):
        with self.beat("Vek12Close-1"):
            h = heading("What Vekto does not claim")
            lst = bullet_list(["termination (partial correctness, G-004); C-to-machine-code correspondence",
                               "Hexagon modelled as LP64, though it is ILP32 (M-ilp32)",
                               "in-place calls: not covered (C-018)",
                               "bugs found: confirmed candidates, not yet reported upstream"],
                              size=S.SMALL_SIZE + 3, color=S.WARN, buff=0.35)
            lst.next_to(h, DOWN, buff=0.7).set_x(0)
            c = cite("repo: research/project-plan-20261102/CONDITIONS.zh-CN.md (G-004, VEKTO-M-ilp32, C-018); "
                     "research/bugs/xnnpack/")
            self.play(FadeIn(h), FadeIn(c), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in lst], lag_ratio=0.4), run_time=2.2)
        with self.beat("Vek12Close-2"):
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            m = series_map(None).shift(UP * 0.6)
            nodes = m[0]
            caps = ["a program state", "a learned\nexplanation", "an audit of\na spec",
                    "an input where two\nkernels disagree"]
            labs = VGroup(*[T(t, size=S.SMALL_SIZE - 1, color=S.EPISODES[i][3], line_spacing=1.1)
                            .next_to(nodes[i], DOWN, buff=0.3) for i, t in enumerate(caps)])
            head = T("what the counterexample was", size=S.SMALL_SIZE, color=S.MUTED).next_to(nodes, UP, buff=0.4)
            self.play(FadeIn(m[0]), FadeIn(m[1]), FadeIn(head), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in labs], lag_ratio=0.5), run_time=2.4)
        with self.beat("Vek12Close-3"):
            trust = T("every proof re-checked  ·  no spec silently weakened  ·  every assumption stated",
                      size=S.SMALL_SIZE + 2, color=S.INK).next_to(labs, DOWN, buff=0.7)
            if trust.width > 13:
                trust.scale_to_fit_width(13)
            self.play(FadeIn(trust, shift=UP * 0.1), run_time=1.0)
