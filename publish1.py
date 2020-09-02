# MQTT Publish Demo
# Publish two messages, to two different topics

import paho.mqtt.publish as publish

publish.single("rpi/android", "android sent msg", hostname="192.168.30.1")
print("Done")
