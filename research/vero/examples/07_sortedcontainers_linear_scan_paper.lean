-- SOURCE: Vero paper, Appendix H.4, page 31. Both snippets are ELIDED IN THE PAPER ITSELF ("..." is the
-- paper's own elision, rendered ". . ." in the PDF). Transcribed from the PDF text layer; indentation restored.

-- Reference (curator) binary search, p.31:
def bisectLeftGo (lst : List a) (val : a) (lo hi : Nat) : Nat :=
  ...
  if ... then bisectLeftGo lst val (mid + 1) hi
  else bisectLeftGo lst val lo mid
termination_by hi - lo

-- GPT-5.5 (xhigh) code-and-proof replacement, p.31:
def linearBisectLeft {a : Type} [Ord a] (value : a) : List a -> Nat
  | [] => 0
  | x :: xs => if ordLt x value then linearBisectLeft value xs + 1 else 0

def insertOrd {a : Type} [Ord a] (value : a) : List a -> List a
  ...
def sortOrd {a : Type} [Ord a] : List a -> List a
  | x :: xs => insertOrd x (sortOrd xs)
