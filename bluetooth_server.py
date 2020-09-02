from bluetooth import *
import sys, traceback

class BluetoothConnection():
	def __init__(self, port=8, uuid="94f39d29-7d6d-437d-973b-fba39e49d4ee"):
	    self.port = port
	    self.btcon = None
	    self.server_sock = None
	    self.uuid = uuid

	def connect(self):
	    try:
	        self.server_sock=BluetoothSocket( RFCOMM )
	        self.server_sock.bind(("",self.port)) # channel 8
	        self.server_sock.listen(1)

	        advertise_service( self.server_sock, "MDPGrp30",
	                           service_id = self.uuid,
	                           service_classes = [ self.uuid, SERIAL_PORT_CLASS ],
	                           profiles = [ SERIAL_PORT_PROFILE ])
	                           
	        print("\nWaiting for connection on RFCOMM channel %d" % self.port)

	        self.btcon, self.client_info = self.server_sock.accept()
	        println("Accepted connection from ", self.client_info)
	    
	    except Exception as e:
	        print("Bluetooth connection error")
	        traceback.print_exc(limit=10, file=sys.stdout)

	def disconnect(self):
	    try:
	        if self.btcon: 
	        	self.btcon.close()
	        	self.btcon = None
	        	print("\nBluetooth disconnected")
	        
	        if self.server_sock:
	        	self.server_sock.close()
	        	self.server_sock = None
	        
	    except Exception as e:
	        print("Bluetooth disconnection error: ")
	        traceback.print_exc(limit=10, file=sys.stdout)

	def send(self, msg):
		try:
			self.btcon.send(msg)
		except Exception as e:
			print("Bluetooth send error: ")
			traceback.print_exc(limit=10, file=sys.stdout)

	def receive(self):
		try:
			msg = self.btcon.recv(2048).decode("utf-8")
			return msg
		except Exception as e:
			print("Bluetooth receive error: ")
			traceback.print_exc(limit=10, file=sys.stdout)