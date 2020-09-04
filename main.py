from bluetooth_server import BluetoothConnection
from socket_server import SocketConnection
from serial_server import SerialConnection
import sys, traceback, threading
import paho.mqtt.publish as publish
import mqtt_server


def bluetooth_loop(mqttServer):
	#while True:
		try:
			mqttServer.btConnect = BluetoothConnection()
			mqttServer.btConnect.disconnect()
			mqttServer.btConnect.connect()
			while True:
				data = mqttServer.btConnect.receive()
				if data is None: break
				print("received [%s] from android" % data)
				#mqttServer.btConnect.send("\nreply back from rpi")
				publish.single("android", data, hostname="192.168.30.1")
			mqttServer.btConnect.disconnect()

		except KeyboardInterrupt:
			mqttServer.btConnect.disconnect()
			
		except Exception:
			print("Main exec - Bluetooth connection error: ")
			traceback.print_exc(limit=10, file=sys.stdout)
			time.sleep(0.5)

def pc_loop(mqttServer):
	#while True:
		try:
			mqttServer.pcConnect = SocketConnection()
			mqttServer.pcConnect.disconnect()
			mqttServer.pcConnect.connect()
			while True:
				data = mqttServer.pcConnect.receive()
				if data == 'quit': break
				print("received [%s] from PC" % data)
				publish.single("pc", data, hostname="192.168.30.1")
			mqttServer.pcConnect.disconnect()

		except KeyboardInterrupt:
			mqttServer.pcConnect.disconnect()

		except Exception:
			print("Main exec - Socket connection error: ")
			traceback.print_exc(limit=10, file=sys.stdout)
			time.sleep(0.5)

def arduino_loop(mqttServer):
	#while True:
		try:
			mqttServer.sConnect = SerialConnection()
			mqttServer.sConnect.disconnect()
			mqttServer.sConnect.connect()
			while True:
				data = mqttServer.sConnect.receive()
				if data is None: break
				print("received [%s] from arduino" % data) 
				publish.single("arduino", data, hostname="192.168.30.1")
			mqttServer.sConnect.disconnect()

		except KeyboardInterrupt:
			mqttServer.sConnect.disconnect()

		except Exception:
			print("Main exec - Serial connection error: ")
			traceback.print_exc(limit=10, file=sys.stdout)
			time.sleep(0.5)


mqttServer = mqtt_server.MqttServer()

#sThread = threading.Thread(target=arduino_loop, args=((mqttServer,)), name = 'Arduino Thread')
#sThread.setDaemon(True)
#sThread.start()
#sThread.join()

btThread = threading.Thread(target=bluetooth_loop, args=((mqttServer,)), name = 'Bluetooth Thread')
btThread.setDaemon(True)
btThread.start()

pcThread = threading.Thread(target=pc_loop, args=((mqttServer,)), name = 'PC Thread')
pcThread.setDaemon(True)
pcThread.start()

mqttThread = threading.Thread(target=mqttServer.run())
mqttThread.setDaemon(True)
mqttThread.start()

btThread.join()
pcThread.join()
mqttThread.join()


