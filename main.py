from bluetooth_server import BluetoothConnection

btConnect = BluetoothConnection()

try:
	btConnect.connect()
	while True:
		data = btConnect.receive()
		if len(data) == 0: break
		print("received [%s]" % data)
	btConnect.disconnect()
	
except Exception:
	print("Main exec - Bluetooth connection error")