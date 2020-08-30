# MQTT Publish Demo
# Publish two messages, to two different topics

import paho.mqtt.publish as publish

publish.single("arduino topic", "test1", hostname="test.mosquitto.org")
print("Done")
