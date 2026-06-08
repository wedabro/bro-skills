# bro-skills

Dự án: bro-skills

## 1. PHÁP LỆNH TỐI CAO
- Tuân thủ nghiêm ngặt file `.agent/memory/constitution.md`.
- Docker-First: Mọi hoạt động code và chạy app phải diễn ra trong container. KHÔNG chạy node/python trên host.
- Ports: Sử dụng dải port 8900-8999. Tuân thủ lấy port từ biến môi trường (.env).

## 2. bro-skills PROTOCOL
- Mọi task phải đi qua quy trình: Specify → Plan → Tasks → Implement.
- Sử dụng Workflows trong `.agent/workflows/` và Skills trong `.agent/skills/`.

## 3. NGÔN NGỮ & CODE
- Phản hồi developer hoàn toàn bằng Tiếng Việt.
- 15-Minute Rule: Mỗi task phải atomic, ≤ 15 phút, ảnh hưởng ≤ 3 files.
- PowerShell 5.1+, ngăn cách lệnh bằng dấu `;` (KHÔNG dùng `&&`).
- KHÔNG hard-code URLs, Tokens, Keys. Dùng ENV vars (`.env`).

## 4. AN TOÀN
- KHÔNG chạy `docker compose down -v` trên Production.
- Tạo script tự động (`.agent/scripts/`) cho lỗi lặp lại.
- Kiểm tra logs ngay khi lỗi: `docker compose logs -f <service>`.
- **Auto-Commit**: PHẢI thực hiện git commit & push ngay lập tức sau khi hoàn thành bất kỳ chức năng hoặc task nào theo chuẩn Conventional Commits.

## 5. AGENTIC MODE SYNC (Antigravity Only)
- **Task Tracking**: Sử dụng `task_boundary` để đồng bộ trạng thái với `@speckit.tasks` (tasks.md).
- **Planning Artifacts**: Luôn tạo `implementation_plan.md` khi thực hiện các thay đổi lớn (atomic > 3 files).
- **Verification**: Sau khi hoàn thành task, sử dụng `walkthrough.md` để đối chiếu kết quả với `spec.md`.


## Project Structure
- `.agent/memory/constitution.md` — Project Constitution (Source of Law)
- `.agent/identity/master-identity.md` — AI Persona & Soul
- `.agent/knowledge_base/` — Domain knowledge (infrastructure, data, API)
- `.agent/skills/` — AI skills (@mentions)
- `.agent/workflows/` — Automation workflows (/commands)
- `.agent/specs/` — Feature specifications
