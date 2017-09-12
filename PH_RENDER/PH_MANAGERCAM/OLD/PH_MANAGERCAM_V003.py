import maya.cmds
import maya.mel
camListBox = ['x']
camListTrf = ['']

def selectChanged():

    selectCam = cmds.textScrollList(camListBox, q=True, selectItem=True)
    selectCam = cmds.listRelatives(selectCam[0],children=True, fullPath=True)
    cmds.select(selectCam)

def selectTrf():
    cmds.textScrollList(camListBox, edit=True, removeAll=True)
    #query selection in list
    #then do select command with selected item in list
    selectCam = cmds.textScrollList(camListTrf, q=True, selectItem=True)
    cameras= cmds.listRelatives(selectCam[0],children=True)
    cameras.sort()
    for aCam in cameras:
        cmds.textScrollList(camListBox, edit=True, append=aCam)
    cmds.select(aCam)

def delSelected():

    selectCam = cmds.textScrollList(camListTrf, q=True, selectItem=True)
    cmds.delete(selectCam[0])
    cmds.warning('SE BORRO ' + str(selectCam[0]))
    refreshGui()

def newCam():
    cmds.camera(name='C_RENOMBRAME_RENOMBRAME__CAM')
    refreshGui()
#Enfocar en esa camara
def camLook():
    selectLook = cmds.textScrollList(camListBox, q=True, selectItem=True)
    cmds.select(selectLook[0])
    cmds.lookThru(selectLook[0]) # looks through the camera I specify
    lookThroughSelectedCamera()
    #cmds.camera(selectLook[0],displayFilmGate=True)
    padreSrc = cmds.listRelatives(selectLook[0],type='transform', parent=True, fullPath=True)
    #selecciono el control del rig
    cnts=[]
    if '|' in padreSrc[0]:
        childrenS = cmds.listRelatives(padreSrc[0].split('|')[1], path=True)
        if len(childrenS) > 0:
            for cnt in childrenS:
                if 'Control' in cnt:
                    cnts.append(cnt)
            _rangeTimeLine(cnt)
    else:
        None
    cmds.headsUpMessage('ESTAS VIENDO LA CAMARA ' + str(selectLook[0]) , verticalOffset=-120)

def lookThroughSelectedCamera():
    panel = "modelPanel4"  
    sel = cmds.ls(selection=True)

    #if camera is only selection look through it in chosen panel
    if( len(sel) == 1 ):
        if( len(cmds.listRelatives(children = True, type = "camera")) == 1 ):
            mel.eval("lookThroughModelPanel "+sel[0]+" "+panel)

def initGui():
    #lista de camaras en scena
    trfCams = cmds.ls('SCAM*_E*_P*', type='transform')
    excludeListB=['_Control','control','Control']
    #filtro trf de camaras
    for x in excludeListB:
        for item in trfCams:
            if item.find(x) != -1:
                trfCams.remove(item)
    #ordeno listas
    trfCams.sort()

    for cTrf in trfCams:
    	cmds.textScrollList(camListTrf, edit=True, append=cTrf)

    if len(cmds.textScrollList(camListTrf, q=True, allItems=True)):
    	cmds.textScrollList(camListTrf, edit=True, selectIndexedItem=1)

def refreshGui():
    # remove all existing items from the textScrollList, then repopulate it with initGui()
    cmds.textScrollList(camListTrf, edit=True, removeAll=True)
    cmds.textScrollList(camListBox, edit=True, removeAll=True)
    initGui();

#Busca el control y cheque el rango de la animacion inicio y final
def _rangeTimeLine(cnts):
    keys=cmds.keyframe(cnts, q=1)
    cTime=cmds.currentTime( query=True )
    if keys:
        keys.sort()
        firstKey = keys[1]
        lastKey = keys[-1]
        cmds.playbackOptions(min=int(firstKey),max=int(lastKey))
        cmds.playbackOptions(animationStartTime=int(firstKey),animationEndTime=int(lastKey))
        cmds.currentTime(cTime)
        cmds.warning( 'RANGO ANIMADO DE ' + str(firstKey) + ' A ' + str(lastKey))
    else:
        cmds.warning(('Lo que seleccionaste no tiene animacion.').upper())
        cmds.currentTime(cTime)

def makeWindow(winName='PH_MANAGERCAM'):

    if cmds.window(winName, exists=True):
        cmds.deleteUI(winName)
    
    cmds.window( winName, h=250 ,w=200 )
    #cmds.columnLayout( adjustableColumn=True )
    #cmds.checkBox( label='Show Ortho Cameras' )
    #lista camListBox
    cmds.paneLayout("test", configuration='horizontal3')
    #cmds.rowLayout( numberOfColumns=3)
    #cmds.text('loco')
    cmds.rowLayout( numberOfColumns=3, columnWidth3=(80, 75, 150), adjustableColumn=2, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)] )
    cmds.textScrollList(camListTrf, deleteKeyCommand="delSelected()", allowMultiSelection=False, selectCommand="selectTrf()",h=400,w=200)
    cmds.textScrollList(camListBox, allowMultiSelection=False, selectCommand="selectChanged()",h=400,w=200)
    cmds.columnLayout(adjustableColumn = True)
    cmds.button( label='VER', command="camLook()", bgc=(0.2,0.8,0.0))
    #cmds.button( label='TIMERANGE', command="_rangeTimeLine()", bgc=(0.2,0.8,0.0))
    #cmds.button( label='NUEVA CAMARA COMUN', command="newCam()" )
    #cmds.button( label='NUEVA CAMARA SCAM', command="newScam()" )
    cmds.button( label='ACTUALIZAR', command="refreshGui()", bgc=(0.5,0.2,0.0) )
    cmds.showWindow()
    
    #fill gui with cameras
    initGui()

makeWindow()