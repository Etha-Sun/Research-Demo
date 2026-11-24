-- SOURCE: github.com/sunblaze-ucb/vero @ 0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09
--   reference/BankLedger/BankLedger/Spec/Account.lean, lines 13-17 (verbatim).
-- NOTE: the released exemplar nests APIs in a bundle (impl.bankLedger.*); the paper's Figure 2 flattens this to impl.*

/-- Creating a new account gives it zero balance. -/
def spec_create_zero_balance (impl : RepoImpl) : Prop :=
  ∀ (id : AccountId) (ledger : Ledger),
    impl.bankLedger.accountExists id ledger = false →
    impl.bankLedger.getBalance id (impl.bankLedger.createAccount id ledger) = some 0
