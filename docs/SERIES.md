# Series design: "From a failed proof to a trusted one"

Four connected episodes about Yuechun Sun's research in LLMs and formal verification. Each runs 6 to 9 minutes.
The research briefs are in `research/<ep>/BRIEF.md` and the production rules in `docs/PRODUCTION-SPEC.md`.

## The through-line

One question runs through all four episodes. When a proof fails, what concrete evidence tells us why, and how do we make
sure the fixed proof means what we think it means?

- **Counterexamples** are the evidence. They are concrete states or inputs that make a failure visible.
- **Trust** is the guard. Every repair is re-checked by a verifier, specs may not be weakened, and assumptions stay visible.

The episodes climb in scale and in the strength of the trust question:

| # | Episode | Scale | Who produces the counterexample | Trust question |
|---|---------|-------|---------------------------------|----------------|
| 1 | ExVerus | one loop invariant, Rust/Verus | an LLM writes a small solver query; a validator confirms it | the LLM may be wrong, so Verus re-checks every repair |
| 2 | TopoVerus | one function, learned model | the model itself, trained with RL | the reward can be gamed, so a safety gate checks that code and specs are untouched |
| 3 | Vero | whole repositories, Lean 4 | agents, and even agents auditing the specs | proofs can be true yet meaningless, so the checker controls axioms and specs |
| 4 | Vekto | real optimised SIMD kernels, C | the pipeline finds inputs where two kernels disagree | which assumptions does a C-level equivalence proof rely on? |

Theme line for the series map: **"counterexamples connect a failed proof to its repair"**, the default caption of `series_map()`.

## Episode openings and closings (fixed, so the series reads as one)

Each episode opens with the series map, its own tile lit, and the recap line. It ends with its bridge line and the map with
the next tile lit. Use these sentences in narration.json; small wording changes are fine but keep the meaning.

**Episode 1, ExVerus**
- Series intro (first beat of the whole series, about 20 s): "This is a four-part tour of one research thread: getting AI
  systems to write proofs we can actually trust. Each part climbs a level: from fixing one loop invariant, to a model
  that learns to fix proofs, to proving whole software repositories, to proving that optimised machine-level kernels
  still compute the same thing."
- Bridge: "ExVerus *searches* for a counterexample at every repair. What if the model could learn to produce the
  counterexample itself?"

**Episode 2, TopoVerus**
- Recap: "Last time, ExVerus showed that a concrete counterexample is better feedback than a verifier's one-line error."
- Bridge: "TopoVerus repairs proofs one function at a time. Real verified software is a repository of modules that
  depend on each other. Can agents build that?"

**Episode 3, Vero**
- Recap: "So far we repaired single proofs, first by searching for counterexamples and then with a model trained to
  produce them."
- Bridge: "Vero's lesson is that the checker and the specification decide what a proof means. In the last episode we
  take that lesson to real systems code: optimised SIMD kernels, where the question is whether two programs compute
  the same thing."

**Episode 4, Vekto**
- Recap: "We have seen counterexamples drive proof repair, and we have seen that a proof is only as good as its spec and
  its checker."
- Closing of the series: return to the map with all tiles lit. One sentence per episode on what the counterexample was:
  a program state, a learned explanation, an audit of a spec, an input on which two kernels disagree. Then the trust
  thread in one line: every proof re-checked, no spec silently weakened, every assumption stated.

## Motivated examples (decided)

| Ep | Example | Source | Notes |
|----|---------|--------|-------|
| 1 | Cold open: `findmax`. Verus's raw `unknown` model (`i=537`) next to the clean counterexample `nums=[-1,-1], max=0` | Fig. 1 p.3 | Cold open only. The paper does not show ExVerus's fix for it, so do not show one. |
| 1 | Main: `brs1`. Buggy invariant `sum[0] <= i as i32` → "invariant not satisfied before loop" → CEX `sum=vec![1], i=0` → triage "wrong_fact" → fix `i > 0 ==> sum[0] <= i as i32` → verified | Fig. 3 p.13 | The only example with every stage shown. AutoVerus needed 16 attempts and still failed (paper). |
| 2 | Main: Case B, LeetCode 121 max-profit: full-array invariant → counterexample `prices=[5,3,7]` → rationale → repaired proof | Fig. 4 p.9, App. B p.17 | The ending depends on our Verus check (`research/verification/RESULTS.md`). If the recorded repair does not verify, say "the paper reports…" and show only what is recorded; do not claim "verified" for code we could not verify. |
| 2 | Curriculum / graph reward: binary-search insertion (Fig. 1–2), labelled "illustrative example from the paper" | Fig. 1–2 | Worked reward example: label as our reading of the figure where the edge set is inferred. |
| 2 | Safety gate: the repo unit test where moving an `assume` makes Verus say "verified" but the gate says "unsafe" | repo test | Label it "test case from the released code". |
| 3 | Main: verdict Base64. Two specs contradict each other ('=' is padding vs. all bytes 0x39..0x41 rejected); GPT-5.5 proves them jointly unsatisfiable | p.24 | The paper describes but does not print the proof, so show the two specs, not an invented proof. Use the paper's version of the fix and label it. |
| 3 | Short: dijkstar `@[implemented_by]` (a proof can be true by definition while the binary runs other code) | p.19–20 | A trust hook into episode 4. Mark the paper snippet "illustrative" (the name is not in the repo). |
| 4 | Main: E1 f32-vmax NaN. NEON `vmaxq_f32` returns the NaN, the optimised RVV `vfmax` returns 1.0 for `(NaN 0x7fc12345, 1.0)` | Vekto brief §6 Rank 1 | Main result kept as "A ≠ Bopt"; the separate "no NaN" condition C-001 is counted separately. Show the one-line kernels side by side. |
| 4 | Walk-through: x24-transposec SSSE3 → RVV, 12 gates passed, 435 x86 VCs + 22 RVV VCs per VLEN, 5,990 s | APPROVAL-x24-rvv.json | Established result. |

## Numbers policy (from the research briefs' audit)

- **ExVerus.** Do **not** use the intro's "38% more on average", "+60.92%" or "+45%". The briefs found they cannot be
  recomputed. Do not use p.8's "64.49%" or the "$0.04 per task" without its model. Prefer per-table numbers quoted with the
  table and model setting.
- **TopoVerus.** 61.6% / 72.2% Safe-Pass@1/@3 over 471 problems in 7 benchmarks; +5.7 / +6.3 over Claude Sonnet 4.5.
  Ablations: the counterexample format alone +11.2 points; the graph reward vs. pass/fail-only RL +7.9 points; dependency
  order followed 43.8% → 95.8%. All are from the paper; cite the table. Use paper definitions (pass/fail reward, subset
  enumeration). The repo differs; mention it only if needed, labelled.
- **Vero.** 43 repositories, 743 APIs, 2,705 specs; best setup GPT-5.5 xhigh fully solves 27/43 with 87.3% of specs;
  10 repositories resist every setup; 38 benchmark defects found by the audit route. Values marked [inferred] in the
  brief stay off screen.
- **Vekto.** Only numbers from APPROVAL/LEDGER files; dates as of 2026-11-23; label E1–E4 status as in progress.

## Attribution on screen

- ExVerus: Yang, Sun, Wu, Caridad, Yuan, Yao, Lu, Pei. ICML 2026.
- TopoVerus: Sun, Yang, Pei. NeurIPS 2026.
- Vero: Ye, Lou, Sun, Song, Yan, Kasriel, Zhang, Yang, Kong, He, Song (Dawn Song). 2026. The arXiv v1 PDF is marked "Preprint"; the homepage lists NeurIPS 2026, so no venue is shown on screen. Do not claim which parts are Yuechun's.
- Vekto: ongoing work, unpublished. Say "work in progress" on its title card.
