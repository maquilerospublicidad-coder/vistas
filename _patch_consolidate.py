#!/usr/bin/env python3
"""
Consolidation Patch: Merge 20 sidebar sections → 8 grouped modules
- Localización: Localización + Geocercas (toggle) + Historial (popup)
- Pedidos: Pedidos + Reagendamiento + Inv. Vehículo (sub-tabs)
- Repartidores: Repartidores + Gastos + Checks + Penalizaciones + Kilometraje (sub-tabs)
- Reportes: KPIs + Reportes (sub-tabs)
- Alertas: Alertas + Comunicación (sub-tabs)
- Configuración: Zonas + Horarios + Conceptos (sub-tabs)
- Dashboard & Rutas: unchanged
"""

FILE = '/workspaces/vistas/mockup.html'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()
errors = []
count = 0

# ====================================================================
# STEP 1: Add sub-tab + toggle CSS before the </style> that precedes
# the panelControlRepartidores div
# ====================================================================
CSS_ADDITION = """
  /* Sub-tabs & toggle for merged sections */
  #panelControlRepartidores .cr-subtabs { display:flex; gap:2px; background:#e2e8f0; border-radius:8px; padding:3px; margin-bottom:14px; overflow-x:auto; flex-shrink:0; }
  #panelControlRepartidores .cr-subtab { flex:none; padding:7px 14px; border:none; background:transparent; border-radius:6px; font-size:0.50rem; font-weight:700; color:#64748b; cursor:pointer; transition:all 0.15s; white-space:nowrap; }
  #panelControlRepartidores .cr-subtab:hover { background:rgba(255,255,255,0.6); color:#334155; }
  #panelControlRepartidores .cr-subtab.active { background:#fff; color:#1e40af; box-shadow:0 1px 3px rgba(0,0,0,0.1); }
  #panelControlRepartidores .cr-toggle-group { display:inline-flex; gap:2px; background:#1e293b; border-radius:8px; padding:2px; }
  #panelControlRepartidores .cr-toggle { padding:6px 14px; border:none; background:transparent; border-radius:6px; font-size:0.50rem; font-weight:700; color:#94a3b8; cursor:pointer; transition:all 0.15s; }
  #panelControlRepartidores .cr-toggle:hover { color:#cbd5e1; }
  #panelControlRepartidores .cr-toggle.active { background:#3b82f6; color:#fff; }
"""

css_marker = '  #panelControlRepartidores .cr-header-bar { display:flex; align-items:center; gap:10px; margin-bottom:14px; flex-wrap:wrap; }\n</style>'
if css_marker in content:
    content = content.replace(css_marker, '  #panelControlRepartidores .cr-header-bar { display:flex; align-items:center; gap:10px; margin-bottom:14px; flex-wrap:wrap; }' + CSS_ADDITION + '</style>', 1)
    count += 1
    print(f"  {count}. CSS sub-tab/toggle styles added")
else:
    errors.append("CSS marker not found")

# ====================================================================
# STEP 2: Replace sidebar buttons (20 → 8)
# ====================================================================
OLD_SIDEBAR = """        <div style="padding:12px 14px 8px;font-size:0.48rem;font-weight:800;color:#475569;text-transform:uppercase;letter-spacing:1px;">Módulos</div>
        <button class="cr-sidebar-btn active" data-cr-section="dashboard"><span class="cr-ico">📊</span> Dashboard</button>
        <button class="cr-sidebar-btn" data-cr-section="localizacion"><span class="cr-ico">🗺</span> Localización</button>
        <button class="cr-sidebar-btn" data-cr-section="pedidos"><span class="cr-ico">📦</span> Pedidos</button>
        <button class="cr-sidebar-btn" data-cr-section="conceptos"><span class="cr-ico">📋</span> Conceptos Visita</button>
        <button class="cr-sidebar-btn" data-cr-section="zonas"><span class="cr-ico">🏷</span> Zonas</button>
        <button class="cr-sidebar-btn" data-cr-section="geocercas"><span class="cr-ico">📍</span> Geocercas</button>
        <button class="cr-sidebar-btn" data-cr-section="gastos"><span class="cr-ico">💰</span> Gastos Empleado</button>
        <button class="cr-sidebar-btn" data-cr-section="horarios"><span class="cr-ico">🕐</span> Horarios</button>
        <button class="cr-sidebar-btn" data-cr-section="checks"><span class="cr-ico">✅</span> Checks Asistencia</button>
        <button class="cr-sidebar-btn" data-cr-section="repartidores"><span class="cr-ico">👥</span> Repartidores</button>
        <button class="cr-sidebar-btn" data-cr-section="rutas"><span class="cr-ico">🛣</span> Rutas</button>
        <button class="cr-sidebar-btn" data-cr-section="penalizaciones"><span class="cr-ico">⚠️</span> Penalizaciones</button>
        <div style="padding:8px 14px 4px;font-size:0.42rem;font-weight:800;color:#475569;text-transform:uppercase;letter-spacing:1px;border-top:1px solid rgba(255,255,255,0.06);margin-top:4px;">Avanzado</div>
        <button class="cr-sidebar-btn" data-cr-section="historial"><span class="cr-ico">📜</span> Historial Cliente</button>
        <button class="cr-sidebar-btn" data-cr-section="kpis"><span class="cr-ico">📈</span> KPIs</button>
        <button class="cr-sidebar-btn" data-cr-section="alertas"><span class="cr-ico">🔔</span> Alertas</button>
        <button class="cr-sidebar-btn" data-cr-section="inventario"><span class="cr-ico">📋</span> Inv. Vehículo</button>
        <button class="cr-sidebar-btn" data-cr-section="reagendar"><span class="cr-ico">📅</span> Reagendamiento</button>
        <button class="cr-sidebar-btn" data-cr-section="reportes"><span class="cr-ico">📊</span> Reportes</button>
        <button class="cr-sidebar-btn" data-cr-section="comunicacion"><span class="cr-ico">💬</span> Comunicación</button>
        <button class="cr-sidebar-btn" data-cr-section="kilometraje"><span class="cr-ico">🛣️</span> Kilometraje</button>"""

NEW_SIDEBAR = """        <div style="padding:12px 14px 8px;font-size:0.42rem;font-weight:800;color:#475569;text-transform:uppercase;letter-spacing:1px;">Módulos</div>
        <button class="cr-sidebar-btn active" data-cr-section="dashboard"><span class="cr-ico">📊</span> Dashboard</button>
        <button class="cr-sidebar-btn" data-cr-section="localizacion"><span class="cr-ico">🗺</span> Localización</button>
        <button class="cr-sidebar-btn" data-cr-section="pedidos"><span class="cr-ico">📦</span> Pedidos</button>
        <button class="cr-sidebar-btn" data-cr-section="repartidores"><span class="cr-ico">👥</span> Repartidores</button>
        <button class="cr-sidebar-btn" data-cr-section="rutas"><span class="cr-ico">🛣</span> Rutas</button>
        <button class="cr-sidebar-btn" data-cr-section="reportes"><span class="cr-ico">📈</span> Reportes & KPIs</button>
        <button class="cr-sidebar-btn" data-cr-section="alertas"><span class="cr-ico">🔔</span> Alertas & Com.</button>
        <button class="cr-sidebar-btn" data-cr-section="config"><span class="cr-ico">⚙️</span> Configuración</button>"""

if OLD_SIDEBAR in content:
    content = content.replace(OLD_SIDEBAR, NEW_SIDEBAR, 1)
    count += 1
    print(f"  {count}. Sidebar consolidated (20 → 8 buttons)")
else:
    errors.append("Sidebar text not found")

# ====================================================================
# STEP 3: Insert sub-tab bar div right after <div class="cr-main">
# ====================================================================
MAIN_OPEN = '      <div class="cr-main">\n'
MAIN_OPEN_NEW = '      <div class="cr-main">\n        <div id="crSubTabBar" style="display:none;flex-shrink:0;"></div>\n'

if MAIN_OPEN in content:
    content = content.replace(MAIN_OPEN, MAIN_OPEN_NEW, 1)
    count += 1
    print(f"  {count}. Sub-tab bar div inserted")
else:
    errors.append("cr-main opening not found")

# ====================================================================
# STEP 4: Add toggle bar to Localizacion section (replace the card header)
# and add Geocercas-like client list view
# ====================================================================
OLD_LOC_SECTION = """        <div class="cr-section" id="crSecLocalizacion" data-cr-section="localizacion">
          <div class="cr-card">
            <h3>🗺 Mapa General — Ubicación de Vendedores/Repartidores</h3>
            <div id="crMapaGeneral" class="cr-map-placeholder">
              <div style="text-align:center;">
                <div style="font-size:2rem;margin-bottom:8px;">🗺</div>
                <div>Cargando mapa...</div>
                <div style="font-size:0.5rem;color:#94a3b8;margin-top:4px;">Se mostrarán las ubicaciones en tiempo real de los repartidores</div>
              </div>
            </div>
          </div>
          <div class="cr-card">
            <h3>📡 Repartidores en Ruta</h3>
            <div id="crLocRepartidoresEnRuta" style="font-size:0.55rem;color:#64748b;">Sin datos de ubicación</div>
          </div>
        </div>"""

NEW_LOC_SECTION = """        <div class="cr-section" id="crSecLocalizacion" data-cr-section="localizacion">
          <div class="cr-header-bar" style="margin-bottom:10px;">
            <div class="cr-toggle-group" id="crLocToggle">
              <button class="cr-toggle active" data-loc="repartidores">🚚 Repartidores</button>
              <button class="cr-toggle" data-loc="clientes">📍 Clientes</button>
            </div>
            <select id="crLocFiltroZona" class="cr-select"><option value="">Todas las zonas</option></select>
            <input id="crLocBuscar" type="text" class="cr-input" placeholder="🔍 Buscar..." style="max-width:200px;">
          </div>
          <div class="cr-card">
            <div id="crMapaGeneral" class="cr-map-placeholder" style="height:400px;">
              <div style="text-align:center;">
                <div style="font-size:2rem;margin-bottom:8px;">🗺</div>
                <div>Mapa en tiempo real</div>
                <div style="font-size:0.5rem;color:#94a3b8;margin-top:4px;">Alterna entre vista de repartidores y clientes</div>
              </div>
            </div>
          </div>
          <!-- Vista: Repartidores -->
          <div id="crLocViewReps" class="cr-card">
            <h3>📡 Repartidores en Ruta</h3>
            <div id="crLocRepartidoresEnRuta" style="font-size:0.55rem;color:#64748b;">Sin datos de ubicación</div>
          </div>
          <!-- Vista: Clientes -->
          <div id="crLocViewClientes" class="cr-card" style="display:none;">
            <h3>📍 Clientes por Zona</h3>
            <p style="font-size:0.52rem;color:#64748b;margin:0 0 8px 0;">Haz clic en <strong>"📜 Historial"</strong> para ver las entregas de un cliente.</p>
            <div id="crGeocercaResumen" style="font-size:0.55rem;color:#64748b;margin-bottom:10px;">Cargando...</div>
            <div id="crLocClientesList" style="display:flex;flex-direction:column;gap:6px;"></div>
          </div>
        </div>"""

if OLD_LOC_SECTION in content:
    content = content.replace(OLD_LOC_SECTION, NEW_LOC_SECTION, 1)
    count += 1
    print(f"  {count}. Localización section enhanced with toggle")
else:
    errors.append("Old Localizacion section not found")

# ====================================================================
# STEP 5: Add Historial Popup HTML before </div> <!-- /cr-main -->
# ====================================================================
HIST_POPUP = """
        <!-- Historial Popup Overlay -->
        <div id="crHistPopup" style="display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);z-index:10001;">
          <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:#fff;border-radius:16px;max-width:750px;width:95%;max-height:85vh;overflow-y:auto;padding:24px;box-shadow:0 25px 50px rgba(0,0,0,0.25);">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
              <h3 style="margin:0;font-size:0.75rem;font-weight:900;color:#0f172a;">📜 Historial de Entregas</h3>
              <button id="crHistPopupClose" style="background:none;border:1px solid #e2e8f0;border-radius:8px;width:32px;height:32px;font-size:1.1rem;cursor:pointer;color:#64748b;display:flex;align-items:center;justify-content:center;">&times;</button>
            </div>
            <div id="crHistPopupClienteInfo" style="font-weight:800;font-size:0.65rem;color:#1e40af;margin-bottom:12px;"></div>
            <div id="crHistPopupStats" style="display:flex;gap:10px;margin-bottom:14px;"></div>
            <div id="crHistPopupBody">Cargando entregas...</div>
          </div>
        </div>

"""

MAIN_CLOSE = '      </div> <!-- /cr-main -->'
if MAIN_CLOSE in content:
    content = content.replace(MAIN_CLOSE, HIST_POPUP + MAIN_CLOSE, 1)
    count += 1
    print(f"  {count}. Historial popup HTML added")
else:
    errors.append("cr-main close not found")

# ====================================================================
# STEP 6: Replace sidebar handler + renderActiveSection + add merged logic
# The JS block to replace: from sidebarBtns through renderActiveSection
# ====================================================================
OLD_JS_HANDLER = """    var sidebarBtns = panel.querySelectorAll('.cr-sidebar-btn[data-cr-section]');
    var sections = panel.querySelectorAll('.cr-section[data-cr-section]');
    sidebarBtns.forEach(function(btn){
        btn.addEventListener('click',function(){
            sidebarBtns.forEach(function(b){b.classList.remove('active');});
            btn.classList.add('active');
            var target = btn.dataset.crSection;
            sections.forEach(function(s){s.classList.toggle('active',s.dataset.crSection===target);});
            renderActiveSection();
        });
    });
    function getActiveSection(){
        var active = panel.querySelector('.cr-sidebar-btn.active');
        return active ? active.dataset.crSection : 'dashboard';
    }
    function renderActiveSection(){
        var sec = getActiveSection();
        populateZonaSelects();
        populateRepSelects();
        if(sec==='dashboard') renderDashboard();
        else if(sec==='localizacion') renderLocalizacion();
        else if(sec==='pedidos') renderPedidos();
        else if(sec==='conceptos') renderConceptos();
        else if(sec==='zonas') renderZonas();
        else if(sec==='geocercas') renderGeocercas();
        else if(sec==='gastos') renderGastos();
        else if(sec==='horarios') renderHorarios();
        else if(sec==='checks') renderChecks();
        else if(sec==='repartidores') renderRepartidoresSection();
        else if(sec==='rutas') renderRutas();
        else if(sec==='penalizaciones') renderPenalizacionesSec();
        else if(sec==='historial') renderHistorial();
        else if(sec==='kpis') renderKpis();
        else if(sec==='alertas') renderAlertas();
        else if(sec==='inventario') renderInventario();
        else if(sec==='reagendar') renderReagendamiento();
        else if(sec==='reportes') renderReportes();
        else if(sec==='comunicacion') renderComunicacion();
        else if(sec==='kilometraje') renderKilometraje();
        updateSidebarResumen();
    }"""

NEW_JS_HANDLER = """    // ── SECTION GROUPS (merged modules) ──
    var SECTION_GROUPS = {
        dashboard:     { sections:['dashboard'] },
        localizacion:  { sections:['localizacion'] },
        pedidos:       { sections:['pedidos','reagendar','inventario'],         tabs:['📦 Listado','📅 Reagendar','📋 Inv. Vehículo'] },
        repartidores:  { sections:['repartidores','gastos','checks','penalizaciones','kilometraje'], tabs:['👥 Directorio','💰 Gastos','✅ Asistencia','⚠️ Penaliz.','🛣️ Km'] },
        rutas:         { sections:['rutas'] },
        reportes:      { sections:['kpis','reportes'],                         tabs:['📈 KPIs','📊 Exportar'] },
        alertas:       { sections:['alertas','comunicacion'],                  tabs:['🔔 Alertas','💬 Chat'] },
        config:        { sections:['zonas','horarios','conceptos'],            tabs:['🏷 Zonas','🕐 Horarios','📋 Conceptos'] }
    };
    var SEC_RENDERS = {
        dashboard:renderDashboard, localizacion:renderLocalizacion,
        pedidos:renderPedidos, reagendar:renderReagendamiento, inventario:renderInventario,
        repartidores:renderRepartidoresSection, gastos:renderGastos, checks:renderChecks,
        penalizaciones:renderPenalizacionesSec, kilometraje:renderKilometraje,
        kpis:renderKpis, reportes:renderReportes,
        alertas:renderAlertas, comunicacion:renderComunicacion,
        zonas:renderZonas, horarios:renderHorarios, conceptos:renderConceptos,
        rutas:renderRutas, geocercas:renderGeocercas, historial:renderHistorial
    };
    var currentGroup='dashboard', currentSubIdx=0;

    var sidebarBtns = panel.querySelectorAll('.cr-sidebar-btn[data-cr-section]');
    var sections = panel.querySelectorAll('.cr-section[data-cr-section]');
    sidebarBtns.forEach(function(btn){
        btn.addEventListener('click',function(){
            sidebarBtns.forEach(function(b){b.classList.remove('active');});
            btn.classList.add('active');
            currentSubIdx=0;
            renderActiveSection();
        });
    });
    function getActiveSection(){
        var active = panel.querySelector('.cr-sidebar-btn.active');
        return active ? active.dataset.crSection : 'dashboard';
    }

    function showSubSection(groupKey, idx){
        var g=SECTION_GROUPS[groupKey]; if(!g) return;
        // Hide ALL sections first
        sections.forEach(function(s){ s.classList.remove('active'); s.style.display='none'; });
        // Show the target sub-section
        var targetKey=g.sections[idx];
        var el=panel.querySelector('.cr-section[data-cr-section="'+targetKey+'"]');
        if(el){ el.classList.add('active'); el.style.display=''; }
        // Call its render function
        if(SEC_RENDERS[targetKey]) SEC_RENDERS[targetKey]();
        populateZonaSelects();
        populateRepSelects();
    }

    function renderActiveSection(){
        var sec = getActiveSection();
        currentGroup=sec;
        var g=SECTION_GROUPS[sec];
        if(!g){ /* fallback for any unmapped section */
            sections.forEach(function(s){ s.classList.remove('active'); s.style.display='none'; });
            var direct=panel.querySelector('.cr-section[data-cr-section="'+sec+'"]');
            if(direct){direct.classList.add('active');direct.style.display='';}
            if(SEC_RENDERS[sec]) SEC_RENDERS[sec]();
            updateSidebarResumen(); return;
        }
        // Sub-tab bar
        var tabBar=document.getElementById('crSubTabBar');
        if(g.tabs && g.tabs.length>1){
            tabBar.style.display='';
            tabBar.innerHTML='<div class="cr-subtabs">'+g.tabs.map(function(t,i){
                return '<button class="cr-subtab'+(i===currentSubIdx?' active':'')+'" data-sub-idx="'+i+'">'+t+'</button>';
            }).join('')+'</div>';
            tabBar.querySelectorAll('.cr-subtab').forEach(function(btn){
                btn.addEventListener('click',function(){
                    currentSubIdx=parseInt(btn.dataset.subIdx);
                    tabBar.querySelectorAll('.cr-subtab').forEach(function(t){t.classList.remove('active');});
                    btn.classList.add('active');
                    showSubSection(currentGroup, currentSubIdx);
                });
            });
        } else {
            tabBar.style.display='none';
            tabBar.innerHTML='';
        }
        // Show first (or current) sub-section
        showSubSection(sec, currentSubIdx);
        updateSidebarResumen();
    }"""

if OLD_JS_HANDLER in content:
    content = content.replace(OLD_JS_HANDLER, NEW_JS_HANDLER, 1)
    count += 1
    print(f"  {count}. Sidebar handler + renderActiveSection rewritten with groups")
else:
    errors.append("Old JS handler/renderActiveSection not found")

# ====================================================================
# STEP 7: Add Localization toggle + Client list + Historial popup JS
# Insert before the // ── INIT ── block
# ====================================================================
INIT_MARKER = '    // ── INIT ──'

LOC_AND_HIST_JS = """    // ── LOCALIZACIÓN TOGGLE (Repartidores / Clientes) ──
    (function(){
        var toggleBtns=panel.querySelectorAll('#crLocToggle .cr-toggle');
        toggleBtns.forEach(function(btn){
            btn.addEventListener('click',function(){
                toggleBtns.forEach(function(t){t.classList.remove('active');});
                btn.classList.add('active');
                var view=btn.dataset.loc;
                var repsView=document.getElementById('crLocViewReps');
                var cliView=document.getElementById('crLocViewClientes');
                if(repsView) repsView.style.display=(view==='repartidores'?'':'none');
                if(cliView) cliView.style.display=(view==='clientes'?'':'none');
                if(view==='clientes') renderLocClientesList();
            });
        });
        var locZona=document.getElementById('crLocFiltroZona');
        if(locZona) locZona.addEventListener('change',function(){ renderLocClientesList(); });
        var locBuscar=document.getElementById('crLocBuscar');
        if(locBuscar) locBuscar.addEventListener('input',function(){ renderLocClientesList(); });
    })();

    function renderLocClientesList(){
        var container=document.getElementById('crLocClientesList');if(!container) return;
        var zona=((document.getElementById('crLocFiltroZona')||{}).value||'').toLowerCase();
        var busq=((document.getElementById('crLocBuscar')||{}).value||'').toUpperCase().trim();
        // Build client map from entregas
        var clientMap={};
        allEntregas.forEach(function(e){
            if(!e.cliente) return;
            var key=e.cliente;
            if(!clientMap[key]) clientMap[key]={nombre:e.cliente,zona:e.zona||'',entregas:0,exitosas:0,fallidas:0};
            clientMap[key].entregas++;
            if(e.estado==='entregada') clientMap[key].exitosas++;
            if(e.estado==='no_entregada') clientMap[key].fallidas++;
        });
        var clients=Object.values(clientMap);
        // Apply filters
        if(zona) clients=clients.filter(function(c){ return (c.zona||'').toLowerCase()===zona; });
        if(busq) clients=clients.filter(function(c){ return c.nombre.toUpperCase().indexOf(busq)>=0; });
        clients.sort(function(a,b){ return b.entregas-a.entregas; });
        // Update geocerca resumen
        var resumen=document.getElementById('crGeocercaResumen');
        if(resumen) resumen.innerHTML='<span style="font-weight:700;">'+clients.length+'</span> clientes encontrados';
        if(!clients.length){ container.innerHTML='<div style="color:#94a3b8;font-size:0.55rem;padding:10px;text-align:center;">Sin clientes con entregas registradas</div>'; return; }
        container.innerHTML=clients.map(function(c){
            var pct=c.entregas>0?Math.round(c.exitosas/c.entregas*100):0;
            var color=pct>=80?'#10b981':pct>=50?'#f59e0b':'#ef4444';
            return '<div style="display:flex;align-items:center;gap:10px;padding:10px 12px;background:#fff;border:1px solid #e2e8f0;border-radius:10px;transition:box-shadow 0.15s;" onmouseover="this.style.boxShadow=\'0 2px 8px rgba(0,0,0,0.08)\'" onmouseout="this.style.boxShadow=\'none\'">'+
                '<div style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:0.6rem;flex-shrink:0;">'+esc(c.nombre.charAt(0))+'</div>'+
                '<div style="flex:1;min-width:0;">'+
                    '<div style="font-weight:800;font-size:0.58rem;color:#0f172a;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">'+esc(c.nombre)+'</div>'+
                    '<div style="font-size:0.45rem;color:#64748b;">'+c.entregas+' entregas · <span style="color:'+color+';font-weight:700;">'+pct+'% éxito</span> · Zona: '+esc(c.zona||'—')+'</div>'+
                '</div>'+
                '<button class="cr-btn primary cr-ver-historial" data-cliente="'+esc(c.nombre)+'" style="font-size:0.45rem;white-space:nowrap;flex-shrink:0;">📜 Historial</button>'+
            '</div>';
        }).join('');
        container.querySelectorAll('.cr-ver-historial').forEach(function(btn){
            btn.addEventListener('click',function(){ showHistorialPopup(btn.dataset.cliente); });
        });
    }

    // ── HISTORIAL POPUP ──
    function showHistorialPopup(clienteNombre){
        var popup=document.getElementById('crHistPopup');if(!popup) return;
        popup.style.display='block';
        var infoEl=document.getElementById('crHistPopupClienteInfo');
        if(infoEl) infoEl.innerHTML='<span style="font-size:0.8rem;margin-right:6px;">👤</span>'+esc(clienteNombre);
        var entregas=allEntregas.filter(function(e){ return e.cliente===clienteNombre; });
        var exitosas=entregas.filter(function(e){return e.estado==='entregada';}).length;
        var fallidas=entregas.filter(function(e){return e.estado==='no_entregada';}).length;
        var pendientes=entregas.length-exitosas-fallidas;
        var statsEl=document.getElementById('crHistPopupStats');
        if(statsEl) statsEl.innerHTML=
            '<div style="flex:1;background:#f0fdf4;border-radius:10px;padding:10px;text-align:center;"><div style="font-size:1.1rem;font-weight:900;color:#16a34a;">'+exitosas+'</div><div style="font-size:0.42rem;color:#64748b;font-weight:700;">✅ Exitosas</div></div>'+
            '<div style="flex:1;background:#fef2f2;border-radius:10px;padding:10px;text-align:center;"><div style="font-size:1.1rem;font-weight:900;color:#ef4444;">'+fallidas+'</div><div style="font-size:0.42rem;color:#64748b;font-weight:700;">❌ Fallidas</div></div>'+
            '<div style="flex:1;background:#eff6ff;border-radius:10px;padding:10px;text-align:center;"><div style="font-size:1.1rem;font-weight:900;color:#3b82f6;">'+pendientes+'</div><div style="font-size:0.42rem;color:#64748b;font-weight:700;">📬 Pendientes</div></div>'+
            '<div style="flex:1;background:#f8fafc;border-radius:10px;padding:10px;text-align:center;"><div style="font-size:1.1rem;font-weight:900;color:#0f172a;">'+entregas.length+'</div><div style="font-size:0.42rem;color:#64748b;font-weight:700;">📊 Total</div></div>';
        var body=document.getElementById('crHistPopupBody');
        if(!body) return;
        if(!entregas.length){ body.innerHTML='<div style="color:#94a3b8;font-size:0.55rem;padding:30px;text-align:center;">Sin entregas registradas para este cliente</div>'; return; }
        var stColors={entregada:'#10b981',no_entregada:'#ef4444',pendiente:'#f59e0b',en_camino:'#3b82f6'};
        body.innerHTML='<table class="cr-table"><thead><tr><th>Folio</th><th>Producto</th><th>Fecha</th><th>Estado</th><th>Repartidor</th><th>Motivo</th></tr></thead><tbody>'+
            entregas.map(function(e){
                return '<tr><td style="font-weight:700;">'+esc(e.folioProduccion||e.id)+'</td><td>'+esc(e.producto||'—')+'</td><td>'+fmtDate(e.creadoEn)+'</td>'+
                    '<td><span class="cr-badge" style="background:'+(stColors[e.estado]||'#94a3b8')+'18;color:'+(stColors[e.estado]||'#94a3b8')+';">'+esc(e.estado||'pendiente')+'</span></td>'+
                    '<td>'+esc(e.repartidorNombre||'—')+'</td><td>'+esc(e.conceptoNoEntrega||'—')+'</td></tr>';
            }).join('')+'</tbody></table>';
    }
    // Close popup
    (function(){
        var closeBtn=document.getElementById('crHistPopupClose');
        if(closeBtn) closeBtn.addEventListener('click',function(){ document.getElementById('crHistPopup').style.display='none'; });
        var popup=document.getElementById('crHistPopup');
        if(popup) popup.addEventListener('click',function(e){ if(e.target===popup) popup.style.display='none'; });
    })();

    // ── POPULATE LOCALIZACION ZONA SELECT ──
    var _origPopZonas = populateZonaSelects;
    populateZonaSelects = function(){
        _origPopZonas();
        // Also populate the loc filter
        var zonas=getZonas();
        var locSel=document.getElementById('crLocFiltroZona');
        if(locSel){
            var cur=locSel.value;
            var opts='<option value="">Todas las zonas</option>';
            zonas.forEach(function(z){opts+='<option value="'+esc(z.nombre)+'"'+(cur===z.nombre?' selected':'')+'>'+esc(z.nombre)+'</option>';});
            locSel.innerHTML=opts;if(cur)locSel.value=cur;
        }
    };

    """ + INIT_MARKER

if INIT_MARKER in content:
    content = content.replace(INIT_MARKER, LOC_AND_HIST_JS, 1)
    count += 1
    print(f"  {count}. Localization toggle + Client list + Historial popup JS added")
else:
    errors.append("INIT marker not found")

# ====================================================================
# STEP 8: Add populateZonaSelects for crLocFiltroZona and
# keep crGeocercaFiltroZona in the selector list
# ====================================================================
# (Already handled via the wrapper in step 7)
# Just make sure we keep populateRepSelects pointing to new loc selects too

# ====================================================================
# WRITE OUTPUT
# ====================================================================
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nTotal replacements: {count}")
print("=" * 60)
if errors:
    print("WARNINGS:")
    for e in errors:
        print(f"  ⚠ {e}")
else:
    print("✅ CONSOLIDATION COMPLETE! 20 sections → 8 grouped modules")
print("=" * 60)
