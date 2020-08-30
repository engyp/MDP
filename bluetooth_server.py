# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

from bluetooth import *


def __init__(self, port=8, uuid="94f39d29-7d6d-437d-973b-fba39e49d4ee"):
	self.port = port
	self.server_sock = None
	self.uuid = uuid

def connect():
	try:
		self.server_sock=BluetoothSocket( RFCOMM )
		self.server_sock.bind(("",self.port)) # channel 8
		self.server_sock.listen(1)

		advertise_service( self.server_sock, "MDPGrp30",
		                   service_id = self.uuid,
		                   service_classes = [ self.uuid, SERIAL_PORT_CLASS ],
		                   profiles = [ SERIAL_PORT_PROFILE ])
		                   
		print("Waiting for connection on RFCOMM channel %d" % self.port)

		client_sock, client_info = self.server_sock.accept()
		print("Accepted connection from ", client_info)
	
	except Exception as e:
		print("Bluetooth connection error")

def disconnect():
	try:
		self.client_sock.close()
		self.server_sock.close()
		print("Bluetooth disconnected")

	except Exception as e:
		print("Bluetooth disconnection error")


try:
	connect()
	while True:
		data = self.client_sock.recv(1024)
		if len(data) == 0: break
		print("received [%s]" % data)
	disconnect()
except IOError:
	pass