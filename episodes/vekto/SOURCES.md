# Episode 4 — Vekto: sources

Every on-screen number, quote and code snippet, with its repository-relative locator (repository = the surrounding
`vekto` branch; nothing was re-run for this episode). Translations of Chinese sources are ours. Status as of 2026-11-23.

## Code on screen (examples/)

| File | Scene | Source (exact) | Trims |
|---|---|---|---|
| examples/01_vmax_neon_A_core.c | Vek02 | research/project-plan-20261102/final-minmax-reproduction/vmax/neon.c lines 21–26 (E1 kernel A, SALTy-rn be16280c7) | `const` and pointer bumps dropped, blank lines dropped, comment line added |
| examples/02_vmax_rvv_Bopt_core.c | Vek02 | research/project-plan-20261102/final-minmax-reproduction/vmax/rvv.c lines 33–40 (Bopt, optimized-rvv-kernels@80feb4564) | comments/blank lines dropped, comment line added |
| examples/03_fmax_lane_models.v | Vek04 | build/e2e3-workers-20261106/intrinsics-v1.7.3/neon/NeonLib.v lines 87–89, 105–107; rvv/RvvModel.v lines 62–64 | ordered-comparison branches replaced by `...` |
| examples/04_vmax_bopt_nan_repair.c | Vek04 | research/project-plan-20261102/vmax-performance/repair.patch, first hunk (vfmax line + 4 added lines) | diff markers and indentation removed |
| examples/05_bounded_checker_patch.diff | Vek05 | research/project-plan-20261102/final-minmax-reproduction/diagnostic-neon-model.patch, the 6 added lines | indentation reduced |
| examples/06_x24_source_ssse3.c | Vek09 | build/e2e3-workers-20261106/w36-e2-transposec/work/pkg24/impl/x24-transposec-4x4-ssse3.c lines 70–74, 80, 89, 97 (+ closing brace) | rest of tile body and tail replaced by `...` |
| examples/07_x24_target_rvv.c | Vek09 | build/e2e3-workers-20261106/w36-e2-transposec/work/pkg24/impl/x24-transposec-vl-rvv.c lines 29–44 | verbatim, indentation reduced |
| examples/08_x24_spec_equivalent.c | Vek09 | build/e2e3-workers-20261106/w36-e2-transposec/work/pkg24/spec.c (`equivalent()`) | parameters, With list and Require clauses partly replaced by `...`; long lines broken; no clause changed |

Research-agent copies of all of these (with fuller headers) are in research/vekto/examples/ (02a, 02b, 02e, 02f, 02g, 01a, 01b, 01c).

## Numbers, values and claims on screen

| Scene | On screen | Source / locator |
|---|---|---|
| Vek02 | input `a[0]=0x7fc12345` (NaN), `b[0]=0x3f800000` (1.0), n = 1; A → `0x7fc12345`, Bopt → `0x3f800000` | research/project-plan-20261102/final-minmax-reproduction/README.zh-CN.md, section 实际输出; research/bugs/divergences/DIV-001-f32-vmax-nan.zh-CN.md |
| Vek02 | QEMU at VLEN 128/256/512; swapping inputs reproduces | same README (实际输出 table and coverage paragraph) |
| Vek02 | Bopt is the output of an LLM-driven pipeline (SALTy-RN, with its Autocomp optimisation stage); on screen "LLM-optimised RVV" | SaltyRN.pdf (repository root, untracked; title "Semantically Aligned LLM-driven code Translation for RISCVV and Neon", abstract); research/project-plan-20261102/PAPER-POSITIONING-AND-METADATA.zh-CN.md line 36 |
| Vek03 | NEON register 128-bit = 4 × f32; RVV VLEN chosen per chip, `vsetvl` | intrinsic/ISA facts; research/project-plan-20261102/intro-bullets/v2-preconditions.md ¶2 (fixed-width vs runtime vector length) |
| Vek04 | Arm FMAX propagates NaN; RVV vfmax = IEEE 754-2019 maximumNumber | NeonLib.v lines 87–89, 102–110 (comment at 104); RvvModel.v lines 59–68 (comment at 60–61) |
| Vek04 | L1: input reachable (no NaN check on the API → create/setup → ukernel path; narration says exactly this, not "XNNPACK never checks"); no reference (google/XNNPACK#441) | research/project-plan-20261102/LESSONS.zh-CN.md L1, L3; DIV-001 item 5 (links the maintainer comment on issue #441) |
| Vek04 | main result A ≠ Bopt (DIV-001) | DIV-001 header; research/project-plan-20261102/CONDITIONS.zh-CN.md row C-001 (line 40) |
| Vek04 | conditional A ≡ Bopt under C-001 (no NaN), "passed + rechecked", counted separately; early evidence not re-runnable | CONDITIONS.zh-CN.md row C-001 ("条件配对通过（W19），监督者复检通过"); research/project-plan-20261102/SUMMARY-20261111.zh-CN.md §2 (earlier server unavailable) |
| Vek04 | repair = 4 statements after each vfmax; +18.8 % cycles, geometric mean over 7 sizes, Saturn RTL; tested, not proved | research/project-plan-20261102/vmax-performance/REPORT.zh-CN.md, 结论 and 逐尺寸周期 (7 sizes 16…65,536); repair.patch; final-minmax-reproduction README ("regression-tested, not formally proved", via research/vekto/examples/02d) |
| Vek05 | random test buffers flush NaN to 0, tester NaN assertion never fires | research/bugs/xnnpack/XNN-005-f32-vexp-nan-clamp/README.zh-CN.md, 补充 (2026-11-08), NaN 契约 bullet (cites XNNPACK `buffer.h:973-979`) |
| Vek05 | QEMU keeps tail lanes unchanged by default → XNNPACK tests on QEMU don't expose XNN-003 (named in narration; which real chips fail is unknown per the record) | research/bugs/xnnpack/XNN-003-s8u8-rminmax-rvv-tail-agnostic/README.zh-CN.md line 20 |
| Vek05 | SALTy-RN's own bounded checker (local SALTyRN cvc5 backend, run on the final vmax, length 1, VLEN 512) said VERIFIED; NEON model ignored NaN; patched model → COUNTEREXAMPLE | final-minmax-reproduction/README.zh-CN.md, "bounded 检查对照及机制"; diagnostic-neon-model.patch; diagnostic-model-result.json |
| Vek05 | quote "establish equivalence for all inputs permitted by the preconditions in the spec" | research/project-plan-20261102/intro-bullets/v2-preconditions.md ¶3 (Intro V2 draft bullets) |
| Vek06 | three levels (Sail/Islaris, Alive2/Rake, C); assembly needs separate models + correspondence, covers exceptions/privileged execution; C: explicit definition per intrinsic, reviewed against ISA docs | v2-preconditions.md ¶4–5 |
| Vek07 | rule tool: deterministic, vector statements only, no LLM/hand edits, rejects unknown constructs; reason = QCP by-value vector defects | tools/rvv_ptr_lower/README.zh-CN.md (header user rule 2026-11-04; 为什么需要; 做法) |
| Vek07 | one shared intrinsic library, differential tests native x86 / QEMU (NEON, RVV, Hexagon) | build/e2e3-workers-20261106/intrinsics-v1.7.3/INTRINSICS-COMMON.zh-CN.md (交付物 2, 4) |
| Vek07 | spec.c holds only `equivalent()`; impl/ byte-identical | build/e2e3-workers-20261106/w36-e2-transposec/work/pkg24/README.md |
| Vek07 | counterexample replayed on originals → L1/L3 → condition / fix / divergence | LESSONS.zh-CN.md L1, L3; research/vekto/BRIEF.md §4 edges |
| Vek08 | 12 gates and their meaning; run from an empty directory | build/e2e3-workers-20261106/w36-e2-transposec/work/pkg24/proof/check.py docstring lines 4–17 (usage line: `--run-dir <EMPTY dir>`) |
| Vek09 | x24 source = XNNPACK SSSE3, byte-identical; `XNN_OOB_READS`; target = new RVV code, frozen | pkg24/impl/ files; pkg24/ledger.json (via research/vekto/BRIEF.md §5) |
| Vek09 | C-022 (block ≥ 1×1), C-024 (no address wrap), C-033 (input window) | pkg24/spec.c header comment and Require; CONDITIONS.zh-CN.md rows C-022 (line 69), C-024 (line 71), C-033 (line 81); APPROVAL-x24-rvv.json `conditions` |
| Vek09 | `outputs_related`: equal on every byte a transpose writes | pkg24/spec.c header comment |
| Vek10 | RESULT PASS, 12/12 gates, 5,990 s | build/e2e3-workers-20261106/w36-e2-transposec/APPROVAL-x24-rvv.json `result`; build/e2e3-workers-20261106/rechecks/w36x24/run/status.json (`pass: true`, `seconds: 5990`) |
| Vek10 | 435 x86 VCs; 22 RVV VCs per VLEN at 128/256/512 | status.json gates g5/g6; APPROVAL-x24-rvv.json |
| Vek10 | fixed VLEN 128/256/512; C-022, C-024, C-031, C-033 | APPROVAL-x24-rvv.json `status` and `conditions` |
| Vek10 | G-004 partial correctness; G-002 intrinsics = reviewed contracts + differential tests, no formal ISA correspondence | CONDITIONS.zh-CN.md G-rows (lines 29–33) |
| Vek10 | modelling assumptions: 6 `XNN_ALIGN(16)` constant tables assumed aligned (VEKTO-M-local-aligned); assert() compiled out (NDEBUG) | APPROVAL-x24-rvv.json `conditions` (last two entries) |
| Vek10 | out-of-domain edge cases: 14 of 25 differ (e.g. block_width = 0), excluded by C-022 | APPROVAL-x24-rvv.json `notes`; status.json g12 `edge_cases: 25`, `edge_differences: 14` |
| Vek11 | E1: 35 pairs; IN PROGRESS; 17 approval records; most main result A ≠ Bopt | research/project-plan-20261102/EXPERIMENT-DESIGN.zh-CN.md (E1); count of build/e1-codex-20261111/c*/APPROVAL*.json = 17, `status` fields |
| Vek11 | E2: 24 approved migrations; x64-transposec → HVX in progress | research/project-plan-20261102/DECISIONS-FOR-REVIEW.zh-CN.md, 11-23 04:05 entry ("E2 → 24") and 11-23 14:20 entry (484 of 529 non-entail VCs Qed; not shown) — see STORYBOARD open issue 1 |
| Vek11 | E3: as of 11-11, 14 pairs approved + 1 proved not equivalent; 3 planned pairs not started (status ESTABLISHED: 15 + IN PROGRESS) | research/project-plan-20261102/SUMMARY-20261111.zh-CN.md §2.2 — see STORYBOARD open issue 1 |
| Vek11 | E4: not started, softmax candidate | SUMMARY-20261111.zh-CN.md §2; EXPERIMENT-DESIGN.zh-CN.md (E4); v2-preconditions.md ¶9 |
| Vek12 | no termination / no C-to-machine-code correspondence | CONDITIONS.zh-CN.md G-004 |
| Vek12 | Hexagon modelled as LP64 though ILP32 | CONDITIONS.zh-CN.md bullet [VEKTO-M-ilp32] (line 95) |
| Vek12 | in-place calls not covered | CONDITIONS.zh-CN.md row C-018 (line 65) |
| Vek12 | bugs not reported upstream | research/bugs/xnnpack/ records; research/vekto/BRIEF.md §7 |
| Vek01, Vek12 | recap line, per-episode counterexample captions, trust line | docs/SERIES.md "Episode 4, Vekto" |
