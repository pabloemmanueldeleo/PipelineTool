import sys
import maya.cmds
import pymel.core as pm

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
    
    print 'El primer grupo tiene ' + str(len(childrenSrc)) + ' meshs'
    print 'El Segundo grupo tiene ' + str(len(childrenTgt)) + ' meshs'

    for nameSrc in childrenSrc:
        if nameSrc in childrenTgt:
            newListSrc.append(str(padreSrc[0])+'|'+str(nameSrc))
            #cmds.select(newListSrc)
        else:
            aRenombrar.append(str(padreSrc[0])+'|'+str(nameSrc))
    for nameTgt in childrenTgt:
        if nameTgt in childrenSrc:
            newListTgt.append(str(padreTgt[0])+'|'+str(nameTgt))
            #cmds.select(newListTgt)
        else:
            aRenombrar.append(str(padreTgt[0])+'|'+str(nameTgt))
    
    if aRenombrar != 0:
        cmds.warning(('Porfa fijate estos nombres por que no me machean.').upper())
        print ('Porfa fijate estos nombres por que no me machean.').upper()
        print  '\n'
        for er in aRenombrar:
            print str(er)