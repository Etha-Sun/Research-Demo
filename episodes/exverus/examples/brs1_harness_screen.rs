// SOURCE: ExVerus paper, Figure 3 panel "5. Counterexample validation(-) / blocking validation program (+)", page 13.
// Copied from research/exverus/examples/03d_brs1_validation_harness.rs (transcribed from the rendered figure).
// This file = the "-" variant (original invariant as the last assertion). Figure callout (red):
//   "assertopm fail [sic], invariant not correct CEX_1 validated".
// TRIMS: none (the diff markers "-"/"+" of the figure are split into this file and brs1_harness_blocking_screen.rs).
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
    assert(sum[0] <= i as i32);
}
