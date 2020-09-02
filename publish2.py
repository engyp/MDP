# MQTT Publish Demo
# Publish two messages, to two different topics

import paho.mqtt.publish as publish

publish.single("rpi/arduino", "arduino sent msg", hostname="192.168.30.1")
print("Done")