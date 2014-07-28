from draw import *
from vector2 import Vec2d
from collision import polyPointCollides
#
import font
import pygame.font


class Label(object):
	def __init__(self, text, position, size, myfont, side='centered'):
		self.text = text
		self.position = position
		self.size = size
		self.renderText = font.RenderText(self.text, [0, 0, 0], myfont)
		if side == 'left':
			pass
		elif side == 'right':
			self.position.x -= len(self.text) * size
		else:
			self.position.x -= (len(self.text) * size) / 3.0
		self.position.y -= self.size / 2.0

	def draw(self):
		#points2((self.position, self.position), green, size=9)
		self.renderText.draw(self.position)


class Button(object):
	def __init__(self, text, position, width, myfont):
		self.text = text
		self.position = position
		self.width = width
		height = width / len(text) * 2.0
		self.height = height
		p1 = position + Vec2d(-width, height)
		p2 = position + Vec2d(width, height)
		p3 = position + Vec2d(width, -height)
		p4 = position + Vec2d(-width, -height)
		self.points = (p1, p2, p3, p4)
		self.highlighted = False

		textSize = height

		self.label = Label(text, Vec2d(position), textSize, myfont)

	def draw(self):
		color = red if self.highlighted else blue
		polygon(self.points, color, aa=True, alpha=255.0, stipple_pattern=None)
		lines(self.points, color, width=3, aa=True, closed=1)
		points2(self.points, color, size=9)
		#points2((self.position, self.position), red, size=5)
		self.label.draw()

	def collides(self, point):
		return polyPointCollides(self.points, point)


class Menu(object):
	def __init__(self, screenSize, callback, buttons=['Cancel', 'Okee', 'OfCOOurs'], title='Wähle deine Antwort', buttonScroll=False):
		self.screenSize = screenSize
		self.middle = screenSize / 2
		self.scale = screenSize / 6

		self.myfont = pygame.font.SysFont("Courier New", 32, bold=True)

		self.buttonTexts = buttons
		self.buttonScroll = buttonScroll

		self.callback = callback
		charWidth = (self.scale.x / 8.0)
		if buttonScroll:
			self.buttonScrollIndex = 0
			self.scrollButtons()
		else:
			self.setButtons(buttons)

		labelPos = self.middle - Vec2d(0, self.scale.y / 2.0)
		textSize = charWidth
		#textSize = (charWidth * len(title) * 0.5) / len(title) * 2.0
		self.titleLabel = Label(title, labelPos, textSize, self.myfont, side='centered')

	def scrollButtons(self):
		index = self.buttonScrollIndex
		buttonNum = 3
		b = self.buttonTexts[index:index+buttonNum]
		if index > 0:
			buttons = ['<--'] + b
		else:
			buttons = b
		if index + buttonNum < len(self.buttonTexts):
			buttons += ['-->']
		self.setButtons(buttons)

	def setButtons(self, buttons):
		charWidth = (self.scale.x / 8.0)
		totalLength = sum([charWidth * len(text) for text in buttons])
		self.totalLength = totalLength
		currLength = -(totalLength / 2.0)
		self.buttons = []
		for i in range(len(buttons)):
			text = buttons[i]
			step = charWidth * len(text) * 0.5
			currLength += step
			posx = self.middle.x + currLength
			currLength += step
			pos = Vec2d(posx, self.middle.y)
			print('Position', pos)
			b = Button(text, pos, step * 0.9, self.myfont)
			self.buttons.append(b)

	def getCollision(self, pos):
		for b in self.buttons:
			if b.collides(pos):
				return b
		return False

	def draw(self):
		#p2 = self.middle - Vec2d(self.totalLength / 2.0, 0)
		#p3 = self.middle + Vec2d(self.totalLength / 2.0, 0)
		#points2((self.middle, p2, p3), blue, size=15)
		for b in self.buttons:
			b.draw()
		self.titleLabel.draw()

	def mouseMovement(self, mousePosition):
		result = self.getCollision(mousePosition)
		for b in self.buttons:
			b.highlighted = False
		if result:
			#print('highlight', result)
			result.highlighted = True

	def mouseButton(self, event):
		pos = Vec2d(event.pos[0], event.pos[1])
		result = self.getCollision(pos)
		if self.buttonScroll and result:
			if result.text in ['<--', '-->']:
				if result.text == '<--':
					self.buttonScrollIndex -= 1
				else:
					self.buttonScrollIndex += 1
				self.scrollButtons()
				return False
		if result:
			self.callback(result.text)


from mainloop import init, mainloop, StdMain


class MenuMain(StdMain):
	def __init__(self):
		def callback(result):
			print(result)
			self.cb(result)
		self.m = Menu(WINDOWSIZE, callback)
		for b in self.m.buttons:
			print(b.text)
			print(b.points)

	def cb(self, result):
		if result == 'Cancel':
			self.m = Menu(WINDOWSIZE, self.cb, ['Ich bin ein Toaster', 'Du bist ein Toaster'], title='Du bist ein Baum')
		else:
			self.m = Menu(WINDOWSIZE, self.cb)

	def draw(self):
		self.m.draw()

	def onMouseMotion(self, ev):
		#print(ev)
		self.m.mouseMovement(Vec2d(ev.pos[0], ev.pos[1]))

	def onClick(self, ev):
		self.m.mouseButton(ev)

if __name__ == "__main__":

	TITLE = 'MenuTest'
	FPS = 60
	WINDOWSIZE = Vec2d(1920, 1080) * 0.8
	WINDOWSIZE = Vec2d(int(WINDOWSIZE[0]), int(WINDOWSIZE[1]))
	init(WINDOWSIZE, '--Loading--')
	mainloop((WINDOWSIZE, TITLE, FPS), MenuMain, white)
