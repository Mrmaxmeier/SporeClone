import fileParser
import game
import os


class PartManager:
	def __init__(self):
		self.parts = fileParser.loadAllParts()

	def getPart(self, name):
		pass


class CreatureManager:
	def __init__(self):
		self.creatures = {}
		self.activeCreature = None

	def addCreature(self):
		raise NotImplementedError

	def getCreature(self, name):
		if name in self.creatures:
			return self.creatures[name]
		else:
			return None

	def setActiveCreature(self, name):
		if name in self.creatures:
			self.activeCreature = self.creatures[name]
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
