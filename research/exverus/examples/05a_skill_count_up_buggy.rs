// SOURCE: ExVerus artifact repo github.com/claudeyj/exverus @ 4e513a1c, skills/counterexample-guided-proof/SKILL.md, fenced block #1 (running example, top of file). VERBATIM. This teaching example is from the repo's agent skill, NOT from the paper.
fn count_up(n: u32) -> (r: u32)
    requires n < 1000,
    ensures r == n,
{
    let mut i: u32 = 0;
    let mut j: u32 = 0;
    while i < n
        invariant i <= n, j <= 1000,
    {
        i = i + 1;
        j = j + 1;
    }
    j
}
// error: invariant not satisfied at end of loop body:  j <= 1000
