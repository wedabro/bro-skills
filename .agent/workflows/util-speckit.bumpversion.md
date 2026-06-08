---
description: Tự động cập nhật version ở tất cả các file cấu hình và tạo git tag.
---

# Workflow: /bumpversion

Quy trình tự động nâng version và tạo tag cho dự án.

## Steps

1. **Nhận đầu vào**: Xác định số version mới cần cập nhật (dạng `x.y.z`).
2. **Chạy Script**: Thực hiện chạy script python để đồng bộ:
   ```bash
   python .agent/scripts/bump_version.py <version>
   ```
3. **Commit & Tag**:
   - `git add .`
   - `git commit -m "chore(release): bump version to <version>"`
   - `git push origin main`
   - `git tag v<version>`
   - `git push origin v<version>`
