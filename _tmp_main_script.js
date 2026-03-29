document.addEventListener('DOMContentLoaded', () => {
    const FIREBASE_WEB_CONFIG = {
        apiKey: "AIzaSyAr8-ybVqcaeubCs-bApA_FAKnDgj9S7vM",
        authDomain: "maquilero-8344b.firebaseapp.com",
        projectId: "maquilero-8344b",
        storageBucket: "maquilero-8344b.firebasestorage.app",
        messagingSenderId: "323366654858",
        appId: "1:323366654858:web:5527744db419863da6ee73",
        measurementId: "G-H26F2MCQWD"
    };
    const FIREBASE_UPLOAD_COLLECTION = 'design_uploads';
    const ENABLE_FIREBASE_DIRECT_UPLOAD = false;
    const CAN_USE_FIREBASE_DIRECT_UPLOAD = (() => {
        const proto = String(window.location?.protocol || '').toLowerCase();
        const origin = String(window.location?.origin || '').toLowerCase();
        if (proto === 'file:') return false;
        if (!origin || origin === 'null') return false;
        return proto === 'http:' || proto === 'https:';
    })();

    const productos = [
        {
            nombre: 'Bolsa Boutique Troquelada',
            modulo: 'BOLSA BOUTIQUE TROQUELADA',
            colores: ['Rojo', 'Naranja', 'Amarillo', 'Verde', 'Celeste', 'Azul', 'Morado', 'Lila', 'Fucsia', 'Rosa', 'Blanco', 'Negro', 'Gris Claro', 'Beige', 'Gris'],
            medidas: ['MINI', 'CHICA', 'MEDIANA', 'GRANDE'],
            extras: []
        },
        {
            nombre: 'Bolsas Kraft',
            modulo: 'BOLSAS KRAFT',
            colores: ['Kraft Natural', 'Kraft Claro', 'Kraft Oscuro', 'Blanco', 'Negro'],
            medidas: ['MINI', 'CHICA', 'MEDIANA', 'GRANDE'],
            extras: []
        },
        {
            nombre: 'Tarjetas de presentación',
            modulo: 'TARJETAS DE PRESENTACIÓN',
            colores: [],
            medidas: ['9x5 cm'],
            extras: ['Tipo: Estandar', 'Tipo: Laminada']
        },
        {
            nombre: 'Volantes',
            modulo: 'VOLANTES',
            colores: [],
            medidas: ['1/4 carta', 'Media carta', 'Carta'],
            extras: ['Impresión: 4X0', 'Impresión: 4X1', 'Impresión: 4X4']
        }
    ];

    const normalize = (str = '') => str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();

    const colorHex = (name) => {
        const mapa = {
            'Rojo': '#e53935', 'Naranja': '#fb8c00', 'Amarillo': '#fdd835', 'Verde': '#43a047', 'Celeste': '#4fc3f7', 'Azul': '#1e88e5', 'Morado': '#8e24aa', 'Lila': '#ba68c8', 'Fucsia': '#e91e63', 'Rosa': '#f8bbd0', 'Blanco': '#f5f5f5', 'Negro': '#111111', 'Gris Claro': '#e0e0e0', 'Beige': '#d7ccc8', 'Gris': '#9e9e9e',
            'Kraft Natural': '#C9A46B', 'Kraft Claro': '#D9C09A', 'Kraft Oscuro': '#9C7443',
            'Tarjeta Blanco': '#ffffff', 'Tarjeta Negro': '#0f0f0f'
        };
        return mapa[name] || '#e0e0e0';
    };

    const medidaTexto = (med) => {
        const map = {
            'MINI': '20x22 cm',
            'CHICA': '28x35 cm',
            'MEDIANA': '35x41 cm',
            'GRANDE': '50x50 cm',
            '9x5 cm': '9x5 cm',
            'STD 9x5 cm (horizontal)': '9x5 cm',
            'VERT 5x9 cm (vertical)': '5x9 cm',
            'PREMIUM 8.5x5.5 cm': '8.5x5.5 cm',
            'VOLANTE 10.5x14 cm': '10.5x14 cm',
            '10.5x14 cm': '10.5x14 cm',
            '1/4 CARTA': '10.5x14 cm',
            'MEDIA CARTA': '14x21.5 cm',
            'CARTA': '21.5x28 cm'
        };
        return map[med] || med;
    };

    const getDefaultDateTimeLocal = () => {
        const now = new Date();
        const local = new Date(now.getTime() - now.getTimezoneOffset() * 60000);
        return local.toISOString().slice(0, 16);
    };

    const URGENCIA_META = {
        'muy-urgente': { peso: 4, label: 'Muy urgente' },
        urgente: { peso: 3, label: 'Urgente' },
        normal: { peso: 2, label: 'Normal' },
        baja: { peso: 1, label: 'Poco urgente' }
    };

    const formatDateTime = (iso) => {
        if (!iso) return '';
        const dt = new Date(iso);
        if (Number.isNaN(dt.getTime())) return iso;
        return dt.toLocaleString('es-MX', {
            year: 'numeric', month: '2-digit', day: '2-digit',
            hour: '2-digit', minute: '2-digit'
        });
    };

    let ordenLineas = [];
    let ordenLineaActiva = -1;
    let ordenTaxRate = 0;
    let ordenDiscount = 0;
    let ordenDiscountAmount = 0;
    let ordenDiscountLabel = '';
    let ordenInversion = 0;
    let ordenStockSearchTerm = '';
    let ordenStockPriceMode = 'general';
    let ordenStockSelectedId = '';
    let ordenStockQty = 1;
    let ordenPickerTipo = 'stock';
    let ordenTickets = [];
    let ordenTicketActivo = 0;
    let ordenAnticipo = 0;
    let ordenPagoDetalle = null;

    window.cotizadorActivo = window.cotizadorActivo || null;

    const btnListadoRapido = document.getElementById('btnListadoRapido');
    const popupListado = document.getElementById('popupListado');
    const btnOrdenBackMenu = document.getElementById('ordenBackMenu');
    const ordenStockPopup = document.getElementById('ordenStockPopup');
    const ordenStockSearch = document.getElementById('ordenStockSearch');
    const ordenStockTableBody = document.getElementById('ordenStockTableBody');
    const ordenStockResultCount = document.getElementById('ordenStockResultCount');
    const ordenStockTabuladorBtn = document.getElementById('ordenStockTabuladorBtn');
    const ordenStockPriceGeneral = document.getElementById('ordenStockPriceGeneral');
    const ordenStockPriceRevendedor = document.getElementById('ordenStockPriceRevendedor');
    const ordenStockPhoto = document.getElementById('ordenStockPhoto');
    const ordenStockColorsList = document.getElementById('ordenStockColorsList');
    const ordenStockExistencias = document.getElementById('ordenStockExistencias');
    const ordenStockPrecio = document.getElementById('ordenStockPrecio');
    const ordenStockCosto = document.getElementById('ordenStockCosto');
    const ordenStockGanancia = document.getElementById('ordenStockGanancia');
    const ordenStockQtyPopup = document.getElementById('ordenStockQtyPopup');
    const ordenStockQtyInput = document.getElementById('ordenStockQtyInput');
    const ordenStockTotal = document.getElementById('ordenStockTotal');
    const ordenStockAccept = document.getElementById('ordenStockAccept');
    const ordenStockClose = document.getElementById('ordenStockClose');
    const btnCerrarPopupListado = document.getElementById('cerrarPopupListado');
    const ordenTicketTabs = document.getElementById('ordenTicketTabs');
    const ordenBtnVentaRapida = document.getElementById('ordenBtnVentaRapida');
    const ordenPagoPopup = document.getElementById('ordenPagoPopup');
    const ordenPagoTitulo = document.getElementById('ordenPagoTitulo');
    const ordenPagoBody = document.getElementById('ordenPagoBody');
    const ordenPagoCancelar = document.getElementById('ordenPagoCancelar');
    const ordenPagoAceptar = document.getElementById('ordenPagoAceptar');
    const ordenConfirmPopup = document.getElementById('ordenConfirmPopup');
    const ordenConfirmMensaje = document.getElementById('ordenConfirmMensaje');
    const ordenConfirmCancelar = document.getElementById('ordenConfirmCancelar');
    const ordenConfirmAceptar = document.getElementById('ordenConfirmAceptar');
    const ordenVentaRapidaPopup = document.getElementById('ordenVentaRapidaPopup');
    const ordenVrNombre = document.getElementById('ordenVrNombre');
    const ordenVrMonto = document.getElementById('ordenVrMonto');
    const ordenVrCancelar = document.getElementById('ordenVrCancelar');
    const ordenVrAgregar = document.getElementById('ordenVrAgregar');
    const ordenDescuentoPopup = document.getElementById('ordenDescuentoPopup');
    const ordenDescuentoCodigo = document.getElementById('ordenDescuentoCodigo');
    const ordenDescuentoPorcentaje = document.getElementById('ordenDescuentoPorcentaje');
    const ordenDescuentoMonto = document.getElementById('ordenDescuentoMonto');
    const ordenDescuentoCancelar = document.getElementById('ordenDescuentoCancelar');
    const ordenDescuentoLimpiar = document.getElementById('ordenDescuentoLimpiar');
    const ordenDescuentoAplicar = document.getElementById('ordenDescuentoAplicar');
    const ordenClienteSelectPopup = document.getElementById('ordenClienteSelectPopup');
    const ordenClienteSelectSearch = document.getElementById('ordenClienteSelectSearch');
    const ordenClienteSelectTableBody = document.getElementById('ordenClienteSelectTableBody');
    const ordenClienteSelectCount = document.getElementById('ordenClienteSelectCount');
    const ordenClienteSelectCancel = document.getElementById('ordenClienteSelectCancel');
    const ordenClienteSelectAccept = document.getElementById('ordenClienteSelectAccept');
    const btnAccessData = document.getElementById('btnAccessData');
    const btnSeguimientoDiseno = document.getElementById('btnSeguimientoDiseno');
    const popupAccess = document.getElementById('popupAccess');
    const btnAccessClose = document.getElementById('btnAccessClose');
    const btnAccessRefresh = document.getElementById('btnAccessRefresh');
    const btnAccessLoad = document.getElementById('btnAccessLoad');
    const accessTableSelect = document.getElementById('accessTableSelect');
    const accessLimitInput = document.getElementById('accessLimitInput');
    const accessStatus = document.getElementById('accessStatus');
    const accessTableWrap = document.getElementById('accessTableWrap');
    const popupDesignTracking = document.getElementById('popupDesignTracking');
    const btnDesignClose = document.getElementById('btnDesignClose');
    const btnDesignRefresh = document.getElementById('btnDesignRefresh');
    const btnDesignUpload = document.getElementById('btnDesignUpload');
    const designLimitInput = document.getElementById('designLimitInput');
    const designStatus = document.getElementById('designStatus');
    const designTableWrap = document.getElementById('designTableWrap');
    const designSelectedOrder = document.getElementById('designSelectedOrder');
    const designFileFront = document.getElementById('designFileFront');
    const designFileBack = document.getElementById('designFileBack');
    const popupNotify = document.getElementById('popupNotify');
    const notifyTitle = document.getElementById('notifyTitle');
    const notifyMessage = document.getElementById('notifyMessage');
    const notifyOk = document.getElementById('notifyOk');
    
    // Referencias para Fondo de Caja
    const popupFondoCaja = document.getElementById('popupFondoCaja');
    const fondoCajaInputMonto = document.getElementById('fondoCajaInputMonto');
    const fondoCajaAceptar = document.getElementById('fondoCajaAceptar');
    const fondoCajaCancelar = document.getElementById('fondoCajaCancelar');
    
    // Referencias para Configuraciones
    const popupConfiguraciones = document.getElementById('popupConfiguraciones');
    const configBack = document.getElementById('configBack');
    const configGuardar = document.getElementById('configGuardar');
    const configCerrar = document.getElementById('configCerrar');
    
    // Caja
    const configCajaNombre = document.getElementById('configCajaNombre');
    const configCajaId = document.getElementById('configCajaId');
    const configCajaMoneda = document.getElementById('configCajaMoneda');
    const configCajaCorteAutomatico = document.getElementById('configCajaCorteAutomatico');
    const configCajaBancoReceptor = document.getElementById('configCajaBancoReceptor');
    const configCajaCuentasBeneficiario = document.getElementById('configCajaCuentasBeneficiario');
    const configCajaDisenadores = document.getElementById('configCajaDisenadores');
    const configCajaFondoMinimo = document.getElementById('configCajaFondoMinimo');
    const configCajaFuentePredeterminada = document.getElementById('configCajaFuentePredeterminada');
    const configCajaMetodoEfectivo = document.getElementById('configCajaMetodoEfectivo');
    const configCajaMetodoTarjeta = document.getElementById('configCajaMetodoTarjeta');
    const configCajaMetodoTransferencia = document.getElementById('configCajaMetodoTransferencia');
    const configCajaMetodoDeposito = document.getElementById('configCajaMetodoDeposito');
    const configCajaPermitirIngresoManual = document.getElementById('configCajaPermitirIngresoManual');
    const configCajaPermitirGastos = document.getElementById('configCajaPermitirGastos');
    
    // Clientes
    const configClientesCategoriaPorDefecto = document.getElementById('configClientesCategoriaPorDefecto');
    const configClientesCreditoMaximo = document.getElementById('configClientesCreditoMaximo');
    const configClientesAlertaBajaExistencia = document.getElementById('configClientesAlertaBajaExistencia');
    const configClientesAceptarOrdenesSinCliente = document.getElementById('configClientesAceptarOrdenesSinCliente');
    
    // Productos
    const configProductosUnidadPorDefecto = document.getElementById('configProductosUnidadPorDefecto');
    const configProductosMargenPorDefecto = document.getElementById('configProductosMargenPorDefecto');
    const configProductosAlertaBajaExistencia = document.getElementById('configProductosAlertaBajaExistencia');
    const configProductosActualizarPreciosAutomatico = document.getElementById('configProductosActualizarPreciosAutomatico');
    
    // Proveedores
    const configProveedoresDiasCredito = document.getElementById('configProveedoresDiasCredito');
    const configProveedoresMonedaPorDefecto = document.getElementById('configProveedoresMonedaPorDefecto');
    const configProveedoresAlertaSaldoPendiente = document.getElementById('configProveedoresAlertaSaldoPendiente');
    const configProveedoresAceptarSinEntre = document.getElementById('configProveedoresAceptarSinEntre');
    
    // Insumos
    const configInsumosUnidadPorDefecto = document.getElementById('configInsumosUnidadPorDefecto');
    const configInsumosStockMinimoAlerta = document.getElementById('configInsumosStockMinimoAlerta');
    const configInsumosAceptarComprasConStock = document.getElementById('configInsumosAceptarComprasConStock');
    const configInsumosMostrarCostoProduccion = document.getElementById('configInsumosMostrarCostoProduccion');
    
    // Almacén
    const configAlmacenUbicacionPorDefecto = document.getElementById('configAlmacenUbicacionPorDefecto');
    const configAlmacenStockMinimoAlerta = document.getElementById('configAlmacenStockMinimoAlerta');
    const configAlmacenAceptarStockNegativo = document.getElementById('configAlmacenAceptarStockNegativo');
    const configAlmacenOverstockAlerta = document.getElementById('configAlmacenOverstockAlerta');
    
    // Reportes
    const configReportesRangoPorDefecto = document.getElementById('configReportesRangoPorDefecto');
    const configReportesFormatoMoneda = document.getElementById('configReportesFormatoMoneda');
    const configReportesAccion1 = document.getElementById('configReportesAccion1');
    const configReportesAccion2 = document.getElementById('configReportesAccion2');
    const configPromocionesLista = document.getElementById('configPromocionesLista');
    const configPermisosDescuentoUsuarios = document.getElementById('configPermisosDescuentoUsuarios');
    
    const popupMisPedidos = document.getElementById('popupMisPedidos');
    const btnAjustesMain = document.getElementById('btnAjustesMain');
    const popupClientesModulo = document.getElementById('popupClientesModulo');
    const clientesmodBack = document.getElementById('clientesmodBack');
    const clientesmodSearch = document.getElementById('clientesmodSearch');
    const clientesmodAdd = document.getElementById('clientesmodAdd');
    const clientesmodEdit = document.getElementById('clientesmodEdit');
    const clientesmodDelete = document.getElementById('clientesmodDelete');
    const clientesmodTableBody = document.getElementById('clientesmodTableBody');
    const clientesmodConteo = document.getElementById('clientesmodConteo');
    const popupClientesForm = document.getElementById('popupClientesForm');
    const clientesformTitulo = document.getElementById('clientesformTitulo');
    const cliFormId = document.getElementById('cliFormId');
    const cliFormNombre = document.getElementById('cliFormNombre');
    const cliFormEmpresa = document.getElementById('cliFormEmpresa');
    const cliFormCorreo = document.getElementById('cliFormCorreo');
    const cliFormTipo = document.getElementById('cliFormTipo');
    const cliFormTelefono = document.getElementById('cliFormTelefono');
    const cliFormCalle = document.getElementById('cliFormCalle');
    const cliFormColonia = document.getElementById('cliFormColonia');
    const cliFormNumero = document.getElementById('cliFormNumero');
    const cliFormPais = document.getElementById('cliFormPais');
    const cliFormCiudad = document.getElementById('cliFormCiudad');
    const cliFormEstado = document.getElementById('cliFormEstado');
    const cliFormCp = document.getElementById('cliFormCp');
    const cliFormRazonSocial = document.getElementById('cliFormRazonSocial');
    const cliFormRfc = document.getElementById('cliFormRfc');
    const cliFormReferenciaBancaria = document.getElementById('cliFormReferenciaBancaria');
    const cliFormCancel = document.getElementById('cliFormCancel');
    const cliFormSave = document.getElementById('cliFormSave');
    const popupCaja = document.getElementById('popupCaja');
    const popupCalendario = document.getElementById('popupCalendario');
    const calBack = document.getElementById('calBack');
    const calMesLabel = document.getElementById('calMesLabel');
    const calPrevMonth = document.getElementById('calPrevMonth');
    const calNextMonth = document.getElementById('calNextMonth');
    const calGridDays = document.getElementById('calGridDays');
    const calListaBody = document.getElementById('calListaBody');
    const calFiltroFecha = document.getElementById('calFiltroFecha');
    const calFiltroFechaText = document.getElementById('calFiltroFechaText');
    const calListSub = document.getElementById('calListSub');
    const calQuickStats = document.getElementById('calQuickStats');
    const calScopeSelect = document.getElementById('calScopeSelect');
    const calStatusSelect = document.getElementById('calStatusSelect');
    const calSearchInput = document.getElementById('calSearchInput');
    const calClearFilter = document.getElementById('calClearFilter');
    const cajaBack = document.getElementById('cajaBack');
    const cajaTabCorte = document.getElementById('cajaTabCorte');
    const cajaTabGasto = document.getElementById('cajaTabGasto');
    const cajaPanelCorte = document.getElementById('cajaPanelCorte');
    const cajaPanelGasto = document.getElementById('cajaPanelGasto');
    const cajaNombreLabel = document.getElementById('cajaNombreLabel');
    const cajaIdLabel = document.getElementById('cajaIdLabel');
    const cajaUsuarioLabel = document.getElementById('cajaUsuarioLabel');
    const cajaNombreLabelGasto = document.getElementById('cajaNombreLabelGasto');
    const cajaIdLabelGasto = document.getElementById('cajaIdLabelGasto');
    const cajaUsuarioLabelGasto = document.getElementById('cajaUsuarioLabelGasto');
    const cajaKpiFondo = document.getElementById('cajaKpiFondo');
    const cajaKpiEfectivo = document.getElementById('cajaKpiEfectivo');
    const cajaKpiTarjeta = document.getElementById('cajaKpiTarjeta');
    const cajaKpiTransferencia = document.getElementById('cajaKpiTransferencia');
    const cajaKpiDeposito = document.getElementById('cajaKpiDeposito');
    const cajaKpiGastos = document.getElementById('cajaKpiGastos');
    const cajaBtnRealizarCorte = document.getElementById('cajaBtnRealizarCorte');
    const cajaGastoFuente = document.getElementById('cajaGastoFuente');
    const cajaDisponibleMonto = document.getElementById('cajaDisponibleMonto');
    const cajaGastoMotivo = document.getElementById('cajaGastoMotivo');
    const cajaGastoMonto = document.getElementById('cajaGastoMonto');
    const cajaBtnIngresarDinero = document.getElementById('cajaBtnIngresarDinero');
    const cajaBtnRealizarGasto = document.getElementById('cajaBtnRealizarGasto');
    const popupProductos = document.getElementById('popupProductos');
    const productosBack = document.getElementById('productosBack');
    const productosTabStock = document.getElementById('productosTabStock');
    const productosTabFormato = document.getElementById('productosTabFormato');
    const productosLegend = document.getElementById('productosLegend');
    const prodRegistrosCount = document.getElementById('prodRegistrosCount');
    const productosTablaHead = document.getElementById('productosTablaHead');
    const productosTablaBody = document.getElementById('productosTablaBody');
    const productosSearchInput = document.getElementById('productosSearchInput');
    const prodActualizar = document.getElementById('prodActualizar');
    const prodLowStock = document.getElementById('prodLowStock');
    const prodExportPdf = document.getElementById('prodExportPdf');
    const prodFiltroCategoria = document.getElementById('prodFiltroCategoria');
    const prodFiltroCodigo = document.getElementById('prodFiltroCodigo');
    const prodEntradaStock = document.getElementById('prodEntradaStock');
    const prodImprimir = document.getElementById('prodImprimir');
    const prodExcel = document.getElementById('prodExcel');
    const prodAbrirPlantilla = document.getElementById('prodAbrirPlantilla');
    const prodImportarDesde = document.getElementById('prodImportarDesde');
    const prodGfToolbar = document.getElementById('prodGfToolbar');
    const prodGfAbrirPlantilla = document.getElementById('prodGfAbrirPlantilla');
    const prodGfImportarDesde = document.getElementById('prodGfImportarDesde');
    const prodGfExportarDesde = document.getElementById('prodGfExportarDesde');
    const prodImportFile = document.getElementById('prodImportFile');
    const prodAgregar = document.getElementById('prodAgregar');
    const prodEditar = document.getElementById('prodEditar');
    const prodEliminar = document.getElementById('prodEliminar');
    const popupProdCategoria = document.getElementById('popupProdCategoria');
    const prodCategoriaLista = document.getElementById('prodCategoriaLista');
    const prodCategoriaCerrar = document.getElementById('prodCategoriaCerrar');
    const popupProdEntrada = document.getElementById('popupProdEntrada');
    const prodEntradaBuscar = document.getElementById('prodEntradaBuscar');
    const prodEntradaSelect = document.getElementById('prodEntradaSelect');
    const prodEntradaCantidad = document.getElementById('prodEntradaCantidad');
    const prodEntradaGuardar = document.getElementById('prodEntradaGuardar');
    const prodEntradaCerrar = document.getElementById('prodEntradaCerrar');
    const popupProdForm = document.getElementById('popupProdForm');
    const prodFormCard = document.getElementById('prodFormCard');
    const prodFormTitulo = document.getElementById('prodFormTitulo');
    const prodFormCodigo = document.getElementById('prodFormCodigo');
    const prodFormGenerarCodigo = document.getElementById('prodFormGenerarCodigo');
    const prodFormTipo = document.getElementById('prodFormTipo');
    const prodFormProducto = document.getElementById('prodFormProducto');
    const prodFormCategoria = document.getElementById('prodFormCategoria');
    const prodFormMedida = document.getElementById('prodFormMedida');
    const prodFormMaterial = document.getElementById('prodFormMaterial');
    const prodFormMinima = document.getElementById('prodFormMinima');
    const prodFormExistencias = document.getElementById('prodFormExistencias');
    const prodFormPrecioCompra = document.getElementById('prodFormPrecioCompra');
    const prodFormTipoImpresion = document.getElementById('prodFormTipoImpresion');
    const prodFormProveedor = document.getElementById('prodFormProveedor');
    const prodFormDescripcion = document.getElementById('prodFormDescripcion');
    const prodGfCobroTipo = document.getElementById('prodGfCobroTipo');
    const prodGfPrecioGeneralM2 = document.getElementById('prodGfPrecioGeneralM2');
    const prodGfPrecioRevM2 = document.getElementById('prodGfPrecioRevM2');
    const prodGfPrecioGeneralML = document.getElementById('prodGfPrecioGeneralML');
    const prodGfPrecioRevML = document.getElementById('prodGfPrecioRevML');
    const prodGfCostoM2 = document.getElementById('prodGfCostoM2');
    const prodGfCostoML = document.getElementById('prodGfCostoML');
    const prodGfAjusteAncho = document.getElementById('prodGfAjusteAncho');
    const prodFormFotoPrincipal = document.getElementById('prodFormFotoPrincipal');
    const prodFormFotoPreview = document.getElementById('prodFormFotoPreview');
    const prodColorNombre = document.getElementById('prodColorNombre');
    const prodColorExistencias = document.getElementById('prodColorExistencias');
    const prodColorFoto = document.getElementById('prodColorFoto');
    const prodColorAgregar = document.getElementById('prodColorAgregar');
    const prodColorLista = document.getElementById('prodColorLista');
    const prodFormRevendedor = document.getElementById('prodFormRevendedor');
    const prodFormVenta = document.getElementById('prodFormVenta');
    const prodFormSiguiente = document.getElementById('prodFormSiguiente');
    const prodFormCerrar = document.getElementById('prodFormCerrar');
    const popupProdTabulador = document.getElementById('popupProdTabulador');
    const prodTabuladorSelect = document.getElementById('prodTabuladorSelect');
    const prodTabRangosPreview = document.getElementById('prodTabRangosPreview');
    const prodTabPreciosPreview = document.getElementById('prodTabPreciosPreview');
    const prodTabFotoPreview = document.getElementById('prodTabFotoPreview');
    const prodTabVolver = document.getElementById('prodTabVolver');
    const prodTabGuardarProducto = document.getElementById('prodTabGuardarProducto');
    const prodTabCerrar = document.getElementById('prodTabCerrar');
    const popupAjustesTabuladores = document.getElementById('popupAjustesTabuladores');
    const ajustesCajaNombre = document.getElementById('ajustesCajaNombre');
    const ajustesCajaId = document.getElementById('ajustesCajaId');
    const ajustesTabSelect = document.getElementById('ajustesTabSelect');
    const ajustesTabNombre = document.getElementById('ajustesTabNombre');
    const ajustesTabRangosTable = document.getElementById('ajustesTabRangosTable');
    const ajustesTabPreciosTable = document.getElementById('ajustesTabPreciosTable');
    const ajustesTabNuevo = document.getElementById('ajustesTabNuevo');
    const ajustesTabEliminar = document.getElementById('ajustesTabEliminar');
    const ajustesTabGuardar = document.getElementById('ajustesTabGuardar');
    const ajustesTabCerrar = document.getElementById('ajustesTabCerrar');
    const mispedidosBack = document.getElementById('mispedidosBack');
    const mispedidosTabVentas = document.getElementById('mispedidosTabVentas');
    const mispedidosTabCot = document.getElementById('mispedidosTabCot');
    const mpTablaBody = document.getElementById('mpTablaBody');
    const mpConteoLabel = document.getElementById('mpConteoLabel');
    const mpConteoValor = document.getElementById('mpConteoValor');
    const mpAdeudoPendiente = document.getElementById('mpAdeudoPendiente');
    const mpTotalVentas = document.getElementById('mpTotalVentas');
    const mpTotalInversion = document.getElementById('mpTotalInversion');
    const mpTotalGanancia = document.getElementById('mpTotalGanancia');
    const mpFiltroFolio = document.getElementById('mpFiltroFolio');
    const mpFiltroNombre = document.getElementById('mpFiltroNombre');
    const mpFiltroTelefono = document.getElementById('mpFiltroTelefono');
    const mpFiltroDisenador = document.getElementById('mpFiltroDisenador');
    const mpFiltroFechaEmitida = document.getElementById('mpFiltroFechaEmitida');
    const mpFiltroFechaEntrega = document.getElementById('mpFiltroFechaEntrega');
    const mpFiltroEstatus = document.getElementById('mpFiltroEstatus');
    const mpFiltroAdeudo = document.getElementById('mpFiltroAdeudo');
    const mpLimpiarFiltros = document.getElementById('mpLimpiarFiltros');
    const mpEditarSeleccion = document.getElementById('mpEditarSeleccion');
    const mpExportarSeleccion = document.getElementById('mpExportarSeleccion');
    let designPendingRows = [];
    let selectedDesignOrder = null;
    const MIS_PEDIDOS_KEY = 'mock_mis_pedidos_v1';
    let misPedidosTab = 'venta';
    let misPedidosData = [];
    let mpSelectedIds = new Set();
    const PRODUCTOS_KEY = 'mock_productos_v1';
    const CAJA_SETTINGS_KEY = 'mock_caja_settings_v1';
    const CAJA_MOVS_KEY = 'mock_caja_movs_v1';
    const CAJA_APERTURAS_KEY = 'mock_caja_aperturas_v1';
    const CAL_ALERTS_KEY = 'mock_calendario_alertas_v1';
    const CLIENTES_MODULO_KEY = 'mock_clientes_modulo_v1';
    let productosTab = 'stock';
    let productosData = [];
    let productosSelectedIds = new Set();
    let productosSelectionAnchorId = '';
    let productosSearchTerm = '';
    let productosCodigoFilter = '';
    let productosCategoriaFilter = '';
    let productosLowStockOnly = false;
    let productoEditandoId = '';
    let prodMainPhotoData = '';
    let prodColorDraftList = [];
    let prodPendingPayload = null;
    let prodPendingTabuladorId = '';
    let prodPendingTabuladorPrecios = [];
    const TABULADORES_KEY = 'mock_productos_tabuladores_v1';
    let tabuladoresData = [];
    let ajustesTabuladorId = '';
    let cajaTabActiva = 'corte';
    let cajaSettings = { nombre: 'Caja principal', id: 'CAJA-01' };
    let cajaMovimientos = [];
    let cajaAperturas = {};
    let calendarioAlertas = {};
    let calViewDate = new Date();
    let calSelectedDate = '';
    let calScopeMode = 'selected';
    let calStatusMode = 'all';
    let calSearchTerm = '';
    let clientesModuloData = [];
    let clientesModuloSelectedId = '';
    let clientesModuloEditingId = '';
    let ordenClienteSeleccionadoId = '';
    let ordenClienteFormMode = '';

    if (!btnListadoRapido || !popupListado) {
        return;
    }

    const el = (id) => document.getElementById(id);
    const refs = {
        clienteNombre: el('ordenClienteNombre'),
        clienteId: el('ordenClienteId'),
        clienteCorreo: el('ordenClienteCorreo'),
        clienteTelefono: el('ordenClienteTelefono'),
        clienteNegocio: el('ordenClienteNegocio'),
        fechaEntrega: el('ordenFechaEntrega'),
        entregaDias: el('ordenEntregaDias'),
        tablaBody: el('ordenTablaBody'),
        subtotal: el('ordenSubtotal'),
        impuestos: el('ordenImpuestos'),
        descuento: el('ordenDescuento'),
        inversion: el('ordenInversion'),
        ganancia: el('ordenGanancia'),
        totalMain: el('ordenTotalMain'),
        cotizacionPopup: el('ordenCotizacionPopup')
    };

    let syncingEntrega = false;

    const formatMoney = (n = 0) => `$${Number(n || 0).toFixed(2)}`;
    const todayISO = () => new Date().toISOString().slice(0, 10);
    const mkClientId = () => `CLI-${Date.now().toString(36).toUpperCase()}`;
    const mkFolio = () => `OT-${Date.now().toString(36).toUpperCase()}`;
    const getSelectedPayMethod = () => {
        const active = document.querySelector('.orden-pay-btn.active[data-pay]');
        const raw = String(active?.dataset?.pay || '').toUpperCase().trim();
        if (raw === 'TARJETA') return 'TARJETA';
        if (raw === 'TRANSFERENCIA') return 'TRANSFERENCIA';
        if (raw === 'DEPOSITO' || raw === 'DEPÓSITO') return 'DEPOSITO';
        if (raw === 'GUARDAR SIN ANTICIPO') return 'GUARDAR SIN ANTICIPO';
        return 'EFECTIVO';
    };

    const getActivePayMethodRaw = () => {
        const active = document.querySelector('.orden-pay-btn.active[data-pay]');
        return String(active?.dataset?.pay || '').toUpperCase().trim();
    };

    const buildEmptyOrdenState = () => ({
        lineas: [],
        lineaActiva: -1,
        taxRate: 0,
        discount: 0,
        discountAmount: 0,
        discountLabel: '',
        inversion: 0,
        anticipo: 0,
        pagoDetalle: null,
        folio: mkFolio(),
        clienteNombre: 'SIN CLIENTE SELECCIONADO',
        clienteId: 'SIN ASIGNAR',
        clienteCorreo: '',
        clienteTelefono: '',
        clienteNegocio: '',
        fechaEntrega: todayISO(),
        entregaDias: '3',
        comentarios: '',
        disenador: (getDisenadoresConfigurados()[0] || 'DISEÑADOR 1'),
        vendedor: getUsuarioLogeado(),
        payMethod: ''
    });

    const captureOrdenState = () => ({
        lineas: ordenLineas.map((row) => ({ ...row })),
        lineaActiva: Number(ordenLineaActiva || -1),
        taxRate: Number(ordenTaxRate || 0),
        discount: Number(ordenDiscount || 0),
        discountAmount: Number(ordenDiscountAmount || 0),
        discountLabel: String(ordenDiscountLabel || ''),
        inversion: Number(ordenInversion || 0),
        folio: ordenTrabajoFolio || mkFolio(),
        clienteNombre: String(refs.clienteNombre?.textContent || 'SIN CLIENTE SELECCIONADO'),
        clienteId: String(refs.clienteId?.value || ''),
        clienteCorreo: String(refs.clienteCorreo?.value || ''),
        clienteTelefono: String(refs.clienteTelefono?.value || ''),
        clienteNegocio: String(refs.clienteNegocio?.value || ''),
        fechaEntrega: String(refs.fechaEntrega?.value || todayISO()),
        entregaDias: String(refs.entregaDias?.value || '3'),
        comentarios: String(el('ordenComentarios')?.value || ''),
        disenador: String(el('ordenDisenador')?.value || ''),
        vendedor: String(el('ordenVendedor')?.value || ''),
        anticipo: Number(ordenAnticipo || 0),
        pagoDetalle: ordenPagoDetalle ? { ...ordenPagoDetalle } : null,
        payMethod: getActivePayMethodRaw()
    });

    const applyOrdenState = (state = buildEmptyOrdenState()) => {
        const safe = state || buildEmptyOrdenState();
        ordenLineas = Array.isArray(safe.lineas) ? safe.lineas.map((row) => ({ ...row })) : [];
        ordenLineaActiva = Number.isFinite(Number(safe.lineaActiva)) ? Number(safe.lineaActiva) : -1;
        ordenTaxRate = Math.max(0, Number(safe.taxRate || 0));
        ordenDiscount = Math.max(0, Number(safe.discount || 0));
        ordenDiscountAmount = Math.max(0, Number(safe.discountAmount || 0));
        ordenDiscountLabel = String(safe.discountLabel || '');
        ordenInversion = Math.max(0, Number(safe.inversion || 0));
        ordenAnticipo = Math.max(0, Number(safe.anticipo || 0));
        ordenPagoDetalle = safe.pagoDetalle && typeof safe.pagoDetalle === 'object' ? { ...safe.pagoDetalle } : null;
        ordenTrabajoFolio = String(safe.folio || mkFolio());

        if (refs.clienteNombre) refs.clienteNombre.textContent = String(safe.clienteNombre || 'SIN CLIENTE SELECCIONADO');
        if (refs.clienteId) refs.clienteId.value = String(safe.clienteId || 'SIN ASIGNAR');
        if (refs.clienteCorreo) refs.clienteCorreo.value = String(safe.clienteCorreo || '');
        if (refs.clienteTelefono) refs.clienteTelefono.value = String(safe.clienteTelefono || '');
        if (refs.clienteNegocio) refs.clienteNegocio.value = String(safe.clienteNegocio || '');
        if (refs.fechaEntrega) refs.fechaEntrega.value = String(safe.fechaEntrega || todayISO());
        if (refs.entregaDias) refs.entregaDias.value = String(safe.entregaDias || '3');

        const comentarios = el('ordenComentarios');
        const disenador = el('ordenDisenador');
        const vendedor = el('ordenVendedor');
        renderDisenadoresSelect();
        if (comentarios) comentarios.value = String(safe.comentarios || '');
        if (disenador) disenador.value = String(safe.disenador || '');
        if (vendedor) vendedor.value = String(safe.vendedor || getUsuarioLogeado());

        const payButtons = Array.from(document.querySelectorAll('.orden-pay-btn[data-pay]'));
        payButtons.forEach((b) => b.classList.remove('active'));
        const payMethod = String(safe.payMethod || '').toUpperCase().trim();
        if (payMethod) {
            const target = payButtons.find((b) => String(b.dataset.pay || '').toUpperCase().trim() === payMethod);
            if (target) target.classList.add('active');
        }

        const impuestosBtn = el('ordenBtnImpuestos');
        if (impuestosBtn) impuestosBtn.classList.toggle('active', Number(ordenTaxRate || 0) > 0);

        renderTabla();
    };

    const saveTicketActivo = () => {
        if (!ordenTickets.length) return;
        ordenTickets[ordenTicketActivo] = captureOrdenState();
    };

    const renderTicketTabs = () => {
        if (!ordenTicketTabs) return;
        const tabsHtml = ordenTickets.map((_, idx) => {
            const active = idx === ordenTicketActivo ? ' active' : '';
            return `<button class="orden-ticket-tab${active}" type="button" data-ticket-index="${idx}">TICKET ${idx + 1}</button>`;
        }).join('');
        ordenTicketTabs.innerHTML = `${tabsHtml}<button id="ordenTicketAdd" class="orden-ticket-add" type="button" title="Agregar ticket" aria-label="Agregar ticket">+</button>`;
    };

    const switchTicket = (idx) => {
        const next = Number(idx);
        if (!Number.isFinite(next) || next < 0 || next >= ordenTickets.length || next === ordenTicketActivo) return;
        saveTicketActivo();
        ordenTicketActivo = next;
        applyOrdenState(ordenTickets[ordenTicketActivo] || buildEmptyOrdenState());
        renderTicketTabs();
    };

    const addNewTicket = () => {
        saveTicketActivo();
        const nuevo = buildEmptyOrdenState();
        ordenTickets.push(nuevo);
        ordenTicketActivo = ordenTickets.length - 1;
        applyOrdenState(nuevo);
        renderTicketTabs();
    };

    const removeCurrentTicket = () => {
        if (ordenTickets.length <= 1) {
            const limpio = buildEmptyOrdenState();
            ordenTickets[0] = limpio;
            ordenTicketActivo = 0;
            applyOrdenState(limpio);
            renderTicketTabs();
            return;
        }
        ordenTickets.splice(ordenTicketActivo, 1);
        ordenTicketActivo = Math.max(0, ordenTicketActivo - 1);
        applyOrdenState(ordenTickets[ordenTicketActivo] || buildEmptyOrdenState());
        renderTicketTabs();
    };

    const getDisenadoresConfigurados = () => {
        const arr = getConfigValue('caja', 'disenadores');
        if (Array.isArray(arr) && arr.length) return arr;
        return ['DISEÑADOR 1'];
    };

    const renderDisenadoresSelect = () => {
        const sel = el('ordenDisenador');
        if (!sel) return;
        const current = String(sel.value || '').trim();
        const options = getDisenadoresConfigurados();
        sel.innerHTML = options.map((d) => `<option value="${prodEscape(d)}">${prodEscape(d)}</option>`).join('');
        if (current && options.includes(current)) {
            sel.value = current;
        }
    };

    const upsertClienteEnStores = (cliente = {}) => {
        const id = String(cliente.id || '').trim() || mkClienteModuloId();
        const nombre = String(cliente.nombre || cliente.clienteNombre || '').trim();
        if (!nombre) return;
        const correo = String(cliente.email || cliente.correo || '').trim();
        const telefono = String(cliente.telefono || cliente.numero || '').trim();
        const negocio = String(cliente.negocio || cliente.empresa || '').trim();

        const payloadModulo = {
            id,
            nombre,
            empresa: negocio,
            telefono,
            correo,
            calle: '',
            colonia: '',
            numero: '',
            pais: 'Mexico',
            ciudad: '',
            estado: '',
            cp: '',
            razonSocial: '',
            rfc: '',
            referenciaBancaria: '',
            tipoCliente: 'Publico en general'
        };

        loadClientesModulo();
        const idx = clientesModuloData.findIndex((c) => String(c.id || '').trim() === id);
        if (idx >= 0) {
            clientesModuloData[idx] = { ...clientesModuloData[idx], ...payloadModulo };
        } else {
            clientesModuloData.unshift(payloadModulo);
        }
        saveClientesModulo();

        try {
            const key = 'mock_clientes_quick_v1';
            const raw = localStorage.getItem(key);
            const arr = Array.isArray(JSON.parse(raw || '[]')) ? JSON.parse(raw || '[]') : [];
            const quick = { id, nombre, telefono, email: correo, negocio };
            const qIdx = arr.findIndex((c) => String(c.id || '').trim() === id || String(c.nombre || '').trim().toUpperCase() === nombre.toUpperCase());
            if (qIdx >= 0) arr[qIdx] = { ...arr[qIdx], ...quick };
            else arr.unshift(quick);
            localStorage.setItem(key, JSON.stringify(arr));
        } catch (_) {}
    };

    const getClientesOrdenSelectable = () => {
        loadClientesModulo();
        return clientesModuloData.map((c) => ({
            id: String(c.id || '').trim(),
            nombre: String(c.nombre || '').trim(),
            negocio: String(c.empresa || '').trim(),
            telefono: String(c.telefono || '').trim(),
            correo: String(c.correo || '').trim(),
            tipoCliente: String(c.tipoCliente || 'Publico en general').trim() || 'Publico en general'
        }));
    };

    const renderOrdenClienteSelectTable = () => {
        if (!ordenClienteSelectTableBody) return;
        const term = String(ordenClienteSelectSearch?.value || '').trim().toLowerCase();
        const rows = getClientesOrdenSelectable().filter((c) => {
            if (!term) return true;
            return [c.nombre, c.negocio, c.telefono].some((v) => String(v || '').toLowerCase().includes(term));
        });

        if (!rows.length) {
            ordenClienteSelectTableBody.innerHTML = '<tr><td colspan="6" style="text-align:center;color:#6b7280;padding:12px;">No hay clientes para ese filtro.</td></tr>';
            if (ordenClienteSelectCount) ordenClienteSelectCount.textContent = '0 resultados';
            if (ordenClienteSelectAccept) ordenClienteSelectAccept.disabled = true;
            return;
        }

        if (!rows.some((r) => r.id === ordenClienteSeleccionadoId)) {
            ordenClienteSeleccionadoId = rows[0].id;
        }

        ordenClienteSelectTableBody.innerHTML = rows.map((r) => {
            const cls = r.id === ordenClienteSeleccionadoId ? 'orden-client-select-row active' : 'orden-client-select-row';
            return `<tr class="${cls}" data-orden-cli-id="${escCliMod(r.id)}">
                <td>${escCliMod(r.id)}</td>
                <td>${escCliMod(r.nombre)}</td>
                <td>${escCliMod(r.negocio)}</td>
                <td>${escCliMod(r.telefono)}</td>
                <td>${escCliMod(r.correo)}</td>
                <td>${escCliMod(r.tipoCliente)}</td>
            </tr>`;
        }).join('');

        if (ordenClienteSelectCount) {
            ordenClienteSelectCount.textContent = `${rows.length} registro${rows.length === 1 ? '' : 's'}`;
        }
        if (ordenClienteSelectAccept) ordenClienteSelectAccept.disabled = false;

        ordenClienteSelectTableBody.querySelectorAll('[data-orden-cli-id]').forEach((tr) => {
            tr.addEventListener('click', () => {
                ordenClienteSeleccionadoId = String(tr.getAttribute('data-orden-cli-id') || '');
                renderOrdenClienteSelectTable();
            });
        });
    };

    const openOrdenClienteSelectPopup = () => {
        if (!ordenClienteSelectPopup) return;
        ordenClienteSeleccionadoId = '';
        if (ordenClienteSelectSearch) ordenClienteSelectSearch.value = '';
        renderOrdenClienteSelectTable();
        openOrdenPopup(ordenClienteSelectPopup);
        setTimeout(() => ordenClienteSelectSearch?.focus(), 20);
    };

    const closeOrdenClienteSelectPopup = () => {
        closeOrdenPopup(ordenClienteSelectPopup);
    };

    const initOrdenTickets = () => {
        ordenTickets = [buildEmptyOrdenState()];
        ordenTicketActivo = 0;
        applyOrdenState(ordenTickets[0]);
        renderTicketTabs();
    };

    const getTotalActualOrden = () => {
        const subtotalVal = ordenLineas.reduce((acc, row) => acc + (Number(row.precio) * Number(row.cantidad)), 0);
        const impuestosVal = subtotalVal * (ordenTaxRate / 100);
        const descuentoPctVal = subtotalVal * (ordenDiscount / 100);
        const descuentoVal = descuentoPctVal + Math.max(0, Number(ordenDiscountAmount || 0));
        return Math.max(0, subtotalVal + impuestosVal - descuentoVal);
    };

    const parsePromocionesConfiguradas = () => {
        const raw = getConfigValue('promociones', 'lista');
        const rows = Array.isArray(raw) ? raw : [];
        return rows
            .map((line) => String(line || '').trim())
            .filter(Boolean)
            .map((line) => {
                const parts = line.split(/[|,;]/).map((s) => String(s || '').trim());
                const codigo = String(parts[0] || '').toUpperCase();
                const tipoRaw = String(parts[1] || 'porcentaje').toLowerCase();
                const valor = Math.max(0, Number(parts[2] || 0));
                const tipo = tipoRaw === 'monto' ? 'monto' : 'porcentaje';
                return { codigo, tipo, valor };
            })
            .filter((p) => p.codigo && Number.isFinite(p.valor) && p.valor > 0);
    };

    const canUsuarioAplicarDescuento = () => {
        const usuario = String(getUsuarioLogeado() || '').trim().toLowerCase();
        const lista = getConfigValue('permisos', 'descuentoUsuarios');
        const permitidos = (Array.isArray(lista) ? lista : [])
            .map((v) => String(v || '').trim().toLowerCase())
            .filter(Boolean);
        if (!permitidos.length) return false;
        if (permitidos.includes('*') || permitidos.includes('todos')) return true;
        return permitidos.includes(usuario);
    };

    const openDescuentoPopup = () => {
        if (!ordenDescuentoPopup) return;
        if (!canUsuarioAplicarDescuento()) {
            notifyError('Tu usuario no tiene permisos para aplicar descuentos.', 'Permisos');
            return;
        }
        if (ordenDescuentoCodigo) ordenDescuentoCodigo.value = '';
        if (ordenDescuentoPorcentaje) ordenDescuentoPorcentaje.value = ordenDiscount > 0 ? String(ordenDiscount) : '';
        if (ordenDescuentoMonto) ordenDescuentoMonto.value = ordenDiscountAmount > 0 ? String(ordenDiscountAmount.toFixed(2)) : '';
        openOrdenPopup(ordenDescuentoPopup);
        setTimeout(() => ordenDescuentoCodigo?.focus(), 20);
    };

    const applyDescuento = () => {
        const codigo = String(ordenDescuentoCodigo?.value || '').trim().toUpperCase();
        const promociones = parsePromocionesConfiguradas();
        const promo = promociones.find((p) => p.codigo === codigo);
        if (promo) {
            if (promo.tipo === 'monto') {
                ordenDiscount = 0;
                ordenDiscountAmount = promo.valor;
            } else {
                ordenDiscount = promo.valor;
                ordenDiscountAmount = 0;
            }
            ordenDiscountLabel = promo.codigo;
            recalcResumen();
            saveTicketActivo();
            closeOrdenPopup(ordenDescuentoPopup);
            notifyInfo(`Descuento aplicado con código ${promo.codigo}.`, 'Descuento');
            return;
        }

        const pct = Math.max(0, Number(ordenDescuentoPorcentaje?.value || 0));
        const amount = Math.max(0, Number(ordenDescuentoMonto?.value || 0));
        if (pct <= 0 && amount <= 0) {
            notifyError('Ingresa un código válido o un descuento manual.', 'Descuento');
            return;
        }
        if (pct > 0 && amount > 0) {
            notifyError('Usa solo porcentaje o monto, no ambos al mismo tiempo.', 'Descuento');
            return;
        }

        ordenDiscount = pct > 0 ? pct : 0;
        ordenDiscountAmount = amount > 0 ? amount : 0;
        ordenDiscountLabel = '';
        recalcResumen();
        saveTicketActivo();
        closeOrdenPopup(ordenDescuentoPopup);
    };

    const hasClienteSeleccionado = () => {
        const nombre = String(refs.clienteNombre?.textContent || '').trim().toUpperCase();
        return !!nombre && nombre !== 'SIN CLIENTE SELECCIONADO';
    };

    const ensureCanProcessPayment = () => {
        if (!ordenLineas.length) {
            notifyError('Debes añadir al menos un producto al ticket para continuar.', 'Método de pago');
            return false;
        }
        if (!hasClienteSeleccionado()) {
            notifyError('Necesitas registrar o seleccionar un cliente de la lista para realizar la venta.', 'Cliente requerido');
            return false;
        }
        return true;
    };

    const setMetodoPagoActivo = (method) => {
        const raw = String(method || '').toUpperCase().trim();
        document.querySelectorAll('.orden-pay-btn[data-pay]').forEach((b) => {
            b.classList.toggle('active', String(b.dataset.pay || '').toUpperCase().trim() === raw);
        });
    };

    const openOrdenPopup = (popupEl) => {
        if (!popupEl) return;
        popupEl.style.display = 'flex';
        popupEl.setAttribute('aria-hidden', 'false');
    };

    const closeOrdenPopup = (popupEl) => {
        if (!popupEl) return;
        popupEl.style.display = 'none';
        popupEl.setAttribute('aria-hidden', 'true');
    };

    const showConfirmPopup = (message, onAccept) => {
        if (!ordenConfirmPopup || !ordenConfirmMensaje || !ordenConfirmAceptar || !ordenConfirmCancelar) {
            if (confirm(message)) onAccept?.();
            return;
        }
        ordenConfirmMensaje.textContent = String(message || '¿Seguro que deseas continuar?');
        openOrdenPopup(ordenConfirmPopup);
        ordenConfirmAceptar.onclick = () => {
            closeOrdenPopup(ordenConfirmPopup);
            onAccept?.();
        };
        ordenConfirmCancelar.onclick = () => closeOrdenPopup(ordenConfirmPopup);
    };

    const getCuentasBeneficiario = () => {
        const arr = getConfigValue('caja', 'cuentasBeneficiario');
        return Array.isArray(arr) && arr.length ? arr : ['BBVA - 0123456789'];
    };

    const registrarPagoYActivarMetodo = (method, anticipo, detalle = {}) => {
        ordenAnticipo = Math.max(0, Number(anticipo || 0));
        ordenPagoDetalle = { metodo: method, ...detalle };
        if (ordenAnticipo > 0) {
            loadMisPedidos();
            const venta = buildPedidoRegistro('venta');
            upsertMisPedidoRegistro(venta);
            saveMisPedidos();
        }
        setMetodoPagoActivo(method);
        saveTicketActivo();
        recalcResumen();
        notifyInfo(`Pago registrado por ${formatMoney(ordenAnticipo)}.`, 'Pago aplicado');
    };

    const renderPagoPopup = (method) => {
        if (!ordenPagoPopup || !ordenPagoBody || !ordenPagoTitulo || !ordenPagoAceptar || !ordenPagoCancelar) return;
        const total = getTotalActualOrden();
        const totalTxt = formatMoney(total);
        const bancoReceptor = String(getConfigValue('caja', 'bancoReceptor') || 'BBVA México');
        const cuentas = getCuentasBeneficiario();
        const cuentasOptions = cuentas.map((c) => `<option value="${prodEscape(c)}">${prodEscape(c)}</option>`).join('');

        const calc50Btn = '<button id="ordenPagoCalc50" class="orden-btn" type="button">CALCULAR 50%</button>';

        if (method === 'EFECTIVO' || method === 'TARJETA') {
            ordenPagoTitulo.textContent = method === 'EFECTIVO' ? 'PAGO EN EFECTIVO' : 'PAGO CON TARJETA';
            ordenPagoBody.innerHTML = `
                <div class="orden-field full"><label>Total de la venta</label><input type="text" value="${totalTxt}" readonly></div>
                <div class="orden-field full"><label for="ordenPagoCantidad">Cantidad recibida</label><input id="ordenPagoCantidad" type="number" min="0" step="0.01" placeholder="0.00"></div>
                <div class="orden-field full">${calc50Btn}</div>
            `;
            const cantidadInput = document.getElementById('ordenPagoCantidad');
            const calcBtn = document.getElementById('ordenPagoCalc50');
            if (calcBtn && cantidadInput) {
                calcBtn.onclick = () => { cantidadInput.value = (total * 0.5).toFixed(2); };
            }
            ordenPagoAceptar.onclick = () => {
                const monto = Math.max(0, Number(cantidadInput?.value || 0));
                if (monto <= 0) {
                    notifyError('Ingresa una cantidad válida para continuar.', 'Pago');
                    return;
                }
                registrarPagoYActivarMetodo(method, monto, { totalVenta: total });
                closeOrdenPopup(ordenPagoPopup);
            };
        } else if (method === 'TRANSFERENCIA') {
            ordenPagoTitulo.textContent = 'PAGO POR TRANSFERENCIA';
            ordenPagoBody.innerHTML = `
                <div class="orden-field"><label for="ordenPagoBancoEmisor">Banco emisor</label><input id="ordenPagoBancoEmisor" type="text" placeholder="Banco del cliente"></div>
                <div class="orden-field"><label for="ordenPagoBancoReceptor">Banco receptor</label><input id="ordenPagoBancoReceptor" type="text" value="${prodEscape(bancoReceptor)}" readonly></div>
                <div class="orden-field"><label for="ordenPagoReferencia">No. de referencia (opcional)</label><input id="ordenPagoReferencia" type="text" placeholder="Referencia"></div>
                <div class="orden-field"><label for="ordenPagoRastreo">No. de rastreo (opcional)</label><input id="ordenPagoRastreo" type="text" placeholder="Rastreo"></div>
                <div class="orden-field full"><label for="ordenPagoCuentaBeneficiario">Cuenta beneficiario</label><select id="ordenPagoCuentaBeneficiario">${cuentasOptions}</select></div>
                <div class="orden-field full"><label for="ordenPagoCantidad">Cantidad</label><input id="ordenPagoCantidad" type="number" min="0" step="0.01" placeholder="0.00"></div>
                <div class="orden-field full">${calc50Btn}</div>
            `;
            const cantidadInput = document.getElementById('ordenPagoCantidad');
            const calcBtn = document.getElementById('ordenPagoCalc50');
            if (calcBtn && cantidadInput) {
                calcBtn.onclick = () => { cantidadInput.value = (total * 0.5).toFixed(2); };
            }
            ordenPagoAceptar.onclick = () => {
                const monto = Math.max(0, Number(cantidadInput?.value || 0));
                if (monto <= 0) {
                    notifyError('Ingresa una cantidad válida para continuar.', 'Pago');
                    return;
                }
                registrarPagoYActivarMetodo('TRANSFERENCIA', monto, {
                    bancoEmisor: String(document.getElementById('ordenPagoBancoEmisor')?.value || ''),
                    bancoReceptor,
                    referencia: String(document.getElementById('ordenPagoReferencia')?.value || ''),
                    rastreo: String(document.getElementById('ordenPagoRastreo')?.value || ''),
                    cuentaBeneficiario: String(document.getElementById('ordenPagoCuentaBeneficiario')?.value || '')
                });
                closeOrdenPopup(ordenPagoPopup);
            };
        } else if (method === 'DEPOSITO') {
            ordenPagoTitulo.textContent = 'PAGO POR DEPÓSITO';
            ordenPagoBody.innerHTML = `
                <div class="orden-field full"><label for="ordenPagoProcedencia">Origen de procedencia</label>
                    <select id="ordenPagoProcedencia">
                        <option value="OXXO">OXXO</option>
                        <option value="7-Eleven">7-Eleven</option>
                        <option value="Farmacias del Ahorro">Farmacias del Ahorro</option>
                        <option value="Walmart">Walmart</option>
                        <option value="Chedraui">Chedraui</option>
                        <option value="Bodega Aurrera">Bodega Aurrera</option>
                    </select>
                </div>
                <div class="orden-field"><label for="ordenPagoBancoReceptor">Banco receptor</label><input id="ordenPagoBancoReceptor" type="text" value="${prodEscape(bancoReceptor)}" readonly></div>
                <div class="orden-field"><label for="ordenPagoCuentaBeneficiario">Cuenta beneficiario</label><select id="ordenPagoCuentaBeneficiario">${cuentasOptions}</select></div>
                <div class="orden-field full"><label for="ordenPagoCantidad">Cantidad</label><input id="ordenPagoCantidad" type="number" min="0" step="0.01" placeholder="0.00"></div>
                <div class="orden-field full">${calc50Btn}</div>
            `;
            const cantidadInput = document.getElementById('ordenPagoCantidad');
            const calcBtn = document.getElementById('ordenPagoCalc50');
            if (calcBtn && cantidadInput) {
                calcBtn.onclick = () => { cantidadInput.value = (total * 0.5).toFixed(2); };
            }
            ordenPagoAceptar.onclick = () => {
                const monto = Math.max(0, Number(cantidadInput?.value || 0));
                if (monto <= 0) {
                    notifyError('Ingresa una cantidad válida para continuar.', 'Pago');
                    return;
                }
                registrarPagoYActivarMetodo('DEPOSITO', monto, {
                    procedencia: String(document.getElementById('ordenPagoProcedencia')?.value || ''),
                    bancoReceptor,
                    cuentaBeneficiario: String(document.getElementById('ordenPagoCuentaBeneficiario')?.value || '')
                });
                closeOrdenPopup(ordenPagoPopup);
            };
        }

        ordenPagoCancelar.onclick = () => closeOrdenPopup(ordenPagoPopup);
        openOrdenPopup(ordenPagoPopup);
    };

    const openVentaRapidaPopup = () => {
        if (!ordenVentaRapidaPopup || !ordenVrNombre || !ordenVrMonto) return;
        ordenVrNombre.value = '';
        ordenVrMonto.value = '';
        openOrdenPopup(ordenVentaRapidaPopup);
        setTimeout(() => ordenVrNombre.focus(), 20);
    };

    const closeNotifyPopup = () => {
        if (!popupNotify) return;
        popupNotify.style.display = 'none';
        popupNotify.setAttribute('aria-hidden', 'true');
    };

    const openNotifyPopup = (title, message) => {
        if (!popupNotify) return;
        if (notifyTitle) notifyTitle.textContent = String(title || 'Notificación');
        if (notifyMessage) notifyMessage.textContent = String(message || '');
        popupNotify.style.display = 'flex';
        popupNotify.setAttribute('aria-hidden', 'false');
    };

    const notifyInfo = (message, title = 'Notificación') => openNotifyPopup(title, message);
    const notifyError = (message, title = 'Atención') => openNotifyPopup(title, message);

    // ===== CONFIGURACIONES DEL SISTEMA =====
    const CONFIG_SYSTEM_KEY = 'mock_config_system_v1';
    
    let systemConfig = {
        caja: {
            nombre: 'Caja principal',
            id: 'CAJA-01',
            moneda: 'MXN',
            corteAutomatico: 'manual',
            bancoReceptor: 'BBVA México',
            cuentasBeneficiario: ['BBVA - 0123456789'],
            disenadores: ['DISEÑADOR 1'],
            fondoMinimo: 1,
            fuentePredeterminada: 'EFECTIVO',
            metodosActivos: ['EFECTIVO', 'TARJETA', 'TRANSFERENCIA', 'DEPOSITO'],
            permitirIngresoManual: true,
            permitirGastos: true
        },
        clientes: { categoriaPorDefecto: 'Mayoreo', creditoMaximo: 0, alertaBajaExistencia: 5000, aceptarOrdenesSinCliente: true },
        productos: { unidadPorDefecto: 'pza', margenPorDefecto: 30, alertaBajaExistencia: 10, actualizarPreciosAutomatico: true },
        proveedores: { diasCredito: 30, monedaPorDefecto: 'MXN', alertaSaldoPendiente: 10000, aceptarSinEntre: false },
        insumos: { unidadPorDefecto: 'pza', stockMinimoAlerta: 50, aceptarComprasConStock: false, mostrarCostoProduccion: true },
        almacen: { ubicacionPorDefecto: 'PISO_1', stockMinimoAlerta: 20, aceptarStockNegativo: false, overstockAlerta: true },
        reportes: { rangoPorDefecto: 30, formatoMoneda: 'MXN', mostrarGraficos: true, actualizarKpisAutomatico: true },
        promociones: { lista: ['PROMO10|porcentaje|10', 'BIENVENIDA50|monto|50'] },
        permisos: { descuentoUsuarios: ['admin'] }
    };

    const loadSystemConfig = () => {
        try {
            const stored = JSON.parse(localStorage.getItem(CONFIG_SYSTEM_KEY) || '{}');
            systemConfig = { ...systemConfig, ...stored };
        } catch (_) {
            // fallback to defaults
        }
    };

    const saveSystemConfig = () => {
        try {
            localStorage.setItem(CONFIG_SYSTEM_KEY, JSON.stringify(systemConfig));
        } catch (_) {
            notifyError('No se pudo guardar las configuraciones.', 'Error');
        }
    };

    const getConfigValue = (category, key) => {
        return systemConfig[category]?.[key];
    };

    const setConfigValue = (category, key, value) => {
        if (!systemConfig[category]) systemConfig[category] = {};
        systemConfig[category][key] = value;
    };

    // Popups - FONDO DE CAJA
    const closeFondoCajaPopup = () => {
        if (!popupFondoCaja) return;
        popupFondoCaja.style.display = 'none';
        popupFondoCaja.setAttribute('aria-hidden', 'true');
    };

    const openFondoCajaPopup = () => {
        if (!popupFondoCaja || !fondoCajaInputMonto) return;
        fondoCajaInputMonto.value = '1';
        fondoCajaInputMonto.focus();
        popupFondoCaja.style.display = 'flex';
        popupFondoCaja.setAttribute('aria-hidden', 'false');
        document.body.classList.add('popup-open');
        document.documentElement.classList.add('popup-open');
    };

    // Popups - CONFIGURACIONES
    const closeConfiguracionesPopup = () => {
        if (!popupConfiguraciones) return;
        popupConfiguraciones.style.display = 'none';
        popupConfiguraciones.setAttribute('aria-hidden', 'true');
        if (popupFondoCaja?.style.display !== 'flex') {
            document.body.classList.remove('popup-open');
            document.documentElement.classList.remove('popup-open');
        }
    };

    const switchConfigTab = (tabName) => {
        // Hide all tabs
        document.querySelectorAll('.config-tab-panel').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.config-tab').forEach(t => t.classList.remove('active'));
        
        // Show selected tab
        const panel = document.getElementById(`tab${tabName.charAt(0).toUpperCase() + tabName.slice(1)}`);
        if (panel) panel.classList.add('active');
        
        // Mark tab as active
        document.querySelector(`[data-tab="${tabName}"]`)?.classList.add('active');
    };

    const renderConfiguracionesPopup = () => {
        // Caja
        if (configCajaNombre) configCajaNombre.value = getConfigValue('caja', 'nombre') || 'Caja principal';
        if (configCajaId) configCajaId.value = getConfigValue('caja', 'id') || 'CAJA-01';
        if (configCajaMoneda) configCajaMoneda.value = getConfigValue('caja', 'moneda') || 'MXN';
        if (configCajaCorteAutomatico) configCajaCorteAutomatico.value = getConfigValue('caja', 'corteAutomatico') || 'manual';
        if (configCajaBancoReceptor) configCajaBancoReceptor.value = getConfigValue('caja', 'bancoReceptor') || 'BBVA México';
        if (configCajaCuentasBeneficiario) {
            const cuentas = getConfigValue('caja', 'cuentasBeneficiario');
            const arr = Array.isArray(cuentas) ? cuentas : [];
            configCajaCuentasBeneficiario.value = arr.join('\n');
        }
        if (configCajaDisenadores) {
            const disenadores = getConfigValue('caja', 'disenadores');
            const arr = Array.isArray(disenadores) ? disenadores : [];
            configCajaDisenadores.value = arr.join('\n');
        }
        if (configCajaFondoMinimo) configCajaFondoMinimo.value = Number(getConfigValue('caja', 'fondoMinimo') || 1);
        if (configCajaFuentePredeterminada) configCajaFuentePredeterminada.value = getConfigValue('caja', 'fuentePredeterminada') || 'EFECTIVO';
        const metodos = getConfigValue('caja', 'metodosActivos');
        const metodosActivos = Array.isArray(metodos) && metodos.length ? metodos : ['EFECTIVO', 'TARJETA', 'TRANSFERENCIA', 'DEPOSITO'];
        if (configCajaMetodoEfectivo) configCajaMetodoEfectivo.checked = metodosActivos.includes('EFECTIVO');
        if (configCajaMetodoTarjeta) configCajaMetodoTarjeta.checked = metodosActivos.includes('TARJETA');
        if (configCajaMetodoTransferencia) configCajaMetodoTransferencia.checked = metodosActivos.includes('TRANSFERENCIA');
        if (configCajaMetodoDeposito) configCajaMetodoDeposito.checked = metodosActivos.includes('DEPOSITO');
        if (configCajaPermitirIngresoManual) configCajaPermitirIngresoManual.checked = getConfigValue('caja', 'permitirIngresoManual') !== false;
        if (configCajaPermitirGastos) configCajaPermitirGastos.checked = getConfigValue('caja', 'permitirGastos') !== false;

        // Clientes
        if (configClientesCategoriaPorDefecto) configClientesCategoriaPorDefecto.value = getConfigValue('clientes', 'categoriaPorDefecto') || 'Mayoreo';
        if (configClientesCreditoMaximo) configClientesCreditoMaximo.value = getConfigValue('clientes', 'creditoMaximo') || 0;
        if (configClientesAlertaBajaExistencia) configClientesAlertaBajaExistencia.value = getConfigValue('clientes', 'alertaBajaExistencia') || 5000;
        if (configClientesAceptarOrdenesSinCliente) configClientesAceptarOrdenesSinCliente.checked = getConfigValue('clientes', 'aceptarOrdenesSinCliente') !== false;

        // Productos
        if (configProductosUnidadPorDefecto) configProductosUnidadPorDefecto.value = getConfigValue('productos', 'unidadPorDefecto') || 'pza';
        if (configProductosMargenPorDefecto) configProductosMargenPorDefecto.value = getConfigValue('productos', 'margenPorDefecto') || 30;
        if (configProductosAlertaBajaExistencia) configProductosAlertaBajaExistencia.value = getConfigValue('productos', 'alertaBajaExistencia') || 10;
        if (configProductosActualizarPreciosAutomatico) configProductosActualizarPreciosAutomatico.checked = getConfigValue('productos', 'actualizarPreciosAutomatico') !== false;

        // Proveedores
        if (configProveedoresDiasCredito) configProveedoresDiasCredito.value = getConfigValue('proveedores', 'diasCredito') || 30;
        if (configProveedoresMonedaPorDefecto) configProveedoresMonedaPorDefecto.value = getConfigValue('proveedores', 'monedaPorDefecto') || 'MXN';
        if (configProveedoresAlertaSaldoPendiente) configProveedoresAlertaSaldoPendiente.value = getConfigValue('proveedores', 'alertaSaldoPendiente') || 10000;
        if (configProveedoresAceptarSinEntre) configProveedoresAceptarSinEntre.checked = getConfigValue('proveedores', 'aceptarSinEntre') === true;

        // Insumos
        if (configInsumosUnidadPorDefecto) configInsumosUnidadPorDefecto.value = getConfigValue('insumos', 'unidadPorDefecto') || 'pza';
        if (configInsumosStockMinimoAlerta) configInsumosStockMinimoAlerta.value = getConfigValue('insumos', 'stockMinimoAlerta') || 50;
        if (configInsumosAceptarComprasConStock) configInsumosAceptarComprasConStock.checked = getConfigValue('insumos', 'aceptarComprasConStock') === true;
        if (configInsumosMostrarCostoProduccion) configInsumosMostrarCostoProduccion.checked = getConfigValue('insumos', 'mostrarCostoProduccion') !== false;

        // Almacén
        if (configAlmacenUbicacionPorDefecto) configAlmacenUbicacionPorDefecto.value = getConfigValue('almacen', 'ubicacionPorDefecto') || 'PISO_1';
        if (configAlmacenStockMinimoAlerta) configAlmacenStockMinimoAlerta.value = getConfigValue('almacen', 'stockMinimoAlerta') || 20;
        if (configAlmacenAceptarStockNegativo) configAlmacenAceptarStockNegativo.checked = getConfigValue('almacen', 'aceptarStockNegativo') === true;
        if (configAlmacenOverstockAlerta) configAlmacenOverstockAlerta.checked = getConfigValue('almacen', 'overstockAlerta') !== false;

        // Reportes
        if (configReportesRangoPorDefecto) configReportesRangoPorDefecto.value = getConfigValue('reportes', 'rangoPorDefecto') || 30;
        if (configReportesFormatoMoneda) configReportesFormatoMoneda.value = getConfigValue('reportes', 'formatoMoneda') || 'MXN';
        if (configReportesAccion1) configReportesAccion1.checked = getConfigValue('reportes', 'mostrarGraficos') !== false;
        if (configReportesAccion2) configReportesAccion2.checked = getConfigValue('reportes', 'actualizarKpisAutomatico') !== false;
        if (configPromocionesLista) {
            const lista = getConfigValue('promociones', 'lista');
            configPromocionesLista.value = (Array.isArray(lista) ? lista : []).join('\n');
        }
        if (configPermisosDescuentoUsuarios) {
            const lista = getConfigValue('permisos', 'descuentoUsuarios');
            configPermisosDescuentoUsuarios.value = (Array.isArray(lista) ? lista : []).join('\n');
        }
    };

    const saveConfiguracionesFromPopup = () => {
        // Caja
        setConfigValue('caja', 'nombre', configCajaNombre?.value?.trim() || 'Caja principal');
        setConfigValue('caja', 'id', configCajaId?.value?.trim() || 'CAJA-01');
        setConfigValue('caja', 'moneda', configCajaMoneda?.value || 'MXN');
        setConfigValue('caja', 'corteAutomatico', configCajaCorteAutomatico?.value || 'manual');
        setConfigValue('caja', 'bancoReceptor', configCajaBancoReceptor?.value?.trim() || 'BBVA México');
        const cuentasTxt = String(configCajaCuentasBeneficiario?.value || '');
        const cuentasArr = cuentasTxt.split(/\r?\n/).map((s) => s.trim()).filter(Boolean);
        setConfigValue('caja', 'cuentasBeneficiario', cuentasArr.length ? cuentasArr : ['BBVA - 0123456789']);
        const disenadoresTxt = String(configCajaDisenadores?.value || '');
        const disenadoresArr = disenadoresTxt.split(/\r?\n/).map((s) => s.trim()).filter(Boolean);
        setConfigValue('caja', 'disenadores', disenadoresArr.length ? disenadoresArr : ['DISEÑADOR 1']);
        setConfigValue('caja', 'fondoMinimo', Math.max(1, Number(configCajaFondoMinimo?.value || 1)));
        setConfigValue('caja', 'fuentePredeterminada', String(configCajaFuentePredeterminada?.value || 'EFECTIVO').toUpperCase());
        const metodosActivosCaja = [
            configCajaMetodoEfectivo?.checked ? 'EFECTIVO' : '',
            configCajaMetodoTarjeta?.checked ? 'TARJETA' : '',
            configCajaMetodoTransferencia?.checked ? 'TRANSFERENCIA' : '',
            configCajaMetodoDeposito?.checked ? 'DEPOSITO' : ''
        ].filter(Boolean);
        setConfigValue('caja', 'metodosActivos', metodosActivosCaja.length ? metodosActivosCaja : ['EFECTIVO']);
        setConfigValue('caja', 'permitirIngresoManual', configCajaPermitirIngresoManual?.checked ?? true);
        setConfigValue('caja', 'permitirGastos', configCajaPermitirGastos?.checked ?? true);

        // Clientes
        setConfigValue('clientes', 'categoriaPorDefecto', configClientesCategoriaPorDefecto?.value || 'Mayoreo');
        setConfigValue('clientes', 'creditoMaximo', Number(configClientesCreditoMaximo?.value) || 0);
        setConfigValue('clientes', 'alertaBajaExistencia', Number(configClientesAlertaBajaExistencia?.value) || 5000);
        setConfigValue('clientes', 'aceptarOrdenesSinCliente', configClientesAceptarOrdenesSinCliente?.checked ?? true);

        // Productos
        setConfigValue('productos', 'unidadPorDefecto', configProductosUnidadPorDefecto?.value || 'pza');
        setConfigValue('productos', 'margenPorDefecto', Number(configProductosMargenPorDefecto?.value) || 30);
        setConfigValue('productos', 'alertaBajaExistencia', Number(configProductosAlertaBajaExistencia?.value) || 10);
        setConfigValue('productos', 'actualizarPreciosAutomatico', configProductosActualizarPreciosAutomatico?.checked ?? true);

        // Proveedores
        setConfigValue('proveedores', 'diasCredito', Number(configProveedoresDiasCredito?.value) || 30);
        setConfigValue('proveedores', 'monedaPorDefecto', configProveedoresMonedaPorDefecto?.value || 'MXN');
        setConfigValue('proveedores', 'alertaSaldoPendiente', Number(configProveedoresAlertaSaldoPendiente?.value) || 10000);
        setConfigValue('proveedores', 'aceptarSinEntre', configProveedoresAceptarSinEntre?.checked ?? false);

        // Insumos
        setConfigValue('insumos', 'unidadPorDefecto', configInsumosUnidadPorDefecto?.value || 'pza');
        setConfigValue('insumos', 'stockMinimoAlerta', Number(configInsumosStockMinimoAlerta?.value) || 50);
        setConfigValue('insumos', 'aceptarComprasConStock', configInsumosAceptarComprasConStock?.checked ?? false);
        setConfigValue('insumos', 'mostrarCostoProduccion', configInsumosMostrarCostoProduccion?.checked ?? true);

        // Almacén
        setConfigValue('almacen', 'ubicacionPorDefecto', configAlmacenUbicacionPorDefecto?.value || 'PISO_1');
        setConfigValue('almacen', 'stockMinimoAlerta', Number(configAlmacenStockMinimoAlerta?.value) || 20);
        setConfigValue('almacen', 'aceptarStockNegativo', configAlmacenAceptarStockNegativo?.checked ?? false);
        setConfigValue('almacen', 'overstockAlerta', configAlmacenOverstockAlerta?.checked ?? true);

        // Reportes
        setConfigValue('reportes', 'rangoPorDefecto', Number(configReportesRangoPorDefecto?.value) || 30);
        setConfigValue('reportes', 'formatoMoneda', configReportesFormatoMoneda?.value || 'MXN');
        setConfigValue('reportes', 'mostrarGraficos', configReportesAccion1?.checked ?? true);
        setConfigValue('reportes', 'actualizarKpisAutomatico', configReportesAccion2?.checked ?? true);

        const promoLines = String(configPromocionesLista?.value || '')
            .split(/\r?\n/)
            .map((s) => s.trim())
            .filter(Boolean);
        setConfigValue('promociones', 'lista', promoLines);

        const permisoLines = String(configPermisosDescuentoUsuarios?.value || '')
            .split(/\r?\n/)
            .map((s) => s.trim())
            .filter(Boolean);
        setConfigValue('permisos', 'descuentoUsuarios', permisoLines);

        saveSystemConfig();
        cajaSettings.nombre = String(getConfigValue('caja', 'nombre') || 'Caja principal');
        cajaSettings.id = String(getConfigValue('caja', 'id') || 'CAJA-01');
        saveCajaSettings();
        syncCajaFuenteOptions();
        renderCajaUI();
        renderDisenadoresSelect();
        notifyInfo('Configuraciones guardadas correctamente.', 'Configuraciones');
    };

    const openConfiguracionesPopup = () => {
        if (!popupConfiguraciones) return;
        loadSystemConfig();
        renderConfiguracionesPopup();
        switchConfigTab('caja');
        popupConfiguraciones.style.display = 'flex';
        popupConfiguraciones.setAttribute('aria-hidden', 'false');
        document.body.classList.add('popup-open');
        document.documentElement.classList.add('popup-open');
    };

    const loadCajaSettings = () => {
        try {
            const parsed = JSON.parse(localStorage.getItem(CAJA_SETTINGS_KEY) || '{}');
            cajaSettings = {
                nombre: String(parsed.nombre || 'Caja principal').trim() || 'Caja principal',
                id: String(parsed.id || 'CAJA-01').trim() || 'CAJA-01'
            };
        } catch (_) {
            cajaSettings = { nombre: 'Caja principal', id: 'CAJA-01' };
        }
    };

    const saveCajaSettings = () => {
        try {
            localStorage.setItem(CAJA_SETTINGS_KEY, JSON.stringify(cajaSettings));
        } catch (_) {}
    };

    const loadCajaMovimientos = () => {
        try {
            const parsed = JSON.parse(localStorage.getItem(CAJA_MOVS_KEY) || '[]');
            cajaMovimientos = Array.isArray(parsed) ? parsed : [];
        } catch (_) {
            cajaMovimientos = [];
        }
    };

    const saveCajaMovimientos = () => {
        try {
            localStorage.setItem(CAJA_MOVS_KEY, JSON.stringify(cajaMovimientos));
        } catch (_) {}
    };

    const loadCajaAperturas = () => {
        try {
            const parsed = JSON.parse(localStorage.getItem(CAJA_APERTURAS_KEY) || '{}');
            cajaAperturas = (parsed && typeof parsed === 'object') ? parsed : {};
        } catch (_) {
            cajaAperturas = {};
        }
    };

    const saveCajaAperturas = () => {
        try {
            localStorage.setItem(CAJA_APERTURAS_KEY, JSON.stringify(cajaAperturas));
        } catch (_) {}
    };

    const getUsuarioLogeado = () => {
        const candidates = [
            localStorage.getItem('mock_usuario_logeado') || '',
            localStorage.getItem('logged_user_name') || '',
            el('ordenVendedor')?.value || '',
            el('ordenDisenador')?.value || ''
        ].map((v) => String(v || '').trim()).filter(Boolean);
        return candidates[0] || 'Usuario en turno';
    };

    const getCajaMetodosActivos = () => {
        const configured = getConfigValue('caja', 'metodosActivos');
        const base = Array.isArray(configured) && configured.length
            ? configured
            : ['EFECTIVO', 'TARJETA', 'TRANSFERENCIA', 'DEPOSITO'];
        const allowed = ['EFECTIVO', 'TARJETA', 'TRANSFERENCIA', 'DEPOSITO'];
        const normalized = base
            .map((m) => String(m || '').toUpperCase().trim())
            .filter((m) => allowed.includes(m));
        return normalized.length ? normalized : ['EFECTIVO'];
    };

    const syncCajaFuenteOptions = () => {
        if (!cajaGastoFuente) return;
        const active = getCajaMetodosActivos();
        const selected = String(cajaGastoFuente.value || '').toUpperCase();
        cajaGastoFuente.innerHTML = active.map((metodo) => {
            const label = metodo === 'DEPOSITO' ? 'Depósito' : `${metodo.charAt(0)}${metodo.slice(1).toLowerCase()}`;
            return `<option value="${metodo}">${label}</option>`;
        }).join('');
        const fallback = String(getConfigValue('caja', 'fuentePredeterminada') || 'EFECTIVO').toUpperCase();
        if (active.includes(selected)) cajaGastoFuente.value = selected;
        else cajaGastoFuente.value = active.includes(fallback) ? fallback : active[0];
    };

    const ensureCajaFondoDelDia = () => {
        const day = todayISO();
        const minFondo = Math.max(1, Number(getConfigValue('caja', 'fondoMinimo') || 1));
        const current = Number(cajaAperturas[day]);
        if (Number.isFinite(current) && current >= minFondo) return current;
        let fondo = NaN;
        while (!Number.isFinite(fondo) || fondo < minFondo) {
            const raw = prompt(`Ingresa el fondo inicial de caja para hoy (mínimo ${formatMoney(minFondo)}):`, String(minFondo));
            if (raw === null) {
                fondo = minFondo;
                break;
            }
            fondo = Number(raw);
            if (!Number.isFinite(fondo) || fondo < minFondo) {
                notifyError(`El fondo inicial debe ser mayor o igual a ${formatMoney(minFondo)}.`, 'Caja');
            }
        }
        cajaAperturas[day] = Math.max(minFondo, fondo);
        saveCajaAperturas();
        return cajaAperturas[day];
    };

    const getCajaResumenDelDia = () => {
        const day = todayISO();
        const fondo = Math.max(1, Number(cajaAperturas[day] || 1));
        const ventasHoy = misPedidosData.filter((r) => r.tipo === 'venta' && String(r.fechaEmitida || '').slice(0, 10) === day);
        const movsHoy = cajaMovimientos.filter((m) => String(m.fecha || '').slice(0, 10) === day);

        const ingresos = { EFECTIVO: 0, TARJETA: 0, TRANSFERENCIA: 0, DEPOSITO: 0 };
        ventasHoy.forEach((r) => {
            const metodo = String(r.metodoPago || 'EFECTIVO').toUpperCase();
            const amount = Math.max(0, Number(r.anticipo || 0));
            if (amount <= 0) return;
            if (metodo in ingresos) ingresos[metodo] += amount;
            else ingresos.EFECTIVO += amount;
        });

        movsHoy.forEach((m) => {
            const metodo = String(m.fuente || 'EFECTIVO').toUpperCase();
            const amount = Math.max(0, Number(m.monto || 0));
            if (!(metodo in ingresos)) return;
            if (m.tipo === 'ingreso') ingresos[metodo] += amount;
            if (m.tipo === 'gasto') ingresos[metodo] -= amount;
        });

        const gastos = movsHoy
            .filter((m) => m.tipo === 'gasto')
            .reduce((acc, m) => acc + Math.max(0, Number(m.monto || 0)), 0);

        return {
            day,
            fondo,
            efectivo: ingresos.EFECTIVO,
            tarjeta: ingresos.TARJETA,
            transferencia: ingresos.TRANSFERENCIA,
            deposito: ingresos.DEPOSITO,
            gastos,
            totalNeto: fondo + ingresos.EFECTIVO + ingresos.TARJETA + ingresos.TRANSFERENCIA + ingresos.DEPOSITO
        };
    };

    const getDisponiblePorFuente = (fuente) => {
        const r = getCajaResumenDelDia();
        if (fuente === 'TARJETA') return Math.max(0, r.tarjeta);
        if (fuente === 'TRANSFERENCIA') return Math.max(0, r.transferencia);
        if (fuente === 'DEPOSITO') return Math.max(0, r.deposito);
        return Math.max(0, r.fondo + r.efectivo);
    };

    const renderCajaUI = () => {
        if (!popupCaja) return;
        loadMisPedidos();
        syncCajaFuenteOptions();
        const resumen = getCajaResumenDelDia();
        const usuario = getUsuarioLogeado();

        if (cajaNombreLabel) cajaNombreLabel.textContent = cajaSettings.nombre;
        if (cajaIdLabel) cajaIdLabel.textContent = cajaSettings.id;
        if (cajaUsuarioLabel) cajaUsuarioLabel.textContent = usuario;
        if (cajaNombreLabelGasto) cajaNombreLabelGasto.textContent = cajaSettings.nombre;
        if (cajaIdLabelGasto) cajaIdLabelGasto.textContent = cajaSettings.id;
        if (cajaUsuarioLabelGasto) cajaUsuarioLabelGasto.textContent = usuario;

        if (cajaKpiFondo) cajaKpiFondo.textContent = formatMoney(resumen.fondo);
        if (cajaKpiEfectivo) cajaKpiEfectivo.textContent = formatMoney(resumen.efectivo);
        if (cajaKpiTarjeta) cajaKpiTarjeta.textContent = formatMoney(resumen.tarjeta);
        if (cajaKpiTransferencia) cajaKpiTransferencia.textContent = formatMoney(resumen.transferencia);
        if (cajaKpiDeposito) cajaKpiDeposito.textContent = formatMoney(resumen.deposito);
        if (cajaKpiGastos) cajaKpiGastos.textContent = formatMoney(resumen.gastos);

        if (cajaTabCorte) cajaTabCorte.classList.toggle('active', cajaTabActiva === 'corte');
        if (cajaTabGasto) cajaTabGasto.classList.toggle('active', cajaTabActiva === 'gasto');
        if (cajaPanelCorte) cajaPanelCorte.style.display = cajaTabActiva === 'corte' ? '' : 'none';
        if (cajaPanelGasto) cajaPanelGasto.style.display = cajaTabActiva === 'gasto' ? '' : 'none';

        const fuente = String(cajaGastoFuente?.value || 'EFECTIVO').toUpperCase();
        const disponible = getDisponiblePorFuente(fuente);
        if (cajaDisponibleMonto) {
            cajaDisponibleMonto.textContent = `Dinero disponible: ${formatMoney(disponible)}`;
            cajaDisponibleMonto.classList.toggle('blocked', disponible <= 0);
        }

        const permitirIngreso = getConfigValue('caja', 'permitirIngresoManual') !== false;
        const permitirGasto = getConfigValue('caja', 'permitirGastos') !== false;
        if (cajaBtnIngresarDinero) cajaBtnIngresarDinero.disabled = !permitirIngreso;
        if (cajaBtnRealizarGasto) cajaBtnRealizarGasto.disabled = !permitirGasto;
    };

    const printCajaTicket = () => {
        const r = getCajaResumenDelDia();
        const usuario = getUsuarioLogeado();
        const now = new Date();
        const stamp = `${now.toLocaleDateString('es-MX')} ${now.toLocaleTimeString('es-MX')}`;
        const html = `<!doctype html><html><head><meta charset="utf-8"><title>Corte de Caja</title>
            <style>
                body{font-family:Consolas,monospace;padding:10px;color:#111}
                h1{font-size:16px;margin:0 0 8px}
                .line{display:flex;justify-content:space-between;font-size:13px;padding:2px 0;border-bottom:1px dotted #999}
                .meta{font-size:12px;margin:2px 0}
                .total{font-weight:700;border-top:2px solid #111;margin-top:8px;padding-top:4px}
            </style></head><body>
            <h1>CORTE DE CAJA</h1>
            <div class="meta">Caja: ${cajaSettings.nombre}</div>
            <div class="meta">ID caja: ${cajaSettings.id}</div>
            <div class="meta">Usuario: ${usuario}</div>
            <div class="meta">Fecha: ${stamp}</div>
            <div class="line"><span>Fondo</span><span>${formatMoney(r.fondo)}</span></div>
            <div class="line"><span>Efectivo</span><span>${formatMoney(r.efectivo)}</span></div>
            <div class="line"><span>Tarjeta</span><span>${formatMoney(r.tarjeta)}</span></div>
            <div class="line"><span>Transferencias</span><span>${formatMoney(r.transferencia)}</span></div>
            <div class="line"><span>Depósitos</span><span>${formatMoney(r.deposito)}</span></div>
            <div class="line"><span>Gastos</span><span>${formatMoney(r.gastos)}</span></div>
            <div class="line total"><span>Total neto</span><span>${formatMoney(r.totalNeto)}</span></div>
            </body></html>`;
        const w = window.open('', '_blank', 'width=420,height=700');
        if (!w) {
            notifyError('No se pudo abrir la ventana de impresión.', 'Caja');
            return;
        }
        w.document.open();
        w.document.write(html);
        w.document.close();
        w.focus();
        w.print();
    };

    const openCajaPopup = () => {
        if (!popupCaja) return;
        loadCajaSettings();
        loadCajaMovimientos();
        loadCajaAperturas();
        ensureCajaFondoDelDia();
        cajaTabActiva = 'corte';
        popupCaja.style.display = 'flex';
        popupCaja.setAttribute('aria-hidden', 'false');
        document.body.classList.add('popup-open');
        document.documentElement.classList.add('popup-open');
        renderCajaUI();
    };

    const closeCajaPopup = () => {
        if (!popupCaja) return;
        popupCaja.style.display = 'none';
        popupCaja.setAttribute('aria-hidden', 'true');
        if (popupListado?.style.display !== 'flex' && popupAccess?.style.display !== 'flex' && popupDesignTracking?.style.display !== 'flex' && popupMisPedidos?.style.display !== 'flex' && popupAjustesTabuladores?.style.display !== 'flex' && popupProdTabulador?.style.display !== 'flex' && popupProductos?.style.display !== 'flex' && popupCalendario?.style.display !== 'flex' && popupClientesModulo?.style.display !== 'flex') {
            document.body.classList.remove('popup-open');
            document.documentElement.classList.remove('popup-open');
        }
    };

    window.openCajaPopupGlobal = openCajaPopup;

    const loadCalendarioAlertas = () => {
        try {
            const parsed = JSON.parse(localStorage.getItem(CAL_ALERTS_KEY) || '{}');
            calendarioAlertas = (parsed && typeof parsed === 'object') ? parsed : {};
        } catch (_) {
            calendarioAlertas = {};
        }
    };

    const saveCalendarioAlertas = () => {
        try {
            localStorage.setItem(CAL_ALERTS_KEY, JSON.stringify(calendarioAlertas));
        } catch (_) {}
    };

    const parseISODateLocal = (isoText) => {
        const txt = String(isoText || '').trim();
        if (!/^\d{4}-\d{2}-\d{2}$/.test(txt)) return null;
        const [y, m, d] = txt.split('-').map((n) => Number(n));
        const dt = new Date(y, m - 1, d);
        return Number.isFinite(dt.getTime()) ? dt : null;
    };

    const startOfDay = (dt) => new Date(dt.getFullYear(), dt.getMonth(), dt.getDate());
    const diffDays = (a, b) => Math.round((startOfDay(a).getTime() - startOfDay(b).getTime()) / 86400000);

    const normalizeStatus = (value) => String(value || '')
        .trim()
        .toLowerCase()
        .replace(/á/g, 'a')
        .replace(/é/g, 'e')
        .replace(/í/g, 'i')
        .replace(/ó/g, 'o')
        .replace(/ú/g, 'u');

    const isPendientePorEntregar = (status) => {
        const s = normalizeStatus(status).replace(/\s+/g, '-');
        return s === 'pendiente-por-entregar';
    };

    const isEntregado = (status) => normalizeStatus(status) === 'entregado';

    const buildCalendarioQueue = () => {
        const today = new Date();
        const rows = misPedidosData
            .filter((r) => r.tipo === 'venta')
            .map((row) => {
                const fechaEntrega = parseISODateLocal(row.fechaEntrega || '');
                if (!fechaEntrega) return null;
                const daysLeft = diffDays(fechaEntrega, today);
                const status = String(row.estatusProduccion || '').trim();
                const pendienteEntrega = isPendientePorEntregar(status);
                const delivered = isEntregado(status);
                let level = 'normal';
                if (!delivered) {
                    if (daysLeft < 0) level = 'overdue';
                    else if (!pendienteEntrega && daysLeft <= 1) level = 'high';
                    else if (!pendienteEntrega && daysLeft === 2) level = 'mid';
                }
                return {
                    ...row,
                    fechaEntregaDate: fechaEntrega,
                    daysLeft,
                    urgency: level,
                    pendienteEntrega,
                    delivered,
                    folioSafe: String(row.folio || row.id || 'SIN-FOLIO')
                };
            })
            .filter(Boolean)
            .filter((r) => !r.delivered)
            .sort((a, b) => {
                const weight = { overdue: 0, high: 1, mid: 2, normal: 3 };
                const wa = weight[a.urgency] ?? 3;
                const wb = weight[b.urgency] ?? 3;
                if (wa !== wb) return wa - wb;
                if (a.daysLeft !== b.daysLeft) return a.daysLeft - b.daysLeft;
                const feA = startOfDay(a.fechaEntregaDate).getTime();
                const feB = startOfDay(b.fechaEntregaDate).getTime();
                if (feA !== feB) return feA - feB;
                const emA = parseISODateLocal(a.fechaEmitida || '')?.getTime() || 0;
                const emB = parseISODateLocal(b.fechaEmitida || '')?.getTime() || 0;
                return emA - emB;
            });

        return rows;
    };

    const renderCalendarioMonth = (queue = []) => {
        if (!calGridDays || !calMesLabel) return;
        const view = new Date(calViewDate.getFullYear(), calViewDate.getMonth(), 1);
        const y = view.getFullYear();
        const m = view.getMonth();
        const now = new Date();
        const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        calMesLabel.textContent = view.toLocaleDateString('es-MX', { month: 'long', year: 'numeric' }).toUpperCase();

        const first = new Date(y, m, 1);
        const last = new Date(y, m + 1, 0);
        const firstIdx = (first.getDay() + 6) % 7;
        const daysInMonth = last.getDate();
        const prevLast = new Date(y, m, 0).getDate();

        const byDay = new Map();
        queue.forEach((r) => {
            if (r.fechaEntregaDate.getFullYear() !== y || r.fechaEntregaDate.getMonth() !== m) return;
            const d = r.fechaEntregaDate.getDate();
            if (!byDay.has(d)) byDay.set(d, []);
            byDay.get(d).push(r);
        });

        const cells = [];
        for (let i = 0; i < firstIdx; i += 1) {
            const num = prevLast - firstIdx + i + 1;
            cells.push(`<div class="cal-day muted"><span class="num">${num}</span></div>`);
        }

        for (let d = 1; d <= daysInMonth; d += 1) {
            const list = byDay.get(d) || [];
            const count = list.length;
            const levels = Array.from(new Set(list.map((r) => r.urgency))).sort((a, b) => {
                const w = { overdue: 0, high: 1, mid: 2, normal: 3 };
                return (w[a] ?? 9) - (w[b] ?? 9);
            });
            const dots = levels.slice(0, 3).map((lv) => `<i class="cal-dot ${lv === 'normal' ? 'normal' : lv}"></i>`).join('');
            const cls = ['cal-day'];
            const iso = `${y}-${String(m + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
            const thisDate = new Date(y, m, d);
            if (!calSelectedDate && thisDate.getTime() === today.getTime()) cls.push('today');
            if (calSelectedDate && calSelectedDate === iso) cls.push('selected');
            cells.push(`<button type="button" class="${cls.join(' ')}" data-cal-date="${iso}"><div class="cal-topline"><span class="num">${d}</span>${count > 0 ? `<span class="cal-count-badge">${count}</span>` : ''}</div><div class="cal-dot-wrap">${dots}</div></button>`);
        }

        const totalCells = Math.ceil(cells.length / 7) * 7;
        for (let i = cells.length; i < totalCells; i += 1) {
            const num = i - (firstIdx + daysInMonth) + 1;
            cells.push(`<div class="cal-day muted"><span class="num">${num}</span></div>`);
        }

        calGridDays.innerHTML = cells.join('');
    };

    const renderCalendarioLista = (queue = []) => {
        if (!calListaBody) return;
        const today = startOfDay(new Date());
        const plus7 = new Date(today);
        plus7.setDate(plus7.getDate() + 7);
        const plus15 = new Date(today);
        plus15.setDate(plus15.getDate() + 15);

        let filtered = queue.slice();
        if (calScopeMode === 'selected') {
            filtered = filtered.filter((r) => String(r.fechaEntrega || '').slice(0, 10) === calSelectedDate);
        } else if (calScopeMode === 'today') {
            filtered = filtered.filter((r) => String(r.fechaEntrega || '').slice(0, 10) === todayISO());
        } else if (calScopeMode === 'week') {
            filtered = filtered.filter((r) => {
                const t = startOfDay(r.fechaEntregaDate).getTime();
                return t >= today.getTime() && t <= plus7.getTime();
            });
        } else if (calScopeMode === 'next15') {
            filtered = filtered.filter((r) => {
                const t = startOfDay(r.fechaEntregaDate).getTime();
                return t >= today.getTime() && t <= plus15.getTime();
            });
        } else if (calScopeMode === 'month') {
            filtered = filtered.filter((r) => {
                const d = r.fechaEntregaDate;
                return d.getFullYear() === calViewDate.getFullYear() && d.getMonth() === calViewDate.getMonth();
            });
        } else if (calScopeMode === 'overdue') {
            filtered = filtered.filter((r) => Number(r.daysLeft) < 0);
        }

        if (calStatusMode !== 'all') {
            filtered = filtered.filter((r) => String(r.estatusProduccion || '').toLowerCase() === calStatusMode);
        }

        const search = String(calSearchTerm || '').trim().toLowerCase();
        if (search) {
            filtered = filtered.filter((r) => {
                const blob = `${r.folioSafe || ''} ${r.clienteNombre || ''} ${r.telefono || ''} ${r.productoNombre || r.producto || ''}`.toLowerCase();
                return blob.includes(search);
            });
        }

        // Orden fijo obligatorio: de más urgente a menos urgente.
        filtered.sort((a, b) => {
            const w = { overdue: 0, high: 1, mid: 2, normal: 3 };
            const wa = w[a.urgency] ?? 3;
            const wb = w[b.urgency] ?? 3;
            if (wa !== wb) return wa - wb;
            if (a.daysLeft !== b.daysLeft) return a.daysLeft - b.daysLeft;
            const feA = startOfDay(a.fechaEntregaDate).getTime();
            const feB = startOfDay(b.fechaEntregaDate).getTime();
            if (feA !== feB) return feA - feB;
            const emA = parseISODateLocal(a.fechaEmitida || '')?.getTime() || 0;
            const emB = parseISODateLocal(b.fechaEmitida || '')?.getTime() || 0;
            return emA - emB;
        });

        if (calListSub) {
            calListSub.textContent = 'Orden forzoso: de más urgente a menos urgente';
        }

        if (calQuickStats) {
            const total = queue.length;
            const urgentes = queue.filter((r) => r.urgency === 'high' || r.urgency === 'overdue').length;
            const vencidos = queue.filter((r) => r.urgency === 'overdue').length;
            const hoy = queue.filter((r) => String(r.fechaEntrega || '').slice(0, 10) === todayISO()).length;
            calQuickStats.innerHTML = [
                `<span class="cal-stat-chip">Pendientes <b>${total}</b></span>`,
                `<span class="cal-stat-chip">Urgentes <b>${urgentes}</b></span>`,
                `<span class="cal-stat-chip">Vencidos <b>${vencidos}</b></span>`,
                `<span class="cal-stat-chip">Entrega hoy <b>${hoy}</b></span>`,
                `<span class="cal-stat-chip">Mostrando <b>${filtered.length}</b></span>`
            ].join('');
        }

        if (calFiltroFecha) {
            if (calScopeMode === 'selected' && calSelectedDate) {
                calFiltroFecha.style.display = 'inline-flex';
                const d = parseISODateLocal(calSelectedDate);
                const txt = d ? d.toLocaleDateString('es-MX') : calSelectedDate;
                if (calFiltroFechaText) calFiltroFechaText.textContent = `Filtrado: ${txt}`;
            } else if (calScopeMode === 'today') {
                calFiltroFecha.style.display = 'inline-flex';
                if (calFiltroFechaText) calFiltroFechaText.textContent = 'Filtrado: solo hoy';
            } else if (calScopeMode === 'week') {
                calFiltroFecha.style.display = 'inline-flex';
                if (calFiltroFechaText) calFiltroFechaText.textContent = 'Filtrado: próximos 7 días';
            } else if (calScopeMode === 'next15') {
                calFiltroFecha.style.display = 'inline-flex';
                if (calFiltroFechaText) calFiltroFechaText.textContent = 'Filtrado: próximos 15 días';
            } else if (calScopeMode === 'month') {
                calFiltroFecha.style.display = 'inline-flex';
                if (calFiltroFechaText) {
                    const txt = new Date(calViewDate.getFullYear(), calViewDate.getMonth(), 1)
                        .toLocaleDateString('es-MX', { month: 'long', year: 'numeric' });
                    calFiltroFechaText.textContent = `Filtrado: ${txt}`;
                }
            } else if (calScopeMode === 'overdue') {
                calFiltroFecha.style.display = 'inline-flex';
                if (calFiltroFechaText) calFiltroFechaText.textContent = 'Filtrado: solo vencidos';
            } else {
                calFiltroFecha.style.display = 'none';
            }
        }

        if (!filtered.length) {
            calListaBody.innerHTML = '<tr><td colspan="14" style="text-align:center;color:#6b7280;padding:14px;">No hay pedidos para esta vista.</td></tr>';
            return;
        }
        const labelUrg = {
            overdue: 'Vencido',
            high: '1 día o menos',
            mid: '2 días',
            normal: 'En tiempo'
        };
        calListaBody.innerHTML = filtered.map((r) => {
            const rowCls = r.urgency === 'overdue' ? 'cal-row-overdue' : (r.urgency === 'high' ? 'cal-row-high' : (r.urgency === 'mid' ? 'cal-row-mid' : ''));
            const producto = String(r.productoNombre || r.producto || r.productoActual || '-');
            const dLabel = r.fechaEntregaDate.toLocaleDateString('es-MX');
            const emitida = parseISODateLocal(r.fechaEmitida || '')?.toLocaleDateString('es-MX') || '-';
            const days = r.daysLeft < 0 ? `Atrasado ${Math.abs(r.daysLeft)}d` : (r.daysLeft === 0 ? 'Hoy' : `${r.daysLeft}d`);
            const estatus = String(r.estatusProduccion || 'pendiente').replace(/-/g, ' ');
            return `<tr class="${rowCls}">
                <td><span class="urg-chip ${r.urgency}">${labelUrg[r.urgency] || 'En tiempo'}</span></td>
                <td>${dLabel}</td>
                <td>${days}</td>
                <td>${emitida}</td>
                <td>${escapeHtml(r.folioSafe)}</td>
                <td>${escapeHtml(r.clienteNombre || 'Sin cliente')}</td>
                <td>${escapeHtml(r.telefono || '-')}</td>
                <td>${escapeHtml(r.disenador || '-')}</td>
                <td>${escapeHtml(r.vendedor || '-')}</td>
                <td>${escapeHtml(producto)}</td>
                <td>${formatMoney(Number(r.subtotal || 0))}</td>
                <td>${formatMoney(Number(r.total || 0))}</td>
                <td>${formatMoney(Number(r.anticipo || 0))}</td>
                <td>${formatMoney(Number(r.adeudoCliente || 0))}</td>
                <td>${escapeHtml(estatus)}</td>
            </tr>`;
        }).join('');
    };

    const runCalendarioAlertas = (queue = []) => {
        loadCalendarioAlertas();
        const ordered = queue.filter((r) => ['mid', 'high', 'overdue'].includes(r.urgency));
        if (!ordered.length) return;
        const dayKey = todayISO();
        for (const row of ordered) {
            const alertKey = `${dayKey}|${row.folioSafe}|${row.urgency}`;
            if (calendarioAlertas[alertKey]) continue;
            let msg = '';
            if (row.urgency === 'mid') {
                msg = `El pedido ${row.folioSafe} se entrega en 2 días y no está en estatus pendiente por entregar.`;
            } else if (row.urgency === 'high') {
                msg = `ALERTA ALTA: el pedido ${row.folioSafe} se entrega en 1 día (o hoy) y aún no está en pendiente por entregar.`;
            } else {
                msg = `ALERTA CRÍTICA: el pedido ${row.folioSafe} ya venció y no está entregado.`;
            }
            notifyError(msg, 'Calendario de entregas');
            calendarioAlertas[alertKey] = 1;
            saveCalendarioAlertas();
            break;
        }
    };

    const renderCalendarioUI = () => {
        if (!popupCalendario) return;
        loadMisPedidos();
        const queue = buildCalendarioQueue();
        renderCalendarioMonth(queue);
        renderCalendarioLista(queue);
        runCalendarioAlertas(queue);
    };

    const openCalendarioPopup = () => {
        if (!popupCalendario) return;
        calViewDate = new Date();
        calSelectedDate = todayISO();
        calScopeMode = 'selected';
        calStatusMode = 'all';
        calSearchTerm = '';
        if (calScopeSelect) calScopeSelect.value = calScopeMode;
        if (calStatusSelect) calStatusSelect.value = calStatusMode;
        if (calSearchInput) calSearchInput.value = calSearchTerm;
        popupCalendario.style.display = 'flex';
        popupCalendario.setAttribute('aria-hidden', 'false');
        document.body.classList.add('popup-open');
        document.documentElement.classList.add('popup-open');
        renderCalendarioUI();
    };

    const closeCalendarioPopup = () => {
        if (!popupCalendario) return;
        popupCalendario.style.display = 'none';
        popupCalendario.setAttribute('aria-hidden', 'true');
        if (popupListado?.style.display !== 'flex' && popupAccess?.style.display !== 'flex' && popupDesignTracking?.style.display !== 'flex' && popupMisPedidos?.style.display !== 'flex' && popupAjustesTabuladores?.style.display !== 'flex' && popupProdTabulador?.style.display !== 'flex' && popupProductos?.style.display !== 'flex' && popupCaja?.style.display !== 'flex' && popupClientesModulo?.style.display !== 'flex') {
            document.body.classList.remove('popup-open');
            document.documentElement.classList.remove('popup-open');
        }
    };

    window.openCalendarioPopupGlobal = openCalendarioPopup;

    const escCliMod = (value) => String(value == null ? '' : value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');

    const mkClienteModuloId = () => `CL-${Date.now().toString(36).toUpperCase()}-${Math.floor(Math.random() * 90 + 10)}`;

    const seedClientesModulo = () => ([
        {
            id: 'CL-001',
            nombre: 'Alma Cruz',
            empresa: 'Boutique Alma',
            telefono: '9511012233',
            correo: 'alma.cruz@correo.com',
            calle: 'Av. Juarez',
            colonia: 'Centro',
            numero: 'Int 2, Ext 18',
            pais: 'Mexico',
            ciudad: 'Oaxaca de Juarez',
            estado: 'Oaxaca',
            cp: '68000',
            razonSocial: 'Alma Cruz Boutique SA de CV',
            rfc: 'ACB210101AB1',
            referenciaBancaria: 'BBVA 01234',
            tipoCliente: 'Publico en general'
        },
        {
            id: 'CL-002',
            nombre: 'Luis Mendoza',
            empresa: 'Mendoza Publicidad',
            telefono: '9513342210',
            correo: 'luis.mendoza@correo.com',
            calle: 'Calzada Madero',
            colonia: 'Reforma',
            numero: 'Ext 230',
            pais: 'Mexico',
            ciudad: 'Oaxaca de Juarez',
            estado: 'Oaxaca',
            cp: '68050',
            razonSocial: 'Mendoza Publicidad SA de CV',
            rfc: 'MPS220202CD2',
            referenciaBancaria: 'Santander 44556',
            tipoCliente: 'Revendedor'
        }
    ]);

    const saveClientesModulo = () => {
        try {
            localStorage.setItem(CLIENTES_MODULO_KEY, JSON.stringify(clientesModuloData));
        } catch (_) {}
    };

    const loadClientesModulo = () => {
        try {
            const raw = localStorage.getItem(CLIENTES_MODULO_KEY);
            const parsed = JSON.parse(raw || '[]');
            if (Array.isArray(parsed) && parsed.length) {
                clientesModuloData = parsed.map((c) => ({
                    id: String(c.id || mkClienteModuloId()).trim(),
                    nombre: String(c.nombre || '').trim(),
                    empresa: String(c.empresa || '').trim(),
                    telefono: String(c.telefono || '').trim(),
                    correo: String(c.correo || '').trim(),
                    calle: String(c.calle || '').trim(),
                    colonia: String(c.colonia || '').trim(),
                    numero: String(c.numero || '').trim(),
                    pais: String(c.pais || 'Mexico').trim() || 'Mexico',
                    ciudad: String(c.ciudad || '').trim(),
                    estado: String(c.estado || '').trim(),
                    cp: String(c.cp || '').trim(),
                    razonSocial: String(c.razonSocial || '').trim(),
                    rfc: String(c.rfc || '').trim(),
                    referenciaBancaria: String(c.referenciaBancaria || '').trim(),
                    tipoCliente: String(c.tipoCliente || 'Publico en general').trim() || 'Publico en general'
                }));
                return;
            }
        } catch (_) {}
        clientesModuloData = seedClientesModulo();
        saveClientesModulo();
    };

    const updateClientesModuloButtons = () => {
        const hasSelection = Boolean(clientesModuloSelectedId);
        if (clientesmodEdit) clientesmodEdit.disabled = !hasSelection;
        if (clientesmodDelete) clientesmodDelete.disabled = !hasSelection;
    };

    const renderClientesModulo = () => {
        if (!clientesmodTableBody) return;
        const term = String(clientesmodSearch?.value || '').trim().toLowerCase();
        const rows = clientesModuloData.filter((c) => {
            if (!term) return true;
            return [
                c.id,
                c.nombre,
                c.empresa,
                c.telefono,
                c.correo,
                c.tipoCliente,
                c.rfc
            ].some((v) => String(v || '').toLowerCase().includes(term));
        });

        if (!rows.length) {
            clientesmodTableBody.innerHTML = '<tr><td colspan="4" class="clientesmod-empty">No hay clientes para este filtro.</td></tr>';
            if (clientesmodConteo) clientesmodConteo.textContent = `Total de clientes: ${clientesModuloData.length}`;
            updateClientesModuloButtons();
            return;
        }

        clientesmodTableBody.innerHTML = rows.map((c) => {
            const selected = c.id === clientesModuloSelectedId ? ' clientesmod-row-selected' : '';
            return `<tr class="${selected}" data-cli-id="${escCliMod(c.id)}"><td>${escCliMod(c.id)}</td><td>${escCliMod(c.nombre)}</td><td>${escCliMod(c.correo)}</td><td>${escCliMod(c.tipoCliente)}</td></tr>`;
        }).join('');

        if (clientesmodConteo) clientesmodConteo.textContent = `Total de clientes: ${clientesModuloData.length}`;

        clientesmodTableBody.querySelectorAll('[data-cli-id]').forEach((row) => {
            row.addEventListener('click', () => {
                const id = String(row.getAttribute('data-cli-id') || '');
                if (!id) return;
                clientesModuloSelectedId = id;
                renderClientesModulo();
            });
        });

        updateClientesModuloButtons();
    };

    const closeClientesFormPopup = () => {
        if (!popupClientesForm) return;
        popupClientesForm.style.display = 'none';
        popupClientesForm.setAttribute('aria-hidden', 'true');
        clientesModuloEditingId = '';
        if (cliFormSave) cliFormSave.textContent = 'Guardar cliente';
        ordenClienteFormMode = '';
    };

    const openClientesFormPopup = (mode, cliente) => {
        if (!popupClientesForm) return;
        const isEdit = mode === 'edit';
        clientesModuloEditingId = isEdit ? String(cliente?.id || '') : '';

        if (clientesformTitulo) clientesformTitulo.textContent = isEdit ? 'Editar cliente' : 'Agregar cliente';
        if (cliFormId) cliFormId.value = isEdit ? String(cliente?.id || '') : mkClienteModuloId();
        if (cliFormNombre) cliFormNombre.value = isEdit ? String(cliente?.nombre || '') : '';
        if (cliFormEmpresa) cliFormEmpresa.value = isEdit ? String(cliente?.empresa || '') : '';
        if (cliFormTelefono) cliFormTelefono.value = isEdit ? String(cliente?.telefono || '') : '';
        if (cliFormCorreo) cliFormCorreo.value = isEdit ? String(cliente?.correo || '') : '';
        if (cliFormCalle) cliFormCalle.value = isEdit ? String(cliente?.calle || '') : '';
        if (cliFormColonia) cliFormColonia.value = isEdit ? String(cliente?.colonia || '') : '';
        if (cliFormNumero) cliFormNumero.value = isEdit ? String(cliente?.numero || '') : '';
        if (cliFormPais) cliFormPais.value = isEdit ? String(cliente?.pais || 'Mexico') : 'Mexico';
        if (cliFormCiudad) cliFormCiudad.value = isEdit ? String(cliente?.ciudad || '') : '';
        if (cliFormEstado) cliFormEstado.value = isEdit ? String(cliente?.estado || '') : '';
        if (cliFormCp) cliFormCp.value = isEdit ? String(cliente?.cp || '') : '';
        if (cliFormRazonSocial) cliFormRazonSocial.value = isEdit ? String(cliente?.razonSocial || '') : '';
        if (cliFormRfc) cliFormRfc.value = isEdit ? String(cliente?.rfc || '') : '';
        if (cliFormReferenciaBancaria) cliFormReferenciaBancaria.value = isEdit ? String(cliente?.referenciaBancaria || '') : '';
        if (cliFormTipo) cliFormTipo.value = isEdit ? String(cliente?.tipoCliente || 'Publico en general') : 'Publico en general';
        if (cliFormSave) cliFormSave.textContent = ordenClienteFormMode === 'register-order' ? 'Aceptar' : 'Guardar cliente';

        popupClientesForm.style.display = 'flex';
        popupClientesForm.setAttribute('aria-hidden', 'false');
        if (cliFormNombre) cliFormNombre.focus();
    };

    const saveClienteFromForm = () => {
        const payload = {
            id: String(cliFormId?.value || '').trim(),
            nombre: String(cliFormNombre?.value || '').trim(),
            empresa: String(cliFormEmpresa?.value || '').trim(),
            telefono: String(cliFormTelefono?.value || '').replace(/\D/g, '').trim(),
            correo: String(cliFormCorreo?.value || '').trim(),
            calle: String(cliFormCalle?.value || '').trim(),
            colonia: String(cliFormColonia?.value || '').trim(),
            numero: String(cliFormNumero?.value || '').trim(),
            pais: String(cliFormPais?.value || 'Mexico').trim() || 'Mexico',
            ciudad: String(cliFormCiudad?.value || '').trim(),
            estado: String(cliFormEstado?.value || '').trim(),
            cp: String(cliFormCp?.value || '').trim(),
            razonSocial: String(cliFormRazonSocial?.value || '').trim(),
            rfc: String(cliFormRfc?.value || '').trim(),
            referenciaBancaria: String(cliFormReferenciaBancaria?.value || '').trim(),
            tipoCliente: String(cliFormTipo?.value || 'Publico en general').trim() || 'Publico en general'
        };

        if (!payload.id) payload.id = mkClienteModuloId();
        if (!payload.nombre) {
            notifyError('El nombre del cliente es obligatorio.', 'Clientes');
            cliFormNombre?.focus();
            return null;
        }
        if (!payload.telefono) {
            notifyError('El telefono del cliente es obligatorio.', 'Clientes');
            cliFormTelefono?.focus();
            return null;
        }
        if (!/^\d{10}$/.test(payload.telefono)) {
            notifyError('El telefono debe tener exactamente 10 digitos numéricos.', 'Clientes');
            cliFormTelefono?.focus();
            return null;
        }

        const repeatedId = clientesModuloData.find((c) => c.id === payload.id && c.id !== clientesModuloEditingId);
        if (repeatedId) {
            notifyError('El ID de cliente ya existe. Usa otro ID.', 'Clientes');
            cliFormId?.focus();
            return null;
        }

        if (clientesModuloEditingId) {
            clientesModuloData = clientesModuloData.map((c) => c.id === clientesModuloEditingId ? payload : c);
            clientesModuloSelectedId = payload.id;
        } else {
            clientesModuloData.unshift(payload);
            clientesModuloSelectedId = payload.id;
        }

        saveClientesModulo();
        closeClientesFormPopup();
        renderClientesModulo();
        notifyInfo('Cliente guardado correctamente.', 'Clientes');
        return payload;
    };

    const openClientesModuloPopup = () => {
        if (!popupClientesModulo) return;
        loadClientesModulo();
        if (!clientesModuloData.find((c) => c.id === clientesModuloSelectedId)) {
            clientesModuloSelectedId = '';
        }
        popupClientesModulo.style.display = 'flex';
        popupClientesModulo.setAttribute('aria-hidden', 'false');
        document.body.classList.add('popup-open');
        document.documentElement.classList.add('popup-open');
        renderClientesModulo();
    };

    const closeClientesModuloPopup = () => {
        if (!popupClientesModulo) return;
        closeClientesFormPopup();
        popupClientesModulo.style.display = 'none';
        popupClientesModulo.setAttribute('aria-hidden', 'true');
        if (popupListado?.style.display !== 'flex' && popupAccess?.style.display !== 'flex' && popupDesignTracking?.style.display !== 'flex' && popupMisPedidos?.style.display !== 'flex' && popupAjustesTabuladores?.style.display !== 'flex' && popupProdTabulador?.style.display !== 'flex' && popupProductos?.style.display !== 'flex' && popupCaja?.style.display !== 'flex' && popupCalendario?.style.display !== 'flex' && popupClientesModulo?.style.display !== 'flex') {
            document.body.classList.remove('popup-open');
            document.documentElement.classList.remove('popup-open');
        }
    };

    window.openClientesPopupGlobal = openClientesModuloPopup;

    const popupProveedoresModulo = document.getElementById('popupProveedoresModulo');
    const proveedoresBack = document.getElementById('proveedoresBack');
    const proveedoresSearch = document.getElementById('proveedoresSearch');
    const proveedoresAdd = document.getElementById('proveedoresAdd');
    const proveedoresEdit = document.getElementById('proveedoresEdit');
    const proveedoresDelete = document.getElementById('proveedoresDelete');
    const proveedoresTableBody = document.getElementById('proveedoresTableBody');
    const proveedoresConteo = document.getElementById('proveedoresConteo');
    const popupProveedorForm = document.getElementById('popupProveedorForm');
    const proveedorFormTitulo = document.getElementById('proveedorFormTitulo');
    const provFormId = document.getElementById('provFormId');
    const provFormNombre = document.getElementById('provFormNombre');
    const provFormEmpresa = document.getElementById('provFormEmpresa');
    const provFormTelefono = document.getElementById('provFormTelefono');
    const provFormCorreo = document.getElementById('provFormCorreo');
    const provFormCredito = document.getElementById('provFormCredito');
    const provFormSaldo = document.getElementById('provFormSaldo');
    const provFormNotas = document.getElementById('provFormNotas');
    const provFormCancel = document.getElementById('provFormCancel');
    const provFormSave = document.getElementById('provFormSave');

    const popupInsumosModulo = document.getElementById('popupInsumosModulo');
    const insumosBack = document.getElementById('insumosBack');
    const insumosSearch = document.getElementById('insumosSearch');
    const insumosAdd = document.getElementById('insumosAdd');
    const insumosEdit = document.getElementById('insumosEdit');
    const insumosDelete = document.getElementById('insumosDelete');
    const insumosTableBody = document.getElementById('insumosTableBody');
    const insumosConteo = document.getElementById('insumosConteo');
    const popupInsumoForm = document.getElementById('popupInsumoForm');
    const insumoFormTitulo = document.getElementById('insumoFormTitulo');
    const insFormId = document.getElementById('insFormId');
    const insFormNombre = document.getElementById('insFormNombre');
    const insFormCategoria = document.getElementById('insFormCategoria');
    const insFormUnidad = document.getElementById('insFormUnidad');
    const insFormExistencias = document.getElementById('insFormExistencias');
    const insFormMinimo = document.getElementById('insFormMinimo');
    const insFormCosto = document.getElementById('insFormCosto');
    const insFormNotas = document.getElementById('insFormNotas');
    const insFormCancel = document.getElementById('insFormCancel');
    const insFormSave = document.getElementById('insFormSave');

    const popupAlmacenModulo = document.getElementById('popupAlmacenModulo');
    const almacenBack = document.getElementById('almacenBack');
    const almacenSearch = document.getElementById('almacenSearch');
    const almacenAdd = document.getElementById('almacenAdd');
    const almacenEdit = document.getElementById('almacenEdit');
    const almacenDelete = document.getElementById('almacenDelete');
    const almacenTableBody = document.getElementById('almacenTableBody');
    const almacenConteo = document.getElementById('almacenConteo');
    const almacenValorTotal = document.getElementById('almacenValorTotal');
    const popupAlmacenForm = document.getElementById('popupAlmacenForm');
    const almFormTitulo = document.getElementById('almFormTitulo');
    const almFormId = document.getElementById('almFormId');
    const almFormSku = document.getElementById('almFormSku');
    const almFormProducto = document.getElementById('almFormProducto');
    const almFormCategoria = document.getElementById('almFormCategoria');
    const almFormStock = document.getElementById('almFormStock');
    const almFormMinimo = document.getElementById('almFormMinimo');
    const almFormUbicacion = document.getElementById('almFormUbicacion');
    const almFormCosto = document.getElementById('almFormCosto');
    const almFormNotas = document.getElementById('almFormNotas');
    const almFormCancel = document.getElementById('almFormCancel');
    const almFormSave = document.getElementById('almFormSave');

    const popupReportesModulo = document.getElementById('popupReportesModulo');
    const reportesmodBack = document.getElementById('reportesmodBack');
    const reportesRango = document.getElementById('reportesRango');
    const reportesRefresh = document.getElementById('reportesRefresh');
    const repKpiVentas = document.getElementById('repKpiVentas');
    const repKpiInversion = document.getElementById('repKpiInversion');
    const repKpiGanancia = document.getElementById('repKpiGanancia');
    const repKpiOrdenes = document.getElementById('repKpiOrdenes');
    const repKpiTicket = document.getElementById('repKpiTicket');
    const repKpiAdeudo = document.getElementById('repKpiAdeudo');
    const repTopProductosBody = document.getElementById('repTopProductosBody');
    const repResumenFuentesBody = document.getElementById('repResumenFuentesBody');
    const repUltimaActualizacion = document.getElementById('repUltimaActualizacion');

    const PROVEEDORES_MODULO_KEY = 'mock_proveedores_modulo_v1';
    const INSUMOS_MODULO_KEY = 'mock_insumos_modulo_v1';
    const ALMACEN_MODULO_KEY = 'mock_almacen_modulo_v1';

    let proveedoresData = [];
    let proveedoresSelectedId = '';
    let proveedoresEditingId = '';

    let insumosData = [];
    let insumosSelectedId = '';
    let insumosEditingId = '';

    let almacenData = [];
    let almacenSelectedId = '';
    let almacenEditingId = '';

    const mkProveedorId = () => `PRV-${Date.now().toString(36).toUpperCase()}-${Math.floor(Math.random() * 90 + 10)}`;
    const mkInsumoId = () => `INS-${Date.now().toString(36).toUpperCase()}-${Math.floor(Math.random() * 90 + 10)}`;
    const mkAlmacenId = () => `ALM-${Date.now().toString(36).toUpperCase()}-${Math.floor(Math.random() * 90 + 10)}`;

    const seedProveedoresModulo = () => ([
        { id: 'PRV-001', nombre: 'Papelera del Centro', empresa: 'Papelera del Centro SA', telefono: '9511008899', correo: 'ventas@papeleracentro.mx', creditoDias: 30, saldoPendiente: 18500, notas: 'Entrega martes y viernes' },
        { id: 'PRV-002', nombre: 'Insumos Graficos MX', empresa: 'Insumos Graficos MX', telefono: '9512234455', correo: 'contacto@insumosgraficos.mx', creditoDias: 15, saldoPendiente: 9200, notas: 'Tinta y viniles' }
    ]);

    const seedInsumosModulo = () => ([
        { id: 'INS-001', nombre: 'Tinta negra', categoria: 'Tintas', unidad: 'Litro', existencias: 12, minimo: 4, costoUnitario: 420, notas: 'Uso diario' },
        { id: 'INS-002', nombre: 'Vinil mate', categoria: 'Viniles', unidad: 'Metro lineal', existencias: 58, minimo: 20, costoUnitario: 72, notas: 'Proveedor principal PRV-002' }
    ]);

    const seedAlmacenModulo = () => ([
        { id: 'ALM-001', sku: 'BOL-MINI-001', producto: 'Bolsa Boutique Mini', categoria: 'Bolsas', stock: 340, minimo: 120, ubicacion: 'Pasillo A / Estante 2', costoUnitario: 3.8, notas: '' },
        { id: 'ALM-002', sku: 'TAR-STD-015', producto: 'Tarjeta Estandar', categoria: 'Tarjetas', stock: 0, minimo: 100, ubicacion: 'Pasillo C / Gaveta 4', costoUnitario: 0.65, notas: 'Sin existencia' }
    ]);

    const saveProveedoresModulo = () => {
        try {
            localStorage.setItem(PROVEEDORES_MODULO_KEY, JSON.stringify(proveedoresData));
        } catch (_) {}
    };

    const loadProveedoresModulo = () => {
        try {
            const raw = localStorage.getItem(PROVEEDORES_MODULO_KEY);
            const parsed = JSON.parse(raw || '[]');
            if (Array.isArray(parsed) && parsed.length) {
                proveedoresData = parsed.map((p) => ({
                    id: String(p.id || mkProveedorId()).trim(),
                    nombre: String(p.nombre || '').trim(),
                    empresa: String(p.empresa || '').trim(),
                    telefono: String(p.telefono || '').trim(),
                    correo: String(p.correo || '').trim(),
                    creditoDias: Math.max(0, Number(p.creditoDias || 0)),
                    saldoPendiente: Math.max(0, Number(p.saldoPendiente || 0)),
                    notas: String(p.notas || '').trim()
                }));
                return;
            }
        } catch (_) {}
        proveedoresData = seedProveedoresModulo();
        saveProveedoresModulo();
    };

    const saveInsumosModulo = () => {
        try {
            localStorage.setItem(INSUMOS_MODULO_KEY, JSON.stringify(insumosData));
        } catch (_) {}
    };

    const loadInsumosModulo = () => {
        try {
            const raw = localStorage.getItem(INSUMOS_MODULO_KEY);
            const parsed = JSON.parse(raw || '[]');
            if (Array.isArray(parsed) && parsed.length) {
                insumosData = parsed.map((i) => ({
                    id: String(i.id || mkInsumoId()).trim(),
                    nombre: String(i.nombre || '').trim(),
                    categoria: String(i.categoria || '').trim(),
                    unidad: String(i.unidad || '').trim(),
                    existencias: Math.max(0, Number(i.existencias || 0)),
                    minimo: Math.max(0, Number(i.minimo || 0)),
                    costoUnitario: Math.max(0, Number(i.costoUnitario || 0)),
                    notas: String(i.notas || '').trim()
                }));
                return;
            }
        } catch (_) {}
        insumosData = seedInsumosModulo();
        saveInsumosModulo();
    };

    const saveAlmacenModulo = () => {
        try {
            localStorage.setItem(ALMACEN_MODULO_KEY, JSON.stringify(almacenData));
        } catch (_) {}
    };

    const loadAlmacenModulo = () => {
        try {
            const raw = localStorage.getItem(ALMACEN_MODULO_KEY);
            const parsed = JSON.parse(raw || '[]');
            if (Array.isArray(parsed) && parsed.length) {
                almacenData = parsed.map((a) => ({
                    id: String(a.id || mkAlmacenId()).trim(),
                    sku: String(a.sku || '').trim(),
                    producto: String(a.producto || '').trim(),
                    categoria: String(a.categoria || '').trim(),
                    stock: Math.max(0, Number(a.stock || 0)),
                    minimo: Math.max(0, Number(a.minimo || 0)),
                    ubicacion: String(a.ubicacion || '').trim(),
                    costoUnitario: Math.max(0, Number(a.costoUnitario || 0)),
                    notas: String(a.notas || '').trim()
                }));
                return;
            }
        } catch (_) {}
        almacenData = seedAlmacenModulo();
        saveAlmacenModulo();
    };

    const closeProveedorFormPopup = () => {
        if (!popupProveedorForm) return;
        popupProveedorForm.style.display = 'none';
        popupProveedorForm.setAttribute('aria-hidden', 'true');
        proveedoresEditingId = '';
    };

    const closeInsumoFormPopup = () => {
        if (!popupInsumoForm) return;
        popupInsumoForm.style.display = 'none';
        popupInsumoForm.setAttribute('aria-hidden', 'true');
        insumosEditingId = '';
    };

    const closeAlmacenFormPopup = () => {
        if (!popupAlmacenForm) return;
        popupAlmacenForm.style.display = 'none';
        popupAlmacenForm.setAttribute('aria-hidden', 'true');
        almacenEditingId = '';
    };

    const updateProveedoresButtons = () => {
        const hasSelection = Boolean(proveedoresSelectedId);
        if (proveedoresEdit) proveedoresEdit.disabled = !hasSelection;
        if (proveedoresDelete) proveedoresDelete.disabled = !hasSelection;
    };

    const updateInsumosButtons = () => {
        const hasSelection = Boolean(insumosSelectedId);
        if (insumosEdit) insumosEdit.disabled = !hasSelection;
        if (insumosDelete) insumosDelete.disabled = !hasSelection;
    };

    const updateAlmacenButtons = () => {
        const hasSelection = Boolean(almacenSelectedId);
        if (almacenEdit) almacenEdit.disabled = !hasSelection;
        if (almacenDelete) almacenDelete.disabled = !hasSelection;
    };

    const renderProveedoresModulo = () => {
        if (!proveedoresTableBody) return;
        const term = String(proveedoresSearch?.value || '').trim().toLowerCase();
        const rows = proveedoresData.filter((p) => {
            if (!term) return true;
            return [p.id, p.nombre, p.empresa, p.telefono, p.correo]
                .some((v) => String(v || '').toLowerCase().includes(term));
        });

        if (!rows.length) {
            proveedoresTableBody.innerHTML = '<tr><td colspan="6" class="clientesmod-empty">No hay proveedores para este filtro.</td></tr>';
            if (proveedoresConteo) proveedoresConteo.textContent = `Total de proveedores: ${proveedoresData.length}`;
            updateProveedoresButtons();
            return;
        }

        proveedoresTableBody.innerHTML = rows.map((p) => {
            const selected = p.id === proveedoresSelectedId ? ' clientesmod-row-selected' : '';
            return `<tr class="${selected}" data-prov-id="${escCliMod(p.id)}"><td>${escCliMod(p.id)}</td><td>${escCliMod(p.nombre)}</td><td>${escCliMod(p.empresa)}</td><td>${escCliMod(p.telefono)}</td><td>${Number(p.creditoDias || 0)}</td><td>${formatMoney(Number(p.saldoPendiente || 0))}</td></tr>`;
        }).join('');

        proveedoresTableBody.querySelectorAll('[data-prov-id]').forEach((row) => {
            row.addEventListener('click', () => {
                const id = String(row.getAttribute('data-prov-id') || '');
                if (!id) return;
                proveedoresSelectedId = id;
                renderProveedoresModulo();
            });
        });

        if (proveedoresConteo) proveedoresConteo.textContent = `Total de proveedores: ${proveedoresData.length}`;
        updateProveedoresButtons();
    };

    const renderInsumosModulo = () => {
        if (!insumosTableBody) return;
        const term = String(insumosSearch?.value || '').trim().toLowerCase();
        const rows = insumosData.filter((i) => {
            if (!term) return true;
            return [i.id, i.nombre, i.categoria, i.unidad]
                .some((v) => String(v || '').toLowerCase().includes(term));
        });

        if (!rows.length) {
            insumosTableBody.innerHTML = '<tr><td colspan="7" class="clientesmod-empty">No hay insumos para este filtro.</td></tr>';
            if (insumosConteo) insumosConteo.textContent = `Total de insumos: ${insumosData.length}`;
            updateInsumosButtons();
            return;
        }

        insumosTableBody.innerHTML = rows.map((i) => {
            const selected = i.id === insumosSelectedId ? ' clientesmod-row-selected' : '';
            return `<tr class="${selected}" data-ins-id="${escCliMod(i.id)}"><td>${escCliMod(i.id)}</td><td>${escCliMod(i.nombre)}</td><td>${escCliMod(i.categoria)}</td><td>${escCliMod(i.unidad)}</td><td>${Number(i.existencias || 0)}</td><td>${Number(i.minimo || 0)}</td><td>${formatMoney(Number(i.costoUnitario || 0))}</td></tr>`;
        }).join('');

        insumosTableBody.querySelectorAll('[data-ins-id]').forEach((row) => {
            row.addEventListener('click', () => {
                const id = String(row.getAttribute('data-ins-id') || '');
                if (!id) return;
                insumosSelectedId = id;
                renderInsumosModulo();
            });
        });

        if (insumosConteo) insumosConteo.textContent = `Total de insumos: ${insumosData.length}`;
        updateInsumosButtons();
    };

    const renderAlmacenModulo = () => {
        if (!almacenTableBody) return;
        const term = String(almacenSearch?.value || '').trim().toLowerCase();
        const rows = almacenData.filter((a) => {
            if (!term) return true;
            return [a.id, a.sku, a.producto, a.categoria, a.ubicacion]
                .some((v) => String(v || '').toLowerCase().includes(term));
        });

        if (!rows.length) {
            almacenTableBody.innerHTML = '<tr><td colspan="8" class="clientesmod-empty">No hay productos para este filtro.</td></tr>';
            if (almacenConteo) almacenConteo.textContent = `Total de productos: ${almacenData.length}`;
            if (almacenValorTotal) {
                const total = almacenData.reduce((acc, a) => acc + (Number(a.stock || 0) * Number(a.costoUnitario || 0)), 0);
                almacenValorTotal.textContent = `Valor total: ${formatMoney(total)}`;
            }
            updateAlmacenButtons();
            return;
        }

        almacenTableBody.innerHTML = rows.map((a) => {
            const selected = a.id === almacenSelectedId ? ' clientesmod-row-selected' : '';
            return `<tr class="${selected}" data-alm-id="${escCliMod(a.id)}"><td>${escCliMod(a.id)}</td><td>${escCliMod(a.sku)}</td><td>${escCliMod(a.producto)}</td><td>${escCliMod(a.categoria)}</td><td>${Number(a.stock || 0)}</td><td>${Number(a.minimo || 0)}</td><td>${escCliMod(a.ubicacion)}</td><td>${formatMoney(Number(a.costoUnitario || 0))}</td></tr>`;
        }).join('');

        almacenTableBody.querySelectorAll('[data-alm-id]').forEach((row) => {
            row.addEventListener('click', () => {
                const id = String(row.getAttribute('data-alm-id') || '');
                if (!id) return;
                almacenSelectedId = id;
                renderAlmacenModulo();
            });
        });

        if (almacenConteo) almacenConteo.textContent = `Total de productos: ${almacenData.length}`;
        if (almacenValorTotal) {
            const total = almacenData.reduce((acc, a) => acc + (Number(a.stock || 0) * Number(a.costoUnitario || 0)), 0);
            almacenValorTotal.textContent = `Valor total: ${formatMoney(total)}`;
        }
        updateAlmacenButtons();
    };

    const openProveedorFormPopup = (mode, proveedor) => {
        if (!popupProveedorForm) return;
        const isEdit = mode === 'edit';
        proveedoresEditingId = isEdit ? String(proveedor?.id || '') : '';
        if (proveedorFormTitulo) proveedorFormTitulo.textContent = isEdit ? 'Editar proveedor' : 'Agregar proveedor';
        if (provFormId) provFormId.value = isEdit ? String(proveedor?.id || '') : mkProveedorId();
        if (provFormNombre) provFormNombre.value = isEdit ? String(proveedor?.nombre || '') : '';
        if (provFormEmpresa) provFormEmpresa.value = isEdit ? String(proveedor?.empresa || '') : '';
        if (provFormTelefono) provFormTelefono.value = isEdit ? String(proveedor?.telefono || '') : '';
        if (provFormCorreo) provFormCorreo.value = isEdit ? String(proveedor?.correo || '') : '';
        if (provFormCredito) provFormCredito.value = isEdit ? String(Number(proveedor?.creditoDias || 0)) : '0';
        if (provFormSaldo) provFormSaldo.value = isEdit ? String(Number(proveedor?.saldoPendiente || 0)) : '0';
        if (provFormNotas) provFormNotas.value = isEdit ? String(proveedor?.notas || '') : '';
        popupProveedorForm.style.display = 'flex';
        popupProveedorForm.setAttribute('aria-hidden', 'false');
        provFormNombre?.focus();
    };

    const openInsumoFormPopup = (mode, insumo) => {
        if (!popupInsumoForm) return;
        const isEdit = mode === 'edit';
        insumosEditingId = isEdit ? String(insumo?.id || '') : '';
        if (insumoFormTitulo) insumoFormTitulo.textContent = isEdit ? 'Editar insumo' : 'Agregar insumo';
        if (insFormId) insFormId.value = isEdit ? String(insumo?.id || '') : mkInsumoId();
        if (insFormNombre) insFormNombre.value = isEdit ? String(insumo?.nombre || '') : '';
        if (insFormCategoria) insFormCategoria.value = isEdit ? String(insumo?.categoria || '') : '';
        if (insFormUnidad) insFormUnidad.value = isEdit ? String(insumo?.unidad || '') : '';
        if (insFormExistencias) insFormExistencias.value = isEdit ? String(Number(insumo?.existencias || 0)) : '0';
        if (insFormMinimo) insFormMinimo.value = isEdit ? String(Number(insumo?.minimo || 0)) : '0';
        if (insFormCosto) insFormCosto.value = isEdit ? String(Number(insumo?.costoUnitario || 0)) : '0';
        if (insFormNotas) insFormNotas.value = isEdit ? String(insumo?.notas || '') : '';
        popupInsumoForm.style.display = 'flex';
        popupInsumoForm.setAttribute('aria-hidden', 'false');
        insFormNombre?.focus();
    };

    const openAlmacenFormPopup = (mode, item) => {
        if (!popupAlmacenForm) return;
        const isEdit = mode === 'edit';
        almacenEditingId = isEdit ? String(item?.id || '') : '';
        if (almFormTitulo) almFormTitulo.textContent = isEdit ? 'Editar producto de almacén' : 'Agregar producto al almacén';
        if (almFormId) almFormId.value = isEdit ? String(item?.id || '') : mkAlmacenId();
        if (almFormSku) almFormSku.value = isEdit ? String(item?.sku || '') : '';
        if (almFormProducto) almFormProducto.value = isEdit ? String(item?.producto || '') : '';
        if (almFormCategoria) almFormCategoria.value = isEdit ? String(item?.categoria || '') : '';
        if (almFormStock) almFormStock.value = isEdit ? String(Number(item?.stock || 0)) : '0';
        if (almFormMinimo) almFormMinimo.value = isEdit ? String(Number(item?.minimo || 0)) : '0';
        if (almFormUbicacion) almFormUbicacion.value = isEdit ? String(item?.ubicacion || '') : '';
        if (almFormCosto) almFormCosto.value = isEdit ? String(Number(item?.costoUnitario || 0)) : '0';
        if (almFormNotas) almFormNotas.value = isEdit ? String(item?.notas || '') : '';
        popupAlmacenForm.style.display = 'flex';
        popupAlmacenForm.setAttribute('aria-hidden', 'false');
        almFormProducto?.focus();
    };

    const saveProveedorFromForm = () => {
        const payload = {
            id: String(provFormId?.value || '').trim() || mkProveedorId(),
            nombre: String(provFormNombre?.value || '').trim(),
            empresa: String(provFormEmpresa?.value || '').trim(),
            telefono: String(provFormTelefono?.value || '').trim(),
            correo: String(provFormCorreo?.value || '').trim(),
            creditoDias: Math.max(0, Number(provFormCredito?.value || 0)),
            saldoPendiente: Math.max(0, Number(provFormSaldo?.value || 0)),
            notas: String(provFormNotas?.value || '').trim()
        };

        if (!payload.nombre) {
            notifyError('El nombre del proveedor es obligatorio.', 'Proveedores');
            provFormNombre?.focus();
            return;
        }
        if (!payload.telefono) {
            notifyError('El teléfono del proveedor es obligatorio.', 'Proveedores');
            provFormTelefono?.focus();
            return;
        }
        if (payload.correo && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(payload.correo)) {
            notifyError('Correo de proveedor inválido.', 'Proveedores');
            provFormCorreo?.focus();
            return;
        }
        const repeatedId = proveedoresData.find((p) => p.id === payload.id && p.id !== proveedoresEditingId);
        if (repeatedId) {
            notifyError('El ID de proveedor ya existe.', 'Proveedores');
            provFormId?.focus();
            return;
        }

        if (proveedoresEditingId) {
            proveedoresData = proveedoresData.map((p) => p.id === proveedoresEditingId ? payload : p);
            proveedoresSelectedId = payload.id;
        } else {
            proveedoresData.unshift(payload);
            proveedoresSelectedId = payload.id;
        }
        saveProveedoresModulo();
        closeProveedorFormPopup();
        renderProveedoresModulo();
        notifyInfo('Proveedor guardado correctamente.', 'Proveedores');
    };

    const saveInsumoFromForm = () => {
        const payload = {
            id: String(insFormId?.value || '').trim() || mkInsumoId(),
            nombre: String(insFormNombre?.value || '').trim(),
            categoria: String(insFormCategoria?.value || '').trim(),
            unidad: String(insFormUnidad?.value || '').trim(),
            existencias: Math.max(0, Number(insFormExistencias?.value || 0)),
            minimo: Math.max(0, Number(insFormMinimo?.value || 0)),
            costoUnitario: Math.max(0, Number(insFormCosto?.value || 0)),
            notas: String(insFormNotas?.value || '').trim()
        };

        if (!payload.nombre) {
            notifyError('El nombre del insumo es obligatorio.', 'Insumos');
            insFormNombre?.focus();
            return;
        }
        if (!payload.unidad) {
            notifyError('La unidad del insumo es obligatoria.', 'Insumos');
            insFormUnidad?.focus();
            return;
        }
        const repeatedId = insumosData.find((i) => i.id === payload.id && i.id !== insumosEditingId);
        if (repeatedId) {
            notifyError('El ID de insumo ya existe.', 'Insumos');
            insFormId?.focus();
            return;
        }

        if (insumosEditingId) {
            insumosData = insumosData.map((i) => i.id === insumosEditingId ? payload : i);
            insumosSelectedId = payload.id;
        } else {
            insumosData.unshift(payload);
            insumosSelectedId = payload.id;
        }
        saveInsumosModulo();
        closeInsumoFormPopup();
        renderInsumosModulo();
        notifyInfo('Insumo guardado correctamente.', 'Insumos');
    };

    const saveAlmacenFromForm = () => {
        const payload = {
            id: String(almFormId?.value || '').trim() || mkAlmacenId(),
            sku: String(almFormSku?.value || '').trim(),
            producto: String(almFormProducto?.value || '').trim(),
            categoria: String(almFormCategoria?.value || '').trim(),
            stock: Math.max(0, Number(almFormStock?.value || 0)),
            minimo: Math.max(0, Number(almFormMinimo?.value || 0)),
            ubicacion: String(almFormUbicacion?.value || '').trim(),
            costoUnitario: Math.max(0, Number(almFormCosto?.value || 0)),
            notas: String(almFormNotas?.value || '').trim()
        };

        if (!payload.producto) {
            notifyError('El nombre del producto es obligatorio.', 'Almacén');
            almFormProducto?.focus();
            return;
        }
        if (!payload.sku) {
            notifyError('El SKU es obligatorio.', 'Almacén');
            almFormSku?.focus();
            return;
        }
        const repeatedId = almacenData.find((a) => a.id === payload.id && a.id !== almacenEditingId);
        if (repeatedId) {
            notifyError('El ID de almacén ya existe.', 'Almacén');
            almFormId?.focus();
            return;
        }

        if (almacenEditingId) {
            almacenData = almacenData.map((a) => a.id === almacenEditingId ? payload : a);
            almacenSelectedId = payload.id;
        } else {
            almacenData.unshift(payload);
            almacenSelectedId = payload.id;
        }
        saveAlmacenModulo();
        closeAlmacenFormPopup();
        renderAlmacenModulo();
        notifyInfo('Producto de almacén guardado correctamente.', 'Almacén');
    };

    const openProveedoresPopup = () => {
        if (!popupProveedoresModulo) return;
        loadProveedoresModulo();
        if (!proveedoresData.find((p) => p.id === proveedoresSelectedId)) proveedoresSelectedId = '';
        popupProveedoresModulo.style.display = 'flex';
        popupProveedoresModulo.setAttribute('aria-hidden', 'false');
        document.body.classList.add('popup-open');
        document.documentElement.classList.add('popup-open');
        renderProveedoresModulo();
    };

    const closeProveedoresPopup = () => {
        if (!popupProveedoresModulo) return;
        closeProveedorFormPopup();
        popupProveedoresModulo.style.display = 'none';
        popupProveedoresModulo.setAttribute('aria-hidden', 'true');
        if (popupListado?.style.display !== 'flex' && popupAccess?.style.display !== 'flex' && popupDesignTracking?.style.display !== 'flex' && popupMisPedidos?.style.display !== 'flex' && popupAjustesTabuladores?.style.display !== 'flex' && popupProdTabulador?.style.display !== 'flex' && popupProductos?.style.display !== 'flex' && popupCaja?.style.display !== 'flex' && popupCalendario?.style.display !== 'flex' && popupClientesModulo?.style.display !== 'flex' && popupInsumosModulo?.style.display !== 'flex' && popupAlmacenModulo?.style.display !== 'flex' && popupReportesModulo?.style.display !== 'flex') {
            document.body.classList.remove('popup-open');
            document.documentElement.classList.remove('popup-open');
        }
    };

    const openInsumosPopup = () => {
        if (!popupInsumosModulo) return;
        loadInsumosModulo();
        if (!insumosData.find((i) => i.id === insumosSelectedId)) insumosSelectedId = '';
        popupInsumosModulo.style.display = 'flex';
        popupInsumosModulo.setAttribute('aria-hidden', 'false');
        document.body.classList.add('popup-open');
        document.documentElement.classList.add('popup-open');
        renderInsumosModulo();
    };

    const closeInsumosPopup = () => {
        if (!popupInsumosModulo) return;
        closeInsumoFormPopup();
        popupInsumosModulo.style.display = 'none';
        popupInsumosModulo.setAttribute('aria-hidden', 'true');
        if (popupListado?.style.display !== 'flex' && popupAccess?.style.display !== 'flex' && popupDesignTracking?.style.display !== 'flex' && popupMisPedidos?.style.display !== 'flex' && popupAjustesTabuladores?.style.display !== 'flex' && popupProdTabulador?.style.display !== 'flex' && popupProductos?.style.display !== 'flex' && popupCaja?.style.display !== 'flex' && popupCalendario?.style.display !== 'flex' && popupClientesModulo?.style.display !== 'flex' && popupProveedoresModulo?.style.display !== 'flex' && popupAlmacenModulo?.style.display !== 'flex' && popupReportesModulo?.style.display !== 'flex') {
            document.body.classList.remove('popup-open');
            document.documentElement.classList.remove('popup-open');
        }
    };

    const openAlmacenPopup = () => {
        if (!popupAlmacenModulo) return;
        loadAlmacenModulo();
        if (!almacenData.find((a) => a.id === almacenSelectedId)) almacenSelectedId = '';
        popupAlmacenModulo.style.display = 'flex';
        popupAlmacenModulo.setAttribute('aria-hidden', 'false');
        document.body.classList.add('popup-open');
        document.documentElement.classList.add('popup-open');
        renderAlmacenModulo();
    };

    const closeAlmacenPopup = () => {
        if (!popupAlmacenModulo) return;
        closeAlmacenFormPopup();
        popupAlmacenModulo.style.display = 'none';
        popupAlmacenModulo.setAttribute('aria-hidden', 'true');
        if (popupListado?.style.display !== 'flex' && popupAccess?.style.display !== 'flex' && popupDesignTracking?.style.display !== 'flex' && popupMisPedidos?.style.display !== 'flex' && popupAjustesTabuladores?.style.display !== 'flex' && popupProdTabulador?.style.display !== 'flex' && popupProductos?.style.display !== 'flex' && popupCaja?.style.display !== 'flex' && popupCalendario?.style.display !== 'flex' && popupClientesModulo?.style.display !== 'flex' && popupProveedoresModulo?.style.display !== 'flex' && popupInsumosModulo?.style.display !== 'flex' && popupReportesModulo?.style.display !== 'flex') {
            document.body.classList.remove('popup-open');
            document.documentElement.classList.remove('popup-open');
        }
    };

    const getDateDaysAgo = (days) => {
        const base = new Date();
        base.setHours(0, 0, 0, 0);
        base.setDate(base.getDate() - Math.max(0, Number(days || 0)));
        return base;
    };

    const renderReportesModulo = () => {
        loadMisPedidos();
        loadProductos();
        loadInsumosModulo();
        loadAlmacenModulo();

        const rangoDias = Math.max(1, Number(reportesRango?.value || 30));
        const since = getDateDaysAgo(rangoDias - 1);
        const rows = misPedidosData.filter((r) => {
            const dt = new Date(`${r.fechaEmitida || ''}T00:00:00`);
            if (Number.isNaN(dt.getTime())) return false;
            return dt >= since;
        });

        const ventas = rows.reduce((acc, r) => acc + Number(r.total || 0), 0);
        const inversion = rows.reduce((acc, r) => acc + Number(r.inversion || 0), 0);
        const ganancia = rows.reduce((acc, r) => acc + Number(r.ganancia || 0), 0);
        const adeudo = rows.reduce((acc, r) => acc + Number(r.adeudoCliente || 0), 0);
        const ordenes = rows.length;
        const ticket = ordenes ? (ventas / ordenes) : 0;

        if (repKpiVentas) repKpiVentas.textContent = formatMoney(ventas);
        if (repKpiInversion) repKpiInversion.textContent = formatMoney(inversion);
        if (repKpiGanancia) repKpiGanancia.textContent = formatMoney(ganancia);
        if (repKpiOrdenes) repKpiOrdenes.textContent = String(ordenes);
        if (repKpiTicket) repKpiTicket.textContent = formatMoney(ticket);
        if (repKpiAdeudo) repKpiAdeudo.textContent = formatMoney(adeudo);

        const topMap = new Map();
        rows.forEach((r) => {
            if (Array.isArray(r.lineas) && r.lineas.length) {
                r.lineas.forEach((ln) => {
                    const name = String(ln.producto || 'Producto').trim() || 'Producto';
                    const qty = Math.max(0, Number(ln.cantidad || 0));
                    const total = qty * Math.max(0, Number(ln.precio || 0));
                    const prev = topMap.get(name) || { qty: 0, total: 0 };
                    topMap.set(name, { qty: prev.qty + qty, total: prev.total + total });
                });
            } else if (r.producto) {
                const name = String(r.producto || 'Producto').trim() || 'Producto';
                const prev = topMap.get(name) || { qty: 0, total: 0 };
                topMap.set(name, { qty: prev.qty + 1, total: prev.total + Number(r.total || 0) });
            }
        });

        const topRows = Array.from(topMap.entries())
            .map(([name, val]) => ({ name, qty: val.qty, total: val.total }))
            .sort((a, b) => b.total - a.total)
            .slice(0, 8);

        if (repTopProductosBody) {
            if (!topRows.length) {
                repTopProductosBody.innerHTML = '<tr><td colspan="3" class="clientesmod-empty">Sin detalle de productos en el periodo.</td></tr>';
            } else {
                repTopProductosBody.innerHTML = topRows.map((t) => `<tr><td>${escCliMod(t.name)}</td><td>${Number(t.qty || 0)}</td><td>${formatMoney(Number(t.total || 0))}</td></tr>`).join('');
            }
        }

        const totalInsumosValor = insumosData.reduce((acc, i) => acc + (Number(i.existencias || 0) * Number(i.costoUnitario || 0)), 0);
        const totalAlmacenValor = almacenData.reduce((acc, a) => acc + (Number(a.stock || 0) * Number(a.costoUnitario || 0)), 0);
        const lowStockInsumos = insumosData.filter((i) => Number(i.existencias || 0) <= Number(i.minimo || 0)).length;
        const lowStockAlmacen = almacenData.filter((a) => Number(a.stock || 0) <= Number(a.minimo || 0)).length;

        if (repResumenFuentesBody) {
            repResumenFuentesBody.innerHTML = [
                ['Pedidos en periodo', ordenes, formatMoney(ventas)],
                ['Proveedores activos', proveedoresData.length, formatMoney(proveedoresData.reduce((acc, p) => acc + Number(p.saldoPendiente || 0), 0))],
                ['Insumos en inventario', insumosData.length, formatMoney(totalInsumosValor)],
                ['Productos en almacén', almacenData.length, formatMoney(totalAlmacenValor)],
                ['Bajo stock (insumos)', lowStockInsumos, '-'],
                ['Bajo stock (almacén)', lowStockAlmacen, '-']
            ].map((r) => `<tr><td>${escCliMod(r[0])}</td><td>${escCliMod(r[1])}</td><td>${escCliMod(r[2])}</td></tr>`).join('');
        }

        if (repUltimaActualizacion) {
            repUltimaActualizacion.textContent = `Actualización: ${new Date().toLocaleString('es-MX')}`;
        }
    };

    const openReportesPopup = () => {
        if (!popupReportesModulo) return;
        loadProveedoresModulo();
        loadInsumosModulo();
        loadAlmacenModulo();
        popupReportesModulo.style.display = 'flex';
        popupReportesModulo.setAttribute('aria-hidden', 'false');
        document.body.classList.add('popup-open');
        document.documentElement.classList.add('popup-open');
        renderReportesModulo();
    };

    const closeReportesPopup = () => {
        if (!popupReportesModulo) return;
        popupReportesModulo.style.display = 'none';
        popupReportesModulo.setAttribute('aria-hidden', 'true');
        if (popupListado?.style.display !== 'flex' && popupAccess?.style.display !== 'flex' && popupDesignTracking?.style.display !== 'flex' && popupMisPedidos?.style.display !== 'flex' && popupAjustesTabuladores?.style.display !== 'flex' && popupProdTabulador?.style.display !== 'flex' && popupProductos?.style.display !== 'flex' && popupCaja?.style.display !== 'flex' && popupCalendario?.style.display !== 'flex' && popupClientesModulo?.style.display !== 'flex' && popupProveedoresModulo?.style.display !== 'flex' && popupInsumosModulo?.style.display !== 'flex' && popupAlmacenModulo?.style.display !== 'flex') {
            document.body.classList.remove('popup-open');
            document.documentElement.classList.remove('popup-open');
        }
    };

    window.openProveedoresPopupGlobal = openProveedoresPopup;
    window.openInsumosPopupGlobal = openInsumosPopup;
    window.openAlmacenPopupGlobal = openAlmacenPopup;
    window.openReportesPopupGlobal = openReportesPopup;
    let ordenTrabajoFolio = mkFolio();

    const loadMisPedidos = () => {
        try {
            const raw = localStorage.getItem(MIS_PEDIDOS_KEY);
            const parsed = JSON.parse(raw || '[]');
            misPedidosData = Array.isArray(parsed) ? parsed.map((r) => {
                const total = Number(r.total || 0);
                const anticipo = Number(r.anticipo || 0);
                return {
                    ...r,
                    vendedor: r.vendedor || '',
                    inversion: Number(r.inversion || 0),
                    ganancia: Number(r.ganancia || (total - Number(r.inversion || 0))),
                    anticipo,
                    adeudoCliente: Number(r.adeudoCliente != null ? r.adeudoCliente : (total - anticipo)),
                    estatusProduccion: r.estatusProduccion || r.estatus || 'pendiente'
                };
            }) : [];
        } catch (_) {
            misPedidosData = [];
        }
    };

    const saveMisPedidos = () => {
        try {
            localStorage.setItem(MIS_PEDIDOS_KEY, JSON.stringify(misPedidosData));
        } catch (_) {}
    };

    const upsertMisPedidoRegistro = (registro = {}) => {
        if (!registro || !registro.folio || !registro.tipo) return;
        const idx = misPedidosData.findIndex((r) => r.folio === registro.folio && r.tipo === registro.tipo);
        if (idx >= 0) {
            misPedidosData[idx] = { ...misPedidosData[idx], ...registro, id: misPedidosData[idx].id };
        } else {
            misPedidosData.unshift(registro);
        }
    };

    const buildPedidoRegistro = (tipo = 'cotizacion') => {
        const subtotalVal = ordenLineas.reduce((acc, row) => acc + (Number(row.precio) * Number(row.cantidad)), 0);
        const impuestosVal = subtotalVal * (ordenTaxRate / 100);
        const descuentoPctVal = subtotalVal * (ordenDiscount / 100);
        const descuentoVal = descuentoPctVal + Math.max(0, Number(ordenDiscountAmount || 0));
        const totalVal = Math.max(0, subtotalVal + impuestosVal - descuentoVal);
        const inversionVal = Number(ordenInversion || 0);
        const gananciaVal = totalVal - inversionVal;
        const clienteNombre = (refs.clienteNombre?.textContent || 'SIN CLIENTE').trim();
        const telefono = (refs.clienteTelefono?.value || '').trim();
        const metodoPago = getSelectedPayMethod();
        const disenador = (el('ordenDisenador')?.value || '').trim();
        const vendedor = (el('ordenVendedor')?.value || '').trim();
        const fechaEntrega = refs.fechaEntrega?.value || todayISO();
        const anticipo = Math.max(0, Number(ordenAnticipo || 0));
        const adeudoCliente = Math.max(0, totalVal - anticipo);

        return {
            id: `MP-${Date.now().toString(36).toUpperCase()}`,
            tipo,
            folio: ordenTrabajoFolio,
            clienteNombre,
            telefono,
            metodoPago,
            disenador,
            vendedor,
            fechaEmitida: todayISO(),
            fechaEntrega,
            estatusProduccion: 'pendiente',
            anticipo,
            adeudoCliente,
            subtotal: subtotalVal,
            impuestos: impuestosVal,
            descuento: descuentoVal,
            total: totalVal,
            inversion: inversionVal,
            ganancia: gananciaVal
        };
    };

    const mpInput = (v) => String(v || '').toLowerCase();
    const mpMatch = (src, term) => mpInput(src).includes(mpInput(term));

    const getMisPedidosFiltrados = () => {
        const minAdeudo = Number(mpFiltroAdeudo?.value || 0);
        return misPedidosData.filter((row) => {
            if (row.tipo !== misPedidosTab) return false;
            if (!mpMatch(row.folio, mpFiltroFolio?.value || '')) return false;
            if (!mpMatch(row.clienteNombre, mpFiltroNombre?.value || '')) return false;
            if (!mpMatch(row.telefono, mpFiltroTelefono?.value || '')) return false;
            if (!mpMatch(row.disenador, mpFiltroDisenador?.value || '')) return false;
            if ((mpFiltroFechaEmitida?.value || '') && row.fechaEmitida !== mpFiltroFechaEmitida.value) return false;
            if ((mpFiltroFechaEntrega?.value || '') && row.fechaEntrega !== mpFiltroFechaEntrega.value) return false;
            if ((mpFiltroEstatus?.value || '') && row.estatusProduccion !== mpFiltroEstatus.value) return false;
            if ((mpFiltroAdeudo?.value || '') && Number(row.adeudoCliente || 0) < minAdeudo) return false;
            return true;
        });
    };

    const getSelectedMisPedidos = (rows = []) => rows.filter((r) => mpSelectedIds.has(r.id));

    const renderMisPedidos = () => {
        if (!mpTablaBody) return;
        const rows = getMisPedidosFiltrados();
        const selectedRows = getSelectedMisPedidos(rows);

        mispedidosTabVentas?.classList.toggle('active', misPedidosTab === 'venta');
        mispedidosTabCot?.classList.toggle('active', misPedidosTab === 'cotizacion');
        if (mpConteoLabel) {
            mpConteoLabel.textContent = misPedidosTab === 'venta' ? 'Número de órdenes' : 'Número de cotizaciones';
        }
        if (mpConteoValor) mpConteoValor.textContent = String(rows.length);

        if (!rows.length) {
            mpTablaBody.innerHTML = '<tr><td colspan="12" style="text-align:center;color:#6b7280;padding:14px;">Sin registros para los filtros actuales.</td></tr>';
        } else {
            mpTablaBody.innerHTML = rows.map((row) => `<tr data-mp-id="${escapeHtml(row.id)}" class="${mpSelectedIds.has(row.id) ? 'mispedidos-row-selected' : ''}">
                <td>${escapeHtml(row.folio)}</td>
                <td>${escapeHtml(row.clienteNombre)}</td>
                <td>${escapeHtml(row.fechaEmitida)}</td>
                <td>${escapeHtml(row.fechaEntrega)}</td>
                <td>${escapeHtml(row.disenador || '-')}</td>
                <td>${escapeHtml(row.vendedor || '-')}</td>
                <td>${formatMoney(Number(row.inversion || 0))}</td>
                <td>${formatMoney(Number(row.ganancia || 0))}</td>
                <td>${formatMoney(Number(row.total || 0))}</td>
                <td>${formatMoney(Number(row.anticipo || 0))}</td>
                <td>${formatMoney(Number(row.adeudoCliente || 0))}</td>
                <td>${escapeHtml((row.estatusProduccion || '').replace('-', ' '))}</td>
            </tr>`).join('');
        }

        const adeudoPendiente = rows.reduce((acc, r) => acc + Number(r.adeudoCliente || 0), 0);
        const totalVentas = rows.reduce((acc, r) => acc + Number(r.total || 0), 0);
        const totalInversion = rows.reduce((acc, r) => acc + Number(r.inversion || 0), 0);
        const totalGanancia = rows.reduce((acc, r) => acc + Number(r.ganancia || 0), 0);

        if (mpAdeudoPendiente) mpAdeudoPendiente.textContent = formatMoney(adeudoPendiente);
        if (mpTotalVentas) mpTotalVentas.textContent = formatMoney(totalVentas);
        if (mpTotalInversion) mpTotalInversion.textContent = formatMoney(totalInversion);
        if (mpTotalGanancia) mpTotalGanancia.textContent = formatMoney(totalGanancia);

        if (mpEditarSeleccion) mpEditarSeleccion.textContent = `Editar selección (${selectedRows.length})`;
        if (mpExportarSeleccion) mpExportarSeleccion.innerHTML = `<span class="excel-icon">📗</span>Exportar selección (${selectedRows.length})`;
    };

    const exportRowsAsCsv = (rows = []) => {
        if (!rows.length) {
            alert('Selecciona al menos un registro para exportar.');
            return;
        }
        const headers = ['FOLIO','NOMBRE DEL CLIENTE','FECHA EMITIDA','FECHA DE ENTREGA','DISEÑADOR','VENDEDOR','INVERSION','GANANCIA','TOTAL','ANTICIPO','ADEUDO','ESTATUS'];
        const esc = (v) => `"${String(v ?? '').replace(/"/g, '""')}"`;
        const lines = [headers.join(',')].concat(rows.map((r) => [
            r.folio,
            r.clienteNombre,
            r.fechaEmitida,
            r.fechaEntrega,
            r.disenador || '',
            r.vendedor || '',
            Number(r.inversion || 0).toFixed(2),
            Number(r.ganancia || 0).toFixed(2),
            Number(r.total || 0).toFixed(2),
            Number(r.anticipo || 0).toFixed(2),
            Number(r.adeudoCliente || 0).toFixed(2),
            r.estatusProduccion || ''
        ].map(esc).join(',')));
        const blob = new Blob([lines.join('\n')], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `mis_pedidos_${todayISO()}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    const editarRegistrosSeleccionados = (rows = []) => {
        if (!rows.length) {
            alert('Selecciona al menos un registro para editar.');
            return;
        }

        const base = rows[0];
        const disenador = prompt('Diseñador (deja vacío para no cambiar):', rows.length === 1 ? (base.disenador || '') : '');
        if (disenador === null) return;
        const vendedor = prompt('Vendedor (deja vacío para no cambiar):', rows.length === 1 ? (base.vendedor || '') : '');
        if (vendedor === null) return;
        const estatus = prompt('Estatus (pendiente|en-produccion|pendiente-por-entregar|terminado|entregado):', rows.length === 1 ? (base.estatusProduccion || 'pendiente') : '');
        if (estatus === null) return;
        const anticipoTxt = prompt('Anticipo (deja vacío para no cambiar):', rows.length === 1 ? String(base.anticipo || 0) : '');
        if (anticipoTxt === null) return;

        const patch = {};
        if (String(disenador).trim()) patch.disenador = String(disenador).trim();
        if (String(vendedor).trim()) patch.vendedor = String(vendedor).trim();
        if (String(estatus).trim()) patch.estatusProduccion = String(estatus).trim();
        if (String(anticipoTxt).trim()) {
            const ant = Number(anticipoTxt);
            if (Number.isFinite(ant) && ant >= 0) patch.anticipo = ant;
        }

        if (!Object.keys(patch).length) return;

        const ids = new Set(rows.map((r) => r.id));
        misPedidosData = misPedidosData.map((r) => {
            if (!ids.has(r.id)) return r;
            const next = { ...r, ...patch };
            next.adeudoCliente = Math.max(0, Number(next.total || 0) - Number(next.anticipo || 0));
            next.ganancia = Number(next.total || 0) - Number(next.inversion || 0);
            return next;
        });
        saveMisPedidos();
        renderMisPedidos();
    };

    const openMisPedidosPopup = () => {
        if (!popupMisPedidos) return;
        popupMisPedidos.style.display = 'flex';
        popupMisPedidos.setAttribute('aria-hidden', 'false');
        document.body.classList.add('popup-open');
        document.documentElement.classList.add('popup-open');
        loadMisPedidos();
        renderMisPedidos();
    };

    const closeMisPedidosPopup = () => {
        if (!popupMisPedidos) return;
        popupMisPedidos.style.display = 'none';
        popupMisPedidos.setAttribute('aria-hidden', 'true');
        if (popupListado?.style.display !== 'flex' && popupAccess?.style.display !== 'flex' && popupDesignTracking?.style.display !== 'flex' && popupProductos?.style.display !== 'flex' && popupCaja?.style.display !== 'flex' && popupCalendario?.style.display !== 'flex' && popupClientesModulo?.style.display !== 'flex') {
            document.body.classList.remove('popup-open');
            document.documentElement.classList.remove('popup-open');
        }
    };

    window.openMisPedidosPopupGlobal = openMisPedidosPopup;

    const prodEscape = (value) => String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');

    const makeTabuladorRows = () => ([
        { tipo: 'lt', min: '', max: '100', precioRevendedor: 0, precioGeneral: 0 },
        { tipo: 'range', min: '101', max: '250', precioRevendedor: 0, precioGeneral: 0 },
        { tipo: 'range', min: '251', max: '500', precioRevendedor: 0, precioGeneral: 0 },
        { tipo: 'range', min: '501', max: '1000', precioRevendedor: 0, precioGeneral: 0 },
        { tipo: 'gte', min: '1001', max: '', precioRevendedor: 0, precioGeneral: 0 }
    ]);

    const mkTabuladorId = () => `TAB-${Date.now().toString(36).toUpperCase()}-${Math.floor(Math.random() * 99)}`;

    const buildTabulador = (name = 'Tabulador base') => ({
        id: mkTabuladorId(),
        nombre: name,
        filas: makeTabuladorRows()
    });

    const seedTabuladores = () => {
        const t1 = buildTabulador('Mayoreo base');
        const t2 = buildTabulador('Mostrador base');
        t1.filas = [
            { tipo: 'lt', min: '', max: '100', precioRevendedor: 3.8, precioGeneral: 5.2 },
            { tipo: 'range', min: '101', max: '250', precioRevendedor: 3.4, precioGeneral: 4.8 },
            { tipo: 'range', min: '251', max: '500', precioRevendedor: 3.1, precioGeneral: 4.5 },
            { tipo: 'range', min: '501', max: '1000', precioRevendedor: 2.7, precioGeneral: 4.1 },
            { tipo: 'gte', min: '1001', max: '', precioRevendedor: 2.4, precioGeneral: 3.8 }
        ];
        t2.filas = [
            { tipo: 'lt', min: '', max: '50', precioRevendedor: 7.8, precioGeneral: 10.5 },
            { tipo: 'range', min: '51', max: '100', precioRevendedor: 7.2, precioGeneral: 9.9 },
            { tipo: 'range', min: '101', max: '200', precioRevendedor: 6.8, precioGeneral: 9.2 },
            { tipo: 'range', min: '201', max: '500', precioRevendedor: 6.3, precioGeneral: 8.7 },
            { tipo: 'gte', min: '501', max: '', precioRevendedor: 5.9, precioGeneral: 8.1 }
        ];
        return [t1, t2];
    };

    const loadTabuladores = () => {
        try {
            const raw = localStorage.getItem(TABULADORES_KEY);
            const parsed = JSON.parse(raw || '[]');
            if (!Array.isArray(parsed) || !parsed.length) {
                tabuladoresData = seedTabuladores();
                return;
            }
            tabuladoresData = parsed.map((t) => ({
                id: t.id || mkTabuladorId(),
                nombre: String(t.nombre || 'Tabulador').trim() || 'Tabulador',
                filas: Array.isArray(t.filas) && t.filas.length === 5
                    ? t.filas.map((f, i) => ({
                        tipo: ['lt', 'range', 'range', 'range', 'gte'][i],
                        min: String(f.min ?? ''),
                        max: String(f.max ?? ''),
                        precioRevendedor: Number(f.precioRevendedor || 0),
                        precioGeneral: Number(f.precioGeneral || 0)
                    }))
                    : makeTabuladorRows()
            }));
        } catch (_) {
            tabuladoresData = seedTabuladores();
        }
    };

    const saveTabuladores = () => {
        try {
            localStorage.setItem(TABULADORES_KEY, JSON.stringify(tabuladoresData));
        } catch (_) {}
    };

    const getTabuladorById = (id = '') => tabuladoresData.find((t) => t.id === id) || tabuladoresData[0] || null;

    const renderAjustesTabuladorSelect = () => {
        if (!ajustesTabSelect) return;
        ajustesTabSelect.innerHTML = tabuladoresData.map((t) => `<option value="${prodEscape(t.id)}">${prodEscape(t.nombre)}</option>`).join('');
        if (!ajustesTabuladorId || !tabuladoresData.some((t) => t.id === ajustesTabuladorId)) {
            ajustesTabuladorId = tabuladoresData[0]?.id || '';
        }
        ajustesTabSelect.value = ajustesTabuladorId;
        const active = getTabuladorById(ajustesTabuladorId);
        if (ajustesTabNombre) ajustesTabNombre.value = active?.nombre || '';
    };

    const renderAjustesTabuladorTables = () => {
        const active = getTabuladorById(ajustesTabuladorId);
        if (!active || !ajustesTabRangosTable || !ajustesTabPreciosTable) return;

        const filaLabel = (f) => (f.tipo === 'lt' ? 'Menor a' : (f.tipo === 'gte' ? 'O más piezas' : 'Rango'));

        ajustesTabRangosTable.innerHTML = `<thead><tr><th>Fila</th><th>Desde</th><th>Hasta</th></tr></thead><tbody>${active.filas.map((f, i) => `
            <tr data-aj-row="${i}">
                <td>${filaLabel(f)}</td>
                <td>${f.tipo === 'lt' ? '-' : `<input data-aj-min="${i}" type="number" min="0" step="1" value="${prodEscape(f.min)}">`}</td>
                <td>${f.tipo === 'gte' ? '-' : `<input data-aj-max="${i}" type="number" min="0" step="1" value="${prodEscape(f.max)}">`}</td>
            </tr>`).join('')}</tbody>`;

        ajustesTabPreciosTable.innerHTML = `<thead><tr><th>Fila</th><th>Revendedor</th><th>General</th></tr></thead><tbody>${active.filas.map((f, i) => `
            <tr data-aj-price-row="${i}">
                <td>${i + 1}</td>
                <td>Se captura en producto</td>
                <td>Se captura en producto</td>
            </tr>`).join('')}</tbody>`;
    };

    const syncAjustesRowsFromUI = () => {
        const active = getTabuladorById(ajustesTabuladorId);
        if (!active) return;
        active.filas = active.filas.map((f, i) => {
            const minEl = document.querySelector(`[data-aj-min="${i}"]`);
            const maxEl = document.querySelector(`[data-aj-max="${i}"]`);
            return {
                ...f,
                min: minEl ? String(minEl.value || '') : f.min,
                max: maxEl ? String(maxEl.value || '') : f.max
            };
        });
        if (ajustesTabNombre) active.nombre = String(ajustesTabNombre.value || '').trim() || active.nombre;
    };

    const renderProdTabuladorSelect = () => {
        if (!prodTabuladorSelect) return;
        prodTabuladorSelect.innerHTML = tabuladoresData.map((t) => `<option value="${prodEscape(t.id)}">${prodEscape(t.nombre)}</option>`).join('');
        const def = prodPendingTabuladorId || tabuladoresData[0]?.id || '';
        prodTabuladorSelect.value = def;
        prodPendingTabuladorId = def;
    };

    const renderProdTabuladorPreview = () => {
        const active = getTabuladorById(prodPendingTabuladorId);
        if (!active || !prodTabRangosPreview || !prodTabPreciosPreview) return;

        if (!prodPendingTabuladorPrecios.length || prodPendingTabuladorPrecios.length !== active.filas.length) {
            prodPendingTabuladorPrecios = active.filas.map((f) => ({
                precioRevendedor: Number(f.precioRevendedor || 0),
                precioGeneral: Number(f.precioGeneral || 0)
            }));
        }

        prodTabRangosPreview.innerHTML = `<thead><tr><th>Fila</th><th>Estructura</th></tr></thead><tbody>${active.filas.map((f, i) => {
            if (f.tipo === 'lt') return `<tr><td>${i + 1}</td><td>Menor a ${prodEscape(f.max)}</td></tr>`;
            if (f.tipo === 'gte') return `<tr><td>${i + 1}</td><td>${prodEscape(f.min)} o más piezas</td></tr>`;
            return `<tr><td>${i + 1}</td><td>De ${prodEscape(f.min)} a ${prodEscape(f.max)}</td></tr>`;
        }).join('')}</tbody>`;

        prodTabPreciosPreview.innerHTML = `<thead><tr><th>Fila</th><th>Revendedor</th><th>General</th></tr></thead><tbody>${active.filas.map((f, i) =>
            `<tr>
                <td>${i + 1}</td>
                <td><input data-pt-rev="${i}" type="number" min="0" step="0.01" value="${Number(prodPendingTabuladorPrecios[i]?.precioRevendedor || 0)}"></td>
                <td><input data-pt-gen="${i}" type="number" min="0" step="0.01" value="${Number(prodPendingTabuladorPrecios[i]?.precioGeneral || 0)}"></td>
            </tr>`
        ).join('')}</tbody>`;
    };

    const syncProdTabPreciosFromUI = () => {
        const active = getTabuladorById(prodPendingTabuladorId);
        if (!active) return;
        prodPendingTabuladorPrecios = active.filas.map((_, i) => {
            const revEl = document.querySelector(`[data-pt-rev="${i}"]`);
            const genEl = document.querySelector(`[data-pt-gen="${i}"]`);
            return {
                precioRevendedor: Math.max(0, Number(revEl?.value || 0)),
                precioGeneral: Math.max(0, Number(genEl?.value || 0))
            };
        });
    };

    const readFileAsDataUrlLocal = (file) => new Promise((resolve, reject) => {
        if (!file) return resolve('');
        const reader = new FileReader();
        reader.onload = () => resolve(String(reader.result || ''));
        reader.onerror = (e) => reject(e);
        reader.readAsDataURL(file);
    });

    const seedProductos = () => ([
        { id: 'PR-1001', codigo: 'BOL-MINI-001', producto: 'Bolsa Boutique Mini', medida: '20x22 cm', material: 'Couche 300 gr', minima: 120, existencias: 340, precioRevendedor: 4.8, precioVenta: 6.2, categoria: 'Bolsas', tipo: 'stock' },
        { id: 'PR-1002', codigo: 'BOL-MED-002', producto: 'Bolsa Boutique Mediana', medida: '35x41 cm', material: 'Couche 300 gr', minima: 80, existencias: 62, precioRevendedor: 8.5, precioVenta: 10.9, categoria: 'Bolsas', tipo: 'stock' },
        { id: 'PR-1003', codigo: 'TAR-STD-015', producto: 'Tarjeta Estandar', medida: '9x5 cm', material: 'Cartulina Sulfatada', minima: 100, existencias: 0, precioRevendedor: 0.75, precioVenta: 1.2, categoria: 'Tarjetas', tipo: 'stock' },
        { id: 'PR-1004', codigo: 'VOL-MC-040', producto: 'Volante Media Carta', medida: '14x21.5 cm', material: 'Couché 150 gr', minima: 150, existencias: 210, precioRevendedor: 1.15, precioVenta: 1.85, categoria: 'Volantes', tipo: 'stock' },
        { id: 'PR-2001', codigo: 'GF-LON-001', producto: 'Lona Front', medida: '1x1 m', material: 'Lona Front 13 oz', minima: 10, existencias: 18, precioRevendedor: 120, precioVenta: 165, categoria: 'Lonas', tipo: 'gran-formato' },
        { id: 'PR-2002', codigo: 'GF-VIN-002', producto: 'Vinil Adhesivo', medida: '1x1 m', material: 'Vinil Brillante', minima: 8, existencias: 6, precioRevendedor: 95, precioVenta: 130, categoria: 'Viniles', tipo: 'gran-formato' },
        { id: 'PR-2003', codigo: 'GF-TRO-003', producto: 'Trovisel Impreso', medida: '60x90 cm', material: 'Trovisel 3 mm', minima: 6, existencias: 11, precioRevendedor: 138, precioVenta: 178, categoria: 'Rígidos', tipo: 'gran-formato' }
    ]);

    const loadProductos = () => {
        try {
            const raw = localStorage.getItem(PRODUCTOS_KEY);
            const parsed = JSON.parse(raw || '[]');
            if (!Array.isArray(parsed) || !parsed.length) {
                productosData = seedProductos();
                return;
            }
            productosData = parsed.map((row) => ({
                id: row.id || `PR-${Date.now().toString(36).toUpperCase()}${Math.floor(Math.random() * 999)}`,
                codigo: String(row.codigo || '').trim(),
                producto: String(row.producto || row.nombre || '').trim(),
                medida: String(row.medida || '-').trim(),
                material: String(row.material || '-').trim(),
                minima: Math.max(0, Number(row.minima || row.cantMinima || 0)),
                existencias: Math.max(0, Number(row.existencias || 0)),
                precioCompra: Math.max(0, Number(row.precioCompra || 0)),
                tipoImpresion: String(row.tipoImpresion || '').trim(),
                proveedor: String(row.proveedor || '').trim(),
                descripcion: String(row.descripcion || '').trim(),
                fotoPrincipal: String(row.fotoPrincipal || ''),
                coloresSubproductos: Array.isArray(row.coloresSubproductos) ? row.coloresSubproductos.map((c) => ({
                    color: String(c.color || '').trim(),
                    existencias: Math.max(0, Number(c.existencias || 0)),
                    foto: String(c.foto || '')
                })).filter((c) => c.color) : [],
                gfCobroTipo: row.gfCobroTipo === 'm-lineal' ? 'm-lineal' : 'm2',
                gfAjusteAncho: ['metro', 'medio', 'sin'].includes(row.gfAjusteAncho) ? row.gfAjusteAncho : 'sin',
                gfPrecioGeneralM2: Math.max(0, Number(row.gfPrecioGeneralM2 || 0)),
                gfPrecioRevM2: Math.max(0, Number(row.gfPrecioRevM2 || 0)),
                gfPrecioGeneralML: Math.max(0, Number(row.gfPrecioGeneralML || 0)),
                gfPrecioRevML: Math.max(0, Number(row.gfPrecioRevML || 0)),
                gfCostoM2: Math.max(0, Number(row.gfCostoM2 || 0)),
                gfCostoML: Math.max(0, Number(row.gfCostoML || 0)),
                tabuladorId: String(row.tabuladorId || ''),
                tabuladorDetalle: Array.isArray(row.tabuladorDetalle) && row.tabuladorDetalle.length === 5
                    ? row.tabuladorDetalle.map((r, i) => ({
                        tipo: ['lt', 'range', 'range', 'range', 'gte'][i],
                        min: String(r.min ?? ''),
                        max: String(r.max ?? ''),
                        precioRevendedor: Math.max(0, Number(r.precioRevendedor || 0)),
                        precioGeneral: Math.max(0, Number(r.precioGeneral || 0))
                    }))
                    : [],
                precioRevendedor: Math.max(0, Number(row.precioRevendedor || row.precioReventa || 0)),
                precioVenta: Math.max(0, Number(row.precioVenta || 0)),
                categoria: String(row.categoria || 'General').trim() || 'General',
                tipo: row.tipo === 'gran-formato' ? 'gran-formato' : 'stock'
            }));
        } catch (_) {
            productosData = seedProductos();
        }
    };

    const saveProductos = () => {
        try {
            localStorage.setItem(PRODUCTOS_KEY, JSON.stringify(productosData));
        } catch (_) {}
    };

    const getCategoriasProductos = () => {
        const set = new Set(productosData
            .filter((p) => p.tipo === productosTab)
            .map((p) => String(p.categoria || '').trim())
            .filter(Boolean));
        return ['Todas'].concat(Array.from(set).sort((a, b) => a.localeCompare(b, 'es')));
    };

    const getProductosFiltrados = () => {
        const term = String(productosSearchTerm || '').toLowerCase();
        const code = String(productosCodigoFilter || '').toLowerCase();
        return productosData.filter((p) => {
            if (p.tipo !== productosTab) return false;
            if (productosCategoriaFilter && p.categoria !== productosCategoriaFilter) return false;
            if (productosLowStockOnly && Number(p.existencias || 0) > Number(p.minima || 0)) return false;
            if (term) {
                const blob = `${p.codigo} ${p.producto} ${p.medida} ${p.material} ${p.categoria}`.toLowerCase();
                if (!blob.includes(term)) return false;
            }
            if (code && !String(p.codigo || '').toLowerCase().includes(code)) return false;
            return true;
        });
    };

    const getProductosSeleccionados = () => productosData.filter((p) => productosSelectedIds.has(p.id));

    const renderProductosHead = () => {
        if (!productosTablaHead) return;
        if (productosTab === 'gran-formato') {
            productosTablaHead.innerHTML = `<tr>
                <th>ID</th>
                <th>Producto</th>
                <th>Material</th>
                <th>Precio general M2</th>
                <th>Precio M2 revendedor</th>
                <th>Precio M/lineal general</th>
                <th>Precio M/lineal revendedor</th>
            </tr>`;
            return;
        }
        productosTablaHead.innerHTML = `<tr>
            <th>Producto</th>
            <th>Medida</th>
            <th>Material</th>
            <th>Cant. minima</th>
            <th>Existencias</th>
            <th>Precio para revendedor</th>
            <th>Precio de venta</th>
        </tr>`;
    };

    const toggleProductosToolbarByTab = () => {
        const isGF = productosTab === 'gran-formato';
        if (prodGfToolbar) prodGfToolbar.style.display = isGF ? 'flex' : 'none';
        const iconGrid = document.querySelector('.productos-icon-grid');
        if (iconGrid) iconGrid.style.display = isGF ? 'none' : 'flex';
    };

    const syncProdFormModeByTipo = () => {
        const isGF = (prodFormTipo?.value === 'gran-formato');
        document.querySelectorAll('.prod-stock-only').forEach((elx) => {
            elx.style.display = isGF ? 'none' : '';
        });
        document.querySelectorAll('.prod-gf-only').forEach((elx) => {
            elx.style.display = isGF ? '' : 'none';
        });
        if (prodFormCard) {
            prodFormCard.classList.toggle('gf-compact', isGF);
        }
        const useML = (prodGfCobroTipo?.value === 'm-lineal');
        document.querySelectorAll('.prod-gf-m2-only').forEach((elx) => {
            elx.style.display = (isGF && !useML) ? '' : 'none';
        });
        document.querySelectorAll('.prod-gf-ml-only').forEach((elx) => {
            elx.style.display = (isGF && useML) ? '' : 'none';
        });
    };

    const renderProductosTabla = () => {
        if (!productosTablaBody) return;
        const rows = getProductosFiltrados();
        const totalTabRows = productosData.filter((p) => String(p.tipo || '') === String(productosTab)).length;
        renderProductosHead();
        toggleProductosToolbarByTab();
        if (productosLegend) {
            const baseLabel = productosTab === 'stock' ? 'Listado de productos' : 'Listado de productos gran formato';
            const low = productosLowStockOnly ? ' | agotados o por agotarse' : '';
            const cat = productosCategoriaFilter ? ` | categoría: ${productosCategoriaFilter}` : '';
            const cod = productosCodigoFilter ? ` | código: ${productosCodigoFilter}` : '';
            productosLegend.textContent = `${baseLabel}${low}${cat}${cod}`;
        }

        productosTabStock?.classList.toggle('active', productosTab === 'stock');
        productosTabFormato?.classList.toggle('active', productosTab === 'gran-formato');
        prodLowStock?.classList.toggle('active', productosLowStockOnly);
        if (prodRegistrosCount) {
            prodRegistrosCount.textContent = `Registros: ${totalTabRows}`;
        }

        if (!rows.length) {
            productosTablaBody.innerHTML = '<tr><td colspan="7" style="text-align:center;color:#6b7280;padding:14px;">Sin productos para los filtros actuales.</td></tr>';
            return;
        }

        productosTablaBody.innerHTML = rows.map((row) => {
            const isLowStock = productosTab === 'stock'
                && Number(row.existencias || 0) <= Number(row.minima || 0);
            const classes = [
                productosSelectedIds.has(row.id) ? 'productos-row-selected' : '',
                isLowStock ? 'productos-row-low-stock' : ''
            ].filter(Boolean).join(' ');
            if (productosTab === 'gran-formato') {
                return `<tr data-prod-id="${prodEscape(row.id)}" class="${classes}">
                    <td>${prodEscape(row.codigo || row.id || '')}</td>
                    <td>${prodEscape(row.producto)}</td>
                    <td>${prodEscape(row.material)}</td>
                    <td>${formatMoney(Number(row.gfPrecioGeneralM2 || 0))}</td>
                    <td>${formatMoney(Number(row.gfPrecioRevM2 || 0))}</td>
                    <td>${formatMoney(Number(row.gfPrecioGeneralML || 0))}</td>
                    <td>${formatMoney(Number(row.gfPrecioRevML || 0))}</td>
                </tr>`;
            }
            return `<tr data-prod-id="${prodEscape(row.id)}" class="${classes}">
                <td>${prodEscape(row.producto)}</td>
                <td>${prodEscape(row.medida)}</td>
                <td>${prodEscape(row.material)}</td>
                <td>${Number(row.minima || 0)}</td>
                <td>${Number(row.existencias || 0)}</td>
                <td>${formatMoney(Number(row.precioRevendedor || 0))}</td>
                <td>${formatMoney(Number(row.precioVenta || 0))}</td>
            </tr>`;
        }).join('');
    };

    const exportProductosCsv = (filename = `inventario_${todayISO()}.csv`) => {
        const rows = getProductosFiltrados();
        if (!rows.length) {
            alert('No hay productos para exportar.');
            return;
        }
        const headers = productosTab === 'gran-formato'
            ? ['ID', 'PRODUCTO', 'MATERIAL', 'PRECIO_GENERAL_M2', 'PRECIO_M2_REVENDEDOR', 'PRECIO_M_LINEAL_GENERAL', 'PRECIO_M_LINEAL_REVENDEDOR']
            : ['CODIGO', 'PRODUCTO', 'MEDIDA', 'MATERIAL', 'CANT_MINIMA', 'EXISTENCIAS', 'PRECIO_REVENDEDOR', 'PRECIO_VENTA', 'CATEGORIA', 'TIPO'];
        const escCsv = (v) => `"${String(v ?? '').replace(/"/g, '""')}"`;
        const lines = [headers.join(',')].concat(rows.map((p) => {
            if (productosTab === 'gran-formato') {
                return [
                    p.codigo || p.id,
                    p.producto,
                    p.material,
                    Number(p.gfPrecioGeneralM2 || 0).toFixed(2),
                    Number(p.gfPrecioRevM2 || 0).toFixed(2),
                    Number(p.gfPrecioGeneralML || 0).toFixed(2),
                    Number(p.gfPrecioRevML || 0).toFixed(2)
                ].map(escCsv).join(',');
            }
            return [
                p.codigo,
                p.producto,
                p.medida,
                p.material,
                Number(p.minima || 0),
                Number(p.existencias || 0),
                Number(p.precioRevendedor || 0).toFixed(2),
                Number(p.precioVenta || 0).toFixed(2),
                p.categoria,
                p.tipo
            ].map(escCsv).join(',');
        }));
        const blob = new Blob([lines.join('\n')], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    const parseImportedCsvLine = (line = '') => {
        const out = [];
        let token = '';
        let quote = false;
        for (let i = 0; i < line.length; i += 1) {
            const c = line[i];
            if (c === '"') {
                const next = line[i + 1];
                if (quote && next === '"') {
                    token += '"';
                    i += 1;
                } else {
                    quote = !quote;
                }
            } else if (c === ',' && !quote) {
                out.push(token);
                token = '';
            } else {
                token += c;
            }
        }
        out.push(token);
        return out.map((v) => String(v || '').trim());
    };

    const applyCsvImportProductos = async (file) => {
        if (!file) return;
        const raw = await file.text();
        const lines = raw.split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
        if (lines.length < 2) {
            alert('Archivo sin datos.');
            return;
        }

        const imported = [];
        for (let i = 1; i < lines.length; i += 1) {
            const cols = parseImportedCsvLine(lines[i]);
            if (!cols.length) continue;
            const codigo = cols[0] || `IMP-${Date.now().toString(36).toUpperCase()}-${i}`;
            const producto = cols[1] || 'Producto importado';
            const material = cols[3] || cols[2] || '-';
            const tipo = productosTab === 'gran-formato' ? 'gran-formato' : (cols[9] === 'gran-formato' ? 'gran-formato' : productosTab);
            const medida = cols[2] || '-';
            const minima = Math.max(0, Number(cols[4] || 0));
            const existencias = Math.max(0, Number(cols[5] || 0));
            const precioRevendedor = Math.max(0, Number(cols[6] || 0));
            const precioVenta = Math.max(0, Number(cols[7] || 0));
            const categoria = cols[8] || 'General';
            const gfPrecioGeneralM2 = Math.max(0, Number(cols[3] || 0));
            const gfPrecioRevM2 = Math.max(0, Number(cols[4] || 0));
            const gfPrecioGeneralML = Math.max(0, Number(cols[5] || 0));
            const gfPrecioRevML = Math.max(0, Number(cols[6] || 0));
            imported.push({
                id: `PR-${Date.now().toString(36).toUpperCase()}-${i}`,
                codigo,
                producto,
                medida,
                material,
                minima,
                existencias,
                precioCompra: 0,
                tipoImpresion: '',
                proveedor: '',
                descripcion: '',
                fotoPrincipal: '',
                coloresSubproductos: [],
                gfCobroTipo: 'm2',
                gfAjusteAncho: 'sin',
                gfPrecioGeneralM2: tipo === 'gran-formato' ? gfPrecioGeneralM2 : 0,
                gfPrecioRevM2: tipo === 'gran-formato' ? gfPrecioRevM2 : 0,
                gfPrecioGeneralML: tipo === 'gran-formato' ? gfPrecioGeneralML : 0,
                gfPrecioRevML: tipo === 'gran-formato' ? gfPrecioRevML : 0,
                gfCostoM2: 0,
                gfCostoML: 0,
                tabuladorId: '',
                precioRevendedor: tipo === 'gran-formato' ? gfPrecioRevM2 : precioRevendedor,
                precioVenta: tipo === 'gran-formato' ? gfPrecioGeneralM2 : precioVenta,
                categoria,
                tipo
            });
        }

        if (!imported.length) {
            alert('No se encontraron filas válidas para importar.');
            return;
        }

        productosData = productosData.concat(imported);
        saveProductos();
        renderProductosTabla();
        alert(`Se importaron ${imported.length} productos.`);
    };

    const openProductosPopup = () => {
        if (!popupProductos) return;
        popupProductos.style.display = 'flex';
        popupProductos.setAttribute('aria-hidden', 'false');
        document.body.classList.add('popup-open');
        document.documentElement.classList.add('popup-open');
        productosSelectedIds = new Set();
        productosSelectionAnchorId = '';
        loadProductos();
        renderProductosTabla();
    };

    const closeProductosPopup = () => {
        if (!popupProductos) return;
        popupProductos.style.display = 'none';
        popupProductos.setAttribute('aria-hidden', 'true');
        if (popupListado?.style.display !== 'flex' && popupAccess?.style.display !== 'flex' && popupDesignTracking?.style.display !== 'flex' && popupMisPedidos?.style.display !== 'flex' && popupAjustesTabuladores?.style.display !== 'flex' && popupProdTabulador?.style.display !== 'flex' && popupCaja?.style.display !== 'flex' && popupCalendario?.style.display !== 'flex' && popupClientesModulo?.style.display !== 'flex') {
            document.body.classList.remove('popup-open');
            document.documentElement.classList.remove('popup-open');
        }
    };

    const openProdModal = (modal) => {
        if (!modal) return;
        modal.style.display = 'flex';
        modal.setAttribute('aria-hidden', 'false');
    };

    const closeProdModal = (modal) => {
        if (!modal) return;
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
    };

    const renderCategoriaPopup = () => {
        if (!prodCategoriaLista) return;
        const categories = getCategoriasProductos();
        prodCategoriaLista.innerHTML = categories.map((cat) => {
            const isActive = (!productosCategoriaFilter && cat === 'Todas') || productosCategoriaFilter === cat;
            return `<button type="button" class="productos-modal-item ${isActive ? 'active' : ''}" data-prod-cat="${prodEscape(cat)}">${prodEscape(cat)}</button>`;
        }).join('');
    };

    const renderEntradaSelect = () => {
        if (!prodEntradaSelect) return;
        const term = String(prodEntradaBuscar?.value || '').toLowerCase();
        const rows = productosData.filter((p) => p.tipo === productosTab && `${p.codigo} ${p.producto}`.toLowerCase().includes(term));
        prodEntradaSelect.innerHTML = rows.map((p) => `<option value="${prodEscape(p.id)}">${prodEscape(p.codigo)} - ${prodEscape(p.producto)} (${Number(p.existencias || 0)})</option>`).join('');
    };

    const generarCodigoProducto = () => {
        const stamp = Date.now().toString(36).toUpperCase();
        const pref = (prodFormTipo?.value === 'gran-formato') ? 'GF' : 'ST';
        return `${pref}-${stamp}`;
    };

    const renderProdMainPhotoPreview = () => {
        if (!prodFormFotoPreview) return;
        if (!prodMainPhotoData) {
            prodFormFotoPreview.innerHTML = 'Sin foto principal';
            if (prodTabFotoPreview) prodTabFotoPreview.innerHTML = 'Sin foto principal';
            return;
        }
        const imgHtml = `<img src="${prodEscape(prodMainPhotoData)}" alt="Foto principal">`;
        prodFormFotoPreview.innerHTML = imgHtml;
        if (prodTabFotoPreview) prodTabFotoPreview.innerHTML = imgHtml;
    };

    const renderProdColorDraftList = () => {
        if (!prodColorLista) return;
        if (!prodColorDraftList.length) {
            prodColorLista.innerHTML = '<div style="padding:8px;color:#6b7280;font-size:0.58rem;">Sin colores agregados.</div>';
            return;
        }
        prodColorLista.innerHTML = prodColorDraftList.map((item, idx) => `
            <div class="prod-color-item">
                <div class="prod-color-thumb">${item.foto ? `<img src="${prodEscape(item.foto)}" alt="${prodEscape(item.color)}">` : 'Sin foto'}</div>
                <div><b>${prodEscape(item.color)}</b><span>Existencias: ${Number(item.existencias || 0)}</span></div>
                <button type="button" class="productos-btn" data-prod-color-del="${idx}">Eliminar</button>
            </div>
        `).join('');
    };

    const resetProdForm = () => {
        productoEditandoId = '';
        prodPendingPayload = null;
        prodPendingTabuladorId = '';
        prodPendingTabuladorPrecios = [];
        prodMainPhotoData = '';
        prodColorDraftList = [];
        if (prodFormTitulo) prodFormTitulo.textContent = 'Agregar producto';
        if (prodFormCodigo) prodFormCodigo.value = '';
        if (prodFormTipo) prodFormTipo.value = productosTab;
        if (prodFormProducto) prodFormProducto.value = '';
        if (prodFormCategoria) prodFormCategoria.value = '';
        if (prodFormMedida) prodFormMedida.value = '';
        if (prodFormMaterial) prodFormMaterial.value = '';
        if (prodFormMinima) prodFormMinima.value = '0';
        if (prodFormExistencias) prodFormExistencias.value = '0';
        if (prodFormPrecioCompra) prodFormPrecioCompra.value = '0';
        if (prodFormTipoImpresion) prodFormTipoImpresion.value = '';
        if (prodFormProveedor) prodFormProveedor.value = '';
        if (prodFormDescripcion) prodFormDescripcion.value = '';
        if (prodGfCobroTipo) prodGfCobroTipo.value = 'm2';
        if (prodGfPrecioGeneralM2) prodGfPrecioGeneralM2.value = '0';
        if (prodGfPrecioRevM2) prodGfPrecioRevM2.value = '0';
        if (prodGfPrecioGeneralML) prodGfPrecioGeneralML.value = '0';
        if (prodGfPrecioRevML) prodGfPrecioRevML.value = '0';
        if (prodGfCostoM2) prodGfCostoM2.value = '0';
        if (prodGfCostoML) prodGfCostoML.value = '0';
        if (prodGfAjusteAncho) prodGfAjusteAncho.value = 'sin';
        if (prodFormRevendedor) prodFormRevendedor.value = '0';
        if (prodFormVenta) prodFormVenta.value = '0';
        if (prodFormFotoPrincipal) prodFormFotoPrincipal.value = '';
        if (prodColorNombre) prodColorNombre.value = '';
        if (prodColorExistencias) prodColorExistencias.value = '0';
        if (prodColorFoto) prodColorFoto.value = '';
        renderProdMainPhotoPreview();
        renderProdColorDraftList();
        syncProdFormModeByTipo();
    };

    const openProdFormForEdit = (row) => {
        if (!row) return;
        productoEditandoId = row.id;
        if (prodFormTitulo) prodFormTitulo.textContent = 'Editar producto';
        if (prodFormCodigo) prodFormCodigo.value = row.codigo || '';
        if (prodFormTipo) prodFormTipo.value = row.tipo || 'stock';
        if (prodFormProducto) prodFormProducto.value = row.producto || '';
        if (prodFormCategoria) prodFormCategoria.value = row.categoria || '';
        if (prodFormMedida) prodFormMedida.value = row.medida || '';
        if (prodFormMaterial) prodFormMaterial.value = row.material || '';
        if (prodFormMinima) prodFormMinima.value = String(Number(row.minima || 0));
        if (prodFormExistencias) prodFormExistencias.value = String(Number(row.existencias || 0));
        if (prodFormPrecioCompra) prodFormPrecioCompra.value = String(Number(row.precioCompra || 0));
        if (prodFormTipoImpresion) prodFormTipoImpresion.value = row.tipoImpresion || '';
        if (prodFormProveedor) prodFormProveedor.value = row.proveedor || '';
        if (prodFormDescripcion) prodFormDescripcion.value = row.descripcion || '';
        if (prodGfCobroTipo) prodGfCobroTipo.value = row.gfCobroTipo || 'm2';
        if (prodGfPrecioGeneralM2) prodGfPrecioGeneralM2.value = String(Number(row.gfPrecioGeneralM2 || 0));
        if (prodGfPrecioRevM2) prodGfPrecioRevM2.value = String(Number(row.gfPrecioRevM2 || 0));
        if (prodGfPrecioGeneralML) prodGfPrecioGeneralML.value = String(Number(row.gfPrecioGeneralML || 0));
        if (prodGfPrecioRevML) prodGfPrecioRevML.value = String(Number(row.gfPrecioRevML || 0));
        if (prodGfCostoM2) prodGfCostoM2.value = String(Number(row.gfCostoM2 || 0));
        if (prodGfCostoML) prodGfCostoML.value = String(Number(row.gfCostoML || 0));
        if (prodGfAjusteAncho) prodGfAjusteAncho.value = row.gfAjusteAncho || 'sin';
        if (prodFormRevendedor) prodFormRevendedor.value = String(Number(row.precioRevendedor || 0));
        if (prodFormVenta) prodFormVenta.value = String(Number(row.precioVenta || 0));
        if (prodFormFotoPrincipal) prodFormFotoPrincipal.value = '';
        prodMainPhotoData = row.fotoPrincipal || '';
        prodColorDraftList = Array.isArray(row.coloresSubproductos) ? row.coloresSubproductos.map((c) => ({ ...c })) : [];
        prodPendingTabuladorId = row.tabuladorId || '';
        prodPendingTabuladorPrecios = Array.isArray(row.tabuladorDetalle) ? row.tabuladorDetalle.map((r) => ({
            precioRevendedor: Math.max(0, Number(r.precioRevendedor || 0)),
            precioGeneral: Math.max(0, Number(r.precioGeneral || 0))
        })) : [];
        renderProdMainPhotoPreview();
        renderProdColorDraftList();
        syncProdFormModeByTipo();
    };

    const collectProductFormPayload = () => {
        const payload = {
            codigo: String(prodFormCodigo?.value || '').trim(),
            tipo: prodFormTipo?.value === 'gran-formato' ? 'gran-formato' : 'stock',
            producto: String(prodFormProducto?.value || '').trim(),
            categoria: String(prodFormCategoria?.value || '').trim() || 'General',
            medida: String(prodFormMedida?.value || '').trim() || '-',
            material: String(prodFormMaterial?.value || '').trim() || '-',
            minima: Math.max(0, Number(prodFormMinima?.value || 0)),
            existencias: Math.max(0, Number(prodFormExistencias?.value || 0)),
            precioCompra: Math.max(0, Number(prodFormPrecioCompra?.value || 0)),
            tipoImpresion: String(prodFormTipoImpresion?.value || '').trim(),
            proveedor: String(prodFormProveedor?.value || '').trim(),
            descripcion: String(prodFormDescripcion?.value || '').trim(),
            fotoPrincipal: prodMainPhotoData,
            coloresSubproductos: prodColorDraftList.map((c) => ({
                color: String(c.color || '').trim(),
                existencias: Math.max(0, Number(c.existencias || 0)),
                foto: String(c.foto || '')
            })).filter((c) => c.color),
            gfCobroTipo: prodGfCobroTipo?.value === 'm-lineal' ? 'm-lineal' : 'm2',
            gfAjusteAncho: ['metro', 'medio', 'sin'].includes(prodGfAjusteAncho?.value || '') ? prodGfAjusteAncho.value : 'sin',
            gfPrecioGeneralM2: Math.max(0, Number(prodGfPrecioGeneralM2?.value || 0)),
            gfPrecioRevM2: Math.max(0, Number(prodGfPrecioRevM2?.value || 0)),
            gfPrecioGeneralML: Math.max(0, Number(prodGfPrecioGeneralML?.value || 0)),
            gfPrecioRevML: Math.max(0, Number(prodGfPrecioRevML?.value || 0)),
            gfCostoM2: Math.max(0, Number(prodGfCostoM2?.value || 0)),
            gfCostoML: Math.max(0, Number(prodGfCostoML?.value || 0)),
            tabuladorId: prodPendingTabuladorId,
            precioRevendedor: Math.max(0, Number(prodFormRevendedor?.value || 0)),
            precioVenta: Math.max(0, Number(prodFormVenta?.value || 0))
        };

        if (payload.tipo === 'gran-formato') {
            if (payload.gfCobroTipo === 'm-lineal') {
                payload.gfPrecioGeneralM2 = 0;
                payload.gfPrecioRevM2 = 0;
                payload.gfCostoM2 = 0;
            } else {
                payload.gfPrecioGeneralML = 0;
                payload.gfPrecioRevML = 0;
                payload.gfCostoML = 0;
            }
            payload.precioRevendedor = payload.gfCobroTipo === 'm-lineal' ? payload.gfPrecioRevML : payload.gfPrecioRevM2;
            payload.precioVenta = payload.gfCobroTipo === 'm-lineal' ? payload.gfPrecioGeneralML : payload.gfPrecioGeneralM2;
        }

        if (!payload.codigo || !payload.producto) {
            alert('Código y nombre del producto son obligatorios.');
            return null;
        }
        return payload;
    };

    const getProductoSeleccionado = () => {
        const first = Array.from(productosSelectedIds)[0] || '';
        return productosData.find((p) => p.id === first);
    };

    const openAjustesTabuladoresPopup = () => {
        loadCajaSettings();
        loadTabuladores();
        if (ajustesCajaNombre) ajustesCajaNombre.value = cajaSettings.nombre;
        if (ajustesCajaId) ajustesCajaId.value = cajaSettings.id;
        renderAjustesTabuladorSelect();
        renderAjustesTabuladorTables();
        document.body.classList.add('popup-open');
        document.documentElement.classList.add('popup-open');
        openProdModal(popupAjustesTabuladores);
    };

    const closeAjustesTabuladoresPopup = () => {
        syncAjustesRowsFromUI();
        closeProdModal(popupAjustesTabuladores);
        if (popupListado?.style.display !== 'flex' && popupProductos?.style.display !== 'flex' && popupMisPedidos?.style.display !== 'flex' && popupAccess?.style.display !== 'flex' && popupDesignTracking?.style.display !== 'flex' && popupCaja?.style.display !== 'flex' && popupCalendario?.style.display !== 'flex' && popupClientesModulo?.style.display !== 'flex') {
            document.body.classList.remove('popup-open');
            document.documentElement.classList.remove('popup-open');
        }
    };

    const openProdTabuladorPopup = () => {
        loadTabuladores();
        if (!tabuladoresData.length) {
            alert('Primero configura al menos un tabulador en Ajustes.');
            return;
        }
        const active = getTabuladorById(prodPendingTabuladorId || tabuladoresData[0]?.id || '');
        const savedDetalle = Array.isArray(prodPendingPayload?.tabuladorDetalle) ? prodPendingPayload.tabuladorDetalle : [];
        if (savedDetalle.length === 5) {
            prodPendingTabuladorPrecios = savedDetalle.map((r) => ({
                precioRevendedor: Math.max(0, Number(r.precioRevendedor || 0)),
                precioGeneral: Math.max(0, Number(r.precioGeneral || 0))
            }));
        } else {
            prodPendingTabuladorPrecios = (active?.filas || []).map((f) => ({
                precioRevendedor: Math.max(0, Number(f.precioRevendedor || 0)),
                precioGeneral: Math.max(0, Number(f.precioGeneral || 0))
            }));
        }
        renderProdTabuladorSelect();
        renderProdTabuladorPreview();
        renderProdMainPhotoPreview();
        openProdModal(popupProdTabulador);
    };

    const closeProdTabuladorPopup = () => {
        closeProdModal(popupProdTabulador);
    };

    const commitPendingProduct = () => {
        if (!prodPendingPayload) return;
        syncProdTabPreciosFromUI();
        const active = getTabuladorById(prodPendingTabuladorId);
        const detalle = (active?.filas || []).map((f, i) => ({
            tipo: f.tipo,
            min: String(f.min ?? ''),
            max: String(f.max ?? ''),
            precioRevendedor: Math.max(0, Number(prodPendingTabuladorPrecios[i]?.precioRevendedor || 0)),
            precioGeneral: Math.max(0, Number(prodPendingTabuladorPrecios[i]?.precioGeneral || 0))
        }));

        const payload = {
            ...prodPendingPayload,
            tabuladorId: prodPendingTabuladorId || '',
            tabuladorDetalle: detalle,
            precioRevendedor: Math.max(0, Number(detalle[0]?.precioRevendedor || prodPendingPayload.precioRevendedor || 0)),
            precioVenta: Math.max(0, Number(detalle[0]?.precioGeneral || prodPendingPayload.precioVenta || 0))
        };

        if (productoEditandoId) {
            productosData = productosData.map((p) => p.id === productoEditandoId ? { ...p, ...payload } : p);
            productosSelectedIds = new Set([productoEditandoId]);
            productosSelectionAnchorId = productoEditandoId;
        } else {
            const newId = `PR-${Date.now().toString(36).toUpperCase()}`;
            productosData.unshift({ id: newId, ...payload });
            productosSelectedIds = new Set([newId]);
            productosSelectionAnchorId = newId;
        }

        saveProductos();
        renderProductosTabla();
        closeProdTabuladorPopup();
        closeProdModal(popupProdForm);
        prodPendingPayload = null;
        prodPendingTabuladorPrecios = [];
    };

    window.openProductosPopupGlobal = openProductosPopup;

    const recalcResumen = () => {
        const subtotalVal = ordenLineas.reduce((acc, row) => acc + (Number(row.precio) * Number(row.cantidad)), 0);
        const impuestosVal = subtotalVal * (ordenTaxRate / 100);
        const descuentoPctVal = subtotalVal * (ordenDiscount / 100);
        const descuentoVal = descuentoPctVal + Math.max(0, Number(ordenDiscountAmount || 0));
        const totalVal = Math.max(0, subtotalVal + impuestosVal - descuentoVal);
        const gananciaVal = totalVal - Number(ordenInversion || 0);

        refs.subtotal.textContent = formatMoney(subtotalVal);
        refs.impuestos.textContent = formatMoney(impuestosVal);
        refs.descuento.textContent = formatMoney(descuentoVal);
        refs.inversion.textContent = formatMoney(ordenInversion);
        refs.ganancia.textContent = formatMoney(gananciaVal);
        refs.totalMain.innerHTML = `<span class="orden-total-label">TOTAL</span><span class="orden-total-amount">${formatMoney(totalVal)}</span>`;

        window.cotizadorActivo = {
            id: `COT-${Date.now().toString(36).toUpperCase()}`,
            clienteNombre: refs.clienteNombre.textContent || '',
            clienteNumero: refs.clienteTelefono.value || '',
            clienteCorreo: refs.clienteCorreo.value || '',
            fechaEntrega: refs.fechaEntrega.value || '',
            subtotal: subtotalVal,
            impuestos: impuestosVal,
            descuento: descuentoVal,
            total: totalVal,
            lineas: ordenLineas.slice()
        };
    };

    const renderTabla = () => {
        if (!refs.tablaBody) return;
        if (!ordenLineas.length) {
            refs.tablaBody.innerHTML = '<tr><td colspan="6" style="text-align:center;color:#7f7f7f;padding:12px;">No hay productos agregados.</td></tr>';
            recalcResumen();
            return;
        }

        refs.tablaBody.innerHTML = ordenLineas.map((row, idx) => {
            const importe = Number(row.precio) * Number(row.cantidad);
            const cls = idx === ordenLineaActiva ? ' class="orden-row-selected"' : '';
            return `<tr data-orden-row="${idx}"${cls}>
                <td>${row.producto}</td>
                <td>${row.medida}</td>
                <td>${row.material}</td>
                <td>${formatMoney(row.precio)}</td>
                <td data-orden-qty="${idx}" class="orden-qty-cell">${row.cantidad}</td>
                <td>${formatMoney(importe)}</td>
            </tr>`;
        }).join('');

        recalcResumen();
    };

    const getProductosStockOrden = () => {
        const term = String(ordenStockSearchTerm || '').trim().toLowerCase();
        return productosData
            .filter((p) => String(p.tipo || '').toLowerCase() === String(ordenPickerTipo || 'stock').toLowerCase())
            .filter((p) => {
                if (!term) return true;
                const blob = `${p.codigo || ''} ${p.producto || ''} ${p.medida || ''} ${p.material || ''} ${p.categoria || ''}`.toLowerCase();
                return blob.includes(term);
            })
            .sort((a, b) => String(a.producto || '').localeCompare(String(b.producto || ''), 'es'));
    };

    const getProductoStockSeleccionadoOrden = () => {
        if (!ordenStockSelectedId) return null;
        return productosData.find((p) => p.id === ordenStockSelectedId && String(p.tipo || '').toLowerCase() === String(ordenPickerTipo || 'stock').toLowerCase()) || null;
    };

    const getPrecioProductoStockOrden = (producto) => {
        if (!producto) return 0;
        return ordenStockPriceMode === 'revendedor'
            ? Number(producto.precioRevendedor || 0)
            : Number(producto.precioVenta || 0);
    };

    const getProductoTabuladorFilas = (producto) => {
        if (!producto) return [];
        if (Array.isArray(producto.tabuladorDetalle) && producto.tabuladorDetalle.length) {
            return producto.tabuladorDetalle;
        }
        if (producto.tabuladorId) {
            const tab = getTabuladorById(String(producto.tabuladorId || ''));
            if (tab && Array.isArray(tab.filas)) return tab.filas;
        }
        return [];
    };

    const getLabelRangoTabulador = (fila = {}) => {
        const tipo = String(fila.tipo || 'range');
        const min = String(fila.min || '').trim();
        const max = String(fila.max || '').trim();
        if (tipo === 'lt') return `Menor a ${max || '?'} pzas`;
        if (tipo === 'gte') return `${min || '?'} pzas o más`;
        return `${min || '?'} a ${max || '?'} pzas`;
    };

    const openOrdenStockTabuladorInfo = () => {
        const producto = getProductoStockSeleccionadoOrden();
        if (!producto) {
            notifyError('Selecciona un producto para ver su tabulador.', 'Tabulador');
            return;
        }

        const filas = getProductoTabuladorFilas(producto);
        if (!filas.length) {
            notifyError('Este producto no tiene tabulador configurado.', 'Tabulador');
            return;
        }

        const campoPrecio = ordenStockPriceMode === 'revendedor' ? 'precioRevendedor' : 'precioGeneral';
        const modoLabel = ordenStockPriceMode === 'revendedor' ? 'REVENDEDOR' : 'GENERAL';
        const detalle = filas.map((fila, idx) => {
            const precio = Number(fila?.[campoPrecio] || 0);
            return `${idx + 1}. ${getLabelRangoTabulador(fila)}: ${formatMoney(precio)} c/u`;
        }).join('\n');

        notifyInfo(detalle, `Tabulador ${modoLabel} · ${String(producto.producto || 'Producto')}`);
    };

    const setOrdenStockQty = (value) => {
        const parsed = Math.floor(Number(value));
        ordenStockQty = Number.isFinite(parsed) && parsed > 0 ? parsed : 1;
        if (ordenStockQtyInput) ordenStockQtyInput.value = String(ordenStockQty);
    };

    const openOrdenStockQtyPopup = () => {
        if (!ordenStockQtyPopup || !ordenStockQtyInput) return;
        setOrdenStockQty(1);
        ordenStockQtyPopup.style.display = 'block';
        ordenStockQtyInput.focus();
        ordenStockQtyInput.select();
    };

    const closeOrdenStockQtyPopup = () => {
        if (ordenStockQtyPopup) ordenStockQtyPopup.style.display = 'none';
    };

    const renderOrdenStockPriceModeUI = () => {
        const labels = document.querySelectorAll('.orden-stock-price-option');
        labels.forEach((lbl) => {
            const input = lbl.querySelector('input[name="ordenStockPriceMode"]');
            lbl.classList.toggle('active', !!input && input.value === ordenStockPriceMode);
        });
        if (ordenStockPriceGeneral) ordenStockPriceGeneral.checked = ordenStockPriceMode === 'general';
        if (ordenStockPriceRevendedor) ordenStockPriceRevendedor.checked = ordenStockPriceMode === 'revendedor';
    };

    const renderOrdenStockDetalle = () => {
        const producto = getProductoStockSeleccionadoOrden();
        if (!producto) {
            if (ordenStockPhoto) ordenStockPhoto.textContent = 'Selecciona un producto';
            if (ordenStockColorsList) ordenStockColorsList.innerHTML = '<div class="orden-stock-color-row"><span>Sin colores</span><b>0</b></div>';
            if (ordenStockExistencias) ordenStockExistencias.textContent = '0';
            if (ordenStockPrecio) ordenStockPrecio.textContent = formatMoney(0);
            if (ordenStockCosto) ordenStockCosto.textContent = formatMoney(0);
            if (ordenStockGanancia) ordenStockGanancia.textContent = formatMoney(0);
            if (ordenStockTotal) ordenStockTotal.textContent = formatMoney(0);
            if (ordenStockAccept) ordenStockAccept.disabled = true;
            return;
        }

        const precio = getPrecioProductoStockOrden(producto);
        const costo = Number(producto.precioCompra || 0);
        const ganancia = precio - costo;
        const total = precio * Number(ordenStockQty || 1);

        if (ordenStockPhoto) {
            if (producto.fotoPrincipal) {
                ordenStockPhoto.innerHTML = `<img src="${prodEscape(producto.fotoPrincipal)}" alt="${prodEscape(producto.producto || 'Producto')}">`;
            } else {
                ordenStockPhoto.textContent = 'Sin foto principal';
            }
        }

        if (ordenStockColorsList) {
            const colores = Array.isArray(producto.coloresSubproductos) ? producto.coloresSubproductos : [];
            if (!colores.length) {
                ordenStockColorsList.innerHTML = '<div class="orden-stock-color-row"><span>Sin colores registrados</span><b>-</b></div>';
            } else {
                ordenStockColorsList.innerHTML = colores.map((c) => `
                    <div class="orden-stock-color-row">
                        <span>${prodEscape(c.color || 'Color')}</span>
                        <b>${Number(c.existencias || 0)}</b>
                    </div>
                `).join('');
            }
        }

        if (ordenStockExistencias) ordenStockExistencias.textContent = String(Math.max(0, Number(producto.existencias || 0)));
        if (ordenStockPrecio) ordenStockPrecio.textContent = formatMoney(precio);
        if (ordenStockCosto) ordenStockCosto.textContent = formatMoney(costo);
        if (ordenStockGanancia) ordenStockGanancia.textContent = formatMoney(ganancia);
        if (ordenStockTotal) ordenStockTotal.textContent = formatMoney(total);
        if (ordenStockAccept) ordenStockAccept.disabled = false;
    };

    const renderOrdenStockTabla = () => {
        if (!ordenStockTableBody) return;
        const rows = getProductosStockOrden();

        if (!rows.length) {
            const txt = ordenPickerTipo === 'gran-formato'
                ? 'Sin productos de gran formato para ese filtro.'
                : 'Sin productos de stock para ese filtro.';
            ordenStockTableBody.innerHTML = `<tr><td colspan="3" style="text-align:center;color:#6b7280;padding:12px;">${txt}</td></tr>`;
            ordenStockSelectedId = '';
            if (ordenStockResultCount) ordenStockResultCount.textContent = '0 resultados';
            renderOrdenStockDetalle();
            return;
        }

        if (!ordenStockSelectedId || !rows.some((p) => p.id === ordenStockSelectedId)) {
            ordenStockSelectedId = rows[0].id;
        }

        ordenStockTableBody.innerHTML = rows.map((p) => {
            const active = p.id === ordenStockSelectedId ? ' class="active"' : '';
            return `<tr data-orden-stock-id="${prodEscape(p.id)}"${active}>
                <td>${prodEscape(p.producto || '')}</td>
                <td>${prodEscape(p.medida || '-')}</td>
                <td>${prodEscape(p.material || '-')}</td>
            </tr>`;
        }).join('');

        if (ordenStockResultCount) {
            ordenStockResultCount.textContent = `${rows.length} resultado${rows.length === 1 ? '' : 's'}`;
        }
        renderOrdenStockDetalle();
    };

    const openOrdenStockPopup = (tipo = 'stock') => {
        if (!ordenStockPopup) return;
        loadProductos();
        ordenPickerTipo = tipo === 'gran-formato' ? 'gran-formato' : 'stock';
        ordenStockSearchTerm = '';
        ordenStockPriceMode = 'general';
        ordenStockSelectedId = '';
        setOrdenStockQty(1);
        closeOrdenStockQtyPopup();
        if (ordenStockSearch) {
            ordenStockSearch.placeholder = ordenPickerTipo === 'gran-formato'
                ? 'Nombre, medida, material, categoria o codigo de gran formato'
                : 'Nombre, medida, material, categoria o codigo';
        }
        const stockTitle = document.getElementById('ordenStockTitle');
        if (stockTitle) {
            stockTitle.textContent = ordenPickerTipo === 'gran-formato'
                ? 'Detalle del producto de gran formato'
                : 'Detalle del producto de stock';
        }
        renderOrdenStockPriceModeUI();
        renderOrdenStockTabla();
        if (ordenStockSearch) ordenStockSearch.value = '';
        ordenStockPopup.style.display = 'flex';
        ordenStockPopup.setAttribute('aria-hidden', 'false');
        if (ordenStockSearch) {
            setTimeout(() => ordenStockSearch.focus(), 20);
        }
    };

    const closeOrdenStockPopup = () => {
        if (!ordenStockPopup) return;
        closeOrdenStockQtyPopup();
        ordenStockPopup.style.display = 'none';
        ordenStockPopup.setAttribute('aria-hidden', 'true');
    };

    const addLineaDesdeStockSeleccion = () => {
        const producto = getProductoStockSeleccionadoOrden();
        if (!producto) {
            alert('Selecciona un producto.');
            return;
        }

        const qty = Math.max(1, Math.floor(Number(ordenStockQty || 1)));
        const available = Math.max(0, Number(producto.existencias || 0));
        if (available > 0 && qty > available) {
            alert(`No hay suficiente stock. Existencias disponibles: ${available}.`);
            return;
        }

        ordenLineas.push({
            producto: producto.producto || 'Producto de stock',
            medida: producto.medida || '-',
            material: producto.material || '-',
            precio: getPrecioProductoStockOrden(producto),
            cantidad: qty
        });
        ordenLineaActiva = ordenLineas.length - 1;
        renderTabla();
        closeOrdenStockPopup();
    };

    const addLineaManual = (tipo) => {
        const pDefault = tipo === 'stock' ? 'Producto de stock' : 'Producto gran formato';
        const producto = (prompt('Producto:', pDefault) || '').trim();
        if (!producto) return;
        const medida = (prompt('Medida:', '50x70 cm') || '').trim() || '-';
        const material = (prompt('Material:', tipo === 'stock' ? 'Stock' : 'Lona') || '').trim() || '-';
        const precio = Number(prompt('Precio unitario:', '0') || 0);
        const cantidad = Number(prompt('Cantidad:', '1') || 1);
        if (!Number.isFinite(precio) || !Number.isFinite(cantidad) || cantidad <= 0) {
            alert('Precio o cantidad inválidos.');
            return;
        }
        ordenLineas.push({ producto, medida, material, precio, cantidad });
        ordenLineaActiva = ordenLineas.length - 1;
        renderTabla();
    };

    const addLinea = (tipo) => {
        if (tipo === 'stock' || tipo === 'gran-formato') {
            openOrdenStockPopup(tipo);
            return;
        }
        addLineaManual(tipo);
    };

    const resetOrden = () => {
        if (!ordenTickets.length) {
            initOrdenTickets();
            return;
        }
        const limpio = buildEmptyOrdenState();
        ordenTickets[ordenTicketActivo] = limpio;
        applyOrdenState(limpio);
        renderTicketTabs();
    };

    const ajustarFechaEntrega = (source = 'dias') => {
        if (!refs.entregaDias || !refs.fechaEntrega || syncingEntrega) return;
        syncingEntrega = true;

        const today = new Date();
        today.setHours(0, 0, 0, 0);

        if (source === 'dias') {
            const dias = Math.max(1, Number(refs.entregaDias.value || 1));
            refs.entregaDias.value = String(dias);
            const base = new Date(today);
            base.setDate(base.getDate() + dias);
            refs.fechaEntrega.value = base.toISOString().slice(0, 10);
        } else {
            const selected = new Date(refs.fechaEntrega.value || todayISO());
            selected.setHours(0, 0, 0, 0);
            const diffMs = selected.getTime() - today.getTime();
            const diffDays = Math.max(1, Math.ceil(diffMs / 86400000));
            refs.entregaDias.value = String(diffDays);
        }

        syncingEntrega = false;
    };

    const aplicarCliente = (cliente = {}) => {
        const nombre = cliente.nombre || cliente.clienteNombre || 'SIN CLIENTE SELECCIONADO';
        refs.clienteNombre.textContent = nombre.toUpperCase();
        refs.clienteId.value = cliente.id || 'SIN ASIGNAR';
        refs.clienteCorreo.value = cliente.email || cliente.correo || '';
        refs.clienteTelefono.value = cliente.telefono || cliente.numero || '';
        refs.clienteNegocio.value = cliente.negocio || cliente.empresa || '';
    };

    const openPopup = () => {
        popupListado.style.display = 'flex';
        popupListado.setAttribute('aria-hidden', 'false');
        document.body.classList.add('popup-open');
        document.documentElement.classList.add('popup-open');
        initOrdenTickets();
    };

    const closePopup = () => {
        closeOrdenStockPopup();
        popupListado.style.display = 'none';
        popupListado.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('popup-open');
        document.documentElement.classList.remove('popup-open');
    };

    window.openPopupListadoGlobal = openPopup;
    window.closePopupListadoGlobal = closePopup;
    window.aplicarClienteEnCotizacionGlobal = aplicarCliente;

    const openQuotePopup = () => {
        if (!refs.cotizacionPopup) return;
        refs.cotizacionPopup.style.display = 'flex';
        refs.cotizacionPopup.setAttribute('aria-hidden', 'false');
    };

    const closeQuotePopup = () => {
        if (!refs.cotizacionPopup) return;
        refs.cotizacionPopup.style.display = 'none';
        refs.cotizacionPopup.setAttribute('aria-hidden', 'true');
    };

    btnListadoRapido.onclick = openPopup;
    if (btnCerrarPopupListado) btnCerrarPopupListado.onclick = closePopup;
    if (btnOrdenBackMenu) {
        btnOrdenBackMenu.onclick = () => {
            closePopup();
            if (typeof mostrarInicioSistema === 'function') {
                mostrarInicioSistema();
            }
        };
    }

    if (refs.tablaBody) {
        refs.tablaBody.addEventListener('click', (ev) => {
            const qtyCell = ev.target.closest('[data-orden-qty]');
            if (qtyCell) {
                const idxQty = Number(qtyCell.getAttribute('data-orden-qty'));
                if (!Number.isFinite(idxQty) || idxQty < 0 || idxQty >= ordenLineas.length) return;
                const actual = Math.max(1, Number(ordenLineas[idxQty].cantidad || 1));
                const val = prompt('Nueva cantidad:', String(actual));
                if (val === null) return;
                const n = Math.floor(Number(val));
                if (!Number.isFinite(n) || n <= 0) {
                    notifyError('Cantidad inválida.', 'Cantidad');
                    return;
                }
                ordenLineas[idxQty].cantidad = n;
                ordenLineaActiva = idxQty;
                renderTabla();
                saveTicketActivo();
                return;
            }
            const tr = ev.target.closest('tr[data-orden-row]');
            if (!tr) return;
            ordenLineaActiva = Number(tr.dataset.ordenRow);
            renderTabla();
        });
    }

    const btnAddStock = el('ordenAddStock');
    const btnAddFormato = el('ordenAddFormato');
    const btnEliminar = el('ordenEliminarProducto');
    const btnImpuestos = el('ordenBtnImpuestos');
    const btnDescuento = el('ordenBtnDescuento');
    const btnCotizacion = el('ordenBtnCotizacion');
    const btnLimpiar = el('ordenBtnLimpiar');
    const btnRegistrar = el('ordenRegistrarCliente');
    const btnSeleccionar = el('ordenSeleccionarCliente');

    if (ordenStockSearch) {
        ordenStockSearch.addEventListener('input', () => {
            ordenStockSearchTerm = ordenStockSearch.value || '';
            renderOrdenStockTabla();
        });
    }

    const onOrdenStockPriceModeChange = (ev) => {
        const value = String(ev?.target?.value || 'general');
        ordenStockPriceMode = value === 'revendedor' ? 'revendedor' : 'general';
        renderOrdenStockPriceModeUI();
        renderOrdenStockDetalle();
    };
    if (ordenStockPriceGeneral) ordenStockPriceGeneral.addEventListener('change', onOrdenStockPriceModeChange);
    if (ordenStockPriceRevendedor) ordenStockPriceRevendedor.addEventListener('change', onOrdenStockPriceModeChange);

    if (ordenStockTableBody) {
        ordenStockTableBody.addEventListener('click', (ev) => {
            const tr = ev.target.closest('tr[data-orden-stock-id]');
            if (!tr) return;
            ordenStockSelectedId = String(tr.dataset.ordenStockId || '');
            renderOrdenStockTabla();
        });
    }

    if (ordenStockQtyInput) {
        if (ordenStockQtyPopup) ordenStockQtyPopup.style.display = 'none';
        ordenStockQtyInput.addEventListener('input', () => {
            setOrdenStockQty(ordenStockQtyInput.value);
            renderOrdenStockDetalle();
        });
        ordenStockQtyInput.addEventListener('keydown', (ev) => {
            if (ev.key === 'Enter') {
                ev.preventDefault();
                setOrdenStockQty(ordenStockQtyInput.value);
                renderOrdenStockDetalle();
                addLineaDesdeStockSeleccion();
            }
            if (ev.key === 'Escape') {
                ev.preventDefault();
                closeOrdenStockQtyPopup();
            }
        });
        ordenStockQtyInput.addEventListener('blur', () => {
            setOrdenStockQty(ordenStockQtyInput.value);
            renderOrdenStockDetalle();
        });
    }

    if (ordenStockAccept) {
        ordenStockAccept.addEventListener('click', () => {
            addLineaDesdeStockSeleccion();
        });
    }

    if (ordenStockClose) {
        ordenStockClose.addEventListener('click', () => {
            closeOrdenStockPopup();
        });
    }

    if (ordenStockTabuladorBtn) {
        ordenStockTabuladorBtn.addEventListener('click', () => {
            openOrdenStockTabuladorInfo();
        });
    }

    if (ordenStockPopup) {
        ordenStockPopup.addEventListener('click', (ev) => {
            if (ev.target === ordenStockPopup) {
                closeOrdenStockPopup();
                return;
            }
            if (ordenStockQtyPopup && ordenStockQtyPopup.style.display === 'block') {
                const insideQty = ev.target.closest('#ordenStockQtyPopup, #ordenStockQtyInput');
                if (!insideQty) closeOrdenStockQtyPopup();
            }
        });

        ordenStockPopup.addEventListener('keydown', (ev) => {
            if (ordenStockPopup.style.display !== 'flex') return;
            if (ev.key === 'Enter' && ev.target !== ordenStockQtyInput) {
                ev.preventDefault();
                const p = getProductoStockSeleccionadoOrden();
                if (!p) return;
                openOrdenStockQtyPopup();
            }
        });
    }

    document.addEventListener('keydown', (ev) => {
        if (ev.key !== 'Escape') return;
        if (ordenStockPopup?.style.display === 'flex') {
            closeOrdenStockPopup();
            return;
        }
        if (ordenPagoPopup?.style.display === 'flex') {
            closeOrdenPopup(ordenPagoPopup);
            return;
        }
        if (ordenConfirmPopup?.style.display === 'flex') {
            closeOrdenPopup(ordenConfirmPopup);
            return;
        }
        if (ordenVentaRapidaPopup?.style.display === 'flex') {
            closeOrdenPopup(ordenVentaRapidaPopup);
            return;
        }
        if (ordenDescuentoPopup?.style.display === 'flex') {
            closeOrdenPopup(ordenDescuentoPopup);
            return;
        }
        if (ordenClienteSelectPopup?.style.display === 'flex') {
            closeOrdenClienteSelectPopup();
        }
    });

    if (btnAddStock) btnAddStock.onclick = () => addLinea('stock');
    if (btnAddFormato) btnAddFormato.onclick = () => addLinea('gran-formato');
    if (btnEliminar) {
        btnEliminar.onclick = () => {
            if (ordenLineaActiva < 0 || ordenLineaActiva >= ordenLineas.length) {
                alert('Selecciona una fila de la tabla para eliminar.');
                return;
            }
            ordenLineas.splice(ordenLineaActiva, 1);
            ordenLineaActiva = -1;
            renderTabla();
        };
    }

    if (btnImpuestos) {
        btnImpuestos.onclick = () => {
            ordenTaxRate = Number(ordenTaxRate || 0) > 0 ? 0 : 16;
            btnImpuestos.classList.toggle('active', ordenTaxRate > 0);
            recalcResumen();
            saveTicketActivo();
        };
    }

    if (btnDescuento) {
        btnDescuento.onclick = () => {
            openDescuentoPopup();
        };
    }

    if (btnCotizacion) btnCotizacion.onclick = openQuotePopup;
    if (btnLimpiar) {
        btnLimpiar.onclick = () => {
            const msg = ordenTickets.length > 1
                ? '¿Seguro que deseas eliminar este ticket completo?'
                : '¿Seguro que deseas limpiar este ticket?';
            showConfirmPopup(msg, () => {
                removeCurrentTicket();
            });
        };
    }

    if (ordenTicketTabs) {
        ordenTicketTabs.addEventListener('click', (ev) => {
            const addBtn = ev.target.closest('#ordenTicketAdd');
            if (addBtn) {
                addNewTicket();
                return;
            }
            const ticketBtn = ev.target.closest('.orden-ticket-tab[data-ticket-index]');
            if (!ticketBtn) return;
            switchTicket(ticketBtn.dataset.ticketIndex);
        });
    }

    if (ordenBtnVentaRapida) {
        ordenBtnVentaRapida.addEventListener('click', () => {
            openVentaRapidaPopup();
        });
    }

    if (ordenVrCancelar) {
        ordenVrCancelar.addEventListener('click', () => closeOrdenPopup(ordenVentaRapidaPopup));
    }

    if (ordenVrAgregar) {
        ordenVrAgregar.addEventListener('click', () => {
            const nombre = String(ordenVrNombre?.value || '').trim();
            const monto = Number(ordenVrMonto?.value || 0);
            if (!nombre) {
                notifyError('Escribe el nombre para la venta rápida.', 'Venta rápida');
                return;
            }
            if (!Number.isFinite(monto) || monto <= 0) {
                notifyError('Escribe un monto válido para la venta rápida.', 'Venta rápida');
                return;
            }
            ordenLineas.push({
                producto: nombre,
                medida: '-',
                material: 'VENTA RÁPIDA',
                precio: monto,
                cantidad: 1
            });
            ordenLineaActiva = ordenLineas.length - 1;
            renderTabla();
            saveTicketActivo();
            closeOrdenPopup(ordenVentaRapidaPopup);
            notifyInfo('Producto de venta rápida agregado al ticket.', 'Venta rápida');
        });
    }

    if (btnRegistrar) {
        btnRegistrar.onclick = () => {
            ordenClienteFormMode = 'register-order';
            openClientesFormPopup('add');
        };
    }

    if (btnSeleccionar) {
        btnSeleccionar.onclick = () => {
            const rows = getClientesOrdenSelectable();
            if (!rows.length) {
                notifyError('No hay clientes registrados todavía.', 'Clientes');
                return;
            }
            openOrdenClienteSelectPopup();
        };
    }

    if (refs.entregaDias) refs.entregaDias.addEventListener('input', () => ajustarFechaEntrega('dias'));
    if (refs.fechaEntrega) refs.fechaEntrega.addEventListener('change', () => ajustarFechaEntrega('fecha'));

    document.querySelectorAll('.orden-pay-btn').forEach((btn) => {
        btn.addEventListener('click', () => {
            const method = String(btn.dataset.pay || '').toUpperCase().trim();
            if (!method) return;

            if (method === 'GUARDAR SIN ANTICIPO') {
                if (!ensureCanProcessPayment()) return;
                showConfirmPopup('Guardar venta sin anticipo (pago contra entrega)?', () => {
                    registrarPagoYActivarMetodo('GUARDAR SIN ANTICIPO', 0, { contraEntrega: true });
                    notifyInfo('Venta guardada sin anticipo. Se liquidará al entregar.', 'Sin anticipo');
                });
                return;
            }

            if (!ensureCanProcessPayment()) return;

            if (method === 'EFECTIVO' || method === 'TARJETA' || method === 'TRANSFERENCIA' || method === 'DEPOSITO') {
                renderPagoPopup(method);
            }
        });
    });

    if (ordenPagoPopup) {
        ordenPagoPopup.addEventListener('click', (ev) => {
            if (ev.target === ordenPagoPopup) closeOrdenPopup(ordenPagoPopup);
        });
    }

    if (ordenConfirmPopup) {
        ordenConfirmPopup.addEventListener('click', (ev) => {
            if (ev.target === ordenConfirmPopup) closeOrdenPopup(ordenConfirmPopup);
        });
    }

    if (ordenVentaRapidaPopup) {
        ordenVentaRapidaPopup.addEventListener('click', (ev) => {
            if (ev.target === ordenVentaRapidaPopup) closeOrdenPopup(ordenVentaRapidaPopup);
        });
    }

    if (ordenDescuentoPopup) {
        ordenDescuentoPopup.addEventListener('click', (ev) => {
            if (ev.target === ordenDescuentoPopup) closeOrdenPopup(ordenDescuentoPopup);
        });
    }

    if (ordenDescuentoCancelar) {
        ordenDescuentoCancelar.addEventListener('click', () => closeOrdenPopup(ordenDescuentoPopup));
    }

    if (ordenDescuentoLimpiar) {
        ordenDescuentoLimpiar.addEventListener('click', () => {
            ordenDiscount = 0;
            ordenDiscountAmount = 0;
            ordenDiscountLabel = '';
            recalcResumen();
            saveTicketActivo();
            closeOrdenPopup(ordenDescuentoPopup);
        });
    }

    if (ordenDescuentoAplicar) {
        ordenDescuentoAplicar.addEventListener('click', () => {
            applyDescuento();
        });
    }

    const quoteGuardar = el('ordenQuoteGuardar');
    const quoteWA = el('ordenQuoteWhatsapp');
    const quoteTicket = el('ordenQuoteTicket');
    const quotePdf = el('ordenQuotePdf');
    const quoteVenta = el('ordenQuoteVenta');
    const quoteVerCotizaciones = el('ordenQuoteVerCotizaciones');
    if (quoteGuardar) {
        quoteGuardar.onclick = () => {
            alert('Borrador guardado localmente. Para contar como cotización usa WhatsApp o PDF.');
            closeQuotePopup();
        };
    }
    if (quoteWA) {
        quoteWA.onclick = () => {
            loadMisPedidos();
            const registro = buildPedidoRegistro('cotizacion');
            upsertMisPedidoRegistro(registro);
            saveMisPedidos();
            const chatTarget = window.chatClientePedidoTarget;
            if (chatTarget && chatTarget.id && typeof window.pushMensajeChatCliente === 'function') {
                const resumen = [
                    `Cotización ${registro.folio}`,
                    `Cliente: ${registro.clienteNombre}`,
                    `Total: ${formatMoney(registro.total)}`,
                    `Entrega: ${registro.fechaEntrega}`,
                    `Estatus: pendiente de aprobación`
                ].join('\n');

                const productoChat = String(chatTarget.producto || chatTarget.modulo || chatTarget.tipoProducto || 'Producto personalizado');
                window.pushMensajeChatCliente(chatTarget.id, {
                    origen: 'propio',
                    texto: resumen,
                    fecha: new Date().toISOString(),
                    pedido: {
                        folio: registro.folio,
                        total: Number(registro.total || 0),
                        fechaEntrega: registro.fechaEntrega,
                        clienteNombre: registro.clienteNombre,
                        telefono: registro.telefono,
                        producto: productoChat,
                        cantidad: 1,
                        metodoPago: registro.metodoPago
                    }
                });

                if (typeof window.actualizarFlujoChatCliente === 'function') {
                    window.actualizarFlujoChatCliente(chatTarget.id, {
                        pedidoEnviado: true,
                        muestraEnviada: false,
                        produccionEnviada: false,
                        pedido: {
                            folio: registro.folio,
                            total: Number(registro.total || 0),
                            fechaEntrega: registro.fechaEntrega,
                            clienteNombre: registro.clienteNombre,
                            telefono: registro.telefono,
                            producto: productoChat,
                            cantidad: 1,
                            metodoPago: registro.metodoPago
                        }
                    });
                }

                closeQuotePopup();
                closePopup();
                alert('Cotización enviada al chat del cliente. Ahora podrás enviar muestra desde su chat.');
                if (typeof window.openChatClienteById === 'function') {
                    window.openChatClienteById(chatTarget.id);
                }
                window.chatClientePedidoTarget = null;
                return;
            }

            const numero = (refs.clienteTelefono.value || '').replace(/\D/g, '');
            if (!numero) {
                alert('Primero captura el teléfono del cliente.');
                return;
            }
            const totalTxt = refs.totalMain.textContent || 'TOTAL $0.00';
            const mensaje = `Hola ${refs.clienteNombre.textContent}. Tu cotización está lista. ${totalTxt}`;
            window.open(`https://wa.me/52${numero}?text=${encodeURIComponent(mensaje)}`, '_blank');
        };
    }
    if (quoteTicket) quoteTicket.onclick = () => window.print();
    if (quotePdf) {
        quotePdf.onclick = () => {
            loadMisPedidos();
            const registro = buildPedidoRegistro('cotizacion');
            upsertMisPedidoRegistro(registro);
            saveMisPedidos();
            alert('Se abrirá el diálogo de impresión para guardar como PDF.');
            window.print();
        };
    }
    if (quoteVenta) {
        quoteVenta.onclick = () => {
            if (Number(ordenAnticipo || 0) <= 0) {
                alert('Para contar como venta debes registrar dinero en un método de pago.');
                return;
            }
            alert('La venta ya se registró al capturar el pago.');
            closeQuotePopup();
        };
    }

    if (quoteVerCotizaciones) {
        quoteVerCotizaciones.onclick = () => {
            closeQuotePopup();
            misPedidosTab = 'cotizacion';
            openMisPedidosPopup();
        };
    }

    if (refs.cotizacionPopup) {
        refs.cotizacionPopup.addEventListener('click', (ev) => {
            if (ev.target === refs.cotizacionPopup) closeQuotePopup();
        });

        document.addEventListener('keydown', (ev) => {
            if (ev.key !== 'Escape') return;
            if (refs.cotizacionPopup.style.display === 'flex') {
                ev.preventDefault();
                closeQuotePopup();
            }
        });
    }

    if (mispedidosBack) {
        mispedidosBack.addEventListener('click', () => {
            closeMisPedidosPopup();
            if (typeof mostrarInicioSistema === 'function') mostrarInicioSistema();
        });
    }

    if (popupMisPedidos) {
        popupMisPedidos.addEventListener('click', (ev) => {
            if (ev.target === popupMisPedidos) closeMisPedidosPopup();
        });
    }

    if (cajaBack) {
        cajaBack.addEventListener('click', () => {
            closeCajaPopup();
            if (typeof mostrarInicioSistema === 'function') mostrarInicioSistema();
        });
    }

    if (popupCaja) {
        popupCaja.addEventListener('click', (ev) => {
            if (ev.target === popupCaja) closeCajaPopup();
        });
    }

    if (calBack) {
        calBack.addEventListener('click', () => {
            closeCalendarioPopup();
            if (typeof mostrarInicioSistema === 'function') mostrarInicioSistema();
        });
    }

    if (popupCalendario) {
        popupCalendario.addEventListener('click', (ev) => {
            if (ev.target === popupCalendario) closeCalendarioPopup();
        });
    }

    if (clientesmodBack) {
        clientesmodBack.addEventListener('click', () => {
            closeClientesModuloPopup();
            if (typeof mostrarInicioSistema === 'function') mostrarInicioSistema();
        });
    }

    if (popupClientesModulo) {
        popupClientesModulo.addEventListener('click', (ev) => {
            if (ev.target === popupClientesModulo) closeClientesModuloPopup();
        });
    }

    if (clientesmodSearch) {
        clientesmodSearch.addEventListener('input', () => {
            renderClientesModulo();
        });
    }

    if (clientesmodAdd) {
        clientesmodAdd.addEventListener('click', () => {
            openClientesFormPopup('add');
        });
    }

    if (clientesmodEdit) {
        clientesmodEdit.addEventListener('click', () => {
            if (!clientesModuloSelectedId) {
                notifyError('Selecciona un cliente para editar.', 'Clientes');
                return;
            }
            const target = clientesModuloData.find((c) => c.id === clientesModuloSelectedId);
            if (!target) {
                notifyError('No se encontró el cliente seleccionado.', 'Clientes');
                return;
            }
            openClientesFormPopup('edit', target);
        });
    }

    if (clientesmodDelete) {
        clientesmodDelete.addEventListener('click', () => {
            if (!clientesModuloSelectedId) {
                notifyError('Selecciona un cliente para eliminar.', 'Clientes');
                return;
            }
            const target = clientesModuloData.find((c) => c.id === clientesModuloSelectedId);
            if (!target) {
                notifyError('No se encontró el cliente seleccionado.', 'Clientes');
                return;
            }
            if (!confirm(`Eliminar cliente "${target.nombre}" (${target.id})?`)) return;
            clientesModuloData = clientesModuloData.filter((c) => c.id !== clientesModuloSelectedId);
            clientesModuloSelectedId = '';
            saveClientesModulo();
            renderClientesModulo();
            notifyInfo('Cliente eliminado correctamente.', 'Clientes');
        });
    }

    if (cliFormCancel) {
        cliFormCancel.addEventListener('click', () => {
            closeClientesFormPopup();
        });
    }

    if (cliFormSave) {
        cliFormSave.addEventListener('click', () => {
            const saved = saveClienteFromForm();
            if (saved && ordenClienteFormMode === 'register-order') {
                aplicarCliente(saved);
                ordenClienteFormMode = '';
            }
        });
    }

    if (popupClientesForm) {
        popupClientesForm.addEventListener('click', (ev) => {
            if (ev.target === popupClientesForm) closeClientesFormPopup();
        });
    }

    if (ordenClienteSelectSearch) {
        ordenClienteSelectSearch.addEventListener('input', () => {
            renderOrdenClienteSelectTable();
        });
    }

    if (ordenClienteSelectCancel) {
        ordenClienteSelectCancel.addEventListener('click', () => {
            closeOrdenClienteSelectPopup();
        });
    }

    if (ordenClienteSelectAccept) {
        ordenClienteSelectAccept.addEventListener('click', () => {
            const row = getClientesOrdenSelectable().find((c) => c.id === ordenClienteSeleccionadoId);
            if (!row) {
                notifyError('Selecciona un cliente válido.', 'Clientes');
                return;
            }
            aplicarCliente({
                id: row.id,
                nombre: row.nombre,
                telefono: row.telefono,
                email: row.correo,
                negocio: row.negocio
            });
            closeOrdenClienteSelectPopup();
        });
    }

    if (ordenClienteSelectPopup) {
        ordenClienteSelectPopup.addEventListener('click', (ev) => {
            if (ev.target === ordenClienteSelectPopup) closeOrdenClienteSelectPopup();
        });
    }

    if (proveedoresBack) {
        proveedoresBack.addEventListener('click', () => {
            closeProveedoresPopup();
            if (typeof mostrarInicioSistema === 'function') mostrarInicioSistema();
        });
    }

    if (popupProveedoresModulo) {
        popupProveedoresModulo.addEventListener('click', (ev) => {
            if (ev.target === popupProveedoresModulo) closeProveedoresPopup();
        });
    }

    if (proveedoresSearch) {
        proveedoresSearch.addEventListener('input', () => {
            renderProveedoresModulo();
        });
    }

    if (proveedoresAdd) {
        proveedoresAdd.addEventListener('click', () => {
            openProveedorFormPopup('add');
        });
    }

    if (proveedoresEdit) {
        proveedoresEdit.addEventListener('click', () => {
            if (!proveedoresSelectedId) {
                notifyError('Selecciona un proveedor para editar.', 'Proveedores');
                return;
            }
            const target = proveedoresData.find((p) => p.id === proveedoresSelectedId);
            if (!target) {
                notifyError('No se encontró el proveedor seleccionado.', 'Proveedores');
                return;
            }
            openProveedorFormPopup('edit', target);
        });
    }

    if (proveedoresDelete) {
        proveedoresDelete.addEventListener('click', () => {
            if (!proveedoresSelectedId) {
                notifyError('Selecciona un proveedor para eliminar.', 'Proveedores');
                return;
            }
            const target = proveedoresData.find((p) => p.id === proveedoresSelectedId);
            if (!target) {
                notifyError('No se encontró el proveedor seleccionado.', 'Proveedores');
                return;
            }
            if (!confirm(`Eliminar proveedor "${target.nombre}" (${target.id})?`)) return;
            proveedoresData = proveedoresData.filter((p) => p.id !== proveedoresSelectedId);
            proveedoresSelectedId = '';
            saveProveedoresModulo();
            renderProveedoresModulo();
            notifyInfo('Proveedor eliminado correctamente.', 'Proveedores');
        });
    }

    if (provFormCancel) {
        provFormCancel.addEventListener('click', () => {
            closeProveedorFormPopup();
        });
    }

    if (provFormSave) {
        provFormSave.addEventListener('click', () => {
            saveProveedorFromForm();
        });
    }

    if (popupProveedorForm) {
        popupProveedorForm.addEventListener('click', (ev) => {
            if (ev.target === popupProveedorForm) closeProveedorFormPopup();
        });
    }

    if (insumosBack) {
        insumosBack.addEventListener('click', () => {
            closeInsumosPopup();
            if (typeof mostrarInicioSistema === 'function') mostrarInicioSistema();
        });
    }

    if (popupInsumosModulo) {
        popupInsumosModulo.addEventListener('click', (ev) => {
            if (ev.target === popupInsumosModulo) closeInsumosPopup();
        });
    }

    if (insumosSearch) {
        insumosSearch.addEventListener('input', () => {
            renderInsumosModulo();
        });
    }

    if (insumosAdd) {
        insumosAdd.addEventListener('click', () => {
            openInsumoFormPopup('add');
        });
    }

    if (insumosEdit) {
        insumosEdit.addEventListener('click', () => {
            if (!insumosSelectedId) {
                notifyError('Selecciona un insumo para editar.', 'Insumos');
                return;
            }
            const target = insumosData.find((i) => i.id === insumosSelectedId);
            if (!target) {
                notifyError('No se encontró el insumo seleccionado.', 'Insumos');
                return;
            }
            openInsumoFormPopup('edit', target);
        });
    }

    if (insumosDelete) {
        insumosDelete.addEventListener('click', () => {
            if (!insumosSelectedId) {
                notifyError('Selecciona un insumo para eliminar.', 'Insumos');
                return;
            }
            const target = insumosData.find((i) => i.id === insumosSelectedId);
            if (!target) {
                notifyError('No se encontró el insumo seleccionado.', 'Insumos');
                return;
            }
            if (!confirm(`Eliminar insumo "${target.nombre}" (${target.id})?`)) return;
            insumosData = insumosData.filter((i) => i.id !== insumosSelectedId);
            insumosSelectedId = '';
            saveInsumosModulo();
            renderInsumosModulo();
            notifyInfo('Insumo eliminado correctamente.', 'Insumos');
        });
    }

    if (insFormCancel) {
        insFormCancel.addEventListener('click', () => {
            closeInsumoFormPopup();
        });
    }

    if (insFormSave) {
        insFormSave.addEventListener('click', () => {
            saveInsumoFromForm();
        });
    }

    if (popupInsumoForm) {
        popupInsumoForm.addEventListener('click', (ev) => {
            if (ev.target === popupInsumoForm) closeInsumoFormPopup();
        });
    }

    if (almacenBack) {
        almacenBack.addEventListener('click', () => {
            closeAlmacenPopup();
            if (typeof mostrarInicioSistema === 'function') mostrarInicioSistema();
        });
    }

    if (popupAlmacenModulo) {
        popupAlmacenModulo.addEventListener('click', (ev) => {
            if (ev.target === popupAlmacenModulo) closeAlmacenPopup();
        });
    }

    if (almacenSearch) {
        almacenSearch.addEventListener('input', () => {
            renderAlmacenModulo();
        });
    }

    if (almacenAdd) {
        almacenAdd.addEventListener('click', () => {
            openAlmacenFormPopup('add');
        });
    }

    if (almacenEdit) {
        almacenEdit.addEventListener('click', () => {
            if (!almacenSelectedId) {
                notifyError('Selecciona un producto para editar.', 'Almacén');
                return;
            }
            const target = almacenData.find((a) => a.id === almacenSelectedId);
            if (!target) {
                notifyError('No se encontró el producto seleccionado.', 'Almacén');
                return;
            }
            openAlmacenFormPopup('edit', target);
        });
    }

    if (almacenDelete) {
        almacenDelete.addEventListener('click', () => {
            if (!almacenSelectedId) {
                notifyError('Selecciona un producto para eliminar.', 'Almacén');
                return;
            }
            const target = almacenData.find((a) => a.id === almacenSelectedId);
            if (!target) {
                notifyError('No se encontró el producto seleccionado.', 'Almacén');
                return;
            }
            if (!confirm(`Eliminar producto "${target.producto}" (${target.id})?`)) return;
            almacenData = almacenData.filter((a) => a.id !== almacenSelectedId);
            almacenSelectedId = '';
            saveAlmacenModulo();
            renderAlmacenModulo();
            notifyInfo('Producto eliminado correctamente.', 'Almacén');
        });
    }

    if (almFormCancel) {
        almFormCancel.addEventListener('click', () => {
            closeAlmacenFormPopup();
        });
    }

    if (almFormSave) {
        almFormSave.addEventListener('click', () => {
            saveAlmacenFromForm();
        });
    }

    if (popupAlmacenForm) {
        popupAlmacenForm.addEventListener('click', (ev) => {
            if (ev.target === popupAlmacenForm) closeAlmacenFormPopup();
        });
    }

    if (reportesmodBack) {
        reportesmodBack.addEventListener('click', () => {
            closeReportesPopup();
            if (typeof mostrarInicioSistema === 'function') mostrarInicioSistema();
        });
    }

    if (popupReportesModulo) {
        popupReportesModulo.addEventListener('click', (ev) => {
            if (ev.target === popupReportesModulo) closeReportesPopup();
        });
    }

    if (reportesRango) {
        reportesRango.addEventListener('change', () => {
            renderReportesModulo();
        });
    }

    if (reportesRefresh) {
        reportesRefresh.addEventListener('click', () => {
            renderReportesModulo();
        });
    }

    if (calPrevMonth) {
        calPrevMonth.addEventListener('click', () => {
            calViewDate = new Date(calViewDate.getFullYear(), calViewDate.getMonth() - 1, 1);
            renderCalendarioUI();
        });
    }

    if (calNextMonth) {
        calNextMonth.addEventListener('click', () => {
            calViewDate = new Date(calViewDate.getFullYear(), calViewDate.getMonth() + 1, 1);
            renderCalendarioUI();
        });
    }

    if (calGridDays) {
        calGridDays.addEventListener('click', (ev) => {
            const btn = ev.target.closest('[data-cal-date]');
            if (!btn) return;
            const date = String(btn.dataset.calDate || '').trim();
            if (!date) return;
            calSelectedDate = date;
            calScopeMode = 'selected';
            if (calScopeSelect) calScopeSelect.value = 'selected';
            renderCalendarioUI();
        });
    }

    if (calClearFilter) {
        calClearFilter.addEventListener('click', () => {
            calScopeMode = 'all';
            if (calScopeSelect) calScopeSelect.value = 'all';
            renderCalendarioUI();
        });
    }

    if (calScopeSelect) {
        calScopeSelect.addEventListener('change', () => {
            const v = String(calScopeSelect.value || 'all');
            calScopeMode = (
                v === 'selected' ||
                v === 'today' ||
                v === 'week' ||
                v === 'next15' ||
                v === 'month' ||
                v === 'overdue' ||
                v === 'all'
            ) ? v : 'all';
            if (calScopeMode === 'selected' && !calSelectedDate) calSelectedDate = todayISO();
            renderCalendarioUI();
        });
    }

    if (calStatusSelect) {
        calStatusSelect.addEventListener('change', () => {
            const v = String(calStatusSelect.value || 'all').toLowerCase();
            calStatusMode = (
                v === 'all' ||
                v === 'pendiente' ||
                v === 'en-produccion' ||
                v === 'pendiente-por-entregar'
            ) ? v : 'all';
            renderCalendarioUI();
        });
    }

    if (calSearchInput) {
        calSearchInput.addEventListener('input', () => {
            calSearchTerm = String(calSearchInput.value || '').trim();
            renderCalendarioUI();
        });
    }

    if (cajaTabCorte) {
        cajaTabCorte.addEventListener('click', () => {
            cajaTabActiva = 'corte';
            renderCajaUI();
        });
    }

    if (cajaTabGasto) {
        cajaTabGasto.addEventListener('click', () => {
            cajaTabActiva = 'gasto';
            renderCajaUI();
        });
    }

    if (cajaGastoFuente) {
        cajaGastoFuente.addEventListener('change', () => {
            renderCajaUI();
        });
    }

    if (cajaBtnRealizarCorte) {
        cajaBtnRealizarCorte.addEventListener('click', () => {
            renderCajaUI();
            printCajaTicket();
        });
    }

    if (cajaBtnIngresarDinero) {
        cajaBtnIngresarDinero.addEventListener('click', () => {
            if (getConfigValue('caja', 'permitirIngresoManual') === false) {
                notifyError('El ingreso manual está desactivado en Configuración de caja.', 'Caja');
                return;
            }
            const fuente = String(cajaGastoFuente?.value || 'EFECTIVO').toUpperCase();
            const raw = prompt(`Cantidad a ingresar en ${fuente}:`, '0');
            if (raw === null) return;
            const monto = Number(raw);
            if (!Number.isFinite(monto) || monto <= 0) {
                notifyError('Cantidad inválida.', 'Caja');
                return;
            }
            cajaMovimientos.unshift({
                id: `CJ-${Date.now().toString(36).toUpperCase()}`,
                fecha: new Date().toISOString(),
                tipo: 'ingreso',
                fuente,
                monto,
                motivo: 'Ingreso manual'
            });
            saveCajaMovimientos();
            renderCajaUI();
            notifyInfo('Dinero ingresado correctamente.', 'Caja');
        });
    }

    if (cajaBtnRealizarGasto) {
        cajaBtnRealizarGasto.addEventListener('click', () => {
            if (getConfigValue('caja', 'permitirGastos') === false) {
                notifyError('Registrar gastos está desactivado en Configuración de caja.', 'Caja');
                return;
            }
            const fuente = String(cajaGastoFuente?.value || 'EFECTIVO').toUpperCase();
            const motivo = String(cajaGastoMotivo?.value || '').trim();
            const monto = Math.max(0, Number(cajaGastoMonto?.value || 0));
            const disponible = getDisponiblePorFuente(fuente);
            if (disponible <= 0) {
                notifyError('No hay dinero disponible en esa fuente hoy.', 'Caja');
                return;
            }
            if (!motivo) {
                notifyError('Escribe el motivo del gasto.', 'Caja');
                return;
            }
            if (!Number.isFinite(monto) || monto <= 0) {
                notifyError('La cantidad a sacar debe ser mayor a cero.', 'Caja');
                return;
            }
            if (monto > disponible) {
                notifyError(`No puedes sacar más de lo disponible (${formatMoney(disponible)}).`, 'Caja');
                return;
            }
            cajaMovimientos.unshift({
                id: `CJ-${Date.now().toString(36).toUpperCase()}`,
                fecha: new Date().toISOString(),
                tipo: 'gasto',
                fuente,
                monto,
                motivo
            });
            saveCajaMovimientos();
            if (cajaGastoMotivo) cajaGastoMotivo.value = '';
            if (cajaGastoMonto) cajaGastoMonto.value = '';
            renderCajaUI();
            notifyInfo('Gasto registrado.', 'Caja');
        });
    }

    if (mpTablaBody) {
        mpTablaBody.addEventListener('click', (ev) => {
            const tr = ev.target.closest('tr[data-mp-id]');
            if (!tr) return;
            const id = tr.dataset.mpId;
            if (!id) return;
            if (mpSelectedIds.has(id)) mpSelectedIds.delete(id);
            else mpSelectedIds.add(id);
            renderMisPedidos();
        });
    }

    if (mispedidosTabVentas) {
        mispedidosTabVentas.addEventListener('click', () => {
            misPedidosTab = 'venta';
            mpSelectedIds = new Set();
            renderMisPedidos();
        });
    }
    if (mispedidosTabCot) {
        mispedidosTabCot.addEventListener('click', () => {
            misPedidosTab = 'cotizacion';
            mpSelectedIds = new Set();
            renderMisPedidos();
        });
    }

    if (mpEditarSeleccion) {
        mpEditarSeleccion.addEventListener('click', () => {
            const rows = getSelectedMisPedidos(getMisPedidosFiltrados());
            editarRegistrosSeleccionados(rows);
        });
    }
    if (mpExportarSeleccion) {
        mpExportarSeleccion.addEventListener('click', () => {
            const rows = getSelectedMisPedidos(getMisPedidosFiltrados());
            exportRowsAsCsv(rows);
        });
    }

    [mpFiltroFolio, mpFiltroNombre, mpFiltroTelefono, mpFiltroDisenador, mpFiltroFechaEmitida, mpFiltroFechaEntrega, mpFiltroEstatus, mpFiltroAdeudo]
        .filter(Boolean)
        .forEach((input) => {
            input.addEventListener('input', renderMisPedidos);
            input.addEventListener('change', renderMisPedidos);
        });

    if (mpLimpiarFiltros) {
        mpLimpiarFiltros.addEventListener('click', () => {
            [mpFiltroFolio, mpFiltroNombre, mpFiltroTelefono, mpFiltroDisenador, mpFiltroFechaEmitida, mpFiltroFechaEntrega, mpFiltroEstatus, mpFiltroAdeudo]
                .filter(Boolean)
                .forEach((input) => {
                    input.value = '';
                });
            mpSelectedIds = new Set();
            renderMisPedidos();
        });
    }

    if (productosBack) {
        productosBack.addEventListener('click', () => {
            closeProductosPopup();
            if (typeof mostrarInicioSistema === 'function') mostrarInicioSistema();
        });
    }

    if (popupProductos) {
        popupProductos.addEventListener('click', (ev) => {
            if (ev.target === popupProductos) closeProductosPopup();
        });
    }

    if (btnAjustesMain) {
        btnAjustesMain.addEventListener('click', () => {
            openConfiguracionesPopup();
        });
    }

    if (productosTabStock) {
        productosTabStock.addEventListener('click', () => {
            productosTab = 'stock';
            productosSelectedIds = new Set();
            productosSelectionAnchorId = '';
            productosCategoriaFilter = '';
            productosLowStockOnly = false;
            renderProductosTabla();
        });
    }

    if (productosTabFormato) {
        productosTabFormato.addEventListener('click', () => {
            productosTab = 'gran-formato';
            productosSelectedIds = new Set();
            productosSelectionAnchorId = '';
            productosCategoriaFilter = '';
            productosLowStockOnly = false;
            renderProductosTabla();
        });
    }

    if (productosTablaBody) {
        productosTablaBody.addEventListener('click', (ev) => {
            const tr = ev.target.closest('tr[data-prod-id]');
            if (!tr) return;
            const id = tr.dataset.prodId || '';
            const rows = getProductosFiltrados();
            const clickedIndex = rows.findIndex((r) => r.id === id);
            const anchorIndex = rows.findIndex((r) => r.id === productosSelectionAnchorId);
            const isShift = !!ev.shiftKey;
            const isMetaToggle = !!(ev.ctrlKey || ev.metaKey);

            if (isShift && anchorIndex >= 0 && clickedIndex >= 0) {
                const start = Math.min(anchorIndex, clickedIndex);
                const end = Math.max(anchorIndex, clickedIndex);
                const rangeIds = rows.slice(start, end + 1).map((r) => r.id);
                productosSelectedIds = new Set(rangeIds);
            } else if (isMetaToggle) {
                if (productosSelectedIds.has(id)) productosSelectedIds.delete(id);
                else productosSelectedIds.add(id);
                productosSelectionAnchorId = id;
            } else {
                productosSelectedIds = new Set([id]);
                productosSelectionAnchorId = id;
            }

            renderProductosTabla();
        });
    }

    if (productosSearchInput) {
        productosSearchInput.addEventListener('input', () => {
            productosSearchTerm = productosSearchInput.value || '';
            renderProductosTabla();
        });
    }

    if (prodActualizar) {
        prodActualizar.addEventListener('click', () => {
            loadProductos();
            renderProductosTabla();
            alert('Inventario actualizado.');
        });
    }

    if (prodLowStock) {
        prodLowStock.addEventListener('click', () => {
            productosLowStockOnly = !productosLowStockOnly;
            renderProductosTabla();
        });
    }

    if (prodExportPdf) {
        prodExportPdf.addEventListener('click', () => {
            alert('Se abrirá el diálogo de impresión para guardar como PDF.');
            window.print();
        });
    }

    if (prodFiltroCategoria) {
        prodFiltroCategoria.addEventListener('click', () => {
            renderCategoriaPopup();
            openProdModal(popupProdCategoria);
        });
    }

    if (prodCategoriaLista) {
        prodCategoriaLista.addEventListener('click', (ev) => {
            const btn = ev.target.closest('button[data-prod-cat]');
            if (!btn) return;
            const cat = String(btn.dataset.prodCat || '').trim();
            productosCategoriaFilter = (cat === 'Todas') ? '' : cat;
            closeProdModal(popupProdCategoria);
            renderProductosTabla();
        });
    }

    if (prodCategoriaCerrar) {
        prodCategoriaCerrar.addEventListener('click', () => closeProdModal(popupProdCategoria));
    }

    if (popupProdCategoria) {
        popupProdCategoria.addEventListener('click', (ev) => {
            if (ev.target === popupProdCategoria) closeProdModal(popupProdCategoria);
        });
    }

    if (prodFiltroCodigo) {
        prodFiltroCodigo.addEventListener('click', () => {
            const actual = productosCodigoFilter || '';
            const code = prompt('Filtrar por código de producto (vacío para limpiar):', actual);
            if (code === null) return;
            productosCodigoFilter = String(code || '').trim();
            renderProductosTabla();
        });
    }

    if (prodEntradaStock) {
        prodEntradaStock.addEventListener('click', () => {
            if (prodEntradaBuscar) prodEntradaBuscar.value = '';
            if (prodEntradaCantidad) prodEntradaCantidad.value = '1';
            renderEntradaSelect();
            openProdModal(popupProdEntrada);
        });
    }

    if (prodEntradaBuscar) {
        prodEntradaBuscar.addEventListener('input', renderEntradaSelect);
    }

    if (prodEntradaGuardar) {
        prodEntradaGuardar.addEventListener('click', () => {
            const id = String(prodEntradaSelect?.value || '').trim();
            const qty = Math.max(0, Number(prodEntradaCantidad?.value || 0));
            if (!id) return alert('Selecciona un producto.');
            if (!Number.isFinite(qty) || qty <= 0) return alert('Cantidad inválida.');
            productosData = productosData.map((p) => p.id === id ? { ...p, existencias: Number(p.existencias || 0) + qty } : p);
            saveProductos();
            renderProductosTabla();
            closeProdModal(popupProdEntrada);
            alert('Entrada registrada.');
        });
    }

    if (prodEntradaCerrar) {
        prodEntradaCerrar.addEventListener('click', () => closeProdModal(popupProdEntrada));
    }

    if (popupProdEntrada) {
        popupProdEntrada.addEventListener('click', (ev) => {
            if (ev.target === popupProdEntrada) closeProdModal(popupProdEntrada);
        });
    }

    if (prodImprimir) {
        prodImprimir.addEventListener('click', () => window.print());
    }

    if (prodExcel) {
        prodExcel.addEventListener('click', () => exportProductosCsv(`inventario_${todayISO()}.csv`));
    }

    if (prodAbrirPlantilla) {
        prodAbrirPlantilla.addEventListener('click', () => {
            const header = productosTab === 'gran-formato'
                ? 'ID,PRODUCTO,MATERIAL,PRECIO_GENERAL_M2,PRECIO_M2_REVENDEDOR,PRECIO_M_LINEAL_GENERAL,PRECIO_M_LINEAL_REVENDEDOR'
                : 'CODIGO,PRODUCTO,MEDIDA,MATERIAL,CANT_MINIMA,EXISTENCIAS,PRECIO_REVENDEDOR,PRECIO_VENTA,CATEGORIA,TIPO';
            const sample = productosTab === 'gran-formato'
                ? 'GF-0001,Lona Front,Lona Front 13 oz,165.00,120.00,140.00,100.00'
                : 'COD-0001,Producto ejemplo,50x70 cm,Material ejemplo,10,25,120.00,165.00,Categoria,stock';
            const blob = new Blob([`${header}\n${sample}\n`], { type: 'text/csv;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = productosTab === 'gran-formato' ? 'plantilla_gran_formato.csv' : 'plantilla_productos.csv';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        });
    }

    if (prodImportarDesde && prodImportFile) {
        prodImportarDesde.addEventListener('click', () => prodImportFile.click());
        prodImportFile.addEventListener('change', async () => {
            const file = prodImportFile.files?.[0];
            try {
                await applyCsvImportProductos(file);
            } catch (err) {
                alert(`No se pudo importar: ${err?.message || 'Error desconocido'}`);
            } finally {
                prodImportFile.value = '';
            }
        });
    }

    if (prodGfAbrirPlantilla) {
        prodGfAbrirPlantilla.addEventListener('click', () => {
            prodAbrirPlantilla?.click();
        });
    }

    if (prodGfImportarDesde && prodImportFile) {
        prodGfImportarDesde.addEventListener('click', () => {
            prodImportFile.click();
        });
    }

    if (prodGfExportarDesde) {
        prodGfExportarDesde.addEventListener('click', () => {
            exportProductosCsv(`gran_formato_${todayISO()}.csv`);
        });
    }

    if (prodFormGenerarCodigo) {
        prodFormGenerarCodigo.addEventListener('click', () => {
            if (prodFormCodigo) prodFormCodigo.value = generarCodigoProducto();
        });
    }

    if (prodFormTipo) {
        prodFormTipo.addEventListener('change', () => {
            if (!prodFormCodigo?.value?.trim()) {
                prodFormCodigo.value = generarCodigoProducto();
            }
            syncProdFormModeByTipo();
        });
    }

    if (prodGfCobroTipo) {
        prodGfCobroTipo.addEventListener('change', () => {
            syncProdFormModeByTipo();
        });
    }

    if (prodFormFotoPrincipal) {
        prodFormFotoPrincipal.addEventListener('change', async () => {
            const file = prodFormFotoPrincipal.files?.[0];
            try {
                prodMainPhotoData = await readFileAsDataUrlLocal(file);
                renderProdMainPhotoPreview();
            } catch (_) {
                alert('No se pudo leer la foto principal.');
            }
        });
    }

    if (prodColorAgregar) {
        prodColorAgregar.addEventListener('click', async () => {
            const color = String(prodColorNombre?.value || '').trim();
            const existencias = Math.max(0, Number(prodColorExistencias?.value || 0));
            if (!color) {
                alert('Escribe el color del subproducto.');
                return;
            }
            try {
                const foto = await readFileAsDataUrlLocal(prodColorFoto?.files?.[0]);
                prodColorDraftList.push({ color, existencias, foto });
                if (prodColorNombre) prodColorNombre.value = '';
                if (prodColorExistencias) prodColorExistencias.value = '0';
                if (prodColorFoto) prodColorFoto.value = '';
                renderProdColorDraftList();
            } catch (_) {
                alert('No se pudo leer la foto del color.');
            }
        });
    }

    if (prodColorLista) {
        prodColorLista.addEventListener('click', (ev) => {
            const btn = ev.target.closest('button[data-prod-color-del]');
            if (!btn) return;
            const idx = Number(btn.dataset.prodColorDel);
            if (!Number.isFinite(idx)) return;
            prodColorDraftList.splice(idx, 1);
            renderProdColorDraftList();
        });
    }

    if (prodAgregar) {
        prodAgregar.addEventListener('click', () => {
            resetProdForm();
            if (prodFormCodigo) prodFormCodigo.value = generarCodigoProducto();
            syncProdFormModeByTipo();
            openProdModal(popupProdForm);
        });
    }

    if (prodEditar) {
        prodEditar.addEventListener('click', () => {
            const selected = getProductosSeleccionados();
            if (!selected.length) {
                alert('Selecciona un producto para editar.');
                return;
            }

            if (selected.length === 1) {
                openProdFormForEdit(selected[0]);
                syncProdFormModeByTipo();
                openProdModal(popupProdForm);
                return;
            }

            const categoria = prompt('Categoría para los seleccionados (vacío = no cambiar):', '');
            if (categoria === null) return;
            const material = prompt('Material para los seleccionados (vacío = no cambiar):', '');
            if (material === null) return;
            const minimaTxt = prompt('Cant. minima para los seleccionados (vacío = no cambiar):', '');
            if (minimaTxt === null) return;
            const revTxt = prompt('Precio revendedor para los seleccionados (vacío = no cambiar):', '');
            if (revTxt === null) return;
            const ventaTxt = prompt('Precio venta para los seleccionados (vacío = no cambiar):', '');
            if (ventaTxt === null) return;

            const patch = {};
            if (String(categoria).trim()) patch.categoria = String(categoria).trim();
            if (String(material).trim()) patch.material = String(material).trim();
            if (String(minimaTxt).trim()) {
                const n = Number(minimaTxt);
                if (!Number.isFinite(n) || n < 0) return alert('Cant. minima inválida.');
                patch.minima = n;
            }
            if (String(revTxt).trim()) {
                const n = Number(revTxt);
                if (!Number.isFinite(n) || n < 0) return alert('Precio revendedor inválido.');
                patch.precioRevendedor = n;
            }
            if (String(ventaTxt).trim()) {
                const n = Number(ventaTxt);
                if (!Number.isFinite(n) || n < 0) return alert('Precio venta inválido.');
                patch.precioVenta = n;
            }

            if (!Object.keys(patch).length) return;
            const ids = new Set(selected.map((r) => r.id));
            productosData = productosData.map((p) => ids.has(p.id) ? { ...p, ...patch } : p);
            saveProductos();
            renderProductosTabla();
            alert(`Se actualizaron ${ids.size} productos.`);
        });
    }

    if (prodEliminar) {
        prodEliminar.addEventListener('click', () => {
            const selected = getProductosSeleccionados();
            if (!selected.length) {
                alert('Selecciona un producto para eliminar.');
                return;
            }
            const ask = selected.length === 1
                ? `¿Eliminar ${selected[0].producto}?`
                : `¿Eliminar ${selected.length} productos seleccionados?`;
            if (!confirm(ask)) return;
            const ids = new Set(selected.map((r) => r.id));
            productosData = productosData.filter((p) => !ids.has(p.id));
            productosSelectedIds = new Set();
            productosSelectionAnchorId = '';
            saveProductos();
            renderProductosTabla();
        });
    }

    if (prodFormSiguiente) {
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
    }

    if (prodFormCerrar) {
        prodFormCerrar.addEventListener('click', () => closeProdModal(popupProdForm));
    }

    if (popupProdForm) {
        popupProdForm.addEventListener('click', (ev) => {
            if (ev.target === popupProdForm) closeProdModal(popupProdForm);
        });
    }

    if (prodTabuladorSelect) {
        prodTabuladorSelect.addEventListener('change', () => {
            syncProdTabPreciosFromUI();
            prodPendingTabuladorId = prodTabuladorSelect.value || '';
            if (prodPendingPayload) prodPendingPayload.tabuladorId = prodPendingTabuladorId;
            prodPendingTabuladorPrecios = [];
            renderProdTabuladorPreview();
        });
    }

    if (prodTabGuardarProducto) {
        prodTabGuardarProducto.addEventListener('click', () => {
            if (!prodPendingTabuladorId) {
                alert('Selecciona un tabulador.');
                return;
            }
            commitPendingProduct();
        });
    }

    if (prodTabVolver) {
        prodTabVolver.addEventListener('click', () => {
            closeProdTabuladorPopup();
            openProdModal(popupProdForm);
        });
    }

    if (prodTabCerrar) {
        prodTabCerrar.addEventListener('click', () => closeProdTabuladorPopup());
    }

    if (popupProdTabulador) {
        popupProdTabulador.addEventListener('click', (ev) => {
            if (ev.target === popupProdTabulador) closeProdTabuladorPopup();
        });
    }

    if (ajustesTabSelect) {
        ajustesTabSelect.addEventListener('change', () => {
            syncAjustesRowsFromUI();
            ajustesTabuladorId = ajustesTabSelect.value || '';
            renderAjustesTabuladorSelect();
            renderAjustesTabuladorTables();
        });
    }

    if (ajustesTabNuevo) {
        ajustesTabNuevo.addEventListener('click', () => {
            syncAjustesRowsFromUI();
            const nuevo = buildTabulador(`Tabulador ${tabuladoresData.length + 1}`);
            tabuladoresData.push(nuevo);
            ajustesTabuladorId = nuevo.id;
            renderAjustesTabuladorSelect();
            renderAjustesTabuladorTables();
        });
    }

    if (ajustesTabEliminar) {
        ajustesTabEliminar.addEventListener('click', () => {
            if (tabuladoresData.length <= 1) {
                alert('Debe existir al menos un tabulador.');
                return;
            }
            const active = getTabuladorById(ajustesTabuladorId);
            if (!active) return;
            if (!confirm(`¿Eliminar tabulador ${active.nombre}?`)) return;
            tabuladoresData = tabuladoresData.filter((t) => t.id !== active.id);
            ajustesTabuladorId = tabuladoresData[0]?.id || '';
            renderAjustesTabuladorSelect();
            renderAjustesTabuladorTables();
        });
    }

    if (ajustesTabGuardar) {
        ajustesTabGuardar.addEventListener('click', () => {
            syncAjustesRowsFromUI();
            cajaSettings.nombre = String(ajustesCajaNombre?.value || 'Caja principal').trim() || 'Caja principal';
            cajaSettings.id = String(ajustesCajaId?.value || 'CAJA-01').trim() || 'CAJA-01';
            saveCajaSettings();
            saveTabuladores();
            renderCajaUI();
            notifyInfo('Tabuladores y ajustes de caja guardados.', 'Ajustes');
        });
    }

    if (ajustesTabCerrar) {
        ajustesTabCerrar.addEventListener('click', () => closeAjustesTabuladoresPopup());
    }

    if (popupAjustesTabuladores) {
        popupAjustesTabuladores.addEventListener('click', (ev) => {
            if (ev.target === popupAjustesTabuladores) closeAjustesTabuladoresPopup();
        });
    }

    const setAccessStatus = (msg, isError = false) => {
        if (!accessStatus) return;
        accessStatus.textContent = msg;
        accessStatus.style.color = isError ? '#ff8e8e' : '#d6e7ff';
    };

    const openAccessPopup = () => {
        if (!popupAccess) return;
        popupAccess.style.display = 'flex';
        popupAccess.setAttribute('aria-hidden', 'false');
        document.body.classList.add('popup-open');
        document.documentElement.classList.add('popup-open');
    };

    const closeAccessPopup = () => {
        if (!popupAccess) return;
        popupAccess.style.display = 'none';
        popupAccess.setAttribute('aria-hidden', 'true');
        if (popupListado?.style.display !== 'flex' && popupDesignTracking?.style.display !== 'flex' && popupMisPedidos?.style.display !== 'flex' && popupProductos?.style.display !== 'flex' && popupCaja?.style.display !== 'flex' && popupCalendario?.style.display !== 'flex' && popupClientesModulo?.style.display !== 'flex') {
            document.body.classList.remove('popup-open');
            document.documentElement.classList.remove('popup-open');
        }
    };

    const setDesignStatus = (msg, isError = false, showPopup = false) => {
        if (!designStatus) return;
        designStatus.textContent = msg;
        designStatus.style.color = isError ? '#ff8e8e' : '#d6e7ff';
        if (showPopup) {
            if (isError) notifyError(msg, 'Diseños');
            else notifyInfo(msg, 'Diseños');
        }
    };

    const updateDesignEditableState = () => {
        const locked = !selectedDesignOrder;
        [designFileFront, designFileBack, btnDesignUpload].forEach((elx) => {
            if (!elx) return;
            elx.disabled = locked;
            elx.style.opacity = locked ? '0.55' : '1';
        });
        if (btnDesignUpload) {
            btnDesignUpload.textContent = locked ? 'Selecciona pedido' : 'Subir diseño';
        }
    };

    const openDesignPopup = () => {
        if (!popupDesignTracking) return;
        popupDesignTracking.style.display = 'flex';
        popupDesignTracking.setAttribute('aria-hidden', 'false');
        document.body.classList.add('popup-open');
        document.documentElement.classList.add('popup-open');
        updateDesignEditableState();
    };

    const closeDesignPopup = () => {
        if (!popupDesignTracking) return;
        popupDesignTracking.style.display = 'none';
        popupDesignTracking.setAttribute('aria-hidden', 'true');
        if (popupListado?.style.display !== 'flex' && popupAccess?.style.display !== 'flex' && popupMisPedidos?.style.display !== 'flex' && popupProductos?.style.display !== 'flex' && popupCaja?.style.display !== 'flex' && popupCalendario?.style.display !== 'flex' && popupClientesModulo?.style.display !== 'flex') {
            document.body.classList.remove('popup-open');
            document.documentElement.classList.remove('popup-open');
        }
    };

    const getOrderIdCandidate = (row = {}) => {
        const keys = Object.keys(row || {});
        if (!keys.length) return '';
        const idKey = keys.find((k) => /^(id|idpedido|pedidoid)$/i.test(k))
            || keys.find((k) => /(pedido|folio|orden|ot)/i.test(k))
            || keys[0];
        return `${row[idKey] ?? ''}`.trim();
    };

    const getClientCandidate = (row = {}) => {
        const keys = Object.keys(row || {});
        const key = keys.find((k) => /(cliente|nombre|razonsocial)/i.test(k));
        return key ? `${row[key] ?? ''}`.trim() : '';
    };

    const rowSummary = (row = {}) => {
        const orderId = getOrderIdCandidate(row) || 'Sin ID';
        const cliente = getClientCandidate(row);
        return cliente ? `${orderId} · ${cliente}` : orderId;
    };

    const renderDesignOrders = (rows = []) => {
        if (!designTableWrap) return;
        if (!rows.length) {
            designTableWrap.innerHTML = '<div style="padding:12px; color:#b8c8db; font-size:0.86rem;">No hay pedidos pendientes de diseño.</div>';
            return;
        }

        const cols = Object.keys(rows[0]);
        const head = '<th style="position:sticky;top:0;background:#0f1827;color:#d9ebff;border-bottom:1px solid rgba(255,255,255,0.12);padding:8px;text-align:left;font-size:0.78rem;">Acción</th>'
            + cols.map(c => `<th style="position:sticky;top:0;background:#0f1827;color:#d9ebff;border-bottom:1px solid rgba(255,255,255,0.12);padding:8px;text-align:left;font-size:0.78rem;">${escapeHtml(c)}</th>`).join('');
        const body = rows.map((r, idx) => `<tr>
            <td style="padding:7px 8px;border-bottom:1px solid rgba(255,255,255,0.08);font-size:0.76rem;white-space:nowrap;">
                <button type="button" data-design-idx="${idx}" style="background:linear-gradient(135deg,#1d4ed8 0%,#2563eb 100%);color:#fff;border:none;border-radius:7px;padding:5px 8px;cursor:pointer;font-size:0.72rem;font-weight:700;">Seleccionar</button>
            </td>
            ${cols.map(c => `<td style="padding:7px 8px;border-bottom:1px solid rgba(255,255,255,0.08);font-size:0.76rem;color:#e8f0ff;white-space:nowrap;">${escapeHtml(r[c])}</td>`).join('')}
        </tr>`).join('');
        designTableWrap.innerHTML = `<table style="width:100%;border-collapse:collapse;min-width:760px;"><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table>`;
    };

    const loadDesignPending = async () => {
        try {
            if (!window.AccessAPI) throw new Error('No se encontró AccessAPI. Verifica access-api-client.js');
            const limit = Math.max(1, Math.min(500, Number(designLimitInput?.value || 150)));
            setDesignStatus('Consultando pedidos pendientes de diseño...');
            const res = await window.AccessAPI.getDesignPendingOrders(limit);
            designPendingRows = res.rows || [];
            renderDesignOrders(designPendingRows);
            selectedDesignOrder = null;
            if (designSelectedOrder) designSelectedOrder.textContent = 'Ninguno';
            updateDesignEditableState();
            setDesignStatus(`Pendientes cargados: ${designPendingRows.length}`, false, true);
        } catch (err) {
            designPendingRows = [];
            renderDesignOrders([]);
            selectedDesignOrder = null;
            if (designSelectedOrder) designSelectedOrder.textContent = 'Ninguno';
            updateDesignEditableState();
            setDesignStatus(`Error al consultar pendientes: ${err.message}`, true, true);
        }
    };

    const readFileAsBase64 = (file) => new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
            const result = String(reader.result || '');
            const splitIndex = result.indexOf(',');
            resolve(splitIndex >= 0 ? result.slice(splitIndex + 1) : result);
        };
        reader.onerror = () => reject(new Error(`No se pudo leer ${file?.name || 'archivo'}`));
        reader.readAsDataURL(file);
    });

    const sanitizePathPart = (value = '') => String(value || '')
        .trim()
        .replace(/[^A-Za-z0-9._-]/g, '_')
        .slice(0, 180) || 'archivo';

    const getFirebaseWebApp = () => {
        if (!window.firebase) {
            throw new Error('Firebase SDK no está cargado en el frontend.');
        }
        if (!window.firebase.apps || !window.firebase.apps.length) {
            window.firebase.initializeApp(FIREBASE_WEB_CONFIG);
        }
        return window.firebase.app();
    };

    const uploadToFirebaseDirect = async (order, frontFile, backFile) => {
        getFirebaseWebApp();
        const storage = window.firebase.storage();
        const firestore = window.firebase.firestore();

        const orderRefRaw = getOrderIdCandidate(order) || getClientCandidate(order) || 'pedido';
        const orderRef = sanitizePathPart(orderRefRaw);
        const ts = new Date().toISOString().replace(/[-:.]/g, '').replace('T', '_').replace('Z', 'Z');

        const mkPath = (side, filename) => `designs/${orderRef}/${ts}_${side}_${sanitizePathPart(filename)}`;
        const frontPath = mkPath('frente', frontFile.name);
        const backPath = mkPath('reverso', backFile.name);

        const [frontSnap, backSnap] = await Promise.all([
            storage.ref(frontPath).put(frontFile, { contentType: frontFile.type || 'application/octet-stream' }),
            storage.ref(backPath).put(backFile, { contentType: backFile.type || 'application/octet-stream' })
        ]);

        const [frontUrl, backUrl] = await Promise.all([
            frontSnap.ref.getDownloadURL(),
            backSnap.ref.getDownloadURL()
        ]);

        await firestore.collection(FIREBASE_UPLOAD_COLLECTION).add({
            order,
            orderRef,
            uploadedAt: new Date().toISOString(),
            source: 'boutique-web-direct',
            files: [
                {
                    side: 'frente',
                    filename: frontFile.name,
                    contentType: frontFile.type || 'application/octet-stream',
                    sizeBytes: frontFile.size || 0,
                    storagePath: frontPath,
                    storageUrl: frontUrl,
                },
                {
                    side: 'reverso',
                    filename: backFile.name,
                    contentType: backFile.type || 'application/octet-stream',
                    sizeBytes: backFile.size || 0,
                    storagePath: backPath,
                    storageUrl: backUrl,
                }
            ]
        });
    };

    const uploadDesignFiles = async () => {
        try {
            if (!selectedDesignOrder) {
                setDesignStatus('Primero selecciona un pedido pendiente.', true, true);
                return;
            }
            const front = designFileFront?.files?.[0];
            const back = designFileBack?.files?.[0];
            if (!front || !back) {
                setDesignStatus('Debes cargar los dos archivos (frente y reverso).', true, true);
                return;
            }
            setDesignStatus('Subiendo archivos en calidad original...');

            const sendByBackend = async () => {
                const [frontBase64, backBase64] = await Promise.all([
                    readFileAsBase64(front),
                    readFileAsBase64(back)
                ]);

                await window.AccessAPI.uploadDesignFiles({
                    order: selectedDesignOrder,
                    files: [
                        {
                            side: 'frente',
                            filename: front.name,
                            contentType: front.type || 'application/octet-stream',
                            dataBase64: frontBase64
                        },
                        {
                            side: 'reverso',
                            filename: back.name,
                            contentType: back.type || 'application/octet-stream',
                            dataBase64: backBase64
                        }
                    ]
                });
            };

            let uploadedVia = 'backend';
            if (ENABLE_FIREBASE_DIRECT_UPLOAD && CAN_USE_FIREBASE_DIRECT_UPLOAD) {
                try {
                    await uploadToFirebaseDirect(selectedDesignOrder, front, back);
                    uploadedVia = 'firebase';
                } catch (_) {
                    await sendByBackend();
                }
            } else {
                await sendByBackend();
            }

            setDesignStatus(uploadedVia === 'firebase'
                ? 'Diseño enviado correctamente a Firebase.'
                : 'Diseño enviado correctamente (vía backend).', false, true);
            if (designFileFront) designFileFront.value = '';
            if (designFileBack) designFileBack.value = '';
        } catch (err) {
            setDesignStatus(`Error al subir diseño: ${err.message}`, true, true);
        }
    };

    const escapeHtml = (value) => String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');

    const renderAccessRows = (rows = []) => {
        if (!accessTableWrap) return;
        if (!rows.length) {
            accessTableWrap.innerHTML = '<div style="padding:12px; color:#b8c8db; font-size:0.86rem;">La tabla no tiene registros para mostrar.</div>';
            return;
        }

        const cols = Object.keys(rows[0]);
        const head = cols.map(c => `<th style="position:sticky;top:0;background:#0f1827;color:#d9ebff;border-bottom:1px solid rgba(255,255,255,0.12);padding:8px;text-align:left;font-size:0.78rem;">${escapeHtml(c)}</th>`).join('');
        const body = rows.map(r => `<tr>${cols.map(c => `<td style="padding:7px 8px;border-bottom:1px solid rgba(255,255,255,0.08);font-size:0.76rem;color:#e8f0ff;white-space:nowrap;">${escapeHtml(r[c])}</td>`).join('')}</tr>`).join('');
        accessTableWrap.innerHTML = `<table style="width:100%;border-collapse:collapse;min-width:640px;"><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table>`;
    };

    const loadAccessTables = async () => {
        try {
            if (!window.AccessAPI) throw new Error('No se encontró AccessAPI. Verifica access-api-client.js');
            setAccessStatus('Consultando tablas de Access...');
            const res = await window.AccessAPI.getAccessTables();
            accessTableSelect.innerHTML = '';
            (res.tables || []).forEach((t) => {
                const op = document.createElement('option');
                op.value = t;
                op.textContent = t;
                accessTableSelect.appendChild(op);
            });
            if (!res.tables?.length) {
                setAccessStatus('No se encontraron tablas en la base.', true);
                renderAccessRows([]);
                return;
            }
            setAccessStatus(`Tablas cargadas: ${res.tables.length}`);
        } catch (err) {
            setAccessStatus(`Error al consultar tablas: ${err.message}`, true);
            renderAccessRows([]);
        }
    };

    const loadAccessRows = async () => {
        try {
            if (!window.AccessAPI) throw new Error('No se encontró AccessAPI. Verifica access-api-client.js');
            const table = accessTableSelect?.value;
            if (!table) {
                setAccessStatus('Selecciona una tabla primero.', true);
                return;
            }
            const limit = Math.max(1, Math.min(2000, Number(accessLimitInput?.value || 100)));
            setAccessStatus(`Cargando ${limit} filas de ${table}...`);
            const res = await window.AccessAPI.getAccessTableRows(table, limit);
            renderAccessRows(res.rows || []);
            setAccessStatus(`Tabla ${table}: ${res.count || 0} filas mostradas.`);
        } catch (err) {
            setAccessStatus(`Error al cargar filas: ${err.message}`, true);
            renderAccessRows([]);
        }
    };

    const validateAccessPassword = () => {
        const expected = String(ACCESS_PANEL_PASSWORD || '').trim();
        if (!expected) return true;
        const typed = prompt('Ingresa la contraseña para abrir Access:');
        if (typed === null) return false;
        if (typed.trim() !== expected) {
            alert('Contraseña incorrecta.');
            return false;
        }
        return true;
    };

    if (btnAccessData) {
        btnAccessData.onclick = async () => {
            if (!validateAccessPassword()) return;
            openAccessPopup();
            await loadAccessTables();
            await loadAccessRows();
        };
    }
    if (btnAccessClose) btnAccessClose.onclick = closeAccessPopup;
    if (btnAccessRefresh) btnAccessRefresh.onclick = async () => { await loadAccessTables(); };
    if (btnAccessLoad) btnAccessLoad.onclick = async () => { await loadAccessRows(); };
    if (popupAccess) {
        popupAccess.addEventListener('click', (ev) => {
            if (ev.target === popupAccess) closeAccessPopup();
        });
    }

    if (designTableWrap) {
        designTableWrap.addEventListener('click', (ev) => {
            const btn = ev.target.closest('button[data-design-idx]');
            if (!btn) return;
            const idx = Number(btn.dataset.designIdx);
            if (!Number.isFinite(idx) || idx < 0 || idx >= designPendingRows.length) return;
            selectedDesignOrder = designPendingRows[idx];
            if (designSelectedOrder) designSelectedOrder.textContent = rowSummary(selectedDesignOrder);
            updateDesignEditableState();
            setDesignStatus(`Pedido seleccionado: ${rowSummary(selectedDesignOrder)}`);
        });
    }

    if (btnSeguimientoDiseno) {
        btnSeguimientoDiseno.onclick = async () => {
            openDesignPopup();
            await loadDesignPending();
        };
    }
    if (btnDesignRefresh) btnDesignRefresh.onclick = async () => { await loadDesignPending(); };
    if (btnDesignUpload) {
        btnDesignUpload.onclick = async () => {
            // Si estamos en modo "enviar al cliente", maneja diferente
            if (window.enviarDisenoAlCliente) {
                await enviarDisenoAlChatCliente();
            } else {
                await uploadDesignFiles();
            }
        };
    }
    if (btnDesignClose) btnDesignClose.onclick = closeDesignPopup;
    if (popupDesignTracking) {
        popupDesignTracking.addEventListener('click', (ev) => {
            if (ev.target === popupDesignTracking) closeDesignPopup();
        });
    }

    if (notifyOk) {
        notifyOk.addEventListener('click', closeNotifyPopup);
    }

    if (popupNotify) {
        popupNotify.addEventListener('click', (ev) => {
            if (ev.target === popupNotify) closeNotifyPopup();
        });
    }

    // EVENT LISTENERS: FONDO DE CAJA
    if (fondoCajaAceptar) {
        fondoCajaAceptar.addEventListener('click', () => {
            const montoStr = (fondoCajaInputMonto?.value || '1').trim();
            const monto = Number(montoStr);
            if (!Number.isFinite(monto) || monto < 1) {
                notifyError('El fondo inicial debe ser un número mayor o igual a 1.', 'Caja');
                fondoCajaInputMonto.focus();
                return;
            }
            const day = todayISO();
            cajaAperturas[day] = monto;
            saveCajaAperturas();
            closeFondoCajaPopup();
            renderCajaUI();
        });
    }

    if (fondoCajaCancelar) {
        fondoCajaCancelar.addEventListener('click', () => {
            closeFondoCajaPopup();
        });
    }

    if (popupFondoCaja) {
        popupFondoCaja.addEventListener('click', (ev) => {
            if (ev.target === popupFondoCaja) {
                closeFondoCajaPopup();
            }
        });
    }

    // EVENT LISTENERS: CONFIGURACIONES
    if (configBack) {
        configBack.addEventListener('click', () => {
            closeConfiguracionesPopup();
        });
    }

    if (configCerrar) {
        configCerrar.addEventListener('click', () => {
            closeConfiguracionesPopup();
        });
    }

    if (configGuardar) {
        configGuardar.addEventListener('click', () => {
            saveConfiguracionesFromPopup();
        });
    }

    // Tab switching
    document.querySelectorAll('.config-tab').forEach((tab) => {
        tab.addEventListener('click', () => {
            const tabName = tab.getAttribute('data-tab');
            if (tabName) {
                switchConfigTab(tabName);
            }
        });
    });

    if (popupConfiguraciones) {
        popupConfiguraciones.addEventListener('click', (ev) => {
            if (ev.target === popupConfiguraciones) {
                closeConfiguracionesPopup();
            }
        });
    }

    // NUEVO: Abrir configuraciones desde botón (si existe)
    window.openConfiguracionesPopupGlobal = openConfiguracionesPopup;

    loadCajaSettings();
    loadCajaMovimientos();
    loadCajaAperturas();
    loadSystemConfig();
    
    const day = todayISO();
    const current = Number(cajaAperturas[day]);
    if (!Number.isFinite(current) || current < 1) {
        openFondoCajaPopup();
    } else {
        renderCajaUI();
    }

});
