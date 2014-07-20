import fileParser
import game
import os


class PartManager:
	def __init__(self):
		self.refreshParts()

	def getPart(self, name):
		if name in self.parts:
			return self.parts[name]
		return None

	def refreshParts(self):
		self.parts = fileParser.loadAllParts()

	def getAvalibleParts(self):
		return self.parts.keys()


class CreatureManager:
	def __init__(self, partManager):
		self.partManager = partManager
		self.creatures = {}
		self.activeCreature = None
		self.avalibleCreatures = fileParser.loadAllCreatures(self.partManager)

	def addCreature(self):
		raise NotImplementedError

	def getCreature(self, name):
		if name in self.creatures:
			return self.creatures[name]
		else:
			return None

	def getAvalibleCreatures(self):
		return list(self.avalibleCreatures.keys())

	def setActiveCreature(self, name):
		if name in self.avalibleCreatures:
			self.activeCreature = self.avalibleCreatures[name]()
			return True
		else:
			return False


class GameManager:
	def __init__(self):
		self.game = game.Game()

	def loadGame(self, savegameName):
		self.game = fileParser.loadGame('data/saveGame/'+savegameName)

	def getAvalibleSavegames(self):
		files = os.listdir("data/saveGame")
		return [f if f.endswith(".json") else "!WRONG SUFFIX!" for f in files]

	def getPart(self, partName):
		raise FloatingPointError
