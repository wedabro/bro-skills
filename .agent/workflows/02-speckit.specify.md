---
description: Create Feature Specification (spec.md)
---

# 📝 Feature Specification

## Pre-conditions
- `.agent/memory/constitution.md` exists

## Steps

1. Developers describe features in natural language
2. **@speckit.specify** — Parse description → create standardized spec.md
3. Review output: spec.md must have Overview, User Scenarios, Requirements, Success Criteria

## Success Criteria
- ✅ spec.md has ≥1 User Scenario
- ✅ Each scenario has Actor + Action + Value
- ✅ Success Criteria is testable
