import sys
import maya.cmds
meshListSrc.remove('LOwerFlapSkinGEOShape')

listExcept=['FaceGEO1BaseShape','LOwerFlapSkinGEOShape','LOwerFlapSkinGEOShapeOrig','LOwerFlapBorderSkinGEO1Shape','LOwerFlapBorderSkinGEO1ShapeOrig']
if len(cmds.ls(sl=True)) > 2:
    geoSrc=cmds.ls( sl=True )
    geoTgt=cmds.ls( sl=True )[1]
    if geoSrc:
        childrenSrc = cmds.listRelatives(geoSrc, type='transform', parent=True, fullPath=True)
        cmds.select(childrenSrc)
        #selecciono el padre de la geometria y guardo sus hijos
        meshListSrc = cmds.listRelatives( childrenSrc, allDescendents=True, noIntermediate=True, type="mesh" )
        try:
            for nameGeo in meshListSrc:
                for exp in listExcept:
                    if nameGeo == exp:
                        meshListSrc.remove(exp)
        except:
            None
    if geoTgt:
        childrenTgt = cmds.listRelatives(geoTgt, type='transform', parent=True, fullPath=True)
        cmds.select(childrenTgt)
        #selecciono el padre de la geometria y guardo sus hijos
        meshListTgt = cmds.listRelatives( childrenTgt, allDescendents=True, noIntermediate=True, type="mesh" )
        if 'FaceGEO1Base' in meshListSrc:
            meshListSrc.remove('FaceGEO1Base')
        if 'LOwerFlapSkinGEO' in meshListSrc:
            meshListSrc.remove('LOwerFlapSkinGEO')
        if 'LOwerFlapBorderSkinGEO1' in meshListSrc:
            meshListSrc.remove('LOwerFlapBorderSkinGEO1')
    cmds.select(cl=True)
    grpGeoTgt = cmds.select(meshListTgt)

    if len(meshListSrc) = len(meshListTgt):
        print 'Tiene la misma cantidad de meshes en el grupo !!!UNA BUENA!!!'
         for src in meshListSrc:
             for tgr in meshListSrc:
                 try:
                     if src == tgr:
                         print 'iguales'
                 except:
                     print 'che no machean'
                     None
    else:
       print 'Los grupos no tiene la misma cantidad de meshes'

else:
    print ''
    print '########################### MAN_LEETEESTOPORFA ################################'
    print '1) Seleccionar cualquier parte del mesh ORIGINAL'
    print '2) Seleccionar cualquier parte del mesh a TRANSFERIR'
    print '3) Resa que machen todos los nombres o tambien tenes el boton para hacerlo 1X1'
    print '###############################################################################'
    print ''

for chil in meshList:

    #selecciono el padre de la geometria seleccionada
    
