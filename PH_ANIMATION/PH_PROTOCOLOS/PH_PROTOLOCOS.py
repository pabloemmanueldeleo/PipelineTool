#---------------------------------------------------------------------------------------------------------------------------------
#Import
#---------------------------------------------------------------------------------------------------------------------------------
import sys
import maya.cmds as mc
import random as rm
import os

#---------------------------------------------------------------------------------------------------------------------------------
#Funciones Utilidades
#---------------------------------------------------------------------------------------------------------------------------------
#Funcion para el protocolo 100, el cual graba y coloca todo en default los valores de los atrivutos seleccionados
def _characterCtrl(charName,mode=0):

	#Listo todos container del personaje seleccionado
	charControls=mc.ls('%s:*__STKR' % charName,'%s:*__CNTR' % charName)
	#recorro los controles y coloco un key
	for cntr in charControls:
		if mode==0:
			mc.setKeyframe(cntr)

		if mode==1:
			if mc.container(cntr,q=1,pap=1,ba=1):
				for node in mc.container(cntr,q=1,pap=1,ba=1):
					if node!='%s:C_facemask_main__ZTR' % charName:
						_ZeroKey(node)

			mc.setKeyframe(cntr)

def _ZeroKey(cnt):

	keyableAttr=mc.listAttr(cnt,k=1)
	#recorro los atributos
	for attr in keyableAttr:

		#trato de hacer esto
		try:
			#pregunto cual es el valor default de cada atributo y lo seteo
			mc.setAttr(cnt+"."+attr,mc.attributeQuery(attr,n=cnt,ld=1)[0])
			#coloco un key en esos atributos
			mc.setKeyframe (cnt+"."+attr)

		except:
			#De paso trato de dejar un key en ese atributo
			mc.setKeyframe (cnt+"."+attr)

def _cleanUpLista(listName):
	if listName:
		#Ordeno la lista de mayor a menor
		listName.sort()
		#Selecciono el ultimo de la lista
		last = listName[-1]
		for i in range(len(listName)-2, -1, -1):
			if last == listName[i]:
				del listName[i]
			else:
				last = listName[i]
		print listName
	#Devuelvo el dato ordenado de la funcion
	return listName

#---------------------------------------------------------------------------------------------------------------------------------
#Funciones para UI
#---------------------------------------------------------------------------------------------------------------------------------
def _protocolo0Key():

	nameSpaceSelected=[]

	for obj in mc.ls(sl=1):
		if len(obj.split(':'))==3:
			nameSpace=':'.join(obj.split(':')[:-1])
			nameSpaceSelected.append(nameSpace)
			print nameSpace

	nameSpaceSelected=_cleanUpLista(nameSpaceSelected)

	for nameSpace in nameSpaceSelected:
		_characterCtrl(nameSpace,mode=1)

'''
	#Aqui guardare los namespace
	nameSpaceSelected=[]

	for obj in mc.ls(sl=1):
		if len(obj.split(':'))==3:
			nameSpace=':'.join(obj.split(':')[:-1])
			nameSpaceSelected.append(nameSpace)
			print nameSpace

	#Ejecuto la funcion para ordenar y limpiar los namespace
	nameSpaceSelected=_cleanUpLista(nameSpaceSelected)
	print 'NAMESPACESELECTED ',nameSpaceSelected

	if len(nameSpaceSelected)>0:

		#suspend the refresh
		mc.refresh(su=1)

		#get the current frame and go to start point
		currentFrame=mc.currentTime(q=1)
		mc.currentTime(0)

		#try to put the keys
		for nameSpace in nameSpaceSelected:
			try:
				_characterCtrl(nameSpace,mode=1)
				print 'PROTOCOLO FRAME 0 FUNCIONO EN: ',nameSpace
			except:
				print 'NO FUNCIONO PROTOCOLO 0 EN: ',nameSpace

		#set the current frame back to where it was
		mc.currentTime(currentFrame)

		#resume refresh
		mc.refresh(su=0)
 '''

def _Protocolo60Key():
	mc.copyKey( charName, time=(0,90), option="curve")
	mc.currentTime(60)
	mc.pasteKey()

#Range Time Line
def _rangeTimeLine():

    cnts= mc.ls(sl=1)
    keys=mc.keyframe(cnts, q=1)
    cTime=mc.currentTime( query=True )
    if keys:
        keys.sort()
        firstKey = keys[1]
        lastKey = keys[-1]
        '''firstKey = mc.findKeyframe(timeSlider=True, which='first')
        lastKey = len(mc.keyframe(q=1)) + firstKey
        mc.findKeyframe(timeSlider=True, which='last')
        if firstKey == lastKey:
            mc.warning('El control tiene un solo key')'''
        mc.playbackOptions(min=int(firstKey)-10,max=int(lastKey)+24)
        mc.playbackOptions(animationStartTime=int(firstKey)-14,animationEndTime=int(lastKey)+14)
        mc.currentTime(cTime)
    else:
        mc.warning(('Lo que seleccionaste no tiene animacion.').upper())
        mc.currentTime(cTime)

#---------------------------------------------------------------------------------------------------------------------------------
#UI
#---------------------------------------------------------------------------------------------------------------------------------
def _UIprotoloco():
	if mc.window('protowin',ex=True):
		mc.deleteUI('protowin')

	if mc.dockControl('dockWin',ex=True):
		mc.deleteUI('dockWin')


	protoWinV=mc.window('protowin',s=0)
	buttonForm=mc.rowColumnLayout(parent=protoWinV, numberOfRows=1)
	mc.button(parent=buttonForm, label='TIME RANGE', command='PH_PROTOLOCOS._rangeTimeLine()',bgc=(0.1,0.8,0.0))
	mc.button(parent=buttonForm, label='Protocolo KEY 0', command='PH_PROTOLOCOS._protocolo0Key()',w=100,h=20,bgc=(1.0,0.4,0.0),visible=0 )
	mc.button(parent=buttonForm, label='Protocolo KEY 60', command='PH_PROTOLOCOS._protocolo60Key()',bgc=(1.0,0.5,0.0),visible=0 )
	mc.button(parent=buttonForm, label='Protocolo KEY 90', bgc=(1.0,0.6,0.0),visible=0 )
	mc.button(parent=buttonForm, label='Protocolo KEY 100', bgc=(1.0,0.7,0.0),visible=0  )
	mc.button(parent=buttonForm, label='Protocolo KEY +5', bgc=(1.0,0.8,0.0),visible=0  )
	#dock bar
	mc.dockControl('dockWin',label='PROTOLOCOS PH TOOL v0.2', area='bottom', content=protoWinV, allowedArea='right')
