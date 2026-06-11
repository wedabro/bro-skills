---
name: speckit.analyze
description: Consistency Checker - Analyze consistency between spec, plan, tasks.
role: Consistency Analyst
---

## 🎯 Mission
Make sure spec.md, plan.md, tasks.md do not conflict and cover all requirements.

## 📥 Input
- `.agent/specs/[feature]/spec.md`
- `.agent/specs/[feature]/plan.md`
- `.agent/specs/[feature]/tasks.md`

## 📋 Protocol
1. **Coverage Check**: Each User Scenario in the spec → must have task(s) in tasks.md.
2. **Conflict Check**: Plan says to use tech A but tasks reference tech B → ERROR REPORT.
3. **Constitution Check**: Compare plan.md with constitution.md → detect violations.
4. **Completeness Check**: Each data model in the plan → must have a model creation + migration task.
5. **Gap Analysis table output**:
   ```
   | Spec Requirement | Plan Section | Task ID | Status |
   |------------------|-------------|---------|--------|
   | User login       | Auth flow   | T005    | ✅ OK  |
   | Payment          | -           | -       | ❌ GAP |
   ```
6. Calculate Coverage Score: `(matched / total) × 100%` .

## 📤 Output
- Console: Gap Analysis table + Coverage Score
- File: `.agent/memory/analyze-report.md`

## 🚫 Guard Rails
- Reporting ONLY — DO NOT arbitrarily edit artifacts.
- Each gap must clearly indicate which artifact is missing.
