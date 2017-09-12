import maya.cmds as cmds

isolate = False
deactivateSSS = False
deactivateDisplacement = False

myLights = cmds.ls(type='light')
myLightsOn = cmds.ls(type='light', visible=True)
mySelection = cmds.ls (selection = True)

#mySSS = defaultArnoldRenderOptions.ignoreSss
#myDisp

#cmds.setAttr ( 'defaultArnoldRenderOptions.ignoreSss', 0)
#cmds.setAttr ( 'defaultArnoldRenderOptions.ignoreDisplacement', 0)

# Accion del boton, cambia de estado y oculta todas las luces menos la seleccionada cuando es Verdadero, caso contrario deja solo las luces que estaban visibles.

def IsolateButtonPush(*args):
	global isolate
	global myLights
	global myLightsOn
	global mySelection

# verificando las luces de la escena

	if isolate == True:
		#print 'Apagado'
		#print myLights
		#print myLightsOn
		#print mySelection
		isolate = False
		cmds.button ('isoButton', edit = True, bgc = [0,1,0])
		for lights in myLights:
			cmds.showHidden(myLightsOn, a = True, b = True)

	else:
		#print 'Prendido'
		myLights = cmds.ls(type='light')
		myLightsOn = cmds.ls(type='light', visible=True)
		mySelection = cmds.ls (selection = True)
		#print myLights
		#print myLightsOn
		#print mySelection
		isolate = True
		cmds.button ('isoButton', edit = True, bgc = [1,0,0])
		for lights in myLights:
			cmds.hide(myLights)
			cmds.showHidden(mySelection, a = True, b = True)

#DEACTIVATE SSS
def deactivateSSS(*args):
	global deactivateSSS

	if deactivateSSS == True:
		deactivateSSS = False
		cmds.button ('deactivateSSSButton', edit = True, bgc = [0.510,0.850,1])
		cmds.setAttr ( 'defaultArnoldRenderOptions.ignoreSss', 0)
	else:
		deactivateSSS = True
		cmds.button ('deactivateSSSButton', edit = True, bgc = [1,0,0])
		cmds.setAttr ( 'defaultArnoldRenderOptions.ignoreSss', 1)

#DEACTIVATE SUBDIVISION
def deactivateDisp(*args):
	global deactivateDisplacement

	if deactivateDisplacement == True:
		deactivateDisplacement = False
		cmds.button ('deactivateDispButton', edit = True, bgc = [0.350,0.660,1])
		cmds.setAttr ( 'defaultArnoldRenderOptions.ignoreDisplacement', 0)
	else:
		deactivateDisplacement = True
		cmds.button ('deactivateDispButton', edit = True, bgc = [1,0,0])
		cmds.setAttr ( 'defaultArnoldRenderOptions.ignoreDisplacement', 1)

winISO='PH_ISO'
if cmds.window(winISO, exists=True):
	cmds.deleteUI(winISO)
cmds.window(winISO,title='PH_ISOLATELIGHTS v0.3', width=80 ,toolbox=1)
cmds.columnLayout( adjustableColumn=True )
cmds.button( 'isoButton', label='ISOLATE LIT', bgc = [0,255,0], command=IsolateButtonPush,w=100,h=80 )
cmds.button( 'deactivateSSSButton', label='ON/OFF\nSSS', bgc = [0.510,0.850,1], command=deactivateSSS )
cmds.button( 'deactivateDispButton', label='ON/OFF\nDISPLACE', bgc = [0.350,0.660,1], command=deactivateDisp )
cmds.showWindow(winISO)
