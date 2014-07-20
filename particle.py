###################
# Particle Engine #
###################

from vector2 import *
import draw
import random

class Particle:
	def __init__(self, particlespace, pos=Vec2d(0, 0), vel=Vec2d(0, 0), lifetime=10):
		self.particlespace = particlespace
		self.pos = pos
		self.vel = vel
		self.lifetime = float(lifetime)
		self.totallifetime = self.lifetime
		self.isDead = False
		self.veldecay = 0.1
		self.color = draw.black
		self.size = 10
		self.totalsize = self.size
		self.alpha = 255.0

	def update(self, dt):
		self.pos += self.vel * dt
		self.vel -= self.vel * dt * self.veldecay
		self.lifetime -= dt
		self.age(dt)
		if self.lifetime < 0:
			self.destroy()

	def age(self, dt):
		pass

	def draw(self, drawVelocity=False):
		if drawVelocity:
			draw.line(self.pos, self.pos+self.vel, draw.red)
		draw.point(self.pos, self.color, self.size, self.alpha)

	def destroy(self):
		self.isDead = True
		self.particlespace.destroyParticle(self)

	def accelerate(self, vec, dt):
		self.vel += vec * dt


class p_Shrinking(Particle):
	def age(self, dt):
		self.size = self.totalsize * (self.lifetime / self.totallifetime)


class p_Explode_on_death(Particle):

	def update(self, dt):
		Particle.update(self, dt)
		self.age(dt)

	def age(self, dt):
		p_Shrinking.age(self, dt)
		if type(self.color) == tuple:
			self.color = [self.color[0], self.color[1], self.color[2]]
		self.color[0] = self.totallifetime/float(self.lifetime)

	def destroy(self):
		Particle.destroy(self)
		for i in range(0, 36):
			angle = i*10 + random.randrange(-10, 10)
			speed = random.randint(10, 80)
			vel = Vec2d(speed, 0).rotated(angle)
			vel += self.vel
			p = self.particlespace.spawnParticle(p_Shrinking, Vec2d(self.pos), vel, 3)
			p.color = random.choice((draw.red, draw.green, draw.black, draw.blue))


class p_FireSource(Particle):
	def __init__(self, particlespace, pos=Vec2d(0, 0), vel=Vec2d(0, 0), lifetime=20):
		Particle.__init__(self, particlespace, pos, vel, lifetime)
		self.time2flameSpawn = 0
		self.timeBetweenFlameSpawn = 0.075
		self.p_flames = []
		self.color = (254, 206, 12)

	def update(self, dt):
		Particle.update(self, dt)
		self.time2flameSpawn -= dt
		if self.time2flameSpawn < 0:
			self.time2flameSpawn = self.timeBetweenFlameSpawn
			self.spawnFlame()

	def spawnFlame(self):
		vel = Vec2d(random.randint(-15, 15), 0).rotated(random.randint(-5, 5))
		self.particlespace.spawnParticle(p_Flame, self, Vec2d(self.pos), vel)


class p_Flame(p_Shrinking):
	def __init__(self, particlespace, firesource, pos=Vec2d(0, 0), vel=Vec2d(0, 0), lifetime=10):
		p_Shrinking.__init__(self, particlespace, pos, vel, lifetime)
		flameColors = [(254, 206, 12), (246, 153, 23), (238, 67, 28), (203, 0, 26)]
		self.color = (254, 206, 12)
		self.size = random.randint(20, 30)
		self.totalsize = self.size

		self.time2smokeSpawn = 4
		self.timeBetweenSmokeSpawn = 1
		self.firesource = firesource

	def update(self, dt):
		p_Shrinking.update(self, dt)
		self.modColor(dt)
		self.accelerate(Vec2d(random.randint(-20, 20), random.randint(-40, 0)), dt)
		self.time2smokeSpawn -= dt
		if self.time2smokeSpawn < 0:
			self.time2smokeSpawn = self.timeBetweenSmokeSpawn
			self.spawnSmoke()

	def modColor(self, dt):
		distance = self.pos.get_distance(self.firesource.pos)
		if distance < 15:
			c = (254, 206, 12)
		elif distance < 75:
			c = (246, 153, 23)
		elif distance < 125:
			c = (238, 67, 28)
		elif distance < 500:
			c = (203, 0, 26)
		else:
			c = (40, 40, 40)
			self.alpha = 100
		self.color = c


	def spawnSmoke(self):
		vel = Vec2d(random.randint(-30, 30), 0).rotated(random.randint(-5, 5))
		self.particlespace.spawnParticle(p_Smoke, Vec2d(self.pos), vel)


class p_Smoke(Particle):
	def __init__(self, particlespace, pos=Vec2d(0, 0), vel=Vec2d(0, 0), lifetime=10):
		p_Shrinking.__init__(self, particlespace, pos, vel, lifetime)
		self.grey = random.choice([0.3, 0.8])
		self.color = [self.grey, self.grey, self.grey]
		self.alpha = 100
		self.size = random.randint(10, 20)
		self.totalsize = self.size

	def update(self, dt):
		p_Shrinking.update(self, dt)
		self.modColor(dt)
		self.accelerate(Vec2d(random.randint(-40, 40), random.randint(-50, 0)), dt)

	def modColor(self, dt):
		self.alpha += dt*10






class Emitter:
	def __init__(self, particlespace, particleClass, *args):
		self.particlespace = particlespace
		self.particleClass = particleClass
		self.time2spawn = tts
		self.totaltime2spawn = ttts

	def update(self, dt):
		pass


class Attractor:
	pass


class ParticleSpace:
	def __init__(self, size):
		self.size = size
		self.particles = []
		self.drawVelocity = False

	def destroyParticle(self, particle):
		self.particles.remove(particle)

	def spawnParticle(self, particleClass, *args):
		particle = particleClass(self, *args)
		self.particles.append(particle)
		return particle

	def update(self, dt):
		#if len(self.particles) > 10:
		#	for particle in self.particles:
		#		self.threadQueue.put((particle, dt))
		#	self.threadQueue.join()
		#else:
		#	for particle in self.particles:
		#		particle.update(dt)
		for particle in self.particles:
			particle.update(dt)

	def threadWorker(self, threadNumber):
		while 1:
			particle, dt = self.threadQueue.get()
			particle.update(dt)
			self.threadQueue.task_done()

	def draw(self):
		for particle in self.particles:
			particle.draw(drawVelocity=self.drawVelocity)


class ps_Gravity(ParticleSpace):
	def __init__(self, size, gforce=Vec2d(0, 15.0)):
		ParticleSpace.__init__(self, size)
		self.gforce = gforce

	def update(self, dt):
		ParticleSpace.update(self, dt)
		gforce = self.gforce * dt
		for particle in self.particles:
			particle.vel += gforce
