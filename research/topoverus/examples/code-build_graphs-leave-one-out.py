# SOURCE: github.com/Etha-Sun/Topoverus @ 878496237052eeccdd8478b9f9037041affe1431
# FILE: topoverus/build_graphs.py lines 48-84 (dependency-edge construction used by the released code)
# ---- verbatim content below (no edits) ----
def build(task: dict, binary: str, lynette: str, work_dir: Path) -> dict:
    code = task["verified_code"]
    invariants = first_invariants(code)
    record = {"source_id": task["source_id"], "source_sha256": task["source_sha256"],
              "reference_sha256": digest(code), "builder_version": "inductive-v2.0",
              "invariants": invariants, "dependency_edges": [], "checks": [], "status": "valid"}
    if not invariants or len(invariants) > 10:
        record["status"] = "no_invariants" if not invariants else "unsupported_size"
        return record
    safe = safety(task["unverified_code"], code, lynette, work_dir)
    record["reference_safety"] = safe.to_dict()
    if safe.status != "safe":
        record["status"] = "reference_unsafe" if safe.status == "unsafe" else "reference_safety_unknown"
        return record
    baseline = verify(code, binary, work_dir, multiple_errors=100)
    record["baseline"] = baseline.to_dict()
    if baseline.status != "verified":
        record["status"] = "baseline_failed"
        return record
    if len(invariants) == 1:
        return record
    for removed in range(len(invariants)):
        try:
            candidate, ranges = replace_first_block(code, removed)
            checked = verify(candidate, binary, work_dir, multiple_errors=100)
            if checked.status not in ("verified", "verification_failed"):
                raise ValueError(f"Removal tool result: {checked.status}")
            failures = failed_invariants(checked.stderr, ranges)
            record["checks"].append({"removed": removed, "target_failures": failures,
                                      "verification": checked.to_dict()})
            record["dependency_edges"].extend([[removed, target] for target in failures])
        except ValueError as exc:
            record.update(status="inconclusive", failure=str(exc))
            # A partial graph is not evidence of absence of missing edges.
            record["dependency_edges"] = None
            break
    return record
