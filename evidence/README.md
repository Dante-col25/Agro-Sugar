# Evidencias del laboratorio

Capturas de consola compartidas por el equipo. Se conservan como JPG originales y se agrupan por herramienta. No prueban por sí solas los puntos marcados como diseño en el informe.

## Docker

| Archivo | Qué muestra | Observación |
|---|---|---|
| [01-health-and-image.jpg](docker/01-health-and-image.jpg) | Respuesta HTTP 200 de `/health/live` y la imagen `agrosugar/telemetry-api:1.0.0`. | La respuesta es `status: alive`; esta etiqueta es distinta de la imagen local de ejemplo del repositorio. |
| [02-build-and-container-run.jpg](docker/02-build-and-container-run.jpg) | Build exitoso, etiqueta de imagen y ejecución de contenedor con CPU, memoria y PIDs limitados. | La captura corresponde a `agrosugar/telemetry-api:1.0.0`, no al código de ejemplo agregado después a `app/`. |
| [03-stats-cgroups-and-processes.jpg](docker/03-stats-cgroups-and-processes.jpg) | `docker stats`, límites inspeccionados, procesos del contenedor y valores cgroup. | Se observan 512 MiB, cuota CPU 1.0 y límite de 128 PIDs. |

## Kubernetes

| Archivo | Qué muestra | Observación |
|---|---|---|
| [01-apply-and-cluster-status.jpg](kubernetes/01-apply-and-cluster-status.jpg) | Aplicación de Deployment, Service y HPA; nodo Ready y dos réplicas; HPA entre 2 y 8. | La consola registra también un comando inicial con error de sintaxis y luego el comando correcto. |
| [02-pod-replacement.jpg](kubernetes/02-pod-replacement.jpg) | El Pod eliminado termina y el Deployment crea otro que llega a Running/Ready aproximadamente en 6 segundos. | Evidencia de auto-sanación en el clúster de un solo nodo mostrado. |
| [03-delete-pod-command.jpg](kubernetes/03-delete-pod-command.jpg) | Nodo, Pods y Service junto con el comando de eliminación. | Complementa la secuencia de reposición de la captura anterior. |
| [04-hpa-scale-events.jpg](kubernetes/04-hpa-scale-events.jpg) | Eventos de HPA: escalado exitoso a 4 réplicas y luego a 3 al bajar el uso. | El historial también muestra errores previos al obtener métricas; se documenta la condición tal como aparece. |
| [05-hpa-baseline.jpg](kubernetes/05-hpa-baseline.jpg) | HPA en reposo: CPU 2%, objetivo 70%, mínimo 2, máximo 8 y 2 réplicas. | Es una lectura en reposo, no una prueba de carga. |

## KVM/libvirt y almacenamiento

| Archivo | Qué muestra | Observación |
|---|---|---|
| [01-vms-and-domain-config.jpg](virsh/01-vms-and-domain-config.jpg) | `virsh list --all`, `dominfo` y XML de `agro-cp`; ambas VM aparecen corriendo. | El XML indica `domain type='qemu'`: es emulación, no KVM acelerado por hardware ni evidencia de EPT activo. |
| [02-qcow2-thin-provisioning.jpg](virsh/02-qcow2-thin-provisioning.jpg) | `qemu-img info` para el disco qcow2. | Tamaño virtual 10 GiB, espacio ocupado cercano a 27,2 MiB y archivo base/backing file. |

## Límites de estas evidencias

Las capturas Docker muestran una imagen/tag anterior (`agrosugar/telemetry-api:1.0.0`); el directorio `app/` es una base de ejemplo agregada al repositorio y no debe atribuirse a esa ejecución. Las capturas de virsh corresponden a QEMU emulado. El HPA de las capturas permite hasta 8 Pods; por coherencia, `k8s/telemetry.yaml` también usa `maxReplicas: 8`.
