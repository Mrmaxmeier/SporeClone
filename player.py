from vector2 import Vec2d
import random


class Player(object):
	def __init__(self, body):
		print('Spawned Player w/ body', body.name)
		self.body = body
		self.vel = Vec2d(0, 0)
		self.pos = Vec2d(0, 0)

	def updatePhysics(self, dt):
		self.pos += self.vel * dt
		self.vel *= 1 - dt

	def update(self, dt):
		self.updatePhysics(dt)

	def draw(self):
		self.body.draw(self.pos)


class OwnPlayer(Player):
	def __init__(self, body, input):
		Player.__init__(self, body)
		self.input = input


class NetworkPlayer(Player):
	pass


class ArtificialPlayer(Player):
	def __init__(self, body, world):
		Player.__init__(self, body)
		self.world = world

	def update(self, dt):
		self.updatePhysics(dt)
		direction = Vec2d(0, 0)
		for p in self.world.getPlayers():
			dirr = p.pos - self.pos
			dirr = dirr.normalized()
			dirr *= self.getRelativeFriendlyness(p) * 50
			direction += dirr
		if direction.get_length() < 0.5:
			direction += Vec2d(random.randint(-10, 10), random.randint(-10, 10))
		if direction.get_length() > 1:
			direction = direction.normalized()
		self.vel += direction * 10 * dt

	def getRelativeFriendlyness(self, p):
		#own = self.body.stats['social'] if 'social' in self.body.stats else 0
		#own -= self.body.stats['aggressive'] if 'aggressive' in self.body.stats else 0
		their = p.body.stats['social'] if 'social' in p.body.stats else 0
		their -= p.body.stats['aggressive'] if 'aggressive' in p.body.stats else 0
		#if own > 0:
		#	friendlyness = their
		#else:
		friendlyness = their
		friendlyness *= (self.body.size - p.body.size) / 10
		if abs(friendlyness) > 1:
			friendlyness /= abs(friendlyness)
		if friendlyness == 0:
			friendlyness = 0.3
		return friendlyness
