# SOURCE: ExVerus paper, Figure 1 top-middle panel "ExVerus-synthesized Z3Py script", page 3.
# Copied from research/exverus/examples/02b_findmax_exverus_z3py.py (transcribed from the rendered figure).
# Written by an LLM inside ExVerus, not by hand.
# TRIMS for screen: the four blank lines of the figure (8, 10, 14, 17) are removed. Every other line is verbatim.
# On screen line 3 = the concretisation "array length fixed to 2" (figure callout, lines 3-7).
# ---- on screen below ----
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
