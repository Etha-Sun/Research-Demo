/* SOURCE: build/e2e3-workers-20261106/w36-e2-transposec/work/pkg24/impl/x24-transposec-vl-rvv.c lines 29-44
 * (new RVV target written for E2 and frozen, ledger.json targets.rvv; copied in research/vekto/examples/01b_*)
 * VERBATIM, indentation reduced by 2 spaces. Screen content starts below this header. */
do {
  const uint8_t* i0 = (const uint8_t*) input;
  uint8_t* o0 = (uint8_t*) output;
  size_t bh = block_height;
  while (bh != 0) {
    const size_t vl = __riscv_vsetvl_e8m1(bh);
    vuint8m1x3_t tuple = __riscv_vlsseg3e8_v_u8m1x3(i0, input_stride, vl);
    __riscv_vsseg3e8_v_u8m1x3(o0, tuple, vl);
    i0 = (const uint8_t*) ((uintptr_t) i0 + vl * input_stride);
    o0 += vl * 3;
    bh -= vl;
  }
  input = (const void*) ((uintptr_t) input + 3);
  output = (void*) ((uintptr_t) output + output_stride);
  block_width -= 1;
} while (block_width != 0);
