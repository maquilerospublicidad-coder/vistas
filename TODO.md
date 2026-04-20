# TODO: Implementar Módulo Repartidores + App Móvil

Estado: ✅ Plan aprobado. Progreso: 0/11 pasos completados.

## Pasos del Plan (secuencial, tool por tool):

1. **[PENDIENTE]** Editar `config.js`: Agregar `configZonas: ['Centro', 'Norte', 'Sur', 'Este', 'Oeste']`.
2. **[PENDIENTE]** Editar `mockup.html`: Configuraciones - nueva sección "Zonas" (textarea → array).
3. **[PENDIENTE]** Editar `_tmp_main_script.js`: `load/saveZonasConfig()`, `renderConfigZonas()`.
4. **[PENDIENTE]** Editar `mockup.html`: Clientes form (`cliFormZona` select de zonas).
5. **[PENDIENTE]** Editar `mockup.html`: Clientes table/col/search + zona.
6. **[PENDIENTE]** Editar `_tmp_main_script.js`: `upsertClienteEnStores()` + zona, `renderClientesModulo()` update.
7. **[PENDIENTE]** Editar `mockup.html`: Nueva landing card "Control Repartidores" → popup.
8. **[PENDIENTE]** Editar `mockup.html`: CSS/UI full para popup (left: repartidores table/form, right: pedidos list+assign).
9. **[PENDIENTE]** Editar `_tmp_main_script.js`: `load/saveRepartidores()`, CRUD, assign pedido→repartidor.
10. **[PENDIENTE]** Editar `mockup.html`: Nueva card/tab "Reparto App Móvil" → popup (loads por repartidor, scanner sim).
11. **[PENDIENTE]** Editar `_tmp_main_script.js`: `load/savePendingLoads()`, scan logic, sync status main↔movil.

**Siguiente**: Paso 1 (config.js). Confirmar cada paso antes next.

**Notas**: Test incremental. localStorage: `ZONAS_KEY`, `REPARTIDORES_MODULO_KEY`, `PENDING_LOADS_KEY`.

