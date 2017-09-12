import maya.cmds as cmds
import math
import random
global source
global targets
global fuente
global lFuente
source=[]
targets=[]

#remplaza todos los objetos por uno solo dejandole la misma posicion y el mismo shader
#input: source= array[],targets=[]
def remplaceObj(source=None,targets=None):
	if len(source)>0 and len(targets)>0:
		padre=None
		t=[None]
		r=[None]
		s=[None]
		for obj in targets:
			try:
				if '|' in obj:
					newName=str(obj.split('|')[-1])
					shapeName=cmds.listRelatives(str(obj.split('|')[-1]))
			except:
				newName=str(obj)
				shapeName=cmds.listRelatives(obj)
			try:
				if ':' in newName:
					newName=str(newName.split(':')[-1])
			except:
				newName=str(obj)
				shapeName=cmds.listRelatives(obj)

			#duplicamos objeto
			try:
				objNew = cmds.duplicate( source,n=str(source)+'_NEWOBJ'+str(random.randint(0,10000)) )
			except ValueError:
				cmds.delete(objNew)
				print 'No es valido esa fuente'

			try:
				#llevar el objeto al otro
				PCNS=cmds.parentConstraint(obj,objNew[0],maintainOffset=False)
				SCNS=cmds.scaleConstraint(obj,objNew[0],maintainOffset=False)
				cmds.delete(PCNS)
				cmds.delete(SCNS)
			except:
				pass

			#si contiene grupo lo emparento
			try:
				if cmds.listRelatives(obj,parent=True):
					padre=cmds.listRelatives(obj,parent=True,fullPath=True)[0]
					cmds.parent( objNew[0],padre )
			except:
				pass

			#aplico el material
			mat=obtenerSG(cmds.listRelatives(source)[0])
			try:
				asignarSHDaListaObjetos(objNew[0],mat)
				print 'Se aplico el shader '+ mat
			except:
				cmds.delete(objNew)
				pass

			print cmds.delete(obj)

			newName= cmds.rename(objNew[0],newName)
			try:
				print cmds.rename(cmds.listRelatives(newName,str(shapeName)))
			except:
				print 'No pude renombrar'+ newName
	else:
		cmds.warning('No hay objetos en la lista ameooooo.')

def remplace(*args):
	global source
	global targets
	refreshGui()
	remplaceObj( source, targets )

def deleteO(*args):
	global lFuente
	global targets
	selec=cmds.textScrollList(lFuente, q=1, selectItem=True)
	for sel in selec:
		targets.remove(sel)
		print 'Se borro de la lista a remplazar '+ sel
	refreshGui()

def getFuente(*args):
	global fuente
	global source
	if cmds.ls(sl=1):
		source=cmds.ls(sl=1,absoluteName=True)[0]
		cmds.textField(fuente, edit=True, placeholderText=str(source))
		cmds.textField(fuente, edit=True, text=source)
		refreshGui()
	else:
		cmds.warning('Aun no has seleccionado un objeto fuente.')

def getObjetivos(*args):
	global source
	global targets
	global lFuente
	global fuente
	targets=cmds.ls(sl=1)
	for target in targets:
		cmds.textScrollList(lFuente, edit=True, append=target)
	refreshGui()

def refreshGui():
	global lFuente
	global targets
	global source
	global num

	source=cmds.textField( fuente,q=1, text=True )
	if source in targets:
		selec=cmds.textField(fuente,q=1 ,text=True)
		targets.remove(source)

	cmds.textScrollList(lFuente, edit=True, removeAll=True)

	for t in targets:
		cmds.textScrollList(lFuente, edit=True, append=t)
	cmds.text(num,edit=True,label=str(len(targets)))

#Busco el shaderGroup de un material
def obtenerSG(shader=None):
    if shader:
        if cmds.objExists(shader):
            sgq = cmds.listConnections(shader, d=True, et=True, t='shadingEngine')
            if sgq:
                return sgq[0]
    return None
#Asigna material a una lista de objetos.
def asignarSHDaListaObjetos(objList=None, shader=None):
    shaderSG = obtenerSG(shader)
    if objList:
        if shaderSG:
			try:
				cmds.sets(objList, e=True, forceElement=shaderSG)
			except:
				pass
        else:
            print 'NO ENCONTRO EL SHADING GROUP.'
    else:
        print 'CHABON SELECCIONA UNO O MAS OBJETOS.'

def UI_REMPLAZAROBJETOS(*args):
	global fuente
	global lFuente
	global source
	global targets
	global num
	vUIREM='PH_REMPLAZAROBJETOS'
	v=' v0.1'

	if cmds.window(vUIREM,title=vUIREM,exists=True):
		cmds.deleteUI(vUIREM)

	winPH=cmds.window(vUIREM,title=vUIREM+v,s=1)
	cmds.columnLayout(vUIREM+'cl',adj=True,adjustableColumn=True)
	cmds.button(label='AGREGAR FUENTE',c=getFuente)
	fuente=cmds.textField(placeholderText='FUENTE',enable=True)
	cmds.separator( vUIREM+'sp',style='in', h=20)
	cmds.columnLayout(vUIREM+'cl1',adj=True,adjustableColumn=True)
	cmds.rowColumnLayout( vUIREM+'rl', numberOfColumns=2,p=vUIREM+'cl1')
	cmds.text ( vUIREM+'tx2',label='OBJETOS A REMPLAZAR: ',align='left' )
	num=cmds.text ( vUIREM+'txtnum',label= '0',align='left')

	cmds.columnLayout(vUIREM+'cl2',adj=True,adjustableColumn=True,p=winPH)
	cmds.button(label='AGREGAR OBJETOS',c=getObjetivos)
	lFuente=cmds.textScrollList(vUIREM+'tslNodos',append=targets,h=250,allowMultiSelection=True,deleteKeyCommand=deleteO)
	cmds.button(label='REMPLAZAR X FUENTE',c=remplace,h=50,bgc=(0.2,0.3,0.6))
	cmds.showWindow(winPH)
