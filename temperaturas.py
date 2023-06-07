import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Conectado con éxito")
    client.subscribe("temperature/#")

def on_message(client, userdata, msg):
    global sensor_data
    sensor_id = msg.topic.split('/')[-1]
    temperature = float(msg.payload.decode())

    if sensor_id not in sensor_data:
        sensor_data[sensor_id] = []
    sensor_data[sensor_id].append(temperature)

def process_sensor_data(sensor_data):
    all_temperatures = []
    for sensor_id, temperatures in sensor_data.items():
        min_temp = min(temperatures)
        max_temp = max(temperatures)
        avg_temp = sum(temperatures) / len(temperatures)
        print(f"Sensor {sensor_id}: Min: {min_temp}, Max: {max_temp}, Avg: {avg_temp}")
        all_temperatures.extend(temperatures)

    if all_temperatures:
        min_temp = min(all_temperatures)
        max_temp = max(all_temperatures)
        avg_temp = sum(all_temperatures) / len(all_temperatures)
        print(f"Todos los sensores: Min: {min_temp}, Max: {max_temp}, Avg: {avg_temp}")

sensor_data = {}

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("simba.fdi.ucm.es", 1883, 60)
client.loop_start()

interval = 6 

while True:
    time.sleep(interval)
    print("\nProcesando datos de sensores...")
    process_sensor_data(sensor_data)
    sensor_data = {}  # Reinicia los datos del sensor para el siguiente intervalo
