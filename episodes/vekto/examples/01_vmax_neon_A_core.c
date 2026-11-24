/* SOURCE: research/project-plan-20261102/final-minmax-reproduction/vmax/neon.c (copied in research/vekto/examples/02a_vmax_neon_A.c)
 * E1 kernel A, original NEON f32-vmax (SALTy-rn be16280c7). Main-loop body, original lines 21-26.
 * TRIMS: `const` qualifiers dropped; the pointer bumps `input_a += 4;` / `input_b += 4;` / `output += 4;` dropped;
 * blank lines dropped. Header comment line added for the screen. Meaning unchanged.
 * Screen content starts below this header. */
/* A: original NEON, 4 floats per step */
float32x4_t va = vld1q_f32(input_a);
float32x4_t vb = vld1q_f32(input_b);
float32x4_t vacc = vmaxq_f32(va, vb);
vst1q_f32(output, vacc);
