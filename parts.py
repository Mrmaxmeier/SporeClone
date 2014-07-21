import draw
from vector2 import Vec2d
import math


class Hinge(object):

	def __init__(self, position, parent=None, rotation=0):
		self.parent = parent
		self.position = Vec2d(position)
		self.origPosition = Vec2d(position)
		self.part = None
		self.color = draw.blue
		self.size = 0.2
		self.rotation = rotation
		if parent:
			self.name = 'Hinge on '+self.parent.name
		else:
			self.name = 'Hinge on FakePart'

	def collides(self, ownpos, collpos, size):
		distancesqrt = ownpos.get_dist_sqrd(collpos)
		radius = self.size*size
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
		draw.point(position, draw.blue, self.size * size * 3)


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
		#self.rotation = 0

	def draw(self, position, size):
		draw.point(draw.blue, position, self.size*size)

	def drawSubParts(self, position, size, drawHinges=False):
		self.draw(position, size)
		for hinge in self.getHinges():
			if hinge.hasPart():
				relpos = hinge.position * size
				relpos.rotate(hinge.rotation)
				newpos = relpos + position
				hinge.getPart().drawSubParts(newpos, hinge.getPart().size*size, drawHinges)
			else:
				if drawHinges:
					relpos = hinge.position * size
					relpos.rotate(hinge.rotation)
					newpos = relpos + position
					hinge.draw(newpos, size)

	def getAllSubParts(self, position, size, getHinges=False, onlyGetEmptyHinges=True):
		partsList = []
		if not getHinges:
			partsList.append((self, position))
		for hinge in self.getHinges():
			if hinge.hasPart():
				relpos = hinge.position * size
				relpos.rotate(hinge.rotation)
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
					relpos.rotate(hinge.rotation)
					newpos = relpos + position
					partsList.append((hinge, newpos))
		#log(self.name, position, partsList, level='MATH')
		return partsList

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
			self.update(0.0)
		else:
			if self.size > self.sizeRange[1]:
				self.size = self.sizeRange[1]
			else:
				self.size = self.sizeRange[0]
		#self.update()

	def setSize(self, size):
		self.size = size
		if self.sizeRange[0] <= self.size <= self.sizeRange[1]:
			self.update(0.0)
		else:
			if self.size > self.sizeRange[1]:
				self.size = self.sizeRange[1]
			else:
				self.size = self.sizeRange[0]

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
	def __init__(self):
		#{
		# 'attatchmentPoints': [[10, 0], [7, 7], [0, 10], [7, -7], [0, -10], [-7, -7], [-10, 0], [-7, 7]],
		# 'partClass': 'BodyBase',
		# 'stats': {'health': 10, 'energyCost': 2, 'mass': 2},
		# 'name': 'BasePart',
		# 'structure': [{'size': 10, 'position': [0, 0], 'name': 'point'}]
		#}
		pass

	def getClass(self, d):
		classDict = {}
		if 'partClass' in d:
			classDerv = (CLASSNAME2CLASS[d['partClass']],)
		else:
			classDerv = (GeneratedPart,)
		if 'name' in d:
			className = d['name']
			classDict['name'] = d['name']
		else:
			className = 'UnnamedGeneratedPart | FIXME'
			classDict['name'] = 'UnnamedGeneratedPart | FIXME'
		if 'stats' in d:
			classDict['stats'] = d['stats']
		else:
			self.stats = {}
		if 'structure' in d:
			struct = d['structure']
			struct.sort(key=lambda s: s['layer'] if 'layer' in s else 0)
			classDict['structure'] = struct
			#structure = [{'size': 10, 'position': [0, 0], 'name': 'point'},]
		else:
			raise NotImplementedError
		classDict['classDict'] = d
		return type(className, classDerv, classDict)


class GeneratedPart(GenericPart):
	def __init__(self, hinge):

		self.hinge = hinge
		self.size = 1
		self.sizeRange = [0.5, 2]
		self.rotation = 0
		self.hinges = []
		if 'attatchmentPoints' in self.classDict:
			for d in self.classDict['attatchmentPoints']:
				self.hinges.append(Hinge(Vec2d(d['x'], d['y']), self, rotation=d['rot']))

	def getHinges(self):
		return self.hinges

	def draw(self, position, size):
		size *= self.size
		for d in self.structure:
			if d['draw'] == 'point':
				pos = Vec2d(d['position'])*size
				if self.hinge:
					pos.rotate(self.hinge.rotation)
				pos += position
				color = d['color']
				draw.point(pos, color, size * d['size'], alpha=255.0)
			elif d['draw'] == 'rect':
				p1, p3 = d['positions']
				p1 = Vec2d(p1)*size
				p3 = Vec2d(p3)*size
				if self.hinge:
					p1.rotate(self.hinge.rotation)
					p3.rotate(self.hinge.rotation)
				p1 += position
				p3 += position
				color = d['color']
				p2 = Vec2d(p1.x, p3.y)
				p4 = Vec2d(p3.x, p1.y)
				draw.polygon((p1, p2, p3, p4), color)
				#draw.points2((p1, p2, p3, p4), color, size=10.0, alpha=255.0)
			elif d['draw'] == 'ngon':
				pos = Vec2d(d['position'])*size
				if self.hinge:
					pos.rotate(self.hinge.rotation)
				pos += position
				color = d['color']
				vertices = d['vertices']
				r = d['radius']*size
				steps = int(360/vertices)
				points = [Vec2d(math.sin(math.radians(x))*r, math.cos(math.radians(x))*r)+pos for x in range(0, 360, steps)]
				#print(points)
				draw.polygon(points, color)
				#draw.points2(points, color, size=10.0, alpha=255.0)
			elif d['draw'] == 'poly':
				raise NotImplementedError


class Base(GeneratedPart):
	def __init__(self, hinge):
		GeneratedPart.__init__(self, hinge)
		self.origSize = self.size
		self.time = 0

	def onCollision(self):
		raise NotImplementedError

	def update(self, dt):
		self.time += dt
		mod = math.sin(self.time*2)*0.025
		self.size = self.origSize + mod
		for hinge in self.getHinges():
			hinge.setPosition(hinge.origPosition * (1+mod))

	def getHandles(self):
		return {'collision': self.onCollision, 'update': self.update}


class Mouth(GeneratedPart):
	def onCollision(self):
		raise NotImplementedError

	def getHandles(self):
		return {'collision': self.onCollision}


class Eye(GeneratedPart):
	def __init__(self, hinge):
		GeneratedPart.__init__(self, hinge)
		self.mousePos = False

	def draw(self, position, size):
		for d in self.structure:
			if d['draw'] == 'point':
				pos = Vec2d(d['position'])*size + position
				if 'name' in d:
					if d['name'] == 'pupil':
						v = self.mousePos-pos
						if v.get_length() > 10:
							v = v.normalized() * 10
						pos += v
					elif d['name'] == 'iris':
						v = self.mousePos-pos
						if v.get_length() > 20:
							v = v.normalized() * 20
						pos += v
					elif d['name'] == 'subiris':
						v = self.mousePos-pos
						if v.get_length() > 30:
							v = v.normalized() * 30
						pos += v
				color = d['color']
				draw.point(pos, color, size * d['size'], alpha=255.0)

	def onMouse(self, position):
		self.mousePos = position

	def getHandles(self):
		return {'mouseMovement': self.onMouse}


class Paddle(GeneratedPart):

	def onBodyMovement(self, mv):
		raise NotImplementedError

	def getHandles(self):
		return {'bodyMovement': self.onBodyMovement}


CLASSNAME2CLASS = {'Base': Base, 'Mouth': Mouth, 'Eye': Eye, 'Paddle': Paddle}
