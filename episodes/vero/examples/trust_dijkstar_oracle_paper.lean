-- SOURCE: Vero paper, Appendix D "Splitting the proof target from the runtime function", page 20 (verbatim,
-- line numbers removed); via research/vero/examples/03a_dijkstar_spec_oracle_cheat_paper.lean.
-- The PDF prints the last name with a prime (findPathCost'); reproduced as printed.
noncomputable def findPathCost : FindPathCostSig :=
  fun g s t => if h : exists c, isMinWalkCost g s t c then h.choose else 0
@[implemented_by realBellmanFord] def findPathCost' := findPathCost
