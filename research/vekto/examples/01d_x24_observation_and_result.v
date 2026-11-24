(* SOURCE: build/e2e3-workers-20261106/w36-e2-transposec/work/pkg24/proof/coq/VektoSpec/Observation.v (full file) + build/e2e3-workers-20261106/w36-e2-transposec/work/pkg24/proof/coq/XtLib/XtDefs.v lines 24-33 + XtBaseE.v lines 12-34
   Observation relation and the abstract transpose result used by both kernel contracts.
   Content below this header is VERBATIM from the source file. *)
(* Observation relation of the E2 transposec packages (x8 / x16 / x24 / x64, element size E bytes).
   The visible effect of a transpose kernel is the set of output bytes it writes: output byte k = j*os + r (column j, byte r of
   that output row) is written iff j < block_width and r / E < block_height (the bytes between E*block_height and the output
   stride are padding which a kernel never touches).  Two runs are related iff the buffers have the same size and agree on every
   written byte.  Bytes that are not written keep the caller's initial contents and are not compared (the buffers may start
   with different contents).  Same relation as E3-35 (w26) with the element size as a parameter. *)
From Coq Require Import ZArith List Bool.
From AUXLib Require Import ListLib Axioms.
From XtLib Require Import XtBaseE.
Local Open Scope Z_scope.

Definition xt_related (E bw bh os : Z) (R1 R2 : list Z) : Prop :=
  Zlength R1 = Zlength R2 /\
  forall k, 0 <= k < Zlength R1 -> xt_cell E bw bh os k = true -> Znth k R1 0 = Znth k R2 0.

(* the relation as named in spec.c (`outputs_related`): element size, block parameters, then the two final output buffers *)
Definition outputs_related (E bw bh os : Z) (R1 R2 : list Z) : Prop := xt_related E bw bh os R1 R2.

(* ---- XtDefs.v lines 24-33 ---- *)
Definition xt_part (E W : Z) (IN OLD : list Z) (bw bh is os jm ir : Z) : list Z :=
  xt_gen (Zlength OLD) (fun k =>
    let j := xt_j bw os k in
    let r := xt_r bw os k in
    let i := r / E in
    let c := r mod E in
    if (j <? bw) && (i <? bh) && xt_done W jm ir j i then Znth (i * is + E * j + c) IN 0 else Znth k OLD 0).

Definition xt_result (E : Z) (IN OLD : list Z) (bw bh is os : Z) : list Z :=
  xt_part E 1 IN OLD bw bh is os bw 0.

(* ---- XtBaseE.v lines 12-34 ---- *)
Definition xt_nout (E bw bh os : Z) : Z := (bw - 1) * os + E * bh.
Definition xt_nin_exact (E bw bh is : Z) : Z := (bh - 1) * is + E * bw.

(* input window readable by a kernel that loads whole tile rows in the last column group (XNN_OOB_READS):
   T = bytes read per row in that group; the rows before the last start at multiples of is. *)
Definition xt_nin_rows (bh is last_row_bytes : Z) : Z := (bh - 1) * is + last_row_bytes.
(* x16 SSE2 8x8, x8 SSE2 16x16: 16-byte row loads, groups of 16/E columns *)
Definition xt_last16 (E bw : Z) : Z := 16 * ((E * bw + 15) / 16).
(* x24 SSSE3 4x4: 16-byte row loads at byte offset 12 * (group index) *)
Definition xt_last24 (bw : Z) : Z := 12 * ((bw - 1) / 4) + 16.

(* decomposition of an output byte index *)
Definition xt_j (bw os k : Z) : Z := if bw =? 1 then 0 else k / os.
Definition xt_r (bw os k : Z) : Z := if bw =? 1 then k else k mod os.

Definition xt_cell (E bw bh os k : Z) : bool :=
  (xt_j bw os k <? bw) && (xt_r bw os k / E <? bh).

(* the XNNPACK asserts as 0/1 flags (opaque to QCP, see the w26 note on pure `||` in callee Require):
   x8 / x16 / x64:  block_width == 1 || os >= bh * E   (and symmetric for the input)
   x24:             os >= 3 * bh  and  is >= 3 * bw    (unconditional asserts) *)
Definition xt_strideok (E w h s : Z) : Z := if (w =? 1) || (E * h <=? s) then 1 else 0.
Definition xt_strideok_all (E w h s : Z) : Z := if E * h <=? s then 1 else 0.
