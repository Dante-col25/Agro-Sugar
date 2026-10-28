# Cloud bursting de demostración

`ndvi-cloudburst-job.yaml` define un ConfigMap de muestra y un Job de Kubernetes. `scripts/burst.sh` lo aplica en un contexto de nube ya configurado cuando se cumple la regla documentada en el informe (más de 3 Pods pendientes durante al menos 10 minutos, o cola con más de 30 minutos). Si la cola lleva 30 minutos vacía, elimina el Job gestionado y el ConfigMap.

## Requisitos antes de ejecutar

- Un contexto Kubernetes de nube existente en `kubectl config`; este ejemplo no crea la cuenta, red ni nodos cloud.
- `kubectl`, `envsubst` (paquete `gettext-base`), `python3` y una imagen worker publicada en un registry accesible por el clúster.
- El comando recibe métricas ya medidas mediante variables de entorno; no consulta por sí solo una cola.

Ejemplo con datos ficticios:

```bash
export CLOUD_CONTEXT=mi-cluster-cloud
export NDVI_WORKER_IMAGE=registry.example/agrosugar/ndvi-worker:1.0.0
export PENDING_NDVI_PODS=4 PENDING_DURATION_MINUTES=12 QUEUE_AGE_MINUTES=0
./scripts/burst.sh
```

Este ejemplo solo demuestra el envío de un Job con una lista JSON pequeña. No transfiere imágenes NDVI, no guarda resultados en almacenamiento de objetos y no aprovisiona ni apaga nodos. Para cumplir el bursting productivo hay que añadir transferencia de entrada/salida, identidad del workload, almacenamiento, métricas reales de cola y provisión efímera del pool. No ejecutar hasta configurar y confirmar el contexto y sus cuotas.
