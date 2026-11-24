-- SOURCE: Vero paper, Appendix F "Audit 1", page 24 (PRE-FIX specifications as printed in the paper).
-- Transcribed verbatim from the PDF text layer; line numbers removed; indentation restored by hand.
def spec_char_to_bits_padding (impl : RepoImpl) : Prop :=
  impl.verdict.charToBits 0x3D = some none

def spec_char_to_bits_reject (impl : RepoImpl) : Prop :=
  ∀ (c : UInt8),
    (c < 0x2B ∨ (c > 0x2B ∧ c < 0x2F) ∨
     (c > 0x39 ∧ c < 0x41) ∨ (c > 0x5A ∧ c < 0x61) ∨ c > 0x7A) →
    impl.verdict.charToBits c = none

-- Paper's fix (page 24, verbatim; the PDF glyph is "̸=", i.e. ≠):
--   (c > 0x39 ∧ c < 0x41 ∧ c ≠ 0x3D) ∨ -- excluded '='
-- Why they conflict (paper p.24): '=' is 0x3D, and 0x39 < 0x3D < 0x41, so _reject demands
-- charToBits 0x3D = none while _padding demands some none. GPT-5.5 (xhigh) closed a
-- joint-unsatisfiability proof that "collapses to a one-line 0x3D < 0x41 ∧ 0x3D > 0x39 contradiction".
-- The agent's actual proof script is NOT printed in the paper and is not in the repo.
