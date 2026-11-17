
from concurrent.futures import ThreadPoolExecutor
import threading
import time
import random

# ============================================================
# COMPARTIMENTOS (Bulkhead) - pools independientes
# ============================================================
pool_alertas = ThreadPoolExecutor(max_workers=16, thread_name_prefix="uci-alerta")
pool_telemetria = ThreadPoolExecutor(max_workers=8, thread_name_prefix="telemetria")
pool_ia = ThreadPoolExecutor(max_workers=4, thread_name_prefix="ia-nube")

# Semáforo para limitar cola de IA (4 en ejecución + 20 en cola)
cupo_ia = threading.BoundedSemaphore(4 + 20)

def tarea_alerta_critica(id_alerta):
    """Alertas UCI: NUNCA se descartan"""
    time.sleep(0.1)
    return f"ALERTA {id_alerta} procesada (prioridad max)"

def tarea_telemetria(id_tele):
    """Telemetría regular: puede descartarse si se llena"""
    time.sleep(0.05)
    return f"Telemetría {id_tele} registrada"

def tarea_ia(muestra):
    """Cliente IA: si el compartimento está lleno -> fallback inmediato"""
    time.sleep(0.5)  # Simula latencia WAN
    return f"IA procesó {muestra}"

def enviar_a_ia(muestra):
    """Bulkhead: si no hay cupo, NO bloquea, usa fallback"""
    if not cupo_ia.acquire(blocking=False):
        # Compartimento lleno -> fail-fast al fallback
        return {"fuente": "fallback_por_bulkhead", "muestra": muestra}
    
    fut = pool_ia.submit(tarea_ia, muestra)
    fut.add_done_callback(lambda _: cupo_ia.release())
    return {"fuente": "ia_nube", "futuro": fut}

# ============================================================
# DEMOSTRACIÓN: 30 tareas mixtas
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("DEMOSTRACIÓN BULKHEAD - Aislamiento de compartimentos")
    print("=" * 60)
    
    # Enviar 30 tareas de IA rápidamente (más de lo que el pool soporta)
    print("\n--- Enviando 30 tareas de IA (pool max=4, cola max=20) ---")
    resultados_ia = []
    for i in range(30):
        res = enviar_a_ia(f"muestra_{i}")
        resultados_ia.append(res)
    
    # Contar cuántas usaron fallback por bulkhead lleno
    fallbacks = sum(1 for r in resultados_ia if r["fuente"] == "fallback_por_bulkhead")
    print(f"Tareas IA enviadas a nube: {30 - fallbacks}")
    print(f"Tareas IA con FALLBACK por bulkhead lleno: {fallbacks}")
    print("(Las que no cupieron usaron fallback INMEDIATO, sin bloquear hilos)")
    
    # Alertas críticas SIEMPRE tienen su pool libre
    print("\n--- Alertas críticas (pool separado, max=16) ---")
    for i in range(5):
        pool_alertas.submit(tarea_alerta_critica, i)
        print(f"Alerta {i} enviada a pool_alertas (NO compite con IA)")
    
    # Esperar a que terminen
    time.sleep(2)
    pool_alertas.shutdown(wait=True)
    pool_telemetria.shutdown(wait=True)
    pool_ia.shutdown(wait=True)
    print("\n✅ Demostración completada: los compartimentos están aislados.")
