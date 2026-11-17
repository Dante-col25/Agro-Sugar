# Ejercicio 1 · Trazabilidad de AgroSugar

## Archivos

- `src/traza_agrosugar.py`: genera una traza simulada de sensor → Edge MQTT → API → ingesta → TimescaleDB usando spans de OpenTelemetry.
- `salidas/resultado_traza.txt`: salida guardada de la ejecución incluida en el ZIP.
- `requirements.txt`: versiones recuperadas del `venv-otel` incluido en el ZIP.

El script usa latencias simuladas de 12 ms (Edge), 8 ms (API), 45 ms (ingesta) y 3 ms (base de datos): 68 ms sumados. La salida observa cerca de 85,65 ms de tiempo total del proceso. Esto demuestra propagación de contexto en una simulación; no es medición de latencia de la arquitectura desplegada.

Nota de contenido: el identificador de cultivo en el script dice `cultivo_cafe_01`, aunque el proyecto es caña de azúcar. Cambiarlo a un identificador de caña y regenerar la salida antes de usarla como evidencia final.

## Reproducir

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/traza_agrosugar.py | tee salidas/resultado_traza.txt
```

El entorno virtual no se versiona; se reconstruye con el archivo de dependencias.
