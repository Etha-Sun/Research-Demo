/* SCREEN-SIMPLIFIED. NOT verbatim. Derived from:
 *   examples/02a_vmax_neon_A.c   = research/project-plan-20261102/final-minmax-reproduction/vmax/neon.c   lines 20-27 (main loop)
 *   examples/02b_vmax_rvv_Bopt.c = research/project-plan-20261102/final-minmax-reproduction/vmax/rvv.c    lines 24-48 (main loop)
 * Changes: asserts, the NEON 1..3-element tail (lines 28-42), the RVV variable-length tail (lines 52-61), all comments and the
 * `const` qualifiers were dropped; the RVV loop counter `n` and the `batch` byte counter are shown as in the originals. */

/* A: original NEON (from XNNPACK via SALTy-rn) -- 4 floats per step */
for (; batch >= 4 * sizeof(float); batch -= 4 * sizeof(float)) {
  float32x4_t va = vld1q_f32(input_a); input_a += 4;
  float32x4_t vb = vld1q_f32(input_b); input_b += 4;
  float32x4_t vacc = vmaxq_f32(va, vb);          /* Arm FMAX: NaN in -> NaN out */
  vst1q_f32(output, vacc); output += 4;
}

/* Bopt: agent-optimized RVV for Saturn -- LMUL=8, VLMAX floats per step */
size_t vlmax = __riscv_vsetvlmax_e32m8();
while (n >= vlmax) {
  vfloat32m8_t va = __riscv_vle32_v_f32m8(input_a, vlmax);
  vfloat32m8_t vb = __riscv_vle32_v_f32m8(input_b, vlmax);
  vfloat32m8_t vacc = __riscv_vfmax_vv_f32m8(va, vb, vlmax);   /* RVV vfmax: maximumNumber, NaN is ignored */
  __riscv_vse32_v_f32m8(output, vacc, vlmax);
  input_a += vlmax; input_b += vlmax; output += vlmax; n -= vlmax;
}
