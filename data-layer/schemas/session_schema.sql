-- A·0 Data Layer
-- Session Schema v0.1
-- Database schema for session and experience tracking

-- ============================================================
-- CORE TABLES
-- ============================================================

-- Main sessions table
CREATE TABLE sessions (
    session_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id      VARCHAR(50) NOT NULL,
    venue_name      VARCHAR(100),
    session_date    TIMESTAMP NOT NULL DEFAULT NOW(),
    duration_min    INTEGER,                    -- Total duration in minutes
    scene_version   VARCHAR(20),                -- Version of the experience deployed
    notes           TEXT                        -- Optional operational notes
);

-- Audience metrics per session
CREATE TABLE audience_metrics (
    metric_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      UUID REFERENCES sessions(session_id),
    timestamp       TIMESTAMP NOT NULL,
    zone_id         VARCHAR(20),                -- Space zone (A, B, C...)
    occupancy_count INTEGER,                    -- Number of people in that zone
    dwell_time_sec  INTEGER,                    -- Time spent in zone (seconds)
    interaction     BOOLEAN DEFAULT FALSE       -- Whether interaction was triggered
);

-- System events table
CREATE TABLE system_events (
    event_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      UUID REFERENCES sessions(session_id),
    event_time      TIMESTAMP NOT NULL DEFAULT NOW(),
    event_type      VARCHAR(50),                -- Type: trigger, error, transition
    module_id       VARCHAR(20),                -- Which module generated the event
    severity        VARCHAR(10) DEFAULT 'info', -- info, warning, error
    description     TEXT                        -- Human-readable event description
);

-- ============================================================
-- ENGAGEMENT TABLES
-- ============================================================

-- Emotional engagement data (biometric capture)
CREATE TABLE emotional_engagement (
    record_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      UUID REFERENCES sessions(session_id),
    zone_id         VARCHAR(20),
    timestamp       TIMESTAMP NOT NULL,
    gsr_value       FLOAT,                      -- Galvanic skin response (arousal)
    bpm_value       FLOAT,                      -- Heart rate (beats per minute)
    engagement_score FLOAT,                     -- Calculated 0-100 engagement index
    visitor_cohort  VARCHAR(10)                 -- Anonymous group ID (no PII stored)
);

-- Content performance per zone
CREATE TABLE content_performance (
    perf_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      UUID REFERENCES sessions(session_id),
    module_id       VARCHAR(20),                -- M01, M02... M10
    zone_id         VARCHAR(20),
    start_time      TIMESTAMP,
    end_time        TIMESTAMP,
    avg_occupancy   FLOAT,                      -- Average visitors during content
    peak_occupancy  INTEGER,                    -- Maximum visitors at any point
    interaction_rate FLOAT                      -- % of visitors who interacted
);

-- ============================================================
-- REPORTING VIEWS
-- ============================================================

-- Session summary view (used by Power BI dashboard)
CREATE OR REPLACE VIEW session_summary AS
SELECT
    s.session_id,
    s.project_id,
    s.venue_name,
    s.session_date,
    s.duration_min,
    COUNT(DISTINCT am.zone_id)          AS zones_active,
    SUM(am.occupancy_count)             AS total_visitor_touches,
    AVG(ee.engagement_score)            AS avg_engagement_score,
    MAX(ee.engagement_score)            AS peak_engagement_score
FROM sessions s
LEFT JOIN audience_metrics am ON s.session_id = am.session_id
LEFT JOIN emotional_engagement ee ON s.session_id = ee.session_id
GROUP BY s.session_id, s.project_id, s.venue_name, s.session_date, s.duration_min;

-- Zone performance view
CREATE OR REPLACE VIEW zone_performance AS
SELECT
    am.session_id,
    am.zone_id,
    AVG(am.dwell_time_sec)              AS avg_dwell_seconds,
    MAX(am.occupancy_count)             AS peak_occupancy,
    SUM(CASE WHEN am.interaction THEN 1 ELSE 0 END) AS total_interactions,
    AVG(ee.engagement_score)            AS avg_engagement
FROM audience_metrics am
LEFT JOIN emotional_engagement ee
    ON am.session_id = ee.session_id AND am.zone_id = ee.zone_id
GROUP BY am.session_id, am.zone_id;

-- ============================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================

CREATE INDEX idx_sessions_project ON sessions(project_id);
CREATE INDEX idx_metrics_session ON audience_metrics(session_id);
CREATE INDEX idx_metrics_zone ON audience_metrics(zone_id);
CREATE INDEX idx_engagement_session ON emotional_engagement(session_id);
CREATE INDEX idx_events_session ON system_events(session_id);
CREATE INDEX idx_events_type ON system_events(event_type);

-- ============================================================
-- A·0 Data Layer -- session_schema.sql -- v0.1 -- Barcelona 2026
-- ============================================================
