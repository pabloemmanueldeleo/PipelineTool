# -*- encoding: utf-8 -*-
import sys
import maya.cmds as mc
import pymel.core as pm
import maya.mel as mel
from pymel.core.runtime import BakeNonDefHistory
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
        trfDicTrg = {}
        ConnectionsNodoAlembic = {}
        #input and output
        outAttr='outPolyMesh'
        inAttr='inMesh'
        outMesh='outMesh'
        #arrays
        childrenT=[]
        polyMeshNumber = []
        #cantidad de polymesh en nodo alembic
        polyMeshNumber = mc.getAttr(aNode+'.'+outAttr, size=True)
        #------------------#recorro el tamaño de conexiones en el polyMesh
        for i in range(polyMeshNumber):
            conectionCurrentMSH=mc.connectionInfo(aNode+'.'+outAttr+'['+str(i)+']', destinationFromSource=True)[0]
            conectionCurrentID=mc.connectionInfo(conectionCurrentMSH, sourceFromDestination=True)
            ConnectionsNodoAlembic[i]=conectionCurrentMSH

        padreTgt= newGeo
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

        for ID,GEO in ConnectionsNodoAlembic.items():#alembic list
            for RUTA,shapeSHD in trfDicTrg.items():#shader list
                if ':' in GEO and shapeSHD:
                    cuerrentConnectionNodeAbc = GEO.split(':')[0:][-1].split('.')[0]
                    cuerrentGeoSHD = shapeSHD.split(':')[0:][-1]
                    if cuerrentConnectionNodeAbc == cuerrentGeoSHD:
                        if not mc.isConnected(aNode+'.'+outAttr+'['+str(ID)+']',RUTA+shapeSHD+'.'+inAttr):
                            conect = mc.connectAttr(aNode+'.'+outAttr+'['+str(ID)+']',RUTA+shapeSHD+'.'+inAttr,force=True)
                            print str(conect)
                        else:
                            conect = mc.connectAttr(aNode+'.'+outAttr+'['+str(ID)+']',GEO,force=True)
                            print aNode+'.'+outAttr+'['+str(ID)+']',RUTA+shapeSHD+'.'+inAttr + '/n no tiene conexion o ya esta conectado a otra cosa.'

    else:
        print 'El script por ahora solo contempla si el nodo tiene polyMesh'

def _selectForceAlembic():
    if len(mc.ls(sl=1)) == 2:
        alembicGEO=mc.ls(sl=1,r=1)[0]
        shdGEO=mc.ls(sl=1,r=1)[1]
        BConnection=mc.connectionInfo(str(alembicGEO)+'.inMesh',sourceFromDestination=True)
        if BConnection!=0:
            conect=mc.connectAttr(str(BConnection),str(shdGEO)+'.inMesh',force=True)
        else:
            print 'No se encontro conexion con alembic'
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
    version=' v2.0'
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
        4) ULTIMA OPCION FORCE
        ''',align='left')
    mc.columnLayout(adjustableColumn=True, rowSpacing=5)
    mc.button( label='REFRESH', command="PH_ALEMBICINMESH._refreshGui()", bgc=(0.4,0.8,0.3))
    mc.button( label='TRANFER ALEMBIC', command="PH_ALEMBICINMESH._startTranfer()", bgc=(0.3,0.4,0.3))
    mc.rowLayout(numberOfColumns=2 )
    mc.button( label='FORCE SELECT', command="PH_ALEMBICINMESH._selectForceAlembic()", bgc=(1,0.4,0.3))
    mc.showWindow()
    #inicio la lista
    _initGui()
_makeWindow()
