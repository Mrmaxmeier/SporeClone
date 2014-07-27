import player
from vector2 import Vec2d
import random


class World(object):
	def __init__(self, size, creatureManager):
		self.size = size
		self.players = []
		self.creatureManager = creatureManager

	def getPlayers(self):
		return self.players

	def update(self, dt):
		for p in self.players:
			p.update(dt)

	def draw(self):
		for p in self.players:
			p.draw()

	def spawnAI(self, pos=Vec2d(0, 0)):
		bodyName = random.choice(self.creatureManager.getAvalibleCreatures())
		body = self.creatureManager.getCreature(bodyName)()
		p = player.ArtificialPlayer(body, self)
		p.pos = pos
		p.body.size *= 10
		self.players.append(p)

	def getCropped(self, pos, radius):
		raise NotImplementedError
