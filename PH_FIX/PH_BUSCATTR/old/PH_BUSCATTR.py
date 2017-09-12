import maya.cmds
global lista
lista=['']
global tf
wCoco='PH_BUSCATTR'
vCoco=' v0.1'
if cmds.window(wCoco,title=wCoco,exists=True):
	cmds.deleteUI(wCoco)
winCoco=cmds.window(wCoco,title=wCoco+vCoco,s=1)
cmds.columnLayout(adj=True)
cmds.text(label='BUSCA NODOS Y ATRIBUTOS')
cmds.separator(style='in', h=20)
cmds.text(label='Nodo:')
tf=cmds.textField(annotation='Ej.: Si pones exactamente "camera"\n te listara todas los nodos de camaras en la escena.',placeholderText='ej. "aiStandard"',changeCommand='buscarNodo()',enterCommand='buscarNodo()')
cmds.text(label='Atributo:')
nameAttr=cmds.textField(annotation='Ej.: Si pones exactamente ".tx"\n te seleccionara todos los nodos que contenga esos atributos.',placeholderText='ej. "transforms"',changeCommand='selectAttr()',enterCommand='selectAttr()')
cmds.separator(style='in', h=30)
listaN=cmds.textScrollList(lista,append=lista,h=300)
cmds.textField(placeholderText='Buscar')
cmds.showWindow(winCoco)

def buscarNodo():
	global lista
	global tf

	nodoType='camera'
	nodoType = str(cmds.textField(tf,q=1,text=True))

	nodoList=[]
	try:
		nodoList = cmds.ls( type=nodoType)
	except:
		pass

	if nodoList == None:
		nodoList.append('Especifica un tipo de nodo.')
	nodoList.sort()

	lista=[]

	for nodo in nodoList:
		cmds.textScrollList(listaN, edit=True, append=nodo)

def selectAttr():
	global lista
	global nameAttr
	OBJ_ATTR={}
	nameAttr=''
	nameAttr = str(cmds.textField(nameAttr,q=1,text=True))

	for n in lista:
		OBJ_ATTR[n]=attr=cmds.listAttr(n)
	if nameAttr in atr:
		nameAttr=cmds.getAttr(atr)
