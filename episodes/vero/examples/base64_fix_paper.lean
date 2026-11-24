-- SOURCE: Vero paper, Appendix F "Audit 1", page 24: the paper's fix, line 1 of its listing (verbatim; the PDF glyph
-- for "not equal" is rendered as ≠). It replaces the (c > 0x39 ∧ c < 0x41) disjunct of spec_char_to_bits_reject.
-- NOTE: the released repo (benchmarks/verdict/Verdict/Spec/Base64.lean lines 42-48) instead splits the range into
-- (c > 0x39 ∧ c < 0x3D) ∨ (c > 0x3D ∧ c < 0x41); logically equivalent for UInt8. The video shows the paper's version.
(c > 0x39 ∧ c < 0x41 ∧ c ≠ 0x3D) ∨ -- excluded '='
