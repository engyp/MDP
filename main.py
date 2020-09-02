from bluetooth_server import BluetoothConnection
from socket_server import SocketConnection
from serial_server import SerialConnection
import sys, traceback, threading
import paho.mqtt.publish as publish
import mqtt_server


def bluetooth_loop():
	#while True:
		try:
			btConnect = BluetoothConnection()
			btConnect.disconnect()
			btConnect.connect()
			while True:
				data = btConnect.receive()
				if data is None: break
				print("received [%s] from android" % data)
				btConnect.send("\nreply back from rpi")
				publish.single("rpi/android", data, hostname="192.168.30.1")
			btConnect.disconnect()

		except KeyboardInterrupt:
			btConnect.disconnect()
			
		except Exception:
			print("Main exec - Bluetooth connection error: ")
			traceback.print_exc(limit=10, file=sys.stdout)

def pc_loop():
	#while True:
		try:
			pcConnect = SocketConnection()
			pcConnect.disconnect()
			pcConnect.connect()
			while True:
				data = pcConnect.receive()
				if data == 'quit': break
				print("received [%s] from PC" % data)
				publish.single("rpi/android", data, hostname="192.168.30.1")
			pcConnect.disconnect()

		except KeyboardInterrupt:
			pcConnect.disconnect()

		except Exception:
			print("Main exec - Socket connection error: ")
			traceback.print_exc(limit=10, file=sys.stdout)

def arduino_loop():
	#while True:
		try:
			sConnect = SerialConnection()
			sConnect.disconnect()
			sConnect.connect()
			while True:
				if (serialCon.in_waiting > 0):
					data = sConnect.receive()
					if data is None: break
					print("received [%s]" % data) 
					serialCon.write("This is message from rpi".encode('ascii'))
				
			sConnect.disconnect()

		except KeyboardInterrupt:
			sConnect.disconnect()

		except Exception:
			print("Main exec - Serial connection error: ")
			traceback.print_exc(limit=10, file=sys.stdout)


threading.Thread(target = bluetooth_loop, name = 'Bluetooth Thread').start()
threading.Thread(target = pc_loop, name = 'PC Thread').start()

mqtt_server.run()