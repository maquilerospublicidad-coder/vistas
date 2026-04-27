#!/usr/bin/env python3
"""Patch correctivo Mis Pedidos:
1. Elimina botones Nueva Orden / Eliminar selección
2. Quita la etiqueta del buscador (solo placeholder tenue)
3. Botones de pago abren el mismo popup de Nueva Orden  
4. Quita la línea separatoria del panel de abono
"""
import sys

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
# 1. ELIMINAR los botones de tabla HTML (Nueva Orden + Eliminar)
# ═══════════════════════════════════════════════════════════
patch('1-remove-table-btns-html',
'''        <div style="display:flex;justify-content:flex-end;gap:6px;margin-bottom:4px;">
            <button id="mpNuevaOrdenBtn" type="button" style="padding:5px 12px;background:#ff9900;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:0.6rem;font-weight:800;display:none;">＋ Nueva Orden</button>
            <button id="mpEliminarSelBtn" type="button" style="padding:5px 10px;background:#fef2f2;color:#dc2626;border:1px solid #fecaca;border-radius:6px;cursor:pointer;font-size:0.6rem;font-weight:800;display:none;">🗑 Eliminar selección</button>
        </div>
        <div class="mispedidos-table-wrap">''',
'''        <div class="mispedidos-table-wrap">''')

# ═══════════════════════════════════════════════════════════
# 2. BUSCADOR: quitar la etiqueta visible, dejar solo el placeholder
#    El label "Buscar (Folio, Cliente, Teléfono)" se convierte en
#    aria-label para accesibilidad, el placeholder ya es descriptivo
# ═══════════════════════════════════════════════════════════
patch('2-buscador-label',
'''            <div class="orden-field" style="flex:2;min-width:180px;">
                <label>Buscar (Folio, Cliente, Teléfono)</label>
                <input id="mpFiltroBuscar" type="text" placeholder="Folio, nombre o teléfono...">''',
'''            <div class="orden-field" style="flex:2;min-width:180px;">
                <input id="mpFiltroBuscar" type="text" placeholder="🔍  Folio, nombre o teléfono..." aria-label="Buscar por folio, nombre o teléfono" style="margin-top:6px;">''')

# ═══════════════════════════════════════════════════════════
# 3. PANEL ABONO: quitar línea separatoria y mejorar diseño
#    Usar clase orden-btn orden-pay-btn (mismo look que Nueva Orden)
#    Botones en grid de 4 con orden-pagos-grid
#    Al hacer clic → abre #mpPagoPopup (como ordenPagoPopup)
# ═══════════════════════════════════════════════════════════
patch('3-abono-redesign',
'''                <!-- Abono section: método de pago en cuadrícula (ventas only) -->
                <div id="mpDetAbonoWrap" style="margin-top:14px;border-top:2px solid #fde8c8;padding-top:12px;">
                    <div style="font-size:0.55rem;font-weight:800;color:#92400e;margin-bottom:8px;text-transform:uppercase;">Registrar Abono</div>
                    <div id="mpDetPayGrid" style="display:grid;grid-template-columns:1fr 1fr;gap:5px;">
                        <button class="mp-pay-btn" data-pay="EFECTIVO" type="button"><span class="mp-pay-icon">◉</span><span class="mp-pay-lbl">EFECTIVO</span><span class="mp-pay-key">F4</span></button>
                        <button class="mp-pay-btn" data-pay="TARJETA" type="button"><span class="mp-pay-icon">▣</span><span class="mp-pay-lbl">TARJETA</span><span class="mp-pay-key">F5</span></button>
                        <button class="mp-pay-btn" data-pay="TRANSFERENCIA" type="button"><span class="mp-pay-icon">⇄</span><span class="mp-pay-lbl">TRANSFERENCIA</span><span class="mp-pay-key">F6</span></button>
                        <button class="mp-pay-btn" data-pay="DEPOSITO" type="button"><span class="mp-pay-icon">↓</span><span class="mp-pay-lbl">DEPÓSITO</span><span class="mp-pay-key">F7</span></button>
                    </div>
                    <!-- Hidden inputs for backward compat (used in abonarBtn handler) -->
                    <input id="mpDetAbonoMonto" type="hidden" value="">
                    <input id="mpDetAbonoMetodo" type="hidden" value="EFECTIVO">
                    <div id="mpDetAbonoConfirm" style="display:none;margin-top:8px;padding:8px;background:#fff7ed;border-radius:7px;border:1px solid #fde8c8;">
                        <div style="font-size:0.55rem;color:#92400e;font-weight:700;margin-bottom:5px;">Confirmar abono — <span id="mpDetAbonoMetodoLabel"></span></div>
                        <input id="mpDetAbonoMontoInput" type="number" min="0" step="0.01" placeholder="Monto a abonar" style="width:100%;padding:7px 9px;font-size:0.6rem;border:1px solid #fde8c8;border-radius:6px;box-sizing:border-box;margin-bottom:5px;">
                        <div style="display:flex;gap:5px;">
                            <button id="mpDetAbonoCancelar" type="button" style="flex:1;font-size:0.58rem;padding:7px;background:#f3f4f6;color:#374151;border:none;border-radius:6px;cursor:pointer;font-weight:700;">✕ Cancelar</button>
                            <button id="mpDetAbonoBtn" type="button" style="flex:2;font-size:0.58rem;padding:7px;background:#ff9900;color:#fff;border:none;border-radius:6px;cursor:pointer;font-weight:800;">✓ REGISTRAR ABONO</button>
                        </div>
                    </div>
                    <!-- IMPRIMIR debajo de los botones de pago -->
                    <button id="mpDetImprimir" type="button" style="width:100%;font-size:0.6rem;padding:10px;background:#1e3a5f;color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:800;margin-top:8px;">🖨 IMPRIMIR ORDEN</button>
                </div>''',
'''                <!-- Abono section: método de pago (ventas only) -->
                <div id="mpDetAbonoWrap" style="margin-top:12px;">
                    <div style="font-size:0.5rem;font-weight:800;color:#9ca3af;margin-bottom:6px;text-transform:uppercase;letter-spacing:0.5px;">Registrar abono</div>
                    <div id="mpDetPayGrid" class="orden-pagos-grid" style="grid-template-columns:repeat(2,1fr);">
                        <button class="orden-btn orden-pay-btn" data-mp-pay="EFECTIVO" type="button" title="Efectivo"><span class="orden-pay-icon">◉</span><span class="orden-pay-label">EFECTIVO</span><span class="shortcut-hint">F4</span></button>
                        <button class="orden-btn orden-pay-btn" data-mp-pay="TARJETA" type="button" title="Tarjeta"><span class="orden-pay-icon">▣</span><span class="orden-pay-label">TARJETA</span><span class="shortcut-hint">F5</span></button>
                        <button class="orden-btn orden-pay-btn" data-mp-pay="TRANSFERENCIA" type="button" title="Transferencia"><span class="orden-pay-icon">⇄</span><span class="orden-pay-label">TRANSFERENCIA</span><span class="shortcut-hint">F6</span></button>
                        <button class="orden-btn orden-pay-btn" data-mp-pay="DEPOSITO" type="button" title="Depósito"><span class="orden-pay-icon">↓</span><span class="orden-pay-label">DEPÓSITO</span><span class="shortcut-hint">F7</span></button>
                    </div>
                    <input id="mpDetAbonoMonto" type="hidden" value="">
                    <input id="mpDetAbonoMetodo" type="hidden" value="EFECTIVO">
                    <!-- IMPRIMIR debajo de los botones de pago -->
                    <button id="mpDetImprimir" type="button" style="width:100%;font-size:0.6rem;padding:10px;background:#1e3a5f;color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:800;margin-top:8px;">🖨 IMPRIMIR ORDEN</button>
                </div>''')

# ═══════════════════════════════════════════════════════════
# 4. AGREGAR #mpPagoPopup HTML (igual que ordenPagoPopup pero con IDs propios)
#    Va justo después de ordenConfirmPopup en el HTML
# ═══════════════════════════════════════════════════════════
patch('4-add-mpPagoPopup',
'''<div id="ordenConfirmPopup" class="orden-pay-popup" aria-hidden="true">
    <div class="orden-pay-card" role="dialog" aria-modal="true" aria-labelledby="ordenConfirmTitulo">
        <h3 id="ordenConfirmTitulo" style="margin:0;font-size:0.9rem;font-weight:900;color:#111827;">Confirmación</h3>''',
'''<div id="mpPagoPopup" class="orden-pay-popup" aria-hidden="true" style="z-index:100030;">
    <div class="orden-pay-card" role="dialog" aria-modal="true" aria-labelledby="mpPagoTitulo">
        <h3 id="mpPagoTitulo" style="margin:0;font-size:0.9rem;font-weight:900;color:#111827;">REGISTRAR ABONO</h3>
        <div id="mpPagoBody" class="orden-pay-grid"></div>
        <div class="orden-pay-actions">
            <button id="mpPagoCancelar" class="orden-btn" type="button">CANCELAR</button>
            <button id="mpPagoAceptar" class="orden-btn primary" type="button">REGISTRAR</button>
        </div>
    </div>
</div>

<div id="ordenConfirmPopup" class="orden-pay-popup" aria-hidden="true">
    <div class="orden-pay-card" role="dialog" aria-modal="true" aria-labelledby="ordenConfirmTitulo">
        <h3 id="ordenConfirmTitulo" style="margin:0;font-size:0.9rem;font-weight:900;color:#111827;">Confirmación</h3>''')

# ═══════════════════════════════════════════════════════════
# 5a. LIMPIAR openDetalleOrdenPopup: quitar referencias a nvaBtn/delBtn
# ═══════════════════════════════════════════════════════════
patch('5a-clean-opendet',
'''        // Ocultar acciones secundarias para cotizaciones
        const accionesSec = elF('mpDetAccionesSecundarias');
        if (accionesSec) accionesSec.style.display = esCotizacion ? 'none' : '';
        // Reiniciar estado de botones de pago
        document.querySelectorAll('#mpDetPayGrid .mp-pay-btn').forEach(b => b.classList.remove('active'));
        elF('mpDetAbonoConfirm')?.style && (elF('mpDetAbonoConfirm').style.display = 'none');
        // Botones tabla solo para órdenes
        const nvaBtn = document.getElementById('mpNuevaOrdenBtn');
        const delBtn = document.getElementById('mpEliminarSelBtn');
        if (nvaBtn) nvaBtn.style.display = esCotizacion ? 'none' : '';
        if (delBtn) delBtn.style.display = esCotizacion ? 'none' : '';''',
'''        // Ocultar acciones secundarias para cotizaciones
        const accionesSec = elF('mpDetAccionesSecundarias');
        if (accionesSec) accionesSec.style.display = esCotizacion ? 'none' : '';
        // Reiniciar estado de botones de pago
        document.querySelectorAll('#mpDetPayGrid .orden-pay-btn').forEach(b => b.classList.remove('active'));''')

# ═══════════════════════════════════════════════════════════
# 5b. ELIMINAR bloque IIFE de botones de tabla (admin guard)
# ═══════════════════════════════════════════════════════════
patch('5b-remove-admin-iife',
'''    // ── Botones de tabla (Nueva Orden / Eliminar) ─────────────
    (() => {
        const getLoggedRole = () => (localStorage.getItem('logged_user_role') || '').toLowerCase().trim();
        let adminGrantedForOrderId = null; // Una vez concedido el permiso admin, solo para este ID

        const requireAdmin = (ordenId, callback) => {
            const role = getLoggedRole();
            if (role === 'admin') { callback(); return; }
            // Ya concedido para esta orden
            if (adminGrantedForOrderId === ordenId) { callback(); return; }
            // Solicitar contraseña de admin
            const pass = prompt('Esta acción requiere autorización de administrador.\\nIngresa la contraseña de administrador:');
            if (pass === null) return; // Cancelado
            // Verificar contra usuarios configurados
            let usuarios = [];
            try { usuarios = JSON.parse(localStorage.getItem('mock_usuarios_v1') || '[]'); } catch(_){}
            const admin = usuarios.find(u => u.rol === 'admin' && u.password === pass);
            if (!admin) {
                const email = localStorage.getItem('logged_user_email') || '';
                // También verificar por email+pass de Firebase no aplica aquí; solo comprobamos local
                alert('Contraseña incorrecta. Acceso denegado.');
                return;
            }
            // Permiso concedido para esta orden (una sola vez)
            adminGrantedForOrderId = ordenId;
            alert('Acceso de administrador concedido para esta orden. El permiso expirará al cerrar.');
            callback();
        };

        // Botón Nueva Orden en panel detalle: agrega un producto a la orden actual
        document.getElementById('mpNuevaOrdenBtn')?.addEventListener('click', () => {
            if (!mpDetOrdenActual) return;
            requireAdmin(mpDetOrdenActual.id, () => {
                const nombre = prompt('Nombre del producto/servicio:');
                if (!nombre) return;
                const cantStr = prompt('Cantidad:', '1');
                const cantidad = Math.max(1, parseInt(cantStr || '1') || 1);
                const precioStr = prompt('Precio unitario:', '0');
                const precio = Math.max(0, parseFloat(precioStr || '0') || 0);
                const nuevaLinea = {
                    producto: nombre.trim(),
                    medida: '',
                    material: '',
                    cantidad,
                    precio
                };
                if (!Array.isArray(mpDetOrdenActual.lineas)) mpDetOrdenActual.lineas = [];
                mpDetOrdenActual.lineas.push(nuevaLinea);
                // Recalcular totales
                const subtotal = mpDetOrdenActual.lineas.reduce((s, l) => s + Number(l.precio||0)*Number(l.cantidad||1), 0);
                mpDetOrdenActual.subtotal = subtotal;
                mpDetOrdenActual.total = subtotal + Number(mpDetOrdenActual.impuestos||0) - Number(mpDetOrdenActual.descuento||0);
                mpDetOrdenActual.adeudoCliente = Math.max(0, mpDetOrdenActual.total - Number(mpDetOrdenActual.anticipo||0));
                mpDetOrdenActual.ganancia = mpDetOrdenActual.total - Number(mpDetOrdenActual.inversion||0);
                // Guardar
                const idx = misPedidosData.findIndex(r => r.id === mpDetOrdenActual.id);
                if (idx >= 0) misPedidosData[idx] = { ...mpDetOrdenActual };
                saveMisPedidos();
                openDetalleOrdenPopup(mpDetOrdenActual);
                renderMisPedidos();
            });
        });

        // Botón Eliminar selección en panel detalle: elimina líneas seleccionadas
        document.getElementById('mpEliminarSelBtn')?.addEventListener('click', () => {
            if (!mpDetOrdenActual) return;
            requireAdmin(mpDetOrdenActual.id, () => {
                const lineas = Array.isArray(mpDetOrdenActual.lineas) ? mpDetOrdenActual.lineas : [];
                if (!lineas.length) { alert('Esta orden no tiene productos.'); return; }
                const opciones = lineas.map((l, i) => `${i+1}. ${l.producto} (x${l.cantidad})`).join('\\n');
                const sel = prompt(`¿Qué línea eliminar?\\n${opciones}\\n\\nEscribe el número de línea:`);
                if (!sel) return;
                const idx = parseInt(sel) - 1;
                if (isNaN(idx) || idx < 0 || idx >= lineas.length) { alert('Número inválido.'); return; }
                mpDetOrdenActual.lineas.splice(idx, 1);
                // Recalcular
                const subtotal = mpDetOrdenActual.lineas.reduce((s, l) => s + Number(l.precio||0)*Number(l.cantidad||1), 0);
                mpDetOrdenActual.subtotal = subtotal;
                mpDetOrdenActual.total = subtotal + Number(mpDetOrdenActual.impuestos||0) - Number(mpDetOrdenActual.descuento||0);
                mpDetOrdenActual.adeudoCliente = Math.max(0, mpDetOrdenActual.total - Number(mpDetOrdenActual.anticipo||0));
                mpDetOrdenActual.ganancia = mpDetOrdenActual.total - Number(mpDetOrdenActual.inversion||0);
                const dataIdx = misPedidosData.findIndex(r => r.id === mpDetOrdenActual.id);
                if (dataIdx >= 0) misPedidosData[dataIdx] = { ...mpDetOrdenActual };
                saveMisPedidos();
                openDetalleOrdenPopup(mpDetOrdenActual);
                renderMisPedidos();
            });
        });

        // Al cerrar el popup, revocar permisos admin
        document.getElementById('mpDetCerrar')?.addEventListener('click', () => {
            adminGrantedForOrderId = null;
        });
    })();

    // ===== DETALLE ORDEN POPUP =====''',
'''    // ===== DETALLE ORDEN POPUP =====''')

# ═══════════════════════════════════════════════════════════
# 5c. LIMPIAR dblclick: quitar líneas de nvaBtn/delBtn
# ═══════════════════════════════════════════════════════════
patch('5c-clean-dblclick',
'''            if (row) openDetalleOrdenPopup(row);
            // Mostrar botones de tabla solo para venta (no cotización)
            const nvaBtn = document.getElementById('mpNuevaOrdenBtn');
            const delBtn = document.getElementById('mpEliminarSelBtn');
            if (nvaBtn) nvaBtn.style.display = (row && row.tipo !== 'cotizacion') ? '' : 'none';
            if (delBtn) delBtn.style.display = (row && row.tipo !== 'cotizacion') ? '' : 'none';''',
'''            if (row) openDetalleOrdenPopup(row);''')

# ═══════════════════════════════════════════════════════════
# 6. REEMPLAZAR handlers de pay grid con renderMpPagoPopup
# ═══════════════════════════════════════════════════════════
patch('6-pay-handlers',
'''    // ── Pay-grid buttons (abono por método de pago) ──────────
    document.querySelectorAll('#mpDetPayGrid .mp-pay-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            if (!mpDetOrdenActual) return;
            document.querySelectorAll('#mpDetPayGrid .mp-pay-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const metodo = btn.dataset.pay;
            const metodoInput = document.getElementById('mpDetAbonoMetodo');
            if (metodoInput) metodoInput.value = metodo;
            const lbl = document.getElementById('mpDetAbonoMetodoLabel');
            if (lbl) lbl.textContent = metodo;
            const confirmDiv = document.getElementById('mpDetAbonoConfirm');
            if (confirmDiv) {
                confirmDiv.style.display = '';
                document.getElementById('mpDetAbonoMontoInput')?.focus();
            }
        });
    });

    document.getElementById('mpDetAbonoCancelar')?.addEventListener('click', () => {
        document.querySelectorAll('#mpDetPayGrid .mp-pay-btn').forEach(b => b.classList.remove('active'));
        const confirmDiv = document.getElementById('mpDetAbonoConfirm');
        if (confirmDiv) confirmDiv.style.display = 'none';
    });

    document.getElementById('mpDetAbonoBtn')?.addEventListener('click', () => {
        if (!mpDetOrdenActual) return;
        const montoInput = document.getElementById('mpDetAbonoMontoInput');
        const metodoInput = document.getElementById('mpDetAbonoMetodo');
        const monto = Number(montoInput?.value || 0);
        const metodo = metodoInput?.value || 'EFECTIVO';
        if (!monto || monto <= 0) { alert('Ingresa un monto válido.'); return; }
        const adeudo = Number(mpDetOrdenActual.adeudoCliente || 0);
        if (monto > adeudo) { alert(`El monto supera el adeudo de $${adeudo.toFixed(2)}.`); return; }
        const nuevoAnticipo = Number(mpDetOrdenActual.anticipo || 0) + monto;
        const nuevoAdeudo = Math.max(0, Number(mpDetOrdenActual.total || 0) - nuevoAnticipo);
        mpDetOrdenActual.anticipo = nuevoAnticipo;
        mpDetOrdenActual.adeudoCliente = nuevoAdeudo;
        const idx = misPedidosData.findIndex(r => r.id === mpDetOrdenActual.id);
        if (idx >= 0) {
            misPedidosData[idx].anticipo = nuevoAnticipo;
            misPedidosData[idx].adeudoCliente = nuevoAdeudo;
        }
        const movCaja = {
            id: 'CM-' + Date.now().toString(36).toUpperCase(),
            tipo: 'ingreso',
            monto: monto,
            concepto: `Abono Orden ${mpDetOrdenActual.folio} — ${mpDetOrdenActual.clienteNombre}`,
            fecha: todayISO(),
            formaPago: metodo,
            folio: mpDetOrdenActual.folio
        };
        try {
            const cajaMov = JSON.parse(localStorage.getItem('mock_caja_movs_v1') || '[]');
            cajaMov.push(movCaja);
            localStorage.setItem('mock_caja_movs_v1', JSON.stringify(cajaMov));
        } catch (_) {}
        saveMisPedidos();
        document.getElementById('mpDetAnticipo').textContent = `$${nuevoAnticipo.toFixed(2)}`;
        document.getElementById('mpDetAdeudo').textContent = `$${nuevoAdeudo.toFixed(2)}`;
        const abonoWrap = document.getElementById('mpDetAbonoWrap');
        if (nuevoAdeudo <= 0 && abonoWrap) abonoWrap.style.display = 'none';
        // Reset confirm panel
        document.querySelectorAll('#mpDetPayGrid .mp-pay-btn').forEach(b => b.classList.remove('active'));
        const confirmDiv = document.getElementById('mpDetAbonoConfirm');
        if (confirmDiv) confirmDiv.style.display = 'none';
        if (montoInput) montoInput.value = '';
        renderMisPedidos();
        alert(`Abono de $${monto.toFixed(2)} registrado exitosamente.`);
    });''',

'''    // ── Popup de pago para Mis Pedidos (mismo look que Nueva Orden) ──────
    (() => {
        const mpPagoPopupEl  = document.getElementById('mpPagoPopup');
        const mpPagoBodyEl   = document.getElementById('mpPagoBody');
        const mpPagoTituloEl = document.getElementById('mpPagoTitulo');
        const mpPagoAceptarEl = document.getElementById('mpPagoAceptar');
        const mpPagoCancelarEl = document.getElementById('mpPagoCancelar');

        const openMpPago  = () => { if (mpPagoPopupEl) { mpPagoPopupEl.style.display = 'flex'; mpPagoPopupEl.setAttribute('aria-hidden','false'); }};
        const closeMpPago = () => { if (mpPagoPopupEl) { mpPagoPopupEl.style.display = 'none';  mpPagoPopupEl.setAttribute('aria-hidden','true');  }};

        const registrarAbono = (monto, metodo, extras) => {
            if (!mpDetOrdenActual) return;
            const adeudo = Number(mpDetOrdenActual.adeudoCliente || 0);
            if (monto <= 0) { notifyError('Ingresa una cantidad válida.', 'Abono'); return false; }
            if (monto > adeudo + 0.01) { notifyError(`El monto supera el restante de ${formatMoney(adeudo)}.`, 'Abono'); return false; }
            const nuevoAnticipo = Number(mpDetOrdenActual.anticipo || 0) + monto;
            const nuevoAdeudo   = Math.max(0, Number(mpDetOrdenActual.total || 0) - nuevoAnticipo);
            mpDetOrdenActual.anticipo      = nuevoAnticipo;
            mpDetOrdenActual.adeudoCliente = nuevoAdeudo;
            mpDetOrdenActual.metodoPago    = metodo;
            const idx = misPedidosData.findIndex(r => r.id === mpDetOrdenActual.id);
            if (idx >= 0) { misPedidosData[idx].anticipo = nuevoAnticipo; misPedidosData[idx].adeudoCliente = nuevoAdeudo; misPedidosData[idx].metodoPago = metodo; }
            const movCaja = { id: 'CM-' + Date.now().toString(36).toUpperCase(), tipo: 'ingreso', monto, concepto: `Abono Orden ${mpDetOrdenActual.folio} — ${mpDetOrdenActual.clienteNombre}`, fecha: todayISO(), formaPago: metodo, folio: mpDetOrdenActual.folio, ...extras };
            try { const cajaMov = JSON.parse(localStorage.getItem('mock_caja_movs_v1') || '[]'); cajaMov.push(movCaja); localStorage.setItem('mock_caja_movs_v1', JSON.stringify(cajaMov)); } catch (_) {}
            saveMisPedidos();
            document.getElementById('mpDetAnticipo').textContent = formatMoney(nuevoAnticipo);
            document.getElementById('mpDetAdeudo').textContent   = formatMoney(nuevoAdeudo);
            document.getElementById('mpDetMetodoPago').textContent = metodo;
            const abonoWrap = document.getElementById('mpDetAbonoWrap');
            if (nuevoAdeudo <= 0 && abonoWrap) abonoWrap.style.display = 'none';
            document.querySelectorAll('#mpDetPayGrid .orden-pay-btn').forEach(b => b.classList.remove('active'));
            renderMisPedidos();
            notifyInfo(`Abono de ${formatMoney(monto)} registrado.`, 'Abono');
            return true;
        };

        const renderMpPagoPopup = (method) => {
            if (!mpPagoPopupEl || !mpPagoBodyEl || !mpPagoTituloEl) return;
            const adeudo = Number(mpDetOrdenActual?.adeudoCliente || 0);
            const adeudoTxt = formatMoney(adeudo);
            const bancoReceptor = String(getConfigValue('caja', 'bancoReceptor') || 'BBVA México');
            const cuentas = getCuentasBeneficiario?.() || [];
            const cuentasOpts = cuentas.map(c => `<option value="${prodEscape(c)}">${prodEscape(c)}</option>`).join('');
            const calc50Btn = `<button id="mpPagoCalc50" class="orden-btn" type="button">CALCULAR 50%</button>`;

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
            }

            mpPagoCancelarEl.onclick = closeMpPago;
            mpPagoPopupEl.addEventListener('click', (ev) => { if (ev.target === mpPagoPopupEl) closeMpPago(); }, { once: true });
            openMpPago();
            setTimeout(() => document.getElementById('mpPagoCantidad')?.focus(), 50);
        };

        // Conectar botones de pay-grid
        document.querySelectorAll('#mpDetPayGrid .orden-pay-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                if (!mpDetOrdenActual) return;
                document.querySelectorAll('#mpDetPayGrid .orden-pay-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                renderMpPagoPopup(btn.dataset.mpPay);
            });
        });
    })();''')

# ═══════════════════════════════════════════════════════════
# 7. CSS: quitar estilos de .mp-pay-btn/.mp-pay-lbl/.mp-pay-key/.mp-pay-icon
#    que ya no se usan (ahora usa orden-pay-btn del sistema original)
#    También limpiar el label extra que queda en el CSS
# ═══════════════════════════════════════════════════════════
patch('7-clean-unused-css',
'''        /* ── Mis Pedidos: payment grid ── */
        .mp-pay-btn {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 2px;
            padding: 8px 4px;
            background: #fff;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.5rem;
            color: #374151;
            font-weight: 700;
            transition: all 0.15s;
        }
        .mp-pay-btn:hover { border-color: #ff9900; background:#fff7ed; }
        .mp-pay-btn.active { border-color: #ff9900; background:#fff3cd; color:#92400e; box-shadow:0 0 0 2px rgba(255,153,0,.3); }
        .mp-pay-icon { font-size: 0.9rem; }
        .mp-pay-lbl { font-size: 0.5rem; font-weight: 800; letter-spacing: 0.3px; }
        .mp-pay-key { font-size: 0.42rem; color: #9ca3af; background: #f3f4f6; padding: 1px 4px; border-radius: 3px; }''',
'''        /* ── Mis Pedidos: payment grid uses orden-pay-btn (same as Nueva Orden) ── */''')

# ═══════════════════════════════════════════════════════════
# Guardar
# ═══════════════════════════════════════════════════════════
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(c)

print('\n'.join(ok))
if fail: print('\n'.join(fail))
print(f'\nTotal: {len(ok)} OK, {len(fail)} FAIL')
print(f'Len: {original_len} -> {len(c)} ({len(c)-original_len:+})')
