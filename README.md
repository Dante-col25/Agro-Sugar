# AgroSugar-IoT — Avance 2

Repositorio del equipo para la entrega de Arquitectura de Sistemas Computacionales (UNIAJC), caso AgroSugar. El informe técnico está en [docs/informe-avance2.docx](docs/informe-avance2.docx).

## Alcance

El diseño documenta la ruta KVM/QEMU → Docker → Kubernetes (k3s) y el procesamiento por lotes NDVI con posibilidad de Cloud Bursting. La alerta crítica menor a 100 ms permanece en Edge; Kubernetes no forma parte de ese camino crítico.

Este repositorio separa el diseño reproducible de la evidencia del laboratorio. El informe registra que el laboratorio usó QEMU emulado porque KVM/EPT no estuvo disponible, y que el clúster k3s tenía un solo nodo. No se reportan como ejecutados el bursting ni la medición real del PUE. Consulta la matriz de evidencias del informe antes de presentar resultados.

## Estructura

- `app/`: API de telemetría y su imagen Docker.
- `worker/`: plantilla para trabajos por lotes NDVI.
- `k8s/`: manifiestos Kubernetes para el entorno local.
- `k8s-nube/`: punto de partida para los trabajos en nube; requiere completar proveedor, almacenamiento y credenciales mediante secretos.
- `scripts/`: operaciones auxiliares de despliegue/bursting.
- `virtualization/`: comandos, XML de referencia y configuración de laboratorio KVM/QEMU.
- `evidence/`: capturas originales organizadas por herramienta. Añadir solo capturas reales y sanitizadas.
- `docs/`: informe de Avance 2.

## Entorno documentado

- Ubuntu Server en las VM del diseño; Docker; Kubernetes ligero k3s en laboratorio.
- Las versiones exactas deben registrarse con `uname -a`, `docker version`, `kubectl version` y `virsh version` antes de cerrar la entrega.
- No guardar contraseñas, claves SSH, tokens ni archivos `.env` en Git. Los datos de acceso se inyectan fuera del repositorio.

## Verificaciones del laboratorio

Usa estos comandos en el entorno donde se hizo la práctica y guarda la salida o captura en `evidence/`:

```bash
virsh list --all
docker stats --no-stream
kubectl get nodes -o wide
kubectl get pods -o wide
kubectl get deployments,services,ingress,hpa,cronjobs,pvc
```

Para documentar auto-sanación, elimina un Pod administrado por un Deployment y observa su reposición: `kubectl delete pod <pod>`, seguido de `kubectl get pods -w`. Anota hora inicial, hora de disponibilidad y contexto del clúster. No sustituyas capturas por salidas transcritas.

## Estado antes de entregar

- [ ] Revisar los manifiestos finales y validar CPU/memoria (requests y limits).
- [ ] Adjuntar capturas auténticas de `virsh list`, `docker stats` y `kubectl get pods`.
- [ ] Adjuntar evidencia de eliminación y reposición del Pod.
- [ ] Registrar claramente funcionalidades no ejecutadas o simuladas.
- [ ] Revisar que no haya secretos ni datos sensibles en el historial Git.
- [ ] Verificar integrantes, docente y versiones de herramientas en el informe.

## Construcción local del ejemplo

El código en `app/` y `worker/` es una base didáctica preparada para organizar el repositorio; no se afirma que sea el código usado para generar las capturas del informe. El worker procesa una lista pequeña de valores NDVI de ejemplo, no imágenes satelitales. Reemplacen o validen esta base con el código real del equipo antes de la entrega.

Para construir las imágenes en Docker:

```bash
docker build -t agro-sugar/telemetry-api:local ./app
docker build -t agro-sugar/ndvi-worker:local ./worker
```

En k3s, asegúrate de que las imágenes estén disponibles en el runtime del clúster (o publícalas en un registry configurado) antes de aplicar `k8s/`. El HPA necesita métricas de CPU disponibles; verifica el estado de metrics-server y del controlador Ingress del clúster. El host `telemetry.agrosugar.local` es un nombre de ejemplo que debe resolverse al Ingress local.

Los manifiestos son un punto de partida y pueden requerir ajustes según StorageClass, IngressClass, registry y configuración de k3s.
