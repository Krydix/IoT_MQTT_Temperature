import paho.mqtt.client as mqtt
import sqlite3
import datetime

# Datenbankverbindung einrichten
conn = sqlite3.connect('temperature_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS temperature
             (date text, temp real)''')
conn.commit()

# MQTT Callbacks
def on_connect(client, userdata, flags, rc, propperties=None):
    print("Connected with result code "+str(rc))
    client.subscribe("esp32/temperature")

def on_message(client, userdata, msg):
    temp = float(msg.payload.decode())
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO temperature (date, temp) VALUES (?, ?)", (now, temp))
    conn.commit()

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="espServer")
client.on_connect = on_connect
client.on_message = on_message

client.connect("172.20.49.17", 1883, 60)

client.loop_forever()