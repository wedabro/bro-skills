#!/usr/bin/env python3
"""
⚡ bro-skills - Spec-Driven Development CLI (ASF 3.3)

Backward compatibility wrapper.
Nếu đã pip install, dùng lệnh `bro-skills` trực tiếp.
"""
import sys
import os

# Đảm bảo package bro_skills có thể import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from bro_skills.cli import main
except ImportError:
    # Fallback nếu ai đó vẫn dùng tên cũ
    from antigravity_ssd.cli import main

if __name__ == "__main__":
    main()
