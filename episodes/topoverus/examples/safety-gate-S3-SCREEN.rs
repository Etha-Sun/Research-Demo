// SOURCE: github.com/Etha-Sun/Topoverus @ 878496237052eeccdd8478b9f9037041affe1431
// FILE: tests/test_trust.py lines 138-149, test_existing_assumption_cannot_move_past_assignment
//   (copy: research/topoverus/examples/safety-gate-SCREEN.txt, Example S3). TEST CASE FROM THE RELEASED CODE, not a model output.
// Verbatim body lines 140-141 of the `original` string; the candidate is the test's own
//   original.replace('assume(y > 1); y = y - 1;', 'y = y - 1; assume(y > 1);').
// SCREEN TRIMS: the `use vstd::prelude::*; verus! {` prefix and `} } fn main() {}` suffix are dropped; `}` kept on its own line.
// Outcomes shown on screen are the TEST'S ASSERTIONS (Verus: original verification_failed, candidate verified;
//   trust_change: None; Lynette safety: unsafe). We did not execute the test.
// ---- screen text below: original ----
fn target(x: i32) -> (r: i32) requires x > 1, x < 10 ensures r > 1 {
    let mut y = x; assume(y > 1); y = y - 1; y
}
// ---- screen text below: candidate ----
fn target(x: i32) -> (r: i32) requires x > 1, x < 10 ensures r > 1 {
    let mut y = x; y = y - 1; assume(y > 1); y
}
