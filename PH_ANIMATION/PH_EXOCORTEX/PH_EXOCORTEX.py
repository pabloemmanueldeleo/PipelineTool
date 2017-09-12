import maya.cmds
import maya.mel
path='M:\PH_SCRIPTS\_PLUGINS\exocortex\scripts\ExocortexAlembic'
if not path in sys.path:
    sys.path.append(path)
import ExocortexAlembic as Exo
help(Exo._import)
help(Exo._export)
help(Exo._attach)
help(Exo._import.IJobInfo)

filename=r'D:/PH_SCRIPTS/SCENES_RIG/EXOCORTE/ARTURO_EXO.abc'
exInframe=0
exOutframe=20
exObjects=cmds.listRelatives(cmds.ls('arturo004A:Asset|arturo004A:Geometries'))

#exportar exocortex
jobInfo=["_filename=filename", "useNormals=False", "useUVs=False", "useFaceSets=False", "multi=False"]
cmds.ExocortexAlembic_import(filename)


Exo._export.doIt(filename,
			exInframe,
			exOutframe,
			exObjects,
			exStepframe=1,
			exSubstepframe=1,
			exTopology=3,
			exWithoutHierarchy=True,
			exGlobSpace=False,
			exDynTopo=False,
			exXformCache=False,
			exUseInitShadGrp=False,
			exUseOgawa=True,
			exUVs=True)

#CLASE
#importar exocortex jobInfo(name, _filename, useNormals=False, useUVs=True, useFaceSets=True, multi=False)
Exo._import.IJobInfo(_filename=filename,
					useNormals=False,
					useUVs=False,
					useFaceSets=False,
					multi=False)

Exo._attach.attachPoints(filename,
			attachToExisting=True,
			multi=False,
			normals=False,
			facesets=False,
			uvs=False)


def alembicCreateNode(name, type, parentXform=None):
	""" create a node and make sure to return a full name and create namespaces if necessary! """
	cmds.ExocortexAlembic_profileBegin(f="Python.ExocortexAlembic._functions.createAlembicNode")
	#print("alembicCreateNode(" + str(name) + ", " + str(type) + ", " + str(parentXform) + ")")
	result = subCreateNode(name.split('|'), type, parentXform)
	cmds.ExocortexAlembic_profileEnd(f="Python.ExocortexAlembic._functions.createAlembicNode")
	return result
alembicCreateNode
sys.path.remove(path)
