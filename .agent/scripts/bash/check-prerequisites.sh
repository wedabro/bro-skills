#!/bin/bash
# Verify prerequisite artifacts exist
set -e
FEATURE_NAME=${1:?"Usage: ./check-prerequisites.sh <feature-name>"}
SPECS_DIR=".agent/specs/$FEATURE_NAME"
ERRORS=0
for f in spec.md plan.md tasks.md; do
  if [ ! -f "$SPECS_DIR/$f" ]; then
    echo "❌ Missing: $SPECS_DIR/$f"
    ERRORS=$((ERRORS + 1))
  else
    echo "✅ Found: $SPECS_DIR/$f"
  fi
done
if [ $ERRORS -gt 0 ]; then
  echo "⚠️  $ERRORS prerequisite(s) missing"
  exit 1
fi
echo "✅ All prerequisites met"
