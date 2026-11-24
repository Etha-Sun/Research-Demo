-- SOURCE: Vero paper, Appendix G "Replacing an algorithm with a simpler one", page 26.
-- Transcribed verbatim from the PDF text layer; line numbers removed; indentation restored by hand.
-- Submitted (in essentially the same form, per the paper) by GPT-5.5 (xhigh), GPT-5.5 (mid) and Claude Opus 4.8
-- in code-and-proof mode; replaces the 409-line Hungarian-algorithm reference with a 164-line brute force.
def permsAuxImpl : List Nat -> List (List Nat)
  | [] => [[]]
  | x :: xs => (permsAuxImpl xs).flatMap (fun p => insertEverywhereImpl x p)

def permCostImpl (M : List (List Nat)) (p : List Nat) : Nat :=
  sumN ((List.range p.length).map (fun i => matGetN M i (natGet p i)))

def bestPermFrom (M : List (List Nat)) (best : List Nat) : List (List Nat) -> List Nat
  | [] => best
  | p :: ps =>
    if permCostImpl M p < permCostImpl M best then bestPermFrom M p ps
    else bestPermFrom M best ps
