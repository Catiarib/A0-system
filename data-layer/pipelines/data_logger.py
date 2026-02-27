"""
A·0 Data Layer - Data Logger v0.1
Logs session metrics in real time via OSC
Stack: Python + OSC + PostgreSQL
BCN / 2026
"""

import psycopg2
import uuid
from datetime import datetime
from pythonosc import dispatcher, osc_server
import threading
import json
import logging
import os

# --- CONFIGURATION ---
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "a0_system"),
    "user": os.getenv("DB_USER", "a0_admin"),
    "password": os.getenv("DB_PASSWORD", ""),
    "port": os.getenv("DB_PORT", "5432")
}

OSC_IP = "0.0.0.0"       # Listen on all network interfaces
OSC_PORT = 8000           # Default OSC port for A·0 system

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


# --- DATABASE CONNECTION ---
def get_db_connection():
    """Establish and return a PostgreSQL database connection."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        logger.info("Database connection established")
        return conn
    except psycopg2.Error as e:
        logger.error(f"Database connection failed: {e}")
        raise


# --- SESSION MANAGEMENT ---
def create_session(project_id: str, venue_name: str, scene_version: str = "v0.1") -> str:
    """
    Creates a new session record in the database.
    Returns the generated session_id (UUID).
    """
    session_id = str(uuid.uuid4())
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO sessions (session_id, project_id, venue_name, scene_version)
                VALUES (%s, %s, %s, %s)
            """, (session_id, project_id, venue_name, scene_version))
            conn.commit()
            logger.info(f"Session created: {session_id} | Project: {project_id} | Venue: {venue_name}")
    except psycopg2.Error as e:
        conn.rollback()
        logger.error(f"Failed to create session: {e}")
        raise
    finally:
        conn.close()
    return session_id


def close_session(session_id: str, duration_min: int, notes: str = ""):
    """Closes a session by recording its total duration and optional notes."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE sessions
                SET duration_min = %s, notes = %s
                WHERE session_id = %s
            """, (duration_min, notes, session_id))
            conn.commit()
            logger.info(f"Session closed: {session_id} | Duration: {duration_min} min")
    except psycopg2.Error as e:
        conn.rollback()
        logger.error(f"Failed to close session: {e}")
    finally:
        conn.close()


# --- OSC HANDLERS ---
def handle_audience_metric(address, *args):
    """
    OSC handler: /audience/metric
    Expected args: session_id, zone_id, occupancy_count, dwell_time_sec, interaction (0/1)
    """
    if len(args) < 5:
        logger.warning(f"Insufficient arguments for audience metric: {args}")
        return

    session_id, zone_id, occupancy, dwell, interaction = args[0], args[1], args[2], args[3], bool(args[4])

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO audience_metrics
                    (session_id, timestamp, zone_id, occupancy_count, dwell_time_sec, interaction)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (session_id, datetime.now(), zone_id, occupancy, dwell, interaction))
            conn.commit()
            logger.debug(f"Metric logged | Zone: {zone_id} | Occupancy: {occupancy} | Dwell: {dwell}s")
    except psycopg2.Error as e:
        conn.rollback()
        logger.error(f"Failed to log audience metric: {e}")
    finally:
        conn.close()


def handle_system_event(address, *args):
    """
    OSC handler: /system/event
    Expected args: session_id, event_type, module_id, severity, description
    """
    if len(args) < 5:
        logger.warning(f"Insufficient arguments for system event: {args}")
        return

    session_id, event_type, module_id, severity, description = args[0], args[1], args[2], args[3], args[4]

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO system_events
                    (session_id, event_type, module_id, severity, description)
                VALUES (%s, %s, %s, %s, %s)
            """, (session_id, event_type, module_id, severity, description))
            conn.commit()
            logger.info(f"System event: [{severity.upper()}] {module_id} - {event_type}: {description}")
    except psycopg2.Error as e:
        conn.rollback()
        logger.error(f"Failed to log system event: {e}")
    finally:
        conn.close()


def handle_engagement_data(address, *args):
    """
    OSC handler: /engagement/biometric
    Expected args: session_id, zone_id, gsr_value, bpm_value, visitor_cohort
    """
    if len(args) < 5:
        logger.warning(f"Insufficient arguments for engagement data: {args}")
        return

    session_id, zone_id, gsr, bpm, cohort = args[0], args[1], args[2], args[3], args[4]

    # Calculate engagement score (weighted formula)
    # GSR contributes 60%, BPM deviation from resting (70 bpm) contributes 40%
    gsr_normalized = min(gsr / 10.0, 1.0) * 60          # Scale GSR to 0-60
    bpm_deviation = min(abs(bpm - 70) / 50.0, 1.0) * 40  # Scale BPM deviation to 0-40
    engagement_score = round(gsr_normalized + bpm_deviation, 2)

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO emotional_engagement
                    (session_id, zone_id, timestamp, gsr_value, bpm_value, engagement_score, visitor_cohort)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (session_id, zone_id, datetime.now(), gsr, bpm, engagement_score, cohort))
            conn.commit()
            logger.debug(f"Engagement logged | Zone: {zone_id} | Score: {engagement_score} | Cohort: {cohort}")
    except psycopg2.Error as e:
        conn.rollback()
        logger.error(f"Failed to log engagement data: {e}")
    finally:
        conn.close()


# --- OSC SERVER SETUP ---
def start_osc_server():
    """Configure and start the OSC server with all registered handlers."""
    d = dispatcher.Dispatcher()

    # Register OSC address handlers
    d.map("/audience/metric", handle_audience_metric)
    d.map("/system/event", handle_system_event)
    d.map("/engagement/biometric", handle_engagement_data)

    server = osc_server.ThreadingOSCUDPServer((OSC_IP, OSC_PORT), d)
    logger.info(f"A·0 OSC Logger listening on {OSC_IP}:{OSC_PORT}")

    # Run server in a daemon thread
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    return server


# --- ENTRY POINT ---
if __name__ == "__main__":
    logger.info("Starting A·0 Data Logger...")
    server = start_osc_server()

    # Example: create a test session on startup
    test_session_id = create_session(
        project_id="A0-BCN-001",
        venue_name="Pilot Venue - Barcelona",
        scene_version="v0.1-beta"
    )
    logger.info(f"Test session active: {test_session_id}")
    logger.info("Logger running. Press Ctrl+C to stop.")

    try:
        # Keep main thread alive
        while True:
            pass
    except KeyboardInterrupt:
        logger.info("A·0 Data Logger stopped.")
        close_session(test_session_id, duration_min=0, notes="Manual stop via KeyboardInterrupt")
