#!/usr/bin/env python3
"""Patch: Remove Producción/Muestrario/Clientes reports, redesign Historial Cliente."""

FILE = '/workspaces/vistas/mockup.html'

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. Remove 3 buttons from grid: Producción, Muestrario, Clientes
# ============================================================
content = content.replace('''                        <button id="repBtnProduccion" class="rep-modulo-card" type="button">
                            <span class="rep-modulo-ico">🏭</span>
                            <span class="rep-modulo-name">PRODUCCIÓN</span>
                            <span class="rep-modulo-desc">Estado de producción de todas las órdenes</span>
                        </button>
''', '', 1)

content = content.replace('''                        <button id="repBtnMuestrario" class="rep-modulo-card" type="button">
                            <span class="rep-modulo-ico">📋</span>
                            <span class="rep-modulo-name">MUESTRARIO</span>
                            <span class="rep-modulo-desc">Productos vinculados a muestras</span>
                        </button>
''', '', 1)

content = content.replace('''                        <button id="repBtnClientes" class="rep-modulo-card" type="button">
                            <span class="rep-modulo-ico">👥</span>
                            <span class="rep-modulo-name">CLIENTES</span>
                            <span class="rep-modulo-desc">Directorio completo de clientes</span>
                        </button>
''', '', 1)

# Also change grid from 4 columns to 3 (now 12 modules fits better in 3 cols)
content = content.replace(
    'grid-template-columns:repeat(4,1fr);gap:10px;padding:12px 24px;max-width:980px;',
    'grid-template-columns:repeat(3,1fr);gap:12px;padding:14px 30px;max-width:900px;',
    1
)

# ============================================================
# 2. Redesign Historial Cliente - open with search bar, no prompt
# ============================================================
# Replace the generarReporteHistorialCliente function
old_historial = '''    const generarReporteHistorialCliente = () => {
        const clienteFilter = String(document.getElementById('repFiltroCliente')?.value || '').trim().toLowerCase();
        if (!clienteFilter) {
            const clienteNombre = prompt('NOMBRE DEL CLIENTE PARA CONSULTAR HISTORIAL:');
            if (!clienteNombre) return;
            const el = document.getElementById('repFiltroCliente');
            if (el) el.value = clienteNombre;
        }
        const term = String(document.getElementById('repFiltroCliente')?.value || '').trim().toLowerCase();
        if (!term) return;
        const { since, until } = getRepFiltroDates();
        loadMisPedidos();
        const rows = misPedidosData.filter((r) => {
            const dt = new Date(`${r.fechaEmitida || ''}T00:00:00`);
            if (!Number.isNaN(dt.getTime()) && (dt < since || dt > until)) return false;
            return String(r.cliente || r.clienteNombre || '').toLowerCase().includes(term);
        });
        const head = document.getElementById('repReporteHead');
        const body = document.getElementById('repReporteBody');
        if (head) head.innerHTML = '<tr><th>FECHA</th><th>ORDEN</th><th>TOTAL</th><th>PAGADO</th><th>ADEUDO</th><th>ESTADO</th></tr>';
        const totalCompras = rows.reduce((a, r) => a + Number(r.total || 0), 0);
        const resumen = document.getElementById('repVistaResumen');
        if (resumen) resumen.innerHTML = `<span class="rep-chip">REGISTROS: ${rows.length}</span><span class="rep-chip">TOTAL COMPRAS: ${formatMoney(totalCompras)}</span>`;
        if (body) {
            if (!rows.length) { body.innerHTML = '<tr><td colspan="6" class="clientesmod-empty">SIN ORDENES PARA ESTE CLIENTE</td></tr>'; return; }
            body.innerHTML = rows.map((r) => `<tr><td>${escCliMod(r.fechaEmitida||'')}</td><td>${escCliMod(r.id||'')}</td><td>${formatMoney(Number(r.total||0))}</td><td>${formatMoney(Number(r.totalPagado||0))}</td><td>${formatMoney(Number(r.adeudoCliente||0))}</td><td>${escCliMod(r.estatusProduccion || r.estado||'')}</td></tr>`).join('');
        }
    };'''

new_historial = '''    const generarReporteHistorialCliente = () => {
        const term = String(document.getElementById('repFiltroCliente')?.value || '').trim().toLowerCase();
        const head = document.getElementById('repReporteHead');
        const body = document.getElementById('repReporteBody');
        const resumen = document.getElementById('repVistaResumen');
        if (head) head.innerHTML = '<tr><th>FECHA</th><th>ORDEN</th><th>PRODUCTO</th><th>TOTAL</th><th>PAGADO</th><th>ADEUDO</th><th>MÉTODO</th><th>ESTADO</th></tr>';
        if (!term) {
            if (resumen) resumen.innerHTML = '';
            if (body) body.innerHTML = '<tr><td colspan="8" class="clientesmod-empty" style="padding:40px 0;font-size:0.65rem;">🔍 ESCRIBE EL NOMBRE DEL CLIENTE EN EL CAMPO DE ARRIBA Y PRESIONA APLICAR FILTROS</td></tr>';
            return;
        }
        const { since, until } = getRepFiltroDates();
        loadMisPedidos();
        const rows = misPedidosData.filter((r) => {
            const dt = new Date((r.fechaEmitida || '') + 'T00:00:00');
            if (!Number.isNaN(dt.getTime()) && (dt < since || dt > until)) return false;
            return String(r.cliente || r.clienteNombre || '').toLowerCase().includes(term);
        });
        const totalCompras = rows.reduce((a, r) => a + Number(r.total || 0), 0);
        const totalPagado = rows.reduce((a, r) => a + Number(r.totalPagado || 0), 0);
        const totalAdeudo = rows.reduce((a, r) => a + Number(r.adeudoCliente || 0), 0);
        if (resumen) resumen.innerHTML = [
            '<span class="rep-chip">CLIENTE: ' + escCliMod(term.toUpperCase()) + '</span>',
            '<span class="rep-chip">ÓRDENES: ' + rows.length + '</span>',
            '<span class="rep-chip" style="background:#d1fae5;border-color:#10b981;color:#065f46;">TOTAL COMPRAS: ' + formatMoney(totalCompras) + '</span>',
            '<span class="rep-chip" style="background:#dbeafe;border-color:#3b82f6;color:#1e40af;">PAGADO: ' + formatMoney(totalPagado) + '</span>',
            totalAdeudo > 0 ? '<span class="rep-chip" style="background:#fee2e2;border-color:#ef4444;color:#991b1b;">ADEUDO: ' + formatMoney(totalAdeudo) + '</span>' : ''
        ].filter(Boolean).join('');
        if (body) {
            if (!rows.length) { body.innerHTML = '<tr><td colspan="8" class="clientesmod-empty">SIN ÓRDENES PARA ESTE CLIENTE</td></tr>'; return; }
            body.innerHTML = rows.map((r) => {
                const prod = Array.isArray(r.lineas) && r.lineas.length ? r.lineas.map(l => l.producto).join(', ') : (r.producto || '--');
                return '<tr><td>' + escCliMod(r.fechaEmitida||'') + '</td><td>' + escCliMod(r.id||r.folio||'') + '</td><td style="max-width:180px;overflow:hidden;text-overflow:ellipsis;">' + escCliMod(prod) + '</td><td>' + formatMoney(Number(r.total||0)) + '</td><td>' + formatMoney(Number(r.totalPagado||0)) + '</td><td>' + formatMoney(Number(r.adeudoCliente||0)) + '</td><td>' + escCliMod(r.metodoPago||'--') + '</td><td>' + escCliMod(r.estatusProduccion||r.estado||'') + '</td></tr>';
            }).join('');
        }
    };'''
content = content.replace(old_historial, new_historial, 1)

# ============================================================
# 3. Remove references in event listeners
# ============================================================
# Remove the addEventListener lines for removed reports
content = content.replace(
    "    if (repBtnProduccion) repBtnProduccion.addEventListener('click', () => abrirReporteVista('REPORTE DE PRODUCCIÓN', generarReporteProduccion));\n",
    '', 1
)
content = content.replace(
    "    if (repBtnMuestrario) repBtnMuestrario.addEventListener('click', () => abrirReporteVista('REPORTE DE MUESTRARIO', generarReporteMuestrario));\n",
    '', 1
)
content = content.replace(
    "    if (repBtnClientes) repBtnClientes.addEventListener('click', () => abrirReporteVista('DIRECTORIO DE CLIENTES', generarReporteClientes));\n",
    '', 1
)

# Remove variable declarations
content = content.replace(
    "    const repBtnProduccion = document.getElementById('repBtnProduccion');\n",
    '', 1
)
content = content.replace(
    "    const repBtnMuestrario = document.getElementById('repBtnMuestrario');\n",
    '', 1
)
content = content.replace(
    "    const repBtnClientes = document.getElementById('repBtnClientes');\n",
    '', 1
)

# ============================================================
# 4. Remove from filtro aplicar map
# ============================================================
content = content.replace(
    "            'REPORTE DE PRODUCCIÓN': generarReporteProduccion,\n",
    '', 1
)
content = content.replace(
    "            'REPORTE DE MUESTRARIO': generarReporteMuestrario,\n",
    '', 1
)
content = content.replace(
    "            'DIRECTORIO DE CLIENTES': generarReporteClientes,\n",
    '', 1
)

# ============================================================
# 5. Clean up abrirReporteVista - remove PRODUCCIÓN from estado filter and noDate list
# ============================================================
content = content.replace(
    "if (estWrap) estWrap.style.display = ['REPORTE DE VENTAS', 'REPORTE DE PRODUCCIÓN'].includes(titulo) ? '' : 'none';",
    "if (estWrap) estWrap.style.display = titulo === 'REPORTE DE VENTAS' ? '' : 'none';",
    1
)
content = content.replace(
    "const noDateReports = ['DIRECTORIO DE CLIENTES', 'INVENTARIO ALMACÉN', 'REPORTE DE INSUMOS', 'DIRECTORIO PROVEEDORES', 'REPORTE DE MUESTRARIO'];",
    "const noDateReports = ['INVENTARIO ALMACÉN', 'REPORTE DE INSUMOS', 'DIRECTORIO PROVEEDORES'];",
    1
)

# ============================================================
# 6. Remove KPIs de producción from dashboard (they duplicate producción module)  
# ============================================================
# Remove the production KPI row from HTML
old_prod_kpis_html = '''
                <!-- KPIs de producción -->
                <div style="display:grid;grid-template-columns:repeat(5,minmax(120px,1fr));gap:8px;margin-top:8px;">
                    <div class="caja-kpi" style="border-left:3px solid #f59e0b;"><b>🏭 EN PRODUCCIÓN</b><span id="repKpiEnProduccion" style="color:#f59e0b;">0</span></div>
                    <div class="caja-kpi" style="border-left:3px solid #10b981;"><b>✅ TERMINADOS</b><span id="repKpiTerminados" style="color:#10b981;">0</span></div>
                    <div class="caja-kpi" style="border-left:3px solid #8b5cf6;"><b>📦 POR ENTREGAR</b><span id="repKpiPorEntregar" style="color:#8b5cf6;">0</span></div>
                    <div class="caja-kpi" style="border-left:3px solid #6b7280;"><b>🚚 ENTREGADOS</b><span id="repKpiEntregados" style="color:#6b7280;">0</span></div>
                    <div class="caja-kpi" style="border-left:3px solid #dc2626;"><b>⚠️ INSUMOS BAJO MÍN</b><span id="repKpiInsumosBajo" style="color:#dc2626;">0</span></div>
                </div>'''
content = content.replace(old_prod_kpis_html, '', 1)

# Remove production KPI JS logic from renderReportesModulo
old_prod_kpis_js = '''        // KPIs de producción
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

'''
content = content.replace(old_prod_kpis_js, '\n', 1)

# ============================================================
# WRITE
# ============================================================
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Patch applied!")
print("  - Removed: Producción, Muestrario, Clientes reports")
print("  - Removed: Production KPIs from dashboard (duplicate)")
print("  - Redesigned: Historial Cliente opens empty with search prompt")
print("  - Grid changed to 3 columns (12 modules)")
