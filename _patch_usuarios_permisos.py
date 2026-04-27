#!/usr/bin/env python3
"""
Patch: Usuarios y Permisos mejorado
- Rediseña #tabPermisos con matriz de toggles por rol/módulo
- Admin hardcode: axelbrayan166@gmail.com / 123456 (fallback local)
- Siembra admin en mock_usuarios_v1 para mpRequireAdmin
- Permisos guardan en localStorage y se aplican al iniciar sesión
"""
import re

FILENAME = 'mockup.html'

with open(FILENAME, 'r', encoding='utf-8') as f:
    html = f.read()

patches = []

# ─────────────────────────────────────────────────────────────────────────────
# PATCH 1: CSS — Añadir estilos de matriz de permisos
# ─────────────────────────────────────────────────────────────────────────────
OLD_CSS = '        #configUserCrearStatus { color: #6b7280 !important; }\n    </style>'
NEW_CSS = '''        #configUserCrearStatus { color: #6b7280 !important; }

        /* ===== PERMISOS MATRIX ===== */
        #tabPermisos .popup-panel { display: block !important; grid-template-columns: unset !important; background: transparent !important; padding: 0 !important; border: none !important; }
        .permisos-matrix { width: 100%; border-collapse: collapse; font-size: 0.52rem; }
        .permisos-matrix th { background: #f9fafb; padding: 9px 10px; font-weight: 800; color: #374151; text-align: center; border: 1px solid #e5e7eb; font-size: 0.5rem; text-transform: uppercase; letter-spacing: 0.3px; }
        .permisos-matrix th:first-child { text-align: left; min-width: 155px; background: #fff; }
        .permisos-matrix td { padding: 8px 10px; border: 1px solid #e5e7eb; text-align: center; vertical-align: middle; }
        .permisos-matrix td:first-child { text-align: left; font-weight: 600; color: #1f2937; font-size: 0.54rem; background: #fafafa; }
        .permisos-matrix tr:hover td { background: #fef7ed; }
        .permisos-matrix tr:hover td:first-child { background: #fef3c7; }
        /* Toggle switch */
        .perm-toggle { position: relative; display: inline-flex; align-items: center; cursor: pointer; }
        .perm-toggle input[type=checkbox] {
            width: 32px; height: 17px; appearance: none; -webkit-appearance: none;
            background: #d1d5db; border-radius: 9px; cursor: pointer; position: relative;
            transition: background 0.2s; outline: none; border: none;
        }
        .perm-toggle input[type=checkbox]:checked { background: #10b981; }
        .perm-toggle input[type=checkbox]::after {
            content: ''; position: absolute; width: 13px; height: 13px; background: #fff;
            border-radius: 50%; top: 2px; left: 2px; transition: left 0.2s;
            box-shadow: 0 1px 3px rgba(0,0,0,0.25);
        }
        .perm-toggle input[type=checkbox]:checked::after { left: 17px; }
        .perm-toggle input[type=checkbox]:disabled { opacity: 0.55; cursor: not-allowed; }
        .permisos-role-head { display: flex; flex-direction: column; align-items: center; gap: 4px; }
        .permisos-role-icon { font-size: 1rem; }
        .permisos-role-label { font-size: 0.48rem; font-weight: 800; letter-spacing: 0.3px; }
        .perm-role-admin    { color: #d97706; }
        .perm-role-vendedor { color: #1d4ed8; }
        .perm-role-disenador{ color: #7c3aed; }
        .perm-role-repartidor{ color: #15803d; }
        .perm-role-caja     { color: #db2777; }
        .permisos-save-bar { display: flex; gap: 10px; align-items: center; margin-top: 14px; padding-top: 12px; border-top: 1px solid #e5e7eb; }
    </style>'''

if OLD_CSS in html:
    html = html.replace(OLD_CSS, NEW_CSS, 1)
    patches.append('✅ P1 CSS permisos matrix')
else:
    patches.append('❌ P1 CSS NOT FOUND')

# ─────────────────────────────────────────────────────────────────────────────
# PATCH 2: HTML — Reemplazar #tabPermisos con matriz interactiva
# ─────────────────────────────────────────────────────────────────────────────
OLD_TAB_PERMISOS = '''            <!-- TAB: PERMISOS -->
            <div class="config-tab-panel" id="tabPermisos" data-tab="permisos">
                <h3>Permisos de usuarios</h3>
                <div class="popup-panel">
                    <div class="orden-field" style="grid-column: 1 / -1;">
                        <label for="configPermisosDescuentoUsuarios">Usuarios autorizados a aplicar descuentos (uno por línea)</label>
                        <textarea id="configPermisosDescuentoUsuarios" rows="8" placeholder="juan.perez&#10;caja1&#10;admin"></textarea>
                    </div>
                </div>
            </div>'''

NEW_TAB_PERMISOS = '''            <!-- TAB: PERMISOS -->
            <div class="config-tab-panel" id="tabPermisos" data-tab="permisos">
                <h3>Permisos por rol</h3>
                <div class="popup-panel">
                    <p style="font-size:0.52rem;color:#6b7280;margin:0 0 12px;">Define qué módulos puede acceder cada rol. El <strong>Admin</strong> siempre tiene acceso total y no puede modificarse.</p>
                    <div style="overflow-x:auto;">
                        <table class="permisos-matrix" id="permisosMatrizTable">
                            <thead>
                                <tr>
                                    <th>Módulo / Función</th>
                                    <th>
                                        <div class="permisos-role-head">
                                            <span class="permisos-role-icon">👑</span>
                                            <span class="permisos-role-label perm-role-admin">Admin</span>
                                        </div>
                                    </th>
                                    <th>
                                        <div class="permisos-role-head">
                                            <span class="permisos-role-icon">💼</span>
                                            <span class="permisos-role-label perm-role-vendedor">Vendedor</span>
                                        </div>
                                    </th>
                                    <th>
                                        <div class="permisos-role-head">
                                            <span class="permisos-role-icon">🎨</span>
                                            <span class="permisos-role-label perm-role-disenador">Diseñador</span>
                                        </div>
                                    </th>
                                    <th>
                                        <div class="permisos-role-head">
                                            <span class="permisos-role-icon">💰</span>
                                            <span class="permisos-role-label perm-role-caja">Caja</span>
                                        </div>
                                    </th>
                                    <th>
                                        <div class="permisos-role-head">
                                            <span class="permisos-role-icon">🚚</span>
                                            <span class="permisos-role-label perm-role-repartidor">Repartidor</span>
                                        </div>
                                    </th>
                                </tr>
                            </thead>
                            <tbody id="permisosMatrizBody">
                                <!-- Generado por JS -->
                                <tr><td colspan="6" style="text-align:center;color:#9ca3af;padding:16px;">Cargando permisos...</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="permisos-save-bar">
                        <button id="permisosGuardarBtn" class="productos-btn primary" type="button" style="padding:8px 20px;font-size:0.58rem;font-weight:800;background:#ff9900;border:none;color:#fff;border-radius:8px;cursor:pointer;">💾 GUARDAR PERMISOS</button>
                        <button id="permisosResetBtn" class="productos-btn" type="button" style="padding:8px 14px;font-size:0.55rem;background:#f3f4f6;border:1px solid #d1d5db;color:#374151;border-radius:8px;cursor:pointer;">↩ Restaurar predeterminados</button>
                        <span id="permisosStatus" style="font-size:0.52rem;color:#6b7280;margin-left:4px;"></span>
                    </div>
                </div>
            </div>'''

if OLD_TAB_PERMISOS in html:
    html = html.replace(OLD_TAB_PERMISOS, NEW_TAB_PERMISOS, 1)
    patches.append('✅ P2 #tabPermisos rediseñado')
else:
    patches.append('❌ P2 #tabPermisos NOT FOUND')

# ─────────────────────────────────────────────────────────────────────────────
# PATCH 3: JS LOGIN — Agregar fallback local ANTES del bloque Firebase
# ─────────────────────────────────────────────────────────────────────────────
OLD_LOGIN_TRY = '''        try {
            const app = getAuthApp();
            if (!app) throw new Error('Firebase no disponible.');
            const auth = window.firebase.auth(app);
            const cred = await auth.signInWithEmailAndPassword(email, pass);'''

NEW_LOGIN_TRY = '''        // ── Fallback local (sin Firebase) ──────────────────────
        const _LOCAL_ADMINS = [
            { email: 'axelbrayan166@gmail.com', password: '123456', nombre: 'Administrador', rol: 'admin' }
        ];
        const _localMatch = _LOCAL_ADMINS.find(u =>
            u.email.toLowerCase() === email.toLowerCase() && u.password === pass
        );
        if (_localMatch) {
            // Sembrar en mock_usuarios_v1 para mpRequireAdmin
            try {
                let _lu = JSON.parse(localStorage.getItem('mock_usuarios_v1') || '[]');
                if (!_lu.find(u => (u.email || u.correo || '').toLowerCase() === _localMatch.email.toLowerCase())) {
                    _lu.unshift({ id: 'admin-local-1', nombre: _localMatch.nombre, email: _localMatch.email, correo: _localMatch.email, password: _localMatch.password, rol: _localMatch.rol });
                    localStorage.setItem('mock_usuarios_v1', JSON.stringify(_lu));
                }
            } catch(_le) {}
            localStorage.setItem('logged_user_email', _localMatch.email);
            localStorage.setItem('logged_user_name', _localMatch.nombre);
            localStorage.setItem('logged_user_role', _localMatch.rol);
            sessionStorage.setItem('_admin_temp_pass', pass);
            loginBtn.disabled = false;
            loginBtn.textContent = 'INGRESAR';
            completeLogin(_localMatch.nombre, _localMatch.rol);
            return;
        }
        // ────────────────────────────────────────────────────────
        try {
            const app = getAuthApp();
            if (!app) throw new Error('Firebase no disponible.');
            const auth = window.firebase.auth(app);
            const cred = await auth.signInWithEmailAndPassword(email, pass);'''

if OLD_LOGIN_TRY in html:
    html = html.replace(OLD_LOGIN_TRY, NEW_LOGIN_TRY, 1)
    patches.append('✅ P3 Login fallback local')
else:
    patches.append('❌ P3 Login fallback NOT FOUND')

# ─────────────────────────────────────────────────────────────────────────────
# PATCH 4: JS — Sembrar admin en mock_usuarios_v1 al inicio (DOMContentLoaded)
# Añadimos un bloque de inicialización antes del cierre </body>
# ─────────────────────────────────────────────────────────────────────────────
OLD_BODY_END = '</body>\n</html>'
NEW_BODY_END = '''<script>
// ===== INIT: Sembrar usuario admin local en mock_usuarios_v1 =====
(function() {
    try {
        var _ADMIN_SEED = { id: 'admin-local-1', nombre: 'Administrador', email: 'axelbrayan166@gmail.com', correo: 'axelbrayan166@gmail.com', password: '123456', rol: 'admin' };
        var _lu = [];
        try { _lu = JSON.parse(localStorage.getItem('mock_usuarios_v1') || '[]'); } catch(_) {}
        var _exists = _lu.find(function(u) { return (u.email || u.correo || '').toLowerCase() === _ADMIN_SEED.email; });
        if (!_exists) {
            _lu.unshift(_ADMIN_SEED);
            localStorage.setItem('mock_usuarios_v1', JSON.stringify(_lu));
        }
    } catch(_ie) {}
})();

// ===== PERMISSIONS SYSTEM =====
(function() {
    var PERMISOS_KEY = 'mock_permisos_v1';
    var ROLES = ['admin', 'vendedor', 'disenador', 'caja', 'repartidor'];
    var MODULOS = [
        { id: 'pedidos',       label: '🛒 Pedidos / Mis Pedidos',      text: ['pedidos', 'mis pedidos', 'orden'] },
        { id: 'caja',          label: '💰 Caja',                        text: ['caja'] },
        { id: 'clientes',      label: '👥 Clientes',                    text: ['clientes'] },
        { id: 'productos',     label: '📦 Productos e Insumos',         text: ['productos', 'insumos'] },
        { id: 'reportes',      label: '📊 Reportes',                    text: ['reportes'] },
        { id: 'configuracion', label: '⚙️ Configuración del sistema',   text: ['configur', 'ajustes'] },
        { id: 'descuentos',    label: '💸 Aplicar Descuentos',          text: [] },
        { id: 'cotizaciones',  label: '📋 Cotizaciones',                text: ['cotizaci'] },
        { id: 'reparto',       label: '🚚 Reparto / Entregas',          text: ['reparto', 'entrega'] },
        { id: 'diseno',        label: '🎨 Diseño / Tracking',           text: ['diseño', 'diseno', 'tracking'] },
        { id: 'almacen',       label: '🏪 Almacén Físico',              text: ['almac'] },
        { id: 'calendario',    label: '📅 Calendario de Producción',    text: ['calendario', 'produccion', 'producción'] },
    ];

    var DEFAULT_PERMISOS = {
        admin:      { pedidos:true, caja:true, clientes:true, productos:true, reportes:true, configuracion:true, descuentos:true, cotizaciones:true, reparto:true, diseno:true, almacen:true, calendario:true },
        vendedor:   { pedidos:true, caja:true, clientes:true, productos:false, reportes:true, configuracion:false, descuentos:false, cotizaciones:true, reparto:false, diseno:false, almacen:false, calendario:true },
        disenador:  { pedidos:false, caja:false, clientes:false, productos:true, reportes:false, configuracion:false, descuentos:false, cotizaciones:false, reparto:false, diseno:true, almacen:true, calendario:true },
        caja:       { pedidos:true, caja:true, clientes:true, productos:false, reportes:true, configuracion:false, descuentos:false, cotizaciones:false, reparto:false, diseno:false, almacen:false, calendario:false },
        repartidor: { pedidos:false, caja:false, clientes:false, productos:false, reportes:false, configuracion:false, descuentos:false, cotizaciones:false, reparto:true, diseno:false, almacen:false, calendario:false },
    };

    function loadPermisos() {
        try { var s = localStorage.getItem(PERMISOS_KEY); return s ? JSON.parse(s) : null; } catch(_) { return null; }
    }
    function savePermisos(data) {
        try { localStorage.setItem(PERMISOS_KEY, JSON.stringify(data)); } catch(_) {}
    }
    function getPermisos() {
        var saved = loadPermisos();
        var merged = {};
        for (var r = 0; r < ROLES.length; r++) {
            var rol = ROLES[r];
            merged[rol] = Object.assign({}, DEFAULT_PERMISOS[rol] || {}, saved ? (saved[rol] || {}) : {});
        }
        return merged;
    }

    function renderPermisosMatrix() {
        var tbody = document.getElementById('permisosMatrizBody');
        if (!tbody) return;
        var permisos = getPermisos();
        var html = '';
        for (var m = 0; m < MODULOS.length; m++) {
            var mod = MODULOS[m];
            html += '<tr><td>' + mod.label + '</td>';
            for (var r = 0; r < ROLES.length; r++) {
                var rol = ROLES[r];
                var checked = permisos[rol] && permisos[rol][mod.id] !== false ? 'checked' : '';
                var disabled = rol === 'admin' ? 'disabled' : '';
                html += '<td><label class="perm-toggle"><input type="checkbox" data-rol="' + rol + '" data-modulo="' + mod.id + '" ' + checked + ' ' + disabled + '></label></td>';
            }
            html += '</tr>';
        }
        tbody.innerHTML = html;
    }

    function applyPermisosConfig(role) {
        var permisos = getPermisos();
        var rolePerms = permisos[role] || DEFAULT_PERMISOS[role] || DEFAULT_PERMISOS.vendedor;
        var isAdmin = role === 'admin';
        if (isAdmin) return; // admin: no restrictions

        // Show/hide inicio cards based on permissions
        var cards = document.querySelectorAll('.inicio-card');
        cards.forEach(function(card) {
            var txt = (card.textContent || '').trim().toLowerCase();
            for (var m = 0; m < MODULOS.length; m++) {
                var mod = MODULOS[m];
                if (!mod.text || !mod.text.length) continue;
                var match = mod.text.some(function(kw) { return txt.includes(kw); });
                if (match) {
                    var allowed = rolePerms[mod.id] !== false;
                    card.style.opacity = allowed ? '' : '0.35';
                    card.style.pointerEvents = allowed ? '' : 'none';
                    break;
                }
            }
        });

        // Discount button
        var descBtn = document.getElementById('ordenBtnDescuento');
        if (descBtn) {
            var descAllowed = rolePerms['descuentos'] !== false;
            descBtn.style.opacity = descAllowed ? '1' : '0.4';
            descBtn.title = descAllowed ? '' : 'Sin permiso para aplicar descuentos';
        }

        // Config button
        var cfgBtn = document.getElementById('btnAjustesMain');
        if (cfgBtn) {
            var cfgAllowed = rolePerms['configuracion'] !== false;
            cfgBtn.style.opacity = cfgAllowed ? '' : '0.4';
            cfgBtn.style.pointerEvents = cfgAllowed ? '' : 'none';
            cfgBtn.title = cfgAllowed ? '' : 'Sin permiso para configuración';
        }
    }

    // Expose globally
    window._permisosSystem = {
        getPermisos: getPermisos,
        savePermisos: savePermisos,
        renderMatrix: renderPermisosMatrix,
        applyConfig: applyPermisosConfig
    };

    document.addEventListener('DOMContentLoaded', function() {
        // Render matrix when permisos tab is opened
        document.querySelectorAll('.config-tab').forEach(function(tab) {
            tab.addEventListener('click', function() {
                if (tab.dataset.tab === 'permisos') {
                    setTimeout(renderPermisosMatrix, 40);
                }
            });
        });

        // Save button
        var saveBtn = document.getElementById('permisosGuardarBtn');
        if (saveBtn) {
            saveBtn.addEventListener('click', function() {
                var newPermisos = {};
                ROLES.forEach(function(rol) { newPermisos[rol] = {}; });
                document.querySelectorAll('#permisosMatrizBody input[type=checkbox]').forEach(function(cb) {
                    var rol = cb.dataset.rol, mod = cb.dataset.modulo;
                    if (rol && mod) newPermisos[rol][mod] = cb.checked;
                });
                // Admin always has all perms
                MODULOS.forEach(function(m) { newPermisos['admin'][m.id] = true; });
                savePermisos(newPermisos);
                // Re-apply to current user
                var curRole = (localStorage.getItem('logged_user_role') || 'vendedor').toLowerCase();
                applyPermisosConfig(curRole);
                var status = document.getElementById('permisosStatus');
                if (status) {
                    status.textContent = '✅ Permisos guardados correctamente.';
                    status.style.color = '#10b981';
                    setTimeout(function() { status.textContent = ''; }, 3000);
                }
            });
        }

        // Reset button
        var resetBtn = document.getElementById('permisosResetBtn');
        if (resetBtn) {
            resetBtn.addEventListener('click', function() {
                if (!confirm('¿Restaurar permisos a los valores predeterminados para todos los roles?')) return;
                savePermisos(JSON.parse(JSON.stringify(DEFAULT_PERMISOS)));
                renderPermisosMatrix();
                var curRole = (localStorage.getItem('logged_user_role') || 'vendedor').toLowerCase();
                applyPermisosConfig(curRole);
                var status = document.getElementById('permisosStatus');
                if (status) {
                    status.textContent = '↩ Permisos restaurados.';
                    status.style.color = '#6b7280';
                    setTimeout(function() { status.textContent = ''; }, 3000);
                }
            });
        }

        // Apply saved permissions for currently logged user on page load
        var curRole = (localStorage.getItem('logged_user_role') || '').toLowerCase();
        if (curRole) { applyPermisosConfig(curRole); }
    });
})();
</script>
</body>
</html>'''

if OLD_BODY_END in html:
    html = html.replace(OLD_BODY_END, NEW_BODY_END, 1)
    patches.append('✅ P4 JS permisos + init admin seed')
else:
    patches.append('❌ P4 </body> NOT FOUND')

# ─────────────────────────────────────────────────────────────────────────────
# Guardar
# ─────────────────────────────────────────────────────────────────────────────
with open(FILENAME, 'w', encoding='utf-8') as f:
    f.write(html)

print('\n'.join(patches))
print('\nDone.')
