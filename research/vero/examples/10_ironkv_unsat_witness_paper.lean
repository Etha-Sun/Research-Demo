-- SOURCE: Vero paper, Appendix F "Audit 2", page 25. Agent: GPT-5.5 (xhigh).
-- Transcribed from the PDF text layer; line numbers removed; indentation restored by hand.
-- The text layer shows the anonymous-constructor brackets correctly as ⟨ ⟩ here.
theorem unsat_strictly_ordered_vec_no_duplicates :
    ¬ (∃ impl : RepoImpl,
        spec_strictly_ordered_vec_no_duplicates impl) := by
  intro ⟨impl, h⟩
  -- Adversarial KeyTrait: cmpSpec returns Less for every pair.
  let bad : KeyTrait Unit :=
    { zeroSpec := (), cmpSpec := fun _ _ => Ordering.Less }
  -- A two-element vector of () is valid under bad but has duplicates.
  let s : StrictlyOrderedVec Unit := ⟨[(), ()]⟩
  exact (h _ bad s (by intro i j _; rfl)) ⟨0, 1⟩ rfl rfl
