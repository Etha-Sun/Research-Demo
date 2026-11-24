"""Reusable Manim building blocks for the Research-Demo series (Manim Community 0.19).

Main pieces
-----------
NarratedScene   Scene base class. Narration lives in episodes/<ep>/narration.json as
                "beats"; `with self.beat("id"):` runs the animations of one beat and then
                waits until the beat's duration has passed. The real start/end time of
                every beat is written to media/timeline/<Scene>.json, which tools/mux.py
                uses to place the voice-over and subtitles exactly.
series_map      The four-episode strip shown at the start/end of every episode.
pipeline        Architecture diagram from explicit node/edge lists.
code_panel      Syntax-highlighted code card with a title bar; highlight_lines() boxes lines.
state_table     Small key/value table (program states, counterexamples).
bar_chart       Horizontal bars for results with a citation.
cite            Source footnote in the bottom-left corner.
"""
from __future__ import annotations

import json
import os
from contextlib import contextmanager
from pathlib import Path

from manim import (
    DOWN, LEFT, RIGHT, UP, ORIGIN, UL, DL, DR,
    Arrow, Create, CurvedArrow, FadeIn, FadeOut, GrowArrow, Line, Rectangle,
    RoundedRectangle, Scene, SurroundingRectangle, Text, VGroup, Write, Code,
    config, LaggedStart,
)

from . import style as S

ROOT = Path(__file__).resolve().parent.parent
config.background_color = S.BG


# ------------------------------------------------------------------ text helpers
def T(text: str, size: float = S.BODY_SIZE, color: str = S.INK, weight: str = "NORMAL", mono: bool = False, **kw) -> Text:
    """Text with the series fonts."""
    return Text(text, font=S.FONT_MONO if mono else S.FONT_SANS, font_size=size, color=color, weight=weight, **kw)


def cite(text: str) -> Text:
    """Small source line, bottom-left. Every number or quoted result on screen gets one."""
    c = T(text, size=S.CITE_SIZE, color=S.MUTED)
    c.to_corner(DL, buff=0.25)
    return c


def bullet_list(items, size=S.BODY_SIZE, color=S.INK, buff=0.28) -> VGroup:
    rows = VGroup(*[T("•  " + s, size=size, color=color) for s in items])
    rows.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    return rows


# ------------------------------------------------------------------ narrated scene
class NarratedScene(Scene):
    """Base class: set EPISODE (e.g. "exverus"); use `with self.beat(id):`.

    narration.json format:
        {"episode": "exverus",
         "scenes": {"S01Hook": [{"id": "hook-1", "seconds": 6.0, "en": "...", "zh": "..."}, ...]}}
    `seconds` is replaced by the measured voice length (+ padding) by tools/sync_durations.py.
    """

    EPISODE: str = ""

    def setup(self):
        super().setup()
        path = ROOT / "episodes" / self.EPISODE / "narration.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        beats = data["scenes"].get(type(self).__name__, [])
        self._beats = {b["id"]: b for b in beats}
        self._timeline = []

    @contextmanager
    def beat(self, beat_id: str):
        b = self._beats[beat_id]          # KeyError = narration.json and scene out of sync
        start = self.renderer.time
        yield b
        elapsed = self.renderer.time - start
        rest = float(b.get("seconds", 0)) - elapsed
        if rest > 0.02:
            self.wait(rest)
        self._timeline.append({"id": beat_id, "start": start, "end": self.renderer.time,
                               "en": b.get("en", ""), "zh": b.get("zh", "")})

    def tear_down(self):
        out = Path(config.media_dir) / "timeline"
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{type(self).__name__}.json").write_text(
            json.dumps({"episode": self.EPISODE, "scene": type(self).__name__, "beats": self._timeline},
                       indent=1, ensure_ascii=False), encoding="utf-8")
        super().tear_down()

    # convenience
    def clear_all(self, run_time=0.6):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=run_time)


# ------------------------------------------------------------------ cards and maps
def card(width: float, height: float, edge: str = S.PANEL_EDGE, fill: str = S.PANEL) -> RoundedRectangle:
    return RoundedRectangle(width=width, height=height, corner_radius=0.15,
                            stroke_color=edge, stroke_width=2, fill_color=fill, fill_opacity=1)


def title_card(episode_key: str, number: int | None = None, extra: str | None = None) -> VGroup:
    """Video opening: title and subtitle in the video's accent colour; `extra` = authors · venue.
    `number` is kept for backward compatibility and ignored: each video stands on its own."""
    _, title, subtitle, accent = next(e for e in S.EPISODES if e[0] == episode_key)
    t = T(title, size=S.TITLE_SIZE + 16, weight="BOLD")
    s = T(subtitle, size=S.HEADING_SIZE - 8, color=S.MUTED)
    g = VGroup(t, s).arrange(DOWN, buff=0.3)
    if extra:
        g.add(T(extra, size=S.SMALL_SIZE, color=S.MUTED).next_to(s, DOWN, buff=0.4))
    bar = Line(LEFT * 1.5, RIGHT * 1.5, color=accent, stroke_width=6).next_to(g, DOWN, buff=0.4)
    return VGroup(g, bar)


def series_map(current: str | None = None, theme: str = "counterexamples connect a failed proof to its repair") -> VGroup:
    """Strip of the four episodes; `current` is drawn bright, the rest dimmed."""
    nodes = VGroup()
    for i, (key, title, subtitle, accent) in enumerate(S.EPISODES, start=1):
        on = current is None or key == current
        box = card(2.9, 1.3, edge=accent if on else S.PANEL_EDGE)
        lab = VGroup(T(f"{i}", size=S.SMALL_SIZE, color=accent if on else S.MUTED),
                     T(title, size=S.BODY_SIZE, weight="BOLD", color=S.INK if on else S.MUTED)).arrange(DOWN, buff=0.08)
        lab.move_to(box)
        nodes.add(VGroup(box, lab))
    nodes.arrange(RIGHT, buff=0.45)
    arrows = VGroup(*[Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), buff=0.05,
                            stroke_width=3, color=S.MUTED, max_tip_length_to_length_ratio=0.3)
                      for i in range(len(nodes) - 1)])
    caption = T(theme, size=S.SMALL_SIZE, color=S.MUTED).next_to(nodes, DOWN, buff=0.45)
    return VGroup(nodes, arrows, caption)


# ------------------------------------------------------------------ pipeline diagram
def pipeline(nodes: list[dict], edges: list[dict], scale: float = 1.0) -> VGroup:
    """Architecture diagram from explicit specs.

    nodes: [{"id": "llm", "label": "LLM", "sub": "proposes repair", "pos": [x, y],
             "color": "#F0883E", "w": 2.6, "h": 1.1}]      (pos in Manim units, frame is 14.2 x 8)
    edges: [{"from": "a", "to": "b", "label": "error", "curve": 0}]   curve: angle in radians (0 = straight)
    Returns VGroup(boxes, arrows, edge_labels); boxes/arrows are also reachable by id via .by_id / .edge_by_id.
    """
    boxes = VGroup()
    by_id = {}
    for n in nodes:
        w, h = n.get("w", 2.6) * scale, n.get("h", 1.1) * scale
        col = n.get("color", S.INFO)
        r = card(w, h, edge=col)
        parts = [T(n["label"], size=S.BODY_SIZE * scale, weight="BOLD")]
        if n.get("sub"):
            parts.append(T(n["sub"], size=S.SMALL_SIZE * scale, color=S.MUTED))
        lab = VGroup(*parts).arrange(DOWN, buff=0.08)
        if lab.width > w - 0.2:
            lab.scale_to_fit_width(w - 0.2)
        lab.move_to(r)
        g = VGroup(r, lab).move_to([n["pos"][0], n["pos"][1], 0])
        boxes.add(g)
        by_id[n["id"]] = g
    arrows, labels = VGroup(), VGroup()
    edge_by_id = {}
    for e in edges:
        a, b = by_id[e["from"]], by_id[e["to"]]
        curve = e.get("curve", 0)
        if curve:
            ar = CurvedArrow(a.get_center(), b.get_center(), angle=curve, color=e.get("color", S.MUTED), stroke_width=3)
            # shorten to box borders
            ar = CurvedArrow(_border_point(a, b), _border_point(b, a), angle=curve, color=e.get("color", S.MUTED), stroke_width=3)
        else:
            ar = Arrow(_border_point(a, b), _border_point(b, a), buff=0.05, color=e.get("color", S.MUTED),
                       stroke_width=3, max_tip_length_to_length_ratio=0.15)
        arrows.add(ar)
        edge_by_id[(e["from"], e["to"])] = ar
        if e.get("label"):
            lab = T(e["label"], size=S.SMALL_SIZE * scale, color=e.get("color", S.MUTED))
            lab.move_to(ar.point_from_proportion(0.5)).shift(UP * 0.25 if not curve else ORIGIN)
            labels.add(lab)
    g = VGroup(boxes, arrows, labels)
    g.by_id, g.edge_by_id = by_id, edge_by_id
    return g


def _border_point(a, b):
    """Point on a's bounding box in the direction of b."""
    import numpy as np
    ca, cb = a.get_center(), b.get_center()
    d = cb - ca
    if abs(d[0]) * a.height >= abs(d[1]) * a.width:
        return a.get_right() if d[0] > 0 else a.get_left()
    return a.get_top() if d[1] > 0 else a.get_bottom()


def animate_pipeline(scene: Scene, g: VGroup, order: list[str] | None = None, run_time: float = 0.6):
    """Reveal boxes (in `order` if given) then arrows and labels."""
    boxes = [g.by_id[i] for i in order] if order else list(g[0])
    scene.play(LaggedStart(*[FadeIn(b, shift=UP * 0.15) for b in boxes], lag_ratio=0.25), run_time=run_time * len(boxes) ** 0.5 * 1.5)
    scene.play(LaggedStart(*[GrowArrow(a) if isinstance(a, Arrow) else Create(a) for a in g[1]], lag_ratio=0.15),
               FadeIn(g[2]), run_time=run_time * 2)


def pulse_path(scene: Scene, g: VGroup, path: list[str], color: str = S.INFO, run_time: float = 0.5):
    """Highlight the boxes along a path one after another (data flowing through)."""
    for i in path:
        box = g.by_id[i][0]
        scene.play(box.animate.set_stroke(color=color, width=6), run_time=run_time)
        scene.play(box.animate.set_stroke(width=2), run_time=run_time * 0.5)


# ------------------------------------------------------------------ code
def code_panel(code: str, language: str, title: str | None = None, font_size: float = S.CODE_FONT_SIZE,
               line_numbers: bool = True, max_width: float = 12.5, max_height: float = 6.2) -> VGroup:
    """Code card with an optional title bar (file name / role). Returns VGroup(card, header?, code).

    `.code` is the Manim Code object; `.lines` its code lines (for highlight_lines).
    """
    c = Code(code_string=code.rstrip("\n"), language=language, formatter_style=S.CODE_STYLE,
             add_line_numbers=line_numbers, background="rectangle",
             background_config={"stroke_width": 0, "fill_color": S.PANEL, "fill_opacity": 1},
             paragraph_config={"font": S.FONT_MONO, "font_size": font_size})
    if c.width > max_width:
        c.scale_to_fit_width(max_width)
    if c.height > max_height:
        c.scale_to_fit_height(max_height)
    parts = []
    if title:
        head = T(title, size=S.SMALL_SIZE, color=S.MUTED, mono=True)
        head.next_to(c, UP, buff=0.12, aligned_edge=LEFT)
        parts.append(head)
    body = VGroup(*parts, c)
    frame = card(body.width + 0.3, body.height + 0.3)
    frame.move_to(body)
    g = VGroup(frame, body)
    g.code, g.lines = c, c.code_lines
    return g


def highlight_lines(panel: VGroup, first: int, last: int | None = None, color: str = S.WARN) -> SurroundingRectangle:
    """Box around code lines first..last (1-based, inclusive)."""
    last = last or first
    rows = VGroup(*panel.lines[first - 1:last])
    return SurroundingRectangle(rows, color=color, buff=0.06, stroke_width=3, corner_radius=0.05)


# ------------------------------------------------------------------ tables and charts
def state_table(rows: list[tuple[str, str]], title: str | None = None, key_color: str = S.MUTED,
                val_color: str = S.INK, size: float = S.SMALL_SIZE + 2) -> VGroup:
    """Two-column table, e.g. a counterexample state [("i", "3"), ("sum", "7")]."""
    keys = VGroup(*[T(k, size=size, color=key_color, mono=True) for k, _ in rows])
    vals = VGroup(*[T(v, size=size, color=val_color, mono=True) for _, v in rows])
    keys.arrange(DOWN, aligned_edge=RIGHT, buff=0.22)
    for k, v in zip(keys, vals):
        v.next_to(k, RIGHT, buff=0.5)
        v.align_to(keys, LEFT).shift(RIGHT * (keys.width + 0.5))
    body = VGroup(keys, vals)
    parts = [body]
    if title:
        parts.insert(0, T(title, size=size, weight="BOLD"))
    inner = VGroup(*parts).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    frame = card(inner.width + 0.6, inner.height + 0.5)
    frame.move_to(inner)
    return VGroup(frame, inner)


def bar_chart(items: list[tuple[str, float]], unit: str = "%", max_value: float = 100.0, highlight: str | None = None,
              accent: str = S.INFO, width: float = 7.0, size: float = S.SMALL_SIZE + 2) -> VGroup:
    """Horizontal bars [(label, value)]. The bar whose label == highlight uses `accent`, others are muted."""
    rows = VGroup()
    for label, value in items:
        lab = T(label, size=size, color=S.INK if label == highlight else S.MUTED)
        bar = Rectangle(width=max(0.02, width * value / max_value), height=0.38, stroke_width=0,
                        fill_color=accent if label == highlight else S.PANEL_EDGE, fill_opacity=1)
        val = T(f"{value:g}{unit}", size=size, color=S.INK if label == highlight else S.MUTED)
        rows.add(VGroup(lab, bar, val))
    lw = max(r[0].width for r in rows)
    for i, r in enumerate(rows):
        r[0].move_to([0, -i * 0.6, 0], aligned_edge=RIGHT).shift(LEFT * 0.0)
        r[0].align_to([-0.0 - 0.2, 0, 0], RIGHT)
        r[1].next_to([0, -i * 0.6, 0], RIGHT, buff=0)
        r[2].next_to(r[1], RIGHT, buff=0.15)
    rows.center()
    return rows


def badge(text: str, color: str) -> VGroup:
    """Rounded label, e.g. badge("VERIFIED", OK) or badge("counterexample", BAD)."""
    t = T(text, size=S.SMALL_SIZE, color=color, weight="BOLD")
    r = RoundedRectangle(width=t.width + 0.4, height=t.height + 0.25, corner_radius=0.12,
                         stroke_color=color, stroke_width=2, fill_opacity=0)
    r.move_to(t)
    return VGroup(r, t)
