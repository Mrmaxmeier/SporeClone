#

from vector2 import Vec2d
from player import ArtificialPlayer, NetworkPlayer

#

#Serverstuffs

import supersocket
import json
import threading
import socket
import queue

sampleMsg = {'joined': {'desc': 'Is called on Connection', 'name': 'Mrmaxmeier', 'body': {'desc': 'BodyDict from data/creatures'}},
	'u': {'desc': 'Used to update PlayerVars', 'pos': [10, 10]},
	'msg': {'desc': 'Sends a message to everybody', 'body': 'hi'},
	'share': {'desc': 'share Body/Part/Save with other Users', 'body': {'desc': 'BodyDict from data/creatures'}}
}


#


#


class SimpleServer(threading.Thread):
	def __init__(self, ip, port, newThreadHandler):
		threading.Thread.__init__(self)
		self.setDaemon(True)
		self.newThreadHandler = newThreadHandler

		server_address = (ip, port)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(server_address)
		self.server_address = self.sock.getsockname()
		print('Server bound to ', self.server_address)
		self.sock.listen(5)
		self.isAlive = True

		self.connectedClients = []
		self.name2thread = {}

		self.start()

	def serve(self):
		while self.isAlive:
			(clientsock, (ip, port)) = self.sock.accept()
			print('New Connection @', ip, ':', port)
			sendToClientQueue = queue.Queue()
			newThread = self.newThreadHandler(clientsock, sendToClientQueue, self)
			self.connectedClients.append(newThread)

	def sendToName(self, name, msg, sendDirect=True):
		if name in self.name2thread:
			self.name2thread[name].queue.put(msg)
			if sendDirect:
				self.name2thread.processQueue()
			return True
		else:
			print(name, 'not in name2queue')
			return False

	def sendToAllBut(self, names, msg, sendDirect=True):
		sendTo = self.name2thread.keys()
		for n in sendTo:
			if n not in names:
				self.sendToName(n, msg, sendDirect)

	def sendToAll(self, msg):
		for thread in self.connectedClients:
			thread.sendQueue.put(msg)
			thread.processQueue()

	def registerName(self, name, thread):
		self.name2thread[name] = thread


class ClientHandlerThread(threading.Thread):
	def __init__(self, clientsock, sendQueue, server):
		threading.Thread.__init__(self)
		self.sock = clientsock
		self.sendQueue = sendQueue
		self.supersock = supersocket.SuperSocket(clientsock)
		self.server = server
		self.start()

	def run(self):
		print('Thread started')
		self.handle()

	def handleData(self, d):
		return {'return': 'no_response'}

	def handle(self):
		try:
			while 1:
				bdata = self.supersock.recv()
				if not bdata:
					#if bdata == b'':
					print('Connection Closed!')
					return
				#print('RAW', bdata)
				data = json.loads(bdata)
				# process the data, i.e. print it:
				print("Recv'ed", data)
				response = self.handleData(data)
				# send some 'ok' back
				resp = json.dumps(response)
				#respBytes = bytes(resp, 'UTF-8')
				self.supersock.send(resp)

				self.processQueue()
		except Exception as e:
			print(type(e), "while receiving message: ", e)

	def processQueue(self):
		while True:
			try:
				msg = self.sendQueue.get_nowait()
				self.supersock.send(msg)
			except queue.Empty:
				break
			except Exception as e:
				print(type(e), "while sending queued message: ", e)


if __name__ == "__main__":
	server = SimpleServer('0.0.0.0', 13373, ClientHandlerThread)
	server.serve()
