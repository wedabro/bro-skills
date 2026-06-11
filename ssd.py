#!/usr/bin/env python3
"""
⚡ bro-skills - Spec-Driven Development CLI (ASF 3.3)

Backward compatibility wrapper.
If pip installed, use the `bro-skills` command directly.
"""
import sys
import os

# Make sure the bro_skills package can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from bro_skills.cli import main
except ImportError:
    # Fallback if someone still uses the old name
    from antigravity_ssd.cli import main

if __name__ == "__main__":
    main()
