# A·0 — Technical Architecture

> System Book v0.1 | BCN | 2026

---

## General Vision

A·0 operates as an operating system in three integrated layers:

```
[LAYER 1]  Modular Visual Engine    →  The 10 Base Blocks
[LAYER 2]  Data Layer               →  Python + SQL + Power BI
[LAYER 3]  Dashboard & Reporting    →  Real-time metrics
```

---

## The 10 Modular Blocks

### Block 1: Reactive Particle Flow
- **Function:** Generates particle flows whose positions are calculated from GPU textures
- **Input:** OSC data / occupancy sensors
- **Output:** Visual in real time
- **Stack:** TouchDesigner + GLSL shaders

### Block 2: Generative Projection Mapping
- **Function:** Dynamic 3D mapping adapted to irregular surfaces
- **Input:** Architectural geometry + real-time triggers
- **Output:** Precisely calibrated projection
- **Stack:** TouchDesigner + Resolume + MadMapper

### Block 3: Spatial Audio Reactive
- **Function:** Multi-channel audio that responds to visitor movement
- **Input:** Tracking data (position + velocity)
- **Output:** 3D immersive soundscape
- **Stack:** Max/MSP + Ableton Live + spatial audio API

### Block 4: Biometric Emotional Capture
- **Function:** Real-time measurement of emotional response
- **Input:** Wristbands (GSR/BPM) + optional facial analysis
- **Output:** Structured emotional dataset
- **Stack:** Python (biometric API) + SQL

### Block 5: Visitor Flow Tracking
- **Function:** Spatial mapping of visitor movement
- **Input:** Infrared cameras + floor sensors
- **Output:** Heatmaps + dwell time per zone
- **Stack:** OpenCV + Python + PostgreSQL

### Block 6: Dynamic LED Control
- **Function:** Architectural lighting responsive to events
- **Input:** OSC triggers + sensor data
- **Output:** Synchronized lighting atmosphere
- **Stack:** ENTTEC DMX + Resolume + Python control

### Block 7: Interactive Surface
- **Function:** Touch or gesture-responsive projection surfaces
- **Input:** Leap Motion / depth cameras
- **Output:** Interactive visual response
- **Stack:** TouchDesigner + Unity (optional)

### Block 8: Brand Narrative Engine
- **Function:** Visual storytelling system linked to brand identity
- **Input:** Brand assets + narrative script
- **Output:** Coherent multi-screen visual sequence
- **Stack:** After Effects + TouchDesigner + custom templates

### Block 9: Real-Time Analytics Dashboard
- **Function:** Live visualization of all experience KPIs
- **Input:** All sensor + tracking data streams
- **Output:** Power BI dashboard (public + internal)
- **Stack:** Python ETL + SQL + Power BI streaming

### Block 10: Replication Protocol
- **Function:** Complete documentation for deploying the experience in new locations
- **Input:** System Book v1 + module configurations
- **Output:** Operational guide + calibration files
- **Stack:** Markdown docs + Git versioning

---

## Data Layer Architecture

### Data Flow

```
SENSORS / INPUTS
      |
      v
[Python Collector] ——> Raw data ingestion
      |
      v
[ETL Pipeline] ————> Cleaning + transformation
      |
      v
[PostgreSQL DB] ————> Structured storage
      |
      v
[Power BI] ——————> Dashboards + reports
      |
      v
[REST API] ——————> Client delivery
```

### Main Database Schema

```sql
-- Core session table
CREATE TABLE sessions (
  session_id    UUID PRIMARY KEY,
  project_name  VARCHAR(100),
  location      VARCHAR(100),
  start_time    TIMESTAMP,
  end_time      TIMESTAMP,
  total_visitors INT
);

-- Visitor tracking table  
CREATE TABLE visitor_events (
  event_id      UUID PRIMARY KEY,
  session_id    UUID REFERENCES sessions(session_id),
  zone_id       VARCHAR(50),
  entry_time    TIMESTAMP,
  exit_time     TIMESTAMP,
  dwell_seconds INT
);

-- Emotional engagement table
CREATE TABLE emotional_data (
  record_id     UUID PRIMARY KEY,
  session_id    UUID REFERENCES sessions(session_id),
  zone_id       VARCHAR(50),
  timestamp     TIMESTAMP,
  gsr_value     FLOAT,
  bpm_value     FLOAT,
  engagement_score FLOAT
);
```

---

## Technical Stack Summary

| Layer | Technology | Purpose |
|-------|------------|---------|
| Visual Engine | TouchDesigner, Resolume, Unity | Real-time rendering |
| Audio | Max/MSP, Ableton, IRCAM spat | Spatial sound |
| Tracking | OpenCV, Depth cameras, IR | Visitor movement |
| Data Collection | Python 3.11+ | ETL pipelines |
| Database | PostgreSQL | Structured storage |
| Analytics | Power BI, SQL | Reporting + KPIs |
| Version Control | Git + GitHub | System documentation |
| API | FastAPI + REST | Client data delivery |

---

## Deployment Model

### On-Site Setup
- Dedicated local server (minimum: 32GB RAM, RTX 4080)
- Local network for sensor communication
- Redundant systems for critical projections

### Remote Monitoring
- VPN access for real-time dashboard
- Automated alerts for system failures
- Nightly data sync to cloud (AWS / Azure)

### Client Delivery
- Power BI embedded dashboard (client access)
- PDF automated report post-experience
- Raw data export (CSV / JSON) on request

---

## Security & Privacy

- All biometric data anonymized at collection point
- GDPR compliant data handling
- No facial recognition data stored
- Visitor consent via on-site signage
- Data retention: 12 months maximum

---

*A·0 Technical Architecture — System Book v0.1 — Barcelona, 2026*
