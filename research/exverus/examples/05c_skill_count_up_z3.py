# SOURCE: ExVerus artifact repo github.com/claudeyj/exverus @ 4e513a1c, skills/counterexample-guided-proof/SKILL.md, fenced block #3 (section '2. Solve (e.g. with Z3)'). VERBATIM. This teaching example is from the repo's agent skill, NOT from the paper.
import z3
n, i, j = z3.Ints("n i j")
s = z3.Solver()
for v in (n, i, j): s.add(0 <= v, v < 2**32)            # u32
s.add(i < n, i <= n, j <= 1000)                         # before
s.add(z3.Not(z3.And(i + 1 <= n, j + 1 <= 1000)))       # after fails
# enumerate a few models with blocking clauses
# -> {n: 1, i: 0, j: 1000}, {n: 2, i: 1, j: 1000}, ...
