import sys
import maya.cmds
import pymel.core as pm

newListSrc=[]
newListTgt=[]
aRenombrar=[]
srcWithoutNS=[]
childrenSrcWithOutNs=[]
childrenTgtWithOutNs=[]

if len(cmds.ls(sl=True)) == 2:
    geoSrc=cmds.ls( sl=True )[0]
    print geoSrc
    geoTgt=cmds.ls( sl=True )[1]
    print geoTgt
    if geoSrc:
        padreSrc = cmds.listRelatives(geoSrc, type='transform', parent=True, fullPath=True)
        childrenSrc = cmds.listRelatives(padreSrc)
        #cmds.select(childrenSrc)
        #selecciono el padre de la geometria y guardo sus hijos
        #meshListSrc = cmds.listRelatives( childrenSrc, allDescendents=True, noIntermediate=True,type="mesh")
        childrenSrc.sort()
    if geoTgt:
        padreTgt = cmds.listRelatives(geoTgt, type='transform', parent=True, fullPath=True)
        childrenTgt = cmds.listRelatives(padreTgt)
        #cmds.select(str(padreTgt[0])+'|'+str(childrenTgt[0]))
        #selecciono el padre de la geometria y guardo sus hijos
        #meshListTgt = cmds.listRelatives( childrenTgt, allDescendents=True, noIntermediate=True, type="mesh" )
        childrenTgt.sort()
    
    print 'El primer grupo tiene ' + str(len(childrenSrc)) + ' meshs'
    print 'El Segundo grupo tiene ' + str(len(childrenTgt)) + ' meshs'

    if ':' in geoSrc or geoTgt:
        print 'OJO QUE TENEMOS NAMESPACES EN ESTA'
        excludeList=['UI','shared']
        nsList = cmds.namespaceInfo(lon=True)
        [nsList.remove(ns) for ns in excludeList if nsList.count(ns)]
        print 'se borraron temporalmente los siguientes namespaces ' + str(nsList)
        for i in range(len(childrenSrc)):
            childrenSrcWithOutNs.append(childrenSrc[i].split(':')[-1])#.encode("utf-8"))
        for i in range(len(childrenTgt)):
            childrenTgtWithOutNs.append(childrenTgt[i].split(':')[-1])#.encode("utf-8"))
        #Recorremos y vemos si existen en el otro grupo las geometrias del source y las guardaos
        for i in range(len(childrenSrcWithOutNs)):
            # Si existe el nombre sin el namespace en el otro grupo de geometria hace algo
            if childrenSrcWithOutNs[i] in childrenTgtWithOutNs:
                #Lo guardo en una lista nueva para ordenar
                newListSrc.append(childrenSrc[i])#cmds.select(newListSrc)
            else:
                aRenombrar.append(childrenSrc[i])

        #Recorremos y vemos si existen en el otro grupo las geometrias del target y las guardamos
        for i in range(len(childrenTgtWithOutNs)):
            # Si existe el nombre sin el namespace en el otro grupo de geometria hace algo
            if childrenTgtWithOutNs[i] in childrenSrcWithOutNs:
                #Lo guardo en una lista nueva para ordenar
                newListTgt.append(childrenTgt[i])#cmds.select(newListSrc)
            else:
                aRenombrar.append(childrenTgt[i])
    else:

        for nameSrc in childrenSrc:
            if nameSrc in childrenTgt:
                newListSrc.append(str(padreSrc[0])+'|'+str(nameSrc))
                #cmds.select(newListSrc)
            else:
                aRenombrar.append(str(padreSrc[0])+'|'+str(nameSrc))

        for nameTgt in childrenTgt:
            if nameTgt in childrenSrc:
                newListTgt.append(str(padreTgt[1])+'|'+str(nameTgt))
                #cmds.select(newListTgt)
            else:
                aRenombrar.append(str(padreTgt[1])+'|'+str(nameTgt))
    
    if aRenombrar != 0:
        cmds.warning(('---Porfa fijate estos nombres por que no me machean.---').upper())
        print  '\n'
        for er in aRenombrar:
            print str(er)
        print  '\n'
        print ('---Igual intentare con el resto---').upper()
    
    if len(newListSrc) == len(newListTgt):
        if ':' in geoSrc or geoTgt:
            print 'TIENE NAMESPACE'
            for i in range(len(newListSrc)):
                    cmds.select(clear=True)
                    newListTft=cmds.listRelatives(newListTgt[i])[1]
                    cmds.setAttr(str(newListTft)+'.'+'intermediateObject', lock=0)
                    cmds.setAttr(str(newListTft)+'.'+'intermediateObject', 0)
                    tfrAtt=cmds.transferAttributes(str(newListSrc[i]),newListTgt[i],
                                    transferPositions=False,
                                    transferNormals=False,
                                    transferUVs=2,
                                    transferColors=2,
                                    sampleSpace=4,
                                    sourceUvSpace="map1",
                                    targetUvSpace="map1",
                                    searchMethod=3,
                                    flipUVs=False,
                                    colorBorders=True)
                    cmds.setAttr(str(newListTft)+'.'+'intermediateObject', 0)
                    #Rename nodo tranfer attribute
                    cmds.rename(tfrAtt,(str(newListTgt[i]).split('|')[-1]).upper()+'__TFATT')
        else:
            cmds.warning('NO TIENEN LA MISMA C/ DE MESHES TRATARE DE HACERLO CON EL RESTO, PERO MIRALO')
    else:
        for i in range(len(newListSrc)):
            cmds.select(clear=True)
            newListTft=cmds.listRelatives(newListTgt[i])[1]
            cmds.setAttr(str(newListTft)+'.'+'intermediateObject', lock=0)
            cmds.setAttr(str(newListTft)+'.'+'intermediateObject', 0)
            tfrAtt=cmds.transferAttributes(str(newListSrc[i]),newListTgt[i],
                            transferPositions=False,
                            transferNormals=False,
                            transferUVs=2,
                            transferColors=2,
                            sampleSpace=4,
                            sourceUvSpace="map1",
                            targetUvSpace="map1",
                            searchMethod=3,
                            flipUVs=False,
                            colorBorders=True)
            cmds.setAttr(str(newListTft)+'.'+'intermediateObject', 0)
            #Rename nodo tranfer attribute
            cmds.rename(tfrAtt,(str(newListTgt[i]).split('|')[-1]).upper()+'__TFATT')

    mel.eval('print ("RESULT: PARECE QUE FUNCO CHE, MIRALO POR LAS DUDAS.")')
else:
    print ''
    print '########################### MAN_LEETEESTOPORFA ################################'
    print '1) Seleccionar cualquier parte del mesh ORIGINAL'
    print '2) Seleccionar cualquier parte del mesh a TRANSFERIR'
    print '3) Resa que machen todos los nombres o tambien tenes el boton para hacerlo 1X1'
    print '###############################################################################'
    print ''