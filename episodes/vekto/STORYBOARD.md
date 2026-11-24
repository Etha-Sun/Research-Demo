# Episode 4 — Vekto: storyboard

Work in progress, unpublished. 12 scenes, 55 beats, narration estimate about 9.0 min (words/2.6 + 0.5 s per beat; `tools/sync_durations.py` will replace it). Scene order = narration.json. All on-screen code is in `examples/`; every number carries a cite and is listed in SOURCES.md.

## 1. Vek01Open  (~28 s)

**Purpose.** Open the episode: title card ("work in progress · unpublished"), series map with tile 4 lit, recap line from docs/SERIES.md, then the episode question.

**On screen.** Title card centred. Then the four-tile series map (Vekto lit, default caption) with the recap in two muted lines above. Then three centred lines: the question (white / accent) and the assumptions question (WARN).

**Code panels.** none

**Citations.** none (fixed series text)

**Narration.**

- `Vek01Open-1` (7.0 s)
  - en: Episode four: Vekto. This is unpublished work in progress, so treat what follows as a status report.
  - zh: 第四集：Vekto。这是尚未发表、仍在进行的工作，请把接下来的内容看作一份进展报告。
- `Vek01Open-2` (9.7 s)
  - en: We have seen counterexamples drive proof repair, and we have seen that a proof is only as good as its spec and its checker.
  - zh: 我们已经看到 counterexample 如何推动证明修复，也看到一个证明的可信程度取决于它的 spec 和它的 checker。
- `Vek01Open-3` (11.7 s)
  - en: Now the code is real optimised SIMD kernels. Ported to another instruction set, does a kernel still compute the same thing, and which assumptions does that answer rely on?
  - zh: 这一集的代码是真实的、经过优化的 SIMD kernel。移植到另一套指令集之后，kernel 还算出同样的结果吗？这个回答又依赖哪些假设？

## 2. Vek02Hook  (~39 s)

**Purpose.** Hook: a concrete failure in real code, the E1 f32-vmax NaN counterexample.

**On screen.** Left: two stacked code panels (A NEON, Bopt RVV), the max line of each boxed (INFO, then BAD). Right: state_table 'input, n = 1' (a[0]=0x7fc12345 NaN, b[0]=0x3f800000 1.0), state_table 'output[0]' (A NaN / Bopt 1.0 in BAD), badge 'A ≠ Bopt', note 'QEMU at VLEN 128/256/512; inputs swapped: same difference'.

**Code panels.** examples/01_vmax_neon_A_core.c (all 5 lines, line 4 highlighted); examples/02_vmax_rvv_Bopt_core.c (all 5 lines, line 4 highlighted)

**Citations.** final-minmax-reproduction/README.zh-CN.md; DIV-001

**Narration.**

- `Vek02Hook-1` (9.3 s)
  - en: Here is a kernel from XNNPACK, written for Arm NEON. It takes the element-wise maximum of two float arrays, four floats per step.
  - zh: 这是 XNNPACK 中一个为 Arm NEON 写的 kernel。它对两个 float 数组逐元素取最大值，每一步处理四个 float。
- `Vek02Hook-2` (8.2 s)
  - en: An LLM-driven pipeline, SALTy-RN, ported it to RISC-V Vector, RVV, and optimised it. We call this final optimised version B-opt.
  - zh: 一个由 LLM 驱动的流水线 SALTy-RN 把它移植到 RISC-V Vector（RVV）并做了优化。我们把这个最终优化版本叫作 Bopt。
- `Vek02Hook-3` (6.7 s)
  - en: Give both kernels a single element: a quiet NaN with payload 0x7fc12345, and the number 1.0.
  - zh: 给两个 kernel 同一个单元素输入：一个带 payload 0x7fc12345 的 quiet NaN，和数字 1.0。
- `Vek02Hook-4` (6.7 s)
  - en: The NEON kernel returns the NaN. The optimised RVV kernel returns 1.0. Same input, different output.
  - zh: NEON kernel 返回 NaN，优化后的 RVV kernel 返回 1.0。同一个输入，不同的输出。
- `Vek02Hook-5` (8.2 s)
  - en: This reproduces under QEMU at vector lengths 128, 256 and 512 bits, and swapping the inputs gives the same difference.
  - zh: 这个结果在 QEMU 中、向量长度 128、256 和 512 位下都能复现；交换两个输入，差异依然存在。

## 3. Vek03Lanes  (~36 s)

**Purpose.** Background: SIMD lanes and intrinsics, NEON fixed width vs RVV VLEN/vsetvl; locate the counterexample in lane 0.

**On screen.** Rows of lane boxes va = [NaN, a1, a2, a3], vb = [1.0, b1, b2, b3], arrows to vacc = [?, max, max, max]; label 'NEON: fixed 128-bit register = 4 × f32'; the intrinsic call in mono. Beat 3: an 8-lane RVV row (accent) with 'vl = vsetvl(n)'. Beat 4: lanes 1–3 dimmed, lane 0 outlined BAD, two output boxes NaN (A, NEON FMAX) and 1.0 (Bopt, RVV vfmax). a1/b1… are placeholders, not data.

**Code panels.** none (one intrinsic call shown as text, from examples/01 line 4)

**Citations.** none

**Narration.**

- `Vek03Lanes-1` (7.8 s)
  - en: Two terms first. SIMD, single instruction multiple data: one instruction works on a whole vector register, split into lanes.
  - zh: 先解释两个术语。SIMD 是单指令多数据：一条指令作用于整个向量寄存器，寄存器被分成若干 lane。
- `Vek03Lanes-2` (9.7 s)
  - en: An intrinsic is a C function for one such instruction. vmaxq_f32 takes two registers of four floats and computes the maximum lane by lane.
  - zh: intrinsic 是对应一条这类指令的 C 函数。vmaxq_f32 接收两个各含四个 float 的寄存器，逐 lane 取最大值。
- `Vek03Lanes-3` (10.1 s)
  - en: NEON registers have a fixed width. In RVV the register width, VLEN, differs between chips, and the program asks vsetvl how many elements it gets.
  - zh: NEON 的寄存器宽度是固定的。RVV 的寄存器宽度 VLEN 因芯片而异，程序用 vsetvl 询问这次能处理多少个元素。
- `Vek03Lanes-4` (8.2 s)
  - en: In our counterexample only lane zero matters: NaN against 1.0. That one lane is where the two instruction sets disagree.
  - zh: 在我们的 counterexample 中，只有第 0 个 lane 起作用：NaN 对 1.0。两套指令集正是在这一个 lane 上产生分歧。

## 4. Vek04Resolve  (~60 s)

**Purpose.** Why the kernels differ (lane models) and how Vekto handled it: L1 triage, main result kept, separate condition C-001, measured cost of the repair alternative.

**On screen.** Beat 1: two Coq panels (NEON FMAX, RVV vfmax) with NaN lines boxed and plain-language labels on the right. Beats 2–4: triage questions with answers; badge BAD 'main result: A ≠ Bopt (DIV-001)'; badge WARN 'conditional: A ≡ Bopt under C-001 (no NaN inputs)' + muted note 'counted separately · recorded as passed + rechecked · early evidence not re-runnable here'. Beat 5: the vfmax line transforms into the 5-line repaired block (lines 2–5 boxed WARN); '+18.8 % cycles' with 'geometric mean over 7 sizes, Saturn RTL · tested, not proved'.

**Code panels.** examples/03_fmax_lane_models.v panel 1 (lines 3–6 boxed) and panel 2 (lines 2–3 boxed); examples/04_vmax_bopt_nan_repair.c (line 1, then all 5; lines 2–5 boxed)

**Citations.** NeonLib.v, RvvModel.v; LESSONS L1/L3; DIV-001; CONDITIONS C-001; SUMMARY-20261111 §2; vmax-performance/REPORT

**Narration.**

- `Vek04Resolve-1` (10.1 s)
  - en: Why? Vekto gives every intrinsic a lane model. Arm FMAX propagates a NaN operand. RVV vfmax implements IEEE 754 maximumNumber, which ignores a single NaN.
  - zh: 为什么？Vekto 给每个 intrinsic 一个 lane 模型。Arm FMAX 会传播 NaN 操作数；RVV vfmax 实现 IEEE 754 的 maximumNumber，会忽略单个 NaN。
- `Vek04Resolve-2` (13.2 s)
  - en: Which side is wrong? Nothing on XNNPACK's call path checks for NaN, so the input can occur. And there is no reference: the maintainers say min and max NaN behaviour is not guaranteed.
  - zh: 哪一边错了？XNNPACK 的调用路径上没有任何 NaN 检查，所以这个输入确实可能出现。而且没有参考语义：维护者表示 min/max 的 NaN 行为不作保证。
- `Vek04Resolve-3` (9.0 s)
  - en: Vekto keeps the main result exactly as found: the original A is not equivalent to B-opt. It is recorded as divergence DIV-001.
  - zh: Vekto 按原样保留主结果：原始 A 与 Bopt 不等价。它被登记为分歧记录 DIV-001。
- `Vek04Resolve-4` (12.0 s)
  - en: Separately, under an explicit condition, C-001, no NaN inputs, the register records a conditional result as passed and rechecked, counted on its own. That early evidence cannot be re-run here.
  - zh: 另外，在显式条件 C-001（输入不含 NaN）下，登记表记录了一个条件结果，已通过并经复检，单独计数。这批早期证据无法在当前环境重跑。
- `Vek04Resolve-5` (13.2 s)
  - en: The alternative, repairing B-opt to propagate NaN, adds four statements after each vfmax. On Saturn RTL that costs 18.8 percent more cycles, as a geometric mean, and the repair was tested, not proved.
  - zh: 另一种做法是修复 Bopt 让它传播 NaN：在每个 vfmax 之后加四条语句。在 Saturn RTL 上，这使周期数增加 18.8%（几何平均）；这个修复做过测试，但没有被证明。

## 5. Vek05Testing  (~46 s)

**Purpose.** Why testing (and a bounded checker) is not enough; Vero link; the goal statement.

**On screen.** Three numbered rows (red numerals) with source lines; under row 3 the checker-model diff panel; badges 'VERIFIED' (struck through) → 'COUNTEREXAMPLE'. Beat 5: quote of the goal (Intro V2 ¶3) and a line in Vero's accent colour.

**Code panels.** examples/05_bounded_checker_patch.diff (all 6 lines)

**Citations.** XNN-005, XNN-003, final-minmax-reproduction README, Intro V2 ¶3

**Narration.**

- `Vek05Testing-1` (5.9 s)
  - en: Why didn't testing catch this? The repository records three ways that checks miss it.
  - zh: 为什么测试没有发现？仓库记录了检查漏掉它的三种方式。
- `Vek05Testing-2` (7.8 s)
  - en: First, XNNPACK's random test buffers replace NaN with zero, so its NaN assertion never fires on a NaN input.
  - zh: 第一，XNNPACK 的随机测试缓冲区会把 NaN 替换成 0，所以它的 NaN 断言从未在 NaN 输入上触发。
- `Vek05Testing-3` (9.0 s)
  - en: Second, QEMU leaves RVV tail lanes unchanged by default, so a tail-lane bug we found, XNN-003, stays hidden from XNNPACK's own tests.
  - zh: 第二，QEMU 默认保持 RVV 尾部 lane 不变，于是我们发现的一个尾部 lane bug（XNN-003）在 XNNPACK 自带的测试中无法暴露。
- `Vek05Testing-4` (10.9 s)
  - en: Third, SALTy-RN's own bounded checker said VERIFIED for this vmax pair, because its NEON model ignored NaN. With the model fixed, the same harness found the counterexample.
  - zh: 第三，SALTy-RN 自带的有界检查器对这一对 vmax 给出了 VERIFIED，因为它对这条 NEON 指令的模型忽略了 NaN。修正模型之后，同一个测试框架就找到了这个 counterexample。
- `Vek05Testing-5` (12.4 s)
  - en: This is Vero's lesson again: a verdict is only as good as the model and the spec behind it. Vekto aims for equivalence on every input that the spec's preconditions allow.
  - zh: 这又是 Vero 的教训：结论的可信程度取决于背后的模型和 spec。Vekto 的目标是：在 spec 前置条件允许的每一个输入上都证明等价。

## 6. Vek06Level  (~33 s)

**Purpose.** Why C-level equivalence: three levels, assembly drawbacks, C with reviewed intrinsic definitions.

**On screen.** Three cards: Assembly / ISA (Sail, Islaris), Compiler IR (Alive2, Rake), C + intrinsic contracts (Vekto). Beat 2: WARN bullets under assembly. Beat 3: C card in accent, others dimmed, accent bullets under it.

**Code panels.** none

**Citations.** Intro V2 ¶4–5

**Narration.**

- `Vek06Level-1` (8.2 s)
  - en: Where should such a proof live? There are three candidate levels: assembly with ISA models, a compiler IR, or C.
  - zh: 这样的证明应该放在哪一层？有三个候选层次：带 ISA 模型的汇编、编译器 IR，或者 C。
- `Vek06Level-2` (13.2 s)
  - en: At the assembly level we would need separate ISA models for fixed-width NEON and length-agnostic RVV, plus a correspondence between them, and those models cover exceptions and privileged execution that kernels never use.
  - zh: 在汇编层，需要分别为固定宽度的 NEON 和与向量长度无关的 RVV 建立 ISA 模型，再建立两者的对应关系；这些模型还涵盖 kernel 用不到的异常处理和特权执行。
- `Vek06Level-3` (12.0 s)
  - en: Vekto works at the C level. Every supported intrinsic gets an explicit C definition of its numerical and memory behaviour, and human experts review these definitions against the ISA documentation.
  - zh: Vekto 选择在 C 层工作。每个支持的 intrinsic 都有一个显式的 C 定义，描述其数值行为和内存行为，并由人类专家对照 ISA 文档审查这些定义。

## 7. Vek07Pipeline  (~63 s)

**Purpose.** Architecture diagram built step by step; the NaN path (failure → counterexample → triage → spec) pulsed at the end.

**On screen.** Middle row: impl/ → rule tool → QCP → VCs → Coq; above QCP: intrinsic contracts ← differential tests; below QCP: spec.c (accent); below Coq: check.py (12 gates → APPROVAL, OK); bottom: counterexample (BAD) → L1/L3 triage (WARN) → spec.c. Beat 2 adds a muted note on the rule tool. Beat 7 pulses VCs → counterexample → triage → spec.

**Code panels.** none

**Citations.** tools/rvv_ptr_lower/README.zh-CN.md; INTRINSICS-COMMON.zh-CN.md; pkg24/README.md

**Narration.**

- `Vek07Pipeline-1` (5.9 s)
  - en: Here is the pipeline. It starts from the original kernels, kept byte-identical to upstream.
  - zh: 这是整个流水线。它从原始 kernel 出发，它们与上游逐字节一致。
- `Vek07Pipeline-2` (12.0 s)
  - en: The C verifier, QCP, mishandles vectors passed by value, so a deterministic rule tool rewrites just the vector statements into pointer form. No language model or person edits the sources.
  - zh: C 验证器 QCP 处理按值传递的向量时有缺陷，所以由一个确定性的规则工具只把涉及向量的语句改写成指针形式。源代码不由语言模型或人工修改。
- `Vek07Pipeline-3` (6.7 s)
  - en: QCP symbolically executes the annotated C and emits verification conditions, which agents then prove in Coq.
  - zh: QCP 对带标注的 C 代码做 symbolic execution，生成 verification condition，再由 agent 在 Coq 中证明。
- `Vek07Pipeline-4` (9.3 s)
  - en: Intrinsic calls resolve to one shared contract library, differentially tested against real instructions: natively for x86, under QEMU for NEON, RVV and Hexagon.
  - zh: intrinsic 调用统一对应一个共享的契约库，并与真实指令做差分测试：x86 在本机运行，NEON、RVV 和 Hexagon 在 QEMU 中运行。
- `Vek07Pipeline-5` (8.2 s)
  - en: The human-reviewed part is small: spec.c holds only equivalent, which runs both kernels on one input and relates their outputs.
  - zh: 需要人工审查的部分很小：spec.c 只包含函数 equivalent，它在同一输入上运行两个 kernel，并给出它们输出之间的关系。
- `Vek07Pipeline-6` (7.4 s)
  - en: Finally, check.py re-runs everything from an empty directory, and a package counts only if all twelve gates pass.
  - zh: 最后，check.py 在一个空目录中把一切从头重跑；只有十二道 gate 全部通过，这个包才算数。
- `Vek07Pipeline-7` (12.8 s)
  - en: When a proof fails, it becomes a concrete input, replayed on the original code, then triaged into an explicit condition, a minimal fix, or a recorded divergence. Our NaN took that path.
  - zh: 证明失败时，失败被转化为一个具体输入，在原始代码上重放，再分流为显式条件、最小修复或登记在案的分歧。我们的 NaN 走的就是这条路。

## 8. Vek08Gates  (~49 s)

**Purpose.** The 12 gates of check.py as a checklist, grouped as narrated.

**On screen.** Two columns of 6 rows: empty tick box, gate name (mono bold), short description (muted). Each group appears and is outlined (inputs g1–g4, proofs g5–g7, trust g8–g9 and g10–g11 in accent, tests g12).

**Code panels.** none

**Citations.** pkg24/proof/check.py docstring lines 4–17

**Narration.**

- `Vek08Gates-1` (10.9 s)
  - en: The twelve gates read like a checklist. The first four pin the inputs: sources identical to upstream, the rewrite regenerated byte for byte, libraries pinned and rebuilt.
  - zh: 这十二道 gate 就像一张检查清单。前四道固定输入：源代码与上游一致，改写结果逐字节重新生成，各个库固定版本并重新编译。
- `Vek08Gates-2` (8.6 s)
  - en: Then the proofs: every condition is closed with Qed, including the equivalence units, and Print Assumptions may list only whitelisted axioms.
  - zh: 接着是证明：每个 verification condition（包括等价性单元）都以 Qed 结束，Print Assumptions 只能列出白名单内的公理。
- `Vek08Gates-3` (11.3 s)
  - en: Next, trust checks: each kernel contract must be textually identical wherever it appears, and a scan rejects goals that a known QCP soundness bug could make vacuously true.
  - zh: 然后是信任检查：每个 kernel 契约在出现的每一处都必须文本一致；另有一次扫描，排除那些可能因 QCP 一个已知 soundness bug 而空洞成立的目标。
- `Vek08Gates-4` (12.4 s)
  - en: A concrete witness shows the precondition is satisfiable, so the proof is not about an empty input set, and every callee must be a proved body or a pinned library contract.
  - zh: 一个具体见证说明前置条件可以满足，因此证明讨论的不是空的输入集合。并且每个被调用函数都必须是已证明的函数体，或是固定版本的库契约。
- `Vek08Gates-5` (5.9 s)
  - en: Last, the library models and the two original kernels are tested against each other.
  - zh: 最后，库模型与两个原始 kernel 相互做测试比对。

## 9. Vek09Walk  (~55 s)

**Purpose.** Walk-through of the x24-transposec SSSE3 → RVV package: source, target, spec, conditions, observation.

**On screen.** Beat 1–2: SSSE3 panel, loads boxed (INFO), then unpack/shuffle lines, then loads boxed WARN with tag 'XNN_OOB_READS: 16-byte loads may over-read'. Beat 3: RVV panel, vsetvl line then the segment load/store lines boxed (accent), caption below. Beat 4: spec panel, the two kernel calls boxed. Beat 5: the box moves to the C-022, C-024, C-033 lines while WARN tags appear below the panel. Beat 6: outputs_related line boxed (accent) with its tag.

**Code panels.** examples/06_x24_source_ssse3.c (lines 2–5, 7–9 boxed); examples/07_x24_target_rvv.c (line 6, then 7–8 boxed); examples/08_x24_spec_equivalent.c (12–13, 5, 6–7, 8, 10 boxed)

**Citations.** pkg24/impl/, pkg24/spec.c, CONDITIONS

**Narration.**

- `Vek09Walk-1` (7.4 s)
  - en: Now one complete package, x24-transposec, which transposes blocks of three-byte pixels. The source is XNNPACK's x86 SSSE3 kernel.
  - zh: 现在看一个完整的包：x24-transposec，它转置由三字节像素构成的块。源程序是 XNNPACK 的 x86 SSSE3 kernel。
- `Vek09Walk-2` (9.7 s)
  - en: It works on four-by-four tiles with 16-byte loads, unpacks and byte shuffles. Its loads may read past the bytes it needs, which XNNPACK declares.
  - zh: 它按四乘四的 tile 工作，使用 16 字节加载、unpack 和字节 shuffle。它的加载可能读到所需字节之外，XNNPACK 对此做了声明。
- `Vek09Walk-3` (10.9 s)
  - en: The RVV target is new code. It handles one column per pass: vsetvl picks how many rows fit, and a strided segment load does the transpose itself.
  - zh: RVV 目标程序是新写的代码。它每一轮处理一列：vsetvl 决定能放下多少行，一条 strided segment load 本身就完成了转置。
- `Vek09Walk-4` (6.3 s)
  - en: The spec, equivalent, runs both kernels on the same input into two separate output buffers.
  - zh: spec 中的 equivalent 在同一个输入上运行两个 kernel，结果写入两个独立的输出缓冲区。
- `Vek09Walk-5` (13.6 s)
  - en: Its precondition names the conditions: blocks at least one by one, C-022, and the input window C-033, since x86 may read to the end of a 16-byte vector while RVV reads only a prefix.
  - zh: 它的前置条件写出了带编号的条件：块至少为一乘一，即 C-022；以及输入窗口 C-033，因为 x86 一侧可能读到 16 字节向量的末尾，而 RVV 只读其中的前缀。
- `Vek09Walk-6` (6.3 s)
  - en: The postcondition is outputs_related: the two outputs agree on every byte that a transpose writes.
  - zh: 后置条件是 outputs_related：两个输出在转置会写入的每一个字节上都一致。

## 10. Vek10Results  (~49 s)

**Purpose.** Results of the supervisor recheck for x24, with assumptions on screen.

**On screen.** Row of 12 green gate chips; 'RESULT: PASS · 12 / 12 gates · 5,990 s'. Beat 2: tiles '435 / x86 VCs, all Qed' and '22 per VLEN / RVV VCs at VLEN 128/256/512'. Beats 3–4: WARN 'assumptions' list (fixed VLEN set; C-022, C-024, C-031, C-033; G-004; G-002; modelling: 6 aligned const tables, NDEBUG). Beat 5: BAD line on out-of-domain edge cases 14/25.

**Code panels.** none

**Citations.** APPROVAL-x24-rvv.json; rechecks/w36x24/run/status.json; CONDITIONS G-rows

**Narration.**

- `Vek10Results-1` (9.3 s)
  - en: The supervisor re-ran check.py for this package from an empty directory. The record reports RESULT PASS: twelve of twelve gates, in 5,990 seconds.
  - zh: 监督者在一个空目录中为这个包重跑了 check.py。记录显示 RESULT PASS：十二道 gate 全部通过，用时 5,990 秒。
- `Vek10Results-2` (10.9 s)
  - en: QCP produced 435 verification conditions for the x86 kernel and 22 for the RVV kernel at each vector length, and all of them are closed in Coq.
  - zh: QCP 为 x86 kernel 生成了 435 个 verification condition，为 RVV kernel 在每个向量长度下各生成 22 个，全部在 Coq 中证完。
- `Vek10Results-3` (12.8 s)
  - en: The assumptions stay on screen. The result holds at three fixed vector lengths, 128, 256 and 512 bits, not at any length, and under conditions C-022, C-024, C-031 and the window C-033.
  - zh: 假设要始终留在屏幕上。结果只在三个固定向量长度 128、256 和 512 位下成立，并非任意长度，且依赖条件 C-022、C-024、C-031 和输入窗口 C-033。
- `Vek10Results-4` (10.5 s)
  - en: Globally, this is partial correctness, intrinsic semantics rest on reviewed contracts and tests rather than a formal ISA proof, and six constant tables are assumed aligned.
  - zh: 从全局看，这是部分正确性；intrinsic 的语义依赖经审查的契约和测试，而不是相对 ISA 的形式化证明；另外假设六个常量表是对齐的。
- `Vek10Results-5` (7.8 s)
  - en: Of 25 edge cases outside the domain, 14 behave differently, such as block width zero: exactly what C-022 excludes.
  - zh: 在定义域之外的 25 个边界用例中，有 14 个行为不同，例如块宽为 0：这正是 C-022 排除的输入。

## 11. Vek11Status  (~47 s)

**Purpose.** E1–E4 status as of 2026-11-23, labelled established / in progress / not started.

**On screen.** Four rows: key (accent), what it measures, detail line, status badge(s) on the right. E1 IN PROGRESS; E2 ESTABLISHED: 24 + IN PROGRESS; E3 ESTABLISHED: 15 + IN PROGRESS (as of 11-11, 3 planned pairs not started); E4 NOT STARTED. The cite changes per row.

**Code panels.** none

**Citations.** E1 APPROVAL files; DECISIONS-FOR-REVIEW 11-23; SUMMARY-20261111; EXPERIMENT-DESIGN

**Narration.**

- `Vek11Status-1` (15.5 s)
  - en: As of November 23, 2026: E1 asks whether LLM-optimised RVV kernels verify against their NEON originals without rewriting. It is in progress: 17 approval records so far, most keeping the main result that A is not equivalent to B-opt.
  - zh: 截至 2026 年 11 月 23 日：E1 研究 LLM 优化后的 RVV kernel 能否不经改写、相对 NEON 原版得到验证。它仍在进行中：目前有 17 份审批记录，多数保留了“A 与 Bopt 不等价”的主结果。
- `Vek11Status-2` (11.7 s)
  - en: E2 translates x86 operations that RVV and Hexagon lack and proves each translation: 24 approved migrations in the supervisor log, with a Hexagon port of x64-transposec still in progress.
  - zh: E2 把 RVV 和 Hexagon 缺少的 x86 操作翻译过去，并证明每次翻译：监督者日志记录了 24 个已批准的迁移，x64-transposec 的 Hexagon 移植仍在进行中。
- `Vek11Status-3` (12.0 s)
  - en: E3 cross-checks independent XNNPACK implementations of the same operator. As of November 11, 14 pairs were approved, one pair was proved not equivalent, and three planned pairs had not started.
  - zh: E3 交叉检查同一算子在 XNNPACK 中的不同独立实现。截至 11 月 11 日，有 14 对获批，一对被证明不等价，另有三对计划中的配对尚未开始。
- `Vek11Status-4` (8.6 s)
  - en: E4, one application-level program, with softmax as the candidate, has not started. So none of this is a program-level result yet.
  - zh: E4 针对一个应用级程序，候选是 softmax，目前尚未开始。所以以上都还不是程序级的结果。

## 12. Vek12Close  (~35 s)

**Purpose.** Limitations, then the series close: map with all tiles lit, what the counterexample was in each episode, the trust line.

**On screen.** Beat 1: WARN bullet list 'What Vekto does not claim'. Beat 2: series map all lit (no default caption), header 'what the counterexample was', one caption per tile in its accent. Beat 3: trust line below.

**Code panels.** none

**Citations.** CONDITIONS (G-004, VEKTO-M-ilp32, C-018); research/bugs/xnnpack/; docs/SERIES.md

**Narration.**

- `Vek12Close-1` (14.3 s)
  - en: Vekto does not claim termination or a link from C to machine code. Hexagon is modelled as 64-bit though it is 32-bit, in-place calls are not covered, and no bug found has been reported upstream yet.
  - zh: Vekto 不声称终止性，也不声称 C 与机器码之间的对应。Hexagon 是 32 位平台，却按 64 位建模；原地调用没有覆盖；发现的 bug 目前都还没有向上游报告。
- `Vek12Close-2` (14.0 s)
  - en: Across the series, the counterexample took four forms: a program state in ExVerus, a learned explanation in TopoVerus, an audit of a spec in Vero, and an input on which two kernels disagree in Vekto.
  - zh: 回顾整个系列，counterexample 有四种形态：ExVerus 中的程序状态，TopoVerus 中学到的解释，Vero 中对 spec 的审计，以及 Vekto 中让两个 kernel 产生分歧的输入。
- `Vek12Close-3` (6.7 s)
  - en: And one trust thread held throughout: every proof re-checked, no spec silently weakened, every assumption stated.
  - zh: 贯穿始终的是同一条信任主线：每个证明都被重新检查，没有任何 spec 被悄悄削弱，每个假设都明确写出。

## Open issues

1. **Numbers policy vs. E2/E3 counts.** docs/SERIES.md says Vekto numbers come only from APPROVAL/LEDGER files. E1's 17 is a count of `build/e1-codex-20261111/c*/APPROVAL*.json`. E2's "24 approved migrations" comes from the supervisor decision log (`DECISIONS-FOR-REVIEW.zh-CN.md`, 11-23 04:05, "E2 → 24", the entry that writes APPROVAL-x24-rvv.json), and E3's "14 approved + 1 proved not equivalent" comes from `SUMMARY-20261111.zh-CN.md` §2.2, not from a direct count of APPROVAL files. I did not recount them: `build/e2e3-workers-20261106` holds 46 APPROVAL*.json files mixing E2, E3, library and tool approvals. Labelled on screen as "supervisor log" / "as of 11-11". Supervisor: confirm, or drop the numbers and keep only the labels.
2. **C-001 conditional proof.** CONDITIONS row C-001 records it as passed and rechecked, but the evidence package is on an earlier server and cannot be re-run (SUMMARY-20261111 §2). Shown as a WARN badge with that caveat, never as a fresh result.
3. **vmax as motivating example.** The repo itself notes no confirmed speed advantage of Bopt over XNNPACK (0.982×) and a +18.8 % repair cost. The episode uses vmax as a correctness case only; it does not claim Bopt is fast. 0.982× / 0.826× are left off screen.
4. **Vero ↔ Vekto parallels** (Vek05-5, Vek12) are the research brief's [INFERRED] framing plus docs/SERIES.md's fixed lines; they need author confirmation.
5. **Vek03 lane picture.** a1–a3/b1–b3 are placeholders, not data. The only values shown are the counterexample's NaN and 1.0.
6. **Local helpers** not in common/components.py: `example()` (strip source header, split .v panels), `heading()`, `tag()`, `lane_box()/lane_row()`, `gate_row()/gate_grid()`, `status_row()`. `example()` and `heading()` would likely be reused by other episodes.
7. **code_panel frame offset.** When the title bar is wider than the code, `code_panel` centres the card on the wider body, so the card is narrower than the title (seen while building Vek05 and Vek09; worked around with shorter titles). Worth fixing in common/components.py.
8. **Draft Intro wording.** Quotes from Intro V2 (Vek05-5, Vek06) come from the draft bullet points, labelled "Intro V2, draft" on screen.
9. Not shown on screen, on purpose: the vclamp C-019 inconsistency (brief §10.3), the early 16 E1 pairs, worker costs, and the upstream bug list. None of the bugs has been reported upstream.
