/* SOURCE: build/e2e3-workers-20261106/w36-e2-transposec/work/pkg24/impl/x24-transposec-vl-rvv.c
 * x24 transposec TARGET kernel (RVV), new code written for E2 by worker w36 and frozen (ledger.json targets.rvv). Full file, 45 lines.
 * Content below this header is VERBATIM from the source file. */
// Copyright 2026 Google LLC
//
// This source code is licensed under the BSD-style license found in the
// LICENSE file in the root directory of this source tree.

#include <riscv_vector.h>

#include <assert.h>

#include "src/xnnpack/common.h"
#include "src/xnnpack/math.h"
#include "src/xnnpack/transpose.h"

// Vector-length agnostic transpose of 3-byte elements: the block height is
// strip-mined with vsetvl; one column is handled per pass, a strided segment
// load of 3 byte planes (the load performs the transpose) followed by an
// interleaving segment store of the 3 planes into the output row.
void xnn_x24_transposec_ukernel__vlx1_rvv(
  const void* input,
  void* output,
  size_t input_stride,
  size_t output_stride,
  size_t block_width,
  size_t block_height) XNN_OOB_READS
{
  assert(output_stride >= block_height * 3);
  assert(input_stride >= block_width * 3);

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
}
