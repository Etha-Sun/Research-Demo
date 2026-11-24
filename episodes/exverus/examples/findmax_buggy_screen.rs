// SOURCE: ExVerus paper (arXiv 2603.25810v2), Figure 1 left panel "Buggy Proof", page 3. Task: VerusBench Misc/findmax.
// Copied from research/exverus/examples/02a_findmax_buggy_proof.rs (transcribed from the rendered figure; ligature
// glyphs written as ASCII "<=" "==>").
// TRIMS for screen: dropped the requires/ensures clauses (replaced by "..."), the `decreases nums.len() - i` line,
// and the end-of-line annotation comment. All remaining lines are verbatim.
// On screen line 11 = the failing invariant ("invariant not satisfied at end of loop body", Fig. 1).
// ---- on screen below ----
fn find_max(nums: Vec<i32>) -> (ret:i32)
    ...
{
    let mut max = nums[0];
    let mut i = 1;
    while i < nums.len()
        invariant
            i >= 1,
            i <= nums.len(),
            forall |j: int| 0 <= j < i ==> nums@[j] <= max,
            exists |j: int| 0 <= j < i ==> nums@[j] == max,
    {
        if nums[i] > max {
            max = nums[i];
        }
        i += 1;
    }
    max
}
