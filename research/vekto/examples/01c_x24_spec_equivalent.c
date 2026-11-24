/* SOURCE: build/e2e3-workers-20261106/w36-e2-transposec/work/pkg24/spec.c
 * The human-reviewed equivalence spec: equivalent() calls both kernels on the same input, separate outputs. Full file, 50 lines.
 * Content below this header is VERBATIM from the source file. */
/* x24 transposec: SSSE3 4x4 (x86, source) versus the strided 3-plane segment RVV target (target).
 * Both kernels run on the same input with the same block parameters into two separate output buffers; the outputs must be
 * related under spec/observation.v (outputs_related): same size, equal on every output byte that a transpose writes
 * (output byte k = j*os + r is written iff j < block_width and r / 3 < block_height).
 * Input domain = the XNNPACK preconditions of both kernels (the asserts of x24 are unconditional: output_stride >= 3 * block_height, input_stride >= 3 * block_width; xt_strideok_all(3, w, h, s) == 1 iff 3 * h <= s) plus
 *   [VEKTO-C-022] block_width >= 1 and block_height >= 1;
 *   [VEKTO-C-024] PI + nin16, PA + nout, PB + nout <= UINT64_MAX (no address wrap);
 *   [VEKTO-C-候选 XNN_OOB_READS] the input is readable for nin16 = (block_height-1)*input_stride + xt_last24(block_width) bytes, xt_last24(w) = 12*((w-1)/4)+16:
 *     the SSSE3 kernel loads whole 16-byte vectors at byte offset 12 * (column group) in every row (it is declared XNN_OOB_READS, XNN_EXTRA_BYTES = 16 covers the over-read);
 *     the RVV target reads exactly (block_height-1)*input_stride + 3*block_width bytes, a prefix of that window (same kind as C-032 of x8-transposec);
 *   [VEKTO-C-031] nin16 <= INT64_MAX;
 *   vsl_ok(XT_N, vf): vf models vsetvl of RVV 1.0 for SEW = 8, LMUL = 1 and VLEN = 8 * XT_N (non-deterministic, library model).
 * The input and the two outputs are pairwise disjoint (separating conjunction).
 * Environment premises: ledger.json. */
/*@ Import Coq Require Import VektoSpec.Observation */
/*@ Import Coq Require Import XtLib.XtBaseE */
/*@ Import Coq Require Import XtLib.XtDefs */
/*@ Import Coq Require Import VektoRvv.RvvModel */
/*@ Extern Coq (outputs_related : Z -> Z -> Z -> Z -> list Z -> list Z -> Prop)
               (xt_nin_rows : Z -> Z -> Z -> Z)
               (xt_last24 : Z -> Z)
               (xt_nout : Z -> Z -> Z -> Z -> Z)
               (xt_strideok_all : Z -> Z -> Z -> Z -> Z)
               (vsl_ok : Z -> (Z -> Z) -> Prop) */
void equivalent(
    const uint8_t* input,
    uint8_t* output_a,
    uint8_t* output_b,
    size_t input_stride,
    size_t output_stride,
    size_t block_width,
    size_t block_height)
/*@ With (IN : list Z) (OLD1 : list Z) (OLD2 : list Z) (BW : Z) (BH : Z) (IS : Z) (OS : Z) (PI : Z) (PA : Z) (PB : Z) (vf : Z -> Z)
    Require input == PI && output_a == PA && output_b == PB && input_stride == IS && output_stride == OS &&
            block_width == BW && block_height == BH &&
            1 <= BW && 1 <= BH && xt_strideok_all(3, BW, BH, OS) == 1 && xt_strideok_all(3, BH, BW, IS) == 1 && vsl_ok(XT_N, vf) &&
            0 <= PI && PI + xt_nin_rows(BH, IS, xt_last24(BW)) <= 18446744073709551615 &&
            xt_nin_rows(BH, IS, xt_last24(BW)) <= 9223372036854775807 &&
            0 <= PA && PA + xt_nout(3, BW, BH, OS) <= 18446744073709551615 &&
            0 <= PB && PB + xt_nout(3, BW, BH, OS) <= 18446744073709551615 &&
            UCharArray::full(PI, xt_nin_rows(BH, IS, xt_last24(BW)), IN) * UCharArray::full(PA, xt_nout(3, BW, BH, OS), OLD1) *
            UCharArray::full(PB, xt_nout(3, BW, BH, OS), OLD2)
    Ensure exists (R1 : list Z) (R2 : list Z),
            outputs_related(3, BW, BH, OS, R1, R2) &&
            UCharArray::full(PI, xt_nin_rows(BH, IS, xt_last24(BW)), IN) * UCharArray::full(PA, xt_nout(3, BW, BH, OS), R1) *
            UCharArray::full(PB, xt_nout(3, BW, BH, OS), R2) */
{
  xnn_x24_transposec_ukernel__4x4_ssse3(input, output_a, input_stride, output_stride, block_width, block_height);
  xnn_x24_transposec_ukernel__vlx1_rvv(input, output_b, input_stride, output_stride, block_width, block_height);
}
