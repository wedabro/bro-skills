---
name: speckit.clarify
description: Ambiguity Resolver - Detect and resolve ambiguity in spec.
---

## 🎯 Mission
Scan spec.md → detect ambiguity → ask developer up to 3 questions → update spec.

## 📥 Input
- `.agents/specs/[feature]/spec.md`

## 📋 Protocol
1. Scan spec.md to find:
   - **Vague language**: "fast", "many", "easy to use", "similar", "etc."
   - **Missing boundaries**: Unknown min/max, pagination limits, file size limits
   - **Undefined error handling**: What happens when X fails?
   - **Ambiguous actors**: Who is "User"? Admin? Guest? Registered?
2. Categorize each issue:
   - 🔴 **CRITICAL**: Architectural influence, MUST ask developer
   - 🟡 **IMPORTANT**: Should ask but can suggest default
   - 🟢 **MINOR**: Editorial correction that cannot change behavior, such as a
     typo, broken reference, or inconsistent requirement ID.
3. Ask the developer MAXIMUM 3 CRITICAL questions, each question has an options table:
   ```
| Option | Describe | Impact |
   |--------|-------|--------|
   | A      | ...   | ...    |
   | B      | ...   | ...    |
   | C      | ...   | ...    |
   ```
4. Auto-fix only behavior-neutral 🟢 MINOR items. Present missing limits,
   permissions, defaults, and error behavior as assumptions or questions; do
   not write them into the spec without approval.
5. Update spec.md with clarifications → mark `[CLARIFIED]` .

## 📤 Output
- File: Updated `.agents/specs/[feature]/spec.md`

## 🚫 Guard Rails
- MAXIMUM 3 questions — don't ask too many.
- DO NOT change the original intent of the spec.
- DO NOT invent product limits, permissions, defaults, or acceptance criteria.
