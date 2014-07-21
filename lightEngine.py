from mainloop import init, mainloop, StdMain
from vector2 import Vec2d

import draw
import math


TITLE = 'LightEngineTest'
FPS = 30
WINDOWSIZE = (1200, 720)
init(WINDOWSIZE, '--Loading--')


class Intersect(object):

	def __init__(self, x, y, param=False):
		self.x = x
		self.y = y
		self.param = param

	def draw(self):
		draw.circle(Vec2d(self.x, self.y), 5, draw.red)


class Line(object):

	def __init__(self, vec1, vec2):
		self.a = vec1
		self.b = vec2
		self.d = vec2 - vec1

	def draw(self, color=draw.red):
		draw.line(self.a, self.b, color)


def getIntersection(ray, segment):
	# RAY in parametric:
	#	Point + Direction * T1
	r_px = ray.a.x
	r_py = ray.a.y
	r_dx = ray.b.x - ray.a.x
	r_dy = ray.b.y - ray.a.y

	# SEGMENT in parametric:
	#	Point + Direction * T2
	s_px = segment.a.x
	s_py = segment.a.y
	s_dx = segment.b.x - segment.a.x
	s_dy = segment.b.y - segment.a.y

	# Are they parallel? If so, no intersect
	r_mag = math.sqrt(r_dx*r_dx+r_dy*r_dy)
	s_mag = math.sqrt(s_dx*s_dx+s_dy*s_dy)
	# todo: fix zerodivision error handling
	try:
		if r_dx/r_mag == s_dx/s_mag and r_dy/r_mag == s_dy/s_mag:
			return None
	except ZeroDivisionError:
		return None

	# SOLVE FOR T1 & T2
	# r_px+r_dx*T1 = s_px+s_dx*T2 && r_py+r_dy*T1 = s_py+s_dy*T2
	# ==> T1 = (s_px+s_dx*T2-r_px)/r_dx = (s_py+s_dy*T2-r_py)/r_dy
	# ==> s_px*r_dy + s_dx*T2*r_dy - r_px*r_dy = s_py*r_dx + s_dy*T2*r_dx - r_py*r_dx
	# ==> T2 = (r_dx*(s_py-r_py) + r_dy*(r_px-s_px))/(s_dx*r_dy - s_dy*r_dx)

	try:
		T2 = (r_dx*(s_py-r_py) + r_dy*(r_px-s_px))/(s_dx*r_dy - s_dy*r_dx)
	except ZeroDivisionError:
		T2 = (r_dx*(s_py-r_py) + r_dy*(r_px-s_px))/(s_dx*r_dy - s_dy*r_dx-0.01)

	try:
		T1 = (s_px+s_dx*T2-r_px)/r_dx
	except ZeroDivisionError:
		T1 = (s_px+s_dx*T2-r_px)/(r_dx-0.01)

	# Must be within parametic whatevers for RAY/SEGMENT
	if T1 < 0:
		return None
	if T2 < 0 or T2 > 1:
		return None

	# Return the POINT OF INTERSECTION
	return r_px + r_dx * T1, r_py + r_dy * T1, T1


def getIntersect(ray, segment):
	intersect = getIntersection(ray, segment)
	if intersect:
		x, y, t1 = intersect
		return Vec2d(x, y)
	else:
		return False


def getClosestIntersect(ray, segments, toPoint):
	closestIntersect = None
	closest = False
	for segment in segments:
		result = getIntersect(ray, segment)
		if result:
			draw.point(result, draw.red, 4)
			distance = toPoint.get_distance(result)
			if distance == 0:
				#print(distance, result)
				continue
			if not closest:
				closest = distance
				closestIntersect = result
			if distance < closest:
				closest = distance
				closestIntersect = result
	return closestIntersect


class Poly():
	def __init__(self, vecList):
		self.pointList = []
		self.vecList = []

	def addPoint(self, px, py):
		self.pointList.append((px, py))
		self.vecList.append(Vec2d(px, py))

	def draw(self):
		#draw.polygon(self.pointList, draw.green)
		if len(self.pointList) < 2:
			draw.points2(self.pointList, draw.green, 5)
		else:
			draw.lines(self.pointList, draw.green, width=3, closed=True)

	def deletePoints(self):
		self.pointList = []
		self.vecList = []


def genPolys():
	l = []
	border = 5
	poly = Poly([])
	poly.addPoint(border, border)
	poly.addPoint(WINDOWSIZE[0]-border, border)
	poly.addPoint(WINDOWSIZE[0]-border, WINDOWSIZE[1]-border)
	poly.addPoint(border, WINDOWSIZE[1]-border)
	l.append(poly)
	return l


def getSegments(polyList):
	l = []
	for poly in polyList:
		for i in range(len(poly.vecList)):
			seg_a, seg_b = (poly.vecList[i], poly.vecList[i - 1])
			segment = Line(seg_a, seg_b)
			l.append(segment)
	return l


def addLine2Dict(line, d):
	d[line.d.get_angle()] = line


def getRays(mousePos, polyList):
	lsorted = {}
	for poly in polyList:
		for i in range(len(poly.vecList)):
			#
			draw.point(poly.vecList[i], draw.blue, 10)
			#
			line = Line(mousePos, poly.vecList[i])
			addLine2Dict(rotateLine(line, -0.001), lsorted)
			addLine2Dict(line, lsorted)
			addLine2Dict(rotateLine(line, 0.001), lsorted)
	lsortedkeys = sorted(lsorted)
	l = []
	for key in lsortedkeys:
		l.append(lsorted[key])
	return l


def rotateLine(lineObj, rotation):
	d = lineObj.d
	rotated = d.rotated(rotation)
	d = rotated - d
	b = lineObj.b + d
	line = Line(lineObj.a, b)
	return line


def sortPolyByAngle(poly, point):
	pd = {}
	for p in poly:
		d = p - point
		angle = d.get_angle()
		pd[angle] = p
	pdkeys = sorted(pd)
	pl = []
	for key in pdkeys:
		pl.append(pd[key])
	return pl


class LightEngineTest(StdMain):

	def __init__(self):
		self.polys = genPolys()
		self.segments = getSegments(self.polys)
		self.mousePos = Vec2d(0, 0)
		self.currPoly = Poly([])

	def onKey(self, ev):
		pass

	def update(self, dt):
		pass

	def onActiveEvent(self, ev):
		pass

	def draw(self):
		for p in self.polys[1:]:
			p.draw()

		lightPoly = []
		for ray in getRays(self.mousePos, self.polys):
			#ray.draw()
			isect = getClosestIntersect(ray, self.segments, self.mousePos)
			if isect:
				lightPoly.append(isect)
		lightPoly = sortPolyByAngle(lightPoly, self.mousePos)
		#draw.polygon(lightPoly, draw.white)
		draw.lines(lightPoly, draw.blue, width=20, aa=True, closed=1)
		for p in lightPoly:
			draw.point(p, draw.black, 15)

	def onMouseMotion(self, ev):
		self.mousePos = Vec2d(ev.pos[0], ev.pos[1])

	def onClick(self, ev):
		if ev.button == 1:
			self.currPoly.addPoint(ev.pos[0], ev.pos[1])
		else:
			self.currPoly.deletePoints()
		self.polys = genPolys()  + [self.currPoly]
		self.segments = getSegments(self.polys)
		print(self.currPoly.vecList)


mainloop((WINDOWSIZE, TITLE, FPS), LightEngineTest, draw.white)
