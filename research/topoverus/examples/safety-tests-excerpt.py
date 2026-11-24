# SOURCE: github.com/Etha-Sun/Topoverus @ 878496237052eeccdd8478b9f9037041affe1431
# FILE: tests/test_trust.py lines 75-172 (Verus+Lynette integration tests; these are AUTHOR-CONSTRUCTED unit tests, not model outputs; they only run when VERUS_BIN and LYNETTE_BIN are set; NOT executed here)
# ---- verbatim content below (no edits) ----
@unittest.skipUnless(os.environ.get("VERUS_BIN") and os.environ.get("LYNETTE_BIN"),
                     "Set VERUS_BIN and LYNETTE_BIN for real-tool trust regressions")
class TrustedContractIntegrationTests(unittest.TestCase):
    original = """use vstd::prelude::*;
verus! {
#[verifier::external_body]
proof fn helper() ensures true { }
fn target() ensures false { }
}
fn main() {}
"""

    def test_verifier_success_cannot_hide_changed_trusted_contract(self):
        candidate = self.original.replace("helper() ensures true", "helper() ensures false").replace(
            "fn target() ensures false { }", "fn target() ensures false { proof { helper(); } }")
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            self.assertEqual(verify(self.original, os.environ["VERUS_BIN"], work).status, "verification_failed")
            self.assertEqual(verify(candidate, os.environ["VERUS_BIN"], work).status, "verified")
            self.assertIsNone(trust_change(self.original, candidate))
            self.assertEqual(safety(self.original, candidate, os.environ["LYNETTE_BIN"], work).status, "unsafe")

    def test_existing_annotation_cannot_be_relocated_to_target(self):
        candidate = self.original.replace("#[verifier::external_body]\nproof fn helper", "proof fn helper").replace(
            "fn target()", "#[verifier::external_body]\nfn target()")
        with tempfile.TemporaryDirectory() as directory:
            self.assertIsNone(trust_change(self.original, candidate))
            self.assertEqual(safety(self.original, candidate, os.environ["LYNETTE_BIN"], Path(directory)).status, "unsafe")

    def test_ignored_body_change_and_normal_proof_repair_are_allowed(self):
        candidate = self.original.replace("helper() ensures true { }", "helper() ensures true { assert(false); }").replace(
            "fn target() ensures false { }", "fn target() ensures false { proof { helper(); } }")
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(safety(self.original, candidate, os.environ["LYNETTE_BIN"], Path(directory)).status, "safe")

    def test_existing_assumption_cannot_hide_changed_helper_contract(self):
        original = self.original.replace('#[verifier::external_body]\nproof fn helper() ensures true { }',
            'proof fn helper() requires false ensures false { assume(false); }')
        candidate = original.replace('requires false', 'requires true').replace(
            'fn target() ensures false { }', 'fn target() ensures false { proof { helper(); } }')
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            self.assertEqual(verify(candidate, os.environ["VERUS_BIN"], work).status, "verified")
            self.assertIsNone(trust_change(original, candidate))
            self.assertEqual(safety(original, candidate, os.environ["LYNETTE_BIN"], work).status, "unsafe")
            repair = original.replace('assume(false);', 'assume(false); assert(true);')
            self.assertEqual(safety(original, repair, os.environ["LYNETTE_BIN"], work).status, "safe")

    def test_macro_target_contract_and_executable_code_cannot_change(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            changed_contract = self.original.replace('target() ensures false', 'target() ensures true')
            self.assertEqual(safety(self.original, changed_contract, os.environ["LYNETTE_BIN"], work).status, 'unsafe')
            original = 'use vstd::prelude::*; verus! { fn f() -> u32 { 1 } } fn main() {}'
            self.assertEqual(safety(original, original.replace('{ 1 }', '{ 2 }'), os.environ["LYNETTE_BIN"], work).status, 'unsafe')

    def test_solver_settings_and_new_proof_helpers_remain_allowed(self):
        original = self.original.replace('fn target()', 'pub fn target()')
        candidate = original.replace('pub fn target()', '#[verifier::loop_isolation(false)] pub fn target()')
        candidate += '\n/// A new verified helper\nverus! { proof fn aux() ensures true {} }\n'
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(safety(original, candidate, os.environ["LYNETTE_BIN"], Path(directory)).status, 'safe')

    def test_existing_assumption_cannot_move_past_assignment(self):
        original = '''use vstd::prelude::*; verus! {
fn target(x: i32) -> (r: i32) requires x > 1, x < 10 ensures r > 1 {
    let mut y = x; assume(y > 1); y = y - 1; y
} } fn main() {}'''
        candidate = original.replace('assume(y > 1); y = y - 1;', 'y = y - 1; assume(y > 1);')
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            self.assertEqual(verify(original, os.environ['VERUS_BIN'], work).status, 'verification_failed')
            self.assertEqual(verify(candidate, os.environ['VERUS_BIN'], work).status, 'verified')
            self.assertIsNone(trust_change(original, candidate))
            self.assertEqual(safety(original, candidate, os.environ['LYNETTE_BIN'], work).status, 'unsafe')

    def test_existing_proof_assumption_cannot_become_unconditional(self):
        original = '''use vstd::prelude::*; verus! {
proof fn helper() ensures false { if false { assume(false); } }
fn target() ensures false { }
} fn main() {}'''
        candidate = original.replace('if false { assume(false); }', 'assume(false);').replace(
            'fn target() ensures false { }', 'fn target() ensures false { proof { helper(); } }')
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            self.assertEqual(verify(original, os.environ['VERUS_BIN'], work).status, 'verification_failed')
            self.assertEqual(verify(candidate, os.environ['VERUS_BIN'], work).status, 'verified')
            self.assertIsNone(trust_change(original, candidate))
            self.assertEqual(safety(original, candidate, os.environ['LYNETTE_BIN'], work).status, 'unsafe')

    def test_erased_branch_cannot_hide_executable_condition_effect(self):
        original = 'use vstd::prelude::*; verus! { fn target(v: &mut Vec<u32>) ensures true { } } fn main() {}'
        candidate = original.replace('ensures true { }', 'ensures true { if { v.push(0); true } { assert(true); } }')
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            self.assertEqual(verify(original, os.environ['VERUS_BIN'], work).status, 'verified')
            self.assertEqual(verify(candidate, os.environ['VERUS_BIN'], work).status, 'verified')
            self.assertEqual(safety(original, candidate, os.environ['LYNETTE_BIN'], work).status, 'unsafe')
