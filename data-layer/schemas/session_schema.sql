-- A·0 Data Layer
-- Session Schema v0.1
-- Esquema de base de datos para el registro de sesiones

-- Tabla principal de sesiones
CREATE TABLE sessions (
    session_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id      VARCHAR(50) NOT NULL,
    venue_name      VARCHAR(100),
    session_date    TIMESTAMP NOT NULL DEFAULT NOW(),
    duration_min    INTEGER,
    scene_version   VARCHAR(20),
    notes           TEXT
);

-- Tabla de metricas de audiencia por sesion
CREATE TABLE audience_metrics (
    metric_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      UUID REFERENCES sessions(session_id),
    timestamp       TIMESTAMP NOT NULL,
    zone_id         VARCHAR(20),        -- zona del espacio (A, B, C...)
    occupancy_count INTEGER,            -- personas en esa zona
    dwell_time_sec  INTEGER,            -- tiempo de permanencia
    interaction     BOOLEAN DEFAULT FALSE
);

-- Tabla de eventos del sistema
CREATE TABLE system_events (
    event_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      UUID REFERENCES sessions(session_id),
    timestamp       TIMESTAMP NOT NULL,
    block_id        INTEGER,            -- bloque modular que genera el evento (1-10)
    event_type      VARCHAR(50),        -- 'scene_change', 'peak_occupancy', 'audio_spike'
    event_value     FLOAT,              -- valor numerico del evento
    osc_address     VARCHAR(100)        -- direccion OSC del evento
);

-- Tabla de metricas de escenas
CREATE TABLE scene_metrics (
    scene_metric_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      UUID REFERENCES sessions(session_id),
    scene_name      VARCHAR(50),
    start_time      TIMESTAMP,
    end_time        TIMESTAMP,
    peak_occupancy  INTEGER,
    avg_occupancy   FLOAT,
    total_events    INTEGER
);

-- Vista resumen por sesion (para Power BI)
CREATE VIEW session_summary AS
SELECT
    s.session_id,
    s.project_id,
    s.venue_name,
    s.session_date,
    s.duration_min,
    s.scene_version,
    COUNT(DISTINCT am.zone_id) AS zones_tracked,
    MAX(am.occupancy_count) AS peak_occupancy,
    AVG(am.occupancy_count) AS avg_occupancy,
    AVG(am.dwell_time_sec) AS avg_dwell_time_sec,
    COUNT(DISTINCT se.event_id) AS total_events
FROM sessions s
LEFT JOIN audience_metrics am ON s.session_id = am.session_id
LEFT JOIN system_events se ON s.session_id = se.session_id
GROUP BY s.session_id, s.project_id, s.venue_name,
         s.session_date, s.duration_min, s.scene_version;

-- A·0 / Data Layer / Schema v0.1 / BCN / 2026
