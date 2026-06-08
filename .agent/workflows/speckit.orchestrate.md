---
description: Multi-Agent Orchestration - Chọn và điều phối agent theo project_type + attributes
---

# 🧭 Multi-Agent Orchestration

## Pre-conditions
- `.agent/project.json` tồn tại (có `project_type` + `attributes`)
- `.agent/agents/registry.json` tồn tại
- `.agent/memory/constitution.md` tồn tại

## Steps

1. **@orchestrator** — Resolve agent set:
   - Đọc `project.json.project_type` + `attributes`
   - `active = core + base[type] + modifiers[architecture|platforms|flags]`
   - Log danh sách agent được kích hoạt (loại trùng)

2. Chạy pipeline với agent đã chọn:
   - Specify → Clarify → Plan → Tasks → Implement → Verify
   - Mỗi task gắn tag `@agent:<name>` để route

3. **Routing**: Orchestrator giao task cho domain agent theo tag.
   - VD project_type=`game` → task gameplay route tới `@speckit.gamedev`
   - VD `platforms:[ios]` → task mobile route tới `@speckit.ios`

4. **Conflict resolution**: Constitution > Orchestrator > Domain Agent.

## Success Criteria
- ✅ Đúng tập agent kích hoạt theo project_type + attributes
- ✅ Mỗi task có owner agent rõ ràng
- ✅ Không vi phạm Constitution
