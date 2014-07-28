from mainloop import mainloop, StdMain
from vector2 import Vec2d

import manager
import fileParser
import eventhandler
import parts

import draw
import font
import pygame
import copy

import json

import sys

import menu

import client
import queue


#

STARTUP_CREATURE = """{"name":"New Creature","structure":{"name":"Base","sizeMod":1,"attatched":{}}}"""

#


TITLE = 'CreatureCreator'
FPS = 60
WINDOWSIZE = Vec2d(1920, 1080) * 0.8
WINDOWSIZE = Vec2d(int(WINDOWSIZE[0]), int(WINDOWSIZE[1]))


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
				part = self.partManager.getPart(self.parts[row][p])(hinge)
				hinge.setPart(part)
				hingeRow.append(hinge)
			self.hinges.append(hingeRow)

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
						self.mouseHinge.setPart(p)
						break


class CreatureCreator(StdMain):

	def __init__(self):
		self.mousePos = Vec2d(0, 0)
		#Font
		self.myfont = pygame.font.SysFont("Courier New", 32, bold=True)
		self.fps_display = font.RenderText("", [0, 0, 0], self.myfont)
		self.creature_name = font.RenderText("...Loading...", [0, 0, 0], self.myfont)
		#Parts
		self.partManager = manager.PartManager()
		self.creatureManager = manager.CreatureManager(self.partManager)
		self.creatureManager.activeCreature = fileParser.loadCreature(STARTUP_CREATURE, self.partManager)()
		self.creatureManager.activeCreature.size *= 20
		self.creature_name.change_text(self.creatureManager.activeCreature.name)
		self.updateCreature()
		#
		#
		#
		#

		self.mouseHinge = parts.Hinge(Vec2d(0, 0))
		#self.mouseHinge.setPart(self.partManager.getPart('Eye')(self.mouseHinge))
		self.partSelector = PartSelector(self.partManager, WINDOWSIZE, self.mouseHinge)

		#

		self.menu = False

		#

		self.clientQueue = queue.Queue()
		self.clientThread = client.Client(self.clientQueue)
		self.clientThread.start()
		self.clientThread.send({'joined': 'creaturecreator'})

	def setActiveCreature(self, arg):
		avalible = self.creatureManager.getAvalibleCreatures()
		if isinstance(arg, int):
			crea = avalible[arg]
		elif isinstance(arg, str):
			crea = arg

		assert self.creatureManager.setActiveCreature(crea) is True, 'No Creature loaded'
		activeCreature = self.creatureManager.activeCreature
		#print(self.creatureManager.activeCreature.size)
		activeCreature.size *= 20
		self.updateCreature()
		self.creature_name.change_text(activeCreature.name)

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
			print('Pressed <TAB>')
		elif ev.unicode == 's':
			print('Saving Creature')
			self.creatureManager.saveActiveCreature('savedCreature.json')
		elif ev.unicode == 'o':
			def menuCallback(result):
				print(result)
				if result == 'Cancel':
					self.menu = False
					return
				self.setActiveCreature(result)
				self.menu = False
			b = ['Cancel']+self.creatureManager.getAvalibleCreatures()
			self.menu = menu.Menu(WINDOWSIZE, menuCallback, buttons=b, title='Open...?', buttonScroll=True)
		elif ev.unicode == 'm':
			def menuCallback(result):
				if result == 'Cancel':
					self.menu = False
					return
				elif result == 'Fetch Creatures':
					self.clientThread.send({'creature': {'request': 'ALL'}})
				elif result == 'Share current Creature':
					activeCreature = self.creatureManager.activeCreature
					json = activeCreature.getJson()
					self.clientThread.send({'creature': {'add': json}})
				else:
					print(result)
				self.menu = False
			b = ['Cancel', 'Fetch Creatures', 'Share current Creature']
			self.menu = menu.Menu(WINDOWSIZE, menuCallback, buttons=b, title='Actions?')

	def update(self, dt):
		self.eventHandler.update(dt)
		self.fps_display.change_text(str(int(self.clock.get_fps())) + " fps")
		try:
			d = self.clientQueue.get_nowait()
			self.handleServerData(d)
			self.clientQueue.task_done()
		except queue.Empty:
			pass

	def onActiveEvent(self, ev):
		pass

	def draw(self):
		if self.menu:
			self.menu.draw()
		else:
			self.creatureManager.activeCreature.draw(WINDOWSIZE/2)
			if self.mouseHinge.hasPart():
				self.mouseHinge.getPart().draw(self.mouseHinge.position, 10)
				# 10: Size
			self.mouseHinge.draw(self.mouseHinge.position, 10)
			self.partSelector.draw()
			self.fps_display.draw([10, 10])
			d = 20+20*len(self.creatureManager.activeCreature.name)
			self.creature_name.draw([WINDOWSIZE.x-d, 10])

	def onMouseMotion(self, ev):
		self.mousePos = Vec2d(ev.pos[0], ev.pos[1])
		self.eventHandler.mouseMovement(self.mousePos)
		self.mouseHinge.setPosition(self.mousePos)
		if self.menu:
			self.menu.mouseMovement(self.mousePos)

	def onClick(self, ev):
		if self.menu:
			self.menu.mouseButton(ev)
			return False

		button = ev.button
		positionVec = Vec2d(ev.pos[0], ev.pos[1])

		#
		key_mods = pygame.key.get_mods()
		# MacOS LClick + Alt -> MClick fix
		if sys.platform == 'darwin':
			if key_mods & pygame.KMOD_LALT or key_mods & pygame.KMOD_RALT:
				if button == 2:
					button = 1
					ev.button = 1
					print('modded Button')

		if button == 1:
			for h, pos, size in self.activeAllHinges:
				if h.collides(positionVec, pos, size*5):
					if self.mouseHinge.hasPart():
						h.setPart(copy.deepcopy(self.mouseHinge.getPart()))
						h.getPart().hinge = h
						self.mouseHinge.setPart(None)
						print('Mouse -> Click')
						self.updateCreature()
					else:
						self.mouseHinge.setPart(copy.deepcopy(h.getPart()))
						if key_mods & pygame.KMOD_LALT or key_mods & pygame.KMOD_RALT:
							pass
							#print('Leftclick w/ alternate', '(on stock OSX)')
						else:
							h.setPart(None)
						print('Click -> Mouse')
						self.updateCreature()
			self.partSelector.onClick(ev)
		elif button == 3:
			if self.mouseHinge.hasPart():
				self.mouseHinge.setPart(None)
		elif button == 4 or button == 5:
			sizeDirection = 0.1 if button == 4 else -0.1
			for h, pos, size in self.activeAllHinges:
				if h.hasPart():
					if h.collides(positionVec, pos, size*5):
						h.getPart().setSize(h.getPart().size + sizeDirection, setOrigSize=True)
						print('RESIZED')

	def handleServerData(self, d):
		print('ServerData', d)
		if 'creatures' in d:
			creatureList = d['creatures']
			for creatureDict in creatureList:
				creatureJson = json.dumps(creatureDict)
				self.creatureManager.loadJson(creatureJson)


creatureCreatorObj = mainloop((WINDOWSIZE, TITLE, FPS), CreatureCreator, draw.white)
creatureCreatorObj.clientThread.sockAlive = False
creatureCreatorObj.clientThread.close()
