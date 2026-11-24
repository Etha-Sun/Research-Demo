-- SOURCE: Vero paper, Appendix D "Layer 2: axiom allowlist", page 19 (verbatim, line numbers removed);
-- via research/vero/examples/04_base58_native_decide_paper.lean. Produced by GPT-5.5 (xhigh) on base58.
theorem b58Idx_b58Char_fin (d : Fin 58) :
    b58Idx (b58Char d.val) = some d.val := by
  native_decide +revert
