#!/bin/bash
# Create new feature branch + specs directory
set -e
FEATURE_NAME=${1:?"Usage: ./create-new-feature.sh <feature-name>"}
SPECS_DIR=".agents/specs/$FEATURE_NAME"
mkdir -p "$SPECS_DIR"
echo "✅ Created specs directory: $SPECS_DIR"
echo "📋 Next: Run /02-speckit.specify to create spec.md"
