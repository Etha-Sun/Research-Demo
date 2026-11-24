// SOURCE: same as brs1_loop_screen.rs, with line 7 replaced by mutant_1's invariant from ExVerus paper,
// Figure 3 panel "4. Patch on the buggy invariant of mutant_1", page 13:
//   - sum[0] <= i as i32,
//   + i > 0 ==> sum[0] <= i as i32,
// The paper (p.13) reports that mutant-1 blocks all counterexamples and passes Verus. The full repaired file is
// not printed in the paper; the other lines here are the unchanged lines of the buggy proof.
// ---- on screen below ----
pub fn myfun(a: &mut Vec<i32>, sum: &mut Vec<i32>, N: i32)
    ...
    i = 0;
    while (i < N as usize)
        invariant
            ...
            i > 0 ==> sum[0] <= i as i32,
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
