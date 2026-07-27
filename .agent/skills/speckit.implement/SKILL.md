---
name: speckit.implement
description: Code Builder (Anti-Regression) - Deploy code in tasks with IRONCLAD protocols.
---

## 🎯 Mission
Implement code according to tasks.md, complying with IRONCLAD Protocols and **Deviation Rules** to operate automatically when encountering errors.

## 📋 Protocol

### IRONCLAD Protocols:
1. **Blast Radius**: Analyzes risk based on the number of affected files.
2. **Strategy**: Choose direct editing or Strangler Pattern.
3. **TDD**: Create repro script fail -> code -> pass.
4. **Context Anchoring**: Re-read constitution every 3 tasks.
5. **Verification Gate**: Run the smallest applicable configured check after
   each task (targeted test/type/lint), then run the full project build at the
   phase boundary. Use Docker only when required by project configuration.

### Deviation Rules (Self-handling when deviating) ⭐
- **Bug detected**: Automatically fix if within scope, or create new task if serious.
- **Missing Critical**: If important config/file is missing, automatically add it immediately.
- **Blocker**: If stuck, perform "Root Cause Analysis" yourself before asking the user.
- **Arch Change**: If you need to change the architecture, you MUST ask the user.

### Self-Check Protocol
- A task is complete only when its applicable targeted checks pass. The phase
  is complete only when the configured full build/test gate passes.

## 🚫 Guard Rails
- DO NOT commit build error code.
- NO hard-code sensitive info.
