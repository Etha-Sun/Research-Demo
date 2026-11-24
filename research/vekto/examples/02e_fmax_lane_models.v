(* SOURCE: build/e2e3-workers-20261106/intrinsics-v1.7.3/neon/NeonLib.v lines 87-89 and 102-110 (NEON FMAX lane model) and build/e2e3-workers-20261106/intrinsics-v1.7.3/rvv/RvvModel.v lines 59-68 (RVV vfmax lane model)
   Unified intrinsic library v1.7.3 (lane functions are differentially tested against real instructions under QEMU). VERBATIM. *)
(* ---- NeonLib.v lines 87-89 ---- *)
Definition nl_procnan (x y : Z) : option Z :=
  if issnan x then Some (quiet x) else if issnan y then Some (quiet y)
  else if isnan x then Some x else if isnan y then Some y else None.
(* ---- NeonLib.v lines 102-110 ---- *)
(* order key of a non-NaN pattern (signed magnitude -> integer order; -0 and +0 both 0) *)
Definition fkey (b : Z) : Z := if fsgn b then - (b mod 2147483648) else b.
(* FMAX / FMIN (not the NM variants): NaN propagates (FPProcessNaNs); +0 > -0 *)
Definition nl_fmax (x y : Z) : Z :=
  match nl_procnan x y with
  | Some r => r
  | None => if fkey x <? fkey y then y else if fkey y <? fkey x then x
            else if fkey x =? 0 then (if fsgn x then y else x) else x
  end.

(* ---- RvvModel.v lines 59-68 ---- *)

(* vfmax / vfmin (IEEE 754-2019 maximumNumber / minimumNumber): one NaN operand is ignored, two NaNs give the canonical NaN,
   max(-0,+0) = +0, min(-0,+0) = -0 *)
Definition rv_fmax (a b : Z) : Z :=
  if isnan32 a then (if isnan32 b then cnan_bits else b)
  else if isnan32 b then a
  else match Binary.Bcompare 24 128 (of32 a) (of32 b) with
       | Some Datatypes.Lt => b
       | Some Datatypes.Gt => a
       | _ => if sign32 a then b else a
