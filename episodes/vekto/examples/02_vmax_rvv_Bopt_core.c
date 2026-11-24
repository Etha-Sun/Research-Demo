/* SOURCE: research/project-plan-20261102/final-minmax-reproduction/vmax/rvv.c (copied in research/vekto/examples/02b_vmax_rvv_Bopt.c)
 * E1 kernel Bopt, LLM-optimised RVV f32-vmax (optimized-rvv-kernels@80feb4564). Main-loop body, original lines 33-40.
 * TRIMS: comments and blank lines dropped (kept lines are verbatim apart from leading indentation). Header comment line added.
 * Screen content starts below this header. */
/* Bopt: LLM-optimised RVV, VLMAX floats per step */
vfloat32m8_t va = __riscv_vle32_v_f32m8(input_a, vlmax);
vfloat32m8_t vb = __riscv_vle32_v_f32m8(input_b, vlmax);
vfloat32m8_t vacc = __riscv_vfmax_vv_f32m8(va, vb, vlmax);
__riscv_vse32_v_f32m8(output, vacc, vlmax);
