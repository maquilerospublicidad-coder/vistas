#!/usr/bin/env python3
"""Patch correctivo 3:
1. Fix mini calendario (cerrar, números, abrir desde botón Fecha directamente)
2. Quitar el select duplicado de fecha; solo botón 📅
3. Quitar botón 50% del popup de abono en Mis Pedidos
4. Restaurar botones agregar/eliminar producto (con admin guard)
5. Restaurar botones en cotizaciones emitidas
6. Arreglar espaciado barra de filtros
"""
FILE = '/workspaces/vistas/mockup.html'
with open(FILE, 'r', encoding='utf-8') as f:
    c = f.read()

original_len = len(c)
ok = []
fail = []

def patch(name, old, new, count=1):
    global c
    n = c.count(old)
    if n == 0:
        fail.append(f'FAIL [{name}]: not found')
        return False
    if count == 1 and n > 1:
        fail.append(f'FAIL [{name}]: found {n} times')
        return False
    c = c.replace(old, new, count)
    ok.append(f'OK [{name}]')
    return True

# ═══════════════════════════════════════════════════════════
# 1. HTML: Reemplazar selector de fecha + calBtn  →  un solo botón 📅
#    + arreglar espaciado de la barra de filtros
# ═══════════════════════════════════════════════════════════
patch('1-fecha-filter-html',
'''        <div class="mispedidos-filters">
            <div class="orden-field" style="flex:2;min-width:180px;">
                <input id="mpFiltroBuscar" type="text" placeholder="🔍  Folio, nombre o teléfono..." aria-label="Buscar por folio, nombre o teléfono" style="margin-top:6px;">
                <!-- Alias hidden inputs kept for JS compatibility -->
                <input id="mpFiltroFolio" type="hidden">
                <input id="mpFiltroNombre" type="hidden">
                <input id="mpFiltroTelefono" type="hidden">
            </div>
            <div class="orden-field">
                <label>Diseñador</label>
                <select id="mpFiltroDisenador">
                    <option value="">Todos</option>
                </select>
            </div>
            <div class="orden-field" style="position:relative;">
                <label>Fecha</label>
                <div style="display:flex;align-items:center;gap:4px;">
                    <select id="mpFiltroFechaRapido">
                        <option value="">Todas</option>
                        <option value="hoy">Hoy</option>
                        <option value="semana">Semana</option>
                        <option value="mes">Mes</option>
                        <option value="ano">Año</option>
                        <option value="90dias">Últimos 90 días</option>
                        <option value="3meses">Últimos 3 meses</option>
                        <option value="rango">Personalizado...</option>
                    </select>
                    <button id="mpFechaCalBtn" type="button" title="Seleccionar rango en calendario"
                        style="padding:5px 8px;background:#fff7ed;border:1px solid #fde8c8;border-radius:6px;cursor:pointer;font-size:0.75rem;color:#92400e;white-space:nowrap;display:none;">📅 <span id="mpFechaCalLabel">Sin rango</span></button>
                </div>
                <!-- Hidden date inputs for compatibility -->
                <input id="mpFiltroFechaDesde" type="hidden">
                <input id="mpFiltroFechaHasta" type="hidden">
                <div id="mpFechaRangoWrap" style="display:none;"></div>
                <div id="mpFechaRangoWrap2" style="display:none;"></div>
            </div>
            <div class="orden-field">
                <label>Estatus de producción</label>
                <select id="mpFiltroEstatus">
                    <option value="">Todos</option>
                </select>
            </div>
            <div class="orden-field"><label>Adeudo mínimo</label><input id="mpFiltroAdeudo" type="number" min="0" step="0.01" placeholder="Min"></div>
            <div class="orden-field"><label> </label><button id="mpLimpiarFiltros" class="orden-btn" type="button">Limpiar</button></div>
        </div>''',
#────────────────────────────────────────
'''        <div class="mispedidos-filters" style="gap:10px;align-items:flex-end;">
            <div class="orden-field" style="flex:2;min-width:180px;">
                <input id="mpFiltroBuscar" type="text" placeholder="🔍  Folio, nombre o teléfono..." aria-label="Buscar por folio, nombre o teléfono">
                <input id="mpFiltroFolio" type="hidden">
                <input id="mpFiltroNombre" type="hidden">
                <input id="mpFiltroTelefono" type="hidden">
            </div>
            <div class="orden-field" style="min-width:130px;">
                <label>Diseñador</label>
                <select id="mpFiltroDisenador">
                    <option value="">Todos</option>
                </select>
            </div>
            <div class="orden-field" style="min-width:130px;">
                <label>Fecha</label>
                <!-- selector oculto, solo para que getMpDateRange() lea su valor -->
                <select id="mpFiltroFechaRapido" style="display:none;" aria-hidden="true">
                    <option value=""></option>
                    <option value="hoy">Hoy</option>
                    <option value="semana">Semana</option>
                    <option value="mes">Mes</option>
                    <option value="ano">Año</option>
                    <option value="90dias">90 días</option>
                    <option value="3meses">3 meses</option>
                    <option value="rango">Rango</option>
                </select>
                <button id="mpFechaCalBtn" type="button"
                    style="width:100%;padding:7px 10px;background:#fff;border:1px solid #d1d5db;border-radius:6px;cursor:pointer;font-size:0.6rem;color:#374151;text-align:left;display:flex;align-items:center;gap:5px;">
                    📅 <span id="mpFechaCalLabel" style="flex:1;color:#9ca3af;">Todas las fechas</span>
                </button>
                <input id="mpFiltroFechaDesde" type="hidden">
                <input id="mpFiltroFechaHasta" type="hidden">
                <div id="mpFechaRangoWrap" style="display:none;"></div>
                <div id="mpFechaRangoWrap2" style="display:none;"></div>
            </div>
            <div class="orden-field" style="min-width:130px;">
                <label>Estatus</label>
                <select id="mpFiltroEstatus">
                    <option value="">Todos</option>
                </select>
            </div>
            <div class="orden-field" style="min-width:90px;">
                <label>Adeudo</label>
                <input id="mpFiltroAdeudo" type="number" min="0" step="0.01" placeholder="Mínimo">
            </div>
            <div class="orden-field" style="min-width:70px;">
                <label>&nbsp;</label>
                <button id="mpLimpiarFiltros" class="orden-btn" type="button">Limpiar</button>
            </div>
        </div>''')

# ═══════════════════════════════════════════════════════════
# 2. HTML: agregar botones + / − sobre la tabla de productos,
#    solo visible para órdenes (id="mpDetProdAcciones")
#    + columna de eliminar en filas (función inline mpDelProdRow)
# ═══════════════════════════════════════════════════════════
patch('2-prod-actions-toolbar',
'''                <!-- Products table -->
                <div style="font-size:0.55rem;font-weight:800;color:#ff9900;margin-bottom:6px;text-transform:uppercase;letter-spacing:0.5px;">Productos Solicitados</div>
                <table style="width:100%;border-collapse:collapse;font-size:0.6rem;">
                    <thead>
                        <tr style="background:#fff7ed;">
                            <th style="padding:8px 10px;text-align:left;border-bottom:2px solid #ff9900;color:#92400e;font-weight:800;font-size:0.55rem;">PRODUCTO</th>
                            <th style="padding:8px 10px;text-align:left;border-bottom:2px solid #ff9900;color:#92400e;font-weight:800;font-size:0.55rem;">MEDIDA</th>
                            <th style="padding:8px 10px;text-align:left;border-bottom:2px solid #ff9900;color:#92400e;font-weight:800;font-size:0.55rem;">MATERIAL</th>
                            <th style="padding:8px 10px;text-align:center;border-bottom:2px solid #ff9900;color:#92400e;font-weight:800;font-size:0.55rem;">CANT.</th>
                            <th style="padding:8px 10px;text-align:right;border-bottom:2px solid #ff9900;color:#92400e;font-weight:800;font-size:0.55rem;">PRECIO</th>
                            <th style="padding:8px 10px;text-align:right;border-bottom:2px solid #ff9900;color:#92400e;font-weight:800;font-size:0.55rem;">IMPORTE</th>
                        </tr>
                    </thead>
                    <tbody id="mpDetProductosBody"></tbody>
                </table>''',
'''                <!-- Products table -->
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">
                    <div style="font-size:0.55rem;font-weight:800;color:#ff9900;text-transform:uppercase;letter-spacing:0.5px;">Productos Solicitados</div>
                    <div id="mpDetProdAcciones" style="display:none;gap:4px;display:none;">
                        <button id="mpDetAgregarProdBtn" type="button"
                            style="padding:3px 9px;font-size:0.52rem;font-weight:800;background:#fff7ed;color:#92400e;border:1px solid #fde8c8;border-radius:5px;cursor:pointer;">＋ Agregar</button>
                        <button id="mpDetEliminarProdBtn" type="button"
                            style="padding:3px 9px;font-size:0.52rem;font-weight:800;background:#fef2f2;color:#dc2626;border:1px solid #fecaca;border-radius:5px;cursor:pointer;">− Eliminar</button>
                    </div>
                </div>
                <table style="width:100%;border-collapse:collapse;font-size:0.6rem;">
                    <thead>
                        <tr style="background:#fff7ed;">
                            <th style="padding:8px 10px;text-align:left;border-bottom:2px solid #ff9900;color:#92400e;font-weight:800;font-size:0.55rem;">PRODUCTO</th>
                            <th style="padding:8px 10px;text-align:left;border-bottom:2px solid #ff9900;color:#92400e;font-weight:800;font-size:0.55rem;">MEDIDA</th>
                            <th style="padding:8px 10px;text-align:left;border-bottom:2px solid #ff9900;color:#92400e;font-weight:800;font-size:0.55rem;">MATERIAL</th>
                            <th style="padding:8px 10px;text-align:center;border-bottom:2px solid #ff9900;color:#92400e;font-weight:800;font-size:0.55rem;">CANT.</th>
                            <th style="padding:8px 10px;text-align:right;border-bottom:2px solid #ff9900;color:#92400e;font-weight:800;font-size:0.55rem;">PRECIO</th>
                            <th style="padding:8px 10px;text-align:right;border-bottom:2px solid #ff9900;color:#92400e;font-weight:800;font-size:0.55rem;">IMPORTE</th>
                        </tr>
                    </thead>
                    <tbody id="mpDetProductosBody"></tbody>
                </table>''')

# ═══════════════════════════════════════════════════════════
# 3. HTML: hacer visible los botones de acción secundaria
#    para cotizaciones también (solo ocultar abono sección)
#    Mover los botones a DENTRO del popup, fuera del condicional
# ═══════════════════════════════════════════════════════════
# Los botones ya están en #mpDetAccionesSecundarias – solo necesitamos
# que el JS no los oculte para cotizaciones.
# (cambio JS en step 5)

# ═══════════════════════════════════════════════════════════
# 4. CSS: mp-cal-month — asegurar que los números sean visibles
#    y ajustar tamaños del grid
# ═══════════════════════════════════════════════════════════
patch('4-cal-css',
'''        /* ── Mini calendario ── */
        .mp-cal-quick {
            padding: 4px 10px;
            background: #f3f4f6;
            border: 1px solid #e5e7eb;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.55rem;
            font-weight: 700;
            color: #374151;
            transition: background 0.15s;
        }
        .mp-cal-quick:hover, .mp-cal-quick.active { background: #fff7ed; color: #92400e; border-color: #fde8c8; }
        .mp-cal-month { font-size: 0.56rem; min-width: 230px; }
        .mp-cal-month .cal-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; font-weight:800; color:#1f2937; font-size:0.6rem; }
        .mp-cal-month .cal-header button { background:none; border:none; cursor:pointer; font-size:0.85rem; color:#6b7280; padding:2px 6px; }
        .mp-cal-month .cal-grid { display:grid; grid-template-columns:repeat(7, 1fr); gap:1px; }
        .mp-cal-month .cal-dow { text-align:center; font-weight:700; color:#9ca3af; font-size:0.48rem; padding:3px 0; }
        .mp-cal-month .cal-day { text-align:center; padding:5px 2px; border-radius:4px; cursor:pointer; transition:all 0.1s; }
        .mp-cal-month .cal-day:hover { background:#fff7ed; color:#92400e; }
        .mp-cal-month .cal-day.today { font-weight:900; color:#ff9900; }
        .mp-cal-month .cal-day.in-range { background:#fff7ed; }
        .mp-cal-month .cal-day.range-start, .mp-cal-month .cal-day.range-end { background:#ff9900; color:#fff; border-radius:50%; font-weight:900; }
        .mp-cal-month .cal-day.other-month { color:#d1d5db; }
        .mp-cal-month .cal-day.empty { cursor:default; }''',
'''        /* ── Mini calendario ── */
        .mp-cal-quick {
            padding: 5px 12px;
            background: #f3f4f6;
            border: 1px solid #e5e7eb;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.6rem;
            font-weight: 700;
            color: #374151;
            transition: background 0.15s;
            white-space: nowrap;
        }
        .mp-cal-quick:hover, .mp-cal-quick.active { background: #fff7ed; color: #92400e; border-color: #fde8c8; }
        .mp-cal-month { font-size: 0.72rem; min-width: 220px; }
        .mp-cal-month .cal-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; font-weight:800; color:#1f2937; font-size:0.72rem; }
        .mp-cal-month .cal-header button { background:none; border:none; cursor:pointer; font-size:1rem; color:#6b7280; padding:2px 8px; line-height:1; }
        .mp-cal-month .cal-header button:hover { color:#ff9900; }
        .mp-cal-month .cal-grid { display:grid; grid-template-columns:repeat(7, 1fr); gap:2px; }
        .mp-cal-month .cal-dow { text-align:center; font-weight:800; color:#9ca3af; font-size:0.58rem; padding:4px 0; }
        .mp-cal-month .cal-day { text-align:center; padding:6px 3px; border-radius:5px; cursor:pointer; transition:all 0.1s; font-size:0.7rem; color:#374151; line-height:1.2; }
        .mp-cal-month .cal-day:hover { background:#fff7ed; color:#92400e; }
        .mp-cal-month .cal-day.today { font-weight:900; color:#ff9900; }
        .mp-cal-month .cal-day.in-range { background:#fff7ed; color:#92400e; }
        .mp-cal-month .cal-day.range-start, .mp-cal-month .cal-day.range-end { background:#ff9900; color:#fff; border-radius:50%; font-weight:900; }
        .mp-cal-month .cal-day.other-month { color:#d1d5db; }
        .mp-cal-month .cal-day.empty { cursor:default; pointer-events:none; }''')

# ═══════════════════════════════════════════════════════════
# 5. JS: openDetalleOrdenPopup — mostrar botones de producto
#    para órdenes, y NO ocultar acciones secundarias para cotizaciones
# ═══════════════════════════════════════════════════════════
patch('5-opendet-fix',
'''        // Ocultar acciones secundarias para cotizaciones
        const accionesSec = elF('mpDetAccionesSecundarias');
        if (accionesSec) accionesSec.style.display = esCotizacion ? 'none' : '';
        // Reiniciar estado de botones de pago
        document.querySelectorAll('#mpDetPayGrid .orden-pay-btn').forEach(b => b.classList.remove('active'));''',
'''        // Acciones secundarias: siempre visibles (historial, WA, PDF, estatus)
        const accionesSec = elF('mpDetAccionesSecundarias');
        if (accionesSec) accionesSec.style.display = '';
        // Botones de producto: solo para órdenes (no cotizaciones)
        const prodAcciones = elF('mpDetProdAcciones');
        if (prodAcciones) prodAcciones.style.display = esCotizacion ? 'none' : 'flex';
        // Reiniciar estado de botones de pago
        document.querySelectorAll('#mpDetPayGrid .orden-pay-btn').forEach(b => b.classList.remove('active'));''')

# ═══════════════════════════════════════════════════════════
# 6. JS: botones de producto agregar/eliminar (admin guard)
#    Se colocan justo después del cierre del popup de detalle
# ═══════════════════════════════════════════════════════════
patch('6-prod-mgmt-js',
'''    const closeDetalleOrdenPopup = () => {
        if (!popupDetalleOrden) return;
        popupDetalleOrden.style.display = 'none';
        popupDetalleOrden.setAttribute('aria-hidden', 'true');
        mpDetOrdenActual = null;
    };

    // Detalle buttons
    document.getElementById('mpDetCerrar')?.addEventListener('click', closeDetalleOrdenPopup);''',
'''    const closeDetalleOrdenPopup = () => {
        if (!popupDetalleOrden) return;
        popupDetalleOrden.style.display = 'none';
        popupDetalleOrden.setAttribute('aria-hidden', 'true');
        mpDetOrdenActual = null;
        mpDetAdminGranted = false;
    };

    // ── Admin guard + product management ─────────────────────
    let mpDetAdminGranted = false;

    const mpRequireAdmin = (callback) => {
        const role = (localStorage.getItem('logged_user_role') || '').toLowerCase().trim();
        if (role === 'admin' || mpDetAdminGranted) { callback(); return; }
        const pass = prompt('Acción de administrador.\\nIngresa la contraseña de admin:');
        if (!pass) return;
        let usuarios = [];
        try { usuarios = JSON.parse(localStorage.getItem('mock_usuarios_v1') || '[]'); } catch(_){}
        const found = usuarios.find(u => (u.rol === 'admin' || u.role === 'admin') && u.password === pass);
        if (!found) { notifyError('Contraseña incorrecta.', 'Admin'); return; }
        mpDetAdminGranted = true;
        notifyInfo('Acceso de administrador concedido para esta orden.', 'Admin');
        callback();
    };

    const mpRefreshProductos = () => {
        if (!mpDetOrdenActual) return;
        const esc = (v) => String(v ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
        const fm = (n) => `$${Number(n||0).toFixed(2)}`;
        const lineas = Array.isArray(mpDetOrdenActual.lineas) ? mpDetOrdenActual.lineas : [];
        const tbody = document.getElementById('mpDetProductosBody');
        if (!tbody) return;
        if (!lineas.length) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;color:#9ca3af;padding:12px;">Sin productos registrados</td></tr>';
        } else {
            tbody.innerHTML = lineas.map((l, i) => {
                const importe = Number(l.precio||0) * Number(l.cantidad||1);
                return `<tr style="border-bottom:1px solid #f0f0f0;">
                    <td style="padding:7px 10px;font-weight:600;">${esc(l.producto)}</td>
                    <td style="padding:7px 10px;">${esc(l.medida)}</td>
                    <td style="padding:7px 10px;">${esc(l.material)}</td>
                    <td style="padding:7px 10px;text-align:center;">${l.cantidad||1}</td>
                    <td style="padding:7px 10px;text-align:right;">${fm(l.precio)}</td>
                    <td style="padding:7px 10px;text-align:right;font-weight:700;color:#92400e;">${fm(importe)}</td>
                </tr>`;
            }).join('');
        }
        // Recalcular totales
        const sub = lineas.reduce((s, l) => s + Number(l.precio||0)*Number(l.cantidad||1), 0);
        mpDetOrdenActual.subtotal = sub;
        mpDetOrdenActual.total = sub + Number(mpDetOrdenActual.impuestos||0) - Number(mpDetOrdenActual.descuento||0);
        mpDetOrdenActual.adeudoCliente = Math.max(0, mpDetOrdenActual.total - Number(mpDetOrdenActual.anticipo||0));
        mpDetOrdenActual.ganancia = mpDetOrdenActual.total - Number(mpDetOrdenActual.inversion||0);
        const idx = misPedidosData.findIndex(r => r.id === mpDetOrdenActual.id);
        if (idx >= 0) misPedidosData[idx] = { ...mpDetOrdenActual };
        saveMisPedidos();
        // Actualizar totales en pantalla
        const fm2 = (n) => `$${Number(n||0).toFixed(2)}`;
        const el2 = (id) => document.getElementById(id);
        if (el2('mpDetSubtotal')) el2('mpDetSubtotal').textContent = fm2(mpDetOrdenActual.subtotal);
        if (el2('mpDetTotal'))    el2('mpDetTotal').textContent    = fm2(mpDetOrdenActual.total);
        if (el2('mpDetAdeudo'))   el2('mpDetAdeudo').textContent   = fm2(mpDetOrdenActual.adeudoCliente);
        if (el2('mpDetGanancia')) el2('mpDetGanancia').textContent = fm2(mpDetOrdenActual.ganancia);
        renderMisPedidos();
    };

    document.getElementById('mpDetAgregarProdBtn')?.addEventListener('click', () => {
        if (!mpDetOrdenActual) return;
        mpRequireAdmin(() => {
            const nombre = prompt('Nombre del producto / servicio:');
            if (!nombre) return;
            const cant = Math.max(1, parseInt(prompt('Cantidad:', '1') || '1') || 1);
            const precio = Math.max(0, parseFloat(prompt('Precio unitario ($):', '0') || '0') || 0);
            if (!Array.isArray(mpDetOrdenActual.lineas)) mpDetOrdenActual.lineas = [];
            mpDetOrdenActual.lineas.push({ producto: nombre.trim(), medida: '', material: '', cantidad: cant, precio });
            mpRefreshProductos();
        });
    });

    document.getElementById('mpDetEliminarProdBtn')?.addEventListener('click', () => {
        if (!mpDetOrdenActual) return;
        const lineas = Array.isArray(mpDetOrdenActual.lineas) ? mpDetOrdenActual.lineas : [];
        if (!lineas.length) { notifyError('Esta orden no tiene productos.', 'Productos'); return; }
        mpRequireAdmin(() => {
            const lista = lineas.map((l, i) => `${i+1}. ${l.producto} (x${l.cantidad})`).join('\\n');
            const sel = prompt(`¿Qué línea eliminar?\\n${lista}\\n\\nEscribe el número:`);
            if (!sel) return;
            const i = parseInt(sel) - 1;
            if (isNaN(i) || i < 0 || i >= lineas.length) { notifyError('Número inválido.', 'Productos'); return; }
            mpDetOrdenActual.lineas.splice(i, 1);
            mpRefreshProductos();
        });
    });

    // Detalle buttons
    document.getElementById('mpDetCerrar')?.addEventListener('click', closeDetalleOrdenPopup);''')

# ═══════════════════════════════════════════════════════════
# 7. JS: Quitar botón CALCULAR 50% del renderMpPagoPopup
# ═══════════════════════════════════════════════════════════
patch('7-remove-50pct',
'''            const calc50Btn = `<button id="mpPagoCalc50" class="orden-btn" type="button">CALCULAR 50%</button>`;

            if (method === 'EFECTIVO' || method === 'TARJETA') {
                mpPagoTituloEl.textContent = method === 'EFECTIVO' ? 'PAGO EN EFECTIVO' : 'PAGO CON TARJETA';
                mpPagoBodyEl.innerHTML = `
                    <div class="orden-field full"><label>Restante de la orden</label><input type="text" value="${prodEscape(adeudoTxt)}" readonly></div>
                    <div class="orden-field full"><label for="mpPagoCantidad">Cantidad a abonar</label><input id="mpPagoCantidad" type="number" min="0" step="0.01" placeholder="0.00"></div>
                    <div class="orden-field full">${calc50Btn}</div>`;
                const inp = document.getElementById('mpPagoCantidad');
                document.getElementById('mpPagoCalc50')?.addEventListener('click', () => { if (inp) inp.value = (adeudo * 0.5).toFixed(2); });
                mpPagoAceptarEl.onclick = () => {
                    if (registrarAbono(Math.max(0, Number(inp?.value || 0)), method, {})) closeMpPago();
                };
            } else if (method === 'TRANSFERENCIA') {
                mpPagoTituloEl.textContent = 'PAGO POR TRANSFERENCIA';
                mpPagoBodyEl.innerHTML = `
                    <div class="orden-field"><label for="mpPagoBancoEmisor">Banco emisor</label><input id="mpPagoBancoEmisor" type="text" placeholder="Banco del cliente"></div>
                    <div class="orden-field"><label for="mpPagoBancoReceptor">Banco receptor</label><input id="mpPagoBancoReceptor" type="text" value="${prodEscape(bancoReceptor)}" readonly></div>
                    <div class="orden-field"><label for="mpPagoReferencia">No. de referencia (opcional)</label><input id="mpPagoReferencia" type="text" placeholder="Referencia"></div>
                    <div class="orden-field full"><label for="mpPagoCuentaBenef">Cuenta beneficiario</label><select id="mpPagoCuentaBenef">${cuentasOpts}</select></div>
                    <div class="orden-field full"><label for="mpPagoCantidad">Cantidad</label><input id="mpPagoCantidad" type="number" min="0" step="0.01" placeholder="0.00"></div>
                    <div class="orden-field full">${calc50Btn}</div>`;
                const inp = document.getElementById('mpPagoCantidad');
                document.getElementById('mpPagoCalc50')?.addEventListener('click', () => { if (inp) inp.value = (adeudo * 0.5).toFixed(2); });
                mpPagoAceptarEl.onclick = () => {
                    if (registrarAbono(Math.max(0, Number(inp?.value || 0)), method, {
                        bancoEmisor: document.getElementById('mpPagoBancoEmisor')?.value || '',
                        bancoReceptor,
                        referencia: document.getElementById('mpPagoReferencia')?.value || '',
                        cuentaBeneficiario: document.getElementById('mpPagoCuentaBenef')?.value || ''
                    })) closeMpPago();
                };
            } else if (method === 'DEPOSITO') {
                mpPagoTituloEl.textContent = 'PAGO POR DEPÓSITO';
                mpPagoBodyEl.innerHTML = `
                    <div class="orden-field full"><label for="mpPagoProcedencia">Origen de procedencia</label>
                        <select id="mpPagoProcedencia"><option>OXXO</option><option>7-Eleven</option><option>Farmacias del Ahorro</option><option>Walmart</option><option>Chedraui</option><option>Bodega Aurrera</option></select></div>
                    <div class="orden-field"><label for="mpPagoBancoReceptor">Banco receptor</label><input id="mpPagoBancoReceptor" type="text" value="${prodEscape(bancoReceptor)}" readonly></div>
                    <div class="orden-field full"><label for="mpPagoCuentaBenef">Cuenta beneficiario</label><select id="mpPagoCuentaBenef">${cuentasOpts}</select></div>
                    <div class="orden-field full"><label for="mpPagoCantidad">Cantidad</label><input id="mpPagoCantidad" type="number" min="0" step="0.01" placeholder="0.00"></div>
                    <div class="orden-field full">${calc50Btn}</div>`;
                const inp = document.getElementById('mpPagoCantidad');
                document.getElementById('mpPagoCalc50')?.addEventListener('click', () => { if (inp) inp.value = (adeudo * 0.5).toFixed(2); });
                mpPagoAceptarEl.onclick = () => {
                    if (registrarAbono(Math.max(0, Number(inp?.value || 0)), method, {
                        procedencia: document.getElementById('mpPagoProcedencia')?.value || '',
                        bancoReceptor,
                        cuentaBeneficiario: document.getElementById('mpPagoCuentaBenef')?.value || ''
                    })) closeMpPago();
                };
            }''',
'''            if (method === 'EFECTIVO' || method === 'TARJETA') {
                mpPagoTituloEl.textContent = method === 'EFECTIVO' ? 'PAGO EN EFECTIVO' : 'PAGO CON TARJETA';
                mpPagoBodyEl.innerHTML = `
                    <div class="orden-field full"><label>Restante de la orden</label><input type="text" value="${prodEscape(adeudoTxt)}" readonly></div>
                    <div class="orden-field full"><label for="mpPagoCantidad">Cantidad a abonar</label><input id="mpPagoCantidad" type="number" min="0" step="0.01" placeholder="0.00" style="font-size:1rem;font-weight:700;"></div>`;
                const inp = document.getElementById('mpPagoCantidad');
                mpPagoAceptarEl.onclick = () => {
                    if (registrarAbono(Math.max(0, Number(inp?.value || 0)), method, {})) closeMpPago();
                };
            } else if (method === 'TRANSFERENCIA') {
                mpPagoTituloEl.textContent = 'PAGO POR TRANSFERENCIA';
                mpPagoBodyEl.innerHTML = `
                    <div class="orden-field"><label for="mpPagoBancoEmisor">Banco emisor</label><input id="mpPagoBancoEmisor" type="text" placeholder="Banco del cliente"></div>
                    <div class="orden-field"><label for="mpPagoBancoReceptor">Banco receptor</label><input id="mpPagoBancoReceptor" type="text" value="${prodEscape(bancoReceptor)}" readonly></div>
                    <div class="orden-field"><label for="mpPagoReferencia">No. de referencia (opcional)</label><input id="mpPagoReferencia" type="text" placeholder="Referencia"></div>
                    <div class="orden-field full"><label for="mpPagoCuentaBenef">Cuenta beneficiario</label><select id="mpPagoCuentaBenef">${cuentasOpts}</select></div>
                    <div class="orden-field full"><label for="mpPagoCantidad">Cantidad</label><input id="mpPagoCantidad" type="number" min="0" step="0.01" placeholder="0.00" style="font-size:1rem;font-weight:700;"></div>`;
                const inp = document.getElementById('mpPagoCantidad');
                mpPagoAceptarEl.onclick = () => {
                    if (registrarAbono(Math.max(0, Number(inp?.value || 0)), method, {
                        bancoEmisor: document.getElementById('mpPagoBancoEmisor')?.value || '',
                        bancoReceptor,
                        referencia: document.getElementById('mpPagoReferencia')?.value || '',
                        cuentaBeneficiario: document.getElementById('mpPagoCuentaBenef')?.value || ''
                    })) closeMpPago();
                };
            } else if (method === 'DEPOSITO') {
                mpPagoTituloEl.textContent = 'PAGO POR DEPÓSITO';
                mpPagoBodyEl.innerHTML = `
                    <div class="orden-field full"><label for="mpPagoProcedencia">Origen de procedencia</label>
                        <select id="mpPagoProcedencia"><option>OXXO</option><option>7-Eleven</option><option>Farmacias del Ahorro</option><option>Walmart</option><option>Chedraui</option><option>Bodega Aurrera</option></select></div>
                    <div class="orden-field"><label for="mpPagoBancoReceptor">Banco receptor</label><input id="mpPagoBancoReceptor" type="text" value="${prodEscape(bancoReceptor)}" readonly></div>
                    <div class="orden-field full"><label for="mpPagoCuentaBenef">Cuenta beneficiario</label><select id="mpPagoCuentaBenef">${cuentasOpts}</select></div>
                    <div class="orden-field full"><label for="mpPagoCantidad">Cantidad</label><input id="mpPagoCantidad" type="number" min="0" step="0.01" placeholder="0.00" style="font-size:1rem;font-weight:700;"></div>`;
                const inp = document.getElementById('mpPagoCantidad');
                mpPagoAceptarEl.onclick = () => {
                    if (registrarAbono(Math.max(0, Number(inp?.value || 0)), method, {
                        procedencia: document.getElementById('mpPagoProcedencia')?.value || '',
                        bancoReceptor,
                        cuentaBeneficiario: document.getElementById('mpPagoCuentaBenef')?.value || ''
                    })) closeMpPago();
                };
            }''')

# ═══════════════════════════════════════════════════════════
# 8. JS: Arreglar el calendario — quitar DOMContentLoaded wrapper,
#    arreglar openMpCalPopup (posicionar desde el botón fecha visible),
#    arreglar close con escape, eliminar el handler change del select fecha
# ═══════════════════════════════════════════════════════════
patch('8-cal-js-fix',
'''    if (mpFiltroFechaRapido) {
        mpFiltroFechaRapido.addEventListener('change', () => {
            const isRango = mpFiltroFechaRapido.value === 'rango';
            const calBtn = document.getElementById('mpFechaCalBtn');
            if (calBtn) calBtn.style.display = isRango ? '' : 'none';
            if (isRango) { openMpCalPopup(); }
            renderMisPedidos();
        });
    }

    // ── Mini calendario ──────────────────────────────────────
    let mpCalRangeStart = null, mpCalRangeEnd = null;
    let mpCal1Month, mpCal1Year, mpCal2Month, mpCal2Year;

    const openMpCalPopup = () => {
        const popup = document.getElementById('mpCalPopup');
        const btn = document.getElementById('mpFechaCalBtn');
        if (!popup || !btn) return;
        const now = new Date();
        mpCal1Month = now.getMonth() - 1 < 0 ? 11 : now.getMonth() - 1;
        mpCal1Year = now.getMonth() - 1 < 0 ? now.getFullYear() - 1 : now.getFullYear();
        mpCal2Month = now.getMonth();
        mpCal2Year = now.getFullYear();
        renderMpCalMonths();
        // Position near the button
        const rect = btn.getBoundingClientRect();
        popup.style.display = 'block';
        popup.style.top = (rect.bottom + 6) + 'px';
        popup.style.left = Math.max(4, rect.left - 200) + 'px';
    };

    const closeMpCalPopup = () => {
        const popup = document.getElementById('mpCalPopup');
        if (popup) popup.style.display = 'none';
    };

    const renderMpCalMonths = () => {
        renderMpCalMonth(document.getElementById('mpCal1'), mpCal1Year, mpCal1Month, 1);
        renderMpCalMonth(document.getElementById('mpCal2'), mpCal2Year, mpCal2Month, 2);
        updateMpCalRangeLabel();
    };

    const renderMpCalMonth = (container, year, month, which) => {
        if (!container) return;
        const MESES = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'];
        const today = new Date(); today.setHours(0,0,0,0);
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const startDow = firstDay.getDay(); // 0=Sun
        let html = `<div class="cal-header">
            <button type="button" onclick="mpCalNavMonth(${which}, -1)">‹</button>
            <span>${MESES[month]} ${year}</span>
            <button type="button" onclick="mpCalNavMonth(${which}, 1)">›</button>
        </div>
        <div class="cal-grid">
            <div class="cal-dow">Do</div><div class="cal-dow">Lu</div><div class="cal-dow">Ma</div><div class="cal-dow">Mi</div><div class="cal-dow">Ju</div><div class="cal-dow">Vi</div><div class="cal-dow">Sá</div>`;
        // empty cells
        for (let i = 0; i < startDow; i++) html += '<div class="cal-day empty"></div>';
        for (let d = 1; d <= lastDay.getDate(); d++) {
            const date = new Date(year, month, d);
            date.setHours(0,0,0,0);
            const isToday = date.getTime() === today.getTime();
            let cls = 'cal-day';
            if (isToday) cls += ' today';
            if (mpCalRangeStart && mpCalRangeEnd) {
                const s = mpCalRangeStart.getTime(), e = mpCalRangeEnd.getTime(), t = date.getTime();
                if (t === s) cls += ' range-start';
                else if (t === e) cls += ' range-end';
                else if (t > s && t < e) cls += ' in-range';
            } else if (mpCalRangeStart && date.getTime() === mpCalRangeStart.getTime()) {
                cls += ' range-start';
            }
            const iso = year + '-' + String(month+1).padStart(2,'0') + '-' + String(d).padStart(2,'0');
            html += `<div class="${cls}" onclick="mpCalPickDay('${iso}')">${d}</div>`;
        }
        html += '</div>';
        container.innerHTML = html;
    };

    window.mpCalNavMonth = (which, delta) => {
        if (which === 1) {
            mpCal1Month += delta;
            if (mpCal1Month > 11) { mpCal1Month = 0; mpCal1Year++; }
            if (mpCal1Month < 0) { mpCal1Month = 11; mpCal1Year--; }
        } else {
            mpCal2Month += delta;
            if (mpCal2Month > 11) { mpCal2Month = 0; mpCal2Year++; }
            if (mpCal2Month < 0) { mpCal2Month = 11; mpCal2Year--; }
        }
        renderMpCalMonths();
    };

    window.mpCalPickDay = (iso) => {
        const d = new Date(iso + 'T00:00:00');
        if (!mpCalRangeStart || (mpCalRangeStart && mpCalRangeEnd)) {
            mpCalRangeStart = d;
            mpCalRangeEnd = null;
        } else {
            if (d < mpCalRangeStart) { mpCalRangeEnd = mpCalRangeStart; mpCalRangeStart = d; }
            else { mpCalRangeEnd = d; }
        }
        renderMpCalMonths();
    };

    const updateMpCalRangeLabel = () => {
        const el = document.getElementById('mpCalRangeLabel');
        if (!el) return;
        if (!mpCalRangeStart) { el.textContent = 'Haz clic en el día de inicio'; return; }
        if (!mpCalRangeEnd) { el.textContent = `Inicio: ${mpCalRangeStart.toLocaleDateString('es-MX')} — Selecciona el día de fin`; return; }
        el.textContent = `Del ${mpCalRangeStart.toLocaleDateString('es-MX')} al ${mpCalRangeEnd.toLocaleDateString('es-MX')}`;
    };

    const applyMpCalRange = () => {
        if (!mpCalRangeStart) return;
        const end = mpCalRangeEnd || mpCalRangeStart;
        const toISO = d => d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') + '-' + String(d.getDate()).padStart(2,'0');
        const desdeEl = document.getElementById('mpFiltroFechaDesde');
        const hastaEl = document.getElementById('mpFiltroFechaHasta');
        if (desdeEl) desdeEl.value = toISO(mpCalRangeStart);
        if (hastaEl) hastaEl.value = toISO(end);
        // Update select to rango and label
        if (mpFiltroFechaRapido) mpFiltroFechaRapido.value = 'rango';
        const calBtn = document.getElementById('mpFechaCalBtn');
        const lbl = document.getElementById('mpFechaCalLabel');
        if (calBtn) calBtn.style.display = '';
        if (lbl) lbl.textContent = toISO(mpCalRangeStart) + ' – ' + toISO(end);
        closeMpCalPopup();
        renderMisPedidos();
    };

    const applyMpCalQuick = (q) => {
        mpCalRangeStart = null; mpCalRangeEnd = null;
        const desdeEl = document.getElementById('mpFiltroFechaDesde');
        const hastaEl = document.getElementById('mpFiltroFechaHasta');
        if (desdeEl) desdeEl.value = '';
        if (hastaEl) hastaEl.value = '';
        if (mpFiltroFechaRapido) mpFiltroFechaRapido.value = q;
        const calBtn = document.getElementById('mpFechaCalBtn');
        if (calBtn) calBtn.style.display = 'none';
        closeMpCalPopup();
        renderMisPedidos();
        // Re-highlight active quick button
        document.querySelectorAll('#mpCalPopup .mp-cal-quick').forEach(b => b.classList.toggle('active', b.dataset.q === q));
    };

    // Cal popup event wiring
    document.addEventListener('DOMContentLoaded', () => {
        document.getElementById('mpCalCerrar')?.addEventListener('click', closeMpCalPopup);
        document.getElementById('mpCalLimpiar')?.addEventListener('click', () => {
            mpCalRangeStart = null; mpCalRangeEnd = null;
            if (mpFiltroFechaRapido) mpFiltroFechaRapido.value = '';
            const calBtn = document.getElementById('mpFechaCalBtn');
            if (calBtn) calBtn.style.display = 'none';
            const desdeEl = document.getElementById('mpFiltroFechaDesde');
            const hastaEl = document.getElementById('mpFiltroFechaHasta');
            if (desdeEl) desdeEl.value = '';
            if (hastaEl) hastaEl.value = '';
            closeMpCalPopup();
            renderMisPedidos();
        });
        document.getElementById('mpCalAceptar')?.addEventListener('click', applyMpCalRange);
        document.getElementById('mpFechaCalBtn')?.addEventListener('click', openMpCalPopup);
        document.querySelectorAll('#mpCalPopup .mp-cal-quick').forEach(btn => {
            btn.addEventListener('click', () => applyMpCalQuick(btn.dataset.q));
        });
        // Close calendar on outside click
        document.addEventListener('click', (ev) => {
            const popup = document.getElementById('mpCalPopup');
            if (!popup || popup.style.display === 'none') return;
            const calBtn = document.getElementById('mpFechaCalBtn');
            const fecSel = document.getElementById('mpFiltroFechaRapido');
            if (!popup.contains(ev.target) && ev.target !== calBtn && ev.target !== fecSel) closeMpCalPopup();
        }, true);
    });''',

# ─── NUEVO BLOQUE ───
'''    // ── Mini calendario ──────────────────────────────────────
    let mpCalRangeStart = null, mpCalRangeEnd = null;
    let mpCal1Month = 0, mpCal1Year = 2024, mpCal2Month = 1, mpCal2Year = 2024;

    const openMpCalPopup = (anchorEl) => {
        const popup = document.getElementById('mpCalPopup');
        if (!popup) return;
        const now = new Date();
        mpCal1Month = now.getMonth() === 0 ? 11 : now.getMonth() - 1;
        mpCal1Year  = now.getMonth() === 0 ? now.getFullYear() - 1 : now.getFullYear();
        mpCal2Month = now.getMonth();
        mpCal2Year  = now.getFullYear();
        renderMpCalMonths();
        // Posicionar debajo del ancla (botón de fecha)
        const anchor = anchorEl || document.getElementById('mpFechaCalBtn');
        if (anchor) {
            const rect = anchor.getBoundingClientRect();
            const popW = 560;
            let left = rect.left;
            if (left + popW > window.innerWidth - 8) left = window.innerWidth - popW - 8;
            if (left < 4) left = 4;
            popup.style.top  = (rect.bottom + 4 + window.scrollY) + 'px';
            popup.style.left = left + 'px';
        } else {
            popup.style.top = '80px';
            popup.style.left = '20px';
        }
        popup.style.display = 'block';
    };

    const closeMpCalPopup = () => {
        const popup = document.getElementById('mpCalPopup');
        if (popup) popup.style.display = 'none';
    };

    const renderMpCalMonths = () => {
        renderMpCalMonth(document.getElementById('mpCal1'), mpCal1Year, mpCal1Month, 1);
        renderMpCalMonth(document.getElementById('mpCal2'), mpCal2Year, mpCal2Month, 2);
        updateMpCalRangeLabel();
    };

    const renderMpCalMonth = (container, year, month, which) => {
        if (!container) return;
        const MESES = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'];
        const today = new Date(); today.setHours(0,0,0,0);
        const firstDay = new Date(year, month, 1);
        const lastDay  = new Date(year, month + 1, 0);
        const startDow = firstDay.getDay();
        let html = `<div class="cal-header">
            <button type="button" onclick="window._mpCalNav(${which},-1)">‹</button>
            <span>${MESES[month]} ${year}</span>
            <button type="button" onclick="window._mpCalNav(${which},1)">›</button>
        </div><div class="cal-grid">
        <div class="cal-dow">Do</div><div class="cal-dow">Lu</div><div class="cal-dow">Ma</div><div class="cal-dow">Mi</div><div class="cal-dow">Ju</div><div class="cal-dow">Vi</div><div class="cal-dow">Sá</div>`;
        for (let i = 0; i < startDow; i++) html += '<div class="cal-day empty"></div>';
        for (let d = 1; d <= lastDay.getDate(); d++) {
            const date = new Date(year, month, d); date.setHours(0,0,0,0);
            let cls = 'cal-day';
            if (date.getTime() === today.getTime()) cls += ' today';
            if (mpCalRangeStart && mpCalRangeEnd) {
                const s = mpCalRangeStart.getTime(), e = mpCalRangeEnd.getTime(), t = date.getTime();
                if (t === s) cls += ' range-start';
                else if (t === e) cls += ' range-end';
                else if (t > s && t < e) cls += ' in-range';
            } else if (mpCalRangeStart && date.getTime() === mpCalRangeStart.getTime()) {
                cls += ' range-start';
            }
            const iso = year + '-' + String(month+1).padStart(2,'0') + '-' + String(d).padStart(2,'0');
            html += `<div class="${cls}" onclick="window._mpCalPick('${iso}')">${d}</div>`;
        }
        html += '</div>';
        container.innerHTML = html;
    };

    window._mpCalNav = (which, delta) => {
        if (which === 1) {
            mpCal1Month += delta;
            if (mpCal1Month > 11) { mpCal1Month = 0; mpCal1Year++; }
            if (mpCal1Month < 0)  { mpCal1Month = 11; mpCal1Year--; }
        } else {
            mpCal2Month += delta;
            if (mpCal2Month > 11) { mpCal2Month = 0; mpCal2Year++; }
            if (mpCal2Month < 0)  { mpCal2Month = 11; mpCal2Year--; }
        }
        renderMpCalMonths();
    };
    window.mpCalNavMonth = window._mpCalNav; // alias

    window._mpCalPick = (iso) => {
        const d = new Date(iso + 'T00:00:00');
        if (!mpCalRangeStart || (mpCalRangeStart && mpCalRangeEnd)) {
            mpCalRangeStart = d; mpCalRangeEnd = null;
        } else {
            if (d < mpCalRangeStart) { mpCalRangeEnd = mpCalRangeStart; mpCalRangeStart = d; }
            else                     { mpCalRangeEnd = d; }
        }
        renderMpCalMonths();
    };
    window.mpCalPickDay = window._mpCalPick; // alias

    const updateMpCalRangeLabel = () => {
        const el = document.getElementById('mpCalRangeLabel');
        if (!el) return;
        if (!mpCalRangeStart) { el.textContent = 'Haz clic en el día de inicio'; return; }
        if (!mpCalRangeEnd)   { el.textContent = `Inicio: ${mpCalRangeStart.toLocaleDateString('es-MX')} — selecciona fin`; return; }
        el.textContent = `Del ${mpCalRangeStart.toLocaleDateString('es-MX')} al ${mpCalRangeEnd.toLocaleDateString('es-MX')}`;
    };

    const toDateISO = d => d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') + '-' + String(d.getDate()).padStart(2,'0');

    const applyMpCalRange = () => {
        if (!mpCalRangeStart) return;
        const end = mpCalRangeEnd || mpCalRangeStart;
        const desdeEl = document.getElementById('mpFiltroFechaDesde');
        const hastaEl = document.getElementById('mpFiltroFechaHasta');
        if (desdeEl) desdeEl.value = toDateISO(mpCalRangeStart);
        if (hastaEl) hastaEl.value = toDateISO(end);
        if (mpFiltroFechaRapido) mpFiltroFechaRapido.value = 'rango';
        const lbl = document.getElementById('mpFechaCalLabel');
        if (lbl) lbl.textContent = toDateISO(mpCalRangeStart) + ' – ' + toDateISO(end);
        const btn = document.getElementById('mpFechaCalBtn');
        if (btn) { btn.style.background = '#fff7ed'; btn.style.borderColor = '#fde8c8'; btn.style.color = '#92400e'; }
        closeMpCalPopup();
        renderMisPedidos();
    };

    const QUICK_LABELS = { hoy:'Hoy', semana:'Semana', mes:'Mes', ano:'Año', '90dias':'Últimos 90 días', '3meses':'Últimos 3 meses' };

    const applyMpCalQuick = (q) => {
        mpCalRangeStart = null; mpCalRangeEnd = null;
        const desdeEl = document.getElementById('mpFiltroFechaDesde');
        const hastaEl = document.getElementById('mpFiltroFechaHasta');
        if (desdeEl) desdeEl.value = '';
        if (hastaEl) hastaEl.value = '';
        if (mpFiltroFechaRapido) mpFiltroFechaRapido.value = q;
        const lbl = document.getElementById('mpFechaCalLabel');
        if (lbl) lbl.textContent = QUICK_LABELS[q] || q;
        const btn = document.getElementById('mpFechaCalBtn');
        if (btn) { btn.style.background = '#fff7ed'; btn.style.borderColor = '#fde8c8'; btn.style.color = '#92400e'; }
        document.querySelectorAll('#mpCalPopup .mp-cal-quick').forEach(b => b.classList.toggle('active', b.dataset.q === q));
        closeMpCalPopup();
        renderMisPedidos();
    };

    // ── Cal popup — event wiring (directo, sin DOMContentLoaded) ──
    (() => {
        const calPopup   = document.getElementById('mpCalPopup');
        const cerrarBtn  = document.getElementById('mpCalCerrar');
        const limpiarBtn = document.getElementById('mpCalLimpiar');
        const aceptarBtn = document.getElementById('mpCalAceptar');
        const calBtn     = document.getElementById('mpFechaCalBtn');

        if (cerrarBtn)  cerrarBtn.addEventListener('click', closeMpCalPopup);
        if (aceptarBtn) aceptarBtn.addEventListener('click', applyMpCalRange);
        if (calBtn)     calBtn.addEventListener('click', (ev) => { ev.stopPropagation(); openMpCalPopup(calBtn); });

        if (limpiarBtn) limpiarBtn.addEventListener('click', () => {
            mpCalRangeStart = null; mpCalRangeEnd = null;
            if (mpFiltroFechaRapido) mpFiltroFechaRapido.value = '';
            const de = document.getElementById('mpFiltroFechaDesde');
            const ha = document.getElementById('mpFiltroFechaHasta');
            if (de) de.value = ''; if (ha) ha.value = '';
            const lbl = document.getElementById('mpFechaCalLabel');
            if (lbl) lbl.textContent = 'Todas las fechas';
            if (calBtn) { calBtn.style.background = '#fff'; calBtn.style.borderColor = '#d1d5db'; calBtn.style.color = '#374151'; }
            closeMpCalPopup();
            renderMisPedidos();
        });

        document.querySelectorAll('#mpCalPopup .mp-cal-quick').forEach(btn => {
            btn.addEventListener('click', (ev) => { ev.stopPropagation(); applyMpCalQuick(btn.dataset.q); });
        });

        // Cerrar con click fuera del popup
        document.addEventListener('click', (ev) => {
            if (!calPopup || calPopup.style.display === 'none') return;
            if (!calPopup.contains(ev.target) && ev.target !== calBtn) closeMpCalPopup();
        });

        // Cerrar con Escape
        document.addEventListener('keydown', (ev) => {
            if (ev.key === 'Escape') closeMpCalPopup();
        });
    })();''')

# ═══════════════════════════════════════════════════════════
# Guardar
# ═══════════════════════════════════════════════════════════
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(c)

print('\n'.join(ok))
if fail: print('\n'.join(fail))
print(f'\nTotal: {len(ok)} OK, {len(fail)} FAIL')
print(f'Len: {original_len} -> {len(c)} ({len(c)-original_len:+})')
