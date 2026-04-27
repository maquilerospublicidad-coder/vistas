#!/usr/bin/env python3
"""
Further compact product form popup.
Fix: flex-shrink, deduplicate height rules, reduce padding/gaps more aggressively.
"""
FILE = '/workspaces/vistas/mockup.html'

with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

orig_len = len(html)

# ── 1. Fix .productos-modal-card.wide — deduplicate + reduce sizes + fix flex-shrink ──
old_wide = '''        .productos-modal-card.wide {
            width: min(98vw, 1120px) !important;
            height: min(99dvh, 860px) !important;
            height: min(99dvh, 860px) !important;
            min-height: min(99dvh, 860px) !important;
            min-height: min(99dvh, 860px) !important;
            max-height: min(99dvh, 860px) !important;
            max-height: min(99dvh, 860px) !important;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            flex-shrink: 0;
            box-sizing: border-box;
            gap: 4px;
            padding: 8px 10px;
        }'''

new_wide = '''        .productos-modal-card.wide {
            width: min(98vw, 1120px) !important;
            height: min(98dvh, 830px) !important;
            max-height: min(98dvh, 830px) !important;
            min-height: 0 !important;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            flex-shrink: 1;
            box-sizing: border-box;
            gap: 2px;
            padding: 5px 8px;
        }'''

if old_wide in html:
    html = html.replace(old_wide, new_wide)
    print("✅ .productos-modal-card.wide corregido")
else:
    print("❌ No se encontró .productos-modal-card.wide")

# ── 2. Fix #prodTabCard ────────────────────────────────────────────────────────
old_tab = '''        #prodTabCard {
            width: min(98vw, 1120px) !important;
            height: min(99dvh, 860px) !important;
            height: min(99dvh, 860px) !important;
            min-height: min(99dvh, 860px) !important;
            min-height: min(99dvh, 860px) !important;
            max-height: min(99dvh, 860px) !important;
            max-height: min(99dvh, 860px) !important;
            overflow: hidden !important;
            box-sizing: border-box !important;
            display: flex !important;
            flex-direction: column !important;
        }'''

new_tab = '''        #prodTabCard {
            width: min(98vw, 1120px) !important;
            height: min(98dvh, 830px) !important;
            max-height: min(98dvh, 830px) !important;
            min-height: 0 !important;
            overflow: hidden !important;
            box-sizing: border-box !important;
            display: flex !important;
            flex-direction: column !important;
            flex-shrink: 1 !important;
        }'''

if old_tab in html:
    html = html.replace(old_tab, new_tab)
    print("✅ #prodTabCard corregido")
else:
    print("❌ No se encontró #prodTabCard")

# ── 3. Fix #prodFormCard ───────────────────────────────────────────────────────
old_form = '''        #prodFormCard {
            width: min(98vw, 1120px) !important;
            height: min(99dvh, 860px) !important;
            height: min(99dvh, 860px) !important;
            min-height: min(99dvh, 860px) !important;
            min-height: min(99dvh, 860px) !important;
            max-height: min(99dvh, 860px) !important;
            max-height: min(99dvh, 860px) !important;
            overflow: hidden !important;
            box-sizing: border-box !important;
            display: flex !important;
            flex-direction: column !important;
        }'''

new_form = '''        #prodFormCard {
            width: min(98vw, 1120px) !important;
            height: min(98dvh, 830px) !important;
            max-height: min(98dvh, 830px) !important;
            min-height: 0 !important;
            overflow: hidden !important;
            box-sizing: border-box !important;
            display: flex !important;
            flex-direction: column !important;
            flex-shrink: 1 !important;
        }'''

if old_form in html:
    html = html.replace(old_form, new_form)
    print("✅ #prodFormCard corregido")
else:
    print("❌ No se encontró #prodFormCard")

# ── 4. Fix responsive override ─────────────────────────────────────────────────
old_resp = '''            #prodFormCard {
                width: min(98vw, 1120px) !important;
                height: min(99dvh, 860px) !important;
                height: min(99dvh, 860px) !important;
                min-height: min(99dvh, 860px) !important;
                min-height: min(99dvh, 860px) !important;
                max-height: min(99dvh, 860px) !important;
                max-height: min(99dvh, 860px) !important;
            }'''

new_resp = '''            #prodFormCard {
                width: min(98vw, 1120px) !important;
                height: min(98dvh, 830px) !important;
                max-height: min(98dvh, 830px) !important;
                min-height: 0 !important;
            }'''

if old_resp in html:
    html = html.replace(old_resp, new_resp)
    print("✅ Responsive override corregido")
else:
    print("⚠️  Responsive override no encontrado exacto")

# ── 5. More aggressive field compaction ───────────────────────────────────────
old_fields = '''        .productos-modal-card.wide .orden-field {
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

new_fields = '''        .productos-modal-card.wide .orden-field {
            gap: 1px;
            font-size: 0.68rem;
        }
        .productos-modal-card.wide .orden-field label {
            font-size: 0.62rem;
            margin-bottom: 0;
            line-height: 1.15;
            padding: 0;
        }
        .productos-modal-card.wide .orden-field input,
        .productos-modal-card.wide .orden-field select,
        .productos-modal-card.wide .orden-field textarea {
            font-size: 0.74rem;
            padding: 3px 6px;
            border-radius: 5px;
            line-height: 1.25;
        }
        .productos-modal-card.wide .orden-field textarea {
            resize: none;
        }
        .productos-modal-card.wide .productos-btn {
            font-size: 0.68rem;
            padding: 3px 9px;
        }'''

if old_fields in html:
    html = html.replace(old_fields, new_fields)
    print("✅ Campos más compactos")
else:
    print("❌ No se encontró el CSS de campos wide")

# ── 6. Reduce wizard gap and photo-pane padding ───────────────────────────────
old_wizard = '''        .prod-form-wizard {
            display: grid;
            grid-template-columns: 180px minmax(0, 1fr);
            grid-template-rows: minmax(0, 1fr);
            gap: 6px;
            flex: 1 1 0;
            min-height: 0;
            overflow: hidden;
        }'''

new_wizard = '''        .prod-form-wizard {
            display: grid;
            grid-template-columns: 170px minmax(0, 1fr);
            grid-template-rows: minmax(0, 1fr);
            gap: 4px;
            flex: 1 1 0;
            min-height: 0;
            overflow: hidden;
        }'''

if old_wizard in html:
    html = html.replace(old_wizard, new_wizard)
    print("✅ Wizard gap reducido")
else:
    print("❌ No se encontró .prod-form-wizard")

old_photo = '''        .prod-photo-pane {
            background: #ff9900;
            border-radius: 10px;
            overflow-y: auto;
            padding: 8px;
            display: flex;
            flex-direction: column;
            gap: 6px;
            color: #fff;
            overflow-y: auto;
            min-height: 0;
        }'''

new_photo = '''        .prod-photo-pane {
            background: #ff9900;
            border-radius: 10px;
            overflow-y: auto;
            padding: 6px;
            display: flex;
            flex-direction: column;
            gap: 4px;
            color: #fff;
            min-height: 0;
        }'''

if old_photo in html:
    html = html.replace(old_photo, new_photo)
    print("✅ Photo pane compactado")
else:
    print("❌ No se encontró .prod-photo-pane")

# ── 7. Reduce photo-pane-extras gap ────────────────────────────────────────────
old_extras = '''        .prod-photo-pane-extras {
            display: flex;
            flex-direction: column;
            gap: 6px;
            margin-top: 2px;
        }'''

new_extras = '''        .prod-photo-pane-extras {
            display: flex;
            flex-direction: column;
            gap: 4px;
            margin-top: 1px;
        }'''

if old_extras in html:
    html = html.replace(old_extras, new_extras)
    print("✅ Photo pane extras compactado")
else:
    print("❌ No se encontró .prod-photo-pane-extras")

# ── 8. Compact products-modal-actions ─────────────────────────────────────────
old_actions = '''        .productos-modal-actions {
            display: flex;
            justify-content: flex-end;
            gap: 6px;
            flex-shrink: 0;
            padding-top: 2px;
        }'''

new_actions = '''        .productos-modal-actions {
            display: flex;
            justify-content: flex-end;
            gap: 6px;
            flex-shrink: 0;
            padding-top: 1px;
        }'''

if old_actions in html:
    html = html.replace(old_actions, new_actions)
    print("✅ Actions compactado")
else:
    print("❌ No se encontró .productos-modal-actions")

# ── 9. Reduce título size ──────────────────────────────────────────────────────
old_title = '''        .productos-modal-title {
            margin: 0;
            font-size: 0.74rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 0.22px;
            color: #1f2937;
        }'''

new_title = '''        .productos-modal-title {
            margin: 0;
            font-size: 0.72rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 0.22px;
            color: #1f2937;
            line-height: 1.2;
        }'''

if old_title in html:
    html = html.replace(old_title, new_title)
    print("✅ Título compactado")
else:
    print("❌ No se encontró .productos-modal-title")

# ── 10. Reduce pack dimensions grid inline gap ──────────────────────────────────
# The inline style on the 5-col medidas grid has gap:8px — reduce to 4px
html = html.replace(
    'style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr 1fr;gap:8px;"',
    'style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr 1fr;gap:4px;"'
)
print("✅ Grid medidas inline gap reducido")

# ── 11. Reduce .prod-form-main gap (already 1px but verify) ───────────────────
# Was set to 1px already, keep as is

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nListo. Longitud: {orig_len} → {len(html)}")
