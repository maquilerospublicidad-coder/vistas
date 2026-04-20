#!/usr/bin/env python3
"""Patch: 1) Remove reportes tabs, 2) Per-order production notes, 3) Delivery scan redesign."""

FILE = '/workspaces/vistas/mockup.html'

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

errors = []

# ============================================================
# PART 1: Remove Dashboard/Reportes tabs, show only Reportes section
# ============================================================

# 1a. Remove the tab buttons from header
old_head = '''            <div class="clientesmod-head-right" id="repHeadRight">
                <button id="repTabDash" class="clientesmod-btn primary" type="button" style="font-size:0.48rem;padding:4px 12px;">DASHBOARD</button>
                <button id="repTabRep" class="clientesmod-btn" type="button" style="font-size:0.48rem;padding:4px 12px;">REPORTES</button>
            </div>'''
new_head = '''            <div class="clientesmod-head-right" id="repHeadRight">
            </div>'''
if old_head in content:
    content = content.replace(old_head, new_head, 1)
    print("  1a. Tab buttons removed")
else:
    errors.append("1a: Could not find tab buttons in header")

# 1b. Change title from DASHBOARD to REPORTES
old_title = '<h2 id="reportesmodTitulo" class="clientesmod-title">DASHBOARD</h2>'
new_title = '<h2 id="reportesmodTitulo" class="clientesmod-title">REPORTES</h2>'
if old_title in content:
    content = content.replace(old_title, new_title, 1)
    print("  1b. Title changed to REPORTES")
else:
    errors.append("1b: Could not find DASHBOARD title")

# 1c. Hide dashboard section, show reportes section by default
old_dash = '<div id="repSeccionDashboard">'
new_dash = '<div id="repSeccionDashboard" style="display:none;">'
if old_dash in content:
    content = content.replace(old_dash, new_dash, 1)
    print("  1c. Dashboard section hidden")
else:
    errors.append("1c: Could not find repSeccionDashboard")

old_rep = '<div id="repSeccionReportes" style="display:none;">'
new_rep = '<div id="repSeccionReportes">'
if old_rep in content:
    content = content.replace(old_rep, new_rep, 1)
    print("  1c. Reportes section shown by default")
else:
    errors.append("1c: Could not find repSeccionReportes hidden")

# 1d. Update openReportesPopup to open reportes tab directly
old_switch = "switchRepTab(tab || 'dashboard');"
new_switch = "switchRepTab('reports');"
if old_switch in content:
    content = content.replace(old_switch, new_switch, 1)
    print("  1d. openReportesPopup updated")
else:
    errors.append("1d: Could not find switchRepTab call")

old_if_dash = "if (tab === 'dashboard') renderReportesModulo();"
new_if_dash = "// Dashboard tab removed"
if old_if_dash in content:
    content = content.replace(old_if_dash, new_if_dash, 1)
    print("  1d. Dashboard render removed")
else:
    errors.append("1d: Could not find dashboard render call")

# 1e. Make module cards smaller
old_card_css = '''        .rep-modulo-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
            padding: 20px 14px;
            border: 1px solid #e3e8f0;
            border-radius: 14px;
            background: #fff;
            cursor: pointer;
            transition: none;
            text-align: center;
            min-height: 130px;
            justify-content: center;
        }'''
new_card_css = '''        .rep-modulo-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            padding: 10px 8px;
            border: 1px solid #e3e8f0;
            border-radius: 10px;
            background: #fff;
            cursor: pointer;
            transition: none;
            text-align: center;
            min-height: 70px;
            justify-content: center;
        }'''
if old_card_css in content:
    content = content.replace(old_card_css, new_card_css, 1)
    print("  1e. Card CSS compacted")
else:
    errors.append("1e: Could not find card CSS")

old_ico_css = '''        .rep-modulo-ico {
            font-size: 2rem;
            line-height: 1;
        }'''
new_ico_css = '''        .rep-modulo-ico {
            font-size: 1.4rem;
            line-height: 1;
        }'''
if old_ico_css in content:
    content = content.replace(old_ico_css, new_ico_css, 1)
    print("  1e. Icon size reduced")
else:
    errors.append("1e: Could not find icon CSS")

# 1f. Reduce grid header
old_grid_header = '''                    <div style="text-align:center;padding:14px 0 6px;">
                        <h3 style="margin:0;font-size:0.85rem;font-weight:900;color:#1f2937;letter-spacing:0.3px;">CENTRO DE REPORTES</h3>
                        <p style="margin:4px 0 0;font-size:0.55rem;color:#6b7280;">Selecciona un módulo para generar un reporte detallado</p>
                    </div>'''
new_grid_header = '''                    <div style="text-align:center;padding:6px 0 2px;">
                        <p style="margin:0;font-size:0.52rem;color:#6b7280;">Selecciona un módulo para generar un reporte</p>
                    </div>'''
if old_grid_header in content:
    content = content.replace(old_grid_header, new_grid_header, 1)
    print("  1f. Grid header compacted")
else:
    errors.append("1f: Could not find grid header")

# 1g. Grid: 4 columns, smaller gaps
old_grid = "display:grid;grid-template-columns:repeat(3,1fr);gap:12px;padding:14px 30px;max-width:900px;margin:0 auto;"
new_grid = "display:grid;grid-template-columns:repeat(4,1fr);gap:8px;padding:6px 16px;max-width:960px;margin:0 auto;"
if old_grid in content:
    content = content.replace(old_grid, new_grid, 1)
    print("  1g. Grid to 4 columns")
else:
    errors.append("1g: Could not find grid style")

print("PART 1 done: Reportes tabs removed, grid optimized")

# ============================================================
# PART 2: Per-order production notes
# ============================================================

# 2a. Add a notes button to each production order card
old_order_actions = """                  (o.estado === 'pendiente' ? '<button class="prod-btn-action print" data-action="imprimir-instrucciones" data-id="'+esc(o.id)+'">🖨 IMPRIMIR ORDEN</button>' : '')+"""
new_order_actions = """                  '<button class="prod-btn-action" style="background:#fffbf5;border-color:#fde8c8;color:#92400e;" data-action="notas-orden" data-id="'+esc(o.id)+'">📝 Nota</button>'+
                  (o.estado === 'pendiente' ? '<button class="prod-btn-action print" data-action="imprimir-instrucciones" data-id="'+esc(o.id)+'">🖨 IMPRIMIR ORDEN</button>' : '')+"""
if old_order_actions in content:
    content = content.replace(old_order_actions, new_order_actions, 1)
    print("  2a. Notes button added to order cards")
else:
    errors.append("2a: Could not find order actions for notes button")

# 2b. Add the notes-orden action handler
old_action_handler = "                if(action==='iniciar') iniciarTrabajoOrden(docId);"
new_action_handler = """                if(action==='notas-orden') abrirPopupNotaOrden(orden);
                if(action==='iniciar') iniciarTrabajoOrden(docId);"""
if old_action_handler in content:
    content = content.replace(old_action_handler, new_action_handler, 1)
    print("  2b. Notes action handler added")
else:
    errors.append("2b: Could not find action handler for notas-orden")

# 2c. Add the popup function for per-order notes (before cargarOrdenes)
old_cargar = '    function cargarOrdenes() {'
new_cargar = '''    function abrirPopupNotaOrden(orden) {
        var existing = document.getElementById('popupNotaOrden');
        if (existing) existing.remove();
        var notasArr = [];
        try { notasArr = JSON.parse(orden.notasHistorial || '[]'); } catch(e) { notasArr = []; }
        if (!Array.isArray(notasArr)) notasArr = [];
        if (orden.notas && !notasArr.length) notasArr = [{texto: orden.notas, fecha: orden.creadoEn ? (orden.creadoEn.toDate ? orden.creadoEn.toDate().toLocaleString('es-MX') : String(orden.creadoEn)) : '', usuario: ''}];
        var histHtml = notasArr.length ? notasArr.map(function(n,i) {
            return '<div style="padding:6px 8px;background:#f9fafb;border:1px solid #e5e7eb;border-radius:6px;font-size:0.65rem;color:#374151;margin-bottom:4px;">'+
                '<div style="display:flex;justify-content:space-between;margin-bottom:2px;">'+
                    '<span style="font-weight:700;color:#6b7280;">'+(n.usuario||'Usuario')+'</span>'+
                    '<span style="color:#9ca3af;font-size:0.55rem;">'+(n.fecha||'')+'</span>'+
                '</div>'+
                '<div>'+esc(n.texto||'')+'</div>'+
            '</div>';
        }).join('') : '<div style="text-align:center;color:#9ca3af;font-size:0.65rem;padding:10px;">Sin notas</div>';
        var ov = document.createElement('div');
        ov.id = 'popupNotaOrden';
        ov.style.cssText = 'position:fixed;inset:0;z-index:99999;background:rgba(0,0,0,0.5);display:flex;justify-content:center;align-items:center;';
        ov.innerHTML = '<div style="background:#fff;border-radius:12px;padding:20px;width:min(92vw,420px);max-height:80vh;display:flex;flex-direction:column;box-shadow:0 8px 32px rgba(0,0,0,0.3);">'+
            '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">'+
                '<h3 style="margin:0;font-size:0.85rem;color:#1f2937;">\\u{1F4DD} Notas \\u2014 '+esc(orden.folio||'Orden')+'</h3>'+
                '<button id="notaOrdenCerrar" style="background:none;border:none;font-size:1.2rem;cursor:pointer;color:#6b7280;">\\u2715</button>'+
            '</div>'+
            '<div style="flex:1;overflow-y:auto;max-height:300px;margin-bottom:10px;" id="notaOrdenHistorial">'+histHtml+'</div>'+
            '<textarea id="notaOrdenTexto" rows="3" placeholder="Escribe una nota para esta orden..." style="border:1px solid #e5e7eb;border-radius:8px;padding:8px;font-size:0.7rem;font-family:inherit;resize:none;margin-bottom:8px;"></textarea>'+
            '<button id="notaOrdenGuardar" style="background:#ff9900;color:#fff;border:none;border-radius:8px;padding:8px 0;font-weight:800;font-size:0.72rem;cursor:pointer;">\\u{1F4BE} AGREGAR NOTA</button>'+
        '</div>';
        document.body.appendChild(ov);
        document.getElementById('notaOrdenCerrar').addEventListener('click', function() { ov.remove(); });
        ov.addEventListener('click', function(e) { if (e.target === ov) ov.remove(); });
        document.getElementById('notaOrdenGuardar').addEventListener('click', function() {
            var texto = document.getElementById('notaOrdenTexto').value.trim();
            if (!texto) return;
            var userName = localStorage.getItem('logged_user_name') || 'Produccion';
            var now = new Date().toLocaleString('es-MX');
            notasArr.push({texto: texto, fecha: now, usuario: userName});
            var db = getProdDB(); if (!db) return;
            db.collection(PROD_COLLECTION).doc(orden.id).update({
                notas: texto,
                notasHistorial: JSON.stringify(notasArr),
                actualizadoEn: window.firebase.firestore.FieldValue.serverTimestamp()
            }).then(function() {
                orden.notas = texto;
                orden.notasHistorial = JSON.stringify(notasArr);
                ov.remove();
                renderOrdenes();
            }).catch(function(err) { alert('Error: ' + err.message); });
        });
        document.getElementById('notaOrdenTexto').addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); document.getElementById('notaOrdenGuardar').click(); }
        });
    }

    function cargarOrdenes() {'''
if old_cargar in content:
    content = content.replace(old_cargar, new_cargar, 1)
    print("  2c. Notes popup function added")
else:
    errors.append("2c: Could not find cargarOrdenes for notes popup insertion")

# 2d. Show note count badge on orders that have notes
old_notas_display = """(o.notas?'<span style="grid-column:1/-1"><strong>Notas prod:</strong> '+esc(o.notas)+'</span>':'')"""
new_notas_display = """(function(){var nArr=[];try{nArr=JSON.parse(o.notasHistorial||'[]');}catch(e){}if(!Array.isArray(nArr))nArr=[];var cnt=nArr.length;return o.notas?'<span style="grid-column:1/-1"><strong>\\u{1F4DD} Última nota:</strong> '+esc(o.notas)+(cnt>1?' <span style="color:#ff9900;font-weight:700;">('+cnt+' notas)</span>':'')+'</span>':'';}())"""
if old_notas_display in content:
    content = content.replace(old_notas_display, new_notas_display, 1)
    print("  2d. Notes display updated with count badge")
else:
    errors.append("2d: Could not find old notes display in order card")

print("PART 2 done: Per-order notes added")

# ============================================================
# PART 3: Delivery module scan redesign
# ============================================================

# 3a. Replace the big scan button
old_scan_section = '''    <!-- Scan button below header -->
    <div style="padding:4px 8px 0;">
      <button id="entBtnAbrirPopupEtiqueta" type="button" style="width:100%;padding:10px 0;background:#ff9900;color:#fff;border:none;border-radius:10px;cursor:pointer;font-weight:800;font-size:0.78rem;">📷 Escanear Etiqueta</button>
    </div>'''
new_scan_section = '''    <!-- Scan buttons moved to header -->'''
if old_scan_section in content:
    content = content.replace(old_scan_section, new_scan_section, 1)
    print("  3a. Old scan section removed")
else:
    errors.append("3a: Could not find scan section below header")

# 3b. Add scan buttons to the header bar
old_header_end = '''      <span style="margin-left:auto;font-size:0.62rem;color:#64748b;font-weight:600;">Gestión y seguimiento de entregas a clientes</span>'''
new_header_end = '''      <span style="flex:1;font-size:0.55rem;color:#64748b;font-weight:600;">Gestión y seguimiento</span>
      <button id="entBtnScanConsulta" type="button" style="padding:5px 10px;background:#1e40af;color:#fff;border:none;border-radius:6px;cursor:pointer;font-weight:700;font-size:0.55rem;">🔍 CONSULTA</button>
      <button id="entBtnAbrirPopupEtiqueta" type="button" style="padding:5px 10px;background:#ff9900;color:#fff;border:none;border-radius:6px;cursor:pointer;font-weight:700;font-size:0.55rem;">📷 RECIBIR</button>'''
if old_header_end in content:
    content = content.replace(old_header_end, new_header_end, 1)
    print("  3b. Scan buttons added to header")
else:
    errors.append("3b: Could not find header end for scan buttons")

# 3c. Replace the scan popup creation and handler
old_scan_popup = '''        btnAbrir.addEventListener('click', function() {
            var existing = document.getElementById('popupEtiquetaScan');
            if (existing) existing.remove();
            var overlay = document.createElement('div');
            overlay.id = 'popupEtiquetaScan';
            overlay.style.cssText = 'position:fixed;inset:0;z-index:99999;background:rgba(0,0,0,0.6);display:flex;justify-content:center;align-items:center;';
            overlay.innerHTML = '<div style="background:#fff;border-radius:14px;padding:24px;width:min(94vw,440px);max-height:85vh;overflow-y:auto;box-shadow:0 8px 32px rgba(0,0,0,0.3);">'+
                '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">'+
                    '<h3 style="margin:0;font-size:1rem;color:#1f2937;">🏷 Escanear Etiqueta de Entrega</h3>'+
                    '<button id="etqPopupCerrar" style="background:none;border:none;font-size:1.3rem;cursor:pointer;color:#6b7280;">✕</button>'+
                '</div>'+
                '<div id="etqPopupQrReader" style="width:100%;max-width:320px;margin:0 auto 10px;border-radius:8px;overflow:hidden;"></div>'+
                '<div id="etqPopupStatus" style="font-size:0.72rem;color:#ff9900;font-weight:700;text-align:center;margin-bottom:10px;">Iniciando cámara...</div>'+
                '<div style="display:flex;gap:6px;margin-bottom:10px;">'+
                    '<input type="text" id="etqPopupManualInput" placeholder="Código de barras o folio..." style="flex:1;border:1px solid #e5e7eb;border-radius:8px;padding:8px 10px;font-size:0.72rem;">'+
                    '<button id="etqPopupBtnManual" style="padding:8px 14px;background:#ff9900;color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:700;font-size:0.72rem;">→</button>'+
                '</div>'+
            '</div>';
            document.body.appendChild(overlay);'''

new_scan_popup = '''        function abrirScanPopup(modo) {
            var existing = document.getElementById('popupEtiquetaScan');
            if (existing) existing.remove();
            var esRecibir = modo === 'recibir';
            var titulo = esRecibir ? '📦 RECIBIR MERCANCÍA' : '🔍 CONSULTA DE ORDEN';
            var colorBtn = esRecibir ? '#ff9900' : '#1e40af';
            var overlay = document.createElement('div');
            overlay.id = 'popupEtiquetaScan';
            overlay.dataset.modo = modo;
            overlay.style.cssText = 'position:fixed;inset:0;z-index:99999;background:rgba(0,0,0,0.6);display:flex;justify-content:center;align-items:center;';
            overlay.innerHTML = '<div style="background:#fff;border-radius:12px;padding:18px;width:min(92vw,400px);max-height:80vh;overflow-y:auto;box-shadow:0 8px 32px rgba(0,0,0,0.3);">'+
                '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">'+
                    '<h3 style="margin:0;font-size:0.85rem;color:#1f2937;">'+titulo+'</h3>'+
                    '<button id="etqPopupCerrar" style="background:none;border:none;font-size:1.2rem;cursor:pointer;color:#6b7280;">✕</button>'+
                '</div>'+
                '<div id="etqPopupQrReader" style="width:100%;max-width:280px;margin:0 auto 8px;border-radius:8px;overflow:hidden;"></div>'+
                '<div id="etqPopupStatus" style="font-size:0.65rem;color:'+colorBtn+';font-weight:700;text-align:center;margin-bottom:8px;">Iniciando cámara...</div>'+
                '<div style="display:flex;gap:6px;margin-bottom:8px;">'+
                    '<input type="text" id="etqPopupManualInput" placeholder="Folio o código de barras..." style="flex:1;border:1px solid #e5e7eb;border-radius:8px;padding:7px 10px;font-size:0.68rem;" autofocus>'+
                    '<button id="etqPopupBtnManual" style="padding:7px 12px;background:'+colorBtn+';color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:700;font-size:0.68rem;">→</button>'+
                '</div>'+
                '<div id="etqPopupResult" style="display:none;margin-top:6px;"></div>'+
            '</div>';
            document.body.appendChild(overlay);
            setTimeout(function(){ var inp=document.getElementById('etqPopupManualInput'); if(inp)inp.focus(); },100);'''

if old_scan_popup in content:
    content = content.replace(old_scan_popup, new_scan_popup, 1)
    print("  3c. Scan popup redesigned with modes")
else:
    errors.append("3c: Could not find old scan popup handler")

# 3d. Replace buscarYMostrarEtiqueta
old_buscar = '''            function buscarYMostrarEtiqueta(codigo) {
                var entrega = allEntregas.find(function(e) {
                    return e.folioProduccion === codigo || e.codigoBarras === codigo || e.id === codigo;
                });
                if (entrega) {
                    cerrarPopup();
                    mostrarEtiquetaEntrega(entrega);
                } else {
                    statusEl.textContent = '❌ No se encontró entrega con código: ' + codigo;
                    statusEl.style.color = '#dc2626';
                    setTimeout(function() { statusEl.textContent = 'Listo para escanear'; statusEl.style.color = '#ff9900'; }, 2500);
                }
            }'''

new_buscar = '''            function buscarYMostrarEtiqueta(codigo) {
                var entrega = allEntregas.find(function(e) {
                    return e.folioProduccion === codigo || e.codigoBarras === codigo || e.id === codigo;
                });
                var esRecibir = overlay.dataset.modo === 'recibir';
                if (!entrega) {
                    statusEl.textContent = '❌ No se encontró entrega con código: ' + codigo;
                    statusEl.style.color = '#dc2626';
                    setTimeout(function() { statusEl.textContent = 'Listo para escanear'; statusEl.style.color = esRecibir?'#ff9900':'#1e40af'; }, 2500);
                    return;
                }
                if (esRecibir) {
                    if (entrega.recibidoPorRepartidor) {
                        statusEl.textContent = '⚠️ '+escEnt(entrega.folioProduccion||entrega.id)+' ya fue recibida';
                        statusEl.style.color = '#f59e0b';
                        setTimeout(function(){statusEl.textContent='Listo para escanear';statusEl.style.color='#ff9900';},2500);
                        return;
                    }
                    var nuevoEstado = entrega.estado === 'pendiente' ? 'en_camino' : entrega.estado;
                    var db = getEntDB(); if(!db) return;
                    db.collection(ENT_COLLECTION).doc(entrega.id).update({
                        estado: nuevoEstado,
                        recibidoPorRepartidor: true,
                        fechaRecepcion: new Date().toISOString(),
                        actualizadoEn: window.firebase.firestore.FieldValue.serverTimestamp()
                    }).then(function(){
                        entrega.estado = nuevoEstado;
                        entrega.recibidoPorRepartidor = true;
                        statusEl.textContent = '✅ '+escEnt(entrega.folioProduccion||entrega.id)+' — MERCANCÍA RECIBIDA';
                        statusEl.style.color = '#16a34a';
                        renderEntregas(); actualizarResumenEntregas();
                        var inp=document.getElementById('etqPopupManualInput');
                        if(inp){inp.value='';inp.focus();}
                        setTimeout(function(){statusEl.textContent='Listo - escanear siguiente';statusEl.style.color='#ff9900';},2000);
                    }).catch(function(err){statusEl.textContent='Error: '+err.message;statusEl.style.color='#dc2626';});
                } else {
                    var resultEl=document.getElementById('etqPopupResult');
                    if(resultEl){
                        var estadoLabel={pendiente:'📬 Pendiente',en_camino:'🚚 En Camino',entregada:'✅ Entregada',no_entregada:'❌ No Entregada'};
                        resultEl.style.display='block';
                        resultEl.innerHTML='<div style="background:#f9fafb;border:1px solid #e5e7eb;border-radius:8px;padding:10px;font-size:0.62rem;">'+
                            '<div style="font-weight:900;font-size:0.75rem;color:#1f2937;margin-bottom:6px;">'+escEnt(entrega.folioProduccion||entrega.id)+'</div>'+
                            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:4px;">'+
                                '<span><strong>Cliente:</strong> '+escEnt(entrega.cliente||'—')+'</span>'+
                                '<span><strong>Teléfono:</strong> '+escEnt(entrega.telefono||'—')+'</span>'+
                                '<span><strong>Producto:</strong> '+escEnt(entrega.producto||'—')+'</span>'+
                                '<span><strong>Cantidad:</strong> '+escEnt(entrega.cantidad||'—')+'</span>'+
                                '<span><strong>Estado:</strong> '+(estadoLabel[entrega.estado]||escEnt(entrega.estado))+'</span>'+
                                '<span><strong>Entrega:</strong> '+escEnt(entrega.fechaEntrega||'—')+'</span>'+
                                '<span style="grid-column:1/-1"><strong>Dirección:</strong> '+escEnt(entrega.direccion||'—')+'</span>'+
                                '<span><strong>Adeudo:</strong> <span style="color:#ef5350;font-weight:700;">$'+escEnt(entrega.adeudo||'0')+'</span></span>'+
                                (entrega.recibidoPorRepartidor?'<span><strong>Recibida:</strong> <span style="color:#16a34a;font-weight:700;">SÍ</span></span>':'<span><strong>Recibida:</strong> <span style="color:#dc2626;">NO</span></span>')+
                            '</div>'+
                        '</div>';
                        statusEl.textContent='✅ Orden encontrada';
                        statusEl.style.color='#16a34a';
                        var inp=document.getElementById('etqPopupManualInput');
                        if(inp){inp.value='';inp.focus();}
                    }
                }
            }'''
if old_buscar in content:
    content = content.replace(old_buscar, new_buscar, 1)
    print("  3d. buscarYMostrarEtiqueta updated with modes")
else:
    errors.append("3d: Could not find buscarYMostrarEtiqueta function")

# 3e. Replace closing of scan popup to support both buttons
old_listener_end = '''            document.getElementById('etqPopupManualInput').addEventListener('keydown', function(e) {
                if (e.key === 'Enter') { var code = this.value.trim(); if (code) { buscarYMostrarEtiqueta(code); this.value = ''; } }
            });
        });
    })();'''

new_listener_end = '''            document.getElementById('etqPopupManualInput').addEventListener('keydown', function(e) {
                if (e.key === 'Enter') { var code = this.value.trim(); if (code) { buscarYMostrarEtiqueta(code); this.value = ''; } }
            });
        }

        btnAbrir.addEventListener('click', function() { abrirScanPopup('recibir'); });
        var btnConsulta = document.getElementById('entBtnScanConsulta');
        if (btnConsulta) btnConsulta.addEventListener('click', function() { abrirScanPopup('consulta'); });
    })();'''

if old_listener_end in content:
    content = content.replace(old_listener_end, new_listener_end, 1)
    print("  3e. Scan event listeners updated")
else:
    errors.append("3e: Could not find scan listener end block")

# 3f. Update en_camino buttons
old_en_camino_btn = """            else if (e.estado==='en_camino') nextBtn = '<button class="entrega-btn nav" data-action="cambiar-estado" data-id="'+escEnt(e.id)+'" data-nuevo="entregada" style="background:rgba(76,175,80,0.15);border-color:rgba(76,175,80,0.4);color:#66bb6a;">✅ Marcar Entregada</button>' +
                '<button class="entrega-btn del" data-action="cambiar-estado" data-id="'+escEnt(e.id)+'" data-nuevo="no_entregada">❌ No Entregada</button>';"""

new_en_camino_btn = """            else if (e.estado==='en_camino') nextBtn = '<button class="entrega-btn nav" data-action="escanear-entregar" data-id="'+escEnt(e.id)+'" style="background:rgba(76,175,80,0.15);border-color:rgba(76,175,80,0.4);color:#66bb6a;">📷 ENTREGAR</button>' +
                '<button class="entrega-btn del" data-action="cambiar-estado" data-id="'+escEnt(e.id)+'" data-nuevo="no_entregada">❌ No Entregada</button>';"""

if old_en_camino_btn in content:
    content = content.replace(old_en_camino_btn, new_en_camino_btn, 1)
    print("  3f. En camino buttons updated")
else:
    errors.append("3f: Could not find en_camino buttons")

# 3g. Update pendiente buttons
old_pendiente_btn = """            if (e.estado==='pendiente') nextBtn = '<button class="entrega-btn nav" data-action="cambiar-estado" data-id="'+escEnt(e.id)+'" data-nuevo="en_camino" style="background:rgba(255,193,7,0.15);border-color:rgba(255,193,7,0.4);color:#f59e0b;">🚚 Marcar En Camino</button>';"""

new_pendiente_btn = """            if (e.estado==='pendiente') nextBtn = (e.recibidoPorRepartidor?'<span style="font-size:0.52rem;color:#16a34a;font-weight:700;padding:4px 8px;">✅ Recibida</span>':'<button class="entrega-btn nav" data-action="recibir-mercancia" data-id="'+escEnt(e.id)+'" style="background:rgba(255,153,0,0.15);border-color:rgba(255,153,0,0.4);color:#ff9900;">📦 Recibir</button>')+
                '<button class="entrega-btn nav" data-action="cambiar-estado" data-id="'+escEnt(e.id)+'" data-nuevo="en_camino" style="background:rgba(255,193,7,0.15);border-color:rgba(255,193,7,0.4);color:#f59e0b;">🚚 En Camino</button>';"""

if old_pendiente_btn in content:
    content = content.replace(old_pendiente_btn, new_pendiente_btn, 1)
    print("  3g. Pendiente buttons updated with Recibir")
else:
    errors.append("3g: Could not find pendiente buttons")

# 3h. Add action handlers for new buttons
old_action_cambiar = "                if (action === 'cambiar-estado') {"
new_action_cambiar = """                if (action === 'recibir-mercancia') {
                    var db = getEntDB(); if (!db) return;
                    db.collection(ENT_COLLECTION).doc(docId).update({
                        recibidoPorRepartidor: true,
                        fechaRecepcion: new Date().toISOString(),
                        actualizadoEn: window.firebase.firestore.FieldValue.serverTimestamp()
                    }).then(function() {
                        entrega.recibidoPorRepartidor = true;
                        renderEntregas(); actualizarResumenEntregas();
                    }).catch(function(err) { alert('Error: '+err.message); });
                    return;
                }
                if (action === 'escanear-entregar') {
                    verificarEntregaConGeo(entrega);
                    return;
                }
                if (action === 'cambiar-estado') {"""
if old_action_cambiar in content:
    content = content.replace(old_action_cambiar, new_action_cambiar, 1)
    print("  3h. New action handlers added")
else:
    errors.append("3h: Could not find cambiar-estado action handler")

print("PART 3 done: Delivery scan redesigned")

# ============================================================
# WRITE
# ============================================================
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "="*60)
if errors:
    print("PATCH APPLIED WITH WARNINGS:")
    for e in errors:
        print("  - " + e)
else:
    print("ALL PATCHES APPLIED SUCCESSFULLY!")
print("="*60)
