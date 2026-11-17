# Propuesta de Sprints

Los Sprints siguientes son una secuencia sugerida, no un historial de iteraciones realizadas. Se propone una duración fija de dos semanas para cada Sprint; el equipo debe confirmarla antes de usar el plan. Las fechas, responsables y estimaciones se acuerdan durante Sprint Planning. No se asignan puntos sin estimación del equipo.

| Sprint | Objetivo | Historias candidatas | Incremento revisable |
|---|---|---|---|
| S1 · Flujo observable | Acordar el flujo de datos y hacer visibles sus etapas y límites. | HU-01, HU-02, HU-07 | Diagrama actualizado, trazas con datos de prueba y plan de medición Edge. |
| S2 · Servicio desplegable | Empaquetar la API y ejecutar una versión reproducible en Kubernetes. | HU-03, HU-04, HU-05 | Imagen identificada, Deployment/Service/Ingress/probes/HPA aplicados y evidencia del clúster. |
| S3 · Resiliencia y lotes | Separar el procesamiento por lotes y proteger el servicio ante fallos y ráfagas. | HU-06, HU-08, HU-09 | Job NDVI con datos definidos, simulación de jitter y patrón de resiliencia adaptado a AgroSugar. |
| S4 · Operación híbrida | Decidir con mediciones si y cuándo se necesita capacidad externa o ajuste de infraestructura. | HU-10, HU-11, HU-12 | Prueba de bursting con costo/limpieza, medición KVM compatible y PUE medido; si el entorno no está disponible, registrar impedimentos y evidencia alternativa. |

## Revisión de cada Sprint

1. **Sprint Planning:** definir por qué este Sprint aporta valor, qué Product Backlog Items caben y cómo se abordarán.
2. **Daily Scrum:** revisar cada día el avance hacia el Sprint Goal y ajustar el plan de trabajo.
3. **Sprint Review:** revisar el incremento con interesados, criterios de aceptación y evidencia original.
4. **Sprint Retrospective:** acordar una mejora concreta para el siguiente Sprint.
5. Registrar trabajo no terminado y reordenar el Product Backlog antes de la siguiente planificación.

Las tareas se pueden mover en un tablero Kanban de GitHub Projects; el tablero visualiza el flujo, pero no reemplaza los objetivos ni los eventos de Scrum.
