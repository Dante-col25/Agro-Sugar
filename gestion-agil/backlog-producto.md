# Product Backlog

Historias candidatas derivadas de la guía, el informe y las evidencias actuales. Las prioridades son iniciales; el Product Owner y el equipo deben refinarlas. El estado de evidencia distingue una salida de laboratorio o simulación de una capacidad productiva.

| ID | Prioridad sugerida | Historia de usuario | Criterios de aceptación resumidos | Estado conocido |
|---|---|---|---|---|
| HU-01 | P1 | Como operador de campo, quiero que Edge genere alertas críticas sin depender de la nube para responder a tiempo. | Medir latencia en el nodo Edge; demostrar el objetivo <100 ms y conservar funcionamiento durante una desconexión. | Objetivo de diseño; falta prueba de campo. |
| HU-02 | P1 | Como operador de planta, quiero recibir datos sincronizados y recuperar los almacenados durante una caída de red. | Evidenciar sincronización <2 s cuando hay conexión y reenvío tras desconexión de hasta 24 h. | Objetivo de diseño; falta evidencia extremo a extremo. |
| HU-03 | P1 | Como desarrollador, quiero construir la API en una imagen reproducible y limitada para ejecutarla con seguridad. | Build documentado, endpoint de salud, usuario no root y CPU/memoria verificables; origen de la imagen y código deben corresponder. | Capturas históricas; código del repositorio es reconstrucción funcional, no fuente original de la imagen. |
| HU-04 | P1 | Como operador técnico, quiero que Kubernetes reponga una réplica caída. | Eliminar un Pod de un Deployment, registrar transición y confirmar una réplica Ready nuevamente. | Evidencia de laboratorio disponible: recuperación aproximada de 6 s en k3s de un nodo. |
| HU-05 | P1 | Como operador técnico, quiero que la API escale según carga y tenga límites explícitos. | HPA reporta métricas, alcanza objetivo configurado y muestra escala de subida y bajada; publicar captura sin errores activos de métricas. | Evidencia de 2→4→3→2; el historial también muestra advertencias previas de métricas. |
| HU-06 | P1 | Como analista agrícola, quiero procesar lotes NDVI sin bloquear la telemetría. | El Job consume imágenes reales, persiste salidas y deja logs/metadatos; CronJob y almacenamiento validados. | Manifiesto y worker de ejemplo; el worker actual promedia números y no procesa imágenes. |
| HU-07 | P2 | Como soporte, quiero seguir una muestra desde Edge hasta la base de datos para ubicar demoras. | Una traza conserva trace ID y spans padre/hijo; cada latencia medida está separada de la simulada. | Script y salida OpenTelemetry incluidos; latencias son simuladas. |
| HU-08 | P2 | Como servicio, quiero usar backoff y jitter para reducir reconexiones sincronizadas. | Reproducir comparación con semilla definida, publicar parámetros y aclarar capacidad asumida del gateway. | Simulación de 10.000 clientes; no es una prueba de carga real. |
| HU-09 | P2 | Como responsable de resiliencia, quiero aislar fallos y aplicar fallback para proteger operaciones críticas. | Demostrar fallo remoto, transición del breaker, fallback y recursos aislados; usar el caso AgroSugar y no mezclar manifiestos de UCI. | Los archivos actuales de breaker/bulkhead son ejemplo HospitValle UCI; adaptar antes de atribuir a AgroSugar. |
| HU-10 | P2 | Como operador de cosecha, quiero desbordar lotes pendientes a un pool de nube y retirarlo al bajar la cola. | Métricas de cola reales activan Job; entrada y salida se transfieren; se registra costo y limpieza de recursos. | Script demostrativo depende de un contexto preconfigurado; no aprovisiona nodos ni mueve imágenes. |
| HU-11 | P2 | Como administrador, quiero virtualizar el host de planta con KVM y thin provisioning. | `virsh`, XML, EPT/NPT y qcow2 se verifican en hardware compatible y se capturan. | Laboratorio usó QEMU emulado; KVM acelerado y EPT no demostrados. |
| HU-12 | P3 | Como responsable de infraestructura, quiero medir PUE y costos con datos observados. | Medir energía TI e instalación en el mismo periodo y documentar tarifa/cotización y límites. | Informe presenta supuestos; falta medición/cotización vigente. |

## Estados sugeridos para issues

- `propuesta`: requisito acordado, implementación aún no iniciada.
- `en progreso`: existe trabajo activo y un responsable asignado.
- `simulado`: resultado reproducible con cargas o datos sintéticos.
- `validado en laboratorio`: evidencia capturada en el entorno del equipo.
- `validado en campo`: prueba en el entorno AgroSugar representativo.

No usar `Done` para una salida simulada cuando el criterio exige una medida de campo.
