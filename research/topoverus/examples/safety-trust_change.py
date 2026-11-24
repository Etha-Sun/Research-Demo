# SOURCE: github.com/Etha-Sun/Topoverus @ 878496237052eeccdd8478b9f9037041affe1431
# FILE: topoverus/trust.py lines 185-221
# ---- verbatim content below (no edits) ----
def trusted_constructs(code: str) -> Counter:
    tokens, result = rust_tokens(code), Counter()
    for i, token in enumerate(tokens):
        if token in ("assume", "admit") and i + 1 < len(tokens) and tokens[i + 1] == "(":
            depth, end = 0, i + 1
            while end < len(tokens):
                depth += (tokens[end] == "(") - (tokens[end] == ")")
                end += 1
                if depth == 0:
                    break
            if depth:
                raise ValueError("Unclosed trusted call")
            result[tuple(tokens[i:end])] += 1
        elif token == "assume_specification":
            # This construct changes the trusted API; release inputs do not use it.
            raise ValueError("assume_specification is unsupported by strict safety")
        elif token == "axiom" and tokens[i + 1:i + 2] == ["fn"]:
            result[("axiom", "fn")] += 1
        elif token == "proof" and tokens[i:i + 5] == ["proof", "(", "axiom", ")", "fn"]:
            result[("proof", "(", "axiom", ")", "fn")] += 1
        elif token == "#" and tokens[i + 1:i + 2] == ["["]:
            end = i + 2
            while end < len(tokens) and tokens[end] != "]":
                end += 1
            attribute = tokens[i:end + 1]
            if "verifier" in attribute and ("external_body" in attribute or "external" in attribute
                    or ("verify" in attribute and "false" in attribute)):
                result[tuple(attribute)] += 1
    return result


def trust_change(original: str, candidate: str) -> str | None:
    try:
        additions = trusted_constructs(candidate) - trusted_constructs(original)
    except ValueError as exc:
        return str(exc)
    return "New or modified trusted assumption/verification bypass" if additions else None
