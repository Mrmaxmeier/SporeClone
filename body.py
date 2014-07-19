import parts
from vector2 import Vec2d


def generatePartSubTree(struct, partManager):
	part = partManager.getPart(struct['name'])
	part.sizeMod(struct['sizeMod'])
	for i in xrange(len(part.getHinges())):
		if i in struct['attatched']:
			p = generatePartSubTree(struct['attatched'][i], partManager)
			part.getHinges()[i].setPart(p)
	return part


def generateBodyHinge(struct, partManager):
	# {'sizeMod': 1, 'attatched':
	#         {'3': {'sizeMod': 1, 'attatched': {}, 'name': 'paddle'},
	#            '4': {'sizeMod': 1, 'attatched': {}, 'name': 'paddle'}
	#          },
	#     'name': 'base'}
	h = parts.Hinge(Vec2d(0, 0))
	h.setPart(generatePartSubTree(struct, partManager))
	return h


class GenericBody(object):
	def __init__(self):
		#__Dict:
		#{'name': 'Mouthotronix',
		# 'structure':
		#    {'sizeMod': 1, 'attatched':
		#         {'3': {'sizeMod': 1, 'attatched': {}, 'name': 'paddle'},
		#            '4': {'sizeMod': 1, 'attatched': {}, 'name': 'paddle'}
		#          },
		#     'name': 'base'}
		# }
		#
		pass

	def getClass(self, d, partManager):
		classDict = {}
		classDerv = (GeneratedBody)
		if 'name' in d:
			className = d['name']
		else:
			className = 'UnnamedPart | FIXME'
		if 'stats' in d:
			classDict['stats'] = d['stats']
		else:
			self.stats = {}
		if 'structure' in d:
			classDict['baseHinge'] = generateBodyHinge(d['structure'], partManager)
		else:
			raise NotImplementedError
		return type(className, classDerv, classDict)


class GeneratedBody(GenericBody):
	pass
