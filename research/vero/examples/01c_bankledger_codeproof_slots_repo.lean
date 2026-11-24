-- SOURCE: github.com/sunblaze-ucb/vero @ 0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09
--   reference/BankLedger/BankLedger/Proof_modecodeproof/Account.lean, lines 26-53 (verbatim).
-- Shows the three audit-aware slots per spec in code-and-proof mode: prove_S / unsat_S / sat_S,
-- delimited by '!benchmark @start ... @end' markers (only marker interiors are graded).

-- !benchmark @start global_aux
-- !benchmark @end global_aux

-- ── spec_create_zero_balance ─────────────────────────────────

-- !benchmark @start proof_aux def=prove_create_zero_balance
-- !benchmark @end proof_aux def=prove_create_zero_balance

theorem prove_create_zero_balance : spec_create_zero_balance canonical := by
-- !benchmark @start proof def=prove_create_zero_balance kind=prove target=spec_create_zero_balance
  sorry
-- !benchmark @end proof def=prove_create_zero_balance

-- !benchmark @start proof_aux def=unsat_create_zero_balance
-- !benchmark @end proof_aux def=unsat_create_zero_balance

theorem unsat_create_zero_balance : ¬ ∃ impl : RepoImpl, spec_create_zero_balance impl := by
-- !benchmark @start proof def=unsat_create_zero_balance kind=unsat target=spec_create_zero_balance
  sorry
-- !benchmark @end proof def=unsat_create_zero_balance

-- !benchmark @start proof_aux def=sat_create_zero_balance
-- !benchmark @end proof_aux def=sat_create_zero_balance

theorem sat_create_zero_balance : ∃ impl : RepoImpl, spec_create_zero_balance impl := by
-- !benchmark @start proof def=sat_create_zero_balance kind=sat target=spec_create_zero_balance
  sorry
-- !benchmark @end proof def=sat_create_zero_balance
