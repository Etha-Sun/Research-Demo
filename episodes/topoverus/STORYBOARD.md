# TopoVerus (Episode 2) storyboard

Paper: *Curriculum Proof Repair with Learned Counterexamples*, Yuechun Sun, Jun Yang, Kexin Pei, NeurIPS 2026 (arXiv 2611.13627v1). Code: github.com/Etha-Sun/Topoverus @ 8784962. Page numbers are PDF pages. Narration below is copied from narration.json (the source of truth); durations are words/2.6 + 0.5 s estimates.

## 1. Topo01Map  (~19 s)

**Purpose.** Series map with tile 2 lit; recap of ExVerus (SERIES.md fixed line); title card with authors and venue.

**On screen.** Beat 1: series_map('topoverus') centred, recap line above it. Beat 2: map fades; title_card (Episode 2, TopoVerus, subtitle) with 'Yuechun Sun, Jun Yang, Kexin Pei · NeurIPS 2026' and the episode question in the accent colour, centred.

**Code panels.** none

**Citations.** Attribution per docs/SERIES.md; paper p.1.

**Narration.**

- `Topo01Map-1` (6.7 s)
  - en: Last time, ExVerus showed that a concrete counterexample is better feedback than a verifier's one-line error.
  - zh: 上一集，ExVerus 告诉我们：一个具体的 counterexample，比 verifier 的一行报错更有用。
- `Topo01Map-2` (12.0 s)
  - en: This is episode two: TopoVerus, by Sun, Yang and Pei, at NeurIPS 2026. Its question is whether a model can learn to produce that counterexample itself, in a single pass.
  - zh: 这是第二集：TopoVerus，作者 Sun、Yang 和 Pei，发表于 NeurIPS 2026。它要回答的问题是：模型能否学会自己写出这个 counterexample，而且一次生成就完成。

## 2. Topo02Hook  (~46 s)

**Purpose.** Hook: a concrete failing proof (Case B, LeetCode 121) and Verus's one-line error that names the obligation but not the cause.

**On screen.** Left: code panel (rust, no line numbers). Box moves ensures (screen lines 4-5, INFO) -> loop (10-19) -> buggy invariant (14-15, WARN). Right: 'Verus output' terminal card (red border) with the two verbatim lines; the box turns red and an arrow joins card and line. Right-bottom: 'Which state breaks it? Why?' in accent.

**Code panels.** examples/caseB-loop-SCREEN.rs (trim of repo buggy.rs:24-52, see header); examples/caseB-verifier-error.txt (verifier-error.txt:2-3).

**Citations.** Case B repo files; TopoVerus Fig. 4 p.9.

**Narration.**

- `Topo02Hook-1` (13.2 s)
  - en: Here is a Verus proof for LeetCode 121, best time to buy and sell a stock. The postcondition says the result beats every pair of a buy day and a later sell day.
  - zh: 这是 LeetCode 121“买卖股票的最佳时机”的一个 Verus 证明。后置条件说：对任意一个买入日和之后的卖出日，结果都不小于它们的差价。
- `Topo02Hook-2` (11.7 s)
  - en: The loop tracks the cheapest price so far and the best profit so far. Its last invariant claims that no pair of days in the whole array beats max_pro.
  - zh: 循环维护到目前为止的最低价和最大利润。最后一条 loop invariant 声称：整个数组里任何一对日子的差价都不超过 max_pro。
- `Topo02Hook-3` (9.0 s)
  - en: Verus rejects the proof with one line: invariant not satisfied before loop. It names the failed obligation, but not why it fails.
  - zh: Verus 只用一行拒绝了这个证明：invariant not satisfied before loop。它指出了哪个证明义务失败，却没有说为什么失败。
- `Topo02Hook-4` (11.7 s)
  - en: A repair model that sees only this line has to guess. To fix the proof reliably, it should first explain the failure: which state breaks the invariant, and why.
  - zh: 只看到这一行的修复模型只能去猜。要可靠地修好证明，它应该先解释失败：哪个程序状态破坏了 invariant，以及为什么。

## 3. Topo03Background  (~42 s)

**Purpose.** Only the background needed: loop invariant = holds before the loop + preserved; counterexample = (state, trace, violation); ExVerus vs TopoVerus; usefulness defined by downstream repair.

**On screen.** Beat 1: two boxes 'Before the loop' -> 'Every iteration'. Beat 2: three red cards [State] σ / [Execution Trace] τ / [Violation] ψ under the word 'counterexample'. Beat 3: ExVerus card (ExVerus accent) -> TopoVerus card (accent). Beat 4: WARN line 'the model's counterexample is not checked by a solver' + abstract quote card.

**Code panels.** none

**Citations.** Eq. 1 and §3.1 p.4-5; §1 ¶4-5 p.2; Abstract p.1 (quote verbatim).

**Narration.**

- `Topo03Background-1` (7.4 s)
  - en: A loop invariant must hold before the loop starts, and every iteration must preserve it. Verus checks both.
  - zh: loop invariant 必须在循环开始前成立，并且每次迭代都要保持它。Verus 会检查这两点。
- `Topo03Background-2` (12.4 s)
  - en: A counterexample makes a failure concrete. TopoVerus writes it in three parts: a program state where the obligation fails, an execution trace from that state, and the violation in plain words.
  - zh: counterexample 让失败变得具体。TopoVerus 把它写成三部分：一个让证明义务失败的程序状态，从这个状态出发的执行轨迹，以及用自然语言说明的违反原因。
- `Topo03Background-3` (12.0 s)
  - en: ExVerus searched for such counterexamples and validated them at every repair, which costs inference time. TopoVerus moves that work into training, so the model writes the counterexample in one pass.
  - zh: ExVerus 在每次修复时都要搜索并验证 counterexample，这会消耗推理开销。TopoVerus 把这部分工作挪到训练阶段，让模型一次就写出 counterexample。
- `Topo03Background-4` (10.1 s)
  - en: No solver checks the model's counterexample. In the paper's words, it is useful when conditioning on it helps the model produce a safe, verifier-passing proof.
  - zh: 模型写出的 counterexample 不经过任何 solver 检查。用论文的话说：如果以它为条件能帮助模型写出安全且通过 verifier 的证明，它就是有用的。

## 4. Topo04Format  (~27 s)

**Purpose.** The one-trajectory output format verbatim (BRIEF §6, App. D.1), then filled with Case B's recorded output.

**On screen.** Beats 1-2: prompt panel (verbatim App. D.1, 4 lines); lines 2/3/4 get coloured bars (BAD / INFO / accent) as narration names each section; note '(a free <think> block may come first)' (App. D p.20). Beat 3: three panels in recorded order, '1 · counterexample' (red), '2 · rationale' (blue), '3 · repaired proof' (accent), with arrows; header 'recorded TopoVerus output for Case B (released case study)'.

**Code panels.** examples/appD-output-format.txt (verbatim); examples/caseB-trajectory-filled-SCREEN.txt (three sections; trims listed in its header).

**Citations.** App. D.1 p.21, App. D p.20; repo model-output.txt.

**Narration.**

- `Topo04Format-1` (6.7 s)
  - en: Every TopoVerus response has the same shape. The paper's prompt asks for three sections, in order.
  - zh: TopoVerus 的每个回答都有相同的结构。论文的 prompt 要求按顺序给出三个部分。
- `Topo04Format-2` (9.7 s)
  - en: First a counterexample, with State, Execution Trace and Violation. Then a concise repair plan. Then a single Rust block with the complete repaired program.
  - zh: 先是 counterexample，包含 State、Execution Trace 和 Violation；然后是简洁的修复计划；最后是一个 Rust 代码块，给出完整的修复后程序。
- `Topo04Format-3` (10.5 s)
  - en: Here is that format filled in by TopoVerus for our max-profit proof, as recorded in the released case study. We will read it piece by piece.
  - zh: 这是 TopoVerus 针对我们的最大利润证明填写的结果，来自公开的 case study 记录。我们逐段来看。

## 5. Topo05Counterexample  (~37 s)

**Purpose.** Read the counterexample against the code: state as a state_table next to the code, the (j,k) instantiation on the array, the false inequality, the cause.

**On screen.** Left: same code panel. Right column: state_table '[State] before the loop' (prices, i, max_pro, min_price; red border); boxes on init lines 8-9 then buggy lines 14-15; array cells 5|3|7 with indices and j/k pointers (cells 0 and 2 turn red); 'prices[2] - prices[0] = 7 - 5 = 2'; '2 <= max_pro = 0 : false' (red); 'range = the whole array, but nothing is processed yet' replaced by 'cause: quantifier range is too wide' (accent).

**Code panels.** examples/caseB-loop-SCREEN.rs.

**Citations.** model-output.txt:2-17; Fig. 4 p.9. Values: i = 0 from the paper's Fig. 4 [State] ('i = 0') and model-output.txt:8 ('i = 0').

**Narration.**

- `Topo05Counterexample-1` (8.6 s)
  - en: The state: prices is five, three, seven. Before the loop, i is zero and max_pro is zero. All input bounds hold.
  - zh: 状态：prices 是 5、3、7。循环开始前，i 为 0，max_pro 为 0。所有输入范围条件都满足。
- `Topo05Counterexample-2` (9.7 s)
  - en: The trace: Verus checks the invariant at loop entry. Take j equal to zero and k equal to two. Seven minus five is two.
  - zh: 轨迹：Verus 在进入循环时检查 invariant。取 j 等于 0、k 等于 2，7 减 5 等于 2。
- `Topo05Counterexample-3` (11.3 s)
  - en: The violation: the invariant demands that two is at most zero, which is false. Its range covers the whole array, but before the loop nothing has been processed.
  - zh: 违反：invariant 要求 2 小于等于 0，这是假的。它的范围覆盖了整个数组，但循环开始前还没有处理任何元素。
- `Topo05Counterexample-4` (7.0 s)
  - en: Three small numbers turn a one-line error into a precise cause: the quantifier range is too wide.
  - zh: 三个小数字，就把一行报错变成了一个精确的原因：量词的范围太宽了。

## 6. Topo06Repair  (~35 s)

**Purpose.** Rationale -> repaired line (transform the failing line into the fixed line); show the extra deletion honestly; state that the repair's verification is not reported and not run.

**On screen.** Left: code panel. Right: rationale card (verbatim fragments of model-output.txt:23, elisions marked). Beat 2: screen line 14 transforms into the repaired line (k < i), box turns accent. Beat 3: line 12 struck through in red, note 'also deleted in the recorded output' with arrow. Beat 4: WARN badge 'Verus on this repaired program: not reported' + 'The paper reports the counterexample and the repair target. We could not run Verus.' below the panel.

**Code panels.** examples/caseB-loop-SCREEN.rs; examples/caseB-repaired-line-SCREEN.rs (model-output.txt:73).

**Citations.** model-output.txt:23, 29, 73; Fig. 4 p.9 (paper gives the repair target 'k < i' / '0 <= j < k < i').

**Narration.**

- `Topo06Repair-1` (11.3 s)
  - en: The rationale follows from the counterexample: restrict the range to the processed prefix, k less than i. At i equal to zero, the claim is then vacuously true.
  - zh: 修复理由直接来自 counterexample：把范围限制在已处理的前缀上，也就是 k 小于 i。当 i 等于 0 时，这个断言就空真成立。
- `Topo06Repair-2` (3.2 s)
  - en: The repaired program changes exactly that range.
  - zh: 修复后的程序正好改了这个范围。
- `Topo06Repair-3` (7.0 s)
  - en: The recorded output also deletes one other invariant: i equals zero implies min_price is the largest i32.
  - zh: 记录下来的输出还删掉了另一条 invariant：i 等于 0 时 min_price 等于 i32 的最大值。
- `Topo06Repair-4` (13.6 s)
  - en: The paper reports this counterexample and this repair target. It does not report a Verus run of this exact program, and we could not run one, so we make no claim that it verifies.
  - zh: 论文报告了这个 counterexample 和这个修复目标。论文没有报告对这个程序本身的 Verus 运行结果，我们也没能运行，所以我们不声称它能通过验证。

## 7. Topo07Pipeline  (~44 s)

**Purpose.** Training pipeline as an architecture diagram: counterexample-guided SFT -> GRPO with Verus feedback -> safety gate -> Topological Graph Reward; Eq. 2.

**On screen.** Boxes built step by step: QwQ-32B -> Counterexample SFT (red; note 'teacher: Sonnet 4.6 · 461 trajectories from 249 programs') -> GRPO ('8 responses per prompt'); GRPO -> Safety gate (WARN; 'unsafe -> reward 0' in red) -> Verus (R_pass) -> Reward (Eq. 2); GRPO -> Topological Graph Reward (accent, R_dep) -> Reward. Bottom: Eq. 2 in mono text.

**Code panels.** none

**Citations.** §3.2 p.5 (Eq. 2, gate, zero reward); §4.1 p.6-7 (461/249, teacher, 8 rollouts).

**Narration.**

- `Topo07Pipeline-1` (4.3 s)
  - en: How is such a model trained? It starts from QwQ-32B.
  - zh: 这样的模型是怎么训练出来的？它从 QwQ-32B 出发。
- `Topo07Pipeline-2` (15.1 s)
  - en: Stage one is counterexample-guided fine-tuning. A teacher model, Sonnet 4.6, sees the failed proof, the error, and the verified reference proof, and writes the diagnosis that leads to that known answer. That gives 461 trajectories from 249 programs.
  - zh: 第一阶段是 counterexample 引导的监督微调。教师模型 Sonnet 4.6 能看到失败的证明、报错和已验证的参考证明，并写出通向这个已知答案的诊断过程。这样得到来自 249 个程序的 461 条轨迹。
- `Topo07Pipeline-3` (9.0 s)
  - en: Stage two is reinforcement learning with GRPO. For each failed proof the model samples eight responses, and Verus checks every repaired program.
  - zh: 第二阶段是用 GRPO 做强化学习。对每个失败的证明，模型采样 8 个回答，由 Verus 检查每个修复后的程序。
- `Topo07Pipeline-4` (7.4 s)
  - en: Before any reward, a safety gate checks that only proof annotations changed. An unsafe response gets zero reward.
  - zh: 在给奖励之前，安全门会检查是否只改动了证明标注。不安全的回答奖励为 0。
- `Topo07Pipeline-5` (8.6 s)
  - en: Next to the pass reward sits the Topological Graph Reward. It scores which invariants the model writes, and in what order.
  - zh: 在通过奖励之外，还有 Topological Graph Reward。它评估模型写了哪些 invariant，以及写的顺序。

## 8. Topo08Order  (~50 s)

**Purpose.** Why order matters, on the paper's illustrative binary-search example (Fig. 1-2): under-constrained vs constrained counterexample; the repair high <= i -> high < i.

**On screen.** Top badge 'illustrative example from the paper'. Invariant panel I1..I5 (Fig. 2 bottom list, I5 with the boundary error). Beat 2: boxes I1, I2-I3, I4-I5. Beat 3: I1-I3 dimmed + 'missing'; red card 'Under-constrained counterexample (Fig. 2, top)': 'state high = 2, yet it checks i = 1', 'mid = 0: a hallucinated value'. Beat 4: I1-I3 restored; state_table 'Constrained (Fig. 2, bottom)': nums [1, 3, 5], target 5, high 2, low after 1 step 2; 'I5 at i = 2: nums[2] > 5 ?  nums[2] = 5 false'. Beat 5: I5 transforms to 'high < i'; 'high <= i -> high < i'.

**Code panels.** examples/binary-search-invariants-SCREEN.rs (Fig. 2 p.4 lines I1-I5); examples/binary-search-I5-fixed-SCREEN.rs (Fig. 2 repair signal applied).

**Citations.** Fig. 1 p.3; Fig. 2 and text p.4 (illustrative).

**Narration.**

- `Topo08Order-1` (6.7 s)
  - en: Why order? Take binary-search insertion, an illustrative example from the paper. Its proof needs five invariants.
  - zh: 为什么顺序重要？看论文里的一个示意例子：二分查找插入位置。它的证明需要五条 invariant。
- `Topo08Order-2` (12.0 s)
  - en: I1 bounds the array length. I2 and I3 keep low and high in range. I4 and I5 are the partition facts, and they are useful only once the bounds hold.
  - zh: I1 约束数组长度。I2 和 I3 让 low 和 high 保持在范围内。I4 和 I5 是划分性质，只有在边界条件成立之后它们才有用。
- `Topo08Order-3` (12.0 s)
  - en: If an attempt skips I1 to I3, its counterexample is under-constrained. In the paper's illustration, it checks an index that contradicts its own state, and invents a value for mid.
  - zh: 如果一次尝试跳过了 I1 到 I3，它的 counterexample 就缺乏约束。在论文的示意中，它检查的下标和自己给出的状态相矛盾，还编造了 mid 的值。
- `Topo08Order-4` (14.0 s)
  - en: With the bounds in place, the counterexample is exact: nums is one, three, five, the target is five, and high is two. I5 then needs nums at two to exceed five, but it equals five.
  - zh: 有了边界条件，counterexample 就很精确：nums 是 1、3、5，target 是 5，high 是 2。这时 I5 要求 nums[2] 大于 5，但它等于 5。
- `Topo08Order-5` (5.1 s)
  - en: The repair follows directly: high less-or-equal i becomes high less than i.
  - zh: 修复随之而来：把 high <= i 改成 high < i。

## 9. Topo09GraphReward  (~49 s)

**Purpose.** The Topological Graph Reward: dependency graph, R_dep = α·β, a worked example, training-only.

**On screen.** Left: graph I1 -> I2, I3 -> I4, I5 (circles), label 'edges: our reading of Fig. 2 (illustrative example from the paper)'; explanation 'edge a -> b: a must hold before b can be proven'. Right: 'R_dep = α × β' with α = coverage, β = edge satisfaction; table of three orders with β and R_dep (6/6 1.0; 2/6 0.33; 0/6 0) labelled 'our computation (illustrative edge set, all α = 1)'; WARN badge 'training-time signal only' + 'evaluation: no reference proof, no graph'.

**Code panels.** none (graph + table; values from examples/rdep-worked-example-DERIVED.txt).

**Citations.** Defs. 1-3 p.5-6; Eq. 6 p.6; §4.1 p.6 (graph not provided during evaluation).

**Narration.**

- `Topo09GraphReward-1` (13.2 s)
  - en: TopoVerus turns this into a reward. Offline, it builds a dependency graph over the invariants of the verified reference proof. An edge means one invariant must hold before the other can be proven.
  - zh: TopoVerus 把这一点变成奖励。它离线地在已验证参考证明的 invariant 之间构建依赖图。一条边表示：前一条 invariant 必须先成立，后一条才能被证明。
- `Topo09GraphReward-2` (8.6 s)
  - en: Here is our reading of the paper's figure: I1 points to I2 and I3, and both point to I4 and I5.
  - zh: 这是我们对论文图示的理解：I1 指向 I2 和 I3，二者又都指向 I4 和 I5。
- `Topo09GraphReward-3` (9.3 s)
  - en: The reward multiplies coverage, the fraction of reference invariants the model wrote, by edge satisfaction, the fraction of edges written in dependency order.
  - zh: 奖励等于覆盖率乘以边满足率：覆盖率是模型写出的参考 invariant 所占比例，边满足率是按依赖顺序写出的边所占比例。
- `Topo09GraphReward-4` (10.5 s)
  - en: In our own calculation with this edge set, writing I1 to I5 in order scores one. Partition facts first scores one third. Fully reversed scores zero.
  - zh: 按这个边集，我们自己算了一下：按 I1 到 I5 的顺序写，得分为 1；先写划分性质，得分为三分之一；完全倒序，得分为 0。
- `Topo09GraphReward-5` (7.8 s)
  - en: The graph is a training signal only. At test time the model sees no reference proof and no graph.
  - zh: 依赖图只是训练信号。测试时，模型看不到参考证明，也看不到依赖图。

## 10. Topo10Safety  (~42 s)

**Purpose.** Safety gate: Verus success alone can be gamed; the released-code unit test where moving an existing assume makes Verus report verified but the gate says unsafe.

**On screen.** Top badge 'test case from the released code'. Panel 'original' (3 lines); boxes on the contract line then the body line; note 'x = 2 -> y = 1, but ensures r > 1' (our arithmetic) and badge 'Verus: verification failed'. Panel '"repair": move the existing assume' whose body line transforms into the candidate; badge 'Verus: verified' (OK colour) then 'safety gate: unsafe -> reward 0' (BAD).

**Code panels.** examples/safety-gate-S3-SCREEN.rs (tests/test_trust.py:138-149).

**Citations.** repo tests/test_trust.py:138-149; outcomes are the test's assertions, not run by us; zero reward: paper §3.2 p.5.

**Narration.**

- `Topo10Safety-1` (8.2 s)
  - en: Why the safety gate? Because "Verus says verified" can be gamed. Here is a test case from the released code.
  - zh: 为什么需要安全门？因为“Verus 说通过了”是可以被钻空子的。这是公开代码里的一个测试用例。
- `Topo10Safety-2` (15.5 s)
  - en: The function requires x greater than one and promises a result greater than one. It copies x into y, assumes y is greater than one, then subtracts one. For x equal to two it returns one, so verification fails.
  - zh: 这个函数要求 x 大于 1，并承诺结果大于 1。它把 x 复制给 y，假设 y 大于 1，然后减 1。当 x 等于 2 时返回 1，所以验证失败。
- `Topo10Safety-3` (8.6 s)
  - en: Now move the existing assume after the subtraction. No new assumption is added, yet the test expects Verus to report verified.
  - zh: 现在把已有的 assume 挪到减法之后。没有新增任何假设，但测试预期 Verus 会报告 verified。
- `Topo10Safety-4` (10.1 s)
  - en: The gate compares the two programs and says unsafe, because an existing assumption moved to a new place. In training, this response gets zero reward.
  - zh: 安全门比较两个程序，判定为 unsafe，因为一条已有的假设被挪到了新的位置。在训练中，这个回答的奖励为 0。

## 11. Topo11Results  (~42 s)

**Purpose.** Results with citations, per docs/SERIES.md numbers policy: Safe-Pass@1/@3, the +5.7/+6.3 margin with the setting difference, ablations (+11.2, +7.9), ordering effect (43.8% -> 95.8%).

**On screen.** Beat 1-2: two bar charts (Safe-Pass@1: TopoVerus 61.6, Sonnet-4.5 55.9; @3: 72.2, 65.9), '+5.7' '+6.3', settings note. Beat 3: ablation ladder bars CoT-Init 39.3, CTX-Init 50.5, CTX-Binary 53.7, CTX-Dep = TopoVerus 61.6 with brackets '+11.2 counterexample format', '+7.9 graph reward vs pass/fail RL'. Beat 4: edge satisfaction β bars CTX-Binary 43.8, CTX-Dep 95.8; coverage note 98.6% / 98.5%.

**Code panels.** none

**Citations.** Table 1 p.7; Table 4 p.18; §4.2-4.3 p.7; Table 7 p.20.

**Narration.**

- `Topo11Results-1` (8.2 s)
  - en: Results. On 471 problems from seven Verus benchmarks, TopoVerus reaches 61.6 percent Safe-Pass at 1, and 72.2 percent at 3.
  - zh: 结果。在来自七个 Verus benchmark 的 471 个问题上，TopoVerus 的 Safe-Pass@1 为 61.6%，Safe-Pass@3 为 72.2%。
- `Topo11Results-2` (12.4 s)
  - en: That is 5.7 and 6.3 points above Sonnet 4.5, the strongest prompted baseline. Note the settings differ: the baselines repair iteratively with verifier feedback, TopoVerus uses three chains of ten iterations.
  - zh: 这比最强的 prompt 基线 Sonnet 4.5 分别高出 5.7 和 6.3 个百分点。注意设置不同：基线用 verifier 反馈迭代修复，TopoVerus 使用 3 条链、每条 10 次迭代。
- `Topo11Results-3` (11.3 s)
  - en: The ablations isolate each idea. The counterexample format alone, before any RL, adds 11.2 points. The graph reward adds 7.9 points over RL with a pass-fail reward only.
  - zh: 消融实验分别检验了每个想法。仅仅 counterexample 格式本身，在任何 RL 之前，就提高了 11.2 个百分点。图奖励相比只用通过与否奖励的 RL，又提高了 7.9 个百分点。
- `Topo11Results-4` (10.1 s)
  - en: And the order changes as intended: on 24 paired verified tasks, edge satisfaction rises from 43.8 to 95.8 percent, while coverage stays about the same.
  - zh: 顺序也如预期那样改变了：在 24 个成对的已验证任务上，边满足率从 43.8% 升到 95.8%，而覆盖率基本不变。

## 12. Topo12Close  (~32 s)

**Purpose.** Limitations (what the work does not claim), bridge line to Vero, series map with tile 3 lit.

**On screen.** Heading 'What TopoVerus does not claim'; three bullets appear one per beat (loop invariants only; counterexamples not formally checked; VeruSAGE Sonnet-4.5 75.5% vs TopoVerus 30.2% Safe-Pass@1). Beat 4: series_map('vero') with 'Next: can agents build verified repositories?' in the Vero accent.

**Code panels.** none

**Citations.** §6 Limitations p.10; Table 1 p.7.

**Narration.**

- `Topo12Close-1` (7.0 s)
  - en: What TopoVerus does not claim. The curriculum targets loop invariants only, not assertions or other proof structure.
  - zh: TopoVerus 没有声称什么？它的课程只针对 loop invariant，不涉及 assertion 或其他证明结构。
- `Topo12Close-2` (7.0 s)
  - en: The counterexamples are not formally checked. The paper notes that the model may hallucinate imprecise execution traces.
  - zh: counterexample 没有经过形式化检查。论文指出，模型可能会幻觉出不精确的执行轨迹。
- `Topo12Close-3` (7.8 s)
  - en: And on systems code, the VeruSAGE suite, Sonnet 4.5 stays far ahead: 75.5 versus 30.2 percent Safe-Pass at 1.
  - zh: 在系统代码 VeruSAGE 上，Sonnet 4.5 仍然遥遥领先：Safe-Pass@1 为 75.5% 对 30.2%。
- `Topo12Close-4` (10.1 s)
  - en: TopoVerus repairs proofs one function at a time. Real verified software is a repository of modules that depend on each other. Can agents build that?
  - zh: TopoVerus 一次修复一个函数的证明。而真正的已验证软件，是由相互依赖的模块组成的代码仓库。智能体能构建出这样的软件吗？

**Total narration:** ~7.7 min, 12 scenes, 48 beats.

## Open issues

1. **Case B repair is unverified.** `research/verification/RESULTS.md` does not exist and we could not run Verus. The episode
   therefore says "the paper reports the counterexample and the repair target" and shows a WARN badge "Verus on this
   repaired program: not reported". The paper does not report a Verus run of this exact program either. The DERIVED
   minimal-repair file (`caseB-6-minimal-repair-DERIVED-UNVERIFIED.rs`) is not shown. If a Verus run becomes available,
   only Topo06Repair-4 and its badge need to change.
2. **The recorded repair also deletes `i == 0 ==> min_price == i32::MAX`.** We show this (strike-through + narration)
   rather than hide it. The research brief's unconfirmed reading is that this deletion may break preservation; we do not
   say that on screen.
3. **Binary-search edge set is our reading of Fig. 2** (labelled on screen). The R_dep values 1.0 / 0.33 / 0 are our own
   computation with a re-implementation of the released matcher/score logic (labelled "our computation"). Confirm edges
   with the author (BRIEF §12 Q3) or drop the table.
4. **Paper vs repo discrepancies are not shown**: R_pass binary (paper) vs fraction (released config); graph builder
   (subset enumeration vs leave-one-out); 461 vs 1,210 raw SFT rows; 471 vs 472 eval rows. The episode uses the paper's
   definitions only (SERIES numbers policy).
5. **Teacher name.** The paper says "Sonnet 4.6"; repo data.py says teacher provenance is absent in the source rows. We say
   "Sonnet 4.6" (paper) with citation.
6. **Safety-gate outcomes are test assertions**, not executed by us (cite line says so). The "x = 2 -> y = 1" note is our
   arithmetic from the code.
7. **Local helpers to lift into common/** (if other episodes need them): `screen()` (sectioned examples loader),
   `aligned_twin()` (line-aligned twin code panel for Transforming a failing line into its fix), `term_box()` (plain
   terminal-output card; `code_panel` with language "text" pads heavily and drops visible indentation), `strike()`, and
   `TopoScene` (TOPO_STOP env var ends a scene after a given beat, for mid-scene stills with `-s`; `-n` produced blank
   frames here).
8. **Font sizes.** The Case B code panel uses font 15 and the trajectory panels 14 so that code and the state table fit
   side by side; readable at 1080p in the stills but smaller than CODE_FONT_SIZE. The Verus output card uses 14.
9. Safe-Pass@1/@3 comparison: TopoVerus uses 3 chains × 10 iterations, cloud baselines iterative repair with verifier
   feedback (Table 1 caption); stated on screen and in narration.
