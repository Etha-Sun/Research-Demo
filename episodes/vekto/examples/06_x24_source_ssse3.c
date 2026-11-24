/* SOURCE: build/e2e3-workers-20261106/w36-e2-transposec/work/pkg24/impl/x24-transposec-4x4-ssse3.c
 * (byte-identical to XNNPACK 867d5a34 src/x24-transposec/x24-transposec-4x4-ssse3.c; copied in research/vekto/examples/01a_*)
 * Shown lines (original numbering): 70-74, 80, 89, 97 and the closing brace of the tile loop; everything else of the tile
 * body (pointer bumps, 6 more unpacks, 5 more shuffles/ORs, 7 more stores) and the 1-3 row tail replaced by "...".
 * Indentation reduced by 4 spaces. Kept lines verbatim. Screen content starts below this header. */
for (; bh >= 4; bh -= 4) {
  const __m128i v0 = _mm_loadu_si128((const __m128i*) i0);
  const __m128i v1 = _mm_loadu_si128((const __m128i*) i1);
  const __m128i v2 = _mm_loadu_si128((const __m128i*) i2);
  const __m128i v3 = _mm_loadu_si128((const __m128i*) i3);
  ...
  const __m128i v1_0 = _mm_unpacklo_epi8(v0, v1);
  ...
  __m128i v4_0 = _mm_shuffle_epi8(v3_0, vperm0);
  ...
  _mm_storel_epi64((__m128i*) o0, v4_0);
  ...
}
... /* tail: 1-3 remaining rows */
