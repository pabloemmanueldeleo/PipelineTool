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
if len(cmds.ls(sl=True)) == 2:
    geoSrc=cmds.ls( sl=True )[0]
    print geoSrc
    geoTgt=cmds.ls( sl=True )[1]
    print geoTgt
    if geoSrc:
        childrenSrc = cmds.listRelatives(geoSrc, type='transform', parent=True, fullPath=True)
        cmds.select(childrenSrc)
        #selecciono el padre de la geometria y guardo sus hijos
        meshListSrc = cmds.listRelatives( childrenSrc, allDescendents=True, noIntermediate=True, type="mesh" )
        meshListSrc.sort()
    if geoTgt:
        childrenTgt = cmds.listRelatives(geoTgt, type='transform', parent=True, fullPath=True)
        cmds.select(childrenTgt)
        #selecciono el padre de la geometria y guardo sus hijos
        meshListTgt = cmds.listRelatives( childrenTgt, allDescendents=True, noIntermediate=True, type="mesh" )
        meshListTgt.sort()

    try:
        for nameSrc in meshListSrc:
            for nameTgt in meshListTgt:
                if nameSrc == nameTgt:
                    newListSrc.append(nameSrc)
                    newListTgt.append(nameTgt)

    except:
        print 'Algo no se machio, pero no importa'

    print 'El primer grupo tiene ' + str(len(newListSrc)) + ' meshs'
    print 'El Segundo grupo tiene ' + str(len(newListTgt)) + ' meshs'

    if len(newListSrc) == len(newListTgt):
       cmds.warning('NO TIENEN LA MISMA C/ DE MESHES TRATARE DE HACERLO CON EL RESTO, PERO MIRALO')

else:
    print ''
    print '########################### MAN_LEETEESTOPORFA ################################'
    print '1) Seleccionar cualquier parte del mesh ORIGINAL'
    print '2) Seleccionar cualquier parte del mesh a TRANSFERIR'
    print '3) Resa que machen todos los nombres o tambien tenes el boton para hacerlo 1X1'
    print '###############################################################################'
    print ''
