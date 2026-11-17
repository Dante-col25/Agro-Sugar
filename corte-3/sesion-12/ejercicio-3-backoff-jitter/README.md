# Ejercicio 3 · Backoff exponencial y jitter

## Archivos

- `informe/Seccion3_Ejercicio3_Backoff_Jitter.docx`: informe Word original incluido en el ZIP.
- `README-original.md`: guía original de la entrega, conservada como referencia.
- `src/`: simulaciones de jitter sin jitter, jitter fijo y Full Jitter.
- `salidas/`: resultados de consola incluidos en el ZIP.
- `evidencias/ubuntu/`: capturas originales de las ejecuciones en Ubuntu.
- `graficas/`: histograma original en PDF y versión recortada en PNG.
- `requirements.txt`: dependencia de graficación fijada en el ZIP.

El análisis simula el primer reintento de 10.000 sensores con una capacidad supuesta del gateway de 2.000 TPS. El informe aclara que no incluye latencia de red y que la capacidad debe validarse con la arquitectura integrada. Los resultados son de simulación, no pruebas de carga sobre el gateway real.

## Reproducir

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/backoff_jitter.py | tee salidas/salida_guia.txt
python src/backoff_extendido.py | tee salidas/salida_extendida.txt
```

`backoff_extendido.py` guarda `histograma_jitter.png` en el directorio desde el que se ejecuta.

## Pendiente antes de entregar

El informe Word todavía contiene marcadores para integrantes, fecha y enlace al repositorio. También se debe verificar que la Figura 1 corresponde a la gráfica final y que las salidas presentadas son las generadas por el código versionado.
