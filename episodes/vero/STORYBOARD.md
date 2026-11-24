# Episode 3: Vero — storyboard

Paper: *Vero: Can AI Agents Build Formally Verified Software Repositories?* (Ye, Lou, Sun, Song, Yan, Kasriel, Zhang, Yang, Kong, He, Song, arXiv 2608.13522v1, 2026). Benchmark repo snapshot: `repos/vero` @ `0a7325d`.
No claim is made on screen or in narration about which parts are Yuechun Sun's contribution.

Scene names, order and beat ids follow `narration.json`. Durations are estimates (words/2.6 + 0.5 s); total ≈ 7.6 min.

## 1. Vero01Open (~16 s)

**Purpose.** Series map (tile 3 lit) + fixed recap line; episode title card.

**On screen.** Beat 1: series_map(current='vero'), Vero tile stroke pulses; muted recap caption under map. Beat 2: map fades; title_card('vero', 3) with author line 'Ye, Lou, Sun, Song, Yan, Kasriel, Zhang, Yang, Kong, He, Song · 2026'; accent question line below.

**Code panels.** none

**Citations.** authors: paper p.1 (SERIES.md attribution string)

**Narration.**

- `vero01open-1` (8.2 s)
  - en: So far we repaired single proofs, first by searching for counterexamples and then with a model trained to produce them.
  - zh: 到目前为止，我们修复的都是单个证明：先是搜索 counterexample，然后是训练一个模型来生成它们。
- `vero01open-2` (7.8 s)
  - en: Episode three scales up. Vero asks whether AI agents can build whole formally verified software repositories in Lean 4.
  - zh: 第三集把规模放大。Vero 问的是：AI agent 能否在 Lean 4 中构建完整的、经过形式化验证的软件仓库？

## 2. Vero02Hook (~38 s)

**Purpose.** Hook: one real benchmark spec and the episode question.

**On screen.** Code panel centred, then shrinks to top; a schematic row of module boxes (Impl/, Spec/, Proof/, Harness, helpers, Test; labelled 'schematic') with thin dependency arcs; question in accent at bottom.

**Code panels.** examples/hook_dijkstar_spec.lean (repo benchmarks/dijkstar/Dijkstar/Spec/ShortestPath.lean:200-203). Highlight line 3 (findPathCost = some c), then line 4 (c ≤ walkCost).

**Citations.** repo ShortestPath.lean:200-203; dijkstar = Python source, paper Table 3 p.16

**Narration.**

- `vero02hook-1` (7.4 s)
  - en: Here is one specification from the benchmark. It comes from dijkstar, a Python shortest-path library translated into Lean.
  - zh: 这是 benchmark 中的一条 specification。它来自 dijkstar，一个被翻译成 Lean 的 Python 最短路径库。
- `vero02hook-2` (12.8 s)
  - en: It says: if findPathCost returns a cost c from s to t, then c is no larger than the cost of any walk from s to t. The reported cost is minimal.
  - zh: 它说：如果 findPathCost 返回从 s 到 t 的代价 c，那么 c 不超过从 s 到 t 的任何一条路径的代价。也就是说，返回的代价是最小的。
- `vero02hook-3` (10.5 s)
  - en: An agent must write findPathCost and prove this in Lean. And it is only one spec among many, spread over modules that depend on each other.
  - zh: agent 需要写出 findPathCost，并在 Lean 中证明这条性质。而这只是众多 spec 中的一条，它们分布在相互依赖的多个模块里。
- `vero02hook-4` (7.4 s)
  - en: So the question of this episode is: can an agent implement and prove a whole repository like this?
  - zh: 所以本集的问题是：agent 能否把这样一个完整的仓库既实现出来、又证明出来？

## 3. Vero03Instance (~46 s)

**Purpose.** Background: instance anatomy (Fig. 2) and the two task modes.

**On screen.** Panel 1 left (interface), notes on right appear per highlighted block: signatures (lines 1-3), RepoImpl (5-8), canonical (10-14). Panel 2 centred: spec (1-4) highlighted, then 'sorry' (line 7) boxed in BAD with 'agent fills this'. Then two cards: Proof-only (INFO) / Code-and-proof (accent), WARN caption about cross-module breakage.

**Code panels.** examples/fig2_interface.lean, examples/fig2_spec.lean (paper Fig. 2 p.5, comments/blank lines trimmed)

**Citations.** Fig. 2 p.5; §3.2 p.5

**Narration.**

- `vero03instance-1` (9.7 s)
  - en: Every Vero instance has the same shape. The paper's Figure 2 uses a small bank ledger. First come the API signatures, which are frozen.
  - zh: 每个 Vero 实例的结构都一样。论文的 Figure 2 用一个小型银行账本做例子。最前面是 API 签名，它们是冻结的。
- `vero03instance-2` (7.4 s)
  - en: A structure called RepoImpl has one field per API, and canonical names the implementation that will be graded.
  - zh: 一个名为 RepoImpl 的 structure 为每个 API 提供一个字段，而 canonical 指定将被评分的那个实现。
- `vero03instance-3` (10.5 s)
  - en: A spec is a predicate over RepoImpl. Here: a newly created account has balance zero. The agent's job is to replace each sorry with a proof.
  - zh: spec 是关于 RepoImpl 的谓词。这里的意思是：新建账户的余额为零。agent 的任务是把每个 sorry 替换成证明。
- `vero03instance-4` (7.8 s)
  - en: This gives two task modes. In proof-only mode, canonical is the curator's reference code, and the agent only proves.
  - zh: 由此有两种任务模式。在 proof-only 模式下，canonical 是策展人提供的参考实现，agent 只负责证明。
- `vero03instance-5` (10.9 s)
  - en: In code-and-proof mode, the agent writes the code too. It may refactor toward provable code, but a change in the code can break proofs in other modules.
  - zh: 在 code-and-proof 模式下，agent 还要自己写代码。它可以把代码改写得更容易证明，但代码的改动可能会破坏其他模块中的证明。

## 4. Vero04Scale (~39 s)

**Purpose.** Benchmark scale and the full-solve rule.

**On screen.** Big '43' + split bar 13 formal (INFO) / 30 Python; '743' and '2,705' stats; OK badge 'no public Lean 4 ground truth'. Then cleared to 'Solved = every spec proved' + paraphrase subline.

**Code panels.** none

**Citations.** §3.4 p.6; Table 1 p.7; contamination p.7; §3.2 p.5

**Narration.**

- `vero04scale-1` (9.0 s)
  - en: The benchmark has 43 such repositories. 13 are translated from formal sources in Dafny, Verus and Coq, and 30 from Python libraries.
  - zh: 这个 benchmark 有 43 个这样的仓库。其中 13 个翻译自 Dafny、Verus 和 Coq 的形式化项目，30 个来自 Python 库。
- `vero04scale-2` (9.0 s)
  - en: Together they contain 743 scored APIs and 2,705 scored specifications, from smart contracts and consensus protocols to data structures and numerical utilities.
  - zh: 它们总共包含 743 个计分 API 和 2,705 条计分 specification，覆盖从智能合约、共识协议到数据结构和数值工具等领域。
- `vero04scale-3` (10.5 s)
  - en: All the Lean code is new curation work with no public Lean 4 ground truth, so the paper argues the benchmark is largely free of contamination.
  - zh: 所有 Lean 代码都是全新的策展成果，没有公开的 Lean 4 标准答案，因此论文认为这个 benchmark 基本不存在数据污染问题。
- `vero04scale-4` (10.9 s)
  - en: And a repository counts as solved only when every one of its specs is proved. Any open spec leaves room for a bug it would have caught.
  - zh: 而且只有当一个仓库的每一条 spec 都被证明时，它才算被解决。任何一条未证明的 spec，都给它本可以捕获的 bug 留下了空间。

## 5. Vero05Architecture (~38 s)

**Purpose.** Method diagram (paper Fig. 1), built step by step.

**On screen.** Real repos → Curation (stage list above) → Benchmark → Proof-only / Code+proof → Grader (OK) and Formal audit (WARN); WARN return path from audit back under the diagram to Curation, labelled 'defects back to curation'; pulse along cp → audit → curation.

**Code panels.** none

**Citations.** Fig. 1 p.4; §3.3 p.6

**Narration.**

- `vero05architecture-1` (12.4 s)
  - en: Here is the whole system, following the paper's Figure 1. Real repositories go through a human-gated curation pipeline. Each stage is run by an LLM agent and approved by a curator.
  - zh: 这是整个系统，对应论文的 Figure 1。真实的仓库要经过一个由人把关的策展流水线。每个阶段由一个 LLM agent 执行，并由策展人批准。
- `vero05architecture-2` (6.3 s)
  - en: The result is the Lean benchmark. Agents then work in one of the two modes.
  - zh: 结果就是这个 Lean benchmark。随后 agent 在两种模式之一中工作。
- `vero05architecture-3` (7.8 s)
  - en: Their output goes to an independent grader, which rebuilds the repository from a clean state before it counts anything.
  - zh: 它们的输出交给一个独立的 grader，grader 在计分之前先从干净状态重新构建仓库。
- `vero05architecture-4` (12.0 s)
  - en: There is a second exit. Instead of a proof, an agent may submit machine-checked evidence that the benchmark itself is wrong. This formal audit route sends defects back to curation.
  - zh: 还有第二个出口。agent 可以不提交证明，而是提交经过机器检查的证据，说明 benchmark 本身有错。这条形式化审计路线会把缺陷送回策展环节。

## 6. Vero06Grader (~46 s)

**Purpose.** Anti-cheating: the grader's three layers.

**On screen.** Three layer cards in a row at top; the active one gets a thick stroke. Detail area below: (1) slot code panel, marker lines 2-4 highlighted + caption; (2) axioms.py line 31 + three OK badges, then '368' in BAD; (3) bullet list of screening checks.

**Code panels.** examples/grader_slot.lean (repo Account.lean:33-36), examples/grader_allowlist.py (repo axioms.py:31)

**Citations.** App. D p.19-20; axioms.py:31; hygiene.py:20-27; 368 at p.19

**Narration.**

- `vero06grader-1` (9.0 s)
  - en: The grader has three layers, because the paper shows that a check that only asks whether the code compiles can be gamed.
  - zh: grader 有三层，因为论文表明，只问代码能否编译的检查是可以被钻空子的。
- `vero06grader-2` (11.7 s)
  - en: First, only the inside of marked slots counts. Those bodies are copied into a fresh copy of the benchmark, so a weakened spec or a deleted obligation simply reverts.
  - zh: 第一层：只有标记槽位内部的内容才算数。这些内容会被拷贝进一份全新的 benchmark 副本，所以被削弱的 spec 或被删除的证明义务会自动恢复原样。
- `vero06grader-3` (9.7 s)
  - en: Second, every scored theorem is checked with print axioms. Only Lean's three standard axioms are allowed: Classical dot choice, propext and Quot dot sound.
  - zh: 第二层：每个计分定理都要用 print axioms 检查。只允许 Lean 的三条标准公理：Classical.choice、propext 和 Quot.sound。
- `vero06grader-4` (6.7 s)
  - en: This layer is not hypothetical. The paper reports 368 specification outcomes rejected at this stage alone.
  - zh: 这一层并非纸上谈兵。论文报告，仅在这一层就有 368 个 specification 结果被拒绝。
- `vero06grader-5` (9.0 s)
  - en: Third, declaration screening flags tricks such as hollow typeclass instances, and any run that puts implemented by into implementation files is voided.
  - zh: 第三层：声明筛查会标记诸如空壳 typeclass instance 之类的把戏；任何在实现文件中使用 implemented_by 的运行都会被作废。

## 7. Vero07Base64 (~43 s)

**Purpose.** Main motivated example: two contradicting verdict specs.

**On screen.** Left column: spec 1 (padding, line 2 highlighted INFO) above spec 2 (reject, line 4 highlighted BAD). Right: byte number line 0x37..0x43, reject gap (0x39,0x41) shaded BAD with open endpoints, '=' 0x3D dot in INFO (then indicated in BAD). Below: state_table 'Conflict at one byte' (c=0x3D; spec 1 demands some none; spec 2 demands none) and BAD badge 'no implementation satisfies both'.

**Code panels.** examples/base64_padding_spec_paper.lean, examples/base64_reject_spec_paper.lean (paper p.24, pre-fix, verbatim)

**Citations.** App. F Audit 1 p.24; verdict = Verus source, Table 3 p.16

**Narration.**

- `vero07base64-1` (8.6 s)
  - en: Now the main example. In the verdict instance, translated from a Verus project, a function called charToBits classifies one Base64 character.
  - zh: 现在来看主要例子。在 verdict 实例中（翻译自一个 Verus 项目），一个名为 charToBits 的函数对单个 Base64 字符进行分类。
- `vero07base64-2` (7.0 s)
  - en: The first spec says that byte 0x3D, the equals sign, is padding. charToBits must return some none.
  - zh: 第一条 spec 说：字节 0x3D，也就是等号，是填充符。charToBits 必须返回 some none。
- `vero07base64-3` (10.1 s)
  - en: The second spec lists byte ranges outside the Base64 alphabet that must be rejected. One of them is every byte strictly between 0x39 and 0x41.
  - zh: 第二条 spec 列出了 Base64 字母表之外、必须被拒绝的字节范围。其中一个范围是严格介于 0x39 和 0x41 之间的所有字节。
- `vero07base64-4` (9.0 s)
  - en: Put them on a number line. The digit nine is 0x39, capital A is 0x41, and 0x3D sits right inside that gap.
  - zh: 把它们放到数轴上。数字 9 是 0x39，大写 A 是 0x41，而 0x3D 恰好落在这个区间内。
- `vero07base64-5` (8.2 s)
  - en: So for the input 0x3D, one spec demands some none and the other demands none. No implementation can satisfy both.
  - zh: 所以对于输入 0x3D，一条 spec 要求 some none，另一条要求 none。没有任何实现能同时满足两者。

## 8. Vero08Audit (~47 s)

**Purpose.** Audit route resolves the conflict; paper's fix; audit totals and defect taxonomy.

**On screen.** Generic joint_unsat claim form panel (repo Harness doc comment), accent line naming GPT-5.5 (xhigh); paper quote of the one-line contradiction + muted note that the proof script is not published. Then spec 2 with line 4 boxed BAD; TransformFromCopy of that line into the 'paper's fix (p.24)' panel; OK badge '0x3D excluded'; WARN quote. Then '38 spec defects / 9 instances + 6 groups' and Table 6 bar chart, 'Direct conflict' bar in accent tagged 'verdict'.

**Code panels.** examples/joint_unsat_claim_form_repo.lean (repo dijkstar Harness.lean:34-35, generic form, NOT the agent proof); examples/base64_reject_spec_paper.lean; examples/base64_fix_paper.lean (paper p.24 fix line)

**Citations.** App. F p.24; Table 6 p.24

**Narration.**

- `vero08audit-1` (10.1 s)
  - en: During benchmark development, GPT-5.5 at xhigh effort flagged this pair through the audit route, with a machine-checked proof that the two specs are jointly unsatisfiable.
  - zh: 在 benchmark 开发期间，GPT-5.5（xhigh）通过审计路线标记了这一对 spec，并给出一个经过机器检查的证明，说明这两条 spec 联合不可满足。
- `vero08audit-2` (9.7 s)
  - en: The paper says that after unfolding both specs, the proof collapses to a one-line contradiction: 0x3D is less than 0x41 and greater than 0x39.
  - zh: 论文说，在展开两条 spec 之后，这个证明归结为一行矛盾：0x3D 小于 0x41 且大于 0x39。
- `vero08audit-3` (10.9 s)
  - en: The paper's fix excludes 0x3D from the reject range. In the paper's words, this error survived manual review and type-checking but was caught automatically by the agent.
  - zh: 论文给出的修复是把 0x3D 从拒绝范围中排除。用论文的话说，这个错误逃过了人工审查和类型检查，却被 agent 自动发现了。
- `vero08audit-4` (9.7 s)
  - en: Across the released benchmark, the audit route produced 38 specification defects in 9 instances, plus 6 jointly unsatisfiable groups, all repaired before the evaluation.
  - zh: 在发布的 benchmark 中，审计路线一共发现了 9 个实例中的 38 个 specification 缺陷，外加 6 组联合不可满足的 spec，全部在评测前修复。
- `vero08audit-5` (7.0 s)
  - en: Most were mistranslated semantics or missing conditions. The verdict pair is the single direct conflict between specs.
  - zh: 其中大多数是语义翻译错误或缺失的前提条件。verdict 这一对是唯一一例 spec 之间的直接冲突。

## 9. Vero09Trust (~56 s)

**Purpose.** Trust segment: true-but-meaningless proofs (implemented_by, native_decide).

**On screen.** Accent headline. dijkstar oracle panel with WARN tag 'illustrative (paper p.20)': lines 1-2 boxed INFO + note, line 3 boxed BAD + note; '20,440 graphs' text + OK badge 'grader: impl_oracle, run voided'. Then base58 native_decide panel, line 3 boxed BAD, 'depends on [Lean.ofReduceBool] not in the allowlist', '28 of that run's 53 specs fail this way'. Close: 'the checker + the specs, not “it compiles”'.

**Code panels.** examples/trust_dijkstar_oracle_paper.lean (paper p.20, illustrative); examples/trust_base58_native_decide_paper.lean (paper p.19)

**Citations.** App. D p.19-20

**Narration.**

- `vero09trust-1` (10.1 s)
  - en: The audit shows that a spec can be wrong. The opposite also happens: a proof can be true and still not mean what you think.
  - zh: 审计说明 spec 本身可能是错的。反过来也会发生：一个证明可以是真的，却并不意味着你以为的那件事。
- `vero09trust-2` (11.7 s)
  - en: The paper describes a trick met on dijkstar during benchmark development. findPathCost is defined as the choice of a minimal cost, so every optimality proof is true by definition.
  - zh: 论文描述了在 dijkstar 上开发 benchmark 时遇到的一个把戏：把 findPathCost 定义为对某个最小代价的选择，于是每个最优性证明都按定义成立。
- `vero09trust-3` (11.3 s)
  - en: Then implemented by swaps in a real Bellman-Ford at run time. The paper reports no output difference across 20,440 generated graphs. The grader now voids any such run.
  - zh: 然后用 implemented_by 在运行时换上一个真正的 Bellman-Ford。论文报告，在 20,440 个生成的图上输出没有任何差别。现在 grader 会作废任何这样的运行。
- `vero09trust-4` (15.5 s)
  - en: native decide is subtler. This base58 lemma is true, but it is decided by compiled code, not by the kernel, which adds the axiom Lean dot of reduce bool. In that run, 28 of 53 specs failed this way.
  - zh: native_decide 更隐蔽。这条 base58 引理是真的，但它由编译后的代码而不是 kernel 来判定，因此引入了公理 Lean.ofReduceBool。在那次运行中，53 条 spec 里有 28 条因此失败。
- `vero09trust-5` (7.8 s)
  - en: So in Vero, the checker and the specs decide what a proof means, not the fact that it compiles.
  - zh: 所以在 Vero 中，决定一个证明意味着什么的是 checker 和 spec，而不是它能通过编译这一事实。

## 10. Vero10Results (~36 s)

**Purpose.** Results with citations.

**On screen.** Setup line; bar chart 'Full solves, code-and-proof mode' (27/8/2/2 of 43, GPT-5.5 xhigh in accent); chart shrinks left; '87.3%' big on right with caption; bottom row '73.6%' (helper lemmas) and '10' (repos resisting all eight configurations).

**Code panels.** none

**Citations.** §4.1 p.7; Fig. 3 caption p.8; p.8 text; Fig. 3(a); Fig. 5(b)

**Narration.**

- `vero10results-1` (5.5 s)
  - en: Now the results. Four agent setups, two modes, 43 repositories, 90 minutes each.
  - zh: 现在看结果。四种 agent 配置，两种模式，43 个仓库，每次 90 分钟。
- `vero10results-2` (12.4 s)
  - en: In code-and-proof mode, the best setup, GPT-5.5 at xhigh, fully solves 27 of 43. Claude Opus 4.8 solves 8, and GPT-5.5 at medium effort and Claude Sonnet 5 solve 2 each.
  - zh: 在 code-and-proof 模式下，最好的配置 GPT-5.5（xhigh）完整解决了 43 个中的 27 个。Claude Opus 4.8 解决了 8 个，GPT-5.5（mid）和 Claude Sonnet 5 各解决 2 个。
- `vero10results-3` (7.8 s)
  - en: Yet that best agent passes 87.3 percent of all specs. High per-spec coverage does not mean a finished repository.
  - zh: 然而，这个最好的 agent 通过了 87.3% 的 spec。逐条 spec 的高覆盖率并不等于完成了整个仓库。
- `vero10results-4` (10.1 s)
  - en: In the code-and-proof full solves, a median of 73.6 percent of proof lines live in agent-written helper lemmas. And 10 repositories resist all eight configurations.
  - zh: 在 code-and-proof 模式的完整解决中，证明代码行的中位数 73.6% 位于 agent 自己写的辅助引理中。而有 10 个仓库在全部八种配置下都没有被解决。

## 11. Vero11Limits (~29 s)

**Purpose.** Limitations at the paper's strength.

**On screen.** Three WARN-edged cards appear one per beat; muted sortedcontainers example line.

**Code panels.** none

**Citations.** Limitations p.11; App. H.4 p.31

**Narration.**

- `vero11limits-1` (8.2 s)
  - en: What Vero does not claim. It targets Lean 4 only, and concurrent or temporal protocols are absent from the corpus.
  - zh: Vero 没有声称什么？它目前只面向 Lean 4，语料中也没有并发或时序协议。
- `vero11limits-2` (6.7 s)
  - en: The audit certifies that specs are formally satisfiable, not that they are semantically correct or complete.
  - zh: 审计只能证明 spec 在形式上可满足，而不能保证它们在语义上正确或完整。
- `vero11limits-3` (14.3 s)
  - en: And a full solve says nothing about what the specs leave out, such as running time. On sortedcontainers, one agent's linear scan passed every spec with O of n lookup instead of O of log n.
  - zh: 完整解决也说明不了 spec 没有覆盖的东西，比如运行时间。在 sortedcontainers 上，一个 agent 用线性扫描通过了所有 spec，查找复杂度是 O(n) 而不是 O(log n)。

## 12. Vero12Bridge (~18 s)

**Purpose.** Fixed bridge line, then series map with tile 4 lit.

**On screen.** Two-line lesson (second line in accent), Vekto-green 'Next' line; then series_map(current='vekto').

**Code panels.** none

**Citations.** none

**Narration.**

- `vero12bridge-1` (15.9 s)
  - en: Vero's lesson is that the checker and the specification decide what a proof means. In the last episode we take that lesson to real systems code: optimised SIMD kernels, where the question is whether two programs compute the same thing.
  - zh: Vero 的启示是：checker 和 specification 决定了一个证明的意义。在最后一集，我们把这个启示带到真实的系统代码中：优化过的 SIMD kernel，问题是两个程序是否计算出相同的结果。
- `vero12bridge-2` (2.0 s)
  - en: Next: episode four, Vekto.
  - zh: 下一集：第四集，Vekto。

## Open issues

1. **verdict proof not shown.** The agent's joint-unsat proof script is not published (paper p.24 describes it only). The episode shows the two specs verbatim, the generic claim form from the repo's `joint_unsat` macro doc comment (labelled 'generic'), and the paper's one-line description as a quote. If the authors release the run artifact, Vero08Audit beat 1-2 could show it.
2. **Fix version.** On screen is the paper's fix (`c ≠ 0x3D` conjunct, p.24), labelled 'paper's fix (p.24)'. The released repo splits the range instead (`Spec/Base64.lean:42-48`); the citation line says so. Logically equivalent for UInt8 (research brief), not re-checked in Lean here.
3. **Failure taxonomy chart.** Fig. 7b (gave up / unfilled / build / cheat) and Fig. 8a (spec types) pairings are [inferred] in the brief, so neither is charted. The only taxonomy chart is Table 6 (audit defect categories 18/17/2/1), whose values are printed in a table on p.24 (verified from the PDF text layer). The Fig. 7b text-only statements (a third at build time, 14% cheat) are not used.
4. **Hook spec choice.** The hook uses a real benchmark spec (`dijkstar`, `spec_cost_minimal_unbounded`); Fig. 2's BankLedger is a paper/repo exemplar (repo `reference/`), so it is used only to explain the instance format, labelled as Fig. 2. The module row in Vero02Hook is a schematic (labelled), using folder names that exist in the benchmark layout; its arcs are not a measured dependency graph.
5. **Grader slot snippet** comes from the BankLedger exemplar (`reference/…/Proof_modecodeproof/Account.lean:33-36`), labelled 'BankLedger exemplar'. Its marker line is ~90 columns (over the ~70-column guideline); it is shown full width at font 18 rather than trimmed.
6. **Local helpers** (could be lifted into common/ if other episodes need them): `load()` (example file without header), `byte_line()` (number line with an open interval and a highlighted point), `CurvedArrowLink()` (thin arc between boxes in a row), and the Fig. 1 return path drawn as an orthogonal polyline (components.pipeline's curved edges cut through boxes for a long back-edge).
7. **Fig. 1 crossing edges.** Proof-only→audit and code+proof→grader cross in the middle, as both modes feed both exits in the paper's figure. Acceptable at 1080p; a layout with a merge node would avoid it.
8. **Paper text checks.** Key quotes and numbers (p.2, p.6-8, p.11, p.19-20, p.24, p.31) were re-checked against the PDF text layer (pypdf, temporary install outside the project); figures were not seen as images.
