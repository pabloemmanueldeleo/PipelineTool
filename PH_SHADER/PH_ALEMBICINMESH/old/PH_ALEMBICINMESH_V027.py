# -*- encoding: utf-8 -*-
import sys
import maya.cmds as mc
import pymel.core as pm
import maya.mel as mel
listNodesAlemb=['']

def _startTranfer():
    aNode = str(_selectNode())
    newGeo= str(mc.ls( sl=True )[0])
    if not aNode or newGeo:
        mc.warning('No estas haciendo algo bien.')
    _oldNodeTonewNode(aNode,newGeo)

def _oldNodeTonewNode(aNode,newGeo):
    #Si el nodo tiene un outPolyMesh se conectara
    if 'outPolyMesh' in mc.listAttr(aNode,readOnly=True):
        #diccionarios
        nodoDict = {}
        trfDicTrg = {}
        nodoDictConect = {}
        #input and output
        outAttr='outPolyMesh'
        inAttr='inMesh'
        outMesh='outMesh'
        n=''
        s=''
        nsN=''
        nsS=''
        #arrays
        childrenMsh=[]
        childrenT=[]
        polyMeshNumber = []
        #bools
        nNS=False
        sNS=False
        #cantidad de polymesh en nodo alembic
        polyMeshNumber = mc.getAttr(aNode+'.'+outAttr, size=True)
        #------------------#recorro el tamaño de conexiones en el polyMesh
        for i in range(polyMeshNumber):
            #guardo la conexion completa vieja donde se conecta el nodo
            if mc.listConnections(aNode+'.'+outAttr+str([i]),plugs=1,connections=True)!= None:
                nodoDictConect[i] = mc.listConnections(aNode+'.'+outAttr+str([i]),plugs=1)[0]
            else:
                nodoDictConect[i]= 'None'
            #si esta dentro de un grupo vamos por aca
            if 'Deformed' in nodoDictConect[i]:
                #si no tiene grupo el string se le agrega
                if not '|' in nodoDictConect[i]:
                    grp=mc.listRelatives(nodoDictConect[i].split('.')[0],allParents=True,fullPath=True)[0]
                    nodoDictConect[i]=grp+'|'+nodoDictConect[i]
            '''else:
                grp=mc.listRelatives(nodoDictConect[i].split('.')[0],allParents=True,fullPath=True)[0]
                if not str(grp) in nodoDictConect[i]:
                    grp=mc.listRelatives(nodoDictConect[i].split('.')[0],allParents=True,fullPath=True)[0]
                    nodoDictConect[i]=grp+'|'+nodoDictConect[i]'''
            #-------------------#listamos el grupo a conectar
            if len(mc.ls( sl=True )) == 1:
                #Lista de nodos a lo que voy a conectar el alembic IMPORTANTE
                padreTgt= newGeo
                #childrenT = mc.listRelatives(padreTgt, path=True)
                childrenT = mc.listRelatives(padreTgt, fullPath=True,noIntermediate=True)
                for x in range(len(childrenT)):
                    #busco el shape
                    o=mc.listRelatives(childrenT[x],fullPath=True)
                    if mc.nodeType(str(o[0])) == 'mesh':
                        if '|' in o[0]:
                            o=o[0].split('|')[-1:]
                            trfDicTrg[childrenT[x]+'|'] = o[0]
                        else:
                            trfDicTrg[childrenT[x]] = o[0]
            #------------------------
            for f in childrenT:
                #Conectamos
                for k, v in trfDicTrg.items():
                    if ':' in nodoDictConect[i]:
                        n=nodoDictConect[i].split(':')[-1:][0]
                        nsN=nodoDictConect[i].split(':')[:-1][0]
                        nNS=True
                    if ':' in v:
                        s=v.split(':')[-1:][0]
                        nsS=v.split(':')[:-1][0]
                        sNS=True
                    #si tienen namespace esto
                    if nNS==True and sNS==True:
                        if s in nodoDictConect[i]:
                            nodoDesc=nodoDictConect[i]
                            outAtt=outAttr+str([i])
                            inAtt=inAttr
                            targetNode=k+v
                            _connectToAlembic(aNode,nodoDesc,targetNode,outAtt,inAtt)
                    elif nNS==True and sNS==False:
                        if v in n:
                            nodoDesc=nodoDictConect[i]
                            outAtt=outAttr+str([i])
                            inAtt=inAttr
                            targetNode=k+v
                            _connectToAlembic(aNode,nodoDesc,targetNode,outAtt,inAtt)
                    elif nNS==False and sNS==True:
                        if s in nodoDictConect[i]:
                            nodoDesc=nodoDictConect[i]
                            outAtt=outAttr+str([i])
                            inAtt=inAttr
                            targetNode=k+v
                            _connectToAlembic(aNode,nodoDesc,targetNode,outAtt,inAtt)
                    else:
                        if str(v) in nodoDictConect[i]:
                            nodoDesc=nodoDictConect[i]
                            outAtt=outAttr+str([i])
                            inAtt=inAttr
                            targetNode=k+v
                            _connectToAlembic(aNode,nodoDesc,targetNode,outAtt,inAtt)
    else:
        print 'El script por ahora solo contempla si el nodo tiene polyMesh'
    
def _connectToAlembic(aNode,nodoDesc,targetNode,outAtt,inAtt):
    if mc.isConnected(aNode+'.'+outAtt,nodoDesc):
        desConects = mc.disconnectAttr(aNode+'.'+outAtt,nodoDesc)
        print str(desConects)
        conect = mc.connectAttr(aNode+'.'+outAtt,targetNode+'.'+inAtt,force=True)
        print str(conect)
    else:
        print str(aNode+'.'+outAtt) + ' no tiene conexion.'
        
def _selectToAlembic():
    selA, selB=mc.ls(sl=1)
    if sel == 2:
        BakeNonDefHistory()
        mc.connectAttr(str(selB)+'.outMesh',str(selA)+'.inMesh',force=True)
        BakeNonDefHistory()
    else:
        print 'Selecciona primero el mesh shader y luego el mesh alembic.'
        
def _initGui():
        #lista de camaras en scena
        NodesAlemb = mc.ls(type='AlembicNode')
        if NodesAlemb==[]:
            mc.warning('NO EXISTE NINGUN NODO DE ALEMBIC EN ESTE FILE')
        else:
            #ordeno listas
            NodesAlemb.sort()
            for i in NodesAlemb:
                mc.textScrollList(listNodesAlemb, edit=True, append=i)
            if len(mc.textScrollList(listNodesAlemb, q=True, allItems=True)):
                mc.textScrollList(listNodesAlemb, edit=True, selectIndexedItem=1)
def _selectNode():

    selectNode = mc.textScrollList(listNodesAlemb, q=True, selectItem=True)
    return selectNode[0]
    
def _refreshGui():
    # remove all existing items from the textScrollList, then repopulate it with initGui()
    mc.textScrollList(listNodesAlemb, edit=True, removeAll=True)
    _initGui();

def _makeWindow():

    winName='PH_ALEMBICINMESH'
    version=' v1.0'
    if mc.window(winName, exists=True):
        mc.deleteUI(winName)
    mc.window( winName, title=winName+version, h=200 ,w=200,s=False,resizeToFitChildren=True )
    mc.columnLayout(adjustableColumn = True)
    mc.text('LISTA DE ALEMBIC EN ESCENA',align='center',h=20 )
    mc.textScrollList(listNodesAlemb, allowMultiSelection=False, selectCommand="PH_ALEMBICINMESH._selectNode()")
    mc.rowLayout( numberOfColumns=2 )
    mc.text('''
        1) SELECCIONA EL NODO DE ALEMBIC
        2) SELECCIONA EL GRUPO DEL SHADER
        3) TRANFERIR ALEMBIC
        ''',align='left')
    mc.columnLayout(columnAttach=('left',50), rowSpacing=2)
    mc.button( label='REFRESH', command="PH_ALEMBICINMESH._refreshGui()", bgc=(0.1,0.5,0.1))
    mc.button( label='TRANFER ALEMBIC', command="PH_ALEMBICINMESH._startTranfer()", bgc=(0.1,0.5,0.1))
    mc.showWindow()
    #inicio la lista
    _initGui()