import parts
from vector2 import Vec2d


def generatePartSubTree(struct, partManager, parent):
	partClass = partManager.getPart(struct['name'])
	if not partClass:
		raise RuntimeError('Part "'+str(struct['name'])+'" is not avalible!')
	part = partClass(parent)
	size = float(struct['sizeMod'])
	part.setSize(size)
	for i in range(len(part.getHinges())):
		if str(i) in struct['attatched']:
			p = generatePartSubTree(struct['attatched'][str(i)], partManager, part.getHinges()[i])
			part.getHinges()[i].setPart(p)
	return part


def generateBodyHinge(struct, partManager):
	# {'sizeMod': 1, 'attatched':
	#         {'3': {'sizeMod': 1, 'attatched': {}, 'name': 'paddle'},
	#            '4': {'sizeMod': 1, 'attatched': {}, 'name': 'paddle'}
	#          },
	#     'name': 'base'}
	h = parts.Hinge(Vec2d(0, 0))
	mainPart = generatePartSubTree(struct, partManager, h)
	h.setPart(mainPart)
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
		classDerv = (GeneratedBody,)
		if 'name' in d:
			className = d['name']
			classDict['name'] = d['name']
		else:
			className = 'UnnamedGeneratedBody | FIXME'
			classDict['name'] = 'UnnamedGeneratedBody | FIXME'
		if 'stats' in d:
			classDict['stats'] = d['stats']
		else:
			self.stats = {}
		if 'structure' in d:
			classDict['baseHinge'] = generateBodyHinge(d['structure'], partManager)
		else:
			raise NotImplementedError
		classDict['size'] = 1
		return type(className, classDerv, classDict)

	def draw(self, pos):
		self.baseHinge.getPart().drawSubParts(pos, self.size, drawHinges=True)


class GeneratedBody(GenericBody):
	pass
