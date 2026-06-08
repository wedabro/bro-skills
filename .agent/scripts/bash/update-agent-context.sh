#!/bin/bash
# Update agent context files after changes
set -e
echo "🔄 Updating agent context..."
if [ -f ".agent/memory/constitution.md" ]; then
  echo "✅ Constitution: OK"
else
  echo "⚠️  Constitution missing — run /01-speckit.constitution"
fi
if [ -d ".agent/identity" ]; then
  echo "✅ Identity: OK"
else
  echo "⚠️  Identity missing — run bro-skills init"
fi
echo "✅ Context update complete"
