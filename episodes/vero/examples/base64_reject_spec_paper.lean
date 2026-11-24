-- SOURCE: Vero paper, Appendix F "Audit 1", page 24 (PRE-FIX), lines 4-8 of the paper listing (verbatim, line
-- numbers removed, indentation restored); via research/vero/examples/02a_verdict_charToBits_conflict_paper.lean.
def spec_char_to_bits_reject (impl : RepoImpl) : Prop :=
  ∀ (c : UInt8),
    (c < 0x2B ∨ (c > 0x2B ∧ c < 0x2F) ∨
     (c > 0x39 ∧ c < 0x41) ∨ (c > 0x5A ∧ c < 0x61) ∨ c > 0x7A) →
    impl.verdict.charToBits c = none
