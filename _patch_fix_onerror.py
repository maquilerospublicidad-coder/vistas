#!/usr/bin/env python3
"""Fix unescaped single quotes in onerror handler"""
FILE = '/workspaces/vistas/mockup.html'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

OLD = """onerror="this.style.display='none'">"""
NEW = """onerror="this.style.display=\\'none\\'">"""

count = content.count(OLD)
if count:
    content = content.replace(OLD, NEW)
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Fixed {count} occurrence(s)")
else:
    print("ERROR: pattern not found")
