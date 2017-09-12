import maya.cmds
camListBox = ['']

def _selectChanged():
    #query selection in list
    #then do select command with selected item in list
    selectCam = cmds.textScrollList(camListBox, q=True, selectItem=True)
    cmds.select(selectCam)

def _delSelected():
    #query selection in list
    #then do select command with selected item in list
    #then delete it
    selectCam = cmds.textScrollList(camListBox, q=True, selectItem=True)
    for cam in selectCam:
        #Cambie para que borre la raiz de la camara
        selectCamRoot = cmds.listRelatives(selectCam[0],type='transform', parent=True, fullPath=True)
        if '|' in selectCamRoot[0]:
            selectCamRoot = selectCamRoot[0].split('|')[1]
            cmds.delete(selectCamRoot)
        else:
            cmds.delete(selectCam)
    refreshGui()

def _newCam():
    cmds.camera(name='C_RENOMBRAME_RENOMBRAME__CAM')
    refreshGui()

#Enfocar en esa camara
def _camLook():
    selectLook = cmds.textScrollList(camListBox, q=True, selectItem=True)
    cmds.lookThru(selectLook[0]) # looks through the camera I specify
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

def _initGui():
    #here we will add all cameras in scene to list box
    allCams = cmds.listCameras(perspective=False) #p=True is grabbing the perspective cameras only.
    excludeList=['persp','top','front','side']
    for ns in excludeList:
        if allCams.count(ns):
            allCams.remove(ns)
    allCams.sort()

    for aCam in allCams:
        cmds.textScrollList(camListBox, edit=True, append=aCam)

    if len(cmds.textScrollList(camListBox, q=True, allItems=True)):
    	cmds.textScrollList(camListBox, edit=True, selectIndexedItem=1)

def _refreshGui():
    # remove all existing items from the textScrollList, then repopulate it with initGui()
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
        cmds.playbackOptions(min=int(firstKey)-10,max=int(lastKey)+24)
        cmds.playbackOptions(animationStartTime=int(firstKey)-14,animationEndTime=int(lastKey)+14)
        cmds.currentTime(cTime)
        cmds.warning( 'RANGO ANIMADO DE ' + str(firstKey) + ' A ' + str(lastKey))
    else:
        cmds.warning(('Lo que seleccionaste no tiene animacion.').upper())
        cmds.currentTime(cTime)

def _makeWindow(winName='PH_MANAGERCAM'):

    if cmds.window(winName, exists=True):
        cmds.deleteUI(winName)
    
    cmds.window( winName, h=250 ,w=200 )
    #cmds.columnLayout( adjustableColumn=True )
    #cmds.checkBox( label='Show Ortho Cameras' )
    #lista camListBox
    cmds.paneLayout("test", configuration='horizontal3')
    cmds.textScrollList(camListBox, deleteKeyCommand="delSelected()", allowMultiSelection=False, selectCommand="selectChanged()",h=400,w=200)
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