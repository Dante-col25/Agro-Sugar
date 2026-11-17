# Corte 3 · Sesión 12

## Índice

| Ejercicio | Tema | Contenido |
|---|---|---|
| [1 · Trazabilidad AgroSugar](ejercicio-1-trazabilidad/README.md) | Trazas distribuidas con OpenTelemetry | Script, dependencias recuperadas del entorno incluido y salida de consola. |
| [2 · Patrones de resiliencia](ejercicio-2-resiliencia/README.md) | Circuit Breaker, Bulkhead, disponibilidad y cgroups | Scripts, manifiesto Kubernetes y capturas. El ejemplo de código/manifiesto usa el caso HospitValle UCI. |
| [3 · Backoff y jitter](ejercicio-3-backoff-jitter/README.md) | Tormenta de reintentos y simulación de 10.000 sensores | Informe Word, scripts, dependencias, salidas, capturas de Ubuntu y gráficas. |

## Criterio de organización

- Las capturas originales se guardan en `evidencias/`; las salidas de texto en `salidas/`; las figuras en `graficas/`.
- El entorno virtual `venv-otel/` del ZIP se excluyó: no es portable y como contenía cientos de archivos de paquetes instalados. Entonces sus versiones relevantes quedaron fijadas en `ejercicio-1-trazabilidad/requirements.txt`.
- No se incluyen bytecode, cachés ni ejecutables del entorno virtual.
- Los resultados de simulación se mantienen como resultados del ejercicio; no se presentan como mediciones de producción.


## Alcance del caso

El Ejercicio 1 está orientado a AgroSugar. El Ejercicio 2 contiene un escenario de UCI/HospitValle y se conserva separado para no confundirlo con la arquitectura agrícola. El Ejercicio 3 es una simulación del taller integrado, con supuestos explícitos sobre sensores y capacidad del gateway.
