import sys
import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel

def _startTranfer():
    if cmds.ls( sl=True ):
        childrenT=['']
        childrenTgt=[]
        #Lista de nodos de alembic para mostrar
        listNodesAlemb=[]
        padreTgt=cmds.ls( sl=True )[0]
        childrenT = cmds.listRelatives(padreTgt, path=True)
        for v in childrenT:
            if cmds.nodeType(v[0]) == 'mesh':
                childrenTgt.append(v[0])
        childrenTgt.sort()
        aNode = _selectNode()[0]
        for nodeNew in childrenTgt:
            _oldNodeTonewNode(aNode,nodeNew)
            print 'copado'
    else:
        print 'SELECCIONA UN NODO DE ALEMBIC'

def _oldNodeTonewNode(aNode,nodeNew):
    nodeNew=''
    #Si el nodo tiene un outPolyMesh se conectara
    if 'outPolyMesh' in cmds.listAttr(aNode,readOnly=True):
        outAttr='outPolyMesh'
        inAttr='inMesh'
        polyMeshNumbre = []
        polyMeshNumbre = cmds.getAttr(aNode+'.'+outAttr, size=True)
        #recorro el tamaño de conexiones en el polyMesh
        for i in range(polyMeshNumbre):
            #agarro el shape del nodo
            nodeOLD = cmds.listConnections(aNode+'.'+outAttr+str([i]), shapes=1)
            #si esta dentro de un grupo vamos por aca
            if '|' in nodeOLD:
                nodeOLD=nodeOLD[0].split('|')[-1:]
            #guardo la conexion completa vieja donde se conecta el nodo
            nodeOLDplug = cmds.listConnections(aNode+'.'+outAttr+str([i]),plugs=1)[0]
            if nodeOLD == nodeNew:
                #Desconecto y lo guardo
                if cmds.isConnected( aNode+'.'+outAttr+str([i]),nodeOLDplug):
                    desConects = cmds.disconnectAttr(aNode+'.'+outAttr+str([i]),nodeOLD+'.'+inAttr,nextAvailable=True)
                    #Spliteo el resultado de la desconeccion
                    desConects = str(str(desConects).split('Disconnect')[1]).split('from')
                    #Guardo esos nombres para usarlos
                    desConect,conectOld=str(conects[0]).replace(" ", "")+str([i]), str(conects[1]).replace(" ", "")
                    print 'Desconecte ' + str(desConect) +' de ' + str(conectOld)
                    #Conecto el nodo a la otra geometria en inMehs
                    conect = cmds.connectAttr(aNode+'.'+outAttr[i],nodeNEW+'.'+inAttr)
                    print 'Conectado'
                else:
                    print 'No existe conexion de ' + aNode+'.'+outAttr+str([i]) + 'con' + str(nodeOLDplug)
    else:
        print 'El script por ahora solo contempla si el nodo tiene polyMesh'

def _selectNode():

    selectNode = cmds.textScrollList(listNodesAlemb, q=True, selectItem=True)
    #selectNode = cmds.listRelatives(selectNode[0],children=True, fullPath=True)
    #cmds.select(selectNode)
    return selectNode

def _initGui():
    #lista de camaras en scena
    listNodesAlemb= cmds.ls(type='AlembicNode')
    excludeListB=['nada para escluir']
    #filtro trf de camaras
    for x in excludeListB:
        for item in listNodesAlemb:
            if item.find(x) != -1:
                listNodesAlemb.remove(item)
    #ordeno listas
    listNodesAlemb.sort()

    for lna in listNodesAlemb:
    	cmds.textScrollList(listNodesAlemb, edit=True, append=lna)

    if len(cmds.textScrollList(listNodesAlemb, q=True, allItems=True)):
    	cmds.textScrollList(listNodesAlemb, edit=True, selectIndexedItem=1)

def _refreshGui():
    # remove all existing items from the textScrollList, then repopulate it with initGui()
    cmds.textScrollList(listNodesAlemb, edit=True, removeAll=True)
    _initGui();

def _makeWindow(winName='PH_ALEMBICtoINMESH'):

    if cmds.window(winName, exists=True):
        cmds.deleteUI(winName)
    
    cmds.window( winName, h=250 ,w=200 )
    cmds.columnLayout(adjustableColumn = True)
    cmds.text('NODOS ALEMBIC EN FILE')
    cmds.rowLayout( numberOfColumns=3 )
    cmds.textScrollList(listNodesAlemb, allowMultiSelection=False, selectCommand="_selectNode()",h=400,w=200)
    cmds.columnLayout(adjustableColumn = True)
    cmds.button( label='TRANFER ALEMBIC', command="_startTranfer()", bgc=(0.2,0.8,0.0))
    cmds.showWindow()
    
    #fill gui with cameras
    _initGui()

_makeWindow()