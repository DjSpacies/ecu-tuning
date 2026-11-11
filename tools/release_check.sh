#!/bin/sh
# Run before every push. Fails if the commit would carry private material or the tests fail.
set -u
cd "$(dirname "$0")/.."
fail=0
git rev-parse --git-dir >/dev/null 2>&1 || { echo "not a git repository"; exit 1; }
files=$(git ls-files --cached --others --exclude-standard)
bad=$(echo "$files" | grep -E '^(collateral|inbox)/' | grep -vE '^(collateral|inbox)/README\.md$')
[ -n "$bad" ] && { echo "PRIVATE PATHS STAGED:"; echo "$bad"; fail=1; }
bin=$(echo "$files" | grep -iE '\.(pclr|llg|msq|hal|mlg|mp4|m4a|pdf|exe)$')
[ -n "$bin" ] && { echo "TUNE/LOG/MEDIA/BINARY FILES STAGED:"; echo "$bin"; fail=1; }
big=$(echo "$files" | while read -r f; do [ -f "$f" ] && [ "$(wc -c <"$f")" -gt 1000000 ] && echo "$f"; done)
[ -n "$big" ] && { echo "FILES OVER 1 MB:"; echo "$big"; fail=1; }
sh tools/test_all.sh >/tmp/release_check_tests.txt 2>&1 || { echo "TESTS FAILED (see /tmp/release_check_tests.txt)"; fail=1; }
[ $fail -eq 0 ] && echo "release check: OK ($(echo "$files" | wc -l) files)"
exit $fail
