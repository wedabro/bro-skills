---
name: speckit.checklist
description: Requirements Validator - Create and validate checklist from spec.
---

## 🎯 Mission
Extract all functional requirements from spec.md into a trackable checklist.

## 📥 Input
- `.agent/specs/[feature]/spec.md`
- `.agent/specs/[feature]/tasks.md` (if available)

## 📋 Protocol
1. Read spec.md → extract all requirements (from User Scenarios + Success Criteria).
2. Create checklist format:
   ```markdown
   ## Functional Requirements
   - [ ] FR01: User can register an account → T003, T004
   - [ ] FR02: User can log in → T005
   - [x] FR03: User can view product → T010 ✅
   ```
3. If there is tasks.md → link each requirement to task IDs.
4. Enter status: ✅ Met / ❌ Not Met / ⚠️ Partial.

## 📤 Output
- File: `.agent/specs/[feature]/checklist.md`

## 🚫 Guard Rails
- Each requirement MUST be quoted from spec.md (not made up).
