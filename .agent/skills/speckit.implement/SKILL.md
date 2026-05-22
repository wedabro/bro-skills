---
name: speckit.implement
description: Code Builder (Anti-Regression) - Triển khai code theo tasks với IRONCLAD protocols.
role: Master Builder
---

## 🎯 Mission
Implement code theo tasks.md, tuân thủ 5 IRONCLAD Protocols, zero regression.

## 📥 Input
- `.agent/specs/[feature]/tasks.md` (danh sách tasks)
- `.agent/specs/[feature]/plan.md` (kiến trúc)
- `.agent/memory/constitution.md` (rules)

## 📋 Protocol — Cho MỖI task chưa complete:

### Protocol 1: Blast Radius Analysis
- List TẤT CẢ files bị ảnh hưởng bởi task.
- Rate: 🟢 LOW (1-2 files) / 🟡 MED (3 files) / 🔴 HIGH (>3 files)
- Nếu HIGH → BÁO developer trước khi code.

### Protocol 2: Strategy Selection
- 🟢 LOW risk → Sửa trực tiếp (inline edit)
- 🔴 HIGH risk → **Strangler Pattern**: Tạo file mới → migrate → xóa file cũ

### Protocol 3: TDD (Reproduction First)
- Tạo script `repro_task_[ID].sh` chứng minh bug/feature TRƯỚC khi code.
- Chạy → phải FAIL → Implement fix → Chạy lại → phải PASS.

### Protocol 4: Context Anchoring
- Mỗi 3 tasks → re-read `constitution.md` + project structure.
- Đảm bảo không drift khỏi architecture.

### Protocol 5: Post-Implementation Build Gate ⭐
**SAU MỖI TASK**, chạy kiểm tra compile:
1. **TypeScript Check**:
   ```bash
   docker compose exec <service> npx tsc --noEmit
   # Hoặc:
   docker compose build 2>&1 | tail -n 50
   ```
2. **Interface Contract Check**:
   - Nếu task THÊM/SỬA props vào component → grep TẤT CẢ nơi gọi component đó.
   - Nếu task THÊM/SỬA type interface → grep TẤT CẢ nơi dùng type đó.
   ```bash
   grep -rn "ComponentName" apps/*/src/ --include="*.tsx"
   ```
3. **Dockerfile Path Check** (nếu task liên quan):
   - Nếu task tạo/xóa/di chuyển file → verify Dockerfile COPY paths vẫn hợp lệ.
   - Nếu task đổi `output` config (standalone, etc.) → verify runner CMD path.

Nếu build gate FAIL → fix ngay TRƯỚC KHI chuyển task tiếp theo.

### Protocol 6: Deviation Rules (Xử lý sai lệch)
NẾU phát hiện lỗi phát sinh ngoài plan trong quá trình code, tự động xử lý:
- **Rule 1 (Auto-fix bugs):** Tự sửa lỗi logic, cú pháp do task gây ra.
- **Rule 2 (Auto-add missing):** Tự thêm error handling, validation nếu bị thiếu.
- **Rule 3 (Auto-fix blockers):** Tự cài thư viện thiếu, sửa lỗi import.
- **Rule 4 (Ask human):** DỪNG và hỏi user nếu thay đổi Kiến trúc (thêm/đổi DB, Framework, core architecture).

### Completion (Self-Check Protocol)
- Bắt buộc chạy kiểm tra file đã tồn tại và lệnh `Verify` pass 100%.
- Đánh `- [X] T001 ...` trong tasks.md khi task pass **VÀ build gate pass**.
- Commit message format: `feat(T001): [description]`

## 📤 Output
- Code files (theo plan.md paths)
- Updated `tasks.md` (checkboxes)

## 🚫 Guard Rails
- KHÔNG import thư viện không có trong `package.json` / `pyproject.toml`.
- KHÔNG sửa quá 3 files trong 1 task mà không hỏi.
- KHÔNG bỏ qua TDD step — phải có repro script.
- KHÔNG hard-code URLs, tokens, keys, default text.
- KHÔNG tick task [X] nếu chưa qua build gate. ⭐
