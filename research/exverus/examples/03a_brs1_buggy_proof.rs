// SOURCE: ExVerus paper, Figure 3 panel "1. Buggy Proof", page 13 (Appendix A.1). Task: VerusBench Diffy/brs1.
// TRANSCRIBED from the rendered figure; ligature glyphs written in ASCII ("<=", "==>", "=="). The buggy proof
// is an LLM-generated "almost-correct" proof (paper text, p.13), not the benchmark's unverified input.
// Figure annotation on the highlighted line: "error: invariant not satisfied before loop".
pub fn myfun(a: &mut Vec<i32>, sum: &mut Vec<i32>, N: i32)
    requires
        N > 0,
        old(a).len() == N,
        old(sum).len() == 1,
    ensures
        sum[0] <= N,
{
    let mut i: usize = 0;
    while (i < N as usize)
        invariant
            i <= N as usize,
            a.len() == N,
            sum.len() == 1,
            forall |k: int| 0 <= k < i ==> a[k] == 1,
        decreases N - i,
    {
        if (i % 1 == 0) {
            a.set(i, 1);
        } else {
            a.set(i, 0);
        }
        i = i + 1;
    }

    i = 0;
    while (i < N as usize)
        invariant
            i <= N as usize,
            a.len() == N,
            sum.len() == 1,
            forall |k: int| 0 <= k < a.len() ==> a[k] == 1,
            sum[0] <= i as i32,        // <-- error: invariant not satisfied before loop
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
}
