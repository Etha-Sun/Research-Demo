// SOURCE: TopoVerus paper (arXiv 2611.13627v1), Figure 2 bottom panel "Correct Case (Inductive)", invariant list, PDF p.4
//   (copy: research/topoverus/examples/paper-fig2-diagnostics.txt:31-35). 
//   Fig. 2 lists I1..I5 with I5 carrying the "[Boundary error]" `high <= i`; I1..I4 equal Fig. 1 (p.3) lines I1..I4
//   up to the `: int` annotation.
// SCREEN TRIMS: the "[Boundary error]" tag is dropped (the scene marks the line in red instead); labels I1..I5 kept as prefixes.
// ---- screen text below ----
I1  1 <= nums@.len() <= 10000
I2  0 <= low <= nums@.len()
I3  -1 <= high <= nums@.len() - 1
I4  forall|i: int| 0 <= i < low ==> nums@[i] < target
I5  forall|i: int| high <= i < nums@.len() ==> nums@[i] > target
