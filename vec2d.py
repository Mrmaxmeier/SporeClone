import math

# VECTOR2 is tollar und funzt


class Vec2D(object):

	def __init__(self, x=0, y=0):
		self.x, self.y = x, y

	def normalize(self, length=1):
		newVec = self.normalized(length)
		self.x, self.y = newVec.x, newVec.y

	def normalized(self, length=1):
		l = 1 / self.length() * length
		x, y = self.x, self.y
		return Vec2D(x * l, y * l)

	def length(self):
		return math.sqrt(self.x ** 2 + self.y ** 2)

	def rotate(self, rotation):
		pass

	def distance(self, vec2D):
		relVec = Vec2D(self.x - vec2D.x, self.y - vec2D.y)
		return relVec.length()

	def add(self, vec2D):
		newVec = Vec2D(self.x+vec2D.x, self.y+vec2D.y)
		return newVec

	def cross(self, vec2D):
		pass


class Rotation(object):

	def __init__(self, angle):
		self.setAngle(angle)

	def setAngle(self, angle):
		self.angle = angle
		self.radian = math.radians(angle)

	def setRadian(self, radian):
		self.angle = math.degrees(radian)
		self.radian = radian


def vecFd(rotation, magnitude=1):
	#rotation in degrees
	r = math.radians(rotation)
	x, y = math.sin(r) * magnitude, math.cos(r) * magnitude
	return Vec2D(x, y)


def rotationFromVec2d(vec2d):
	print('NOT IMPLEMENTED')
	return 0
