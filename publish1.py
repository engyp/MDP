# MQTT Publish Demo
# Publish two messages, to two different topics

import paho.mqtt.publish as publish

publish.single("arduino topic", "arduino sent msg", hostname="test.mosquitto.org")
print("Done")