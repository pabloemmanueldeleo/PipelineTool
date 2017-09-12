import sys
import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
childrenMsh=[]
listNodesAlemb=[]
def _startTranfer():
    if len(cmds.ls( sl=True )) == 1:
        childrenT=[]
        #Lista de nodos de alembic para mostrar
        padreTgt= cmds.ls( sl=True )[0]
        #childrenT = cmds.listRelatives(padreTgt, path=True)
        childrenT = cmds.listRelatives(padreTgt, fullPath=True,noIntermediate=True)
        for v in range(len(childrenT)):
            o=cmds.listRelatives(childrenT[v],fullPath=True)
            if cmds.nodeType(o[0]) == 'mesh':
                childrenMsh.append(o[0])
                
    else:
        print 'SELECCIONA UN NODO DE ALEMBIC'
aNode=_selectNode()
nodeNew=childrenMsh[0]
def _oldNodeTonewNode(aNode,nodeNew):
#Si el nodo tiene un outPolyMesh se conectara
if 'outPolyMesh' in cmds.listAttr(aNode,readOnly=True):
    nodoDict = {}
    trfDicTrg = {}
    nodoDictConect = {}
    outAttr='outPolyMesh'
    inAttr='inMesh'
    childrenMsh=[]
    childrenT=[]
    polyMeshNumbre = []
    polyMeshNumbre = cmds.getAttr(aNode+'.'+outAttr, size=True)
    #------------------#recorro el tamaño de conexiones en el polyMesh
    for i in range(polyMeshNumbre):
        #agarro el shape del nodo y lo guardo con su key en su diccionario
        nodoDict[i] = str(cmds.listConnections(aNode+'.'+outAttr+str([i]), shapes=1)[0])
        #si esta dentro de un grupo vamos por aca
        if '|' in nodoDict[i]:
            nodoDict[i] = nodoDict[i].split('|')[-1:]
        #guardo la conexion completa vieja donde se conecta el nodo
        nodoDictConect[i] = cmds.listConnections(aNode+'.'+outAttr+str([i]),plugs=1)[0]
    #-------------------#listamos el grupo a conectar
        if len(cmds.ls( sl=True )) == 1:
            #Lista de nodos de alembic para mostrar
            padreTgt= cmds.ls( sl=True )[0]
            #childrenT = cmds.listRelatives(padreTgt, path=True)
            childrenT = cmds.listRelatives(padreTgt, fullPath=True,noIntermediate=True)
            for v in range(len(childrenT)):
                #busco el shape
                o=cmds.listRelatives(childrenT[v],fullPath=True)
                if cmds.nodeType(str(o[0])) == 'mesh':
                    if '|' in o[0]:
                        o=o[0].split('|')[-1:]
                        trfDicTrg[childrenT[v]+'|'] = o[0]
                        childrenMsh.append(str(o[0]))
                    else:
                        childrenMsh.append(o[0])
    
        #------------------------
            for k, v in trfDicTrg.items():
                if nodoDict[i][0] == v:
                    #Desconecto y lo guardo
                    if cmds.isConnected(aNode+'.'+outAttr+str([i]),nodoDictConect[i]):
                        desConects = cmds.disconnectAttr(aNode+'.'+outAttr+str([i]),nodoDictConect[i])
                        print 'Desconecte ' + str(desConects)
                        #Conecto el nodo a la otra geometria en inMehs
                        conect = cmds.connectAttr(aNode+'.'+outAttr+str([i]),k+v+'.'+inAttr)
                        print 'Conectado'
                    else:
                        print 'No existe conexion de ' + aNode+'.'+outAttr+str([i]) + 'con' + str(nodeOLDplug)
else:
    print 'El script por ahora solo contempla si el nodo tiene polyMesh'

def _selectNode():

    selectNode = cmds.textScrollList(listNodesAlemb, q=True, selectItem=True)
    #selectNode = cmds.listRelatives(selectNode[0],children=True, fullPath=True)
    #cmds.select(selectNode)
    return selectNode[0]

def _initGui():
    
    if listNodesAlemb==[]:
        print 'NO EXISTE NINGUN NODO DE ALEMBIC EN ESTE FILE'
    else:
        #ordeno listas
        listNodesAlemb.sort()
    
        for lna in listNodesAlemb:
        	cmds.textScrollList(listNodesAlemb, edit=True, append=str(lna))
    
        if len(cmds.textScrollList(listNodesAlemb, q=True, allItems=True)):
        	cmds.textScrollList(listNodesAlemb, edit=True, selectIndexedItem=1)

def _refreshGui():
    # remove all existing items from the textScrollList, then repopulate it with initGui()
    cmds.textScrollList(listNodesAlemb, edit=True, removeAll=True)
    _initGui();

def _makeWindow(winName='PH_ALEMBICtoINMESH'):
    
    listNodesAlemb=[]
    #lista de camaras en scena
    listNodesAlemb = cmds.ls(type='AlembicNode')
    
    if cmds.window(winName, exists=True):
        cmds.deleteUI(winName)
    
    cmds.window( winName, h=250 ,w=200,s=True )
    cmds.columnLayout(adjustableColumn = True)
    cmds.text('NODOS ALEMBIC EN FILE')
    cmds.rowLayout( numberOfColumns=2 )
    cmds.textScrollList(listNodesAlemb, allowMultiSelection=False, selectCommand="_selectNode()")
    cmds.columnLayout(adjustableColumn = True)
    cmds.button( label='TRANFER ALEMBIC', command="_startTranfer()", bgc=(0.2,0.8,0.0))
    cmds.showWindow()
    
    #inicio la lista
    _initGui()

_makeWindow()