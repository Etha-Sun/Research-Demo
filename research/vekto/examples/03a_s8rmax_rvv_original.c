/* SOURCE: build/e2e3-workers-20261106/w04-e3-s8rmax/work/impl/s8-rmax-rvv-u8v.c lines 22-44
 * E3-33 kernel B: XNNPACK RVV s8-rmax (generated from src/s8-rminmax/rvv.c.in, XNNPACK 867d5a34), as copied into the w04 package. VERBATIM excerpt. */
void xnn_s8_rmax_ukernel__rvv_u8v(
    size_t batch,
    const int8_t* input,
    int8_t* output,
    const void* params)
{
  assert(batch != 0);
  assert(batch % sizeof(int8_t) == 0);
  assert(input != NULL);
  assert(output != NULL);

  size_t vlmax = __riscv_vsetvl_e8m8(batch); batch -= vlmax;
  vint8m8_t vmax = __riscv_vle8_v_i8m8(input, vlmax); input += vlmax;

  while (batch > 0) {
    size_t vl = __riscv_vsetvl_e8m8(batch); batch -= vl;
    vint8m8_t vinput = __riscv_vle8_v_i8m8(input, vl); input += vl;
    vmax = __riscv_vmax(vmax, vinput, vl);
  }

  vint8m1_t max = __riscv_vle8_v_i8m1(output + 0, 1);
  output[0] = __riscv_vmv_x_s_i8m1_i8(__riscv_vredmax(vmax, max, vlmax));
}
