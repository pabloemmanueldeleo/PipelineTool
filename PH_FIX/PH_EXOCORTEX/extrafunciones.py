import maya.cmds
import maya.mel
path='M:\PH_SCRIPTS\_PLUGINS\exocortex\scripts\ExocortexAlembic'
if not path in sys.path:
    sys.path.append(path)
import ExocortexAlembic as EA

help(EA._import)
help(EA._export)
help(EA._attach)
help(EA._import.IJobInfo)

filename=r'D:/PH_SCRIPTS/SCENES_RIG/EXOCORTE/ARTURO_EXO.abc'
exInframe=0
exOutframe=20
exObjects=cmds.listRelatives(cmds.ls('arturo004A:Asset|arturo004A:Geometries'))

#exportar exocortex
Exo._export.doIt(filename,
			exInframe,
			exOutframe,
			exObjects,
			exStepframe=1,
			exSubstepframe=1,
			exTopology=1,
			exWithoutHierarchy=True,
			exGlobSpace=False,
			exDynTopo=False,
			exXformCache=False,
			exUseInitShadGrp=False,
			exUseOgawa=True,
			exUVs=True)

#CLASSE
#importar exocortex jobInfo(name, _filename, useNormals=False, useUVs=True, useFaceSets=True, multi=False)
EA._import.IJobInfo(_filename=filename,
					useNormals=False,
					useUVs=False,
					useFaceSets=False,
					multi=False)

#jobInfo=["_filename=filename", "useNormals=False", "useUVs=False", "useFaceSets=False", "multi=False"]
EA._import.IJobInfo(filename, False, False, False, False)

EA._attach.attachPoints(filename)


def alembicCreateNode(name, type, parentXform=None):
	""" create a node and make sure to return a full name and create namespaces if necessary! """
	cmds.ExocortexAlembic_profileBegin(f="Python.ExocortexAlembic._functions.createAlembicNode")
	#print("alembicCreateNode(" + str(name) + ", " + str(type) + ", " + str(parentXform) + ")")
	result = subCreateNode(name.split('|'), type, parentXform)
	cmds.ExocortexAlembic_profileEnd(f="Python.ExocortexAlembic._functions.createAlembicNode")
	return result
alembicCreateNode
sys.path.remove(path)
