#!/usr/bin/env python3
"""Replace ALMACÉN PEDIDOS button with RECEPCIÓN SUCURSAL and add handler"""
FILE = '/workspaces/vistas/mockup.html'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# 1. Replace menu button
OLD_BTN = """<button class="inicio-card" type="button" onclick="abrirModuloPrincipal('ALMACEN PEDIDOS')"><span class="ico">📦</span><span>ALMACÉN PEDIDOS</span></button>"""
NEW_BTN = """<button class="inicio-card" type="button" onclick="abrirModuloPrincipal('RECEPCION SUCURSAL')"><span class="ico">📷</span><span>RECEPCIÓN<br>SUCURSAL</span></button>"""

if OLD_BTN in content:
    content = content.replace(OLD_BTN, NEW_BTN, 1)
    changes += 1
    print("✅ 1: Menu button replaced")
else:
    print("⚠ 1: Menu button not found")

# 2. Replace the ALMACEN PEDIDOS handler with RECEPCION SUCURSAL
OLD_HANDLER = """        if (key === 'ALMACEN PEDIDOS') {
            ocultarInicioSistema();
            if (window.openAlmacenPedidosPopupGlobal) window.openAlmacenPedidosPopupGlobal();
            return;
        }"""

NEW_HANDLER = """        if (key === 'RECEPCION SUCURSAL') {
            ocultarInicioSistema();
            if (window.openRecepcionSucursalGlobal) window.openRecepcionSucursalGlobal();
            return;
        }"""

if OLD_HANDLER in content:
    content = content.replace(OLD_HANDLER, NEW_HANDLER, 1)
    changes += 1
    print("✅ 2: Handler replaced")
else:
    print("⚠ 2: Handler not found")

if changes:
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"\n✅ Done — {changes} change(s) applied")
else:
    print("\n❌ No changes made")
