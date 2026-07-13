---
name: speckit.uat
description: UAT Analyzer - Analyze manual acceptance results and process gaps from the User.
---

## 🎯 Mission
Bridging the actual user experience and code logic, ensuring features run as customers expect.

## 📋 Protocol

### Phase 1: UAT Intake (Acceptance)
- Collect manual user feedback after each Phase.
- Recorded in `.agent/verification/[phase]-UAT.md` .

### Phase 2: Gap Analysis (Gap Analysis)
- Compare the actual results User reports with the original Spec.md.
- Error classification: UI Bug, Logic Bug, or New Requirement.

### Phase 3: Restoration Plan (Patch plan)
- Automatically generate a Tasks list to patch the "Gaps" just found.
- Forwarding for `speckit.implement` processes as `--gaps-only` .

## 🚫 Guard Rails
- There MUST be a clear distinction between "Bug" and "New Feature Requested".
- It is PROHIBITED to mark Phase completed if the User has not yet Approve the core UAT criteria.
