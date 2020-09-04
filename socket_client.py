import socket, threading
import paho.mqtt.publish as publish

HOST = '192.168.30.1' # Enter IP or Hostname of your server
PORT = 12345 # Pick an open Port (1000+ recommended), must match the server port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

def send():
	#Lets loop awaiting for your input
	while True:
		command = input('Enter your text: ')
		s.send(command.encode('utf-8'))
		#publish.single("android", command.encode('utf-8'), hostname="192.168.30.1")


def receive():
	#Lets loop awaiting for your input
	while True:
		#command = input('Enter your command: ')
		#s.send(command.encode('utf-8'))
		#publish.single("rpi/android", command.encode('utf-8'), hostname="192.168.30.1")
		reply = s.recv(2048).decode("utf-8")
		#if reply == 'terminate':
		#	break
		print("\n" + reply)



threading.Thread(target=send, name = 'send Thread').start()
threading.Thread(target=receive, name = 'receive Thread').start()