# MQTT Client demo
# Continuously monitor two different MQTT topics for data,
# check if the received data matches two predefined 'commands'
 
import paho.mqtt.client as mqtt

class MqttServer(): 

    def __init__(self, hostname="192.168.30.1"):
        self.hostname = hostname
        self.btConnect = None
        self.pcConnect = None
        self.sConnect = None
        self.client = None


    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("\nMqtt Server connected with result code "+str(rc))
     
    def on_message(self, client, userdata, msg):
        print(msg.topic+": "+str(msg.payload.decode("utf-8")))

    def on_message_arduino(self, client, userdata, msg):
        message = str(msg.payload.decode("utf-8"))
        if message.split(",")[0] == "arduino":
            print("arduino" + message)
            self.sConnect.send(message.split(",")[1])

    def on_message_android(self, client, userdata, msg):
        message = str(msg.payload.decode("utf-8"))
        if message.split(",")[0] == "android":
            print("android" + message)
            self.btConnect.send(message.split(",")[1])

    def on_message_pc(self, client, userdata, msg):
        message = str(msg.payload.decode("utf-8"))
        if message.split(",")[0] == "pc":
            print("pc"+ message)
            self.pcConnect.send(message.split(",")[1])

    def run(self):
        try:
            # Create an MQTT client and attach our routines to it.
            self.client = mqtt.Client()
            self.client.connect(self.hostname, 1883, 60)
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.subscribe("arduino")
            self.client.subscribe("android")
            self.client.subscribe("pc")
            self.client.message_callback_add("arduino", self.on_message_arduino)
            self.client.message_callback_add("android", self.on_message_android)
            self.client.message_callback_add("pc", self.on_message_pc)
             
            
             
            # Process network traffic and dispatch callbacks. This will also handle
            # reconnecting. Check the documentation at
            # https://github.com/eclipse/paho.mqtt.python
            # for information on how to use other loop*() functions
            self.client.loop_forever()

        except KeyboardInterrupt:
            self.client.loop_stop()
            self.client.disconnect()
            