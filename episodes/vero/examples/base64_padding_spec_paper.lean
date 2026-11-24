-- SOURCE: Vero paper, Appendix F "Audit 1", page 24 (PRE-FIX), lines 1-2 of the paper listing (verbatim, line
-- numbers removed, indentation restored); via research/vero/examples/02a_verdict_charToBits_conflict_paper.lean.
def spec_char_to_bits_padding (impl : RepoImpl) : Prop :=
  impl.verdict.charToBits 0x3D = some none
