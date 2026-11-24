# TopoVerus (Episode 2): on-screen sources

Paper = *Curriculum Proof Repair with Learned Counterexamples*, Sun, Yang, Pei, NeurIPS 2026, arXiv 2611.13627v1
(`papers/topoverus.pdf`; "p.N" = PDF page). Repo = github.com/Etha-Sun/Topoverus @ 878496237052eeccdd8478b9f9037041affe1431
(`repos/Topoverus`). Research copies are in `research/topoverus/examples/`. Nothing was executed: no Verus, Lynette or
model runs. "Ours" marks our own wording or arithmetic.

## Code and text panels (episodes/topoverus/examples/)

| File | Shown in | Source | Trims |
|---|---|---|---|
| caseB-loop-SCREEN.rs | Topo02, 05, 06 | repo docs/case-studies/b-prefix-invariant/buggy.rs:24-52 | elisions `...` for requires (25-27), 2nd ensures (30-31), four invariants (43-47); comments 36-39 dropped; two long lines split (whitespace only). Listed line by line in the file header |
| caseB-verifier-error.txt | Topo02 | repo .../verifier-error.txt:2-3 | caret excerpt dropped. The `44:13` refers to the authors' original file, not to the screen lines |
| appD-output-format.txt | Topo04 | paper App. D.1 user message, p.21 (BRIEF §6) | verbatim |
| caseB-trajectory-filled-SCREEN.txt | Topo04 | research/topoverus/examples/trajectory-template-SCREEN.txt, values verbatim from repo .../model-output.txt:2-17, 21-23, 73 | <think> dropped (not recorded), steps 2-4 elided, [Violation] reduced to its key clause, reasoning item 2 first sentence, rust block = changed line only; wraps are whitespace only; header lists each trim |
| caseB-repaired-line-SCREEN.rs | Topo06 | repo .../model-output.txt:73 | split after `< i` |
| binary-search-invariants-SCREEN.rs | Topo08 | paper Fig. 2 bottom, invariant list, p.4 | "[Boundary error]" tag dropped (shown in red instead) |
| binary-search-I5-fixed-SCREEN.rs | Topo08 | Fig. 2 repair signal "high <= i -> high < i" (p.4) applied to the I5 line; equals Fig. 1 I5 (p.3) up to `: int` | derived by applying the paper's stated edit |
| safety-gate-S3-SCREEN.rs | Topo10 | repo tests/test_trust.py:138-149 (`original`, and the test's own `.replace(...)` for the candidate) | `use vstd...verus! {` prefix and `} } fn main() {}` suffix dropped |
| rdep-worked-example-DERIVED.txt | Topo09 (values) | our re-implementation of repo topoverus/matcher_v2.py and graph.py `dependency_score` (copied from research/topoverus/examples) | DERIVED; illustrative edge set |

## Numbers and quotes on screen

| Scene | On screen | Source |
|---|---|---|
| Topo01 | "Yuechun Sun, Jun Yang, Kexin Pei · NeurIPS 2026" | paper p.1 footer; docs/SERIES.md attribution |
| Topo01 | recap line | docs/SERIES.md fixed recap (paraphrased on screen) |
| Topo02 | `error: invariant not satisfied before loop` / `--> best_time_sell_v2.rs:44:13` | repo verifier-error.txt:2-3; paper Fig. 4 p.9 shows the condensed version (line 37) |
| Topo03 | [State] σ, [Execution Trace] τ, [Violation] ψ | paper Eq. 1 and §3.1, p.4-5 |
| Topo03 | ExVerus: search + validate at every repair; TopoVerus: one pass | paper §1 ¶4-5 p.2 ("iterative refinement", "hand-written validators"); Abstract p.1 ("in a single pass") |
| Topo03 | "a counterexample is useful when conditioning on it helps the model produce a safe, verifier-passing proof" | paper Abstract p.1, verbatim |
| Topo03 | "the model's counterexample is not checked by a solver" | paper p.5 ("Rather than relying on an external SMT-based tool ...") and §6 Limitations p.10 (validity not formally guaranteed); wording ours |
| Topo04 | prompt text | paper App. D.1 p.21, verbatim |
| Topo04 | "(a free <think> block may come first)" | paper App. D p.20 (chain-of-thought <think> block); wording ours |
| Topo05 | prices = [5, 3, 7]; i = 0; max_pro = 0; min_price = i32::MAX | repo model-output.txt:3-4, 8; paper Fig. 4 p.9 [State] |
| Topo05 | (j=0, k=2), 7 - 5 = 2, 2 <= 0 false | repo model-output.txt:12-13; paper Fig. 4 p.9 |
| Topo05 | "range = the whole array, but nothing is processed yet"; "cause: quantifier range is too wide" | paraphrase of model-output.txt:17 and paper Fig. 4 p.9 ("identifies the quantifier range as the root cause") |
| Topo06 | rationale fragments | repo model-output.txt:23, verbatim with elisions |
| Topo06 | repaired line `0 <= j < k < i` | repo model-output.txt:73; paper Fig. 4 p.9 ("0 <= j < k < i") |
| Topo06 | deleted invariant `i == 0 ==> min_price == i32::MAX` | diff of buggy.rs:42 vs the recorded program (research/topoverus/examples/caseB-5-diff-DERIVED.txt); rationale item 4, model-output.txt:29 |
| Topo06 | "Verus on this repaired program: not reported" | paper (Fig. 4 and App. B p.17 report counterexample and repair target, no Verus run); repo (no record, BRIEF §5); we could not run Verus |
| Topo07 | QwQ-32B; Sonnet 4.6 teacher; 461 trajectories from 249 programs; 8 responses per prompt | paper §4.1 p.6-7 |
| Topo07 | safety gate, unsafe -> reward 0; Eq. 2 | paper §3.2 p.5 |
| Topo08 | I1..I5, nums = [1, 3, 5], target = 5, high = 2, low -> 2, nums[2] = 5, `high <= i -> high < i` | paper Fig. 1 p.3, Fig. 2 bottom and text p.4 (illustrative) |
| Topo08 | "state high = 2, yet it checks i = 1"; "mid = 0: a hallucinated value" | paper Fig. 2 top annotations p.4 ("hallucination, contradicting with high=2"; "mid=0 is a hallunicated value") |
| Topo09 | edge set I1->I2, I1->I3, I2->I4, I3->I4, I2->I5, I3->I5 | ours: reading of §2.1 p.3 and Fig. 2 p.4 (labelled "our reading of Fig. 2") |
| Topo09 | R_dep = α × β; α coverage, β edge satisfaction | paper Eq. 6 p.6 |
| Topo09 | 6/6 -> 1.0; 2/6 -> 0.33 (0.333); 0/6 -> 0 | ours: examples/rdep-worked-example-DERIVED.txt (labelled "our computation") |
| Topo09 | graph not given at evaluation | paper §4.1 p.6 ("The reference proof, its invariant set V, and the dependency graph G are not provided during evaluation") |
| Topo10 | verification failed / verified / unsafe | repo tests/test_trust.py:146-149 assertions (not run by us) |
| Topo10 | "x = 2 -> y = 1, but ensures r > 1" | ours, arithmetic on the code |
| Topo11 | 471 problems, 7 benchmarks | paper §4.1 p.6 |
| Topo11 | TopoVerus 61.6 / 72.2; Sonnet-4.5 55.9 / 65.9; +5.7 / +6.3 | paper §4.2 p.7; Table 4 p.18 (micro-average = "weighted") |
| Topo11 | settings: cloud LLMs iterative repair with verifier feedback; ours 3 chains × 10 iterations | paper Table 1 caption p.7 |
| Topo11 | CoT-Init 39.3, CTX-Init 50.5 (+11.2) | paper §4.3 text p.7 ("from 39.3% to 50.5%, a gain of 11.2 points") |
| Topo11 | CTX-Binary 53.7, CTX-Dep 61.6 (+7.9) | paper Table 4 p.18; §4.2 p.7 ("7.9 / 4.3" above CTX-Binary) |
| Topo11 | β 43.8% -> 95.8%; coverage 98.6% vs 98.5% | paper Table 7 p.20 (24 paired tasks accepted by Verus) |
| Topo12 | loop invariants only; counterexamples not formally guaranteed / may hallucinate traces | paper §6 Limitations p.10 |
| Topo12 | VeruSAGE Safe-Pass@1: Sonnet-4.5 75.5%, CTX-Dep 30.2% | paper Table 1 p.7 |
| Topo12 | bridge line | docs/SERIES.md fixed bridge (Episode 2) |
