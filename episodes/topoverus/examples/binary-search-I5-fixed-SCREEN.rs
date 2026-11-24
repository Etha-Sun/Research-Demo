// SOURCE: TopoVerus paper Figure 2 bottom, "Repair signal: Exclude the boundary index high: high <= i -> high < i." (p.4),
//   and text p.4 "change high <= i to high < i". This line = binary-search-invariants-SCREEN.rs line I5 with exactly that
//   edit applied; it matches Fig. 1 (p.3) I5 `forall|i| high < i < nums@.len() ==> nums@[i] > target` up to `: int`.
// ---- screen text below ----
I5  forall|i: int| high < i < nums@.len() ==> nums@[i] > target
