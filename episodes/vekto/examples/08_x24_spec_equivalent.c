/* SOURCE: build/e2e3-workers-20261106/w36-e2-transposec/work/pkg24/spec.c (copied in research/vekto/examples/01c_*)
 * TRIMS for the screen: the 7 parameters are shown as "input, output_a, output_b, ..."; in the With list only IN and vf are
 * kept; the Require keeps the clauses for C-022 (1 <= BW && 1 <= BH), vsl_ok, C-024 for the input (PI + nin16 <= UINT64_MAX)
 * and the input ownership atom; other clauses (variable bindings, stride asserts, C-031, output bounds, output atoms) are "...".
 * The Ensure keeps outputs_related; the two kernel calls keep their first two arguments. Long lines are broken.
 * No clause is changed. Screen content starts below this header. */
void equivalent(const uint8_t* input,
    uint8_t* output_a, uint8_t* output_b, ...)
/*@ With (IN : list Z) ... (vf : Z -> Z)
    Require ... &&
      1 <= BW && 1 <= BH && ... && vsl_ok(XT_N, vf) &&
      0 <= PI && PI + xt_nin_rows(BH, IS, xt_last24(BW))
                   <= 18446744073709551615 && ...
      UCharArray::full(PI, xt_nin_rows(BH, IS, xt_last24(BW)), IN) * ...
    Ensure exists (R1 : list Z) (R2 : list Z),
      outputs_related(3, BW, BH, OS, R1, R2) && ... */
{
  xnn_x24_transposec_ukernel__4x4_ssse3(input, output_a, ...);
  xnn_x24_transposec_ukernel__vlx1_rvv(input, output_b, ...);
}
