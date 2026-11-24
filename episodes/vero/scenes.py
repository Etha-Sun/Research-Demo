"""Episode 3: Vero -- verified software at repository scale (Lean 4).

Scenes (order = narration.json):
  Vero01Open, Vero02Hook, Vero03Instance, Vero04Scale, Vero05Architecture, Vero06Grader,
  Vero07Base64, Vero08Audit, Vero09Trust, Vero10Results, Vero11Limits, Vero12Bridge

All code on screen is loaded from episodes/vero/examples/ (header comment = exact source).
Sources for every number: episodes/vero/SOURCES.md.
"""
from __future__ import annotations

from pathlib import Path

from manim import (
    DOWN, LEFT, RIGHT, UP, ORIGIN, UR,
    Arrow, Circle, Create, DashedLine, Dot, FadeIn, FadeOut, GrowArrow, GrowFromEdge, Indicate,
    Line, Rectangle, ReplacementTransform, TransformFromCopy, VGroup, Write, LaggedStart,
)

from common import style as S
from common.components import (
    NarratedScene, T, cite, card, title_card, series_map, pipeline, animate_pipeline, pulse_path,
    code_panel, highlight_lines, state_table, bar_chart, badge, bullet_list,
)

EP = "vero"
ACC = S.ACCENT[EP]
EX = Path(__file__).resolve().parent / "examples"

PAPER = "Vero paper (arXiv 2608.13522)"
REPO = "repo sunblaze-ucb/vero@0a7325d"


def load(name: str) -> str:
    """Example file without its leading source-header comment lines."""
    lines = (EX / name).read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines) and (lines[i].startswith("--") or lines[i].startswith("#")):
        i += 1
    return "\n".join(lines[i:]).strip("\n")


def label_tag(text: str, color: str = S.WARN) -> "VGroup":
    """Small coloured tag such as 'illustrative (paper p.20)'. Local helper (badge with smaller text)."""
    return badge(text, color)


def CurvedArrowLink(a, b):
    """Thin arc above a row of boxes from a to b (dependency hint). Local helper."""
    from manim import ArcBetweenPoints
    return ArcBetweenPoints(a.get_top() + UP * 0.05, b.get_top() + UP * 0.05, angle=-0.9 if a.get_x() < b.get_x() else 0.9,
                            color=S.PANEL_EDGE, stroke_width=2)


# ====================================================================== 1
class Vero01Open(NarratedScene):
    EPISODE = EP

    def construct(self):
        m = series_map(current=EP).scale(0.9).shift(UP * 0.6)
        recap = T("So far: repair one proof at a time", size=S.SMALL_SIZE + 2, color=S.MUTED)
        recap.next_to(m, DOWN, buff=0.6)
        with self.beat("vero01open-1"):
            self.play(FadeIn(m[0], lag_ratio=0.2), FadeIn(m[1]), run_time=1.5)
            self.play(FadeIn(m[2]), FadeIn(recap, shift=UP * 0.1), run_time=0.8)
            self.play(m[0][2][0].animate.set_stroke(width=6), run_time=0.5)
        tc = title_card(EP, 3, extra="Ye, Lou, Sun, Song, Yan, Kasriel, Zhang, Yang, Kong, He, Song · NeurIPS 2026")
        with self.beat("vero01open-2"):
            self.play(FadeOut(m), FadeOut(recap), run_time=0.6)
            self.play(FadeIn(tc, shift=UP * 0.2), run_time=1.0)
            q = T("Can AI agents build formally verified repositories?", size=S.SMALL_SIZE + 2, color=ACC)
            q.next_to(tc, DOWN, buff=0.5)
            self.play(FadeIn(q), run_time=0.6)


# ====================================================================== 2
class Vero02Hook(NarratedScene):
    EPISODE = EP

    def construct(self):
        head = T("One spec from the benchmark: dijkstar", size=S.HEADING_SIZE - 6, weight="BOLD")
        head.to_edge(UP, buff=0.5)
        p = code_panel(load("hook_dijkstar_spec.lean"), "lean", title="Dijkstar/Spec/ShortestPath.lean")
        p.move_to(UP * 0.4)
        src = cite(f"{REPO}, benchmarks/dijkstar/Dijkstar/Spec/ShortestPath.lean:200-203")
        with self.beat("vero02hook-1"):
            self.play(FadeIn(head), run_time=0.6)
            self.play(FadeIn(p, shift=UP * 0.2), FadeIn(src), run_time=1.0)
        with self.beat("vero02hook-2"):
            h1 = highlight_lines(p, 3, color=S.INFO)
            self.play(Create(h1), run_time=0.6)
            self.wait(2.2)
            h2 = highlight_lines(p, 4, color=ACC)
            self.play(ReplacementTransform(h1, h2), run_time=0.6)
            gloss = T("returned cost  ≤  cost of every walk s → t", size=S.SMALL_SIZE + 2, color=ACC)
            gloss.next_to(p, DOWN, buff=0.4)
            self.play(FadeIn(gloss), run_time=0.5)
        with self.beat("vero02hook-3"):
            self.play(FadeOut(gloss), FadeOut(h2), FadeOut(head),
                      p.animate.scale(0.85).to_edge(UP, buff=0.4), run_time=0.8)
            # many specs across modules: a schematic row of module boxes (folder names as in the repo layout)
            mods = VGroup()
            for n in ["Impl/", "Spec/", "Proof/", "Harness", "helpers", "Test"]:
                box = card(1.7, 0.75, edge=S.PANEL_EDGE)
                mods.add(VGroup(box, T(n, size=S.SMALL_SIZE, color=S.MUTED, mono=True).move_to(box)))
            mods.arrange(RIGHT, buff=0.3).move_to(DOWN * 0.25)
            links = VGroup(*[CurvedArrowLink(mods[a], mods[b]) for a, b in [(2, 1), (1, 0), (2, 4)]])
            sch = T("schematic", size=S.CITE_SIZE, color=S.MUTED).next_to(mods, DOWN, buff=0.15).align_to(mods, RIGHT)
            self.play(LaggedStart(*[FadeIn(g) for g in mods], lag_ratio=0.15), run_time=1.0)
            self.play(Create(links), FadeIn(sch), run_time=0.8)
            self.play(mods[0][0].animate.set_stroke(color=ACC, width=4), mods[2][0].animate.set_stroke(color=ACC, width=4),
                      run_time=0.6)
        with self.beat("vero02hook-4"):
            q = T("Can an agent implement and prove\nthis across many modules?", size=S.HEADING_SIZE - 6, color=ACC,
                  weight="BOLD", line_spacing=0.9)
            q.to_edge(DOWN, buff=0.9)
            self.play(Write(q), run_time=1.4)


# ====================================================================== 3
class Vero03Instance(NarratedScene):
    EPISODE = EP

    def construct(self):
        head = T("A Vero instance (paper Fig. 2)", size=S.HEADING_SIZE - 6, weight="BOLD").to_edge(UP, buff=0.45)
        p1 = code_panel(load("fig2_interface.lean"), "lean", title="interface (frozen)", max_height=5.8, max_width=8.3)
        p1.to_edge(LEFT, buff=0.4).shift(DOWN * 0.35)
        src = cite(f"{PAPER}, Fig. 2, p.5")
        notes = VGroup()

        def note(text, color, anchor):
            n = T(text, size=S.SMALL_SIZE, color=color)
            n.next_to(p1, RIGHT, buff=0.3).match_y(anchor)
            return n

        with self.beat("vero03instance-1"):
            self.play(FadeIn(head), FadeIn(src), run_time=0.6)
            self.play(FadeIn(p1, shift=UP * 0.2), run_time=0.9)
            h = highlight_lines(p1, 1, 3, color=S.MUTED)
            n1 = note("API signatures: frozen", S.MUTED, h)
            self.play(Create(h), FadeIn(n1), run_time=0.7)
            notes.add(h, n1)
        with self.beat("vero03instance-2"):
            h2 = highlight_lines(p1, 5, 8, color=S.INFO)
            n2 = note("RepoImpl: one field per API", S.INFO, h2)
            self.play(Create(h2), FadeIn(n2), run_time=0.7)
            self.wait(1.0)
            h3 = highlight_lines(p1, 10, 14, color=ACC)
            n3 = note("canonical: what gets graded", ACC, h3)
            self.play(Create(h3), FadeIn(n3), run_time=0.7)
            notes.add(h2, n2, h3, n3)
        p2 = code_panel(load("fig2_spec.lean"), "lean", title="spec + proof obligation")
        p2.move_to(DOWN * 0.2)
        with self.beat("vero03instance-3"):
            self.play(FadeOut(notes), FadeOut(p1), run_time=0.6)
            self.play(FadeIn(p2, shift=UP * 0.2), run_time=0.8)
            hs = highlight_lines(p2, 1, 4, color=S.INFO)
            self.play(Create(hs), run_time=0.6)
            self.wait(1.6)
            hp = highlight_lines(p2, 7, color=S.BAD)
            tag = T("agent fills this", size=S.SMALL_SIZE + 2, color=S.BAD).next_to(hp, RIGHT, buff=0.3)
            self.play(ReplacementTransform(hs, hp), FadeIn(tag), run_time=0.7)
        # two modes
        po = VGroup(card(5.6, 2.3, edge=S.INFO),
                    VGroup(T("Proof-only", size=S.BODY_SIZE, weight="BOLD"),
                           T("canonical = reference code", size=S.SMALL_SIZE, color=S.MUTED),
                           T("agent proves every spec", size=S.SMALL_SIZE, color=S.MUTED)).arrange(DOWN, buff=0.18))
        cp = VGroup(card(5.6, 2.3, edge=ACC),
                    VGroup(T("Code-and-proof", size=S.BODY_SIZE, weight="BOLD"),
                           T("canonical = agent's own code", size=S.SMALL_SIZE, color=S.MUTED),
                           T("agent writes code and proves", size=S.SMALL_SIZE, color=S.MUTED)).arrange(DOWN, buff=0.18))
        for g in (po, cp):
            g[1].move_to(g[0])
        modes = VGroup(po, cp).arrange(RIGHT, buff=0.6).move_to(DOWN * 0.3)
        msrc = cite(f"{PAPER}, §3.2, p.5")
        with self.beat("vero03instance-4"):
            self.play(FadeOut(p2), FadeOut(hp), FadeOut(tag), FadeOut(src), run_time=0.6)
            self.play(head.animate.become(T("Two task modes", size=S.HEADING_SIZE - 6, weight="BOLD").to_edge(UP, buff=0.45)),
                      FadeIn(po, shift=UP * 0.2), FadeIn(msrc), run_time=0.9)
        with self.beat("vero03instance-5"):
            self.play(FadeIn(cp, shift=UP * 0.2), run_time=0.8)
            warn = T("a code change can break proofs in other modules", size=S.SMALL_SIZE + 2, color=S.WARN)
            warn.next_to(modes, DOWN, buff=0.45)
            self.play(FadeIn(warn), run_time=0.6)


# ====================================================================== 4
class Vero04Scale(NarratedScene):
    EPISODE = EP

    def construct(self):
        head = T("The benchmark", size=S.HEADING_SIZE - 6, weight="BOLD").to_edge(UP, buff=0.45)

        def stat(num, lab, color=S.INK):
            return VGroup(T(num, size=S.TITLE_SIZE + 8, weight="BOLD", color=color),
                          T(lab, size=S.SMALL_SIZE + 2, color=S.MUTED)).arrange(DOWN, buff=0.15)

        s1 = stat("43", "Lean 4 repositories", ACC)
        # split bar 13 / 30
        W = 6.0
        b13 = Rectangle(width=W * 13 / 43, height=0.45, stroke_width=0, fill_color=S.INFO, fill_opacity=1)
        b30 = Rectangle(width=W * 30 / 43, height=0.45, stroke_width=0, fill_color=S.PANEL_EDGE, fill_opacity=1)
        bar = VGroup(b13, b30).arrange(RIGHT, buff=0.04)
        l13 = T("13 formal: Dafny, Verus, Coq", size=S.SMALL_SIZE, color=S.INFO).next_to(b13, DOWN, buff=0.15, aligned_edge=LEFT)
        l30 = T("30 Python", size=S.SMALL_SIZE, color=S.MUTED).next_to(b30, DOWN, buff=0.15, aligned_edge=RIGHT)
        split = VGroup(bar, l13, l30)
        top = VGroup(s1, split).arrange(RIGHT, buff=1.0).move_to(UP * 1.2)
        c1 = cite(f"{PAPER}, §3.4, p.6; Table 1, p.7; contamination, p.7")
        with self.beat("vero04scale-1"):
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(s1, shift=UP * 0.2), FadeIn(c1), run_time=0.8)
            self.play(GrowFromEdge(b13, LEFT), GrowFromEdge(b30, LEFT), FadeIn(l13), FadeIn(l30), run_time=1.0)
        s2 = stat("743", "scored APIs")
        s3 = stat("2,705", "scored specifications")
        row = VGroup(s2, s3).arrange(RIGHT, buff=2.0).move_to(DOWN * 1.2)
        with self.beat("vero04scale-2"):
            self.play(LaggedStart(FadeIn(s2, shift=UP * 0.2), FadeIn(s3, shift=UP * 0.2), lag_ratio=0.4), run_time=1.2)
        with self.beat("vero04scale-3"):
            gt = badge("no public Lean 4 ground truth", S.OK).next_to(row, DOWN, buff=0.5)
            self.play(FadeIn(gt), run_time=0.6)
        with self.beat("vero04scale-4"):
            self.play(FadeOut(VGroup(top, row, gt)), run_time=0.6)
            rule = T("Solved = every spec proved", size=S.HEADING_SIZE, weight="BOLD", color=ACC).move_to(UP * 0.6)
            sub = T("one open spec leaves room for a bug it would have caught", size=S.SMALL_SIZE + 2, color=S.MUTED)
            sub.next_to(rule, DOWN, buff=0.4)
            self.play(FadeOut(c1), FadeIn(cite(f"{PAPER}, §3.2, p.5")), Write(rule), run_time=1.0)
            self.play(FadeIn(sub), run_time=0.6)


# ====================================================================== 5
def vero_fig1(scale: float = 1.0):
    """Paper Fig. 1 as nodes/edges (audit->curation return edge drawn separately)."""
    nodes = [
        {"id": "repos", "label": "Real repos", "sub": "30 Python, 13 formal", "pos": [-5.75, 0.0], "w": 2.5, "h": 1.15, "color": S.MUTED},
        {"id": "cur", "label": "Curation", "sub": "human-gated", "pos": [-3.1, 0.0], "w": 2.3, "h": 1.15, "color": S.INFO},
        {"id": "bench", "label": "Benchmark", "sub": "Lean 4 instances", "pos": [-0.35, 0.0], "w": 2.6, "h": 1.15, "color": ACC},
        {"id": "po", "label": "Proof-only", "sub": "prove specs", "pos": [2.45, 1.35], "w": 2.3, "h": 1.0, "color": S.INFO},
        {"id": "cp", "label": "Code + proof", "sub": "implement, prove", "pos": [2.45, -1.35], "w": 2.3, "h": 1.0, "color": S.INFO},
        {"id": "grader", "label": "Grader", "sub": "clean rebuild", "pos": [5.6, 1.35], "w": 2.3, "h": 1.0, "color": S.OK},
        {"id": "audit", "label": "Formal audit", "sub": "negative evidence", "pos": [5.6, -1.35], "w": 2.3, "h": 1.0, "color": S.WARN},
    ]
    edges = [
        {"from": "repos", "to": "cur"}, {"from": "cur", "to": "bench"},
        {"from": "bench", "to": "po"}, {"from": "bench", "to": "cp"},
        {"from": "po", "to": "grader"}, {"from": "cp", "to": "grader"},
        {"from": "po", "to": "audit", "color": S.WARN}, {"from": "cp", "to": "audit", "color": S.WARN},
    ]
    g = pipeline(nodes, edges, scale=scale)
    a, c = g.by_id["audit"], g.by_id["cur"]
    y = -2.75
    p0 = a.get_bottom()
    path = VGroup(Line(p0, [p0[0], y, 0], color=S.WARN, stroke_width=3),
                  Line([p0[0], y, 0], [c.get_bottom()[0], y, 0], color=S.WARN, stroke_width=3))
    ret = Arrow([c.get_bottom()[0], y, 0], c.get_bottom(), buff=0.0, color=S.WARN, stroke_width=3,
                max_tip_length_to_length_ratio=0.25)
    lab = T("defects back to curation", size=S.SMALL_SIZE, color=S.WARN).move_to([-0.35, y - 0.3, 0])
    back = VGroup(path, ret, lab)
    return g, back


class Vero05Architecture(NarratedScene):
    EPISODE = EP

    def construct(self):
        head = T("Vero end to end (paper Fig. 1)", size=S.HEADING_SIZE - 6, weight="BOLD").to_edge(UP, buff=0.45)
        g, back = vero_fig1()
        g.shift(UP * 0.35)
        back.shift(UP * 0.35)
        src = cite(f"{PAPER}, Fig. 1, p.4; §3.3, p.6")
        stages = T("discover → select → plan → translate\n→ spec write (Python only) → validate", size=S.CITE_SIZE + 2,
                   color=S.MUTED, line_spacing=0.9)
        stages.next_to(g.by_id["cur"], UP, buff=0.35)
        stages.shift(RIGHT * max(0.0, -6.8 - stages.get_left()[0]))
        with self.beat("vero05architecture-1"):
            self.play(FadeIn(head), FadeIn(src), run_time=0.5)
            self.play(FadeIn(g.by_id["repos"], shift=UP * 0.1), run_time=0.5)
            self.play(GrowArrow(g.edge_by_id[("repos", "cur")]), FadeIn(g.by_id["cur"], shift=UP * 0.1), run_time=0.7)
            self.play(FadeIn(stages), run_time=0.6)
        with self.beat("vero05architecture-2"):
            self.play(GrowArrow(g.edge_by_id[("cur", "bench")]), FadeIn(g.by_id["bench"], shift=UP * 0.1), run_time=0.7)
            self.play(GrowArrow(g.edge_by_id[("bench", "po")]), GrowArrow(g.edge_by_id[("bench", "cp")]),
                      FadeIn(g.by_id["po"]), FadeIn(g.by_id["cp"]), run_time=0.8)
        with self.beat("vero05architecture-3"):
            self.play(GrowArrow(g.edge_by_id[("po", "grader")]), GrowArrow(g.edge_by_id[("cp", "grader")]),
                      FadeIn(g.by_id["grader"]), run_time=0.8)
            self.play(Indicate(g.by_id["grader"], color=S.OK, scale_factor=1.06), run_time=0.8)
        with self.beat("vero05architecture-4"):
            self.play(GrowArrow(g.edge_by_id[("po", "audit")]), GrowArrow(g.edge_by_id[("cp", "audit")]),
                      FadeIn(g.by_id["audit"]), run_time=0.8)
            self.play(Create(back[0]), run_time=0.8)
            self.play(GrowArrow(back[1]), FadeIn(back[2]), run_time=0.6)
            pulse_path(self, g, ["cp", "audit", "cur"], color=S.WARN, run_time=0.35)


# ====================================================================== 6
class Vero06Grader(NarratedScene):
    EPISODE = EP

    def construct(self):
        head = T("The grader: three layers", size=S.HEADING_SIZE - 6, weight="BOLD").to_edge(UP, buff=0.45)
        names = [("1  Slot re-rendering", S.INFO), ("2  Axiom allowlist", S.OK), ("3  Declaration screening", ACC)]
        layers = VGroup()
        for n, col in names:
            c = card(4.0, 0.85, edge=col)
            t = T(n, size=S.SMALL_SIZE + 2, weight="BOLD")
            if t.width > c.width - 0.35:
                t.scale_to_fit_width(c.width - 0.35)
            t.move_to(c)
            layers.add(VGroup(c, t))
        layers.arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.4)
        right_x = -0.6
        DY = -0.4  # vertical centre of the detail area
        src = cite(f"{PAPER}, App. D, p.19-20")
        with self.beat("vero06grader-1"):
            self.play(FadeIn(head), FadeIn(src), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in layers], lag_ratio=0.25), run_time=1.2)
            naive = T("“does it compile?” is not enough", size=S.SMALL_SIZE + 2, color=S.WARN).move_to([0, DY, 0])
            self.play(FadeIn(naive), run_time=0.5)
        # layer 1
        slot = code_panel(load("grader_slot.lean"), "lean", title="Proof slot (BankLedger exemplar)", font_size=18,
                          max_width=13.0)
        slot.move_to([0, DY + 0.5, 0])
        cap1 = T("only marker interiors are copied\ninto a fresh copy of the benchmark", size=S.SMALL_SIZE, color=S.MUTED,
                 line_spacing=0.9)
        cap1.next_to(slot, DOWN, buff=0.35)
        c1 = cite(f"{REPO}, reference/BankLedger/.../Proof_modecodeproof/Account.lean:33-36; paper App. D, p.19")
        with self.beat("vero06grader-2"):
            self.play(FadeOut(naive), layers[0][0].animate.set_stroke(width=6), run_time=0.5)
            self.play(FadeIn(slot), FadeOut(src), FadeIn(c1), run_time=0.8)
            h = highlight_lines(slot, 2, 4, color=S.INFO)
            self.play(Create(h), FadeIn(cap1), run_time=0.7)
        # layer 2
        allow = code_panel(load("grader_allowlist.py"), "python", title="src/vero/evaluation/axioms.py:31",
                           font_size=20, max_width=12.0)
        allow.move_to([0, DY + 0.9, 0])
        c2 = cite(f"{REPO}, src/vero/evaluation/axioms.py:31; paper App. D, p.19")
        with self.beat("vero06grader-3"):
            self.play(FadeOut(VGroup(slot, h, cap1)), FadeOut(c1), layers[0][0].animate.set_stroke(width=2),
                      layers[1][0].animate.set_stroke(width=6), run_time=0.6)
            self.play(FadeIn(allow), FadeIn(c2), run_time=0.8)
            three = VGroup(*[badge(a, S.OK) for a in ("Classical.choice", "propext", "Quot.sound")]).arrange(RIGHT, buff=0.25)
            three.next_to(allow, DOWN, buff=0.4)
            self.play(LaggedStart(*[FadeIn(b) for b in three], lag_ratio=0.3), run_time=0.9)
        with self.beat("vero06grader-4"):
            n = VGroup(T("368", size=S.TITLE_SIZE, weight="BOLD", color=S.BAD),
                       T("spec outcomes rejected at this layer", size=S.SMALL_SIZE + 2, color=S.MUTED)).arrange(RIGHT, buff=0.3)
            n.next_to(three, DOWN, buff=0.5)
            self.play(FadeIn(n, shift=UP * 0.1), FadeOut(c2), FadeIn(c2b := cite(f"{REPO}, axioms.py:31; paper App. D, p.19 (368)")),
                      run_time=0.7)
        # layer 3
        c3 = cite(f"{PAPER}, App. D, p.19-20; {REPO}, src/vero/evaluation/hygiene.py:20-27")
        with self.beat("vero06grader-5"):
            self.play(FadeOut(VGroup(allow, three, n)), FadeOut(c2b), layers[1][0].animate.set_stroke(width=2),
                      layers[2][0].animate.set_stroke(width=6), run_time=0.6)
            items = bullet_list(["hollow typeclass instances", "priority shadowing", "unsafe  →  run voided",
                                 "@[implemented_by] in Impl/  →  run voided"], size=S.SMALL_SIZE + 2)
            items.move_to([0, DY, 0])
            self.play(FadeIn(c3), LaggedStart(*[FadeIn(i, shift=RIGHT * 0.1) for i in items], lag_ratio=0.25), run_time=1.2)


# ====================================================================== 7
def byte_line():
    """Number line 0x37..0x43 with the reject gap (0x39, 0x41) and the '=' byte 0x3D. Local helper."""
    lo, hi = 0x37, 0x43
    W = 5.0
    x0 = -W / 2

    def X(v):
        return x0 + W * (v - lo) / (hi - lo)

    axis = Line([X(lo), 0, 0], [X(hi), 0, 0], color=S.MUTED, stroke_width=3)
    ticks = VGroup()
    labs = VGroup()
    for v in range(lo, hi + 1):
        major = v in (0x39, 0x3D, 0x41)
        ticks.add(Line([X(v), -0.1, 0], [X(v), 0.1, 0], color=S.INK if major else S.MUTED,
                       stroke_width=3 if major else 1.5))
        if major:
            labs.add(T(f"0x{v:02X}", size=S.SMALL_SIZE, color=S.INK, mono=True).next_to([X(v), -0.1, 0], DOWN, buff=0.15))
    chars = VGroup(T("'9'", size=S.SMALL_SIZE, color=S.MUTED, mono=True).next_to(labs[0], DOWN, buff=0.1),
                   T("'A'", size=S.SMALL_SIZE, color=S.MUTED, mono=True).next_to(labs[2], DOWN, buff=0.1))
    gap = Rectangle(width=X(0x41) - X(0x39), height=0.32, stroke_width=0, fill_color=S.BAD, fill_opacity=0.35)
    gap.move_to([(X(0x39) + X(0x41)) / 2, 0, 0])
    ends = VGroup(Circle(radius=0.09, color=S.BAD, stroke_width=3).move_to([X(0x39), 0, 0]),
                  Circle(radius=0.09, color=S.BAD, stroke_width=3).move_to([X(0x41), 0, 0]))
    gap_lab = T("reject: 0x39 < c < 0x41", size=S.SMALL_SIZE, color=S.BAD).next_to(gap, UP, buff=0.55)
    eq = Dot([X(0x3D), 0, 0], radius=0.13, color=S.INFO)
    eq_lab = T("'=' 0x3D: padding", size=S.SMALL_SIZE, color=S.INFO).next_to(eq, UP, buff=0.2)
    base = VGroup(axis, ticks, labs, chars)
    return base, VGroup(gap, ends, gap_lab), VGroup(eq, eq_lab)


class Vero07Base64(NarratedScene):
    EPISODE = EP

    def construct(self):
        head = T("verdict: Base64 charToBits", size=S.HEADING_SIZE - 6, weight="BOLD").to_edge(UP, buff=0.45)
        pad = code_panel(load("base64_padding_spec_paper.lean"), "lean", title="spec 1 (pre-fix)", font_size=18,
                         max_width=7.5)
        rej = code_panel(load("base64_reject_spec_paper.lean"), "lean", title="spec 2 (pre-fix)", font_size=18,
                         max_width=7.5)
        col = VGroup(pad, rej).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_edge(LEFT, buff=0.3).shift(DOWN * 0.25)
        src = cite(f"{PAPER}, App. F, Audit 1, p.24 (specs as printed, pre-fix); Table 3, p.16")
        with self.beat("vero07base64-1"):
            self.play(FadeIn(head), FadeIn(src), run_time=0.6)
            fn = T("charToBits : one byte → digit, padding, or reject", size=S.SMALL_SIZE + 2, color=S.MUTED)
            fn.next_to(head, DOWN, buff=0.35)
            self.play(FadeIn(fn), run_time=0.6)
        with self.beat("vero07base64-2"):
            self.play(FadeOut(fn), FadeIn(pad, shift=UP * 0.1), run_time=0.7)
            hp = highlight_lines(pad, 2, color=S.INFO)
            self.play(Create(hp), run_time=0.5)
        with self.beat("vero07base64-3"):
            self.play(FadeIn(rej, shift=UP * 0.1), run_time=0.7)
            hr = highlight_lines(rej, 4, color=S.BAD)
            self.play(Create(hr), run_time=0.5)
        base, gap, eq = byte_line()
        nl = VGroup(base, gap, eq)
        nl.move_to([4.15, 1.3, 0])
        with self.beat("vero07base64-4"):
            self.play(Create(base[0]), FadeIn(base[1]), FadeIn(base[2]), FadeIn(base[3]), run_time=0.9)
            self.play(FadeIn(gap[0]), Create(gap[1]), FadeIn(gap[2]), run_time=0.8)
            self.play(FadeIn(eq[0], scale=1.6), FadeIn(eq[1]), run_time=0.6)
            self.play(Indicate(eq[0], color=S.BAD, scale_factor=1.8), run_time=0.8)
        with self.beat("vero07base64-5"):
            tab = state_table([("input c", "0x3D  ('=')"),
                               ("spec 1 demands", "some none"),
                               ("spec 2 demands", "none")], title="Conflict at one byte")
            tab.scale(0.85).next_to(nl, DOWN, buff=0.4)
            tab[1][1][1][1].set_color(S.INFO)
            tab[1][1][1][2].set_color(S.BAD)
            self.play(FadeIn(tab, shift=UP * 0.1), run_time=0.8)
            verdict = badge("no implementation satisfies both", S.BAD).next_to(tab, DOWN, buff=0.3)
            self.play(FadeIn(verdict), run_time=0.5)


# ====================================================================== 8
class Vero08Audit(NarratedScene):
    EPISODE = EP

    def construct(self):
        head = T("The agent audits the specs", size=S.HEADING_SIZE - 6, weight="BOLD").to_edge(UP, buff=0.45)
        form = code_panel(load("joint_unsat_claim_form_repo.lean"), "lean",
                          title="joint_unsat claim form (Harness.lean, generic)", font_size=18, max_width=12.0)
        form.move_to(UP * 1.4)
        who = T("GPT-5.5 (xhigh): spec 1 and spec 2 are jointly unsatisfiable", size=S.SMALL_SIZE + 2, color=ACC)
        who.next_to(form, DOWN, buff=0.4)
        c1 = cite(f"{PAPER}, App. F, Audit 1, p.24; {REPO}, benchmarks/dijkstar/.../Harness.lean:34-35")
        with self.beat("vero08audit-1"):
            self.play(FadeIn(head), FadeIn(c1), run_time=0.6)
            self.play(FadeIn(form, shift=UP * 0.1), run_time=0.8)
            self.play(FadeIn(who), run_time=0.6)
        with self.beat("vero08audit-2"):
            q = T("“collapses to a one-line  0x3D < 0x41 ∧ 0x3D > 0x39  contradiction”", size=S.SMALL_SIZE + 2,
                  color=S.INK)
            q.next_to(who, DOWN, buff=0.45)
            note = T("(paper's description; the proof script itself is not published)", size=S.CITE_SIZE + 2, color=S.MUTED)
            note.next_to(q, DOWN, buff=0.2)
            self.play(FadeIn(q), run_time=0.8)
            self.play(FadeIn(note), run_time=0.5)
        rej = code_panel(load("base64_reject_spec_paper.lean"), "lean", title="spec 2 (pre-fix)", font_size=18,
                         max_width=9.5)
        rej.move_to(UP * 1.45)
        fix = code_panel(load("base64_fix_paper.lean"), "lean", title="paper's fix (p.24)", font_size=16,
                         line_numbers=False, max_width=8.0)
        fix.next_to(rej, DOWN, buff=0.45)
        c2 = cite(f"{PAPER}, App. F, Audit 1, p.24 (fix as printed in the paper; the released repo splits the range instead)")
        with self.beat("vero08audit-3"):
            self.play(FadeOut(VGroup(form, who, q, note)), FadeOut(c1), FadeIn(c2), run_time=0.6)
            self.play(FadeIn(rej), run_time=0.6)
            h = highlight_lines(rej, 4, color=S.BAD)
            self.play(Create(h), run_time=0.4)
            self.play(TransformFromCopy(rej.lines[3], fix), run_time=1.2)
            ok = badge("0x3D excluded", S.OK).next_to(fix, RIGHT, buff=0.3)
            self.play(FadeIn(ok), run_time=0.4)
            quote = T("“survived manual review and type-checking but was caught automatically by the agent”",
                      size=S.SMALL_SIZE, color=S.WARN)
            quote.next_to(fix, DOWN, buff=0.45).set_x(0)
            self.play(FadeIn(quote), run_time=0.5)
        # Table 6 (non-inferred values, p.24)
        items = [("Mistranslated definition or semantics", 18), ("Missing domain or operation condition", 17),
                 ("Reference implementation mismatch", 2), ("Direct conflict between specs", 1)]
        chart = bar_chart(items, unit="", max_value=18, highlight="Direct conflict between specs", accent=ACC,
                          width=4.2, size=S.SMALL_SIZE)
        chart.move_to(DOWN * 0.9)
        totals = VGroup(T("38 spec defects", size=S.HEADING_SIZE - 4, weight="BOLD", color=ACC),
                        T("in 9 instances  +  6 jointly unsatisfiable groups", size=S.SMALL_SIZE + 2, color=S.MUTED)
                        ).arrange(DOWN, buff=0.15)
        totals.move_to(UP * 1.7)
        c3 = cite(f"{PAPER}, App. F, p.24; Table 6, p.24")
        with self.beat("vero08audit-4"):
            self.play(FadeOut(VGroup(rej, h, fix, ok, quote)), FadeOut(c2), FadeIn(c3), run_time=0.6)
            self.play(FadeIn(totals, shift=UP * 0.1), run_time=0.8)
        with self.beat("vero08audit-5"):
            ttl = T("Audit findings by category (Table 6)", size=S.SMALL_SIZE + 2, color=S.MUTED)
            ttl.next_to(chart, UP, buff=0.35)
            self.play(FadeIn(ttl), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in chart], lag_ratio=0.2), run_time=1.2)
            tag = T("verdict", size=S.SMALL_SIZE, color=ACC).next_to(chart[3], RIGHT, buff=0.3)
            self.play(FadeIn(tag), Indicate(chart[3], color=ACC, scale_factor=1.05), run_time=0.8)


# ====================================================================== 9
class Vero09Trust(NarratedScene):
    EPISODE = EP

    def construct(self):
        head = T("A proof can be true and still not mean what you think", size=S.HEADING_SIZE - 10, weight="BOLD",
                 color=ACC).to_edge(UP, buff=0.45)
        with self.beat("vero09trust-1"):
            self.play(Write(head), run_time=1.2)
        orc = code_panel(load("trust_dijkstar_oracle_paper.lean"), "lean", title="dijkstar spec-oracle trick",
                         font_size=18, max_width=12.6)
        orc.move_to(UP * 1.25)
        ill = label_tag("illustrative (paper p.20)", S.WARN).next_to(orc, UP, buff=0.12).align_to(orc, RIGHT)
        c1 = cite(f"{PAPER}, App. D, p.20 (illustrative snippet; isMinWalkCost is not in the released repo)")
        with self.beat("vero09trust-2"):
            self.play(FadeIn(orc), FadeIn(ill), FadeIn(c1), run_time=0.8)
            h = highlight_lines(orc, 1, 2, color=S.INFO)
            n = T("proof target = the spec's own answer  →  optimality holds by definition", size=S.SMALL_SIZE + 2,
                  color=S.INFO).next_to(orc, DOWN, buff=0.3)
            self.play(Create(h), FadeIn(n), run_time=0.7)
        with self.beat("vero09trust-3"):
            h2 = highlight_lines(orc, 3, color=S.BAD)
            n2 = T("runtime code = a real Bellman-Ford (different function)", size=S.SMALL_SIZE + 2, color=S.BAD)
            n2.next_to(n, DOWN, buff=0.2)
            self.play(ReplacementTransform(h, h2), FadeIn(n2), run_time=0.7)
            st = VGroup(T("no output difference across 20,440 graphs", size=S.SMALL_SIZE + 2, color=S.MUTED),
                        badge("grader: impl_oracle, run voided", S.OK)).arrange(RIGHT, buff=0.4)
            st.next_to(n2, DOWN, buff=0.3)
            self.play(FadeIn(st), run_time=0.7)
        nd = code_panel(load("trust_base58_native_decide_paper.lean"), "lean", title="base58, GPT-5.5 (xhigh)",
                        font_size=20, max_width=10.0)
        nd.move_to(UP * 1.1)
        c2 = cite(f"{PAPER}, App. D, Layer 2, p.19")
        with self.beat("vero09trust-4"):
            self.play(FadeOut(VGroup(orc, ill, h2, n, n2, st)), FadeOut(c1), FadeIn(c2), run_time=0.6)
            self.play(FadeIn(nd), run_time=0.6)
            hn = highlight_lines(nd, 3, color=S.BAD)
            ax = VGroup(T("depends on", size=S.SMALL_SIZE + 2, color=S.MUTED),
                        badge("Lean.ofReduceBool", S.BAD),
                        T("not in the allowlist", size=S.SMALL_SIZE + 2, color=S.MUTED)).arrange(RIGHT, buff=0.3)
            ax.next_to(nd, DOWN, buff=0.4)
            self.play(Create(hn), FadeIn(ax), run_time=0.8)
            cnt = T("28 of that run's 53 specs fail this way", size=S.SMALL_SIZE + 2, color=S.INK).next_to(ax, DOWN, buff=0.35)
            self.play(FadeIn(cnt), run_time=0.5)
        with self.beat("vero09trust-5"):
            self.play(FadeOut(VGroup(nd, hn, ax, cnt)), FadeOut(c2), run_time=0.6)
            line = VGroup(T("What a proof means is decided by", size=S.BODY_SIZE, color=S.MUTED),
                          T("the checker  +  the specs", size=S.HEADING_SIZE, weight="BOLD", color=ACC),
                          T("not by “it compiles”", size=S.BODY_SIZE, color=S.MUTED)).arrange(DOWN, buff=0.3)
            self.play(FadeIn(line, shift=UP * 0.1), run_time=0.9)


# ====================================================================== 10
class Vero10Results(NarratedScene):
    EPISODE = EP

    def construct(self):
        head = T("Results", size=S.HEADING_SIZE - 6, weight="BOLD").to_edge(UP, buff=0.45)
        setup = T("4 agent setups  ×  2 modes  ×  43 repos  ·  90 min per run", size=S.SMALL_SIZE + 2, color=S.MUTED)
        setup.next_to(head, DOWN, buff=0.3)
        c0 = cite(f"{PAPER}, §4.1, p.7; Fig. 3 caption, p.8")
        with self.beat("vero10results-1"):
            self.play(FadeIn(head), FadeIn(setup), FadeIn(c0), run_time=0.8)
        items = [("GPT-5.5 (xhigh)", 27), ("Claude Opus 4.8 (xhigh)", 8), ("GPT-5.5 (mid)", 2), ("Claude Sonnet 5 (xhigh)", 2)]
        chart = bar_chart(items, unit=" / 43", max_value=43, highlight="GPT-5.5 (xhigh)", accent=ACC, width=6.0)
        chart.move_to(DOWN * 0.1)
        ttl = T("Full solves, code-and-proof mode", size=S.SMALL_SIZE + 2, color=S.INK).next_to(chart, UP, buff=0.35)
        c1 = cite(f"{PAPER}, p.8; Fig. 3(a)")
        with self.beat("vero10results-2"):
            self.play(FadeOut(c0), FadeIn(c1), FadeIn(ttl), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in chart], lag_ratio=0.3), run_time=1.6)
        with self.beat("vero10results-3"):
            self.play(VGroup(ttl, chart).animate.scale(0.7).to_edge(LEFT, buff=0.5).shift(UP * 0.5), run_time=0.7)
            big = VGroup(T("87.3%", size=S.TITLE_SIZE + 8, weight="BOLD", color=ACC),
                         T("of specs passed by GPT-5.5 (xhigh)\nin code-and-proof mode", size=S.SMALL_SIZE + 2, color=S.MUTED,
                           line_spacing=0.9),
                         T("vs. 27 / 43 repositories fully solved", size=S.SMALL_SIZE + 2, color=S.MUTED)
                         ).arrange(DOWN, buff=0.2)
            big.move_to([3.6, 0.6, 0])
            self.play(FadeIn(big, shift=UP * 0.1), run_time=0.8)
        with self.beat("vero10results-4"):
            a = VGroup(T("73.6%", size=S.HEADING_SIZE, weight="BOLD", color=S.INFO),
                       T("median share of proof lines in\nhelper lemmas (code-and-proof\nfull solves)", size=S.SMALL_SIZE,
                         color=S.MUTED, line_spacing=0.9)).arrange(RIGHT, buff=0.3)
            b = VGroup(T("10", size=S.HEADING_SIZE, weight="BOLD", color=S.BAD),
                       T("repositories resist all\neight configurations", size=S.SMALL_SIZE, color=S.MUTED,
                         line_spacing=0.9)
                       ).arrange(RIGHT, buff=0.3)
            facts = VGroup(a, b).arrange(RIGHT, buff=1.2, aligned_edge=UP).move_to([0, -2.2, 0])
            self.play(FadeOut(c1), FadeIn(cite(f"{PAPER}, p.8; Fig. 3, Fig. 5(b)")), FadeIn(a), run_time=0.8)
            self.play(FadeIn(b), run_time=0.6)


# ====================================================================== 11
class Vero11Limits(NarratedScene):
    EPISODE = EP

    def construct(self):
        head = T("What Vero does not claim", size=S.HEADING_SIZE - 6, weight="BOLD").to_edge(UP, buff=0.5)
        rows = [
            ("Lean 4 only; no concurrent or temporal protocols", "p.11"),
            ("Audit proves specs satisfiable, not semantically right or complete", "p.11"),
            ("Full solve ignores what specs omit, e.g. running time", "p.31"),
        ]
        cards = VGroup()
        for text, _ in rows:
            c = card(11.6, 1.05, edge=S.WARN)
            t = T(text, size=S.SMALL_SIZE + 4).move_to(c)
            cards.add(VGroup(c, t))
        cards.arrange(DOWN, buff=0.35).move_to(DOWN * 0.1)
        src = cite(f"{PAPER}, Limitations, p.11; App. H.4, p.31")
        with self.beat("vero11limits-1"):
            self.play(FadeIn(head), FadeIn(src), run_time=0.5)
            self.play(FadeIn(cards[0], shift=UP * 0.1), run_time=0.7)
        with self.beat("vero11limits-2"):
            self.play(FadeIn(cards[1], shift=UP * 0.1), run_time=0.7)
        with self.beat("vero11limits-3"):
            self.play(FadeIn(cards[2], shift=UP * 0.1), run_time=0.7)
            ex = T("sortedcontainers: linear scan, O(n) lookup instead of O(log n), passes every spec",
                   size=S.SMALL_SIZE, color=S.MUTED).next_to(cards, DOWN, buff=0.35)
            self.play(FadeIn(ex), run_time=0.6)


# ====================================================================== 12
class Vero12Bridge(NarratedScene):
    EPISODE = EP

    def construct(self):
        l1 = T("The checker and the specification", size=S.HEADING_SIZE - 4, color=S.INK)
        l2 = T("decide what a proof means.", size=S.HEADING_SIZE - 4, color=ACC, weight="BOLD")
        nxt = T("Next: optimised SIMD kernels. Do two programs compute the same thing?", size=S.SMALL_SIZE + 2,
                color=S.ACCENT["vekto"])
        g = VGroup(l1, l2, nxt).arrange(DOWN, buff=0.35)
        nxt.shift(DOWN * 0.3)
        with self.beat("vero12bridge-1"):
            self.play(FadeIn(l1), run_time=0.7)
            self.play(FadeIn(l2), run_time=0.7)
            self.wait(3.5)
            self.play(FadeIn(nxt, shift=UP * 0.1), run_time=0.7)
        m = series_map(current="vekto").scale(0.9)
        with self.beat("vero12bridge-2"):
            self.play(FadeOut(g), run_time=0.4)
            self.play(FadeIn(m), run_time=0.8)
