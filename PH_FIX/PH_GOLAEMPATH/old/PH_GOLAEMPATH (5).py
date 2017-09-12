import maya.cmds as cmds
import os
from functools import partial
from collections import OrderedDict

global types
types={'CrowdEntityTypeNode':[[0.23,0.23,0.23],'GOLAEM_CLOW'],
		'SimulationCacheProxy':[[0.16,0.16,0.16],'GOLAEM_PROXY'],
			'TerrainLocator':[[0.21,0.21,0.21],'GOLAEM_TERRAIN'],
			'AlembicNode':[[0.20,0.20,0.20],'ALEMBIC_FILE'],
			'reference':[[0.17,0.17,0.17],'REFERENCIA_NODE']}
def golaemCurrentDir(types={}):
	tipos=types.keys()
	tipos.sort()
	for t in tipos:
		algo=cmds.ls(type=t,objectsOnly=1)
		if not algo:
			tipos.remove(t)

	selection=cmds.ls(type=tipos)
	data={}
	currentPath=None
	for sel in selection:
		if cmds.nodeType(sel) == 'CrowdEntityTypeNode':
			currentPath=cmds.getAttr(sel+'.characterFile')
			color=types['CrowdEntityTypeNode'][0]
			tipo=types['CrowdEntityTypeNode'][1]
		elif cmds.nodeType(sel) == 'SimulationCacheProxy':
			inputCacheDir=cmds.getAttr(sel+'.inputCacheDir')
			inputCacheName=cmds.getAttr(sel+'.inputCacheName')
			crowdFields=cmds.getAttr(sel+'.crowdFields')
			currentPath=inputCacheDir+'/'+inputCacheName+'/'
			color=types['SimulationCacheProxy'][0]
			tipo=types['SimulationCacheProxy'][1]
		elif cmds.nodeType(sel) == 'TerrainLocator':
			navMeshFile=cmds.getAttr(sel+'.navMeshFile')
			currentPath=navMeshFile
			color=types['TerrainLocator'][0]
			tipo=types['TerrainLocator'][1]
		elif cmds.nodeType(sel) == 'AlembicNode':
			AlembicNode=cmds.getAttr(sel+'.abc_File')
			currentPath=str(AlembicNode)
			color=types['AlembicNode'][0]
			tipo=types['AlembicNode'][1]
		elif cmds.nodeType(sel) == 'reference':
			try:
				reference=cmds.referenceQuery( sel,filename=True )
				currentPath=str(reference)
				color=types['reference'][0]
				tipo=types['reference'][1]
			except:
				pass

		if not str(currentPath) == 'None':
			#print sel +': [' + sel + '] --> ' + str(currentPath)
			data[sel]=currentPath,color,tipo
	return data

def nodosGolem(*args):
	global types
	data=golaemCurrentDir(types)
	global wFilaNodo
	global wRowLay
	global wScroll
	wRowLay={}
	wFilaNodo={}
	wScroll={}
	num=0

	# dictionary sorted by key
	#data=OrderedDict(sorted(data.items(), key=lambda t: t[0]))
	data = OrderedDict(sorted(data.items()))

	wScroll['scroll'] = cmds.scrollLayout(horizontalScrollBarThickness=16,verticalScrollBarThickness=16,childResizable=0)
	#rutas y archivos
	for k,v in data.items():
		base=os.path.basename(v[0])
		path=os.path.dirname(v[0])
		if base:
			fileName=str(base)
		else:
			fileName='Nada por aqui'
		if path:
			pathName=str(path)+'/'
		else:
			pathName='Nada por aqui'

		wRowLay['rl_'+k]=cmds.rowLayout(numberOfColumns=4,bgc=v[1],columnAttach4=['left','right','right','right'],columnWidth4=(150,50,370,340),columnAlign4=["left","left", "right","right"])
		wFilaNodo[k] = [  cmds.text(l=v[2],annotation=k),
								cmds.button(label=':',c=partial(selectNode,k),w=50),
								cmds.textField(w=370,editable=False),
								cmds.textField(w=350,editable=False)]

		#pop(wFilaNodo[k][2])
		#print k,fileName,pathName, wFilaNodo[k][2],wFilaNodo[k][3]
		cmds.textField(wFilaNodo[k][2], edit=1,ec=partial(queryGetPathTextField,k,wFilaNodo[k][2],wFilaNodo[k][3]),text=pathName)
		#pop(wFilaNodo[k][3])
		cmds.textField(wFilaNodo[k][3], edit=1,ec=partial(queryGetPathTextField,k,wFilaNodo[k][2],wFilaNodo[k][3]),text=fileName)
		num=num+1
		cmds.setParent('..')

def queryGetPathTextField(v,textFieldsRuta,textFieldsFile,*args):
	global wFilaNodo
	global getPath
	path = cmds.textField ( textFieldsRuta ,q=1, text=1 )
	file = cmds.textField ( textFieldsFile ,q=1, text=1 )
	cmds.setAttr(v+'.characterFile', str(path)+str(file),type="string")

def selectDir(v,*args):
	global wFilaNodo
	basicFilter = "*.gcha"
	folder=cmds.fileDialog2(cap=" -ELIJE EL NUEVO ARCHIVO GOLAEM- ",
								fm=1,fileFilter=basicFilter)
	if folder:
		setPath()
	#filePath=str(str(folder[0]).replace('\\','/'))
	return str(folder)

def pop(parent_=''):
	pop = cmds.popupMenu( p=parent_ ,button=3 )
	pathText = cmds.textField( parent_ ,q=1 ,fullPathName=1 )
	cmds.menuItem(l="CAMBIAR RUTA" , c = partial(queryGetPathTextField,pathText), p=pop)

def selectNode(sel='',*args):
	if cmds.objExists(sel):
		cmds.select(sel)
	else:
		cmds.warning('No existe el nodo' + str(sel))

def checkIfExistPathFile(*args):
	rojo=[1.0,0.2,0.6]
	nada=[1.0,1.0,1.0]
	global wFilaNodo
	for kp,kf in wFilaNodo.items():
		path= cmds.textField(str(wFilaNodo[kp][2]),q=1,text=1)
		file= cmds.textField(str(wFilaNodo[kp][3]),q=1,text=1)
		if not os.path.isdir(str(path)):
			cmds.textField(str(wFilaNodo[kp][2]),edit=1,backgroundColor=rojo)
			#print 'Chequiar ruta si existe. ' + str(path)
		else:
			cmds.textField(str(wFilaNodo[kp][2]),edit=1,enableBackground=0)
		if not os.path.exists(str(path)+str(file)):
			cmds.textField(str(wFilaNodo[kp][3]),edit=1,backgroundColor=rojo)
			#print 'Chequiar Archivo si existe '+str(file)
		else:
			cmds.textField(str(wFilaNodo[kp][3]),edit=1,enableBackground=0)

def closeUIrefresh(*args):
	global wGolaem
	if cmds.window(wGolaem, ex=1):
		cmds.deleteUI(wGolaem)
		UI_GOLEM()

def UI_GOLEM(*args):
	global wGolaem
	wGolaem='PH_GOLAEMPATH'
	wV=' v0.9'
	wFilaNodo={}
	wColumns={}
	wCheckBoxs={}
	global wRowLay
	wRowLay={}
	wText={}
	if cmds.window(wGolaem, ex=1):
		cmds.deleteUI(wGolaem)
	cmds.window(wGolaem,title=wGolaem+wV,w=980,h=500,s=1,resizeToFitChildren=1)
	wColumns['cltext_']=cmds.columnLayout(adjustableColumn=1,columnAttach=['both',0],columnOffset=['both',0])
	#Banner image
	imagePath = cmds.internalVar(upd = True) + "M:\PH_SCRIPTS\ICONS\BANNER_GOLEM_.png"
	cmds.image(w = 700, h = 50,backgroundColor=[1,0.8,0], image = imagePath)

	cmds.button(label='Refrescar Nodos', c=closeUIrefresh)
	#cmds.button(label='Chequiar Rutas y Archivos', c=checkIfExistPathFile)
	wRowLay['rlText_']=cmds.rowLayout(numberOfColumns=4,columnAttach4=['left','left','left','left'],columnWidth4=(150,50,370,340),columnAlign4=["center","left", "left","right"])
	wText['Nodos']=cmds.text(label='Nodos',align='center')
	wText['Sel']=cmds.text(label='Sel',align='center')
	wText['Rutas']=cmds.text(label='Rutas',align='center')
	wText['Files']=cmds.text(label='Archivos',align='center')
	cmds.setParent('..')

	nodosGolem()

	checkIfExistPathFile()

	cmds.showWindow(wGolaem)
