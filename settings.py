import json


class Settings(object):
	def __init__(self, path='settings.json'):
		self.path = path
		self.load()

	def save(self):
		with open(self.path, "w") as jsonfile:
			jsonfile.write(json.dumps(self.d))

	def load(self):
		try:
			with open(self.path, "r") as jsonfile:
				data = jsonfile.read()
				d = json.loads(data)
				self.d = d
		except Exception as e:
			print('Exception', e)
			print('Assuming corrupt Settings file')
			print('Rebuilding Settings File')
			self.d = {'screensize': [1280, 720], 'name': 'Player', 'ip': 'localhost', 'FPS_Lock': 60}
			self.save()
			print('ReLoading')
			self.load()

	def get(self, key):
		if key in self.d:
			return self.d[key]
		print(key, 'not in settings!')
		raise Exception()

	def set(self, key, val):
		self.d[key] = val
		self.save()

if __name__ == '__main__':
	s = Settings()
	print(s.get('screensize'))
	print(s.get('name'))
	print(s.get('ip'))
