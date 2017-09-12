'''
Descripcion:

	Guarda posiciones en base a grupo o seleccion de controles,

	Se puede usar para un reloqueo grupal.

	Autor: Pablo Emmanuel De Leo.

	url='www.pabloemmanueldeleo.com/python-tools.html'

	Ultima actualizacion: 05/01/13
'''
#----------------------------------------------------------
#IMPORTACION
#----------------------------------------------------------
import maya.cmds as mc
import sys
import json
import os.path

#----------------------------------------------------------
#VARIABLES
#----------------------------------------------------------

#vuelvo a generar el archivo con datos por defecto si no existe

vFile = '/RelocationPositionList.pos'

#posicion para relleno de diccionario nuevo o vacio
pos = {'NONE' : [0, 0, 0, 0, 0, 0]}

global dicGlobal
dicGlobal = {}

temDic = {}

global group
group = []

lista = []

#nombre de la ventana de la lista
posList = 'posList'

#----------------------------------------------------------
#FUNCIONES UTILES
#----------------------------------------------------------
#Crea ventanas de dialogo para mensajes WARNING
def printWAR(input='something'):

	if mc.window('errorWAR',ex=True):
		mc.deleteUI('errorWAR')

	# Make a new window
	mc.window('errorWAR', title="WARNING...", s=False, iconName='Short Name', toolbox=1, w=100, h=50)
	mc.columnLayout(adjustableColumn=True)
	mc.text(label='')
	mc.text(label=(input))
	mc.text(label='')
	mc.button('  OK  ', command = 'mc.deleteUI("errorWAR")',al=True)
	mc.showWindow('errorWAR')

#Crea ventanas de dialogo para mensajes DONE
def printDONE(input='something'):

	if mc.window('errorDONE',ex=True):
		mc.deleteUI('errorDONE')

	# Make a new window
	mc.window('errorDONE', title="DONE!", s=False, iconName='Short Name', toolbox=1, w=100, h=50)
	mc.columnLayout(adjustableColumn=True)
	mc.text(label='')
	mc.text(label=(input))
	mc.text(label='')
	mc.button('  OK  ', command = 'mc.deleteUI("errorDONE")',al=True)
	mc.showWindow('errorDONE')


#funcion para guardar cualquier archivo de json
def saveJSONFile(dataBlock, filePath):
	outputFile = open(filePath, 'w')
	JSONData = json.dumps(dataBlock, sort_keys=True, indent=4)
	outputFile.write(JSONData)
	outputFile.close()

#funcion para leer cualquier archivo de json
def loadJSONFile(filePath):
	inputFile = open(filePath, 'r')
	JSONData = json.load(inputFile)
	print '<<file was loaded>>'
	inputFile.close()
	return JSONData

#funcion solo para leer datos de archivo con json
def writeJSONFile(dataBlock, filePath):
	# append in file
	f = open(filePath, 'a')
	d = json.dumps(dataBlock, sort_keys=True, indent=4)
	f.write(d)
	f.close()

#Coloca la posicion al objeto
def setPos(tx=0, ty=0, tz=0, rx=0, ry=0, rz=0):

		grp = (mc.ls(sl=1))[0]
		mc.setAttr(grp + '.tx', tx)
		mc.setAttr(grp + '.ty', ty)
		mc.setAttr(grp + '.tz', tz)
		mc.setAttr(grp + '.rx', rx)
		mc.setAttr(grp + '.ry', ry)
		mc.setAttr(grp + '.rz', rz)

#Obtiene la posicion del objeto seleccionado
def getPos():

	obj = (mc.ls(sl=1))[0]
	tX = mc.getAttr(obj + '.tx')
	tY = mc.getAttr(obj + '.ty')
	tZ = mc.getAttr(obj + '.tz')
	rX = mc.getAttr(obj + '.rx')
	rY = mc.getAttr(obj + '.ry')
	rZ = mc.getAttr(obj + '.rz')

	print 'Se guardo la po', tX, tY, tZ, rX, rY, rZ
	return tX, tY, tZ, rX, rY, rZ

#Pregunta de la lista y acciona la funcion setPos.
def onMoveClick(args):

	sel = mc.ls(sl=1)
	#Chequeo cual estoy seleccionando en la lista.
	key = mc.textScrollList(posList, query=True, selectItem=True)[0]

	if len(key) >= 0 and sel:

		val = dicGlobal[key]
		setPos(val[0], val[1], val[2], val[3], val[4], val[5])
		printDONE(str(sel) + ' it moved to position of' + str(key) + '.')

	else:
		printWAR('Select a group, then the position you want.')

#borra con delet la selecicon dentro del dic
def delSelected():

	keyes = mc.textScrollList(posList, query=True, selectItem=True)
	for key in keyes:
		#borro todo lo seleccionado del diccionario y lo vuelvo a guardar.
		del dicGlobal[key]
		print 'Removed the key:'
		print key
		dicGlobal.update(pos)
	saveJSONFile(dicGlobal, vFile)
	refreshGui

#creo el grupo y lo coloco el pivot en el 0.0.0
def mainGroup(args):
	global group

	try:
		sel = mc.ls(sl=1)[0]
		if sel:
			printDONE('Group created')
	except IndexError:
		printWAR('Select something that grouping')
		return
	group = mc.group(n='GroupReloc', w=1)
	mc.xform(group, objectSpace=1, pivots=[0, 0, 0])

#desagrupo lo seleccionado.
def unGroup(args):

	sel = mc.ls(sl=1)

	try:
		if sel:
			mc.ungroup(sel, w=1)

			printDONE('Ungrop Done.')

		else:
			printWAR('select some group')
	except:
		printWAR('This dont group')
#funcion de bakeo de animacion
def bake(obj):

	mini = mc.playbackOptions(q=1, min=1)
	maxi = mc.playbackOptions(q=1, max=1)
	mc.bakeResults(obj, simulation=True, t=(mini, maxi), sampleBy=1,
						disableImplicitControl=True, preserveOutsideKeys=True,
						sparseAnimCurveBake=False, controlPoints=False,
						shape=True, hierarchy=True, attribute=True)

#complemento para funcion bake()
def bakeObj():

	sel = mc.ls(sl=1)
	if group:
		currentP = mc.paneLayout('viewPanes', q=True, pane1=True)
		mc.isolateSelect(currentP, state=1)
		for o in sel:
			bake(o)
	mc.isolateSelect(currentP, state=0)

#Se encarga de guardar una posicion nueva en la lista y en el archivo
def savePos(args):

	if mc.ls(sl=1):
		gPos = getPos()
		newSec = mc.textFieldGrp('wReloc_Seq', q=True, text=True)

		if newSec and mc.ls(sl=1):
			#si hay algo escrito lo guardo en el dic nuevo
			temDic[newSec] = gPos
			#agrego al diccionario global el diccionario nuevo con el contenido nuevo.
			dicGlobal.update(temDic)
			#vuevlo a grabar la lista con el nuevo dato
			saveJSONFile(dicGlobal, vFile)

		else:
			printWAR('Type a name for the position.')
	else:
		printWAR('Create or select a group.')
	refreshGui

#Actualiza los datos de la lista
def refreshGui(arg):
	#Limpio la lista para luego volverla a cargar.
	mc.textScrollList(posList, edit=True, removeAll=True)
	update()

#Complemento para funcion refreshGui()
def update():
	nLista = []

	for key in dicGlobal:
		#Agrego a la lista en cada posicion para luego visualizar
		nLista.append(key)
		#Ordena la lista alfabeticamente
		nLista.sort()
	#logro visualizar la lista pero con los datos nuevos.
	mc.textScrollList(posList, edit=True, append=nLista)
	mc.textScrollList(posList, edit=True, selectItem='NONE')

#----------------------------------------------------------
#MAIN
#----------------------------------------------------------
#Funcion de la interface grafica de la tools y chequeo si existe el archivo donde guarda las posiciones.
def relocUI():

	global dicGlobal
	win = 'wReloc_'

	if mc.window(win, ex=1):
		mc.deleteUI(win)
	#Si existe el archivo en el sistema se carga
	if os.path.isfile(vFile):
		dicGlobal = loadJSONFile(vFile)

	#si no existe se genera con un NONE
	if not os.path.isfile(vFile):
		saveJSONFile(pos, vFile)

	mc.window(win, title='Reloqueitor v1.1', s=0, w=250, h=180, toolbox=1)
	mc.columnLayout(adjustableColumn=True)
	mc.separator(height=5, style='none')
	mc.text(label='Positions:', align='left')
	mc.separator(height=5, style='none')
	mc.textScrollList(posList, w=190, h=190, allowMultiSelection=True, deleteKeyCommand=delSelected)
	mc.separator(height=10, style='none')
	mc.button(win + 'b1', ann='Create a group for the entire selection.', l='1.GROUP', command=mainGroup, bgc=[0.5, 0.5, 0.6])
	mc.button(win + 'b2', ann='Move in the position list selectined.', l='2.MOVE', command=onMoveClick, bgc=[0.35, 0.46, 0.53])
	mc.button(win + 'b3', ann='Ungroup.', l='3.UNGROUP', command=unGroup, bgc=[0.5, 0.46, 0.6])
	mc.button(win + 'b5', ann='REFRESH.', l='REFRESH', command=refreshGui, bgc=[0.29,0.36,0.38])
	mc.columnLayout(adjustableColumn=True)
	mc.separator(height=1, style='none')
	mc.text(l='Write name new position.', align='left')
	mc.textFieldGrp(win + 'Seq', ann='Ej. s123_010a')
	mc.separator(height=1, style='none')
	mc.columnLayout(adjustableColumn=True)
	mc.button(win + 'b4', ann='Save a new position in the list', l='SAVE', command=savePos, bgc=[0.8, 0.4, 0.3])
	mc.separator(height=5, style='none')
	mc.text(l='By Pablo Emmanuel De Leo', align='right', hyperlink=True)
	mc.showWindow(win)
	refreshGui
