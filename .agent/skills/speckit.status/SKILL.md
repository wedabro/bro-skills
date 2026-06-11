---
name: speckit.status
description: Progress Dashboard - Displays project progress status.
role: Progress Tracker
---

## 🎯 Mission
Parse tasks.md → calculate progress → display visual dashboard.

## 📥 Input
- `.agent/specs/[feature]/tasks.md`

## 📋 Protocol
1. Parse tasks.md → count checkboxes:
   - `- [X]` = completed
   - `- [ ]` = pending
2. Group by Phase → calculate % for each phase.
3. Output dashboard:
   ```
   📊 Progress Dashboard: [Feature Name]
   ═══════════════════════════════════════
   Phase 1: Setup        ████████████████ 100% (4/4)
   Phase 2: Foundation   ████████░░░░░░░░  50% (3/6)
   Phase 3: User Auth    ░░░░░░░░░░░░░░░░   0% (0/5)
   ───────────────────────────────────────
   Total:                ███████░░░░░░░░░  47% (7/15)
   ```
4. List of pending tasks (next to do).

## 📤 Output
- Console: Dashboard visualization

## 🚫 Guard Rails
- DO NOT change tasks.md — read and report only.
