-- SOURCE: github.com/sunblaze-ucb/vero @ 0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09
--   benchmarks/dijkstar/Dijkstar/Spec/ShortestPath.lean, lines 200-203 (verbatim; the doc comment
--   on lines 194-199 is omitted). Also in research/vero/examples/03b_dijkstar_minimality_specs_repo.lean.
def spec_cost_minimal_unbounded (impl : RepoImpl) : Prop :=
  ∀ (g : Graph) (s t c : Nat),
    impl.dijkstar.findPathCost g s t = some c →
      ∀ (walk : List Nat), isWalk g s t walk = true → c ≤ walkCost g walk
