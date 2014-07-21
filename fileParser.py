import json
import parts
import os
import body


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


def saveCreature(filename, creatureObj):
	raise NotImplementedError


def loadGame(filename):
	raise NotImplementedError


def saveGame(filename, gameObj):
	raise NotImplementedError


def loadAllParts():
	parts = {}
	for f in sorted(os.listdir("data/parts")):
		if f.endswith(".json"):
			print('Loading Part', f)
			p = loadPart("data/parts/"+f)
			parts[p.name] = p
	return parts


def loadAllCreatures(partManager):
	creatures = {}
	for f in sorted(os.listdir("data/creatures")):
		if f.endswith(".json"):
			print('Loading Creature', f)
			c = loadCreature("data/creatures/"+f, partManager)
			creatures[c.name] = c
	return creatures
