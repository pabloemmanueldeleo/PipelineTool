import sys
import maya.cmds
import pymel.core as pm

listExcept=['FaceGEO1BaseShape',
            'LOwerFlapSkinGEOShape',
            'LOwerFlapSkinGEOShapeOrig',
            'LOwerFlapBorderSkinGEO1Shape',
            'LOwerFlapBorderSkinGEO1ShapeOrig']
meshListSrc=[]
meshListTgt=[]
newListSrc=[]
newListTgt=[]
aRenombrar=[]
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

    try:
        for nameSrc in childrenSrc:
            if nameSrc in childrenTgt:
                newListSrc.append(str(padreSrc[0])+'|'+str(nameSrc))
                #cmds.select(newListSrc)
            else:
                aRenombrar.append(str(padreTgt[0])+'|'+str(nameTgt))
        for nameTgt in childrenTgt:
            if nameTgt in childrenSrc:
                newListTgt.append(str(padreTgt[0])+'|'+str(nameTgt))
                #cmds.select(newListTgt)
            else:
                aRenombrar.append(str(padreTgt[0])+'|'+str(nameSrc))
    except:
        cmds.select(aRenombrar)
        print 'Algo no se machio, pero no importa'
    print 'Porfa fijate estos nombres por que no me machean' + str(aRenombrar)

    print 'El primer grupo tiene ' + str(len(childrenSrc)) + ' meshs'
    print 'El Segundo grupo tiene ' + str(len(childrenTgt)) + ' meshs'
    
    if len(newListSrc) != len(newListTgt):
       cmds.warning('NO TIENEN LA MISMA C/ DE MESHES TRATARE DE HACERLO CON EL RESTO, PERO MIRALO')
    else:
        for meshSrc in newListSrc:
            for meshTgt in newListTgt:
                cmds.select(clear=True)
                cmds.transferAttributes(meshSrc,meshTgt,
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
                
            
        mel.eval('print ("RESULT: PARECE QUE FUNCO CHE, CELEBREMOS.")')
else:
    print ''
    print '########################### MAN_LEETEESTOPORFA ################################'
    print '1) Seleccionar cualquier parte del mesh ORIGINAL'
    print '2) Seleccionar cualquier parte del mesh a TRANSFERIR'
    print '3) Resa que machen todos los nombres o tambien tenes el boton para hacerlo 1X1'
    print '###############################################################################'
    print ''