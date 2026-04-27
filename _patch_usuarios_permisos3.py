#!/usr/bin/env python3
"""
Patch seguridad usuarios:
1. Agrega "ACCESO DENEGADO" overlay HTML
2. Reemplaza applyRolePermissions() con tabla de permisos real por módulo
3. Refuerza abrirModuloPrincipal() con chequeo de permisos
4. Reemplaza checkSession/waitForFirebase con onAuthStateChanged (Firebase Auth real)
5. Elimina bypass via localStorage en ocultarInicioSistema
6. Agrega rol "productor" al select de creación de usuarios
"""

FILE = '/workspaces/vistas/mockup.html'
with open(FILE, 'r', encoding='utf-8') as f:
    c = f.read()

orig_len = len(c)
ok = []
fail = []

def patch(name, old, new, count=1):
    global c
    n = c.count(old)
    if n == 0:
        fail.append(f'FAIL [{name}]: not found')
        return False
    if count == 1 and n > 1:
        fail.append(f'FAIL [{name}]: found {n} times (expected 1)')
        return False
    c = c.replace(old, new, count)
    ok.append(f'OK [{name}]')
    return True

# ─────────────────────────────────────────────────────────────
# 1. AGREGAR ROL "productor" AL SELECT DE CREACIÓN DE USUARIOS
# ─────────────────────────────────────────────────────────────
patch('1-rol-productor',
    '''                            <select id="configUserRol" style="width:100%;box-sizing:border-box;">
                                <option value="vendedor">VENDEDOR</option>
                                <option value="disenador">DISENADOR</option>
                                <option value="repartidor">REPARTIDOR</option>
                                <option value="admin">ADMINistrador</option>
                            </select>''',
    '''                            <select id="configUserRol" style="width:100%;box-sizing:border-box;">
                                <option value="vendedor">VENDEDOR</option>
                                <option value="disenador">DISEÑADOR</option>
                                <option value="productor">PRODUCTOR</option>
                                <option value="repartidor">REPARTIDOR</option>
                                <option value="admin">ADMINISTRADOR</option>
                            </select>''')

# ─────────────────────────────────────────────────────────────
# 2. ELIMINAR BYPASS VÍA LOCALSTORAGE EN ocultarInicioSistema
#    (línea 9454 aprox - solo se muestra el inicio si Firebase confirmó sesión)
# ─────────────────────────────────────────────────────────────
patch('2-remove-localstorage-bypass',
    '        if (loginOv && localStorage.getItem(\'logged_user_email\')) loginOv.style.display = \'none\';',
    '        // loginOverlay se oculta únicamente via onAuthStateChanged (Firebase Auth real)')

# ─────────────────────────────────────────────────────────────
# 3. AGREGAR OVERLAY "ACCESO DENEGADO" HTML (después del loginOverlay)
# ─────────────────────────────────────────────────────────────
patch('3-acceso-denegado-html',
    '<div id="inicioSistema" class="inicio-sistema-overlay" aria-hidden="true">',
    '''<div id="accesoDenegadoOverlay" style="display:none;position:fixed;inset:0;z-index:999999;background:rgba(0,0,0,0.82);display:flex;align-items:center;justify-content:center;flex-direction:column;gap:0;" aria-modal="true" role="alertdialog">
  <div style="background:#fff;border-radius:16px;padding:36px 40px;max-width:420px;width:90%;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,0.4);">
    <div style="font-size:3rem;margin-bottom:12px;">🚫</div>
    <h2 style="margin:0 0 8px;font-size:1.1rem;color:#dc2626;font-weight:900;">ACCESO DENEGADO</h2>
    <p id="accesoDenegadoMsg" style="margin:0 0 20px;font-size:0.7rem;color:#6b7280;line-height:1.5;">No tienes permisos para acceder a este módulo.</p>
    <button id="accesoDenegadoVolverBtn" type="button" style="background:#ff9900;color:#fff;border:none;border-radius:8px;padding:10px 24px;font-size:0.7rem;font-weight:800;cursor:pointer;">← Volver al inicio</button>
  </div>
</div>
<div id="inicioSistema" class="inicio-sistema-overlay" aria-hidden="true">''')

# ─────────────────────────────────────────────────────────────
# 4. REEMPLAZAR applyRolePermissions() CON TABLA REAL DE PERMISOS
# ─────────────────────────────────────────────────────────────
OLD_APPLY = '''    // ===== PERMISOS POR ROL =====
    const applyRolePermissions = (role) => {
        const isAdmin = role === 'admin';
        const isVendedor = role === 'vendedor';
        const isDisenador = role === 'disenador';

        // Config button: visible for all roles (permissions enforced inside)
        const btnAjustes = document.getElementById('btnAjustesMain');
        if (btnAjustes) btnAjustes.style.display = '';

        // Caja module: admin and vendedor
        const cajaCards = document.querySelectorAll('.inicio-card');
        cajaCards.forEach(card => {
            const label = (card.textContent || '').trim().toLowerCase();
            if (label.includes('caja') || label.includes('reportes')) {
                card.style.opacity = (isAdmin || isVendedor) ? '1' : '0.4';
                card.style.pointerEvents = (isAdmin || isVendedor) ? '' : 'none';
            }
            if (label.includes('producción')) {
                card.style.opacity = '1';
                card.style.pointerEvents = '';
            }
        });

        // Discount button: only admin
        const descuentoBtn = document.getElementById('ordenBtnDescuento');
        if (descuentoBtn) {
            descuentoBtn.style.opacity = isAdmin ? '1' : '0.5';
            if (!isAdmin) {
                descuentoBtn.title = 'Solo administradores pueden aplicar descuentos';
            }
        }

        // Show logged user role badge (only if role differs from label context)
        const vendedorInput = document.getElementById('ordenVendedor');
        if (vendedorInput && vendedorInput.parentElement) {
            // Remove any existing badge to avoid duplicates
            const existingBadge = vendedorInput.parentElement.querySelector('.login-user-badge');
            if (existingBadge) existingBadge.remove();
            // Only show badge if role is NOT vendedor (since the label already says VENDEDOR)
            if (role !== 'vendedor') {
                const badge = document.createElement('span');
                badge.className = 'login-user-badge';
                const roleLabels = { admin: 'ADMIN', vendedor: 'VENDEDOR', disenador: 'DISENADOR' };
                badge.textContent = roleLabels[role] || role;
                vendedorInput.parentElement.appendChild(badge);
            }
        }

        // For disenador, also clean up badge in diseñador field
        const disenadorSelect = document.getElementById('ordenDisenador');
        if (disenadorSelect && disenadorSelect.parentElement) {
            const existingDisBadge = disenadorSelect.parentElement.querySelector('.login-user-badge');
            if (existingDisBadge) existingDisBadge.remove();
        }
    };'''

NEW_APPLY = '''    // ===== TABLA DE PERMISOS POR ROL Y MÓDULO =====
    // admin: todos | vendedor: ventas+clientes | disenador: diseño | productor: producción | repartidor: reparto
    const MODULE_PERMISSIONS = {
        'NUEVA ORDEN':          ['admin','vendedor'],
        'MIS PEDIDOS':          ['admin','vendedor','disenador','productor'],
        'DISENO':               ['admin','disenador','vendedor'],
        'DISEÑO':               ['admin','disenador','vendedor'],
        'PRODUCCION':           ['admin','productor'],
        'RECEPCION SUCURSAL':   ['admin','productor','repartidor'],
        'CONTROL REPARTIDORES': ['admin','repartidor'],
        'REPARTO APP MOVIL':    ['admin','repartidor'],
        'REPARTO TEMPORAL':     ['admin','repartidor','vendedor'],
        'REPARTO':              ['admin','repartidor','vendedor'],
        'ENTREGAS':             ['admin','repartidor','vendedor'],
        'PRODUCTOS':            ['admin','vendedor'],
        'DASHBOARD':            ['admin','vendedor'],
        'CAJA':                 ['admin','vendedor'],
        'MUESTRARIO':           ['admin','vendedor','disenador'],
        'CLIENTES':             ['admin','vendedor'],
        'PROVEEDORES':          ['admin','vendedor'],
        'REPORTES':             ['admin','vendedor'],
        'CALENDARIO':           ['admin','vendedor','disenador','productor'],
        'CONFIGURACIONES':      ['admin'],
        'ALMACEN PEDIDOS':      ['admin','productor','repartidor'],
    };

    const canAccessModule = (role, moduleName) => {
        if (!role) return false;
        const key = String(moduleName || '').trim().toUpperCase();
        const allowed = MODULE_PERMISSIONS[key];
        if (!allowed) return role === 'admin'; // módulos no listados: solo admin
        return allowed.includes(role);
    };

    const showAccesoDenegado = (moduleName) => {
        const overlay = document.getElementById('accesoDenegadoOverlay');
        const msg = document.getElementById('accesoDenegadoMsg');
        if (msg) msg.textContent = `No tienes permisos para acceder al módulo "${moduleName}". Contacta a un administrador.`;
        if (overlay) { overlay.style.display = 'flex'; }
        const btn = document.getElementById('accesoDenegadoVolverBtn');
        if (btn && !btn._adListener) {
            btn._adListener = true;
            btn.addEventListener('click', () => {
                if (overlay) overlay.style.display = 'none';
                const inicio = document.getElementById('inicioSistema');
                if (inicio) { inicio.style.display = 'flex'; inicio.setAttribute('aria-hidden','false'); }
            });
        }
    };

    window.canAccessModule = canAccessModule;
    window.showAccesoDenegado = showAccesoDenegado;

    // ===== PERMISOS POR ROL =====
    const applyRolePermissions = (role) => {
        const isAdmin = role === 'admin';

        // Descuento: solo admin
        const descuentoBtn = document.getElementById('ordenBtnDescuento');
        if (descuentoBtn) {
            descuentoBtn.style.opacity = isAdmin ? '1' : '0.5';
            if (!isAdmin) descuentoBtn.title = 'Solo administradores pueden aplicar descuentos';
        }

        // Mostrar/ocultar tarjetas del menú según rol
        document.querySelectorAll('.inicio-card').forEach(card => {
            const onclick = card.getAttribute('onclick') || '';
            const match = onclick.match(/abrirModuloPrincipal\(['"]([^'"]+)['"]\)/);
            if (!match) return;
            const modKey = match[1].trim().toUpperCase();
            const allowed = canAccessModule(role, modKey);
            card.style.opacity = allowed ? '1' : '0.35';
            card.style.pointerEvents = allowed ? '' : '';
            card.setAttribute('data-requires-perm', allowed ? '0' : '1');
            card.title = allowed ? '' : '🚫 Sin acceso — ' + (role || 'sin rol');
        });

        // Badge de rol
        const vendedorInput = document.getElementById('ordenVendedor');
        if (vendedorInput && vendedorInput.parentElement) {
            const existingBadge = vendedorInput.parentElement.querySelector('.login-user-badge');
            if (existingBadge) existingBadge.remove();
            if (role !== 'vendedor') {
                const badge = document.createElement('span');
                badge.className = 'login-user-badge';
                const roleLabels = { admin:'ADMIN', vendedor:'VENDEDOR', disenador:'DISEÑADOR', productor:'PRODUCTOR', repartidor:'REPARTIDOR' };
                badge.textContent = roleLabels[role] || role.toUpperCase();
                vendedorInput.parentElement.appendChild(badge);
            }
        }
        const disenadorSelect = document.getElementById('ordenDisenador');
        if (disenadorSelect && disenadorSelect.parentElement) {
            const b = disenadorSelect.parentElement.querySelector('.login-user-badge');
            if (b) b.remove();
        }

        // Config tab usuarios visibles solo para admin
        const tabUsuariosBtn = document.querySelector('.config-tab[data-tab="usuarios"]');
        if (tabUsuariosBtn) tabUsuariosBtn.style.display = isAdmin ? '' : 'none';
    };'''

patch('4-apply-role-permissions', OLD_APPLY, NEW_APPLY)

# ─────────────────────────────────────────────────────────────
# 5. REFORZAR abrirModuloPrincipal CON CHECK DE PERMISOS
# ─────────────────────────────────────────────────────────────
OLD_ABRIR = '''    function abrirModuloPrincipal(modulo) {
        const key = String(modulo || '').trim().toUpperCase();

        if (key === 'NUEVA ORDEN') {'''

NEW_ABRIR = '''    function abrirModuloPrincipal(modulo) {
        const key = String(modulo || '').trim().toUpperCase();

        // ── GUARDIA DE PERMISOS ──
        // Verificar que hay una sesión Firebase activa
        const _fbUser = (window._currentFirebaseUser !== undefined)
            ? window._currentFirebaseUser
            : null;
        const _role = localStorage.getItem('logged_user_role') || '';
        if (!_role) {
            // No hay sesión conocida — mostrar login
            const lo = document.getElementById('loginOverlay');
            if (lo) lo.style.display = 'flex';
            return;
        }
        if (!canAccessModule(_role, key)) {
            showAccesoDenegado(key);
            return;
        }

        if (key === 'NUEVA ORDEN') {'''

patch('5-guardia-permisos-abrirModulo', OLD_ABRIR, NEW_ABRIR)

# ─────────────────────────────────────────────────────────────
# 6. REEMPLAZAR checkSession / waitForFirebase CON onAuthStateChanged
# ─────────────────────────────────────────────────────────────
OLD_CHECK = '''    // Check session on load
    const checkSession = () => {
        const savedName = localStorage.getItem('logged_user_name');
        const savedEmail = localStorage.getItem('logged_user_email');
        if (savedName && savedEmail) {
            const role = localStorage.getItem('logged_user_role') || 'vendedor';
            completeLogin(savedName, role);
            // Reload user data from Firestore in background
            loadUsersFromFirestore().then(async () => {
                let sysUser = findUserByEmail(savedEmail);
                // Auto-register if not in Firestore yet
                if (!sysUser) {
                    try {
                        await saveUserToFirestore({ correo: savedEmail, nombre: savedName, rol: role });
                        await loadUsersFromFirestore();
                        sysUser = findUserByEmail(savedEmail);
                    } catch (_) {}
                }
                if (sysUser && sysUser.rol !== role) {
                    localStorage.setItem('logged_user_role', sysUser.rol);
                    applyRolePermissions(sysUser.rol);
                }
            }).catch(() => {});
        } else {
            if (loginOverlay) loginOverlay.style.display = 'flex';
        }
    };

    if (loginBtn) loginBtn.addEventListener('click', doLogin);
    if (loginPassword) loginPassword.addEventListener('keydown', (e) => { if (e.key === 'Enter') { e.preventDefault(); doLogin(); } });
    if (loginCorreo) loginCorreo.addEventListener('keydown', (e) => { if (e.key === 'Enter') { e.preventDefault(); loginPassword?.focus(); } });

    const waitForFirebase = () => {
        if (window.firebase) { checkSession(); }
        else { setTimeout(waitForFirebase, 100); }
    };
    if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', waitForFirebase); }
    else { waitForFirebase(); }'''

NEW_CHECK = '''    if (loginBtn) loginBtn.addEventListener('click', doLogin);
    if (loginPassword) loginPassword.addEventListener('keydown', (e) => { if (e.key === 'Enter') { e.preventDefault(); doLogin(); } });
    if (loginCorreo) loginCorreo.addEventListener('keydown', (e) => { if (e.key === 'Enter') { e.preventDefault(); loginPassword?.focus(); } });

    // ===== AUTH STATE LISTENER (Firebase Auth real — única fuente de verdad) =====
    // El sistema NO muestra nada hasta que Firebase confirme la sesión.
    // El inicio se bloquea completamente hasta que onAuthStateChanged dispare.
    window._currentFirebaseUser = undefined; // undefined = pendiente, null = no autenticado, object = autenticado

    const _blockingOverlay = (() => {
        // Pantalla de carga inicial mientras Firebase verifica sesión
        const el = document.createElement('div');
        el.id = 'authLoadingOverlay';
        el.style.cssText = 'position:fixed;inset:0;z-index:999998;background:#0f172a;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:12px;';
        el.innerHTML = '<div style="font-size:2.5rem;">🔐</div><div style="color:#fff;font-size:0.75rem;font-weight:700;letter-spacing:1px;">VERIFICANDO SESIÓN...</div><div style="width:40px;height:4px;background:#ff9900;border-radius:2px;animation:authPulse 1s ease-in-out infinite;"></div>';
        const style = document.createElement('style');
        style.textContent = '@keyframes authPulse{0%,100%{opacity:0.3;transform:scaleX(0.5)}50%{opacity:1;transform:scaleX(1)}}';
        document.head.appendChild(style);
        document.body.insertBefore(el, document.body.firstChild);
        return el;
    })();

    const _initAuthListener = () => {
        if (!window.firebase) { setTimeout(_initAuthListener, 100); return; }
        try {
            const authApp = getAuthApp();
            if (!authApp) { setTimeout(_initAuthListener, 150); return; }
            const auth = window.firebase.auth(authApp);

            auth.onAuthStateChanged(async (fbUser) => {
                window._currentFirebaseUser = fbUser;
                // Remove blocking overlay
                if (_blockingOverlay && _blockingOverlay.parentNode) _blockingOverlay.remove();

                if (!fbUser) {
                    // ── NO AUTENTICADO: limpiar sesión y mostrar login ──
                    localStorage.removeItem('logged_user_email');
                    localStorage.removeItem('logged_user_name');
                    localStorage.removeItem('logged_user_role');
                    sessionStorage.removeItem('_admin_temp_pass');
                    if (loginOverlay) loginOverlay.style.display = 'flex';
                    // Ocultar el sistema completamente
                    const inicio = document.getElementById('inicioSistema');
                    if (inicio) { inicio.style.display = 'none'; inicio.setAttribute('aria-hidden','true'); }
                    return;
                }

                // ── AUTENTICADO: cargar perfil desde Firestore ──
                try {
                    await loadUsersFromFirestore();
                    let sysUser = findUserByEmail(fbUser.email);

                    // Auto-registro si existe en Auth pero no en Firestore
                    if (!sysUser) {
                        try {
                            const autoName = fbUser.displayName || fbUser.email.split('@')[0];
                            await saveUserToFirestore({ correo: fbUser.email, nombre: autoName, rol: 'vendedor' });
                            await loadUsersFromFirestore();
                            sysUser = findUserByEmail(fbUser.email);
                        } catch (_) {}
                    }

                    // Verificar que el usuario está activo
                    if (sysUser && sysUser.activo === false) {
                        auth.signOut().catch(() => {});
                        if (loginOverlay) { loginOverlay.style.display = 'flex'; }
                        const errEl = document.getElementById('loginError');
                        if (errEl) errEl.textContent = 'Tu cuenta ha sido desactivada. Contacta al administrador.';
                        return;
                    }

                    const userName = sysUser?.nombre || fbUser.displayName || fbUser.email.split('@')[0];
                    const userRole = sysUser?.rol || 'vendedor';

                    localStorage.setItem('logged_user_email', fbUser.email);
                    localStorage.setItem('logged_user_name', userName);
                    localStorage.setItem('logged_user_role', userRole);

                    completeLogin(userName, userRole);
                } catch (err) {
                    console.error('Error cargando perfil de usuario:', err);
                    // Usar datos del token si Firestore falla
                    const fallbackName = fbUser.displayName || fbUser.email.split('@')[0];
                    const fallbackRole = localStorage.getItem('logged_user_role') || 'vendedor';
                    localStorage.setItem('logged_user_email', fbUser.email);
                    localStorage.setItem('logged_user_name', fallbackName);
                    completeLogin(fallbackName, fallbackRole);
                }
            });
        } catch (err) {
            console.error('Error iniciando auth listener:', err);
            // Fallback: mostrar login
            if (_blockingOverlay && _blockingOverlay.parentNode) _blockingOverlay.remove();
            if (loginOverlay) loginOverlay.style.display = 'flex';
        }
    };

    if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', _initAuthListener); }
    else { _initAuthListener(); }'''

patch('6-onAuthStateChanged', OLD_CHECK, NEW_CHECK)

# ─────────────────────────────────────────────────────────────
# 7. REFORZAR renderConfigUsersTable: mostrar rol "productor"
# ─────────────────────────────────────────────────────────────
patch('7-role-labels-productor',
    "                const roleLabel = u.rol === 'admin' ? 'Administrador' : u.rol === 'disenador' ? 'Diseñador' : 'Vendedor';",
    "                const roleLabel = {admin:'Administrador', disenador:'Diseñador', productor:'Productor', repartidor:'Repartidor', vendedor:'Vendedor'}[u.rol] || (u.rol||'Vendedor');")

# ─────────────────────────────────────────────────────────────
# 8. REFORZAR: en el change de rol des de tabla usuarios, agregar "productor"
# ─────────────────────────────────────────────────────────────
patch('8-rol-change-table',
    """                        <select class="config-user-rol-select" data-doc="${u.id}" ${canChangeRole ? '' : 'disabled'}>
                                <option value="vendedor"${u.rol==='vendedor'?' selected':''}>Vendedor</option>
                                <option value="disenador"${u.rol==='disenador'?' selected':''}>Diseñador</option>
                                <option value="admin"${u.rol==='admin'?' selected':''}>Admin</option>
                            </select>""",
    """                        <select class="config-user-rol-select" data-doc="${u.id}" ${canChangeRole ? '' : 'disabled'}>
                                <option value="vendedor"${u.rol==='vendedor'?' selected':''}>Vendedor</option>
                                <option value="disenador"${u.rol==='disenador'?' selected':''}>Diseñador</option>
                                <option value="productor"${u.rol==='productor'?' selected':''}>Productor</option>
                                <option value="repartidor"${u.rol==='repartidor'?' selected':''}>Repartidor</option>
                                <option value="admin"${u.rol==='admin'?' selected':''}>Admin</option>
                            </select>""")

# ─────────────────────────────────────────────────────────────
# GUARDAR
# ─────────────────────────────────────────────────────────────
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(c)

print('='*60)
print(f'Longitud: {orig_len} → {len(c)} (delta: {len(c)-orig_len:+d})')
for m in ok: print(' ', m)
for m in fail: print(' ', m)
if fail:
    print(f'\n⚠ PATCH CON {len(fail)} ADVERTENCIAS')
else:
    print(f'\n✅ PATCH COMPLETO — {len(ok)} cambios aplicados')
