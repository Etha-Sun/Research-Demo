/* SOURCE: build/e2e3-workers-20261106/intrinsics-v1.7.3/rvv/rvv_contracts_vlen256.h lines 255-259 and 1383-1389
 * Intrinsic contracts from the unified, differentially tested library v1.7.3 (VLEN 256 profile: 32 lanes of e8m1).
 * Note: tail lanes are an existentially quantified list T (tail-agnostic = arbitrary contents). VERBATIM. */
size_t __riscv_vsetvl_e8m1(size_t avl)
/*@ With (vf : Z -> Z)
    Require 0 < avl && vsl_ok(32, vf) && emp
    Ensure __return == vsl_app(vf, avl@pre) && vsl_ok(32, vf) &&
           1 <= __return && __return <= avl@pre && __return <= 32 && emp */;

void qcp_p_vlsseg3e8_v_u8m1x3(vuint8m1x3_t *qcp_r, const uint8_t *qcp_a0, long long qcp_a1, size_t qcp_a2)
/*@ With (b : Z) (n : Z) (L : list Z)
    Require 0 <= qcp_a2 && qcp_a2 <= 32 && b <= (size_t)qcp_a0 && (size_t)qcp_a0 + rv_stride_widthE(1, 3, qcp_a2) <= b + 1 * n && b <= (size_t)qcp_a0 + rv_stride_last(qcp_a2, qcp_a1) && (size_t)qcp_a0 + rv_stride_last(qcp_a2, qcp_a1) + rv_stride_widthE(1, 3, qcp_a2) <= b + 1 * n &&
      UCharArray::full(b, n, L) * UCharArray::undef_full(qcp_r->s, 96)
    Ensure exists T, Zlength(T) == 3 * (32 - qcp_a2@pre) &&
      UCharArray::full(b, n, L) * UCharArray::full(qcp_r@pre->s, 96,
        rv_strided_tupleG(1, 1, 3, 32, qcp_a2@pre, (size_t)qcp_a0@pre - b, qcp_a1@pre, L, T)) */;
