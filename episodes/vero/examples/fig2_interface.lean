-- SOURCE: Vero paper (arXiv 2608.13522v1), Figure 2, page 5; via research/vero/examples/01a_instance_format_paper_fig2.lean.
-- TRIM: the figure's comment lines and blank lines between blocks are dropped; code lines verbatim.
-- Shown as panel 1 of 2 (interface part of the figure).
abbrev CreateAccountSig := AccountId -> Ledger -> Ledger
abbrev AccountExistsSig := AccountId -> Ledger -> Bool
abbrev GetBalanceSig := AccountId -> Ledger -> Option Balance

structure RepoImpl where
  createAccount : CreateAccountSig
  accountExists : AccountExistsSig
  getBalance : GetBalanceSig

def canonical : RepoImpl := {
  createAccount := Bank.createAccount,
  accountExists := Bank.accountExists,
  getBalance := Bank.getBalance,
}
