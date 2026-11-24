"""Shared visual style for the Research-Demo video series.

Every episode imports from here so that the four videos look like one series.
Fonts can be overridden with environment variables (useful on a local machine
that has nicer fonts installed):

    VIDEO_FONT_SANS   default "Sans"       e.g. "Inter", "Helvetica Neue", "PingFang SC"
    VIDEO_FONT_MONO   default "Monospace"  e.g. "JetBrains Mono", "Menlo"
"""
import os

# ---------------------------------------------------------------- fonts
FONT_SANS = os.environ.get("VIDEO_FONT_SANS", "Sans")
FONT_MONO = os.environ.get("VIDEO_FONT_MONO", "Monospace")

# ---------------------------------------------------------------- palette
BG = "#0E1117"          # background
PANEL = "#161B22"       # code / card background
PANEL_EDGE = "#30363D"  # card border
INK = "#E6EDF3"         # primary text
MUTED = "#8B949E"       # secondary text, citations
GRID = "#21262D"

OK = "#3FB950"          # verified / pass
BAD = "#F85149"         # failure / counterexample
WARN = "#D29922"        # assumption / condition
INFO = "#58A6FF"        # neutral highlight

# one accent colour per episode (also used on the series map)
EPISODES = [
    # key,        title,        subtitle,                                         accent
    ("exverus",   "ExVerus",    "Proof repair via counterexample reasoning",      "#F0883E"),
    ("topoverus", "TopoVerus",  "Learning to repair with counterexamples",        "#39C5BB"),
    ("vero",      "Vero",       "Verified software at repository scale",          "#A371F7"),
    ("vekto",     "Vekto",      "Proving SIMD kernel migrations equivalent",      "#56D364"),
]
ACCENT = {k: c for k, _, _, c in EPISODES}

# ---------------------------------------------------------------- sizes
TITLE_SIZE = 56
HEADING_SIZE = 40
BODY_SIZE = 28
SMALL_SIZE = 20
CITE_SIZE = 16
CODE_FONT_SIZE = 20     # Code paragraph font size (fits ~70 columns at 1080p)

CODE_STYLE = "github-dark"   # pygments style for Code
