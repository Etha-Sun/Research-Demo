# SOURCE: ExVerus paper, Figure 1 (top-middle panel "ExVerus-synthesized Z3Py script"), page 3.
# TRANSCRIBED from the rendered figure (19 numbered lines; lines 8, 10, 14, 17 are blank in the figure;
# figure glyphs "==", ">=", "<=", "!=" written in ASCII). This script was synthesized by an LLM, not hand-written.
# Figure callouts: lines 3-7 "Adaptive variable concretization to minimize number of quantifiers"
#   (array length fixed to 2); "Semantic preserving (variable, types)"; lines 11-19 "Direct source-level translation".
import z3
s = z3.Solver()
__vec__nums__len = z3.IntVal(2)
__vec__nums__0 = z3.Int('__vec__nums__0')
__vec__nums__1 = z3.Int('__vec__nums__1')
i = z3.Int('i')
max = z3.Int('max')

s.add(i == 1)

s.add(i >= 1)
s.add(i < __vec__nums__len)
s.add(__vec__nums__0 <= max)

max_post = z3.If(__vec__nums__1 > max,
    __vec__nums__1, max)

s.add(z3.And(__vec__nums__0 != max_post,
    __vec__nums__1 != max_post))
