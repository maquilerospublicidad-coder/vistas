#!/usr/bin/env python3
"""Fix unescaped quotes in Almacén Físico inline handlers"""
FILE = '/workspaces/vistas/mockup.html'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# Fix onmouseover="this.style.borderColor='#ff9900'" -> escaped
OLD = """onmouseover="this.style.borderColor='#ff9900'" onmouseout="this.style.borderColor='#e5e7eb'" """
NEW = """onmouseover="this.style.borderColor=\\'#ff9900\\'" onmouseout="this.style.borderColor=\\'#e5e7eb\\'" """

c = content.count(OLD)
if c:
    content = content.replace(OLD, NEW)
    changes += c
    print(f"✅ Fixed {c} onmouseover/onmouseout instances")

if changes:
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Done — {changes} fix(es)")
else:
    print("No fixes needed")
