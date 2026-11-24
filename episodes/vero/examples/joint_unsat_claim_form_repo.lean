-- SOURCE: github.com/sunblaze-ucb/vero @ 0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09
--   benchmarks/dijkstar/Dijkstar/Harness.lean lines 34-35 (doc comment of the joint_unsat macro, verbatim);
--   the same macro is in benchmarks/verdict/Verdict/Harness.lean lines 54-66 (research/vero/examples/01d_*).
--   This is the generic FORM of a joint-unsat claim, not the agent's verdict proof (which is not published).
theorem joint_unsat.spec_A.spec_B.… :
    ¬ ∃ impl : RepoImpl, spec_A impl ∧ spec_B impl ∧ … := by <proof>
