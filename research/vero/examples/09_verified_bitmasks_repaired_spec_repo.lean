-- SOURCE: github.com/sunblaze-ucb/vero @ 0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09
--   benchmarks/VerifiedBitmasks/VerifiedBitmasks/Spec/BitmaskImplIF.lean, lines 93-96 (verbatim): released spec after the
--   audit added the 'A.length = B.length' precondition (paper Appendix F Audit 3, p.25).

def spec_bIIF_and_nbits_preserved (impl : RepoImpl) : Prop :=
  ∀ (A B : T), A.length = B.length →
    impl.verifiedBitmasks.bIIF_nbits (impl.verifiedBitmasks.bIIF_and A B) =
      impl.verifiedBitmasks.bIIF_nbits A
