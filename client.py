import socket
import json
from world import World
import threading
import queue

NAME = 'me'
d = {'joined': {'desc': 'Is called on Connection', 'name': NAME, 'body': {'desc': 'BodyDict from data/creatures'}}}


class Client(threading.Thread):
	def __init__(self, clientQueue, ip='127.0.0.1'):
		threading.Thread.__init__(self)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((ip, 13373))
		self.sockAlive = True
		self.queue = clientQueue

	def run(self):
		self.recvLoop()

	def send(self, d):
		self.sock.send(bytes(json.dumps(d), 'UTF-8'))

	def recv(self, size=1024):
		try:
			data = self.sock.recv(size)
			if data == b'':
				self.sockAlive = False
				return {'connectionStatus': 'closed'}
			return json.loads(data.decode('UTF-8'))
		except Exception as e:
			return {'return': {'type': 'Malformed Data', 'exception': str(e)}}

	def recvLoop(self):
		while self.sockAlive:
			data = self.recv()
			self.queue.put(data)

	def close(self):
		self.sock.close()
		self.sockAlive = False

if __name__ == "__main__":
	import time
	clientThread = Client('127.0.0.1')
	queue = queue.Queue()
	clientThread.recvLoop(queue)
	clientThread.close()
	while clientThread.isAlive:
		time.sleep(5)
