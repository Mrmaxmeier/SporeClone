import json
import parts
import os
import body


paths = {'parts': 'data/parts',
	'creatures': 'data/creatures'}


def loadPart(filename):
	with open(filename, "r") as jsonfile:
		data = json.loads(jsonfile.read())
		partClass = parts.GenericPart().getClass(data)
		return partClass


def loadCreature(filename, partManager):
	with open(filename, "r") as jsonfile:
		data = json.loads(jsonfile.read())
		bodyClass = body.GenericBody().getClass(data, partManager)
		return bodyClass


def saveCreature(filename, creatureObj, creatureName=False):
	json = creatureObj.getJson(creatureName)
	with open(paths['creatures']+"/"+filename, "w") as jsonfile:
		jsonfile.write(json)
	print('Wrote', filename)


def loadGame(filename):
	raise NotImplementedError


def saveGame(filename, gameObj):
	raise NotImplementedError


def loadAllParts():
	parts = {}
	path = paths['parts']
	for f in sorted(os.listdir(path)):
		if f.endswith(".json"):
			print('Loading Part', f)
			p = loadPart(path+"/"+f)
			parts[p.name] = p
	return parts


def loadAllCreatures(partManager):
	creatures = {}
	path = paths['creatures']
	print('Loading from', path)
	for f in sorted(os.listdir(path)):
		if f.endswith(".json"):
			print('Loading Creature', f)
			c = loadCreature(path+"/"+f, partManager)
			creatures[c.name] = c
	return creatures
