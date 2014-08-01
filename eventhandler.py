class EventHandler(object):
	def __init__(self):
		self.handlers = {'bodyMovement': [], 'mouseMovement': [], 'collision': []}

	def update(self, dt):
		self.callHandlers('update', dt)

	def frame(self):
		self.callHandlers('frame')

	def mouseMovement(self, position):
		self.callHandlers('mouseMovement', position)

	def callHandlers(self, name, *args):
		for h in self.handlers[name]:
			h(*args)

	def register(self, name, func):
		if not name in self.handlers:
			self.handlers[name] = []
		self.handlers[name].append(func)

	def registerDict(self, d):
		for key in d:
			self.register(key, d[key])

	def sceneChange(self, sceneName):
		self.callhandlers('sceneChange', sceneName)
