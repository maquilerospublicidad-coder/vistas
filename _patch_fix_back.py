#!/usr/bin/env python3
"""Fix: All back buttons use mostrarInicioSistema() correctly"""
FILE = '/workspaces/vistas/mockup.html'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix Control de Reparto back button
old = "var ini=document.getElementById('inicio-sistema');if(ini)ini.style.display='';"
new = "if(typeof mostrarInicioSistema==='function') mostrarInicioSistema();"
if old in content:
    content = content.replace(old, new)
    print("Fixed: ctrlRepBack now calls mostrarInicioSistema()")
else:
    print("WARNING: inicio-sistema ref not found")

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done!")
