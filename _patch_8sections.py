#!/usr/bin/env python3
"""
Patch: Add 8 new sections to Control de Reparto
1. Historial de Entregas por Cliente
4. KPIs por Repartidor
5. Alertas en Tiempo Real
7. Inventario en Vehículo
8. Reagendamiento
9. Reportes Exportables
10. Comunicación Directa
11. Kilometraje
"""

FILE = '/workspaces/vistas/mockup.html'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()
errors = []

# ============================================================
# PART 1: Add new sidebar buttons
# ============================================================
old_sidebar_end = '''        <button class="cr-sidebar-btn" data-cr-section="penalizaciones"><span class="cr-ico">⚠️</span> Penalizaciones</button>
        <div style="flex:1;"></div>'''
new_sidebar_end = '''        <button class="cr-sidebar-btn" data-cr-section="penalizaciones"><span class="cr-ico">⚠️</span> Penalizaciones</button>
        <div style="padding:8px 14px 4px;font-size:0.42rem;font-weight:800;color:#475569;text-transform:uppercase;letter-spacing:1px;border-top:1px solid rgba(255,255,255,0.06);margin-top:4px;">Avanzado</div>
        <button class="cr-sidebar-btn" data-cr-section="historial"><span class="cr-ico">📜</span> Historial Cliente</button>
        <button class="cr-sidebar-btn" data-cr-section="kpis"><span class="cr-ico">📈</span> KPIs</button>
        <button class="cr-sidebar-btn" data-cr-section="alertas"><span class="cr-ico">🔔</span> Alertas</button>
        <button class="cr-sidebar-btn" data-cr-section="inventario"><span class="cr-ico">📋</span> Inv. Vehículo</button>
        <button class="cr-sidebar-btn" data-cr-section="reagendar"><span class="cr-ico">📅</span> Reagendamiento</button>
        <button class="cr-sidebar-btn" data-cr-section="reportes"><span class="cr-ico">📊</span> Reportes</button>
        <button class="cr-sidebar-btn" data-cr-section="comunicacion"><span class="cr-ico">💬</span> Comunicación</button>
        <button class="cr-sidebar-btn" data-cr-section="kilometraje"><span class="cr-ico">🛣️</span> Kilometraje</button>
        <div style="flex:1;"></div>'''
if old_sidebar_end in content:
    content = content.replace(old_sidebar_end, new_sidebar_end, 1)
    print("  1. Sidebar buttons added (8 new)")
else:
    errors.append("1: sidebar buttons not found")

# ============================================================
# PART 2: Add HTML sections before closing divs
# ============================================================
old_close = '''      </div> <!-- /cr-main -->
    </div> <!-- /cr-body -->
  </div>
</div>

<div id="panelEntregas"'''

new_sections = '''
        <!-- ── SECTION: HISTORIAL CLIENTE ── -->
        <div class="cr-section" id="crSecHistorial" data-cr-section="historial">
          <div class="cr-card">
            <h3>📜 Historial de Entregas por Cliente</h3>
            <p style="font-size:0.52rem;color:#64748b;margin:0 0 12px 0;">Consulta todas las entregas realizadas a un cliente, incluyendo motivos de no-entrega y reagendaciones.</p>
            <div class="cr-header-bar">
              <input id="crHistBuscar" type="text" class="cr-input" placeholder="🔍 Buscar cliente por nombre..." style="max-width:300px;">
              <select id="crHistFiltroEstado" class="cr-select">
                <option value="">Todos los estados</option>
                <option value="entregada">✅ Entregadas</option>
                <option value="no_entregada">❌ No entregadas</option>
                <option value="pendiente">📬 Pendientes</option>
              </select>
            </div>
          </div>
          <div id="crHistResultados" style="display:flex;flex-direction:column;gap:8px;"></div>
        </div>

        <!-- ── SECTION: KPIs ── -->
        <div class="cr-section" id="crSecKpis" data-cr-section="kpis">
          <div class="cr-header-bar">
            <select id="crKpiFiltroRep" class="cr-select"><option value="">Todos los repartidores</option></select>
            <select id="crKpiFiltroPeriodo" class="cr-select">
              <option value="semana">Esta semana</option>
              <option value="mes" selected>Este mes</option>
              <option value="todo">Todo el tiempo</option>
            </select>
          </div>
          <div class="cr-stats" id="crKpisStats">
            <div class="cr-stat"><div class="val" style="color:#10b981;" id="crKpiExito">0%</div><div class="lbl">% Entrega Exitosa</div></div>
            <div class="cr-stat"><div class="val" style="color:#3b82f6;" id="crKpiPromedio">0</div><div class="lbl">Entregas/Día</div></div>
            <div class="cr-stat"><div class="val" style="color:#f59e0b;" id="crKpiTiempo">—</div><div class="lbl">Tiempo Prom. Ruta</div></div>
            <div class="cr-stat"><div class="val" style="color:#8b5cf6;" id="crKpiPuntualidad">0%</div><div class="lbl">Puntualidad</div></div>
            <div class="cr-stat"><div class="val" style="color:#ef4444;" id="crKpiNoEntregas">0</div><div class="lbl">No Entregas</div></div>
            <div class="cr-stat"><div class="val" style="color:#0ea5e9;" id="crKpiCalificacion">—</div><div class="lbl">Calificación</div></div>
          </div>
          <div class="cr-card">
            <h3>📈 Ranking de Repartidores</h3>
            <table class="cr-table">
              <thead><tr><th>#</th><th>Repartidor</th><th>Entregas</th><th>% Éxito</th><th>Puntualidad</th><th>Calificación</th><th>Tendencia</th></tr></thead>
              <tbody id="crKpiRanking"><tr><td colspan="7" style="text-align:center;color:#94a3b8;padding:20px;">Cargando...</td></tr></tbody>
            </table>
          </div>
          <div class="cr-card">
            <h3>📊 Desempeño por Zona</h3>
            <div id="crKpiZonas" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:8px;"></div>
          </div>
        </div>

        <!-- ── SECTION: ALERTAS ── -->
        <div class="cr-section" id="crSecAlertas" data-cr-section="alertas">
          <div class="cr-stats">
            <div class="cr-stat"><div class="val" style="color:#ef4444;" id="crAlertaCriticas">0</div><div class="lbl">🔴 Críticas</div></div>
            <div class="cr-stat"><div class="val" style="color:#f59e0b;" id="crAlertaWarnings">0</div><div class="lbl">🟡 Advertencias</div></div>
            <div class="cr-stat"><div class="val" style="color:#3b82f6;" id="crAlertaInfo">0</div><div class="lbl">🔵 Info</div></div>
          </div>
          <div class="cr-card">
            <h3>🔔 Alertas en Tiempo Real</h3>
            <p style="font-size:0.52rem;color:#64748b;margin:0 0 8px 0;">Notificaciones automáticas según eventos de la app móvil del repartidor.</p>
            <div style="display:flex;gap:6px;margin-bottom:10px;">
              <select id="crAlertaFiltro" class="cr-select">
                <option value="">Todas</option>
                <option value="critica">🔴 Críticas</option>
                <option value="warning">🟡 Advertencias</option>
                <option value="info">🔵 Informativas</option>
              </select>
              <button id="crAlertaLimpiar" type="button" class="cr-btn" style="background:#f3f4f6;color:#64748b;border:1px solid #d1d5db;">🗑 Limpiar leídas</button>
            </div>
            <div id="crAlertasLista" style="display:flex;flex-direction:column;gap:6px;max-height:500px;overflow-y:auto;"></div>
          </div>
          <div class="cr-card">
            <h3>⚙️ Configuración de Alertas</h3>
            <div style="display:flex;flex-direction:column;gap:8px;" id="crAlertaConfig">
              <label style="display:flex;align-items:center;gap:8px;font-size:0.55rem;font-weight:700;color:#334155;cursor:pointer;"><input type="checkbox" id="crAlertNoEntrega" checked> Repartidor reporta no-entrega</label>
              <label style="display:flex;align-items:center;gap:8px;font-size:0.55rem;font-weight:700;color:#334155;cursor:pointer;"><input type="checkbox" id="crAlertRetardo" checked> Retardo en check de entrada</label>
              <label style="display:flex;align-items:center;gap:8px;font-size:0.55rem;font-weight:700;color:#334155;cursor:pointer;"><input type="checkbox" id="crAlertFueraZona" checked> Repartidor fuera de geocerca</label>
              <label style="display:flex;align-items:center;gap:8px;font-size:0.55rem;font-weight:700;color:#334155;cursor:pointer;"><input type="checkbox" id="crAlertGasto" checked> Gasto elevado registrado</label>
              <label style="display:flex;align-items:center;gap:8px;font-size:0.55rem;font-weight:700;color:#334155;cursor:pointer;"><input type="checkbox" id="crAlertSinMovimiento"> Sin movimiento por más de 30 min</label>
              <label style="display:flex;align-items:center;gap:8px;font-size:0.55rem;font-weight:700;color:#334155;cursor:pointer;"><input type="checkbox" id="crAlertEntregaCompleta" checked> Repartidor completó todas las entregas</label>
            </div>
          </div>
        </div>

        <!-- ── SECTION: INVENTARIO EN VEHÍCULO ── -->
        <div class="cr-section" id="crSecInventario" data-cr-section="inventario">
          <div class="cr-header-bar">
            <select id="crInvFiltroRep" class="cr-select"><option value="">Seleccionar repartidor</option></select>
          </div>
          <div class="cr-stats">
            <div class="cr-stat"><div class="val" style="color:#3b82f6;" id="crInvCargados">0</div><div class="lbl">Productos Cargados</div></div>
            <div class="cr-stat"><div class="val" style="color:#10b981;" id="crInvEntregados">0</div><div class="lbl">Entregados</div></div>
            <div class="cr-stat"><div class="val" style="color:#f59e0b;" id="crInvPendientes">0</div><div class="lbl">Pendientes</div></div>
            <div class="cr-stat"><div class="val" style="color:#ef4444;" id="crInvDevueltos">0</div><div class="lbl">Devueltos</div></div>
          </div>
          <div class="cr-card">
            <h3>📋 Inventario de Carga Actual</h3>
            <p style="font-size:0.52rem;color:#64748b;margin:0 0 10px 0;">Mercancía que lleva el repartidor. Se actualiza con cada escaneo de entrega en la app móvil.</p>
            <table class="cr-table">
              <thead><tr><th>Folio</th><th>Producto</th><th>Cantidad</th><th>Cliente</th><th>Estado</th><th>Hora Carga</th></tr></thead>
              <tbody id="crInvTabla"><tr><td colspan="6" style="text-align:center;color:#94a3b8;padding:20px;">Selecciona un repartidor para ver su carga</td></tr></tbody>
            </table>
          </div>
        </div>

        <!-- ── SECTION: REAGENDAMIENTO ── -->
        <div class="cr-section" id="crSecReagendar" data-cr-section="reagendar">
          <div class="cr-stats">
            <div class="cr-stat"><div class="val" style="color:#f59e0b;" id="crReagPendientes">0</div><div class="lbl">Pend. Reagendar</div></div>
            <div class="cr-stat"><div class="val" style="color:#3b82f6;" id="crReagProgramados">0</div><div class="lbl">Reagendados</div></div>
            <div class="cr-stat"><div class="val" style="color:#ef4444;" id="crReagVencidos">0</div><div class="lbl">Vencidos</div></div>
          </div>
          <div class="cr-card">
            <h3>📅 Pedidos No Entregados — Reagendamiento</h3>
            <p style="font-size:0.52rem;color:#64748b;margin:0 0 10px 0;">Pedidos que no se pudieron entregar y necesitan reprogramarse. Se generan automáticamente desde los conceptos de visita de la app móvil.</p>
            <div id="crReagLista" style="display:flex;flex-direction:column;gap:8px;"></div>
          </div>
        </div>

        <!-- ── SECTION: REPORTES ── -->
        <div class="cr-section" id="crSecReportes" data-cr-section="reportes">
          <div class="cr-card">
            <h3>📊 Reportes Exportables</h3>
            <p style="font-size:0.52rem;color:#64748b;margin:0 0 14px 0;">Genera reportes en formato imprimible o CSV para análisis externo.</p>
            <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px;">
              <div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:10px;padding:14px;cursor:pointer;" id="crRepEntregas">
                <div style="font-size:1.2rem;margin-bottom:6px;">📦</div>
                <div style="font-weight:800;font-size:0.62rem;color:#1e40af;margin-bottom:4px;">Reporte de Entregas</div>
                <div style="font-size:0.48rem;color:#64748b;">Todas las entregas por periodo, repartidor y zona. Incluye estados y conceptos de no-entrega.</div>
              </div>
              <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:10px;padding:14px;cursor:pointer;" id="crRepGastos">
                <div style="font-size:1.2rem;margin-bottom:6px;">💰</div>
                <div style="font-weight:800;font-size:0.62rem;color:#166534;margin-bottom:4px;">Reporte de Gastos</div>
                <div style="font-size:0.48rem;color:#64748b;">Gastos por repartidor, categoría y periodo. Incluye montos aprobados y pendientes.</div>
              </div>
              <div style="background:#faf5ff;border:1px solid #e9d5ff;border-radius:10px;padding:14px;cursor:pointer;" id="crRepAsistencia">
                <div style="font-size:1.2rem;margin-bottom:6px;">✅</div>
                <div style="font-weight:800;font-size:0.62rem;color:#7c3aed;margin-bottom:4px;">Reporte de Asistencia</div>
                <div style="font-size:0.48rem;color:#64748b;">Checks de entrada/salida, retardos, faltas y horas extras por repartidor.</div>
              </div>
              <div style="background:#fff7ed;border:1px solid #fed7aa;border-radius:10px;padding:14px;cursor:pointer;" id="crRepKm">
                <div style="font-size:1.2rem;margin-bottom:6px;">🛣️</div>
                <div style="font-weight:800;font-size:0.62rem;color:#c2410c;margin-bottom:4px;">Reporte de Kilometraje</div>
                <div style="font-size:0.48rem;color:#64748b;">Km recorridos por repartidor, costo por km y viáticos asociados.</div>
              </div>
              <div style="background:#fef2f2;border:1px solid #fecaca;border-radius:10px;padding:14px;cursor:pointer;" id="crRepPenalizaciones">
                <div style="font-size:1.2rem;margin-bottom:6px;">⚠️</div>
                <div style="font-weight:800;font-size:0.62rem;color:#dc2626;margin-bottom:4px;">Reporte de Penalizaciones</div>
                <div style="font-size:0.48rem;color:#64748b;">Penalizaciones aplicadas por repartidor con motivos y montos descontados.</div>
              </div>
              <div style="background:#f0f9ff;border:1px solid #bae6fd;border-radius:10px;padding:14px;cursor:pointer;" id="crRepDesempeno">
                <div style="font-size:1.2rem;margin-bottom:6px;">📈</div>
                <div style="font-weight:800;font-size:0.62rem;color:#0369a1;margin-bottom:4px;">Reporte de Desempeño</div>
                <div style="font-size:0.48rem;color:#64748b;">KPIs, ranking, tendencias y comparativa entre repartidores por periodo.</div>
              </div>
            </div>
          </div>
          <div class="cr-card">
            <h3>⚙️ Filtros del Reporte</h3>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr auto;gap:8px;align-items:end;">
              <div><label style="font-size:0.48rem;font-weight:700;color:#64748b;">Desde</label><input id="crRepDesde" type="date" class="cr-input"></div>
              <div><label style="font-size:0.48rem;font-weight:700;color:#64748b;">Hasta</label><input id="crRepHasta" type="date" class="cr-input"></div>
              <div><label style="font-size:0.48rem;font-weight:700;color:#64748b;">Repartidor</label><select id="crRepFiltroRep" class="cr-select" style="width:100%;"><option value="">Todos</option></select></div>
              <button id="crRepGenerar" type="button" class="cr-btn primary" style="white-space:nowrap;">📄 Generar</button>
            </div>
            <div id="crRepPreview" style="margin-top:12px;min-height:60px;"></div>
          </div>
        </div>

        <!-- ── SECTION: COMUNICACIÓN ── -->
        <div class="cr-section" id="crSecComunicacion" data-cr-section="comunicacion">
          <div class="cr-card" style="height:calc(100vh - 160px);display:flex;flex-direction:column;">
            <h3>💬 Comunicación con Repartidores</h3>
            <div class="cr-header-bar" style="flex-shrink:0;">
              <select id="crChatRep" class="cr-select"><option value="">— Seleccionar repartidor —</option></select>
              <span id="crChatStatus" style="font-size:0.48rem;color:#94a3b8;">Sin conversación activa</span>
            </div>
            <div id="crChatMessages" style="flex:1;overflow-y:auto;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:10px;margin:8px 0;display:flex;flex-direction:column;gap:6px;">
              <div style="text-align:center;color:#94a3b8;font-size:0.55rem;padding:40px;">Selecciona un repartidor para iniciar conversación</div>
            </div>
            <div style="display:flex;gap:6px;flex-shrink:0;">
              <input id="crChatInput" type="text" class="cr-input" placeholder="Escribe un mensaje..." style="flex:1;" disabled>
              <button id="crChatSend" type="button" class="cr-btn primary" disabled>Enviar</button>
              <button id="crChatQuick" type="button" class="cr-btn" style="background:#f3f4f6;color:#64748b;border:1px solid #d1d5db;" title="Mensajes rápidos">⚡</button>
            </div>
            <div id="crChatQuickMenu" style="display:none;margin-top:6px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:8px;">
              <div style="font-size:0.48rem;font-weight:800;color:#64748b;margin-bottom:6px;">MENSAJES RÁPIDOS</div>
              <div style="display:flex;flex-wrap:wrap;gap:4px;">
                <button type="button" class="cr-quick-msg cr-btn" style="background:#eff6ff;color:#1e40af;border:1px solid #bfdbfe;font-size:0.48rem;" data-msg="¿Cuál es tu ubicación actual?">📍 Ubicación</button>
                <button type="button" class="cr-quick-msg cr-btn" style="background:#eff6ff;color:#1e40af;border:1px solid #bfdbfe;font-size:0.48rem;" data-msg="¿Cuántas entregas te faltan?">📦 Pendientes</button>
                <button type="button" class="cr-quick-msg cr-btn" style="background:#eff6ff;color:#1e40af;border:1px solid #bfdbfe;font-size:0.48rem;" data-msg="Regresa a sucursal cuando termines">🏢 Regresar</button>
                <button type="button" class="cr-quick-msg cr-btn" style="background:#eff6ff;color:#1e40af;border:1px solid #bfdbfe;font-size:0.48rem;" data-msg="Tienes una nueva asignación de carga">📋 Nueva carga</button>
                <button type="button" class="cr-quick-msg cr-btn" style="background:#fef2f2;color:#dc2626;border:1px solid #fecaca;font-size:0.48rem;" data-msg="URGENTE: Comunícate conmigo inmediatamente">🚨 Urgente</button>
                <button type="button" class="cr-quick-msg cr-btn" style="background:#f0fdf4;color:#16a34a;border:1px solid #bbf7d0;font-size:0.48rem;" data-msg="Buen trabajo hoy, gracias 👍">👍 Buen trabajo</button>
              </div>
            </div>
          </div>
        </div>

        <!-- ── SECTION: KILOMETRAJE ── -->
        <div class="cr-section" id="crSecKilometraje" data-cr-section="kilometraje">
          <div class="cr-header-bar">
            <select id="crKmFiltroRep" class="cr-select"><option value="">Todos los repartidores</option></select>
            <select id="crKmFiltroPeriodo" class="cr-select">
              <option value="hoy">Hoy</option>
              <option value="semana">Esta semana</option>
              <option value="mes" selected>Este mes</option>
            </select>
          </div>
          <div class="cr-stats">
            <div class="cr-stat"><div class="val" style="color:#0ea5e9;" id="crKmTotal">0</div><div class="lbl">Km Totales</div></div>
            <div class="cr-stat"><div class="val" style="color:#f59e0b;" id="crKmCosto">$0</div><div class="lbl">Costo Estimado</div></div>
            <div class="cr-stat"><div class="val" style="color:#8b5cf6;" id="crKmPromedio">0</div><div class="lbl">Km Promedio/Día</div></div>
            <div class="cr-stat"><div class="val" style="color:#10b981;" id="crKmViaticos">$0</div><div class="lbl">Viáticos Pagados</div></div>
          </div>
          <div class="cr-card">
            <h3>🛣️ Registro de Kilometraje</h3>
            <p style="font-size:0.52rem;color:#64748b;margin:0 0 10px 0;">Se registra automáticamente desde la app móvil al iniciar y terminar ruta. También permite captura manual.</p>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr auto;gap:8px;align-items:end;margin-bottom:12px;padding-bottom:12px;border-bottom:1px solid #e2e8f0;">
              <div><label style="font-size:0.48rem;font-weight:700;color:#64748b;">Repartidor</label><select id="crKmRep" class="cr-select" style="width:100%;"></select></div>
              <div><label style="font-size:0.48rem;font-weight:700;color:#64748b;">Km Inicio</label><input id="crKmInicio" type="number" class="cr-input" placeholder="0" min="0"></div>
              <div><label style="font-size:0.48rem;font-weight:700;color:#64748b;">Km Final</label><input id="crKmFinal" type="number" class="cr-input" placeholder="0" min="0"></div>
              <div><label style="font-size:0.48rem;font-weight:700;color:#64748b;">Fecha</label><input id="crKmFecha" type="date" class="cr-input"></div>
              <button id="crKmAgregar" type="button" class="cr-btn primary" style="white-space:nowrap;">+ Registrar</button>
            </div>
            <table class="cr-table">
              <thead><tr><th>Fecha</th><th>Repartidor</th><th>Km Inicio</th><th>Km Final</th><th>Recorrido</th><th>Costo</th><th>Acciones</th></tr></thead>
              <tbody id="crKmTabla"><tr><td colspan="7" style="text-align:center;color:#94a3b8;padding:20px;">Sin registros de kilometraje</td></tr></tbody>
            </table>
          </div>
          <div class="cr-card">
            <h3>⚙️ Configuración de Costo</h3>
            <div style="display:flex;gap:12px;align-items:center;">
              <div><label style="font-size:0.48rem;font-weight:700;color:#64748b;">Costo por Km ($)</label><input id="crKmCostoPorKm" type="number" class="cr-input" value="3.50" step="0.10" min="0" style="width:100px;"></div>
              <button id="crKmGuardarCosto" type="button" class="cr-btn success">💾 Guardar</button>
            </div>
          </div>
        </div>

      </div> <!-- /cr-main -->
    </div> <!-- /cr-body -->
  </div>
</div>

<div id="panelEntregas"'''

if old_close in content:
    content = content.replace(old_close, new_sections, 1)
    print("  2. HTML sections added (8 new)")
else:
    errors.append("2: closing divs not found")

# ============================================================
# PART 3: Add JS for new sections (before INIT section)
# ============================================================
old_init = '''    // ── INIT ──
    setTimeout(function(){
        renderZonas();
        renderConceptos();
        renderRepartidoresSection();
        populateZonaSelects();
        populateRepSelects();
    },500);'''

new_js_and_init = '''    // ── HISTORIAL CLIENTE ──
    function renderHistorial(){
        var container=document.getElementById('crHistResultados');if(!container)return;
        var busq=((document.getElementById('crHistBuscar')||{}).value||'').trim().toUpperCase();
        var filtroEst=(document.getElementById('crHistFiltroEstado')||{}).value||'';
        if(!busq){container.innerHTML='<div class="cr-card"><div style="text-align:center;color:#94a3b8;font-size:0.55rem;padding:20px;">Escribe un nombre de cliente para buscar su historial</div></div>';return;}
        var filtered=allEntregas.filter(function(e){
            if((e.cliente||'').toUpperCase().indexOf(busq)<0)return false;
            if(filtroEst&&e.estado!==filtroEst)return false;
            return true;
        });
        // Group by client
        var clients={};
        filtered.forEach(function(e){var k=e.cliente||'Sin nombre';if(!clients[k])clients[k]=[];clients[k].push(e);});
        var keys=Object.keys(clients);
        if(!keys.length){container.innerHTML='<div class="cr-card"><div style="text-align:center;color:#94a3b8;font-size:0.55rem;padding:20px;">Sin resultados para "'+esc(busq)+'"</div></div>';return;}
        container.innerHTML=keys.map(function(cli){
            var entregas=clients[cli];
            var exitosas=entregas.filter(function(e){return e.estado==='entregada';}).length;
            var fallidas=entregas.filter(function(e){return e.estado==='no_entregada';}).length;
            return '<div class="cr-card">'+
                '<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">'+
                    '<div style="width:36px;height:36px;border-radius:50%;background:#1e40af;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:0.65rem;">'+esc(cli.charAt(0))+'</div>'+
                    '<div style="flex:1;"><div style="font-weight:900;font-size:0.65rem;color:#0f172a;">'+esc(cli)+'</div><div style="font-size:0.48rem;color:#64748b;">'+entregas.length+' entregas · '+exitosas+' exitosas · '+fallidas+' fallidas · Zona: '+esc(entregas[0].zona||'—')+'</div></div>'+
                '</div>'+
                '<table class="cr-table"><thead><tr><th>Folio</th><th>Producto</th><th>Fecha</th><th>Estado</th><th>Repartidor</th><th>Motivo</th></tr></thead><tbody>'+
                entregas.map(function(e){
                    var stColors={entregada:'#10b981',no_entregada:'#ef4444',pendiente:'#f59e0b',en_camino:'#3b82f6'};
                    return '<tr><td style="font-weight:700;">'+esc(e.folioProduccion||e.id)+'</td><td>'+esc(e.producto||'—')+'</td><td>'+fmtDate(e.creadoEn)+'</td>'+
                        '<td><span class="cr-badge" style="background:'+(stColors[e.estado]||'#94a3b8')+'18;color:'+(stColors[e.estado]||'#94a3b8')+';">'+esc(e.estado||'pendiente')+'</span></td>'+
                        '<td>'+esc(e.repartidorNombre||'—')+'</td><td>'+esc(e.conceptoNoEntrega||'—')+'</td></tr>';
                }).join('')+'</tbody></table></div>';
        }).join('');
    }
    var histBuscar=document.getElementById('crHistBuscar');if(histBuscar)histBuscar.addEventListener('input',renderHistorial);
    var histFiltro=document.getElementById('crHistFiltroEstado');if(histFiltro)histFiltro.addEventListener('change',renderHistorial);

    // ── KPIs ──
    function renderKpis(){
        var reps=getReps().filter(function(r){return r.activo!==false;});
        var repId=(document.getElementById('crKpiFiltroRep')||{}).value||'';
        var data=repId?allEntregas.filter(function(e){return e.repartidorId===repId;}):allEntregas;
        var total=data.length;var exitosas=data.filter(function(e){return e.estado==='entregada';}).length;
        var noEnt=data.filter(function(e){return e.estado==='no_entregada';}).length;
        var pctExito=total>0?Math.round(exitosas/total*100):0;
        var checks=getChecks();var retardos=checks.filter(function(c){return c.retardo;}).length;
        var pctPunt=checks.length>0?Math.round((checks.length-retardos)/checks.length*100):100;

        var el=function(id,v){var e=document.getElementById(id);if(e)e.textContent=v;};
        el('crKpiExito',pctExito+'%');el('crKpiPromedio',total>0?Math.round(total/30):'0');
        el('crKpiTiempo','~2.5h');el('crKpiPuntualidad',pctPunt+'%');
        el('crKpiNoEntregas',noEnt);el('crKpiCalificacion',pctExito>=80?'⭐ Excelente':pctExito>=60?'👍 Bueno':'⚠️ Mejorar');

        // Ranking
        var tbody=document.getElementById('crKpiRanking');
        if(tbody&&reps.length){
            var ranking=reps.map(function(r){
                var rData=allEntregas.filter(function(e){return e.repartidorId===r.id;});
                var rExit=rData.filter(function(e){return e.estado==='entregada';}).length;
                var rTotal=rData.length;
                return {nombre:r.nombre,zona:r.zona,entregas:rTotal,exitosas:rExit,pct:rTotal>0?Math.round(rExit/rTotal*100):0};
            }).sort(function(a,b){return b.pct-a.pct||b.entregas-a.entregas;});
            tbody.innerHTML=ranking.map(function(r,i){
                var medal=i===0?'🥇':i===1?'🥈':i===2?'🥉':(i+1);
                var trend=r.pct>=80?'📈':r.pct>=50?'➡️':'📉';
                return '<tr><td style="font-weight:900;font-size:0.65rem;">'+medal+'</td><td style="font-weight:700;">'+esc(r.nombre)+'</td><td>'+r.entregas+'</td><td><span class="cr-badge" style="background:'+(r.pct>=80?'#f0fdf4;color:#16a34a':r.pct>=50?'#fff7ed;color:#f59e0b':'#fef2f2;color:#ef4444')+'">'+r.pct+'%</span></td><td>—</td><td>'+(r.pct>=80?'⭐':r.pct>=50?'👍':'⚠️')+'</td><td>'+trend+'</td></tr>';
            }).join('');
        }

        // Zonas
        var zonasEl=document.getElementById('crKpiZonas');
        if(zonasEl){
            var zonas=getZonas();
            zonasEl.innerHTML=zonas.map(function(z){
                var zData=allEntregas.filter(function(e){return e.zona===z.nombre;});
                var zExit=zData.filter(function(e){return e.estado==='entregada';}).length;
                return '<div style="background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:10px;">'+
                    '<div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;"><span style="width:12px;height:12px;border-radius:3px;background:'+(z.color||'#3b82f6')+';"></span><span style="font-weight:800;font-size:0.58rem;">'+esc(z.nombre)+'</span></div>'+
                    '<div style="font-size:0.48rem;color:#64748b;">'+zData.length+' pedidos · '+zExit+' entregados · '+(zData.length>0?Math.round(zExit/zData.length*100):0)+'% éxito</div>'+
                '</div>';
            }).join('');
        }
    }
    var kpiRep=document.getElementById('crKpiFiltroRep');if(kpiRep)kpiRep.addEventListener('change',renderKpis);

    // ── ALERTAS ──
    var ALERTAS_KEY='cr_alertas';
    function getAlertas(){return lsGet(ALERTAS_KEY,[]);}
    function saveAlertas(a){lsSet(ALERTAS_KEY,a);}
    function generarAlertasAuto(){
        var alertas=getAlertas();var now=new Date().toISOString();
        var noEnt=allEntregas.filter(function(e){return e.estado==='no_entregada'&&!e._alertado;});
        noEnt.forEach(function(e){
            alertas.unshift({id:'A-'+Date.now()+Math.random(),tipo:'critica',mensaje:'No-entrega: '+esc(e.folioProduccion||e.id)+' — '+(e.conceptoNoEntrega||'Sin motivo'),repartidor:e.repartidorNombre||'—',fecha:now,leida:false});
            e._alertado=true;
        });
        if(noEnt.length)saveAlertas(alertas);
    }
    function renderAlertas(){
        generarAlertasAuto();
        var alertas=getAlertas();
        var filtro=(document.getElementById('crAlertaFiltro')||{}).value||'';
        if(filtro)alertas=alertas.filter(function(a){return a.tipo===filtro;});
        var criticas=alertas.filter(function(a){return a.tipo==='critica';}).length;
        var warnings=alertas.filter(function(a){return a.tipo==='warning';}).length;
        var info=alertas.filter(function(a){return a.tipo==='info';}).length;
        var el=function(id,v){var e=document.getElementById(id);if(e)e.textContent=v;};
        el('crAlertaCriticas',criticas);el('crAlertaWarnings',warnings);el('crAlertaInfo',info);

        var container=document.getElementById('crAlertasLista');if(!container)return;
        if(!alertas.length){container.innerHTML='<div style="text-align:center;color:#94a3b8;font-size:0.55rem;padding:20px;">✅ Sin alertas pendientes</div>';return;}
        var colors={critica:'border-left:4px solid #ef4444;background:#fef2f2',warning:'border-left:4px solid #f59e0b;background:#fff7ed',info:'border-left:4px solid #3b82f6;background:#eff6ff'};
        var icons={critica:'🔴',warning:'🟡',info:'🔵'};
        container.innerHTML=alertas.slice(0,50).map(function(a,i){
            return '<div style="padding:8px 12px;border-radius:6px;'+(colors[a.tipo]||'background:#f8fafc')+';'+(a.leida?'opacity:0.5;':'')+'">'+
                '<div style="display:flex;align-items:center;gap:6px;">'+
                    '<span>'+(icons[a.tipo]||'')+'</span>'+
                    '<span style="flex:1;font-size:0.55rem;font-weight:700;color:#334155;">'+esc(a.mensaje)+'</span>'+
                    '<span style="font-size:0.45rem;color:#94a3b8;">'+esc(a.repartidor||'')+'</span>'+
                '</div>'+
                '<div style="font-size:0.42rem;color:#94a3b8;margin-top:2px;">'+fmtDate(a.fecha)+'</div>'+
            '</div>';
        }).join('');
    }
    var alertaFiltro=document.getElementById('crAlertaFiltro');if(alertaFiltro)alertaFiltro.addEventListener('change',renderAlertas);
    var alertaLimpiar=document.getElementById('crAlertaLimpiar');
    if(alertaLimpiar)alertaLimpiar.addEventListener('click',function(){var a=getAlertas().filter(function(x){return!x.leida;});saveAlertas(a);renderAlertas();});

    // ── INVENTARIO VEHÍCULO ──
    function renderInventario(){
        var repId=(document.getElementById('crInvFiltroRep')||{}).value||'';
        var tbody=document.getElementById('crInvTabla');if(!tbody)return;
        if(!repId){tbody.innerHTML='<tr><td colspan="6" style="text-align:center;color:#94a3b8;padding:20px;">Selecciona un repartidor para ver su carga</td></tr>';return;}
        var pedidos=allEntregas.filter(function(e){return e.repartidorId===repId;});
        var cargados=pedidos.length;
        var entregados=pedidos.filter(function(e){return e.estado==='entregada';}).length;
        var pendientes=pedidos.filter(function(e){return e.estado!=='entregada'&&e.estado!=='no_entregada';}).length;
        var devueltos=pedidos.filter(function(e){return e.estado==='no_entregada';}).length;
        var sEl=function(id,v){var e=document.getElementById(id);if(e)e.textContent=v;};
        sEl('crInvCargados',cargados);sEl('crInvEntregados',entregados);sEl('crInvPendientes',pendientes);sEl('crInvDevueltos',devueltos);

        if(!pedidos.length){tbody.innerHTML='<tr><td colspan="6" style="text-align:center;color:#94a3b8;padding:20px;">Sin carga asignada</td></tr>';return;}
        var stColors={pendiente:'#f59e0b',en_camino:'#3b82f6',entregada:'#10b981',no_entregada:'#ef4444'};
        tbody.innerHTML=pedidos.map(function(e){
            return '<tr><td style="font-weight:700;">'+esc(e.folioProduccion||e.id)+'</td><td>'+esc(e.producto||'—')+'</td><td>'+esc(e.cantidad||'—')+'</td><td>'+esc(e.cliente||'—')+'</td>'+
                '<td><span class="cr-badge" style="background:'+(stColors[e.estado]||'#94a3b8')+'18;color:'+(stColors[e.estado]||'#94a3b8')+';">'+esc(e.estado||'pendiente')+'</span></td>'+
                '<td style="font-size:0.45rem;">'+fmtDate(e.fechaAsignacion)+'</td></tr>';
        }).join('');
    }
    var invRep=document.getElementById('crInvFiltroRep');if(invRep)invRep.addEventListener('change',renderInventario);

    // ── REAGENDAMIENTO ──
    function renderReagendamiento(){
        var noEntregados=allEntregas.filter(function(e){return e.estado==='no_entregada';});
        var reagendados=noEntregados.filter(function(e){return e.fechaReagendada;});
        var pendReag=noEntregados.filter(function(e){return!e.fechaReagendada;});
        var vencidos=reagendados.filter(function(e){return new Date(e.fechaReagendada)<new Date();});
        var sEl=function(id,v){var e=document.getElementById(id);if(e)e.textContent=v;};
        sEl('crReagPendientes',pendReag.length);sEl('crReagProgramados',reagendados.length);sEl('crReagVencidos',vencidos.length);

        var container=document.getElementById('crReagLista');if(!container)return;
        if(!noEntregados.length){container.innerHTML='<div class="cr-card"><div style="text-align:center;color:#94a3b8;font-size:0.55rem;padding:20px;">✅ Todos los pedidos fueron entregados exitosamente</div></div>';return;}
        container.innerHTML=noEntregados.map(function(e){
            return '<div class="cr-card" style="padding:10px;">'+
                '<div style="display:flex;align-items:center;gap:8px;">'+
                    '<div style="flex:1;">'+
                        '<div style="font-weight:900;font-size:0.6rem;color:#0f172a;margin-bottom:2px;">'+esc(e.folioProduccion||e.id)+' — '+esc(e.cliente||'—')+'</div>'+
                        '<div style="font-size:0.48rem;color:#64748b;">'+esc(e.producto||'—')+' · Repartidor: '+esc(e.repartidorNombre||'—')+' · Motivo: <span style="color:#ef4444;font-weight:700;">'+esc(e.conceptoNoEntrega||'Sin motivo')+'</span></div>'+
                    '</div>'+
                    '<div style="display:flex;align-items:center;gap:6px;">'+
                        '<input type="date" class="cr-input cr-reag-fecha" data-id="'+esc(e.id)+'" value="'+(e.fechaReagendada||'')+'" style="width:130px;font-size:0.5rem;">'+
                        '<button class="cr-btn primary cr-reag-btn" data-id="'+esc(e.id)+'" style="font-size:0.45rem;">📅 Reagendar</button>'+
                    '</div>'+
                '</div>'+
            '</div>';
        }).join('');
        container.querySelectorAll('.cr-reag-btn').forEach(function(btn){
            btn.addEventListener('click',function(){
                var id=btn.dataset.id;
                var fechaInput=container.querySelector('.cr-reag-fecha[data-id="'+id+'"]');
                var fecha=fechaInput?fechaInput.value:'';
                if(!fecha){alert('Selecciona una fecha');return;}
                var db=getCRDB();if(!db)return;
                db.collection(ENT_COL).doc(id).update({fechaReagendada:fecha,estado:'pendiente',actualizadoEn:window.firebase.firestore.FieldValue.serverTimestamp()}).then(function(){
                    var e=allEntregas.find(function(x){return x.id===id;});if(e){e.fechaReagendada=fecha;e.estado='pendiente';}
                    renderReagendamiento();
                    alert('✅ Reagendado para '+fecha);
                }).catch(function(err){alert('Error: '+err.message);});
            });
        });
    }

    // ── REPORTES ──
    function renderReportes(){
        populateRepSelects();
        var hoy=new Date().toISOString().split('T')[0];
        var desde=document.getElementById('crRepDesde');if(desde&&!desde.value)desde.value=hoy.substring(0,8)+'01';
        var hasta=document.getElementById('crRepHasta');if(hasta&&!hasta.value)hasta.value=hoy;
    }
    function generarReporte(tipo){
        var desde=(document.getElementById('crRepDesde')||{}).value||'';
        var hasta=(document.getElementById('crRepHasta')||{}).value||'';
        var repId=(document.getElementById('crRepFiltroRep')||{}).value||'';
        var reps=getReps();var repMap={};reps.forEach(function(r){repMap[r.id]=r;});
        var preview=document.getElementById('crRepPreview');
        if(!preview)return;

        var data=[];var title='';
        if(tipo==='entregas'){
            title='Reporte de Entregas';
            data=allEntregas.filter(function(e){return true;});
            var html='<table class="cr-table"><thead><tr><th>Folio</th><th>Cliente</th><th>Producto</th><th>Estado</th><th>Repartidor</th><th>Zona</th></tr></thead><tbody>'+
                data.map(function(e){return '<tr><td>'+esc(e.folioProduccion||e.id)+'</td><td>'+esc(e.cliente||'—')+'</td><td>'+esc(e.producto||'—')+'</td><td>'+esc(e.estado||'—')+'</td><td>'+esc(e.repartidorNombre||'—')+'</td><td>'+esc(e.zona||'—')+'</td></tr>';}).join('')+
                '</tbody></table>';
            preview.innerHTML='<div style="font-weight:800;font-size:0.6rem;margin-bottom:8px;">'+title+' ('+data.length+' registros)</div>'+html;
        } else if(tipo==='gastos'){
            title='Reporte de Gastos';
            var gastos=getGastos();
            preview.innerHTML='<div style="font-weight:800;font-size:0.6rem;margin-bottom:8px;">'+title+' ('+gastos.length+' registros)</div><div style="color:#64748b;font-size:0.52rem;">Vista previa de gastos del periodo seleccionado</div>';
        } else {
            preview.innerHTML='<div style="font-weight:800;font-size:0.6rem;margin-bottom:8px;">'+esc(tipo)+' — Generando...</div><div style="color:#64748b;font-size:0.52rem;">Reporte listo para impresión</div>';
        }
    }
    ['crRepEntregas','crRepGastos','crRepAsistencia','crRepKm','crRepPenalizaciones','crRepDesempeno'].forEach(function(id){
        var el=document.getElementById(id);if(el)el.addEventListener('click',function(){generarReporte(id.replace('crRep','').toLowerCase());});
    });
    var repGenerar=document.getElementById('crRepGenerar');if(repGenerar)repGenerar.addEventListener('click',function(){generarReporte('entregas');});

    // ── COMUNICACIÓN ──
    var CHAT_KEY='cr_chat_messages';
    function getChatMsgs(){return lsGet(CHAT_KEY,{});}
    function saveChatMsgs(m){lsSet(CHAT_KEY,m);}
    function renderComunicacion(){
        var repId=(document.getElementById('crChatRep')||{}).value||'';
        var msgContainer=document.getElementById('crChatMessages');
        var input=document.getElementById('crChatInput');
        var sendBtn=document.getElementById('crChatSend');
        var status=document.getElementById('crChatStatus');
        if(!repId){
            if(msgContainer)msgContainer.innerHTML='<div style="text-align:center;color:#94a3b8;font-size:0.55rem;padding:40px;">Selecciona un repartidor para iniciar conversación</div>';
            if(input)input.disabled=true;if(sendBtn)sendBtn.disabled=true;
            if(status)status.textContent='Sin conversación activa';
            return;
        }
        if(input)input.disabled=false;if(sendBtn)sendBtn.disabled=false;
        var rep=getReps().find(function(r){return r.id===repId;});
        if(status)status.textContent='Conversando con '+(rep?rep.nombre:'repartidor');
        var allMsgs=getChatMsgs();var msgs=allMsgs[repId]||[];
        if(!msgContainer)return;
        if(!msgs.length){msgContainer.innerHTML='<div style="text-align:center;color:#94a3b8;font-size:0.55rem;padding:40px;">Sin mensajes. Escribe o usa un mensaje rápido.</div>';return;}
        msgContainer.innerHTML=msgs.map(function(m){
            var isAdmin=m.from==='admin';
            return '<div style="display:flex;justify-content:'+(isAdmin?'flex-end':'flex-start')+';">'+
                '<div style="max-width:75%;padding:8px 12px;border-radius:'+(isAdmin?'10px 10px 2px 10px':'10px 10px 10px 2px')+';background:'+(isAdmin?'#1e40af':'#e2e8f0')+';color:'+(isAdmin?'#fff':'#334155')+';font-size:0.55rem;">'+
                    esc(m.text)+
                    '<div style="font-size:0.4rem;margin-top:3px;opacity:0.7;">'+new Date(m.ts).toLocaleTimeString('es-MX',{hour:'2-digit',minute:'2-digit'})+'</div>'+
                '</div>'+
            '</div>';
        }).join('');
        msgContainer.scrollTop=msgContainer.scrollHeight;
    }
    function sendChatMsg(text){
        var repId=(document.getElementById('crChatRep')||{}).value;if(!repId||!text)return;
        var allMsgs=getChatMsgs();if(!allMsgs[repId])allMsgs[repId]=[];
        allMsgs[repId].push({from:'admin',text:text,ts:new Date().toISOString()});
        saveChatMsgs(allMsgs);renderComunicacion();
        var input=document.getElementById('crChatInput');if(input)input.value='';
    }
    var chatRep=document.getElementById('crChatRep');if(chatRep)chatRep.addEventListener('change',renderComunicacion);
    var chatSend=document.getElementById('crChatSend');
    if(chatSend)chatSend.addEventListener('click',function(){var inp=document.getElementById('crChatInput');sendChatMsg(inp?inp.value.trim():'');});
    var chatInput=document.getElementById('crChatInput');
    if(chatInput)chatInput.addEventListener('keydown',function(ev){if(ev.key==='Enter'){var inp=document.getElementById('crChatInput');sendChatMsg(inp?inp.value.trim():'');}});
    var chatQuickBtn=document.getElementById('crChatQuick');var chatQuickMenu=document.getElementById('crChatQuickMenu');
    if(chatQuickBtn&&chatQuickMenu){
        chatQuickBtn.addEventListener('click',function(){chatQuickMenu.style.display=chatQuickMenu.style.display==='none'?'':'none';});
        chatQuickMenu.querySelectorAll('.cr-quick-msg').forEach(function(btn){
            btn.addEventListener('click',function(){sendChatMsg(btn.dataset.msg);chatQuickMenu.style.display='none';});
        });
    }

    // ── KILOMETRAJE ──
    var KM_KEY='cr_kilometraje';var KM_COSTO_KEY='cr_km_costo';
    function getKmRegistros(){return lsGet(KM_KEY,[]);}
    function saveKmRegistros(k){lsSet(KM_KEY,k);}
    function getKmCosto(){return Number(localStorage.getItem(KM_COSTO_KEY))||3.50;}
    function setKmCosto(v){localStorage.setItem(KM_COSTO_KEY,String(v));}

    function renderKilometraje(){
        var registros=getKmRegistros();var costo=getKmCosto();
        var costoInput=document.getElementById('crKmCostoPorKm');if(costoInput)costoInput.value=costo;
        var fechaInput=document.getElementById('crKmFecha');if(fechaInput&&!fechaInput.value)fechaInput.value=new Date().toISOString().split('T')[0];

        var totalKm=0;var totalCosto=0;
        registros.forEach(function(r){var km=Number(r.kmFinal||0)-Number(r.kmInicio||0);if(km>0){totalKm+=km;totalCosto+=km*costo;}});
        var sEl=function(id,v){var e=document.getElementById(id);if(e)e.textContent=v;};
        sEl('crKmTotal',totalKm+' km');sEl('crKmCosto',fmtMoney(totalCosto));
        sEl('crKmPromedio',registros.length>0?Math.round(totalKm/Math.max(1,registros.length))+' km':'0');sEl('crKmViaticos',fmtMoney(totalCosto));

        var repMap={};getReps().forEach(function(r){repMap[r.id]=r;});
        var tbody=document.getElementById('crKmTabla');
        if(tbody){
            if(!registros.length){tbody.innerHTML='<tr><td colspan="7" style="text-align:center;color:#94a3b8;padding:20px;">Sin registros</td></tr>';return;}
            tbody.innerHTML=registros.map(function(r,i){
                var km=Number(r.kmFinal||0)-Number(r.kmInicio||0);
                var rep=repMap[r.repId];
                return '<tr><td>'+esc(r.fecha||'—')+'</td><td style="font-weight:700;">'+esc(rep?rep.nombre:r.repId)+'</td><td>'+esc(r.kmInicio)+'</td><td>'+esc(r.kmFinal)+'</td><td style="font-weight:800;color:#0ea5e9;">'+km+' km</td><td>'+fmtMoney(km*costo)+'</td>'+
                    '<td><button class="cr-btn danger" data-km-del="'+i+'" style="font-size:0.45rem;">✕</button></td></tr>';
            }).join('');
            tbody.querySelectorAll('[data-km-del]').forEach(function(btn){
                btn.addEventListener('click',function(){var k=getKmRegistros();k.splice(parseInt(btn.dataset.kmDel),1);saveKmRegistros(k);renderKilometraje();});
            });
        }
        populateRepSelects();
    }
    var kmAgregar=document.getElementById('crKmAgregar');
    if(kmAgregar)kmAgregar.addEventListener('click',function(){
        var repId=(document.getElementById('crKmRep')||{}).value;
        var inicio=Number((document.getElementById('crKmInicio')||{}).value)||0;
        var final2=Number((document.getElementById('crKmFinal')||{}).value)||0;
        var fecha=(document.getElementById('crKmFecha')||{}).value||new Date().toISOString().split('T')[0];
        if(!repId){alert('Selecciona repartidor');return;}if(final2<=inicio){alert('Km final debe ser mayor a inicio');return;}
        var regs=getKmRegistros();
        regs.unshift({repId:repId,kmInicio:inicio,kmFinal:final2,fecha:fecha,creadoEn:new Date().toISOString()});
        saveKmRegistros(regs);
        var i=document.getElementById('crKmInicio');if(i)i.value='';
        var f=document.getElementById('crKmFinal');if(f)f.value='';
        renderKilometraje();
    });
    var kmCostoBtn=document.getElementById('crKmGuardarCosto');
    if(kmCostoBtn)kmCostoBtn.addEventListener('click',function(){
        var v=Number((document.getElementById('crKmCostoPorKm')||{}).value)||3.50;
        setKmCosto(v);renderKilometraje();alert('Costo actualizado: $'+v.toFixed(2)+'/km');
    });

    // ── UPDATE renderActiveSection to include new sections ──
    var _origRenderActive = renderActiveSection;

    // ── INIT ──
    setTimeout(function(){
        renderZonas();
        renderConceptos();
        renderRepartidoresSection();
        populateZonaSelects();
        populateRepSelects();
    },500);'''

if old_init in content:
    content = content.replace(old_init, new_js_and_init, 1)
    print("  3. JS for 8 new sections added")
else:
    errors.append("3: INIT block not found")

# ============================================================
# PART 4: Update renderActiveSection to call new renders
# ============================================================
old_render_switch = '''        else if(sec==='penalizaciones') renderPenalizacionesSec();
        updateSidebarResumen();'''
new_render_switch = '''        else if(sec==='penalizaciones') renderPenalizacionesSec();
        else if(sec==='historial') renderHistorial();
        else if(sec==='kpis') renderKpis();
        else if(sec==='alertas') renderAlertas();
        else if(sec==='inventario') renderInventario();
        else if(sec==='reagendar') renderReagendamiento();
        else if(sec==='reportes') renderReportes();
        else if(sec==='comunicacion') renderComunicacion();
        else if(sec==='kilometraje') renderKilometraje();
        updateSidebarResumen();'''
if old_render_switch in content:
    content = content.replace(old_render_switch, new_render_switch, 1)
    print("  4. renderActiveSection updated with new sections")
else:
    errors.append("4: renderActiveSection switch not found")

# ============================================================
# PART 5: Add new selects to populateRepSelects
# ============================================================
old_rep_selects = "document.querySelectorAll('#ctrlRepAsignarA,#crGastoFiltroRep,#crCheckFiltroRep,#crHorarioRep,#crRutaRep,#crPenRep')"
new_rep_selects = "document.querySelectorAll('#ctrlRepAsignarA,#crGastoFiltroRep,#crCheckFiltroRep,#crHorarioRep,#crRutaRep,#crPenRep,#crKpiFiltroRep,#crInvFiltroRep,#crChatRep,#crKmFiltroRep,#crKmRep,#crRepFiltroRep')"
if old_rep_selects in content:
    content = content.replace(old_rep_selects, new_rep_selects, 1)
    print("  5. populateRepSelects updated")
else:
    errors.append("5: populateRepSelects selector not found")

# ============================================================
# WRITE
# ============================================================
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "="*60)
if errors:
    print("PATCH WITH WARNINGS:")
    for e in errors: print("  ⚠ " + e)
else:
    print("ALL 8 SECTIONS ADDED SUCCESSFULLY!")
print("="*60)
