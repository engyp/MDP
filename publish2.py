# MQTT Publish Demo
# Publish two messages, to two different topics

import paho.mqtt.publish as publish

publish.single("android topic", "android sent msg", hostname="test.mosquitto.org")
print("Done")