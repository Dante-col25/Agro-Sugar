# Virtualización

`diagnostico.sh` reúne inspecciones de libvirt/qcow2 y consulta EPT solo si el módulo Intel KVM está disponible. Ejecutar desde el host Linux de laboratorio y conservar la salida original.

Las capturas adjuntas muestran `domain type='qemu'`: VM emuladas, no aceleración KVM. Por eso no demuestran EPT ni el rendimiento esperado de KVM. El informe registra que EPT y la captura de diagnóstico del host quedaron pendientes; estas limitaciones no se reemplazan con configuración de referencia.
