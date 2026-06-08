#!/usr/bin/env python3
import sys
import re
import os
import subprocess

def bump_version(new_version):
    print(f"🔄 Bắt đầu nâng version lên: {new_version}...")
    
    # 1. Update package.json
    pkg_path = "package.json"
    if os.path.exists(pkg_path):
        with open(pkg_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(r'"version":\s*"[^"]+"', f'"version": "{new_version}"', content)
        with open(pkg_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("  ✅ Đã cập nhật package.json")

    # 2. Update pyproject.toml
    pyproj_path = "pyproject.toml"
    if os.path.exists(pyproj_path):
        with open(pyproj_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(r'version\s*=\s*"[^"]+"', f'version = "{new_version}"', content)
        with open(pyproj_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("  ✅ Đã cập nhật pyproject.toml")

    # 3. Update bro_skills/__init__.py
    init_path = os.path.join("bro_skills", "__init__.py")
    if os.path.exists(init_path):
        with open(init_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(r'__version__\s*=\s*"[^"]+"', f'__version__ = "{new_version}"', content)
        with open(init_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("  ✅ Đã cập nhật bro_skills/__init__.py")

    # 4. Update bro_skills/generator.py
    gen_path = os.path.join("bro_skills", "generator.py")
    if os.path.exists(gen_path):
        with open(gen_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(r'"bro_skills_version":\s*"[^"]+"', f'"bro_skills_version": "{new_version}"', content)
        with open(gen_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("  ✅ Đã cập nhật bro_skills/generator.py")

    print("\n🎉 Đã cập nhật thành công tất cả các file cấu hình!")
    print("\n💡 Gợi ý lệnh Git tiếp theo:")
    print(f"  git add .")
    print(f'  git commit -m "chore(release): bump version to {new_version}"')
    print(f"  git push origin main")
    print(f"  git tag v{new_version}")
    print(f"  git push origin v{new_version}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Lỗi: Vui lòng cung cấp số version mới.")
        print("Sử dụng: python .agent/scripts/bump_version.py <new_version>")
        sys.exit(1)
        
    version_arg = sys.argv[1]
    # Simple regex to check version format x.y.z
    if not re.match(r'^\d+\.\d+\.\d+$', version_arg):
        print(f"❌ Lỗi: Định dạng version '{version_arg}' không hợp lệ. Phải là dạng x.y.z (ví dụ: 1.3.2)")
        sys.exit(1)
        
    bump_version(version_arg)
