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
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
     
        # Subscribing in on_connect() - if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.client.subscribe("rpi/arduino")
        self.client.subscribe("rpi/android")
     
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
        print("oi")
        if message.split(",")[0] == "android":
            print("hi")
            self.pcConnect.send(message.split(",")[1])

    def run(self):
        try:
            # Create an MQTT client and attach our routines to it.
            self.client = mqtt.Client()
            self.client.connect(self.hostname, 1883, 60)
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message

            self.client.message_callback_add("rpi/android", self.on_message_android)
             
            
             
            # Process network traffic and dispatch callbacks. This will also handle
            # reconnecting. Check the documentation at
            # https://github.com/eclipse/paho.mqtt.python
            # for information on how to use other loop*() functions
            self.client.loop_forever()

        except KeyboardInterrupt:
            self.client.loop_stop()
            self.client.disconnect()
            