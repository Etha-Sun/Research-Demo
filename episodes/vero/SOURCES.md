# Episode 3: Vero — sources

Paper = *Vero: Can AI Agents Build Formally Verified Software Repositories?*, arXiv 2608.13522v1 (`papers/vero.pdf`; PDF page numbers = printed page numbers).
Repo = `github.com/sunblaze-ucb/vero` at commit `0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09` (read-only clone `repos/vero`).
Quotes and numbers below were re-checked against the paper's text layer; figure values are used only where the main text states them.

## Code on screen

| Scene | File (episodes/vero/examples/) | Exact source | Trim |
|---|---|---|---|
| Vero02Hook | `hook_dijkstar_spec.lean` | Repo `benchmarks/dijkstar/Dijkstar/Spec/ShortestPath.lean` lines 200-203 | doc comment (194-199) omitted |
| Vero03Instance | `fig2_interface.lean` | Paper Fig. 2, p.5 (API signatures, RepoImpl, canonical) | figure comments and some blank lines dropped |
| Vero03Instance | `fig2_spec.lean` | Paper Fig. 2, p.5 (spec + theorem) | figure comments dropped |
| Vero06Grader | `grader_slot.lean` | Repo `reference/BankLedger/BankLedger/Proof_modecodeproof/Account.lean` lines 33-36 | none |
| Vero06Grader | `grader_allowlist.py` | Repo `src/vero/evaluation/axioms.py` line 31 | none |
| Vero07Base64, Vero08Audit | `base64_padding_spec_paper.lean` | Paper App. F Audit 1, p.24, listing lines 1-2 (pre-fix) | none |
| Vero07Base64, Vero08Audit | `base64_reject_spec_paper.lean` | Paper App. F Audit 1, p.24, listing lines 4-8 (pre-fix) | none |
| Vero08Audit | `base64_fix_paper.lean` | Paper App. F Audit 1, p.24, fix listing line 1 | none (PDF glyph for ≠ normalised) |
| Vero08Audit | `joint_unsat_claim_form_repo.lean` | Repo `benchmarks/dijkstar/Dijkstar/Harness.lean` lines 34-35 (macro doc comment; same macro in verdict Harness.lean 54-66) | none; shown as the generic claim form, not the agent's proof |
| Vero09Trust | `trust_dijkstar_oracle_paper.lean` | Paper App. D, p.20 | none; labelled "illustrative" (`isMinWalkCost` not in repo) |
| Vero09Trust | `trust_base58_native_decide_paper.lean` | Paper App. D Layer 2, p.19 | none |

## Numbers and claims on screen or in narration

| Scene | Item | Source |
|---|---|---|
| Vero01Open | author list (all 11 authors), 2026 | Paper p.1 (arXiv 2608.13522v1, "Preprint", p.1 footer) |
| Vero02Hook | dijkstar is a Python library | Paper Table 3, p.16 |
| Vero03Instance | instance format, RepoImpl, canonical, spec as predicate | Paper §3.1 p.4, Fig. 2 p.5 |
| Vero03Instance | two modes; code-and-proof may refactor and can invalidate proofs across modules | Paper §3.2, p.5 |
| Vero04Scale | 43 instances; 13 Track 1 (Dafny, Verus, Coq) + 30 Track 2 (Python) | Paper §3.4 p.6; Table 1 p.7 |
| Vero04Scale | 743 scored APIs, 2,705 scored specifications | Paper p.2, §3.4 p.6, Fig. 1 p.4 |
| Vero04Scale | domains (smart contracts, consensus, data structures, numerical utilities) | Paper §3.4, p.6 |
| Vero04Scale | no public Lean 4 ground truth; "largely free" of contamination | Paper "Contamination", p.7 |
| Vero04Scale | full solve only; open spec leaves room for a bug | Paper §3.2 p.5; p.8 |
| Vero05Architecture | Fig. 1 nodes/edges; audit route returns evidence to curation | Paper Fig. 1 + caption, p.4 |
| Vero05Architecture | stage list; LLM agent per stage with curator approval | Paper §3.3, p.6 |
| Vero06Grader | three layers; naive "does it compile" check | Paper App. D, p.19 |
| Vero06Grader | slot re-rendering onto a fresh copy; weakened spec / deleted obligation revert | Paper App. D Layer 1, p.19 |
| Vero06Grader | allowlist Classical.choice, propext, Quot.sound | Paper App. D Layer 2, p.19; repo axioms.py:31 |
| Vero06Grader | 368 spec outcomes rejected at this layer | Paper App. D, p.19 |
| Vero06Grader | hollow instances, priority shadowing; `unsafe` and `@[implemented_by]` in Impl/ void the run | Paper App. D Layer 3, p.19-20; repo `src/vero/evaluation/hygiene.py` 20-27, `grade.py` 11-23 |
| Vero07Base64 | verdict translated from a Verus project | Paper Table 3, p.16 |
| Vero07Base64 | '=' is 0x3D, lies in (0x39, 0x41) between '9' and 'A'; no implementation can satisfy both | Paper App. F Audit 1, p.24 |
| Vero08Audit | GPT-5.5 (xhigh) flagged the pair via a joint-unsatisfiability proof; "collapses to a one-line 0x3D < 0x41 ∧ 0x3D > 0x39 contradiction" | Paper p.24 |
| Vero08Audit | fix excludes 0x3D (paper version); "survived manual review and type-checking but was caught automatically by the agent" | Paper p.24 |
| Vero08Audit | released repo's different fix form (split range) | Repo `benchmarks/verdict/Verdict/Spec/Base64.lean` lines 42-48 |
| Vero08Audit | 38 defects across 9 instances, 6 joint-unsat groups, all repaired before evaluation | Paper App. F, p.24 |
| Vero08Audit | Table 6 categories: 18 / 17 / 2 / 1; direct conflict = verdict (1) | Paper Table 6, p.24 |
| Vero09Trust | spec-oracle trick on dijkstar during benchmark development; definitionally true; 20,440 graphs; grader voids run as impl_oracle | Paper App. D, p.20 |
| Vero09Trust | native_decide evaluated in compiler, Lean.ofReduceBool; 28 of 53 specs in that cell fail this way | Paper App. D Layer 2, p.19 |
| Vero10Results | 4 configurations, 2 modes, 43 instances; 90-minute budget | Paper §4.1 p.7; Fig. 3 caption p.8 |
| Vero10Results | full solves code-and-proof: GPT-5.5 xhigh 27, Opus 4.8 8, GPT-5.5 mid 2, Sonnet 5 2 (of 43) | Paper p.8 text; Fig. 3(a) |
| Vero10Results | 87.3% of specs passed by GPT-5.5 (xhigh), code-and-proof | Paper p.8 |
| Vero10Results | median 73.6% of proof lines in helper theorems (code-and-proof full solves) | Paper p.8; Fig. 5(b) |
| Vero10Results | 10 instances resist all eight configurations | Paper p.2, p.8 |
| Vero11Limits | Lean 4 only; concurrent/temporal protocols absent; audit certifies satisfiability, not semantic correctness/completeness | Paper Limitations, p.11 |
| Vero11Limits | sortedcontainers linear scan, O(n) lookup instead of O(log n), satisfies every scored spec | Paper App. H.4, p.31 |
| Vero12Bridge | bridge line | docs/SERIES.md (fixed text) |

## Not used (per numbers policy / brief)

- Fig. 7b segment values (42 / 10.8 / 33.5 / 13.7) and Fig. 8a per-type failure rates: label pairing is [inferred] in the brief.
- Any claim about which parts Yuechun Sun contributed.
