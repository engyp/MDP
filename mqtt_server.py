# MQTT Client demo
# Continuously monitor two different MQTT topics for data,
# check if the received data matches two predefined 'commands'
 
import paho.mqtt.client as mqtt
from bluetooth_server import BluetoothConnection
from socket_server import SocketConnection
from serial_server import SerialConnection

btConnect = BluetoothConnection()
pcConnect = SocketConnection()
sConnect = SerialConnection()
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("rpi/arduino")
    client.subscribe("rpi/android")
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+": "+str(msg.payload.decode("utf-8")))

    if msg.payload == "test1":
        print("Received message #1, do something")
        # Do something


    if msg.payload == "test2":
        print("Received message #2, do something else")
        # Do something else

def on_message_android(client, userdata, msg):
    message = str(msg.payload.decode("utf-8"))
    print("\n" + message.split(",")[0])
    print("\n" + message.split(",")[1])
    if message.split(",")[0] == "android":
        pcConnect.send(message.split(",")[1])

def run():
    try:
        # Create an MQTT client and attach our routines to it.
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.message_callback_add("rpi/android", on_message_android)
         
        client.connect("192.168.30.1", 1883, 60)
         
        # Process network traffic and dispatch callbacks. This will also handle
        # reconnecting. Check the documentation at
        # https://github.com/eclipse/paho.mqtt.python
        # for information on how to use other loop*() functions
        client.loop_forever()

    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()
        