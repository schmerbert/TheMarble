#!/usr/bin/env bash
# Maintainer sweep — run all executable specimen tests from repo root.
# Usage: ./verify_examples.sh
# Same suites as verify_examples.ps1, for Linux/macOS and CI.

set -u
root="$(cd "$(dirname "$0")" && pwd)"
fail=0

step() {
    name="$1"; shift
    echo ""
    echo "== $name =="
    if "$@"; then
        echo "OK: $name"
    else
        echo "FAIL: $name"
        fail=1
    fi
}

run_in() { d="$1"; shift; (cd "$root/$d" && "$@"); }

step "Fall tests"          run_in EXAMPLEmarbles/fall       python -m unittest discover -s tests -p "test_*.py" -q
step "Lighthouse tests"    run_in EXAMPLEmarbles/lighthouse python -m unittest discover -s tests -p "test_*.py" -q
step "Arrival ref check"   node "$root/Reference/verify_arrival_refs.mjs"
step "Trench gate suite"   run_in EXAMPLEmarbles/trench/tests node run-all.mjs
step "Cabin hostile floor" run_in EXAMPLEmarbles/cabin      python tests/test_hostile.py

echo ""
if [ "$fail" -ne 0 ]; then
    echo "One or more specimen suites failed."
    exit 1
fi
echo "All specimen suites passed."
