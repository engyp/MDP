from bluetooth_server import BluetoothConnection
from socket_server import SocketConnection
from serial_server import SerialConnection
import sys, os, traceback, threading
import paho.mqtt.publish as publish
import mqtt_server,time
sys.path.append("/home/pi/.local/lib/python3.7/site-packages")
sys.path.append("/home/pi")
sys.path.append("/home/pi/MDP/tflite1")
import cv2
import TFLite_detection_webcam

def bluetooth_loop(mqttServer):
	while True:
		try:
			mqttServer.btConnect = BluetoothConnection()
			mqttServer.btConnect.disconnect()
			mqttServer.btConnect.connect()
			while True:
				data = mqttServer.btConnect.receive()
				if data is None: break
				if data != '':
					#print("received %s from android %s" % (data,time.strftime("%H: %M: %S",time.localtime())))
					print("received %s from android" % data)
				#mqttServer.btConnect.send("\nreply back from rpi")
				publish.single("android", data, hostname="192.168.30.1")
			mqttServer.btConnect.disconnect()

		except KeyboardInterrupt:
			mqttServer.btConnect.disconnect()
			
		except Exception:
			print("Main exec - Bluetooth connection error: ")
			traceback.print_exc(limit=10, file=sys.stdout)

def pc_loop(mqttServer):
	while True:
		try:
			mqttServer.pcConnect = SocketConnection()
			mqttServer.pcConnect.disconnect()
			mqttServer.pcConnect.connect()
			while True:
				data = mqttServer.pcConnect.receive()
				if data == 'quit': break
				if data != '':
					#print("received %s from pc %s" % (data,time.strftime("%H: %M: %S",time.localtime())))
					print("received %s from pc" % data)
				publish.single("pc", data, hostname="192.168.30.1")
			mqttServer.pcConnect.disconnect()

		except KeyboardInterrupt:
			mqttServer.pcConnect.disconnect()

		except Exception:
			print("Main exec - Socket connection error: ")
			traceback.print_exc(limit=10, file=sys.stdout)

def arduino_loop(mqttServer):
#	while True:
		try:
			mqttServer.sConnect = SerialConnection()
			mqttServer.sConnect.disconnect()
			mqttServer.sConnect.connect()
			while True:
				data = mqttServer.sConnect.receive()
				if data is None: break
				if data != '':
					#print("received %s from arduino %s" % (data,time.strftime("%H: %M: %S",time.localtime())))
					print("received %s from arduino" % data)
				publish.single("arduino", data, hostname="192.168.30.1")
			mqttServer.sConnect.disconnect()

		except KeyboardInterrupt:
			mqttServer.sConnect.disconnect()

		except Exception:
			print("Main exec - Serial connection error: ")
			traceback.print_exc(limit=10, file=sys.stdout)


mqttServer = mqtt_server.MqttServer()
#ir = TFLite_detection_webcam.image

sThread = threading.Thread(target=arduino_loop, args=((mqttServer,)), name = 'Arduino Thread')
sThread.setDaemon(True)
sThread.start()

btThread = threading.Thread(target=bluetooth_loop, args=((mqttServer,)), name = 'Bluetooth Thread')
btThread.setDaemon(True)
btThread.start()

pcThread = threading.Thread(target=pc_loop, args=((mqttServer,)), name = 'PC Thread')
pcThread.setDaemon(True)
pcThread.start()

irThread = threading.Thread(target=TFLite_detection_webcam.run)
irThread.setDaemon(True)
irThread.start()

mqttThread = threading.Thread(target=mqttServer.run())
mqttThread.setDaemon(True)
mqttThread.start()


while True:
	sThread.join(0.1)
	btThread.join(0.1)
	pcThread.join(0.1)
	irThread.join(0.1)
	mqttThread.join(0.1)
	if not sThread.isAlive():
		break
	if not btThread.isAlive():
		break
	if not pcThread.isAlive():
		break
	if not irThread.isAlive():
                break
	if not mqttThread.isAlive():
		break
