#

from vector2 import Vec2d
from player import ArtificialPlayer, NetworkPlayer

#

#Serverstuffs

import socketserver
import json


sampleMsg = {'joined': {'desc': 'Is called on Connection', 'name': 'Mrmaxmeier', 'body': {'desc': 'BodyDict from data/creatures'}},
	'u': {'desc': 'Used to update PlayerVars', 'pos': [10, 10]},
	'msg': {'desc': 'Sends a message to everybody', 'body': 'hi'},
	'share': {'desc': 'share Body/Part/Save with other Users', 'body': {'desc': 'BodyDict from data/creatures'}}
}


#


#


class TCPServer(socketserver.ThreadingTCPServer):
	allow_reuse_address = True


class ServerHandler(socketserver.BaseRequestHandler):

	def processJson(self, d):
		if 'joined' in d:
			#playerDict = d['joined']
			#name = playerDict['name']
			#newPlayer = NetworkPlayer()
			raise NotImplementedError
		return {'result': True}

	def handle(self):
		try:
			data = json.loads(self.request.recv(1024).decode('UTF-8').strip())
			# process the data, i.e. print it:
			print(data)
			# send some 'ok' back
			self.request.sendall(bytes(json.dumps({'return': 'ok'}), 'UTF-8'))
			self.request.sendall(bytes(json.dumps({'return': 'määä'}), 'UTF-8'))
		except Exception as e:
			print("Exception wile receiving message: ", e)

server = TCPServer(('127.0.0.1', 13373), ServerHandler)
server.serve_forever()
