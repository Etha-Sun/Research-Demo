-- SOURCE: github.com/sunblaze-ucb/vero @ 0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09
--   benchmarks/verdict/Verdict/Impl/Base64.lean, lines 45-65 (verbatim): reference implementation.
-- Note line 'else if c = 0x3D then some none' - the reference agreed with _padding, so the bug was in _reject.

-- !benchmark @start code_aux def=charToBits
-- !benchmark @end code_aux def=charToBits

def Verdict.charToBits : Verdict.CharToBitsSig :=
-- !benchmark @start code def=charToBits
  fun c =>
    -- 'A'..'Z' → 0..25
    if c ≥ 0x41 ∧ c ≤ 0x5A then some (some (c - 0x41))
    -- 'a'..'z' → 26..51
    else if c ≥ 0x61 ∧ c ≤ 0x7A then some (some (c - 0x61 + 26))
    -- '0'..'9' → 52..61
    else if c ≥ 0x30 ∧ c ≤ 0x39 then some (some (c - 0x30 + 52))
    -- '+' → 62
    else if c = 0x2B then some (some 62)
    -- '/' → 63
    else if c = 0x2F then some (some 63)
    -- '=' → padding
    else if c = 0x3D then some none
    -- invalid
    else none
-- !benchmark @end code def=charToBits
