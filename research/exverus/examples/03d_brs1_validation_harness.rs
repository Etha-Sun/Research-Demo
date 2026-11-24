// SOURCE: ExVerus paper, Figure 3 panel "5. Counterexample validation(-) / blocking validation program (+)", page 13.
// TRANSCRIBED from the rendered figure (ASCII glyphs). The dotted box is CEX_1 injected as concrete `let` bindings.
// Figure callouts: red "assertopm fail, invariant not correct CEX_1 validated" [sic, typo in the figure];
//                  green "assertion pass CEX_1 blocking validated".
// The '-' line is the original (buggy) invariant as an assertion; the '+' line is mutant_1's invariant.
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
-   assert(sum[0] <= i as i32);
+   assert(i > 0 ==> sum[0] <= i as i32);
}
