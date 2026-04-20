#!/usr/bin/env python3
"""
Add ALMACÉN FÍSICO module inside Productos.
- Button in Productos toolbar
- Full overlay panel with: Ubicaciones, Movimientos, Inventario rápido, Historial
- localStorage-based storage
"""
FILE = '/workspaces/vistas/mockup.html'
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# ── 1: Add button in Productos icon grid ──
OLD_TOOLBAR = """                         <button id="prodImprimir" class="productos-btn productos-icon-btn" type="button" data-tip="Imprimir inventario" title="Imprimir inventario" aria-label="Imprimir inventario">🖨</button>"""

NEW_TOOLBAR = """                         <button id="prodImprimir" class="productos-btn productos-icon-btn" type="button" data-tip="Imprimir inventario" title="Imprimir inventario" aria-label="Imprimir inventario">🖨</button>
                         <button id="prodAlmacenFisico" class="productos-btn productos-icon-btn" type="button" data-tip="Almacén Físico" title="Almacén Físico" aria-label="Almacén Físico" style="background:#ff9900;color:#fff;font-weight:800;font-size:0.6rem;padding:5px 10px;border-radius:8px;">📦 ALMACÉN FÍSICO</button>"""

if OLD_TOOLBAR in content:
    content = content.replace(OLD_TOOLBAR, NEW_TOOLBAR, 1)
    changes += 1
    print("✅ 1: Almacén Físico button added to Productos toolbar")
else:
    print("⚠ 1: Toolbar marker not found")

# ── 2: Add overlay HTML before popupCaja ──
ALMACEN_HTML = '''
<!-- ═══════ ALMACÉN FÍSICO OVERLAY ═══════ -->
<div id="popupAlmacenFisico" style="display:none;position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,0.5);justify-content:center;align-items:center;">
<div style="background:#fff;width:min(96vw,1100px);height:min(92vh,800px);border-radius:16px;display:flex;flex-direction:column;overflow:hidden;box-shadow:0 8px 40px rgba(0,0,0,0.25);">
  <!-- Header -->
  <div style="display:flex;align-items:center;gap:12px;padding:14px 20px;border-bottom:2px solid #ff9900;background:linear-gradient(135deg,#fff7ed,#fffbeb);">
    <button id="almFisicoBack" type="button" style="background:none;border:none;font-size:1.3rem;cursor:pointer;padding:4px 8px;border-radius:8px;" title="Volver">←</button>
    <h2 style="margin:0;font-size:0.9rem;font-weight:900;color:#1f2937;flex:1;">📦 ALMACÉN FÍSICO</h2>
    <div id="almFisicoTabs" style="display:flex;gap:4px;">
      <button class="almf-tab active" data-almf-tab="ubicaciones">🗄 Ubicaciones</button>
      <button class="almf-tab" data-almf-tab="movimientos">🔄 Movimientos</button>
      <button class="almf-tab" data-almf-tab="inventario">📋 Inventario</button>
      <button class="almf-tab" data-almf-tab="historial">📜 Historial</button>
    </div>
  </div>
  <!-- Body -->
  <div style="flex:1;overflow-y:auto;padding:16px;" id="almFisicoBody">
    <!-- TAB: Ubicaciones -->
    <div id="almfSecUbicaciones" class="almf-section">
      <div style="display:flex;gap:8px;margin-bottom:12px;align-items:center;flex-wrap:wrap;">
        <input id="almfBuscarUbi" type="text" placeholder="🔍 Buscar ubicación, estante o contenedor..." style="flex:1;min-width:200px;padding:8px 12px;border:1px solid #e5e7eb;border-radius:8px;font-size:0.68rem;">
        <button id="almfAddUbi" type="button" style="padding:8px 16px;background:#ff9900;color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:800;font-size:0.65rem;">＋ NUEVA UBICACIÓN</button>
      </div>
      <div id="almfUbiGrid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:10px;"></div>
    </div>
    <!-- TAB: Movimientos -->
    <div id="almfSecMovimientos" class="almf-section" style="display:none;">
      <div style="background:#fffbeb;border:1px solid #fde68a;border-radius:12px;padding:16px;margin-bottom:14px;">
        <div style="font-weight:900;font-size:0.75rem;color:#92400e;margin-bottom:10px;">🔄 MOVER / TRASLADAR PRODUCTO</div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:end;">
          <div style="flex:1;min-width:160px;">
            <label style="font-size:0.52rem;font-weight:700;color:#6b7280;display:block;margin-bottom:3px;">ESCANEAR O BUSCAR PRODUCTO</label>
            <input id="almfMovProducto" type="text" placeholder="Código, etiqueta o nombre..." style="width:100%;padding:8px 10px;border:1px solid #d1d5db;border-radius:8px;font-size:0.65rem;">
          </div>
          <div style="min-width:140px;">
            <label style="font-size:0.52rem;font-weight:700;color:#6b7280;display:block;margin-bottom:3px;">DESDE (ORIGEN)</label>
            <select id="almfMovOrigen" style="width:100%;padding:8px;border:1px solid #d1d5db;border-radius:8px;font-size:0.62rem;"></select>
          </div>
          <div style="min-width:140px;">
            <label style="font-size:0.52rem;font-weight:700;color:#6b7280;display:block;margin-bottom:3px;">HACIA (DESTINO)</label>
            <select id="almfMovDestino" style="width:100%;padding:8px;border:1px solid #d1d5db;border-radius:8px;font-size:0.62rem;"></select>
          </div>
          <div style="min-width:80px;">
            <label style="font-size:0.52rem;font-weight:700;color:#6b7280;display:block;margin-bottom:3px;">CANTIDAD</label>
            <input id="almfMovCant" type="number" min="1" value="1" style="width:100%;padding:8px;border:1px solid #d1d5db;border-radius:8px;font-size:0.65rem;">
          </div>
          <div style="display:flex;gap:6px;">
            <button id="almfMovTrasladar" type="button" style="padding:8px 16px;background:#1e40af;color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:800;font-size:0.62rem;">🔄 TRASLADAR</button>
            <button id="almfMovRetirar" type="button" style="padding:8px 16px;background:#dc2626;color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:800;font-size:0.62rem;">📤 RETIRAR</button>
          </div>
        </div>
      </div>
      <div style="font-weight:800;font-size:0.68rem;color:#1f2937;margin-bottom:8px;">📋 MOVIMIENTOS RECIENTES</div>
      <div id="almfMovHistorial" style="max-height:400px;overflow-y:auto;"></div>
    </div>
    <!-- TAB: Inventario Rápido -->
    <div id="almfSecInventario" class="almf-section" style="display:none;">
      <div style="display:flex;gap:8px;margin-bottom:12px;align-items:center;flex-wrap:wrap;">
        <button id="almfIniciarInventario" type="button" style="padding:10px 20px;background:#16a34a;color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:800;font-size:0.7rem;">📋 INICIAR INVENTARIO</button>
        <select id="almfInvUbicacion" style="padding:8px 12px;border:1px solid #d1d5db;border-radius:8px;font-size:0.62rem;min-width:180px;">
          <option value="">TODAS LAS UBICACIONES</option>
        </select>
        <div style="flex:1;"></div>
        <span id="almfInvStatus" style="font-size:0.6rem;font-weight:700;color:#6b7280;">Sin inventario en curso</span>
      </div>
      <div id="almfInvPanel" style="display:none;">
        <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;padding:14px;margin-bottom:12px;">
          <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
            <input id="almfInvScan" type="text" placeholder="📷 Escanear etiqueta de producto o contenedor..." style="flex:1;min-width:200px;padding:10px 12px;border:2px solid #16a34a;border-radius:8px;font-size:0.72rem;font-weight:700;">
            <input id="almfInvCantidad" type="number" min="1" value="1" style="width:80px;padding:10px;border:1px solid #d1d5db;border-radius:8px;font-size:0.68rem;" placeholder="Cant.">
            <button id="almfInvAgregar" type="button" style="padding:10px 16px;background:#16a34a;color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:800;font-size:0.65rem;">✅ REGISTRAR</button>
          </div>
        </div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:12px;">
          <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:10px;text-align:center;">
            <div style="font-size:1.2rem;font-weight:900;color:#1e40af;" id="almfInvContados">0</div>
            <div style="font-size:0.5rem;color:#6b7280;">CONTADOS</div>
          </div>
          <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:10px;text-align:center;">
            <div style="font-size:1.2rem;font-weight:900;color:#16a34a;" id="almfInvCoinciden">0</div>
            <div style="font-size:0.5rem;color:#6b7280;">COINCIDEN</div>
          </div>
          <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:10px;text-align:center;">
            <div style="font-size:1.2rem;font-weight:900;color:#dc2626;" id="almfInvDiferencias">0</div>
            <div style="font-size:0.5rem;color:#6b7280;">DIFERENCIAS</div>
          </div>
          <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:10px;text-align:center;">
            <div style="font-size:1.2rem;font-weight:900;color:#f59e0b;" id="almfInvFaltantes">0</div>
            <div style="font-size:0.5rem;color:#6b7280;">FALTANTES</div>
          </div>
        </div>
        <div id="almfInvLista" style="max-height:350px;overflow-y:auto;"></div>
        <div style="display:flex;gap:8px;margin-top:12px;justify-content:flex-end;">
          <button id="almfInvCerrar" type="button" style="padding:8px 16px;border:1px solid #d1d5db;border-radius:8px;background:#fff;cursor:pointer;font-size:0.62rem;font-weight:700;">CANCELAR</button>
          <button id="almfInvFinalizar" type="button" style="padding:8px 16px;background:#ff9900;color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:800;font-size:0.62rem;">📋 FINALIZAR INVENTARIO</button>
        </div>
      </div>
    </div>
    <!-- TAB: Historial -->
    <div id="almfSecHistorial" class="almf-section" style="display:none;">
      <div style="display:flex;gap:8px;margin-bottom:12px;align-items:center;flex-wrap:wrap;">
        <input id="almfHistBuscar" type="text" placeholder="🔍 Buscar en historial..." style="flex:1;min-width:200px;padding:8px 12px;border:1px solid #e5e7eb;border-radius:8px;font-size:0.68rem;">
        <select id="almfHistTipo" style="padding:8px;border:1px solid #d1d5db;border-radius:8px;font-size:0.62rem;">
          <option value="">TODOS</option>
          <option value="traslado">TRASLADOS</option>
          <option value="retiro">RETIROS</option>
          <option value="ingreso">INGRESOS</option>
          <option value="inventario">INVENTARIOS</option>
        </select>
      </div>
      <div id="almfHistLista" style="max-height:500px;overflow-y:auto;"></div>
    </div>
  </div>
</div>
</div>

<style>
.almf-tab{padding:6px 12px;border:1px solid #e5e7eb;border-radius:8px;background:#fff;cursor:pointer;font-size:0.55rem;font-weight:700;color:#6b7280;transition:all .2s;}
.almf-tab:hover{background:#fff7ed;border-color:#ff9900;}
.almf-tab.active{background:#ff9900;color:#fff;border-color:#ff9900;}
</style>

'''

CAJA_MARKER = '<div id="popupCaja" class="caja-overlay" aria-hidden="true">'
if CAJA_MARKER in content:
    content = content.replace(CAJA_MARKER, ALMACEN_HTML + CAJA_MARKER, 1)
    changes += 1
    print("✅ 2: Almacén Físico HTML panel inserted")
else:
    print("⚠ 2: popupCaja marker not found")

# ── 3: Add JS before the Productos closeProductosPopup ──
# Insert after window.openProductosPopupGlobal line
JS_MARKER = "    window.openProductosPopupGlobal = openProductosPopup;"

ALMACEN_JS = '''    window.openProductosPopupGlobal = openProductosPopup;

    // ═══════ ALMACÉN FÍSICO JS ═══════
    (function(){
        var ALMF_UBI_KEY = 'almf_ubicaciones_v1';
        var ALMF_MOV_KEY = 'almf_movimientos_v1';
        var ALMF_INV_KEY = 'almf_inventarios_v1';

        var popup = document.getElementById('popupAlmacenFisico');
        var btnOpen = document.getElementById('prodAlmacenFisico');
        var btnClose = document.getElementById('almFisicoBack');
        if(!popup) return;

        function esc(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
        function loadJSON(k){try{return JSON.parse(localStorage.getItem(k)||'[]');}catch(e){return [];}}
        function saveJSON(k,d){localStorage.setItem(k,JSON.stringify(d));}
        function now(){return new Date().toLocaleString('es-MX',{day:'2-digit',month:'2-digit',year:'numeric',hour:'2-digit',minute:'2-digit',second:'2-digit'});}
        function getUser(){return localStorage.getItem('logged_user_email')||'admin';}

        var ubicaciones = loadJSON(ALMF_UBI_KEY);
        var movimientos = loadJSON(ALMF_MOV_KEY);
        var inventarios = loadJSON(ALMF_INV_KEY);
        var invEnCurso = null;

        // Open/close
        if(btnOpen) btnOpen.addEventListener('click',function(){
            popup.style.display='flex';
            ubicaciones=loadJSON(ALMF_UBI_KEY);
            movimientos=loadJSON(ALMF_MOV_KEY);
            renderUbicaciones();
            refreshUbiSelects();
        });
        if(btnClose) btnClose.addEventListener('click',function(){ popup.style.display='none'; });
        popup.addEventListener('click',function(e){ if(e.target===popup) popup.style.display='none'; });

        // Tabs
        document.getElementById('almFisicoTabs').addEventListener('click',function(e){
            var btn=e.target.closest('.almf-tab');if(!btn)return;
            document.querySelectorAll('.almf-tab').forEach(function(b){b.classList.remove('active');});
            btn.classList.add('active');
            var tab=btn.dataset.almfTab;
            document.querySelectorAll('.almf-section').forEach(function(s){s.style.display='none';});
            var sec=document.getElementById('almfSec'+tab.charAt(0).toUpperCase()+tab.slice(1));
            if(sec) sec.style.display='';
            if(tab==='ubicaciones') renderUbicaciones();
            if(tab==='movimientos'){refreshUbiSelects();renderMovHistorial();}
            if(tab==='historial') renderHistorial();
            if(tab==='inventario') refreshInvUbiSelect();
        });

        // ── UBICACIONES ──
        function renderUbicaciones(){
            var grid=document.getElementById('almfUbiGrid');if(!grid)return;
            var buscar=(document.getElementById('almfBuscarUbi')||{}).value||'';
            buscar=buscar.toLowerCase().trim();
            var lista=ubicaciones.filter(function(u){
                if(!buscar) return true;
                return (u.nombre||'').toLowerCase().includes(buscar)||(u.tipo||'').toLowerCase().includes(buscar)||(u.codigo||'').toLowerCase().includes(buscar);
            });
            if(!lista.length){
                grid.innerHTML='<div style="grid-column:1/-1;text-align:center;padding:40px;color:#94a3b8;font-size:0.65rem;"><div style="font-size:2rem;margin-bottom:8px;">🗄</div>Sin ubicaciones registradas.<br>Agrega estantes, contenedores o zonas.</div>';
                return;
            }
            grid.innerHTML=lista.map(function(u){
                var items=u.items||[];
                var totalQty=items.reduce(function(a,i){return a+(i.cantidad||0);},0);
                var tipoIcon={'estante':'🗄','contenedor':'📦','zona':'📍','rack':'🏗','refrigerador':'❄️'};
                return '<div style="background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:14px;transition:border-color .2s;cursor:pointer;" onmouseover="this.style.borderColor=\'#ff9900\'" onmouseout="this.style.borderColor=\'#e5e7eb\'" data-almf-ubi-id="'+esc(u.id)+'">'+
                    '<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">'+
                        '<span style="font-size:1.3rem;">'+(tipoIcon[u.tipo]||'📦')+'</span>'+
                        '<div style="flex:1;">'+
                            '<div style="font-weight:900;font-size:0.7rem;color:#0f172a;">'+esc(u.nombre)+'</div>'+
                            '<div style="font-size:0.5rem;color:#94a3b8;">'+esc(u.codigo||'Sin código')+' · '+esc(u.tipo||'general')+'</div>'+
                        '</div>'+
                        '<div style="text-align:right;">'+
                            '<div style="font-size:1rem;font-weight:900;color:#ff9900;">'+totalQty+'</div>'+
                            '<div style="font-size:0.42rem;color:#94a3b8;">productos</div>'+
                        '</div>'+
                    '</div>'+
                    (items.length?'<div style="display:flex;flex-wrap:wrap;gap:4px;">'+items.slice(0,5).map(function(it){
                        return '<span style="font-size:0.45rem;background:#f1f5f9;border-radius:4px;padding:2px 6px;color:#475569;">'+esc(it.nombre)+' x'+it.cantidad+'</span>';
                    }).join('')+(items.length>5?'<span style="font-size:0.45rem;color:#94a3b8;">+'+(items.length-5)+' más</span>':'')+'</div>':'')+
                    '<div style="display:flex;gap:4px;margin-top:8px;">'+
                        '<button class="almf-ubi-edit" data-id="'+esc(u.id)+'" style="font-size:0.48rem;padding:3px 8px;border:1px solid #d1d5db;border-radius:6px;background:#fff;cursor:pointer;">✏️ Editar</button>'+
                        '<button class="almf-ubi-del" data-id="'+esc(u.id)+'" style="font-size:0.48rem;padding:3px 8px;border:1px solid #fecaca;border-radius:6px;background:#fef2f2;color:#dc2626;cursor:pointer;">🗑 Eliminar</button>'+
                    '</div>'+
                '</div>';
            }).join('');

            grid.querySelectorAll('.almf-ubi-edit').forEach(function(b){
                b.addEventListener('click',function(e){e.stopPropagation();editarUbicacion(b.dataset.id);});
            });
            grid.querySelectorAll('.almf-ubi-del').forEach(function(b){
                b.addEventListener('click',function(e){e.stopPropagation();eliminarUbicacion(b.dataset.id);});
            });
        }

        document.getElementById('almfBuscarUbi').addEventListener('input',renderUbicaciones);

        document.getElementById('almfAddUbi').addEventListener('click',function(){
            var nombre=prompt('Nombre de la ubicación (ej: Estante A-1, Contenedor Rojo):');
            if(!nombre||!nombre.trim()) return;
            var tipo=prompt('Tipo: estante, contenedor, zona, rack, refrigerador','estante');
            var codigo=prompt('Código / Etiqueta (opcional):','');
            var id='ubi_'+Date.now()+'_'+Math.random().toString(36).substr(2,4);
            ubicaciones.push({id:id,nombre:nombre.trim(),tipo:(tipo||'estante').toLowerCase().trim(),codigo:(codigo||'').trim(),items:[],creadoEn:now(),creadoPor:getUser()});
            saveJSON(ALMF_UBI_KEY,ubicaciones);
            renderUbicaciones();
            refreshUbiSelects();
        });

        function editarUbicacion(id){
            var u=ubicaciones.find(function(x){return x.id===id;});if(!u)return;
            var nombre=prompt('Nombre:',u.nombre);if(!nombre||!nombre.trim())return;
            var tipo=prompt('Tipo:',u.tipo);
            var codigo=prompt('Código:',u.codigo);
            u.nombre=nombre.trim();u.tipo=(tipo||u.tipo).trim();u.codigo=(codigo||'').trim();
            saveJSON(ALMF_UBI_KEY,ubicaciones);
            renderUbicaciones();refreshUbiSelects();
        }

        function eliminarUbicacion(id){
            if(!confirm('¿Eliminar esta ubicación y todos sus productos?'))return;
            ubicaciones=ubicaciones.filter(function(x){return x.id!==id;});
            saveJSON(ALMF_UBI_KEY,ubicaciones);
            renderUbicaciones();refreshUbiSelects();
        }

        // ── MOVIMIENTOS ──
        function refreshUbiSelects(){
            var opts='<option value="">— Seleccionar —</option>'+ubicaciones.map(function(u){
                return '<option value="'+esc(u.id)+'">'+esc(u.nombre)+' ('+esc(u.codigo||u.tipo)+')</option>';
            }).join('');
            var orig=document.getElementById('almfMovOrigen');
            var dest=document.getElementById('almfMovDestino');
            if(orig) orig.innerHTML=opts;
            if(dest) dest.innerHTML=opts;
        }

        function registrarMovimiento(tipo,producto,origenId,destinoId,cantidad,notas){
            var mov={
                id:'mov_'+Date.now()+'_'+Math.random().toString(36).substr(2,4),
                tipo:tipo,producto:producto,origenId:origenId||'',destinoId:destinoId||'',
                cantidad:cantidad,notas:notas||'',fecha:now(),usuario:getUser()
            };
            movimientos.unshift(mov);
            if(movimientos.length>500) movimientos=movimientos.slice(0,500);
            saveJSON(ALMF_MOV_KEY,movimientos);
            return mov;
        }

        document.getElementById('almfMovTrasladar').addEventListener('click',function(){
            var prod=(document.getElementById('almfMovProducto')||{}).value.trim();
            var origId=(document.getElementById('almfMovOrigen')||{}).value;
            var destId=(document.getElementById('almfMovDestino')||{}).value;
            var cant=parseInt((document.getElementById('almfMovCant')||{}).value)||1;
            if(!prod){alert('Ingresa un producto');return;}
            if(!origId){alert('Selecciona ubicación de origen');return;}
            if(!destId){alert('Selecciona ubicación de destino');return;}
            if(origId===destId){alert('Origen y destino no pueden ser iguales');return;}

            var orig=ubicaciones.find(function(u){return u.id===origId;});
            var dest=ubicaciones.find(function(u){return u.id===destId;});
            if(!orig||!dest) return;

            // Remove from origin
            var item=orig.items.find(function(i){return i.nombre.toLowerCase()===prod.toLowerCase()||i.codigo===prod;});
            if(!item){alert('Producto no encontrado en origen. Se registrará igualmente.');} 
            else {
                item.cantidad=Math.max(0,(item.cantidad||0)-cant);
                if(item.cantidad<=0) orig.items=orig.items.filter(function(i){return i!==item;});
            }

            // Add to destination
            var destItem=dest.items.find(function(i){return i.nombre.toLowerCase()===prod.toLowerCase();});
            if(destItem) destItem.cantidad=(destItem.cantidad||0)+cant;
            else dest.items.push({nombre:prod,cantidad:cant,codigo:prod,movidoEn:now()});

            saveJSON(ALMF_UBI_KEY,ubicaciones);
            registrarMovimiento('traslado',prod,origId,destId,cant,'De '+orig.nombre+' a '+dest.nombre);
            alert('✅ '+cant+'x '+prod+' trasladado de '+orig.nombre+' a '+dest.nombre);
            document.getElementById('almfMovProducto').value='';
            renderMovHistorial();
        });

        document.getElementById('almfMovRetirar').addEventListener('click',function(){
            var prod=(document.getElementById('almfMovProducto')||{}).value.trim();
            var origId=(document.getElementById('almfMovOrigen')||{}).value;
            var cant=parseInt((document.getElementById('almfMovCant')||{}).value)||1;
            if(!prod){alert('Ingresa un producto');return;}
            if(!origId){alert('Selecciona ubicación de origen');return;}

            var orig=ubicaciones.find(function(u){return u.id===origId;});
            if(!orig) return;
            var item=orig.items.find(function(i){return i.nombre.toLowerCase()===prod.toLowerCase()||i.codigo===prod;});
            if(item){
                item.cantidad=Math.max(0,(item.cantidad||0)-cant);
                if(item.cantidad<=0) orig.items=orig.items.filter(function(i){return i!==item;});
            }
            saveJSON(ALMF_UBI_KEY,ubicaciones);
            registrarMovimiento('retiro',prod,origId,'',cant,'Retirado de '+orig.nombre);
            alert('📤 '+cant+'x '+prod+' retirado de '+orig.nombre);
            document.getElementById('almfMovProducto').value='';
            renderMovHistorial();
        });

        function renderMovHistorial(){
            var el=document.getElementById('almfMovHistorial');if(!el)return;
            var recientes=movimientos.slice(0,30);
            if(!recientes.length){el.innerHTML='<div style="text-align:center;padding:20px;color:#94a3b8;font-size:0.6rem;">Sin movimientos registrados</div>';return;}
            el.innerHTML=recientes.map(function(m){
                var icons={traslado:'🔄',retiro:'📤',ingreso:'📥',inventario:'📋'};
                var colors={traslado:'#1e40af',retiro:'#dc2626',ingreso:'#16a34a',inventario:'#f59e0b'};
                return '<div style="display:flex;align-items:center;gap:10px;padding:8px 12px;border-bottom:1px solid #f1f5f9;">'+
                    '<span style="font-size:1.1rem;">'+(icons[m.tipo]||'📦')+'</span>'+
                    '<div style="flex:1;">'+
                        '<div style="font-weight:700;font-size:0.62rem;color:#0f172a;">'+esc(m.producto)+' <span style="color:'+(colors[m.tipo]||'#6b7280')+';font-size:0.5rem;">'+esc(m.tipo.toUpperCase())+'</span></div>'+
                        '<div style="font-size:0.48rem;color:#94a3b8;">'+esc(m.notas||'')+'</div>'+
                    '</div>'+
                    '<div style="text-align:right;">'+
                        '<div style="font-weight:800;font-size:0.65rem;color:'+(colors[m.tipo]||'#6b7280')+';">x'+m.cantidad+'</div>'+
                        '<div style="font-size:0.42rem;color:#94a3b8;">'+esc(m.fecha)+'</div>'+
                        '<div style="font-size:0.42rem;color:#94a3b8;">'+esc(m.usuario)+'</div>'+
                    '</div>'+
                '</div>';
            }).join('');
        }

        // ── INVENTARIO RÁPIDO ──
        function refreshInvUbiSelect(){
            var sel=document.getElementById('almfInvUbicacion');if(!sel)return;
            sel.innerHTML='<option value="">TODAS LAS UBICACIONES</option>'+ubicaciones.map(function(u){
                return '<option value="'+esc(u.id)+'">'+esc(u.nombre)+'</option>';
            }).join('');
        }

        document.getElementById('almfIniciarInventario').addEventListener('click',function(){
            var ubiId=(document.getElementById('almfInvUbicacion')||{}).value;
            invEnCurso={id:'inv_'+Date.now(),ubicacionId:ubiId,inicio:now(),usuario:getUser(),items:[],finalizado:false};
            document.getElementById('almfInvPanel').style.display='';
            document.getElementById('almfInvStatus').textContent='📋 Inventario en curso...';
            document.getElementById('almfInvStatus').style.color='#16a34a';
            document.getElementById('almfInvScan').focus();
            renderInvLista();
        });

        document.getElementById('almfInvAgregar').addEventListener('click',function(){registrarItemInv();});
        document.getElementById('almfInvScan').addEventListener('keydown',function(e){
            if(e.key==='Enter') registrarItemInv();
        });

        function registrarItemInv(){
            if(!invEnCurso) return;
            var scan=(document.getElementById('almfInvScan')||{}).value.trim();
            var cant=parseInt((document.getElementById('almfInvCantidad')||{}).value)||1;
            if(!scan) return;
            var existente=invEnCurso.items.find(function(i){return i.codigo===scan||i.nombre===scan;});
            if(existente) existente.contado=(existente.contado||0)+cant;
            else invEnCurso.items.push({codigo:scan,nombre:scan,contado:cant});
            document.getElementById('almfInvScan').value='';
            document.getElementById('almfInvScan').focus();
            renderInvLista();
        }

        function renderInvLista(){
            if(!invEnCurso) return;
            var el=document.getElementById('almfInvLista');if(!el)return;

            // Compare with actual stock in selected location
            var ubiId=invEnCurso.ubicacionId;
            var stockReal=[];
            if(ubiId){
                var ubi=ubicaciones.find(function(u){return u.id===ubiId;});
                if(ubi) stockReal=ubi.items||[];
            } else {
                ubicaciones.forEach(function(u){(u.items||[]).forEach(function(it){
                    var ex=stockReal.find(function(s){return s.nombre===it.nombre;});
                    if(ex) ex.cantidad=(ex.cantidad||0)+(it.cantidad||0);
                    else stockReal.push({nombre:it.nombre,cantidad:it.cantidad||0});
                });});
            }

            var contados=invEnCurso.items.length;
            var coinciden=0;var diferencias=0;
            invEnCurso.items.forEach(function(it){
                var real=stockReal.find(function(s){return s.nombre.toLowerCase()===it.nombre.toLowerCase();});
                if(real && real.cantidad===it.contado) coinciden++;
                else diferencias++;
            });
            var faltantes=stockReal.filter(function(s){
                return !invEnCurso.items.find(function(i){return i.nombre.toLowerCase()===s.nombre.toLowerCase();});
            }).length;

            document.getElementById('almfInvContados').textContent=contados;
            document.getElementById('almfInvCoinciden').textContent=coinciden;
            document.getElementById('almfInvDiferencias').textContent=diferencias;
            document.getElementById('almfInvFaltantes').textContent=faltantes;

            var rows=invEnCurso.items.map(function(it){
                var real=stockReal.find(function(s){return s.nombre.toLowerCase()===it.nombre.toLowerCase();});
                var esperado=real?real.cantidad:0;
                var diff=it.contado-esperado;
                var diffColor=diff===0?'#16a34a':(diff>0?'#f59e0b':'#dc2626');
                return '<div style="display:flex;align-items:center;gap:10px;padding:8px 12px;border-bottom:1px solid #f1f5f9;">'+
                    '<div style="flex:1;font-weight:700;font-size:0.62rem;color:#0f172a;">'+esc(it.nombre)+'</div>'+
                    '<div style="text-align:center;width:70px;"><div style="font-size:0.5rem;color:#6b7280;">CONTADO</div><div style="font-weight:900;font-size:0.72rem;color:#1e40af;">'+it.contado+'</div></div>'+
                    '<div style="text-align:center;width:70px;"><div style="font-size:0.5rem;color:#6b7280;">SISTEMA</div><div style="font-weight:900;font-size:0.72rem;">'+esperado+'</div></div>'+
                    '<div style="text-align:center;width:70px;"><div style="font-size:0.5rem;color:#6b7280;">DIFF</div><div style="font-weight:900;font-size:0.72rem;color:'+diffColor+';">'+(diff>0?'+':'')+diff+'</div></div>'+
                '</div>';
            });
            // Show missing items from stock
            stockReal.forEach(function(s){
                if(!invEnCurso.items.find(function(i){return i.nombre.toLowerCase()===s.nombre.toLowerCase();})){
                    rows.push('<div style="display:flex;align-items:center;gap:10px;padding:8px 12px;border-bottom:1px solid #f1f5f9;background:#fef2f2;">'+
                        '<div style="flex:1;font-weight:700;font-size:0.62rem;color:#dc2626;">⚠ '+esc(s.nombre)+' <span style="font-weight:400;font-size:0.5rem;">(no contado)</span></div>'+
                        '<div style="text-align:center;width:70px;"><div style="font-weight:900;font-size:0.72rem;color:#94a3b8;">—</div></div>'+
                        '<div style="text-align:center;width:70px;"><div style="font-weight:900;font-size:0.72rem;">'+s.cantidad+'</div></div>'+
                        '<div style="text-align:center;width:70px;"><div style="font-weight:900;font-size:0.72rem;color:#dc2626;">-'+s.cantidad+'</div></div>'+
                    '</div>');
                }
            });
            el.innerHTML=rows.join('')||'<div style="text-align:center;padding:20px;color:#94a3b8;font-size:0.6rem;">Escanea productos para iniciar el conteo</div>';
        }

        document.getElementById('almfInvCerrar').addEventListener('click',function(){
            invEnCurso=null;
            document.getElementById('almfInvPanel').style.display='none';
            document.getElementById('almfInvStatus').textContent='Sin inventario en curso';
            document.getElementById('almfInvStatus').style.color='#6b7280';
        });

        document.getElementById('almfInvFinalizar').addEventListener('click',function(){
            if(!invEnCurso||!invEnCurso.items.length){alert('No hay items contados');return;}
            invEnCurso.fin=now();invEnCurso.finalizado=true;
            inventarios.unshift(invEnCurso);
            if(inventarios.length>50) inventarios=inventarios.slice(0,50);
            saveJSON(ALMF_INV_KEY,inventarios);
            registrarMovimiento('inventario','Inventario '+invEnCurso.id,invEnCurso.ubicacionId,'',invEnCurso.items.length,'Inventario con '+invEnCurso.items.length+' items por '+invEnCurso.usuario);
            alert('📋 Inventario finalizado con '+invEnCurso.items.length+' items contados.\\nRealizado por: '+invEnCurso.usuario+'\\nHora: '+invEnCurso.fin);
            invEnCurso=null;
            document.getElementById('almfInvPanel').style.display='none';
            document.getElementById('almfInvStatus').textContent='Sin inventario en curso';
            document.getElementById('almfInvStatus').style.color='#6b7280';
        });

        // ── HISTORIAL ──
        function renderHistorial(){
            var el=document.getElementById('almfHistLista');if(!el)return;
            var buscar=((document.getElementById('almfHistBuscar')||{}).value||'').toLowerCase().trim();
            var tipo=(document.getElementById('almfHistTipo')||{}).value;
            var lista=movimientos.filter(function(m){
                if(tipo && m.tipo!==tipo) return false;
                if(buscar && !(m.producto||'').toLowerCase().includes(buscar) && !(m.notas||'').toLowerCase().includes(buscar) && !(m.usuario||'').toLowerCase().includes(buscar)) return false;
                return true;
            });

            // Also add inventarios at the end
            var invList=inventarios.map(function(inv){
                return {id:inv.id,tipo:'inventario',producto:'Inventario General',cantidad:inv.items.length,
                    notas:(inv.ubicacionId?'Ubicación: '+(ubicaciones.find(function(u){return u.id===inv.ubicacionId;})||{}).nombre||inv.ubicacionId:'Todas las ubicaciones')+' — '+inv.items.length+' items',
                    fecha:inv.fin||inv.inicio,usuario:inv.usuario};
            });
            if(tipo===''||tipo==='inventario') lista=lista.concat(invList);

            if(!lista.length){el.innerHTML='<div style="text-align:center;padding:30px;color:#94a3b8;font-size:0.6rem;">Sin registros en historial</div>';return;}

            el.innerHTML=lista.slice(0,100).map(function(m){
                var icons={traslado:'🔄',retiro:'📤',ingreso:'📥',inventario:'📋'};
                var colors={traslado:'#1e40af',retiro:'#dc2626',ingreso:'#16a34a',inventario:'#f59e0b'};
                var bg={traslado:'#eff6ff',retiro:'#fef2f2',ingreso:'#f0fdf4',inventario:'#fffbeb'};
                return '<div style="display:flex;align-items:center;gap:10px;padding:10px 14px;border-bottom:1px solid #f1f5f9;background:'+(bg[m.tipo]||'#fff')+';">'+
                    '<span style="font-size:1.2rem;">'+(icons[m.tipo]||'📦')+'</span>'+
                    '<div style="flex:1;">'+
                        '<div style="font-weight:700;font-size:0.62rem;color:#0f172a;">'+esc(m.producto)+'</div>'+
                        '<div style="font-size:0.5rem;color:#64748b;">'+esc(m.notas||'—')+'</div>'+
                    '</div>'+
                    '<div style="text-align:right;min-width:90px;">'+
                        '<div style="font-weight:800;font-size:0.58rem;color:'+(colors[m.tipo]||'#6b7280')+';">'+esc((m.tipo||'').toUpperCase())+' x'+(m.cantidad||0)+'</div>'+
                        '<div style="font-size:0.45rem;color:#94a3b8;">'+esc(m.fecha||'')+'</div>'+
                        '<div style="font-size:0.45rem;color:#94a3b8;">👤 '+esc(m.usuario||'')+'</div>'+
                    '</div>'+
                '</div>';
            }).join('');
        }

        var histBuscar=document.getElementById('almfHistBuscar');
        var histTipo=document.getElementById('almfHistTipo');
        if(histBuscar) histBuscar.addEventListener('input',renderHistorial);
        if(histTipo) histTipo.addEventListener('change',renderHistorial);

    })();'''

if JS_MARKER in content:
    content = content.replace(JS_MARKER, ALMACEN_JS, 1)
    changes += 1
    print("✅ 3: Almacén Físico JS module added")
else:
    print("⚠ 3: openProductosPopupGlobal marker not found")

if changes:
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"\n✅ Done — {changes} change(s) applied")
else:
    print("\n❌ No changes made")
