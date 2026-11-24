/* SCREEN-SIMPLIFIED version of 01a (x86 SSSE3) and 01b (RVV). NOT verbatim.
 * Original locations (line numbers refer to the original .c files, i.e. the lines after the 3-line header of examples/01a and 01b):
 *   SSSE3: impl/x24-transposec-4x4-ssse3.c lines 70-74 (loop head + 4 loads) and line 97 (one store); everything else in
 *          the tile body (lines 75-115: pointer bumps, 7 unpacks, 6 pshufb with tables pos0..pos5, 2 ORs, 7 more stores) and the
 *          tail (lines 117-182) replaced by "..." comments.
 *   RVV:   impl/x24-transposec-vl-rvv.c lines 29-44; comments removed, the three pointer updates written as
 *          "i0 += ...; o0 += ...; input += 3; output += output_stride;" instead of the original (uintptr_t) casts
 *          (lines 37, 41, 42), and the i0/o0 declarations (lines 30-31) dropped.
 * Verbatim originals: examples/01a_x24_source_ssse3_full.c, examples/01b_x24_target_rvv_full.c. */
/* x86 SSSE3 source (XNNPACK): 4x4 tiles of 3-byte pixels, byte shuffles */
for (; bh >= 4; bh -= 4) {
  const __m128i v0 = _mm_loadu_si128((const __m128i*) i0);   /* 16 bytes per row */
  const __m128i v1 = _mm_loadu_si128((const __m128i*) i1);
  const __m128i v2 = _mm_loadu_si128((const __m128i*) i2);
  const __m128i v3 = _mm_loadu_si128((const __m128i*) i3);
  ...  /* 7 unpacks, 6 pshufb with tables pos0..pos5, 2 ORs */
  _mm_storel_epi64((__m128i*) o0, v4_0);
  ...
}
... /* tail: bh = 1..3 rows, separate store paths */

/* RVV target (new): one column per pass, the strided segment load does the transpose */
do {
  size_t bh = block_height;
  while (bh != 0) {
    const size_t vl = __riscv_vsetvl_e8m1(bh);
    vuint8m1x3_t tuple = __riscv_vlsseg3e8_v_u8m1x3(i0, input_stride, vl);
    __riscv_vsseg3e8_v_u8m1x3(o0, tuple, vl);
    i0 += vl * input_stride;  o0 += vl * 3;  bh -= vl;
  }
  input += 3;  output += output_stride;  block_width -= 1;
} while (block_width != 0);
