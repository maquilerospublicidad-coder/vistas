#!/usr/bin/env python3
"""Patch modulo Mis Pedidos - correcciones pedidas."""
import sys, re

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
        fail.append(f'FAIL [{name}]: found {n} times (expected 1)')
        return False
    c = c.replace(old, new, count)
    ok.append(f'OK [{name}]')
    return True

# ═══════════════════════════════════════════════════════════
# 1. FILTROS HTML: combinar folio+nombre, quitar desde/hasta,
#    agregar botón fecha que abre mini-calendario popup,
#    agregar opciones año y últimos 90 días / últimos 3 meses
# ═══════════════════════════════════════════════════════════
FILTERS_OLD = '''        <div class="mispedidos-filters">
            <div class="orden-field"><label>Folio</label><input id="mpFiltroFolio" type="text"></div>
            <div class="orden-field"><label>Nombre del cliente</label><input id="mpFiltroNombre" type="text"></div>
            <div class="orden-field"><label>Teléfono</label><input id="mpFiltroTelefono" type="text"></div>
            <div class="orden-field">
                <label>Diseñador</label>
                <select id="mpFiltroDisenador">
                    <option value="">Todos</option>
                </select>
            </div>
            <div class="orden-field">
                <label>Fecha</label>
                <select id="mpFiltroFechaRapido">
                    <option value="">Todos</option>
                    <option value="hoy">Hoy</option>
                    <option value="semana">Última semana</option>
                    <option value="mes">Último mes</option>
                    <option value="rango">Rango personalizado</option>
                </select>
            </div>
            <div class="orden-field" id="mpFechaRangoWrap" style="display:none;">
                <label>Desde</label><input id="mpFiltroFechaDesde" type="date">
            </div>
            <div class="orden-field" id="mpFechaRangoWrap2" style="display:none;">
                <label>Hasta</label><input id="mpFiltroFechaHasta" type="date">
            </div>
            <div class="orden-field">
                <label>Estatus de producción</label>
                <select id="mpFiltroEstatus">
                    <option value="">Todos</option>
                </select>
            </div>
            <div class="orden-field"><label>Adeudos del cliente</label><input id="mpFiltroAdeudo" type="number" min="0" step="0.01" placeholder="Min"></div>
            <div class="orden-field"><label> </label><button id="mpLimpiarFiltros" class="orden-btn" type="button">Limpiar filtros</button></div>
        </div>'''

FILTERS_NEW = '''        <div class="mispedidos-filters">
            <div class="orden-field" style="flex:2;min-width:180px;">
                <label>Buscar (Folio, Cliente, Teléfono)</label>
                <input id="mpFiltroBuscar" type="text" placeholder="Folio, nombre o teléfono...">
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
        </div>

        <!-- MINI POPUP CALENDARIO DE RANGO -->
        <div id="mpCalPopup" style="display:none;position:fixed;z-index:100020;background:#fff;border:1px solid #e5e7eb;border-radius:12px;box-shadow:0 12px 40px rgba(0,0,0,0.18);padding:16px;min-width:540px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
                <span style="font-size:0.62rem;font-weight:800;color:#92400e;text-transform:uppercase;">Seleccionar rango de fechas</span>
                <button id="mpCalCerrar" type="button" style="background:none;border:none;font-size:1rem;cursor:pointer;color:#6b7280;">✕</button>
            </div>
            <!-- Quick buttons row -->
            <div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:12px;">
                <button class="mp-cal-quick" data-q="hoy" type="button">Hoy</button>
                <button class="mp-cal-quick" data-q="semana" type="button">Semana</button>
                <button class="mp-cal-quick" data-q="mes" type="button">Mes</button>
                <button class="mp-cal-quick" data-q="ano" type="button">Año</button>
                <button class="mp-cal-quick" data-q="3meses" type="button">Últimos 3 meses</button>
                <button class="mp-cal-quick" data-q="90dias" type="button">Últimos 90 días</button>
            </div>
            <!-- Dual calendar -->
            <div style="display:flex;gap:16px;">
                <div id="mpCal1" class="mp-cal-month"></div>
                <div id="mpCal2" class="mp-cal-month"></div>
            </div>
            <div id="mpCalRangeLabel" style="margin-top:10px;font-size:0.58rem;color:#374151;text-align:center;min-height:16px;"></div>
            <div style="display:flex;justify-content:flex-end;gap:8px;margin-top:10px;">
                <button id="mpCalLimpiar" type="button" style="padding:6px 14px;background:#f3f4f6;color:#374151;border:none;border-radius:6px;cursor:pointer;font-size:0.6rem;font-weight:700;">Limpiar</button>
                <button id="mpCalAceptar" type="button" style="padding:6px 14px;background:#ff9900;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:0.6rem;font-weight:800;">✓ Aplicar</button>
            </div>
        </div>'''

patch('1-filters-html', FILTERS_OLD, FILTERS_NEW)

# ═══════════════════════════════════════════════════════════
# 2. TABLE-WRAP: agregar botones Nueva Orden y Eliminar arriba-derecha
# ═══════════════════════════════════════════════════════════
TABLE_OLD = '''        <div class="mispedidos-table-wrap">
            <table class="mispedidos-table">'''

TABLE_NEW = '''        <div style="display:flex;justify-content:flex-end;gap:6px;margin-bottom:4px;">
            <button id="mpNuevaOrdenBtn" type="button" style="padding:5px 12px;background:#ff9900;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:0.6rem;font-weight:800;display:none;">＋ Nueva Orden</button>
            <button id="mpEliminarSelBtn" type="button" style="padding:5px 10px;background:#fef2f2;color:#dc2626;border:1px solid #fecaca;border-radius:6px;cursor:pointer;font-size:0.6rem;font-weight:800;display:none;">🗑 Eliminar selección</button>
        </div>
        <div class="mispedidos-table-wrap">
            <table class="mispedidos-table">'''

patch('2-table-buttons', TABLE_OLD, TABLE_NEW)

# ═══════════════════════════════════════════════════════════
# 3. POPUP DETALLE ORDEN: rediseñar panel derecho (solo órdenes, no cotizaciones)
#    - quitar campo monto
#    - quitar select método de pago
#    - quitar botón REGISTRAR ABONO
#    - agregar cuadrícula de botones de pago
#    - mover IMPRIMIR debajo de los botones de pago
#    - mover HISTORIAL / WHATSAPP / PDF / ESTATUS a la sección de vendedor/diseñador (izquierda)
# ═══════════════════════════════════════════════════════════

# 3a. Añadir en sección vendedor/diseñador los botones de historial/wa/pdf/estatus
VEND_DIS_OLD = '''                <!-- Vendedor/Diseñador below table -->
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:16px;padding-top:14px;border-top:1px solid #f0f0f0;">
                    <div><div style="font-size:0.5rem;color:#ff9900;font-weight:800;text-transform:uppercase;">Vendedor</div><div id="mpDetVendedor" style="font-weight:700;font-size:0.68rem;color:#374151;"></div></div>
                    <div><div style="font-size:0.5rem;color:#ff9900;font-weight:800;text-transform:uppercase;">Diseñador Asignado</div><div id="mpDetDisenador" style="font-weight:700;font-size:0.68rem;color:#374151;"></div></div>
                </div>'''

VEND_DIS_NEW = '''                <!-- Vendedor/Diseñador below table -->
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:16px;padding-top:14px;border-top:1px solid #f0f0f0;">
                    <div><div style="font-size:0.5rem;color:#ff9900;font-weight:800;text-transform:uppercase;">Vendedor</div><div id="mpDetVendedor" style="font-weight:700;font-size:0.68rem;color:#374151;"></div></div>
                    <div><div style="font-size:0.5rem;color:#ff9900;font-weight:800;text-transform:uppercase;">Diseñador Asignado</div><div id="mpDetDisenador" style="font-weight:700;font-size:0.68rem;color:#374151;"></div></div>
                </div>
                <!-- Acciones secundarias: historial, whatsapp, pdf, estatus -->
                <div id="mpDetAccionesSecundarias" style="display:flex;flex-wrap:wrap;gap:5px;margin-top:12px;">
                    <button id="mpDetPagosBtn" type="button" style="flex:1;min-width:120px;font-size:0.55rem;padding:7px 8px;background:#fff;color:#92400e;border:1px solid #fde8c8;border-radius:7px;cursor:pointer;font-weight:700;">💰 Historial de pagos</button>
                    <button id="mpDetWhatsapp" type="button" style="flex:1;min-width:120px;font-size:0.55rem;padding:7px 8px;background:#dcfce7;color:#15803d;border:1px solid #86efac;border-radius:7px;cursor:pointer;font-weight:700;">📱 Enviar por WhatsApp</button>
                    <button id="mpDetPdf" type="button" style="flex:1;min-width:120px;font-size:0.55rem;padding:7px 8px;background:#fff;color:#374151;border:1px solid #e5e7eb;border-radius:7px;cursor:pointer;font-weight:700;">📄 Exportar PDF</button>
                    <button id="mpDetStatusWA" type="button" style="flex:1;min-width:120px;font-size:0.55rem;padding:7px 8px;background:#fff;color:#374151;border:1px solid #e5e7eb;border-radius:7px;cursor:pointer;font-weight:700;">📩 Estatus por WhatsApp</button>
                </div>'''

patch('3a-vendedor-acciones', VEND_DIS_OLD, VEND_DIS_NEW)

# 3b. Rediseñar panel derecho: quitar abono-monto/select, agregar pay-grid, mover imprimir
RIGHT_OLD = '''                <!-- Abono section (ventas only) -->
                <div id="mpDetAbonoWrap" style="margin-top:14px;border-top:2px solid #fde8c8;padding-top:12px;">
                    <div style="font-size:0.55rem;font-weight:800;color:#92400e;margin-bottom:8px;text-transform:uppercase;">Abonar al Restante</div>
                    <div style="display:flex;flex-direction:column;gap:6px;">
                        <input id="mpDetAbonoMonto" type="number" min="0" step="0.01" placeholder="Monto a abonar" style="width:100%;padding:8px 10px;font-size:0.6rem;border:1px solid #fde8c8;border-radius:8px;box-sizing:border-box;">
                        <select id="mpDetAbonoMetodo" style="width:100%;padding:8px 10px;font-size:0.6rem;border:1px solid #fde8c8;border-radius:8px;">
                            <option value="EFECTIVO">Efectivo</option>
                            <option value="TARJETA">Tarjeta</option>
                            <option value="TRANSFERENCIA">Transferencia</option>
                            <option value="DEPOSITO">Depósito</option>
                        </select>
                        <button id="mpDetAbonoBtn" type="button" style="width:100%;font-size:0.6rem;padding:10px;background:#ff9900;color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:800;">💰 REGISTRAR ABONO</button>
                    </div>
                </div>
                <!-- Action buttons -->
                <div style="margin-top:14px;display:flex;flex-direction:column;gap:6px;">
                    <button id="mpDetImprimir" type="button" style="width:100%;font-size:0.6rem;padding:10px;background:#ff9900;color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:800;">🖨 IMPRIMIR ORDEN</button>
                    <button id="mpDetPagosBtn" type="button" style="width:100%;font-size:0.6rem;padding:10px;background:#fff;color:#92400e;border:2px solid #ff9900;border-radius:8px;cursor:pointer;font-weight:800;">💰 HISTORIAL DE PAGOS</button>
                    <button id="mpDetWhatsapp" type="button" style="width:100%;font-size:0.6rem;padding:10px;background:#25d366;color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:800;">📱 ENVIAR POR WHATSAPP</button>
                    <button id="mpDetPdf" type="button" style="width:100%;font-size:0.6rem;padding:10px;background:#fff;color:#374151;border:1px solid #e5e7eb;border-radius:8px;cursor:pointer;font-weight:700;">📄 EXPORTAR PDF</button>
                    <button id="mpDetStatusWA" type="button" style="width:100%;font-size:0.6rem;padding:10px;background:#fff;color:#374151;border:1px solid #e5e7eb;border-radius:8px;cursor:pointer;font-weight:700;">📩 ESTATUS POR WHATSAPP</button>
                </div>'''

RIGHT_NEW = '''                <!-- Abono section: método de pago en cuadrícula (ventas only) -->
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
                </div>'''

patch('3b-pay-grid', RIGHT_OLD, RIGHT_NEW)

# ═══════════════════════════════════════════════════════════
# 4. CSS: agregar estilos para mp-pay-btn, mp-cal-quick, mp-cal-month
# ═══════════════════════════════════════════════════════════
CSS_ANCHOR = '''        .mispedidos-filters .orden-field {'''
CSS_NEW_BEFORE = '''        /* ── Mis Pedidos: payment grid ── */
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
        .mp-pay-key { font-size: 0.42rem; color: #9ca3af; background: #f3f4f6; padding: 1px 4px; border-radius: 3px; }

        /* ── Mini calendario ── */
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
        .mp-cal-month .cal-day.empty { cursor:default; }

        .mispedidos-filters .orden-field {'''

if CSS_ANCHOR in c:
    c = c.replace(CSS_ANCHOR, CSS_NEW_BEFORE, 1)
    ok.append('OK [4-css]')
else:
    fail.append('FAIL [4-css]: anchor not found')

# ═══════════════════════════════════════════════════════════
# 5. JS: actualizar getMisPedidosFiltrados para usar mpFiltroBuscar
#    y getMpDateRange para soportar nuevas opciones
# ═══════════════════════════════════════════════════════════
GET_DATE_OLD = '''    const getMpDateRange = () => {
        const rapid = mpFiltroFechaRapido?.value || '';
        if (!rapid) return null;
        const now = new Date();
        const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        let desde, hasta;
        if (rapid === 'hoy') {
            desde = hasta = today;
        } else if (rapid === 'semana') {
            desde = new Date(today); desde.setDate(desde.getDate() - 7);
            hasta = today;
        } else if (rapid === 'mes') {
            desde = new Date(today); desde.setMonth(desde.getMonth() - 1);
            hasta = today;
        } else if (rapid === 'rango') {
            const d = mpFiltroFechaDesde?.value || '';
            const h = mpFiltroFechaHasta?.value || '';
            if (!d && !h) return null;
            desde = d ? new Date(d + 'T00:00:00') : new Date('2000-01-01');
            hasta = h ? new Date(h + 'T23:59:59') : new Date('2099-12-31');
        }
        if (!desde || !hasta) return null;
        return { desde, hasta, campo: 'fechaEmitida' };
    };'''

GET_DATE_NEW = '''    const getMpDateRange = () => {
        const rapid = mpFiltroFechaRapido?.value || '';
        if (!rapid) return null;
        const now = new Date();
        const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        let desde, hasta;
        if (rapid === 'hoy') {
            desde = hasta = today;
        } else if (rapid === 'semana') {
            desde = new Date(today); desde.setDate(desde.getDate() - 7);
            hasta = today;
        } else if (rapid === 'mes') {
            desde = new Date(today); desde.setMonth(desde.getMonth() - 1);
            hasta = today;
        } else if (rapid === 'ano') {
            desde = new Date(today.getFullYear(), 0, 1);
            hasta = today;
        } else if (rapid === '90dias') {
            desde = new Date(today); desde.setDate(desde.getDate() - 90);
            hasta = today;
        } else if (rapid === '3meses') {
            desde = new Date(today); desde.setMonth(desde.getMonth() - 3);
            hasta = today;
        } else if (rapid === 'rango') {
            const d = document.getElementById('mpFiltroFechaDesde')?.value || '';
            const h = document.getElementById('mpFiltroFechaHasta')?.value || '';
            if (!d && !h) return null;
            desde = d ? new Date(d + 'T00:00:00') : new Date('2000-01-01');
            hasta = h ? new Date(h + 'T23:59:59') : new Date('2099-12-31');
        }
        if (!desde || !hasta) return null;
        return { desde, hasta, campo: 'fechaEmitida' };
    };'''

patch('5a-getMpDateRange', GET_DATE_OLD, GET_DATE_NEW)

# 5b. getMisPedidosFiltrados: usa mpFiltroBuscar en lugar de folio/nombre/tel separados
FILTER_FN_OLD = '''        return misPedidosData.filter((row) => {
            if (row.tipo !== misPedidosTab) return false;
            if (!mpMatch(row.folio, mpFiltroFolio?.value || '')) return false;
            if (!mpMatch(row.clienteNombre, mpFiltroNombre?.value || '')) return false;
            if (!mpMatch(row.telefono, mpFiltroTelefono?.value || '')) return false;
            if (!mpMatch(row.disenador, mpFiltroDisenador?.value || '')) return false;'''

FILTER_FN_NEW = '''        const buscarQ = (document.getElementById('mpFiltroBuscar')?.value || '').trim().toLowerCase();
        return misPedidosData.filter((row) => {
            if (row.tipo !== misPedidosTab) return false;
            // Buscador unificado (folio, nombre, teléfono)
            if (buscarQ) {
                const hayMatch = mpMatch(row.folio, buscarQ) ||
                                 mpMatch(row.clienteNombre, buscarQ) ||
                                 mpMatch(row.telefono, buscarQ);
                if (!hayMatch) return false;
            }
            if (!mpMatch(row.disenador, mpFiltroDisenador?.value || '')) return false;'''

patch('5b-filter-fn', FILTER_FN_OLD, FILTER_FN_NEW)

# 5c. Eventos de filtros: agregar mpFiltroBuscar y mantener resto
FILTER_EVENTS_OLD = '''    [mpFiltroFolio, mpFiltroNombre, mpFiltroTelefono, mpFiltroDisenador, mpFiltroFechaRapido, mpFiltroFechaDesde, mpFiltroFechaHasta, mpFiltroEstatus, mpFiltroAdeudo]
        .filter(Boolean)
        .forEach((input) => {
            input.addEventListener('input', renderMisPedidos);
            input.addEventListener('change', renderMisPedidos);
        });

    if (mpFiltroFechaRapido) {
        mpFiltroFechaRapido.addEventListener('change', () => {
            const isRango = mpFiltroFechaRapido.value === 'rango';
            if (mpFechaRangoWrap) mpFechaRangoWrap.style.display = isRango ? '' : 'none';
            if (mpFechaRangoWrap2) mpFechaRangoWrap2.style.display = isRango ? '' : 'none';
            renderMisPedidos();
        });
    }

    if (mpLimpiarFiltros) {
        mpLimpiarFiltros.addEventListener('click', () => {
            [mpFiltroFolio, mpFiltroNombre, mpFiltroTelefono, mpFiltroDisenador, mpFiltroFechaRapido, mpFiltroFechaDesde, mpFiltroFechaHasta, mpFiltroEstatus, mpFiltroAdeudo]
                .filter(Boolean)
                .forEach((input) => {
                    input.value = '';
                });
            if (mpFechaRangoWrap) mpFechaRangoWrap.style.display = 'none';
            if (mpFechaRangoWrap2) mpFechaRangoWrap2.style.display = 'none';
            mpSelectedIds = new Set();
            renderMisPedidos();
        });
    }'''

FILTER_EVENTS_NEW = '''    // ── Filtros Mis Pedidos ────────────────────────────────────
    const mpFiltroBuscar = document.getElementById('mpFiltroBuscar');
    [mpFiltroBuscar, mpFiltroDisenador, mpFiltroFechaRapido, mpFiltroEstatus, mpFiltroAdeudo]
        .filter(Boolean)
        .forEach((input) => {
            input.addEventListener('input', renderMisPedidos);
            input.addEventListener('change', renderMisPedidos);
        });

    if (mpFiltroFechaRapido) {
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
    });

    if (mpLimpiarFiltros) {
        mpLimpiarFiltros.addEventListener('click', () => {
            const buscar = document.getElementById('mpFiltroBuscar');
            if (buscar) buscar.value = '';
            [mpFiltroFolio, mpFiltroNombre, mpFiltroTelefono, mpFiltroDisenador, mpFiltroFechaRapido, mpFiltroEstatus, mpFiltroAdeudo]
                .filter(Boolean)
                .forEach((input) => { input.value = ''; });
            mpCalRangeStart = null; mpCalRangeEnd = null;
            const desdeEl = document.getElementById('mpFiltroFechaDesde');
            const hastaEl = document.getElementById('mpFiltroFechaHasta');
            if (desdeEl) desdeEl.value = '';
            if (hastaEl) hastaEl.value = '';
            const calBtn = document.getElementById('mpFechaCalBtn');
            if (calBtn) calBtn.style.display = 'none';
            closeMpCalPopup();
            mpSelectedIds = new Set();
            renderMisPedidos();
        });
    }'''

patch('5c-filter-events', FILTER_EVENTS_OLD, FILTER_EVENTS_NEW)

# ═══════════════════════════════════════════════════════════
# 6. JS: botones de pago en popup detalle (abono por clic en método)
#    y botones de tabla (Nueva Orden / Eliminar)
# ═══════════════════════════════════════════════════════════

# 6a. openDetalleOrdenPopup: ajustar para pay-grid + mostrar botones de tabla solo en venta
OPEN_DET_ADJ_OLD = '''        // For cotizaciones: hide payment-related sections
        const pagosSection = elF('mpDetPagosSection');
        if (pagosSection) pagosSection.style.display = esCotizacion ? 'none' : '';
        const abonoWrap = elF('mpDetAbonoWrap');
        if (abonoWrap) abonoWrap.style.display = (esCotizacion || Number(row.adeudoCliente || 0) <= 0) ? 'none' : '';
        const montoInput = elF('mpDetAbonoMonto');
        if (montoInput) montoInput.value = '';
        const pagosBtn = elF('mpDetPagosBtn');
        if (pagosBtn) pagosBtn.style.display = esCotizacion ? 'none' : '';'''

OPEN_DET_ADJ_NEW = '''        // For cotizaciones: hide payment-related sections
        const pagosSection = elF('mpDetPagosSection');
        if (pagosSection) pagosSection.style.display = esCotizacion ? 'none' : '';
        const abonoWrap = elF('mpDetAbonoWrap');
        if (abonoWrap) abonoWrap.style.display = (esCotizacion || Number(row.adeudoCliente || 0) <= 0) ? 'none' : '';
        const montoInput = elF('mpDetAbonoMonto');
        if (montoInput) montoInput.value = '';
        const pagosBtn = elF('mpDetPagosBtn');
        if (pagosBtn) pagosBtn.style.display = esCotizacion ? 'none' : '';
        // Ocultar acciones secundarias para cotizaciones
        const accionesSec = elF('mpDetAccionesSecundarias');
        if (accionesSec) accionesSec.style.display = esCotizacion ? 'none' : '';
        // Reiniciar estado de botones de pago
        document.querySelectorAll('#mpDetPayGrid .mp-pay-btn').forEach(b => b.classList.remove('active'));
        elF('mpDetAbonoConfirm')?.style && (elF('mpDetAbonoConfirm').style.display = 'none');
        // Botones tabla solo para órdenes
        const nvaBtn = document.getElementById('mpNuevaOrdenBtn');
        const delBtn = document.getElementById('mpEliminarSelBtn');
        if (nvaBtn) nvaBtn.style.display = esCotizacion ? 'none' : '';
        if (delBtn) delBtn.style.display = esCotizacion ? 'none' : '';'''

patch('6a-open-det-adj', OPEN_DET_ADJ_OLD, OPEN_DET_ADJ_NEW)

# 6b. Reemplazar abonoBtn handler con nueva lógica de pay-grid
ABONO_HANDLER_OLD = '''    document.getElementById('mpDetAbonoBtn')?.addEventListener('click', () => {
        if (!mpDetOrdenActual) return;
        const montoInput = document.getElementById('mpDetAbonoMonto');
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
        if (montoInput) montoInput.value = '';
        renderMisPedidos();
        alert(`Abono de $${monto.toFixed(2)} registrado exitosamente.`);
    });'''

ABONO_HANDLER_NEW = '''    // ── Pay-grid buttons (abono por método de pago) ──────────
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
    });'''

patch('6b-abono-handler', ABONO_HANDLER_OLD, ABONO_HANDLER_NEW)

# 6c. imprimir handler (ya no hay que hacer click en pdf, el de imprimir puede hacerlo solo)
# El botón de imprimir ahora también está en el panel de abono, same id works

# ═══════════════════════════════════════════════════════════
# 7. JS: botones de tabla Nueva Orden / Eliminar + permiso admin
# ═══════════════════════════════════════════════════════════
# Agregar handlers después del doble-clic en tabla (openDetalleOrdenPopup)
DBLCLICK_OLD = '''            if (row) openDetalleOrdenPopup(row);'''

DBLCLICK_NEW = '''            if (row) openDetalleOrdenPopup(row);
            // Mostrar botones de tabla solo para venta (no cotización)
            const nvaBtn = document.getElementById('mpNuevaOrdenBtn');
            const delBtn = document.getElementById('mpEliminarSelBtn');
            if (nvaBtn) nvaBtn.style.display = (row && row.tipo !== 'cotizacion') ? '' : 'none';
            if (delBtn) delBtn.style.display = (row && row.tipo !== 'cotizacion') ? '' : 'none';'''

patch('7a-dblclick', DBLCLICK_OLD, DBLCLICK_NEW)

# 7b. Agregar handlers para los botones de tabla (nueva orden / eliminar)
# Los ponemos justo antes del listener de mispedidosBack
MISPED_BACK_OLD = '''    window.openMisPedidosPopupGlobal = openMisPedidosPopup;'''

MISPED_BACK_NEW = '''    window.openMisPedidosPopupGlobal = openMisPedidosPopup;

    // ── Botones de tabla (Nueva Orden / Eliminar) ─────────────
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
    })();'''

patch('7b-tabla-buttons', MISPED_BACK_OLD, MISPED_BACK_NEW)

# ═══════════════════════════════════════════════════════════
# Guardar
# ═══════════════════════════════════════════════════════════
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(c)

print('\n'.join(ok))
if fail: print('\n'.join(fail))
print(f'\nTotal: {len(ok)} OK, {len(fail)} FAIL')
print(f'Len: {original_len} -> {len(c)} ({len(c)-original_len:+})')
