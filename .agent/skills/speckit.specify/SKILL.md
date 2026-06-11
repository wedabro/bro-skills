---
name: speckit.specify
description: Feature Definer - Generates spec.md from natural language description.
role: Domain Scribe
---

## 🎯 Mission
Pass natural language description → standardized spec.md (WHAT, not HOW).

## 📥 Input
- Feature description from developer (free text)
- `.agent/memory/constitution.md` (constraints)

## 📋 Protocol
1. Read description → extract:
   - **Actors**: Who interacts? (User, Admin, System, Guest)
   - **Actions**: Do what? (CRUD, search, filter, export)
   - **Data**: What data? (entities, fields, relationships)
   - **Constraints**: What limits? (auth, permissions, limits)
2. Create `.agent/specs/[feature]/spec.md` with REQUIRED format:
   ```markdown
   ---
   title: [Feature Name]
   status: DRAFT
   version: 1.0.0
   created: [date]
   ---
   ## 1. Overview
   [1-2 sentence description]

   ## 2. User Scenarios
   - **US1**: As a [actor], I want to [action], so that [value].
   - **US2**: ...

   ## 3. Functional Requirements
   - FR01: [specific, measurable requirement]

   ## 4. Non-Functional Requirements
   - NFR01: Response time < 2s

   ## 5. Success Criteria
   - [ ] SC01: [testable criterion]
   ```
3. Each User Scenario MUST have: Actor + Action + Value.
4. Each Functional Requirement MUST be measurable (have specific data).

## 📤 Output
- File: `.agent/specs/[feature]/spec.md`

## 🚫 Guard Rails
- DO NOT write implementation details (HOW) — just describe WHAT.
- DO NOT use technical jargon in User Scenarios (business language).
- DO NOT ignore error cases — each action must have a "what if it fails?"
