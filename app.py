from flask import Flask, render_template, jsonify
import paho.mqtt.client as mqtt

app = Flask(__name__)

mqtt_broker = "172.20.49.30"  # MQTT-Broker-Adresse
mqtt_topic = "esp32/temperature"  # MQTT-Topic für die Temperatur

def on_message(client, userdata, message):
    global current_temperature
    current_temperature = message.payload.decode()

mqtt_client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="espServer")
# mqtt_client.on_message = on_message
# mqtt_client.connect(mqtt_broker)
# mqtt_client.subscribe(mqtt_topic)
# mqtt_client.loop_start()

current_temperature = "N/A"

def connect_to_mqtt_broker():
    mqtt_client.connect(mqtt_broker)
    mqtt_client.subscribe(mqtt_topic)

def read_temperature():
    mqtt_client.loop(timeout=1.0)

    # Check if there's a new message
    if mqtt_client._messages_recd > 0:
        # Get the last message
        message = mqtt_client._in_messages.pop()
        return message.payload.decode()
    
@app.route('/')
def index():
    return render_template('index.html', temperature=current_temperature)

@app.route('/get_temperature')
def get_temperature():
    global current_temperature
    connect_to_mqtt_broker()
    current_temperature = read_temperature()
    return jsonify(temperature=current_temperature)

if __name__ == '__main__':
    app.run(debug=True)
