# MQTT Publish Demo
# Publish two messages, to two different topics

import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import mqtt_server


def on_message(client, userdata, msg):
    print(msg.topic+": "+str(msg.payload.decode("utf-8")))

    if msg.payload == "android sent msg":
        print("Received message #1, do something")
        # Do something
        msg = msg.payload + " - new text !"


    if msg.payload == "test2":
        print("Received message #2, do something else")
        # Do something else


publish.single("rpi/android", "android sent msg", hostname="192.168.30.1")
print("Done")
