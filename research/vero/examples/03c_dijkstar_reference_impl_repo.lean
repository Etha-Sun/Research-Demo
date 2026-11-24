-- SOURCE: github.com/sunblaze-ucb/vero @ 0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09
--   benchmarks/dijkstar/Dijkstar/Impl/ShortestPath.lean, lines 59-89 (verbatim): reference Bellman-Ford.

-- !benchmark @start code_aux def=findPathCost
-- Private helpers of the reference implementation.

def distOf (d : Dist) (v : Nat) : Option Nat :=
  (d.find? (fun p => p.1 == v)).map Prod.snd

def setMin (d : Dist) (v c : Nat) : Dist :=
  match distOf d v with
  | none => (v, c) :: d
  | some old => if c < old then (v, c) :: d else d

def relaxEdge (g : Graph) (d : Dist) (e : Nat × Nat × Nat) : Dist :=
  match distOf d e.1, Dijkstar.edgeWeight g e.1 e.2.1 with
  | some df, some w => setMin d e.2.1 (df + w)
  | _, _ => d

def relaxList (g : Graph) (L : Graph) (d : Dist) : Dist :=
  L.foldl (relaxEdge g) d

def relaxAll (g : Graph) (d : Dist) : Dist :=
  relaxList g g d

def iterRelax (g : Graph) : Nat → Dist → Dist
  | 0, d => d
  | n + 1, d => iterRelax g n (relaxAll g d)
-- !benchmark @end code_aux def=findPathCost

def Dijkstar.findPathCost : Dijkstar.FindPathCostSig :=
-- !benchmark @start code def=findPathCost
  fun g s t => distOf (iterRelax g (g.length + 1) [(s, 0)]) t
-- !benchmark @end code def=findPathCost
