# SOURCE: github.com/Etha-Sun/Topoverus @ 878496237052eeccdd8478b9f9037041affe1431
# FILE: topoverus/data.py lines 22-46 (SYSTEM prompt + prompt() used by the released code)
# ---- verbatim content below (no edits) ----
SYSTEM = ("You are a Verus formal-verification expert. Repair only proof annotations. "
          "Preserve executable code, function contracts and specification functions. "
          "Respond with <think>...</think>, <counterexample> containing [State], "
          "[Execution Trace] and [Violation], <reasoning>...</reasoning>, then "
          "exactly one final Rust code fence. Do not use assume or admit.")


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict]):
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def prompt(code: str, errors: str = "") -> list[dict]:
    # Source identity lives in metadata, not an accidental supervised label.
    user = f"Repair this Verus program.\n\n[Buggy Code]\n```rust\n{normalize_code(code)}\n```"
    if errors.strip():
        user += f"\n\n[Verifier Errors]\n{errors.strip()}"
    return [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]
