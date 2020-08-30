

btConnect = BluetoothConnection()

try:
	btConnect.connect()
	while True:
		data = self.client_sock.recv(1024)
		if len(data) == 0: break
		print("received [%s]" % data)
	btConnect.disconnect()
	
except IOError:
	pass