import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Conectado con éxito")
    client.subscribe("numbers")

def on_message(client, userdata, msg):
    global message_count
    number = float(msg.payload.decode())
    if number.is_integer():
        print(f"Entero: {int(number)}")
    else:
        print(f"Real: {number}")
    message_count += 1

message_count = 0

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("simba.fdi.ucm.es", 1883, 60)

client.loop_forever()
