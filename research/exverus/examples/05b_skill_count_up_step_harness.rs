// SOURCE: ExVerus artifact repo github.com/claudeyj/exverus @ 4e513a1c, skills/counterexample-guided-proof/SKILL.md, fenced block #2 (section '1. Locate the invariant'). VERBATIM. This teaching example is from the repo's agent skill, NOT from the paper.
fn count_up_step(n: u32, i: u32, j: u32) {
    // before: condition + invariants
    assume(i < n && i <= n && j <= 1000);
    let i = i + 1;
    let j = j + 1;
    // after: invariants
    assert(i <= n);
    assert(j <= 1000);
}
