// SOURCE: TopoVerus paper (arXiv 2611.13627v1), Figure 4 "Buggy code.", PDF p.9 (same listing as App. B Case Study B, p.17).
// SCREEN TRIMS (no line changes meaning):
//   screen 2     = "requires ..." replaces the requires clause (Fig. 4 lines 2-5)
//   screen 11    = "..." replaces the two min_price invariants (Fig. 4 lines 14-17)
//   the comment "// BUG: full-array range; should be k < i." (Fig. 4 line 18) is dropped; the scene marks the line instead
//   screen 17    = Fig. 4 lines 25-26 joined (whitespace only)
//   Fig. 4 lines 28-29 ("max_pro", "}") dropped.
// ---- screen text below ----
pub fn max_profit(price: Vec<i32>) -> (res: i32)
    requires ...
    ensures
        forall|j: int, k: int| 0 <= j < k < price.len()
            ==> price[k] - price[j] <= res,
{
    let mut max_pro = 0;
    let mut min_price = i32::MAX;
    for i in 0..price.len()
        invariant
            ...
            forall|j: int, k: int|
                0 <= j < k < price.len()
                ==> price[k] - price[j] <= max_pro,
    {
        min_price = min_i32(min_price, price[i]);
        max_pro = max_i32(max_pro, price[i] - min_price);
    }
