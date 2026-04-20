#!/usr/bin/env python3
"""
Fix Dashboard/Reportes issues:
1. Dashboard opens reports tab instead of dashboard tab
2. Reportes exit goes to muestrario instead of main menu
3. Two back arrows visible in Reportes (hide main back when report expanded)
4. Add Dashboard/Reportes tab buttons in header
"""
FILE = '/workspaces/vistas/mockup.html'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# ── FIX 1: openReportesPopup always uses 'reports' tab, ignoring parameter ──
OLD1 = """    const openReportesPopup = (tab) => {
        if (!popupReportesModulo) return;
        loadProveedoresModulo();
        popupReportesModulo.style.display = 'flex';
        popupReportesModulo.setAttribute('aria-hidden', 'false');
        document.body.classList.add('popup-open');
        document.documentElement.classList.add('popup-open');
        switchRepTab('reports');
        // Dashboard tab removed
    };"""

NEW1 = """    const openReportesPopup = (tab) => {
        if (!popupReportesModulo) return;
        loadProveedoresModulo();
        popupReportesModulo.style.display = 'flex';
        popupReportesModulo.setAttribute('aria-hidden', 'false');
        document.body.classList.add('popup-open');
        document.documentElement.classList.add('popup-open');
        switchRepTab(tab === 'dashboard' ? 'dashboard' : 'reports');
    };"""

if OLD1 in content:
    content = content.replace(OLD1, NEW1, 1)
    changes += 1
    print("✅ 1: openReportesPopup now respects tab parameter")
else:
    print("⚠ 1: openReportesPopup marker not found")

# ── FIX 2: closeReportesPopup does NOT call mostrarInicioSistema ──
OLD2 = """    const closeReportesPopup = () => {
        if (!popupReportesModulo) return;
        popupReportesModulo.style.display = 'none';
        popupReportesModulo.setAttribute('aria-hidden', 'true');"""

NEW2 = """    const closeReportesPopup = () => {
        if (!popupReportesModulo) return;
        popupReportesModulo.style.display = 'none';
        popupReportesModulo.setAttribute('aria-hidden', 'true');
        if (typeof mostrarInicioSistema === 'function') mostrarInicioSistema();"""

if OLD2 in content:
    content = content.replace(OLD2, NEW2, 1)
    changes += 1
    print("✅ 2: closeReportesPopup now calls mostrarInicioSistema")
else:
    print("⚠ 2: closeReportesPopup marker not found")

# ── FIX 3: Hide main back arrow when a report is expanded, show when going back ──
# In the reportesmodBack click handler, the logic already handles going back from expanded view.
# We need to hide reportesmodBack when a report is shown and show when going back.
# The best place is in switchRepTab and volverAModulosReportes and where reports are opened.

# 3a: In the back button handler, we need to make sure it always goes to main menu from dashboard
OLD3A = """    if (reportesmodBack) {
        reportesmodBack.addEventListener('click', () => {
            // Si estamos viendo un reporte expandido, volver a la cuadrícula
            const vistaRep = document.getElementById('repVistaReporte');
            if (vistaRep && vistaRep.style.display !== 'none' && repTabActivo === 'reports') {
                volverAModulosReportes();
                return;
            }
            closeReportesPopup();
        });
    }"""

NEW3A = """    if (reportesmodBack) {
        reportesmodBack.addEventListener('click', () => {
            // Si estamos viendo un reporte expandido, volver a la cuadrícula
            const vistaRep = document.getElementById('repVistaReporte');
            if (vistaRep && vistaRep.style.display !== 'none' && repTabActivo === 'reports') {
                volverAModulosReportes();
                return;
            }
            closeReportesPopup();
        });
    }
    // Hide main back arrow when report expanded, show when back
    var _origAbrirReporteVista = null;
    (function(){
        var vistaRep = document.getElementById('repVistaReporte');
        if(!vistaRep) return;
        var obs = new MutationObserver(function(){
            var expanded = vistaRep.style.display !== 'none';
            if(reportesmodBack) reportesmodBack.style.display = expanded ? 'none' : '';
        });
        obs.observe(vistaRep, {attributes:true, attributeFilter:['style']});
    })();"""

if OLD3A in content:
    content = content.replace(OLD3A, NEW3A, 1)
    changes += 1
    print("✅ 3: Hide main back arrow when report view is expanded")
else:
    print("⚠ 3: reportesmodBack handler marker not found")

# ── FIX 4: Add Dashboard/Reportes tab buttons in the header ──
OLD4 = """            <div class="clientesmod-head-right" id="repHeadRight">
            </div>"""

NEW4 = """            <div class="clientesmod-head-right" id="repHeadRight">
                <button id="repTabDash" class="clientesmod-btn primary" type="button" style="font-size:0.55rem;padding:5px 12px;">📈 DASHBOARD</button>
                <button id="repTabRep" class="clientesmod-btn" type="button" style="font-size:0.55rem;padding:5px 12px;">📊 REPORTES</button>
            </div>"""

if OLD4 in content:
    content = content.replace(OLD4, NEW4, 1)
    changes += 1
    print("✅ 4: Added Dashboard/Reportes tab buttons in header")
else:
    print("⚠ 4: repHeadRight marker not found")

# ── FIX 5: Fix abrirRegistro which always maps DASHBOARD → REPORTES ──
OLD5 = """        abrirModuloPrincipal(key === 'DASHBOARD' ? 'REPORTES' : key);"""
NEW5 = """        abrirModuloPrincipal(key);"""

if OLD5 in content:
    content = content.replace(OLD5, NEW5, 1)
    changes += 1
    print("✅ 5: abrirRegistro no longer redirects DASHBOARD to REPORTES")
else:
    print("⚠ 5: abrirRegistro marker not found")

if changes:
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"\n✅ Done — {changes} change(s) applied")
else:
    print("\n❌ No changes made")
