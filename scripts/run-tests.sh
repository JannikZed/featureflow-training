#!/usr/bin/env bash
# Fallback when make is unavailable. Usage: ./scripts/run-tests.sh [unit|integration|e2e|all]
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PYTEST="${ROOT}/.venv/bin/pytest"
case "${1:-all}" in
  unit) "$PYTEST" -m unit -q ;;
  integration) "$PYTEST" -m integration -q ;;
  e2e) "$PYTEST" -m e2e -q ;;
  all) "$PYTEST" -q ;;
  *) echo "usage: $0 [unit|integration|e2e|all]"; exit 2 ;;
esac
