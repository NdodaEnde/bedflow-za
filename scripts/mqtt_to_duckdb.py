#!/usr/bin/env python3
import os, json, time, duckdb, paho.mqtt.client as mqtt
from datetime import datetime, timezone

DB = "/data/bedflow.duckdb"

def get_conn():
    """Return a live DuckDB connection; reconnect if stale."""
    global _conn
    if '_conn' not in globals():
        _conn = duckdb.connect(DB)
        _conn.execute("""
            CREATE SCHEMA IF NOT EXISTS raw;
            CREATE TABLE IF NOT EXISTS raw.bed_events (
                bed_id TEXT,
                status TEXT,
                ts TIMESTAMP,
                raw_payload TEXT
            );
        """)
    try:
        _conn.execute("SELECT 1")  # ping
    except Exception:
        _conn = duckdb.connect(DB)  # reconnect
    return _conn

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ MQTT connected")
        client.subscribe("bedflow/+/status")
    else:
        print(f"🔴 MQTT connection failed, rc={rc}")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("⚠️ MQTT disconnected; auto-reconnecting…")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload)
        bed_id  = payload.get("bed_id") or msg.topic.split("/")[-2]
        status  = payload.get("status")
        ts_raw  = payload.get("timestamp")
        ts      = datetime.fromisoformat(ts_raw.replace('Z', '+00:00')) if ts_raw else datetime.now(timezone.utc)
        get_conn().execute(
            "INSERT INTO raw.bed_events(bed_id, status, ts, raw_payload) VALUES (?,?,?,?)",
            (bed_id, status, ts, msg.payload.decode())
        )
    except Exception as e:
        print("⚠️ ingest error:", e)

client = mqtt.Client()
client.on_connect    = on_connect
client.on_disconnect = on_disconnect
client.on_message    = on_message
client.connect("mosquitto", 1883, keepalive=60)
client.loop_forever()