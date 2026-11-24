// SOURCE: github.com/Etha-Sun/Topoverus @ 878496237052eeccdd8478b9f9037041affe1431
// FILE: docs/case-studies/b-prefix-invariant/buggy.rs (copy: research/topoverus/examples/caseB-1-buggy.rs)
// SCREEN TRIMS (no line changes meaning):
//   screen 1     = buggy.rs:24 (signature)
//   screen 2     = "..." for buggy.rs:25-27 (requires clause)
//   screen 3-5   = buggy.rs:28-29; the ensures line 29 is split after "prices.len()" (whitespace only)
//   screen 6     = "..." for buggy.rs:30-31 (second ensures clause)
//   screen 7-11  = buggy.rs:32-34, 40-41 (comment lines 36-39 dropped)
//   screen 12    = buggy.rs:42
//   screen 13    = "..." for buggy.rs:43-47 (four other invariants)
//   screen 14-15 = buggy.rs:48, split after "prices.len()" (whitespace only). This is the line Verus reports (44:13 in the
//                  original file best_time_sell_v2.rs, per verifier-error.txt)
//   screen 16-19 = buggy.rs:49-52
//   Leading indentation kept; buggy.rs:53-58 dropped.
// ---- screen text below ----
pub fn max_profit(prices: Vec<i32>) -> (res: i32)
    ...
    ensures
        forall|j: int, k: int| 0 <= j < k < prices.len()
            ==> prices[k] - prices[j] <= res,
        ...
{
    let mut max_pro = 0;
    let mut min_price = i32::MAX;
    for i in 0..prices.len()
        invariant
            i == 0 ==> min_price == i32::MAX,
            ...
            forall|j: int, k: int| 0 <= j < k < prices.len()
                ==> prices[k] - prices[j] <= max_pro,
    {
        min_price = min_i32(min_price, prices[i]);
        max_pro = max_i32(max_pro, prices[i] - min_price);
    }
