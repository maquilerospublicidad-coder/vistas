#!/usr/bin/env python3
"""Add RECEPCIÓN SUCURSAL button to main menu after PRODUCCION"""
FILE = '/workspaces/vistas/mockup.html'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

MARKER = """            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('PRODUCCION')"><span class="ico">🏭</span><span>PRODUCCIÓN</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('CONTROL REPARTIDORES')">"""

REPLACEMENT = """            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('PRODUCCION')"><span class="ico">🏭</span><span>PRODUCCIÓN</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('RECEPCION SUCURSAL')"><span class="ico">📷</span><span>RECEPCIÓN<br>SUCURSAL</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('CONTROL REPARTIDORES')">"""

if MARKER in content:
    content = content.replace(MARKER, REPLACEMENT, 1)
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ RECEPCIÓN SUCURSAL button added to main menu")
else:
    print("ERROR: marker not found")
