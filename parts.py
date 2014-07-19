import draw
from vector2 import Vec2d
from log import *


class Hinge(object):

	def __init__(self, position, parent=None):
		self.parent = parent
		self.position = position
		self.part = None
		self.color = draw.blue
		self.size = 0.2
		# self.hingeType = 0
		# {0:'ALL_THINGS', 1:'SMALL_SHIT_ONLY', 2:'...'}
		if parent:
			self.name = 'Hinge on '+self.parent.name
		else:
			self.name = 'Hinge on FakePart'

	def collides(self, ownpos, collpos, size):
		distancesqrt = ownpos.get_dist_sqrd(collpos)
		radius = self.size*size
		log(distancesqrt, radius**2, ownpos, collpos, level='MATH')
		return distancesqrt < (radius ** 2)

	def hasPart(self):
		return True if self.part else False

	def getPart(self):
		return self.part

	def setPart(self, part):
		self.part = part

	def setPosition(self, position):
		self.position = position

	def draw(self, position, size):
		draw2d.circle(self.color, position, self.size * size)
		log('Drawn', self.name, '@', position, 'sized', self.size * size, level='DRAW')


# ## ## ## ## ## ## ## ## ## ## ## ## ## #
#                                        #
#             All them Parts             #
#                                        #
# ## ## ## ## ## ## ## ## ## ## ## ## ## #


class Part(object):

	def __init__(self, hinge):
		self.hinge = hinge
		self.size = 1
		self.sizeRange = [0.5, 2]
		self.rotation = 0
		self.name = 'UnnamedPart:'+str(type(self))
		self.subParts = []
		self.color = draw2d.green

	def draw(self, position, size):
		draw2d.circle(self.color, position, self.size*size)
		log('Drawn', self.name, '@', position, 'sized', self.size * size, level='DRAW')

	def drawSubParts(self, position, size, drawHinges=False):
		self.draw(position, size)
		for hinge in self.getHinges():
			if hinge.hasPart():
				relpos = hinge.position * size
				relpos.rotate(self.rotation)
				newpos = relpos + position
				hinge.getPart().drawSubParts(newpos, hinge.getPart().size*size, drawHinges)
			else:
				if drawHinges:
					relpos = hinge.position * size
					relpos.rotate(self.rotation)
					newpos = relpos + position
					hinge.draw(newpos, size)

	def getAllSubParts(self, position, size, getHinges=False, onlyGetEmptyHinges=True):
		partsList = []
		if not getHinges:
			partsList.append((self, position))
		for hinge in self.getHinges():
			if hinge.hasPart():
				relpos = hinge.position * size
				relpos.rotate(self.rotation)
				newpos = relpos + position
				if getHinges and not onlyGetEmptyHinges:
					partsList.append((hinge, newpos))
				elif not getHinges:
					partsList.append((hinge.getPart(), newpos))
				subParts = hinge.getPart().getAllSubParts(newpos, hinge.getPart().size*size, getHinges, onlyGetEmptyHinges)
				partsList += subParts
			else:
				if getHinges:
					relpos = hinge.position * size
					relpos.rotate(self.rotation)
					newpos = relpos + position
					partsList.append((hinge, newpos))
		#log(self.name, position, partsList, level='MATH')
		return partsList

	def drawHinges(self, position, size):
		raise NotImplementedError

	def getHinges(self):
		return []

	def update(self, dt):
		pass

	def collides(self, ownpos, collpos, size):
		distancesqrt = ownpos.get_dist_sqrd(collpos)
		radius = self.size*size
		return distancesqrt < (radius ** 2)

	def modSize(self, modifier):
		self.size *= modifier
		if self.sizeRange[0] <= self.size <= self.sizeRange[1]:
			self.update()
		else:
			if self.size > self.sizeRange[1]:
				self.size = self.sizeRange[1]
			else:
				self.size = self.sizeRange[0]
		#self.update()

	def getHandles(self):
		return {}


#class Circle(Part):
#
#	def __init__(self, hinge, color=draw2d.green):
#		Part.__init__(self, hinge)
#		self.name = 'Body_Circle'
#		self.color = color
#		self.size = 1
#		self.sizeRange = [0.5, 2]
#		self.num_hinges = 5
#		#num_hinges = int((self.size*math.pi*2)/25)
#		self.hinges = []
#		for i in range(5):
#			self.hinges.append(Hinge(Vec2d(0, 0), self))
#		self.update()
#
#	def update(self):
#		self.updateHinges()
#
#	def updateHinges(self):
#		for i in range(self.num_hinges):
#			vec = Vec2d(self.size*0.9, 0).rotated(i*360.0/self.num_hinges)
#			self.hinges[i].setPosition(vec)
#
#	def getHinges(self):
#		return self.hinges


class GenericPart(Part):

	def __init__(self, d):
		#{
		# 'attatchmentPoints': [[10, 0], [7, 7], [0, 10], [7, -7], [0, -10], [-7, -7], [-10, 0], [-7, 7]],
		# 'partClass': 'BodyBase',
		# 'stats': {'health': 10, 'energyCost': 2, 'mass': 2},
		# 'name': 'BasePart',
		# 'structure': [{'size': 10, 'position': [0, 0], 'name': 'point'}]
		#}
		pass

	def draw(self):
		for s in self.structure:
			if 'size' in s:
				size = s['size']
			else:
				size = 1
			if 'color' in s:
				color = s['color']
			else:
				color = draw.black
			if 'position' in s:
				pos = s['position']
			else:
				raise NotImplementedError
			draw.point(pos, color, size)

	def getClass(d):
		classDict = {}
		classDerv = (GeneratedPart)
		if 'name' in d:
			className = d['name']
		else:
			className = 'UnnamedPart | FIXME'
		if 'stats' in d:
			classDict['stats'] = d['stats']
		else:
			self.stats = {}
		if 'structure' in d:
			classDict['structure'] = d['structure']
			#structure = [{'size': 10, 'position': [0, 0], 'name': 'point'},]
		else:
			raise NotImplementedError
		if 'attatchmentPoints' in d:
			classDict['hinges'] = [Hinge(position, self) for position in d['attatchmentPoints']]
		else:
			classDict['hinges'] = []
		return type(className, classDerv, classDict)


class GeneratedPart(GenericPart):
	pass


class BodyBase(GenericPart):

	def onCollision(self):
		raise NotImplementedError

	def getHandles(self):
		return {'collision': self.onCollision}


class Mouth(GenericPart):

	def __init__(self, hinge):
		Part.__init__(self, hinge)
		self.name = 'Mouth'
		self.size = 0.2
		self.sizeRange = [0.1, 0.5]
		self.stat_MouthNum = 1
		self.stat_Mass = 1
		self.color = draw2d.blue

	def onCollision(self):
		raise NotImplementedError

	def getHandles(self):
		return {'collision': self.onCollision}

CLASSNAME2CLASS = {'BodyBase': BodyBase, 'GenericPart': GenericPart, 'Mouth': Mouth}
