# Vekto: storyboard

12 scenes, 49 beats, narration estimate about 7.0 min (words/2.6 + 0.5 s per beat; `tools/sync_durations.py` will replace it). Scene order = narration.json. All on-screen code is in `examples/`; every number carries a cite and is listed in SOURCES.md.

## 1. Vek01Open  (~23 s)

**Purpose.** Open: title card ("Vekto" + subtitle), the problem as framed in the Introduction (agents translate/optimise SIMD kernels; tests can be passed without preserving behaviour), then Vekto's question.

**On screen.** Title card centred (title + subtitle only). Then three centred lines (white / muted / BAD), dimmed when the accent question appears below: 'Do two kernels on different instruction sets give the same outputs for every input the spec's preconditions allow?'

**Code panels.** none

**Citations.** none (framing follows research/project-plan-20261102/intro-bullets/v2-preconditions.md ¶2–3)

**Narration.**

- `Vek01Open-1` (2.8 s)
  - en: Vekto: proving SIMD kernel migrations equivalent.
  - zh: Vekto：证明 SIMD kernel 迁移前后等价。
- `Vek01Open-2` (11.7 s)
  - en: Agents now translate and optimise SIMD kernels written with C intrinsics, and tests decide what is accepted. But a kernel can pass its tests and still change its behaviour.
  - zh: 如今 agent 会翻译和优化用 C intrinsic 写的 SIMD kernel，由测试决定是否接受。但一个 kernel 可以通过测试，却仍然改变了行为。
- `Vek01Open-3` (8.2 s)
  - en: Vekto asks whether two kernels on different instruction sets give the same outputs for every input the spec's preconditions allow.
  - zh: Vekto 要回答的是：两套指令集上的两个 kernel，在 spec 前置条件允许的每一个输入上，输出是否都相同。

## 2. Vek02Hook  (~37 s)

**Purpose.** Hook: a concrete failure in real code, the E1 f32-vmax NaN counterexample.

**On screen.** Left: two stacked code panels (A NEON, Bopt RVV), the max line of each boxed (INFO, then BAD). Right: state_table 'input, n = 1' (a[0]=0x7fc12345 NaN, b[0]=0x3f800000 1.0), state_table 'output[0]' (A NaN / Bopt 1.0 in BAD), badge 'A ≠ Bopt', note 'QEMU at VLEN 128/256/512; inputs swapped: same difference'.

**Code panels.** examples/01_vmax_neon_A_core.c (all 5 lines, line 4 highlighted); examples/02_vmax_rvv_Bopt_core.c (all 5 lines, line 4 highlighted)

**Citations.** final-minmax-reproduction/README.zh-CN.md; DIV-001

**Narration.**

- `Vek02Hook-1` (7.8 s)
  - en: Here is an XNNPACK kernel for Arm NEON: the element-wise maximum of two float arrays, four floats per step.
  - zh: 这是 XNNPACK 中一个 Arm NEON kernel：对两个 float 数组逐元素取最大值，每一步处理四个 float。
- `Vek02Hook-2` (8.2 s)
  - en: An LLM-driven pipeline, SALTy-RN, translated it to RISC-V Vector, RVV, and optimised it. We call this final optimised version B-opt.
  - zh: 一个由 LLM 驱动的流水线 SALTy-RN 把它翻译到 RISC-V Vector（RVV）并做了优化。我们把这个最终优化版本叫作 Bopt。
- `Vek02Hook-3` (6.7 s)
  - en: Give both kernels a single element: a quiet NaN with payload 0x7fc12345, and the number 1.0.
  - zh: 给两个 kernel 同一个单元素输入：一个带 payload 0x7fc12345 的 quiet NaN，和数字 1.0。
- `Vek02Hook-4` (6.7 s)
  - en: The NEON kernel returns the NaN. The optimised RVV kernel returns 1.0. Same input, different output.
  - zh: NEON kernel 返回 NaN，优化后的 RVV kernel 返回 1.0。同一个输入，不同的输出。
- `Vek02Hook-5` (7.4 s)
  - en: This reproduces under QEMU at vector lengths 128, 256 and 512 bits, with the inputs in either order.
  - zh: 这个结果在 QEMU 中、向量长度 128、256 和 512 位下都能复现，两个输入交换顺序也一样。

## 3. Vek03Lanes  (~34 s)

**Purpose.** Background: SIMD lanes and intrinsics, NEON fixed width vs RVV VLEN/vsetvl; locate the counterexample in lane 0.

**On screen.** Rows of lane boxes va = [NaN, a1, a2, a3], vb = [1.0, b1, b2, b3], arrows to vacc = [?, max, max, max]; label 'NEON: fixed 128-bit register = 4 × f32'; the intrinsic call in mono. Beat 3: an 8-lane RVV row (accent) with 'vl = vsetvl(n)'. Beat 4: lanes 1–3 dimmed, lane 0 outlined BAD, two output boxes NaN (A, NEON FMAX) and 1.0 (Bopt, RVV vfmax). a1/b1… are placeholders, not data.

**Code panels.** none (one intrinsic call shown as text, from examples/01 line 4)

**Citations.** none

**Narration.**

- `Vek03Lanes-1` (7.8 s)
  - en: Two terms first. SIMD, single instruction multiple data: one instruction works on a whole vector register, split into lanes.
  - zh: 先解释两个术语。SIMD 是单指令多数据：一条指令作用于整个向量寄存器，寄存器被分成若干 lane。
- `Vek03Lanes-2` (8.6 s)
  - en: An intrinsic is a C function for one such instruction: vmaxq_f32 takes the maximum of two four-float registers, lane by lane.
  - zh: intrinsic 是对应一条这类指令的 C 函数：vmaxq_f32 对两个各含四个 float 的寄存器逐 lane 取最大值。
- `Vek03Lanes-3` (9.3 s)
  - en: NEON registers have a fixed width. RVV's register width, VLEN, varies between chips, and the program asks vsetvl how many elements it gets.
  - zh: NEON 的寄存器宽度是固定的。RVV 的寄存器宽度 VLEN 因芯片而异，程序用 vsetvl 询问这次能处理多少个元素。
- `Vek03Lanes-4` (8.2 s)
  - en: In this counterexample only lane zero matters: NaN against 1.0. That one lane is where the two instruction sets disagree.
  - zh: 在这个 counterexample 中，只有第 0 个 lane 起作用：NaN 对 1.0。两套指令集正是在这一个 lane 上产生分歧。

## 4. Vek04Resolve  (~47 s)

**Purpose.** Why the kernels differ (intrinsic definitions), whether the counterexample is real, main result A ≠ Bopt, separate C-001 conditional result, measured cost of the repair.

**On screen.** Beat 1: two Coq panels (NEON FMAX, RVV vfmax) with NaN lines boxed and plain-language labels on the right. Beats 2–4: heading 'Is the counterexample real?' with two questions and answers ('Can the input occur?' / 'Which side is the reference?'); badge BAD 'main result: A ≠ Bopt (DIV-001)'; badge WARN 'conditional: A ≡ Bopt under C-001 (no NaN inputs)' + muted note 'proved under the precondition · counted separately'. Beat 5: the vfmax line transforms into the 5-line block titled 'Bopt with NaN repair' (lines 2–5 boxed WARN); '+18.8 % cycles', 'geometric mean over 7 sizes, Saturn RTL'.

**Code panels.** examples/03_fmax_lane_models.v panel 1 (lines 3–6 boxed) and panel 2 (lines 2–3 boxed); examples/04_vmax_bopt_nan_repair.c (line 1, then all 5; lines 2–5 boxed)

**Citations.** NeonLib.v, RvvModel.v; LESSONS L1/L3; DIV-001; CONDITIONS C-001; SUMMARY-20261111 §2; vmax-performance/REPORT

**Narration.**

- `Vek04Resolve-1` (10.1 s)
  - en: Why? Vekto gives every intrinsic an explicit definition. Arm FMAX propagates a NaN operand. RVV vfmax implements IEEE 754 maximumNumber, which ignores a single NaN.
  - zh: 为什么？Vekto 给每个 intrinsic 一个显式定义。Arm FMAX 会传播 NaN 操作数；RVV vfmax 实现 IEEE 754 的 maximumNumber，会忽略单个 NaN。
- `Vek04Resolve-2` (12.0 s)
  - en: Can this input occur? Yes: nothing on XNNPACK's call path checks for NaN. And XNNPACK does not guarantee how min and max treat NaN, so neither side is the reference.
  - zh: 这个输入会出现吗？会：XNNPACK 的调用路径上没有任何 NaN 检查。而且 XNNPACK 不保证 min 和 max 如何处理 NaN，所以哪一边都不是参考。
- `Vek04Resolve-3` (7.4 s)
  - en: So the result stands as found: the original A is not equivalent to B-opt, recorded as divergence DIV-001.
  - zh: 所以结果按原样成立：原始 A 与 Bopt 不等价，登记为分歧 DIV-001。
- `Vek04Resolve-4` (7.8 s)
  - en: Under an explicit precondition, C-001, no NaN inputs, the pair is proved equivalent. That conditional result is counted separately.
  - zh: 在显式前置条件 C-001（输入不含 NaN）下，这一对被证明等价。这个条件结果单独计数。
- `Vek04Resolve-5` (9.7 s)
  - en: Repairing B-opt to propagate NaN takes four statements after each vfmax and costs 18.8 percent more cycles on Saturn RTL, as a geometric mean.
  - zh: 修复 Bopt 让它传播 NaN，需要在每个 vfmax 之后加四条语句；在 Saturn RTL 上，周期数增加 18.8%（几何平均）。

## 5. Vek05Testing  (~31 s)

**Purpose.** Why tests and a bounded checker missed it; Vekto's goal (Introduction ¶3).

**On screen.** Three numbered rows (red numerals) with source lines; row 1 appears with the heading. Under row 3 the checker-model diff panel; badges 'VERIFIED' (struck through) → 'COUNTEREXAMPLE'. Beat 4: 'Vekto's goal' and the quoted goal sentence.

**Code panels.** examples/05_bounded_checker_patch.diff (all 6 lines)

**Citations.** XNN-005, XNN-003, final-minmax-reproduction README, v2-preconditions.md ¶3

**Narration.**

- `Vek05Testing-1` (8.6 s)
  - en: Why didn't the checks catch this? First, XNNPACK's random test buffers replace NaN with zero, so its NaN assertion never fires.
  - zh: 为什么检查没有发现它？第一，XNNPACK 的随机测试缓冲区会把 NaN 替换成 0，所以它的 NaN 断言从未触发。
- `Vek05Testing-2` (7.4 s)
  - en: Second, QEMU leaves RVV tail lanes unchanged by default, which hides a tail-lane bug, XNN-003, from XNNPACK's tests.
  - zh: 第二，QEMU 默认保持 RVV 尾部 lane 不变，这让一个尾部 lane bug（XNN-003）在 XNNPACK 的测试中无法暴露。
- `Vek05Testing-3` (9.3 s)
  - en: Third, SALTy-RN's bounded checker said VERIFIED for this pair, because its NEON model ignored NaN; with the model fixed, it finds the counterexample.
  - zh: 第三，SALTy-RN 的有界检查器对这一对给出了 VERIFIED，因为它的 NEON 模型忽略了 NaN；修正模型之后，它就找到了这个 counterexample。
- `Vek05Testing-4` (5.9 s)
  - en: Vekto's goal is equivalence for all inputs permitted by the preconditions in the spec.
  - zh: Vekto 的目标是：对 spec 前置条件允许的所有输入证明等价。

## 6. Vek06Level  (~29 s)

**Purpose.** Why C-level equivalence: three levels, assembly drawbacks, C with reviewed intrinsic definitions.

**On screen.** Three cards: 'Assembly / ISA' (Sail, Islaris), 'Compiler IR' (Alive2, Rake), 'C + semantic shims' (Vekto). Beat 2: WARN bullets under assembly. Beat 3: accent bullets under C; the others dim.

**Code panels.** none

**Citations.** Intro V2 ¶4–5

**Narration.**

- `Vek06Level-1` (8.2 s)
  - en: Where should such a proof live? There are three candidate levels: assembly with ISA models, a compiler IR, or C.
  - zh: 这样的证明应该放在哪一层？有三个候选层次：带 ISA 模型的汇编、编译器 IR，或者 C。
- `Vek06Level-2` (10.1 s)
  - en: At the assembly level, NEON and RVV need separate ISA models plus a correspondence between them, and those models also cover exceptions and privileged execution.
  - zh: 在汇编层，NEON 和 RVV 需要各自的 ISA 模型以及两者之间的对应关系；这些模型还涵盖异常处理和特权执行。
- `Vek06Level-3` (10.9 s)
  - en: Vekto works at the C level. Each supported intrinsic gets an explicit C definition of its numerical and memory behaviour, which experts review against the ISA documentation.
  - zh: Vekto 在 C 层工作。每个支持的 intrinsic 都有一个显式的 C 定义，描述其数值行为和内存行为，由专家对照 ISA 文档审查。

## 7. Vek07Pipeline  (~57 s)

**Purpose.** Architecture diagram built step by step; the failure path (VCs → counterexample → expert review → spec) pulsed at the end.

**On screen.** Middle row: impl/ → rule tool → QCP → VCs → Coq; above QCP: C semantic shims ← differential tests; below QCP: spec.c ('equivalent(): expert-reviewed', accent); below Coq: check.py (12 gates → APPROVAL, OK); bottom: counterexample (BAD) → expert review ('precondition · repair · divergence', WARN) → spec.c. Beat 2 adds a muted note on the rule tool. Beat 7 pulses VCs → counterexample → expert review → spec.

**Code panels.** none

**Citations.** tools/rvv_ptr_lower/README.zh-CN.md; INTRINSICS-COMMON.zh-CN.md; pkg24/README.md

**Narration.**

- `Vek07Pipeline-1` (5.9 s)
  - en: Here is the Vekto pipeline. It starts from the original kernels, byte-identical to upstream.
  - zh: 这是 Vekto 的流水线。它从原始 kernel 出发，它们与上游逐字节一致。
- `Vek07Pipeline-2` (7.8 s)
  - en: Because QCP mishandles vectors passed by value, a deterministic rule tool rewrites only the vector statements into pointer form.
  - zh: 由于 QCP 处理按值传递的向量时有缺陷，一个确定性的规则工具只把涉及向量的语句改写成指针形式。
- `Vek07Pipeline-3` (6.7 s)
  - en: QCP symbolically executes the annotated C and emits verification conditions, which agents then prove in Coq.
  - zh: QCP 对带标注的 C 代码做 symbolic execution，生成 verification condition，再由 agent 在 Coq 中证明。
- `Vek07Pipeline-4` (8.6 s)
  - en: Intrinsic calls resolve to one shared library of C semantic shims, differentially tested against the real instructions, natively or under QEMU.
  - zh: intrinsic 调用统一对应一个共享的 C semantic shim 库，并与真实指令做差分测试，在本机或 QEMU 中运行。
- `Vek07Pipeline-5` (9.7 s)
  - en: Experts review only the equivalence spec and the verification feedback. The spec's function, equivalent, runs both kernels on one input and relates their outputs.
  - zh: 专家只需审查等价性 spec 和验证反馈。spec 中的函数 equivalent 在同一输入上运行两个 kernel，并给出它们输出之间的关系。
- `Vek07Pipeline-6` (7.0 s)
  - en: check.py re-runs everything from an empty directory, and a package counts only if all twelve gates pass.
  - zh: check.py 在一个空目录中把一切从头重跑；只有十二道 gate 全部通过，这个包才算数。
- `Vek07Pipeline-7` (11.3 s)
  - en: When a proof fails, the failure becomes a concrete input, replayed on the original code. Experts then add a missing precondition, guide a repair, or record a divergence.
  - zh: 证明失败时，失败被转化为一个具体输入，并在原始代码上重放。专家随后补上缺失的前置条件、指导修复，或登记一条分歧。

## 8. Vek08Gates  (~11 s)

**Purpose.** The 12 gates of check.py as a checklist, in one beat.

**On screen.** Two columns of 6 rows: empty tick box, gate name (mono bold), short description (muted). Groups appear and are outlined in turn: inputs g1–g4, proofs g5–g7 (INFO), trust and tests g8–g12 (accent).

**Code panels.** none

**Citations.** pkg24/proof/check.py docstring lines 4–17

**Narration.**

- `Vek08Gates-1` (11.3 s)
  - en: The twelve gates pin the sources and libraries, require every condition closed with Qed and only whitelisted axioms, and check contracts, callees, a satisfiable precondition, and differential tests.
  - zh: 十二道 gate 固定源代码和库，要求每个 condition 都以 Qed 结束且只用白名单公理，并检查契约、被调用函数、前置条件可满足性以及差分测试。

## 9. Vek09Walk  (~51 s)

**Purpose.** Walk-through of the x24-transposec SSSE3 → RVV package: source, target, spec, conditions, observation.

**On screen.** Beat 1–2: SSSE3 panel, loads boxed (INFO), then unpack/shuffle lines, then loads boxed WARN with tag 'XNN_OOB_READS: 16-byte loads may over-read'. Beat 3: RVV panel, vsetvl line then the segment load/store lines boxed (accent), caption below. Beat 4: spec panel, the two kernel calls boxed. Beat 5: the box moves to the C-022, C-024, C-033 lines while WARN tags appear below the panel. Beat 6: outputs_related line boxed (accent) with its tag.

**Code panels.** examples/06_x24_source_ssse3.c (lines 2–5, 7–9 boxed); examples/07_x24_target_rvv.c (line 6, then 7–8 boxed); examples/08_x24_spec_equivalent.c (12–13, 5, 6–7, 8, 10 boxed)

**Citations.** pkg24/impl/, pkg24/spec.c, CONDITIONS

**Narration.**

- `Vek09Walk-1` (7.4 s)
  - en: Now one complete package: x24-transposec, which transposes blocks of three-byte pixels. The source is XNNPACK's x86 SSSE3 kernel.
  - zh: 现在看一个完整的包：x24-transposec，它转置由三字节像素构成的块。源程序是 XNNPACK 的 x86 SSSE3 kernel。
- `Vek09Walk-2` (7.4 s)
  - en: It works on four-by-four tiles with 16-byte loads, unpacks and shuffles; XNNPACK declares that these loads may over-read.
  - zh: 它按四乘四的 tile 工作，使用 16 字节加载、unpack 和 shuffle；XNNPACK 声明这些加载可能越界读取。
- `Vek09Walk-3` (9.7 s)
  - en: The RVV target is new code: one column per pass, vsetvl picks how many rows fit, and a strided segment load does the transpose.
  - zh: RVV 目标程序是新写的代码：每一轮处理一列，vsetvl 决定能放下多少行，一条 strided segment load 完成转置。
- `Vek09Walk-4` (6.3 s)
  - en: The spec, equivalent, runs both kernels on the same input into two separate output buffers.
  - zh: spec 中的 equivalent 在同一个输入上运行两个 kernel，结果写入两个独立的输出缓冲区。
- `Vek09Walk-5` (14.0 s)
  - en: The precondition names its conditions: blocks of at least one by one, C-022; no address wrap, C-024; and the input window, C-033, because x86 may read a full 16-byte vector where RVV reads a prefix.
  - zh: 前置条件写出了带编号的条件：块至少为一乘一（C-022）；地址不回绕（C-024）；以及输入窗口（C-033），因为 x86 可能读满一个 16 字节向量，而 RVV 只读其前缀。
- `Vek09Walk-6` (6.3 s)
  - en: The postcondition is outputs_related: the two outputs agree on every byte that a transpose writes.
  - zh: 后置条件是 outputs_related：两个输出在转置会写入的每一个字节上都一致。

## 10. Vek10Results  (~39 s)

**Purpose.** x24 package result from the clean-directory check.py run, with the conditions the claim depends on.

**On screen.** Row of 12 green gate chips; 'PASS · 12 / 12 gates · 5,990 s'. Beat 2: tiles '435 / x86 VCs, all Qed' and '22 per VLEN / RVV VCs at VLEN 128/256/512'. Beats 3–4: WARN list headed 'holds under' (VLEN 128/256/512; C-022, C-024, C-031, C-033; partial correctness G-004; intrinsics = reviewed C definitions + differential tests G-002; 6 const tables modelled 16-byte aligned, NDEBUG). Beat 5: BAD line on out-of-domain edge cases 14/25.

**Code panels.** none

**Citations.** APPROVAL-x24-rvv.json; rechecks/w36x24/run/status.json; CONDITIONS G-rows

**Narration.**

- `Vek10Results-1` (6.3 s)
  - en: check.py re-ran this package from an empty directory: all twelve gates pass, in 5,990 seconds.
  - zh: check.py 在一个空目录中重跑了这个包：十二道 gate 全部通过，用时 5,990 秒。
- `Vek10Results-2` (8.2 s)
  - en: QCP produced 435 verification conditions for the x86 kernel and 22 per vector length for RVV, all closed in Coq.
  - zh: QCP 为 x86 kernel 生成了 435 个 verification condition，为 RVV 在每个向量长度下各生成 22 个，全部在 Coq 中证完。
- `Vek10Results-3` (7.4 s)
  - en: The result holds at vector lengths 128, 256 and 512 bits, under conditions C-022, C-024, C-031 and C-033.
  - zh: 结果在向量长度 128、256 和 512 位下成立，前提是条件 C-022、C-024、C-031 和 C-033。
- `Vek10Results-4` (9.7 s)
  - en: It is a partial-correctness result. The intrinsic definitions rest on reviewed contracts and differential tests, and six constant tables are modelled as 16-byte aligned.
  - zh: 这是一个部分正确性结果。intrinsic 定义以经审查的契约和差分测试为依据；六个常量表按 16 字节对齐建模。
- `Vek10Results-5` (7.4 s)
  - en: Outside the domain, 14 of 25 edge cases behave differently, such as block width zero, which C-022 excludes.
  - zh: 在定义域之外的 25 个边界用例中，有 14 个行为不同，例如块宽为 0，这正是 C-022 排除的输入。

## 11. Vek11Status  (~35 s)

**Purpose.** E1–E4 status as of 2026-11-23, labelled established / in progress / not started; tasks named as in the Introduction ¶8–9.

**On screen.** Heading 'Experiments E1–E4 · 2026-11-23'. Four rows: key (accent), task, detail line, status badge(s). E1 'verify optimised kernels' IN PROGRESS, '17 pairs approved: 13 A ≠ Bopt, 4 A ≡ Bopt (one under C-005)'; E2 'translate x86 kernels to RVV / HVX libraries that lack them' ESTABLISHED: 24 + IN PROGRESS, detail includes 'HVX modelled with 64-bit pointers'; E3 'cross-check independent XNNPACK implementations' ESTABLISHED: 15 + IN PROGRESS; E4 NOT STARTED. Beat 3 adds a muted footer: E2/E3 element-wise kernels assume disjoint buffers, no in-place calls (C-018). The cite changes per row.

**Code panels.** none

**Citations.** E1 APPROVAL files (status fields); DECISIONS-FOR-REVIEW 11-23; CONDITIONS [VEKTO-M-ilp32], C-018; SUMMARY-20261111; EXPERIMENT-DESIGN

**Narration.**

- `Vek11Status-1` (10.5 s)
  - en: E1 checks LLM-optimised RVV kernels against their 35 NEON originals and is in progress: of 17 approved pairs, 13 are not equivalent and 4 are equivalent.
  - zh: E1 检查 LLM 优化后的 RVV kernel 与其 35 个 NEON 原版是否等价，仍在进行中：已批准的 17 对中，13 对不等价，4 对等价。
- `Vek11Status-2` (10.1 s)
  - en: E2 translates x86 operations missing from RVV and Hexagon libraries, each with a proof: 24 migrations are approved, and one Hexagon port is in progress.
  - zh: E2 把 RVV 和 Hexagon 库中缺少的 x86 操作翻译过去，并逐个证明：已批准 24 个迁移，另有一个 Hexagon 移植仍在进行中。
- `Vek11Status-3` (9.3 s)
  - en: E3 cross-checks independent XNNPACK implementations of one operator: 14 pairs are approved and one is proved not equivalent; three pairs have not started.
  - zh: E3 交叉检查同一算子在 XNNPACK 中的不同独立实现：14 对已批准，一对被证明不等价；另有三对尚未开始。
- `Vek11Status-4` (5.1 s)
  - en: E4, an application-level program with softmax as the candidate, has not started.
  - zh: E4 针对一个应用级程序，候选是 softmax，目前尚未开始。

## 12. Vek12Close  (~24 s)

**Purpose.** Vekto's own takeaway.

**On screen.** Heading 'Takeaway' (accent). Beat 1: chain of three cards: 'two SIMD kernels' → 'C program verification' (reviewed C definition per intrinsic) → 'QCP + Coq' (same outputs on every allowed input). Beat 2: second chain 'proof fails' (concrete input) → 'f32-vmax' (NaN vs 1.0) → 'expert review' (precondition · repair · divergence), then 'never a weaker spec' in accent.

**Code panels.** none

**Citations.** none

**Narration.**

- `Vek12Close-1` (11.7 s)
  - en: Vekto turns SIMD kernel equivalence into C program verification: each intrinsic has a reviewed C definition, and QCP and Coq prove equal outputs for every input the spec allows.
  - zh: Vekto 把 SIMD kernel 的等价性变成 C 程序验证：每个 intrinsic 都有经审查的 C 定义，QCP 和 Coq 证明在 spec 允许的每个输入上输出相同。
- `Vek12Close-2` (12.4 s)
  - en: When a proof fails, the result is a concrete input, like the NaN in f32-vmax. It leads to a precondition, a repair, or a recorded divergence, never to a weaker spec.
  - zh: 证明失败时，得到的是一个具体输入，比如 f32-vmax 中的 NaN。它会引出一个前置条件、一次修复或一条登记在案的分歧，而不是一个被削弱的 spec。

## Open issues

1. **E2/E3 counts.** The author confirmed (2026-11-23) that E2 = 24 approved migrations and E3 = 14 approved + 1 proved not equivalent are shown as approved results.
2. **C-001 conditional result.** CONDITIONS row C-001 records the conditional pairing as passed and rechecked by the supervisor; shown as a WARN badge, counted separately from the main result.
3. **vmax as motivating example.** The repo notes no confirmed speed advantage of Bopt over XNNPACK (0.982×) and a +18.8 % repair cost. The video uses vmax as a correctness case only; it does not claim Bopt is fast. 0.982× / 0.826× are left off screen.
4. **Vek03 lane picture.** a1–a3/b1–b3 are placeholders, not data. The only values shown are the counterexample's NaN and 1.0.
5. **Local helpers** not in common/components.py: `example()`, `heading()`, `tag()`, `lane_box()/lane_row()`, `gate_row()/gate_grid()`, `status_row()`.
6. **code_panel frame offset.** When the title bar is wider than the code, `code_panel` centres the card on the wider body (worked around with shorter titles).
7. Not shown on screen, on purpose: the vclamp C-019 inconsistency, the early 16 E1 pairs, worker costs, and the upstream bug list.

## Revision 2026-11-23

Following docs/REVISION-BRIEF.md (video self-contained, no hedges, Introduction V2 framing):

- **Vek01Open:** removed "Episode four", the "unpublished work in progress / status report" line, the series map and the recap. Title card shows "Vekto" and its subtitle only. New hook framing from Introduction ¶2–3 (agents optimise intrinsic kernels; tests can be passed without preserving behaviour) and Vekto's question.
- **Vek04Resolve:** "lane model" → "explicit definition"; triage heading/answers rephrased plainly; removed "early evidence cannot be re-run here" and "tested, not proved"; repair panel retitled "Bopt with NaN repair".
- **Vek05Testing:** removed the "Vero's lesson again" analogy and its on-screen line; merged the intro beat into item 1 (5 → 4 beats); goal quote without "(Intro V2, draft)".
- **Vek06Level / Vek07Pipeline:** terms aligned with Introduction ¶4–7 ("C semantic shims", experts review the equivalence spec and verification feedback, precondition / repair / divergence instead of "L1/L3 triage"); shorter narration.
- **Vek08Gates:** 5 beats → 1 beat (same 12-gate grid).
- **Vek09Walk:** narration tightened; C-024 now named in narration as well as on screen.
- **Vek10Results:** "supervisor recheck" / "assumptions stay on screen" / "not at any length" removed; conditions shown under "holds under".
- **Vek11Status:** tasks named as in the Introduction; E1 detail now 13 not equivalent / 4 equivalent of 17 approved (from the APPROVAL status fields); HVX 64-bit-pointer modelling (VEKTO-M-ilp32) and C-018 (no in-place calls) kept, as the E2/E3 claims depend on them; removed "none of this is a program-level result yet".
- **Vek12Close:** removed the "does not claim" list, the four-forms-of-counterexample series close and the trust thread; replaced by Vekto's own takeaway (two beats).
- Total: 12 scenes, 49 beats, about 7.0 min (was 55 beats, about 9.0 min).
