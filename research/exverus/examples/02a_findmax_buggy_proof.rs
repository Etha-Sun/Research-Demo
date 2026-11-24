// SOURCE: ExVerus paper, Figure 1 (left panel "Buggy Proof"), page 3. Task: VerusBench Misc/findmax.
// TRANSCRIBED from the rendered figure. The figure uses a ligature font; glyphs are written here in
// ASCII (">=" "<=" "==>" "==") — the PDF text layer confirms the underlying ASCII tokens.
// Figure annotation on line 15 (highlighted red):  "Error: invariant not satisfied at end of loop body"
// NOTE: line 15 uses `exists ... ==> ...` (implication), not `&&`. The ensures on line 6 also uses `==>`;
// that is how the benchmark's own spec is written (see repo cleaned-verusbench/Misc/unverified/findmax.rs:11).
fn find_max(nums: Vec<i32>) -> (ret:i32)
requires
    nums.len() > 0,
ensures
    forall |i: int| 0 <= i < nums@.len() ==> nums@[i] <= ret,
    exists |i: int| 0 <= i < nums@.len() ==> nums@[i] == ret,
{
    let mut max = nums[0];
    let mut i = 1;
    while i < nums.len()
        invariant
            i >= 1,
            i <= nums.len(),
            forall |j: int| 0 <= j < i ==> nums@[j] <= max,
            exists |j: int| 0 <= j < i ==> nums@[j] == max,   // <-- Fig.1 line 15: invariant not satisfied at end of loop body
        decreases nums.len() - i
    {
        if nums[i] > max {
            max = nums[i];
        }
        i += 1;
    }
    max
}
