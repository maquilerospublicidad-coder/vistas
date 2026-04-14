#!/usr/bin/env python3
"""
Re-apply ALL previous session changes + new changes for patch 14.
Previous session: tipo fusion, admin perms, remove almacen/insumos nav, add filters, move proveedores+config to grid.
New: rename stock→producto, remove emojis, uppercase, fix grid layout.
"""
import re
FILE = 'mockup.html'

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()
original_len = len(content)

# ============================================================
# PREVIOUS SESSION CHANGES - RE-APPLY
# ============================================================

# 1. Unify prodFormTipo + prodFormNaturaleza (prodFormTipo gets 6 options, prodFormNaturaleza hidden)
content = content.replace(
    '<div class="orden-field"><label for="prodFormTipo">Tipo de producto</label><select id="prodFormTipo"><option value="stock">📦 Producto en stock</option><option value="gran-formato">📐 Gran formato</option></select></div>',
    '<div class="orden-field"><label for="prodFormTipo">TIPO DE PRODUCTO</label><select id="prodFormTipo"><option value="stock">PRODUCTO</option><option value="gran-formato">GRAN FORMATO</option><option value="fabricado">FABRICADO</option><option value="insumo">INSUMO</option><option value="proceso">PROCESO</option><option value="servicio">SERVICIO</option></select></div>'
)

# Hide prodFormNaturaleza
content = content.replace(
    '<div class="orden-field"><label for="prodFormNaturaleza">Tipo comercial</label><select id="prodFormNaturaleza"><option value="producto">📦 Producto</option><option value="fabricado">🏭 Fabricado</option><option value="insumo">📦 Insumo</option><option value="proceso">⚙️ Proceso</option><option value="servicio">🛠 Servicio</option></select></div>',
    '<div class="orden-field" style="display:none;"><label for="prodFormNaturaleza">Tipo comercial</label><select id="prodFormNaturaleza"><option value="producto">PRODUCTO</option><option value="fabricado">FABRICADO</option><option value="insumo">INSUMO</option><option value="proceso">PROCESO</option><option value="servicio">SERVICIO</option></select></div>'
)

# 2. Fix admin permissions
content = content.replace(
    """    const canUsuarioAplicarDescuento = () => {
        const usuario = String(getUsuarioLogeado() || '').trim().toLowerCase();
        const lista = getConfigValue('permisos', 'descuentoUsuarios');""",
    """    const canUsuarioAplicarDescuento = () => {
        const role = (localStorage.getItem('logged_user_role') || '').trim().toLowerCase();
        if (role === 'admin') return true;
        const usuario = String(getUsuarioLogeado() || '').trim().toLowerCase();
        const lista = getConfigValue('permisos', 'descuentoUsuarios');"""
)

# 3. Remove REGISTROS dropdown, keep only the comment
content = content.replace(
    """        <div id="registrosDropdownWrap" class="registros-dropdown-wrap">
            <button class="registros-btn" onclick="toggleRegistrosMenu()">
                <span>📋 REGISTROS</span>
                <span class="registros-arrow">▼</span>
            </button>
            <div class="registros-menu">
                <button class="registros-menu-item" onclick="abrirRegistro('PROVEEDORES')">🏢 Proveedores</button>
                <button class="registros-menu-item" onclick="abrirRegistro('INSUMOS')">📦 Insumos</button>
                <button class="registros-menu-item" onclick="abrirRegistro('ALMACEN')">🏬 Almacén</button>
            </div>
        </div>""",
    """        <!-- Dropdown REGISTROS eliminado: Proveedores y Configuraciones ahora en cuadricula principal -->"""
)

# 4. Replace INSUMOS/ALMACEN nav with CONFIGURACIONES
content = content.replace(
    """        if (key === 'INSUMOS') {
            ocultarInicioSistema();
            if (window.openInsumosPopupGlobal) window.openInsumosPopupGlobal();
            return;
        }

        if (key === 'ALMACEN' || key === 'ALMACÉN') {
            ocultarInicioSistema();
            if (window.openAlmacenPopupGlobal) window.openAlmacenPopupGlobal();
            return;
        }""",
    """        if (key === 'CONFIGURACIONES') {
            ocultarInicioSistema();
            if (window.openConfiguracionesPopupGlobal) window.openConfiguracionesPopupGlobal();
            return;
        }"""
)

# 5. Add productosTipoFilter variable
content = content.replace(
    "    let productosLowStockOnly = false;\n    let productoEditandoId",
    "    let productosLowStockOnly = false;\n    let productosTipoFilter = '';\n    let productoEditandoId"
)

# 6. Add productos tipo filter in getProductosFiltrados
content = content.replace(
    """    const getProductosFiltrados = () => {
        const term = String(productosSearchTerm || '').toLowerCase();
        const code = String(productosCodigoFilter || '').toLowerCase();
        return productosData.filter((p) => {
            if (productosCategoriaFilter && p.categoria !== productosCategoriaFilter) return false;""",
    """    const getProductosFiltrados = () => {
        const term = String(productosSearchTerm || '').toLowerCase();
        const code = String(productosCodigoFilter || '').toLowerCase();
        return productosData.filter((p) => {
            if (productosTipoFilter && (p.tipo || 'stock') !== productosTipoFilter) return false;
            if (productosCategoriaFilter && p.categoria !== productosCategoriaFilter) return false;"""
)

# 7. Sync prodFormNaturaleza from unified prodFormTipo - replace the 3 duplicate listeners
# Find the existing listener blocks and replace
old_listeners = """    if (prodFormTipo) {
        prodFormTipo.addEventListener('change', () => {
            syncProdFormModeByTipo();
        });
    }

    if (prodFormNaturaleza) {
        prodFormNaturaleza.addEventListener('change', () => {
            syncProdFormModeByTipo();
        });
    }

    if (prodFormTipo) {
        prodFormTipo.addEventListener('change', () => {
            syncProdFormModeByTipo();
        });
    }"""

new_listeners = """    const syncNaturalezaFromTipo = () => {
        if (!prodFormTipo || !prodFormNaturaleza) return;
        const v = prodFormTipo.value;
        const natMap = { 'stock': 'producto', 'gran-formato': 'producto', 'fabricado': 'fabricado', 'insumo': 'insumo', 'proceso': 'proceso', 'servicio': 'servicio' };
        prodFormNaturaleza.value = natMap[v] || 'producto';
    };
    if (prodFormTipo) {
        prodFormTipo.addEventListener('change', () => {
            syncNaturalezaFromTipo();
            syncProdFormModeByTipo();
        });
    }"""

content = content.replace(old_listeners, new_listeners)

# 8. Update collectProductFormPayload to use natMap/tipoMap
content = content.replace(
    "        const tipoVal = prodFormTipo?.value || 'stock';\n        const natVal = prodFormNaturaleza?.value || 'producto';",
    "        const tipoVal = prodFormTipo?.value || 'stock';\n        const natMap = {'stock':'producto','gran-formato':'producto','fabricado':'fabricado','insumo':'insumo','proceso':'proceso','servicio':'servicio'};\n        const tipoMap = {'stock':'stock','gran-formato':'gran-formato','fabricado':'stock','insumo':'stock','proceso':'stock','servicio':'stock'};\n        const natVal = natMap[tipoVal] || 'producto';"
)

# 9. Update openProdFormForEdit to reverse-map naturaleza
old_edit = """        const editTipo = found.tipo === 'gran-formato' ? 'gran-formato' : 'stock';
        if (prodFormTipo) prodFormTipo.value = editTipo;"""
new_edit = """        const editTipo = (['stock','gran-formato','fabricado','insumo','proceso','servicio'].includes(found.tipo)) ? found.tipo : 'stock';
        if (prodFormTipo) prodFormTipo.value = editTipo;"""
content = content.replace(old_edit, new_edit)

# ============================================================
# NEW CHANGES - PATCH 14
# ============================================================

# 10. Fix inicio-grid: remove emojis, uppercase, add Proveedores + Configuraciones
old_grid = """        <div class="inicio-grid">
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('NUEVA ORDEN')"><span class="ico">🆕</span><span>Nueva Orden</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('MIS PEDIDOS')"><span class="ico">📦</span><span>Mis Pedidos</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('PRODUCCION')"><span class="ico">🏭</span><span>Producción</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('REPARTO')"><span class="ico">🚚</span><span>Reparto</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('PRODUCTOS')"><span class="ico">🧾</span><span>Productos</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('REPORTES')"><span class="ico">📊</span><span>Reportes</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('CAJA')"><span class="ico">💳</span><span>Caja</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('CALENDARIO')"><span class="ico">📅</span><span>Calendario</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('MUESTRARIO')"><span class="ico">🎨</span><span>Muestrario</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('CLIENTES')"><span class="ico">👥</span><span>Clientes</span></button>
        </div>"""

new_grid = """        <div class="inicio-grid">
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('NUEVA ORDEN')"><span>NUEVA ORDEN</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('MIS PEDIDOS')"><span>MIS PEDIDOS</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('PRODUCCION')"><span>PRODUCCION</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('REPARTO')"><span>REPARTO</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('PRODUCTOS')"><span>PRODUCTOS</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('REPORTES')"><span>REPORTES</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('CAJA')"><span>CAJA</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('CALENDARIO')"><span>CALENDARIO</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('MUESTRARIO')"><span>MUESTRARIO</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('CLIENTES')"><span>CLIENTES</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('PROVEEDORES')"><span>PROVEEDORES</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('CONFIGURACIONES')"><span>CONFIGURACIONES</span></button>
        </div>"""

content = content.replace(old_grid, new_grid)

# 11. Fix grid CSS: 12 buttons → 4 columns
content = content.replace(
    'grid-template-columns: repeat(5, 1fr);',
    'grid-template-columns: repeat(4, 1fr);'
)

# 12. Add tipo filter select in productos toolbar (after search input)
old_search = """                <div class="productos-search">
                    <label for="productosSearchInput">Buscar</label>
                    <input id="productosSearchInput" type="text" placeholder="Nombre, material, medida o código">
                </div>"""

new_search = """                <div class="productos-search">
                    <label for="productosSearchInput">BUSCAR</label>
                    <input id="productosSearchInput" type="text" placeholder="NOMBRE, MATERIAL, MEDIDA O CODIGO">
                </div>
                <div class="productos-tipo-filter" style="display:flex;gap:4px;align-items:center;flex-wrap:wrap;">
                    <select id="prodFiltroTipo" style="padding:4px 8px;font-size:0.48rem;border-radius:6px;border:1px solid #d1d5db;background:#fff;cursor:pointer;">
                        <option value="">TODOS LOS TIPOS</option>
                        <option value="stock">PRODUCTO</option>
                        <option value="gran-formato">GRAN FORMATO</option>
                        <option value="fabricado">FABRICADO</option>
                        <option value="insumo">INSUMO</option>
                        <option value="proceso">PROCESO</option>
                        <option value="servicio">SERVICIO</option>
                    </select>
                </div>"""

content = content.replace(old_search, new_search)

# 13. Update renderProductosTabla: fix tipoLabel + update legend + fix totalTabRows
content = content.replace(
    """            const isGF = row.tipo === 'gran-formato';
            const tipoLabel = isGF ? '📐 Gran formato' : '📦 Stock';""",
    """            const isGF = row.tipo === 'gran-formato';
            const tipoLabels = {'stock':'PRODUCTO','gran-formato':'GRAN FORMATO','fabricado':'FABRICADO','insumo':'INSUMO','proceso':'PROCESO','servicio':'SERVICIO'};
            const tipoLabel = tipoLabels[row.tipo] || 'PRODUCTO';"""
)

# Fix totalTabRows to use filtered rows count
content = content.replace(
    "        const totalTabRows = productosData.filter((p) => String(p.tipo || '') === String(productosTab)).length;",
    "        const totalTabRows = rows.length;"
)

# Update legend text
content = content.replace(
    """            const baseLabel = 'Listado de productos';
            const low = productosLowStockOnly ? ' | agotados o por agotarse' : '';
            const cat = productosCategoriaFilter ? ` | categoría: ${productosCategoriaFilter}` : '';
            const cod = productosCodigoFilter ? ` | código: ${productosCodigoFilter}` : '';
            productosLegend.textContent = `${baseLabel}${low}${cat}${cod}`;""",
    """            const baseLabel = 'LISTADO DE PRODUCTOS';
            const tipoF = productosTipoFilter ? ` | TIPO: ${productosTipoFilter.toUpperCase()}` : '';
            const low = productosLowStockOnly ? ' | AGOTADOS O POR AGOTARSE' : '';
            const cat = productosCategoriaFilter ? ` | CATEGORIA: ${productosCategoriaFilter}` : '';
            const cod = productosCodigoFilter ? ` | CODIGO: ${productosCodigoFilter}` : '';
            productosLegend.textContent = `${baseLabel}${tipoF}${low}${cat}${cod}`;"""
)

# 14. Add prodFiltroTipo event listener after productosSearchInput listener
old_search_listener = """    if (productosSearchInput) {
        productosSearchInput.addEventListener('input', () => {
            productosSearchTerm = productosSearchInput.value || '';
            renderProductosTabla();
        });
    }

    if (prodActualizar) {"""

new_search_listener = """    if (productosSearchInput) {
        productosSearchInput.addEventListener('input', () => {
            productosSearchTerm = productosSearchInput.value || '';
            renderProductosTabla();
        });
    }

    const prodFiltroTipo = document.getElementById('prodFiltroTipo');
    if (prodFiltroTipo) {
        prodFiltroTipo.addEventListener('change', () => {
            productosTipoFilter = prodFiltroTipo.value;
            renderProductosTabla();
        });
    }

    if (prodActualizar) {"""

content = content.replace(old_search_listener, new_search_listener)

# 15. Add global CSS for uppercase
css_inject = """
        /* GLOBAL UPPERCASE */
        body, button, input, select, textarea, th, td, label, option,
        h1, h2, h3, h4, h5, h6, span, div, p, a {
            text-transform: uppercase !important;
        }
        input::placeholder, textarea::placeholder {
            text-transform: uppercase !important;
        }
"""
content = content.replace('<style>', '<style>' + css_inject, 1)

# 16. Remove emojis from JS roleLabels
content = content.replace(
    "const roleLabels = { admin: '🟡 Admin', vendedor: '🟢 Vendedor', disenador: '🟣 Diseñador' };",
    "const roleLabels = { admin: 'ADMIN', vendedor: 'VENDEDOR', disenador: 'DISENADOR' };"
)

# Remove emoji from role select options in JS template literals
content = content.replace("🟡 Admin", "ADMIN")
content = content.replace("🟢 Vendedor", "VENDEDOR")
content = content.replace("🟣 Diseñador", "DISENADOR")

# Remove emoji from header home button
content = content.replace('🏠 Menú', 'MENU')

# ============================================================
# VERIFY
# ============================================================
print(f"Original length: {original_len}")
print(f"New length: {len(content)}")

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch 14b applied successfully.")
