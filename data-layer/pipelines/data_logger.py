"""
A·0 Data Layer - Data Logger v0.1
Registra metricas de sesiones en tiempo real via OSC
Stack: Python + OSC + PostgreSQL
BCN / 2026
"""

import psycopg2
import uuid
from datetime import datetime
from pythonosc import dispatcher, osc_server
import threading
import json
import os

# --- CONFIGURACION ---
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "a0_system"),
    "user": os.getenv("DB_USER", "a0_admin"),
    "password": os.getenv("DB_PASSWORD", ""),
    "port": os.getenv("DB_PORT", "5432")
}

OSC_IP = "0.0.0.0"
OSC_PORT = 8000


class A0DataLogger:
    """
    Logger principal del sistema A·0.
    Escucha mensajes OSC del motor visual y los persiste en SQL.
    """

    def __init__(self, project_id: str, venue_name: str, scene_version: str):
        self.project_id = project_id
        self.venue_name = venue_name
        self.scene_version = scene_version
        self.session_id = None
        self.conn = None
        self._connect_db()
        self._create_session()

    def _connect_db(self):
        """Conecta a la base de datos PostgreSQL."""
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            print(f"[A0] DB conectada: {DB_CONFIG['database']}")
        except Exception as e:
            print(f"[A0] ERROR DB: {e}")
            raise

    def _create_session(self):
        """Crea un registro de sesion al inicio."""
        self.session_id = str(uuid.uuid4())
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO sessions (session_id, project_id, venue_name,
                                  session_date, scene_version)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (self.session_id, self.project_id, self.venue_name,
             datetime.now(), self.scene_version)
        )
        self.conn.commit()
        cur.close()
        print(f"[A0] Sesion iniciada: {self.session_id}")

    def log_occupancy(self, zone_id: str, count: int, dwell_time: int = 0):
        """Registra dato de ocupacion por zona."""
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO audience_metrics
                (session_id, timestamp, zone_id, occupancy_count,
                 dwell_time_sec, interaction)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (self.session_id, datetime.now(), zone_id,
             count, dwell_time, count > 0)
        )
        self.conn.commit()
        cur.close()

    def log_event(self, block_id: int, event_type: str,
                  value: float, osc_address: str):
        """Registra un evento del sistema."""
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO system_events
                (session_id, timestamp, block_id, event_type,
                 event_value, osc_address)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (self.session_id, datetime.now(), block_id,
             event_type, value, osc_address)
        )
        self.conn.commit()
        cur.close()

    def close_session(self, duration_min: int):
        """Cierra la sesion con duracion total."""
        cur = self.conn.cursor()
        cur.execute(
            "UPDATE sessions SET duration_min = %s WHERE session_id = %s",
            (duration_min, self.session_id)
        )
        self.conn.commit()
        cur.close()
        if self.conn:
            self.conn.close()
        print(f"[A0] Sesion cerrada: {self.session_id} ({duration_min} min)")


# --- HANDLERS OSC ---

def handle_occupancy(unused_addr, zone_id, count, dwell_time=0):
    """Recibe: /a0/occupancy <zone_id> <count> [dwell_time]"""
    if logger:
        logger.log_occupancy(zone_id, int(count), int(dwell_time))
        print(f"[OSC] Zona {zone_id}: {count} personas")


def handle_event(unused_addr, block_id, event_type, value):
    """Recibe: /a0/event <block_id> <event_type> <value>"""
    if logger:
        logger.log_event(int(block_id), event_type,
                         float(value), unused_addr)
        print(f"[OSC] Bloque {block_id} | {event_type}: {value}")


# --- MAIN ---

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="A·0 Data Logger")
    parser.add_argument("--project", default="A0-BCN-001")
    parser.add_argument("--venue", default="Venue Test")
    parser.add_argument("--scene-version", default="v0.1")
    args = parser.parse_args()

    logger = A0DataLogger(
        project_id=args.project,
        venue_name=args.venue,
        scene_version=args.scene_version
    )

    # Configurar dispatcher OSC
    disp = dispatcher.Dispatcher()
    disp.map("/a0/occupancy", handle_occupancy)
    disp.map("/a0/event", handle_event)

    # Iniciar servidor OSC
    server = osc_server.ThreadingOSCUDPServer((OSC_IP, OSC_PORT), disp)
    print(f"[A0] Data Logger activo en {OSC_IP}:{OSC_PORT}")
    print(f"[A0] Proyecto: {args.project} | Venue: {args.venue}")
    print("[A0] Esperando datos OSC... (Ctrl+C para detener)")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        start = datetime.now()
        duration = int((datetime.now() - start).seconds / 60)
        logger.close_session(duration)
        print("\n[A0] Data Logger detenido.")
