#!/usr/bin/env python3
"""
Fix caja sub-popups: move them inside caja-card as absolute panels
so they're not affected by global overlay reset selectors.
Also add dinero disponible display to cajaPanelGasto.
"""

FILE = '/workspaces/vistas/mockup.html'

with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

orig_len = len(html)

# ── 1. Locate and extract the current sub-popup HTML ──────────────────────────
INGRESO_START = '<!-- ===== POPUP INGRESAR DINERO ====='
GASTO_START   = '<!-- ===== POPUP REALIZAR GASTO ====='
POPUP_CAL_START = '<div id="popupCalendario"'

idx_ingreso = html.index(INGRESO_START)
idx_gasto   = html.index(GASTO_START)
idx_cal     = html.index(POPUP_CAL_START)

# Extract both popup blocks (they sit between ingreso_start and popupCalendario)
# Remove the old standalone popup HTML (including surrounding whitespace)
old_standalone = html[idx_ingreso:idx_cal]
html = html[:idx_ingreso] + html[idx_cal:]
print(f"✅ Removed standalone sub-popups ({len(old_standalone)} chars)")

# ── 2. Build new inline sub-panels ────────────────────────────────────────────
# These go INSIDE caja-card, as absolutely-positioned panels
# class="caja-sub-panel" (NOT caja-overlay) so they're never caught by reset selectors

INGRESO_PANEL = '''
            <!-- SUB-PANEL: INGRESAR DINERO (dentro de caja-card, no es overlay) -->
            <div id="cajaPanelIngreso" class="caja-sub-panel" aria-hidden="true">
                <button class="caja-back" type="button" id="cajaIngresoBack" title="Cerrar">←</button>
                <div class="caja-head"><h2 class="caja-title" id="cajaIngresoTitulo">INGRESAR DINERO</h2></div>
                <div class="caja-rect-wrap" style="padding:18px;">
                    <div class="caja-zone caja-zone-editable">
                        <div class="caja-gasto-grid">
                            <div class="orden-field productos-field-span2">
                                <label for="cajaIngresoMotivoSel">MOTIVO DE INGRESO</label>
                                <select id="cajaIngresoMotivoSel">
                                    <option value="FONDO INICIAL">FONDO INICIAL</option>
                                    <option value="REPOSICIÓN DE FONDO">REPOSICIÓN DE FONDO</option>
                                    <option value="ANTICIPO DE CLIENTE">ANTICIPO DE CLIENTE</option>
                                    <option value="DEVOLUCIÓN">DEVOLUCIÓN</option>
                                    <option value="VENTA ADICIONAL">VENTA ADICIONAL</option>
                                    <option value="PRÉSTAMO">PRÉSTAMO</option>
                                    <option value="OTRO">OTRO...</option>
                                </select>
                            </div>
                            <div class="orden-field productos-field-span2" id="cajaIngresoOtroWrap" style="display:none;">
                                <label for="cajaIngresoOtroInput">ESPECIFICAR MOTIVO</label>
                                <input id="cajaIngresoOtroInput" type="text" placeholder="ESCRIBE EL MOTIVO...">
                            </div>
                            <div class="orden-field">
                                <label for="cajaIngresoFuente">MÉTODO DE INGRESO</label>
                                <select id="cajaIngresoFuente">
                                    <option value="EFECTIVO">EFECTIVO</option>
                                    <option value="TARJETA">TARJETA</option>
                                    <option value="TRANSFERENCIA">TRANSFERENCIA</option>
                                    <option value="DEPOSITO">DEPÓSITO</option>
                                </select>
                            </div>
                            <div class="orden-field">
                                <label for="cajaIngresoMonto">CANTIDAD A INGRESAR</label>
                                <input id="cajaIngresoMonto" type="number" min="0" step="0.01" placeholder="0.00">
                            </div>
                        </div>
                        <div class="caja-actions" style="margin-top:14px;">
                            <button id="cajaBtnConfirmarIngreso" class="caja-btn primary" type="button">✔ CONFIRMAR INGRESO</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- SUB-PANEL: REALIZAR GASTO (dentro de caja-card, no es overlay) -->
            <div id="cajaPanelGastoAcc" class="caja-sub-panel" aria-hidden="true">
                <button class="caja-back" type="button" id="cajaGastoAccBack" title="Cerrar">←</button>
                <div class="caja-head"><h2 class="caja-title" id="cajaGastoAccTitulo">REALIZAR GASTO</h2></div>
                <div class="caja-rect-wrap" style="padding:18px;">
                    <div class="caja-zone caja-zone-editable">
                        <div class="caja-gasto-grid">
                            <div class="orden-field productos-field-span2">
                                <label for="cajaGastoAccMotivoSel">MOTIVO DEL GASTO</label>
                                <select id="cajaGastoAccMotivoSel">
                                    <option value="COMPRA DE INSUMOS">COMPRA DE INSUMOS</option>
                                    <option value="SERVICIO / MANTENIMIENTO">SERVICIO / MANTENIMIENTO</option>
                                    <option value="PAGO A PROVEEDOR">PAGO A PROVEEDOR</option>
                                    <option value="GASTOS OPERATIVOS">GASTOS OPERATIVOS</option>
                                    <option value="PAPELERÍA">PAPELERÍA</option>
                                    <option value="TRANSPORTE">TRANSPORTE</option>
                                    <option value="SALARIO / NÓMINA">SALARIO / NÓMINA</option>
                                    <option value="IMPUESTOS">IMPUESTOS</option>
                                    <option value="OTRO">OTRO...</option>
                                </select>
                            </div>
                            <div class="orden-field productos-field-span2" id="cajaGastoAccOtroWrap" style="display:none;">
                                <label for="cajaGastoAccOtroInput">ESPECIFICAR MOTIVO</label>
                                <input id="cajaGastoAccOtroInput" type="text" placeholder="ESCRIBE EL MOTIVO...">
                            </div>
                            <div class="orden-field">
                                <label for="cajaGastoAccFuente">FONDOS DESDE</label>
                                <select id="cajaGastoAccFuente">
                                    <option value="EFECTIVO">EFECTIVO</option>
                                    <option value="TARJETA">TARJETA</option>
                                    <option value="TRANSFERENCIA">TRANSFERENCIA</option>
                                    <option value="DEPOSITO">DEPÓSITO</option>
                                </select>
                            </div>
                            <div id="cajaDisponibleMontoAcc" class="caja-disponible" style="grid-column:1/-1;">Dinero disponible: $0.00</div>
                            <div class="orden-field">
                                <label for="cajaGastoAccMonto">CANTIDAD A RETIRAR</label>
                                <input id="cajaGastoAccMonto" type="number" min="0" step="0.01" placeholder="0.00">
                            </div>
                        </div>
                        <div class="caja-actions" style="margin-top:14px;">
                            <button id="cajaBtnConfirmarGasto" class="caja-btn warn" type="button">✔ CONFIRMAR GASTO</button>
                        </div>
                    </div>
                </div>
            </div>
'''

# ── 3. Insert sub-panels INSIDE caja-card, just before </div></div> (caja-rect-wrap close + caja-card close) ──
# The caja-card structure is:
# <div class="caja-card">
#   <button id="cajaBack">
#   <div class="caja-head">
#   <div class="caja-rect-wrap">
#     <div class="caja-tabs">
#     <section id="cajaPanelCorte">
#     <section id="cajaPanelGasto">
#   </div>           ← close caja-rect-wrap
# </div>             ← close caja-card
# </div>             ← close popupCaja

OLD_CARD_END = '''            </section>
        </div>
    </div>
</div>

<div id="popupCalendario"'''

NEW_CARD_END = '''            </section>''' + INGRESO_PANEL + '''        </div>
    </div>
</div>

<div id="popupCalendario"'''

if OLD_CARD_END in html:
    html = html.replace(OLD_CARD_END, NEW_CARD_END)
    print("✅ Sub-paneles insertados dentro de caja-card")
else:
    print("❌ No se encontró el cierre de caja-card")

# ── 4. Add CSS for .caja-sub-panel ────────────────────────────────────────────
OLD_CSS = '''        .caja-card {
            width: 100vw;
            height: 100vh;'''

NEW_CSS = '''        .caja-sub-panel {
            display: none;
            position: absolute;
            inset: 0;
            background: #f5f7fb;
            z-index: 10;
            grid-template-rows: auto 1fr;
            gap: 10px;
            padding: 12px;
            overflow-y: auto;
        }
        .caja-sub-panel[aria-hidden="false"] {
            display: grid;
        }

        .caja-card {
            width: 100vw;
            height: 100vh;'''

if OLD_CSS in html:
    html = html.replace(OLD_CSS, NEW_CSS)
    print("✅ CSS .caja-sub-panel agregado")
else:
    print("❌ No se encontró el CSS de .caja-card")

# ── 5. Update JS references from popupCajaIngreso → cajaPanelIngreso ──────────
# The IDs changed: popupCajaIngreso → cajaPanelIngreso, popupCajaGastoAcc → cajaPanelGastoAcc
html = html.replace("document.getElementById('popupCajaIngreso')", "document.getElementById('cajaPanelIngreso')")
html = html.replace("document.getElementById('popupCajaGastoAcc')", "document.getElementById('cajaPanelGastoAcc')")
print("✅ Referencias JS actualizadas (popupCaja* → cajaPanel*)")

# ── 6. Also rename IDs in closeCajaPopup ──────────────────────────────────────
html = html.replace("'popupCajaIngreso','popupCajaGastoAcc'", "'cajaPanelIngreso','cajaPanelGastoAcc'")
print("✅ IDs en closeCajaPopup actualizados")

# ── 7. Add dinero disponible display in cajaPanelGasto ────────────────────────
OLD_GASTO_ZONE = '''                <div class="caja-zone caja-zone-editable">
                    <div class="caja-zone-head">
                        <h4>Operaciones</h4>
                    </div>
                    <div class="caja-actions" style="flex-direction:row;gap:18px;justify-content:center;padding:22px 0;">
                        <button id="cajaBtnIngresarDinero" class="caja-btn primary" type="button" style="min-width:180px;font-size:0.75rem;">💰 Ingresar dinero</button>
                        <button id="cajaBtnRealizarGasto" class="caja-btn warn" type="button" style="min-width:180px;font-size:0.75rem;">💸 Realizar gasto</button>
                    </div>
                </div>'''

NEW_GASTO_ZONE = '''                <div class="caja-zone caja-zone-readonly">
                    <div class="caja-zone-head"><h4>Dinero disponible (efectivo del día)</h4></div>
                    <div id="cajaDisponibleMonto" class="caja-disponible" style="padding:8px 0;font-size:1rem;">$0.00</div>
                </div>
                <div class="caja-zone caja-zone-editable">
                    <div class="caja-zone-head">
                        <h4>Operaciones</h4>
                    </div>
                    <div class="caja-actions" style="flex-direction:row;gap:18px;justify-content:center;padding:22px 0;">
                        <button id="cajaBtnIngresarDinero" class="caja-btn primary" type="button" style="min-width:180px;font-size:0.75rem;">💰 Ingresar dinero</button>
                        <button id="cajaBtnRealizarGasto" class="caja-btn warn" type="button" style="min-width:180px;font-size:0.75rem;">💸 Realizar gasto</button>
                    </div>
                </div>'''

if OLD_GASTO_ZONE in html:
    html = html.replace(OLD_GASTO_ZONE, NEW_GASTO_ZONE)
    print("✅ Dinero disponible agregado a cajaPanelGasto")
else:
    print("❌ No se encontró la zona de operaciones en cajaPanelGasto")

# ── Save ──────────────────────────────────────────────────────────────────────
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nListo. Longitud: {orig_len} → {len(html)}")
