# Vero — sources

Paper = *Vero: Can AI Agents Build Formally Verified Software Repositories?*, arXiv 2608.13522v1, NeurIPS 2026 (`papers/vero.pdf`; PDF page numbers = printed page numbers).
Repo = `github.com/sunblaze-ucb/vero` at commit `0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09` (read-only clone `repos/vero`).
Quotes and numbers below were re-checked against the paper's text layer; figure values are used only where the main text states them.

## Code on screen

| Scene | File (episodes/vero/examples/) | Exact source | Trim |
|---|---|---|---|
| Vero01Hook | `hook_dijkstar_spec.lean` | Repo `benchmarks/dijkstar/Dijkstar/Spec/ShortestPath.lean` lines 200-203 | doc comment (194-199) omitted |
| Vero02Instance | `fig2_interface.lean` | Paper Fig. 2, p.5 (API signatures, RepoImpl, canonical) | figure comments and some blank lines dropped |
| Vero02Instance | `fig2_spec.lean` | Paper Fig. 2, p.5 (spec + theorem) | figure comments dropped |
| Vero05Grader | `grader_slot.lean` | Repo `reference/BankLedger/BankLedger/Proof_modecodeproof/Account.lean` lines 33-36 | none |
| Vero06Base64, Vero07Audit | `base64_padding_spec_paper.lean` | Paper App. F Audit 1, p.24, listing lines 1-2 (pre-fix) | none |
| Vero06Base64, Vero07Audit | `base64_reject_spec_paper.lean` | Paper App. F Audit 1, p.24, listing lines 4-8 (pre-fix) | none |
| Vero07Audit | `base64_fix_paper.lean` | Paper App. F Audit 1, p.24, fix listing line 1 | none (PDF glyph for ≠ normalised) |
| Vero08Trust | `trust_dijkstar_oracle_paper.lean` | Paper App. D, p.20 | none |
| Vero08Trust | `trust_base58_native_decide_paper.lean` | Paper App. D Layer 2, p.19 | none |

## Numbers and claims on screen or in narration

| Scene | Item | Source |
|---|---|---|
| Vero01Hook | author list (all 11 authors) | Paper p.1 |
| Vero01Hook | venue NeurIPS 2026 | docs/SERIES.md |
| Vero01Hook | dijkstar is a Python library | Paper Table 3, p.16 |
| Vero02Instance | instance format, RepoImpl, canonical, spec as predicate | Paper §3.1 p.4, Fig. 2 p.5 |
| Vero02Instance | two modes; code-and-proof may refactor and can invalidate proofs across modules | Paper §3.2, p.5 |
| Vero03Scale | 43 instances; 13 Track 1 (Dafny, Verus, Coq) + 30 Track 2 (Python) | Paper §3.4 p.6; Table 1 p.7 |
| Vero03Scale | 743 scored APIs, 2,705 scored specifications | Paper p.2, §3.4 p.6, Fig. 1 p.4 |
| Vero03Scale | domains (smart contracts, consensus, data structures, numerical utilities) | Paper §3.4, p.6 |
| Vero03Scale | no public Lean 4 ground truth; "largely free" of contamination | Paper "Contamination", p.7 |
| Vero03Scale | full solve only; open spec leaves room for a bug | Paper §3.2 p.5; p.8 |
| Vero04Architecture | Fig. 1 nodes/edges; audit route returns evidence to curation | Paper Fig. 1 + caption, p.4 |
| Vero04Architecture | stage list; LLM agent per stage with curator approval | Paper §3.3, p.6 |
| Vero05Grader | three layers; naive "does it compile" check | Paper App. D, p.19 |
| Vero05Grader | slot re-rendering onto a fresh copy; weakened spec / deleted obligation revert | Paper App. D Layer 1, p.19 |
| Vero05Grader | `#print axioms` on every scored theorem; allowlist Classical.choice, propext, Quot.sound | Paper App. D Layer 2, p.19 |
| Vero05Grader | 368 spec outcomes rejected at this layer | Paper App. D, p.19 |
| Vero05Grader | hollow instances, priority shadowing, decidability laundering; `@[implemented_by]` in Impl/ voids the run | Paper App. D Layer 3, p.19-20 |
| Vero06Base64 | verdict translated from a Verus project | Paper Table 3, p.16 |
| Vero06Base64 | '=' is 0x3D, lies in (0x39, 0x41) between '9' and 'A'; no implementation can satisfy both | Paper App. F Audit 1, p.24 |
| Vero07Audit | joint_unsat claim `¬ ∃ impl : RepoImpl, spec_char_to_bits_padding impl ∧ spec_char_to_bits_reject impl` (Eq. (3) with S' = the two specs; shown as text) | Paper §3.5 Eq. (3), p.7; App. F Audit 1, p.24 |
| Vero07Audit | GPT-5.5 (xhigh) flagged the pair via a joint-unsatisfiability proof; "collapses to a one-line 0x3D < 0x41 ∧ 0x3D > 0x39 contradiction" | Paper p.24 |
| Vero07Audit | fix excludes 0x3D; "survived manual review and type-checking but was caught automatically by the agent" | Paper p.24 |
| Vero07Audit | 38 defects across 9 instances, 6 joint-unsat groups, all repaired before evaluation | Paper App. F, p.24 |
| Vero07Audit | Table 6 categories: 18 / 17 / 2 / 1; direct conflict = verdict (1) | Paper Table 6, p.24 |
| Vero08Trust | an agent's spec-oracle submission on dijkstar during benchmark development; definitionally true; 20,440 graphs; grader voids run as impl_oracle | Paper App. D, p.20 |
| Vero08Trust | native_decide evaluated in compiler, Lean.ofReduceBool; 28 of 53 specs in that cell fail this way | Paper App. D Layer 2, p.19 |
| Vero09Results | 4 configurations, 2 modes, 43 instances; 90-minute budget | Paper §4.1 p.7; Fig. 3 caption p.8 |
| Vero09Results | full solves code-and-proof: GPT-5.5 xhigh 27, Opus 4.8 8, GPT-5.5 mid 2, Sonnet 5 2 (of 43) | Paper p.8 text; Fig. 3(a) |
| Vero09Results | 87.3% of specs passed by GPT-5.5 (xhigh), code-and-proof | Paper p.8 |
| Vero09Results | median 73.6% of proof lines in helper theorems (code-and-proof full solves) | Paper p.8; Fig. 5(b) |
| Vero09Results | 10 instances resist all eight configurations | Paper p.2, p.8 |
| Vero10Takeaway | Lean 4 only; audit certifies satisfiability, not semantic correctness/completeness | Paper Limitations, p.11 |
| Vero10Takeaway | sortedcontainers linear scan, O(n) lookup instead of O(log n), satisfies every scored spec | Paper App. H.4, p.31 |
| Vero10Takeaway | code, specs and proofs coherent across modules ("reason globally about the consistency of the entire codebase"); 27 of 43 fully solved | Paper §1, p.2; p.8 |

## Not used (per numbers policy / brief)

- Fig. 7b segment values (42 / 10.8 / 33.5 / 13.7) and Fig. 8a per-type failure rates: label pairing is [inferred] in the brief.
- Any claim about which parts Yuechun Sun contributed.
