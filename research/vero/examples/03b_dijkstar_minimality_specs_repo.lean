-- SOURCE: github.com/sunblaze-ucb/vero @ 0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09
--   benchmarks/dijkstar/Dijkstar/Spec/ShortestPath.lean, lines 45-55 (frozen walk notion) and 200-212 (verbatim).

def isWalk (g : Graph) (s t : Nat) : List Nat → Bool
  | [] => false
  | [x] => x == s && x == t
  | x :: y :: rest => x == s && (walkEdge g x y).isSome && isWalk g y t (y :: rest)

/-- `walkCost g nodes`: the total weight of a walk — the sum of the
    consecutive edge weights along it. -/
def walkCost (g : Graph) : List Nat → Nat
  | [] => 0
  | [_] => 0
  | x :: y :: rest => (walkEdge g x y).getD 0 + walkCost g (y :: rest)
-- ...
def spec_cost_minimal_unbounded (impl : RepoImpl) : Prop :=
  ∀ (g : Graph) (s t c : Nat),
    impl.dijkstar.findPathCost g s t = some c →
      ∀ (walk : List Nat), isWalk g s t walk = true → c ≤ walkCost g walk

/-- Completeness: if *any* walk `s → t` exists — of *any* length —
    `findPathCost` must return `some`. No reachable target may be
    reported `none`, however long the only witnessing walk is; this closes the
    under-reporting hole where an impl returns `some` only for the source
    itself or a direct edge and `none` for everything multi-hop. -/
def spec_cost_complete_unbounded (impl : RepoImpl) : Prop :=
  ∀ (g : Graph) (s t : Nat) (walk : List Nat),
    isWalk g s t walk = true → impl.dijkstar.findPathCost g s t ≠ none
