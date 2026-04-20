#!/usr/bin/env python3
"""
Mega-patch v2: Replace Control de Repartidores with full module
Sections in right sidebar:
1. Localización (mapa general con vendedores)
2. Pedidos Listos para Entrega
3. Conceptos de Visita (app motivos)
4. Zonas (CRUD, moved from config)
5. Geocercas (mapa interactivo clientes)
6. Gastos de Empleado
7. Horarios
8. Empleados / Checks (llegadas/salidas)
9. Repartidores (config moved here)
10. Estadísticas / Dashboard
"""

FILE = '/workspaces/vistas/mockup.html'

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

errors = []

# ============================================================
# PART 1: Remove Zonas and Repartidores tabs from Config
# ============================================================
old_config_tabs = '''            <button class="config-tab" data-tab="reparto">Reparto</button>
            <button class="config-tab" data-tab="zonas">Zonas</button>
            <button class="config-tab" data-tab="repartidores">Repartidores</button>
            <button class="config-tab" data-tab="checkpoints">Checkpoints</button>'''
new_config_tabs = '''            <button class="config-tab" data-tab="reparto">Reparto</button>
            <button class="config-tab" data-tab="checkpoints">Checkpoints</button>'''
if old_config_tabs in content:
    content = content.replace(old_config_tabs, new_config_tabs, 1)
    print("  1a. Zonas+Repartidores tabs removed from config buttons")
else:
    errors.append("1a: config tab buttons not found")

# Remove Zonas tab panel
old_zonas_panel = '''            <!-- TAB: ZONAS -->
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

            <!-- TAB: CHECKPOINTS GEO -->'''
new_zonas_removed = '''            <!-- TAB: CHECKPOINTS GEO -->'''
if old_zonas_panel in content:
    content = content.replace(old_zonas_panel, new_zonas_removed, 1)
    print("  1b. Zonas+Repartidores tab panels removed from config")
else:
    errors.append("1b: zonas/repartidores panels not found")

print("PART 1 done: Config cleaned")

# ============================================================
# PART 2: Replace Control de Repartidores HTML panel
# ============================================================
old_panel = '''<!-- ═══════════════════════════════════════════════════════════════
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
</div>'''

new_panel = '''<!-- ═══════════════════════════════════════════════════════════════
     MÓDULO CONTROL DE REPARTO — Panel principal completo
════════════════════════════════════════════════════════════════ -->
<style>
  #panelControlRepartidores { display:none; }
  #panelControlRepartidores .cr-body { display:flex; height:calc(100vh - 56px); overflow:hidden; }
  #panelControlRepartidores .cr-sidebar { width:220px; min-width:200px; background:#0f172a; display:flex; flex-direction:column; overflow-y:auto; }
  #panelControlRepartidores .cr-sidebar-btn { display:flex; align-items:center; gap:8px; padding:10px 14px; border:none; background:transparent; color:#94a3b8; font-size:0.58rem; font-weight:700; cursor:pointer; text-align:left; border-left:3px solid transparent; transition:all 0.15s; }
  #panelControlRepartidores .cr-sidebar-btn:hover { background:rgba(255,255,255,0.05); color:#e2e8f0; }
  #panelControlRepartidores .cr-sidebar-btn.active { background:rgba(30,64,175,0.2); color:#60a5fa; border-left-color:#3b82f6; }
  #panelControlRepartidores .cr-sidebar-btn .cr-ico { font-size:0.9rem; width:22px; text-align:center; }
  #panelControlRepartidores .cr-main { flex:1; overflow-y:auto; background:#f1f5f9; padding:16px; }
  #panelControlRepartidores .cr-section { display:none; }
  #panelControlRepartidores .cr-section.active { display:block; }
  #panelControlRepartidores .cr-card { background:#fff; border:1px solid #e2e8f0; border-radius:10px; padding:14px; margin-bottom:12px; }
  #panelControlRepartidores .cr-card h3 { margin:0 0 10px 0; font-size:0.72rem; font-weight:900; color:#1e293b; }
  #panelControlRepartidores .cr-stats { display:grid; grid-template-columns:repeat(auto-fit,minmax(130px,1fr)); gap:10px; margin-bottom:14px; }
  #panelControlRepartidores .cr-stat { background:#fff; border:1px solid #e2e8f0; border-radius:10px; padding:12px; text-align:center; }
  #panelControlRepartidores .cr-stat .val { font-size:1.4rem; font-weight:900; }
  #panelControlRepartidores .cr-stat .lbl { font-size:0.48rem; font-weight:700; color:#64748b; text-transform:uppercase; letter-spacing:0.5px; }
  #panelControlRepartidores .cr-table { width:100%; border-collapse:collapse; font-size:0.55rem; }
  #panelControlRepartidores .cr-table th { background:#f8fafc; padding:8px 10px; text-align:left; font-weight:800; color:#475569; border-bottom:2px solid #e2e8f0; font-size:0.5rem; text-transform:uppercase; }
  #panelControlRepartidores .cr-table td { padding:8px 10px; border-bottom:1px solid #f1f5f9; color:#334155; }
  #panelControlRepartidores .cr-table tr:hover td { background:#f8fafc; }
  #panelControlRepartidores .cr-badge { display:inline-block; padding:2px 8px; border-radius:4px; font-size:0.48rem; font-weight:800; }
  #panelControlRepartidores .cr-btn { padding:6px 14px; border:none; border-radius:6px; cursor:pointer; font-weight:800; font-size:0.52rem; transition:all 0.15s; }
  #panelControlRepartidores .cr-btn.primary { background:#1e40af; color:#fff; }
  #panelControlRepartidores .cr-btn.primary:hover { background:#1e3a8a; }
  #panelControlRepartidores .cr-btn.danger { background:#fef2f2; color:#dc2626; border:1px solid #fecaca; }
  #panelControlRepartidores .cr-btn.success { background:#f0fdf4; color:#16a34a; border:1px solid #bbf7d0; }
  #panelControlRepartidores .cr-map-placeholder { width:100%; height:350px; border-radius:10px; background:#e2e8f0; display:flex; align-items:center; justify-content:center; color:#64748b; font-size:0.65rem; font-weight:700; position:relative; overflow:hidden; }
  #panelControlRepartidores .cr-input { padding:6px 10px; border:1px solid #d1d5db; border-radius:6px; font-size:0.55rem; width:100%; box-sizing:border-box; }
  #panelControlRepartidores .cr-select { padding:6px 10px; border:1px solid #d1d5db; border-radius:6px; font-size:0.55rem; }
  #panelControlRepartidores .cr-header-bar { display:flex; align-items:center; gap:10px; margin-bottom:14px; flex-wrap:wrap; }
</style>
<div id="panelControlRepartidores" class="entrega-overlay">
  <div style="display:flex;flex-direction:column;width:100%;height:100vh;">
    <!-- Header -->
    <div style="background:linear-gradient(135deg,#0f172a 0%,#1e40af 100%);padding:10px 18px;display:flex;align-items:center;gap:12px;flex-shrink:0;">
      <button id="ctrlRepBack" type="button" style="background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:#fff;border-radius:8px;width:34px;height:34px;cursor:pointer;font-size:1rem;display:flex;align-items:center;justify-content:center;" title="Volver">←</button>
      <div style="flex:1;">
        <h2 style="margin:0;font-size:0.82rem;font-weight:900;color:#fff;letter-spacing:0.5px;">🚚 CONTROL DE REPARTO</h2>
        <span style="font-size:0.5rem;color:#93c5fd;">Panel de gestión de repartidores, rutas y entregas</span>
      </div>
      <button id="ctrlRepBtnRefresh" type="button" class="cr-btn primary" style="font-size:0.5rem;">🔄 Actualizar</button>
    </div>
    <!-- Body: Sidebar + Main -->
    <div class="cr-body">
      <!-- Sidebar -->
      <div class="cr-sidebar">
        <div style="padding:12px 14px 8px;font-size:0.48rem;font-weight:800;color:#475569;text-transform:uppercase;letter-spacing:1px;">Módulos</div>
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
        <div style="flex:1;"></div>
        <div style="padding:10px 14px;border-top:1px solid rgba(255,255,255,0.08);">
          <div id="crSidebarResumen" style="font-size:0.48rem;color:#64748b;line-height:1.6;"></div>
        </div>
      </div>
      <!-- Main Content -->
      <div class="cr-main">

        <!-- ── SECTION: DASHBOARD ── -->
        <div class="cr-section active" id="crSecDashboard" data-cr-section="dashboard">
          <div class="cr-stats">
            <div class="cr-stat"><div class="val" style="color:#f59e0b;" id="crStatSinAsignar">0</div><div class="lbl">Sin Asignar</div></div>
            <div class="cr-stat"><div class="val" style="color:#3b82f6;" id="crStatAsignados">0</div><div class="lbl">Asignados</div></div>
            <div class="cr-stat"><div class="val" style="color:#8b5cf6;" id="crStatRecibidos">0</div><div class="lbl">Recibidos</div></div>
            <div class="cr-stat"><div class="val" style="color:#10b981;" id="crStatEntregados">0</div><div class="lbl">Entregados</div></div>
            <div class="cr-stat"><div class="val" style="color:#ef4444;" id="crStatNoEntregados">0</div><div class="lbl">No Entregados</div></div>
            <div class="cr-stat"><div class="val" style="color:#0f172a;" id="crStatRepartidores">0</div><div class="lbl">Repartidores</div></div>
          </div>
          <div class="cr-card">
            <h3>📋 Actividad Reciente</h3>
            <div id="crDashActivity" style="max-height:300px;overflow-y:auto;font-size:0.55rem;color:#475569;">Cargando...</div>
          </div>
          <div class="cr-card">
            <h3>🚚 Estado de Repartidores</h3>
            <div id="crDashRepartidoresStatus"></div>
          </div>
        </div>

        <!-- ── SECTION: LOCALIZACIÓN ── -->
        <div class="cr-section" id="crSecLocalizacion" data-cr-section="localizacion">
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
        </div>

        <!-- ── SECTION: PEDIDOS ── -->
        <div class="cr-section" id="crSecPedidos" data-cr-section="pedidos">
          <div class="cr-header-bar">
            <select id="ctrlRepFiltroZona" class="cr-select"><option value="">Todas las zonas</option></select>
            <select id="ctrlRepFiltroEstado" class="cr-select">
              <option value="sin_asignar">📬 Sin asignar</option>
              <option value="asignado">📋 Asignados</option>
              <option value="recibido">📦 Recibidos</option>
              <option value="en_camino">🚚 En camino</option>
              <option value="entregada">✅ Entregados</option>
              <option value="">Todos</option>
            </select>
            <input type="text" id="ctrlRepBuscador" class="cr-input" placeholder="🔍 Buscar folio o cliente..." style="max-width:250px;">
          </div>
          <!-- Asignación rápida -->
          <div id="ctrlRepAsignacionBar" class="cr-card" style="display:none;background:#eff6ff;border-color:#bfdbfe;">
            <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
              <span style="font-size:0.6rem;font-weight:800;color:#1e40af;">Asignar seleccionados a:</span>
              <select id="ctrlRepAsignarA" class="cr-select" style="flex:1;min-width:150px;"><option value="">— Seleccionar repartidor —</option></select>
              <button id="ctrlRepBtnAsignar" type="button" class="cr-btn primary">✅ ASIGNAR</button>
              <button id="ctrlRepBtnSelAll" type="button" class="cr-btn" style="background:#f3f4f6;color:#374151;border:1px solid #d1d5db;">☑ Todos</button>
              <span id="ctrlRepSelCount" style="font-size:0.52rem;color:#6b7280;font-weight:700;">0 sel.</span>
            </div>
          </div>
          <div id="ctrlRepPedidosList" style="display:flex;flex-direction:column;gap:8px;">
            <div style="text-align:center;color:#9ca3af;padding:30px;font-size:0.6rem;">Cargando pedidos...</div>
          </div>
        </div>

        <!-- ── SECTION: CONCEPTOS DE VISITA ── -->
        <div class="cr-section" id="crSecConceptos" data-cr-section="conceptos">
          <div class="cr-card">
            <h3>📋 Conceptos de Visita</h3>
            <p style="font-size:0.52rem;color:#64748b;margin:0 0 12px 0;">Cuando un repartidor no puede entregar, seleccionará uno de estos motivos desde la app móvil. Los conceptos aparecerán en el historial de entregas.</p>
            <div id="crConceptosLista" style="display:flex;flex-direction:column;gap:6px;margin-bottom:12px;"></div>
            <div style="display:flex;gap:8px;align-items:center;">
              <input id="crConceptoNuevo" type="text" class="cr-input" placeholder="Ej: Cliente no encontrado, Dirección incorrecta, Cancelado..." style="flex:1;">
              <select id="crConceptoTipo" class="cr-select">
                <option value="no_entrega">❌ No entrega</option>
                <option value="reagendar">📅 Reagendar</option>
                <option value="parcial">📦 Entrega parcial</option>
                <option value="otro">📝 Otro</option>
              </select>
              <button id="crConceptoAgregar" type="button" class="cr-btn primary">+ Agregar</button>
            </div>
          </div>
          <div class="cr-card">
            <h3>📊 Uso de Conceptos</h3>
            <div id="crConceptosStats" style="font-size:0.55rem;color:#64748b;">Sin registros aún</div>
          </div>
        </div>

        <!-- ── SECTION: ZONAS ── -->
        <div class="cr-section" id="crSecZonas" data-cr-section="zonas">
          <div class="cr-card">
            <h3>🏷 Zonas de Reparto</h3>
            <p style="font-size:0.52rem;color:#64748b;margin:0 0 12px 0;">Define las zonas geográficas para clasificar clientes y organizar rutas de entrega.</p>
            <div id="configZonasLista" style="display:flex;flex-direction:column;gap:6px;margin-bottom:12px;"></div>
            <div style="display:flex;gap:8px;align-items:center;">
              <input id="configZonaNueva" type="text" class="cr-input" placeholder="Nombre (ej: Zona Centro, Zona Norte...)" style="flex:1;">
              <input id="configZonaColor" type="color" value="#3b82f6" style="width:40px;height:34px;border:1px solid #d1d5db;border-radius:6px;cursor:pointer;">
              <button id="configZonaAgregar" type="button" class="cr-btn primary">+ Agregar Zona</button>
            </div>
          </div>
        </div>

        <!-- ── SECTION: GEOCERCAS ── -->
        <div class="cr-section" id="crSecGeocercas" data-cr-section="geocercas">
          <div class="cr-card">
            <h3>📍 Geocercas — Mapa de Clientes</h3>
            <p style="font-size:0.52rem;color:#64748b;margin:0 0 12px 0;">Mapa interactivo con las ubicaciones de todos los clientes. Útil para planificar rutas y verificar cobertura de zonas.</p>
            <div style="display:flex;gap:8px;margin-bottom:10px;">
              <select id="crGeocercaFiltroZona" class="cr-select"><option value="">Todas las zonas</option></select>
              <input id="crGeocercaBuscar" type="text" class="cr-input" placeholder="🔍 Buscar cliente..." style="max-width:250px;">
            </div>
            <div id="crMapaClientes" class="cr-map-placeholder" style="height:400px;">
              <div style="text-align:center;">
                <div style="font-size:2rem;margin-bottom:8px;">📍</div>
                <div>Mapa de clientes</div>
                <div style="font-size:0.5rem;color:#94a3b8;margin-top:4px;">Se mostrarán todos los clientes mapeados por zona</div>
              </div>
            </div>
          </div>
          <div class="cr-card">
            <h3>📊 Clientes por Zona</h3>
            <div id="crGeocercaResumen" style="font-size:0.55rem;color:#64748b;">Cargando...</div>
          </div>
        </div>

        <!-- ── SECTION: GASTOS EMPLEADO ── -->
        <div class="cr-section" id="crSecGastos" data-cr-section="gastos">
          <div class="cr-header-bar">
            <select id="crGastoFiltroRep" class="cr-select"><option value="">Todos los repartidores</option></select>
            <select id="crGastoFiltroPeriodo" class="cr-select">
              <option value="hoy">Hoy</option>
              <option value="semana">Esta semana</option>
              <option value="mes" selected>Este mes</option>
              <option value="todo">Todo</option>
            </select>
          </div>
          <div class="cr-stats" id="crGastosResumen">
            <div class="cr-stat"><div class="val" style="color:#ef4444;" id="crGastoTotal">$0</div><div class="lbl">Total Gastos</div></div>
            <div class="cr-stat"><div class="val" style="color:#f59e0b;" id="crGastoCombustible">$0</div><div class="lbl">Combustible</div></div>
            <div class="cr-stat"><div class="val" style="color:#3b82f6;" id="crGastoAlimentos">$0</div><div class="lbl">Alimentos</div></div>
            <div class="cr-stat"><div class="val" style="color:#8b5cf6;" id="crGastoOtros">$0</div><div class="lbl">Otros</div></div>
          </div>
          <div class="cr-card">
            <h3>💰 Registro de Gastos</h3>
            <table class="cr-table">
              <thead><tr><th>Fecha</th><th>Repartidor</th><th>Concepto</th><th>Monto</th><th>Evidencia</th><th>Estado</th></tr></thead>
              <tbody id="crGastosTabla"><tr><td colspan="6" style="text-align:center;color:#94a3b8;padding:20px;">Sin gastos registrados</td></tr></tbody>
            </table>
          </div>
        </div>

        <!-- ── SECTION: HORARIOS ── -->
        <div class="cr-section" id="crSecHorarios" data-cr-section="horarios">
          <div class="cr-card">
            <h3>🕐 Configuración de Horarios</h3>
            <p style="font-size:0.52rem;color:#64748b;margin:0 0 12px 0;">Define los horarios de trabajo de cada repartidor. Se usarán para el control de asistencia y cálculo de horas extras.</p>
            <div id="crHorariosLista"></div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr auto;gap:8px;align-items:end;margin-top:12px;padding-top:12px;border-top:1px solid #e2e8f0;">
              <div><label style="font-size:0.48rem;font-weight:700;color:#64748b;">Repartidor</label><select id="crHorarioRep" class="cr-select" style="width:100%;"></select></div>
              <div><label style="font-size:0.48rem;font-weight:700;color:#64748b;">Hora Entrada</label><input id="crHorarioEntrada" type="time" value="08:00" class="cr-input"></div>
              <div><label style="font-size:0.48rem;font-weight:700;color:#64748b;">Hora Salida</label><input id="crHorarioSalida" type="time" value="18:00" class="cr-input"></div>
              <div><label style="font-size:0.48rem;font-weight:700;color:#64748b;">Días</label><select id="crHorarioDias" class="cr-select" style="width:100%;"><option value="lun-sab">Lun-Sáb</option><option value="lun-vie">Lun-Vie</option><option value="todos">Todos</option><option value="personalizado">Personalizado</option></select></div>
              <button id="crHorarioGuardar" type="button" class="cr-btn primary" style="white-space:nowrap;">💾 Guardar</button>
            </div>
          </div>
        </div>

        <!-- ── SECTION: CHECKS ASISTENCIA ── -->
        <div class="cr-section" id="crSecChecks" data-cr-section="checks">
          <div class="cr-header-bar">
            <select id="crCheckFiltroRep" class="cr-select"><option value="">Todos</option></select>
            <select id="crCheckFiltroPeriodo" class="cr-select">
              <option value="hoy" selected>Hoy</option>
              <option value="semana">Esta semana</option>
              <option value="mes">Este mes</option>
            </select>
          </div>
          <div class="cr-stats">
            <div class="cr-stat"><div class="val" style="color:#10b981;" id="crCheckPresentes">0</div><div class="lbl">Presentes Hoy</div></div>
            <div class="cr-stat"><div class="val" style="color:#ef4444;" id="crCheckAusentes">0</div><div class="lbl">Ausentes</div></div>
            <div class="cr-stat"><div class="val" style="color:#f59e0b;" id="crCheckRetardos">0</div><div class="lbl">Retardos</div></div>
            <div class="cr-stat"><div class="val" style="color:#3b82f6;" id="crCheckHorasExtra">0</div><div class="lbl">Horas Extra</div></div>
          </div>
          <div class="cr-card">
            <h3>✅ Registro de Entradas/Salidas</h3>
            <table class="cr-table">
              <thead><tr><th>Fecha</th><th>Repartidor</th><th>Entrada</th><th>Salida</th><th>Horas</th><th>Estado</th><th>Ubicación</th></tr></thead>
              <tbody id="crChecksTabla"><tr><td colspan="7" style="text-align:center;color:#94a3b8;padding:20px;">Sin registros hoy</td></tr></tbody>
            </table>
          </div>
        </div>

        <!-- ── SECTION: REPARTIDORES ── -->
        <div class="cr-section" id="crSecRepartidores" data-cr-section="repartidores">
          <div class="cr-card">
            <h3>👥 Repartidores Registrados</h3>
            <div id="configRepartidoresLista" style="display:flex;flex-direction:column;gap:8px;margin-bottom:14px;"></div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr auto;gap:8px;align-items:end;padding-top:12px;border-top:1px solid #e2e8f0;">
              <div><label style="font-size:0.48rem;font-weight:700;color:#64748b;">Nombre completo</label><input id="configRepartidorNombre" type="text" class="cr-input" placeholder="Juan Pérez"></div>
              <div><label style="font-size:0.48rem;font-weight:700;color:#64748b;">Teléfono</label><input id="configRepartidorTel" type="tel" class="cr-input" placeholder="9511234567"></div>
              <div><label style="font-size:0.48rem;font-weight:700;color:#64748b;">Zona</label><select id="configRepartidorZona" class="cr-select" style="width:100%;"><option value="">— Sin zona —</option></select></div>
              <button id="configRepartidorAgregar" type="button" class="cr-btn primary" style="white-space:nowrap;">+ Agregar</button>
            </div>
          </div>
        </div>

        <!-- ── SECTION: RUTAS ── -->
        <div class="cr-section" id="crSecRutas" data-cr-section="rutas">
          <div class="cr-card">
            <h3>🛣 Optimización de Rutas</h3>
            <p style="font-size:0.52rem;color:#64748b;margin:0 0 12px 0;">Visualiza y optimiza las rutas de entrega por repartidor. El sistema sugiere el orden de entrega más eficiente.</p>
            <div style="display:flex;gap:8px;margin-bottom:12px;">
              <select id="crRutaRep" class="cr-select"><option value="">Seleccionar repartidor</option></select>
              <select id="crRutaFecha" class="cr-select"><option value="hoy">Hoy</option><option value="manana">Mañana</option></select>
              <button id="crRutaGenerar" type="button" class="cr-btn primary">🛣 Generar Ruta</button>
            </div>
            <div id="crRutaMapa" class="cr-map-placeholder" style="height:350px;">
              <div style="text-align:center;"><div style="font-size:2rem;margin-bottom:8px;">🛣</div><div>Selecciona un repartidor para ver su ruta</div></div>
            </div>
          </div>
          <div class="cr-card">
            <h3>📋 Paradas Programadas</h3>
            <div id="crRutaParadas" style="font-size:0.55rem;color:#64748b;">Sin ruta generada</div>
          </div>
        </div>

        <!-- ── SECTION: PENALIZACIONES ── -->
        <div class="cr-section" id="crSecPenalizaciones" data-cr-section="penalizaciones">
          <div class="cr-card">
            <h3>⚠️ Penalizaciones</h3>
            <p style="font-size:0.52rem;color:#64748b;margin:0 0 12px 0;">Registro de penalizaciones para repartidores: retardos, faltantes, incumplimientos, etc.</p>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr auto;gap:8px;align-items:end;margin-bottom:14px;">
              <div><label style="font-size:0.48rem;font-weight:700;color:#64748b;">Repartidor</label><select id="crPenRep" class="cr-select" style="width:100%;"></select></div>
              <div><label style="font-size:0.48rem;font-weight:700;color:#64748b;">Motivo</label><input id="crPenMotivo" type="text" class="cr-input" placeholder="Ej: Retardo, Mercancía dañada..."></div>
              <div><label style="font-size:0.48rem;font-weight:700;color:#64748b;">Monto</label><input id="crPenMonto" type="number" class="cr-input" placeholder="$0.00" min="0" step="0.01"></div>
              <button id="crPenAgregar" type="button" class="cr-btn danger" style="white-space:nowrap;">+ Registrar</button>
            </div>
            <table class="cr-table">
              <thead><tr><th>Fecha</th><th>Repartidor</th><th>Motivo</th><th>Monto</th><th>Acciones</th></tr></thead>
              <tbody id="crPenTabla"><tr><td colspan="5" style="text-align:center;color:#94a3b8;padding:20px;">Sin penalizaciones</td></tr></tbody>
            </table>
          </div>
        </div>

      </div> <!-- /cr-main -->
    </div> <!-- /cr-body -->
  </div>
</div>'''

if old_panel in content:
    content = content.replace(old_panel, new_panel, 1)
    print("  2. Control panel HTML replaced with full module")
else:
    errors.append("2: Could not find old panel HTML")

print("PART 2 done: Panel HTML")

# ============================================================
# PART 3: Replace the JS block
# ============================================================
old_js_start = '''<!-- ═══════════════════════════════════════════════════════════════
     MÓDULO CONTROL DE REPARTIDORES — Script
════════════════════════════════════════════════════════════════ -->
<script>
(function() {
    'use strict';
    var ZONAS_KEY = 'config_zonas_reparto';'''

# Find the full old JS block
idx_start = content.find(old_js_start)
if idx_start < 0:
    errors.append("3: Could not find old JS block start")
    print("  3. FAILED: JS block start not found")
else:
    # Find the closing of this IIFE
    end_marker = "})();\n</script>\n\n</body>"
    idx_end = content.find(end_marker, idx_start)
    if idx_end < 0:
        # Try alternate
        end_marker = "})();\n</script>\n</body>"
        idx_end = content.find(end_marker, idx_start)
    
    if idx_end < 0:
        errors.append("3: Could not find old JS block end")
        print("  3. FAILED: JS block end not found")
    else:
        old_js = content[idx_start:idx_end + len(end_marker)]
        
        new_js = '''<!-- ═══════════════════════════════════════════════════════════════
     MÓDULO CONTROL DE REPARTO — Script completo
════════════════════════════════════════════════════════════════ -->
<script>
(function() {
    'use strict';
    var ZONAS_KEY = 'config_zonas_reparto';
    var REPS_KEY = 'config_repartidores';
    var CONCEPTOS_KEY = 'config_conceptos_visita';
    var HORARIOS_KEY = 'config_horarios_repartidores';
    var GASTOS_KEY = 'config_gastos_empleado';
    var CHECKS_KEY = 'config_checks_asistencia';
    var PENALIZACIONES_KEY = 'config_penalizaciones_rep';
    var ENT_COL = 'delivery_orders';
    var esc = window._escHtml || function(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');};

    function lsGet(k,d){try{return JSON.parse(localStorage.getItem(k)||JSON.stringify(d));}catch(e){return d;}}
    function lsSet(k,v){localStorage.setItem(k,JSON.stringify(v));}
    function fmtDate(d){if(!d)return'—';try{var dt=d.toDate?d.toDate():new Date(d);return dt.toLocaleDateString('es-MX',{day:'2-digit',month:'short',year:'numeric'});}catch(e){return String(d);}}
    function fmtMoney(n){return'$'+Number(n||0).toFixed(2);}
    function getCRDB(){return window.firebase?window.firebase.firestore():null;}

    // ── DATA GETTERS ──
    function getZonas(){return lsGet(ZONAS_KEY,[]);}
    function saveZonas(z){lsSet(ZONAS_KEY,z);}
    function getReps(){return lsGet(REPS_KEY,[]);}
    function saveReps(r){lsSet(REPS_KEY,r);}
    function getConceptos(){return lsGet(CONCEPTOS_KEY,[
        {nombre:'Cliente no encontrado',tipo:'no_entrega'},
        {nombre:'Dirección incorrecta',tipo:'no_entrega'},
        {nombre:'Cliente canceló',tipo:'no_entrega'},
        {nombre:'Reagendar para otro día',tipo:'reagendar'},
        {nombre:'Entrega parcial',tipo:'parcial'},
        {nombre:'Zona insegura',tipo:'no_entrega'},
        {nombre:'Horario no disponible',tipo:'reagendar'}
    ]);}
    function saveConceptos(c){lsSet(CONCEPTOS_KEY,c);}
    function getHorarios(){return lsGet(HORARIOS_KEY,[]);}
    function saveHorarios(h){lsSet(HORARIOS_KEY,h);}
    function getGastos(){return lsGet(GASTOS_KEY,[]);}
    function saveGastos(g){lsSet(GASTOS_KEY,g);}
    function getChecks(){return lsGet(CHECKS_KEY,[]);}
    function saveChecks(c){lsSet(CHECKS_KEY,c);}
    function getPenalizaciones(){return lsGet(PENALIZACIONES_KEY,[]);}
    function savePenalizaciones(p){lsSet(PENALIZACIONES_KEY,p);}

    // ── PANEL OPEN/CLOSE ──
    var panel = document.getElementById('panelControlRepartidores');
    var allEntregas = [];
    var selectedPedidos = {};

    function openControlReparto(){
        if(panel) panel.style.display='flex';
        cargarEntregas();
        renderActiveSection();
    }
    function closeControlReparto(){
        if(panel) panel.style.display='none';
    }
    window.openControlRepartidoresGlobal = openControlReparto;

    document.getElementById('ctrlRepBack').addEventListener('click',function(){
        closeControlReparto();
        var ini=document.getElementById('inicio-sistema');if(ini)ini.style.display='';
    });
    document.getElementById('ctrlRepBtnRefresh').addEventListener('click',function(){cargarEntregas();renderActiveSection();});

    // ── SIDEBAR NAVIGATION ──
    var sidebarBtns = panel.querySelectorAll('.cr-sidebar-btn[data-cr-section]');
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
        updateSidebarResumen();
    }

    // ── POPULATE SELECTS ──
    function populateZonaSelects(){
        var zonas=getZonas();
        document.querySelectorAll('#cliFormZona,#ctrlRepFiltroZona,#configRepartidorZona,#crGeocercaFiltroZona').forEach(function(sel){
            var cur=sel.value;
            var opts='<option value="">'+((sel.id==='cliFormZona'||sel.id==='configRepartidorZona')?'— Sin zona —':'Todas las zonas')+'</option>';
            zonas.forEach(function(z){opts+='<option value="'+esc(z.nombre)+'"'+(cur===z.nombre?' selected':'')+'>'+esc(z.nombre)+'</option>';});
            sel.innerHTML=opts;if(cur)sel.value=cur;
        });
    }
    function populateRepSelects(){
        var reps=getReps().filter(function(r){return r.activo!==false;});
        document.querySelectorAll('#ctrlRepAsignarA,#crGastoFiltroRep,#crCheckFiltroRep,#crHorarioRep,#crRutaRep,#crPenRep').forEach(function(sel){
            var cur=sel.value;
            var first = sel.id==='crGastoFiltroRep'||sel.id==='crCheckFiltroRep' ? '<option value="">Todos</option>' : '<option value="">— Seleccionar —</option>';
            var opts=first;
            reps.forEach(function(r){opts+='<option value="'+esc(r.id)+'">'+esc(r.nombre)+(r.zona?' ('+esc(r.zona)+')':'')+'</option>';});
            sel.innerHTML=opts;if(cur)sel.value=cur;
        });
    }

    // ── LOAD ENTREGAS ──
    function cargarEntregas(){
        var db=getCRDB();if(!db)return;
        db.collection(ENT_COL).orderBy('creadoEn','desc').get().then(function(snap){
            allEntregas=[];
            snap.forEach(function(doc){var d=doc.data();d.id=doc.id;allEntregas.push(d);});
            renderActiveSection();
        }).catch(function(err){console.error('CR: Error cargando entregas:',err);});
    }

    // ── SIDEBAR RESUMEN ──
    function updateSidebarResumen(){
        var el=document.getElementById('crSidebarResumen');if(!el)return;
        var reps=getReps().filter(function(r){return r.activo!==false;});
        var sinA=allEntregas.filter(function(e){return!e.repartidorId&&e.estado!=='entregada';}).length;
        el.innerHTML='<div>👥 '+reps.length+' repartidores</div><div>📦 '+allEntregas.length+' entregas</div><div>📬 '+sinA+' sin asignar</div>';
    }

    // ── DASHBOARD ──
    function renderDashboard(){
        var sinA=allEntregas.filter(function(e){return!e.repartidorId&&e.estado!=='entregada';}).length;
        var asig=allEntregas.filter(function(e){return e.repartidorId&&!e.recibidoPorRepartidor&&e.estado!=='entregada';}).length;
        var rec=allEntregas.filter(function(e){return e.recibidoPorRepartidor&&e.estado!=='entregada'&&e.estado!=='no_entregada';}).length;
        var ent=allEntregas.filter(function(e){return e.estado==='entregada';}).length;
        var noEnt=allEntregas.filter(function(e){return e.estado==='no_entregada';}).length;
        var reps=getReps().filter(function(r){return r.activo!==false;});
        var el=function(id,v){var e=document.getElementById(id);if(e)e.textContent=v;};
        el('crStatSinAsignar',sinA);el('crStatAsignados',asig);el('crStatRecibidos',rec);
        el('crStatEntregados',ent);el('crStatNoEntregados',noEnt);el('crStatRepartidores',reps.length);

        // Activity
        var actEl=document.getElementById('crDashActivity');
        if(actEl){
            var recent=allEntregas.slice(0,15);
            if(!recent.length){actEl.innerHTML='<div style="text-align:center;color:#94a3b8;padding:12px;">Sin actividad</div>';return;}
            actEl.innerHTML=recent.map(function(e){
                var badge=e.estado==='entregada'?'background:#f0fdf4;color:#16a34a':e.estado==='no_entregada'?'background:#fef2f2;color:#dc2626':'background:#eff6ff;color:#1e40af';
                return '<div style="display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid #f1f5f9;">'+
                    '<span class="cr-badge" style="'+badge+'">'+esc(e.estado||'pendiente')+'</span>'+
                    '<span style="font-weight:700;">'+esc(e.folioProduccion||e.id)+'</span>'+
                    '<span style="color:#94a3b8;">'+esc(e.cliente||'—')+'</span>'+
                    (e.repartidorNombre?'<span style="margin-left:auto;font-size:0.48rem;color:#6b7280;">🚚 '+esc(e.repartidorNombre)+'</span>':'')+
                '</div>';
            }).join('');
        }

        // Repartidores status
        var rsEl=document.getElementById('crDashRepartidoresStatus');
        if(rsEl){
            if(!reps.length){rsEl.innerHTML='<div style="text-align:center;color:#94a3b8;font-size:0.55rem;padding:12px;">Sin repartidores. Ve a la sección Repartidores para agregar.</div>';return;}
            rsEl.innerHTML='<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:8px;">'+reps.map(function(r){
                var asignados=allEntregas.filter(function(e){return e.repartidorId===r.id;}).length;
                var entregados=allEntregas.filter(function(e){return e.repartidorId===r.id&&e.estado==='entregada';}).length;
                return '<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:10px;">'+
                    '<div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;">'+
                        '<div style="width:30px;height:30px;border-radius:50%;background:#1e40af;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:0.6rem;">'+esc(r.nombre.charAt(0).toUpperCase())+'</div>'+
                        '<div><div style="font-weight:800;font-size:0.58rem;">'+esc(r.nombre)+'</div><div style="font-size:0.45rem;color:#64748b;">'+esc(r.zona||'Sin zona')+'</div></div>'+
                    '</div>'+
                    '<div style="display:flex;gap:6px;">'+
                        '<span style="flex:1;text-align:center;background:#eff6ff;border-radius:4px;padding:3px;font-size:0.45rem;font-weight:700;color:#1e40af;">'+asignados+' asig.</span>'+
                        '<span style="flex:1;text-align:center;background:#f0fdf4;border-radius:4px;padding:3px;font-size:0.45rem;font-weight:700;color:#16a34a;">'+entregados+' ent.</span>'+
                    '</div>'+
                '</div>';
            }).join('')+'</div>';
        }
    }

    // ── LOCALIZACIÓN ──
    function renderLocalizacion(){
        var container=document.getElementById('crMapaGeneral');
        if(!container||container.dataset.loaded)return;
        var reps=getReps().filter(function(r){return r.activo!==false;});
        var html='<div style="position:absolute;inset:0;background:linear-gradient(135deg,#e0f2fe,#dbeafe);display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius:10px;">'+
            '<div style="font-size:2rem;margin-bottom:8px;">🗺</div>'+
            '<div style="font-size:0.65rem;font-weight:800;color:#1e40af;margin-bottom:10px;">Mapa de Localización</div>'+
            '<div style="font-size:0.5rem;color:#64748b;margin-bottom:12px;">'+reps.length+' repartidores registrados</div>'+
            '<div style="display:flex;flex-wrap:wrap;gap:6px;justify-content:center;max-width:90%;">'+
            reps.map(function(r){
                return '<div style="background:#fff;border:1px solid #bfdbfe;border-radius:6px;padding:6px 10px;display:flex;align-items:center;gap:4px;">'+
                    '<span style="color:#3b82f6;">📍</span><span style="font-size:0.5rem;font-weight:700;">'+esc(r.nombre)+'</span>'+
                    '<span style="font-size:0.45rem;color:#94a3b8;">'+esc(r.zona||'')+'</span></div>';
            }).join('')+'</div>'+
            '<div style="margin-top:12px;font-size:0.45rem;color:#94a3b8;">Integra Google Maps API para ver ubicaciones en tiempo real</div></div>';
        container.innerHTML=html;
    }

    // ── PEDIDOS ──
    function renderPedidos(){
        var list=document.getElementById('ctrlRepPedidosList');if(!list)return;
        var fZona=(document.getElementById('ctrlRepFiltroZona')||{}).value||'';
        var fEstado=(document.getElementById('ctrlRepFiltroEstado')||{}).value||'';
        var busq=((document.getElementById('ctrlRepBuscador')||{}).value||'').trim().toUpperCase();

        var filtered=allEntregas.filter(function(e){
            if(fZona&&e.zona!==fZona)return false;
            if(fEstado==='sin_asignar'&&e.repartidorId)return false;
            if(fEstado==='asignado'&&(!e.repartidorId||e.recibidoPorRepartidor))return false;
            if(fEstado==='recibido'&&(!e.recibidoPorRepartidor||e.estado==='entregada'))return false;
            if(fEstado==='en_camino'&&e.estado!=='en_camino')return false;
            if(fEstado==='entregada'&&e.estado!=='entregada')return false;
            if(busq){var h=(e.folioProduccion||'').toUpperCase().indexOf(busq)>=0||(e.cliente||'').toUpperCase().indexOf(busq)>=0||(e.id||'').toUpperCase().indexOf(busq)>=0;if(!h)return false;}
            return true;
        });

        if(!filtered.length){list.innerHTML='<div style="text-align:center;color:#94a3b8;padding:30px;font-size:0.6rem;">Sin pedidos en este filtro</div>';updateAsignBar();return;}

        var repMap={};getReps().forEach(function(r){repMap[r.id]=r;});
        list.innerHTML=filtered.map(function(e){
            var rep=e.repartidorId?repMap[e.repartidorId]:null;
            var estadoColors={pendiente:'#f59e0b',en_camino:'#3b82f6',entregada:'#10b981',no_entregada:'#ef4444'};
            var estadoIcos={pendiente:'📬',en_camino:'🚚',entregada:'✅',no_entregada:'❌'};
            var est=e.estado||'pendiente';
            var chk=selectedPedidos[e.id]?' checked':'';
            return '<div class="cr-card" style="padding:10px;">'+
                '<div style="display:flex;align-items:center;gap:8px;">'+
                    '<input type="checkbox" class="cr-ped-check" data-id="'+esc(e.id)+'"'+chk+' style="width:16px;height:16px;cursor:pointer;flex-shrink:0;">'+
                    '<div style="flex:1;">'+
                        '<div style="display:flex;align-items:center;gap:6px;margin-bottom:3px;">'+
                            '<span style="font-weight:900;font-size:0.62rem;color:#0f172a;">'+esc(e.folioProduccion||e.id)+'</span>'+
                            '<span class="cr-badge" style="background:'+(estadoColors[est]||'#94a3b8')+'20;color:'+(estadoColors[est]||'#94a3b8')+';">'+(estadoIcos[est]||'')+ ' '+esc(est)+'</span>'+
                            (rep?'<span class="cr-badge" style="background:#eff6ff;color:#1e40af;">🚚 '+esc(rep.nombre)+'</span>':'<span class="cr-badge" style="background:#fef2f2;color:#dc2626;">⚠️ Sin asignar</span>')+
                            (e.recibidoPorRepartidor?'<span class="cr-badge" style="background:#f0fdf4;color:#16a34a;">✅ Recibido</span>':'')+
                        '</div>'+
                        '<div style="font-size:0.5rem;color:#64748b;">'+esc(e.cliente||'—')+' · '+esc(e.producto||'—')+' · Cant: '+esc(e.cantidad||'—')+' · '+esc(e.zona||'Sin zona')+'</div>'+
                        (e.adeudo?'<div style="font-size:0.5rem;color:#ef4444;font-weight:700;">Adeudo: $'+esc(e.adeudo)+'</div>':'')+
                        (e.conceptoNoEntrega?'<div style="font-size:0.5rem;color:#f59e0b;font-weight:700;">📋 '+esc(e.conceptoNoEntrega)+'</div>':'')+
                    '</div>'+
                    (e.repartidorId?'<button class="cr-btn danger" data-action="desasignar" data-id="'+esc(e.id)+'" style="font-size:0.45rem;">✕</button>':'')+
                '</div>'+
            '</div>';
        }).join('');

        list.querySelectorAll('.cr-ped-check').forEach(function(cb){
            cb.addEventListener('change',function(){selectedPedidos[cb.dataset.id]=cb.checked;if(!cb.checked)delete selectedPedidos[cb.dataset.id];updateAsignBar();});
        });
        list.querySelectorAll('[data-action="desasignar"]').forEach(function(btn){
            btn.addEventListener('click',function(){
                var db=getCRDB();if(!db)return;var id=btn.dataset.id;
                db.collection(ENT_COL).doc(id).update({repartidorId:null,repartidorNombre:null,estadoAsignacion:null,actualizadoEn:window.firebase.firestore.FieldValue.serverTimestamp()}).then(function(){
                    var e=allEntregas.find(function(x){return x.id===id;});if(e){e.repartidorId=null;e.repartidorNombre=null;}
                    renderPedidos();renderDashboard();
                });
            });
        });
        updateAsignBar();
    }

    function updateAsignBar(){
        var bar=document.getElementById('ctrlRepAsignacionBar');
        var count=Object.keys(selectedPedidos).filter(function(k){return selectedPedidos[k];}).length;
        var cEl=document.getElementById('ctrlRepSelCount');if(cEl)cEl.textContent=count+' sel.';
        if(bar)bar.style.display=count>0?'':'none';
    }

    // Select all
    var btnSelAll=document.getElementById('ctrlRepBtnSelAll');
    if(btnSelAll)btnSelAll.addEventListener('click',function(){
        var checks=document.querySelectorAll('#ctrlRepPedidosList .cr-ped-check');
        var allC=Array.from(checks).every(function(c){return c.checked;});
        checks.forEach(function(c){c.checked=!allC;selectedPedidos[c.dataset.id]=!allC;if(allC)delete selectedPedidos[c.dataset.id];});
        updateAsignBar();
    });

    // Assign
    var btnAsignar=document.getElementById('ctrlRepBtnAsignar');
    if(btnAsignar)btnAsignar.addEventListener('click',function(){
        var repId=(document.getElementById('ctrlRepAsignarA')||{}).value;
        if(!repId){alert('Selecciona un repartidor');return;}
        var ids=Object.keys(selectedPedidos).filter(function(k){return selectedPedidos[k];});
        if(!ids.length){alert('Selecciona al menos un pedido');return;}
        var rep=getReps().find(function(r){return r.id===repId;});if(!rep)return;
        var db=getCRDB();if(!db)return;
        var batch=db.batch();
        ids.forEach(function(id){batch.update(db.collection(ENT_COL).doc(id),{repartidorId:rep.id,repartidorNombre:rep.nombre,estadoAsignacion:'asignado',fechaAsignacion:new Date().toISOString(),actualizadoEn:window.firebase.firestore.FieldValue.serverTimestamp()});});
        batch.commit().then(function(){
            ids.forEach(function(id){var e=allEntregas.find(function(x){return x.id===id;});if(e){e.repartidorId=rep.id;e.repartidorNombre=rep.nombre;}});
            selectedPedidos={};renderPedidos();renderDashboard();
            alert('✅ '+ids.length+' pedido(s) asignados a '+rep.nombre);
        }).catch(function(err){alert('Error: '+err.message);});
    });

    // Filters
    ['ctrlRepFiltroZona','ctrlRepFiltroEstado'].forEach(function(id){var el=document.getElementById(id);if(el)el.addEventListener('change',renderPedidos);});
    var busqEl=document.getElementById('ctrlRepBuscador');if(busqEl)busqEl.addEventListener('input',renderPedidos);

    // ── CONCEPTOS DE VISITA ──
    function renderConceptos(){
        var container=document.getElementById('crConceptosLista');if(!container)return;
        var conceptos=getConceptos();
        var tipoColors={no_entrega:'#ef4444',reagendar:'#f59e0b',parcial:'#3b82f6',otro:'#6b7280'};
        var tipoIcos={no_entrega:'❌',reagendar:'📅',parcial:'📦',otro:'📝'};
        if(!conceptos.length){container.innerHTML='<div style="text-align:center;color:#94a3b8;font-size:0.55rem;padding:12px;">Sin conceptos</div>';return;}
        container.innerHTML=conceptos.map(function(c,i){
            return '<div style="display:flex;align-items:center;gap:8px;padding:8px 12px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px;">'+
                '<span style="font-size:0.75rem;">'+(tipoIcos[c.tipo]||'📝')+'</span>'+
                '<span style="flex:1;font-size:0.58rem;font-weight:700;color:#334155;">'+esc(c.nombre)+'</span>'+
                '<span class="cr-badge" style="background:'+(tipoColors[c.tipo]||'#6b7280')+'15;color:'+(tipoColors[c.tipo]||'#6b7280')+';">'+esc(c.tipo)+'</span>'+
                '<button type="button" data-concepto-del="'+i+'" style="background:none;border:none;color:#ef4444;cursor:pointer;font-size:0.7rem;">✕</button>'+
            '</div>';
        }).join('');
        container.querySelectorAll('[data-concepto-del]').forEach(function(btn){
            btn.addEventListener('click',function(){var c=getConceptos();c.splice(parseInt(btn.dataset.conceptoDel),1);saveConceptos(c);renderConceptos();});
        });
    }
    var btnAddConcepto=document.getElementById('crConceptoAgregar');
    if(btnAddConcepto)btnAddConcepto.addEventListener('click',function(){
        var inp=document.getElementById('crConceptoNuevo');var tipo=(document.getElementById('crConceptoTipo')||{}).value||'otro';
        var nombre=(inp?inp.value:'').trim();if(!nombre)return;
        var c=getConceptos();c.push({nombre:nombre,tipo:tipo});saveConceptos(c);
        if(inp)inp.value='';renderConceptos();
    });

    // ── ZONAS ──
    function renderZonas(){
        var container=document.getElementById('configZonasLista');if(!container)return;
        var zonas=getZonas();
        if(!zonas.length){container.innerHTML='<div style="text-align:center;color:#94a3b8;font-size:0.55rem;padding:12px;">Sin zonas configuradas</div>';return;}
        container.innerHTML=zonas.map(function(z,i){
            var clientCount=0; // Could count from Firestore
            return '<div style="display:flex;align-items:center;gap:8px;padding:8px 12px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px;">'+
                '<span style="width:18px;height:18px;border-radius:4px;background:'+(z.color||'#3b82f6')+';flex-shrink:0;"></span>'+
                '<span style="flex:1;font-size:0.6rem;font-weight:800;color:#334155;">'+esc(z.nombre)+'</span>'+
                '<button type="button" data-zona-del="'+i+'" style="background:none;border:none;color:#ef4444;cursor:pointer;font-size:0.7rem;" title="Eliminar">✕</button>'+
            '</div>';
        }).join('');
        container.querySelectorAll('[data-zona-del]').forEach(function(btn){
            btn.addEventListener('click',function(){var z=getZonas();z.splice(parseInt(btn.dataset.zonaDel),1);saveZonas(z);renderZonas();populateZonaSelects();});
        });
    }
    var btnAddZona=document.getElementById('configZonaAgregar');
    if(btnAddZona)btnAddZona.addEventListener('click',function(){
        var inp=document.getElementById('configZonaNueva');var colorInp=document.getElementById('configZonaColor');
        var nombre=(inp?inp.value:'').trim();if(!nombre)return;
        var zonas=getZonas();
        if(zonas.some(function(z){return z.nombre.toUpperCase()===nombre.toUpperCase();})){alert('Ya existe esa zona');return;}
        zonas.push({nombre:nombre,color:colorInp?colorInp.value:'#3b82f6'});saveZonas(zonas);
        if(inp)inp.value='';renderZonas();populateZonaSelects();
    });

    // ── GEOCERCAS ──
    function renderGeocercas(){
        var container=document.getElementById('crMapaClientes');if(!container)return;
        var zonas=getZonas();
        var html='<div style="position:absolute;inset:0;background:linear-gradient(135deg,#f0fdf4,#ecfdf5);border-radius:10px;display:flex;flex-direction:column;align-items:center;justify-content:center;">'+
            '<div style="font-size:2rem;margin-bottom:8px;">📍</div>'+
            '<div style="font-size:0.65rem;font-weight:800;color:#166534;">Mapa de Clientes por Zona</div>'+
            '<div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:12px;justify-content:center;">'+
            zonas.map(function(z){
                return '<div style="display:flex;align-items:center;gap:4px;padding:4px 10px;background:#fff;border:1px solid #e2e8f0;border-radius:6px;">'+
                    '<span style="width:10px;height:10px;border-radius:50%;background:'+(z.color||'#3b82f6')+';"></span>'+
                    '<span style="font-size:0.5rem;font-weight:700;">'+esc(z.nombre)+'</span></div>';
            }).join('')+'</div>'+
            '<div style="margin-top:12px;font-size:0.45rem;color:#94a3b8;">Integra Google Maps API para ver clientes mapeados</div></div>';
        container.innerHTML=html;

        // Resumen
        var resEl=document.getElementById('crGeocercaResumen');
        if(resEl){
            if(!zonas.length){resEl.innerHTML='Sin zonas configuradas';return;}
            resEl.innerHTML='<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:6px;">'+
                zonas.map(function(z){
                    return '<div style="display:flex;align-items:center;gap:6px;padding:6px 10px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px;">'+
                        '<span style="width:12px;height:12px;border-radius:3px;background:'+(z.color||'#3b82f6')+';"></span>'+
                        '<span style="font-size:0.52rem;font-weight:700;">'+esc(z.nombre)+'</span></div>';
                }).join('')+'</div>';
        }
    }

    // ── GASTOS EMPLEADO ──
    function renderGastos(){
        var gastos=getGastos();
        var total=0,comb=0,alim=0,otros=0;
        gastos.forEach(function(g){
            var m=Number(g.monto||0);total+=m;
            if(g.categoria==='combustible')comb+=m;
            else if(g.categoria==='alimentos')alim+=m;
            else otros+=m;
        });
        var el=function(id,v){var e=document.getElementById(id);if(e)e.textContent=v;};
        el('crGastoTotal',fmtMoney(total));el('crGastoCombustible',fmtMoney(comb));el('crGastoAlimentos',fmtMoney(alim));el('crGastoOtros',fmtMoney(otros));

        var tbody=document.getElementById('crGastosTabla');
        if(tbody){
            if(!gastos.length){tbody.innerHTML='<tr><td colspan="6" style="text-align:center;color:#94a3b8;padding:20px;">Sin gastos registrados. Los repartidores reportan gastos desde la app móvil.</td></tr>';return;}
            tbody.innerHTML=gastos.map(function(g){
                return '<tr><td>'+esc(fmtDate(g.fecha))+'</td><td>'+esc(g.repartidor||'—')+'</td><td>'+esc(g.concepto||'—')+'</td><td style="font-weight:700;">'+fmtMoney(g.monto)+'</td><td>'+(g.evidencia?'📎':'—')+'</td>'+
                    '<td><span class="cr-badge" style="background:'+(g.aprobado?'#f0fdf4;color:#16a34a':'#fff7ed;color:#f59e0b')+'">'+(g.aprobado?'Aprobado':'Pendiente')+'</span></td></tr>';
            }).join('');
        }
    }

    // ── HORARIOS ──
    function renderHorarios(){
        var container=document.getElementById('crHorariosLista');if(!container)return;
        var horarios=getHorarios();var repMap={};getReps().forEach(function(r){repMap[r.id]=r;});
        if(!horarios.length){container.innerHTML='<div style="text-align:center;color:#94a3b8;font-size:0.55rem;padding:12px;">Sin horarios configurados</div>';return;}
        container.innerHTML='<table class="cr-table"><thead><tr><th>Repartidor</th><th>Entrada</th><th>Salida</th><th>Días</th><th>Acciones</th></tr></thead><tbody>'+
            horarios.map(function(h,i){
                var r=repMap[h.repId];
                return '<tr><td style="font-weight:700;">'+esc(r?r.nombre:h.repId)+'</td><td>'+esc(h.entrada||'—')+'</td><td>'+esc(h.salida||'—')+'</td><td>'+esc(h.dias||'—')+'</td>'+
                    '<td><button class="cr-btn danger" data-hor-del="'+i+'" style="font-size:0.45rem;">✕</button></td></tr>';
            }).join('')+'</tbody></table>';
        container.querySelectorAll('[data-hor-del]').forEach(function(btn){
            btn.addEventListener('click',function(){var h=getHorarios();h.splice(parseInt(btn.dataset.horDel),1);saveHorarios(h);renderHorarios();});
        });
    }
    var btnHorarioSave=document.getElementById('crHorarioGuardar');
    if(btnHorarioSave)btnHorarioSave.addEventListener('click',function(){
        var repId=(document.getElementById('crHorarioRep')||{}).value;
        var entrada=(document.getElementById('crHorarioEntrada')||{}).value;
        var salida=(document.getElementById('crHorarioSalida')||{}).value;
        var dias=(document.getElementById('crHorarioDias')||{}).value;
        if(!repId){alert('Selecciona un repartidor');return;}
        var h=getHorarios();
        var existing=h.findIndex(function(x){return x.repId===repId;});
        if(existing>=0) h[existing]={repId:repId,entrada:entrada,salida:salida,dias:dias};
        else h.push({repId:repId,entrada:entrada,salida:salida,dias:dias});
        saveHorarios(h);renderHorarios();
    });

    // ── CHECKS ASISTENCIA ──
    function renderChecks(){
        var checks=getChecks();
        var hoy=new Date().toISOString().split('T')[0];
        var checksHoy=checks.filter(function(c){return(c.fecha||'').startsWith(hoy);});
        var reps=getReps().filter(function(r){return r.activo!==false;});
        var presentes=checksHoy.filter(function(c){return c.entrada;}).length;
        var ausentes=reps.length-presentes;
        var retardos=checksHoy.filter(function(c){return c.retardo;}).length;

        var el=function(id,v){var e=document.getElementById(id);if(e)e.textContent=v;};
        el('crCheckPresentes',presentes);el('crCheckAusentes',ausentes<0?0:ausentes);el('crCheckRetardos',retardos);el('crCheckHorasExtra','0');

        var tbody=document.getElementById('crChecksTabla');
        if(tbody){
            if(!checks.length){tbody.innerHTML='<tr><td colspan="7" style="text-align:center;color:#94a3b8;padding:20px;">Sin registros. Los checks se generan desde la app móvil del repartidor.</td></tr>';return;}
            var repMap={};getReps().forEach(function(r){repMap[r.id]=r;});
            tbody.innerHTML=checks.slice(0,50).map(function(c){
                var r=repMap[c.repId];
                return '<tr><td>'+esc(c.fecha||'—')+'</td><td style="font-weight:700;">'+esc(r?r.nombre:c.repId)+'</td><td>'+esc(c.entrada||'—')+'</td><td>'+esc(c.salida||'—')+'</td><td>'+esc(c.horas||'—')+'</td>'+
                    '<td><span class="cr-badge" style="background:'+(c.retardo?'#fef2f2;color:#ef4444':'#f0fdf4;color:#16a34a')+'">'+(c.retardo?'Retardo':'OK')+'</span></td>'+
                    '<td style="font-size:0.45rem;">'+esc(c.ubicacion||'—')+'</td></tr>';
            }).join('');
        }
    }

    // ── REPARTIDORES ──
    function renderRepartidoresSection(){
        var container=document.getElementById('configRepartidoresLista');if(!container)return;
        var reps=getReps();
        if(!reps.length){container.innerHTML='<div style="text-align:center;color:#94a3b8;font-size:0.55rem;padding:16px;">Sin repartidores registrados</div>';return;}
        container.innerHTML=reps.map(function(r,i){
            return '<div style="display:flex;align-items:center;gap:10px;padding:10px 12px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;">'+
                '<div style="width:36px;height:36px;border-radius:50%;background:#1e40af;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:0.65rem;flex-shrink:0;">'+esc(r.nombre.charAt(0).toUpperCase())+'</div>'+
                '<div style="flex:1;">'+
                    '<div style="font-size:0.62rem;font-weight:800;color:#0f172a;">'+esc(r.nombre)+'</div>'+
                    '<div style="font-size:0.48rem;color:#64748b;">📱 '+esc(r.telefono||'—')+' · 🏷 '+esc(r.zona||'Sin zona')+' · ID: '+esc(r.id)+'</div>'+
                '</div>'+
                '<span class="cr-badge" style="'+(r.activo!==false?'background:#f0fdf4;color:#16a34a':'background:#fef2f2;color:#dc2626')+'">'+(r.activo!==false?'Activo':'Inactivo')+'</span>'+
                '<button type="button" class="cr-btn" data-rep-toggle="'+i+'" style="font-size:0.45rem;background:#f1f5f9;color:#475569;border:1px solid #d1d5db;">'+(r.activo!==false?'⏸ Desactivar':'▶ Activar')+'</button>'+
                '<button type="button" data-rep-del="'+i+'" style="background:none;border:none;color:#ef4444;cursor:pointer;font-size:0.75rem;">✕</button>'+
            '</div>';
        }).join('');
        container.querySelectorAll('[data-rep-del]').forEach(function(btn){
            btn.addEventListener('click',function(){if(!confirm('¿Eliminar repartidor?'))return;var r=getReps();r.splice(parseInt(btn.dataset.repDel),1);saveReps(r);renderRepartidoresSection();populateRepSelects();});
        });
        container.querySelectorAll('[data-rep-toggle]').forEach(function(btn){
            btn.addEventListener('click',function(){var r=getReps();var idx=parseInt(btn.dataset.repToggle);r[idx].activo=r[idx].activo===false?true:false;saveReps(r);renderRepartidoresSection();});
        });
    }
    var btnAddRep=document.getElementById('configRepartidorAgregar');
    if(btnAddRep)btnAddRep.addEventListener('click',function(){
        var nombre=((document.getElementById('configRepartidorNombre')||{}).value||'').trim();
        var tel=((document.getElementById('configRepartidorTel')||{}).value||'').trim();
        var zona=((document.getElementById('configRepartidorZona')||{}).value||'');
        if(!nombre){alert('Nombre requerido');return;}
        var reps=getReps();
        reps.push({id:'REP-'+Date.now(),nombre:nombre,telefono:tel,zona:zona,activo:true,creadoEn:new Date().toISOString()});
        saveReps(reps);
        var n=document.getElementById('configRepartidorNombre');if(n)n.value='';
        var t=document.getElementById('configRepartidorTel');if(t)t.value='';
        renderRepartidoresSection();populateRepSelects();
    });

    // ── RUTAS ──
    function renderRutas(){
        var container=document.getElementById('crRutaParadas');if(!container)return;
        var repId=(document.getElementById('crRutaRep')||{}).value;
        if(!repId){container.innerHTML='<div style="color:#94a3b8;font-size:0.55rem;">Selecciona un repartidor para ver sus paradas</div>';return;}
        var rep=getReps().find(function(r){return r.id===repId;});
        var pedidos=allEntregas.filter(function(e){return e.repartidorId===repId&&e.estado!=='entregada';});
        if(!pedidos.length){container.innerHTML='<div style="color:#94a3b8;font-size:0.55rem;">Sin pedidos asignados a '+(rep?rep.nombre:'este repartidor')+'</div>';return;}
        container.innerHTML=pedidos.map(function(e,i){
            return '<div style="display:flex;align-items:center;gap:8px;padding:8px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px;margin-bottom:4px;">'+
                '<span style="width:24px;height:24px;border-radius:50%;background:#1e40af;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:0.5rem;flex-shrink:0;">'+(i+1)+'</span>'+
                '<div style="flex:1;"><div style="font-weight:700;font-size:0.55rem;">'+esc(e.folioProduccion||e.id)+'</div><div style="font-size:0.48rem;color:#64748b;">'+esc(e.cliente||'—')+' · '+esc(e.direccion||'Sin dirección')+'</div></div>'+
                '<span class="cr-badge" style="background:#eff6ff;color:#1e40af;">'+esc(e.zona||'—')+'</span>'+
            '</div>';
        }).join('');
    }
    var rutaRepSel=document.getElementById('crRutaRep');if(rutaRepSel)rutaRepSel.addEventListener('change',renderRutas);
    var rutaGen=document.getElementById('crRutaGenerar');if(rutaGen)rutaGen.addEventListener('click',renderRutas);

    // ── PENALIZACIONES ──
    function renderPenalizacionesSec(){
        var pens=getPenalizaciones();var repMap={};getReps().forEach(function(r){repMap[r.id]=r;});
        var tbody=document.getElementById('crPenTabla');if(!tbody)return;
        if(!pens.length){tbody.innerHTML='<tr><td colspan="5" style="text-align:center;color:#94a3b8;padding:20px;">Sin penalizaciones registradas</td></tr>';return;}
        tbody.innerHTML=pens.map(function(p,i){
            var r=repMap[p.repId];
            return '<tr><td>'+esc(fmtDate(p.fecha))+'</td><td style="font-weight:700;">'+esc(r?r.nombre:p.repId)+'</td><td>'+esc(p.motivo||'—')+'</td><td style="font-weight:700;color:#ef4444;">'+fmtMoney(p.monto)+'</td>'+
                '<td><button class="cr-btn danger" data-pen-del="'+i+'" style="font-size:0.45rem;">✕</button></td></tr>';
        }).join('');
        tbody.querySelectorAll('[data-pen-del]').forEach(function(btn){
            btn.addEventListener('click',function(){var p=getPenalizaciones();p.splice(parseInt(btn.dataset.penDel),1);savePenalizaciones(p);renderPenalizacionesSec();});
        });
    }
    var btnAddPen=document.getElementById('crPenAgregar');
    if(btnAddPen)btnAddPen.addEventListener('click',function(){
        var repId=(document.getElementById('crPenRep')||{}).value;
        var motivo=((document.getElementById('crPenMotivo')||{}).value||'').trim();
        var monto=Number((document.getElementById('crPenMonto')||{}).value)||0;
        if(!repId){alert('Selecciona repartidor');return;}if(!motivo){alert('Ingresa motivo');return;}
        var pens=getPenalizaciones();
        pens.push({repId:repId,motivo:motivo,monto:monto,fecha:new Date().toISOString()});
        savePenalizaciones(pens);
        var m=document.getElementById('crPenMotivo');if(m)m.value='';
        var mt=document.getElementById('crPenMonto');if(mt)mt.value='';
        renderPenalizacionesSec();
    });

    // ── INIT ──
    setTimeout(function(){
        renderZonas();
        renderConceptos();
        renderRepartidoresSection();
        populateZonaSelects();
        populateRepSelects();
    },500);

})();
</script>

</body>'''
        
        content = content.replace(old_js, new_js, 1)
        print("  3. JS block replaced with full module script")

print("PART 3 done: JS replaced")

# ============================================================
# WRITE
# ============================================================
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "="*60)
if errors:
    print("PATCH APPLIED WITH WARNINGS:")
    for e in errors:
        print("  ⚠ " + e)
else:
    print("ALL PATCHES APPLIED SUCCESSFULLY!")
print("="*60)
