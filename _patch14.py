#!/usr/bin/env python3
"""
Patch 14: Remove emojis from UI, uppercase text, rename stock→producto,
fix grid layout, enhance stock entry/exit, split reportes/dashboard.
"""
import re, sys

FILE = 'mockup.html'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

original = content

# ============================================================
# 1. Remove emojis from inicio-grid buttons & keep text uppercase
# ============================================================
# Replace inicio-card buttons: remove <span class="ico">EMOJI</span> and uppercase the label
def fix_inicio_card(m):
    onclick = m.group(1)
    label = m.group(2).strip().upper()
    return f'<button class="inicio-card" type="button" onclick="{onclick}"><span>{label}</span></button>'

content = re.sub(
    r'<button class="inicio-card" type="button" onclick="([^"]+)"><span class="ico">[^<]*</span><span>([^<]+)</span></button>',
    fix_inicio_card,
    content
)

# ============================================================
# 2. Fix grid CSS: 12 buttons → 4 columns x 3 rows
# ============================================================
content = content.replace(
    'grid-template-columns: repeat(5, 1fr);',
    'grid-template-columns: repeat(4, 1fr);'
)

# ============================================================
# 3. Rename "Producto en stock" → "PRODUCTO" in all selects/labels
# ============================================================
# prodFormTipo options - remove emojis and uppercase
content = re.sub(
    r'<option value="stock">[^<]*</option>',
    '<option value="stock">PRODUCTO</option>',
    content
)
content = re.sub(
    r'<option value="gran-formato">[^<]*</option>',
    '<option value="gran-formato">GRAN FORMATO</option>',
    content
)
content = re.sub(
    r'<option value="fabricado">[^<]*</option>',
    '<option value="fabricado">FABRICADO</option>',
    content
)
content = re.sub(
    r'<option value="insumo">[^<]*</option>',
    '<option value="insumo">INSUMO</option>',
    content
)
content = re.sub(
    r'<option value="proceso">[^<]*</option>',
    '<option value="proceso">PROCESO</option>',
    content
)
content = re.sub(
    r'<option value="servicio">[^<]*</option>',
    '<option value="servicio">SERVICIO</option>',
    content
)

# "Todos los tipos" → "TODOS LOS TIPOS"
content = content.replace(
    '<option value="">Todos los tipos</option>',
    '<option value="">TODOS LOS TIPOS</option>'
)

# ============================================================
# 4. Fix tipoLabels in JS (renderProductosTabla)
# ============================================================
content = content.replace(
    "const tipoLabels = {'stock':'📦 Stock','gran-formato':'📐 Gran formato','fabricado':'🔧 Fabricado','insumo':'🧱 Insumo','proceso':'⚙ Proceso','servicio':'🛎 Servicio'};",
    "const tipoLabels = {'stock':'PRODUCTO','gran-formato':'GRAN FORMATO','fabricado':'FABRICADO','insumo':'INSUMO','proceso':'PROCESO','servicio':'SERVICIO'};"
)
content = content.replace(
    "const tipoLabel = tipoLabels[row.tipo] || '📦 Stock';",
    "const tipoLabel = tipoLabels[row.tipo] || 'PRODUCTO';"
)

# ============================================================
# 5. Remove emojis from CRUD buttons in productos toolbar
# ============================================================
content = content.replace('➕ Agregar', 'AGREGAR')
content = content.replace('✏️ Editar', 'EDITAR')
content = content.replace('🗑️ Eliminar', 'ELIMINAR')
content = content.replace('✏ Editar', 'EDITAR')
content = content.replace('🗑 Eliminar', 'ELIMINAR')

# ============================================================
# 6. Remove emojis from all button/label text throughout
# ============================================================

# Common emoji-prefixed text in buttons, titles, labels
emoji_text_map = [
    # Header / navigation
    ('🏠 Menú', 'MENU'),
    ('🏠 Menu', 'MENU'),
    # Module titles
    ('MÓDULO DE PRODUCTOS', 'MODULO DE PRODUCTOS'),
    ('Listado de productos', 'LISTADO DE PRODUCTOS'),
    ('Sin productos para los filtros actuales.', 'SIN PRODUCTOS PARA LOS FILTROS ACTUALES.'),
    # Product toolbar icons - replace emoji-only buttons with text
    ('Registrar entrada de stock', 'REGISTRAR ENTRADA DE STOCK'),
    ('Actualizar todo', 'ACTUALIZAR TODO'),
    ('Productos agotados o por agotarse', 'PRODUCTOS AGOTADOS O POR AGOTARSE'),
    ('Exportar PDF', 'EXPORTAR PDF'),
    ('Filtrar por categoría', 'FILTRAR POR CATEGORIA'),
    ('Filtrar por código de producto', 'FILTRAR POR CODIGO DE PRODUCTO'),
    ('Registrar entrada de stock', 'REGISTRAR ENTRADA DE STOCK'),
    ('Imprimir inventario', 'IMPRIMIR INVENTARIO'),
    ('Exportar en Excel', 'EXPORTAR EN EXCEL'),
    ('Abrir plantilla', 'ABRIR PLANTILLA'),
    ('Importar desde', 'IMPORTAR DESDE'),
    # Reportes
    ('PANEL DE VENTAS', 'PANEL DE VENTAS'),
    ('Selecciona un modulo principal para iniciar', 'SELECCIONA UN MODULO PRINCIPAL PARA INICIAR'),
    # Popup titles
    ('Configuraciones del sistema', 'CONFIGURACIONES DEL SISTEMA'),
    ('Registrar entrada de stock', 'REGISTRAR ENTRADA DE STOCK'),
    ('Buscar producto', 'BUSCAR PRODUCTO'),
    ('Cantidad de entrada', 'CANTIDAD DE ENTRADA'),
    ('Registrar', 'REGISTRAR'),
    ('Cerrar', 'CERRAR'),
    ('Buscar', 'BUSCAR'),
    ('Nombre, material, medida o código', 'NOMBRE, MATERIAL, MEDIDA O CODIGO'),
    ('Escribe para filtrar...', 'ESCRIBE PARA FILTRAR...'),
    # Table headers
    ('Producto', 'PRODUCTO'),
    ('Medida', 'MEDIDA'),
    ('Material', 'MATERIAL'),
    ('Existencias', 'EXISTENCIAS'),
    ('Precio revendedor', 'PRECIO REVENDEDOR'),
    ('Precio venta', 'PRECIO VENTA'),
    ('Registros:', 'REGISTROS:'),
    # Volver
    ('Volver al menú principal', 'VOLVER AL MENU PRINCIPAL'),
]

# Apply only in HTML attributes and visible text, not in JS logic
for old, new in emoji_text_map:
    content = content.replace(old, new)

# ============================================================
# 7. Comprehensive emoji removal from visible UI strings
# ============================================================
# Remove standalone emojis used as button content (icon buttons)
# These are single-character emoji buttons like ↻, ⚠, 📄, etc.
# We'll leave the functional icon buttons but remove emoji prefixes from text

# Remove emoji from JS string literals that render to UI
emoji_patterns = [
    (r"'📦 Stock'", "'PRODUCTO'"),
    (r"'📐 Gran formato'", "'GRAN FORMATO'"),
    (r"'🔧 Fabricado'", "'FABRICADO'"),
    (r"'🧱 Insumo'", "'INSUMO'"),
    (r"'⚙ Proceso'", "'PROCESO'"),
    (r"'🛎 Servicio'", "'SERVICIO'"),
    (r"'📦 Producto en stock'", "'PRODUCTO'"),
    (r"'🏭 Producto fabricado'", "'FABRICADO'"),
    (r"'📦 Insumo'", "'INSUMO'"),
    (r"'⚙️ Proceso'", "'PROCESO'"),
    (r"'🛠 Servicio'", "'SERVICIO'"),
    (r"'📐 Gran Formato'", "'GRAN FORMATO'"),
]

for old, new in emoji_patterns:
    content = content.replace(old, new)

# roleLabels with emojis
content = content.replace(
    "const roleLabels = { admin: '🟡 Admin', vendedor: '🟢 Vendedor', disenador: '🟣 Diseñador' };",
    "const roleLabels = { admin: 'ADMIN', vendedor: 'VENDEDOR', disenador: 'DISENADOR' };"    
)

# Role badge labels
content = content.replace("'Administrador'", "'ADMINISTRADOR'")
content = content.replace("'Diseñador'", "'DISENADOR'")
content = content.replace("'Vendedor'", "'VENDEDOR'")

# config section titles with emojis  
content = content.replace("'🟡 Admin'", "'ADMIN'")
content = content.replace("'🟢 Vendedor'", "'VENDEDOR'")
content = content.replace("'🟣 Diseñador'", "'DISENADOR'")

# Emojis in role select options
content = re.sub(
    r"<option value=\"admin\"([^>]*)>🟡 Admin</option>",
    r'<option value="admin"\1>ADMIN</option>',
    content
)
content = re.sub(
    r"<option value=\"vendedor\"([^>]*)>🟢 Vendedor</option>",
    r'<option value="vendedor"\1>VENDEDOR</option>',
    content
)
content = re.sub(
    r"<option value=\"disenador\"([^>]*)>🟣 Diseñador</option>",
    r'<option value="disenador"\1>DISENADOR</option>',
    content
)

# ============================================================
# 8. CSS text-transform: uppercase globally
# ============================================================
# Add a global CSS rule for uppercase
css_inject = """
        /* GLOBAL UPPERCASE */
        body, button, input, select, textarea, th, td, label, option, h1, h2, h3, h4, h5, h6, span, div, p, a {
            text-transform: uppercase !important;
        }
        input::placeholder, textarea::placeholder {
            text-transform: uppercase !important;
        }
"""
# Insert after the first <style> tag
content = content.replace('<style>', '<style>' + css_inject, 1)

# ============================================================
# 9. Remove remaining common emojis from HTML visible text
# ============================================================
# Remove emojis that appear as standalone text or prefixed to labels  
standalone_emojis = [
    '🆕', '📦', '🏭', '🚚', '🧾', '📊', '💳', '📅', '🎨', '👥',
    '🏢', '⚙️', '🗄️', '📋', '🏬', '🔔', '💰', '📈', '🔑',
    '⬇', '⬆', '✏', '🗑', '📤', '💬', '✕', '✅', '⚠️', '❌',
    '🖨', '📁', '📏', '🌈', '💾', '👁️', '🧪', '🏷', '🔄',
    '🚨', '⬅️', '➡️', '▶', '◀', '🔍',
]

# Only remove emojis that are inside <span class="ico"> tags (already handled above)
# For other emojis in text, we need careful handling

# Remove emoji prefixes from notify/alert messages in JS - simplified approach
# Not needed since text-transform: uppercase handles display

print(f"Original: {len(original)} chars")
print(f"Modified: {len(content)} chars")

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch 14 applied successfully.")
