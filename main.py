from bluetooth_server import BluetoothConnection
import sys, traceback

btConnect = BluetoothConnection()

try:
	btConnect.connect()
	while True:
		data = btConnect.receive()
		if data is None: break
		print("received [%s]" % data)
	btConnect.disconnect()
	
except Exception:
	print("Main exec - Bluetooth connection error: ")
	traceback.print_exc(limit=10, file=sys.stdout)