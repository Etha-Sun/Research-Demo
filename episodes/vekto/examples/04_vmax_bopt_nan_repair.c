/* SOURCE: research/project-plan-20261102/vmax-performance/repair.patch (copied in research/vekto/examples/02f_vmax_bopt_nan_repair.patch)
 * Candidate NaN repair of Bopt, first hunk: the vfmax line followed by the 4 added statements. Verbatim, indentation removed,
 * diff "+" markers removed. Measured on Saturn RTL (+18.8 % cycles, geometric mean); regression-tested, NOT formally proved,
 * not adopted as the E1 result. Screen content starts below this header. */
vfloat32m8_t vacc = __riscv_vfmax_vv_f32m8(va, vb, vlmax);
vbool4_t a_nan = __riscv_vmfne_vv_f32m8_b4(va, va, vlmax);
vbool4_t b_nan = __riscv_vmfne_vv_f32m8_b4(vb, vb, vlmax);
vbool4_t any_nan = __riscv_vmor_mm_b4(a_nan, b_nan, vlmax);
vacc = __riscv_vfmerge_vfm_f32m8(vacc, __builtin_nanf(""), any_nan, vlmax);
