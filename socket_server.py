import socket


class SocketConnection():
	def __init__(self, port=12345):
		self.host = ''
		self.port = port
		self.conn = None
		self.socket = None
		self.client_addr = None

	def connect(self):
		try:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
			self.socket.bind((self.host, self.port))
			self.socket.listen(1)

			print('\nSocket connecting...')
			self.conn, self.client_addr = self.socket.accept()
			print('\nSocket Connected')

		except Exception as e:
			raise Exception('Socket connection error: {}'.format(str(e)))

	def disconnect(self):
		try:
			if self.conn is not None:
				self.conn.close()
				self.conn = None
				print("\nSocket disconnected") 

			if self.socket is not None:
				self.socket.close()
				self.socket = None

		except Exception as e:
			raise Exception("Socket disconnection error: {}".format(str(e)))

	def send(self, msg):
		try:
			self.conn.send(msg.encode())
		except Exception as e:
			raise Exception('Socket send error: {}'.format(str(e)))

	def receive(self):
		try:
			msg = self.conn.recv(2048).decode("utf-8")
			return msg
		except Exception as e:
			raise Exception('Socket receive error: {}'.format(str(e)))
