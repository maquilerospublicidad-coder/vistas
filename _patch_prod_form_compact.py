#!/usr/bin/env python3
"""Compact the product form popup so all fields fit without scrolling."""

FILE = '/workspaces/vistas/mockup.html'

with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

orig_len = len(html)

# ── 1. Increase card height from 780 → 860 in .productos-modal-card.wide ──────
html = html.replace(
    '''        .productos-modal-card.wide {
            width: min(98vw, 1120px) !important;
            height: min(96vh, 780px) !important;
            height: min(96dvh, 780px) !important;
            min-height: min(96vh, 780px) !important;
            min-height: min(96dvh, 780px) !important;
            max-height: min(96vh, 780px) !important;
            max-height: min(96dvh, 780px) !important;''',
    '''        .productos-modal-card.wide {
            width: min(98vw, 1120px) !important;
            height: min(99dvh, 860px) !important;
            height: min(99dvh, 860px) !important;
            min-height: min(99dvh, 860px) !important;
            min-height: min(99dvh, 860px) !important;
            max-height: min(99dvh, 860px) !important;
            max-height: min(99dvh, 860px) !important;'''
)

# ── 2. Same for #prodTabCard ───────────────────────────────────────────────────
html = html.replace(
    '''        #prodTabCard {
            width: min(98vw, 1120px) !important;
            height: min(96vh, 780px) !important;
            height: min(96dvh, 780px) !important;
            min-height: min(96vh, 780px) !important;
            min-height: min(96dvh, 780px) !important;
            max-height: min(96vh, 780px) !important;
            max-height: min(96dvh, 780px) !important;''',
    '''        #prodTabCard {
            width: min(98vw, 1120px) !important;
            height: min(99dvh, 860px) !important;
            height: min(99dvh, 860px) !important;
            min-height: min(99dvh, 860px) !important;
            min-height: min(99dvh, 860px) !important;
            max-height: min(99dvh, 860px) !important;
            max-height: min(99dvh, 860px) !important;'''
)

# ── 3. Same for #prodFormCard ──────────────────────────────────────────────────
html = html.replace(
    '''        #prodFormCard {
            width: min(98vw, 1120px) !important;
            height: min(96vh, 780px) !important;
            height: min(96dvh, 780px) !important;
            min-height: min(96vh, 780px) !important;
            min-height: min(96dvh, 780px) !important;
            max-height: min(96vh, 780px) !important;
            max-height: min(96dvh, 780px) !important;''',
    '''        #prodFormCard {
            width: min(98vw, 1120px) !important;
            height: min(99dvh, 860px) !important;
            height: min(99dvh, 860px) !important;
            min-height: min(99dvh, 860px) !important;
            min-height: min(99dvh, 860px) !important;
            max-height: min(99dvh, 860px) !important;
            max-height: min(99dvh, 860px) !important;'''
)

# ── 4. Same for the responsive override of #prodFormCard ─────────────────────
html = html.replace(
    '''            #prodFormCard {
                width: min(98vw, 1120px) !important;
                height: min(96vh, 780px) !important;
                height: min(96dvh, 780px) !important;
                min-height: min(96vh, 780px) !important;
                min-height: min(96dvh, 780px) !important;
                max-height: min(96vh, 780px) !important;
                max-height: min(96dvh, 780px) !important;
            }''',
    '''            #prodFormCard {
                width: min(98vw, 1120px) !important;
                height: min(99dvh, 860px) !important;
                height: min(99dvh, 860px) !important;
                min-height: min(99dvh, 860px) !important;
                min-height: min(99dvh, 860px) !important;
                max-height: min(99dvh, 860px) !important;
                max-height: min(99dvh, 860px) !important;
            }'''
)

# ── 5. Compact field sizes in wide card (reduce padding & gaps) ───────────────
old_field_css = '''        .productos-modal-card.wide .orden-field {
            gap: 3px;
            font-size: 0.72rem;
        }
        .productos-modal-card.wide .orden-field label {
            font-size: 0.7rem;
            margin-bottom: 1px;
            line-height: 1.3;
            padding: 0;
        }
        .productos-modal-card.wide .orden-field input,
        .productos-modal-card.wide .orden-field select,
        .productos-modal-card.wide .orden-field textarea {
            font-size: 0.78rem;
            padding: 6px 8px;
            border-radius: 6px;
            line-height: 1.35;
        }
        .productos-modal-card.wide .orden-field textarea {
            resize: none;
        }
        .productos-modal-card.wide .productos-btn {
            font-size: 0.72rem;
            padding: 5px 12px;
        }'''

new_field_css = '''        .productos-modal-card.wide .orden-field {
            gap: 2px;
            font-size: 0.7rem;
        }
        .productos-modal-card.wide .orden-field label {
            font-size: 0.65rem;
            margin-bottom: 0;
            line-height: 1.2;
            padding: 0;
        }
        .productos-modal-card.wide .orden-field input,
        .productos-modal-card.wide .orden-field select,
        .productos-modal-card.wide .orden-field textarea {
            font-size: 0.76rem;
            padding: 4px 6px;
            border-radius: 5px;
            line-height: 1.3;
        }
        .productos-modal-card.wide .orden-field textarea {
            resize: none;
        }
        .productos-modal-card.wide .productos-btn {
            font-size: 0.70rem;
            padding: 4px 10px;
        }'''

if old_field_css in html:
    html = html.replace(old_field_css, new_field_css)
    print("✅ Campos compactados")
else:
    print("❌ No se encontró el CSS de campos wide")

# ── 6. Compact the grid gap ───────────────────────────────────────────────────
old_grid = '''        .productos-modal-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 1px 3px;
            flex: 1 1 0;
            align-content: start;
            min-height: 0;
            overflow-y: auto;
            overflow-x: hidden;
        }'''

new_grid = '''        .productos-modal-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 1px 2px;
            flex: 1 1 0;
            align-content: start;
            min-height: 0;
            overflow-y: auto;
            overflow-x: hidden;
        }'''

if old_grid in html:
    html = html.replace(old_grid, new_grid)
    print("✅ Grid gap reducido")
else:
    print("❌ No se encontró .productos-modal-grid")

# ── 7. Remove margin-top:4px from medidas block (HTML inline) ─────────────────
html = html.replace(
    '<div class="orden-field productos-field-span3" data-nat="producto,fabricado,insumo" style="margin-top:4px;">',
    '<div class="orden-field productos-field-span3" data-nat="producto,fabricado,insumo">'
)
print("✅ Margin-top eliminado de la sección medidas")

# ── 8. Reduce prod-form-main gap ──────────────────────────────────────────────
old_main = '''        .prod-form-main {
            min-width: 0;
            min-height: 0;
            display: flex;
            flex-direction: column;
            gap: 2px;
            overflow: hidden;
            flex: 1 1 0;
        }'''

new_main = '''        .prod-form-main {
            min-width: 0;
            min-height: 0;
            display: flex;
            flex-direction: column;
            gap: 1px;
            overflow: hidden;
            flex: 1 1 0;
        }'''

if old_main in html:
    html = html.replace(old_main, new_main)
    print("✅ prod-form-main gap reducido")
else:
    print("⚠️  prod-form-main sin cambios (no encontrado exacto)")

# ── 9. Add padding:0 to overlay to maximise card space ───────────────────────
old_overlay = '''        .productos-modal-overlay {
            position: fixed;
            inset: 0;
            z-index: 2180;
            display: none;
            align-items: center;
            justify-content: center;
            background: rgba(9, 13, 22, 0.4);
            padding: 12px;
        }'''

new_overlay = '''        .productos-modal-overlay {
            position: fixed;
            inset: 0;
            z-index: 2180;
            display: none;
            align-items: center;
            justify-content: center;
            background: rgba(9, 13, 22, 0.4);
            padding: 4px;
        }'''

if old_overlay in html:
    html = html.replace(old_overlay, new_overlay)
    print("✅ Overlay padding reducido")
else:
    print("⚠️  Overlay no encontrado exacto")

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nListo. Longitud: {orig_len} → {len(html)}")
