#!/usr/bin/env python3
"""
Convert caja sub-panels back to proper fixed popup modals.
Key: use class 'caja-accion-modal' (not 'caja-overlay') and
     id 'cajaPanelIngreso'/'cajaPanelGastoAcc' (not starting with 'popup')
     so they are NOT caught by the global reset selector.
"""

FILE = '/workspaces/vistas/mockup.html'

with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

orig_len = len(html)

# ── 1. Remove the inline sub-panels from inside caja-card ─────────────────────
OLD_INSIDE = '''            <!-- SUB-PANEL: INGRESAR DINERO (dentro de caja-card, no es overlay) -->
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
        </div>
    </div>
</div>

<div id="popupCalendario"'''

NEW_AFTER_CAJA = '''        </div>
    </div>
</div>

<!-- ===== POPUP INGRESAR DINERO ===== -->
<!-- Nota: clase caja-accion-modal (no caja-overlay), id no empieza con "popup" → no afectado por reset global -->
<div id="cajaPanelIngreso" class="caja-accion-modal" aria-hidden="true" role="dialog" aria-modal="true" aria-labelledby="cajaIngresoTitulo">
    <div class="caja-accion-modal-card">
        <div class="caja-accion-modal-header">
            <h3 id="cajaIngresoTitulo">💰 INGRESAR DINERO</h3>
            <button class="caja-accion-modal-close" type="button" id="cajaIngresoBack" aria-label="Cerrar">✕</button>
        </div>
        <div class="caja-accion-modal-body">
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
        </div>
        <div class="caja-accion-modal-footer">
            <button id="cajaBtnConfirmarIngreso" class="caja-btn primary" type="button" style="width:100%;">✔ CONFIRMAR INGRESO</button>
        </div>
    </div>
</div>

<!-- ===== POPUP REALIZAR GASTO ===== -->
<div id="cajaPanelGastoAcc" class="caja-accion-modal" aria-hidden="true" role="dialog" aria-modal="true" aria-labelledby="cajaGastoAccTitulo">
    <div class="caja-accion-modal-card">
        <div class="caja-accion-modal-header">
            <h3 id="cajaGastoAccTitulo">💸 REALIZAR GASTO</h3>
            <button class="caja-accion-modal-close" type="button" id="cajaGastoAccBack" aria-label="Cerrar">✕</button>
        </div>
        <div class="caja-accion-modal-body">
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
        </div>
        <div class="caja-accion-modal-footer">
            <button id="cajaBtnConfirmarGasto" class="caja-btn warn" type="button" style="width:100%;">✔ CONFIRMAR GASTO</button>
        </div>
    </div>
</div>

<div id="popupCalendario"'''

if OLD_INSIDE in html:
    html = html.replace(OLD_INSIDE, NEW_AFTER_CAJA)
    print("✅ Sub-paneles movidos fuera de caja-card como popups reales")
else:
    print("❌ No se encontró el bloque de sub-paneles")

# ── 2. Replace .caja-sub-panel CSS with .caja-accion-modal CSS ────────────────
OLD_CSS = '''        .caja-sub-panel {
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

        .caja-card {'''

NEW_CSS = '''        /* ── Popup de acción de caja (ingresar / gasto) ── */
        .caja-accion-modal {
            display: none;
            position: fixed;
            inset: 0;
            z-index: 3100;
            background: rgba(0,0,0,0.48);
            align-items: center;
            justify-content: center;
            padding: 16px;
        }
        .caja-accion-modal[aria-hidden="false"] {
            display: flex;
        }
        .caja-accion-modal-card {
            background: #fff;
            border-radius: 14px;
            box-shadow: 0 8px 40px rgba(0,0,0,0.22);
            width: 100%;
            max-width: 480px;
            display: flex;
            flex-direction: column;
            gap: 0;
            overflow: hidden;
        }
        .caja-accion-modal-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 20px 12px;
            border-bottom: 1px solid #e8edf4;
            background: #f5f7fb;
        }
        .caja-accion-modal-header h3 {
            font-size: 1rem;
            font-weight: 800;
            color: #1f2937;
            margin: 0;
            letter-spacing: 0.03em;
        }
        .caja-accion-modal-close {
            background: none;
            border: 1px solid #d4dae4;
            border-radius: 999px;
            width: 30px;
            height: 30px;
            cursor: pointer;
            font-size: 0.85rem;
            color: #6b7280;
            display: grid;
            place-items: center;
        }
        .caja-accion-modal-close:hover { background:#f3f4f6; color:#111; }
        .caja-accion-modal-body {
            padding: 20px;
        }
        .caja-accion-modal-footer {
            padding: 14px 20px 18px;
            border-top: 1px solid #e8edf4;
            background: #f5f7fb;
        }

        .caja-card {'''

if OLD_CSS in html:
    html = html.replace(OLD_CSS, NEW_CSS)
    print("✅ CSS actualizado: caja-sub-panel → caja-accion-modal")
else:
    print("❌ No se encontró el CSS de .caja-sub-panel")

# ── 3. Update JS: show/hide now uses aria-hidden toggle directly ──────────────
# Change display:'flex' → aria-hidden='false' for the new modal style
# The JS already uses: p.style.display='flex' + p.setAttribute('aria-hidden','false')
# For .caja-accion-modal we rely on [aria-hidden="false"] { display:flex } — so style.display is not needed
# But current JS sets p.style.display='flex' which OVERRIDES the CSS selector
# We need to also keep style.display for the open/close to work, so this is fine as-is
# (the CSS uses display:flex via [aria-hidden=false] but JS also sets inline display:flex → both work)

print("✅ JS no necesita cambios (ya usa display:flex + aria-hidden)")

# ── Save ──────────────────────────────────────────────────────────────────────
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nListo. Longitud: {orig_len} → {len(html)}")
