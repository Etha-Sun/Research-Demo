// SOURCE: ExVerus paper (arXiv 2603.25810v2), Section 2.1 "Background: Automated Proof in Verus", page 2.
// Tokens VERBATIM from the paper's listing; changes: listing line numbers removed, the wrapped
// "// post-condition" comment re-joined, indentation normalised (PDF text layer loses indentation). This is a CORRECT proof used to explain pre/post-conditions and loop invariants;
// it is not a failing example. The paper does not state that this snippet was run through Verus.
fn sum_to_n(n: nat) -> (result: nat)
    requires n >= 0, // pre-condition
    ensures result == n*(n+1)/2, // post-condition
{
    let mut i: nat = 0;
    let mut sum: nat = 0;
    while i < n
        invariant // proof annotation
            sum == i*(i+1)/2,
            i <= n,
    {
        i = i + 1;
        sum = sum + i;
    }
    sum
}
