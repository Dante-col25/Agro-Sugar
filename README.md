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
- [ ] Ejecutar `scripts/check-container-namespaces.sh telemetry-api` y adjuntar la salida real de PID, NET y MNT.
- [ ] Adjuntar capturas auténticas de `virsh list`, `docker stats` y `kubectl get pods`.
- [ ] Aplicar los manifiestos actuales y adjuntar la salida de Pods, Ingress, HPA, PVC y CronJob.
- [ ] Capturar salida real del host (`lscpu`, `free`, `lsblk`, `virt-host-validate`) y EPT solo si KVM está disponible.
- [ ] Adjuntar evidencia de eliminación y reposición del Pod.
- [ ] Registrar claramente funcionalidades no ejecutadas o simuladas.
- [ ] Revisar que no haya secretos ni datos sensibles en el historial Git.
- [ ] Verificar integrantes, docente y versiones de herramientas en el informe.

## Evidencias adjuntas

Las capturas originales del laboratorio están en [evidence/](evidence/), con un índice por herramienta y notas sobre su alcance. El código de ejemplo en `app/` ofrece las rutas `/health/live` y `/health/ready` que usan las sondas; el Dockerfile también incluye healthcheck y Gunicorn con `/dev/shm`. El origen de la imagen capturada no estaba en los archivos recibidos, así que la implementación actual reproduce el comportamiento visible, pero no demuestra ser el mismo código binario. La evidencia de virtualización es QEMU emulado (`domain type='qemu'`), no KVM acelerado.

## Construcción local del ejemplo

El código en `app/` y `worker/` es una base didáctica preparada para organizar el repositorio; no se afirma que sea el código usado para generar las capturas del informe. El worker procesa una lista pequeña de valores NDVI de ejemplo, no imágenes satelitales. Reemplacen o validen esta base con el código real del equipo antes de la entrega.

Para construir las imágenes en Docker:

```bash
docker build -t agrosugar/telemetry-api:1.0.0 ./app
docker build -t agrosugar/ndvi-worker:1.0.0 ./worker
```

En k3s, asegúrate de que las imágenes estén disponibles en el runtime del clúster antes de aplicar `k8s/`. Si Docker está separado de containerd de k3s, puedes exportarlas e importarlas así:

```bash
docker save agrosugar/telemetry-api:1.0.0 -o /tmp/telemetry-api.tar
docker save agrosugar/ndvi-worker:1.0.0 -o /tmp/ndvi-worker.tar
sudo k3s ctr images import /tmp/telemetry-api.tar
sudo k3s ctr images import /tmp/ndvi-worker.tar
kubectl apply -f k8s/telemetry.yaml
kubectl apply -f k8s/ndvi-batch.yaml
```

El HPA necesita métricas de CPU disponibles; verifica el estado de metrics-server y del controlador Ingress del clúster. El host `telemetry.agrosugar.local` es un nombre de ejemplo que debe resolverse al Ingress local.

Para recopilar evidencia de aislamiento PID/NET/MNT y límites en el mismo contenedor:

```bash
docker run -d --name telemetry-api -p 8080:8080 --cpus=1.0 --memory=512m --pids-limit=128 agrosugar/telemetry-api:1.0.0
./scripts/check-container-namespaces.sh telemetry-api | tee evidence/docker/namespaces-host.txt
docker stats --no-stream telemetry-api
docker rm -f telemetry-api
```

Guarda `namespaces-host.txt` solo después de ejecutar los comandos en el host Linux; no lo generes a partir de valores esperados.

Los manifiestos son un punto de partida y pueden requerir ajustes según StorageClass, IngressClass, registry y configuración de k3s. `k8s/telemetry.yaml` usa el tag mostrado en la captura; para desplegarlo hay que construir esa imagen y cargarla en el runtime de k3s o publicarla en un registry accesible.
