-- SOURCE: Vero paper, Appendix D "Layer 2: axiom allowlist", page 19.
-- Transcribed verbatim from the PDF text layer; line numbers removed; indentation restored by hand.
-- Produced by GPT-5.5 (xhigh) on base58. The agent proof is not in the released repo.
theorem b58Idx_b58Char_fin (d : Fin 58) :
    b58Idx (b58Char d.val) = some d.val := by
  native_decide +revert

-- Paper p.19: native_decide evaluates in the compiler, not the kernel, and records a dependency on
-- Lean.ofReduceBool, which is outside the allowlist {Classical.choice, propext, Quot.sound}.
-- "Twenty-eight of that cell's 53 specifications fail for this reason while 25 pass."
