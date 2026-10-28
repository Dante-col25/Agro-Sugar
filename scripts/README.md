# Scripts auxiliares

- `check-container-namespaces.sh CONTAINER`: compara namespaces PID, NET y MNT del contenedor con los del host e imprime límites Docker. Ejecutar desde el host Linux donde corre Docker; guardar la salida como evidencia solo después de una ejecución real.
- `burst.sh`: prepara o elimina el Job de demostración en el contexto Kubernetes de nube indicado. Requiere `CLOUD_CONTEXT`, `NDVI_WORKER_IMAGE`, `kubectl` y `envsubst`.

El bursting todavía no fue ejecutado en el laboratorio. El script no aprovisiona infraestructura ni mueve imágenes reales. Revisar `k8s-nube/README.md` antes de usarlo.
