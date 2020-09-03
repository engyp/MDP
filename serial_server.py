import serial
import sys, traceback

class SerialConnection():
	def __init__(self, baud_rate = 115200, port = '/dev/ttyACM0'):
		self.port = port
		self.serialCon = None
		self.baud_rate = baud_rate

	def connect(self): 
		try:
			self.serialCon = serial.Serial(self.port, self.baud_rate)
			print("\nSerial connected at port:  %d" % self.port)

		except Exception:
			print("Serial connection error: ")
			traceback.print_exc(limit=10, file=sys.stdout)

	def disconnect(self):
		try:
			if self.serialCon:
				self.serialCon.close()
				print("\n Serial disconnected")

		except Exception as e:
			print("Serial disconnection error: ")
			traceback.print_exc(limit=10, file=sys.stdout)

	def send(self, msg):
		try:
			self.serialCon.write(msg.encode('ascii'))

		except Exception as e:
			print("Serial send error: ")
			traceback.print_exc(limit=10, file=sys.stdout)

	def receive(self):
		try:
			msg = self.serialCon.readline().decode('utf-8', errors='replace')
			return msg

		except Exception as e:
			print("Serial receive error: ")
			traceback.print_exc(limit=10, file=sys.stdout)