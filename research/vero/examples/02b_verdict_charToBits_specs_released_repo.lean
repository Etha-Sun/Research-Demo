-- SOURCE: github.com/sunblaze-ucb/vero @ 0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09
--   benchmarks/verdict/Verdict/Spec/Base64.lean, lines 38-48 (verbatim): RELEASED (post-fix) specs.
-- NOTE: the released fix splits the gap into (0x39,0x3D) ∨ (0x3D,0x41) rather than the paper's
-- 'c ≠ 0x3D' conjunct; logically equivalent for UInt8, different text.

/-- `charToBits` emits `some none` on the padding character `=`. -/
def spec_char_to_bits_padding (impl : RepoImpl) : Prop :=
  impl.verdict.charToBits 0x3D = some none

/-- `charToBits` rejects any character outside the Base64 alphabet. -/
def spec_char_to_bits_reject (impl : RepoImpl) : Prop :=
  ∀ (c : UInt8),
    (c < 0x2B ∨ (c > 0x2B ∧ c < 0x2F) ∨
     (c > 0x39 ∧ c < 0x3D) ∨ (c > 0x3D ∧ c < 0x41) ∨
     (c > 0x5A ∧ c < 0x61) ∨ c > 0x7A) →
    impl.verdict.charToBits c = none
