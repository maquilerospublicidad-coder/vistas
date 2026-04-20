#!/usr/bin/env python3
"""Fix patch step 8: Add Recolección JS to App Móvil entregas script"""
FILE = '/workspaces/vistas/mockup.html'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

MARKER = "    window.openRepartoPopupGlobal = openRepartoPanel;\n    window.closeRepartoPopupGlobal = closeRepartoPanel;"

RECOL_JS = """    window.openRepartoPopupGlobal = openRepartoPanel;
    window.closeRepartoPopupGlobal = closeRepartoPanel;

    // ── RECOLECCIÓN TAB (Repartidor App Móvil) ──
    var recolTabActive = false;
    var allRecolApp = [];

    function cargarRecolApp(){
        var db = getEntDB(); if(!db) return;
        db.collection('stored_orders').orderBy('creadoEn','desc').get().then(function(snap){
            allRecolApp = snap.docs.map(function(d){ return Object.assign({id:d.id}, d.data()); })
                .filter(function(o){ return ['asignado_recoleccion','recogido','en_transito_sucursal'].indexOf(o.estado)>=0; });
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
                    actionBtn='<button class="recol-action" data-recol-action="escanear" data-recol-id="'+esc(o.id)+'" style="padding:8px 14px;background:#ff9900;color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:800;font-size:0.65rem;width:100%;margin-top:8px;">📷 ESCANEAR Y RECOGER</button>';
                } else if(estado==='recogido'){
                    actionBtn='<button class="recol-action" data-recol-action="llevar" data-recol-id="'+esc(o.id)+'" style="padding:8px 14px;background:#1e40af;color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:800;font-size:0.65rem;width:100%;margin-top:8px;">🏬 SALIR A SUCURSAL</button>';
                } else if(estado==='en_transito_sucursal'){
                    actionBtn='<button class="recol-action" data-recol-action="entregar" data-recol-id="'+esc(o.id)+'" style="padding:8px 14px;background:#16a34a;color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:800;font-size:0.65rem;width:100%;margin-top:8px;">✅ ENTREGADO EN SUCURSAL</button>';
                }
                return '<div style="background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:12px;margin-bottom:8px;">'+
                    '<div style="display:flex;align-items:center;gap:10px;">'+
                        (o.disenoUrl?'<img src="'+esc(o.disenoUrl)+'" style="width:50px;height:50px;object-fit:cover;border-radius:8px;border:1px solid #e2e8f0;" onerror="this.style.display=\\'none\\'">':'')+
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
                if(action==='escanear') escanearRecoleccionApp(id);
                else if(action==='llevar') salirASucursalApp(id);
                else if(action==='entregar') confirmarEntregaSucursalApp(id);
            });
        });
    }

    function escanearRecoleccionApp(docId){
        var orden=allRecolApp.find(function(o){return o.id===docId;});if(!orden)return;
        var folioBuscado=orden.folioProduccion||'';
        var overlay=document.createElement('div');
        overlay.style.cssText='position:fixed;inset:0;z-index:99999;background:rgba(0,0,0,0.6);display:flex;justify-content:center;align-items:center;';
        var card=document.createElement('div');
        card.style.cssText='background:#fff;border-radius:16px;padding:24px;width:min(92vw,500px);max-height:85vh;overflow-y:auto;box-shadow:0 8px 32px rgba(0,0,0,0.3);';
        card.innerHTML='<h3 style="margin:0 0 8px;font-size:0.85rem;color:#1f2937;">📷 Escanear Producto</h3>'+
            '<p style="font-size:0.62rem;color:#6b7280;margin:0 0 14px;">Escanea el código de <strong>'+esc(folioBuscado)+'</strong> para confirmar la recolección.</p>'+
            '<div style="display:flex;gap:8px;margin-bottom:12px;">'+
                '<input type="text" id="recolAppScanInput" placeholder="Código de barras o folio..." style="flex:1;border:1px solid #e5e7eb;border-radius:8px;padding:10px;font-size:0.72rem;">'+
                '<button id="recolAppScanVerify" style="padding:10px 16px;background:#ff9900;color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:700;font-size:0.72rem;">Verificar</button>'+
            '</div>'+
            '<div id="recolAppScanResult" style="margin-bottom:12px;"></div>'+
            (orden.disenoUrl?'<div style="text-align:center;margin-bottom:12px;"><img src="'+esc(orden.disenoUrl)+'" style="max-width:200px;max-height:200px;border-radius:10px;border:2px solid #e2e8f0;"><div style="font-size:0.5rem;color:#94a3b8;margin-top:4px;">Verifica que coincida con la imagen</div></div>':'')+
            '<div style="display:flex;gap:8px;justify-content:flex-end;">'+
                '<button id="recolAppScanClose" style="padding:8px 16px;border:1px solid #d1d5db;border-radius:8px;background:#fff;cursor:pointer;">Cancelar</button></div>';
        overlay.appendChild(card);document.body.appendChild(overlay);
        document.getElementById('recolAppScanClose').addEventListener('click',function(){overlay.remove();});
        overlay.addEventListener('click',function(e){if(e.target===overlay)overlay.remove();});
        function verificar(){
            var code=(document.getElementById('recolAppScanInput')||{}).value.trim();
            var res=document.getElementById('recolAppScanResult');
            if(!code){if(res)res.innerHTML='<div style="color:#f59e0b;font-size:0.65rem;">⚠️ Ingresa un código</div>';return;}
            if(code===folioBuscado||(orden.codigoBarras&&code===orden.codigoBarras)){
                if(res) res.innerHTML='<div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;padding:12px;color:#166534;font-size:0.7rem;font-weight:700;">✅ ¡Correcto! Producto verificado.</div>';
                var db=getEntDB();if(!db)return;
                db.collection('stored_orders').doc(docId).update({estado:'recogido',recogidoEn:new Date().toISOString(),actualizadoEn:window.firebase.firestore.FieldValue.serverTimestamp()}).then(function(){
                    var o=allRecolApp.find(function(x){return x.id===docId;});if(o)o.estado='recogido';
                    setTimeout(function(){overlay.remove();renderRecolApp();},1500);
                }).catch(function(err){alert('Error: '+err.message);});
            } else {
                if(res) res.innerHTML='<div style="background:#fef2f2;border:1px solid #fecaca;border-radius:8px;padding:12px;color:#dc2626;font-size:0.7rem;font-weight:700;">❌ Código no coincide. Esperado: '+esc(folioBuscado)+'</div>';
            }
        }
        document.getElementById('recolAppScanVerify').addEventListener('click',verificar);
        document.getElementById('recolAppScanInput').addEventListener('keydown',function(e){if(e.key==='Enter')verificar();});
        document.getElementById('recolAppScanInput').focus();
    }

    function salirASucursalApp(docId){
        if(!confirm('¿Confirmar salida hacia sucursal?'))return;
        var db=getEntDB();if(!db)return;
        db.collection('stored_orders').doc(docId).update({estado:'en_transito_sucursal',salidaTallerEn:new Date().toISOString(),actualizadoEn:window.firebase.firestore.FieldValue.serverTimestamp()}).then(function(){
            var o=allRecolApp.find(function(x){return x.id===docId;});if(o)o.estado='en_transito_sucursal';
            renderRecolApp();
        }).catch(function(err){alert('Error: '+err.message);});
    }

    function confirmarEntregaSucursalApp(docId){
        if(!confirm('¿Confirmar entrega en sucursal?'))return;
        var db=getEntDB();if(!db)return;
        db.collection('stored_orders').doc(docId).update({estado:'en_sucursal',llegadaSucursalEn:new Date().toISOString(),confirmadoEnSucursal:true,actualizadoEn:window.firebase.firestore.FieldValue.serverTimestamp()}).then(function(){
            allRecolApp=allRecolApp.filter(function(x){return x.id!==docId;});
            renderRecolApp();alert('✅ ¡Producto entregado en sucursal!');
        }).catch(function(err){alert('Error: '+err.message);});
    }

    // Hook: when recoleccion tab clicked, show recoleccion view
    var _origEntTabHandler = null;
    document.querySelectorAll('#entTabs .entrega-tab').forEach(function(tab){
        tab.addEventListener('click',function(){
            recolTabActive = (tab.dataset.status === 'recoleccion');
            if(recolTabActive){ cargarRecolApp(); renderRecolApp(); }
        });
    });
    cargarRecolApp();"""

if MARKER in content:
    content = content.replace(MARKER, RECOL_JS, 1)
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Recolección App Móvil JS added successfully")
else:
    print("ERROR: marker not found")
    # Debug
    import re
    matches = [i for i, line in enumerate(content.split('\n'), 1) if 'openRepartoPopupGlobal' in line]
    print(f"  Lines with 'openRepartoPopupGlobal': {matches}")
