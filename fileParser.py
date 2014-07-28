import json
import parts
import os
import body


paths = {'parts': 'data/parts',
	'creatures': 'data/creatures'}


def loadPartFile(filename):
	with open(filename, "r") as jsonfile:
		return loadPart(jsonfile.read())


def loadPart(jsonstr):
	data = json.loads(jsonstr)
	partClass = parts.GenericPart().getClass(data)
	return partClass


def loadCreatureFile(filename, partManager):
	with open(filename, "r") as jsonfile:
		return loadCreature(jsonfile.read(), partManager)


def loadCreature(jsonstr, partManager):
	data = json.loads(jsonstr)
	bodyClass = body.GenericBody().getClass(data, partManager)
	return bodyClass


def saveCreatureFile(filename, creatureObj, creatureName=False):
	json = saveCreature(creatureObj, creatureName)
	with open(paths['creatures']+"/"+filename, "w") as jsonfile:
		jsonfile.write(json)
	print('Wrote', filename)


def saveCreature(creatureObj, creatureName=False):
	json = creatureObj.getJson(creatureName)
	return json


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
			p = loadPartFile(path+"/"+f)
			parts[p.name] = p
	return parts


def loadAllCreatures(partManager):
	creatures = {}
	path = paths['creatures']
	print('Loading from', path)
	for f in sorted(os.listdir(path)):
		if f.endswith(".json"):
			print('Loading Creature', f)
			c = loadCreatureFile(path+"/"+f, partManager)
			creatures[c.name] = c
	return creatures
