import draw
from vector2 import Vec2d
import math

import collision


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
			partsList.append((self, position, size))
		for hinge in self.getHinges():
			if hinge.hasPart():
				relpos = hinge.position * size
				relpos.rotate(hinge.rotation)
				newpos = relpos + position
				if getHinges and not onlyGetEmptyHinges:
					partsList.append((hinge, newpos, size))
				elif not getHinges:
					partsList.append((hinge.getPart(), newpos, size))
				subParts = hinge.getPart().getAllSubParts(newpos, hinge.getPart().size*size, getHinges, onlyGetEmptyHinges)
				partsList += subParts
			else:
				if getHinges:
					relpos = hinge.position * size
					relpos.rotate(hinge.rotation)
					newpos = relpos + position
					partsList.append((hinge, newpos, size))
		#log(self.name, position, partsList, level='MATH')
		return partsList

	def getAllSubHinges(self, position, size):
		hingeList = []
		subList = []
		for hinge in self.getHinges():
			relpos = hinge.position * size
			relpos.rotate(hinge.rotation)
			newpos = relpos + position
			if hinge.hasPart():
				subHinges = hinge.getPart().getAllSubHinges(newpos, hinge.getPart().size*size)
				subList += subHinges
			hingeList.append((hinge, newpos, size))
		hingeList += subList
		return hingeList

	def getHinges(self):
		return []

	def update(self, dt):
		pass

	def collides(self, collpos, ownpos, size):
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

	def setSize(self, size, setOrigSize=False):
		self.size = size
		if self.sizeRange[0] <= self.size <= self.sizeRange[1]:
			pass
		else:
			if self.size > self.sizeRange[1]:
				self.size = self.sizeRange[1]
			else:
				self.size = self.sizeRange[0]
		if setOrigSize:
			self.origSize = self.size
		self.update(0.0)

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
			classDict['stats'] = {}
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
		self.origSize = self.size
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

				mod = self.structMod(d['name'] if 'name' in d else None, pos, size)
				if mod:
					p, s = mod
					pos += p
					size += s

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

				mod = self.structMod(d['name'] if 'name' in d else None, pos, size)
				if mod:
					p, s = mod
					pos += p
					size += s

				color = d['color']
				vertices = d['vertices']
				r = d['radius']*size
				steps = int(360/vertices)
				points = [Vec2d(math.sin(math.radians(x))*r, math.cos(math.radians(x))*r)+pos for x in range(0, 360, steps)]
				#print(points)
				draw.polygon(points, color)
				#draw.points2(points, color, size=10.0, alpha=255.0)
			elif d['draw'] == 'poly':
				color = d['color']
				points = d['points']
				for p in points:
					p *= size
					if self.hinge:
						p.rotate(self.hinge.rotation)
					p += position
				draw.polygon(points, color)

	def collides(self, collisionPoint, ownPosition, ownSize):
		#print(collisionPoint, ownPosition, ownSize)
		self.collisionPolys = []
		for d in self.structure:
			if d['draw'] == 'point':
				pos = Vec2d(d['position'])*ownSize
				if self.hinge:
					pos.rotate(self.hinge.rotation)
				pos += ownPosition

				mod = self.structMod(d['name'] if 'name' in d else None, pos, ownSize)
				if mod:
					p, s = mod
					pos += p
					ownSize += s

				s = d['size'] * ownSize
				self.collisionPolys.append([pos-Vec2d(s, s), pos-Vec2d(s, -s), pos-Vec2d(-s, -s), pos-Vec2d(-s, s)])
			elif d['draw'] == 'rect':
				p1, p3 = d['positions']
				p1 = Vec2d(p1)*ownSize
				p3 = Vec2d(p3)*ownSize
				if self.hinge:
					p1.rotate(self.hinge.rotation)
					p3.rotate(self.hinge.rotation)
				p1 += ownPosition
				p3 += ownPosition
				p2 = Vec2d(p1.x, p3.y)
				p4 = Vec2d(p3.x, p1.y)
				self.collisionPolys.append([p1, p2, p3, p4])
			elif d['draw'] == 'ngon':
				pos = Vec2d(d['position'])*ownSize
				if self.hinge:
					pos.rotate(self.hinge.rotation)
				pos += ownPosition

				mod = self.structMod(d['name'] if 'name' in d else None, pos, ownSize)
				if mod:
					p, s = mod
					pos += p
					ownSize += s

				vertices = d['vertices']
				r = d['radius']*ownSize
				steps = int(360/vertices)
				points = [Vec2d(math.sin(math.radians(x))*r, math.cos(math.radians(x))*r)+pos for x in range(0, 360, steps)]
				self.collisionPolys.append(points)
			elif d['draw'] == 'poly':
				points = d['points']
				for p in points:
					p *= ownSize
					if self.hinge:
						p.rotate(self.hinge.rotation)
					p += ownPosition
				self.collisionPolys.append(points)
		for poly in self.collisionPolys:
			if collision.polyPointCollides(poly, collisionPoint):
				return True
		return False

	def structMod(self, structName, pos, size):
		return False


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

	#def draw(self, position, size):
	#	for d in self.structure:
	#		if d['draw'] == 'point':
	#			pos = Vec2d(d['position'])*size + position
	#			if 'name' in d:
	#				if d['name'] == 'pupil':
	#					v = self.mousePos-pos
	#					if v.get_length() > 10:
	#						v = v.normalized() * 10
	#					pos += v
	#				elif d['name'] == 'iris':
	#					v = self.mousePos-pos
	#					if v.get_length() > 20:
	#						v = v.normalized() * 20
	#					pos += v
	#				elif d['name'] == 'subiris':
	#					v = self.mousePos-pos
	#					if v.get_length() > 30:
	#						v = v.normalized() * 30
	#					pos += v
	#			color = d['color']
	#			draw.point(pos, color, size * d['size'], alpha=255.0)

	def onMouse(self, position):
		self.mousePos = position

	def getHandles(self):
		return {'mouseMovement': self.onMouse}

	def structMod(self, structName, pos, size):
		if structName == 'pupil':
			v = self.mousePos-pos
			if v.get_length() > 10:
				v = v.normalized() * 10
		elif structName == 'iris':
			v = self.mousePos-pos
			if v.get_length() > 20:
				v = v.normalized() * 20
		elif structName == 'subiris':
			v = self.mousePos-pos
			if v.get_length() > 30:
				v = v.normalized() * 30
		else:
			return False
		return v, 1


class Paddle(GeneratedPart):
	def __init__(self, hinge):
		GeneratedPart.__init__(self, hinge)
		self.sceneName = False
		self.paddleEffect = 0
		self.paddleSpeed = 0
		self.time = 0.0
		self.onSceneChange('CreatureCreator')

	def update(self, dt):
		self.time += dt

	def onBodyMovement(self, mv):
		raise NotImplementedError

	def onSceneChange(self, sceneName):
		self.sceneName = sceneName
		if sceneName == 'CreatureCreator':
			self.paddleEffect = 0.1
			self.paddleSpeed = 4.5
		else:
			self.paddleEffect = 0
			self.paddleSpeed = 0

	def getHandles(self):
		return {'bodyMovement': self.onBodyMovement, 'update': self.update}

	def paddleMod(self, segNum):
		mod = math.sin((self.paddleSpeed * self.time) + (segNum*0.5))
		mod *= (self.paddleEffect * segNum)
		return mod

	def structMod(self, structName, pos, size):
		if 'seg' in structName:
			segNum = int(structName[-1])
			mod = self.paddleMod(segNum)
			relpos = Vec2d(mod, 0).rotated(self.hinge.rotation) * size
			print(segNum, mod, relpos)
			return relpos, 1
		return False


CLASSNAME2CLASS = {'Base': Base, 'Mouth': Mouth, 'Eye': Eye, 'Paddle': Paddle}
