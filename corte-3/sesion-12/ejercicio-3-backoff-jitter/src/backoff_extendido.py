import random
from collections import Counter
import matplotlib.pyplot as plt

T_BASE, T_MAX, JITTER, N, C = 1.0, 30.0, 0.5, 10_000, 2_000
MODOS = ["sin_jitter", "jitter_fijo", "full_jitter"]

def t_wait(intento, modo):
    base = min(T_MAX, T_BASE * 2 ** intento)
    if modo == "sin_jitter":
        return base
    if modo == "jitter_fijo":
        return base + random.uniform(0, JITTER)
    return random.uniform(0, base)  # full_jitter

def pico_por_ms(tiempos):
    return max(Counter(int(t * 1000) for t in tiempos).values())

def segundos_sobre_C(tiempos):
    return sum(1 for v in Counter(int(t) for t in tiempos).values() if v > C)

random.seed(42)
fig, ejes = plt.subplots(1, 3, figsize=(15, 4), sharey=True)
for eje, modo in zip(ejes, MODOS):
    tiempos = [t_wait(1, modo) for _ in range(N)]
    print(f"{modo}: pico/ms = {pico_por_ms(tiempos)}, segundos sobre C = {segundos_sobre_C(tiempos)}")
    eje.hist(tiempos, bins=200)
    eje.set_title(modo)
    eje.set_xlabel("Tiempo tras la falla (s)")
    eje.set_ylabel("Peticiones")
plt.tight_layout()
plt.savefig("histograma_jitter.png", dpi=150)
print("Gráfica guardada: histograma_jitter.png")
