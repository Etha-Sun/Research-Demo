# TopoVerus: on-screen sources

Paper = *Curriculum Proof Repair with Learned Counterexamples*, Sun, Yang, Pei, NeurIPS 2026, arXiv 2611.13627v1
(`papers/topoverus.pdf`; "p.N" = PDF page). The paper is the source for everything except the safety-gate example,
which comes from the released code: github.com/Etha-Sun/Topoverus @ 878496237052eeccdd8478b9f9037041affe1431
(`repos/Topoverus`), because the paper describes the gate (§3.2 p.5) without a worked example.

## Code and text panels (episodes/topoverus/examples/)

| File | Shown in | Source | Trims |
|---|---|---|---|
| caseB-fig4-code-SCREEN.rs | Topo02, 05, 06 | paper Fig. 4 "Buggy code", p.9 (= App. B Case Study B, p.17) | `requires ...` for the requires clause; `...` for the two min_price invariants; the `// BUG` comment dropped; one wrapped line joined; trailing `max_pro }` dropped. Listed in the file header |
| caseB-fig4-verus-error.txt | Topo02 | paper Fig. 4 "Verus error", p.9 | caret excerpt dropped |
| appD-output-format.txt | Topo04 | paper App. D.1 user message, p.21 | verbatim |
| caseB-fig4-counterexample-SCREEN.txt | Topo04, 06 | paper Fig. 4 "Counterexample" box and the sentence below it, p.9 | verbatim, rewrapped |
| caseB-fig4-repair-target-SCREEN.rs | Topo06 | paper Fig. 4 p.9 ("0 <= j < k < i"); §4.6 p.8; App. B p.17 | the range edit applied to screen line 13 |
| binary-search-invariants-SCREEN.rs | Topo08 | paper Fig. 2 bottom, invariant list, p.4 | "[Boundary error]" tag dropped (shown in red instead) |
| binary-search-I5-fixed-SCREEN.rs | Topo08 | Fig. 2 repair signal "high <= i -> high < i" (p.4) applied to the I5 line; equals Fig. 1 I5 (p.3) up to `: int` | the paper's stated edit |
| safety-gate-S3-SCREEN.rs | Topo10 | repo tests/test_trust.py:138-149 (`original`, and the test's own `.replace(...)` for the candidate) | `use vstd...verus! {` prefix and `} } fn main() {}` suffix dropped |

## Numbers and quotes on screen

| Scene | On screen | Source |
|---|---|---|
| Topo01 | "Yuechun Sun, Jun Yang, Kexin Pei · NeurIPS 2026" | paper p.1 |
| Topo02 | `error: invariant not satisfied before loop` / `--> best_time_sell_v2.rs:37:13` | Fig. 4 p.9 |
| Topo03 | [State] σ, [Execution Trace] τ, [Violation] ψ | Eq. 1 and §3.1, p.4-5 |
| Topo03 | "counterexample, rationale and repair in one pass" | Abstract p.1 ("in one trajectory", "in a single pass") |
| Topo03 | "a counterexample is useful when conditioning on it helps the model produce a safe, verifier-passing proof" | Abstract p.1, verbatim |
| Topo03 (narration) | inference-time counterexamples need costly iterative refinement | Abstract p.1; §1 p.2 |
| Topo04 | prompt text; "(preceded by a <think> block)" | App. D.1 p.21; App. D p.20 |
| Topo04 | counterexample text and repair-target sentence | Fig. 4 p.9, verbatim |
| Topo05 | price = [5, 3, 7]; i = 0; max_pro = 0; min_price = i32::MAX; (j=0, k=2), 7 - 5 = 2; 2 <= 0 false; empty prefix 0..i; quantifier range as root cause | Fig. 4 p.9 |
| Topo06 | repair target, `0 <= j < k < i`, "full array -> processed prefix" | Fig. 4 p.9; §4.6 p.8; App. B p.17 ("replace the full-array range with the processed-prefix range k < i") |
| Topo07 | QwQ-32B; Sonnet 4.6 teacher; 461 trajectories from 249 programs; 8 responses per prompt | §4.1 p.6-7 |
| Topo07 | safety gate = Lynette, only proof annotations changed, unsafe -> reward 0; Eq. 2 | §3.2 p.5 |
| Topo08 | I1..I5; under-constrained: "high = 2, yet it checks i = 1", "mid = 0: a hallucinated value"; constrained: nums = [1, 3, 5], target = 5, high = 2, low -> 2, nums[2] = 5; `high <= i -> high < i` | Fig. 1 p.3; Fig. 2 and §2.1 p.4 |
| Topo09 | graph I1 -> {I2, I3} -> I4, I5'; correct / wrong / missing colouring for top and bottom cases | Fig. 2 p.4 (dependency-graph panels); §2.1 p.3 |
| Topo09 | edge meaning | Defs. 1-3 p.5-6 |
| Topo09 | R_dep = α × β; α coverage, β edge satisfaction | Eq. 6 p.6 |
| Topo09 | "prerequisite facts first -> counterexamples for dependent invariants in a better-constrained proof state" | §2.1 "Implication for training" p.4 |
| Topo09 | training signal only; no reference proof, no graph at test time | §4.1 p.6 |
| Topo10 | verification failed / verified / unsafe | repo tests/test_trust.py:146-149 (the test's assertions) |
| Topo10 | "x = 2 -> y = 1, but ensures r > 1" | arithmetic on the code |
| Topo11 | 471 problems, 7 benchmarks | §4.1 p.6 |
| Topo11 | TopoVerus 61.6 / 72.2; Sonnet-4.5 55.9 / 65.9; +5.7 / +6.3 | §4.2 p.7; Table 4 p.18 (micro-average = "weighted") |
| Topo11 | settings: cloud LLMs iterative repair with verifier feedback; TopoVerus 3 chains × 10 iterations | Table 1 caption p.7 |
| Topo11 | CoT-Init 39.3, CTX-Init 50.5 (+11.2) | §4.3 p.7 |
| Topo11 | CTX-Binary 53.7, CTX-Dep 61.6 (+7.9) | Table 4 p.18; §4.2 p.7 |
| Topo11 | β 43.8% -> 95.8%; coverage 98.6% vs 98.5% | Table 7 p.20 (24 paired tasks accepted by Verus) |
| Topo12 | loop invariants only; counterexamples not formally guaranteed, traces may be imprecise | §6 Limitations p.10 |
| Topo12 | VeruSAGE Safe-Pass@1: Sonnet-4.5 75.5%, CTX-Dep 30.2% | Table 1 p.7 |
| Topo12 | takeaway lines | Conclusion p.10, Abstract p.1 (paraphrase) |
