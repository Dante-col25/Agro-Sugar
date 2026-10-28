# API de telemetría de ejemplo

La API devuelve `{"status":"alive"}` en `/health/live` y `{"status":"ready"}` en `/health/ready`. También conserva `/health` como alias de liveness. `POST /telemetry` acepta un objeto JSON no vacío.

La implementación se ajustó para que las rutas de salud coincidan con las capturas aportadas. No se dispone del código fuente original que generó la imagen capturada; este código permite una reconstrucción funcional, pero no acredita que sea idéntico a aquella imagen.

Construcción local: `docker build -t agrosugar/telemetry-api:1.0.0 ./app`.
