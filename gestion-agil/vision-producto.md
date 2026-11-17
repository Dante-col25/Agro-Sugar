# Visión del producto

## Propósito

Ayudar al equipo de operación agrícola a observar telemetría de maquinaria y condiciones del cultivo de caña, conservar datos durante interrupciones de conectividad y procesar lotes de análisis sin poner en riesgo las alertas locales.

## Product Goal propuesto

Entregar una plataforma piloto que capture datos de campo, sostenga alertas locales durante una desconexión y procese lotes de cultivo con trazabilidad y límites operativos medibles.

## Usuarios principales

- Operadores de campo que necesitan alertas accionables cerca de los sensores.
- Personal de planta que supervisa la ingesta y disponibilidad de los servicios.
- Equipo técnico que despliega, mantiene y revisa la infraestructura.

## Objetivos de diseño

- Generar alertas críticas en Edge con una meta de latencia menor a 100 ms.
- Mantener hasta 24 horas de datos en buffer local y sincronizar con la planta en menos de 2 s cuando haya conectividad.
- Separar la API de telemetría de los trabajos por lotes NDVI.
- Escalar servicios stateless con Kubernetes y trasladar lotes de cosecha a la nube bajo una regla explícita.
- Conservar trazabilidad de los datos y evidencia reproducible de cada entrega.

## Fuera del alcance demostrado

Los objetivos anteriores pertenecen al diseño. El laboratorio disponible no probó KVM acelerado/EPT, procesamiento de imágenes reales, Cloud Bursting productivo, latencia de campo ni PUE medido. Esos elementos requieren una historia de usuario con entorno y evidencia antes de declararse completados.
