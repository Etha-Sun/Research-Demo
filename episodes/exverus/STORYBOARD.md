# ExVerus — storyboard

Video key `exverus`, scene prefix `ExV`, 12 scenes, 45 beats, about 7.1 min of narration at the spec's words/2.6 + 0.5 s estimate
(the exact length is set later by `tools/sync_durations.py`). Paper: *ExVerus: Verus Proof Repair via Counterexample Reasoning*,
Yang, Sun, Wu, Caridad, Yuan, Yao, Lu, Pei, ICML 2026 (arXiv 2603.25810v2). All page numbers are PDF pages.
Narration below is copied from `narration.json` (the single source of truth).

## 1. ExV01Title  (~7 s)

**Purpose.** Open the video: title, subtitle, authors and venue.

**On screen.** title_card('exverus') with the author list and 'ICML 2026'.

**Code panels.** none

**Citations.** Author list and venue: paper p.1.

**Narration.**

- `exv01-1` (7.0 s)
  - en: ExVerus: Verus proof repair via counterexample reasoning, by Jun Yang, Yuechun Sun and colleagues, at ICML 2026.
  - zh: ExVerus：基于 counterexample 推理的 Verus 证明修复。作者是 Jun Yang、孙悦淳等人，发表于 ICML 2026。

## 2. ExV02ColdOpen  (~51 s)

**Purpose.** Hook: a real Verus failure whose error says where, not why; Verus's own SMT model is useless; ExVerus's source-level counterexample makes it concrete.

**On screen.** Left: findmax code panel, invariants boxed (lines 8–11), then failing line 11 boxed red; right: 3-line error text + 'where — but why?'. Beat 3: right side becomes 'Verus's own model (Z3)' panel (unknown / i@ 537 / 1681 / Poly!val!31 boxed) + badges '7,083-line SMT query', 'answer: unknown'. Beat 4: raw panel replaced by state_table CEX_1 (nums=vec![-1,-1], i=1, max=0), 'Status: SAT', 'max' row boxed red, '0 is not in [-1, -1]'. Beat 5: three-step line 'one-line error → concrete counterexamples → repaired proof'. No findmax fix is shown (the paper does not show one).

**Code panels.** examples/findmax_buggy_screen.rs (all 19 lines; highlight 8–11, then 11); examples/findmax_verus_raw_model.txt (lines 1,4,8,10 boxed); values of examples/findmax_cex.txt as a state table.

**Citations.** Fig. 1 (p.3); §2.2 (p.3–4).

**Narration.**

- `exv02-1` (11.7 s)
  - en: Here is a small Rust function checked by the Verus verifier. It finds the maximum of a vector, and its loop carries invariants: facts that hold on every pass.
  - zh: 这是一个由 Verus verifier 检查的小 Rust 函数。它求一个 vector 的最大值，循环上带着若干 loop invariant：每一轮都成立的事实。
- `exv02-2` (9.3 s)
  - en: Verus rejects the last invariant: invariant not satisfied at end of loop body. The message says where the proof broke, but not why.
  - zh: Verus 拒绝了最后一条 invariant：invariant not satisfied at end of loop body。这条消息说明了证明在哪里断掉，却没有说明为什么。
- `exv02-3` (11.7 s)
  - en: Verus compiles this proof into a 7,083-line SMT query. The solver answers unknown, and its model says i is 537 and the vector has length 1681, in internal symbols.
  - zh: Verus 把这个证明编译成 7,083 行的 SMT 查询。Solver 的回答是 unknown，它的模型说 i 是 537、vector 长度是 1681，而且用的是内部符号。
- `exv02-4` (9.3 s)
  - en: ExVerus gets this instead: nums is minus one, minus one; i is one; max is zero, a value not even in the array.
  - zh: ExVerus 得到的则是：nums 是负一、负一；i 是一；max 是零，这个值甚至不在数组里。
- `exv02-5` (8.6 s)
  - en: That is the idea of ExVerus: turn a verifier's one-line error into concrete counterexamples, and use them to repair the proof.
  - zh: 这就是 ExVerus 的核心想法：把 verifier 的一行报错变成具体的 counterexample，再用它们来修复证明。

## 3. ExV03Background  (~49 s)

**Purpose.** The concepts this video needs: requires/ensures/invariant, the two invariant obligations, VC → Z3, counterexample definition, why the solver says unknown; then ExVerus's key trick (source-level Z3Py with concretisation).

**On screen.** Beat 1: three cards requires / ensures / invariant. Beat 2: '① before the loop ② after one iteration' → 'verification condition' → 'Z3 (SMT)'. Beat 3: heading 'Counterexample', 'obligation A ⟹ C', 'counterexample σ: σ ⊨ A ∧ ¬C', note about forall/exists → unknown. Beat 4–5: Z3Py panel (left) with line 3 boxed WARN; right notes 'length fixed to 2 → no quantifiers', 'program's own names: nums, i, max'; then 'SAT → CEX_1' table and WARN badge 'not trusted until Verus checks'.

**Code panels.** examples/findmax_z3py_screen.py (15 lines; highlight line 3).

**Citations.** Def. 2.1 (p.4); §2.2 (p.3); Fig. 1 (p.3); trust statement p.2.

**Narration.**

- `exv03-1` (8.6 s)
  - en: In Verus you write Rust plus a specification: requires holds on entry, ensures holds on return, and every loop needs invariants.
  - zh: 在 Verus 中，你写的是 Rust 加上 specification：requires 在进入时成立，ensures 在返回时成立，每个循环都需要 loop invariant。
- `exv03-2` (9.7 s)
  - en: An invariant must hold before the loop and survive one iteration. Verus turns each obligation into a verification condition for the SMT solver Z3.
  - zh: 一条 invariant 必须在循环前成立，并且撑过一轮迭代。Verus 把每一项义务变成 verification condition，交给 SMT solver Z3。
- `exv03-3` (8.6 s)
  - en: A counterexample is a state that satisfies the assumptions but breaks the goal. With quantifiers, the solver often gives up instead.
  - zh: Counterexample 是一个满足前提、却违反目标的状态。公式里有 quantifier 时，solver 常常直接放弃。
- `exv03-4` (12.8 s)
  - en: ExVerus has the language model write a small Z3Py query at the source level, with the program's own names. Here it fixes the vector length to two, so no quantifiers are needed.
  - zh: ExVerus 让语言模型在源码层面写一个小的 Z3Py 查询，使用程序自己的变量名。这里它把 vector 长度固定为二，于是不再需要 quantifier。
- `exv03-5` (9.7 s)
  - en: The solver then quickly returns small, readable states. The query may even relax soundness, because nothing it produces is trusted until Verus checks it.
  - zh: 这样 solver 就能很快返回小而易读的状态。这个查询甚至可以放松 soundness，因为它产生的任何东西在 Verus 检查之前都不被信任。

## 4. ExV04Brs1Bug  (~29 s)

**Purpose.** Introduce the motivated example brs1: what the loop does, the LLM's buggy invariant, Verus's error, and why it is hard (AutoVerus failed).

**On screen.** Left: brs1 second-loop panel. Beat 1: body lines 10–14 boxed, then line 11 with note 'reset only when i == 0'. Beat 2: line 7 boxed WARN + 'LLM's invariant: sum[0] <= i'. Beat 3: line 7 turns BAD, error text 'invariant not satisfied before loop', 'AutoVerus: 16 attempts on this error, task failed'.

**Code panels.** examples/brs1_loop_screen.rs (17 lines; highlight 10–14, 11, 7).

**Citations.** Fig. 3 (p.13); App. A.1 (p.13).

**Narration.**

- `exv04-1` (11.7 s)
  - en: Now the main example, brs1 from VerusBench. A hidden first loop fills a with ones; the second adds them into sum zero, resetting it only on the first pass.
  - zh: 现在看主例子，VerusBench 里的 brs1。省略的第一个循环把 a 全部填成一；第二个循环把它们累加到 sum[0]，只在第一轮把它清零。
- `exv04-2` (7.8 s)
  - en: The language model's proof claims, as an invariant of the second loop, that sum zero is at most i.
  - zh: 语言模型给出的证明，把“sum[0] 不超过 i”作为第二个循环的 invariant。
- `exv04-3` (9.3 s)
  - en: Verus answers: invariant not satisfied before loop. The earlier tool AutoVerus spent 16 attempts on exactly this error and still failed the task.
  - zh: Verus 的回答是：invariant not satisfied before loop。之前的工具 AutoVerus 在这个错误上尝试了 16 次，最终仍然没能完成这个任务。

## 5. ExV05Brs1Cex  (~43 s)

**Purpose.** Counterexample state table next to the code; evaluate the invariant on it; then validation: the loop extracted into a harness with the invariants as assertions, CEX injected, assertion fails → validated.

**On screen.** Beat 1: code left (line 7 red), two state tables CEX_1 / CEX_2 stacked right. Beat 2: CEX_2 fades; sum and i rows flash; 'sum[0] <= i' → '1 <= 0' → 'false'. Beat 3: harness panel left; CEX_1 table top right; lines 2–5 boxed 'CEX_1 injected'; lines 7–11 boxed 'invariants → assertions'; badge 'no LLM in this step'. Beat 4: line 11 boxed red, badges 'assertion fails', 'CEX_1 validated' under the harness.

**Code panels.** examples/brs1_loop_screen.rs; examples/brs1_cex.txt (as tables); examples/brs1_harness_screen.rs (12 lines; highlight 2–5, 7–11, 11).

**Citations.** Fig. 3 (p.13) panels 2 and 5; validation procedure §3.1 (p.5).

**Narration.**

- `exv05-1` (12.8 s)
  - en: ExVerus asks the solver for states that break the invariant at loop entry: a is one, one; sum is one; i is zero; N is two. Another has sum equal to two.
  - zh: ExVerus 向 solver 要在进入循环时违反这条 invariant 的状态：a 是一、一；sum 是一；i 是零；N 是二。另一个状态中 sum 等于二。
- `exv05-2` (12.0 s)
  - en: Plug in the first: sum zero is one, i is zero, and one is not at most zero. At loop entry, sum zero still holds whatever the caller passed in.
  - zh: 代入第一个：sum[0] 是一，i 是零，而一并不小于等于零。进入循环时，sum[0] 仍是调用者传进来的任意值。
- `exv05-3` (10.5 s)
  - en: But the language model could be wrong. So a validator without any language model extracts the loop, turns the invariants into assertions, and injects the counterexample.
  - zh: 但语言模型也可能出错。所以一个不涉及语言模型的 validator 把循环抽取出来，把 invariant 变成 assertion，并注入 counterexample。
- `exv05-4` (7.8 s)
  - en: Verus runs it. The last assertion fails, the same symptom as the real error, so this counterexample is validated.
  - zh: Verus 运行它。最后一条 assertion 失败，和真实错误的症状一致，因此这个 counterexample 通过了验证。

## 6. ExV06Triage  (~38 s)

**Purpose.** Explain reachable vs spurious and the two verdicts; show the real brs1 diagnosis (wrong_fact); contrast with findmax (too_weak).

**On screen.** Beat 1–2: two cards 'reachable' (BAD) / 'spurious' (WARN) with consequences 'wrong_fact → replace' / 'too_weak → strengthen'. Beat 3: JSON diagnosis panel left, verdict line and 'i=0 and sum[0] is positive … reachable' lines boxed; right card 'brs1: reachable, wrong_fact → replace'. Beat 4: second card 'findmax (cold open): max = 0 never occurs for [-1, -1]: spurious, too_weak → strengthen'.

**Code panels.** examples/brs1_triage.json (rationale wrapped; highlight 2, 4–5).

**Citations.** §3.2 (p.5); Fig. 3 (p.13); Fig. 8 (p.23).

**Narration.**

- `exv06-1` (7.4 s)
  - en: Next, triage. A counterexample can be reachable by a real run, or spurious: no run ever reaches it.
  - zh: 接下来是 triage。一个 counterexample 可能是 reachable 的，即真实运行能到达；也可能是 spurious 的，即任何运行都到达不了。
- `exv06-2` (9.7 s)
  - en: Reachable means the invariant is wrong and must be replaced. Spurious means it may be true but too weak, so it must be strengthened.
  - zh: Reachable 说明 invariant 是错的，必须替换。Spurious 说明它可能是对的但太弱，必须加强。
- `exv06-3` (10.9 s)
  - en: For brs1 the verdict is wrong fact: the invariant fails at loop entry when i is zero and sum zero is positive, and those states are reachable.
  - zh: 对 brs1，判定是 wrong_fact：当 i 为零且 sum[0] 为正时，invariant 在进入循环前就不成立，而这些状态是可达的。
- `exv06-4` (9.7 s)
  - en: For findmax the verdict went the other way: max equal to zero cannot occur, so the states were spurious and the invariants too weak.
  - zh: 而对 findmax，判定正好相反：max 等于零不可能出现，所以这些状态是 spurious 的，invariant 太弱。

## 7. ExV07Repair  (~43 s)

**Purpose.** Mutation and ranking by #CEX blocked; transform the failing line into the fixed line; re-run the harness (blocking); the repair verifies.

**On screen.** Beat 1: heading 'Mutate: candidate proofs (replacing mutator)', '5 candidates by default', badge with the shared CEX pattern, one card mutant_1 'i > 0 ==> sum[0] <= i as i32' (Fig. 3 shows only mutant_1). Beat 2: 'rank = # validated counterexamples blocked', definition of blocked, badge 'mutant_1 blocks all CEXs', 'inspired by PDR'. Beat 3: brs1 code; line 7 morphs from buggy to fixed (red box → green box); diff panel at right. Beat 4: harness with the buggy assertion (red) morphs into mutant_1's assertion (green); 'assertion passes: CEX_1 blocked'. Beat 5: green card 'mutant_1 blocks all CEXs / passes Verus / task solved'.

**Code panels.** examples/brs1_loop_screen.rs → examples/brs1_loop_fixed_screen.rs (line 7); examples/brs1_patch.diff; examples/brs1_harness_screen.rs → examples/brs1_harness_blocking_screen.rs (line 11).

**Citations.** §4.1 (p.6, 5 mutants); p.6 'Mutant ranking'; Fig. 3 and App. A.1 (p.13).

**Narration.**

- `exv07-1` (11.3 s)
  - en: Guided by the verdict, a replacing mutator proposes candidate proofs, five by default. It targets the pattern the counterexamples share: i is zero and sum zero is positive.
  - zh: 根据这个判定，一个替换型 mutator 提出若干候选证明，默认五个。它针对这些 counterexample 的共同模式：i 为零，sum[0] 为正。
- `exv07-2` (10.9 s)
  - en: Candidates are ranked by how many validated counterexamples they block, meaning how many no longer trigger the failure. This ranking is inspired by the model-checking algorithm PDR.
  - zh: 候选证明按照它们 block 了多少个经过验证的 counterexample 来排序，也就是有多少个 counterexample 不再触发失败。这种排序受 model checking 算法 PDR 启发。
- `exv07-3` (8.6 s)
  - en: The top candidate, mutant one, guards the invariant: if i is greater than zero, then sum zero is at most i.
  - zh: 排名第一的候选，mutant_1，给 invariant 加上了条件：如果 i 大于零，那么 sum[0] 不超过 i。
- `exv07-4` (7.4 s)
  - en: Run the validation harness again with the new invariant: the assertion now passes, so counterexample one is blocked.
  - zh: 用新的 invariant 再运行一次 validation harness：assertion 现在通过了，所以第一个 counterexample 被 block 了。
- `exv07-5` (5.1 s)
  - en: Mutant one blocks all the counterexamples and passes Verus, solving the task.
  - zh: mutant_1 block 了所有 counterexample，并通过了 Verus 验证，从而解决了这个任务。

## 8. ExV08Architecture  (~57 s)

**Purpose.** The method as one diagram (Fig. 2 / Alg. 1–3), built step by step, then brs1 flows through it with pulse_path; end on the trust point.

**On screen.** Nodes: Proof + Verus → Generate (LLM → Z3Py → CEXs; '≤ 10 CEXs; retry if not SAT') → Validate (Verus, extracted loop) → Triage (wrong_fact / too_weak) → Mutate & rank (5 candidates, # CEX blocked) → Verus (check candidates) → Verified; WARN curved arrow Verus → Proof 'still failing: next iteration (max 10)'. Beats 5–6: each node pulses in turn while a caption under the diagram shows brs1's data at that node (last two captions: 'mutant_1 blocks all CEXs', 'passes Verus'). Beat 7: LLM nodes flash accent ('LLM proposes'); Verus nodes turn OK ('only Verus decides').

**Code panels.** none

**Citations.** Fig. 2 (p.4); Alg. 1–3 (p.19); §4.1 (p.6: 5 mutants, max 10 iterations); §4.3 (p.7: default 10 CEXs); brs1 data from Fig. 3 / App. A.1 (p.13).

**Narration.**

- `exv08-1` (7.0 s)
  - en: Here is the whole method. It starts from the language model's proof and the error Verus reports.
  - zh: 下面是整个方法。它从语言模型写的证明和 Verus 报告的错误开始。
- `exv08-2` (8.6 s)
  - en: Generate: the model writes a Z3Py query and enumerates counterexamples, ten by default, retrying when the solver does not say SAT.
  - zh: Generate：模型写出 Z3Py 查询并枚举 counterexample，默认十个；solver 没有返回 SAT 时就重试。
- `exv08-3` (10.1 s)
  - en: Validate: Verus runs each counterexample in the extracted loop; only those that reproduce the error survive. Triage labels the failure wrong fact or too weak.
  - zh: Validate：Verus 在抽取出的循环里运行每个 counterexample，只有能复现错误的才保留。Triage 把失败归类为 wrong fact 或 too weak。
- `exv08-4` (9.7 s)
  - en: Mutate and rank: five candidates, scored by the counterexamples they block. Verus checks them; if none passes, the loop repeats, up to ten iterations.
  - zh: Mutate and rank：五个候选，按 block 的 counterexample 数打分。Verus 检查它们；如果都没通过就再走一轮，最多十轮。
- `exv08-5` (10.5 s)
  - en: Follow brs1 through it. The invariant fails before the loop; the solver finds states with i zero and sum positive; Verus confirms they reproduce the error.
  - zh: 让 brs1 走一遍。Invariant 在循环前失败；solver 找到 i 为零、sum 为正的状态；Verus 确认它们能复现这个错误。
- `exv08-6` (6.3 s)
  - en: Triage says wrong fact; the guarded invariant blocks the counterexamples; and Verus accepts the proof.
  - zh: Triage 判定为 wrong fact；加了条件的 invariant block 了这些 counterexample；Verus 接受了这个证明。
- `exv08-7` (5.1 s)
  - en: The language model proposes counterexamples, verdicts and repairs, but only Verus decides.
  - zh: 语言模型负责提出 counterexample、判定和修复，但只有 Verus 做最终决定。

## 9. ExV09Results  (~36 s)

**Purpose.** Main results, per table and model setting only (numbers policy).

**On screen.** Beat 1–2: grouped bars (ExVerus / AutoVerus / Iterative Refinement) for VerusBench, DafnyBench, LCBench, HumanEval with Claude-Sonnet-4.5; LCBench+HumanEval boxed WARN 'harder benchmarks: below 50%'. Beat 3: DeepSeek-V3.1 VerusBench bars 71.9 / 24.7 / 60.3. Beat 4: ObfsBench range bars on a 0–100% axis: ExVerus 73.9–86.5%, AutoVerus 24.7–36.5% (DeepSeek-V3.1, 6 strategies).

**Code panels.** none

**Citations.** Table 1 (p.7); Table 2 (p.7); ObfsBench size p.6.

**Narration.**

- `exv09-1` (8.6 s)
  - en: Now the results. Table 1 compares ExVerus with AutoVerus and plain iterative refinement on four benchmarks, here with Claude Sonnet 4.5.
  - zh: 接下来看结果。Table 1 在四个 benchmark 上比较 ExVerus、AutoVerus 和简单的 iterative refinement，这里是 Claude Sonnet 4.5 的结果。
- `exv09-2` (9.7 s)
  - en: ExVerus leads on VerusBench, LCBench and HumanEval, and all three tie on DafnyBench. On the harder LCBench and HumanEval, success stays below one half.
  - zh: ExVerus 在 VerusBench、LCBench 和 HumanEval 上领先，三者在 DafnyBench 上打平。在更难的 LCBench 和 HumanEval 上，成功率仍不到一半。
- `exv09-3` (9.3 s)
  - en: With a weaker model, DeepSeek V3.1, the gap on VerusBench widens: 71.9 percent for ExVerus, 24.7 for AutoVerus, and 60.3 for iterative refinement.
  - zh: 换成较弱的模型 DeepSeek V3.1，VerusBench 上的差距变大：ExVerus 是 71.9%，AutoVerus 是 24.7%，iterative refinement 是 60.3%。
- `exv09-4` (8.2 s)
  - en: On ObfsBench, the same tasks obfuscated six ways, ExVerus with DeepSeek scores 73.9 to 86.5 percent; AutoVerus, 24.7 to 36.5.
  - zh: 在 ObfsBench 上，同样的任务用六种方式混淆。使用 DeepSeek 时，ExVerus 的成功率在 73.9% 到 86.5% 之间，AutoVerus 在 24.7% 到 36.5% 之间。

## 10. ExV10Evidence  (~34 s)

**Purpose.** Why it works and what it costs: ablation, blocking as a predictor, cost per model.

**On screen.** Beat 1: bars ExVerus 81.6 vs ExVerus_NO_MUT 65.4 (ObfsBench, DeepSeek-V3.1). Beat 2: two cards 70.78% (172/243) vs 24.84% (38/153). Beat 3: small table cost/time per task for DeepSeek-V3.1 and GPT-4o, note 'cost depends on the model'.

**Code panels.** none

**Citations.** Table 4 (p.8); §4.3 (p.8); Table 3 (p.8).

**Narration.**

- `exv10-1` (11.3 s)
  - en: Do the counterexamples matter? A variant that hands them straight to the model, without mutators or validation, reaches 65.4 percent on ObfsBench with DeepSeek. Full ExVerus reaches 81.6.
  - zh: Counterexample 真的有用吗？一个把 counterexample 直接交给模型、不用 mutator 也不做 validation 的变体，在 DeepSeek 和 ObfsBench 上达到 65.4%，完整的 ExVerus 是 81.6%。
- `exv10-2` (10.1 s)
  - en: And blocking predicts success. With one counterexample per repair, 172 of 243 mutants that block it verify, against 38 of 153 mutants that block nothing.
  - zh: 而且 block 能预测成功。每次修复只用一个 counterexample 时，block 了它的 243 个 mutant 中有 172 个通过验证；而什么都没 block 的 153 个 mutant 中只有 38 个通过。
- `exv10-3` (12.4 s)
  - en: Cost depends on the model. With DeepSeek V3.1, a task costs 4 cents instead of 17 and takes 720 seconds instead of 2989. With GPT-4o, it costs 42 cents against 69.
  - zh: 成本取决于模型。使用 DeepSeek V3.1 时，每个任务 4 美分而不是 17 美分，耗时 720 秒而不是 2989 秒。使用 GPT-4o 时是 42 美分对 69 美分。

## 11. ExV11Limits  (~18 s)

**Purpose.** The limitations the paper states.

**On screen.** Heading 'Limitations'; four bullets (two per beat), each with its locator under it: validation covers loop-invariant errors only; other errors: counterexamples are unvalidated hints; weaker on asserts / proof blocks (GPT-4o); passing Verus ≠ the spec matches the user's intent.

**Code panels.** none

**Citations.** §3.1 (p.5); §5 (p.8); Table 5 (p.23); Impact Statement (p.9).

**Narration.**

- `exv11-1` (8.2 s)
  - en: The paper also states its limits. Counterexample validation covers loop invariant errors; for other errors, the counterexamples are unvalidated hints.
  - zh: 论文也说明了它的局限。Counterexample validation 只覆盖 loop invariant 错误；对其他错误，counterexample 只是未经验证的提示。
- `exv11-2` (10.1 s)
  - en: ExVerus is weaker on proofs that need assertions or proof blocks. And passing Verus does not show that the specification matches what the user intended.
  - zh: ExVerus 在需要 assertion 或 proof block 的证明上较弱。而且通过 Verus 并不说明 specification 符合用户的本意。

## 12. ExV12Takeaway  (~20 s)

**Purpose.** ExVerus's own takeaway.

**On screen.** Beat 1: 'failed proof → counterexamples → repair ranked by CEXs blocked → Verus re-check'. Beat 2: three lines: 'concrete program states, not one-line errors', 'open-ended proof search → targeted search', 'Verus has the final word'.

**Code panels.** none

**Citations.** App. A.2 (p.14: 'converts debugging into a targeted search'); §7 Conclusion (p.9: 'transforms open-ended proof search into more grounded process').

**Narration.**

- `exv12-1` (8.6 s)
  - en: To sum up: ExVerus makes the counterexample the unit of feedback, and scores every repair by the counterexamples it rules out.
  - zh: 总结一下：ExVerus 把 counterexample 当作反馈的基本单位，并用一个修复排除了多少 counterexample 来给它打分。
- `exv12-2` (11.3 s)
  - en: Instead of a one-line error, the model sees concrete program states. Blocking them turns open-ended proof search into a targeted search, and Verus still has the final word.
  - zh: 模型看到的不再是一行报错，而是具体的程序状态。Block 这些状态，把开放式的证明搜索变成有针对性的搜索，而最终的判定仍然由 Verus 做出。

## Open issues

1. **Paper numbers re-checked (final review, 2026-11-23)** against `papers/exverus.pdf` via pypdf: Table 1 (Sonnet-4.5,
   DeepSeek-V3.1), Table 2 (DeepSeek ranges), Table 3, Table 4 and the p.8 blocking counts all match. See `docs/REVIEW.md`.
2. **ExVerus_NO_MUT label (resolved).** Table 4's caption is "Ablation study on mutation strategies"; §4.2 (p.7) defines
   the baseline as one that "instructs the LLM to directly fix the proof based on the counterexamples without validation".
   Screen and narration now say: counterexamples go straight to the LLM, no error-specific mutators, no validation.
3. **Validation 'after' assertion.** Fig. 3 shows only the base-case ('before') harness; the narration describes only that
   part. The InvFailEnd ('after one iteration') variant is mentioned only in general terms (scene 3 beat 2).
4. **Number of brs1 counterexamples** is not given (the figure shows CEX_1, CEX_2, '......'); the screen says 'all CEXs'.
5. **Fig. 2 simplifications.** The diagram omits the compilation fixer (Alg. 1), the third triage verdict `other`, and the
   fact that non-invariant errors skip validation (shown in Limitations instead). The 'Verified' node is our addition for the
   pass edge of Alg. 3.
6. **Not used on purpose (numbers policy):** '38% more on average', '+60.92%', '+45%', '64.49%', the bare '$0.04 per task',
   project-page numbers.
7. **Local helpers to consider lifting into common/:** `grouped_bars` (multi-series horizontal bars; `bar_chart` is
   single-series), `range_row` (min–max span on a 0–100 axis), and the `ex()` loader that reads the part of an
   `examples/` file below the `---- on screen below ----` marker.
8. `pulse_path` leaves boxes in the pulse colour; scene 8 restores each box's original stroke colour after the pulse.
   Lifting that restore into `pulse_path` would help other episodes.

## Revision 2026-11-23

Per docs/REVISION-BRIEF.md (author feedback: self-contained video, no defensive labels, paper first).

- Removed ExV01SeriesIntro (four-part series intro, series map, author card) and ExV12Bridge (bridge to the next
  video, series map). New ExV01Title: title card with authors and venue, no episode number; the findmax cold open follows.
- New closing scene ExV12Takeaway: one-line method summary plus ExVerus's own takeaway (App. A.2, §7).
- ExV07: the four greyed 'not shown in the paper' mutant cards are gone; only mutant_1 is shown, as in Fig. 3, with
  '5 candidates by default' (§4.1). Dropped the repo-only 'reference proof uses the same guard' card (not in the paper).
- Removed hedges: 'paper reports' (exv04-3, exv07-5, exv08-6 and on-screen captions in ExV07/ExV08), '(paper, p.13)'
  badges, 'this episode'. 'idea from PDR / IC3' → 'inspired by PDR' (p.6 wording).
- ExV11: 'What the paper does not claim' → 'Limitations', two beats, four items; dropped the AutoVerus Verus-version
  item and the 'CEX generation can fail' item (the trust point stays in ExV08 beat 7).
- Narration trimmed throughout (ExV02–ExV10) for length: 8.9 → about 7.1 min, 49 → 45 beats. zh text updated to match.
