import socket
import json
from world import World
import threading
import queue

import supersocket

NAME = 'me'
d = {'joined': {'desc': 'Is called on Connection', 'name': NAME, 'body': {'desc': 'BodyDict from data/creatures'}}}


class Client(threading.Thread):
	def __init__(self, clientQueue, ip='127.0.0.1'):
		threading.Thread.__init__(self)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((ip, 13373))
		self.supersock = supersocket.SuperSocket(self.sock)
		self.sockAlive = True
		self.queue = clientQueue
		self.setDaemon(True)

	def run(self):
		self.recvLoop()

	def send(self, d):
		self.supersock.send(json.dumps(d))

	def recv(self):
		try:
			print("recv'in")
			data = self.supersock.recv()
			print('RAW', data)
			if not data:
				#if data == b'':
				print('Socket Closed :(')
				self.sockAlive = False
				return {'connectionStatus': 'closed'}
			#decoded = data.decode('UTF-8')
			#print(decoded)
			return json.loads(data)
		except Exception as e:
			return {'return': {'type': 'Malformed Data', 'exception': str(e)}}

	def recvLoop(self):
		while self.sockAlive:
			data = self.recv()
			if data:
				self.queue.put(data)

	def close(self):
		self.supersock.close()
		self.sockAlive = False

if __name__ == "__main__":
	import time
	clientThread = Client('127.0.0.1')
	queue = queue.Queue()
	clientThread.recvLoop(queue)
	clientThread.close()
	while clientThread.isAlive:
		time.sleep(2)
