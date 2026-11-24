/* SOURCE: build/e2e3-workers-20261106/w04-e3-s8rmax/work/impl/s8-rmax-neon-u32-acc2.c lines 33-65
 * E3-33 kernel A: XNNPACK NEON s8-rmax-neon-u32-acc2 (main loops + scalar tail). VERBATIM excerpt. */

  xnn_simd_s8_t vmax0 = xnn_set1_s8(output[0]);
  xnn_simd_s8_t vmax1 = vmax0;

  for (; batch >= 32 * sizeof(int8_t); batch -= 32 * sizeof(int8_t)) {
    xnn_simd_s8_t vt0 = xnn_loadu_s8(input + 0 * xnn_simd_size_s8);
    xnn_simd_s8_t vt1 = xnn_loadu_s8(input + 1 * xnn_simd_size_s8);
    input += 2 * xnn_simd_size_s8;

    vmax0 = xnn_max_s8(vmax0, vt0);
    vmax1 = xnn_max_s8(vmax1, vt1);
  }
  vmax0 = xnn_max_s8(vmax0, vmax1);

  for (; batch >= xnn_simd_bytes_s8; batch -= xnn_simd_bytes_s8) {
    xnn_simd_s8_t vt = xnn_loadu_s8(input);
    input += xnn_simd_size_s8;

    vmax0 = xnn_max_s8(vmax0, vt);
  }

  int8_t max0 = xnn_reduce_max_s8(vmax0);

  if XNN_UNLIKELY(batch != 0) {
    do {
      const int8_t vt = *input++;

      max0 = vt > max0 ? vt : max0;
    } while (--batch != 0);
  }

  *output = max0;
}
