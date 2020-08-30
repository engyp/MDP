# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

from bluetooth import *


def connect():
	try:
		server_sock=BluetoothSocket( RFCOMM )
		server_sock.bind(("",8)) # channel 8
		server_sock.listen(1)

		port = server_sock.getsockname()[1]

		uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

		advertise_service( server_sock, "MDPGrp30",
		                   service_id = uuid,
		                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
		                   profiles = [ SERIAL_PORT_PROFILE ])
		                   
		print("Waiting for connection on RFCOMM channel %d" % port)

		client_sock, client_info = server_sock.accept()
		print("Accepted connection from ", client_info)
	
	except Exception as e:
		print("Bluetooth connection error")

def disconnect():
	try:
		client_sock.close()
		server_sock.close()
		print("Bluetooth disconnected")

	except Exception as e:
        print("Bluetooth disconnection error")


try:
	connect()
    while True:
        data = client_sock.recv(1024)
        if len(data) == 0: break
        print("received [%s]" % data)
    disconnect()
except IOError:
    pass