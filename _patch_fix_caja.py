#!/usr/bin/env python3
"""Fix caja popup z-index, cleanup on close, restore datos del turno."""

FILE = '/workspaces/vistas/mockup.html'

with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

orig_len = len(html)

# 1 ── Fix z-index on sub-popups (2100 → 3000)
html = html.replace(
    '<div id="popupCajaIngreso" class="caja-overlay" aria-hidden="true" style="z-index:2100;">',
    '<div id="popupCajaIngreso" class="caja-overlay" aria-hidden="true" style="z-index:3000;">'
)
html = html.replace(
    '<div id="popupCajaGastoAcc" class="caja-overlay" aria-hidden="true" style="z-index:2100;">',
    '<div id="popupCajaGastoAcc" class="caja-overlay" aria-hidden="true" style="z-index:3000;">'
)

# 2 ── closeCajaPopup: also hide sub-popups when main caja popup closes
old_close = '''    const closeCajaPopup = () => {
        if (!popupCaja) return;
        popupCaja.style.display = 'none';
        popupCaja.setAttribute('aria-hidden', 'true');'''

new_close = '''    const closeCajaPopup = () => {
        if (!popupCaja) return;
        popupCaja.style.display = 'none';
        popupCaja.setAttribute('aria-hidden', 'true');
        // Cerrar también los sub-popups de caja
        ['popupCajaIngreso','popupCajaGastoAcc'].forEach(id => {
            const sp = document.getElementById(id);
            if (sp) { sp.style.display = 'none'; sp.setAttribute('aria-hidden','true'); }
        });'''

if old_close in html:
    html = html.replace(old_close, new_close)
    print("✅ closeCajaPopup actualizado")
else:
    print("❌ No se encontró closeCajaPopup")

# 3 ── Restore "Datos del turno" section inside cajaPanelGasto
old_gasto = '''            <section id="cajaPanelGasto" class="caja-panel" style="display:none;">
                <h3 class="caja-legend">Acciones de caja</h3>
                <div class="caja-actions" style="flex-direction:row;gap:18px;justify-content:center;padding:30px 0;">
                    <button id="cajaBtnIngresarDinero" class="caja-btn primary" type="button" style="min-width:180px;font-size:0.75rem;">💰 Ingresar dinero</button>
                    <button id="cajaBtnRealizarGasto" class="caja-btn warn" type="button" style="min-width:180px;font-size:0.75rem;">💸 Realizar gasto</button>
                </div>
            </section>'''

new_gasto = '''            <section id="cajaPanelGasto" class="caja-panel" style="display:none;">
                <h3 class="caja-legend">Acciones de caja</h3>
                <div class="caja-zone caja-zone-readonly">
                    <div class="caja-zone-head">
                        <h4>Información del turno</h4>
                    </div>
                    <div class="caja-meta">
                        <div class="caja-meta-box"><b>Caja</b><span id="cajaNombreLabelGasto">Caja principal</span></div>
                        <div class="caja-meta-box"><b>ID de caja</b><span id="cajaIdLabelGasto">CAJA-01</span></div>
                        <div class="caja-meta-box"><b>Usuario logeado</b><span id="cajaUsuarioLabelGasto">Usuario en turno</span></div>
                    </div>
                </div>
                <div class="caja-zone caja-zone-editable">
                    <div class="caja-zone-head">
                        <h4>Operaciones</h4>
                    </div>
                    <div class="caja-actions" style="flex-direction:row;gap:18px;justify-content:center;padding:22px 0;">
                        <button id="cajaBtnIngresarDinero" class="caja-btn primary" type="button" style="min-width:180px;font-size:0.75rem;">💰 Ingresar dinero</button>
                        <button id="cajaBtnRealizarGasto" class="caja-btn warn" type="button" style="min-width:180px;font-size:0.75rem;">💸 Realizar gasto</button>
                    </div>
                </div>
            </section>'''

if old_gasto in html:
    html = html.replace(old_gasto, new_gasto)
    print("✅ cajaPanelGasto restaurado con sección Datos del turno")
else:
    print("❌ No se encontró cajaPanelGasto exacto")

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Listo. Longitud: {orig_len} → {len(html)}")
