import sys
import maya.cmds
import pymel.core as pm
import maya.mel as mel
listNodesAlemb=['']
def _startTranfer():
    aNode = _selectNode()
    newGeo= cmds.ls( sl=True )[0]
    if not aNode or newGeo:
        cmds.warning('Nada seleccionado')
    _oldNodeTonewNode(aNode,newGeo)

def _oldNodeTonewNode(aNode,newGeo):
    #Si el nodo tiene un outPolyMesh se conectara
    if 'outPolyMesh' in cmds.listAttr(aNode,readOnly=True):
        #diccionarios
        nodoDict = {}
        trfDicTrg = {}
        nodoDictConect = {}
        #input and output
        outAttr='outPolyMesh'
        inAttr='inMesh'
        #arrays
        childrenMsh=[]
        childrenT=[]
        polyMeshNumbre = []
        #cantidad de polymesh en nodo alembic
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
                #Lista de nodos a lo que voy a conectar el alembic IMPORTANTE
                padreTgt= newGeo
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
                            print str(desConects)
                            #Conecto el nodo a la otra geometria en inMehs
                            conect = cmds.connectAttr(aNode+'.'+outAttr+str([i]),k+v+'.'+inAttr)
                            #fix changename
                            try:
                                conect = cmds.connectAttr(aNode+'.'+outAttr+str([i]),k+v+'Deformed'+'.'+inAttr)
                                print 'Intenten con estos que tienen el nombre deformed' + str(conect) 
                            except:
                                None
                            print str(conect)    
                        else:
                            print 'No existe conexion de ' + aNode+'.'+outAttr+str([i]) + ' con ' + str(nodoDictConect[i])
    else:
        print 'El script por ahora solo contempla si el nodo tiene polyMesh'

def _initGui():
        #lista de camaras en scena
        NodesAlemb = cmds.ls(type='AlembicNode')
        
        if NodesAlemb==[]:
            cmds.warning('NO EXISTE NINGUN NODO DE ALEMBIC EN ESTE FILE')
        else:
            #ordeno listas
            NodesAlemb.sort()
    
            for i in NodesAlemb:
                cmds.textScrollList(listNodesAlemb, edit=True, append=i)
        
            if len(cmds.textScrollList(listNodesAlemb, q=True, allItems=True)):
                cmds.textScrollList(listNodesAlemb, edit=True, selectIndexedItem=1)

def _refreshGui():
    # remove all existing items from the textScrollList, then repopulate it with initGui()
    cmds.textScrollList(listNodesAlemb, edit=True, removeAll=True)
    _initGui();

def _makeWindow(winName='PH_ALEMBICINMESH'):
    #listNodesAlemb=[]
        
    if cmds.window(winName, exists=True):
        cmds.deleteUI(winName)
    
    cmds.window( winName, h=200 ,w=200,s=False,resizeToFitChildren=True )
    cmds.columnLayout(adjustableColumn = True)
    cmds.text('LISTA DE ALEMBIC EN ESCENA',align='center',h=20 )
    cmds.textScrollList(listNodesAlemb, allowMultiSelection=False, selectCommand="_selectNode()")
    cmds.rowLayout( numberOfColumns=2 )
    cmds.text('''
        1) SELECCIONA EL NODO DE ALEMBIC
        2) SELECCIONA EL GRUPO DEL SHADER
        3) TRANFERIR ALEMBIC
        ''',align='left')
    cmds.columnLayout(columnAttach=('left',50), rowSpacing=2)
    cmds.button( label='REFRESH', command="_refreshGui()", bgc=(0.1,0.5,0.1))
    cmds.button( label='TRANFER ALEMBIC', command="_startTranfer()", bgc=(0.1,0.5,0.1))
    cmds.showWindow()
    #inicio la lista
    _initGui()

_makeWindow()