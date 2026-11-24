// SOURCE: ExVerus artifact repo github.com/claudeyj/exverus @ 4e513a1c (shallow clone),
//   file cleaned-verusbench/Misc/verified/findmax.rs — the benchmark's GROUND-TRUTH verified proof.
// VERBATIM. IMPORTANT: this is NOT the repair ExVerus produced; the paper never shows ExVerus's final findmax proof.
// The repo only records (vinv/analysis/figure/data/ExVerus/ds_vb_global_repair_status_z3_mut_val.json) that
// verusbench_misc_findmax ended in 'verification_pass' at phase 'cex_repair' (DeepSeek run); the repaired file itself is not in the repo.
// Key difference vs. the Fig.1 buggy invariant: line 18 uses '&&' inside exists (a witness inside the prefix), not '==>'.
#[allow(unused_imports)]
use vstd::prelude::*;
fn main() {}

verus! {
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
        forall |k: int| 0 <= k < i ==> nums@[k] <= max,
        exists |k: int| 0 <= k < i && nums@[k] == max,
    decreases nums.len() - i,
    { 
        if nums[i] > max {
            max = nums[i];
        }
        i += 1;
    }
    max
}
}
