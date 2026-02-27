# A·0 — Arquitectura Tecnica

> System Book v0.1 | BCN | 2026

---

## Vision General

A·0 opera como un sistema operativo en tres capas:

```
[CAPA 1]  Motor Visual Modular    →  Los 10 Bloques Base
[CAPA 2]  Data Layer              →  Python + SQL + Power BI
[CAPA 3]  Dashboard & Reporting   →  Metricas en tiempo real
```

---

## Los 10 Bloques Modulares

### Bloque 1: Particle Flow Reactivo
- **Funcion**: Genera flujos de particulas cuyas posiciones se calculan desde GPU textures
- **Input**: Datos OSC / sensores de ocupacion
- **Output**: Visual en tiempo real
- **Stack**: TouchDesigner + GLSL shaders

### Bloque 2: Material OSC-Controlled
- **Funcion**: Modifica colores y texturas de materiales desde datos externos en tiempo real
- **Input**: Streams OSC con parametros de color (HSV/RGB)
- **Output**: Superficies reactivas al dato

### Bloque 3: Geometry Morphing
- **Funcion**: Transforma la geometria del espacio respondiendo a datos de ocupacion
- **Input**: Conteo de personas, zonas de densidad
- **Output**: Espacio visual que "respira" con la audiencia

### Bloque 4: Narrative Sequencer
- **Funcion**: Encadena escenas narrativas activadas por triggers de datos
- **Input**: Eventos de datos (hora, ocupacion, temperatura, interaccion)
- **Output**: Secuencia narrativa automatizada y versionada

### Bloque 5: Audience Heatmap Visual
- **Funcion**: Convierte datos de posicion y densidad de audiencia en mapa de calor visual
- **Input**: Datos de sensores de posicion / camara de profundidad
- **Output**: Visualizacion superpuesta al espacio

### Bloque 6: Audio Reactor
- **Funcion**: Analiza el audio del espacio y lo convierte en parametros visuales
- **Input**: Stream de audio en tiempo real
- **Output**: Parametros FFT que alimentan otros bloques

### Bloque 7: Light Gradient Engine
- **Funcion**: Controla gradientes de luz parametrizables via datos
- **Input**: Parametros de hora, ocupacion, temperatura emocional
- **Output**: Comandos DMX / Artnet para sistema de iluminacion

### Bloque 8: Scene Transition System
- **Funcion**: Gestiona las transiciones entre escenas versionadas
- **Input**: Triggers de datos o tiempo
- **Output**: Transicion visual fluida entre estados del sistema

### Bloque 9: Data Logger
- **Funcion**: Registra automaticamente todas las metricas de cada sesion
- **Input**: Outputs de todos los bloques + sensores
- **Output**: Dataset estructurado en SQL
- **Stack**: Python + SQLite / PostgreSQL

### Bloque 10: Dashboard Connector
- **Funcion**: Exporta datos del sistema a Power BI en tiempo real
- **Input**: Base de datos SQL del Data Logger
- **Output**: Dashboard actualizado en tiempo real
- **Stack**: Python + Power BI REST API

---

## Stack Tecnologico Completo

```
Capa Visual:
  - TouchDesigner (motor principal)
  - Unreal Engine 5 (proyectos de gran escala)
  - Three.js (deployments web/interactivos)
  - GLSL / HLSL (shaders custom)

Capa de Datos:
  - Python 3.x (ETL, procesamiento, API)
  - SQL / PostgreSQL (almacenamiento estructurado)
  - Power BI (visualizacion y reporting)
  - OSC Protocol (comunicacion en tiempo real)

Infraestructura:
  - GPU: NVIDIA RTX series (rendering en tiempo real)
  - Sensores: LiDAR / camara de profundidad (ocupacion)
  - Red: LAN de baja latencia para OSC
  - Audio: interfaz de audio profesional para Audio Reactor
```

---

## Principio de Modularidad

Cada bloque:
1. **Es independiente**: puede funcionar solo o en combinacion
2. **Tiene inputs/outputs definidos**: protocolo OSC estandarizado
3. **Es versionable**: cada mejora acumula valor de IP
4. **Es reutilizable**: el codigo de un proyecto se reutiliza en el siguiente

```
Proyecto A  →  Bloques 1, 3, 9, 10
Proyecto B  →  Bloques 1, 2, 4, 6, 9, 10
Proyecto C  →  Todos los bloques

Cada proyecto MEJORA los bloques. No los reinventa.
```

---

*A·0 / Architecture Doc v0.1 / BCN / 2026*
