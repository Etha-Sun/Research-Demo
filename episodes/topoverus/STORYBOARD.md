# TopoVerus storyboard

Paper: *Curriculum Proof Repair with Learned Counterexamples*, Yuechun Sun, Jun Yang, Kexin Pei, NeurIPS 2026 (arXiv 2611.13627v1, `papers/topoverus.pdf`). Code: github.com/Etha-Sun/Topoverus @ 8784962 (used only for the safety-gate example). Page numbers are PDF pages. Narration below is copied from narration.json (the source of truth); durations are words/2.6 + 0.5 s estimates.

## 1. Topo01Title  (~14 s)

**Purpose.** Title card and the question.

**On screen.** title_card (TopoVerus, subtitle, 'Yuechun Sun, Jun Yang, Kexin Pei · NeurIPS 2026'); question line in the accent colour.

**Code panels.** none

**Citations.** paper p.1.

**Narration.**

- `Topo01Title-1` (13.6 s)
  - en: TopoVerus: curriculum proof repair with learned counterexamples, by Sun, Yang and Pei, at NeurIPS 2026. Can a model learn to explain a failed proof with a concrete counterexample, then repair it, in one pass?
  - zh: TopoVerus：用学习得到的 counterexample 做课程式证明修复，作者 Sun、Yang 和 Pei，发表于 NeurIPS 2026。模型能否学会用一个具体的 counterexample 解释失败的证明，然后修好它，而且一次生成就完成？

## 2. Topo02Hook  (~44 s)

**Purpose.** Hook: the paper's Case B proof (LeetCode 121) and Verus's one-line error that names the obligation but not the cause.

**On screen.** Left: code panel. Box moves ensures (screen lines 4-5, INFO) -> loop (9-18) -> buggy invariant (12-14, WARN). Right: 'Verus error' card with the two lines from Fig. 4; the box turns red and an arrow joins card and line. 'Which state breaks it? Why?' in accent.

**Code panels.** examples/caseB-fig4-code-SCREEN.rs; examples/caseB-fig4-verus-error.txt.

**Citations.** TopoVerus Fig. 4 p.9 (Case Study B, App. B p.17).

**Narration.**

- `Topo02Hook-1` (14.3 s)
  - en: Here is the paper's case study: a Verus proof for LeetCode 121, best time to buy and sell a stock. The postcondition says the result bounds the profit of every buy day and later sell day.
  - zh: 这是论文中的 case study：LeetCode 121“买卖股票的最佳时机”的一个 Verus 证明。后置条件说：对任意一个买入日和之后的卖出日，结果都不小于它们的利润。
- `Topo02Hook-2` (10.9 s)
  - en: The loop tracks the cheapest price and the best profit so far. Its last invariant claims that no pair of days in the whole array beats max_pro.
  - zh: 循环维护到目前为止的最低价和最大利润。最后一条 loop invariant 声称：整个数组里任何一对日子的利润都不超过 max_pro。
- `Topo02Hook-3` (9.0 s)
  - en: Verus rejects the proof with one line: invariant not satisfied before loop. It names the failed obligation, but not why it fails.
  - zh: Verus 只用一行拒绝了这个证明：invariant not satisfied before loop。它指出了哪个证明义务失败，却没有说为什么失败。
- `Topo02Hook-4` (9.7 s)
  - en: A repair model that sees only this line has to guess. It should first explain the failure: which state breaks the invariant, and why.
  - zh: 只看到这一行的修复模型只能去猜。它应该先解释失败：哪个程序状态破坏了 invariant，以及为什么。

## 3. Topo03Background  (~35 s)

**Purpose.** Background: loop invariant (holds before the loop, preserved); counterexample = (state, trace, violation); single-pass generation and the paper's definition of a useful counterexample.

**On screen.** Beat 1: 'Before the loop' -> 'Every iteration'. Beat 2: three red cards [State] σ / [Execution Trace] τ / [Violation] ψ. Beat 3: 'TopoVerus: counterexample, rationale and repair in one pass' + abstract quote card.

**Code panels.** none

**Citations.** Eq. 1 and §3.1 p.4-5; Abstract p.1 (quote verbatim).

**Narration.**

- `Topo03Background-1` (7.4 s)
  - en: A loop invariant must hold before the loop starts, and every iteration must preserve it. Verus checks both.
  - zh: loop invariant 必须在循环开始前成立，并且每次迭代都要保持它。Verus 会检查这两点。
- `Topo03Background-2` (12.4 s)
  - en: A counterexample makes a failure concrete. TopoVerus writes it in three parts: a program state where the obligation fails, an execution trace from that state, and the violation in plain words.
  - zh: counterexample 让失败变得具体。TopoVerus 把它写成三部分：一个让证明义务失败的程序状态，从这个状态出发的执行轨迹，以及用自然语言说明的违反原因。
- `Topo03Background-3` (15.5 s)
  - en: Generating useful counterexamples at inference time usually needs costly iterative refinement. TopoVerus learns to write one in a single pass. Its key insight: a counterexample is useful when conditioning on it helps the model produce a safe, verifier-passing proof.
  - zh: 在推理时生成有用的 counterexample，通常需要代价高昂的迭代改进。TopoVerus 学会一次就写出 counterexample。它的核心想法是：如果以一个 counterexample 为条件能帮助模型写出安全且通过 verifier 的证明，它就是有用的。

## 4. Topo04Format  (~22 s)

**Purpose.** The response format (App. D.1 prompt) and the generated counterexample for Case B (Fig. 4).

**On screen.** Beat 1-2: prompt panel, the three section lines coloured red / blue / accent; note '(preceded by a <think> block)'. Beat 3: the Fig. 4 counterexample panel (red border) and, below it in accent, the Fig. 4 sentence naming the repair target.

**Code panels.** examples/appD-output-format.txt; examples/caseB-fig4-counterexample-SCREEN.txt.

**Citations.** App. D.1 p.21, App. D p.20; Fig. 4 p.9.

**Narration.**

- `Topo04Format-1` (6.3 s)
  - en: Every TopoVerus response has the same shape. The prompt asks for three sections, in order.
  - zh: TopoVerus 的每个回答都有相同的结构。prompt 要求按顺序给出三个部分。
- `Topo04Format-2` (9.7 s)
  - en: First a counterexample, with State, Execution Trace and Violation. Then a concise repair plan. Then a single Rust block with the complete repaired program.
  - zh: 先是 counterexample，包含 State、Execution Trace 和 Violation；然后是简洁的修复计划；最后是一个 Rust 代码块，给出完整的修复后程序。
- `Topo04Format-3` (6.3 s)
  - en: For the max-profit proof, TopoVerus generates this counterexample. We will read it piece by piece.
  - zh: 针对这个最大利润证明，TopoVerus 生成了这个 counterexample。我们逐段来看。

## 5. Topo05Counterexample  (~36 s)

**Purpose.** Walk through the counterexample next to the code.

**On screen.** Left: code panel. Right: [State] table (price, i, max_pro, min_price); array 5 3 7 with j, k; 'price[2] - price[0] = 7 - 5 = 2'; '2 <= max_pro = 0 : false'; note 'before any day is processed: only the empty prefix 0..i', replaced by 'root cause: the quantifier range'.

**Code panels.** examples/caseB-fig4-code-SCREEN.rs.

**Citations.** Fig. 4 p.9.

**Narration.**

- `Topo05Counterexample-1` (8.6 s)
  - en: The state: price is five, three, seven. Before the loop, i is zero and max_pro is zero. All input bounds hold.
  - zh: 状态：price 是 5、3、7。循环开始前，i 为 0，max_pro 为 0。所有输入范围条件都满足。
- `Topo05Counterexample-2` (9.7 s)
  - en: The trace: Verus checks the invariant at loop entry. Take j equal to zero and k equal to two. Seven minus five is two.
  - zh: 轨迹：Verus 在进入循环时检查 invariant。取 j 等于 0、k 等于 2，7 减 5 等于 2。
- `Topo05Counterexample-3` (11.7 s)
  - en: The violation: the invariant demands that two is at most zero, which is false. Before any day is processed, the proof can only make claims about the empty prefix.
  - zh: 违反：invariant 要求 2 小于等于 0，这是假的。在处理任何一天之前，证明只能对空前缀做出断言。
- `Topo05Counterexample-4` (5.9 s)
  - en: Three small numbers turn a one-line error into a precise cause: the quantifier range.
  - zh: 三个小数字，就把一行报错变成了一个精确的原因：量词的范围。

## 6. Topo06Repair  (~19 s)

**Purpose.** The repair target the counterexample pinpoints, as the paper states it.

**On screen.** Left: code panel with the buggy invariant boxed red. Right: accent card 'repair target' with the Fig. 4 sentence. Beat 2: the range line transforms to '0 <= j < k < i'; box turns accent; 'full array -> processed prefix'.

**Code panels.** examples/caseB-fig4-code-SCREEN.rs; examples/caseB-fig4-repair-target-SCREEN.rs.

**Citations.** Fig. 4 p.9; §4.6 p.8; App. B p.17.

**Narration.**

- `Topo06Repair-1` (11.3 s)
  - en: The counterexample pinpoints a local correction. The last invariant talks about all future days; it should only summarize the processed prefix, j less than k less than i.
  - zh: counterexample 指出了一个局部修正。最后一条 invariant 谈论的是所有未来的日子；它应该只概括已处理的前缀，也就是 j 小于 k 小于 i。
- `Topo06Repair-2` (7.4 s)
  - en: A coarse invariant failure has become a localized repair target: replace the full-array range with the processed prefix.
  - zh: 一个笼统的 invariant 失败，变成了一个定位明确的修复目标：把整个数组的范围换成已处理的前缀。

## 7. Topo07Pipeline  (~41 s)

**Purpose.** Architecture: QwQ-32B -> counterexample SFT -> GRPO; safety gate (Lynette); Verus R_pass; Topological Graph Reward; Eq. 2.

**On screen.** pipeline() diagram built step by step; teacher/data note above SFT; 'unsafe -> reward 0'; Eq. 2 in mono at the bottom.

**Code panels.** none

**Citations.** §3.2 and Eq. 2 p.5; §4.1 p.6-7.

**Narration.**

- `Topo07Pipeline-1` (4.3 s)
  - en: How is such a model trained? It starts from QwQ-32B.
  - zh: 这样的模型是怎么训练出来的？它从 QwQ-32B 出发。
- `Topo07Pipeline-2` (11.3 s)
  - en: Stage one is fine-tuning. A teacher, Sonnet 4.6, sees the failed proof, the error and the verified reference proof, and writes the diagnosis: 461 trajectories from 249 programs.
  - zh: 第一阶段是监督微调。教师模型 Sonnet 4.6 能看到失败的证明、报错和已验证的参考证明，并写出诊断过程：来自 249 个程序的 461 条轨迹。
- `Topo07Pipeline-3` (9.0 s)
  - en: Stage two is reinforcement learning with GRPO. For each failed proof the model samples eight responses, and Verus checks every repaired program.
  - zh: 第二阶段是用 GRPO 做强化学习。对每个失败的证明，模型采样 8 个回答，由 Verus 检查每个修复后的程序。
- `Topo07Pipeline-4` (7.4 s)
  - en: A safety gate, the Lynette checker, confirms that only proof annotations changed. An unsafe response gets zero reward.
  - zh: 安全门，也就是 Lynette 检查器，确认只有证明标注被改动。不安全的回答奖励为 0。
- `Topo07Pipeline-5` (8.6 s)
  - en: Next to the pass reward sits the Topological Graph Reward. It scores which invariants the model writes, and in what order.
  - zh: 在通过奖励之外，还有 Topological Graph Reward。它评估模型写了哪些 invariant，以及写的顺序。

## 8. Topo08Order  (~50 s)

**Purpose.** Why order matters: the paper's motivating example (binary-search insertion, Fig. 1-2).

**On screen.** Invariant panel I1..I5 (Fig. 2). Beat 2: boxes I1, I2-I3, I4-I5. Beat 3: I1-I3 dimmed 'missing', I5 boxed red, red card 'Under-constrained counterexample (Fig. 2, top)'. Beat 4: state table (Fig. 2 bottom) and the I5 check. Beat 5: I5 line transforms to 'high < i'.

**Code panels.** examples/binary-search-invariants-SCREEN.rs; examples/binary-search-I5-fixed-SCREEN.rs.

**Citations.** Fig. 1 p.3; Fig. 2 and §2.1 p.4.

**Narration.**

- `Topo08Order-1` (5.9 s)
  - en: Why order? The paper's motivating example is binary-search insertion. Its proof needs five invariants.
  - zh: 为什么顺序重要？论文的动机例子是二分查找插入位置。它的证明需要五条 invariant。
- `Topo08Order-2` (12.0 s)
  - en: I1 bounds the array length. I2 and I3 keep low and high in range. I4 and I5 are the partition facts, and they become useful only once the bounds hold.
  - zh: I1 约束数组长度。I2 和 I3 让 low 和 high 保持在范围内。I4 和 I5 是划分性质，只有在边界条件成立之后它们才有用。
- `Topo08Order-3` (12.4 s)
  - en: Suppose an attempt omits I1 to I3 and has a wrong I5. Its counterexample is under-constrained: it checks an index that contradicts its own state, and invents a value for mid.
  - zh: 假设一次尝试漏掉了 I1 到 I3，而且 I5 写错了。它的 counterexample 缺乏约束：检查的下标和自己给出的状态相矛盾，还编造了 mid 的值。
- `Topo08Order-4` (14.3 s)
  - en: With I1 to I4 in place, the counterexample is exact: nums is one, three, five, the target is five, and high is two. I5 then needs nums at two to exceed five, but it equals five.
  - zh: 有了 I1 到 I4，counterexample 就很精确：nums 是 1、3、5，target 是 5，high 是 2。这时 I5 要求 nums[2] 大于 5，但它等于 5。
- `Topo08Order-5` (5.1 s)
  - en: The repair follows directly: high less-or-equal i becomes high less than i.
  - zh: 修复随之而来：把 high <= i 改成 high < i。

## 9. Topo09GraphReward  (~54 s)

**Purpose.** Topological Graph Reward: the dependency graph as Fig. 2 draws it, the formula, the qualitative effect the paper states.

**On screen.** Graph as in Fig. 2: I1 -> dashed group {I2, I3} -> I4 and I5'. Beat 2: legend correct/wrong/missing; nodes coloured for Fig. 2 top (I1-I3 missing, I4 correct, I5' wrong), then Fig. 2 bottom (I1-I4 correct, I5' wrong). Beat 3: R_dep = α × β with definitions. Beat 4: 'prerequisite facts first -> counterexamples for dependent invariants in a better-constrained proof state'. Beat 5: 'training signal only' badge + 'at test time: no reference proof, no graph'.

**Code panels.** none

**Citations.** §3.1, Defs. 1-3 p.5-6; Fig. 2 p.4; Eq. 6 p.6; §2.1 'Implication for training' p.4; §4.1 p.6.

**Narration.**

- `Topo09GraphReward-1` (12.4 s)
  - en: TopoVerus turns this into a reward. Offline, it builds a dependency graph over the reference proof's invariants: an edge means one must be established before the other can be inductively verified.
  - zh: TopoVerus 把这一点变成奖励。它离线地在参考证明的 invariant 之间构建依赖图：一条边表示前一条必须先成立，后一条才能被归纳地验证。
- `Topo09GraphReward-2` (14.7 s)
  - en: For binary search, I1 comes before the bounds I2 and I3, and the bounds come before I4 and I5. The first attempt was missing I1 to I3. The second had them, so only the wrong I5 remained.
  - zh: 在二分查找中，I1 在边界 I2 和 I3 之前，边界又在 I4 和 I5 之前。第一次尝试缺了 I1 到 I3；第二次已经有了它们，只剩下写错的 I5。
- `Topo09GraphReward-3` (9.3 s)
  - en: The reward multiplies coverage, the fraction of reference invariants the model wrote, by edge satisfaction, the fraction of edges written in dependency order.
  - zh: 奖励等于覆盖率乘以边满足率：覆盖率是模型写出的参考 invariant 所占比例，边满足率是按依赖顺序写出的边所占比例。
- `Topo09GraphReward-4` (9.3 s)
  - en: So the reward favours repairs that establish prerequisite facts first. Counterexamples for the dependent invariants are then checked in a better-constrained proof state.
  - zh: 所以，这个奖励鼓励先建立前提事实的修复。这样，针对依赖它们的 invariant 的 counterexample，就是在约束更充分的证明状态下检查的。
- `Topo09GraphReward-5` (7.8 s)
  - en: The graph is a training signal only. At test time the model sees no reference proof and no graph.
  - zh: 依赖图只是训练信号。测试时，模型看不到参考证明，也看不到依赖图。

## 10. Topo10Safety  (~34 s)

**Purpose.** Why the safety gate: a change that passes Verus without proving anything.

**On screen.** Heading; original program (line 1 INFO, line 2 WARN); 'Verus: verification failed' + 'x = 2 -> y = 1, but ensures r > 1'; candidate panel, line 2 transforms (assume moved); 'Verus: verified'; 'safety gate: unsafe -> reward 0'.

**Code panels.** examples/safety-gate-S3-SCREEN.rs.

**Citations.** TopoVerus code tests/test_trust.py:138-149 (the paper describes the gate, §3.2 p.5, without a worked example).

**Narration.**

- `Topo10Safety-1` (9.7 s)
  - en: Why the safety gate? Because passing Verus can be gamed. This function requires x greater than one and promises a result greater than one.
  - zh: 为什么需要安全门？因为通过 Verus 是可以被钻空子的。这个函数要求 x 大于 1，并承诺结果大于 1。
- `Topo10Safety-2` (10.1 s)
  - en: It copies x into y, assumes y is greater than one, then subtracts one. For x equal to two it returns one, so verification fails.
  - zh: 它把 x 复制给 y，假设 y 大于 1，然后减 1。当 x 等于 2 时返回 1，所以验证失败。
- `Topo10Safety-3` (7.4 s)
  - en: Now move the existing assume after the subtraction. No new assumption is added, and Verus accepts the program.
  - zh: 现在把已有的 assume 挪到减法之后。没有新增任何假设，Verus 就接受了这个程序。
- `Topo10Safety-4` (6.7 s)
  - en: The gate compares the two programs and reports unsafe. In training, this response gets zero reward.
  - zh: 安全门比较两个程序，判定为 unsafe。在训练中，这个回答的奖励为 0。

## 11. Topo11Results  (~40 s)

**Purpose.** Key results: main Safe-Pass, ablations, ordering effect.

**On screen.** Two bar charts (Safe-Pass@1/@3, TopoVerus vs Sonnet-4.5), +5.7/+6.3, settings note; ablation ladder with +11.2 and +7.9 brackets; edge satisfaction β bars 43.8 -> 95.8 with coverage note.

**Code panels.** none

**Citations.** Table 1 p.7, Table 4 p.18, §4.2-4.3 p.7; Table 7 p.20.

**Narration.**

- `Topo11Results-1` (8.2 s)
  - en: Results. On 471 problems from seven Verus benchmarks, TopoVerus reaches 61.6 percent Safe-Pass at 1, and 72.2 percent at 3.
  - zh: 结果。在来自七个 Verus benchmark 的 471 个问题上，TopoVerus 的 Safe-Pass@1 为 61.6%，Safe-Pass@3 为 72.2%。
- `Topo11Results-2` (10.5 s)
  - en: That is 5.7 and 6.3 points above Sonnet 4.5, the strongest baseline. The baselines repair iteratively with verifier feedback; TopoVerus uses three chains of ten iterations.
  - zh: 这比最强的基线 Sonnet 4.5 分别高出 5.7 和 6.3 个百分点。基线用 verifier 反馈迭代修复；TopoVerus 使用 3 条链、每条 10 次迭代。
- `Topo11Results-3` (11.3 s)
  - en: The ablations isolate each idea. The counterexample format alone, before any RL, adds 11.2 points. The graph reward adds 7.9 points over RL with a pass-fail reward only.
  - zh: 消融实验分别检验了每个想法。仅仅 counterexample 格式本身，在任何 RL 之前，就提高了 11.2 个百分点。图奖励相比只用通过与否奖励的 RL，又提高了 7.9 个百分点。
- `Topo11Results-4` (10.1 s)
  - en: And the order changes as intended: on 24 paired verified tasks, edge satisfaction rises from 43.8 to 95.8 percent, while coverage stays about the same.
  - zh: 顺序也如预期那样改变了：在 24 个成对的已验证任务上，边满足率从 43.8% 升到 95.8%，而覆盖率基本不变。

## 12. Topo12Close  (~27 s)

**Purpose.** Limitations from the paper, then the takeaway.

**On screen.** Beat 1: heading 'Limitations', three bullets. Beat 2: 'TopoVerus' in accent and three takeaway lines.

**Code panels.** none

**Citations.** §6 Limitations p.10; Table 1 p.7; Conclusion p.10.

**Narration.**

- `Topo12Close-1` (13.6 s)
  - en: Two limitations. The curriculum targets loop invariants, not assertions. And the counterexamples are not formally checked, so a trace can be imprecise. On systems code, VeruSAGE, Sonnet 4.5 stays ahead: 75.5 versus 30.2 percent.
  - zh: 有两点局限。课程只针对 loop invariant，不涉及 assertion。counterexample 也没有经过形式化检查，所以执行轨迹可能不精确。在系统代码 VeruSAGE 上，Sonnet 4.5 仍然领先：75.5% 对 30.2%。
- `Topo12Close-2` (13.6 s)
  - en: The takeaway: teach the model to name a concrete failing state before it repairs, and reward it for establishing prerequisite invariants first. Diagnosis then becomes a skill the model carries in a single pass.
  - zh: 结论：让模型在修复之前先说出一个具体的失败状态，并奖励它先建立前提 invariant。这样，诊断就成为模型一次生成就能完成的能力。

Total: 12 scenes, 42 beats, ~6.9 min of narration.

## Revision 2026-11-23

Following docs/REVISION-BRIEF.md (self-contained video, paper first, no defensive labels):

- Removed the series map, the ExVerus recap, the 'Episode 2' wording, the ExVerus-vs-TopoVerus comparison card and the bridge/series map to Vero at the end. Topo01Map is replaced by Topo01Title (title card + question). No other work is named; one plain sentence keeps the paper's related-work point (inference-time counterexamples need costly iterative refinement).
- Case B now uses the paper's Fig. 4 / App. B listing (`price`, two min_price invariants elided, error at 37:13) and the Fig. 4 generated counterexample, instead of the repo case-study files. The repo-only 3-panel trajectory, the deleted-invariant strike, the WARN badge and the 'we could not run Verus' beat are gone. Topo06 shows the repair target the paper states (restrict the range to the processed prefix, `0 <= j < k < i`) and makes no verification claim.
- Graph reward: the graph is drawn as in Fig. 2 (I1 -> {I2, I3} -> I4, I5', with correct/wrong/missing colouring for the top and bottom cases). 'Our reading', 'our own calculation' and the computed ordering table (1 / 0.33 / 0) are removed; the scene shows Eq. 6 and the paper's qualitative statement (§2.1 'Implication for training'). examples/rdep-worked-example-DERIVED.txt deleted.
- Topo08: 'illustrative' badge and wording removed; presented as the paper's motivating example (Fig. 1-2).
- Safety gate: the paper describes the gate (Lynette, §3.2) but gives no example, so the repo unit test is kept and presented plainly (no 'test case from the released code' badge, no 'we did not run it').
- Topo03 'not checked by a solver' WARN line and the Topo09 WARN badge removed; Topo12 merged limitations into one beat and ends with TopoVerus's own takeaway.
- Length 7.7 -> 6.9 min (48 -> 42 beats).
