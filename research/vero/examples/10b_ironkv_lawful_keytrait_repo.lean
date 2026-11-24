-- SOURCE: github.com/sunblaze-ucb/vero @ 0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09
--   benchmarks/VerifiedIronkv/VerifiedIronkv/Impl/DelegationMapV.lean, lines 59-65 (verbatim, truncated at line 65): the
--   LawfulKeyTrait repair introduced after Audit 2.

class LawfulKeyTrait (K : Type) [KeyTrait K] : Prop where
  cmp_refl : ∀ a : K, KeyTrait.cmp_spec a a = KeyOrdering.Equal
  cmp_antisymm : ∀ a b : K,
    orderingLeBool (KeyTrait.cmp_spec a b) = true →
    orderingLeBool (KeyTrait.cmp_spec b a) = true → a = b
  le_lt_trans : ∀ a b c : K,
    orderingLeBool (KeyTrait.cmp_spec a b) = true →
