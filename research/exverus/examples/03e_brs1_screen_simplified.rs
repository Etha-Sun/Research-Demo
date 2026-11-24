// ADAPTED FOR SCREEN — NOT VERBATIM. Derived from ExVerus paper Figure 3 (page 13), second loop of `myfun`.
// What changed vs. the verbatim original (03a_brs1_buggy_proof.rs, second loop):
//   1. Dropped the first loop and the invariants `i <= N as usize`, `a.len() == N`, `sum.len() == 1`,
//      `forall |k: int| 0 <= k < a.len() ==> a[k] == 1` (they are correct and irrelevant to the bug).
//   2. Dropped `decreases N - i`.
//   3. Shown BEFORE (buggy) and AFTER (mutant_1, Fig.3 panel 4) as two lines of one invariant slot.
// Everything else (loop body, the two invariant lines, the CEX values) is verbatim from Figure 3.
//
// Verbatim original second loop (Fig.3 panel 1):
//     i = 0;
//     while (i < N as usize)
//         invariant
//             i <= N as usize,
//             a.len() == N,
//             sum.len() == 1,
//             forall |k: int| 0 <= k < a.len() ==> a[k] == 1,
//             sum[0] <= i as i32,
//         decreases N - i,
//     { if (i == 0) { sum.set(0, 0); } else { let temp = sum[0]; sum.set(0, temp + a[i]); } i = i + 1; }

    i = 0;                       // sum[0] has NOT been reset yet: it holds whatever the caller passed in
    while (i < N as usize)
        invariant
            sum[0] <= i as i32,               // BEFORE  -> "invariant not satisfied before loop"
         // i > 0 ==> sum[0] <= i as i32,     // AFTER (mutant_1)
    {
        if (i == 0) {
            sum.set(0, 0);
        } else {
            let temp = sum[0];
            sum.set(0, temp + a[i]);
        }
        i = i + 1;
    }
// Counterexample (Fig.3 CEX_1): a = vec![1, 1], sum = vec![1], i = 0, N = 2   ->  1 <= 0 is false
