from bluetooth_server import BluetoothConnection
from socket_server import SocketConnection
from serial_server import SerialConnection
import sys, traceback, threading
import paho.mqtt.publish as publish
import mqtt_server

def __init__(self):
        self.btConnect = None
        self.pcConnect = None
        self.sConnect = None

def bluetooth_loop(mqttServer, self):
	#while True:
		try:
			self.mqttServer.btConnect = BluetoothConnection()
			self.mqttServer.btConnect.disconnect()
			self.mqttServer.btConnect.connect()
			while True:
				data = self.mqttServer.btConnect.receive()
				if data is None: break
				print("received [%s] from android" % data)
				#mqttServer.btConnect.send("\nreply back from rpi")
				publish.single("android", data, hostname="192.168.30.1")
			self.mqttServer.btConnect.disconnect()

		except KeyboardInterrupt:
			self.mqttServer.btConnect.disconnect()
			
		except Exception:
			print("Main exec - Bluetooth connection error: ")
			traceback.print_exc(limit=10, file=sys.stdout)

def pc_loop(mqttServer, self):
	#while True:
		try:
			self.mqttServer.pcConnect = SocketConnection()
			self.mqttServer.pcConnect.disconnect()
			self.mqttServer.pcConnect.connect()
			while True:
				data = self.mqttServer.pcConnect.receive()
				if data == 'quit': break
				print("received [%s] from PC" % data)
				publish.single("pc", data, hostname="192.168.30.1")
			self.mqttServer.pcConnect.disconnect()

		except KeyboardInterrupt:
			self.mqttServer.pcConnect.disconnect()

		except Exception:
			print("Main exec - Socket connection error: ")
			traceback.print_exc(limit=10, file=sys.stdout)

def arduino_loop(mqttServer, self):
	#while True:
		try:
			self.mqttServer.sConnect = SerialConnection()
			self.mqttServer.sConnect.disconnect()
			self.mqttServer.sConnect.connect()
			while True:
				data = self.mqttServer.sConnect.receive()
				if data is None: break
				print("received [%s] from arduino" % data) 
				publish.single("arduino", data, hostname="192.168.30.1")
			self.mqttServer.sConnect.disconnect()

		except KeyboardInterrupt:
			self.mqttServer.sConnect.disconnect()

		except Exception:
			print("Main exec - Serial connection error: ")
			traceback.print_exc(limit=10, file=sys.stdout)

try:
	ser = __init__()
	ser.mqttServer = mqtt_server.MqttServer()

	#threading.Thread(target=bluetooth_loop, args=((mqttServer,)), name = 'Bluetooth Thread').start()
	threading.Thread(target=pc_loop, args=((ser.mqttServer,self)), name = 'PC Thread').start()
	#threading.Thread(target=arduino_loop, args=((mqttServer,)), name = 'Arduino Thread').start()

	try:
		ser.mqttServer.run()
	except KeyboardInterrupt:
		ser.print("1111111111111111111111111111")
		ser.mqttServer.btConnect.disconnect()
		ser.mqttServer.pcConnect.disconnect()
		ser.mqttServer.sConnect.disconnect()
		ser.mqttServer.client.loop_stop()
		ser.mqttServer.client.disconnect()

except KeyboardInterrupt:
	print("22222222222222222222222222")
	ser.mqttServer.btConnect.disconnect()
	ser.mqttServer.pcConnect.disconnect()
	ser.mqttServer.sConnect.disconnect()
	ser.mqttServer.client.loop_stop()
	ser.mqttServer.client.disconnect()
