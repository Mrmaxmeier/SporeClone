from mainloop import init, mainloop, StdMain
from vector2 import Vec2d

import manager
import eventhandler
import parts

import draw
import font
import pygame
import copy


TITLE = 'CreatureCreator'
FPS = 60
WINDOWSIZE = Vec2d(1920, 1080) * 0.8
WINDOWSIZE = Vec2d(int(WINDOWSIZE[0]), int(WINDOWSIZE[1]))
init(WINDOWSIZE, '--Loading--')


class PartSelector(object):
	partMargin = 150
	partBorder = Vec2d(100, 100)

	def __init__(self, partManager, windowsize, mouseHinge, width=5):
		self.mouseHinge = mouseHinge
		self.windowsize = windowsize
		self.partManager = partManager
		ps = list(self.partManager.getAvalibleParts())
		self.parts = []
		currentRow = False
		i = 0
		while True:
			if i % width == 0:
				if currentRow:
					self.parts.append(currentRow)
				currentRow = []
			if i >= len(ps):
				self.parts.append(currentRow)
				break
			currentRow.append(ps[i])
			i += 1
		self.hinges = []
		for row in range(len(self.parts)):
			hingeRow = []
			for p in range(len(self.parts[row])):
				hinge = parts.Hinge(Vec2d(row * self.partMargin, p * self.partMargin) + self.partBorder)
				print(hinge.position)
				part = self.partManager.getPart(self.parts[row][p])(hinge)
				hinge.setPart(part)
				hingeRow.append(hinge)
			self.hinges.append(hingeRow)
		print(self.hinges)

	def draw(self):
		for hingeRow in self.hinges:
			for h in hingeRow:
				if h.hasPart():
					h.getPart().draw(h.position, 10)

	def onClick(self, ev):
		mousePosition = Vec2d(ev.pos[0], ev.pos[1])
		button = ev.button
		# LeftClick, Rightclick
		if button == 1:
			for row in self.hinges:
				for h in row:
					p = h.getPart()
					if p.collides(mousePosition, h.position, 10):
						print('COLLISION!', p, h)
						self.mouseHinge.setPart(p)
						break


class CreatureCreator(StdMain):

	def __init__(self):
		self.mousePos = Vec2d(0, 0)
		self.partManager = manager.PartManager()
		self.creatureManager = manager.CreatureManager(self.partManager)
		self.creatureCount = len(self.creatureManager.getAvalibleCreatures())
		assert self.creatureCount > 0, 'No Creatures(.json) in Data/Creatures'
		self.setActiveCreature(0)
		self.currentCreatureIndex = 0
		#
		#
		#
		#
		self.myfont = pygame.font.SysFont("Courier New", 32, bold=True)
		self.fps_display = font.RenderText("", [0, 0, 0], self.myfont)

		self.mouseHinge = parts.Hinge(Vec2d(0, 0))
		#self.mouseHinge.setPart(self.partManager.getPart('Eye')(self.mouseHinge))
		self.partSelector = PartSelector(self.partManager, WINDOWSIZE, self.mouseHinge)

	def setActiveCreature(self, num):
		avalible = self.creatureManager.getAvalibleCreatures()
		assert self.creatureManager.setActiveCreature(avalible[num]) is True, 'No Creature loaded'
		activeCreature = self.creatureManager.activeCreature
		#print(self.creatureManager.activeCreature.size)
		activeCreature.size *= 20
		self.updateCreature()

	def updateCreature(self):
		activeCreature = self.creatureManager.activeCreature
		self.eventHandler = eventhandler.EventHandler()
		subp = activeCreature.baseHinge.getPart().getAllSubParts(WINDOWSIZE/2, activeCreature.size)
		for p, pos, size in subp:
			self.eventHandler.registerDict(p.getHandles())
		self.activeAllHinges = activeCreature.baseHinge.getPart().getAllSubHinges(WINDOWSIZE/2, activeCreature.size)

	def onKey(self, ev):
		if ev.unicode == 'r':
			print()
			print()
			print()
			print('Resetting...')
			self.__init__()
		elif ev.unicode == '\t':
			self.currentCreatureIndex = (self.currentCreatureIndex + 1) % self.creatureCount
			self.setActiveCreature(self.currentCreatureIndex)
			print('Swapped Creature to', self.creatureManager.activeCreature.name)
		elif ev.unicode == 's':
			print()
			self.creatureManager.saveActiveCreature('savedCreature.json')

	def update(self, dt):
		self.eventHandler.update(dt)
		self.fps_display.change_text(str(int(self.clock.get_fps())) + " fps")

	def onActiveEvent(self, ev):
		pass

	def draw(self):
		self.creatureManager.activeCreature.draw(WINDOWSIZE/2)
		self.fps_display.draw([10, 10])
		if self.mouseHinge.hasPart():
			self.mouseHinge.getPart().draw(self.mouseHinge.position, 10)
			# 10: Size
		self.mouseHinge.draw(self.mouseHinge.position, 10)
		self.partSelector.draw()

	def onMouseMotion(self, ev):
		self.mousePos = Vec2d(ev.pos[0], ev.pos[1])
		self.eventHandler.mouseMovement(self.mousePos)
		self.mouseHinge.setPosition(self.mousePos)

	def onClick(self, ev):
		print(ev)
		if ev.button == 1:
			for h, pos, size in self.activeAllHinges:
				print(ev.pos, pos, size)
				if h.collides(Vec2d(ev.pos[0], ev.pos[1]), pos, size*5):
					if self.mouseHinge.hasPart():
						h.setPart(copy.deepcopy(self.mouseHinge.getPart()))
						h.getPart().hinge = h
						self.mouseHinge.setPart(None)
						print('Mouse -> Click')
						self.updateCreature()
					else:
						self.mouseHinge.setPart(copy.deepcopy(h.getPart()))
						h.setPart(None)
						print('Click -> Mouse')
						self.updateCreature()
			self.partSelector.onClick(ev)
		elif ev.button == 3:
			if self.mouseHinge.hasPart():
				self.mouseHinge.setPart(None)


mainloop((WINDOWSIZE, TITLE, FPS), CreatureCreator, draw.white)
