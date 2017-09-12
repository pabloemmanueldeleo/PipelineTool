import maya.cmds as cmds
import maya.mel as mel

def pintar():
    mel.eval ('setNClothMapType("inputAttract","",1); artAttrNClothToolScript 4 inputAttract;')
    mel.eval ('NClothPaintCallback "";')
    mel.eval('toolPropertyWindow;')

def mainBlendSimuSkin():

    objSeleccionadoShape=cmds.listRelatives(objSeleccionado[0],shapes=True)[0]
    namewin='PH_PAINTSIM v0.2'
    if cmds.window(namewin,exists=True):
        cmds.deleteUI(namewin)

    namewin=cmds.window(namewin,title=namewin,widthHeight=(200,100),resizeToFitChildren=1)
    cmds.rowLayout(numberOfColumns=6)
    cmds.separator ( height=10, style='double' )
    cmds.text( label= "  "+objSeleccionadoShape+"  " )
    sliderNCSI_01 = cmds.floatSliderGrp( 'nClothSkin', cw2=[50,100],height=50,field=True, minValue=0, maxValue=1.0, fieldMinValue=0, fieldMaxValue=1, value=0 ,step=0.001)
    cmds.button(label='PINTAR',c='pintar()')
    conecciones=[]
    ncShape=[]
    conecciones=cmds.listConnections (objSeleccionadoShape,connections=True)
    for con in conecciones:
        print 'entro en con'
        if cmds.nodeType (con) == 'transform':
            shapeDeCon=cmds.listRelatives(con,shapes=True)[0]
            if cmds.nodeType (shapeDeCon) == 'nCloth':
                print 'entro en nodetype'
                ncShape = cmds.listRelatives(con,shapes=True)[0]
    cmds.connectControl( 'nClothSkin', str(ncShape)+'.inputMeshAttract', index=2 )
    cmds.connectControl( 'nClothSkin', str(ncShape)+'.inputMeshAttract', index=1 )
    cmds.showWindow(namewin)

#----------------------------------------------

objSeleccionado = cmds.ls(sl=True)
print 'Selecciona una mesh con nCloth para empezar'
if len(objSeleccionado)==1:
    mainBlendSimuSkin()
else:
    cmds.warning ("DEBES SELECCIONAR UN OBJETO")
objSeleccionado=''
