import paho.mqtt.client as mqtt


data = []

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("/topic/qos0")


def on_message(client, userdata, msg):
    try:
        data.append([float(x) for x in msg.payload.decode("utf-8").strip().split()])
        print(data)
    except ValueError:
        print("ERROR")


def connect_mqtt():
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.connect("mqtt.eclipseprojects.io", 1883, 60)
    mqttc.loop_start()


def get_data():
    return data
