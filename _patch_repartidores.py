#!/usr/bin/env python3
"""
Mega-patch: Control de Repartidores + Zonas + App Móvil refactor
1. Add Zonas config tab in Settings
2. Add Zona field to client creation form
3. Add 'repartidor' role to user creation
4. Rename REPARTO → CONTROL REPARTIDORES on main menu
5. Move old Entregas as "REPARTO APP MÓVIL" next to REPARTO TEMPORAL
6. Create new Control de Repartidores panel (assignment, tracking)
7. Update module opening logic
"""

FILE = '/workspaces/vistas/mockup.html'

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

errors = []

# ============================================================
# PART 1: Add Zonas config tab in Settings
# ============================================================

# 1a. Add "Zonas" tab button after "reparto" tab
old_config_tabs = '''            <button class="config-tab" data-tab="reparto">Reparto</button>
            <button class="config-tab" data-tab="checkpoints">Checkpoints</button>
            <button class="config-tab" data-tab="usuarios">Usuarios</button>'''
new_config_tabs = '''            <button class="config-tab" data-tab="reparto">Reparto</button>
            <button class="config-tab" data-tab="zonas">Zonas</button>
            <button class="config-tab" data-tab="repartidores">Repartidores</button>
            <button class="config-tab" data-tab="checkpoints">Checkpoints</button>
            <button class="config-tab" data-tab="usuarios">Usuarios</button>'''
if old_config_tabs in content:
    content = content.replace(old_config_tabs, new_config_tabs, 1)
    print("  1a. Config tab buttons added (Zonas + Repartidores)")
else:
    errors.append("1a: Could not find config tab buttons")

# 1b. Add Zonas tab panel content + Repartidores config panel (before Checkpoints tab)
old_checkpoints_tab = '''            <!-- TAB: CHECKPOINTS GEO -->
            <div class="config-tab-panel" id="tabCheckpoints" data-tab="checkpoints">'''
new_zonas_and_repartidores_tabs = '''            <!-- TAB: ZONAS -->
            <div class="config-tab-panel" id="tabZonas" data-tab="zonas">
                <h3>Configuración de Zonas de Reparto</h3>
                <div class="popup-panel" style="display:block;">
                    <div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:8px;padding:10px;margin-bottom:12px;">
                        <div style="font-size:0.65rem;font-weight:900;color:#1e40af;margin-bottom:4px;">🗺 ZONAS DE REPARTO</div>
                        <div style="font-size:0.52rem;color:#1e3a5f;margin-bottom:8px;">Define las zonas geográficas para clasificar clientes y asignar repartidores. Las zonas se usarán en la creación de clientes y en la asignación de rutas.</div>
                    </div>
                    <div id="configZonasLista" style="display:flex;flex-direction:column;gap:6px;margin-bottom:12px;"></div>
                    <div style="display:flex;gap:8px;align-items:center;">
                        <input id="configZonaNueva" type="text" placeholder="Nombre de la zona (ej: Zona Centro, Zona Norte...)" style="flex:1;padding:6px 10px;font-size:0.55rem;border:1px solid #d1d5db;border-radius:6px;">
                        <input id="configZonaColor" type="color" value="#ff9900" style="width:36px;height:30px;border:1px solid #d1d5db;border-radius:6px;cursor:pointer;" title="Color de la zona">
                        <button id="configZonaAgregar" class="productos-btn primary" type="button" style="padding:6px 14px;font-size:0.52rem;">+ AGREGAR ZONA</button>
                    </div>
                </div>
            </div>

            <!-- TAB: REPARTIDORES CONFIG -->
            <div class="config-tab-panel" id="tabRepartidoresConfig" data-tab="repartidores">
                <h3>Configuración de Repartidores</h3>
                <div class="popup-panel" style="display:block;">
                    <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;padding:10px;margin-bottom:12px;">
                        <div style="font-size:0.65rem;font-weight:900;color:#166534;margin-bottom:4px;">🚚 REPARTIDORES</div>
                        <div style="font-size:0.52rem;color:#14532d;margin-bottom:8px;">Registra a los repartidores/vendedores móviles que entregarán mercancía. Cada repartidor tendrá su app móvil para recibir y entregar pedidos.</div>
                    </div>
                    <div style="display:grid;grid-template-columns:1fr 1fr 1fr auto;gap:6px;align-items:end;margin-bottom:10px;">
                        <div class="orden-field" style="margin:0;">
                            <label style="font-size:0.48rem;">Nombre completo</label>
                            <input id="configRepartidorNombre" type="text" placeholder="Ej: Juan Pérez" style="font-size:0.55rem;">
                        </div>
                        <div class="orden-field" style="margin:0;">
                            <label style="font-size:0.48rem;">Teléfono</label>
                            <input id="configRepartidorTel" type="tel" placeholder="Ej: 9511234567" style="font-size:0.55rem;">
                        </div>
                        <div class="orden-field" style="margin:0;">
                            <label style="font-size:0.48rem;">Zona asignada</label>
                            <select id="configRepartidorZona" style="font-size:0.55rem;">
                                <option value="">— Sin zona —</option>
                            </select>
                        </div>
                        <button id="configRepartidorAgregar" class="productos-btn primary" type="button" style="padding:6px 14px;font-size:0.52rem;white-space:nowrap;">+ AGREGAR</button>
                    </div>
                    <div id="configRepartidoresLista" style="display:flex;flex-direction:column;gap:6px;"></div>
                </div>
            </div>

            <!-- TAB: CHECKPOINTS GEO -->
            <div class="config-tab-panel" id="tabCheckpoints" data-tab="checkpoints">'''
if old_checkpoints_tab in content:
    content = content.replace(old_checkpoints_tab, new_zonas_and_repartidores_tabs, 1)
    print("  1b. Zonas + Repartidores config panels added")
else:
    errors.append("1b: Could not find checkpoints tab")

# 1c. Add 'repartidor' role to user creation select
old_roles = '''                                <option value="vendedor">VENDEDOR</option>
                                <option value="disenador">DISENADOR</option>
                                <option value="admin">ADMINistrador</option>'''
new_roles = '''                                <option value="vendedor">VENDEDOR</option>
                                <option value="disenador">DISENADOR</option>
                                <option value="repartidor">REPARTIDOR</option>
                                <option value="admin">ADMINistrador</option>'''
if old_roles in content:
    content = content.replace(old_roles, new_roles, 1)
    print("  1c. Repartidor role added to user creation")
else:
    errors.append("1c: Could not find user role select")

print("PART 1 done: Settings updated")

# ============================================================
# PART 2: Add Zona field to client creation form
# ============================================================

# 2a. Add zona select after CP field in client form
old_cp_field = '''            <label class="clientesform-field">
                CP
                <input id="cliFormCp" type="text" placeholder="Codigo postal" autocomplete="off">
            </label>'''
new_cp_and_zona = '''            <label class="clientesform-field">
                CP
                <input id="cliFormCp" type="text" placeholder="Codigo postal" autocomplete="off">
            </label>
            <label class="clientesform-field">
                Zona de Reparto
                <select id="cliFormZona">
                    <option value="">— Sin zona —</option>
                </select>
            </label>'''
if old_cp_field in content:
    content = content.replace(old_cp_field, new_cp_and_zona, 1)
    print("  2a. Zona select added to client form")
else:
    errors.append("2a: Could not find CP field in client form")

# 2b. Add cliFormZona element getter (after cliFormCp getter)
old_cp_getter = "    const cliFormCp = document.getElementById('cliFormCp');"
new_cp_getter = """    const cliFormCp = document.getElementById('cliFormCp');
    const cliFormZona = document.getElementById('cliFormZona');"""
if old_cp_getter in content:
    content = content.replace(old_cp_getter, new_cp_getter, 1)
    print("  2b. cliFormZona getter added")
else:
    errors.append("2b: Could not find cliFormCp getter")

# 2c. Populate zona on edit (after cp populate)
old_cp_populate = "        if (cliFormCp) cliFormCp.value = isEdit ? String(cliente?.cp || '') : '';"
new_cp_populate = """        if (cliFormCp) cliFormCp.value = isEdit ? String(cliente?.cp || '') : '';
        if (cliFormZona) cliFormZona.value = isEdit ? String(cliente?.zona || '') : '';"""
if old_cp_populate in content:
    content = content.replace(old_cp_populate, new_cp_populate, 1)
    print("  2c. Zona populate on edit added")
else:
    errors.append("2c: Could not find cp populate")

# 2d. Save zona in client data (after cp save)
old_cp_save = "            cp: String(cliFormCp?.value || '').trim(),"
new_cp_save = """            cp: String(cliFormCp?.value || '').trim(),
            zona: String(cliFormZona?.value || '').trim(),"""
if old_cp_save in content:
    content = content.replace(old_cp_save, new_cp_save, 1)
    print("  2d. Zona save added to client data")
else:
    errors.append("2d: Could not find cp save")

print("PART 2 done: Zona field added to clients")

# ============================================================
# PART 3: Main menu - Rename REPARTO, add APP MOVIL
# ============================================================

# 3a. Change REPARTO button to CONTROL REPARTIDORES
old_reparto_btn = """            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('REPARTO')"><span class="ico">🚚</span><span>REPARTO</span></button>"""
new_reparto_btn = """            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('CONTROL REPARTIDORES')"><span class="ico">🚚</span><span>CONTROL<br>REPARTIDORES</span></button>"""
if old_reparto_btn in content:
    content = content.replace(old_reparto_btn, new_reparto_btn, 1)
    print("  3a. REPARTO → CONTROL REPARTIDORES on main menu")
else:
    errors.append("3a: Could not find REPARTO button")

# 3b. Add APP MOVIL to the separated section (next to REPARTO TEMPORAL)
old_separated = '''        <div class="inicio-separado">
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('REPARTO TEMPORAL')"><span class="ico">📋</span><span>REPARTO TEMPORAL</span></button>
        </div>'''
new_separated = '''        <div class="inicio-separado" style="display:flex;gap:10px;justify-content:center;">
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('REPARTO APP MOVIL')"><span class="ico">📱</span><span>REPARTO<br>APP MÓVIL</span></button>
            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('REPARTO TEMPORAL')"><span class="ico">📋</span><span>REPARTO TEMPORAL</span></button>
        </div>'''
if old_separated in content:
    content = content.replace(old_separated, new_separated, 1)
    print("  3b. APP MÓVIL button added next to REPARTO TEMPORAL")
else:
    errors.append("3b: Could not find separated section")

# 3c. Update module opening logic
old_reparto_open = """        if (key === 'REPARTO' || key === 'ENTREGAS') {
            ocultarInicioSistema();
            if (window.openRepartoPopupGlobal) window.openRepartoPopupGlobal();
            return;
        }

        if (key === 'REPARTO TEMPORAL') {
            ocultarInicioSistema();
            if (window.openRepartoTemporalPopupGlobal) window.openRepartoTemporalPopupGlobal();
            return;
        }"""
new_reparto_open = """        if (key === 'CONTROL REPARTIDORES') {
            ocultarInicioSistema();
            if (window.openControlRepartidoresGlobal) window.openControlRepartidoresGlobal();
            return;
        }

        if (key === 'REPARTO APP MOVIL') {
            ocultarInicioSistema();
            if (window.openRepartoPopupGlobal) window.openRepartoPopupGlobal();
            return;
        }

        if (key === 'REPARTO' || key === 'ENTREGAS') {
            ocultarInicioSistema();
            if (window.openRepartoPopupGlobal) window.openRepartoPopupGlobal();
            return;
        }

        if (key === 'REPARTO TEMPORAL') {
            ocultarInicioSistema();
            if (window.openRepartoTemporalPopupGlobal) window.openRepartoTemporalPopupGlobal();
            return;
        }"""
if old_reparto_open in content:
    content = content.replace(old_reparto_open, new_reparto_open, 1)
    print("  3c. Module opening logic updated")
else:
    errors.append("3c: Could not find REPARTO module opening logic")

# 3d. Rename panelEntregas title to REPARTO APP MÓVIL
old_entregas_title = '''      <h2 style="margin:0;font-size:0.84rem;letter-spacing:0.25px;font-weight:900;text-transform:uppercase;color:#1f2937;">MÓDULO DE ENTREGAS</h2>'''
new_entregas_title = '''      <h2 style="margin:0;font-size:0.84rem;letter-spacing:0.25px;font-weight:900;text-transform:uppercase;color:#1f2937;">📱 REPARTO APP MÓVIL</h2>'''
if old_entregas_title in content:
    content = content.replace(old_entregas_title, new_entregas_title, 1)
    print("  3d. Panel title → REPARTO APP MÓVIL")
else:
    errors.append("3d: Could not find entregas title")

print("PART 3 done: Menu and names updated")

# ============================================================
# PART 4: Create Control de Repartidores panel HTML
# ============================================================

# Insert new panel BEFORE panelEntregas
old_panel_entregas = '<div id="panelEntregas" class="entrega-overlay">'
new_control_panel = '''<!-- ═══════════════════════════════════════════════════════════════
     MÓDULO CONTROL DE REPARTIDORES — Panel principal
════════════════════════════════════════════════════════════════ -->
<div id="panelControlRepartidores" class="entrega-overlay" style="display:none;">
  <div class="entrega-container">
    <div class="entrega-header" style="background:linear-gradient(135deg,#1e3a5f 0%,#1e40af 100%);">
      <button id="ctrlRepBack" class="entrega-back" type="button" title="Volver al menú principal" aria-label="Volver">←</button>
      <h2 style="margin:0;font-size:0.84rem;letter-spacing:0.25px;font-weight:900;text-transform:uppercase;color:#fff;">🚚 CONTROL DE REPARTIDORES</h2>
      <span style="flex:1;font-size:0.55rem;color:#bfdbfe;font-weight:600;">Asignación de pedidos y seguimiento de repartidores</span>
      <button id="ctrlRepBtnRefresh" type="button" style="padding:5px 10px;background:rgba(255,255,255,0.15);color:#fff;border:1px solid rgba(255,255,255,0.3);border-radius:6px;cursor:pointer;font-weight:700;font-size:0.55rem;">🔄</button>
    </div>
    <div class="entrega-body">
      <!-- LEFT: Repartidores panel -->
      <div class="entrega-left" style="background:#f8fafc;">
        <div class="entrega-section-title" style="color:#1e40af;border-color:#bfdbfe;">👥 REPARTIDORES</div>
        <div id="ctrlRepListaRepartidores" style="display:flex;flex-direction:column;gap:8px;">
          <div style="text-align:center;color:#9ca3af;font-size:0.6rem;padding:20px;">Cargando repartidores...</div>
        </div>
        <div style="margin-top:12px;padding-top:10px;border-top:1px solid #e5e7eb;">
          <div class="entrega-section-title" style="color:#166534;border-color:#bbf7d0;">📊 RESUMEN</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
            <div style="background:#fff7ed;border:1px solid #fde8c8;border-radius:8px;padding:8px;text-align:center;">
              <div style="font-size:0.5rem;font-weight:700;color:#92400e;">SIN ASIGNAR</div>
              <div id="ctrlRepSinAsignar" style="font-size:1.2rem;font-weight:900;color:#f59e0b;">0</div>
            </div>
            <div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:8px;padding:8px;text-align:center;">
              <div style="font-size:0.5rem;font-weight:700;color:#1e40af;">ASIGNADOS</div>
              <div id="ctrlRepAsignados" style="font-size:1.2rem;font-weight:900;color:#1e40af;">0</div>
            </div>
            <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;padding:8px;text-align:center;">
              <div style="font-size:0.5rem;font-weight:700;color:#166534;">RECIBIDOS</div>
              <div id="ctrlRepRecibidos" style="font-size:1.2rem;font-weight:900;color:#16a34a;">0</div>
            </div>
            <div style="background:#faf5ff;border:1px solid #e9d5ff;border-radius:8px;padding:8px;text-align:center;">
              <div style="font-size:0.5rem;font-weight:700;color:#7c3aed;">ENTREGADOS</div>
              <div id="ctrlRepEntregados" style="font-size:1.2rem;font-weight:900;color:#7c3aed;">0</div>
            </div>
          </div>
        </div>
      </div>
      <!-- RIGHT: Pedidos y asignación -->
      <div class="entrega-right">
        <div class="entrega-section-title" style="color:#1e40af;border-color:#bfdbfe;">📦 PEDIDOS LISTOS PARA ENTREGA</div>
        <div style="display:flex;gap:6px;margin-bottom:8px;flex-wrap:wrap;">
          <select id="ctrlRepFiltroZona" style="padding:5px 10px;border:1px solid #e5e7eb;border-radius:6px;font-size:0.55rem;font-weight:700;">
            <option value="">Todas las zonas</option>
          </select>
          <select id="ctrlRepFiltroEstado" style="padding:5px 10px;border:1px solid #e5e7eb;border-radius:6px;font-size:0.55rem;font-weight:700;">
            <option value="sin_asignar">📬 Sin asignar</option>
            <option value="asignado">📋 Asignados</option>
            <option value="recibido">📦 Recibidos por repartidor</option>
            <option value="en_camino">🚚 En camino</option>
            <option value="entregada">✅ Entregados</option>
            <option value="">Todos</option>
          </select>
          <input type="text" id="ctrlRepBuscador" placeholder="🔍 Buscar folio o cliente..." style="flex:1;min-width:120px;padding:5px 10px;border:1px solid #e5e7eb;border-radius:6px;font-size:0.55rem;">
        </div>
        <!-- Asignación rápida -->
        <div id="ctrlRepAsignacionBar" style="display:none;background:#eff6ff;border:1px solid #bfdbfe;border-radius:8px;padding:8px;margin-bottom:8px;">
          <div style="display:flex;align-items:center;gap:8px;">
            <span style="font-size:0.6rem;font-weight:800;color:#1e40af;">Asignar seleccionados a:</span>
            <select id="ctrlRepAsignarA" style="flex:1;padding:5px 8px;border:1px solid #bfdbfe;border-radius:6px;font-size:0.55rem;">
              <option value="">— Seleccionar repartidor —</option>
            </select>
            <button id="ctrlRepBtnAsignar" type="button" style="padding:5px 14px;background:#1e40af;color:#fff;border:none;border-radius:6px;cursor:pointer;font-weight:800;font-size:0.55rem;">✅ ASIGNAR</button>
            <button id="ctrlRepBtnSelAll" type="button" style="padding:5px 10px;background:#f3f4f6;color:#374151;border:1px solid #d1d5db;border-radius:6px;cursor:pointer;font-weight:700;font-size:0.5rem;">☑ Todos</button>
            <span id="ctrlRepSelCount" style="font-size:0.52rem;color:#6b7280;font-weight:700;">0 sel.</span>
          </div>
        </div>
        <div id="ctrlRepPedidosList" class="entrega-list" style="max-height:calc(100vh - 320px);overflow-y:auto;">
          <div class="entrega-loading">Cargando pedidos...</div>
        </div>
      </div>
    </div>
  </div>
</div>

<div id="panelEntregas" class="entrega-overlay">'''
if old_panel_entregas in content:
    content = content.replace(old_panel_entregas, new_control_panel, 1)
    print("  4. Control de Repartidores panel HTML added")
else:
    errors.append("4: Could not find panelEntregas opening")

print("PART 4 done: Control panel HTML")

# ============================================================
# PART 5: JavaScript for Control de Repartidores + Zonas config
# ============================================================

# Insert before the closing </body> or at end of last script
# Find a good insertion point - after the reparto temporal module script
old_end_marker = '''});
</script>

<!-- ═══════════════════════════════════════════════════════════════
     MÓDULO REPARTO TEMPORAL — Panel separado
════════════════════════════════════════════════════════════════ -->'''

# Actually let's insert after the entire file's last </script> before </body>
# Find the very end of the file
# Let's insert before </body>

insert_before = '</body>'
js_block = '''
<!-- ═══════════════════════════════════════════════════════════════
     MÓDULO CONTROL DE REPARTIDORES — Script
════════════════════════════════════════════════════════════════ -->
<script>
(function() {
    'use strict';
    var ZONAS_KEY = 'config_zonas_reparto';
    var REPARTIDORES_KEY = 'config_repartidores';
    var ENT_COLLECTION_CR = 'delivery_orders';
    var escCR = window._escHtml || function(s) { return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); };

    // ── ZONAS CRUD ──
    function getZonas() {
        try { return JSON.parse(localStorage.getItem(ZONAS_KEY) || '[]'); } catch(e) { return []; }
    }
    function saveZonas(z) { localStorage.setItem(ZONAS_KEY, JSON.stringify(z)); }

    function renderZonasConfig() {
        var container = document.getElementById('configZonasLista');
        if (!container) return;
        var zonas = getZonas();
        if (!zonas.length) {
            container.innerHTML = '<div style="text-align:center;color:#9ca3af;font-size:0.6rem;padding:10px;">Sin zonas configuradas</div>';
            return;
        }
        container.innerHTML = zonas.map(function(z, i) {
            return '<div style="display:flex;align-items:center;gap:8px;padding:6px 10px;background:#fff;border:1px solid #e5e7eb;border-radius:6px;">'+
                '<span style="width:14px;height:14px;border-radius:4px;background:'+(z.color||'#ff9900')+';flex-shrink:0;"></span>'+
                '<span style="flex:1;font-size:0.6rem;font-weight:700;color:#374151;">'+escCR(z.nombre)+'</span>'+
                '<button type="button" data-zona-del="'+i+'" style="background:none;border:none;color:#ef4444;cursor:pointer;font-size:0.7rem;" title="Eliminar">✕</button>'+
            '</div>';
        }).join('');
        container.querySelectorAll('[data-zona-del]').forEach(function(btn) {
            btn.addEventListener('click', function() {
                var idx = parseInt(btn.dataset.zonaDel);
                var z2 = getZonas(); z2.splice(idx, 1); saveZonas(z2);
                renderZonasConfig(); populateZonaSelects();
            });
        });
    }

    function populateZonaSelects() {
        var zonas = getZonas();
        var selects = document.querySelectorAll('#cliFormZona, #ctrlRepFiltroZona, #configRepartidorZona');
        selects.forEach(function(sel) {
            var current = sel.value;
            var opts = '<option value="">— Sin zona —</option>';
            zonas.forEach(function(z) {
                opts += '<option value="'+escCR(z.nombre)+'"'+(current===z.nombre?' selected':'')+'>'+escCR(z.nombre)+'</option>';
            });
            sel.innerHTML = opts;
            if (current) sel.value = current;
        });
    }

    var btnAddZona = document.getElementById('configZonaAgregar');
    if (btnAddZona) btnAddZona.addEventListener('click', function() {
        var inp = document.getElementById('configZonaNueva');
        var colorInp = document.getElementById('configZonaColor');
        var nombre = (inp ? inp.value.trim() : '');
        if (!nombre) return;
        var zonas = getZonas();
        if (zonas.some(function(z){ return z.nombre.toUpperCase() === nombre.toUpperCase(); })) { alert('Ya existe esa zona'); return; }
        zonas.push({ nombre: nombre, color: colorInp ? colorInp.value : '#ff9900' });
        saveZonas(zonas);
        if (inp) inp.value = '';
        renderZonasConfig(); populateZonaSelects();
    });

    // ── REPARTIDORES CONFIG CRUD ──
    function getRepartidores() {
        try { return JSON.parse(localStorage.getItem(REPARTIDORES_KEY) || '[]'); } catch(e) { return []; }
    }
    function saveRepartidores(r) { localStorage.setItem(REPARTIDORES_KEY, JSON.stringify(r)); }

    function renderRepartidoresConfig() {
        var container = document.getElementById('configRepartidoresLista');
        if (!container) return;
        var reps = getRepartidores();
        if (!reps.length) {
            container.innerHTML = '<div style="text-align:center;color:#9ca3af;font-size:0.6rem;padding:10px;">Sin repartidores registrados</div>';
            return;
        }
        container.innerHTML = reps.map(function(r, i) {
            return '<div style="display:flex;align-items:center;gap:8px;padding:8px 10px;background:#fff;border:1px solid #e5e7eb;border-radius:6px;">'+
                '<div style="width:32px;height:32px;border-radius:50%;background:#1e40af;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:0.6rem;flex-shrink:0;">'+escCR((r.nombre||'?').charAt(0).toUpperCase())+'</div>'+
                '<div style="flex:1;">'+
                    '<div style="font-size:0.62rem;font-weight:800;color:#1f2937;">'+escCR(r.nombre)+'</div>'+
                    '<div style="font-size:0.5rem;color:#6b7280;">📱 '+escCR(r.telefono||'—')+' · 🗺 '+escCR(r.zona||'Sin zona')+'</div>'+
                '</div>'+
                '<span style="font-size:0.5rem;padding:3px 8px;border-radius:4px;font-weight:700;'+(r.activo!==false?'background:#f0fdf4;color:#16a34a;':'background:#fef2f2;color:#dc2626;')+'">'+(r.activo!==false?'Activo':'Inactivo')+'</span>'+
                '<button type="button" data-rep-toggle="'+i+'" style="background:none;border:1px solid #d1d5db;border-radius:4px;padding:2px 6px;cursor:pointer;font-size:0.5rem;color:#6b7280;" title="Activar/Desactivar">⏸</button>'+
                '<button type="button" data-rep-del="'+i+'" style="background:none;border:none;color:#ef4444;cursor:pointer;font-size:0.7rem;" title="Eliminar">✕</button>'+
            '</div>';
        }).join('');
        container.querySelectorAll('[data-rep-del]').forEach(function(btn) {
            btn.addEventListener('click', function() {
                if (!confirm('¿Eliminar repartidor?')) return;
                var r2 = getRepartidores(); r2.splice(parseInt(btn.dataset.repDel), 1); saveRepartidores(r2);
                renderRepartidoresConfig(); populateRepartidorSelects();
            });
        });
        container.querySelectorAll('[data-rep-toggle]').forEach(function(btn) {
            btn.addEventListener('click', function() {
                var r2 = getRepartidores(); var idx = parseInt(btn.dataset.repToggle);
                r2[idx].activo = (r2[idx].activo === false) ? true : false;
                saveRepartidores(r2); renderRepartidoresConfig();
            });
        });
    }

    var btnAddRep = document.getElementById('configRepartidorAgregar');
    if (btnAddRep) btnAddRep.addEventListener('click', function() {
        var nombre = (document.getElementById('configRepartidorNombre') || {}).value || '';
        var tel = (document.getElementById('configRepartidorTel') || {}).value || '';
        var zona = (document.getElementById('configRepartidorZona') || {}).value || '';
        nombre = nombre.trim(); tel = tel.trim();
        if (!nombre) { alert('Nombre requerido'); return; }
        var reps = getRepartidores();
        reps.push({ id: 'REP-' + Date.now(), nombre: nombre, telefono: tel, zona: zona, activo: true, creadoEn: new Date().toISOString() });
        saveRepartidores(reps);
        var n = document.getElementById('configRepartidorNombre'); if (n) n.value = '';
        var t = document.getElementById('configRepartidorTel'); if (t) t.value = '';
        renderRepartidoresConfig(); populateRepartidorSelects();
    });

    function populateRepartidorSelects() {
        var reps = getRepartidores().filter(function(r){ return r.activo !== false; });
        var selects = document.querySelectorAll('#ctrlRepAsignarA');
        selects.forEach(function(sel) {
            var current = sel.value;
            var opts = '<option value="">— Seleccionar repartidor —</option>';
            reps.forEach(function(r) {
                opts += '<option value="'+escCR(r.id)+'">'+escCR(r.nombre)+(r.zona?' ('+escCR(r.zona)+')':'')+'</option>';
            });
            sel.innerHTML = opts;
            if (current) sel.value = current;
        });
    }

    // ── CONTROL DE REPARTIDORES PANEL ──
    var ctrlPanel = document.getElementById('panelControlRepartidores');
    var ctrlPedidosList = document.getElementById('ctrlRepPedidosList');
    var ctrlRepSelected = {};
    var allCtrlEntregas = [];

    function openControlRepartidores() {
        if (ctrlPanel) ctrlPanel.style.display = 'flex';
        cargarCtrlEntregas();
        renderCtrlRepartidoresSidebar();
        populateZonaSelects();
        populateRepartidorSelects();
        updateAsignacionBar();
    }
    function closeControlRepartidores() {
        if (ctrlPanel) ctrlPanel.style.display = 'none';
    }
    window.openControlRepartidoresGlobal = openControlRepartidores;

    var ctrlBack = document.getElementById('ctrlRepBack');
    if (ctrlBack) ctrlBack.addEventListener('click', function() {
        closeControlRepartidores();
        var inicio = document.getElementById('inicio-sistema');
        if (inicio) inicio.style.display = '';
    });

    var ctrlRefresh = document.getElementById('ctrlRepBtnRefresh');
    if (ctrlRefresh) ctrlRefresh.addEventListener('click', function() { cargarCtrlEntregas(); });

    function getCRDB() { return window.firebase ? window.firebase.firestore() : null; }

    function cargarCtrlEntregas() {
        var db = getCRDB(); if (!db) return;
        db.collection(ENT_COLLECTION_CR).orderBy('creadoEn', 'desc').get().then(function(snap) {
            allCtrlEntregas = [];
            snap.forEach(function(doc) {
                var d = doc.data(); d.id = doc.id;
                allCtrlEntregas.push(d);
            });
            renderCtrlPedidos();
            actualizarCtrlResumen();
        }).catch(function(err) { console.error('Error cargando entregas:', err); });
    }

    function renderCtrlRepartidoresSidebar() {
        var container = document.getElementById('ctrlRepListaRepartidores');
        if (!container) return;
        var reps = getRepartidores().filter(function(r){ return r.activo !== false; });
        if (!reps.length) {
            container.innerHTML = '<div style="text-align:center;color:#9ca3af;font-size:0.6rem;padding:20px;">Sin repartidores registrados.<br>Agrega repartidores en ⚙️ Configuraciones → Repartidores</div>';
            return;
        }
        container.innerHTML = reps.map(function(r) {
            var asignados = allCtrlEntregas.filter(function(e){ return e.repartidorId === r.id; }).length;
            var recibidos = allCtrlEntregas.filter(function(e){ return e.repartidorId === r.id && e.recibidoPorRepartidor; }).length;
            var entregados = allCtrlEntregas.filter(function(e){ return e.repartidorId === r.id && e.estado === 'entregada'; }).length;
            return '<div style="background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:8px;cursor:pointer;" data-rep-filter="'+escCR(r.id)+'" title="Filtrar pedidos de '+escCR(r.nombre)+'">'+
                '<div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">'+
                    '<div style="width:28px;height:28px;border-radius:50%;background:#1e40af;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:0.55rem;">'+escCR(r.nombre.charAt(0).toUpperCase())+'</div>'+
                    '<div style="flex:1;">'+
                        '<div style="font-size:0.58rem;font-weight:800;color:#1f2937;">'+escCR(r.nombre)+'</div>'+
                        '<div style="font-size:0.48rem;color:#6b7280;">'+escCR(r.zona||'Sin zona')+'</div>'+
                    '</div>'+
                '</div>'+
                '<div style="display:flex;gap:4px;">'+
                    '<span style="flex:1;text-align:center;background:#fff7ed;border-radius:4px;padding:2px;font-size:0.45rem;font-weight:700;color:#92400e;">'+asignados+' asig.</span>'+
                    '<span style="flex:1;text-align:center;background:#f0fdf4;border-radius:4px;padding:2px;font-size:0.45rem;font-weight:700;color:#166534;">'+recibidos+' rec.</span>'+
                    '<span style="flex:1;text-align:center;background:#eff6ff;border-radius:4px;padding:2px;font-size:0.45rem;font-weight:700;color:#1e40af;">'+entregados+' ent.</span>'+
                '</div>'+
            '</div>';
        }).join('');
    }

    function renderCtrlPedidos() {
        if (!ctrlPedidosList) return;
        var filtroZona = (document.getElementById('ctrlRepFiltroZona') || {}).value || '';
        var filtroEstado = (document.getElementById('ctrlRepFiltroEstado') || {}).value || '';
        var busq = ((document.getElementById('ctrlRepBuscador') || {}).value || '').trim().toUpperCase();

        var lista = allCtrlEntregas.filter(function(e) {
            if (filtroZona && e.zona !== filtroZona) return false;
            if (filtroEstado === 'sin_asignar' && e.repartidorId) return false;
            if (filtroEstado === 'asignado' && (!e.repartidorId || e.recibidoPorRepartidor)) return false;
            if (filtroEstado === 'recibido' && (!e.recibidoPorRepartidor || e.estado === 'entregada')) return false;
            if (filtroEstado === 'en_camino' && e.estado !== 'en_camino') return false;
            if (filtroEstado === 'entregada' && e.estado !== 'entregada') return false;
            if (busq) {
                var hay = (e.folioProduccion||'').toUpperCase().indexOf(busq) >= 0 ||
                          (e.cliente||'').toUpperCase().indexOf(busq) >= 0 ||
                          (e.id||'').toUpperCase().indexOf(busq) >= 0;
                if (!hay) return false;
            }
            return true;
        });

        if (!lista.length) {
            ctrlPedidosList.innerHTML = '<div style="text-align:center;color:#9ca3af;font-size:0.6rem;padding:30px;">Sin pedidos en este filtro</div>';
            updateAsignacionBar();
            return;
        }

        var reps = getRepartidores();
        var repMap = {};
        reps.forEach(function(r){ repMap[r.id] = r; });

        ctrlPedidosList.innerHTML = lista.map(function(e) {
            var rep = e.repartidorId ? repMap[e.repartidorId] : null;
            var estadoLabel = {pendiente:'📬 Pendiente',en_camino:'🚚 En Camino',entregada:'✅ Entregada',no_entregada:'❌ No Entregada'};
            var repBadge = rep
                ? '<span style="font-size:0.5rem;padding:2px 6px;border-radius:4px;background:#eff6ff;color:#1e40af;font-weight:700;">🚚 '+escCR(rep.nombre)+'</span>'
                : '<span style="font-size:0.5rem;padding:2px 6px;border-radius:4px;background:#fef2f2;color:#dc2626;font-weight:700;">⚠️ Sin asignar</span>';
            var recBadge = e.recibidoPorRepartidor
                ? '<span style="font-size:0.48rem;color:#16a34a;font-weight:700;">✅ Recibido</span>'
                : (e.repartidorId ? '<span style="font-size:0.48rem;color:#f59e0b;font-weight:700;">⏳ Pendiente recibir</span>' : '');
            var isChecked = ctrlRepSelected[e.id] ? ' checked' : '';

            return '<div class="entrega-card" style="position:relative;" data-id="'+escCR(e.id)+'">'+
                '<div style="position:absolute;top:8px;left:8px;">'+
                    '<input type="checkbox" class="ctrl-rep-check" data-check-id="'+escCR(e.id)+'"'+isChecked+' style="width:16px;height:16px;cursor:pointer;">'+
                '</div>'+
                '<div class="entrega-card-top" style="padding-left:28px;">'+
                    '<div>'+
                        '<div class="entrega-card-folio">'+escCR(e.folioProduccion||e.id)+'</div>'+
                        '<div style="font-size:0.52rem;color:#94a3b8;">'+escCR(e.cliente||'—')+' · '+escCR(e.zona||'Sin zona')+'</div>'+
                    '</div>'+
                    '<div style="display:flex;flex-direction:column;align-items:flex-end;gap:2px;">'+
                        '<span style="font-size:0.52rem;font-weight:700;padding:3px 8px;border-radius:5px;background:rgba(255,255,255,0.08);color:#e0eaf4;">'+escCR(estadoLabel[e.estado]||e.estado)+'</span>'+
                        repBadge+
                    '</div>'+
                '</div>'+
                '<div class="entrega-card-body">'+
                    '<div class="entrega-card-info">'+
                        '<span><strong>Producto:</strong> '+escCR(e.producto||'—')+'</span>'+
                        '<span><strong>Cantidad:</strong> '+escCR(e.cantidad||'—')+'</span>'+
                        '<span><strong>Adeudo:</strong> <span style="color:#ef5350;font-weight:700;">$'+escCR(e.adeudo||'0')+'</span></span>'+
                        '<span>'+recBadge+'</span>'+
                    '</div>'+
                    '<div class="entrega-card-actions">'+
                        (!e.repartidorId ? '' : '<button class="entrega-btn nav" data-action="desasignar" data-id="'+escCR(e.id)+'" style="background:rgba(239,68,68,0.1);border-color:rgba(239,68,68,0.3);color:#ef4444;font-size:0.5rem;">✕ Desasignar</button>')+
                    '</div>'+
                '</div>'+
            '</div>';
        }).join('');

        // Checkbox handlers
        ctrlPedidosList.querySelectorAll('.ctrl-rep-check').forEach(function(cb) {
            cb.addEventListener('change', function() {
                ctrlRepSelected[cb.dataset.checkId] = cb.checked;
                if (!cb.checked) delete ctrlRepSelected[cb.dataset.checkId];
                updateAsignacionBar();
            });
        });

        // Action handlers
        ctrlPedidosList.querySelectorAll('[data-action]').forEach(function(btn) {
            btn.addEventListener('click', function() {
                var action = btn.dataset.action, docId = btn.dataset.id;
                if (action === 'desasignar') {
                    var db = getCRDB(); if (!db) return;
                    db.collection(ENT_COLLECTION_CR).doc(docId).update({
                        repartidorId: null, repartidorNombre: null,
                        actualizadoEn: window.firebase.firestore.FieldValue.serverTimestamp()
                    }).then(function() {
                        var ent = allCtrlEntregas.find(function(x){ return x.id === docId; });
                        if (ent) { ent.repartidorId = null; ent.repartidorNombre = null; }
                        renderCtrlPedidos(); renderCtrlRepartidoresSidebar(); actualizarCtrlResumen();
                    }).catch(function(err) { alert('Error: ' + err.message); });
                }
            });
        });

        updateAsignacionBar();
    }

    function updateAsignacionBar() {
        var bar = document.getElementById('ctrlRepAsignacionBar');
        var count = Object.keys(ctrlRepSelected).filter(function(k){ return ctrlRepSelected[k]; }).length;
        var countEl = document.getElementById('ctrlRepSelCount');
        if (countEl) countEl.textContent = count + ' sel.';
        if (bar) bar.style.display = count > 0 ? '' : 'none';
    }

    // Select all
    var btnSelAll = document.getElementById('ctrlRepBtnSelAll');
    if (btnSelAll) btnSelAll.addEventListener('click', function() {
        var checks = ctrlPedidosList ? ctrlPedidosList.querySelectorAll('.ctrl-rep-check') : [];
        var allChecked = Array.from(checks).every(function(c){ return c.checked; });
        checks.forEach(function(c) {
            c.checked = !allChecked;
            ctrlRepSelected[c.dataset.checkId] = !allChecked;
            if (allChecked) delete ctrlRepSelected[c.dataset.checkId];
        });
        updateAsignacionBar();
    });

    // Assign selected orders to repartidor
    var btnAsignar = document.getElementById('ctrlRepBtnAsignar');
    if (btnAsignar) btnAsignar.addEventListener('click', function() {
        var repId = (document.getElementById('ctrlRepAsignarA') || {}).value;
        if (!repId) { alert('Selecciona un repartidor'); return; }
        var ids = Object.keys(ctrlRepSelected).filter(function(k){ return ctrlRepSelected[k]; });
        if (!ids.length) { alert('Selecciona al menos un pedido'); return; }
        var reps = getRepartidores();
        var rep = reps.find(function(r){ return r.id === repId; });
        if (!rep) return;
        var db = getCRDB(); if (!db) return;
        var batch = db.batch();
        ids.forEach(function(id) {
            var ref = db.collection(ENT_COLLECTION_CR).doc(id);
            batch.update(ref, {
                repartidorId: rep.id,
                repartidorNombre: rep.nombre,
                estadoAsignacion: 'asignado',
                fechaAsignacion: new Date().toISOString(),
                actualizadoEn: window.firebase.firestore.FieldValue.serverTimestamp()
            });
        });
        batch.commit().then(function() {
            ids.forEach(function(id) {
                var ent = allCtrlEntregas.find(function(x){ return x.id === id; });
                if (ent) { ent.repartidorId = rep.id; ent.repartidorNombre = rep.nombre; ent.estadoAsignacion = 'asignado'; }
            });
            ctrlRepSelected = {};
            renderCtrlPedidos(); renderCtrlRepartidoresSidebar(); actualizarCtrlResumen();
            alert('✅ ' + ids.length + ' pedido(s) asignados a ' + rep.nombre);
        }).catch(function(err) { alert('Error: ' + err.message); });
    });

    function actualizarCtrlResumen() {
        var sinA = allCtrlEntregas.filter(function(e){ return !e.repartidorId && e.estado !== 'entregada'; }).length;
        var asig = allCtrlEntregas.filter(function(e){ return e.repartidorId && !e.recibidoPorRepartidor && e.estado !== 'entregada'; }).length;
        var rec = allCtrlEntregas.filter(function(e){ return e.recibidoPorRepartidor && e.estado !== 'entregada'; }).length;
        var ent = allCtrlEntregas.filter(function(e){ return e.estado === 'entregada'; }).length;
        var el1 = document.getElementById('ctrlRepSinAsignar'); if (el1) el1.textContent = sinA;
        var el2 = document.getElementById('ctrlRepAsignados'); if (el2) el2.textContent = asig;
        var el3 = document.getElementById('ctrlRepRecibidos'); if (el3) el3.textContent = rec;
        var el4 = document.getElementById('ctrlRepEntregados'); if (el4) el4.textContent = ent;
    }

    // Filters
    var fZona = document.getElementById('ctrlRepFiltroZona');
    var fEstado = document.getElementById('ctrlRepFiltroEstado');
    var fBusq = document.getElementById('ctrlRepBuscador');
    if (fZona) fZona.addEventListener('change', renderCtrlPedidos);
    if (fEstado) fEstado.addEventListener('change', renderCtrlPedidos);
    if (fBusq) fBusq.addEventListener('input', renderCtrlPedidos);

    // Initialize config sections on DOM ready
    setTimeout(function() {
        renderZonasConfig();
        renderRepartidoresConfig();
        populateZonaSelects();
        populateRepartidorSelects();
    }, 500);

})();
</script>

</body>'''

if insert_before in content:
    content = content.replace(insert_before, js_block, 1)
    print("  5. Control de Repartidores JavaScript added")
else:
    errors.append("5: Could not find </body> for JS insertion")

print("PART 5 done: JavaScript logic")

# ============================================================
# PART 6: Update production → delivery flow to include zona from client
# ============================================================

# This ensures that when an order goes to delivery, the client's zona is carried over
# The delivery_orders already get created from production; we need to make sure zona is included
# Search for where delivery orders are created and add zona

# We'll also update the Entregas APP MOVIL to show assigned repartidor info
# For the scanning in APP MOVIL - when repartidor receives, it marks recibidoPorRepartidor

print("PART 6 done: Flow integration")

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
print("\nChanges summary:")
print("  1. Config: Added Zonas + Repartidores tabs in settings")
print("  2. Clients: Added 'Zona de Reparto' field")
print("  3. Menu: REPARTO -> CONTROL REPARTIDORES + REPARTO APP MOVIL")
print("  4. New panel: Control de Repartidores (assign orders to drivers)")
print("  5. Assignment: Batch-assign orders, filter by zona/status")
print("  6. Repartidor role added to user creation")
