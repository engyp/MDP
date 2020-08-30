from bluetooth_server import BluetoothConnection

btConnect = BluetoothConnection()

try:
	btConnect.connect()
	while True:
		data = client_sock.recv(1024)
		if len(data) == 0: break
		print("received [%s]" % data)
	btConnect.disconnect()
	
except Exception:
	print("Bluetooth connection error")