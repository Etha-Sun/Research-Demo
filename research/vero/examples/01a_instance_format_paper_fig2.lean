-- SOURCE: Vero paper (arXiv 2608.13522v1), Figure 2, page 5.
-- Transcribed verbatim from the PDF text layer (pypdf extraction); line numbers from the
-- figure removed; indentation restored by hand (the text layer drops leading spaces).
-- The figure's line-12 comment wraps in the PDF; it is joined to one line here.
-- API signatures
abbrev CreateAccountSig := AccountId -> Ledger -> Ledger
abbrev AccountExistsSig := AccountId -> Ledger -> Bool
abbrev GetBalanceSig := AccountId -> Ledger -> Option Balance

-- Interface structure: one field per API signature
structure RepoImpl where
  createAccount : CreateAccountSig
  accountExists : AccountExistsSig
  getBalance : GetBalanceSig

-- Canonical implementation (instantiated to reference implementation in proof-only mode and agent solution in code-and-proof mode)
def canonical : RepoImpl := {
  createAccount := Bank.createAccount,
  accountExists := Bank.accountExists,
  getBalance := Bank.getBalance,
}

-- Specification: a predicate over implementations
def spec_create_zero_balance (impl : RepoImpl) : Prop :=
  ∀ (id : AccountId) (ledger : Ledger),
    impl.accountExists id ledger = false ->
    impl.getBalance id (impl.createAccount id ledger) = some 0

-- Theorem: Proof obligation on the canonical implementation
theorem proof_create_zero_balance : spec_create_zero_balance canonical := by
  sorry
