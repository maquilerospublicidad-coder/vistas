#!/usr/bin/env python3
"""
Patch: Remove "Almacén Pedidos" from main menu, add "Recolección" to
Control de Reparto (admin) and App Móvil (repartidor).
"""
FILE = '/workspaces/vistas/mockup.html'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()
errors = []
count = 0

# ====================================================================
# 1. Remove ALMACEN PEDIDOS button from main menu
# ====================================================================
OLD_MENU_BTN = """            <button class="inicio-card" type="button" onclick="abrirModuloPrincipal('ALMACEN PEDIDOS')"><span class="ico">📦</span><span>ALMACÉN PEDIDOS</span></button>\n"""
if OLD_MENU_BTN in content:
    content = content.replace(OLD_MENU_BTN, '', 1)
    count += 1; print(f"  {count}. Removed ALMACÉN PEDIDOS from main menu")
else:
    errors.append("1: ALMACEN PEDIDOS button not found in menu")

# ====================================================================
# 2. Add "Recolección" sub-tab in Pedidos group (Control de Reparto)
# ====================================================================
OLD_PEDIDOS_GROUP = "pedidos:       { sections:['pedidos','reagendar','inventario'],         tabs:['📦 Listado','📅 Reagendar','📋 Inv. Vehículo'] }"
NEW_PEDIDOS_GROUP = "pedidos:       { sections:['pedidos','recoleccion','reagendar','inventario'],  tabs:['📦 Listado','🏭 Recolección','📅 Reagendar','📋 Inv. Vehículo'] }"
if OLD_PEDIDOS_GROUP in content:
    content = content.replace(OLD_PEDIDOS_GROUP, NEW_PEDIDOS_GROUP, 1)
    count += 1; print(f"  {count}. Added 'recoleccion' to Pedidos group")
else:
    errors.append("2: Pedidos group definition not found")

# ====================================================================
# 3. Add renderRecoleccion to SEC_RENDERS
# ====================================================================
OLD_SEC_RENDERS = "pedidos:renderPedidos, reagendar:renderReagendamiento, inventario:renderInventario,"
NEW_SEC_RENDERS = "pedidos:renderPedidos, recoleccion:renderRecoleccion, reagendar:renderReagendamiento, inventario:renderInventario,"
if OLD_SEC_RENDERS in content:
    content = content.replace(OLD_SEC_RENDERS, NEW_SEC_RENDERS, 1)
    count += 1; print(f"  {count}. Added renderRecoleccion to SEC_RENDERS")
else:
    errors.append("3: SEC_RENDERS pedidos line not found")

# ====================================================================
# 4. Add Recolección section HTML (in Control de Reparto, after Pedidos section)
# ====================================================================
# Find the Reagendar section and insert before it
REAGENDAR_MARKER = '        <!-- ── SECTION: REAGENDAMIENTO ── -->'
RECOLECCION_HTML = """        <!-- ── SECTION: RECOLECCIÓN ── -->
        <div class="cr-section" id="crSecRecoleccion" data-cr-section="recoleccion">
          <div class="cr-stats">
            <div class="cr-stat"><div class="val" style="color:#f59e0b;" id="crRecTerminados">0</div><div class="lbl">🏭 Terminados</div></div>
            <div class="cr-stat"><div class="val" style="color:#3b82f6;" id="crRecAlmacenados">0</div><div class="lbl">📦 Almacenados</div></div>
            <div class="cr-stat"><div class="val" style="color:#8b5cf6;" id="crRecAsignados">0</div><div class="lbl">🚚 Asig. Recolección</div></div>
            <div class="cr-stat"><div class="val" style="color:#10b981;" id="crRecEntregados">0</div><div class="lbl">✅ En Sucursal</div></div>
          </div>
          <div class="cr-card">
            <h3>🏭 Recolección de Pedidos Terminados</h3>
            <p style="font-size:0.52rem;color:#64748b;margin:0 0 12px 0;">Asigna pedidos terminados en taller a un repartidor para que los recoja, escanee y lleve a sucursal.</p>
            <div class="cr-header-bar">
              <select id="crRecFiltroEstado" class="cr-select">
                <option value="">Todos los estados</option>
                <option value="terminada">🏭 Terminados (sin recoger)</option>
                <option value="almacenado">📦 Almacenados</option>
                <option value="asignado_recoleccion">🚚 Asignados a repartidor</option>
                <option value="recogido">📷 Recogidos por repartidor</option>
                <option value="en_transito_sucursal">🏬 En tránsito a sucursal</option>
                <option value="en_sucursal">✅ Entregado en sucursal</option>
              </select>
              <input id="crRecBuscar" type="text" class="cr-input" placeholder="🔍 Buscar folio o cliente..." style="max-width:250px;">
              <button id="crRecRecargar" type="button" class="cr-btn" style="background:#f3f4f6;color:#64748b;border:1px solid #d1d5db;">🔄 Recargar</button>
            </div>
          </div>
          <!-- Asignación masiva -->
          <div id="crRecAsignacionBar" class="cr-card" style="background:#eff6ff;border-color:#bfdbfe;">
            <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
              <span style="font-size:0.55rem;font-weight:800;color:#1e40af;">Asignar recolección:</span>
              <select id="crRecAsignarRep" class="cr-select" style="flex:1;min-width:150px;"><option value="">— Seleccionar repartidor —</option></select>
              <button id="crRecBtnAsignar" type="button" class="cr-btn primary">🚚 ASIGNAR RECOLECCIÓN</button>
              <button id="crRecBtnSelAll" type="button" class="cr-btn" style="background:#f3f4f6;color:#374151;border:1px solid #d1d5db;">☑ Todos</button>
              <span id="crRecSelCount" style="font-size:0.52rem;color:#6b7280;font-weight:700;">0 sel.</span>
            </div>
          </div>
          <div id="crRecPedidosList" style="display:flex;flex-direction:column;gap:8px;">
            <div style="text-align:center;color:#9ca3af;padding:30px;font-size:0.55rem;">Cargando pedidos terminados del taller...</div>
          </div>
        </div>

"""
if REAGENDAR_MARKER in content:
    content = content.replace(REAGENDAR_MARKER, RECOLECCION_HTML + REAGENDAR_MARKER, 1)
    count += 1; print(f"  {count}. Recolección HTML section added to Control de Reparto")
else:
    errors.append("4: Reagendar marker not found")

# ====================================================================
# 5. Add "Recolección" tab to App Móvil (panelEntregas)
# ====================================================================
OLD_TABS = """        <div class="entrega-tabs" id="entTabs">
          <button class="entrega-tab active" data-status="pendiente">📬 Pendientes</button>
          <button class="entrega-tab" data-status="en_camino">🚚 En Camino</button>
          <button class="entrega-tab" data-status="entregada">✅ Entregadas</button>
          <button class="entrega-tab" data-status="no_entregada">❌ No Entregadas</button>
        </div>"""
NEW_TABS = """        <div class="entrega-tabs" id="entTabs">
          <button class="entrega-tab active" data-status="pendiente">📬 Pendientes</button>
          <button class="entrega-tab" data-status="recoleccion">🏭 Recolección</button>
          <button class="entrega-tab" data-status="en_camino">🚚 En Camino</button>
          <button class="entrega-tab" data-status="entregada">✅ Entregadas</button>
          <button class="entrega-tab" data-status="no_entregada">❌ No Entregadas</button>
        </div>"""
if OLD_TABS in content:
    content = content.replace(OLD_TABS, NEW_TABS, 1)
    count += 1; print(f"  {count}. 'Recolección' tab added to App Móvil")
else:
    errors.append("5: App Movil tabs not found")

# ====================================================================
# 6. Add Recolección JS to Control de Reparto (before INIT)
# ====================================================================
INIT_MARKER = '    // ── INIT ──'
RECOLECCION_JS = """    // ── RECOLECCIÓN (Admin: Control de Reparto) ──
    var RECOL_COLLECTION = 'stored_orders';
    var allRecoleccion = [];

    function cargarRecoleccion(){
        var db=getCRDB();if(!db)return;
        // Load from stored_orders + terminadas from production
        Promise.all([
            db.collection(RECOL_COLLECTION).orderBy('creadoEn','desc').get(),
            db.collection('production_orders').where('estado','==','terminada').get()
        ]).then(function(results){
            var stored=results[0].docs.map(function(d){return Object.assign({id:d.id,_source:'stored'},d.data());});
            var terminadas=results[1].docs.map(function(d){return Object.assign({id:d.id,_source:'production'},d.data());});
            // Merge: terminadas that aren't yet in stored_orders
            var storedFolios=stored.map(function(s){return s.folioProduccion||s.produccionDocId;});
            var pendientes=terminadas.filter(function(t){
                return !storedFolios.includes(t.folio)&&!storedFolios.includes(t.id);
            }).map(function(t){
                return {id:t.id,_source:'production',folioProduccion:t.folio||'',cliente:t.cliente||'',producto:t.producto||'',
                    cantidad:t.cantidad||'',color:t.color||'',fechaEntrega:t.fechaEntrega||'',disenoUrl:t.disenoUrl||'',
                    estado:'terminada',creadoEn:t.creadoEn};
            });
            allRecoleccion=pendientes.concat(stored);
            renderRecoleccion();
        }).catch(function(err){console.error('Error cargando recolección:',err);});
    }

    function renderRecoleccion(){
        var filtroEst=(document.getElementById('crRecFiltroEstado')||{}).value||'';
        var busq=((document.getElementById('crRecBuscar')||{}).value||'').toUpperCase().trim();
        // Stats
        var terminados=allRecoleccion.filter(function(o){return o.estado==='terminada';}).length;
        var almacenados=allRecoleccion.filter(function(o){return o.estado==='almacenado';}).length;
        var asignados=allRecoleccion.filter(function(o){return o.estado==='asignado_recoleccion';}).length;
        var enSucursal=allRecoleccion.filter(function(o){return o.estado==='en_sucursal'||o.estado==='recibido_sucursal';}).length;
        var sEl=function(id,v){var e=document.getElementById(id);if(e)e.textContent=v;};
        sEl('crRecTerminados',terminados);sEl('crRecAlmacenados',almacenados);
        sEl('crRecAsignados',asignados);sEl('crRecEntregados',enSucursal);

        var lista=allRecoleccion;
        if(filtroEst) lista=lista.filter(function(o){return o.estado===filtroEst;});
        if(busq) lista=lista.filter(function(o){
            return (o.folioProduccion||o.folio||'').toUpperCase().indexOf(busq)>=0||(o.cliente||'').toUpperCase().indexOf(busq)>=0;
        });

        var container=document.getElementById('crRecPedidosList');if(!container)return;
        if(!lista.length){container.innerHTML='<div class="cr-card"><div style="text-align:center;color:#94a3b8;font-size:0.55rem;padding:20px;">Sin pedidos en este estado</div></div>';return;}

        var stLabels={terminada:'🏭 Terminado',almacenado:'📦 Almacenado',asignado_recoleccion:'🚚 Asignado',recogido:'📷 Recogido',en_transito_sucursal:'🏬 En tránsito',en_sucursal:'✅ En sucursal',recibido_sucursal:'✅ En sucursal',enviado_reparto:'📦 Enviado reparto'};
        var stColors={terminada:'#f59e0b',almacenado:'#3b82f6',asignado_recoleccion:'#8b5cf6',recogido:'#0ea5e9',en_transito_sucursal:'#f97316',en_sucursal:'#10b981',recibido_sucursal:'#10b981',enviado_reparto:'#6366f1'};
        var reps=getReps().filter(function(r){return r.activo!==false;});

        container.innerHTML=lista.map(function(o){
            var folio=o.folioProduccion||o.folio||o.id;
            var canAssign=o.estado==='terminada'||o.estado==='almacenado';
            return '<div class="cr-card" style="padding:10px;">'+
                '<div style="display:flex;align-items:center;gap:10px;">'+
                    (canAssign?'<input type="checkbox" class="cr-rec-check" data-rec-id="'+esc(o.id)+'" data-rec-src="'+esc(o._source||'')+'" style="width:18px;height:18px;cursor:pointer;">':'')+
                    (o.disenoUrl?'<img src="'+esc(o.disenoUrl)+'" style="width:44px;height:44px;object-fit:cover;border-radius:8px;border:1px solid #e2e8f0;" onerror="this.style.display=\'none\'">':'')+
                    '<div style="flex:1;min-width:0;">'+
                        '<div style="display:flex;align-items:center;gap:6px;margin-bottom:2px;">'+
                            '<span style="font-weight:900;font-size:0.62rem;color:#0f172a;">'+esc(folio)+'</span>'+
                            '<span class="cr-badge" style="background:'+(stColors[o.estado]||'#94a3b8')+'18;color:'+(stColors[o.estado]||'#94a3b8')+';font-size:0.42rem;">'+esc(stLabels[o.estado]||o.estado)+'</span>'+
                        '</div>'+
                        '<div style="font-size:0.48rem;color:#64748b;">'+esc(o.cliente||'—')+' · '+esc(o.producto||'—')+(o.cantidad?' x'+esc(o.cantidad):'')+
                            (o.repartidorNombre?' · <span style="color:#8b5cf6;font-weight:700;">🚚 '+esc(o.repartidorNombre)+'</span>':'')+
                        '</div>'+
                    '</div>'+
                    (o.estado==='terminada'?'<button class="cr-btn primary cr-rec-almacenar" data-rec-id="'+esc(o.id)+'" style="font-size:0.42rem;">📦 Almacenar</button>':'')+
                    (o.estado==='almacenado'||o.estado==='asignado_recoleccion'?'<button class="cr-btn cr-rec-enviar-reparto" data-rec-id="'+esc(o.id)+'" style="font-size:0.42rem;background:#eff6ff;color:#1e40af;border:1px solid #bfdbfe;">📦 → Reparto</button>':'')+
                '</div>'+
            '</div>';
        }).join('');

        // Wire checkboxes
        var checks=container.querySelectorAll('.cr-rec-check');
        function updateSelCount(){
            var cnt=container.querySelectorAll('.cr-rec-check:checked').length;
            var el=document.getElementById('crRecSelCount');if(el)el.textContent=cnt+' sel.';
        }
        checks.forEach(function(chk){chk.addEventListener('change',updateSelCount);});
        // Select all
        var selAll=document.getElementById('crRecBtnSelAll');
        if(selAll){selAll.onclick=function(){var st=container.querySelectorAll('.cr-rec-check:not(:checked)').length>0;checks.forEach(function(c){c.checked=st;});updateSelCount();};}

        // Almacenar individual (terminada → almacenado)
        container.querySelectorAll('.cr-rec-almacenar').forEach(function(btn){
            btn.addEventListener('click',function(){
                var id=btn.dataset.recId;
                var orden=allRecoleccion.find(function(o){return o.id===id;});if(!orden)return;
                var db=getCRDB();if(!db)return;
                // Create in stored_orders
                db.collection(RECOL_COLLECTION).add({
                    folioProduccion:orden.folioProduccion||orden.folio||'',produccionDocId:orden.id,
                    cliente:orden.cliente||'',producto:orden.producto||'',cantidad:orden.cantidad||'',
                    color:orden.color||'',fechaEntrega:orden.fechaEntrega||'',disenoUrl:orden.disenoUrl||'',
                    estado:'almacenado',creadoEn:window.firebase.firestore.FieldValue.serverTimestamp(),
                    actualizadoEn:window.firebase.firestore.FieldValue.serverTimestamp()
                }).then(function(){
                    // Update production order
                    db.collection('production_orders').doc(id).update({estado:'almacenada',actualizadoEn:window.firebase.firestore.FieldValue.serverTimestamp()});
                    cargarRecoleccion();
                }).catch(function(err){alert('Error: '+err.message);});
            });
        });

        // Enviar a reparto individual
        container.querySelectorAll('.cr-rec-enviar-reparto').forEach(function(btn){
            btn.addEventListener('click',function(){
                var id=btn.dataset.recId;
                var orden=allRecoleccion.find(function(o){return o.id===id;});if(!orden)return;
                enviarAReparto(orden);
            });
        });
    }

    // Asignar recolección masiva
    var recAsignarBtn=document.getElementById('crRecBtnAsignar');
    if(recAsignarBtn)recAsignarBtn.addEventListener('click',function(){
        var repId=(document.getElementById('crRecAsignarRep')||{}).value;
        if(!repId){alert('Selecciona un repartidor');return;}
        var rep=getReps().find(function(r){return r.id===repId;});
        var checks=document.querySelectorAll('.cr-rec-check:checked');
        if(!checks.length){alert('Selecciona al menos un pedido');return;}
        var db=getCRDB();if(!db)return;
        var batch=db.batch();
        var ids=[];
        checks.forEach(function(chk){
            var docId=chk.dataset.recId;var src=chk.dataset.recSrc;
            ids.push({id:docId,src:src});
            if(src==='production'){
                // Need to first create stored_order, then assign — simpler: batch won't work for adds
                // We'll do sequential for production items
            } else {
                var ref=db.collection(RECOL_COLLECTION).doc(docId);
                batch.update(ref,{
                    estado:'asignado_recoleccion',
                    repartidorId:repId,repartidorNombre:rep?rep.nombre:'',
                    asignadoRecoleccionEn:window.firebase.firestore.FieldValue.serverTimestamp(),
                    actualizadoEn:window.firebase.firestore.FieldValue.serverTimestamp()
                });
            }
        });
        // For production items, create stored_orders first
        var prodItems=ids.filter(function(x){return x.src==='production';});
        var storedItems=ids.filter(function(x){return x.src!=='production';});

        var promises=prodItems.map(function(item){
            var orden=allRecoleccion.find(function(o){return o.id===item.id;});if(!orden)return Promise.resolve();
            return db.collection(RECOL_COLLECTION).add({
                folioProduccion:orden.folioProduccion||orden.folio||'',produccionDocId:orden.id,
                cliente:orden.cliente||'',producto:orden.producto||'',cantidad:orden.cantidad||'',
                color:orden.color||'',fechaEntrega:orden.fechaEntrega||'',disenoUrl:orden.disenoUrl||'',
                estado:'asignado_recoleccion',repartidorId:repId,repartidorNombre:rep?rep.nombre:'',
                asignadoRecoleccionEn:window.firebase.firestore.FieldValue.serverTimestamp(),
                creadoEn:window.firebase.firestore.FieldValue.serverTimestamp(),
                actualizadoEn:window.firebase.firestore.FieldValue.serverTimestamp()
            }).then(function(){
                return db.collection('production_orders').doc(item.id).update({estado:'almacenada',actualizadoEn:window.firebase.firestore.FieldValue.serverTimestamp()});
            });
        });

        Promise.all(promises).then(function(){
            return storedItems.length>0?batch.commit():Promise.resolve();
        }).then(function(){
            alert('✅ '+ids.length+' pedido(s) asignados a '+(rep?rep.nombre:'repartidor')+' para recolección');
            cargarRecoleccion();
        }).catch(function(err){alert('Error: '+err.message);});
    });

    function enviarAReparto(orden){
        var db=getCRDB();if(!db)return;
        db.collection('delivery_orders').add({
            folioProduccion:orden.folioProduccion||'',produccionDocId:orden.produccionDocId||orden.id||'',
            cliente:orden.cliente||'',producto:orden.producto||'',cantidad:orden.cantidad||'',
            fechaEntrega:orden.fechaEntrega||'',disenoUrl:orden.disenoUrl||'',
            estado:'pendiente',tipo:'entrega_cliente',
            notas:'Enviado desde recolección',
            creadoEn:window.firebase.firestore.FieldValue.serverTimestamp(),
            actualizadoEn:window.firebase.firestore.FieldValue.serverTimestamp()
        }).then(function(){
            return db.collection(RECOL_COLLECTION).doc(orden.id).update({
                estado:'enviado_reparto',actualizadoEn:window.firebase.firestore.FieldValue.serverTimestamp()
            });
        }).then(function(){
            alert('✅ Pedido enviado a reparto para entrega al cliente');
            cargarRecoleccion();
        }).catch(function(err){alert('Error: '+err.message);});
    }

    // Filtros
    var recFiltro=document.getElementById('crRecFiltroEstado');if(recFiltro)recFiltro.addEventListener('change',renderRecoleccion);
    var recBuscar=document.getElementById('crRecBuscar');if(recBuscar)recBuscar.addEventListener('input',renderRecoleccion);
    var recRecargar=document.getElementById('crRecRecargar');if(recRecargar)recRecargar.addEventListener('click',cargarRecoleccion);

    // Add crRecAsignarRep to populateRepSelects
    var _origPopReps2=populateRepSelects;
    populateRepSelects=function(){
        _origPopReps2();
        var reps=getReps().filter(function(r){return r.activo!==false;});
        var sel=document.getElementById('crRecAsignarRep');
        if(sel){
            var cur=sel.value;
            var opts='<option value="">— Seleccionar repartidor —</option>';
            reps.forEach(function(r){opts+='<option value="'+esc(r.id)+'">'+esc(r.nombre)+(r.zona?' ('+esc(r.zona)+')':'')+'</option>';});
            sel.innerHTML=opts;if(cur)sel.value=cur;
        }
    };

    """ + INIT_MARKER

if INIT_MARKER in content:
    content = content.replace(INIT_MARKER, RECOLECCION_JS, 1)
    count += 1; print(f"  {count}. Recolección JS added to Control de Reparto")
else:
    errors.append("6: INIT marker not found")

# ====================================================================
# 7. Update INIT to also call cargarRecoleccion
# ====================================================================
OLD_INIT_BODY = """    setTimeout(function(){
        renderZonas();
        renderConceptos();
        renderRepartidoresSection();
        populateZonaSelects();
        populateRepSelects();
    },500);"""
NEW_INIT_BODY = """    setTimeout(function(){
        renderZonas();
        renderConceptos();
        renderRepartidoresSection();
        populateZonaSelects();
        populateRepSelects();
        cargarRecoleccion();
    },500);"""
if OLD_INIT_BODY in content:
    content = content.replace(OLD_INIT_BODY, NEW_INIT_BODY, 1)
    count += 1; print(f"  {count}. cargarRecoleccion() added to INIT")
else:
    errors.append("7: INIT body not found")

# ====================================================================
# 8. Add Recolección view to App Móvil (panelEntregas) JS
# ====================================================================
# Find the allEntregas render function and add the recoleccion tab handling
# We'll add a script block right before the closing </script> of the entregas module
# First find the entregas script end
ENT_SCRIPT_MARKER = "window.openRepartoPopupGlobal = openRepartoPopup;"
RECOLECCION_APP_JS = """window.openRepartoPopupGlobal = openRepartoPopup;

    // ── RECOLECCIÓN TAB (Repartidor App Móvil) ──
    var recolTabActive = false;
    var allRecolApp = [];

    function cargarRecolApp(){
        var db = getEntDB(); if(!db) return;
        db.collection('stored_orders').where('estado','in',['asignado_recoleccion','recogido','en_transito_sucursal']).get().then(function(snap){
            allRecolApp = snap.docs.map(function(d){ return Object.assign({id:d.id}, d.data()); });
            if(recolTabActive) renderRecolApp();
        }).catch(function(err){ console.error('Error cargando recolección app:',err); });
    }

    function renderRecolApp(){
        var listEl = document.getElementById('entregaList');
        if(!listEl) return;
        if(!allRecolApp.length){
            listEl.innerHTML='<div style="text-align:center;padding:30px;color:#94a3b8;font-size:0.65rem;">'+
                '<div style="font-size:2rem;margin-bottom:8px;">🏭</div>'+
                '<div>Sin órdenes de recolección asignadas</div>'+
                '<div style="font-size:0.55rem;margin-top:4px;">El administrador asignará pedidos terminados para que los recojas del taller</div></div>';
            return;
        }
        var stLabels={asignado_recoleccion:'📋 Ir a recoger',recogido:'📦 Recogido — llevar a sucursal',en_transito_sucursal:'🏬 En camino a sucursal'};
        var stColors={asignado_recoleccion:'#f59e0b',recogido:'#3b82f6',en_transito_sucursal:'#8b5cf6'};
        listEl.innerHTML='<div style="padding:8px 0;font-weight:900;font-size:0.7rem;color:#1f2937;">🏭 Recolección del Taller</div>'+
            allRecolApp.map(function(o){
                var folio=o.folioProduccion||o.id;
                var estado=o.estado||'asignado_recoleccion';
                var actionBtn='';
                if(estado==='asignado_recoleccion'){
                    actionBtn='<button class="recol-action" data-recol-action="escanear" data-recol-id="'+esc(o.id)+'" style="padding:8px 14px;background:#ff9900;color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:800;font-size:0.65rem;width:100%;">📷 ESCANEAR Y RECOGER</button>';
                } else if(estado==='recogido'){
                    actionBtn='<button class="recol-action" data-recol-action="llevar" data-recol-id="'+esc(o.id)+'" style="padding:8px 14px;background:#1e40af;color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:800;font-size:0.65rem;width:100%;">🏬 SALIR A SUCURSAL</button>';
                } else if(estado==='en_transito_sucursal'){
                    actionBtn='<button class="recol-action" data-recol-action="entregar" data-recol-id="'+esc(o.id)+'" style="padding:8px 14px;background:#16a34a;color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:800;font-size:0.65rem;width:100%;">✅ CONFIRMAR ENTREGA EN SUCURSAL</button>';
                }
                return '<div style="background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:12px;margin-bottom:8px;">'+
                    '<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">'+
                        (o.disenoUrl?'<img src="'+esc(o.disenoUrl)+'" style="width:50px;height:50px;object-fit:cover;border-radius:8px;border:1px solid #e2e8f0;" onerror="this.style.display=\'none\'">':'')+
                        '<div style="flex:1;">'+
                            '<div style="font-weight:900;font-size:0.75rem;color:#0f172a;">'+esc(folio)+'</div>'+
                            '<div style="font-size:0.58rem;color:#6b7280;">'+esc(o.cliente||'—')+' · '+esc(o.producto||'—')+(o.cantidad?' x'+esc(o.cantidad):'')+'</div>'+
                        '</div>'+
                        '<span style="font-size:0.5rem;font-weight:700;padding:4px 8px;border-radius:6px;background:'+(stColors[estado]||'#94a3b8')+'20;color:'+(stColors[estado]||'#94a3b8')+';">'+esc(stLabels[estado]||estado)+'</span>'+
                    '</div>'+
                    actionBtn+
                '</div>';
            }).join('');

        listEl.querySelectorAll('.recol-action').forEach(function(btn){
            btn.addEventListener('click',function(){
                var id=btn.dataset.recolId;
                var action=btn.dataset.recolAction;
                if(action==='escanear') escanearRecoleccion(id);
                else if(action==='llevar') salirASucursal(id);
                else if(action==='entregar') confirmarEntregaSucursal(id);
            });
        });
    }

    function escanearRecoleccion(docId){
        var orden=allRecolApp.find(function(o){return o.id===docId;});if(!orden)return;
        var folioBuscado=orden.folioProduccion||'';
        // Open scan popup
        var overlay=document.createElement('div');
        overlay.style.cssText='position:fixed;inset:0;z-index:99999;background:rgba(0,0,0,0.6);display:flex;justify-content:center;align-items:center;';
        var card=document.createElement('div');
        card.style.cssText='background:#fff;border-radius:16px;padding:24px;width:min(92vw,500px);max-height:85vh;overflow-y:auto;box-shadow:0 8px 32px rgba(0,0,0,0.3);';
        card.innerHTML='<h3 style="margin:0 0 8px;font-size:0.85rem;color:#1f2937;">📷 Escanear Producto</h3>'+
            '<p style="font-size:0.62rem;color:#6b7280;margin:0 0 14px;">Escanea el código del producto <strong>'+esc(folioBuscado)+'</strong> para confirmar que es el correcto.</p>'+
            '<div style="display:flex;gap:8px;margin-bottom:12px;">'+
                '<input type="text" id="recolScanInput" placeholder="Código de barras o folio..." style="flex:1;border:1px solid #e5e7eb;border-radius:8px;padding:10px;font-size:0.72rem;">'+
                '<button id="recolScanVerify" style="padding:10px 16px;background:#ff9900;color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:700;font-size:0.72rem;">Verificar</button>'+
            '</div>'+
            '<div id="recolScanResult" style="margin-bottom:12px;"></div>'+
            (orden.disenoUrl?'<div style="text-align:center;margin-bottom:12px;"><img src="'+esc(orden.disenoUrl)+'" style="max-width:200px;max-height:200px;border-radius:10px;border:2px solid #e2e8f0;"><div style="font-size:0.5rem;color:#94a3b8;margin-top:4px;">Verifica que el producto coincida con la imagen</div></div>':'')+
            '<div style="display:flex;gap:8px;justify-content:flex-end;">'+
                '<button id="recolScanClose" style="padding:8px 16px;border:1px solid #d1d5db;border-radius:8px;background:#fff;cursor:pointer;">Cancelar</button>'+
            '</div>';
        overlay.appendChild(card);
        document.body.appendChild(overlay);

        document.getElementById('recolScanClose').addEventListener('click',function(){overlay.remove();});
        overlay.addEventListener('click',function(e){if(e.target===overlay)overlay.remove();});

        function verificar(){
            var code=(document.getElementById('recolScanInput')||{}).value.trim();
            var res=document.getElementById('recolScanResult');
            if(!code){if(res)res.innerHTML='<div style="color:#f59e0b;font-size:0.65rem;">⚠️ Ingresa un código</div>';return;}
            if(code===folioBuscado||(orden.codigoBarras&&code===orden.codigoBarras)){
                if(res) res.innerHTML='<div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;padding:12px;color:#166534;font-size:0.7rem;font-weight:700;">✅ ¡Correcto! Producto verificado.</div>';
                // Update Firestore
                var db=getEntDB();if(!db)return;
                db.collection('stored_orders').doc(docId).update({
                    estado:'recogido',
                    recogidoEn:new Date().toISOString(),
                    actualizadoEn:window.firebase.firestore.FieldValue.serverTimestamp()
                }).then(function(){
                    var o=allRecolApp.find(function(x){return x.id===docId;});if(o)o.estado='recogido';
                    setTimeout(function(){overlay.remove();renderRecolApp();},1500);
                }).catch(function(err){alert('Error: '+err.message);});
            } else {
                if(res) res.innerHTML='<div style="background:#fef2f2;border:1px solid #fecaca;border-radius:8px;padding:12px;color:#dc2626;font-size:0.7rem;font-weight:700;">❌ Código no coincide. Esperado: '+esc(folioBuscado)+'</div>';
            }
        }
        document.getElementById('recolScanVerify').addEventListener('click',verificar);
        document.getElementById('recolScanInput').addEventListener('keydown',function(e){if(e.key==='Enter')verificar();});
        document.getElementById('recolScanInput').focus();
    }

    function salirASucursal(docId){
        if(!confirm('¿Confirmar salida hacia sucursal con este producto?'))return;
        var db=getEntDB();if(!db)return;
        db.collection('stored_orders').doc(docId).update({
            estado:'en_transito_sucursal',
            salidaTallerEn:new Date().toISOString(),
            actualizadoEn:window.firebase.firestore.FieldValue.serverTimestamp()
        }).then(function(){
            var o=allRecolApp.find(function(x){return x.id===docId;});if(o)o.estado='en_transito_sucursal';
            renderRecolApp();
        }).catch(function(err){alert('Error: '+err.message);});
    }

    function confirmarEntregaSucursal(docId){
        if(!confirm('¿Confirmar que entregaste este producto en sucursal?'))return;
        var db=getEntDB();if(!db)return;
        db.collection('stored_orders').doc(docId).update({
            estado:'en_sucursal',
            llegadaSucursalEn:new Date().toISOString(),
            confirmadoEnSucursal:true,
            actualizadoEn:window.firebase.firestore.FieldValue.serverTimestamp()
        }).then(function(){
            allRecolApp=allRecolApp.filter(function(x){return x.id!==docId;});
            renderRecolApp();
            alert('✅ ¡Producto entregado en sucursal!');
        }).catch(function(err){alert('Error: '+err.message);});
    }

    // Hook into tab switching
    var _origTabClick=null;
    document.querySelectorAll('#entTabs .entrega-tab').forEach(function(tab){
        tab.addEventListener('click',function(){
            recolTabActive=(tab.dataset.status==='recoleccion');
            if(recolTabActive){
                cargarRecolApp();
            }
        });
    });
    // Initial load
    cargarRecolApp();"""

if ENT_SCRIPT_MARKER in content:
    content = content.replace(ENT_SCRIPT_MARKER, RECOLECCION_APP_JS, 1)
    count += 1; print(f"  {count}. Recolección App Móvil JS integrated")
else:
    errors.append("8: openRepartoPopupGlobal marker not found")

# ====================================================================
# WRITE
# ====================================================================
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nTotal replacements: {count}")
print("=" * 60)
if errors:
    print("WARNINGS:")
    for e in errors: print(f"  ⚠ {e}")
else:
    print("✅ PATCH COMPLETE!")
    print("   - Removed ALMACÉN PEDIDOS from main menu")
    print("   - Added 🏭 Recolección tab to Control de Reparto (Pedidos group)")
    print("   - Added 🏭 Recolección tab to App Móvil (repartidor)")
    print("   - Admin: asigna pedidos terminados → repartidor recoge → lleva a sucursal")
    print("   - Repartidor: escanea → confirma recogida → tránsito → entrega en sucursal")
print("=" * 60)
