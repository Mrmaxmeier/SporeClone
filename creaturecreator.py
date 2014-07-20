from mainloop import init, mainloop, StdMain
from vector2 import Vec2d

import manager
import eventhandler

import draw


TITLE = 'CreatureCreator'
FPS = 30
WINDOWSIZE = Vec2d(1200, 720)
init(WINDOWSIZE, '--Loading--')


class CreatureCreator(StdMain):

	def __init__(self):
		self.mousePos = Vec2d(0, 0)
		self.partManager = manager.PartManager()
		self.creatureManager = manager.CreatureManager(self.partManager)
		avalible = self.creatureManager.getAvalibleCreatures()
		for i in range(len(avalible)):
			print(i, avalible)
		n = 0#int(input('> '))
		assert self.creatureManager.setActiveCreature(avalible[n]) == True, 'Not able to set Creature'
		self.creatureManager.activeCreature.size = 25
		self.eventHandler = eventhandler.EventHandler()

	def onKey(self, ev):
		pass

	def update(self, dt):
		pass

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
