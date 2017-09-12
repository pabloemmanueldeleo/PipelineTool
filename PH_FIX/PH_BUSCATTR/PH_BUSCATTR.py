import maya.cmds
global lista
global listaAttr
global nameAttr
global listaN
global listaA
lista=['']
listaAttr=['']
global OBJ_ATTR
OBJ_ATTR={}

def selectAttr(*arg):
	print 'bien ahi amio'
	global lista
	global nameAttr
	global listaN
	global OBJ_ATTR
	nodoType=[]

	cmds.textScrollList(listaN, edit=True,sii=1)

	nodoType = cmds.textField(nameAttr,q=1,text=True)
	nodoDag=cmds.ls( dagObjects=True )

	for nodo in nodoDag:
		attr=cmds.listAttr(nodo)
		OBJ_ATTR[nodo]=attr
		cmds.textScrollList(listaN, edit=True, append=nodo)


def selectNode():
	global listaN
	sel=cmds.textScrollList(listaN, q=1,selectItem=True)
	print sel


def buscar():
	print 'ok'


def UI_BUSCATTR():
	wCoco='PH_BUSCATTR'
	vCoco=' v0.1'

	if cmds.window(wCoco,title=wCoco,exists=True):
		cmds.deleteUI(wCoco)

	winCoco=cmds.window(wCoco,title=wCoco+vCoco,s=1)
	cmds.columnLayout(winCoco+'cl',adj=True,adjustableColumn=True)
	cmds.text(winCoco+'tx',label='BUSCA EL NODO QUE CONTIENE TAL ATRIBUTO')
	cmds.separator(winCoco+'sp',style='in', h=20)

	cmds.text(winCoco+'tx2',label='Atributo:')
	nameAttr=cmds.textField(winCoco+'tf',annotation='Ej.: Si pones exactamente ".tx"\n te seleccionara todos los nodos que contenga esos atributos.',placeholderText='ej. "transforms"',changeCommand='selectAttr()',enterCommand='selectAttr()')
	cmds.separator(winCoco+'sp2',style='in', h=30)

	cmds.rowLayout(winCoco+'rl', numberOfColumns=2)

	cmds.columnLayout(winCoco+'cl2',adj=True,adjustableColumn=True,p=winCoco+'rl')
	cmds.text(label='Nodos')
	listaN=cmds.textScrollList(winCoco+'tslNodos',append=lista,h=300,doubleClickCommand='selectNode()')
	cmds.textScrollList(winCoco+'tslNodos', edit=True,sii=1)

	cmds.columnLayout(winCoco+'cl3',adj=True,adjustableColumn=True,p=winCoco+'rl')
	cmds.text(label='Atributos')
	listaA=cmds.textScrollList(winCoco+'tslAtrr',append=listaAttr,h=300,doubleClickCommand='selectNode()')

	cmds.columnLayout(winCoco+'cl4',adj=True,adjustableColumn=True,p=wCoco)
	cmds.textField(placeholderText='Buscar',changeCommand='buscar()',enterCommand='buscar()')

	selectAttr()

	cmds.showWindow(winCoco)
UI_BUSCATTR()
