# Ejercicio 3 · Sesión 12 · Backoff con jitter y Thundering Herd

Entrega del Ejercicio 3 del taller guiado (Arquitectura de Sistemas Computacionales, UNIAJC) para el proyecto integrador MetroMIO-IoT, HospitValle UCI y AgroSugar.

## Contenido

| Carpeta | Qué contiene |
|---|---|
| `1_informe/` | Sección 3 del informe en Word (formato APA 7). |
| `2_codigo/` | Scripts de la simulación y `requirements.txt`. |
| `3_salidas/` | Salidas de consola de cada script. |
| `4_evidencias_ubuntu/` | Capturas de la terminal en Ubuntu con la ejecución de ambos scripts. |
| `5_graficas/` | Histograma generado por `backoff_extendido.py` (original y recortado). |

## Cómo reproducir en Ubuntu

```bash
mkdir -p ~/simulacion_backoff && cd ~/simulacion_backoff
cp /ruta/a/esta/carpeta/2_codigo/* .
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 backoff_jitter.py | tee salida_guia.txt
python3 backoff_extendido.py | tee salida_extendida.txt
```

Los scripts usan `random.seed(42)`, así que los números son reproducibles.

## Resultados esperados

| Variante | Pico por ms | Segundos sobre C |
|---|---|---|
| Sin jitter | 10.000 | 1 |
| Jitter fijo (0,5 s) | 37 | 1 |
| Full Jitter | 14 | 2 |

## Antes de entregar

- [ ] Completar en el informe: integrantes, fecha y enlace al repositorio (Anexo A).
- [ ] Reemplazar `2_codigo/` y `3_salidas/` por los archivos reales de `~/simulacion_backoff` en Ubuntu. Los incluidos aquí son reconstrucciones a partir de la guía y de las capturas.
- [ ] Revisar que la Figura 1 del informe corresponda a la gráfica final.
