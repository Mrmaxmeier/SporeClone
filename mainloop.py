from OpenGL.GL import *
import pygame
from pygame.locals import *


class StdMain:

	def __init__(self):
		pass

	def update(self, dt):
		pass

	def onClick(self, ev):
		pass

	def onRelease(self, ev):
		pass

	def onMouseMotion(self, ev):
		pass

	def onKey(self, ev):
		pass

	def onKeyUp(self, ev):
		pass

	def onActiveEvent(self, ev):
		pass

	def draw(self):
		pass


def init(size, title):
	(x, y) = size
	flags = OPENGL | DOUBLEBUF
	pygame.init()
	pygame.display.set_mode((x, y), flags)
	pygame.display.set_caption(title)

	glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)

	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0, x, y, 0, -1, 1)
	glMatrixMode(GL_MODELVIEW)


def mainloop(options, Class):
	(size, title, fps) = options
	init(size, title)
	obj = Class()
	clock = pygame.time.Clock()
	while 1:
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()
		obj.draw()
		pygame.display.flip()
		clock.tick(fps)
		obj.update(clock.get_time() / 1000.)
		for event in pygame.event.get():
			if event.type == QUIT:
				return obj
			elif event.type == MOUSEBUTTONDOWN:
				obj.onClick(event)
			elif event.type == MOUSEBUTTONUP:
				obj.onRelease(event)
			elif event.type == MOUSEMOTION:
				obj.onMouseMotion(event)
			elif event.type == KEYDOWN:
				obj.onKey(event)
			elif event.type == KEYUP:
				obj.onKeyUp(event)
			elif event.type == ACTIVEEVENT:
				obj.onActiveEvent(event)
