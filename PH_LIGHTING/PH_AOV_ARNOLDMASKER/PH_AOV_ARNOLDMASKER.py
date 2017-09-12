import maya.cmds as cmds
import sys
path=r'M:\PH_SCRIPTS\_MODULES'
if not path in sys.path:
    sys.path.append(path)
try:
	import UTILITIES as UTL
	UTL.arnoldON()
except ImportError:
	print 'Preguntale al tipo de pipeline donde esta este modulo.'

def UIAOV(*args):
	#GUI
	#28/10/2015
	winAOVM='PH_AOV_MSK'
	v=' v1.1'
	if cmds.window(winAOVM, exists=True):
		cmds.deleteUI(winAOVM)

	cmds.window(winAOVM, title=winAOVM+v, s=False, w=250,h=100)
	cmds.columnLayout( columnAttach=["both",15], rowSpacing=10,columnWidth= 300)
	cmds.text(label=" ")
	cmds.text( label="SELECCIONA SOLO SETS")
	cmds.text(label=" ")
	cmds.button( bgc=(0.47,0.74,0.05),label="CREATE AOV",w=200,h=50,c=create_aov)
	cmds.text(label=" ")
	cmds.text( label="SELECCIONA SOLO SETS,\nSOLO SI EXISTE EL NOMBRE LO BORRARA")
	cmds.button( bgc=(0.8,0.41,0.08),label="BORRAR AOV MSK",w=200,h=50,c=deleteAOVMSK)
	cmds.text(label=" ")
	cmds.showWindow(winAOVM)

def create_aov(*args):

	sel=cmds.ls(sl=1)
	set={}
	for f in range(len(sel)):
		set[f]=sel[f]

		if cmds.objectType(set[f]) == 'objectSet':
			nameSet=str(set[f])

			cmds.select(cmds.sets(set[f],q=1), hierarchy=True)
			trf=cmds.ls(sl=1,type='mesh')
			if not cmds.objExists("aiAOV_Mask_"+nameSet+"_AIAOV"):
				#creacion de nodos
				if not cmds.objExists( nameSet+'_AIUTL' ):
					nodeU=cmds.createNode('aiUtility', n=nameSet+'_AIUTL')
					cmds.setAttr(nodeU+'.shadeMode',2)
				else:
					cmds.warning('ameoo ya existe el nodo '+ nameSet+'_AIUTL')
					nodeU=nameSet+'_AIUTL'

				if not cmds.objExists( nameSet+'_AIWTC' ):
					nodeW=cmds.createNode('aiWriteColor', n=nameSet+'_AIWTC')
					cmds.setAttr(nodeW+'.beauty', 1,1,1, type='double3')
					cmds.setAttr(nodeW+'.blend', 1)
				else:
					cmds.warning('ameoo ya existe el nodo '+ nameSet+'_AIWTC')
					nodeW=nameSet+'_AIWTC'

				if not cmds.objExists( nameSet+'_AITSS' ):
					nodeT=cmds.createNode('tripleShadingSwitch', n=nameSet+'_AITSS')
					cmds.setAttr(nodeT+'.default', 0,0,0, type='double3')
				else:
					cmds.warning('ameoo ya existe el nodo '+ nameSet+'_AITSS')
					nodeT=nameSet+'_AITSS'

				if cmds.objExists( nameSet+'_AITSS' ):
					#coneccion de nodos
					nodeT=nameSet+'_AITSS'
				if not cmds.isConnected(nodeT+'.output', nodeU+'.color'):
					cmds.connectAttr(nodeT+'.output', nodeU+'.color', f=True)

				for i in range(len(trf)):
					#print i
					if cmds.isConnected(trf[i]+'.instObjGroups[0].objectGroups['+str(i)+']', str(nodeT)+'.input['+str(i)+'].inShape'):
						cmds.disconnectAttr(trf[i]+'.instObjGroups[0].objectGroups['+str(i)+']', str(nodeT)+'.input['+str(i)+'].inShape')
					cmds.connectAttr(trf[i]+'.instObjGroups[0].objectGroups['+str(i)+']', str(nodeT)+'.input['+str(i)+'].inShape',f=1)
					if cmds.isConnected(str(nodeW)+'.outColor', str(nodeT)+'.input['+str(i)+'].inTriple'):
						cmds.disconnectAttr(str(nodeW)+'.outColor', str(nodeT)+'.input['+str(i)+'].inTriple')
					cmds.connectAttr(str(nodeW)+'.outColor', str(nodeT)+'.input['+str(i)+'].inTriple',f=1)
				#Creo AOV y conecto esto
				aov_list = cmds.getAttr("defaultArnoldRenderOptions.aovList",s=True)
				if not cmds.objExists( "aiAOV_Mask_"+nameSet+"_AIAOV" ):
					nombreNodoaiaov = cmds.createNode( "aiAOV", n= "aiAOV_Mask_"+nameSet+"_AIAOV")
				else:
					nombreNodoaiaov= "aiAOV_Mask_"+nameSet+"_AIAOV"
				if not cmds.isConnected(nombreNodoaiaov +".message", "defaultArnoldRenderOptions.aovList["+ str(aov_list) +"]"):
					cmds.connectAttr(nombreNodoaiaov +".message", "defaultArnoldRenderOptions.aovList["+ str(aov_list) +"]",f=True)
				cmds.setAttr(nombreNodoaiaov+'.type',5)
				#saco el namespace
				if ':' in nameSet:
					nameSinNs= nameSet.split(':')[-1]
				else:
					nameSinNs= nameSet
				nodeW=nameSet+'_AIWTC'
				cmds.setAttr(nombreNodoaiaov+'.name',nameSinNs, type='string' )
				cmds.setAttr(nodeW+'.aovName',nameSinNs, type='string' )
				cmds.connectAttr("defaultArnoldDriver.message", nombreNodoaiaov+".outputs[0].driver", f=True)
				cmds.connectAttr("defaultArnoldDriver.message", nombreNodoaiaov+".outputs[0].filter", f=True)
				if not cmds.isConnected(nodeU+'.outColor', nombreNodoaiaov +".defaultValue"):
					cmds.connectAttr(nodeU+'.outColor', nombreNodoaiaov +".defaultValue")
				cmds.select(cl=1)
			else:
				cmds.warning('Ya existe un AOV con el nombre: '+"aiAOV_Mask_"+nameSet+"_AIAOV"+'\n para continuar necesitas borrar ese aov primero.')

		else:
			cmds.warning('Ameoooo selecciona solo sets')

def deletedNODE(nombre=''):
	if cmds.objExists( nombre ):
		cmds.delete(nombre)
		print 'Se elimino ' + nombre

def deleteAOVMSK(*arg):
	sel=cmds.ls(sl=1)
	set={}
	for f in range(len(sel)):
		set[f]=sel[f]
		if cmds.objectType(set[f]) == 'objectSet':
			nameSet=str(set[f])

			deletedNODE(nameSet+'_AIUTL')
			deletedNODE(nameSet+'_AIWTC')
			deletedNODE(nameSet+'_AITSS')
			deletedNODE("aiAOV_Mask_"+nameSet+"_AIAOV")
		else:
			cmds.warning('No es un set: ' + set[f])
