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

	def handleData(self, d):
		return {'return': 'no_response'}

	def handle(self):
		try:
			while 1:
				bdata = self.request.recv(1024 * 10)
				if bdata == b'':
					print('Connection Closed!')
					return
				data = json.loads(bdata.decode('UTF-8').strip())
				# process the data, i.e. print it:
				print("Recv'ed", data)
				response = self.handleData(data)
				# send some 'ok' back
				respBytes = bytes(json.dumps(response), 'UTF-8')
				self.request.sendall(respBytes)
		except Exception as e:
			print("Exception wile receiving message: ", e)


if __name__ == "__main__":
	server = TCPServer(('127.0.0.1', 13373), ServerHandler)
	server.serve_forever()
