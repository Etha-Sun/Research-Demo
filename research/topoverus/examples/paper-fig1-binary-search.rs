// SOURCE: TopoVerus paper (arXiv 2611.13627v1), Figure 1 "Proof annotation for binary-search insertion", PDF p.3.
// Transcribed from the PDF text layer. Changes: listing line numbers (1-28) dropped; indentation re-added (the text layer loses it). Tokens unchanged.
// Paper status: this is the paper's motivating example (Sec. 2.1); the paper does not state a Verus run for it.
// ---- verbatim content below ----
fn search_insert(nums: Vec<i32>, target: i32) -> (res: i32)
requires
  1 <= nums@.len() <= 10000,
  forall|i, j| 0 <= i < j < nums@.len() ==> nums@[i] < nums@[j],
ensures /* insertion-position postcondition */
  0 <= res <= nums@.len(),
  nums@[0] <= target <= nums@[nums@.len() - 1] ==>
    (forall|i| 0 <= i < res ==> nums@[i] < target) &&
    (forall|i| res <= i < nums@.len() ==> nums@[i] >= target),
{
  let mut low = 0i32;
  let mut high = nums.len() as i32 - 1;
  while low <= high
    invariant
      1 <= nums@.len() <= 10000,                                  //I1
      0 <= low <= nums@.len(),                                    //I2
      -1 <= high <= nums@.len() - 1,                              //I3
      forall|i| 0 <= i < low ==> nums@[i] < target,               //I4
      forall|i| high < i < nums@.len() ==> nums@[i] > target      //I5
  {
    let mid = ((low + high) as usize / 2) as i32;
    if nums[mid as usize] == target { return mid; }
    if target < nums[mid as usize] { high = mid - 1; }
    else { low = mid + 1; }
  }
  low
}
