# backoff_jitter.py - Compara reintentos sin jitter vs con jitter (10.000 sensores AgroSugar)
import random
from collections import Counter

T_BASE, T_MAX, JITTER, N = 1.0, 30.0, 0.5, 10_000

def t_wait(intento, jitter=True):
    return min(T_MAX, T_BASE * 2 ** intento) + (random.uniform(0, JITTER) if jitter else 0.0)

def pico_por_ms(jitter, intento=1):
    llegadas = Counter(int(t_wait(intento, jitter) * 1000) for _ in range(N))
    return max(llegadas.values()), len(llegadas)

random.seed(42)
for j in (False, True):
    pico, ventanas = pico_por_ms(j)
    print(f"Jitter={j}: pico = {pico}")
