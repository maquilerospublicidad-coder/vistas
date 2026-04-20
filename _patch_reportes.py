#!/usr/bin/env python3
"""Patch: Complete overhaul of the Reports module."""
import re

FILE = '/workspaces/vistas/mockup.html'

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# ============================================================
# 1. Add tab buttons in repHeadRight (currently empty)
# ============================================================
old_head_right = '            <div class="clientesmod-head-right" id="repHeadRight">\n            </div>'
new_head_right = '''            <div class="clientesmod-head-right" id="repHeadRight">
                <button id="repTabDash" class="clientesmod-btn primary" type="button" style="font-size:0.48rem;padding:4px 12px;">DASHBOARD</button>
                <button id="repTabRep" class="clientesmod-btn" type="button" style="font-size:0.48rem;padding:4px 12px;">REPORTES</button>
            </div>'''
content = content.replace(old_head_right, new_head_right, 1)

# ============================================================
# 2. Replace the report modules grid (7 → 15 modules)
# ============================================================
old_grid_start = '                <div id="repModulosGrid">'
old_grid_end = '                </div>\n                <!-- Vista de reporte expandido (pantalla completa) -->'
# Find the old grid section
idx_start = content.find(old_grid_start)
idx_end = content.find(old_grid_end)
if idx_start == -1 or idx_end == -1:
    print("ERROR: Could not find repModulosGrid section")
    exit(1)

new_grid = '''                <div id="repModulosGrid">
                    <div style="text-align:center;padding:14px 0 6px;">
                        <h3 style="margin:0;font-size:0.85rem;font-weight:900;color:#1f2937;letter-spacing:0.3px;">CENTRO DE REPORTES</h3>
                        <p style="margin:4px 0 0;font-size:0.55rem;color:#6b7280;">Selecciona un módulo para generar un reporte detallado</p>
                    </div>
                    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;padding:12px 24px;max-width:980px;margin:0 auto;">
                        <button id="repBtnVentas" class="rep-modulo-card" type="button">
                            <span class="rep-modulo-ico">📊</span>
                            <span class="rep-modulo-name">VENTAS</span>
                            <span class="rep-modulo-desc">Ventas realizadas, totales y por cliente</span>
                        </button>
                        <button id="repBtnProduccion" class="rep-modulo-card" type="button">
                            <span class="rep-modulo-ico">🏭</span>
                            <span class="rep-modulo-name">PRODUCCIÓN</span>
                            <span class="rep-modulo-desc">Estado de producción de todas las órdenes</span>
                        </button>
                        <button id="repBtnDiseno" class="rep-modulo-card" type="button">
                            <span class="rep-modulo-ico">🎨</span>
                            <span class="rep-modulo-name">DISEÑO</span>
                            <span class="rep-modulo-desc">Órdenes asignadas a diseñadores</span>
                        </button>
                        <button id="repBtnMuestrario" class="rep-modulo-card" type="button">
                            <span class="rep-modulo-ico">📋</span>
                            <span class="rep-modulo-name">MUESTRARIO</span>
                            <span class="rep-modulo-desc">Productos vinculados a muestras</span>
                        </button>
                        <button id="repBtnProductosVendidos" class="rep-modulo-card" type="button">
                            <span class="rep-modulo-ico">🛒</span>
                            <span class="rep-modulo-name">PRODUCTOS VENDIDOS</span>
                            <span class="rep-modulo-desc">Ventas detalladas por producto y variante</span>
                        </button>
                        <button id="repBtnPagosRecibidos" class="rep-modulo-card" type="button">
                            <span class="rep-modulo-ico">💳</span>
                            <span class="rep-modulo-name">PAGOS RECIBIDOS</span>
                            <span class="rep-modulo-desc">Anticipos y pagos por cliente y método</span>
                        </button>
                        <button id="repBtnHistorialCliente" class="rep-modulo-card" type="button">
                            <span class="rep-modulo-ico">👤</span>
                            <span class="rep-modulo-name">HISTORIAL CLIENTE</span>
                            <span class="rep-modulo-desc">Registro completo de un cliente</span>
                        </button>
                        <button id="repBtnClientes" class="rep-modulo-card" type="button">
                            <span class="rep-modulo-ico">👥</span>
                            <span class="rep-modulo-name">CLIENTES</span>
                            <span class="rep-modulo-desc">Directorio completo de clientes</span>
                        </button>
                        <button id="repBtnEntradasSalidas" class="rep-modulo-card" type="button">
                            <span class="rep-modulo-ico">📦</span>
                            <span class="rep-modulo-name">ENTRADAS / SALIDAS</span>
                            <span class="rep-modulo-desc">Movimientos de inventario y stock</span>
                        </button>
                        <button id="repBtnAlmacen" class="rep-modulo-card" type="button">
                            <span class="rep-modulo-ico">🏬</span>
                            <span class="rep-modulo-name">ALMACÉN</span>
                            <span class="rep-modulo-desc">Inventario actual del almacén</span>
                        </button>
                        <button id="repBtnInsumos" class="rep-modulo-card" type="button">
                            <span class="rep-modulo-ico">🧪</span>
                            <span class="rep-modulo-name">INSUMOS</span>
                            <span class="rep-modulo-desc">Existencias y consumo de insumos</span>
                        </button>
                        <button id="repBtnProveedores" class="rep-modulo-card" type="button">
                            <span class="rep-modulo-ico">🚚</span>
                            <span class="rep-modulo-name">PROVEEDORES</span>
                            <span class="rep-modulo-desc">Directorio y saldos de proveedores</span>
                        </button>
                        <button id="repBtnGastos" class="rep-modulo-card" type="button">
                            <span class="rep-modulo-ico">💸</span>
                            <span class="rep-modulo-name">GASTOS</span>
                            <span class="rep-modulo-desc">Gastos de compra de material</span>
                        </button>
                        <button id="repBtnCortesCaja" class="rep-modulo-card" type="button">
                            <span class="rep-modulo-ico">🏦</span>
                            <span class="rep-modulo-name">CORTES DE CAJA</span>
                            <span class="rep-modulo-desc">Historial de cortes y balances</span>
                        </button>
                        <button id="repBtnEnvios" class="rep-modulo-card" type="button">
                            <span class="rep-modulo-ico">✈️</span>
                            <span class="rep-modulo-name">ENVÍOS</span>
                            <span class="rep-modulo-desc">Historial de cotizaciones de envío</span>
                        </button>
                    </div>
                </div>'''
content = content[:idx_start] + new_grid + '\n                <!-- Vista de reporte expandido (pantalla completa) -->' + content[idx_end + len(old_grid_end):]

# ============================================================
# 3. Fix repVistaBack button (remove "VOLVER A REPORTES" text)
# ============================================================
content = content.replace(
    '<button id="repVistaBack" class="clientesmod-btn" type="button" style="font-size:0.52rem;">← VOLVER A REPORTES</button>',
    '<button id="repVistaBack" class="clientesmod-btn" type="button" style="font-size:0.6rem;padding:4px 10px;" title="Volver al centro de reportes">←</button>',
    1
)

# ============================================================
# 4. Add more filter options for new reports (estado filter needs more values)
# ============================================================
old_estado_filter = '''                        <div class="orden-field" id="repFiltroEstadoWrap">
                            <label for="repFiltroEstado">ESTADO</label>
                            <select id="repFiltroEstado">
                                <option value="">TODOS</option>
                                <option value="pendiente">PENDIENTE</option>
                                <option value="en-produccion">EN PRODUCCIÓN</option>
                                <option value="terminado">TERMINADO</option>
                                <option value="entregado">ENTREGADO</option>
                            </select>
                        </div>'''
new_estado_filter = '''                        <div class="orden-field" id="repFiltroEstadoWrap">
                            <label for="repFiltroEstado">ESTADO</label>
                            <select id="repFiltroEstado">
                                <option value="">TODOS</option>
                                <option value="pendiente">PENDIENTE</option>
                                <option value="en-produccion">EN PRODUCCIÓN</option>
                                <option value="pendiente-por-entregar">POR ENTREGAR</option>
                                <option value="terminado">TERMINADO</option>
                                <option value="entregado">ENTREGADO</option>
                            </select>
                        </div>
                        <div class="orden-field" id="repFiltroDisenadorWrap" style="display:none;">
                            <label for="repFiltroDisenador">DISEÑADOR</label>
                            <input id="repFiltroDisenador" type="text" placeholder="Todos">
                        </div>
                        <div class="orden-field" id="repFiltroCategoriaWrap" style="display:none;">
                            <label for="repFiltroCategoria">CATEGORÍA</label>
                            <input id="repFiltroCategoria" type="text" placeholder="Todas">
                        </div>'''
content = content.replace(old_estado_filter, new_estado_filter, 1)

# ============================================================
# 5. Fix reportesmodBack navigation (back arrow goes to grid if in report view)
# ============================================================
old_back_handler = '''    if (reportesmodBack) {
        reportesmodBack.addEventListener('click', () => {
            closeReportesPopup();
            if (typeof mostrarInicioSistema === 'function') mostrarInicioSistema();
        });
    }'''
new_back_handler = '''    if (reportesmodBack) {
        reportesmodBack.addEventListener('click', () => {
            // Si estamos viendo un reporte expandido, volver a la cuadrícula
            const vistaRep = document.getElementById('repVistaReporte');
            if (vistaRep && vistaRep.style.display !== 'none' && repTabActivo === 'reports') {
                volverAModulosReportes();
                return;
            }
            closeReportesPopup();
        });
    }'''
content = content.replace(old_back_handler, new_back_handler, 1)

# ============================================================
# 6. Add tab button event listeners (after reportesmodBack handler)
# ============================================================
# Find the location after the back handler to insert tab listeners
tab_listeners = '''
    // Tab buttons Dashboard / Reportes
    const repTabDash = document.getElementById('repTabDash');
    const repTabRep = document.getElementById('repTabRep');
    if (repTabDash) repTabDash.addEventListener('click', () => {
        switchRepTab('dashboard');
        if (repTabDash) { repTabDash.classList.add('primary'); }
        if (repTabRep) { repTabRep.classList.remove('primary'); }
    });
    if (repTabRep) repTabRep.addEventListener('click', () => {
        switchRepTab('reports');
        if (repTabRep) { repTabRep.classList.add('primary'); }
        if (repTabDash) { repTabDash.classList.remove('primary'); }
    });
'''
# Insert right after the popupReportesModulo click-outside handler
old_click_outside = '''    if (popupReportesModulo) {
        popupReportesModulo.addEventListener('click', (ev) => {
            if (ev.target === popupReportesModulo) closeReportesPopup();
        });
    }'''
content = content.replace(old_click_outside, old_click_outside + tab_listeners, 1)

# ============================================================
# 7. Replace the report button event listeners section
# ============================================================
old_report_btns = '''    // Botones de reportes (abren vista expandida)
    const repBtnVentas = document.getElementById('repBtnVentas');
    const repBtnEntradasSalidas = document.getElementById('repBtnEntradasSalidas');
    const repBtnGastos = document.getElementById('repBtnGastos');
    const repBtnCortesCaja = document.getElementById('repBtnCortesCaja');
    const repBtnPagosRecibidos = document.getElementById('repBtnPagosRecibidos');
    const repBtnHistorialCliente = document.getElementById('repBtnHistorialCliente');
    const repBtnProductosVendidos = document.getElementById('repBtnProductosVendidos');
    if (repBtnVentas) repBtnVentas.addEventListener('click', () => abrirReporteVista('REPORTE DE VENTAS', generarReporteVentas));
    if (repBtnEntradasSalidas) repBtnEntradasSalidas.addEventListener('click', () => abrirReporteVista('ENTRADAS Y SALIDAS', generarReporteEntradasSalidas));
    if (repBtnGastos) repBtnGastos.addEventListener('click', () => abrirReporteVista('REPORTE DE GASTOS', generarReporteGastos));
    if (repBtnCortesCaja) repBtnCortesCaja.addEventListener('click', () => abrirReporteVista('CORTES DE CAJA', generarReporteCortesCaja));
    if (repBtnPagosRecibidos) repBtnPagosRecibidos.addEventListener('click', () => abrirReporteVista('PAGOS RECIBIDOS', generarReportePagosRecibidos));
    if (repBtnHistorialCliente) repBtnHistorialCliente.addEventListener('click', () => abrirReporteVista('HISTORIAL DEL CLIENTE', generarReporteHistorialCliente));
    if (repBtnProductosVendidos) repBtnProductosVendidos.addEventListener('click', () => abrirReporteVista('PRODUCTOS VENDIDOS', generarReporteProductosVendidos));'''

new_report_btns = '''    // Botones de reportes (abren vista expandida)
    const repBtnVentas = document.getElementById('repBtnVentas');
    const repBtnEntradasSalidas = document.getElementById('repBtnEntradasSalidas');
    const repBtnGastos = document.getElementById('repBtnGastos');
    const repBtnCortesCaja = document.getElementById('repBtnCortesCaja');
    const repBtnPagosRecibidos = document.getElementById('repBtnPagosRecibidos');
    const repBtnHistorialCliente = document.getElementById('repBtnHistorialCliente');
    const repBtnProductosVendidos = document.getElementById('repBtnProductosVendidos');
    const repBtnProduccion = document.getElementById('repBtnProduccion');
    const repBtnDiseno = document.getElementById('repBtnDiseno');
    const repBtnMuestrario = document.getElementById('repBtnMuestrario');
    const repBtnClientes = document.getElementById('repBtnClientes');
    const repBtnAlmacen = document.getElementById('repBtnAlmacen');
    const repBtnInsumos = document.getElementById('repBtnInsumos');
    const repBtnProveedores = document.getElementById('repBtnProveedores');
    const repBtnEnvios = document.getElementById('repBtnEnvios');
    if (repBtnVentas) repBtnVentas.addEventListener('click', () => abrirReporteVista('REPORTE DE VENTAS', generarReporteVentas));
    if (repBtnEntradasSalidas) repBtnEntradasSalidas.addEventListener('click', () => abrirReporteVista('ENTRADAS Y SALIDAS', generarReporteEntradasSalidas));
    if (repBtnGastos) repBtnGastos.addEventListener('click', () => abrirReporteVista('REPORTE DE GASTOS', generarReporteGastos));
    if (repBtnCortesCaja) repBtnCortesCaja.addEventListener('click', () => abrirReporteVista('CORTES DE CAJA', generarReporteCortesCaja));
    if (repBtnPagosRecibidos) repBtnPagosRecibidos.addEventListener('click', () => abrirReporteVista('PAGOS RECIBIDOS', generarReportePagosRecibidos));
    if (repBtnHistorialCliente) repBtnHistorialCliente.addEventListener('click', () => abrirReporteVista('HISTORIAL DEL CLIENTE', generarReporteHistorialCliente));
    if (repBtnProductosVendidos) repBtnProductosVendidos.addEventListener('click', () => abrirReporteVista('PRODUCTOS VENDIDOS', generarReporteProductosVendidos));
    if (repBtnProduccion) repBtnProduccion.addEventListener('click', () => abrirReporteVista('REPORTE DE PRODUCCIÓN', generarReporteProduccion));
    if (repBtnDiseno) repBtnDiseno.addEventListener('click', () => abrirReporteVista('REPORTE DE DISEÑO', generarReporteDiseno));
    if (repBtnMuestrario) repBtnMuestrario.addEventListener('click', () => abrirReporteVista('REPORTE DE MUESTRARIO', generarReporteMuestrario));
    if (repBtnClientes) repBtnClientes.addEventListener('click', () => abrirReporteVista('DIRECTORIO DE CLIENTES', generarReporteClientes));
    if (repBtnAlmacen) repBtnAlmacen.addEventListener('click', () => abrirReporteVista('INVENTARIO ALMACÉN', generarReporteAlmacen));
    if (repBtnInsumos) repBtnInsumos.addEventListener('click', () => abrirReporteVista('REPORTE DE INSUMOS', generarReporteInsumos));
    if (repBtnProveedores) repBtnProveedores.addEventListener('click', () => abrirReporteVista('DIRECTORIO PROVEEDORES', generarReporteProveedores));
    if (repBtnEnvios) repBtnEnvios.addEventListener('click', () => abrirReporteVista('HISTORIAL DE ENVÍOS', generarReporteEnvios));'''
content = content.replace(old_report_btns, new_report_btns, 1)

# ============================================================
# 8. Update repFiltroAplicar to handle new report types
# ============================================================
old_filtro_aplicar = '''    if (repFiltroAplicar) repFiltroAplicar.addEventListener('click', () => {
        if (repReporteActivo === 'REPORTE DE VENTAS') generarReporteVentas();
        else if (repReporteActivo === 'ENTRADAS Y SALIDAS') generarReporteEntradasSalidas();
        else if (repReporteActivo === 'REPORTE DE GASTOS') generarReporteGastos();
        else if (repReporteActivo === 'CORTES DE CAJA') generarReporteCortesCaja();
        else if (repReporteActivo === 'PAGOS RECIBIDOS') generarReportePagosRecibidos();
        else if (repReporteActivo === 'HISTORIAL DEL CLIENTE') generarReporteHistorialCliente();
        else if (repReporteActivo === 'PRODUCTOS VENDIDOS') generarReporteProductosVendidos();
    });'''
new_filtro_aplicar = '''    if (repFiltroAplicar) repFiltroAplicar.addEventListener('click', () => {
        const mapFn = {
            'REPORTE DE VENTAS': generarReporteVentas,
            'ENTRADAS Y SALIDAS': generarReporteEntradasSalidas,
            'REPORTE DE GASTOS': generarReporteGastos,
            'CORTES DE CAJA': generarReporteCortesCaja,
            'PAGOS RECIBIDOS': generarReportePagosRecibidos,
            'HISTORIAL DEL CLIENTE': generarReporteHistorialCliente,
            'PRODUCTOS VENDIDOS': generarReporteProductosVendidos,
            'REPORTE DE PRODUCCIÓN': generarReporteProduccion,
            'REPORTE DE DISEÑO': generarReporteDiseno,
            'REPORTE DE MUESTRARIO': generarReporteMuestrario,
            'DIRECTORIO DE CLIENTES': generarReporteClientes,
            'INVENTARIO ALMACÉN': generarReporteAlmacen,
            'REPORTE DE INSUMOS': generarReporteInsumos,
            'DIRECTORIO PROVEEDORES': generarReporteProveedores,
            'HISTORIAL DE ENVÍOS': generarReporteEnvios
        };
        const fn = mapFn[repReporteActivo];
        if (fn) fn();
    });'''
content = content.replace(old_filtro_aplicar, new_filtro_aplicar, 1)

# ============================================================
# 9. Update abrirReporteVista to handle new filter visibility logic
# ============================================================
old_abrir_vista = '''    const abrirReporteVista = (titulo, generarFn) => {
        repReporteActivo = titulo;
        const grid = document.getElementById('repModulosGrid');
        const vista = document.getElementById('repVistaReporte');
        const tituloEl = document.getElementById('repVistaTitulo');
        if (grid) grid.style.display = 'none';
        if (vista) vista.style.display = '';
        if (tituloEl) tituloEl.textContent = titulo;
        // Set default date range
        const repFiltroDesde = document.getElementById('repFiltroDesde');
        const repFiltroHasta = document.getElementById('repFiltroHasta');
        const today = new Date().toISOString().slice(0, 10);
        const d30 = new Date(); d30.setDate(d30.getDate() - 30);
        if (repFiltroDesde && !repFiltroDesde.value) repFiltroDesde.value = d30.toISOString().slice(0, 10);
        if (repFiltroHasta && !repFiltroHasta.value) repFiltroHasta.value = today;
        // Show/hide product-specific filters
        const prodWrap = document.getElementById('repFiltroProductoWrap');
        const varWrap = document.getElementById('repFiltroVarianteWrap');
        const cliWrap = document.getElementById('repFiltroClienteWrap');
        const estWrap = document.getElementById('repFiltroEstadoWrap');
        if (prodWrap) prodWrap.style.display = titulo === 'PRODUCTOS VENDIDOS' ? '' : 'none';
        if (varWrap) varWrap.style.display = titulo === 'PRODUCTOS VENDIDOS' ? '' : 'none';
        if (cliWrap) cliWrap.style.display = titulo === 'HISTORIAL DEL CLIENTE' || titulo === 'REPORTE DE VENTAS' || titulo === 'PAGOS RECIBIDOS' ? '' : 'none';
        if (estWrap) estWrap.style.display = titulo === 'REPORTE DE VENTAS' ? '' : 'none';
        // Populate product filter for Productos Vendidos
        if (titulo === 'PRODUCTOS VENDIDOS') populateProductFilter();
        generarFn();
    };'''

new_abrir_vista = '''    const abrirReporteVista = (titulo, generarFn) => {
        repReporteActivo = titulo;
        const grid = document.getElementById('repModulosGrid');
        const vista = document.getElementById('repVistaReporte');
        const tituloEl = document.getElementById('repVistaTitulo');
        if (grid) grid.style.display = 'none';
        if (vista) vista.style.display = '';
        if (tituloEl) tituloEl.textContent = titulo;
        // Set default date range
        const repFiltroDesde = document.getElementById('repFiltroDesde');
        const repFiltroHasta = document.getElementById('repFiltroHasta');
        const today = new Date().toISOString().slice(0, 10);
        const d30 = new Date(); d30.setDate(d30.getDate() - 30);
        if (repFiltroDesde && !repFiltroDesde.value) repFiltroDesde.value = d30.toISOString().slice(0, 10);
        if (repFiltroHasta && !repFiltroHasta.value) repFiltroHasta.value = today;
        // Show/hide filters based on report type
        const prodWrap = document.getElementById('repFiltroProductoWrap');
        const varWrap = document.getElementById('repFiltroVarianteWrap');
        const cliWrap = document.getElementById('repFiltroClienteWrap');
        const estWrap = document.getElementById('repFiltroEstadoWrap');
        const disWrap = document.getElementById('repFiltroDisenadorWrap');
        const catWrap = document.getElementById('repFiltroCategoriaWrap');
        const noDateReports = ['DIRECTORIO DE CLIENTES', 'INVENTARIO ALMACÉN', 'REPORTE DE INSUMOS', 'DIRECTORIO PROVEEDORES', 'REPORTE DE MUESTRARIO'];
        const desdeEl = repFiltroDesde?.closest('.orden-field');
        const hastaEl = repFiltroHasta?.closest('.orden-field');
        if (desdeEl) desdeEl.style.display = noDateReports.includes(titulo) ? 'none' : '';
        if (hastaEl) hastaEl.style.display = noDateReports.includes(titulo) ? 'none' : '';
        if (prodWrap) prodWrap.style.display = titulo === 'PRODUCTOS VENDIDOS' ? '' : 'none';
        if (varWrap) varWrap.style.display = titulo === 'PRODUCTOS VENDIDOS' ? '' : 'none';
        if (cliWrap) cliWrap.style.display = ['HISTORIAL DEL CLIENTE', 'REPORTE DE VENTAS', 'PAGOS RECIBIDOS'].includes(titulo) ? '' : 'none';
        if (estWrap) estWrap.style.display = ['REPORTE DE VENTAS', 'REPORTE DE PRODUCCIÓN'].includes(titulo) ? '' : 'none';
        if (disWrap) disWrap.style.display = titulo === 'REPORTE DE DISEÑO' ? '' : 'none';
        if (catWrap) catWrap.style.display = titulo === 'REPORTE DE INSUMOS' ? '' : 'none';
        // Populate product filter for Productos Vendidos
        if (titulo === 'PRODUCTOS VENDIDOS') populateProductFilter();
        generarFn();
    };'''
content = content.replace(old_abrir_vista, new_abrir_vista, 1)

# ============================================================
# 10. Add new report generator functions before openReportesPopup
# ============================================================
# Find the openReportesPopup function and add new generators before it
old_open_reportes = '    const openReportesPopup = (tab) => {'

new_generators = '''
    // ===== REPORTE DE PRODUCCIÓN =====
    const generarReporteProduccion = () => {
        const { since, until } = getRepFiltroDates();
        const estadoFilter = String(document.getElementById('repFiltroEstado')?.value || '').trim().toLowerCase();
        loadMisPedidos();
        const rows = misPedidosData.filter((r) => {
            const dt = new Date((r.fechaEmitida || '') + 'T00:00:00');
            if (Number.isNaN(dt.getTime()) || dt < since || dt > until) return false;
            if (estadoFilter) {
                const est = normalizeStatus(r.estatusProduccion || '').replace(/\\s+/g, '-');
                if (est !== estadoFilter) return false;
            }
            return true;
        });
        const head = document.getElementById('repReporteHead');
        const body = document.getElementById('repReporteBody');
        if (head) head.innerHTML = '<tr><th>FOLIO</th><th>CLIENTE</th><th>PRODUCTO</th><th>DISEÑADOR</th><th>VENDEDOR</th><th>F.EMITIDA</th><th>F.ENTREGA</th><th>ESTADO</th><th>TOTAL</th></tr>';
        const pendientes = rows.filter(r => (r.estatusProduccion||'').includes('pendiente')).length;
        const enProd = rows.filter(r => (r.estatusProduccion||'').includes('produccion')).length;
        const terminados = rows.filter(r => (r.estatusProduccion||'') === 'terminado').length;
        const entregados = rows.filter(r => (r.estatusProduccion||'') === 'entregado').length;
        const totalVal = rows.reduce((a,r) => a + Number(r.total||0), 0);
        const resumen = document.getElementById('repVistaResumen');
        if (resumen) resumen.innerHTML = [
            '<span class="rep-chip">TOTAL: ' + rows.length + '</span>',
            '<span class="rep-chip" style="background:#fef3c7;border-color:#f59e0b;color:#92400e;">PENDIENTES: ' + pendientes + '</span>',
            '<span class="rep-chip" style="background:#dbeafe;border-color:#3b82f6;color:#1e40af;">EN PRODUCCIÓN: ' + enProd + '</span>',
            '<span class="rep-chip" style="background:#d1fae5;border-color:#10b981;color:#065f46;">TERMINADOS: ' + terminados + '</span>',
            '<span class="rep-chip" style="background:#e0e7ff;border-color:#6366f1;color:#3730a3;">ENTREGADOS: ' + entregados + '</span>',
            '<span class="rep-chip">VALOR: ' + formatMoney(totalVal) + '</span>'
        ].join('');
        if (body) {
            if (!rows.length) { body.innerHTML = '<tr><td colspan="9" class="clientesmod-empty">SIN ÓRDENES EN EL PERIODO</td></tr>'; return; }
            body.innerHTML = rows.map(r => {
                const prod = Array.isArray(r.lineas) && r.lineas.length ? r.lineas[0].producto : (r.producto || '--');
                const statusColors = {'pendiente':'#f59e0b','en-produccion':'#3b82f6','pendiente-por-entregar':'#8b5cf6','terminado':'#10b981','entregado':'#6b7280'};
                const st = r.estatusProduccion || 'pendiente';
                const stColor = statusColors[st] || '#6b7280';
                return '<tr><td>' + escCliMod(r.folio||r.id||'') + '</td><td>' + escCliMod(r.clienteNombre||r.cliente||'') + '</td><td>' + escCliMod(prod) + '</td><td>' + escCliMod(r.disenador||'--') + '</td><td>' + escCliMod(r.vendedor||'--') + '</td><td>' + escCliMod(r.fechaEmitida||'') + '</td><td>' + escCliMod(r.fechaEntrega||'') + '</td><td><span style="color:' + stColor + ';font-weight:800;text-transform:uppercase;font-size:0.48rem;">' + escCliMod(st) + '</span></td><td>' + formatMoney(Number(r.total||0)) + '</td></tr>';
            }).join('');
        }
    };

    // ===== REPORTE DE DISEÑO =====
    const generarReporteDiseno = () => {
        const { since, until } = getRepFiltroDates();
        const disFilter = String(document.getElementById('repFiltroDisenador')?.value || '').trim().toLowerCase();
        loadMisPedidos();
        const rows = misPedidosData.filter((r) => {
            if (!r.disenador) return false;
            const dt = new Date((r.fechaEmitida || '') + 'T00:00:00');
            if (Number.isNaN(dt.getTime()) || dt < since || dt > until) return false;
            if (disFilter && !String(r.disenador||'').toLowerCase().includes(disFilter)) return false;
            return true;
        });
        const head = document.getElementById('repReporteHead');
        const body = document.getElementById('repReporteBody');
        if (head) head.innerHTML = '<tr><th>FOLIO</th><th>DISEÑADOR</th><th>CLIENTE</th><th>PRODUCTO</th><th>F.EMITIDA</th><th>F.ENTREGA</th><th>ESTADO</th><th>NOTAS DISEÑO</th></tr>';
        // Count by designer
        const byDesigner = {};
        rows.forEach(r => {
            const d = r.disenador || 'SIN ASIGNAR';
            byDesigner[d] = (byDesigner[d]||0) + 1;
        });
        const resumen = document.getElementById('repVistaResumen');
        const chips = ['<span class="rep-chip">TOTAL: ' + rows.length + '</span>'];
        Object.entries(byDesigner).sort((a,b)=>b[1]-a[1]).forEach(([name,count]) => {
            chips.push('<span class="rep-chip" style="background:#fef3c7;border-color:#f59e0b;color:#92400e;">' + escCliMod(name) + ': ' + count + '</span>');
        });
        if (resumen) resumen.innerHTML = chips.join('');
        if (body) {
            if (!rows.length) { body.innerHTML = '<tr><td colspan="8" class="clientesmod-empty">SIN ÓRDENES DE DISEÑO</td></tr>'; return; }
            body.innerHTML = rows.map(r => {
                const prod = Array.isArray(r.lineas) && r.lineas.length ? r.lineas[0].producto : (r.producto || '--');
                return '<tr><td>' + escCliMod(r.folio||r.id||'') + '</td><td>' + escCliMod(r.disenador||'') + '</td><td>' + escCliMod(r.clienteNombre||r.cliente||'') + '</td><td>' + escCliMod(prod) + '</td><td>' + escCliMod(r.fechaEmitida||'') + '</td><td>' + escCliMod(r.fechaEntrega||'') + '</td><td>' + escCliMod(r.estatusProduccion||'') + '</td><td style="max-width:200px;overflow:hidden;text-overflow:ellipsis;">' + escCliMod(r.notasDisenador||r.comentarios||'--') + '</td></tr>';
            }).join('');
        }
    };

    // ===== REPORTE DE MUESTRARIO =====
    const generarReporteMuestrario = () => {
        let cfg = {};
        try { cfg = JSON.parse(localStorage.getItem('muestrario_product_config') || '{}'); } catch(_){}
        const entries = Object.entries(cfg);
        const head = document.getElementById('repReporteHead');
        const body = document.getElementById('repReporteBody');
        if (head) head.innerHTML = '<tr><th>#</th><th>PRODUCTO</th><th>MÓDULO ASIGNADO</th></tr>';
        const resumen = document.getElementById('repVistaResumen');
        if (resumen) resumen.innerHTML = '<span class="rep-chip">CONFIGURACIONES: ' + entries.length + '</span>';
        if (body) {
            if (!entries.length) { body.innerHTML = '<tr><td colspan="3" class="clientesmod-empty">SIN CONFIGURACIÓN DE MUESTRARIO</td></tr>'; return; }
            body.innerHTML = entries.map(([prod, mod], i) => '<tr><td>' + (i+1) + '</td><td>' + escCliMod(prod) + '</td><td>' + escCliMod(String(mod)) + '</td></tr>').join('');
        }
    };

    // ===== DIRECTORIO DE CLIENTES =====
    const generarReporteClientes = () => {
        loadClientesModulo();
        const data = typeof clientesModuloData !== 'undefined' ? clientesModuloData : [];
        const head = document.getElementById('repReporteHead');
        const body = document.getElementById('repReporteBody');
        if (head) head.innerHTML = '<tr><th>NOMBRE</th><th>EMPRESA</th><th>TELÉFONO</th><th>CORREO</th><th>CIUDAD</th><th>RFC</th><th>TIPO</th></tr>';
        const resumen = document.getElementById('repVistaResumen');
        if (resumen) resumen.innerHTML = '<span class="rep-chip">CLIENTES: ' + data.length + '</span>';
        if (body) {
            if (!data.length) { body.innerHTML = '<tr><td colspan="7" class="clientesmod-empty">SIN CLIENTES REGISTRADOS</td></tr>'; return; }
            body.innerHTML = data.map(c => '<tr><td>' + escCliMod(c.nombre||'') + '</td><td>' + escCliMod(c.empresa||'--') + '</td><td>' + escCliMod(c.telefono||'') + '</td><td>' + escCliMod(c.correo||'') + '</td><td>' + escCliMod(c.ciudad||'') + '</td><td>' + escCliMod(c.rfc||'--') + '</td><td>' + escCliMod(c.tipoCliente||'regular') + '</td></tr>').join('');
        }
    };

    // ===== INVENTARIO ALMACÉN =====
    const generarReporteAlmacen = () => {
        let almData = [];
        try { almData = JSON.parse(localStorage.getItem('mock_almacen_modulo_v1') || '[]'); } catch(_){}
        const head = document.getElementById('repReporteHead');
        const body = document.getElementById('repReporteBody');
        if (head) head.innerHTML = '<tr><th>PRODUCTO</th><th>STOCK</th><th>UBICACIÓN</th><th>COSTO UNITARIO</th><th>VALOR TOTAL</th><th>NOTAS</th></tr>';
        const totalStock = almData.reduce((a,x) => a + Number(x.stock||0), 0);
        const totalValor = almData.reduce((a,x) => a + Number(x.stock||0) * Number(x.costoUnitario||0), 0);
        const resumen = document.getElementById('repVistaResumen');
        if (resumen) resumen.innerHTML = '<span class="rep-chip">PRODUCTOS: ' + almData.length + '</span><span class="rep-chip">UNIDADES TOTALES: ' + totalStock + '</span><span class="rep-chip">VALOR INVENTARIO: ' + formatMoney(totalValor) + '</span>';
        if (body) {
            if (!almData.length) { body.innerHTML = '<tr><td colspan="6" class="clientesmod-empty">SIN PRODUCTOS EN ALMACÉN</td></tr>'; return; }
            body.innerHTML = almData.map(x => '<tr><td>' + escCliMod(x.producto||'') + '</td><td>' + Number(x.stock||0) + '</td><td>' + escCliMod(x.ubicacion||'--') + '</td><td>' + formatMoney(Number(x.costoUnitario||0)) + '</td><td>' + formatMoney(Number(x.stock||0)*Number(x.costoUnitario||0)) + '</td><td style="max-width:180px;overflow:hidden;text-overflow:ellipsis;">' + escCliMod(x.notas||'--') + '</td></tr>').join('');
        }
    };

    // ===== REPORTE DE INSUMOS =====
    const generarReporteInsumos = () => {
        let insData = [];
        try { insData = JSON.parse(localStorage.getItem('mock_insumos_modulo_v1') || '[]'); } catch(_){}
        const catFilter = String(document.getElementById('repFiltroCategoria')?.value || '').trim().toLowerCase();
        if (catFilter) insData = insData.filter(x => String(x.categoria||'').toLowerCase().includes(catFilter));
        const head = document.getElementById('repReporteHead');
        const body = document.getElementById('repReporteBody');
        if (head) head.innerHTML = '<tr><th>NOMBRE</th><th>CATEGORÍA</th><th>EXISTENCIAS</th><th>MÍNIMO</th><th>UNIDAD</th><th>COSTO UNIT.</th><th>VALOR STOCK</th><th>ESTADO</th></tr>';
        const totalVal = insData.reduce((a,x) => a + Number(x.existencias||0) * Number(x.costoUnitario||0), 0);
        const bajoMin = insData.filter(x => Number(x.existencias||0) < Number(x.minimo||0)).length;
        const resumen = document.getElementById('repVistaResumen');
        if (resumen) resumen.innerHTML = '<span class="rep-chip">INSUMOS: ' + insData.length + '</span><span class="rep-chip">VALOR: ' + formatMoney(totalVal) + '</span>' + (bajoMin > 0 ? '<span class="rep-chip" style="background:#fee2e2;border-color:#ef4444;color:#991b1b;">BAJO MÍNIMO: ' + bajoMin + '</span>' : '');
        if (body) {
            if (!insData.length) { body.innerHTML = '<tr><td colspan="8" class="clientesmod-empty">SIN INSUMOS REGISTRADOS</td></tr>'; return; }
            body.innerHTML = insData.map(x => {
                const stock = Number(x.existencias||0);
                const min = Number(x.minimo||0);
                const estado = stock <= 0 ? '<span style="color:#dc2626;font-weight:800;">AGOTADO</span>' : (stock < min ? '<span style="color:#f59e0b;font-weight:800;">BAJO</span>' : '<span style="color:#10b981;font-weight:800;">OK</span>');
                return '<tr><td>' + escCliMod(x.nombre||'') + '</td><td>' + escCliMod(x.categoria||'--') + '</td><td>' + stock + '</td><td>' + min + '</td><td>' + escCliMod(x.unidad||'pz') + '</td><td>' + formatMoney(Number(x.costoUnitario||0)) + '</td><td>' + formatMoney(stock * Number(x.costoUnitario||0)) + '</td><td>' + estado + '</td></tr>';
            }).join('');
        }
    };

    // ===== DIRECTORIO PROVEEDORES =====
    const generarReporteProveedores = () => {
        loadProveedoresModulo();
        const data = typeof proveedoresModuloData !== 'undefined' ? proveedoresModuloData : [];
        const head = document.getElementById('repReporteHead');
        const body = document.getElementById('repReporteBody');
        if (head) head.innerHTML = '<tr><th>NOMBRE</th><th>EMPRESA</th><th>TELÉFONO</th><th>CORREO</th><th>CRÉDITO (DÍAS)</th><th>SALDO PENDIENTE</th></tr>';
        const totalSaldo = data.reduce((a,x) => a + Number(x.saldoPendiente||0), 0);
        const resumen = document.getElementById('repVistaResumen');
        if (resumen) resumen.innerHTML = '<span class="rep-chip">PROVEEDORES: ' + data.length + '</span><span class="rep-chip">SALDO TOTAL PENDIENTE: ' + formatMoney(totalSaldo) + '</span>';
        if (body) {
            if (!data.length) { body.innerHTML = '<tr><td colspan="6" class="clientesmod-empty">SIN PROVEEDORES REGISTRADOS</td></tr>'; return; }
            body.innerHTML = data.map(x => '<tr><td>' + escCliMod(x.nombre||'') + '</td><td>' + escCliMod(x.empresa||'--') + '</td><td>' + escCliMod(x.telefono||'') + '</td><td>' + escCliMod(x.correo||'--') + '</td><td>' + (x.creditoDias||'--') + '</td><td>' + formatMoney(Number(x.saldoPendiente||0)) + '</td></tr>').join('');
        }
    };

    // ===== HISTORIAL DE ENVÍOS =====
    const generarReporteEnvios = () => {
        let historial = [];
        try { historial = JSON.parse(localStorage.getItem('paq_historial_costos_v1') || '[]'); } catch(_){}
        const { since, until } = getRepFiltroDates();
        historial = historial.filter(h => {
            if (!h.fecha) return true;
            const dt = new Date(h.fecha);
            return !Number.isNaN(dt.getTime()) && dt >= since && dt <= until;
        });
        const head = document.getElementById('repReporteHead');
        const body = document.getElementById('repReporteBody');
        if (head) head.innerHTML = '<tr><th>FECHA</th><th>PAQUETERÍA</th><th>SERVICIO</th><th>ORIGEN</th><th>DESTINO</th><th>PESO</th><th>COSTO</th></tr>';
        const totalCosto = historial.reduce((a,x) => a + Number(x.precio||x.costo||0), 0);
        const resumen = document.getElementById('repVistaResumen');
        if (resumen) resumen.innerHTML = '<span class="rep-chip">COTIZACIONES: ' + historial.length + '</span><span class="rep-chip">COSTO TOTAL: ' + formatMoney(totalCosto) + '</span>';
        if (body) {
            if (!historial.length) { body.innerHTML = '<tr><td colspan="7" class="clientesmod-empty">SIN HISTORIAL DE ENVÍOS</td></tr>'; return; }
            body.innerHTML = historial.reverse().map(h => '<tr><td>' + escCliMod(h.fecha ? new Date(h.fecha).toLocaleDateString('es-MX') : '--') + '</td><td>' + escCliMod(h.carrier||h.paqueteria||'') + '</td><td>' + escCliMod(h.servicio||h.service||'--') + '</td><td>' + escCliMod(h.origen||'--') + '</td><td>' + escCliMod(h.destino||'--') + '</td><td>' + escCliMod(h.peso ? h.peso + ' kg' : '--') + '</td><td>' + formatMoney(Number(h.precio||h.costo||0)) + '</td></tr>').join('');
        }
    };

    const openReportesPopup = (tab) => {'''

content = content.replace(old_open_reportes, new_generators, 1)

# ============================================================
# 11. Update dashboard KPIs to include production stats 
# ============================================================
# Add production-based KPIs to the dashboard
old_kpi_inventario = '''                <!-- KPIs de inventario -->
                <div style="display:grid;grid-template-columns:repeat(4,minmax(120px,1fr));gap:8px;margin-top:8px;">
                    <div class="caja-kpi"><b>⬆️ ENTRADAS HOY</b><span id="repKpiEntradasHoy" style="color:#16a34a;">0</span></div>
                    <div class="caja-kpi"><b>⬇️ SALIDAS HOY</b><span id="repKpiSalidasHoy" style="color:#dc2626;">0</span></div>
                    <div class="caja-kpi"><b>🔄 MOVS. PERIODO</b><span id="repKpiMovsPeriodo">0</span></div>
                    <div class="caja-kpi"><b>💳 MÉTODO TOP</b><span id="repKpiMetodoTop" style="font-size:0.65rem;">--</span></div>
                </div>'''

new_kpi_inventario = '''                <!-- KPIs de inventario -->
                <div style="display:grid;grid-template-columns:repeat(4,minmax(120px,1fr));gap:8px;margin-top:8px;">
                    <div class="caja-kpi"><b>⬆️ ENTRADAS HOY</b><span id="repKpiEntradasHoy" style="color:#16a34a;">0</span></div>
                    <div class="caja-kpi"><b>⬇️ SALIDAS HOY</b><span id="repKpiSalidasHoy" style="color:#dc2626;">0</span></div>
                    <div class="caja-kpi"><b>🔄 MOVS. PERIODO</b><span id="repKpiMovsPeriodo">0</span></div>
                    <div class="caja-kpi"><b>💳 MÉTODO TOP</b><span id="repKpiMetodoTop" style="font-size:0.65rem;">--</span></div>
                </div>

                <!-- KPIs de producción -->
                <div style="display:grid;grid-template-columns:repeat(5,minmax(120px,1fr));gap:8px;margin-top:8px;">
                    <div class="caja-kpi" style="border-left:3px solid #f59e0b;"><b>🏭 EN PRODUCCIÓN</b><span id="repKpiEnProduccion" style="color:#f59e0b;">0</span></div>
                    <div class="caja-kpi" style="border-left:3px solid #10b981;"><b>✅ TERMINADOS</b><span id="repKpiTerminados" style="color:#10b981;">0</span></div>
                    <div class="caja-kpi" style="border-left:3px solid #8b5cf6;"><b>📦 POR ENTREGAR</b><span id="repKpiPorEntregar" style="color:#8b5cf6;">0</span></div>
                    <div class="caja-kpi" style="border-left:3px solid #6b7280;"><b>🚚 ENTREGADOS</b><span id="repKpiEntregados" style="color:#6b7280;">0</span></div>
                    <div class="caja-kpi" style="border-left:3px solid #dc2626;"><b>⚠️ INSUMOS BAJO MÍN</b><span id="repKpiInsumosBajo" style="color:#dc2626;">0</span></div>
                </div>'''
content = content.replace(old_kpi_inventario, new_kpi_inventario, 1)

# ============================================================
# 12. Update renderReportesModulo to fill new production KPIs
# ============================================================
# Find the timestamp update in renderReportesModulo and add production KPI logic before it
old_timestamp = '''        if (repUltimaActualizacion) {
            repUltimaActualizacion.textContent = `ACTUALIZACION: ${new Date().toLocaleString('es-MX')}`;
        }'''

new_timestamp = '''        // KPIs de producción
        const allOrders = misPedidosData || [];
        const enProdEl = document.getElementById('repKpiEnProduccion');
        const terminadosEl = document.getElementById('repKpiTerminados');
        const porEntregarEl = document.getElementById('repKpiPorEntregar');
        const entregadosEl = document.getElementById('repKpiEntregados');
        const insumosBajoEl = document.getElementById('repKpiInsumosBajo');
        if (enProdEl) enProdEl.textContent = allOrders.filter(r => (r.estatusProduccion||'').includes('produccion')).length;
        if (terminadosEl) terminadosEl.textContent = allOrders.filter(r => (r.estatusProduccion||'') === 'terminado').length;
        if (porEntregarEl) porEntregarEl.textContent = allOrders.filter(r => (r.estatusProduccion||'') === 'pendiente-por-entregar').length;
        if (entregadosEl) entregadosEl.textContent = rows.filter(r => (r.estatusProduccion||'') === 'entregado').length;
        try {
            const insData = JSON.parse(localStorage.getItem('mock_insumos_modulo_v1') || '[]');
            if (insumosBajoEl) insumosBajoEl.textContent = insData.filter(x => Number(x.existencias||0) < Number(x.minimo||0)).length;
        } catch(_) { if (insumosBajoEl) insumosBajoEl.textContent = '0'; }

        if (repUltimaActualizacion) {
            repUltimaActualizacion.textContent = `ACTUALIZACION: ${new Date().toLocaleString('es-MX')}`;
        }'''
content = content.replace(old_timestamp, new_timestamp, 1)

# ============================================================
# 13. Update switchRepTab to also toggle tab button styles
# ============================================================
old_switch = '''    const switchRepTab = (tab) => {
        repTabActivo = tab;
        repModoActual = tab;
        const secDash = document.getElementById('repSeccionDashboard');
        const secRep = document.getElementById('repSeccionReportes');
        const titulo = document.getElementById('reportesmodTitulo');
        if (tab === 'dashboard') {
            if (secDash) secDash.style.display = '';
            if (secRep) secRep.style.display = 'none';
            if (titulo) titulo.textContent = 'DASHBOARD';
        } else {
            if (secDash) secDash.style.display = 'none';
            if (secRep) secRep.style.display = '';
            if (titulo) titulo.textContent = 'REPORTES';
            // Mostrar cuadrícula de módulos
            const grid = document.getElementById('repModulosGrid');
            const vista = document.getElementById('repVistaReporte');
            if (grid) grid.style.display = '';
            if (vista) vista.style.display = 'none';
        }
    };'''

new_switch = '''    const switchRepTab = (tab) => {
        repTabActivo = tab;
        repModoActual = tab;
        const secDash = document.getElementById('repSeccionDashboard');
        const secRep = document.getElementById('repSeccionReportes');
        const titulo = document.getElementById('reportesmodTitulo');
        const tabDash = document.getElementById('repTabDash');
        const tabRep = document.getElementById('repTabRep');
        if (tab === 'dashboard') {
            if (secDash) secDash.style.display = '';
            if (secRep) secRep.style.display = 'none';
            if (titulo) titulo.textContent = 'DASHBOARD';
            if (tabDash) tabDash.classList.add('primary');
            if (tabRep) tabRep.classList.remove('primary');
        } else {
            if (secDash) secDash.style.display = 'none';
            if (secRep) secRep.style.display = '';
            if (titulo) titulo.textContent = 'REPORTES';
            if (tabRep) tabRep.classList.add('primary');
            if (tabDash) tabDash.classList.remove('primary');
            // Mostrar cuadrícula de módulos
            const grid = document.getElementById('repModulosGrid');
            const vista = document.getElementById('repVistaReporte');
            if (grid) grid.style.display = '';
            if (vista) vista.style.display = 'none';
        }
    };'''
content = content.replace(old_switch, new_switch, 1)

# ============================================================
# WRITE
# ============================================================
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Patch applied successfully!")
print("Changes:")
print("  1. Tab buttons (Dashboard/Reportes) added to header")
print("  2. Report grid expanded: 7 → 15 modules (4-column layout)")
print("  3. 'VOLVER A REPORTES' replaced with ← arrow")
print("  4. Back arrow navigates to grid (not home) when in report view")
print("  5. 8 new report generators: Producción, Diseño, Muestrario, Clientes, Almacén, Insumos, Proveedores, Envíos")
print("  6. New filter fields: Diseñador, Categoría")
print("  7. New production KPIs in dashboard")
print("  8. switchRepTab updates tab button styles")
print("  9. abrirReporteVista handles all new report types")
print("  10. repFiltroAplicar handles all new report types")
