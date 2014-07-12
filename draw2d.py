from OpenGL.GL import *
from math import *
from texture import Texture
from pygame.font import Font

black = 0,0,0,1
white = 1,1,1,1
red   = 1,0,0,1
green = 0,1,0,1
blue  = 0,0,1,1
cyan  = 0,1,1,1
magenta = 1,0,1,1
yellow = 1,1,0,1

def transparent(t, xxx_todo_changeme):
	(r,g,b,a) = xxx_todo_changeme
	return (r,g,b,t*a)

def setCol(xxx_todo_changeme1):
	(r,g,b,a) = xxx_todo_changeme1
	glColor4f(r,g,b,a)

def shape(shape, points):
	glBegin(shape)
	for x, y in points:
		glVertex2f(x, y)
	glEnd()

def poly(col, points):
	setCol(col)
	shape(GL_TRIANGLE_FAN, points)

def rect(col, pos1, pos2):
	(x1, y1) = pos1
	(x2, y2) = pos2
	setCol(col)
	shape(GL_QUADS, [(x1,y1), (x1,y2), (x2,y2), (x2,y1)])

def circle(col, position, r):
	r = int(r)
	(x, y) = position
	setCol(col)
	shape(GL_TRIANGLE_FAN, [(x + r*sin(a), y + r*cos(a))
				for a in [2*pi*x/r for x in range(r)]])

def sprite(tex, position, a=1):
	(x, y) = position
	setCol(transparent(a, white))
	glEnable(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D,tex.texID)
	glBegin(GL_QUADS)
	for dx, dy in [(0,0), (0,1), (1,1), (1,0)]:
		glTexCoord2f(dx,dy)
		glVertex2f(x+tex.w*dx, y+tex.h*dy)
	glEnd()
	glDisable(GL_TEXTURE_2D)

def text(text, font, pos, col=(255, 255, 255), a=1):
	img = font.render(text, True, col)
	tex = Texture(img)
	translated(pos,
		scaled, (0, img.get_height()/2), (1, -1),
			sprite, tex, (0,0), a)

fontcache = {}
def font(size, file=None):
	key = (size, file)
	if key in fontcache:
		return fontcache[key]
	font = Font(file, size)
	fontcache[key] = font
	return font

def texpoly(tex, xxx_todo_changeme6, points, a=1):
	(ox, oy) = xxx_todo_changeme6
	setCol(transparent(a, white))
	glEnable(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D,tex.texID)
	glBegin(GL_TRIANGLE_FAN)
	for x, y in points:
		dx, dy = 1.*(x-ox)/tex.w, 1.*(y-oy)/tex.h
		glTexCoord2f(dx,dy)
		glVertex2f(x, y)
	glEnd()
	glDisable(GL_TEXTURE_2D)

def texquads(tex, xxx_todo_changeme7, pointsa, pointsb, a=1):
	(ox, oy) = xxx_todo_changeme7
	setCol(transparent(a, white))
	glEnable(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D,tex.texID)
	glBegin(GL_QUAD_STRIP)
	points = [point
		for pair in zip(pointsa, pointsb)
		for point in pair]
	for x, y in points:
		dx, dy = 1.*(x-ox)/tex.w, 1.*(y-oy)/tex.h
		glTexCoord2f(dx,dy)
		glVertex2f(x, y)
	glEnd()
	glDisable(GL_TEXTURE_2D)


def with_transform(transform, fun, *args, **kwd):
	glPushMatrix()
	transform()
	fun(*args, **kwd)
	glPopMatrix()

def translated(xxx_todo_changeme8, fun, *args, **kwd):
	(x, y) = xxx_todo_changeme8
	f = lambda: glTranslatef(x, y, 0)
	with_transform(f, fun, *args, **kwd)

def translate(xxx_todo_changeme9, xxx_todo_changeme10):
	(tx, ty) = xxx_todo_changeme9
	(x, y) = xxx_todo_changeme10
	return tx+x, ty+y

def rotated(xxx_todo_changeme11, a, fun, *args, **kwd):
	(x, y) = xxx_todo_changeme11
	def f():
		glTranslatef(x, y, 0)
		glRotatef(a, 0, 0, 1)
		glTranslatef(-x, -y, 0)
	with_transform(f, fun, *args, **kwd)

def rotate(opos, a, pos):
	(ox, oy) = opos
	(x, y) = pos
	dx, dy = x-ox, y-oy
	#a = a*pi/180
	a = radians(a)
	dx, dy = dx*cos(a)-dy*sin(a), dx*sin(a)+dy*cos(a)
	return dx+ox, dy+oy

def scaled(xxx_todo_changeme14, xxx_todo_changeme15, fun, *args, **kwd):
	(x, y) = xxx_todo_changeme14
	(sx, sy) = xxx_todo_changeme15
	def f():
		glTranslatef(x, y, 0)
		glScalef(sx, sy, 1)
		glTranslatef(-x, -y, 0)
	with_transform(f, fun, *args, **kwd)

def scale(xxx_todo_changeme16, xxx_todo_changeme17, xxx_todo_changeme18):
	(ox, oy) = xxx_todo_changeme16
	(sx, sy) = xxx_todo_changeme17
	(x, y) = xxx_todo_changeme18
	dx, dy = x-ox, y-oy
	return ox+sx*dx, oy+sy*dy

def skewed(xxx_todo_changeme19, xxx_todo_changeme20, fun, *args, **kwd):
	(x, y) = xxx_todo_changeme19
	(sx, sy) = xxx_todo_changeme20
	def f():
		glTranslatef(x, y, 0)
		glMultMatrixf([1, sy, 0, 0,
			       sx, 1, 0, 0,
			       0,  0, 1, 0,
			       0,  0, 0, 1])
		glTranslatef(-x, -y, 0)
	with_transform(f, fun, *args, **kwd)

def drawGrass(tex, ox, dy_o, dy1, dy2, points, a=1):
	for (xa, ya), (xb, yb) in zip(points, points[1:]):
		oy = dy_o + ya
		y1 = ya + dy1
		y2 = ya + dy2
		skewy = (yb - ya) / float(xb - xa)
		skewed((xa, 42), (0, skewy),
			texpoly, tex, (ox, oy), [(xa, y1), (xb, y1), (xb, y2), (xa, y2)], a=a)
