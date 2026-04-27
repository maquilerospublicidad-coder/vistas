#!/usr/bin/env python3
"""Patch: convertir prodFormCard en wizard multi-paso."""
import sys

FILE = '/workspaces/vistas/mockup.html'

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

original_len = len(content)

# ─────────────────────────────────────────────────────────────
# 1. REEMPLAZAR HTML del prodFormCard
# ─────────────────────────────────────────────────────────────
HTML_OLD_START = '<div id="popupProdForm" class="productos-modal-overlay" aria-hidden="true">'
HTML_OLD_END   = '\n<!-- ============ MODAL: CONFIGURAR UNIDADES DE MEDIDA ============ -->'

idx_start = content.find(HTML_OLD_START)
idx_end   = content.find('\n<!-- ============ MODAL: CONFIGURAR UNIDADES DE MEDIDA ============ -->')

if idx_start == -1:
    print('ERROR: no se encontró popupProdForm'); sys.exit(1)
if idx_end == -1:
    print('ERROR: no se encontró marcador de fin'); sys.exit(1)

NEW_HTML = '''\
<div id="popupProdForm" class="productos-modal-overlay" aria-hidden="true">
    <div id="prodFormCard" class="productos-modal-card wide" role="dialog" aria-modal="true" aria-labelledby="prodFormTitulo">
        <h3 id="prodFormTitulo" class="productos-modal-title">Agregar producto</h3>
        <div class="prod-form-wizard">
            <aside class="prod-photo-pane">
                <h4>📷 Foto del producto</h4>
                <div class="prod-foto-principal-box">
                    <div id="prodFormFotoPreview" class="prod-foto-preview">Sin foto principal</div>
                    <input id="prodFormFotoPrincipal" type="file" accept="image/*">
                </div>
                <div class="prod-photo-pane-extras">
                    <hr class="photo-pane-separator">
                    <label style="font-size:0.52rem;font-weight:900;letter-spacing:0.3px;color:rgba(255,255,255,0.9);">📦 UBICACIÓN EN ALMACÉN</label>
                    <div class="ubicacion-grid">
                        <div class="ubi-cell">
                            <label>PASILLO</label>
                            <input id="prodFormUbiPasillo" type="text" maxlength="4" placeholder="P1" style="text-transform:uppercase;">
                        </div>
                        <div class="ubi-cell">
                            <label>RACK</label>
                            <input id="prodFormUbiRack" type="text" maxlength="4" placeholder="R1" style="text-transform:uppercase;">
                        </div>
                        <div class="ubi-cell">
                            <label>NIVEL</label>
                            <input id="prodFormUbiNivel" type="text" maxlength="4" placeholder="N1" style="text-transform:uppercase;">
                        </div>
                        <div class="ubi-cell">
                            <label>CONT.</label>
                            <input id="prodFormUbiContenedor" type="text" maxlength="4" placeholder="C1" style="text-transform:uppercase;">
                        </div>
                    </div>
                    <div id="prodFormUbiCodigoWrap" class="ubicacion-codigo empty">Sin ubicación asignada</div>
                    <div style="display:flex;gap:3px;">
                        <button type="button" id="prodFormEtiquetaContenedor" class="btn-generar-etiqueta" disabled style="flex:1;font-size:0.48rem;">🏷️ Contenedor</button>
                        <button type="button" id="prodFormEtiquetaProducto" class="btn-generar-etiqueta" disabled style="flex:1;font-size:0.48rem;">Producto</button>
                    </div>
                    <hr class="photo-pane-separator">
                    <label style="font-size:0.52rem;font-weight:900;letter-spacing:0.3px;color:rgba(255,255,255,0.75);margin-bottom:3px;display:block;">📋 PASOS</label>
                    <div id="prodStepNav" class="prod-step-nav"></div>
                    <textarea id="prodFormNotasInternas" style="display:none;" placeholder="Notas solo visibles para el equipo..."></textarea>
                    <hr class="photo-pane-separator">
                    <label class="photo-pane-toggle">
                        <input type="checkbox" id="prodFormActivo" checked>
                        <span>✅ Producto activo</span>
                    </label>
                </div>
            </aside>
            <div class="prod-form-main">
                <div class="prod-wizard-header" id="prodWizardHeader">
                    <span id="prodWizardStepTitle" class="prod-wizard-title">Identificación</span>
                    <span id="prodWizardStepCount" class="prod-wizard-count">Paso 1 de 6</span>
                </div>

                <!-- PASO: basico ─ Identificación -->
                <div class="prod-step-panel active" data-step="basico">
                    <div class="productos-modal-grid">
                        <div class="orden-field productos-field-span3">
                            <label for="prodFormCodigo">Código de producto (15 dígitos)</label>
                            <div class="productos-code-row" style="display:flex;gap:4px;align-items:center;">
                                <input id="prodFormCodigo" type="text" maxlength="15" placeholder="15 dígitos" style="flex:1;">
                                <button id="prodFormGenerarCodigo" class="productos-btn" type="button">Generar</button>
                                <button id="prodFormScanCodigo" class="productos-btn" type="button" title="Escanear código de barras" style="padding:6px 10px;font-size:0.75rem;">📷 Escanear</button>
                            </div>
                        </div>
                        <div class="orden-field"><label for="prodFormTipo">TIPO DE PRODUCTO</label><select id="prodFormTipo"><option value="stock">PRODUCTO</option><option value="gran-formato">GRAN FORMATO</option><option value="fabricado">FABRICADO</option><option value="insumo">INSUMO</option><option value="proceso">PROCESO</option><option value="servicio">SERVICIO</option></select></div>
                        <div class="orden-field" id="prodFormNombreWrap"><label for="prodFormProducto">Nombre</label><input id="prodFormProducto" type="text" placeholder="Nombre del artículo"></div>
                        <div class="orden-field prod-stock-only" data-nat="producto,fabricado,insumo"><label for="prodFormCategoria">Categoría</label><div style="display:flex;gap:4px;align-items:center;"><select id="prodFormCategoria" style="flex:1;"><option value="">Seleccionar...</option></select><button type="button" id="prodFormCategoriaAdd" class="productos-btn" style="padding:4px 8px;font-size:0.7rem;white-space:nowrap;" title="Agregar categoría">+</button></div></div>
                        <div class="orden-field" data-nat="producto,fabricado,insumo"><label for="prodFormMaterial">Material</label><input id="prodFormMaterial" type="text"></div>
                        <div class="orden-field" data-nat="insumo"><label for="prodFormDesgastePorUso">Desgaste por unidad usada</label><input id="prodFormDesgastePorUso" type="number" min="0" step="0.001" value="1" placeholder="Cantidad que se consume por uso"></div>
                        <div class="orden-field prod-stock-only productos-field-span3" data-nat="producto,fabricado,insumo,proceso,servicio"><label for="prodFormDescripcion">Descripción</label><textarea id="prodFormDescripcion" rows="2" placeholder="Descripción del producto" style="resize:none;"></textarea></div>
                    </div>
                </div>

                <!-- PASO: stock-compra ─ Stock y Compra -->
                <div class="prod-step-panel" data-step="stock-compra">
                    <div class="productos-modal-grid">
                        <div class="orden-field prod-stock-only" data-nat="producto,fabricado,insumo">
                            <label for="prodFormUMCompra">U. medida compra</label>
                            <select id="prodFormUMCompra" style="width:100%;"></select>
                        </div>
                        <div class="orden-field prod-stock-only" data-nat="producto,fabricado,insumo">
                            <label for="prodFormUMVenta">U. medida venta</label>
                            <div style="display:flex;gap:4px;align-items:center;">
                                <select id="prodFormUMVenta" style="flex:1;"></select>
                                <button type="button" id="prodFormUMConfig" class="productos-btn" style="padding:4px 8px;font-size:0.7rem;" title="Configurar unidades de medida">⚙</button>
                            </div>
                        </div>
                        <div class="orden-field prod-stock-only" data-nat="producto,fabricado,insumo"><label for="prodFormExistencias">Existencias</label><input id="prodFormExistencias" type="number" min="0" step="1"></div>
                        <div class="orden-field prod-stock-only" data-nat="producto,fabricado"><label for="prodFormMinima">Cantidad mínima</label><input id="prodFormMinima" type="number" min="0" step="1"></div>
                        <div class="orden-field prod-stock-only" data-nat="producto,fabricado,insumo"><label for="prodFormPrecioCompra">Precio de compra</label><input id="prodFormPrecioCompra" type="number" min="0" step="0.01"></div>
                        <div class="orden-field prod-stock-only" data-nat="producto,fabricado,insumo"><label for="prodFormProveedor">Proveedor</label><div style="display:flex;gap:4px;align-items:center;"><select id="prodFormProveedor" style="flex:1;"><option value="">Seleccionar...</option></select><button type="button" id="prodFormProveedorAdd" class="productos-btn" style="padding:4px 8px;font-size:0.7rem;white-space:nowrap;" title="Agregar proveedor" onclick="abrirPopupProveedorDesdeProductos()">+</button></div></div>
                    </div>
                </div>

                <!-- PASO: precios ─ Precios -->
                <div class="prod-step-panel" data-step="precios">
                    <div class="productos-modal-grid">
                        <div class="orden-field prod-stock-only" id="prodFormVentaWrap" data-nat="producto,fabricado,insumo,servicio"><label for="prodFormVenta">Precio unitario venta general</label><input id="prodFormVenta" type="number" min="0" step="0.01"></div>
                        <div class="orden-field prod-stock-only" data-nat="producto,fabricado"><label for="prodFormRevendedor">Precio unitario revendedor</label><input id="prodFormRevendedor" type="number" min="0" step="0.01"></div>
                        <div class="orden-field productos-field-span3 prod-stock-only" data-nat="producto,fabricado">
                            <label style="margin-bottom:2px;">Variantes del producto</label>
                            <div style="display:flex;align-items:center;gap:6px;">
                                <button type="button" id="prodFormVariantesBtn" class="productos-btn" style="padding:6px 14px;font-size:0.62rem;">⚙ Variantes</button>
                                <span id="prodFormVariantesResumen" style="font-size:0.55rem;color:#9ca3af;flex:1;">Sin variantes configuradas</span>
                            </div>
                            <div id="prodFormVariantesPreview" style="margin-top:4px;"></div>
                        </div>
                    </div>
                </div>

                <!-- PASO: config ─ Procesos / Fabricación / Insumos -->
                <div class="prod-step-panel" data-step="config">
                    <div class="productos-modal-grid">
                        <div class="orden-field productos-field-span3 prod-stock-only" data-nat="producto,fabricado"><label style="margin-bottom:2px;">⚙️ Procesos asignados</label><div style="display:flex;align-items:center;gap:6px;"><button type="button" id="prodFormProcesosBtn" class="productos-btn" style="padding:6px 14px;font-size:0.62rem;background:#f07a00;color:#fff;border:none;border-radius:6px;">⚙️ Seleccionar procesos</button><span id="prodFormProcesosResumen" style="font-size:0.55rem;color:#9ca3af;flex:1;">Sin procesos asignados</span></div><div id="prodFormProcesosPreview" style="margin-top:4px;font-size:0.6rem;"></div></div>
                        <div class="orden-field productos-field-span3" data-nat="fabricado"><label style="margin-bottom:2px;">🧪 Receta de fabricación</label><div style="display:flex;align-items:center;gap:6px;"><button type="button" id="prodFormRecetaBtn" class="productos-btn" style="padding:6px 14px;font-size:0.62rem;background:#f07a00;color:#fff;border:none;border-radius:6px;">🧪 Configurar receta</button><span id="prodFormRecetaResumen" style="font-size:0.55rem;color:#9ca3af;flex:1;">Sin insumos en la receta</span></div><div id="prodFormRecetaPreview" style="margin-top:4px;max-height:45px;overflow-y:auto;font-size:0.6rem;"></div></div>
                        <div class="orden-field productos-field-span3" data-nat="proceso"><label style="margin-bottom:2px;">🧰 Insumos del proceso</label><div style="display:flex;align-items:center;gap:6px;"><button type="button" id="prodFormProcesoInsumosBtn" class="productos-btn" style="padding:6px 14px;font-size:0.62rem;background:#f07a00;color:#fff;border:none;border-radius:6px;">🧰 Enlazar insumos</button><span id="prodFormProcesoInsumosResumen" style="font-size:0.55rem;color:#9ca3af;flex:1;">Sin insumos enlazados</span></div><div id="prodFormProcesoInsumosPreview" style="margin-top:4px;font-size:0.6rem;"></div></div>
                    </div>
                </div>

                <!-- PASO: empaque ─ Empaque y Envío -->
                <div class="prod-step-panel" data-step="empaque">
                    <div class="productos-modal-grid">
                        <div class="orden-field productos-field-span3" data-nat="producto,fabricado,insumo">
                            <label style="font-size:0.62rem;font-weight:900;color:#ff9900;letter-spacing:0.5px;margin-bottom:4px;display:block;">📦 MEDIDAS Y PESO DEL PAQUETE (para cotizar envíos)</label>
                            <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr 1fr;gap:4px;">
                                <div class="orden-field"><label for="prodFormPkgLargo">Largo (cm)</label><input id="prodFormPkgLargo" type="number" min="0" step="0.1" value="0" placeholder="cm"></div>
                                <div class="orden-field"><label for="prodFormPkgAncho">Ancho (cm)</label><input id="prodFormPkgAncho" type="number" min="0" step="0.1" value="0" placeholder="cm"></div>
                                <div class="orden-field"><label for="prodFormPkgAlto">Alto (cm)</label><input id="prodFormPkgAlto" type="number" min="0" step="0.1" value="0" placeholder="cm"></div>
                                <div class="orden-field"><label for="prodFormPkgPeso">Peso (kg)</label><input id="prodFormPkgPeso" type="number" min="0" step="0.01" value="0" placeholder="kg"></div>
                                <div class="orden-field"><label>Vol. (cm³)</label><input id="prodFormPkgVol" type="text" readonly style="background:#f3f4f6;opacity:0.8;" value="0"></div>
                            </div>
                            <div id="prodFormPkgVolInfo" style="font-size:0.5rem;color:#9ca3af;margin-top:2px;font-style:italic;">Peso volumétrico: 0 kg (÷5000)</div>
                        </div>
                    </div>
                </div>

                <!-- PASO: muestrario ─ Muestrario -->
                <div class="prod-step-panel" data-step="muestrario">
                    <div class="productos-modal-grid">
                        <div class="orden-field productos-field-span3" data-nat="producto,fabricado"><label for="prodFormMuestrarioAsociado">📁 Muestrario asociado</label><select id="prodFormMuestrarioAsociado"><option value="">Sin muestrario</option><option value="BOLSA BOUTIQUE TROQUELADA">BOLSA BOUTIQUE TROQUELADA</option><option value="BOLSAS KRAFT">BOLSAS KRAFT</option><option value="BOLSAS KRAFT BLANCAS">BOLSAS KRAFT BLANCAS</option><option value="TARJETAS DE PRESENTACIÓN">TARJETAS DE PRESENTACIÓN</option><option value="VOLANTES">VOLANTES</option></select></div>
                        <div class="orden-field" data-nat="producto,fabricado"><label for="prodFormRevisionesGratis">🔄 Revisiones gratis</label><input id="prodFormRevisionesGratis" type="number" min="0" max="20" value="2" step="1" placeholder="Ej: 2"></div>
                        <div class="orden-field" data-nat="producto,fabricado"><label for="prodFormCobroRevision">💰 Cobro extra por revisión</label><input id="prodFormCobroRevision" type="number" min="0" step="0.01" value="0" placeholder="Ej: 150.00"></div>
                        <div class="orden-field productos-field-span3" data-nat="producto,fabricado"><label style="display:flex;align-items:center;gap:6px;cursor:pointer;"><input type="checkbox" id="prodFormImprimirDiseno"> Permitir imprimir diseño en producción</label></div>
                    </div>
                </div>

                <!-- PASO: precios-gf ─ Precios Gran Formato -->
                <div class="prod-step-panel" data-step="precios-gf">
                    <div class="productos-modal-grid">
                        <div class="orden-field">
                            <label for="prodGfCobroTipo">Tipo de precio</label>
                            <select id="prodGfCobroTipo">
                                <option value="m2">Cobrar por metro cuadrado (M2)</option>
                                <option value="m-lineal">Cobrar por metro lineal (M/lineal)</option>
                            </select>
                        </div>
                        <div class="orden-field prod-gf-m2-only"><label for="prodGfPrecioGeneralM2">Precio de venta por M2</label><input id="prodGfPrecioGeneralM2" type="number" min="0" step="0.01"></div>
                        <div class="orden-field prod-gf-m2-only"><label for="prodGfPrecioRevM2">Precio de venta por M2 revendedor</label><input id="prodGfPrecioRevM2" type="number" min="0" step="0.01"></div>
                        <div class="orden-field prod-gf-ml-only"><label for="prodGfPrecioGeneralML">Precio de venta por M/lineal</label><input id="prodGfPrecioGeneralML" type="number" min="0" step="0.01"></div>
                        <div class="orden-field prod-gf-ml-only"><label for="prodGfPrecioRevML">Precio de venta por M/lineal revendedor</label><input id="prodGfPrecioRevML" type="number" min="0" step="0.01"></div>
                        <div class="orden-field prod-gf-m2-only"><label for="prodGfCostoM2">Costo por M2</label><input id="prodGfCostoM2" type="number" min="0" step="0.01"></div>
                        <div class="orden-field prod-gf-ml-only"><label for="prodGfCostoML">Costo por M/lineal</label><input id="prodGfCostoML" type="number" min="0" step="0.01"></div>
                        <div class="orden-field productos-field-span3">
                            <label for="prodGfAjusteAncho">Ajuste del precio al ancho del vinil</label>
                            <select id="prodGfAjusteAncho">
                                <option value="metro">Ajustar al metro</option>
                                <option value="medio">Ajustar a medio metro</option>
                                <option value="sin">Sin ajuste</option>
                            </select>
                        </div>
                    </div>
                </div>

            </div><!-- fin prod-form-main -->
        </div><!-- fin prod-form-wizard -->
        <div class="productos-modal-actions">
            <button id="prodFormAnterior" class="productos-btn gray" type="button" style="display:none;">← Anterior</button>
            <button id="prodFormSiguiente" class="productos-btn primary" type="button">Siguiente →</button>
            <button id="prodFormCerrar" class="productos-btn gray" type="button">Cerrar</button>
        </div>
    </div>
</div>'''

content = content[:idx_start] + NEW_HTML + content[idx_end:]
print(f'[1] HTML reemplazado. Longitud: {len(content)} (delta: {len(content)-original_len:+})')

# ─────────────────────────────────────────────────────────────
# 2. AGREGAR CSS wizard después de .prod-form-main { ... }
# ─────────────────────────────────────────────────────────────
CSS_ANCHOR = '''        .prod-form-main {
            min-width: 0;
            min-height: 0;
            display: flex;
            flex-direction: column;
            gap: 1px;
            overflow: hidden;
            flex: 1 1 0;
        }'''

CSS_NEW = '''        .prod-form-main {
            min-width: 0;
            min-height: 0;
            display: flex;
            flex-direction: column;
            gap: 1px;
            overflow: hidden;
            flex: 1 1 0;
        }

        /* ── Wizard de producto ── */
        .prod-wizard-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 5px 10px;
            background: linear-gradient(90deg,#1e293b,#334155);
            border-radius: 6px 6px 0 0;
            border-bottom: 2px solid #f07a00;
            flex-shrink: 0;
        }
        .prod-wizard-title {
            font-size: 0.68rem;
            font-weight: 900;
            color: #fff;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }
        .prod-wizard-count {
            font-size: 0.56rem;
            font-weight: 700;
            color: #f07a00;
            border: 1px solid rgba(240,122,0,0.5);
            border-radius: 10px;
            padding: 1px 8px;
            background: rgba(240,122,0,0.08);
        }
        .prod-step-panel {
            display: none;
            flex-direction: column;
            overflow-y: auto;
            flex: 1 1 0;
            min-height: 0;
            padding: 8px 10px;
            background: #fff;
            border-radius: 0 0 6px 6px;
        }
        .prod-step-panel.active { display: flex; }
        .prod-step-nav {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        .prod-step-navbtn {
            display: flex;
            align-items: center;
            gap: 5px;
            padding: 5px 7px;
            border: none;
            border-radius: 5px;
            background: rgba(255,255,255,0.08);
            color: rgba(255,255,255,0.7);
            font-size: 0.56rem;
            font-weight: 700;
            cursor: default;
            text-align: left;
            transition: background 0.15s;
            letter-spacing: 0.2px;
        }
        .prod-step-navbtn.active {
            background: rgba(240,122,0,0.85);
            color: #fff;
            cursor: pointer;
        }
        .prod-step-navbtn.done {
            background: rgba(34,197,94,0.2);
            color: #bbf7d0;
            cursor: pointer;
        }
        .prod-step-navbtn .step-icon { font-size: 0.7rem; }'''

if CSS_ANCHOR in content:
    content = content.replace(CSS_ANCHOR, CSS_NEW, 1)
    print('[2] CSS de wizard agregado.')
else:
    print('WARN: no se encontró ancla CSS de prod-form-main')

# ─────────────────────────────────────────────────────────────
# 3. AGREGAR const prodFormAnterior + JS wizard
# ─────────────────────────────────────────────────────────────
JS_ANCHOR = '    const prodFormCerrar = document.getElementById(\'prodFormCerrar\');'

JS_NEW = '''\
    const prodFormCerrar = document.getElementById('prodFormCerrar');
    const prodFormAnterior = document.getElementById('prodFormAnterior');

    // ── Wizard de producto ──────────────────────────────────────
    const PROD_STEPS_MAP = {
        'producto':    [{id:'basico',icon:'📋',label:'Identificación'},{id:'stock-compra',icon:'📦',label:'Stock y Compra'},{id:'precios',icon:'💲',label:'Precios'},{id:'config',icon:'⚙️',label:'Procesos'},{id:'empaque',icon:'📫',label:'Empaque'},{id:'muestrario',icon:'🎨',label:'Muestrario'}],
        'gran-formato':[{id:'basico',icon:'📋',label:'Identificación'},{id:'precios-gf',icon:'💲',label:'Precios GF'}],
        'fabricado':   [{id:'basico',icon:'📋',label:'Identificación'},{id:'stock-compra',icon:'📦',label:'Stock y Compra'},{id:'precios',icon:'💲',label:'Precios'},{id:'config',icon:'🧪',label:'Fabricación'},{id:'empaque',icon:'📫',label:'Empaque'},{id:'muestrario',icon:'🎨',label:'Muestrario'}],
        'insumo':      [{id:'basico',icon:'📋',label:'Identificación'},{id:'stock-compra',icon:'📦',label:'Stock y Compra'},{id:'empaque',icon:'📫',label:'Empaque'}],
        'proceso':     [{id:'basico',icon:'📋',label:'Identificación'},{id:'config',icon:'🧰',label:'Insumos'}],
        'servicio':    [{id:'basico',icon:'📋',label:'Identificación'},{id:'precios',icon:'💲',label:'Precios'}]
    };
    const TIPO_TO_NAT = {'stock':'producto','gran-formato':'gran-formato','fabricado':'fabricado','insumo':'insumo','proceso':'proceso','servicio':'servicio'};

    let prodWizardCurrentStep = 0;

    const getProdWizardSteps = () => {
        const t = prodFormTipo?.value || 'stock';
        const mapKey = TIPO_TO_NAT[t] || 'producto';
        return PROD_STEPS_MAP[mapKey] || PROD_STEPS_MAP['producto'];
    };

    const renderProdStepNav = () => {
        const nav = document.getElementById('prodStepNav');
        if (!nav) return;
        const steps = getProdWizardSteps();
        nav.innerHTML = steps.map((s, i) => {
            let cls = 'prod-step-navbtn';
            if (i === prodWizardCurrentStep) cls += ' active';
            else if (i < prodWizardCurrentStep) cls += ' done';
            const clickable = i <= prodWizardCurrentStep;
            return `<button type="button" class="${cls}" data-step-idx="${i}" ${clickable ? '' : 'disabled'}>
                <span class="step-icon">${s.icon}</span>${s.label}
            </button>`;
        }).join('');
        nav.querySelectorAll('.prod-step-navbtn[data-step-idx]').forEach(btn => {
            const idx = Number(btn.dataset.stepIdx);
            if (idx < prodWizardCurrentStep) {
                btn.addEventListener('click', () => goToProdStep(idx));
            }
        });
    };

    const goToProdStep = (idx) => {
        const steps = getProdWizardSteps();
        if (idx < 0 || idx >= steps.length) return;
        prodWizardCurrentStep = idx;
        // show/hide panels
        document.querySelectorAll('.prod-step-panel').forEach(p => p.classList.remove('active'));
        const targetPanel = document.querySelector(`.prod-step-panel[data-step="${steps[idx].id}"]`);
        if (targetPanel) targetPanel.classList.add('active');
        // update header
        const titleEl = document.getElementById('prodWizardStepTitle');
        const countEl = document.getElementById('prodWizardStepCount');
        if (titleEl) titleEl.textContent = steps[idx].label;
        if (countEl) countEl.textContent = `Paso ${idx+1} de ${steps.length}`;
        // anterior button
        if (prodFormAnterior) prodFormAnterior.style.display = idx > 0 ? '' : 'none';
        // siguiente button label
        if (prodFormSiguiente) prodFormSiguiente.textContent = (idx === steps.length - 1) ? '✓ Guardar →' : 'Siguiente →';
        renderProdStepNav();
        // run naturaleza sync for visibility
        syncProdFormModeByTipo();
    };

    const validateProdCurrentStep = () => {
        const steps = getProdWizardSteps();
        const cur = steps[prodWizardCurrentStep];
        if (cur.id === 'basico') {
            const codigo = document.getElementById('prodFormCodigo');
            const nombre = document.getElementById('prodFormProducto');
            if (!codigo?.value.trim()) {
                codigo?.focus();
                alert('El código del producto es obligatorio.');
                return false;
            }
            if (!nombre?.value.trim()) {
                nombre?.focus();
                alert('El nombre del producto es obligatorio.');
                return false;
            }
        }
        return true;
    };

    const resetProdWizard = () => {
        prodWizardCurrentStep = 0;
        const steps = getProdWizardSteps();
        document.querySelectorAll('.prod-step-panel').forEach(p => p.classList.remove('active'));
        const firstPanel = document.querySelector(`.prod-step-panel[data-step="${steps[0].id}"]`);
        if (firstPanel) firstPanel.classList.add('active');
        const titleEl = document.getElementById('prodWizardStepTitle');
        const countEl = document.getElementById('prodWizardStepCount');
        if (titleEl) titleEl.textContent = steps[0].label;
        if (countEl) countEl.textContent = `Paso 1 de ${steps.length}`;
        if (prodFormAnterior) prodFormAnterior.style.display = 'none';
        if (prodFormSiguiente) prodFormSiguiente.textContent = steps.length === 1 ? '✓ Guardar →' : 'Siguiente →';
        renderProdStepNav();
    };
    // ───────────────────────────────────────────────────────────'''

if JS_ANCHOR in content:
    content = content.replace(JS_ANCHOR, JS_NEW, 1)
    print('[3] JS wizard agregado.')
else:
    print('WARN: no se encontró ancla JS prodFormCerrar')

# ─────────────────────────────────────────────────────────────
# 4. AGREGAR resetProdWizard al final de syncProdFormModeByTipo
# ─────────────────────────────────────────────────────────────
# The function ends with:
#         } else {
#             // PRODUCTO: muchos campos — dejar compacto
#             if (grid) { grid.style.alignContent = 'start'; }
#         }
#     };

SYNC_END_OLD = '''        } else {
            // PRODUCTO: muchos campos — dejar compacto
            if (grid) { grid.style.alignContent = 'start'; }
        }
    };'''

SYNC_END_NEW = '''        } else {
            // PRODUCTO: muchos campos — dejar compacto
            if (grid) { grid.style.alignContent = 'start'; }
        }

        // Actualizar wizard si existe
        if (typeof resetProdWizard === 'function') resetProdWizard();
    };'''

if SYNC_END_OLD in content:
    content = content.replace(SYNC_END_OLD, SYNC_END_NEW, 1)
    print('[4] syncProdFormModeByTipo actualizado.')
else:
    print('WARN: no se encontró fin de syncProdFormModeByTipo')

# ─────────────────────────────────────────────────────────────
# 5. REEMPLAZAR handler prodFormSiguiente
# ─────────────────────────────────────────────────────────────
SIG_OLD = '''    if (prodFormSiguiente) {
        prodFormSiguiente.addEventListener('click', () => {
            const payload = collectProductFormPayload();
            if (!payload) return;
            prodPendingPayload = payload;
            if (payload.tipo === 'gran-formato') {
                prodPendingTabuladorId = '';
                prodPendingTabuladorPrecios = [];
                commitPendingProduct();
                return;
            }
            if (!prodPendingTabuladorId) {
                loadTabuladores();
                prodPendingTabuladorId = payload.tabuladorId || tabuladoresData[0]?.id || '';
            }
            openProdTabuladorPopup();
        });
    }'''

SIG_NEW = '''    if (prodFormSiguiente) {
        prodFormSiguiente.addEventListener('click', () => {
            const steps = getProdWizardSteps();
            const isLast = (prodWizardCurrentStep === steps.length - 1);
            if (!isLast) {
                if (!validateProdCurrentStep()) return;
                goToProdStep(prodWizardCurrentStep + 1);
                return;
            }
            // Último paso → comportamiento original
            const payload = collectProductFormPayload();
            if (!payload) return;
            prodPendingPayload = payload;
            if (payload.tipo === 'gran-formato') {
                prodPendingTabuladorId = '';
                prodPendingTabuladorPrecios = [];
                commitPendingProduct();
                return;
            }
            if (!prodPendingTabuladorId) {
                loadTabuladores();
                prodPendingTabuladorId = payload.tabuladorId || tabuladoresData[0]?.id || '';
            }
            openProdTabuladorPopup();
        });
    }

    if (prodFormAnterior) {
        prodFormAnterior.addEventListener('click', () => {
            goToProdStep(prodWizardCurrentStep - 1);
        });
    }'''

if SIG_OLD in content:
    content = content.replace(SIG_OLD, SIG_NEW, 1)
    print('[5] Handler prodFormSiguiente / prodFormAnterior actualizados.')
else:
    print('WARN: no se encontró handler prodFormSiguiente original')

# ─────────────────────────────────────────────────────────────
# 6. Actualizar listener change de prodFormTipo (naturaleza sync eliminado - ya no es necesario pues
#    TIPO_TO_NAT es usado en getProdWizardSteps directamente basándose en tipo)
#    Solo aseguramos que el listener llame a syncProdFormModeByTipo que a su vez llama resetProdWizard
# ─────────────────────────────────────────────────────────────
# Already handled via syncProdFormModeByTipo → resetProdWizard chain
print('[6] No se necesita cambio adicional en listener tipo (resetProdWizard ya es llamado via sync).')

# ─────────────────────────────────────────────────────────────
# Guardar
# ─────────────────────────────────────────────────────────────
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

new_len = len(content)
print(f'\nArchivo guardado. Longitud original: {original_len}, nueva: {new_len} (delta: {new_len-original_len:+})')
print('Listo.')
