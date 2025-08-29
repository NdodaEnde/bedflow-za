#!/usr/bin/env python3
import os, duckdb, paho.mqtt.client as mqtt
DB = "/data/bedflow.duckdb"
con = duckdb.connect(DB)
con.execute("""
    CREATE SCHEMA IF NOT EXISTS raw;
    CREATE TABLE IF NOT EXISTS raw.bed_events (
        topic TEXT,
        payload TEXT,
        ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")
def on_msg(client, userdata, msg):
    con.execute(
        "INSERT INTO raw.bed_events(topic, payload) VALUES (?,?)",
        (msg.topic, msg.payload.decode())
    )
client = mqtt.Client()
client.on_message = on_msg
client.connect("mosquitto", 1883)
client.subscribe("bedflow/+/status")
client.loop_forever()
