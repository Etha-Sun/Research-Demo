-- SOURCE: Vero paper, Appendix D "Layer 3: declaration screening", pages 19-20.
-- Transcribed from the PDF text layer. The text layer shows anonymous-constructor brackets as
-- "<" ">"; in Lean source these are probably ⟨ ⟩ (the same text layer renders ⟨ ⟩ correctly on p.25, so this is unconfirmed). We print ⟨ ⟩ below - THIS IS THE ONLY CHANGE.
-- Verbatim text-layer forms are kept in the trailing comments.

-- (1) Hollow body (p.19)
instance : LE Float := ⟨fun _ _ => True⟩            -- text layer: instance : LE Float := <fun _ _ => True>

-- (2) Priority shadowing (p.20)
instance (priority := 2000) : LT Float := ⟨fun _ _ => True⟩   -- text layer: ... := <fun _ _ => True>

-- (3) Decidability laundering (p.20), verbatim
instance : DecidableEq (Foo -> Bar) := fun _ _ => .isTrue (by sorry)
theorem prove_x : spec_x canonical := by decide
