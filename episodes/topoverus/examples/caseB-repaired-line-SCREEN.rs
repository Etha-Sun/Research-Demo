// SOURCE: github.com/Etha-Sun/Topoverus @ 878496237052eeccdd8478b9f9037041affe1431
// FILE: docs/case-studies/b-prefix-invariant/model-output.txt line 73 (copy: research/topoverus/examples/caseB-3-model-output-full.txt:78)
//   verbatim: "            forall|j: int, k: int| 0 <= j < k < i ==> prices[k] - prices[j] <= max_pro,"
// SCREEN TRIM: split after "< i" (whitespace only), to replace screen lines 14-15 of caseB-loop-SCREEN.rs.
// The recorded repaired program ALSO deletes the invariant "i == 0 ==> min_price == i32::MAX" (buggy.rs:42; rationale item 4,
//   model-output.txt:29); the scene shows this deletion by striking screen line 12.
// Verification status of the recorded repaired program: NOT recorded in the repo, NOT reported in the paper, NOT run by us.
// ---- screen text below ----
            forall|j: int, k: int| 0 <= j < k < i
                ==> prices[k] - prices[j] <= max_pro,
