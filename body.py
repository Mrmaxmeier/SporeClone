import parts
from vector2 import Vec2d
import json


def generatePartSubTree(struct, partManager, parent):
	partClass = partManager.getPart(struct['name'])
	if not partClass:
		raise RuntimeError('Part "'+str(struct['name'])+'" is not avalible!')
	part = partClass(parent)
	size = float(struct['sizeMod'])
	part.setSize(size)
	part.origSize = size
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


def generateSubStructure(part):
	d = {'name': part.name, 'sizeMod': part.origSize, 'attatched': {}}
	hinges = part.getHinges()
	for i in range(len(hinges)):
		h = hinges[i]
		if h.hasPart():
			p = h.getPart()
			d['attatched'][i] = generateSubStructure(p)
	return d


def generateStructureDict(body):
	d = generateSubStructure(body.baseHinge.getPart())
	return d


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
		if 'structure' in d:
			classDict['baseHinge'] = generateBodyHinge(d['structure'], partManager)
		else:
			raise NotImplementedError
		classDict['size'] = 1
		classDict['classDict'] = d
		return type(className, classDerv, classDict)

	def draw(self, pos):
		self.baseHinge.getPart().drawSubParts(pos, self.size, drawHinges=True)


class GeneratedBody(GenericBody):
	def getJson(self, name=False):
		d = self.classDict
		#{}
		if name:
			d['name'] = name
		else:
			d['name'] = self.name
		d['structure'] = generateStructureDict(self)
		return json.dumps(d)
