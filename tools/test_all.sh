#!/bin/sh
# Run every suite. Exit non-zero if any fails.
cd "$(dirname "$0")/.." || exit 2
s=0
run() { printf '%s: ' "$1"; shift; if out=$("$@" 2>&1); then echo "$out" | tail -1; else echo "$out" | tail -3; s=1; fi; }
run calculators python3 -I principles/calculators/tests/test_calculators.py
run limits python3 -I safety/tests/test_limits.py
run schema python3 -I tools/log-schema/test_schema.py
run link-parsers python3 -I platforms/link-g4plus/parser/tests/test_parsers.py
run msq-adapter python3 -I platforms/tunerstudio-msq/parser/tests/test_msq.py
run tune-diff python3 -I tools/tune-diff/tests/test_diff.py
run haltech-adapter python3 -I platforms/haltech/parser/tests/test_adapter.py
run runcards python3 -I tools/runcards/test_runcards.py
run mcp-conformance python3 -I tools/mcp-mock/conformance.py
run d1-replay python3 -I tools/mcp-mock/d1_replay.py
run evals-d0 python3 -I evals/run_evals.py
run d2-dev python3 -I tools/sim/run_d2.py --seeds dev
run d2-holdout python3 -I tools/sim/run_d2.py --seeds holdout
run kb-lint python3 -I tools/kb-lint/lint.py
run verbatim python3 -I tools/verbatim-check/check.py
run verbatim-selftest python3 -I tools/verbatim-check/check.py --selftest
exit $s
