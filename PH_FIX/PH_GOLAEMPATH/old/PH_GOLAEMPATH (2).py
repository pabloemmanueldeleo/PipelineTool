import maya.cmds as cmds
import os
from functools import partial
def golaemCurrentDir():

	types=['CrowdEntityTypeNode']
	selection=cmds.ls(type=types)
	data={}
	for sel in selection:
		if cmds.nodeType(sel) == types[0]:
			currentPath=cmds.getAttr(sel+'.characterFile')
			if not str(currentPath) == 'None':
				print 'Crowd Entity: [' + sel + '] --> ' + str(currentPath)
				data[sel]=currentPath
	return data

def closeUIrefresh(*args):
	global wGolaem
	if cmds.window(wGolaem, ex=1):
		cmds.deleteUI(wGolaem)
		UI_GOLEM()

def nodosGolem(*args):
	data=golaemCurrentDir()
	global wFilaNodo
	global wRowLay
	global wScroll
	wScroll={}
	wRowLay={}
	wFilaNodo={}
	num=0
	wScroll['scroll'] = cmds.scrollLayout(horizontalScrollBarThickness=16,verticalScrollBarThickness=16,childResizable=1)
	for k,v in data.items():
		pathName=v
		wRowLay['rl_'+k]=cmds.rowLayout(numberOfColumns=3,columnWidth3=(200,500,300))
		wFilaNodo['Fila_'+k]= [cmds.checkBox(l=k),cmds.textField(width=700)]
		pop(wFilaNodo['Fila_'+k][1])
		cmds.textField(wFilaNodo['Fila_'+k][1], edit=1,text=pathName)
		num=num+1
		cmds.setParent('..')

def selectDir(*args):
	basicFilter = "*.gcha"
	folder=cmds.fileDialog2(cap=" -ELIJE EL NUEVO ARCHIVO GOLAEM- ",fm=1,fileFilter=basicFilter )
	#filePath=str(str(folder[0]).replace('\\','/'))
	return str(folder)

def golaemChangePath(newDir):
	if newDir != None:
		result=cmds.setAttr(k+'.characterFile', newPath,type="string")

		print 'RE PATH DEL NODO: [' + str(k) +'] --> '+ str(newPath)

def pop(parent_=''):
	pop = cmds.popupMenu(p=parent_,button=3)
	cmds.menuItem(l="CAMBIAR RUTA" , c = selectDir, p=pop)

def checkIfExistPathFile(*args):
	global wFilaNodo
	for kp,kf in wFilaNodo.items():
		path= cmds.textField(str(wFilaNodo[kp][1]),q=1,text=1)
		if not os.path.isdir(str(path)):
			cmds.textField(str(wFilaNodo[kp][1]),edit=1,enableBackground=1,backgroundColor=[1.0,0.2,0.6])
			print 'Chequiar ruta si existe. ' + str(path)
		else:
			cmds.textField(str(wFilaNodo[kp][1]),enableBackground=0)
		if not os.path.exists(str(path)+str(file)):
			cmds.textField(str(wFilaNodo[kp][1]),edit=1,enableBackground=1,backgroundColor=[1.0,0.5,0.6])
			print 'Chequiar Archivo si existe '+str(file)
		else:
			cmds.textField(str(wFilaNodo[kp][1]),enableBackground=0)

def UI_GOLEM(*args):
	global wGolaem
	wGolaem='GolaemCheckPathNode'
	wV=' v0.5'
	wFilaNodo={}
	wColumns={}
	wCheckBoxs={}
	global wRowLay
	global wScroll
	wRowLay={}
	wText={}
	if cmds.window(wGolaem, ex=1):
		cmds.deleteUI(wGolaem)
	cmds.window(wGolaem,title=wGolaem+wV,widthHeight=[800,600],s=0)
	wColumns['cltext_']=cmds.columnLayout(adjustableColumn=1,columnAttach=['both',0],columnOffset=['both',0])
	#Banner image
	imagePath = cmds.internalVar(upd = True) + "M:\PH_SCRIPTS\ICONS\BANNER_GOLEM_.png"
	cmds.image(w = 700, h = 128,backgroundColor=[1,0.8,0], image = imagePath)
	cmds.button(label='Refrescar Nodos', c=closeUIrefresh)
	cmds.button(label='Chequiar Rutas y Archivos', c=checkIfExistPathFile)
	wRowLay['rlText_']=cmds.rowLayout(numberOfColumns=3,columnWidth3=(200,500,300),columnAlign3=['center','center','center'])
	wText['Nodos']=cmds.text(label='Nodos',align='center')
	wText['Rutas']=cmds.text(label='Rutas',align='center')
	cmds.setParent('..')

	nodosGolem()

	checkIfExistPathFile()

	cmds.showWindow(wGolaem)

UI_GOLEM()
