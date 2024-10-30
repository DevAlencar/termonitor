import paho.mqtt.client as mqtt


broker_url = "a25833zo7tzuak-ats.iot.us-east-1.amazonaws.com"
broker_port = 8883  # Porta padrão para MQTTS

ca_cert = "./certs/AmazonRootCA1.pem"
client_cert = "./certs/7dfa0bf97df2046e0de3bef913fe95b39d0d098b0206d38515e0a9dd0cba24bf-certificate.pem.crt"
client_key = "./certs/7dfa0bf97df2046e0de3bef913fe95b39d0d098b0206d38515e0a9dd0cba24bf-private.pem.key"
data = []

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("temperatura")


def on_message(client, userdata, msg):
    try:
        data.append([float(x) for x in msg.payload.decode("utf-8").strip().split()])
    except ValueError:
        print("ERROR")


def connect_mqtt():
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.tls_set(ca_cert, certfile=client_cert, keyfile=client_key)
    mqttc.connect(broker_url, broker_port)
    mqttc.loop_start()


def get_data():
    return data

def clear_data():
    data.clear()
