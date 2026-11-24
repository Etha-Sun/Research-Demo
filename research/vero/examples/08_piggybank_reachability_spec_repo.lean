-- SOURCE: github.com/sunblaze-ucb/vero @ 0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09
--   benchmarks/piggybank/PiggybankV2/Spec/PiggyBankCorrect.lean, lines 153-161 (verbatim).
-- Paper p.20-21: all 8 configurations fail exactly the 6 piggybank specs quantifying over reachable ChainState/ChainTrace.

/-- For a reachable deployed PiggyBank with no outgoing actions, the on-chain account balance equals the stored contract balance. -/
def spec_balance_on_chain (impl : RepoImpl) : Prop :=
  ∀ (bstate : ChainState) (caddr : Address),
    reachable bstate →
      env_contracts bstate caddr = some (toWeakContract (contract impl)) →
        outgoing_acts bstate caddr = [] →
          ∃ cstate : State,
            contract_state bstate caddr = some cstate ∧
              env_account_balances bstate caddr = cstate.balance
