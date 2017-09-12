import maya.cmds as cmds
import os

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


def nodosGolem(*args):
	data=golaemCurrentDir()
	global wFilaNodo
	global wRowLay
	global wScroll
	wScroll.clear()
	wRowLay.clear()
	wFilaNodo.clear()
	num=0
	wScroll['scroll'] = cmds.scrollLayout(horizontalScrollBarThickness=16,verticalScrollBarThickness=16,childResizable=1)
	for k,v in data.items():
		fileName=str(v.split('/')[-1])
		pathName=str(v.split(fileName)[0])
		wRowLay['rl_'+k]=cmds.rowLayout(numberOfColumns=4,columnWidth4=(200,500,300,250))
		wFilaNodo['Fila_'+k]= [cmds.checkBox(l=k),cmds.textField(width=500),cmds.textField(width=300)]
		cmds.textField(wFilaNodo['Fila_'+k][1], edit=1,text=pathName)
		cmds.textField(wFilaNodo['Fila_'+k][2], edit=1,text=fileName)
		num=num+1
		cmds.setParent('..')

def golaemChangePath(newDir='M:/MAYA/05_SHOTS/UD15/E105/01_CHAR'):
	for k,v in data.items():
			fileName= v.split("/")[3:]
			fileName= str(fileName[0])+"/"+str(fileName[1])
			newPath= os.path.join(fileName,newDir+'/'+fileName)
			#newPath=str(str(newPath).replace('/','\\'))
			result=cmds.setAttr(k+'.characterFile', newPath,type="string")
			print 'RE PATH DEL NODO: [' + str(k) +'] --> '+ str(newPath)

def checkIfExistPathFile(*args):
	global wFilaNodo
	for kp,kf in wFilaNodo.items():
		path= cmds.textField(str(wFilaNodo[kp][1]),q=1,text=1)
		file= cmds.textField(str(wFilaNodo[kp][2]),q=1,text=1)
		if not os.path.isdir(str(path)):
			cmds.textField(str(wFilaNodo[kp][1]),edit=1,backgroundColor=[1.0,0.2,0.6])
			print 'Chequiar ruta si existe. ' + str(path)
		if not os.path.exists(str(path)+str(file)):
			cmds.textField(str(wFilaNodo[kp][2]),edit=1,backgroundColor=[1.0,0.5,0.6])
			print 'Chequiar Archivo si existe '+str(file)

def UI_GOLEM(*args):
	wGolaem='GolaemCheckPathNode'
	wV=' v0.5'
	wFilaNodo={}
	wColumns={}
	wCheckBoxs={}
	global wRowLay
	wRowLay={}
	wScroll={}
	wText={}
	if cmds.window(wGolaem, ex=1):
		cmds.deleteUI(wGolaem)
	cmds.window(wGolaem,title=wGolaem+wV,widthHeight=[480,600])
	wColumns['cltext_']=cmds.columnLayout(adjustableColumn=1,columnAttach=['both',0],columnOffset=['both',0])
	cmds.button(label='Refrescar Nodos', c=nodosGolem)
	cmds.button(label='Chequiar Rutas y Archivos', c=checkIfExistPathFile)
	wRowLay['rlText_']=cmds.rowLayout(numberOfColumns=4,columnWidth4=(200,500,300,250),columnAlign4=['center','center','center','center'])
	wText['Nodos']=cmds.text(label='Nodos',align='center')
	wText['Rutas']=cmds.text(label='Rutas',align='center')
	wText['Files']=cmds.text(label='Files',align='center')
	cmds.setParent('..')

	nodosGolem()

	checkIfExistPathFile()

	cmds.showWindow(wGolaem)

UI_GOLEM()
