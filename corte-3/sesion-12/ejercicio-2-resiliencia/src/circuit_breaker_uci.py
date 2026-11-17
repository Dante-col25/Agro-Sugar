import pybreaker
import time
import random
from datetime import datetime

# ============================================================
# 1. CONFIGURACIÓN DEL CIRCUIT BREAKER (valores del taller)
# ============================================================
# fail_max = 4 equivale a Failure Rate Threshold 20% con ventana de 20 llamadas
# (4 fallos de 20 = 20%)
# reset_timeout = 15 s (Wait Duration in Open State)
breaker = pybreaker.CircuitBreaker(
    fail_max=4,           # Abre tras 4 fallos en ventana
    reset_timeout=15,     # Espera 15s antes de pasar a HALF-OPEN
    success_threshold=3,  # 3 éxitos en HALF-OPEN para cerrar (Permitted Calls)
    exclude=[ValueError]  # Errores de negocio NO cuentan como fallo
)

# ============================================================
# 2. FUNCIÓN QUE SIMULA LA LLAMADA A LA IA EN LA NUBE
# ============================================================
def llamar_ia_nube(muestra_ecg):
    """
    Simula la llamada WAN a la IA de arritmias.
    - 30% de las veces falla (simula WAN caída)
    - 20% de las veces es lenta (>500ms) para probar Slow Call
    """
    escenario = random.random()
    
    if escenario < 0.30:  # 30% fallo de red
        time.sleep(0.1)
        raise ConnectionError("WAN caída o timeout")
    elif escenario < 0.50:  # 20% llamada lenta (Slow Call > 500ms)
        time.sleep(0.6)  # 600ms > 500ms threshold
        return {"diagnostico": "normal", "latencia_ms": 600, "fuente": "nube"}
    else:  # 50% éxito normal
        time.sleep(0.05)  # 50ms
        return {"diagnostico": "normal", "latencia_ms": 50, "fuente": "nube"}

# ============================================================
# 3. FALLBACK LOCAL (caché + modelo ligero en Edge UCI)
# ============================================================
def fallback_local(muestra_ecg):
    """
    Se ejecuta cuando el circuito está OPEN o la llamada falla.
    Respuesta inmediata (<1ms) usando modelo local.
    """
    return {
        "diagnostico": "analisis_basico_local",
        "latencia_ms": 0.8,
        "fuente": "edge_uci_fallback",
        "alerta": False
    }

# ============================================================
# 4. FUNCIÓN PRINCIPAL PROTEGIDA
# ============================================================
def analizar_muestra(muestra_ecg):
    """
    Intenta IA en nube con Circuit Breaker.
    Si el circuito está OPEN o falla, usa fallback local.
    """
    try:
        # pybreaker.call ejecuta la función protegida
        resultado = breaker.call(llamar_ia_nube, muestra_ecg)
        return resultado
    except (pybreaker.CircuitBreakerError, ConnectionError) as e:
        # CircuitBreakerError: circuito OPEN (fail-fast, no espera)
        # ConnectionError: fallo en la llamada
        print(f"  [FALLBACK] Circuito OPEN o fallo: {type(e).__name__}")
        return fallback_local(muestra_ecg)
    except Exception as e:
        print(f"  [ERROR] {e}")
        return fallback_local(muestra_ecg)

# ============================================================
# 5. SIMULACIÓN: 100 consultas para ver el comportamiento
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("SIMULACIÓN CIRCUIT BREAKER - UCI HospitValle")
    print("=" * 60)
    print(f"Config: fail_max={breaker.fail_max}, reset_timeout={breaker.reset_timeout}s")
    print()
    
    exitos_nube = 0
    fallbacks = 0
    
    for i in range(100):
        try:
            resultado = analizar_muestra(f"ECG_{i}")
            fuente = resultado["fuente"]
            latencia = resultado["latencia_ms"]
            
            if fuente == "nube":
                exitos_nube += 1
            else:
                fallbacks += 1
            
            # Mostrar cambios de estado del circuito
            estado_actual = breaker.current_state
            if i % 10 == 0 or estado_actual != "closed":
                print(f"[{i:03d}] Estado CB: {estado_actual.upper():10s} | "
                      f"Fuente: {fuente:20s} | Latencia: {latencia}ms")
                
        except Exception as e:
            print(f"[{i:03d}] Error no controlado: {e}")
        
        time.sleep(0.05)  # Simula frecuencia de llegada de muestras
    
    print()
    print("=" * 60)
    print(f"RESUMEN: Llamadas exitosas a nube: {exitos_nube} | Fallbacks locales: {fallbacks}")
    print(f"Estado final del Circuit Breaker: {breaker.current_state.upper()}")
    print("=" * 60)
