# SOURCE: github.com/Etha-Sun/Topoverus @ 878496237052eeccdd8478b9f9037041affe1431
# FILE: topoverus/code.py lines 42-60 (how an SFT target trajectory is assembled)
# ---- verbatim content below (no edits) ----
def ctx_target(response: str) -> str:
    """Retain reasoning and exactly one final code block; never invent reasoning."""
    parts = []
    for tag in TAGS:
        matches = list(re.finditer(rf"<{tag}>(.*?)</{tag}>", response, re.DOTALL))
        if len(matches) != 1 or len(matches[0].group(1).strip()) < 10:
            raise ValueError(f"Missing, duplicate or empty {tag} section")
        # Reasoning can contain draft code. Remove it from SFT targets so that
        # every consumer observes the same single final fenced program.
        text = FENCE.sub("", matches[0].group(1)).strip()
        if len(text) < 10:
            raise ValueError(f"Empty {tag} after removing draft code")
        parts.append(f"<{tag}>\n{text}\n</{tag}>")
    counterexample = parts[1]
    if not ("[State]" in counterexample and "[Violation]" in counterexample
            and ("[Execution Trace]" in counterexample or "[Execution]" in counterexample)):
        raise ValueError("Counterexample sections incomplete")
    parts.append(f"```rust\n{final_code(response)}\n```")
    return "\n\n".join(parts)
