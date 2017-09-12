import maya.cmds as cmds
import os
from functools import partial

funcionDicc={'ButtonEvents' : {}}
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
	wRowLay={}
	wFilaNodo={}
	wScroll={}
	num=0
	wScroll['scroll'] = cmds.scrollLayout(horizontalScrollBarThickness=16,verticalScrollBarThickness=16,childResizable=1)
	for k,v in data.items():
		fileName=str(v.split('/')[-1])
		pathName=str(v.split(fileName)[0])
		wRowLay['rl_'+k]=cmds.rowLayout(numberOfColumns=4,columnAttach4=['left','right','right','right'],columnWidth4=(150,50,500,400),columnAlign4=["left","left", "right","right"])
		wFilaNodo[k] = [cmds.checkBox(l=k),
								cmds.button(label=':',c=partial(setPath,k)),
								cmds.textField(w=500,cc=partial(getPath,k)),
								cmds.textField(w=400,cc=partial(getPath,k))]
		pop(wFilaNodo[k][2])
		cmds.textField(wFilaNodo[k][2], edit=1,text=pathName)
		pop(wFilaNodo[k][3])
		cmds.textField(wFilaNodo[k][3], edit=1,text=fileName)
		num=num+1
		cmds.setParent('..')

def getPath(control_,*args):
    global getPath
    Path = cmds.textField ( control_ ,q=1, text=1 )
    golaemChangePath(control_,Path)

def setPath(v,):
	global wFilaNodo
	result=cmds.setAttr(v+'.characterFile', newDir,type="string")

def selectDir(v,*args):
	global wFilaNodo
	basicFilter = "*.gcha"
	folder=cmds.fileDialog2(cap=" -ELIJE EL NUEVO ARCHIVO GOLAEM- ",
								fm=1,fileFilter=basicFilter)
	if folder:
		setPath()
	#filePath=str(str(folder[0]).replace('\\','/'))
	return str(folder)


def golaemChangePath(k,newDir):

	if newDir != None:
		result=cmds.setAttr(k+'.characterFile', newDir,type="string")
		print 'RE PATH DEL NODO: [' + str(k) +'] --> '+ str(newDir)

def pop(parent_=''):
	pop = cmds.popupMenu( p=parent_ ,button=3 )
	pathText = cmds.textField( parent_ ,q=1 ,fullPathName=1 )
	cmds.menuItem(l="CAMBIAR RUTA" , c = partial(getPath,pathText), p=pop)


def checkIfExistPathFile(*args):
	rojo=[1.0,0.2,0.6]
	nada=[1.0,1.0,1.0]
	global wFilaNodo
	for kp,kf in wFilaNodo.items():
		path= cmds.textField(str(wFilaNodo[kp][2]),q=1,text=1)
		file= cmds.textField(str(wFilaNodo[kp][3]),q=1,text=1)

		if not os.path.isdir(str(path)):
			cmds.textField(str(wFilaNodo[kp][2]),edit=1,backgroundColor=rojo)
			print 'Chequiar ruta si existe. ' + str(path)
		else:
			cmds.textField(str(wFilaNodo[kp][2]),edit=1,enableBackground=0)
		if not os.path.exists(str(path)+str(file)):
			cmds.textField(str(wFilaNodo[kp][3]),edit=1,backgroundColor=rojo)
			print 'Chequiar Archivo si existe '+str(file)
		else:
			cmds.textField(str(wFilaNodo[kp][3]),edit=1,enableBackground=0)

def UI_GOLEM(*args):
	global wGolaem
	wGolaem='GolaemCheckPathNode'
	wV=' v0.5'
	wFilaNodo={}
	wColumns={}
	wCheckBoxs={}
	global wRowLay
	wRowLay={}
	wText={}
	if cmds.window(wGolaem, ex=1):
		cmds.deleteUI(wGolaem)
	cmds.window(wGolaem,title=wGolaem+wV,s=1)
	wColumns['cltext_']=cmds.columnLayout(adjustableColumn=1,height=460,columnAttach=['both',0],columnOffset=['both',0])
	#Banner image
	imagePath = cmds.internalVar(upd = True) + "M:\PH_SCRIPTS\ICONS\BANNER_GOLEM_.png"
	cmds.image(w = 700, h = 88,backgroundColor=[1,0.8,0], image = imagePath)
	cmds.button(label='Refrescar Nodos', c=closeUIrefresh)
	cmds.button(label='Chequiar Rutas y Archivos', c=checkIfExistPathFile)
	wRowLay['rlText_']=cmds.rowLayout(numberOfColumns=4,columnAttach4=['left','right','right','right'],columnWidth4=(150,50,500,400),columnAlign4=["left","left", "left","right"])
	wText['Nodos']=cmds.text(label='Nodos',align='center')
	wText['Rutas']=cmds.text(label='Rutas',align='center')
	wText['Files']=cmds.text(label='Archivos',align='center')
	cmds.setParent('..')

	nodosGolem()

	#checkIfExistPathFile()

	cmds.showWindow(wGolaem)

UI_GOLEM()
