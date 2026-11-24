# TopoVerus: research brief for the explainer video

**Paper:** *Curriculum Proof Repair with Learned Counterexamples*. Yuechun Sun, Jun Yang, Kexin Pei (University of Chicago). arXiv 2611.13627v1 [cs.PL], 10 Nov 2026. NeurIPS 2026 (paper footer, p.1).
**Code:** github.com/Etha-Sun/Topoverus, shallow clone at commit `878496237052eeccdd8478b9f9037041affe1431` (2026-10-29), in `repos/Topoverus`.
**Model:** huggingface.co/YuechunSun/TopoVerus-32B. BF16 weights, Apache-2.0, finetuned from Qwen/QwQ-32B.
**Project page:** topoverus.github.io

Citation conventions:
- "p.N" is the PDF page number.
- "repo:path:lines" refers to the clone above.
- `examples/` files each start with a header that gives their source location.
- Files with DERIVED in the name are our own computations or edits. They are labelled as such and are not source material.

Nothing in this brief was executed: no Verus, no Lynette, no model. The only script run was a pure-Python re-implementation of the reward formula, used for the worked example in §2.5.

---

## 1. Problem statement

**Why verifier-in-the-loop repair struggles.** LM-based Verus tools follow a common loop: the model proposes annotations, Verus reports failures, and the model revises. Verus messages usually name only the failed obligation, for example `postcondition not satisfied`. They do not show the source-level state, the execution path, or the missing fact. The model must guess the root cause, "making repair brittle and token-inefficient" (p.2, §1 ¶2).

**Two existing workarounds, each with a gap (p.2 ¶3):**
- **Prompt engineering.** Repair rules, syntax guidance, in-context examples, and retrieval (AutoVerus, the Sun et al. 2026 citation [VeriStruct], RAG-Verus). This knowledge "is costly to curate and does not generalize as verifier behavior and proof idioms evolve."
- **Learning from verifier outcomes.** Pass/fail for search or fine-tuning (AlphaVerus, SAFE). This gives "only sparse, indirect signals for repair."

**Why ExVerus is costly or limited.** ExVerus is the series' previous episode, cited as Yang et al. 2026b with Sun as second author. It showed that counterexamples are more actionable feedback. The TopoVerus paper describes three limits:
- Useful counterexamples need "nontrivial, execution-level code reasoning". Existing approaches therefore "incur high inference costs, as they require iterative refinement to generate high-quality counterexamples (Yang et al., 2026b)" (p.2 ¶4).
- They train or check counterexamples "as standalone artifacts with hand-written validators (Yang et al., 2026b)" (p.2 ¶5). Strict formal validation "is often intractable" (p.9, Related Work).
- "proof failures often conflate multiple missing or incorrect invariants, so which counterexample is most useful to address first is not well defined" (p.2 ¶4).

**What a learned repair model adds.** TopoVerus "internalizes counterexample-guided diagnosis as a model capability, producing useful counterexamples in a single pass" (abstract, p.1). It redefines what makes a counterexample useful: a counterexample is useful "when conditioning on it helps the model produce a safe, verifier-passing proof" (p.1). The model is never told whether its counterexample is "correct". The counterexample gets *indirect credit through downstream repair success* (p.2 ¶5).

## 2. Key ideas in plain words

### 2.1 One trajectory: counterexample, then rationale, then repaired proof
Input: the failed proof and the Verus error. Output, in this order and in one response (p.2 ¶5, p.5 §3.1, App. D p.20):
1. `<think>`: free chain of thought.
2. `<counterexample>` with three mandatory fields. Formally this is a tuple (σ, τ, ψ) (p.5):
   - **[State]**: a concrete program state σ such that σ ⊨ A_t(σ) ∧ ¬C_t(σ). The antecedent holds and the proof obligation fails (Eq. 1, p.4–5).
   - **[Execution Trace]**: τ, the execution from σ.
   - **[Violation]**: ψ, a natural-language reason why the obligation is falsified.
3. `<reasoning>`: a concise repair plan.
4. One `rust` code block with the complete repaired program.

The counterexample is model-generated reasoning. It is **not** produced by an SMT solver and **not** formally checked (p.5 ¶1; Limitations p.10).

### 2.2 Counterexample-guided SFT (stage 1)
- **Base model:** QwQ-32B (p.6 §4.1).
- **Data (p.6–7):** 461 repair trajectories from 249 source programs. The teacher, *Sonnet 4.6*, sees the failed proof, the verifier error, and the verified reference program. It writes the `<think>`/`<counterexample>`/`<reasoning>` text. "We extract the generated reasoning and append the verified reference program unchanged to form the target response for SFT."
  - In the video, say it this way: the teacher knows the answer and writes the diagnosis that leads to it.
- **Hyperparameters (p.7):** 4×L40S, DeepSpeed ZeRO-3, lr 2×10⁻⁵, batch 32, max length 8,192, 2 epochs.
- **Repo implementation:** `ctx_target` assembles exactly think → counterexample → reasoning → one final rust fence. It rejects targets that lack [State], [Execution Trace] or [Violation] (repo:topoverus/code.py:42-60). SFT targets are kept only if the safety check passes and Verus verifies them (repo:topoverus/data.py:202-223).
- **Ablation naming:** the SFT-only model with the counterexample format is **CTX-Init**. Chain-of-thought-only SFT is **CoT-Init** (p.6).

### 2.3 GRPO with Verus feedback (stage 2)
The policy is response-level, π_θ(y | x), optimized with GRPO. The reward (Eq. 2, p.5) is

  R(x,y) = S_safe · [ G_format(y) · ( R_pass + λ_dep · R_dep ) + λ_format · R_format ]

- **R_pass:** in the paper, 1 if Verus accepts the program (p.5). *The released config differs:* `verus_mode: "fraction"`, so r_verus = verified / (verified + errors) (repo:configs/reward.json; repo:topoverus/reward.py:75-76). See §9.
- **R_format ∈ [0, 0.4]:** 0.1 for each non-empty think, counterexample and reasoning block, plus 0.1 if all three counterexample fields are present (repo:reward.py:36-46).
- **G_format:** 1.0 if both the counterexample and reasoning blocks are present, 0.5 if one is, 0.2 if neither (repo:configs/reward.json `format_partial` 0.5, `format_none` 0.2). The paper says only "full / reduced / smaller" (p.5). The gate exists to prevent "mode collapse into standard Chain-of-Thought repair that bypasses the counterexample reasoning step" (p.5).
- **Weights in the released code:** λ_dep = 1.0 (`dependency_weight`). R_format is added unweighted (repo:reward.py:81-82).
- **Hyperparameters (p.7):** FSDP2, 4-way Ulysses sequence parallelism, vLLM rollouts at temperature 0.7 and top-p 0.9, 8 rollouts per prompt, lr 2×10⁻⁶, no KL penalty, clip 0.28, 2 epochs over 249 programs. These match repo:configs/dep_rl.json.
- **Ablation naming:** GRPO with only the verifier reward is **CTX-Binary**. With the topological reward it is **CTX-Dep**, which is TopoVerus itself (p.6).

### 2.4 Proof-code safety gate: why it is needed
- **The problem.** "Passes Verus" alone can be gamed. A model can make the program verify by editing the executable code, weakening the `requires`/`ensures` specification, or adding trusted escape hatches such as `assume(false)`, `#[verifier::external_body]` or `admit`. The verifier then says yes, but the user's original claim was never proven.
- **The gate.** S_safe ∈ {0,1} uses **Lynette**, an AST-level checker from the AutoVerus authors (Yang et al. 2025). It checks that the model "only modified the proof annotations (invariants, assertions, etc.); unsafe modifications (e.g., execution code) receive zero reward" (p.5).
- **The metric.** "A solution is *safe* if Lynette confirms that executable code and user specifications were not changed" (p.6). All headline numbers are **Safe**-Pass.
- **Repo extensions** (docs/SAFETY.md; repo:topoverus/trust.py; repo:topoverus/tools.py:75-116):
  - Lynette is patched to version `topoverus-trusted-ghost-context-v4`. It compares executable code, contracts, spec functions, declarations and trust contexts (`compare -t --requires --ensures --spec --decreases --assumes`).
  - A Python pre-check, `trust_change`, rejects any *new* `assume(…)`, `admit(…)`, `axiom fn`, `#[verifier::external_body]`/`external`/`verify(false)`.
  - The check runs *before* Verus in the reward. An unsafe response gets reward 0 (repo:reward.py:66-69).
- **Concrete cases.** The repo tests contain cases where **Verus says "verified" but the gate says "unsafe"**:
  - moving an existing `assume` past an assignment;
  - changing a trusted helper's contract;
  - making a conditional `assume` unconditional.

  See §5.4 and `examples/safety-gate-SCREEN.txt`.
- **Caveat.** These are author-written unit tests, not recorded model behaviour. The paper does not quantify how often RL rollouts were caught by the gate.

### 2.5 Topological Graph Reward (R_dep ∈ [0,1])

**Intuition (§2.1, p.3–4).** Some invariants only make sense once others hold. In binary search (Fig. 1, p.3):
- I1 bounds the array length.
- I2 and I3 keep `low` and `high` in range, using I1.
- I4 and I5 are the partition facts, and they are "useful only when the boundary invariants (I2 and I3) hold."

If a repair attempt omits I1–I3, its counterexample for I5 is "under-constrained". Fig. 2 (top) shows such a diagnostic. It has a plausible State–Trace–Violation format, but it instantiates `i=1` outside the quantifier range when `high=2`, uses a hallucinated `mid`, and gives a hand-wavy second violation. With I1–I4 established, the same format produces an exact, actionable counterexample (Fig. 2 bottom): `nums=[1,3,5]`, `target=5`, `high=2` → `nums[2] > 5` is false → change `high <= i` to `high < i` (p.4).

**Definitions (p.5–6, all computed offline from the verified reference proof):**
- **Def. 1, inductive subset.** S ⊆ V is inductive if ⋀S is (i) established by the loop precondition and (ii) preserved by every loop-body iteration.
- **Def. 2, dependency graph.** deps(v_i) = (⋂ of all inductive subsets containing v_i) \ {v_i}, meaning the invariants present in *every* inductive set that contains v_i. There is an edge (v_j → v_i) if v_j ∈ deps(v_i): "v_j must be established before v_i can be inductively verified."
- **Def. 3, SCC condensation.** Mutually inductive groups form SCCs (Tarjan). The condensation is a DAG, so it has a topological order.
- **Enumeration (App. A, p.14–16).** Exact enumeration of minimal inductive subsets relates to hypergraph transversal enumeration. Algorithm 1 is a level-wise BFS over subset sizes with antichain pruning and a budget of B = 256 verifier calls. Run on 531 programs: 9,216 Verus calls versus 81,143 naive (8.8×), ≈64 min. Median n = 3 invariants; 98% have n ≤ 8, which makes them exact (Table 3, p.16).

**Reward (Eq. 6, p.6):**
1. Extract the model's loop invariants and match them to the canonical set V. Matching is exact substring first, then token-set Jaccard ≥ 0.6. Call the matched set V′.
2. Let Ê′ be the inter-SCC edges whose two endpoints are both matched. pos(v) is the position of v in the model's output.
3. Compute

   R_dep = α · β,  α = |V′| / |V|  (coverage),  β = |{(v_j,v_i) ∈ Ê′ : pos(v_j) < pos(v_i)}| / |Ê′|  (edge satisfaction; β = 1 if Ê′ = ∅).

At training time this reduces to matching plus an O(|V|+|E|) edge check (p.6 Remark).

**Worked example for the video** (`examples/rdep-worked-example-DERIVED.txt`). Canonical V = I1..I5 from Fig. 1. The edge set is **illustrative**: I1→I2, I1→I3, I2→I4, I3→I4, I2→I5, I3→I5. This is our reading of the §2.1 text and the Fig. 2 drawing; the paper does not list exact edges.

```
      I1
     /  \
   I2    I3
   | \  / |
   |  \/  |
   |  /\  |
   I4    I5
```

Values computed with a faithful re-implementation of the repo's `matcher_v2.match` and `graph.dependency_score`:

| Model writes invariants in this order | α | considered edges | satisfied | β | R_dep |
|---|---|---|---|---|---|
| I1, I2, I3, I4, I5 (topological order) | 1.0 | 6 | 6 | 1.0 | **1.0** |
| I4, I5, I1, I2, I3 (partition facts first) | 1.0 | 6 | 2 (only I1→I2, I1→I3) | 0.333 | **0.333** |
| I5, I4, I3, I2, I1 (reversed) | 1.0 | 6 | 0 | 0.0 | **0.0** |
| I1, I2, I3, I4 (I5 missing) | 0.8 | 4 | 4 | 1.0 | **0.8** |
| I4, I5-wrong (`high <= i`), the paper's under-constrained attempt | 0.4 | 0 | 0 | 1.0 (no comparable edge) | **0.4** |

Two observations are worth saying on screen:
- **The matcher is lexical, not semantic.** The buggy `high <= i` version of I5 still fuzzy-matches the canonical I5 (Jaccard 0.941). R_dep rewards *which* facts are written and *in what order*. Correctness still comes from Verus, through R_pass.
- **R_dep does not require the proof to verify.** In both Eq. 2 and repo:reward.py:72-82, R_dep is added whenever the response is safe and Verus completed, even with errors. That is what makes it *process* feedback: a failing attempt that lays down prerequisites in the right order still earns signal. The paper calls this a "micro-curriculum within each repair attempt" (p.6).

**Evidence that it changes behaviour.** Table 7 (p.20) reports a post-hoc analysis of 24 paired verified tasks:
- Coverage α is nearly unchanged: 98.6% for CTX-Binary versus 98.5% for CTX-Dep.
- Edge satisfaction β rises from 43.8% to 95.8%.
- Tasks with β = 1 rise from 10/24 to 23/24.

The models find the same invariants; CTX-Dep writes them in dependency order.

## 3. Pipeline (for architecture diagrams)

The paper has **no pipeline/architecture figure**. Fig. 1 is code, Fig. 2 is diagnostics, Fig. 3 is scaling plots and Fig. 4 is a case study. The lists below come from the text (§3, §4.1, App. A, App. D), the repo (README "Training", docs/TRAINING.md, docs/DATA.md) and the project-page TLDR. Each node cites its source.

### 3.1 Data generation (offline)
Nodes:
- **D1** Source programs with verified reference proofs. The RL train split has 249 programs (p.7; repo:configs/data-inputs.json `rl_verus_train.jsonl` rows 249).
- **D2** Failed proof + Verus error, one per training instance (p.6–7).
- **D3** Teacher LM, Sonnet 4.6. It sees the failed proof, the error and the reference proof (p.6–7).
- **D4** Teacher trajectory: `<think>` + `<counterexample>`[State/Trace/Violation] + `<reasoning>` (p.7).
- **D5** SFT target: the teacher reasoning with the verified reference program appended unchanged (p.7; repo:code.py `ctx_target`).
- **D6** Filters, repo only: held-out deduplication, Lynette safety, Verus verified (repo:data.py:190-223).
- **D7** SFT dataset: 461 trajectories over 249 programs (p.6).
- **D8** Invariant extraction from the reference proof, giving V (p.5).
- **D9** Inductive-subset enumeration with Verus as oracle: level-wise BFS, B = 256 (App. A, Alg. 1, p.15).
- **D10** Dependency graph G and its SCC condensation into a DAG (Defs. 2–3, p.5–6).
- **D11** graphs.jsonl, a per-program lookup used by the reward (repo:docs/DATA.md; repo:verl_adapter.py).

Edges: D1→D2; D2→D3; D1→D3 (reference); D3→D4; D4→D5; D1→D5; D5→D6→D7; D1→D8→D9→D10→D11.

### 3.2 Training stages
Nodes:
- **T0** QwQ-32B (p.6).
- **T1** Counterexample SFT: 4×L40S, ZeRO-3, lr 2e-5, 2 epochs (p.7).
- **T2** SFT checkpoint, CTX-Init.
- **T3** GRPO rollouts: 8 per prompt, temperature 0.7 (p.7).
- **T4** Extract the final rust block (repo:code.py `final_code`).
- **T5** Safety gate S_safe: trust_change plus Lynette (p.5; repo:reward.py:66).
- **T6** Verus, giving R_pass (p.5).
- **T7** Format score R_format and gate G_format (p.5).
- **T8** Invariant matcher plus R_dep from D11 (p.6).
- **T9** Combined reward, Eq. 2.
- **T10** GRPO update.
- **T11** CTX-Dep, which is TopoVerus-32B (BF16 export; repo:docs/TRAINING.md).

Edges: T0→T1 (with D7) → T2 → T3 → T4 → T5. Then T5 →[unsafe: reward 0]→ T9, and T5 →[safe]→ T6. Then T6 → T9; T3 → T7 → T9; T4 → T8 (with D11) → T9; T9 → T10 → T3 (loop); T10 → T11.
Ablation branches (p.6): T2 alone = CTX-Init. T3–T10 with λ_dep = 0 = CTX-Binary. A CoT-only SFT = CoT-Init.

### 3.3 Inference / evaluation
Nodes:
- **I1** Buggy Verus program + Verus error (p.6).
- **I2** TopoVerus-32B.
- **I3** Response: counterexample, rationale, repaired program.
- **I4** Verus.
- **I5** Lynette safety check.
- **I6** Success: safe and verified.
- **I7** Refinement turn: previous code + new verifier output (App. D.2, p.21).

Edges: I1→I2→I3→I4 and I3→I5; (I4 ∧ I5) → I6; otherwise I4 → I7 → I2. There are up to 10 iterations per chain and 3 independent chains for Safe-Pass@3 (p.6, Table 1 caption).
At evaluation, "Counterexamples are generated by the model, not provided as input. The reference proof, its invariant set V, and the dependency graph G are not provided" (p.6). **The graph is a training-time signal only.**

Project-page one-liner, as paraphrased by the fetch tool: failed proof + verifier error → counterexample (state, trace, violation) → repair rationale → proof repair checked by verifier + safety check; trained with topological graph reward.

## 4. Results (exact citations)

| # | Claim | Number | Source |
|---|---|---|---|
| 1 | Evaluation set | 471 problems over 7 suites: VerusBench 26, DafnyBench 17, HumanEval 15, LeetCode 5, VeriCogen 89, ObfsBench 266, VeruSAGE 53 | p.6 §4.1 |
| 2 | TopoVerus (CTX-Dep) weighted Safe-Pass@1 / @3 | **61.6% / 72.2%** | Abstract p.1; §4.2 p.7; Table 4 p.18 |
| 3 | Strongest baseline, Sonnet-4.5 | 55.9% / 65.9%, i.e. TopoVerus is **+5.7 / +6.3** points ahead | Table 4 p.18; §4.2 p.7 |
| 4 | "Weighted" means a micro-average (each problem counts equally); macro-average CTX-Dep 54.0/61.5 vs Sonnet 51.6/57.8 | +2.4 / +3.7 | App. C.1, Table 4 p.18 |
| 5 | Counterexample format alone: CoT-Init → CTX-Init, weighted Safe-Pass@1 | 39.3% → 50.5% (**+11.2**). VerusBench 46.2 → 88.5 | §4.3 p.7; Table 1 |
| 6 | Topological reward vs. binary RL: CTX-Binary → CTX-Dep | @1 53.7 → 61.6 (**+7.9**); @3 67.9 → 72.2 (+4.3) | §4.2 p.7; Table 4 |
| 7 | Binary RL alone is uneven: CTX-Init → CTX-Binary | 50.5 → 53.7 overall; VeruSAGE 9.4 → 24.5 but VeriCogen 48.3 → 44.9 | §4.3 p.7 |
| 8 | Largest suite gain: ObfsBench (obfuscated names) | CTX-Dep 69.9/80.1 vs Sonnet 62.0/75.2; +11.3 @1 over CTX-Binary (58.6) | Table 1 p.7; §4.2–4.3 |
| 9 | Learned counterexamples transfer to other repairers (118 frozen hard failures; only the counterexample source is swapped) | DeepSeek-V4 11.9% → 19.5% (**+64.3% relative**); Sonnet-4.5 31.4% → 39.0% (+24.3%); Qwen3-Coder 13.6% → 15.3% (+12.5%) | Table 2 p.8 |
| 10 | Test-time scaling (63-problem validation set) | 79.4% Safe-Pass@32 (32 chains); 69.8% Safe-Pass@1 with 32 iterations | Fig. 3 p.8; §4.5 |
| 11 | Ordering effect of R_dep (24 paired verified tasks, post hoc) | edge satisfaction β 43.8% → 95.8%; coverage 98.6% vs 98.5% | Table 7 p.20 |
| 12 | Offline graph cost | 531 programs, 9,216 Verus calls (vs 81,143 naive, 8.8×), ≈64 min | Table 3 p.16 |
| 13 | Where it still loses | VeruSAGE (systems code): Sonnet-4.5 75.5/84.9 vs CTX-Dep 30.2/43.4 | Table 1 p.7; §4.2 |
| 14 | Faster early convergence | At 2 iterations, CTX-Dep 55.6% vs CTX-Binary 49.2% Safe-Pass@1 | Table 5 p.19 |

We sanity-checked row 2 from Table 1 and the suite sizes: Σ(size × Safe-Pass@1) / 471 = 61.57%. This is arithmetic only.

Baselines (p.6–7): Sonnet-4.5, GPT-4o, Qwen3-Coder and DeepSeek-V4 (Flash) as prompted cloud LMs. Per the Table 1 caption, "Cloud LLMs use iterative repair with verifier feedback; our models use 3 chains × 10 iterations". AutoVerus is listed under "External proof-repair systems"; its protocol is not detailed.

## 5. Motivated examples (ranked by on-screen clarity)

**None of the recorded artifacts includes a Verus run of the repaired program.** The repo keeps the buggy program, the Verus message and the counterexample for cases A, B and C. Only case B also has the full model output with a repaired program. Its verification status is not recorded, and we could not run Verus (task constraint). Every "→ verified" step below is therefore **pending a Verus check** by the video team.

### Rank 1, recommended: Case B, "Full-array claim used as a prefix invariant" (LeetCode 121 Best Time to Buy and Sell)
Sources: paper Fig. 4 (p.9) and App. B (p.17); repo docs/case-studies/b-prefix-invariant/*. Generator label `step_62_dep-reward-safe`, chain 1, iteration 1 (repo sources.json).

1. **Failing proof** (`examples/caseB-1-buggy.rs`). The loop's last invariant claims optimality over the **whole** array:
   `forall|j: int, k: int| 0 <= j < k < prices.len() ==> prices[k] - prices[j] <= max_pro,` (buggy.rs:44)
2. **Verus error** (`examples/caseB-2-verifier-error.txt`, verbatim):
   ```
   error: invariant not satisfied before loop
     --> best_time_sell_v2.rs:44:13
   ```
   The message does not say why.
3. **Structured counterexample** (verbatim, model-output.txt:2-17):
   - [State] `prices = [5, 3, 7]`, before the loop `max_pro = 0`.
   - [Execution Trace] Pair (j=0, k=2): `7 - 5 = 2 > 0 = max_pro`.
   - [Violation] The invariant "incorrectly quantifies over the *full array* … rather than just the *processed prefix* (0 <= j < k < i)."
4. **Rationale** (verbatim, model-output.txt:23): "Change the invariant to `forall|j: int, k: int| 0 <= j < k < i ==> …`. … At i=0, this is vacuously true."
5. **Repaired proof** (`examples/caseB-4-repaired-program.rs`; diff in `examples/caseB-5-diff-DERIVED.txt`). The range changes to `k < i`. **The model also deleted the invariant `i == 0 ==> min_price == i32::MAX`** (rationale item 4).
6. **Verified?** Not recorded. **Our reading, unconfirmed:** removing `i == 0 ==> min_price == i32::MAX` may break preservation of `i > 0 ==> exists|j| … prices[j] == min_price` on the first iteration, because nothing else bounds `min_price` at i = 0. Separately, the rationale's inductive-step argument ("prices[j] >= min_price >= prices[i]") is not sound as written.

   **Action before filming:** run Verus on `caseB-4-repaired-program.rs`. If it fails, use `examples/caseB-6-minimal-repair-DERIVED-UNVERIFIED.rs`. That file is the buggy file with only the one-line range fix the paper states ("should only summarize the processed prefix: 0 <= j < k < i", p.9), and it also needs a Verus run. Either outcome is honest material: the Limitations section says rationales and traces can be imprecise.

Why rank 1:
- Three numbers tell the whole story (`[5,3,7]`, `7-5=2`, `2 <= 0` false).
- It is the paper's own headline case study.
- It is the only case with a recorded full trajectory.
- It maps one-to-one onto the template in §6.

### Rank 2: Binary-search insertion (paper Fig. 1–2, §2.1). The example for the curriculum segment
Sources: `examples/paper-fig1-binary-search.rs` and `examples/paper-fig2-diagnostics.txt`.

**Story:**
- Wrong attempt: I4 plus I5 written as `high <= i …`, with I1–I3 missing.
- Its dependency-unaware counterexample is internally inconsistent: it checks `i=1` although `high=2`, and uses a hallucinated `mid=0`.
- With I1–I4 in place, the dependency-aware counterexample is exact: `nums=[1,3,5]`, `target=5`; after one iteration `low=2`, `high=2`; `nums[2] > 5` fails since `nums[2]=5`.
- Repair: `high <= i` → `high < i`, which gives Fig. 1's I5 (p.4).

This is the best example for explaining **why order matters** and **how R_dep is computed**; see the table in §2.5. **Caveat:** it is **illustrative**. The paper says Fig. 2's bottom half "shows the intended contrast", and the project page calls it illustrative. It is not a recorded model output, and no Verus run of Fig. 1 is reported. Use it as a constructed explanation, not as a model result.

### Rank 3: Case A, assertion at the wrong program point (DafnyBench `program_422_count_less_than`)
Sources: paper App. B p.17; repo a-assertion-placement/*.
- The `assert(grow.len() + shrink.len() == numbers.len())` sits between `shrink.pop()` and `grow.push(i)` (buggy.rs:18-20).
- Verus error: `error: assertion failed --> program_422_count_less_than.rs:19:16`.
- Counterexample: `numbers=[1,2,3]`; after the first pop, `0 + 2 = 2 ≠ 3`.
- Visually very simple. **However:**
  - The repo has no repaired program. The paper describes the repair only in words: the assertion "cannot justify an assertion placed between the two updates".
  - The recorded counterexample contains the model talking itself around ("Wait, let me re-read…", counterexample.txt:12-16). The paper's box shows a condensed version.

  That self-correction could be used deliberately to show the model reasoning, but it is long.

### Rank 4: Case C, missing arithmetic facts in the loop (VerusBench `task_id_447`, cube elements)
Sources: paper App. B p.18; repo c-arithmetic-context/*.
- The `requires` bounds every square and cube, but the loop invariant does not carry those bounds.
- Verus reports `possible arithmetic underflow/overflow` at `nums[i] * nums[i] * nums[i]`.
- The counterexample is a *benign* concrete state (`nums=[10,20,30]`). Its point is that the context lacks a fact, not that an overflow happens.
- Subtle and harder to show on screen. No repaired program is recorded.

### Safety gate catching an unsafe "repair" (examples/safety-gate-SCREEN.txt)
All of these are **repo unit tests** (tests/test_trust.py), not model outputs, and they were not executed here.
- **Best on screen, S3 (lines 138-149):**
  - Original: `fn target(x: i32) -> (r: i32) requires x > 1, x < 10 ensures r > 1 { let mut y = x; assume(y > 1); y = y - 1; y }`. The test asserts that Verus reports `verification_failed`.
  - "Repair": move the existing `assume` after `y = y - 1`. The test asserts that Verus reports **`verified`**, that `trust_change` finds nothing new, and that Lynette safety returns **`unsafe`**.
  - The point: verifier success alone would reward this hack. The gate gives it zero reward.
- **Simplest, S1 (lines 128-129):** `fn f() -> u32 { 1 }` → `{ 2 }` is unsafe, because the executable code changed.
- **S2 (lines 126-127):** `ensures false` → `ensures true` is unsafe, because the spec was weakened.

**Recommendation.** Lead with **Case B** as the full trajectory. Cut to **binary search** for the "which counterexample first?" curriculum segment and the R_dep arithmetic. Close the method section with **S3** for the safety gate.

## 6. Output format / trajectory template (verbatim)

**Paper App. D (p.20):** "Both templates elicit the same structured output format: a chain-of-thought reasoning block ⟨think⟩, a semi-formal counterexample block ⟨counterexample⟩ with three mandatory subsections ([State], [Execution Trace], [Violation]), a repair rationale block ⟨reasoning⟩, and a single rust code block containing the repaired program."

**User message (App. D.1, p.21; full text in `examples/paper-appD-prompts.txt`):**
```
Respond with these sections in order:
1. <counterexample> with [State], [Execution Trace], [Violation]
2. <reasoning> with a concise repair plan
3. A single ```rust ... ``` block with the complete fixed program
```

**Released code system prompt** (repo:topoverus/data.py:22-26, verbatim; this is also the HF model-card prompt):
```
You are a Verus formal-verification expert. Repair only proof annotations. Preserve executable code, function contracts and specification functions. Respond with <think>...</think>, <counterexample> containing [State], [Execution Trace] and [Violation], <reasoning>...</reasoning>, then exactly one final Rust code fence. Do not use assume or admit.
```

**SFT target assembly** (repo:topoverus/code.py:54,59, verbatim): `parts.append(f"<{tag}>\n{text}\n</{tag}>")` for think, counterexample and reasoning, then `parts.append(f"```rust\n{final_code(response)}\n```")`.

**Screen-ready filled template:** `examples/trajectory-template-SCREEN.txt`. It is built from Case B's verbatim pieces, and every elision is listed in its header.

## 7. Limitations

From the paper (p.10, Discussion):
1. **Loop invariants only.** The dependency curriculum targets loop invariants and does not cover assertions or other proof structure.
2. **No guarantee on counterexample validity.** "Exact reachability checking is fundamentally challenging and often infeasible". The model "may occasionally hallucinate imprecise execution traces that provide ambiguous guidance." Table 2's claim is described as "conservative": the diagnostics "need not be independently formal certificates" (p.8).

From the results and the checklist:

3. **Systems code.** On VeruSAGE, closed models remain far ahead (Table 1).
4. **Diversity.** CTX-Dep is slightly less diverse than CTX-Binary (Table 6, p.19).
5. **No error bars or seeds**, because RL runs are expensive (Checklist Q7, p.25).

Our own observations:

6. **Reward needs references.** The graph needs a verified reference proof per training program, so R_dep is a training-only signal.
7. **The matcher is lexical.** Token-set Jaccard, not semantics (repo:matcher_v2.py docstring "Lexical one-to-one invariant matching, not semantic equivalence").
8. **Graph scope.** The released graph builder handles only the *first* invariant block (repo:matcher_v2.py `first_invariants`) and only programs with ≤ 10 invariants (repo:build_graphs.py:54).
9. **Case-study verification is unrecorded** (see §5).

## 8. Continuity hooks (series: ExVerus → TopoVerus → Vero → Vekto)

- **From ExVerus.** ExVerus is cited as Yang et al. 2026b, with Sun as second author; the homepage lists it at ICML 2026. It established that counterexamples are better repair feedback than raw verifier messages. It paid for this with iterative refinement and hand-written validators at inference time (p.2, p.9). TopoVerus moves that cost into **training**: one pass, no validator, with usefulness judged by downstream repair. ObfsBench (266 problems) also comes from ExVerus (p.6). Theme line: *in ExVerus the system searches for a counterexample; in TopoVerus the model has learned to produce one.*
- **To Vero (repository scale).** Vero is cited as Ye et al. 2026, *"Vero: Can AI agents build formally verified software repositories?"* (p.14 refs). It was also accepted at NeurIPS 2026, and Sun is co-first author (homepage). TopoVerus' weakest suite is VeruSAGE, systems-level tasks from Anvil, Mimalloc and NrOS (Table 1). Its curriculum is per loop, inside one function. Repository-scale verification needs cross-function and cross-module dependencies. This is a natural "next scale up" bridge. *This framing is ours; the TopoVerus paper does not claim it.*
- **To Vekto (other languages and semantics).** Vekto is the current, unpublished project in this workspace: C-level equivalence of SIMD kernels, A (NEON) vs B (RVV), in QCP/Coq (repo AGENTS.md).
  - Its working rule (research/project-plan-20261102/LESSONS.zh-CN.md, L1 and L3): when A ≠ B yields a counterexample, decide whether it is a real input; then fix the kernel, log an upstream bug, or state an explicit spec condition.
  - The counterexample is again the bridge from failed proof to repair. It moves from Rust/Verus loop invariants to C semantics and cross-ISA equivalence.
  - The "no reward hacking" safety gate has a direct analogue: every spec weakening is marked and registered for review rather than accepted silently.
  - *Internal and unpublished; confirm wording with the author.*
- **Open bridge (paper's own words).** TopoVerus' counterexamples "transfer to separate repair policies" (Table 2, p.8). The learned diagnostician can plug into other agents, which is the hook toward agentic systems like Vero.

## 9. Paper vs. repository discrepancies (flag before scripting)

1. **R_pass.**
   - Paper: binary (p.5: "The verifier reward is binary").
   - Released `configs/reward.json`: `"verus_mode": "fraction"`, which gives partial credit verified/(verified+errors) (repo:reward.py:75-76).
2. **Dependency-graph construction.**
   - Paper: inductive-subset enumeration, Defs. 1–2 and Alg. 1, budget 256, n ≤ 16.
   - Repo `build_graphs.py` ("builder_version": "inductive-v2.0"): **leave-one-out**. It removes each invariant in turn and adds edges removed→target for every invariant that then fails "not satisfied / not maintained" (lines 69-78). It caps programs at 10 invariants (line 54); graph.py comments "Graphs contain at most ten nodes".
3. **Prompt.** Paper App. D's system prompt (fix-pattern list) differs from the repo/HF system prompt, which adds "Do not use assume or admit".
4. **Data counts.**
   - Paper: 461 SFT trajectories and 471 test problems.
   - Repo: SFT raw file has 1,210 rows (filtered by data.py; the resulting count is not recorded in the repo), and the evaluation file has 472 rows (configs/data-inputs.json).
   - Not reconciled.
5. **Teacher provenance.**
   - Paper: Sonnet 4.6 (p.6).
   - repo:data.py:246: `"sft_generation": "inherited_legacy_trajectories; teacher-model provenance absent in source rows"`.
6. **Case-study pages.** Repo README/sources.json say App. B pages 15/16/17. In the arXiv PDF, Cases A and B are on p.17 and Case C is on p.18.
7. **Case B display.** The paper's Fig. 4 is condensed: `price`, 3 invariants, error at line 37. The artifact has `prices`, 6 invariants, error at line 44, and an extra postcondition.
8. **Project page.** It lists Paper, GitHub and HF as "Coming soon", although both repo and weights are live (fetched 2026-11-23).
9. **HF metadata.** It shows "33B params" (auto-count), while the name and paper say 32B.

## 10. Author homepage summary (for the series intro)

Source: etha-sun.github.io, fetched 2026-11-23; quoted from page text.
- **Who:** "a senior undergraduate at the School of the Gifted Young, University of Science and Technology of China, majoring in Data Science and Big Data Technology." Based in Berkeley.
- **Advisors:** "Prof. Kexin Pei (University of Chicago) and Prof. Alvin Cheung (University of California, Berkeley)."
- **Interests:** language models and formal verification.
- **Internships:**
  - UChicago with Kexin Pei, 2025.07–09 and 2026.07–09.
  - UC Berkeley Sky Lab with Alvin Cheung, 2026.09–present.
- **Publications in this series:**
  - TopoVerus (first author, NeurIPS 2026).
  - Vero (co-first author with Zhe Ye and Hantao Lou, NeurIPS 2026).
  - ExVerus (second author; first author Jun Yang; ICML 2026).
- **Other publications:**
  - PURE (under review, 2026).
  - Mobile-AI model-update work (ANAI@MobiCom 2025).
  - Multimodal RAG for archaeology (ArtMetrics@ICCV 2025).
- **Honors:**
  - National Scholarship (2026.09).
  - Tsung-Dao Lee Scholarship (2026.06).
  - SGY Class of 87 Innovation Scholarship (2026.01).
  - Yanbao Scholarship (2025.10).
  - ICPC and CCPC Silver (2024).
  - CMO First Prize (2022).
- **Small inconsistency:** the homepage's ExVerus author list omits Jianan Yao. TopoVerus' reference list includes him (p.14).

## 11. Glossary

- **Verus:** a verifier for Rust. Proofs are written as ghost annotations (requires/ensures, loop invariants, asserts) and discharged to SMT solvers (p.3).
- **Proof annotation / ghost code:** text that only the verifier sees. Repairs may change only this.
- **Loop invariant:** a property true at the start of every loop iteration. It must hold on entry (base case) and be preserved by the body (inductiveness) (p.3).
- **Inductive subset:** a set of invariants whose conjunction is established and preserved on its own (Def. 1).
- **Dependency graph / SCC / condensation:** v_j → v_i if v_j is in every inductive subset containing v_i. Cycles are mutually inductive groups; condensing them yields a DAG (Defs. 2–3).
- **Counterexample (σ, τ, ψ):** a concrete state where the obligation's antecedent holds and the consequent fails, plus a trace and a violation explanation (Eq. 1).
- **SFT:** supervised fine-tuning on teacher trajectories.
- **GRPO:** Group Relative Policy Optimization. An RL algorithm that compares several sampled responses (8 here) per prompt.
- **RLVR:** RL with verifiable rewards; here the reward comes from Verus (p.2).
- **Lynette:** an AST-level checker (from AutoVerus) that confirms only proof annotations changed.
- **Safe-Pass@k:** a problem counts as solved if any of k independent repair chains (each up to 10 iterations) yields a program that verifies *and* passes Lynette (p.6).
- **Micro vs. macro average:** per-problem vs. per-suite averaging (App. C.1).
- **CoT-Init / CTX-Init / CTX-Binary / CTX-Dep:** the ablation ladder (p.6); CTX-Dep is TopoVerus.
- **Micro-curriculum:** easy-to-hard ordering *inside a single response* (p.10), as opposed to ordering of training data.
- **Reward hacking:** gaining reward without solving the task, here by changing code or specs to pass the verifier.

## 12. Open questions

1. Do `examples/caseB-4-repaired-program.rs` and `caseB-6-minimal-repair-DERIVED-UNVERIFIED.rs` pass Verus `0.2025.07.12.0b6f3cb`, the version named in the repo README? This blocks the "→ verified" shot.
2. Which graph builder produced the paper's training graphs: Alg. 1 (subset enumeration) or the released leave-one-out builder? Do the paper's numbers use binary or fraction R_pass? Ask the author.
3. What are the exact dependency edges for the binary-search example? Our illustrative edge set should be confirmed, or the paper's Fig. 2 graph read off precisely.
4. How often did the safety gate fire during RL? Is there a recorded *model* rollout that was verified-but-unsafe? That would make a stronger on-screen example than the unit tests.
5. How do 1,210 raw SFT rows reduce to 461, and why are there 472 evaluation rows versus 471 problems?
6. Did RL rollouts receive verifier errors in the prompt? `prompt(code, errors)` supports it, and the paper says each step gets "the failed proof and Verus feedback" (p.6).
7. For the Vekto hook: may internal, unpublished project details appear in a public video?
