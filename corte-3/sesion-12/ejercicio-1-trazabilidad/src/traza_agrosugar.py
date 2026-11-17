# ============================================================
# PROYECTO: AgroSugar
# EJERCICIO 1: TRAZABILIDAD DISTRIBUIDA
# TECNOLOGIA: Python + OpenTelemetry
# ============================================================

import time

from opentelemetry import trace, propagate
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    SimpleSpanProcessor,
    ConsoleSpanExporter
)

# ------------------------------------------------------------
# 1. CONFIGURACION DEL SISTEMA DE TRAZABILIDAD
# ------------------------------------------------------------

resource = Resource.create({
    "service.name": "AgroSugar",
    "service.namespace": "agricultura-iot",
    "deployment.environment": "pruebas"
})

provider = TracerProvider(resource=resource)

# Exportador que muestra las trazas en la terminal
exporter = ConsoleSpanExporter()

provider.add_span_processor(
    SimpleSpanProcessor(exporter)
)

trace.set_tracer_provider(provider)

tracer = trace.get_tracer("agrosugar.tracing")

# ------------------------------------------------------------
# 2. DATOS DEL SENSOR AGRICOLA
# ------------------------------------------------------------

sensor_id = "sensor045"
crop_id = "cultivo_cafe_01"

print("\n======================================")
print(" INICIANDO TRAZABILIDAD - AGROSUGAR")
print("======================================")

print(f"Sensor: {sensor_id}")
print(f"Cultivo: {crop_id}")

# Latencias simuladas en milisegundos
latencias = {
    "edge": 12,
    "api": 8,
    "ingesta": 45,
    "database": 3
}

# ------------------------------------------------------------
# 3. FUNCION PARA PROPAGAR EL CONTEXTO
# ------------------------------------------------------------

def ejecutar_salto(nombre, protocolo, latencia, atributos, siguiente=None):
    """
    Crea un span hijo y propaga el contexto al siguiente servicio.
    """

    # Capturar el contexto del servicio que está ejecutándose
    carrier = {}
    propagate.inject(carrier)

    # Recuperar el contexto recibido
    contexto_recibido = propagate.extract(carrier)

    print(f"\n>>> Enviando contexto a: {nombre}")
    print("traceparent:", carrier.get("traceparent"))

    with tracer.start_as_current_span(
        nombre,
        context=contexto_recibido,
        attributes={
            "service.name": nombre,
            "network.protocol.name": protocolo,
            "tenant": "agrosugar",
            **atributos
        }
    ):
        print(f"Procesando {nombre}...")
        time.sleep(latencia / 1000)
        print(f"Finalizado: {nombre} ({latencia} ms)")

        # Ejecutar el siguiente servicio dentro del span actual
        if siguiente is not None:
            siguiente()


# ------------------------------------------------------------
# 4. TRAZA PRINCIPAL Y FLUJO DISTRIBUIDO
# ------------------------------------------------------------

inicio = time.perf_counter()

# Definir el flujo de servicios de atrás hacia adelante

def paso_database():
    ejecutar_salto(
        "salto4.timescaledb.insert",
        "postgresql",
        latencias["database"],
        {
            "db.system": "postgresql",
            "db.operation": "INSERT",
            "db.name": "agrosugar"
        }
    )

def paso_ingesta():
    ejecutar_salto(
        "salto3.ingesta-service",
        "http",
        latencias["ingesta"],
        {"measurement.type": "soil_moisture"},
        siguiente=paso_database
    )

def paso_api():
    ejecutar_salto(
        "salto2.api-gateway",
        "http",
        latencias["api"],
        {"gateway.name": "api-gateway"},
        siguiente=paso_ingesta
    )

try:
    with tracer.start_as_current_span(
        "root.sensor-agrosugar",
        attributes={
            "sensor.id": sensor_id,
            "crop.id": crop_id,
            "measurement.type": "soil_moisture",
            "tenant": "agrosugar"
        }
    ):
        print("\n[SPAN RAIZ] Sensor IoT AgroSugar")

        ejecutar_salto(
            "salto1.edge-mqtt",
            "mqtt",
            latencias["edge"],
            {"sensor.id": sensor_id},
            siguiente=paso_api
        )

        print("\n[OK] Flujo de datos completado.")

finally:
    fin = time.perf_counter()

    print("\n======================================")
    print(" RESUMEN DE LATENCIAS SIMULADAS")
    print("======================================")

    total = sum(latencias.values())

    for servicio, milisegundos in latencias.items():
        porcentaje = (milisegundos / total) * 100
        print(f"{servicio}: {milisegundos} ms ({porcentaje:.1f}%)")

    print(f"\nLatencia simulada total: {total} ms")
    print(f"Tiempo total observado: {(fin - inicio) * 1000:.2f} ms")

    provider.shutdown()
    print("\nTrazabilidad AgroSugar finalizada.")
