---
description: Tạo/cập nhật Master Identity cho AI Agent
---

# 🆔 Identity Setup

## Pre-conditions
- `.agent/project.json` tồn tại (chạy `bro-skills init` trước)
- `.agent/memory/constitution.md` tồn tại (khuyến nghị)

## Steps

1. **@speckit.identity** — Thu thập thông tin:
   - Đọc `project.json` → project type, name
   - Đọc `constitution.md` → tech stack, principles
   - Scan codebase → patterns, conventions hiện có
2. Tạo/cập nhật `.agent/identity/master-identity.md`:
   - Persona + Core Capabilities
   - Soul (Core Beliefs): "bro-skills First", "Docker is the Law"
   - Project Context (auto-detected)
3. Nếu `web_public`/`fullstack` → thêm SEO & GEO Awareness section

## Success Criteria
- ✅ `master-identity.md` tồn tại
- ✅ Persona gắn chặt domain dự án (không chung chung)
- ✅ Core Beliefs bao gồm mandatory items
