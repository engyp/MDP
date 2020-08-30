from bluetooth_server import BluetoothConnection
from socket_server import SocketConnection
import sys, traceback, threading



def bluetooth_loop():
	while True:
		try:
			btConnect = BluetoothConnection()
			btConnect.connect()
			while True:
				data = btConnect.receive()
				if data is None: break
				print("received [%s]" % data)
			btConnect.disconnect()
			
		except Exception:
			print("Main exec - Bluetooth connection error: ")
			traceback.print_exc(limit=10, file=sys.stdout)

def pc_loop():
	while True:
		try:
			pcConnect = SocketConnection()
			pcConnect.connect()
			while True:
				data = pcConnect.receive()
				if data is None: break
				print("received [%s]" % data) 
			pcConnect.disconnect()

		except Exception:
			print("Main exec - Socket connection error: ")
			traceback.print_exc(limit=10, file=sys.stdout)

threading.Thread(target = bluetooth_loop, name = 'Bluetooth Thread').start()
threading.Thread(target = pc_loop, name = 'PC Thread').start()