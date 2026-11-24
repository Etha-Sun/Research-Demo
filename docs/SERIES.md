# Four independent research videos

There are four self-contained explainer videos, one per work. They share a visual style, but no video depends on
another: none recaps a previous episode, bridges to a next one, or draws analogies to the other works.
(Author decision, 2026-11-23.)

| Video | Work | Venue / status | Primary source |
|-------|------|----------------|----------------|
| ExVerus | Verus proof repair via counterexample reasoning | ICML 2026 | arXiv 2603.25810 |
| TopoVerus | Curriculum proof repair with learned counterexamples | NeurIPS 2026 | arXiv 2611.13627 |
| Vero | Can AI agents build formally verified software repositories? | NeurIPS 2026 | arXiv 2608.13522 |
| Vekto | C-level equivalence of SIMD kernel migrations (QCP + Coq) | ongoing | this research repository |

## Principles

1. **Paper first.** The arXiv version of each paper is the source of truth: its figures, examples, definitions and
   numbers. Released code is used only to show material the paper also describes. Where the paper and the code differ,
   follow the paper. Vekto has no paper, so its source is the research repository (Introduction V2, approved packages).
2. **State things plainly.** Present the paper's examples and figures as the paper presents them, with a normal
   citation footnote (for example "ExVerus, Fig. 3"). Avoid defensive labels such as "our reading", "illustrative" or
   "not shown in the paper", and avoid hedges in the narration. Do not add claims the paper does not make.
3. **Self-contained.** Each video:
   - opens with the title card (title, one-line subtitle, authors, venue) and a concrete hook;
   - explains the background it needs;
   - walks through the motivated example in real code;
   - explains the method with an architecture diagram;
   - shows the key results;
   - closes with its own takeaway.
4. **Code examples are verbatim** from the paper (or, for Vekto, the repository). Trims are documented in the example
   headers and SOURCES.md.

## Motivated examples

| Video | Example | Source |
|-------|---------|--------|
| ExVerus | Cold open: `findmax`, Verus's raw `unknown` model vs. the clean counterexample. Main: `brs1`, buggy invariant `sum[0] <= i as i32` → error → CEX `sum=vec![1], i=0` → triage "wrong_fact" → fix `i > 0 ==> sum[0] <= i as i32` → passes Verus | Fig. 1 p.3, Fig. 3 p.13 |
| TopoVerus | Case B, LeetCode 121 max-profit: counterexample `prices=[5,3,7]` → rationale → repaired proof. Graph reward on the binary-search example. Safety gate | Fig. 1–2, Fig. 4 p.9, App. B p.17 |
| Vero | verdict Base64: two specs contradict each other; the agent proves them jointly unsatisfiable. Trust: `@[implemented_by]`, `native_decide` | p.24, p.19–20 |
| Vekto | E1 f32-vmax NaN: NEON returns NaN, the optimised RVV returns 1.0. Walk-through: x24-transposec SSSE3 → RVV | repository |

## Numbers

- **ExVerus.** Use per-table values with the model setting. Do not use "38% more on average", "+60.92%", "+45%",
  p.8's "64.49%", or "$0.04 per task" without its model.
- **TopoVerus.**
  - 61.6% / 72.2% Safe-Pass@1/@3 over 471 problems in 7 benchmarks;
  - +5.7 / +6.3 over Claude Sonnet 4.5;
  - the counterexample format alone adds +11.2 points;
  - the graph reward adds +7.9 points over pass/fail-only RL;
  - dependency order followed rises from 43.8% to 95.8%.
- **Vero.**
  - 43 repositories, 743 APIs, 2,705 specs;
  - GPT-5.5 xhigh fully solves 27/43 with 87.3% of specs;
  - 10 repositories resist every setup;
  - 38 benchmark defects found.
- **Vekto.**
  - E2: 24 approved migrations;
  - E3: 14 approved pairs + 1 proved not equivalent;
  - E1: per APPROVAL files;
  - x24 package: 12/12 gates, 435 x86 VCs + 22 RVV VCs per VLEN, 5,990 s.

## Attribution

- ExVerus: Yang, Sun, Wu, Caridad, Yuan, Yao, Lu, Pei. ICML 2026.
- TopoVerus: Sun, Yang, Pei. NeurIPS 2026.
- Vero: Ye, Lou, Sun, Song, Yan, Kasriel, Zhang, Yang, Kong, He, Song. NeurIPS 2026.
- Vekto: ongoing work.
