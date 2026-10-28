# Kubernetes local

- `telemetry.yaml`: Deployment con dos réplicas, rolling update sin indisponibilidad intencional, Service ClusterIP, Ingress de ejemplo, probes y HPA (2-8, objetivo CPU 70%).
- `ndvi-batch.yaml`: PVC y CronJob diario con valores NDVI de demostración montados desde ConfigMap.

La imagen `agrosugar/telemetry-api:1.0.0` debe existir en el runtime del nodo k3s o en un registry accesible. Reemplaza el host `telemetry.agrosugar.local` y revisa la clase Ingress, StorageClass, métricas y capacidad de nodo antes de aplicar. Estos manifiestos aún deben validarse en el clúster del equipo.
