import sys
import maya.cmds

listExcept=['FaceGEO1BaseShape',
            'LOwerFlapSkinGEOShape',
            'LOwerFlapSkinGEOShapeOrig',
            'LOwerFlapBorderSkinGEO1Shape',
            'LOwerFlapBorderSkinGEO1ShapeOrig']
meshListSrc=[]
meshListTgt=[]
newListSrc=[]
newListTgt=[]
noMatch=[]
if len(cmds.ls(sl=True)) == 2:
    geoSrc=cmds.ls( sl=True )[0]
    print geoSrc
    geoTgt=cmds.ls( sl=True )[1]
    print geoTgt
    if geoSrc:
        childrenSrc = cmds.listRelatives(geoSrc, type='transform', parent=True, fullPath=True)
        #selecciono el padre de la geometria y guardo sus hijos
        meshListSrc = cmds.listRelatives( childrenSrc, noIntermediate=True)
        meshListSrc.sort()
    if geoTgt:
        childrenTgt = cmds.listRelatives(geoTgt, type='transform', parent=True, fullPath=True)
        #selecciono el padre de la geometria y guardo sus hijos
        meshListTgt = cmds.listRelatives( childrenTgt, noIntermediate=True)
        meshListTgt.sort()

    for nameSrc in meshListSrc:
        for nameTgt in meshListTgt:
            if nameSrc == nameTgt:
                newListSrc.append(nameSrc)
                newListTgt.append(nameTgt)
            else:
                noMatch.append(nameSrc)
                noMatch.append(nameTgt)
    print 'Algo no se machio, pero no importa'
    print 'Fijate este que estos dos no coisiden '
    print '->' + str(noMatch)

    print 'El primer grupo tiene ' + str(len(newListSrc)) + ' meshs'
    print 'El Segundo grupo tiene ' + str(len(newListTgt)) + ' meshs'
    cmds.select(newListSrc)
    if len(newListSrc) == len(newListTgt):
       cmds.warning('NO TIENEN LA MISMA C/ DE MESHES TRATARE DE HACERLO CON EL RESTO, PERO MIRALO')
    for meshSrc in newListSrc:
        for meshTgt in newListTgt:

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
