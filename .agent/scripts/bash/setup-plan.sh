#!/bin/bash
# Locate feature spec for planning
set -e
FEATURE_NAME=${1:?"Usage: ./setup-plan.sh <feature-name>"}
SPEC_FILE=".agent/specs/$FEATURE_NAME/spec.md"
if [ ! -f "$SPEC_FILE" ]; then
  echo "❌ spec.md not found at $SPEC_FILE"
  echo "💡 Run /02-speckit.specify first"
  exit 1
fi
echo "✅ Found spec: $SPEC_FILE"
echo "📋 Next: Run /04-speckit.plan"
