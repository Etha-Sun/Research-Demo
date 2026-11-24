# Vekto — research brief for the explainer video (final episode: ExVerus → TopoVerus → Vero → Vekto)

**What Vekto is.** Vekto is an in-progress research project. It checks that a SIMD kernel and its port to another ISA compute the same outputs for every input allowed by an explicit, human-reviewed precondition. The ports covered are ARM NEON or x86 SSE/AVX to RISC-V Vector (RVV) or Hexagon HVX. The check works at the C level: each intrinsic gets a C contract, QCP (symbolic execution for separation logic) turns the annotated C into verification conditions (VCs), and Coq proves them. The repository is on branch `vekto`. There is no paper yet: the Introduction exists as bullet points (V2), and the LaTeX intro is being written on Overleaf (`research/project-plan-20261102/intro-bullets/CHANGELOG.md`).

**How this brief was made.** I read the repository's planning files, condition register, bug records, approval files, one complete package and its supervisor recheck output. I ran nothing: no QCP, Coq, `check.py`, QEMU or compiler. Most sources are in Chinese, and every translation here is mine. Each number names its file. `sources.json` maps each claim to a file and locator. Code is in `examples/`: every file begins with its repo-relative source, and screen-simplified versions are labelled and sit next to the verbatim originals.

**Status labels used below.** **[ESTABLISHED]** means a supervisor recheck passed and an APPROVAL record exists. **[IN PROGRESS]** means the work is not finished. **[ASSUMPTION]** means a modelling or trust premise that the work does not prove. **[PLANNED]** means a design that is not yet executed. **[INFERRED]** means my own reading of the sources.

---

## 1. Problem

### 1.1 Why SIMD migrations are risky
- **The same operation is written many times.** "The same operator has to be hand-written separately for NEON (ARM), AVX (x86), RVV (RISC-V), HVX (Hexagon)" (`SUMMARY-20261111.zh-CN.md` §1). Paragraph 2 of Intro V2 says the execution models differ: "NEON uses fixed-width vectors, while RVV selects the active vector length at runtime" (`intro-bullets/v2-preconditions.md`, ¶2).
- **Agents now write and optimise kernels, and they can game the tests.** Intro V2 ¶3: "Agents may exploit gaps in test coverage, passing tests without preserving the intended behavior." E1 verifies 35 RVV kernels that an agent pipeline (SALTyRN/Autocomp, Keagan Chern) optimised from NEON originals (`EXPERIMENT-DESIGN.zh-CN.md`, E1).
- **The differences hide in corner cases.** In practice they show up at NaN, at the tail lanes of a vector, at saturation and rounding, and at out-of-bounds windows. §5 gives real examples. One of them changes behaviour only on some legal RVV implementations (XNN-003).

### 1.2 Why check equivalence at the C level
Intro V2 ¶4–5 compares three levels: assembly or ISA models (Sail/Islaris), IR (Alive2, Rake), and C with semantic shims.
- Assembly would need separate ISA models for fixed-width SIMD and for vector-length-agnostic execution, plus a correspondence between them. Those models also cover exception handling and privileged execution, which kernel verification does not need (¶5).
- At the C level "we give each supported intrinsic an explicit C definition of its numerical and memory behavior", and "human experts review these definitions against ISA documentation" (¶5). The project's earlier assembly-level line (Sail/Islaris) is background now (`AGENTS.md`).

### 1.3 Why testing alone is not enough (evidence from this repository)
- **Tests never exercise some inputs.** XNNPACK's random test buffers replace NaN with 0, so the tester's NaN assertion never fires on NaN inputs (`research/bugs/xnnpack/XNN-005…/README.zh-CN.md`, supplement §6).
- **The emulator hides some behaviour.** QEMU keeps RVV tail lanes unchanged by default, "so XNNPACK's own tests on QEMU do not expose" the XNN-003 accumulator bug (`XNN-003…/README.zh-CN.md` §4).
- **A bounded checker can be wrong too.** For the final vmax pair, the earlier SALTyRN cvc5 bounded backend returned VERIFIED because its NEON model of `vmaxq_f32` ignored NaN propagation. With the model fixed, the same harness returned a counterexample (`final-minmax-reproduction/README.zh-CN.md`, "bounded 检查对照及机制"; `examples/02g_*`).
- **Goal (Intro V2 ¶3):** "establish equivalence for all inputs permitted by the preconditions in the spec". This is stronger than bounded equivalence checking.

---

## 2. Approach

### 2.1 Separate the implementation, the spec and the proof
- Each package has `impl/` with the original sources (byte-identical, sha256 in `ledger.json`), `spec.c` holding **only** `equivalent()`, which is the part a human reviews, and `proof/` with the bridge contracts, the rule-tool output, units, Coq and `check.py` (`…/pkg24/README.md`).
- `equivalent()` calls kernel A and kernel B on the **same** input with **separate** output buffers. Its Ensure states `outputs_related(...)` between the two results (`examples/01c_*`).
- Each kernel separately has a functional contract. For the transpose, both contracts say the output equals `xt_result(3, IN, OLD, …)` (`examples/01e_*`). Equivalence therefore follows from the two kernel proofs plus one relational lemma (`examples/01h_*`).
- `QCP-MODULAR-VERIFICATION.zh-CN.md` §3 warns that a wrapper proof alone, with no proved kernel bodies, is only conditional. Gate g11 below closes that gap.

### 2.2 Rewrite sources with deterministic rules, not by hand or LLM
- **Why it is needed.** QCP 2.1.4 has two bugs with vectors passed by value: stale resources remain when a by-value argument is also written to the heap, and by-value return temporaries are never freed. Passing vectors through pointers was proved end to end (`tools/rvv_ptr_lower/README.zh-CN.md`, "为什么需要").
- **User rule (2026-11-04).** Source rewrites that work around QCP defects must come from a rule-based deterministic tool. They must not be made by an LLM or a worker by hand (README header).
- **Design.** The tool is driven by the typed clang 20.1.2 AST. It changes only statements that involve vector values. It rejects any construct outside its rule table instead of guessing, and its output is deterministic. Each rule names its semantic justification. The table runs from R1 (`T v = f(args);` → `T v; qcp_p_f(&v, args');`) up to about R67 (README).
- **x24 example.** There are exactly 2 rewrites, R1 and R6/R8, and 0 rejections (`examples/01f_*`). Gate g2 regenerates the lowered files with the pinned tool (sha256 in the ledger) and requires byte equality.
- **Tool releases are rechecked.** v1.23.10 passed 713/713 fixtures in the supervisor recheck on 11-23 (`DECISIONS-FOR-REVIEW.zh-CN.md`, 11-23 09:30 entry).

### 2.3 Unified intrinsic contract library with differential testing
- **Why a shared library.** Before it existed, the 16 approved packages contained 331 contracted functions. 103 of them appeared in two or more packages, and 78 of those 103 were written differently, sometimes with different semantics (`intrinsics-v1.7.3/INTRINSICS-COMMON.zh-CN.md`, 背景).
- **What the library requires.** One contract per intrinsic. Registers are modelled as bit lanes. Floating point follows real hardware behaviour, including NaN sign and payload. Where hardware behaviour is not unique, the contract is a relation. Every lane function is differentially tested against real instructions: native gcc for x86, qemu-aarch64 for NEON, qemu-riscv64 at VLEN 128/256/512 for RVV, and qemu-hexagon for HVX (same file, 交付物 2 and 4).
- **Example.** `rv_fmax` is IEEE 754-2019 maximumNumber, while `nl_fmax` is Arm FMAX and propagates NaN (`examples/02e_*`). The strided segment-load contract leaves tail lanes as an arbitrary list `T`, which models tail-agnostic behaviour (`examples/01g_*`).
- **Workers may not write contracts.** Missing intrinsics go to a library maintainer, and the supervisor rechecks the result (`build/e1-codex-20261111/E1-COMMON.zh-CN.md`, 复用来源 1).

### 2.4 QCP → VCs → Coq
- The VC kinds are safety, entailment at calls, loop entry, loop preservation, return and partial_solve (`QCP-MODULAR-VERIFICATION.zh-CN.md` §4).
- **x24 package scale [ESTABLISHED].** QCP symbolic execution of 4 units produced 435 x86 VCs and 22 RVV VCs at each of the three VLENs, all proved. The equivalence unit is proved at VLEN 128, 256 and 512 (`examples/01i_*`, gates g5–g7).
- **x8 package scale.** 863 x86 VCs and 105 RVV VCs per VLEN (`examples/01k_*`).

### 2.5 The 12 gates of `check.py` (x24 package)
From the `proof/check.py` docstring (`…/pkg24/proof/check.py` lines 4–17). The run must start in an EMPTY run directory, and `--stages` or `--dev-reuse` runs are "never a pass".

| Gate | What it checks |
|---|---|
| g1 identity | sources are byte-identical to the pinned XNNPACK checkout and to the ledger; the frozen target and shim tree match |
| g2 lowering | the pinned rule tool regenerates `proof/lowered`, byte-equal apart from version strings |
| g3 pins | intrinsic library, tool and Coq library copies match the ledger |
| g4 libs | Coq libraries compile from scratch |
| g5 units | annotated units regenerate with only comments added; QCP symbolic execution |
| g6 proofs | every VC proved with Qed; `VC_Correct` modules; **Print Assumptions shows only whitelisted axioms** |
| g7 equivalence | the three `equivalent()` units (QCP + Qed) |
| g8 contracts | each kernel's contract text in the proved unit == the equivalence-unit declaration == the committed bridge text (**contract equality**) |
| g9 b1 | scan of every goal: no VC whose left-hand side has a duplicate address. This guards against the QCP soundness bug QCP-B1, which can make goals vacuously true |
| g10 witness | **non-vacuity**: the Require of `equivalent()` is satisfiable, with a concrete witness at every VLEN |
| g11 closure | **call closure**: every callee is either a proved body or a pinned library contract; proved bodies contain only tool-output tokens |
| g12 difftests | the library drivers (x86 native, RVV under QEMU) and the two ORIGINAL kernels tested against each other |

**Axiom whitelist.** Five Coq stdlib axioms, the QCP 2.1.4 C-model parameters and axioms, and `Hsz` (`sizeof(__m256i)=32`). The user approved all of them on 11-07 and 11-09. One QCP axiom, `addr_of_arrow_field_inv`, is **forbidden**: the supervisor showed by machine-checked proof that, together with the other axioms, it derives False (`examples/01j_*`; `research/bugs/qcp/QCP-B2…`).

### 2.6 Process and roles
- A supervisor agent manages independent CLI worker processes: Codex (GPT) for E1 and Claude Sonnet for E2 (`DECISIONS-FOR-REVIEW.zh-CN.md`, 11-13 entry).
- Every result counts only after the supervisor rechecks it from an empty directory (`SUMMARY-20261111.zh-CN.md` §1).
- Time and tokens are logged per kernel, including failures (`KERNEL-EXECUTION-POLICY.zh-CN.md` §1, §4).
- **Example cost.** Worker w36, which did the x8/x16/x24/x64 transposec packages and HVX, has 94.02 wall-clock hours and an estimated **$3,277.58** at API prices. That figure is marked as a lower bound and is not actual billing (`build/e2e3-workers-20261106/LEDGER.md`, w36 row and header).

---

## 3. Experiments E1–E4 (dates are 2026)

| | What it measures | Status |
|---|---|---|
| **E1** | 35 pairs: original NEON **A** (SALTy-rn `be16280c7`) vs the agent-optimised RVV **Bopt** (`optimized-rvv-kernels@80feb4564`). Question: is the optimisation verifiable without rewriting it? (`EXPERIMENT-DESIGN.zh-CN.md`) | **Mixed.** 16 pairs were done in the early period (11-05), but that evidence is on an earlier server that is no longer available and cannot be re-run here (`SUMMARY-20261111` §2). The Codex batch has 17 APPROVAL records (`build/e1-codex-20261111/c*/APPROVAL*.json`). Most have the main result "original A ≠ Bopt" plus a conditional or fixed-variant equivalence; c09, c11 and c14 are original A == original Bopt. c02, c04 and c18 are "approved as REFUTED". c06 dwconv2d-chw: not equivalent on finite input, reproduced in C/QEMU only, with no APPROVAL file (`DECISIONS…` 11-12). c03 f32-gemm: QCP generation was killed twice (a 43,200 s timeout, then a user-manager stop). **The user decided on 11-23 not to re-run it** (`DECISIONS…`, last lines). Performance: only vmax was measured on Saturn RTL (§5.1). |
| **E2** | Translate AVX/SSE operations that RVV/HVX lack in XNNPACK `867d5a34` into new RVV/HVX code, and prove the translation. A migration to RVV and one to HVX count as two migrations (user, 11-13) | **[ESTABLISHED] 24 approved migrations** as of 11-23 04:05 (`DECISIONS…`, "E2 → 24"). The first 5 operations (vsigmoid, ibilinear, velu, x8-lut incl. HVX, qs8-vprelu) were done by 11-11 (`SUMMARY-20261111` §2.1). x64 HVX transposec is **[IN PROGRESS]**: 484 of 529 non-entail VCs Qed at 11-23 14:20 (`DECISIONS…`). |
| **E3** | Cross-check independent XNNPACK implementations of the same operator, e.g. NEON vs AVX vs RVV vs HVX. Bugs are a by-product (user, 11-05) | **[ESTABLISHED as of 11-11] 14 pairs approved**, most with conditions or fixed variants, **plus 1 proved not equivalent** (f32-vcmul, a 1-ulp FMA difference) (`SUMMARY-20261111` §2.2). Bug records XNN-001…008 are in `research/bugs/xnnpack/`. None has been reported upstream; external reports need the user's consent. |
| **E4** | One application-level program, NEON → RVV. Softmax is the candidate, not yet frozen | **[PLANNED] not started** (`SUMMARY-20261111` §2). I found no later start record. |

The paper's planned numbers are still "[TBD]" in Intro V2 ¶9.

---

## 4. Architecture diagram (node/edge lists)

**Nodes**
```
N1  Source kernel A (XNNPACK NEON/SSE/AVX; pinned commit; byte-identical)
N2  Target kernel B (agent-optimised RVV Bopt in E1 / new RVV/HVX code in E2 / XNNPACK sibling in E3)
N3  Rule tool rvv_ptr_lower (deterministic rewrite; pinned sha256)
N4  Lowered A', B' (pointer-form intrinsics, QCP-parsable)
N5  Unified intrinsic contract library (C contracts + Coq lane models; NEON/x86/RVV@128/256/512/HVX)
N6  Differential tests of N5 vs real instructions (gcc native, qemu-aarch64, qemu-riscv64, qemu-hexagon)
N7  Kernel contracts (functional spec of each kernel, e.g. output = xt_result(...))
N8  spec.c: equivalent(A,B) + outputs_related + preconditions with [VEKTO-C-xxx] markers  (HUMAN-REVIEWED)
N9  QCP symbolic execution
N10 Verification conditions (Coq goal files)
N11 Coq proofs (lemma libraries + tactics; written by agents)
N12 Gates g1..g12 in check.py (identity, lowering, pins, libs, units, proofs+Print Assumptions whitelist,
    equivalence, contract equality, B1 scan, non-vacuity witness, call closure, difftests)
N13 Supervisor recheck from an empty directory -> APPROVAL.json
N14 Counterexample (concrete input, reproduced on original C under QEMU)
N15 L1/L3 triage (reachable in XNNPACK call path? which side deviates? reference defined?)
N16 Outcomes: (a) added precondition C-xxx with code evidence; (b) fixed variant A_fixed/B_fixed (V-xxx);
    (c) relaxed observation R-xxx; (d) divergence record DIV-xxx / bug record XNN-/BOPT-xxx; main result "A != B" always kept
N17 CONDITIONS register (C/R/V/G/M rows) + PENDING-USER (user decisions)
```
**Edges**
```
N1 -> N3, N2 -> N3            (rewrite)
N3 -> N4
N5 -> N9                      (callee contracts)
N6 -> N5                      (validates)
N4 -> N9, N7 -> N9, N8 -> N9
N9 -> N10 -> N11 -> N12 -> N13
N9/N11 failure -> N14         (failed proof / goal shows a concrete difference)
N12(g12 difftests) -> N14     (auxiliary path)
N14 -> N15 -> N16
N16(a) -> N8                  (precondition strengthened, re-verify)
N16(b) -> N2 or N1            (fixed variant, re-verify; performance measured)
N16 -> N17
N17 -> N8                     (markers grep-able: `grep -rn "VEKTO-" spec.c`)
```

---

## 5. Walk-through: the x24-transposec package (E2, SSSE3 → RVV) [ESTABLISHED]

**Package location:** `build/e2e3-workers-20261106/w36-e2-transposec/work/pkg24`. **Approval:** `APPROVAL-x24-rvv.json`, 2026-11-23. Its sibling `pkg8` (x8 SSE2 16x16 → RVV) was approved on 11-22 (`examples/01k_*`).

1. **Source kernel** (`examples/01a_*`, 193 lines, byte-identical to XNNPACK `src/x24-transposec/x24-transposec-4x4-ssse3.c`). It transposes 3-byte pixels in 4×4 tiles. Each row is read with a 16-byte `_mm_loadu_si128`, followed by 7 unpacks, 6 `pshufb` using tables `pos0..pos5`, and a separate tail path for 1–3 rows. The kernel is declared `XNN_OOB_READS`.
2. **Target kernel** (`examples/01b_*`, 45 lines). This is new RVV code written for the experiment and then frozen (`ledger.json` targets.rvv). Each pass handles one column: `vsetvl_e8m1` strip-mines the height, a strided segment load `vlsseg3e8` (the load itself performs the transpose) is followed by `vsseg3e8`. Screen version: `examples/01l_*`.
3. **Spec** (`examples/01c_*`). `equivalent()` calls both kernels.
   - The preconditions are XNNPACK's asserts plus `[VEKTO-C-022]` (block ≥ 1×1), `[VEKTO-C-024]` (no address wrap), the `XNN_OOB_READS` window (C-033: the SSSE3 side reads `(BH-1)*IS + 12*((BW-1)/4)+16` bytes, while RVV reads only a prefix), `[VEKTO-C-031]`, and `vsl_ok(XT_N, vf)`. The last one models vsetvl as nondeterministic within RVV 1.0 rules.
   - The observation `outputs_related` (`examples/01d_*`) says the buffers have the same size and are equal on every byte a transpose writes. Bytes that are not written are not compared.
4. **Rule rewrite** (`examples/01f_*`). Two statements become pointer-form calls.
5. **Intrinsic contracts** (`examples/01g_*`). `__riscv_vsetvl_e8m1` returns `1 ≤ vl ≤ min(avl, 32)` at VLEN 256. The `vlsseg3e8` contract returns `rv_strided_tupleG(...)` with an arbitrary tail `T`.
6. **One VC and its proof** (`examples/01h_*`). At the return point of `equivalent()`, the VC asks for `outputs_related 3 BW BH OS (xt_result 3 IN OLD1 …) (xt_result 3 (sublist 0 (xt_nin_rows BH IS (3*BW)) IN) OLD2 …)`. In words: the result over the x86-readable window must match the result over the shorter window RVV reads. It is closed by lemma `xt_result_prefix_related24`.
7. **Gate output** (`examples/01i_*`). `RESULT: PASS`, rc=0, 12/12 gates, 5,990 s. Selected figures:
   - g9: 628 VCs, 0 with a duplicate-address LHS.
   - g10 witness: a 4×4 block with stride 12 at each VLEN.
   - g11: 6 `qcp_assume_aligned` calls, one per `XNN_ALIGN(16) static const` table.
   - g12: 43,158 x86 register cases, 4,320 memory cases, and 214,031 / 197,506 / 164,071 RVV cases at VLEN 128 / 256 / 512. The kernel domain has 26,192 cases.
   - 14 of 25 out-of-domain edge cases differ, for example `block_width=0`. C-022 excludes them, and this precondition was adopted under L1.
8. **Caveat.** `pkg24/README.md` still says "g2 … PENDING" (tool rule R64b). That text predates tool v1.23.9; the recheck status shows g2 PASS. The README is stale, not the result.

---

## 6. Motivated example: real counterexamples (ranked by how clearly they work on screen)

### Rank 1 (recommended): E1 f32-vmax, NaN; DIV-001, C-001
- **Code.** NEON A (`examples/02a_*`, 43 lines) computes `float32x4_t vacc = vmaxq_f32(va, vb);` (line 24). Agent-optimised RVV Bopt (`examples/02b_*`, 62 lines) computes `vfloat32m8_t vacc = __riscv_vfmax_vv_f32m8(va, vb, vlmax);` (line 37). Screen version: `examples/02c_*`.
- **Counterexample.** n=1, `a = 0x7fc12345` (qNaN), `b = 0x3f800000` (1.0). A outputs NaN `0x7fc12345` and Bopt outputs `0x3f800000` (1.0), at VLEN 128, 256 and 512. Swapping the inputs also reproduces it.
- **Coverage.** 180 of 360 comparisons differ, and these are exactly the one-sided-NaN cases (`examples/02d_*`).
- **Why they differ.** Arm FMAX propagates NaN. RVV `vfmax` is maximumNumber and ignores a single NaN (`examples/02e_*`).
- **Trust angle.** The earlier bounded checker (SALTyRN cvc5) said VERIFIED because its NEON model was wrong. Fixing the model makes the same check produce a counterexample (`examples/02g_*`).
- **Resolution (L1/L3).** The input is reachable: XNNPACK performs no NaN check. The reference is undefined: the maintainer says min/max NaN behaviour is not guaranteed (google/XNNPACK#441).
  - The main result "original A ≠ Bopt" is kept (DIV-001).
  - A conditional proof under C-001 ("inputs contain no NaN") is recorded as passed and rechecked (`CONDITIONS` C-001). That evidence package is on the unavailable earlier server, so I cannot re-check it.
  - The alternative, repairing Bopt, was measured on Saturn RTL: **+18.8 % cycles** (geometric mean), and 0.982× → 0.826× relative to XNNPACK u8v (`vmax-performance/REPORT.zh-CN.md`).
- **Why rank 1.** The kernel body is one line on each side and the input is one element. The difference is intuitive (NaN vs 1.0). It shows the whole L1/L3 path and the "explicit, separately counted condition" principle. It also ties to two series themes: tests passing and a bounded checker agreeing are both not enough, and the counterexample is what led to a repair together with its measured cost.

### Rank 2: E3-33 s8-rmax, RVV tail-agnostic accumulator (XNN-003, V-006)
- **Code.** `vmax = __riscv_vmax(vmax, vinput, vl);` (`examples/03a_*`, line 39 of the original), followed by `__riscv_vredmax(vmax, max, vlmax)`.
- **Counterexample.** VLEN 128, batch=129, all inputs −128: the reference gives −128, but RVV gives **−1** under QEMU `rvv_ta_all_1s=true`.
- **Why.** Tail-agnostic lanes may be overwritten with all ones, and that is legal in RVV 1.0.
- **Fix.** One line: `__riscv_vmax_vv_i8m8_tu(vmax, vmax, vinput, vl)` (`examples/03c_*`). A ≡ B_fixed is proved at three VLENs and was rechecked on 11-07.
- **Strengths.** It was found by a **failed proof**, not by a test. It is a real bug in production XNNPACK RVV kernels, and the family covers 26 files and 15 registered kernels.
- **Weakness for screen.** It needs an explanation of RVV tail policy. Also, upstream PR #11839 (merged 10-29) fixed the same root cause, so it can only be called an independent finding (`examples/03d_*`).

### Rank 3: E3-03 f32-vexp, NaN through the exponent clamp (XNN-005, V-008)
- **Code.** `vz_prime = xnn_min_f32(xnn_max_f32(vz_prime, vm127), v128);`. On x86, `max_ps` returns the second operand when one is NaN.
- **Counterexample.** `exp(NaN)`: FMA3 outputs **+0.0**, NEON outputs NaN. An exhaustive check over all 2^32 inputs finds differences only on NaN inputs.
- **Fix.** Swap the operands (`examples/04a_*`). On non-NaN inputs the result is bit-identical. A ≡ B_fixed is proved and was rechecked on 11-10 (`examples/04b_*`).
- **Strength.** The fix is very short.
- **Weaknesses.** It is NaN again, as in rank 1. The user ruled that NaN differences form one class of error rather than separate bugs.

**Also usable:** XNN-001 vclamp (`examples/05a_*`). For `x=0, min=1, max=0`, NEON outputs 1 while the reference and Bopt output 0, because the tail does min-then-max. This case is where the L1 procedure came from (`examples/06_*`).

---

## 7. Assumptions and limitations (keep these visible on screen)
- **Global premises** (`CONDITIONS.zh-CN.md`, G-rows):
  - G-001: rounding is RNE, and NEON runs with FZ=0.
  - G-002: intrinsic semantics come from human-reviewed contracts plus differential tests. **There is no formal correspondence proof to the ISA.**
  - G-003: the RVV proof is of the rule-tool output, justified by the rule table and differential tests.
  - G-004: **partial correctness only.** There is no termination proof and no compiler-to-machine-code correspondence.
- **VLEN.** Each RVV result is proved separately at fixed VLEN 128, 256 and 512. That is not "arbitrary VLEN" (approval files; `AGENTS.md` makes the same point for the earlier line).
- **HVX is modelled as LP64.** Hexagon is ILP32, but QCP has only an LP64 model (`[VEKTO-M-ilp32]`, user-signed 11-22). The proof does not cover 32-bit wrap-around behaviour, and pointer arrays use an 8-byte layout. The original kernels are run under qemu-hexagon as tests, not as proof.
- **Conditions narrow some results.**
  - C-017/C-017b: no NaN. This is a narrowed result that the paper must state.
  - C-018: no in-place calls, because QCP does not model `restrict`. XNNPACK does test in-place use.
  - The XNN_OOB_READS window conditions (C-016/020/021/023/025/026/032/033) rely on the `XNN_EXTRA_BYTES` API promise.
  - Every condition cites code evidence, and the original counterexample is kept.
- **Trusted base.** The QCP 2.1.4 C model (whitelisted axioms) and Coq stdlib axioms. The project found two QCP soundness issues: QCP-B1 (vacuous goals) and QCP-B2 (an axiom inconsistency). Both are guarded by gates g9 and g6 (`research/bugs/qcp/`).
- **The observation relation matters.** Unwritten output bytes are not compared, NaN payloads are not compared under R-000, and ±0 is treated as numerically equal. Per-kernel relaxed relations may not compose into a program-level result, which is an E4 concern (`EXPERIMENT-DESIGN` E4).
- **Evidence gaps.**
  - The early E1 packages (16 pairs, including the vmax conditional proof) are on an earlier server that is unavailable, and their cost records are lost (`SUMMARY-20261111` §2, items under 成本).
  - Performance was measured only for vmax. Keagan's paper protocol (FireSim, harness) is not publicly recoverable (`E1-PAIRING…` §3).
- **Not yet reported upstream.** XNN-001…008 have not been reported, and external reporting needs the user's consent.

## 8. Continuity hooks to ExVerus / TopoVerus / Vero
- **Counterexamples link failed proofs to repairs.** ExVerus and TopoVerus used counterexample-guided Verus proof repair; LIT-BRIEF suggests citing them as self-citation for "agent writes proof, counterexample diagnoses" (`intro-bullets/LIT-BRIEF-20261115.zh-CN.md` §5). In Vekto a failed obligation becomes a concrete C input. It is reproduced on the original program under QEMU and then triaged by L1/L3 into one of three outcomes: an added precondition with code evidence, a minimal fix, or a recorded divergence.
- **No weakened specs.** Vero rejects weakened specs through slot-scoped re-rendering (Vero brief §2.5). Vekto has comparable mechanisms, though the parallel is [INFERRED]:
  - gate g1 checks byte identity of the sources;
  - gate g8 checks contract text equality;
  - every narrowing appears as a grep-able `[VEKTO-C-xxx]` marker in `spec.c` plus a CONDITIONS row;
  - the rule "never weaken equivalence to get a proof through" (`KERNEL-EXECUTION-POLICY` §1.4).
- **Explicit assumptions.** Vero's `#print axioms` check plays the same role as Vekto's Print Assumptions whitelist in gate g6. Vekto adds one more check, the non-vacuity witness in gate g10.
- **Scale shifts.** Function-level proofs (ExVerus/TopoVerus) → repository-level proofs (Vero) → cross-ISA, whole-kernel equivalence of real optimised code (Vekto). That ordering is [INFERRED] framing. The only grounding is the series list given in the task.

## 9. Glossary
- **SIMD / NEON / SSE / AVX / RVV / HVX:** vector instruction sets for Arm, x86, RISC-V and Hexagon.
- **VLEN / VLMAX / vl:** the RVV register width in bits; the maximum element count; the active length chosen at run time by `vsetvl`.
- **Tail-agnostic / `_tu`:** RVV policies for lanes beyond `vl`. Tail-agnostic lanes may be left alone or set to all ones. `_tu` leaves them undisturbed.
- **Intrinsic:** a C function that maps to a vector instruction.
- **QCP:** a C verifier that performs symbolic execution in separation logic and emits Coq VCs.
- **VC:** a verification condition.
- **`VC_Correct`:** the Coq interface that collects all VC proofs of a unit.
- **A / B0 / Bopt / A_fixed / B_fixed:** the source kernel; the RVV before optimisation; the final optimised RVV; minimally fixed variants.
- **`equivalent()` / `outputs_related`:** the human-reviewed top-level spec and its observation relation.
- **C-/R-/V-/G-/M-xxx:** register entries for input conditions, observation relaxations, program variants, global premises and modelling premises.
- **L1 / L3:** the counterexample triage procedures (`examples/06_*`).
- **XNN_OOB_READS / XNN_EXTRA_BYTES:** the kernel annotation and the API promise that a buffer may be over-read by up to 16 bytes (128 on Hexagon).
- **B1 scan:** a check that no VC has duplicate-address resources, guarding against QCP-B1.
- **Non-vacuity witness:** a concrete state that satisfies the spec's precondition.

## 10. Open questions (for the video team and for the authors)
1. **Which E1 numbers can be quoted?** The 16 early pairs are not reproducible on the current machine, while the 17 Codex-batch APPROVALs are. How should E1 be counted on screen?
2. **Is vmax still the paper's motivating example?** `final-minmax-reproduction/README` recommends it but notes there is "no confirmed evidence that it is faster than XNNPACK", and the repair costs 18.8 %. It works as a correctness case, but not as an "optimised and verified" showcase.
3. **Possible inconsistency in the vclamp condition.** E3-34 uses C-019 (lo ≤ hi), citing `microparams-init.c:791/803 assert(output_min < output_max)`. But the XNN-001 record says the standalone clamp path has **no** such check, and that the line-791 assert belongs to the s8 minmax init used by maxpool. E1 therefore kept vclamp unconditional and used A_fixed. This needs author review before either case appears on screen.
4. **E4 (Softmax)** has not started. The video should not imply program-level results.
5. **No upstream reports yet.** "Bugs found" should be presented as "confirmed candidates, not reported upstream".
6. **The "Vero ↔ Vekto" parallels** in §8 are my framing and need author confirmation.
