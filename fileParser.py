import json
import parts
import os
import body


def loadPart(filename, partManager):
	with open(filename, "r") as jsonfile:
		data = json.loads(jsonfile.read())
		partClass = parts.GenericPart().getClass(data, partManager)
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


def loadAllParts(partManager):
	parts = []
	for f in os.listdir("data/parts"):
		if f.endswith(".json"):
			p = loadPart("data/parts/"+f, partManager)
			parts.append(p)
	return p

print(loadCreature('data/creatures/bareMinimum.json'))
