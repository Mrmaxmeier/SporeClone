#

from vector2 import Vec2d
from player import ArtificialPlayer, NetworkPlayer

#

#Serverstuffs

import socketserver
import json
import supersocket


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
				supersock = supersocket.SuperSocket(self.request)
				bdata = supersock.recv()
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
				supersock.send(resp)
		except Exception as e:
			print("Exception wile receiving message: ", e)


if __name__ == "__main__":
	server = TCPServer(('0.0.0.0', 13373), ServerHandler)
	server.serve_forever()
