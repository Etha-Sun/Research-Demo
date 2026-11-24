/* SOURCE: build/e2e3-workers-20261106/w36-e2-transposec/work/pkg24/proof/lowered/rvv/x24-transposec-vl-rvv.lowering.json (rewrite log) and build/e2e3-workers-20261106/w36-e2-transposec/work/pkg24/proof/lowered/rvv/x24-transposec-vl-rvv.lowered.c lines 35-38 (rewritten program)
 * What the deterministic rule tool rvv_ptr_lower 1.23.9 did to the RVV target: 2 rewrites (rules R1, R6/R8).
 * Content below is VERBATIM (the log entries are copied from the JSON fields "original"/"rewritten"). */
/* ---- original, impl/x24-transposec-vl-rvv.c lines 34-36 ---- */
      const size_t vl = __riscv_vsetvl_e8m1(bh);
      vuint8m1x3_t tuple = __riscv_vlsseg3e8_v_u8m1x3(i0, input_stride, vl);
      __riscv_vsseg3e8_v_u8m1x3(o0, tuple, vl);
/* ---- after rvv_ptr_lower, proof/lowered/rvv/x24-transposec-vl-rvv.lowered.c lines 35-38 ---- */
      const size_t vl = __riscv_vsetvl_e8m1(bh);
      vuint8m1x3_t tuple;
      qcp_p_vlsseg3e8_v_u8m1x3(&tuple, i0, input_stride, vl);
      qcp_p_vsseg3e8_v_u8m1x3(o0, &tuple, vl);
/* ---- rewrite log (lowering.json "rewrites") ---- */
/* rule R1, line 35 */
/* original:  */ vuint8m1x3_t tuple = __riscv_vlsseg3e8_v_u8m1x3(i0, input_stride, vl);
/* rewritten: */ vuint8m1x3_t tuple;
      qcp_p_vlsseg3e8_v_u8m1x3(&tuple, i0, input_stride, vl);
/* rule R6/R8, line 36 */
/* original:  */ __riscv_vsseg3e8_v_u8m1x3(o0, tuple, vl);
/* rewritten: */ qcp_p_vsseg3e8_v_u8m1x3(o0, &tuple, vl);
/* rule_counts: {'R1': 1, 'R6/R8': 1} ; rejections: [] */
