# Supuestos del taller
AL = 0.999995   # Núcleo local UCI (redundancia activo-activo)
AW = 0.999      # WAN
AC = 0.9995     # IA en nube
AF = 0.9999     # Fallback local (caché/modelo ligero)

# (a) SIN Circuit Breaker: serie
A_remota = AW * AC
A_serie = AL * A_remota
caida_serie_min = (1 - A_serie) * 525600
print(f"--- SIN Circuit Breaker ---")
print(f"A_remota = {A_remota:.8f}")
print(f"A_serie = {A_serie:.8f}")
print(f"Caída anual = {caida_serie_min:.1f} min = {caida_serie_min/60:.1f} h")
print(f"¿Cumple SLA 99.999%? {'SÍ' if caida_serie_min <= 5.256 else 'NO'}")
print()

# (b) CON Circuit Breaker + Fallback: paralelo
A_func = 1 - (1 - A_remota) * (1 - AF)
A_total = AL * A_func
caida_total_min = (1 - A_total) * 525600
print(f"--- CON Circuit Breaker + Fallback ---")
print(f"A_func (remota || fallback) = {A_func:.8f}")
print(f"A_total = {A_total:.8f}")
print(f"Caída anual = {caida_total_min:.2f} min")
print(f"¿Cumple SLA 99.999% (5.256 min)? {'SÍ' if caida_total_min <= 5.256 else 'NO'}")
print()

# Ley de Little
lam = 100  # consultas/s
W_sin_cb = 5.0  # timeout por defecto 5s
L_sin = lam * W_sin_cb
print(f"--- Ley de Little ---")
print(f"Sin CB: L = {lam} × {W_sin_cb} = {L_sin} hilos bloqueados")
W_con_cb = 0.00005  # 0.05ms respuesta fail-fast
L_con = lam * W_con_cb
print(f"Con CB OPEN: L = {lam} × {W_con_cb} = {L_con:.3f} hilos")
print(f"Reducción de hilos bloqueados: {L_sin/L_con:.0f}x")
