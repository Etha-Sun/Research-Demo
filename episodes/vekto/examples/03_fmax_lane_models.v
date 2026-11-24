(* SOURCE: build/e2e3-workers-20261106/intrinsics-v1.7.3/neon/NeonLib.v lines 87-89, 105-107 and
   build/e2e3-workers-20261106/intrinsics-v1.7.3/rvv/RvvModel.v lines 62-64 (copied in research/vekto/examples/02e_fmax_lane_models.v).
   TRIMS: only the NaN-handling lines are shown; the ordered-comparison branches are replaced by "...". Verbatim otherwise.
   Screen panel 1 = NEON lines, panel 2 = RVV lines. *)
(* panel 1: NEON FMAX, NeonLib.v *)
Definition nl_procnan (x y : Z) : option Z :=
  if issnan x then Some (quiet x) else if issnan y then Some (quiet y)
  else if isnan x then Some x else if isnan y then Some y else None.
Definition nl_fmax (x y : Z) : Z :=
  match nl_procnan x y with
  | Some r => r
  ...
(* panel 2: RVV vfmax = maximumNumber, RvvModel.v *)
Definition rv_fmax (a b : Z) : Z :=
  if isnan32 a then (if isnan32 b then cnan_bits else b)
  else if isnan32 b then a
  ...
