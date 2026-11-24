#!/usr/bin/env bash
# usage: verify/run.sh /path/to/verus   — runs Verus on every episode example .rs file and prints the verdicts.
set -u; V=${1:?path to verus}; cd "$(dirname "$0")/.."
for f in episodes/*/examples/*.rs; do
  printf '\n== %s\n' "$f"
  timeout 300 "$V" "$f" 2>&1 | grep -E 'verification results|error(\[|:)|not satisfied|verified' | head -8
done
