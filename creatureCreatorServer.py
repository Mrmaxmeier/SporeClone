from server import TCPServer, ServerHandler
import json
import os
#


#addMsg = {'creature':{'add': 'CREATUREJSON'}}

#requestMsg = {'creature': {'request': 'ALL'}}


class CreatureCreatorServerManager():
	def __init__(self):
		self.creatures = {}
		path = 'data/creatures'
		print('Loading from', path)
		for f in sorted(os.listdir(path)):
			if f.endswith(".json"):
				print('Loading Creature', f)
				with open(path+"/"+f, "r") as jsonfile:
					jsonstr = jsonfile.read()
					#make it readable
					jsonstr = json.dumps(json.loads(jsonstr))
					jsonstr = str(jsonstr)
					self.addCreature(jsonstr)

	def getAllCreatures(self):
		return [json.loads(self.creatures[key]) for key in self.creatures]

	def addCreature(self, creatureJson):
		d = json.loads(creatureJson)
		creatureName = d['name']
		self.creatures[creatureName] = creatureJson


serverManagerObj = CreatureCreatorServerManager()


class CreatureCreatorServerHandler(ServerHandler):
	def handleData(self, d):
		if 'creature' in d:
			if 'request' in d['creature']:
				if d['creature']['request'] == 'ALL':
					s = serverManagerObj.getAllCreatures()
					return {'response': 'creatures', 'creatures': s}
			if 'add' in d['creature']:
				serverManagerObj.addCreature(d['creature']['add'])
				return self.handleData({'creature': {'request': 'ALL'}})
		if 'join' in d:
			return self.handleData({'creature': {'request': 'ALL'}})
		return {'error': 'Message Not Parsed'}

server = TCPServer(('0.0.0.0', 13373), CreatureCreatorServerHandler)
server.serve_forever()
