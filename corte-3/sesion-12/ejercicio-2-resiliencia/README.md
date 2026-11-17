# Ejercicio 2 · Patrones de resiliencia

## Archivos

- `src/circuit_breaker_uci.py`: simulación de llamadas a IA remota con fallos, respuestas lentas y fallback.
- `src/bulkhead_uci.py`: separa pools de tareas y usa un semáforo para aplicar fail-fast.
- `src/calculos_disponibilidad.py`: cálculos basados en supuestos del taller.
- `k8s/bulkhead-hospitvalle.yaml`: PriorityClass y Deployments de referencia.
- `evidencias/`: capturas incluidas en el ZIP.
- `requirements.txt`: dependencia externa identificada en el código.

## Alcance y advertencias

Este material usa el escenario **HospitValle UCI** (alertas médicas e IA de arritmias). Se conserva separado del diseño AgroSugar y su manifiesto no debe aplicarse al clúster AgroSugar tal como está: usa imágenes `hospitvalle/*` y una PriorityClass de UCI.

Las simulaciones y cálculos no son mediciones de disponibilidad real. El ZIP no especificaba la versión instalada de PyBreaker; `requirements.txt` identifica la dependencia, pero debe fijarse a la versión usada por el equipo si se necesita reproducibilidad exacta.

## Reproducir

Los dos primeros scripts requieren Python 3. El Circuit Breaker además requiere PyBreaker:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/circuit_breaker_uci.py
python src/bulkhead_uci.py
python src/calculos_disponibilidad.py
```

No aplicar el manifiesto en un clúster real sin sustituir imágenes de ejemplo, revisar cuotas y validar la política de prioridad.
