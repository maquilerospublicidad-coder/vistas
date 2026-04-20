#!/usr/bin/env python3
"""Fix: Escaped quotes in boxShadow inline handlers"""
FILE = '/workspaces/vistas/mockup.html'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

old = """return '<div style="display:flex;align-items:center;gap:10px;padding:10px 12px;background:#fff;border:1px solid #e2e8f0;border-radius:10px;transition:box-shadow 0.15s;" onmouseover="this.style.boxShadow='0 2px 8px rgba(0,0,0,0.08)'" onmouseout="this.style.boxShadow='none'">'+"""

new = """return '<div style="display:flex;align-items:center;gap:10px;padding:10px 12px;background:#fff;border:1px solid #e2e8f0;border-radius:10px;transition:box-shadow 0.15s;" onmouseover="this.style.boxShadow=\\\'0 2px 8px rgba(0,0,0,0.08)\\\'" onmouseout="this.style.boxShadow=\\\'none\\\'">'+"""

if old in content:
    content = content.replace(old, new, 1)
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed: escaped quotes in boxShadow handlers")
else:
    print("ERROR: pattern not found")
