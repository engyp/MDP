import socket

HOST = '10.27.255.195' # Server IP or Hostname
PORT = 12345 # Pick an open Port (1000+ recommended), must match the client sport
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

#managing error exception
try:
	s.bind((HOST, PORT))
except socket.error:
	print('Bind failed ')

s.listen(5)
print('Socket awaiting messages')
(conn, addr) = s.accept()
print('Connected')
recv_buffer = ""
# awaiting for message
while True:
	data = conn.recv(2048).decode("utf-8")
	recv_buffer = recv_buffer + data
	strings = recv_buffer.split('\n')
	#print(strings)
	#print(strings[:-1])
	for s in strings[:-1]:
		print("Received: %s" % s)
	recv_buffer = strings[-1]
	# reply = ''

	# # process your message
	# if data == 'Hello':
	# 	reply = 'Hi, back!'
	# elif data == 'This is important':
	# 	reply = 'OK, I have done the important thing you have asked me!'

	# #and so on and on until...
	# elif data == 'quit':
	# 	conn.send('Terminating')
	# 	break
	# else:
	# 	reply = 'Unknown command'

	# # Sending reply
	# conn.send(str(reply))

conn.close() # Close connections