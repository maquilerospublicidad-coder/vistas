#!/usr/bin/env python3
"""Add Recolección tab button to App Móvil entTabs"""
FILE = '/workspaces/vistas/mockup.html'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

OLD = '''          <button class="entrega-tab active" data-status="pendiente">📬 Pendientes</button>
          <button class="entrega-tab" data-status="en_camino">🚚 En Camino</button>
          <button class="entrega-tab" data-status="entregada">✅ Entregadas</button>
          <button class="entrega-tab" data-status="no_entregada">❌ No Entregadas</button>'''

NEW = '''          <button class="entrega-tab active" data-status="pendiente">📬 Pendientes</button>
          <button class="entrega-tab" data-status="recoleccion">🏭 Recolección</button>
          <button class="entrega-tab" data-status="en_camino">🚚 En Camino</button>
          <button class="entrega-tab" data-status="entregada">✅ Entregadas</button>
          <button class="entrega-tab" data-status="no_entregada">❌ No Entregadas</button>'''

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Recolección tab added to App Móvil")
else:
    print("ERROR: Tab block not found")
