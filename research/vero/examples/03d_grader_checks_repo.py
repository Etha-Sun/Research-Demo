# SOURCE: github.com/sunblaze-ucb/vero @ 0a7325df9e9e6dbc275c0ad483b3d1cbe38d9b09
#   src/vero/evaluation/hygiene.py lines 20-27 and src/vero/evaluation/axioms.py line 31 (verbatim).

# --- hygiene.py 20-27 ---
_UNSAFE_PATTERN = re.compile(r"\bunsafe\b")
# ``implemented_by`` attribute in either form:
#   ``@[implemented_by foo]`` / ``@[inline, implemented_by foo]`` (prefix attribute), or
#   ``attribute [implemented_by foo] bar`` (standalone attribute command).
# The whole-word ``implemented_by`` token only ever appears as this attribute, so
# matching it (outside comments) is sufficient and evasion-resistant.
_IMPLEMENTED_BY_PATTERN = re.compile(r"\bimplemented_by\b")
_BLOCK_COMMENT = re.compile(r"/-.*?-/", re.DOTALL)

# --- axioms.py 31 ---
_STANDARD = frozenset({"Classical.choice", "propext", "Quot.sound"})

# --- grade.py 11-23 (SpecStatus) ---

SpecStatus = Literal[
    "passed",  # exactly the expected fillings, clean axioms, compiles
    "unfilled",  # no slot was filled
    "overfilled",  # more slots filled than the mode allows (ambiguous intent)
    "sorry_leaked",  # a filled slot still depends on sorryAx
    "axiom_leaked",  # non-standard user axiom used
    "slot_body_tainted",  # filled slot syntactically contains axiom/admit tokens
    "build_error",  # file didn't compile / axiom check reports missing
    "unpaired_sat",  # sat_<S> filled but no verified joint_unsat claim names S
    "unsafe_keyword",  # agent-editable file contains `unsafe` — whole run voided
    "impl_oracle",  # agent impl uses `@[implemented_by]` (spec-oracle hack) — whole run voided
]
