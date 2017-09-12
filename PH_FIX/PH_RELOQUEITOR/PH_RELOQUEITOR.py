'''
Descripcion:
	Guarda posiciones en base a grupo o seleccion de controles,
	Se puede usar para un reloqueo grupal.
	Autores: Pablo Emmanuel De Leo, Gabriel Alejandro Salinas.
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
vFile = 'M:\PH_SCRIPTS\PH_FIX\PH_RELOQUEITOR\RelocationPositionList.pos'
#posicion para relleno de diccionario nuevo o vacio
pos = {'NONE' : [0, 0, 0, 0, 0, 0]}
global objSel
objSel = []
global sel
sel=[]
global constraints
constraints = []
global locsCreados
locsCreados = []
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
#Crea ventanas de dialogo para mensajes DONE
def printLabel(input='something'):
	mc.text("consola" , e=1 , l=input , al="center" )
	print input
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
def onMoveClick():
	sel = mc.ls(sl=1)
	#Chequeo cual estoy seleccionando en la lista.
	key = mc.textScrollList(posList, query=True, selectItem=True)[0]
	if len(key) >= 0 and sel:
		val = dicGlobal[key]
		setPos(val[0], val[1], val[2], val[3], val[4], val[5])
		printLabel('GRUPO MOVIDO A: ' + key )
	else:
		printLabel('ELEGI EL GRUPO, LA POSICION Y APRETA "MOVE"')
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
	refreshGui()
def borrarDuplicados (aConDuplicados):
    a =set(aConDuplicados)
    result = []
    for item in a:
        result.append(item)
    return result
#creo el grupo y lo coloco el pivot en el 0.0.0
def mainGroup():
	global group
	global objSel
	global constraints
	global locsCreados
	locsCreados = []
	mc.refresh (suspend=1)
	try:
		sel = mc.ls(sl=1)
		objSel = sel
		if sel:
			sel = mc.ls(sl=1)
			printLabel('GRUPO CREADO')
	except IndexError:
		printLabel('Select something that grouping')
		return
	for obj in objSel:
		mini = mc.playbackOptions(q=1, min=1)
		maxi = mc.playbackOptions(q=1, max=1)
		mc.bakeResults(obj, simulation = 1 , t= (mini, maxi)  )
		# COMO YA BAKEE, SI TIENE CONSTRAINTS LOS BORRO PARA QUE NO ROMPAN LAS PELOTAS.
		if mc.listConnections (obj, type="constraint" )!=None:
			constraintsdeOBJ = borrarDuplicados(mc.listConnections (obj, type="constraint" ))
			mc.delete(constraintsdeOBJ)
		nombreLoc = mc.spaceLocator ( n = (obj+'__LOC')  )
		locCreado = mc.ls(sl=True)[0]
		objLocHCNS = mc.parentConstraint ( obj , locCreado, name = (obj + locCreado + "__HCNS") )
		mc.bakeResults(locCreado, simulation = 1 , t= (mini, maxi)  )
		mc.delete (objLocHCNS)
		nombreConstraint = mc.parentConstraint ( locCreado ,  obj, name = (locCreado + "__HCNS"))[0]
		constraints.append (nombreConstraint)
		locsCreados.append (locCreado)
		locCreadoSH = mc.listRelatives (locCreado, s=1 ) [0]
		mc.rename (locCreadoSH , ( locCreado + "SH" )  )
		locCreadoSH = (locCreado + "SH" )
	group = mc.group(locsCreados, n='GroupReloc', w=1)
	mc.xform(group, objectSpace=1, pivots=[0, 0, 0])
	mc.refresh (suspend=0)
#desagrupo lo seleccionado.
def unGroup():
	global objSel
	global locsCreados
	global constraints
	constraints = borrarDuplicados (constraints)
	sel = mc.ls(sl=1)
	if len(sel)!=0:
		try:
			for s in objSel:
				bake(s)
				bake(objSel[0])
			for c in constraints:
				mc.delete (c)
			mc.ungroup(sel, w=1)
			mc.delete(locsCreados)
			printLabel('UNGROUP.')
		except :
			printLabel('ERROR')
	else:
		printLabel('ELEGI ALGUN GRUPO')
#funcion de bakeo de animacion
def bake(obj=[]):
	if obj is not None:
		try:
			mc.refresh (suspend=1)
			mini = mc.playbackOptions(q=1, min=1)
			maxi = mc.playbackOptions(q=1, max=1)
			mc.bakeResults(obj, simulation = 1 , t= (mini, maxi)  )
			mc.refresh (suspend=0)
		except:
			mc.refresh (suspend=0)
	else:
		printLabel ("NO HAY NADA PARA BAKEAR")
#Se encarga de guardar una posicion nueva en la lista y en el archivo
def savePos():
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
			printLabel('NOMBRA LA POSICION.')
	else:
		printLabel('ELIGE UN GRUPO.')
	refreshGui()
#Actualiza los datos de la lista
def refreshGui():
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
	mc.window(win, title='Reloqueitor v1.5', s=0, w=250, h=180, toolbox=1)
	mc.columnLayout(adjustableColumn=True)
	mc.separator(height=5, style='none')
	mc.text(label='Positions:', align='left')
	mc.separator(height=5, style='none')
	mc.textScrollList(posList, w=190, h=190, allowMultiSelection=True, deleteKeyCommand=delSelected , doubleClickCommand='PH_RELOQUEITOR.onMoveClick()')
	mc.separator(height=10, style='none')
	mc.button(win + 'b1', ann='Create a group for the entire selection.', l='1.GROUP', command='PH_RELOQUEITOR.mainGroup()', bgc=[0.5, 0.5, 0.6])
	mc.button(win + 'b2', ann='Move in the position list selectined.', l='2.MOVE', command='PH_RELOQUEITOR.onMoveClick()', bgc=[0.35, 0.46, 0.53])
	mc.button(win + 'b3', ann='Ungroup.', l='3.UNGROUP', command='PH_RELOQUEITOR.unGroup()', bgc=[0.5, 0.46, 0.6])
	mc.button(win + 'b5', ann='REFRESH.', l='REFRESH', command='PH_RELOQUEITOR.refreshGui()', bgc=[0.29,0.36,0.38])
	mc.columnLayout(adjustableColumn=True)
	mc.separator(height=1, style='none')
	mc.text(l='Write name new position.', align='left')
	mc.textFieldGrp(win + 'Seq', ann='Ej. s123_010a' , changeCommand='PH_RELOQUEITOR.savePos()')
	mc.separator(height=1, style='none')
	mc.columnLayout(adjustableColumn=True)
	mc.button(win + 'b4', ann='Save a new position in the list', l='SAVE', command='PH_RELOQUEITOR.savePos()', bgc=[0.8, 0.4, 0.3])
	mc.separator(height=5, style='none')
	mc.text("consola" , l='', backgroundColor=[0.1,0.1,0.1] , align='right', hyperlink=True)
	mc.showWindow(win)
	refreshGui()
