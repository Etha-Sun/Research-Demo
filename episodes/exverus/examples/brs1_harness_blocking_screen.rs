// SOURCE: ExVerus paper, Figure 3 panel 5, page 13 — the "+" variant (mutant_1's invariant as the last assertion).
// Figure callout (green): "assertion pass CEX_1 blocking validated".
// TRIMS: none.
// ---- on screen below ----
fn myfun_loop2(a: &mut Vec<i32>, sum: &mut Vec<i32>, N: i32) {
    let mut N = 2;
    let mut a = vec![1, 1];
    let mut sum = vec![1];
    let mut i: usize = 0;
    // Invariants (base case)
    assert(i <= N as usize);
    assert(a.len() == N);
    assert(sum.len() == 1);
    assert(forall|k: int| 0 <= k < N as usize ==> a[k] == 1);
    assert(i > 0 ==> sum[0] <= i as i32);
}
