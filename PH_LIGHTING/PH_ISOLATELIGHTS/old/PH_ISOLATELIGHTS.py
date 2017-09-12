import maya.cmds as cmds

isolate = False

myLights = cmds.ls(type='light')
myLightsOn = cmds.ls(type='light', visible=True)
mySelection = cmds.ls (selection = True)

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
		cmds.button ('isoButton', edit = True, bgc = [0,255,0])
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
		cmds.button ('isoButton', edit = True, bgc = [255,0,0])
		for lights in myLights:
			cmds.hide(myLights)
			cmds.showHidden(mySelection, a = True, b = True)


if cmds.window(winISO, exist=True):
	cmds.deleteUI(winISO)
winISO=cmds.window('PH_ISOLATELIGHTS', width=80 )
cmds.columnLayout( adjustableColumn=True )
cmds.button( 'isoButton', label='Isolate Lights', bgc = [0,255,0], command=IsolateButtonPush )
cmds.showWindow(winISO)
