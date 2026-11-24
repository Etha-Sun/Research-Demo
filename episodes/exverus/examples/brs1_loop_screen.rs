// SOURCE: ExVerus paper, Figure 3 panel "1. Buggy Proof", page 13 (App. A.1). Task: VerusBench Diffy/brs1.
// Copied from research/exverus/examples/03a_brs1_buggy_proof.rs (transcribed from the rendered figure, ASCII glyphs).
// TRIMS for screen: kept the signature line; replaced requires/ensures and the whole first loop (which sets every
// a[k] = 1) by "..."; in the second loop replaced the four correct invariants
//   i <= N as usize, a.len() == N, sum.len() == 1, forall |k: int| 0 <= k < a.len() ==> a[k] == 1,
// by "...". Removed the end-of-line annotation comment. Every shown line is otherwise verbatim.
// On screen line 7 = the buggy invariant ("error: invariant not satisfied before loop", Fig. 3).
// ---- on screen below ----
pub fn myfun(a: &mut Vec<i32>, sum: &mut Vec<i32>, N: i32)
    ...
    i = 0;
    while (i < N as usize)
        invariant
            ...
            sum[0] <= i as i32,
        decreases N - i,
    {
        if (i == 0) {
            sum.set(0, 0);
        } else {
            let temp = sum[0];
            sum.set(0, temp + a[i]);
        }
        i = i + 1;
    }
