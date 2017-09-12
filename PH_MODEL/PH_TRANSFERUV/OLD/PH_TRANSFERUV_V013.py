import sys
import maya.cmds
import pymel.core as pm

newListSrc=[]
newListTgt=[]
aRenombrar=[]
srcWithoutNS=[]
childrenSrcWithOutNs=[]
childrenTgtWithOutNs=[]

def UvTranferTodo():
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
                        #Transfiero los uvs
                        uvTranfer(newListSrc[i],newListTgt[i])
            else:
                cmds.warning('NO TIENEN LA MISMA C/ DE MESHES TRATARE DE HACERLO CON EL RESTO, PERO MIRALO')
        else:
            print 'OJO QUE SI LEES ESTO TE LO DOBLO TODO'
            for i in range(len(newListSrc)):
                #Transfiero los uvs
                uvTranfer(newListSrc[i],newListTgt[i])
        mel.eval('print ("RESULT: PARECE QUE FUNCO CHE, MIRALO POR LAS DUDAS.")')
    else:
        print ''
        print '########################### MAN_LEETEESTOPORFA ################################'
        print '1) Seleccionar cualquier parte del mesh ORIGINAL'
        print '2) Seleccionar cualquier parte del mesh a TRANSFERIR'
        print '3) Resa que machen todos los nombres o tambien tenes el boton para hacerlo 1X1'
        print '###############################################################################'
        print ''

def uvTranfer(mesh_source,mesh_target):
    # Usually the original mesh before skinning has been renamed as *Orig
    # and hidden
    mesh_orig= str(cmds.listRelatives(mesh_target)[1])
    
    # Toggle OFF the Intermediate Object option box
    cmds.setAttr(mesh_orig+'.'+'intermediateObject', lock=0)
    cmds.setAttr(mesh_orig+'.'+'intermediateObject', 0)
    
    # Transfer UV using Transfer Attribute Command
    cmds.select(mesh_source, replace=True)
    cmds.select(mesh_orig, toggle=True)
    
    cmds.transferAttributes(
            transferPositions=False,
            transferNormals=False,
            transferUVs=2,
            transferColors=2,
            sampleSpace=4,
            sourceUvSpace="map1",
            targetUvSpace="map1",
            searchMethod=3,
            flipUVs=False,
            colorBorders=True
        )

    # Delete Construction History of mesh_orig after we transfer the UV information
    cmds.select(mesh_orig, replace=True)
    cmds.delete(constructionHistory=True)
    cmds.select(clear=True)

    # Toggle ON the Intermediate Object option box
    cmds.setAttr(mesh_orig+'.'+'intermediateObject', lock=0)
    cmds.setAttr(mesh_orig+'.'+'intermediateObject', 1)
    cmds.select(mesh_target, toggle=True)

def uvTranferSelect():

    selected_objects = cmds.ls(selection=True)
    mesh_source, mesh_target = selected_objects[0], selected_objects[1]
    uvTranfer(mesh_source,mesh_target)

def UIuvTranfer():
    w=200
    h=50
    
    nameWindow = 'uvTranfer'
    if cmds.window(nameWindow ,ex=True):
    	cmds.deleteUI(nameWindow)
    
    cmds.window(nameWindow, title='-EL PIBE- TE TRANFIERE UVS', sizeable=False, resizeToFitChildren=True, wh=(w,h))
    #form = cmds.formLayout(numberOfDivisions=100)
    cl1 = cmds.columnLayout(columnAlign='left',adjustableColumn = True)
    cmds.text(label='''
        1) Seleccionar cualquier parte del mesh ORIGINAL
        2) Seleccionar cualquier parte del mesh a TRANSFERIR
        3) Resa que machen todos los nombres o tambien tenes el boton para hacerlo 1X1''',align='left')
    cl2 = cmds.columnLayout(columnAlign='left',adjustableColumn = True)
    b1=cmds.button(nameWindow + 'btn1', label="SELECCION", w=50, h=50, command="uvTranferSelect()",bgc=[1,.6,.6])
    b2=cmds.button(nameWindow + 'btn2',label='TODO EL GRUPO', w=50, h=50, command='UvTranferTodo()',bgc=[.3,.3,.4])
    cmds.showWindow(nameWindow)

UIuvTranfer()