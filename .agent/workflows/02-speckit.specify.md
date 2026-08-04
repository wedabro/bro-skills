---
description: Create Feature Specification (spec.md)
---

# 📝 Feature Specification

## Pre-conditions
- `.agent/memory/constitution.md` exists
- **Brainstorm & Align session is completed and confirmed by the User**

## Steps

1. Brainstorm with the User to clarify requirements, propose solutions, and get final alignment
2. Developers describe features in natural language (or output of brainstorm is used)
3. **@speckit.specify** — Parse description → create standardized spec.md
4. Review output: spec.md must have Overview, User Scenarios, Requirements, Success Criteria

## Success Criteria
- ✅ spec.md has ≥1 User Scenario
- ✅ Each scenario has Actor + Action + Value
- ✅ Success Criteria is testable
