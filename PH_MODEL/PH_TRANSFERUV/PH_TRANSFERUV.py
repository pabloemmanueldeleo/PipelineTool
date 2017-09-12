import sys
import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel

newListSrc=[]
newListTgt=[]
aRenombrar=[]
srcWithoutNS=[]
childrenSrcWithOutNs=[]
childrenTgtWithOutNs=[]
previewChildrenSrc=[]
global nameWindowUV
global version
nameWindowUV='UVtranferUI'
version=' v1.5'

def UvTranferTodo(arg):
    history=checkBoxDeform()
    if len(cmds.ls(sl=True)) == 2:
        childrenSrc=[]
        childrenTgt=[]
        geoSrc=cmds.ls( sl=True )[0]
        geoTgt=cmds.ls( sl=True )[1]
        if geoSrc:
            padreSrc = cmds.listRelatives(geoSrc, type='transform', parent=True, fullPath=True)
            childrenS = cmds.listRelatives(padreSrc, path=True)
            for x in childrenS:
                if cmds.nodeType(cmds.listRelatives(x)[0]) == 'mesh':
                    childrenSrc.append(x)
            childrenSrc.sort()
        if geoTgt:
            padreTgt = cmds.listRelatives(geoTgt, type='transform', parent=True, fullPath=True)
            childrenT = cmds.listRelatives(padreTgt, path=True)
            for v in childrenT:
                if cmds.nodeType(cmds.listRelatives(v)[0]) == 'mesh':
                    childrenTgt.append(v)
            childrenTgt.sort()
        if ':' in geoSrc or geoTgt:
            #print 'OJO QUE AHY NAMESPACES EN ESTA'
            excludeList=['UI','shared']
            nsList = cmds.namespaceInfo(lon=True)
            [nsList.remove(ns) for ns in excludeList if nsList.count(ns)]
            for i in range(len(childrenSrc)):
                childrenSrcWithOutNs.append(childrenSrc[i].split(':')[-1])#.encode("utf-8"))
            for o in range(len(childrenTgt)):
                childrenTgtWithOutNs.append(childrenTgt[o].split(':')[-1])#.encode("utf-8"))
            #Recorremos y vemos si existen en el otro grupo las geometrias del source y las guardaos
            for u in range(len(childrenSrcWithOutNs)):
                try:
                    # Si existe el nombre sin el namespace en el otro grupo de geometria hace algo
                    if childrenSrcWithOutNs[u] in childrenTgtWithOutNs:
                        #Lo guardo en una lista nueva para ordenar
                        newListSrc.append(childrenSrc[u])#cmds.select(newListSrc)
                    else:
                        aRenombrar.append(childrenSrc[u])
                except:
                    None
            #Recorremos y vemos si existen en el otro grupo las geometrias del target y las guardamos
            for i in range(len(childrenTgtWithOutNs)):
                try:
                    # Si existe el nombre sin el namespace en el otro grupo de geometria hace algo
                    if childrenTgtWithOutNs[i] in childrenSrcWithOutNs:
                        #Lo guardo en una lista nueva para ordenar
                        newListTgt.append(childrenTgt[i])#cmds.select(newListSrc)
                    else:
                        aRenombrar.append(childrenTgt[i])
                except:
                    print ''
        else:
            for nameSrc in childrenSrc:
                if nameSrc in childrenTgt:
                    newListSrc.append(str(padreSrc[0])+'|'+str(nameSrc))
                else:
                    aRenombrar.append(str(padreSrc[0])+'|'+str(nameSrc))
            for nameTgt in childrenTgt:
                if nameTgt in childrenSrc:
                    newListTgt.append(str(padreTgt[1])+'|'+str(nameTgt))
                else:
                    aRenombrar.append(str(padreTgt[1])+'|'+str(nameTgt))
        if aRenombrar != []:
            print ('---Porfa fijate estos nombres por que no me machean.---').upper()
            for er in aRenombrar:
                print str(er)
            print ('---Igual intentare con el resto---').upper()

        if len(newListSrc) == len(newListTgt):
            if ':' in geoSrc or geoTgt:#print 'TIENE NAMESPACE'
                for i in range(len(newListSrc)):
                    try:
                        uvTranfer(newListSrc[i],newListTgt[i],history)
                    except Exception:
                        print '>>NO PUDE CON ' + str(newListTgt[i]) + ' PERDON<<.'
            else:
                cmds.warning('NO TIENEN LA MISMA C/ DE MESHES TRATARE DE HACERLO CON EL RESTO, PERO MIRALO')
        else:
            print 'OJO QUE SI LEES ESTO TE LO DOBLO TODO'
            for i in range(len(newListSrc)):
                #Transfiero los uvs
                try:
                    uvTranfer(newListSrc[i],newListTgt[i],history)
                except:
                    print '>>NO PUDE CON ' + str(newListTgt[i]) + ' PERDON<<.'
    else:
        print ''
        print '########################### MAN_LEETEESTOPORFA ################################'
        print '1) Seleccionar cualquier parte del mesh SHD'
        print '2) Seleccionar cualquier parte del mesh a RIG'
        print '3) Resa que machen todos los nombres o tambien tenes el boton para hacerlo 1X1'
        print '###############################################################################'
        print ''

def uvTranfer(mesh_source,mesh_target, history=True):

    # Usually the original mesh before skinning has been renamed as *Orig
    # and hidden
    mesh_orig= str(cmds.listRelatives(mesh_target)[-1])

    # Toggle OFF the Intermediate Object option box
    cmds.setAttr(mesh_orig+'.'+'intermediateObject', lock=0)
    cmds.setAttr(mesh_orig+'.'+'intermediateObject', 0)

    # Transfer UV using Transfer Attribute Command
    cmds.select(mesh_source, replace=True)
    cmds.select(mesh_orig, toggle=True)

    cmds.transferAttributes(mesh_source,mesh_orig,
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

    #Delete Construction History of mesh_orig after we transfer the UV informati
    cmds.select(mesh_orig, replace=True)
    if history==True:
        cmds.delete(constructionHistory=True)
    cmds.select(clear=True)

    # Toggle ON the Intermediate Object option box
    cmds.setAttr(mesh_orig+'.'+'intermediateObject', lock=0)
    cmds.setAttr(mesh_orig+'.'+'intermediateObject', 1)
    print 'UV TRANFERIDO '+ str(mesh_target) + ' DONE!!!'
    cmds.select(mesh_target, toggle=True)

def uvWindows(arg):
    #Creo ventana de uv para ver el proceso y apago ver imagenes
    cmds.TextureViewWindow()
    #tomo el nombre del panel
    texWinName = cmds.getPanel(sty='polyTexturePlacementPanel')
    #pregunto si esta prendido o a apagado ver imagen
    if cmds.textureWindow( texWinName[0], q=True , imageDisplay=True):
        #"Show/Hide"
        mel.eval('textureWindowToggleTextureImage( "polyTexturePlacementPanel1", "textureWindow");')
    else:
        None

def checkBoxDeform():
    global nameWindowUV
    checkBoxDeform=cmds.checkBox(nameWindowUV + 'btn4',q = True, v = True)
    return checkBoxDeform

def uvTranferSelect(arg):
    history=checkBoxDeform()
    selected_objects = cmds.ls(selection=True)
    mesh_source, mesh_target = selected_objects[0], selected_objects[1]
    uvTranfer(mesh_target,mesh_source,history)

def UIuvTranfer():
    w=210
    h=50
    global nameWindowUV
    global version
    if cmds.window(nameWindowUV ,ex=True):
        cmds.deleteUI(nameWindowUV)
    cmds.window(nameWindowUV, title=nameWindowUV+version, sizeable=False, resizeToFitChildren=True, wh=(w,h))
    cl1 = cmds.columnLayout(columnAlign='left',adjustableColumn = True)
    cmds.text(label='''
        1) Seleccionar cualquier parte del mesh SHD
        2) Seleccionar cualquier parte del mesh RIG
        3) Presiona TODO EL GRUPO* (funciona si contiene solo un grupo)
        ALTERNATIVA: Elejis 1 X 1 con el mismo nombre y preciona SELECCION.
        * Si tenes varios grupos hay que hacerlo en los demas tambien.
        ''',align='left')
    buttonForm=cmds.rowColumnLayout( numberOfRows=1)
    b1=cmds.button(nameWindowUV + 'btn1',label='TODO EL GRUPO', command=UvTranferTodo,bgc=[.3,.3,.4], enable=1)
    b2=cmds.button(nameWindowUV + 'btn2', label="SELECCION", command=uvTranferSelect,bgc=[1,.6,.6])
    c13= cmds.columnLayout(columnAttach=('both', 5))
    b3=cmds.button(nameWindowUV + 'btn3', label=" SHOW ", command=uvWindows,bgc=[1,.6,.3])
    cb=cmds.checkBox(nameWindowUV + 'btn4', label=' COLLAPSE',v=True)
    cmds.showWindow(nameWindowUV)
