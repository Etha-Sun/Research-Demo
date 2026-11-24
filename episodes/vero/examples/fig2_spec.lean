-- SOURCE: Vero paper (arXiv 2608.13522v1), Figure 2, page 5; via research/vero/examples/01a_instance_format_paper_fig2.lean.
-- TRIM: the figure's comment lines are dropped; code lines verbatim. Panel 2 of 2 (spec + proof obligation).
def spec_create_zero_balance (impl : RepoImpl) : Prop :=
  ∀ (id : AccountId) (ledger : Ledger),
    impl.accountExists id ledger = false ->
    impl.getBalance id (impl.createAccount id ledger) = some 0

theorem proof_create_zero_balance : spec_create_zero_balance canonical := by
  sorry
