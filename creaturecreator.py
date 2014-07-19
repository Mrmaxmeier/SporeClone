from mainloop import init, mainloop, StdMain
from log import *
from vector2 import Vec2d

import manager

import draw


TITLE = 'CreatureCreator'
FPS = 30
WINDOWSIZE = (1200, 720)
init(WINDOWSIZE, '--Loading--')


class CreatureCreator(StdMain):

	def __init__(self):
		self.mousePos = Vec2d(0, 0)
		self.partManager = manager.PartManager()
		self.creatureManager = manager.CreatureManager()

	def onKey(self, ev):
		pass

	def update(self, dt):
		pass

	def onActiveEvent(self, ev):
		pass

	def draw(self):
		pass

	def onMouseMotion(self, ev):
		self.mousePos = Vec2d(ev.pos[0], ev.pos[1])

	def onClick(self, ev):
		pass


mainloop((WINDOWSIZE, TITLE, FPS), CreatureCreator, draw.white)
