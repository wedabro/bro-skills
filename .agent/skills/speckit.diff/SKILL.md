---
name: speckit.diff
description: Artifact Comparator - Compares differences between artifacts.
role: Diff Analyst
---

## 🎯 Mission
Compare 2 versions of artifact → highlight changes → evaluate impact.

## 📥 Input
- 2 files or 2 versions to compare (spec, plan, tasks, code)

## 📋 Protocol
1. Read both versions.
2. Compare section-by-section:
   - ➕ **Added**: New Sections/requirements
   - ➖ **Removed**: Sections/requirements are removed
   - ✏️ **Changed**: Sections have changed content
3. Impact Analysis: What downstream artifact does each change affect?
   - For example: Add fields in spec → need to update plan → need to add tasks
4. Output summary table.

## 📤 Output
- Console: Diff summary table
- File: `.agent/memory/diff-report.md` (if needed to save)

## 🚫 Guard Rails
- Compare and report ONLY — DO NOT arbitrarily edit artifacts.
