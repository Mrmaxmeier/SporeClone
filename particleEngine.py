from mainloop import init, mainloop, StdMain
from vector2 import Vec2d
import particle

import draw
import pygame

TITLE = 'ParticleEngine'
FPS = 30
WINDOWSIZE = (1920, 1080)
init(WINDOWSIZE, '--Loading--')


class ParticleEngine(StdMain):

	def __init__(self):
		self.mousePos = Vec2d(0, 0)
		self.pspace = particle.ps_Gravity(WINDOWSIZE)
		self.pspace.drawVelocity = True
		self.fireSource = False

	def onKey(self, ev):
		print(ev)
		if ev.unicode == 'v':
			self.pspace.drawVelocity = not self.pspace.drawVelocity

	def update(self, dt):
		self.pspace.update(dt)
		pressed = pygame.mouse.get_pressed()
		if pressed[2]:
			if self.fireSource:
				if not self.fireSource.isDead:
					dpos = self.mousePos-self.fireSource.pos
					self.fireSource.accelerate(dpos, dt)

	def onActiveEvent(self, ev):
		pass

	def draw(self):
		self.pspace.draw()

	def onMouseMotion(self, ev):
		self.mousePos = Vec2d(ev.pos[0], ev.pos[1])

	def onClick(self, ev):
		#if ev.button == 4:
		#	self.pspace.spawnParticle(particle.p_Explode_on_death, Vec2d(self.mousePos), Vec2d(100, 0), 3)
		#elif ev.button == 1:
		#	for i in range(0, 18):
		#		vel = Vec2d(100, 0).rotated(i*20)
		#		self.pspace.spawnParticle(particle.p_Shrinking, Vec2d(self.mousePos-(vel/2)), vel)
		if ev.button == 1:
			p = self.pspace.spawnParticle(particle.p_FireSource, Vec2d(self.mousePos), Vec2d(0, 0))
			self.fireSource = p
		else:
			print(ev)


mainloop((WINDOWSIZE, TITLE, FPS), ParticleEngine, draw.white)
