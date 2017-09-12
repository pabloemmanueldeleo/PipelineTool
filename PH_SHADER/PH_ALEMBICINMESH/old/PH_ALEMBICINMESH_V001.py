import maya.cmds
nodeOLD,nodeNEW = 'SleeperGEOShape','pilar:shader:SleeperGEOShape'
aNode='E247_Pilar_AlembicNode'
polyMeshNumbre = cmds.getAttr(aNode+'.'+outAttr, size=True)
outAttr='outPolyMesh'
inAttr='inMesh'

_oldNodeTonewNodePoly(aNode,polyMeshNumbre,nodeOLD,nodeNEW,outAttr,inAttr)
#Funcion para reconectar lo mismo a otro nodo igual

def _oldNodeTonewNodePoly(aNode,polyMeshNumbre,nodeOLD,nodeNEW,outAttr,inAttr):
    if 'outPolyMesh' in cmds.listAttr(aNode,readOnly=True):
        #Desconecto y lo guardo
        if cmds.isConnected( aNode+'.'+outAttr+str([polyMeshNumbre]),nodeOLD+'.'+inAttr):
            desConects = cmds.disconnectAttr(aNode+'.'+outAttr+str([polyMeshNumbre]),nodeOLD+'.'+inAttr,nextAvailable=True)
            #Spliteo el resultado de la desconeccion
            desConects = str(str(desConects).split('Disconnect')[1]).split('from')
            #Guardo esos nombres para usarlos
            desConect,conectOld=str(conects[0]).replace(" ", "")+str([polyMeshNumbre]), str(conects[1]).replace(" ", "")
            print 'Desconecte ' + str(desConect) +' de ' + str(conectOld)
            #Conecto el nodo a la otra geometria en inMehs
            conect = cmds.connectAttr(aNode+'.'+outAttr,nodeNEW+'.'+inAttr)
        else:
            print 'No tiene conexion con esa'
        return conect