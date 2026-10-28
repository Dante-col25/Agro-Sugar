# Worker de ejemplo para lotes NDVI

Lee un arreglo JSON de valores NDVI y escribe cantidad y promedio. No lee ni procesa rásteres de drones o satélite. Se incluye como demostración del ciclo Job/CronJob; reemplazar por el worker real antes de presentar procesamiento geoespacial.

La entrada del CronJob local se proporciona en `k8s/ndvi-batch.yaml` mediante un ConfigMap de valores ficticios. Para datos reales, usar almacenamiento de objetos o un volumen compartido y añadir transferencia/retención verificable.
