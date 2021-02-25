# MQTT Client demo
# Continuously monitor two different MQTT topics for data,
# check if the received data matches two predefined 'commands'

import paho.mqtt.client as mqtt
import json, config,time,os,re
from json import JSONDecodeError

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

    def on_message_rpi(self, client, userdata, msg):
        message = json.loads(str(msg.payload.decode("utf-8")).replace('\'','"'))
        message = json.dumps(message)
        message = json.loads(message)

        if (message['destination'] == 'rpi'):
            # image recognition
            print('################### ' + message['content'])

            dupImage = 0
            imageID = message['content']
            x = int(config.position.split(',')[0])
            y = int(config.position.split(',')[1])

            if (config.orientation == "0"):
                x = x - 2
            elif (config.orientation == "90"):
                y = y + 2
            elif (config.orientation == "180"):
                x = x + 2
            elif (config.orientation == "270"):
                y = y - 2

            imageList = re.findall('(\d+,\d+,\d+)', config.imageString)

            for i in range(len(imageList)):
                if (imageList[i].split(',')[0] == imageID):
                    imageList[i] = imageID + "," + str(x) + "," + str(y)
                    dupImage = 1
            print("DEBUG DEBUG %%%%%%%%%%%%%%%%%: " + str(imageList))
            if (dupImage == 1):
                tmpString = "#im:"
                for item in imageList:
                    tmpString += "(" + item + ")"
                config.imageString = tmpString
            else:
                config.imageString += "(" + imageID + "," + str(x) + "," + str(y) + ")"

            self.btConnect.send(config.imageString)
            print("TIME(android): %s" % (time.strftime("%H: %M: %S",time.localtime())))
            if (config.curImage != imageID or config.curImage != ''):
                os.system("python collage_maker.py -o collage.png -f images -w 800 -i 400 -s")
                config.curImage = imageID


    def on_message_arduino(self, client, userdata, msg):
        message = str(msg.payload.decode("utf-8"))
        message = message.replace('\n','')
        self.pcConnect.send(message)
        print("TIME(pc): %s" % (time.strftime("%H: %M: %S",time.localtime())))

    def on_message_android(self, client, userdata, msg):
        message = json.loads(str(msg.payload.decode("utf-8")).replace('\'','"'))
        message = json.dumps(message)
        message = json.loads(message)


        if (message['destination'] == 'pc'):
            content = ''

            if (message['topic'] == 'exploration'):
                content = message['content']
                config.imageStart = 1

            elif (message['topic'] == 'waypoint'):
                content = 'waypoint ' + str(message['content'])

            elif (message['topic'] == 'beginFastest'):
                content = message['content']

            self.pcConnect.send(content)
            print("TIME(pc): %s" % (time.strftime("%H: %M: %S",time.localtime())))


    def on_message_pc(self, client, userdata, msg):
        counter = 1
        try:
            # 1 json msg
            message = json.loads(str(msg.payload.decode("utf-8")).replace('\'','"'))
            message = json.dumps(message)
            message = json.loads(message)
        except JSONDecodeError as e:
            # 2 json msg
            messageList = str(msg.payload.decode("utf-8")).replace('\'','"').split('\n')
            counter = len(messageList) - 1

        for i in range(counter):
            if (counter != 1):
                #message = json.dumps(messageList[i])
                message = json.loads(messageList[i])

            #print('debug: ' + str(messageList))
            #print('debug: ' + str(message))

            if (message['destination'] == 'android'):
                content = ''

                if (message['topic'] == 'update after movement'):
                    content = '#grid:' + message['content']['map'] + ',' + message['content']['position'][1:-1] + ',' + message['content']['orientation']
                    config.position = message['content']['position'][1:-1]
                    config.orientation = message['content']['orientation']
                    print(config.orientation)
                    self.btConnect.send(content)
                    print("TIME(android): %s" % (time.strftime("%H: %M: %S",time.localtime())))

                elif (message['topic'] == 'exploration done'):
                    content = message['content']
                    self.btConnect.send(content)
                    os.system("python collage_maker.py -o collage.png -f images -w 800 -i 400 -s")
                    print("TIME(android): %s" % (time.strftime("%H: %M: %S",time.localtime())))

            elif (message['destination'] == 'arduino'):
                movement = ''
                content = message['content']

                if (message['topic'] == 'calibrate'):
                    content = 'S'
                    if (message['content'] == 'C' or message['content'] == 'U'):
                       content = message['content']
                    self.sConnect.send(content + '@')
                    print("TIME(arduino): %s" % (time.strftime("%H: %M: %S",time.localtime())))

                elif (message['topic'] == 'exploration move'):
                    if (len(content) > 1):
                        movement = content[0].upper()*int(content[1:])
                    else:
                        movement = message['content'].upper()
                    self.sConnect.send(movement + '@')
                    print("TIME(arduino): %s" % (time.strftime("%H: %M: %S",time.localtime())))

                elif (message['topic'] == 'beginFastest'):
                    #for item in content:
                    #    if (item == 'l' or item == 'L'):
                    #        movement += 'L'
                    #    elif (item == 'r' or item == 'R'):
                    #        movement += 'R'
                    #    elif (len(item) > 1):
                    #        movement += item[0].upper()*int(item[1:])
                    movement = message['content'].upper()
                    self.sConnect.send(movement + '@')
                    print("TIME(arduino): %s" % (time.strftime("%H: %M: %S",time.localtime())))

                elif (message['topic'] == 'pull sensor'):
                    content = 'V'
                    self.sConnect.send(content + '@')
                    print("TIME(arduino): %s" % (time.strftime("%H: %M: %S",time.localtime())))


    def run(self):
        try:
            # Create an MQTT client and attach our routines to it.
            self.client = mqtt.Client()
            self.client.connect(self.hostname, 1883, 60)
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.subscribe("rpi")
            self.client.subscribe("arduino")
            self.client.subscribe("android")
            self.client.subscribe("pc")
            self.client.message_callback_add("rpi", self.on_message_rpi)
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


