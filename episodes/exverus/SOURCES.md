# ExVerus (Episode 1) — sources for everything on screen

Paper: *ExVerus: Verus Proof Repair via Counterexample Reasoning*. Yang, Sun, Wu, Caridad, Yuan, Yao, Lu, Pei. ICML 2026,
arXiv 2603.25810v2, local copy `papers/exverus.pdf`. "p.N" means the PDF page. Repo: github.com/claudeyj/exverus @ 4e513a1c
(shallow clone in `repos/exverus`). Research notes: `research/exverus/BRIEF.md` (§ numbers below) and `research/exverus/sources.json`.

## Code and text panels

| On screen | File in `examples/` | Source | Trims |
|---|---|---|---|
| findmax buggy proof (ExV02) | `findmax_buggy_screen.rs` | Fig. 1 left panel, p.3 (via research `02a`) | requires/ensures → `...`; `decreases` line and annotation comment removed |
| Verus's raw model (ExV02) | `findmax_verus_raw_model.txt` | Fig. 1 bottom-right panel, p.3 (via `02c`) | kept figure lines 6, 7, 625, 980–981, 1095; line numbers dropped; `...` between them |
| findmax CEX_1 table (ExV02, ExV03) | `findmax_cex.txt` | Fig. 1 top-right panel, p.3 | CEX_1 only, shown as key/value rows |
| Z3Py query (ExV03) | `findmax_z3py_screen.py` | Fig. 1 top-middle panel, p.3 (via `02b`) | 4 blank lines removed |
| brs1 second loop (ExV04, ExV05, ExV07) | `brs1_loop_screen.rs` | Fig. 3 panel 1, p.13 (via `03a`) | requires/ensures and first loop → `...`; 4 correct invariants → `...`; annotation comment removed |
| brs1 fixed loop (ExV07) | `brs1_loop_fixed_screen.rs` | line 7 from Fig. 3 panel 4, p.13; other lines as above | only line 7 differs |
| patch (ExV07) | `brs1_patch.diff` | Fig. 3 panel 4, p.13 (via `03c`) | none |
| brs1 CEX_1 / CEX_2 tables (ExV05, ExV07) | `brs1_cex.txt` | Fig. 3 panel 2, p.13 (via `03b`) | shown as key/value rows |
| validation harness (ExV05, ExV07) | `brs1_harness_screen.rs`, `brs1_harness_blocking_screen.rs` | Fig. 3 panel 5, p.13 (via `03d`) | the figure's `-`/`+` lines split into two files |
| LLM diagnosis JSON (ExV06) | `brs1_triage.json` | Fig. 3 panel 3, p.13 (via `03b`) | rationale string wrapped onto lines |

## Numbers, quotes and claims

| Scene | On screen | Source |
|---|---|---|
| ExV01 | Author card: senior undergraduate, School of the Gifted Young, USTC; Data Science and Big Data Technology; advisors Kexin Pei (UChicago), Alvin Cheung (UC Berkeley); interests | Author homepage, fetched 2026-11-23, as summarised in `research/topoverus/BRIEF.md` §10 |
| ExV01 | Author list, "ICML 2026" | p.1; `docs/SERIES.md` "Attribution on screen" |
| ExV02 | error "invariant not satisfied at end of loop body" | Fig. 1, p.3 |
| ExV02 | "7,083-line SMT query", "unknown", `i@ 537`, `1681`, `Poly!val!31` | Fig. 1 p.3; §2.2 p.3–4 (BRIEF R10) |
| ExV02/03 | CEX_1 `nums = vec![-1, -1], i = 1, max = 0`, "Status: SAT" | Fig. 1 top right, p.3 |
| ExV03 | counterexample definition σ ⊨ A ∧ ¬C | Def. 2.1, p.4 |
| ExV03 | "with forall / exists, the solver often answers unknown" | §2.2 p.3; p.3 footnote 1 |
| ExV03 | "length fixed to 2 → no quantifiers"; program's own names | Fig. 1 callouts (lines 3–7), p.3; §3.1 p.5 |
| ExV03 | "not trusted until Verus checks" | p.2 (soundness rests on Verus), BRIEF §2 |
| ExV04 | error "invariant not satisfied before loop" | Fig. 3 panel 1, p.13 |
| ExV04 | "AutoVerus: 16 attempts on this error, task failed" | App. A.1, p.13 (15+4+21 attempts, 16 on this error) |
| ExV05 | CEX_1 `a = vec![1, 1], sum = vec![1], i = 0, N = 2`; CEX_2 `sum = vec![2]` | Fig. 3 panel 2, p.13 |
| ExV05 | validator extracts loop, invariants → assertions, injects CEX; no LLM in this step | §3.1, p.5 |
| ExV05 | "assertion fails", "CEX_1 validated" | Fig. 3 panel 5 red callout, p.13 |
| ExV06 | reachable → wrong_fact → replace; spurious → too_weak → strengthen | §3.2, p.5; App. I.5 p.28 |
| ExV06 | brs1 verdict `wrong_fact` and rationale | Fig. 3 panel 3, p.13 |
| ExV06 | findmax: `max = 0` not in `[-1, -1]`, spurious, `too_weak` | Fig. 8, p.23 |
| ExV07 | five candidate proofs | §4.1, p.6 (5 mutants) |
| ExV07 | shared pattern "i = 0 and sum[0] > 0" | App. A.1 text, p.13 |
| ExV07 | rank by # validated CEXs blocked; PDR/IC3 inspiration; definition of blocking | p.6 "Mutant ranking"; Def. 2.2 p.4 |
| ExV07 | "mutant_1 blocks all CEXs and passes Verus" | App. A.1, p.13 ("mutant-1 successfully blocks all counterexamples and passes Verus verification") |
| ExV07 | "assertion passes: CEX_1 blocked" | Fig. 3 panel 5 green callout, p.13 |
| ExV07 | reference proof uses the same guard | repo `cleaned-verusbench/Diffy/verified/brs1.rs:35` (`i > 0 ==> sum[0] <= i`) |
| ExV08 | pipeline nodes and edges | Fig. 2, p.4; Alg. 1–3, p.19 |
| ExV08 | "≤ 10 CEXs" (default 10), "retry if not SAT" | §4.3 p.7 (default 10 CEXs); Alg. 2 p.19 |
| ExV08 | "5 candidates", "max 10" iterations | §4.1, p.6 |
| ExV09 | Sonnet-4.5 success rates ExVerus / AutoVerus / Iterative Refinement: VerusBench 88.4 / 75.3 / 83.6; DafnyBench 95.5 / 95.5 / 95.5; LCBench 28.6 / 14.3 / 25.0; HumanEval 41.2 / 27.9 / 29.4 | Table 1, p.7 (BRIEF R2) |
| ExV09 | DeepSeek-V3.1 VerusBench 71.9 / 24.7 / 60.3 | Table 1, p.7 (BRIEF R3) |
| ExV09 | ObfsBench 266 tasks; DeepSeek-V3.1 ExVerus 73.9–86.5%, AutoVerus 24.7–36.5% over 6 strategies | Table 2, p.7; size p.6, App. E p.20 (BRIEF R4) |
| ExV10 | ablation ObfsBench DeepSeek-V3.1: ExVerus 81.6 vs ExVerus_NO_MUT 65.4 | Table 4, p.8 (BRIEF R6); label per §4.2 p.7 ("instructs the LLM to directly fix the proof based on the counterexamples without validation"; no error-specific mutators); Table 4 caption "Ablation study on mutation strategies" |
| ExV10 | blocking mutants 172/243 (70.78%) verify vs non-blocking 38/153 (24.84%), ExVerus_ONE_CEX | §4.3, p.8 (BRIEF R8) |
| ExV10 | cost/time per task: DeepSeek-V3.1 $0.04 vs $0.17, 720.3 s vs 2989.1 s; GPT-4o $0.42 vs $0.69, 250.0 s vs 233.9 s | Table 3, p.8 (BRIEF R5, R5b) |
| ExV11 | validation only for loop-invariant errors; other CEXs unvalidated | §3.1 p.5; §5 p.8 |
| ExV11 | CEX generation can fail or be wrong; only Verus trusted | p.2; p.5 |
| ExV11 | passing Verus ≠ user intent | Impact Statement, p.9 |
| ExV11 | weaker on assert / proof-block tasks (GPT-4o) | Table 5, p.23; App. H.3 p.22 |
| ExV11 | Verus version change lowered AutoVerus baseline (narration: built for older Verus, scores lower on the newer version; GPT-4o VerusBench 75.33% vs 52.7%) | App. H.4, p.22; footnote 3, p.6 |
| ExV12 | bridge sentence | `docs/SERIES.md` (fixed bridge line) |

## Deliberately not shown (numbers policy, `docs/SERIES.md`)

"38% more on average" (p.2), "+60.92%" (p.6), "+45%" (project page), "64.49%" (p.8 typo), "$0.04 per task" without the model
name, "2×" claims, the p.7 robustness summary sentence, and all project-page numbers.
