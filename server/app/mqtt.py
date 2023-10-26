from flask_mqtt import Mqtt

mqtt = None
messages = []

def set_mqtt_configuration(app):
    app.config['MQTT_BROKER_URL'] = 'localhost'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = ''
    app.config['MQTT_PASSWORD'] = ''
    app.config['MQTT_KEEPALIVE'] = 120
    app.config['MQTT_TLS_ENABLED'] = False


def init_mqtt(app):
    global mqtt
    if mqtt is not None:
        return

    mqtt = Mqtt(app)

    # SAMPLE CODE - REMOVE!
    @mqtt.on_connect()
    def handle_connect(client, userdata, flags, rc):
        mqtt.subscribe('my_topic')

    @mqtt.on_message()
    def handle_mqtt_message(client, userdata, message):
        topic = message.topic
        payload = message.payload.decode()
        print(f"Received {payload} from {topic}")
        messages.append(payload)