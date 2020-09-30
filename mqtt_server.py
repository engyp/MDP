# MQTT Client demo
# Continuously monitor two different MQTT topics for data,
# check if the received data matches two predefined 'commands'
 
import paho.mqtt.client as mqtt
import json

class MqttServer(): 


    def __init__(self, hostname="192.168.30.1"):
        self.hostname = hostname
        self.btConnect = None
        self.pcConnect = None
        self.sConnect = None
        self.client = None
        self.waypoint = None

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("\nMqtt Server connected with result code "+str(rc))
     

    def on_message(self, client, userdata, msg):
        print(msg.topic+": "+str(msg.payload.decode("utf-8")))


    def on_message_arduino(self, client, userdata, msg):
        message = str(msg.payload.decode("utf-8"))

        self.pcConnect.send(message)

    def on_message_android(self, client, userdata, msg):
        message = json.loads(str(msg.payload.decode("utf-8")).replace('\'','"'))
        message = json.dumps(message)
        message = json.loads(message)

        if (message['destination'] == 'android'):
            self.btConnect.send(json.dumps(message))

        elif (message['destination'] == 'arduino'):
            self.sConnect.send(json.dumps(message))

        elif (message['destination'] == 'pc'):
            content = ''
	    
            if (message['topic'] == 'exploration'):
                content = message['content']

            elif (message['topic'] == 'waypoint'):
                self.waypoint = message['content']

            elif (message['topic'] == 'beginFastest'):
                content += message['content'] + ','
 			
                if (self.waypoint != None):		    
                    content += str(self.waypoint)


            if (message['topic'] != 'waypoint'):
                self.pcConnect.send(content)


    def on_message_pc(self, client, userdata, msg):
        message = json.loads(str(msg.payload.decode("utf-8")).replace('\'','"'))
        message = json.dumps(message)
        message = json.loads(message)

        if (message['destination'] == 'android'):
            content = ''

            if (message['topic'] == 'update after movement'):
                # print('hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
                # content = '#robotPosition:' + message['content']['position'][1:-1] + ',' + message['content']['orientation']
                # print('@@@@@@@@@@@@@' + content)
                # self.btConnect.send(content)

                content = '#grid:' + '\"' + message['content']['map'] + '\"'
                # print('@@@@@@@@@@@@@' + content)
                self.btConnect.send(content)

        elif (message['destination'] == 'arduino'):
            movement = ''
            content = message['content']

            if (message['topic'] == 'exploration move'):
                if (len(content) > 1):
                    movement = content[0].upper()*int(content[1:])
                    # simulation
                    # movement = 'movement done'
                    # self.pcConnect.send(str(movement))
                else:
                    movement = message['content'].upper()

            elif (message['topic'] == 'beginFastest'):
                for item in content:
                    if (item == 'l' or item == 'L'):
                        movement += 'L'
                    elif (item == 'r' or item == 'R'):
                        movement += 'R'
                    elif (len(item) > 1):
                        movement += item[0].upper()*int(item[1:])

    	    elif (message['topic'] == 'pull sensor'):
                content = 'V'
                self.sConnect.send(content)

                # simulation
                # content = [3,3,3,3,3,3]
                # self.pcConnect.send(str(content))

            self.sConnect.send(movement)

        elif (message['destination'] == 'pc'):
            self.pcConnect.send(json.dumps(message))


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
            
