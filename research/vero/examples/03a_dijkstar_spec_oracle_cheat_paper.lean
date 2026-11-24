-- SOURCE: Vero paper, Appendix D "Splitting the proof target from the runtime function", page 20.
-- Transcribed verbatim from the PDF text layer; line numbers removed; indentation restored by hand.
-- The PDF renders the last name as findPathCost' (prime); "exists" is as printed.
-- NOTE: `isMinWalkCost` does not occur in the released repo; the paper presents this as an
-- illustrative rendering of the hack "encountered ... during benchmark development on dijkstar".
noncomputable def findPathCost : FindPathCostSig :=
  fun g s t => if h : exists c, isMinWalkCost g s t c then h.choose else 0
@[implemented_by realBellmanFord] def findPathCost' := findPathCost

-- Paper p.20: every optimality proof is "definitionally true", while the compiled binary runs a
-- real shortest-path algorithm; "no output difference from the reference across 20,440 generated
-- graphs". Grader response: reject @[implemented_by] in any agent-editable Impl/ file, void the run,
-- grade every spec impl_oracle.
