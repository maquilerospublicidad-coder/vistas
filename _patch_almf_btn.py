#!/usr/bin/env python3
"""Add Almacén Físico button to Productos toolbar"""
FILE = '/workspaces/vistas/mockup.html'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

import re
# Find the prodImprimir button line and add after it
pattern = r'(<button id="prodImprimir"[^>]*>🖨</button>)'
match = re.search(pattern, content)
if match:
    old = match.group(0)
    new = old + '\n                        <button id="prodAlmacenFisico" class="productos-btn productos-icon-btn" type="button" data-tip="Almacén Físico" title="Almacén Físico" aria-label="Almacén Físico" style="background:#ff9900;color:#fff;font-weight:800;font-size:0.6rem;padding:5px 10px;border-radius:8px;">📦 ALMACÉN FÍSICO</button>'
    content = content.replace(old, new, 1)
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Almacén Físico button added")
else:
    print("ERROR: prodImprimir not found")
