# ExVerus — research brief for the explainer video

Paper: *ExVerus: Verus Proof Repair via Counterexample Reasoning*. Jun Yang, Yuechun Sun, Yi Wu, Rodrigo Caridad, Yongwei Yuan, Jianan Yao, Shan Lu, Kexin Pei. arXiv 2603.25810v2 (30 Mar 2026), ICML 2026. Affiliations (p.1): UChicago, Purdue, U Toronto, Microsoft Research.
Local PDF: `papers/exverus.pdf` (31 pp). Project page: https://exverus-proof.github.io/. Code: https://github.com/claudeyj/exverus, shallow clone at `repos/exverus` (commit `4e513a1c`, 2026-10-14). The `verus-proof-synthesis` submodule (AutoVerus) was not fetched.

Citation convention: "p.N" means the PDF page. "T1–T5" are Tables 1–5 and "F1–F8" are Figures 1–8. Code files are in `examples/`. Each has a header that gives its exact source and says whether it is verbatim, transcribed from a figure, or adapted.

Figure code was **transcribed from rendered images**, because the PDF text layer scrambles figure code. The figures use a ligature font, so `≤ ⟹ ≠` are written as ASCII `<= ==> !=`. The text layer confirms that the underlying tokens are ASCII.

---

## 1. Problem statement (for a smart CS undergraduate)

**Verus** is a verifier for Rust. You write ordinary Rust plus a *specification*: `requires` (what must hold when the function is called) and `ensures` (what must hold when it returns). You also write *proof annotations*, chiefly **loop invariants**: facts that hold every time the loop is about to check its condition. Verus turns all of this into logical formulas called verification conditions (VCs) and asks the SMT solver Z3 whether they hold (p.2 §2.1). A proof is "done" only when every VC is proved.

When a proof fails, Verus gives a one-line verdict, such as `invariant not satisfied before loop`, `invariant not satisfied at end of loop body`, or `postcondition not satisfied`. The verdict says *where* the proof broke but not *why*. For example, the message does not say whether the invariant is false or merely too weak to carry through the loop (p.1, p.3 §2.2).

LLM-based proof repair loops (generate, run Verus, read the error, retry) therefore work from coarse, ambiguous feedback. Existing tools compensate in two ways (p.1, p.3):
- They hand-write a repair strategy for each error type, as AutoVerus does. These strategies are brittle across Verus versions.
- They train on large synthetic datasets, as SAFE does. The paper cites SAFE's data curation as "a month of non-stop GPT-4o invocations and rejection sampling".

Classical verification instead uses **counterexamples**: concrete program states that show why a proof fails. Verus cannot produce usable ones. Its SMT encoding is lossy and heavy on quantifiers, so the solver often answers `unknown`, and any model it does return is written in internal symbols with meaningless values (p.2, p.3, App. F p.20). The paper says Verus developers discontinued counterexample support because the values were misleading (p.4).

## 2. Key idea and why it works

**Idea:** do not try to decompile Verus's low-level SMT model. Instead, have the LLM write a small, **source-level** Z3Py query that isolates the one failing obligation, using the program's own variable names (p.2 "Our approach"; p.5 §3.1). The LLM may *concretise* aggressively, for example by fixing an arbitrary array's length to 2, which removes quantifiers. The solver then quickly returns small, readable states such as `nums=vec![-1,-1], i=1, max=0` (p.4).

**Pipeline in plain words:**
1. **Generate.** The LLM translates the failing invariant/assertion into Z3Py and enumerates up to *k* distinct models. It retries if the result is not SAT or if there are too few models (Alg. 2 p.19; prompt App. I.1 p.23–24).
2. **Validate** (invariant errors only). A non-LLM step extracts the loop into a standalone function and turns the invariants into "before" and "after" assertions. It injects each counterexample's values and runs Verus. The counterexample counts as genuine only if it triggers the expected symptom:
   - *InvFailFront*: the "before" assertion fails.
   - *InvFailEnd*: "before" passes and "after" fails.

   (p.5 §3.1)
3. **Triage.** An LLM reads the proof, the error and the counterexamples, then judges whether the counterexample states are **reachable**. If they are, the invariant is a *wrong fact* and must be replaced or weakened. If they are **spurious** (unreachable), the invariant is correct but *too weak* and must be strengthened (p.5 §3.2; prompt App. I.5 p.28).
4. **Mutate and rank.** A mutator chosen by the triage verdict, either strengthen-based or replace-based, proposes 5 candidate proofs (p.6 §4.1). Candidates are ranked by **how many validated counterexamples they block**, meaning the counterexample no longer triggers the failure under the new invariant. This ranking is inspired by PDR/IC3 (p.6). For non-invariant errors, ranking falls back to the number of verified sub-goals. If any candidate passes Verus outright, it is returned (Alg. 3).
5. Loop until Verus passes or 10 iterations are used (p.6 §4.1).

**Why it works** (the paper's argument; p.2, p.9, p.14):
- A concrete state turns "invariant fails" into "invariant fails *here*". That points at the root cause, such as an overlooked edge case (`i=0`) or a fact that is simply wrong.
- Several counterexamples make the *pattern* visible, so the LLM can generalise from points to a predicate (for example, "all CEXs have i=0 and sum[0]>0", so guard with `i > 0 ==>`). Fixed-template CEGAR/PDR generalisation struggles with infinite domains such as integers and heaps (p.9).
- Blocking counts give a cheap, verifier-grounded score for choosing among LLM guesses.
- Soundness never depends on the LLM. Counterexamples may be wrong, but every repair is re-checked by Verus (p.2).

## 3. Pipeline for the architecture diagram (matches Figure 2, p.4; details from Alg. 1–3, p.19)

**Groups (as in F2):** ① Initial Proof · ② Counterexample Generation & Validation · ③ Mutation-based Counterexample-guided Repair

**Nodes**

| id | name (F2 label) | role (1 line) |
|---|---|---|
| N1 | Initial Proof & Verus Feedback | LLM drafts proof (AutoVerus phase-1 prompt); Verus checks it and returns errors |
| N1b | Compilation Fixer *(Alg.1 only, not in F2)* | if the proof doesn't compile, an LLM fixes syntax/types first |
| N2 | Synthesize Z3 Query (LLM) | LLM writes a source-level Z3Py script for the one prioritised failing error |
| N3 | Status (Z3) | runs the script: SAT / UNSAT / unknown |
| N4 | Counterexamples CEX_1..CEX_n | concrete source-level states (JSON) from enumerating models |
| N5 | CEX Filtering (Verus) | validation: inject each CEX into the extracted loop harness; keep only those that reproduce the symptom (invariant errors only) |
| N6 | Valid CEXs | the validated set |
| N7 | Error Triage (LLM) | reachable → "Incorrect" (wrong_fact); spurious → "Not Inductive" (too_weak) |
| N8 | Error Category | {Not Inductive, Incorrect} |
| N9 | CEX-guided proof mutation (LLM) | Strengthen-based mutator / Replacing-based mutator; 5 candidates |
| N10 | Mutated Proof Candidates | candidate proofs |
| N11 | Ranking Based on #CEXs Blocked | pick the candidate blocking most valid CEXs (Verus re-run per candidate) |

**Edges**

| from → to | label |
|---|---|
| N1 → N2 | failing proof + error (LLM icon) |
| N2 → N3 | Z3 |
| N3 → N2 | "Retry if not SAT" |
| N3 → N4 | "SAT" |
| N4 → N2 | "Retry if Not Enough Samples" (Alg.2: fewer than k/2 models, or format invalid) |
| N4 → N6 | "CEX Filtering" (via Verus, N5) |
| N6 → N7 | (LLM) |
| N7 → N8 | verdict + rationale |
| N8 (Not Inductive) → N9 Strengthen-based | (LLM) |
| N8 (Incorrect) → N9 Replacing-based | (LLM) |
| N9 → N10 → N11 | "Mutated Proof Candidates" |
| N6 → N11 | valid CEXs used for scoring |
| N11 → N1 | "Updated Proof" (loop; max 10 iterations) |

Accuracy notes for the diagram:
- F2 shows two triage categories. The triage prompt (App. I.5) and Alg. 3 also have a third verdict, `other`, which uses its own "Mutator for other errors" (App. I.4 Prompt 3).
- Validation applies only to invariant errors. For other errors, unvalidated CEXs flow straight to triage (Alg. 1 lines 19–23).

## 4. Results (most important numbers)

| # | Claim | Number | Locator |
|---|---|---|---|
| R1 | Headline gain | "solves 38% more tasks on average than the state-of-the-art, and the advantage widens to 2× on harder benchmarks such as LCBench and HumanEval" | p.2 Intro "Results" |
| R2 | Best model, all 4 benchmarks (Sonnet-4.5) | ExVerus / AutoVerus / Iterative Refinement: VerusBench **88.4** / 75.3 / 83.6; DafnyBench **95.5** / 95.5 / 95.5; LCBench **28.6** / 14.3 / 25.0; HumanEval **41.2** / 27.9 / 29.4 (% success) | T1 p.7 |
| R3 | Weaker model gains most on VerusBench (DeepSeek-V3.1) | ExVerus **71.9%** vs AutoVerus 24.7% vs Iterative Refinement 60.3% | T1 p.7 |
| R4 | Robustness (ObfsBench, 266 obfuscated tasks) | e.g. DeepSeek-V3.1: ExVerus 73.9–86.5% vs AutoVerus 24.7–36.5% across 6 obfuscation strategies; Sonnet-4.5: 78.3–92.3% vs 56.5–77.3% | T2 p.7; benchmark size p.6, App. E p.20 |
| R5 | Cost & speed (DeepSeek-V3.1, per task) | **$0.04 vs $0.17**; **720.3 s vs 2989.1 s**; input/output tokens 93.8k/14.8k vs 422.7k/50.6k (ExVerus vs AutoVerus) | T3 p.8; text p.7 "Cost" |
| R5b | Cost with GPT-4o (per task) | $0.42 vs $0.69; 250.0 s vs 233.9 s (ExVerus slightly slower here) | T3 p.8 |
| R6 | Ablation: mutation + validation matter | ObfsBench DeepSeek-V3.1: **81.6%** full vs 65.4% ExVerus_NO_MUT; VerusBench DeepSeek-V3.1: 71.9% vs 64.4% | T4 p.8; text p.7 |
| R7 | More counterexamples help (single repair, InvariantInjectBench, 187 tasks) | 10 CEXs: **106/187** solved; 1 CEX: 100/187 | p.7–8 §4.3 |
| R8 | Blocking predicts success (ExVerus_ONE_CEX) | mutants that block the CEX: 172/243 (70.78%) verify; mutants blocking 0: 38/153 (24.84%) | p.8 §4.3 |
| R9 | Complementarity | ExVerus uniquely solves 101 tasks AutoVerus cannot; AutoVerus uniquely solves 26 | App. H.1 p.21, F6 p.22 |
| R10 | Motivating contrast: raw Verus counterexample | 7,083-line SMT query; Z3 returns `unknown` with a 3,130-line log; model gives `i=537`, `nums.len=1681` | p.3–4 §2.2, F1 |

Setup facts for on-screen captions:
- 5 LLMs: Claude-Sonnet-4.5, GPT-4o, o4-mini, Qwen3-Coder-480B-A35B, DeepSeek-V3.1. Temperature 1.0, max 10 repair iterations, 5 mutants (p.6). The default is 10 CEXs (p.7).
- Benchmarks: VerusBench 146 tasks (p.6 fn.2), DafnyBench/Dafny2Verus 67, LCBench 28 (~200 LoC each), HumanEval-Verus 68, ObfsBench 266 (p.6).
- Implementation: Verus 0.2025.07.12.0b6f3cb, Z3Py 4.15.1.0, ~13K LoC Python plus ~2K LoC Rust (p.6).

Recommended on-screen subset: R1, R2 (bar chart, 4 benchmarks), R4, R5, R6, R10. Use R8 as the "why blocking works" beat.

## 5. Motivated example: candidates

Ranking by on-screen clarity, plus how completely the paper documents each step:

### ★ Candidate A (RECOMMENDED): `brs1`, "the uninitialised sum" (F3, p.13, App. A.1, VerusBench Diffy/brs1)
Files: `examples/03a`–`03f`. Screen version: `03e_brs1_screen_simplified.rs` (the adaptation is spelled out in its header).
- **(a) Program + failing proof.** `myfun(a, sum, N)` fills `a` with 1s, then a second loop accumulates into `sum[0]` and resets it to 0 only on the first iteration (`if i == 0 { sum.set(0,0) }`). The LLM's proof contains the invariant `sum[0] <= i as i32` (03a).
- **(b) Verifier error:** `error: invariant not satisfied before loop` (InvFailFront) (F3 panel 1; p.13).
- **(c) Counterexamples:** `CEX_1: {a: vec![1,1], sum: vec![1], i: 0, N: 2}`, `CEX_2: {… sum: vec![2], i: 0 …}` (F3 panel 2). Before the loop, `sum[0]` is whatever the caller passed in, so `1 <= 0` is false.
- **Validation:** the CEX is injected into the `myfun_loop2` harness, and `assert(sum[0] <= i as i32)` fails, so the CEX is validated (F3 panel 5, red).
- **Triage:** `"verdict": "wrong_fact"`, "fails before loop entry when i=0 and sum[0] is positive, which are reachable states" (F3 panel 3).
- **(d) Generalisation:** the pattern shared by all CEXs is "i=0 and sum[0] positive". The mutator therefore guards the invariant with `- sum[0] <= i as i32,` → `+ i > 0 ==> sum[0] <= i as i32,` (F3 panel 4; text p.13). The new invariant blocks CEX_1: the harness assertion passes (F3 panel 5, green).
- **(e) Verified:** "mutant-1 successfully blocks all counterexamples and passes Verus verification" (p.13). The benchmark's ground-truth proof uses the same guarded invariant (repo `cleaned-verusbench/Diffy/verified/brs1.rs:35`; `03f`).
- **Hook number:** AutoVerus failed this task after 15+4+21 attempts, 16 of them on this exact error (p.13).
- **Why #1:** it is the only paper example with all five stages shown verbatim. The CEX is two tiny arrays. The fix is a single guard, and it reads as "the edge case the LLM forgot".

### Candidate B: `findmax`, the paper's running example (F1 p.3, F8 p.23, VerusBench Misc/findmax)
Files: `examples/02a`–`02e`.
- **(a)** `find_max(nums)` with invariant `exists |j: int| 0 <= j < i ==> nums@[j] == max` (02a).
- **(b)** `invariant not satisfied at end of loop body` (InvFailEnd) (F1).
- **(c)** CEX_1..CEX_9: `nums=vec![-1,-1], i=1, max=0`, … `vec![-9,-9], max=-8` (F1 top right). The contrast is Verus's own model: `unknown`, `i=537`, `len=1681`, `Poly!val!31` (F1 bottom right; 02c). The split-screen of "LLM-made source-level CEX" against "Verus's raw SMT dump" is the most visual beat in the paper.
- **(d)** The triage recognises that `max=0` is not in `[-1,-1]`, so the state is **spurious**, and returns verdict `too_weak` (F8, verbatim in 02d). This is the "strengthen" branch, which complements A's "replace" branch.
- **(e) GAP:** the paper **does not show ExVerus's final repaired findmax proof**. The repo records only that the task ended in `verification_pass` in the DeepSeek VerusBench run (`vinv/analysis/figure/data/ExVerus/ds_vb_global_repair_status_z3_mut_val.json`, key `verusbench_misc_findmax`), without the repaired file. The benchmark's ground-truth proof replaces `==>` with `&&` inside the `exists` (02e, line 18). Showing that as "ExVerus's fix" would be an extrapolation, so label it "the reference fix".
- **Subtlety for the script:** `exists |j| 0 <= j < i ==> …` is a classic Verus/Dafny pitfall, because it is trivially satisfiable by any out-of-range `j`. The F1 Z3Py script does not encode that pre-state `exists` at all. It encodes only the post-state as `nums0 != max_post && nums1 != max_post`. Keep the narration at "the CEX shows max is not in the array".
- **Best use:** cold open / problem framing (F1 split-screen). Then switch to A for the full repair story.

### Candidate C: `count_up` (repo agent skill, *not in the paper*)
Files: `examples/05a`–`05d` (verbatim from `skills/counterexample-guided-proof/SKILL.md`).
- `i <= n, j <= 1000` fails at end of loop body. The CEX `{n:1, i:0, j:1000}` is unreachable, so the invariant is too weak; adding `j == i` blocks it. Round 2 gives `{n:1001, i:1000, j:1000}`; adding `n < 1000` makes it verify (per the skill text).
- It is the cleanest pedagogical demo (8-line loop, two rounds, shows both "spurious → strengthen" and iteration). It is not a paper result, and the final program appears only in prose, so it must be labelled as the authors' tutorial example.

### Candidate D: `two_sum` (F4 p.14, ObfsBench) — not recommended for screen
It has a nested quantifier over `ii, jj` with a disjunction, making it hard to read at video scale. It is useful only as a second "wrong_fact → remove disjunct" example (`examples/04`).

**Recommendation:** open with B's F1 split-screen (why Verus's own counterexamples are useless), then tell A end-to-end as the motivated example. Optionally use C as an animated "how the loop iterates" explainer, labelled as from the project's agent skill.

## 6. Limitations / what the paper does not claim

- **Validation covers only loop-invariant errors** (InvFailFront/InvFailEnd). Counterexamples for assertion, precondition and other errors are unvalidated "approximate, structured reasoning steps" (p.5, p.8 §5).
- **Counterexample generation is not guaranteed** to succeed or be correct. The LLM may relax soundness (for example, concretising lengths), and CEXs can be spurious or hallucinated. Only the final Verus check is trusted (p.2, p.5).
- **Initial proof generation is not a contribution.** It reuses AutoVerus's prompt (p.8 §5, App. D).
- **Weaker on assertion and proof-block-heavy tasks.** On VerusBench with GPT-4o, AutoVerus beats ExVerus on tasks needing asserts (39.4 vs 18.2%) and proof blocks (36.4 vs 9.1%) (T5 p.23, App. H.3). ExVerus targets invariants.
- **Hard benchmarks remain hard.** Absolute rates are low: LCBench ≤ 28.6%, HumanEval ≤ 41.2% (T1). On LCBench, ExVerus ties the baselines for DeepSeek, GPT-4o and Qwen (10.7%).
- **The baseline is affected by a Verus version change.** AutoVerus drops from 75.33% to 52.7% when moved from Verus 2024/8/13 to 2025/7/12 (App. H.4 p.22), so part of the gap to AutoVerus is version mismatch.
- **Stochastic LLM runs.** Exact numbers may not reproduce bit-for-bit (App. C p.19).
- **The VeruSAGE case (A.3) is one anecdote** of an agentic adaptation (Copilot CLI + Sonnet 4.5 with a CEX-augmented prompt), not the ExVerus pipeline and not a benchmark result. The 81% figure belongs to the Hands-Off baseline from Yang et al. 2025b (p.14).
- **The paper does not claim** completeness, termination guarantees, decompilation of Verus models, or that verified proofs match user intent. The Impact Statement warns against "confus[ing] verifier-passing with correct intent" (p.9).

## 7. Continuity hooks

ExVerus makes the counterexample the unit of feedback. A failed proof becomes a few concrete states, and a repair is scored by how many of those states it rules out. That blocking count is already a verifier-grounded, automatically computed signal. It is the natural thing to *learn from* rather than only prompt with, which is where TopoVerus (learned counterexamples / RL) picks up. *[Confirm the exact TopoVerus framing from its own paper; ExVerus itself does not mention TopoVerus.]* Appendix A.3 already points toward scale: the same "write down a counterexample first" instruction moved an agent past a 4,179-line temporal-logic proof in a Kubernetes controller. This suggests the idea carries from loop invariants to system-level inductive invariants (p.14–18). That is the bridge to larger verification efforts such as C-level kernel equivalence (Vekto).

## 8. Glossary (define on screen)

- **Verus**: verifier for Rust; proofs are Rust code plus annotations checked by an SMT solver (p.1–2).
- **Specification (`requires` / `ensures`)**: pre-condition / post-condition of a function (p.2).
- **Loop invariant**: a fact that holds every time the loop is about to check its condition. It must hold on entry and be preserved by one iteration (p.3, p.5).
- **Inductive (invariant)**: if it holds before an iteration, it still holds after. "Not inductive" = InvFailEnd (p.5).
- **Verification condition (VC)**: logical formula Verus generates and sends to the solver (p.2).
- **SMT solver / Z3 / Z3Py**: automated logic engine; Z3Py is its Python API (p.6).
- **SAT / UNSAT / unknown**: solver found a model / proved none exists / gave up (often due to quantifiers) (p.3).
- **Quantifier (`forall` / `exists`)**: "for all" / "there exists"; makes SMT solving incomplete (p.2).
- **Counterexample (CEX)**: concrete state σ with σ ⊨ A ∧ ¬C for a failing obligation A ⟹ C (Def. 2.1 p.4).
- **Reachable vs. spurious CEX**: can or cannot occur in a real execution. Reachable means the invariant is wrong; spurious means it is too weak (p.5).
- **Blocking**: an updated proof blocks σ if σ no longer violates the new obligation (Def. 2.2 p.4; p.6).
- **InvFailFront / InvFailEnd**: invariant fails at loop entry / is not preserved by the loop body (p.5).
- **Mutator (strengthen / replace)**: LLM prompt that edits invariants in a given direction (p.5; App. I.4).
- **CEGAR / PDR (IC3)**: classic counterexample-driven verification algorithms that ExVerus draws on (p.9).
- **AutoVerus**: prior state-of-the-art LLM Verus prover with hand-crafted repair agents (p.6, p.22).
- **ObfsBench**: the paper's 266-task obfuscated VerusBench variant for robustness (p.6, App. E).

## 9. Open questions / uncertainties

1. **The "38% more on average" (p.2) and "+60.92% on VerusBench" (p.6) figures** are not reproducible by a simple average of T1 values. The derivation is unstated. The project page instead says "+45% over SOTA". Do not show these three side by side; quote one with its source.
2. **"2× on LCBench and HumanEval" (p.2) vs "about 2× and 1.5× … on LCBench and HumanEval, respectively" (p.6).** These are inconsistent; prefer the p.6 wording.
3. **Robustness claim (p.7):** "except GPT-4o, ExVerus … above 73%, whereas AutoVerus remains below 40%". T2 contradicts both halves:
   - Qwen3-Coder × Dead Code Insertion is 65.2%.
   - AutoVerus with Sonnet-4.5 reaches 56.5–77.3%.

   The Intro says "<50%" for the SOTA. Show only T2 cells, not the summary sentence.
4. **p.8 typo:** "repair 41/51 tasks (64.49%)". 41/51 is 80.4%, so the percentage seems copied from the line above.
5. **T1 vs T4:** the Iterative Refinement values for Qwen3-Coder and o4-mini appear swapped between the two tables on DafnyBench, LCBench and HumanEval. T2 also orders the o4-mini and Qwen columns differently from T1.
6. **"$0.04 per task on average" (p.2) is the DeepSeek-V3.1 row of T3.** With GPT-4o the figure is $0.42. Caption the model.
7. **App. H.4 says AutoVerus with GPT-4o on the new Verus gets 52.7%,** but T1 lists 39.0% for AutoVerus/GPT-4o/VerusBench. The settings may differ; this is unexplained.
8. **F6/H.1 (101 vs 26 unique solves):** the model is not stated. F7 says GPT-4o.
9. **Project-page numbers** ("90% robust … vs 33–50%", "70.2% counterexample-blocking", "~75% fewer tokens on DeepSeek, ~25% on GPT-4o", "up to 95.5% with o4-mini") do not appear verbatim in the paper. The 95.5% matches T1 o4-mini **DafnyBench** only; o4-mini on VerusBench is 74.7%. Treat the page as marketing and cite the tables.
10. **findmax final fix:** not shown in the paper (see §5 B). The brs1 repaired file is also not in the repo; the paper text is the only evidence that mutant_1 verified.
11. **Figure transcriptions** were made from 300-dpi renders. Indentation and blank lines in `02a/02b/03a/03d` follow the figure layout, and the ASCII glyph mapping is ours. No example was run through Verus or Z3 (per the no-execution constraint).
12. **F3 panel 5 typo** "assertopm fail" is in the original figure; it is kept in the transcription.
