import paho.mqtt.client as mqtt
import time

K0 = 25.0 
K1 = 50.0
TARGET_SENSOR_ID = "t1" 

def on_connect(client, userdata, flags, rc):
    print("Conectado con éxito")
    client.subscribe("temperature/#")

def on_message(client, userdata, msg):
    topic_parts = msg.topic.split('/')
    sensor_id = topic_parts[-1]
    data_type = topic_parts[0]

    print(f"Mensaje recibido: {msg.topic} - {msg.payload.decode()}")

    if data_type == "temperature" and sensor_id == TARGET_SENSOR_ID:
        temp = float(msg.payload.decode())
        print(f"Temperatura del sensor {sensor_id}: {temp}")

        if temp > K0:
            client.subscribe("humidity")
        else:
            client.unsubscribe("humidity")

    elif data_type == "humidity":
        humidity = float(msg.payload.decode())
        print(f"Humedad: {humidity}")

        if humidity > K1:
            client.unsubscribe("humidity")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("simba.fdi.ucm.es", 1883, 60)
client.loop_start()

while True:
    time.sleep(1)
