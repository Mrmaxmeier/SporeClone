from mainloop import init, mainloop, StdMain
from vector2 import Vec2d

import manager
import eventhandler

import draw


TITLE = 'CreatureCreator'
FPS = 30
WINDOWSIZE = Vec2d(1920, 1080) * 0.8
WINDOWSIZE = Vec2d(int(WINDOWSIZE[0]), int(WINDOWSIZE[1]))
init(WINDOWSIZE, '--Loading--')


class CreatureCreator(StdMain):

	def __init__(self):
		self.mousePos = Vec2d(0, 0)
		self.partManager = manager.PartManager()
		self.creatureManager = manager.CreatureManager(self.partManager)
		self.creatureCount = len(self.creatureManager.getAvalibleCreatures())
		assert self.creatureCount > 0, 'No Creatures(.json) in Data/Creatures'
		self.setActiveCreature(0)
		self.currentCreatureIndex = 0

	def setActiveCreature(self, num):
		assert self.creatureManager.setActiveCreature(self.creatureManager.getAvalibleCreatures()[num]) == True, 'Not able to set Creature'
		#print(self.creatureManager.activeCreature.size)
		self.creatureManager.activeCreature.size *= 20
		self.eventHandler = eventhandler.EventHandler()
		subp = self.creatureManager.activeCreature.baseHinge.getPart().getAllSubParts(WINDOWSIZE/2, 1)
		for p, pos in subp:
			self.eventHandler.registerDict(p.getHandles())

	def onKey(self, ev):
		if ev.unicode == 'r':
			print()
			print()
			print()
			print('Resetting...')
			self.__init__()
		if ev.unicode == '\t':
			self.currentCreatureIndex = (self.currentCreatureIndex + 1) % self.creatureCount
			self.setActiveCreature(self.currentCreatureIndex)
			print('Swapped Creature to', self.creatureManager.activeCreature.name)

	def update(self, dt):
		self.eventHandler.update(dt)

	def onActiveEvent(self, ev):
		pass

	def draw(self):
		self.creatureManager.activeCreature.draw(WINDOWSIZE/2)

	def onMouseMotion(self, ev):
		self.mousePos = Vec2d(ev.pos[0], ev.pos[1])
		self.eventHandler.mouseMovement(self.mousePos)

	def onClick(self, ev):
		pass


mainloop((WINDOWSIZE, TITLE, FPS), CreatureCreator, draw.white)
