# Final review of the four-episode kit (2026-11-23)

Scope: `episodes/{exverus,topoverus,vero,vekto}/`, plus `docs/` and `research/` for privacy. I extracted the paper text with
pypdf from `papers/*.pdf`. Vekto numbers were read from the repository files cited in `episodes/vekto/SOURCES.md`, and the
repository was not modified. No video was rendered. Low-quality stills were made only for changed layouts (Vek10Results,
Vek11Status, Vero01Open, Vek02Hook). The ExV10 ablation legend width was measured numerically. After the edits,
`tools/check_episode.py` prints OK for all four episodes and every `scenes.py` passes `py_compile`.

Narration estimates (words/2.6 + 0.5 s): ExVerus 8.95 min, TopoVerus 7.75, Vero 7.57, Vekto 9.00. All four are within 6 to 9 min.
The narration blocks in every STORYBOARD.md were re-synced from narration.json.

## 1. Fact check: results

### ExVerus (papers/exverus.pdf)
- **Verified as correct.**
  - Table 1 Sonnet-4.5 rows: VerusBench 88.4/75.3/83.6; DafnyBench 95.5×3; LCBench 28.6/14.3/25.0; HumanEval 41.2/27.9/29.4.
  - Table 1 DeepSeek-V3.1 VerusBench: 71.9/24.7/60.3.
  - Table 2 DeepSeek ranges: ExVerus 73.9–86.5, AutoVerus 24.7–36.5. ObfsBench has 266 tasks (p.6).
  - Table 3: $0.04 vs $0.17 and 720.3 vs 2989.1 s; GPT-4o $0.42 vs $0.69 and 250.0 vs 233.9 s.
  - Table 4: ObfsBench DeepSeek 81.6 vs 65.4.
  - §4.3: 172/243 and 38/153.
  - App. A.1: AutoVerus spent 16 attempts on this error; "mutant-1 … passes Verus".
  - §4.1: 5 mutants and at most 10 iterations. Default of 10 counterexamples.
  - 7,083-line query, i=537, len 1681.
  - Author list and ICML 2026.
- **ExVerus_NO_MUT label.** Table 4's caption is "Ablation study on mutation strategies". §4.2 (p.7) defines the baseline as one that "instructs the LLM to directly fix the proof based on the counterexamples without validation", with expert repair knowledge in the prompt.
  - `episodes/exverus/narration.json` exv10-1: "a variant without counterexample mutation and validation drops from 81.6 to 65.4" → "a variant that hands them straight to the model, with no mutators and no validation, reaches 65.4 … Full ExVerus reaches 81.6". The zh text was changed to match.
  - `episodes/exverus/scenes.py` ExV10 legend: "ExVerus_NO_MUT (no mutation, no validation)" → "ExVerus_NO_MUT (CEXs to LLM, no validation)".
  - `episodes/exverus/SOURCES.md` ExV10 row now cites the §4.2 definition and the Table 4 caption. It previously cited only a repo display-name mapping.
- **Verus version claim.** exv11-3 said "part of its lead over AutoVerus comes from a Verus version change that hurt the baseline". That is our inference, which the paper does not state. Changed to: "the paper reports that AutoVerus, built for an older Verus, scores lower on the newer version used here" (App. H.4 p.22: 75.33% vs 52.7%; footnote 3 p.6). The SOURCES row was updated.
- **Soundness wording.** exv03-5 said "may even be unsound" → "may even relax soundness". The paper's wording is "relax the soundness requirements" (p.2).
- **Pronoun in zh.** exv01-3 zh "他是…" → "孙悦淳是…". The sources do not state a pronoun.
- **STORYBOARD.md open issues 1–2** were rewritten as resolved (PDF re-checked; NO_MUT label settled).

### TopoVerus (papers/topoverus.pdf)
No changes were needed. Verified:
- 471 problems in 7 suites, with 61.6/72.2 Safe-Pass@1/@3.
- +5.7/+6.3 over Sonnet-4.5 (55.9/65.9, Table 4 p.18).
- CoT-Init → CTX-Init 39.3 → 50.5 (+11.2); CTX-Binary 53.7 → CTX-Dep 61.6 (+7.9).
- Table 7: β 43.8 → 95.8 and α 98.6/98.5 on 24 paired tasks.
- VeruSAGE 75.5 vs 30.2.
- QwQ-32B, Sonnet 4.6 teacher, 461 trajectories from 249 programs, 8 rollouts.
- 3 chains × 10 iterations; Limitations (loop invariants only, hallucinated traces).
- NeurIPS 2026 footer; LeetCode 121 and [5,3,7] (App. B).
- Repo test `test_trust.py:138-149` and `buggy.rs` match the screen files.

### Vero (papers/vero.pdf)
- **Verified:**
  - 43 instances (13 + 30), 743 APIs, 2,705 specs.
  - Full solves 27/8/2/2; 87.3%; median 73.6%; 10 instances resist all 8 configurations; 90 min.
  - 368 rejections, 28 of 53, 20,440 graphs.
  - 38 defects in 9 instances plus 6 joint-unsat groups; Table 6 18/17/2/1.
  - The 0x3D listing and fix, and the quote "survived manual review…".
  - The contamination wording and the sortedcontainers O(n) case.
- **Overstated agent intent.** vero08audit-1 said "GPT-5.5 … did not try to satisfy both". That claims an intent the paper does not report. Changed to "During benchmark development, GPT-5.5 at xhigh effort flagged this pair through the audit route, with a machine-checked proof that the two specs are jointly unsatisfiable" (App. F p.24; Table 6 caption "during benchmark development"). The zh text was changed to match.
- **Title card.** `scenes.py` Vero01Open: "…Kong, He, et al. 2026" → "…Kong, He, Song · 2026". The paper has 11 authors; "et al." hid only Dawn Song. The change was propagated to STORYBOARD.md, SOURCES.md and docs/SERIES.md, which now also says the arXiv v1 is marked "Preprint" and that no venue is shown.

### Vekto (repository files)
- **Verified:**
  - APPROVAL-x24-rvv.json and `rechecks/w36x24/run/status.json`: PASS, 12/12 gates, 5,990 s; 435 x86 VCs and 22 RVV VCs per VLEN; conditions C-022/C-024/C-031/C-033; edge cases 14 of 25.
  - The check.py docstring for the gates.
  - The DIV-001 and final-minmax README values (0x7fc12345 / 0x3f800000, VLEN 128/256/512, swap).
  - CONDITIONS rows C-001, C-018, G-002/G-004, VEKTO-M-ilp32.
  - +18.8% cycles (geometric mean, Saturn RTL) in vmax-performance/REPORT.
  - The repair patch (4 statements).
  - 17 E1 APPROVAL files, 13 of them A ≠ Bopt.
  - "E2 → 24" in the DECISIONS log (11-23 04:05).
  - E3 14 + 1 (SUMMARY-20261111 §2.2).
  - XNN-005 NaN flushing; XNN-003 QEMU tail lanes; NeonLib.v / RvvModel.v lane models.
- **Bopt provenance.** Vek02-2 "An agent pipeline ported it…" → "An LLM-driven pipeline, SALTy-RN, ported it…". The source is the SaltyRN.pdf title and abstract ("LLM-driven", Autocomp stage) and PAPER-POSITIONING line 36. Matching edits:
  - On-screen panel title "Bopt · agent-optimised RVV" → "Bopt · LLM-optimised RVV".
  - `examples/02_vmax_rvv_Bopt_core.c` comment.
  - Vek11 E1 row and Vek11Status-1 narration.
- **NaN reachability.** Vek04-2 said "XNNPACK never checks for NaN" → "Nothing on XNNPACK's call path checks for NaN". DIV-001 item 4 covers only the API → ukernel path.
- **XNN-003 wording.** Vek05-3 said "a real tail-lane bug" → "a tail-lane bug we found, XNN-003". The record says it is unknown which real chips fail.
- **Bounded checker.** Vek05-4 said "an earlier bounded checker" → "SALTy-RN's own bounded checker". The README says this was a fresh local run of the SALTyRN cvc5 backend, not an earlier run.
- **Missing modelling assumptions** (spec rule 9). APPROVAL-x24 also lists VEKTO-M-local-aligned (6 aligned const tables) and NDEBUG.
  - Added the on-screen bullet "modelling: 6 const tables 16-byte aligned · assert() off (NDEBUG)" in Vek10Results. The still was checked.
  - Added a narration clause in Vek10Results-4 and a SOURCES row.
- **E3 status.** It was labelled only "ESTABLISHED", but SUMMARY-20261111 lists 3 planned pairs as not started.
  - The badges are now "ESTABLISHED: 15" + "IN PROGRESS", with the detail line "…, 3 not started". The still was checked.
  - Vek11Status-3 narration was updated, along with SOURCES and STORYBOARD.
- **Length trims to stay ≤ 9 min.** The meaning is unchanged: Vek04Resolve-4, Vek06Level-2, Vek07Pipeline-2 and Vek09Walk-2 (dropped "plus a tail path").
- **Terminology.** Vek01Open-2 zh "检查器" → "checker", to match Vero's zh.

## 2. Code fidelity (spot checks)
- TopoVerus `caseB-loop-SCREEN.rs` matches `repos/Topoverus/.../buggy.rs` and `safety-gate-S3-SCREEN.rs` matches `tests/test_trust.py:138-149`, both with the documented trims.
- Vero Base64 listings match the p.24 text layer.
- Vekto `01`/`02`/`07` examples match `final-minmax-reproduction/vmax/{neon,rvv}.c` and `pkg24/impl/x24-transposec-vl-rvv.c`. `03_fmax_lane_models.v` matches NeonLib.v and RvvModel.v.
- ExVerus Fig. 1 and Fig. 3 code exists only as vector glyphs, and the extracted text is fragmentary. The fragments are consistent with the transcriptions (tokens, structure, values), but a line-by-line check needs a PDF viewer.

## 3. Continuity
- All recap and bridge lines match docs/SERIES.md: Ep1 series intro and bridge, Ep2 recap and bridge, Ep3 recap and bridge, Ep4 recap and series close.
- The per-episode counterexample forms agree with each other.
- Title cards match the SERIES attribution (Vero updated as above).

## 4. Privacy
- `research/topoverus/sources.json:76`: an absolute server path and a reference to an internal assistant memory note were replaced by "repository AGENTS.md; research/project-plan-20261102/LESSONS.zh-CN.md (L1, L3)".
- `research/topoverus/BRIEF.md:332`: the same memory-note reference was replaced.
- Removed `episodes/{vero,vekto}/__pycache__` (compiled files embed absolute paths).
- The remaining hits are public GitHub repositories (`sunblaze-ucb/vero`, `Etha-Sun/Topoverus`), which are kept on purpose.

## 5. Open issues for the author
1. **Author card (exv01-3).** It uses homepage facts as summarised in research/topoverus/BRIEF.md §10 (fetched 2026-11-23). These were not re-fetched in this review.
2. **Vero venue.** The homepage lists NeurIPS 2026, but the arXiv v1 PDF says "Preprint". The screen shows only "2026"; please decide.
3. **Vekto numbers policy.** E2 "24" (DECISIONS log) and E3 "14 + 1" (SUMMARY-20261111) are not direct APPROVAL/LEDGER counts. They are labelled "supervisor log" and "as of 11-11". Confirm them, or replace them with a recount of APPROVAL files.
4. **C-031 is used for two different conditions.** APPROVAL-x24 uses it for "nin16 ≤ INT64_MAX", while the CONDITIONS row C-031 describes maxpool pointer arithmetic. The screen follows APPROVAL; the register should be reconciled.
5. **SaltyRN.pdf citation.** The file is untracked at the repository root. If it moves, update the Vek02 row in SOURCES.md.
6. **NaN payload in the repair.** The Bopt repair yields a canonical NaN, not A's payload. This is fine under the E1 observation relation, which ignores payloads, but avoid saying it "returns the same NaN".
7. **Scene duration headers.** The per-scene "(~N s)" headers in STORYBOARD.md were not recomputed after the beat edits. The beat values are current.
8. **Existing open item.** Vekto STORYBOARD issue 4 (Vero ↔ Vekto parallels are framing) still needs author confirmation.
