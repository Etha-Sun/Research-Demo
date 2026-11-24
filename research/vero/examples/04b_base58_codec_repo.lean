-- SOURCE: github.com/sunblaze-ucb/vero @ 0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09
--   benchmarks/base58/Base58/Impl/Codec.lean lines 41-47 (verbatim): the functions the native_decide proof is about.

/-- `b58Idx c`: the base58 digit value of character `c` — its index in the
    frozen alphabet — or `none` if `c` is not a base58 character. -/
def b58Idx (c : Char) : Option Nat := b58Alphabet.idxOf? c

/-- `b58Char n`: the `n`-th frozen-alphabet character. Out-of-range indices fall
    back to `'1'` (the zero digit); callers only ever pass `n < 58`. -/
def b58Char (n : Nat) : Char := b58Alphabet.getD n '1'
