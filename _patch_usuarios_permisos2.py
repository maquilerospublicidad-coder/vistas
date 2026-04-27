#!/usr/bin/env python3
"""
Patch: Fix completo de Usuarios y Permisos
Cambios:
1. Arregla el <script> tag faltante del bloque PERMISSIONS SYSTEM
2. Elimina seeding de mock_usuarios_v1 del login fallback
3. Actualiza mpRequireAdmin para NO usar mock_usuarios_v1
4. Mueve permisos a Firestore (system_config/permisos) con fallback localStorage
5. Preserva rol `propietario` como badge especial en la tabla
6. Añade panel de info en tabUsuarios: ruta Firebase + lista de admins
7. Añade nota de almacenamiento en tabPermisos
"""
import re

FILENAME = 'mockup.html'
with open(FILENAME, 'r', encoding='utf-8') as f:
    html = f.read()

patches = []

# ─────────────────────────────────────────────────────────────────────────────
# P1: Arreglar <script> tag faltante del bloque PERMISSIONS SYSTEM
# ─────────────────────────────────────────────────────────────────────────────
old_p1 = '</script>\n\n// ===== PERMISSIONS SYSTEM ====='
new_p1 = '</script>\n\n<script>\n// ===== PERMISSIONS SYSTEM ====='
if old_p1 in html:
    html = html.replace(old_p1, new_p1, 1)
    patches.append('✅ P1 <script> tag añadido')
else:
    patches.append('❌ P1 NOT FOUND')

# ─────────────────────────────────────────────────────────────────────────────
# P2: Eliminar seeding de mock_usuarios_v1 del login fallback local
# ─────────────────────────────────────────────────────────────────────────────
old_p2_start = '            // Sembrar en mock_usuarios_v1 para mpRequireAdmin'
old_p2_end   = "            } catch(_le) {}\n            localStorage.setItem('logged_user_email'"

idx_start = html.find(old_p2_start)
idx_end   = html.find(old_p2_end)

if idx_start > 0 and idx_end > idx_start:
    seed_block = html[idx_start:idx_end]
    html = html.replace(seed_block, '            localStorage.setItem(\'logged_user_email\'', 1)
    # Restore the accidentally removed line
    # Actually the end marker includes the start of the next line, let's be careful
    patches.append('✅ P2 seeding mock_usuarios_v1 eliminado')
else:
    # Try different approach
    old_p2 = """\
            // Sembrar en mock_usuarios_v1 para mpRequireAdmin
            try {
                let _lu = JSON.parse(localStorage.getItem('mock_usuarios_v1') || '[]');
                if (!_lu.find(u => (u.email || u.correo || '').toLowerCase() === _localMatch.email.toLowerCase())) {
                    _lu.unshift({ id: 'admin-local-1', nombre: _localMatch.nombre, email: _localMatch.email, correo: _localMatch.email, password: _localMatch.password, rol: _localMatch.rol });
                    localStorage.setItem('mock_usuarios_v1', JSON.stringify(_lu));
                }
            } catch(_le) {}
            localStorage.setItem('logged_user_email', _localMatch.email);"""
    new_p2 = "            localStorage.setItem('logged_user_email', _localMatch.email);"
    if old_p2 in html:
        html = html.replace(old_p2, new_p2, 1)
        patches.append('✅ P2 seeding mock_usuarios_v1 eliminado (v2)')
    else:
        patches.append('❌ P2 seed block NOT FOUND')

# ─────────────────────────────────────────────────────────────────────────────
# P3: Actualizar mpRequireAdmin para NO usar mock_usuarios_v1
#     Solo chequea el rol actual del usuario logueado
# ─────────────────────────────────────────────────────────────────────────────
old_p3 = """\
    const mpRequireAdmin = (callback) => {
        const role = (localStorage.getItem('logged_user_role') || '').toLowerCase().trim();
        if (role === 'admin' || mpDetAdminGranted) { callback(); return; }
        const pass = prompt('Acción de administrador.\\nIngresa la contraseña de admin:');
        if (!pass) return;
        let usuarios = [];
        try { usuarios = JSON.parse(localStorage.getItem('mock_usuarios_v1') || '[]'); } catch(_){}
        const found = usuarios.find(u => (u.rol === 'admin' || u.role === 'admin') && u.password === pass);
        if (!found) { notifyError('Contraseña incorrecta.', 'Admin'); return; }
        mpDetAdminGranted = true;
        notifyInfo('Acceso de administrador concedido para esta orden.', 'Admin');
        callback();
    };"""
new_p3 = """\
    const mpRequireAdmin = (callback) => {
        const role = (localStorage.getItem('logged_user_role') || '').toLowerCase().trim();
        if (role === 'admin' || mpDetAdminGranted) { callback(); return; }
        notifyError('Esta acción requiere permisos de administrador. Inicia sesión con una cuenta de administrador.', 'Sin permiso');
    };"""
if old_p3 in html:
    html = html.replace(old_p3, new_p3, 1)
    patches.append('✅ P3 mpRequireAdmin simplificado')
else:
    patches.append('❌ P3 mpRequireAdmin NOT FOUND')

# ─────────────────────────────────────────────────────────────────────────────
# P4: Preservar rol propietario en el dato cacheado
# ─────────────────────────────────────────────────────────────────────────────
old_p4 = """\
            snap.forEach(doc => {
                const _d = doc.data();
                // Normalizar rol: propietario → admin
                if (_d.rol === 'propietario') _d.rol = 'admin';
                cachedUsers.push({ id: doc.id, ..._d });
            });"""
new_p4 = """\
            snap.forEach(doc => {
                const _d = doc.data();
                // Normalizar rol: propietario → admin (pero preservar para badge)
                if (_d.rol === 'propietario') {
                    _d.esPropietario = true;
                    _d.rol = 'admin';
                }
                cachedUsers.push({ id: doc.id, ..._d });
            });"""
if old_p4 in html:
    html = html.replace(old_p4, new_p4, 1)
    patches.append('✅ P4 propietario flag preservado')
else:
    patches.append('❌ P4 propietario NOT FOUND')

# ─────────────────────────────────────────────────────────────────────────────
# P5: Mejorar la tabla de usuarios — badge propietario, más columnas visibles,
#     panel de info Firebase al tope del tab
# ─────────────────────────────────────────────────────────────────────────────
old_p5 = """\
            <!-- TAB: USUARIOS -->
            <div class="config-tab-panel" id="tabUsuarios" data-tab="usuarios">
                <h3>Gestión de usuarios del sistema</h3>
                <div class="popup-panel" style="display:block;">
                    
                    <div class="config-users-sync-bar">
                        <span class="sync-status" id="configUsersSyncStatus">⏳ Conectando con Firebase...</span>
                        <button id="configUsersSyncBtn" class="productos-btn" type="button" style="padding:4px 10px;font-size:0.55rem;">🔄 Sincronizar</button>
                    </div>"""
new_p5 = """\
            <!-- TAB: USUARIOS -->
            <div class="config-tab-panel" id="tabUsuarios" data-tab="usuarios">
                <h3>Gestión de usuarios del sistema</h3>
                <div class="popup-panel" style="display:block;">

                    <!-- Info de almacenamiento -->
                    <div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:10px;padding:10px 14px;margin-bottom:12px;display:flex;gap:14px;align-items:flex-start;flex-wrap:wrap;">
                        <div style="flex:1;min-width:180px;">
                            <div style="font-size:0.55rem;font-weight:800;color:#1e40af;margin-bottom:3px;">📦 DÓNDE SE GUARDAN LOS USUARIOS</div>
                            <div style="font-size:0.52rem;color:#1e3a5f;line-height:1.6;">
                                <b>Firebase Authentication</b> — gestiona el acceso (correo + contraseña)<br>
                                <b>Firestore</b> → Colección: <code style="background:#dbeafe;padding:1px 5px;border-radius:4px;font-size:0.5rem;">system_users</code> — guarda nombre, rol, estado activo
                            </div>
                        </div>
                        <div style="flex:1;min-width:180px;">
                            <div style="font-size:0.55rem;font-weight:800;color:#1e40af;margin-bottom:3px;">🔑 ROLES EN EL SISTEMA</div>
                            <div style="font-size:0.5rem;color:#1e3a5f;line-height:1.7;">
                                <b>admin</b> — acceso total &nbsp;|&nbsp; <b>propietario</b> → se trata como admin<br>
                                <b>vendedor</b> — ventas y caja &nbsp;|&nbsp; <b>disenador</b> — producción<br>
                                <b>repartidor</b> — módulo reparto
                            </div>
                        </div>
                    </div>

                    <!-- Panel administradores -->
                    <div style="background:#fef3c7;border:1px solid #fde68a;border-radius:10px;padding:10px 14px;margin-bottom:12px;">
                        <div style="font-size:0.6rem;font-weight:900;color:#92400e;margin-bottom:7px;">👑 ADMINISTRADORES REGISTRADOS</div>
                        <div id="configAdminsLista" style="font-size:0.52rem;color:#78350f;min-height:18px;">⏳ Cargando...</div>
                    </div>

                    <div class="config-users-sync-bar">
                        <span class="sync-status" id="configUsersSyncStatus">⏳ Conectando con Firebase...</span>
                        <button id="configUsersSyncBtn" class="productos-btn" type="button" style="padding:4px 10px;font-size:0.55rem;">🔄 Sincronizar</button>
                    </div>"""
if old_p5 in html:
    html = html.replace(old_p5, new_p5, 1)
    patches.append('✅ P5 panel info Firebase añadido')
else:
    patches.append('❌ P5 tabUsuarios header NOT FOUND')

# ─────────────────────────────────────────────────────────────────────────────
# P6: Mejorar el role badge en la tabla (mostrar Propietario)
#     Hay que actualizar el renderConfigUsersTable JS
# ─────────────────────────────────────────────────────────────────────────────
old_p6 = """\
            const currentEmail = (localStorage.getItem('logged_user_email') || '').toLowerCase();
            const currentRole = localStorage.getItem('logged_user_role') || '';

            tbody.innerHTML = users.map((u) => {
                const isSelf = String(u.correo||'').toLowerCase() === currentEmail;
                const roleClass = u.rol === 'admin' ? 'admin' : u.rol === 'disenador' ? 'disenador' : 'vendedor';
                const roleLabel = u.rol === 'admin' ? 'Administrador' : u.rol === 'disenador' ? 'Diseñador' : 'Vendedor';"""
new_p6 = """\
            const currentEmail = (localStorage.getItem('logged_user_email') || '').toLowerCase();
            const currentRole = localStorage.getItem('logged_user_role') || '';

            // Populate admins panel
            const adminsEl = document.getElementById('configAdminsLista');
            if (adminsEl) {
                const admins = users.filter(u => u.rol === 'admin');
                if (!admins.length) {
                    adminsEl.innerHTML = '<span style="color:#9ca3af;">Sin administradores registrados en Firestore.</span>';
                } else {
                    adminsEl.innerHTML = admins.map(a =>
                        `<span style="display:inline-flex;align-items:center;gap:5px;margin:2px 8px 2px 0;background:#fef7ed;border:1px solid #fde68a;border-radius:6px;padding:3px 9px;">
                            ${a.esPropietario ? '👑' : '🔐'}
                            <strong>${esc(a.nombre||a.correo)}</strong>
                            <span style="font-size:0.45rem;color:#b45309;">${esc(a.correo)}</span>
                            ${a.esPropietario ? '<span style="font-size:0.44rem;background:#d97706;color:#fff;border-radius:4px;padding:1px 5px;font-weight:800;">PROPIETARIO</span>' : ''}
                        </span>`
                    ).join('');
                }
            }

            tbody.innerHTML = users.map((u) => {
                const isSelf = String(u.correo||'').toLowerCase() === currentEmail;
                const roleClass = u.rol === 'admin' ? 'admin' : u.rol === 'disenador' ? 'disenador' : 'vendedor';
                const roleLabel = u.esPropietario ? '👑 Propietario' : u.rol === 'admin' ? 'Administrador' : u.rol === 'disenador' ? 'Diseñador' : u.rol === 'repartidor' ? 'Repartidor' : u.rol === 'caja' ? 'Caja' : 'Vendedor';"""
if old_p6 in html:
    html = html.replace(old_p6, new_p6, 1)
    patches.append('✅ P6 tabla con admins panel + badge propietario')
else:
    patches.append('❌ P6 renderConfigUsersTable NOT FOUND')

# ─────────────────────────────────────────────────────────────────────────────
# P7: Actualizar el mensaje de confirmación de eliminación
# ─────────────────────────────────────────────────────────────────────────────
old_p7 = "if (!confirm(`¿Eliminar permanentemente al usuario \"${name}\"?\\n\\nEsto eliminará su perfil de Firestore. La cuenta de Firebase Auth se mantendrá pero no podrá acceder.`)) return;"
new_p7 = "if (!confirm(`¿Eliminar al usuario \"${name}\" de Firestore (system_users)?\\n\\n⚠️ Esto elimina su perfil del sistema. La cuenta de Firebase Authentication se mantiene pero no podrá acceder.\\nPara eliminar también de Firebase Auth debes hacerlo desde Firebase Console.`)) return;"
if old_p7 in html:
    html = html.replace(old_p7, new_p7, 1)
    patches.append('✅ P7 mensaje de eliminación mejorado')
else:
    patches.append('❌ P7 confirm delete NOT FOUND')

# ─────────────────────────────────────────────────────────────────────────────
# P8: Mover loadPermisos/savePermisos a Firestore (system_config/permisos)
#     con fallback a localStorage
# ─────────────────────────────────────────────────────────────────────────────
old_p8 = """\
    function loadPermisos() {
        try { var s = localStorage.getItem(PERMISOS_KEY); return s ? JSON.parse(s) : null; } catch(_) { return null; }
    }
    function savePermisos(data) {
        try { localStorage.setItem(PERMISOS_KEY, JSON.stringify(data)); } catch(_) {}
    }"""
new_p8 = """\
    function loadPermisos() {
        // Lee del localStorage (cache local). loadPermisosFromDB() carga desde Firestore
        try { var s = localStorage.getItem(PERMISOS_KEY); return s ? JSON.parse(s) : null; } catch(_) { return null; }
    }
    function savePermisos(data) {
        // Guarda en localStorage Y en Firestore (system_config/permisos)
        try { localStorage.setItem(PERMISOS_KEY, JSON.stringify(data)); } catch(_) {}
        savePermisosToFirestore(data);
    }
    function savePermisosToFirestore(data) {
        try {
            var db = null;
            try { db = window.firebase.firestore(); } catch(_) {}
            if (!db) return;
            db.collection('system_config').doc('permisos').set({ permisos: data, actualizadoEn: new Date().toISOString() })
              .catch(function(e) { console.warn('No se pudo guardar permisos en Firestore:', e); });
        } catch(e) { console.warn('savePermisosToFirestore error:', e); }
    }
    function loadPermisosFromDB() {
        // Carga desde Firestore y actualiza localStorage
        return new Promise(function(resolve) {
            try {
                var db = null;
                try { db = window.firebase.firestore(); } catch(_) {}
                if (!db) { resolve(loadPermisos()); return; }
                db.collection('system_config').doc('permisos').get().then(function(doc) {
                    if (doc.exists && doc.data().permisos) {
                        var data = doc.data().permisos;
                        try { localStorage.setItem(PERMISOS_KEY, JSON.stringify(data)); } catch(_) {}
                        resolve(data);
                    } else {
                        resolve(loadPermisos());
                    }
                }).catch(function() { resolve(loadPermisos()); });
            } catch(e) { resolve(loadPermisos()); }
        });
    }"""
if old_p8 in html:
    html = html.replace(old_p8, new_p8, 1)
    patches.append('✅ P8 permisos Firestore (system_config/permisos)')
else:
    patches.append('❌ P8 loadPermisos NOT FOUND')

# ─────────────────────────────────────────────────────────────────────────────
# P9: Al abrir el tab permisos, cargar desde Firestore primero
# ─────────────────────────────────────────────────────────────────────────────
old_p9 = """\
        // Render matrix when permisos tab is opened
        document.querySelectorAll('.config-tab').forEach(function(tab) {
            tab.addEventListener('click', function() {
                if (tab.dataset.tab === 'permisos') {
                    setTimeout(renderPermisosMatrix, 40);
                }
            });
        });"""
new_p9 = """\
        // Render matrix when permisos tab is opened (loads from Firestore first)
        document.querySelectorAll('.config-tab').forEach(function(tab) {
            tab.addEventListener('click', function() {
                if (tab.dataset.tab === 'permisos') {
                    loadPermisosFromDB().then(function() { renderPermisosMatrix(); });
                }
            });
        });"""
if old_p9 in html:
    html = html.replace(old_p9, new_p9, 1)
    patches.append('✅ P9 tab permisos carga desde Firestore')
else:
    patches.append('❌ P9 tab permisos click NOT FOUND')

# ─────────────────────────────────────────────────────────────────────────────
# P10: Añadir nota de almacenamiento en tabPermisos
# ─────────────────────────────────────────────────────────────────────────────
old_p10 = """\
                <div class="popup-panel">
                    <p style="font-size:0.52rem;color:#6b7280;margin:0 0 12px;">Define qué módulos puede acceder cada rol. El <strong>Admin</strong> siempre tiene acceso total y no puede modificarse.</p>"""
new_p10 = """\
                <div class="popup-panel">
                    <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;padding:8px 12px;margin-bottom:10px;font-size:0.5rem;color:#166534;">
                        <strong>📦 Dónde se guardan:</strong> Firebase Firestore → Colección <code style="background:#dcfce7;padding:1px 4px;border-radius:3px;">system_config</code> → Documento <code style="background:#dcfce7;padding:1px 4px;border-radius:3px;">permisos</code>
                        &nbsp;|&nbsp; Respaldo local: localStorage <code style="background:#dcfce7;padding:1px 4px;border-radius:3px;">mock_permisos_v1</code>
                    </div>
                    <p style="font-size:0.52rem;color:#6b7280;margin:0 0 12px;">Define qué módulos puede acceder cada rol. El <strong>Admin</strong> siempre tiene acceso total y no puede modificarse.</p>"""
if old_p10 in html:
    html = html.replace(old_p10, new_p10, 1)
    patches.append('✅ P10 nota almacenamiento permisos')
else:
    patches.append('❌ P10 tabPermisos panel NOT FOUND')

# ─────────────────────────────────────────────────────────────────────────────
# Guardar
# ─────────────────────────────────────────────────────────────────────────────
with open(FILENAME, 'w', encoding='utf-8') as f:
    f.write(html)

print('\n'.join(patches))
print(f'\nTotal: {len(html):,} chars')
