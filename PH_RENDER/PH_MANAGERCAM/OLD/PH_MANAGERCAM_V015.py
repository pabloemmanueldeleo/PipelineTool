import maya.cmds
import maya.mel as mel
import pymel.core.runtime as pm
global camListBox
camListBox = ['x']
global camListTrf
camListTrf = ['']
global dupliname
dupliname = ['d']

#Archivos mels
def sequence():
    mel.eval('source "D:/PH_SCRIPTS/PH_RENDER/PH_MANAGERCAM/PH_CAMERASEQUENCER.mel"')
def importrig():
    mel.eval('source "D:/PH_SCRIPTS/PH_RENDER/PH_MANAGERCAM/PH_IMPORTRIG.mel"')
    refreshGui()
def lockcams():
    mel.eval('source "D:/PH_SCRIPTS/PH_RENDER/PH_MANAGERCAM/PH_LOCKCAMERAS.mel"')
def selectChanged():
    selectCam = cmds.textScrollList(camListBox, q=True, selectItem=True)
    sel= cmds.ls(selectCam[0])
    if len(sel) >= 2:
        cmds.warning('HAY DOS OBJETOS CON EL MISMO NOMBRE OJO:' + str(sel)+'.\nPORFAVOR RENOMBRAR BIEN.')
        DupUI()
    else:
        selectCam = cmds.listRelatives(selectCam[0],children=True, fullPath=True)
        cmds.select(selectCam)

def selectTrf():
    global trfCams
    cmds.textScrollList(camListBox, edit=True, removeAll=True)
    #query selection in list
    #then do select command with selected item in list
    selectCam = cmds.textScrollList(camListTrf, q=True, selectItem=True)
    cameras = cmds.listRelatives(selectCam[0],type='transform',allDescendents=True)
    excludeListA=['_CAM','__CAM','GRP','TRFShape','_HCNS','__HCNS','TRFSH','_SCAMF','_CNTSH','_SCAMF','_SCAMSH','__SCAMH','__SCAMSH','CamLeft_','CamRight_']
    excludeListC=['parentConstraint','parentConstraint1','Frustum']
    if cameras!=[]:
    
        #filtro trf de camaras
        for x in excludeListA+excludeListC+trfCams:
            for item in cameras:
                if item.find(x) != -1:
                    cameras.remove(item)
    
    cameras.sort()
    for aCam in cameras:
        cmds.textScrollList(camListBox, edit=True, append=aCam)
    cmds.select(selectCam)

def delSelected():

    selectCam = cmds.textScrollList(camListTrf, q=True, selectItem=True)
    for sc in selectCam:
        if sc:
            cmds.delete(str(sc))
            cmds.warning('SE BORRO ' + str(sc))
        else:
            cmds.warning('LO SIENTO NO PUDE BORRAR ' + str(sc))
    refreshGui()

def newCam():
    cmds.camera(name='C_RENOMBRAME_RENOMBRAME__CAM')
    refreshGui()

def DupUI():
    global dupliname
    winName='PH_MANAGERCAM'
    winD='FIX->THAT'
    # UI DUP
    if cmds.window(winD, exists=True):
        cmds.deleteUI(winD)
    winD=cmds.window(winD+'w',title=winD)
    cmds.columnLayout( adjustableColumn=True )
    cmds.text(label='¿DESEA RENOMBRAR AUTOMATICAMENTE LOS NOMBRES?')
    cmds.textScrollList(dupliname,selectCommand="dupsel()")
    cmds.button('yes',label='RENOMBRAR DUPLICADOS',command='renameDuplicates()')
    cmds.button('no',label='DEJARLO MAL',command='cmds.deleteUI(winD)')
    cmds.showWindow(winD)
    checkdup()
def checkdup():
    global dupliname
    badXforms = [f for f in cmds.ls(type='camera') if '|' in f]
    badXforms.sort()
    for dup in badXforms:
        cmds.textScrollList(dupliname, edit=True, append=dup)
def dupsel():
    selDup = cmds.textScrollList(dupliname, q=True, selectItem=True)
    cmds.select(selDup)
def renameDuplicates(padding=3):
    badXforms = [f for f in cmds.ls(type='camera') if '|' in f]
    badXformsUnlock = [f for f in badXforms if cmds.lockNode(f,q=1,lock=1)[0] == False]
    count = 0
    countDict = {}
    for f in badXformsUnlock:
        countDict[f] = f.count('|')
    for key,value in sorted(countDict.iteritems(),reverse=True, key=lambda (key,value): (value,key)):
        n = 1
        newObj = cmds.rename(key,key.split('|')[-1]+'_'+str(n).zfill(padding))
        while newObj.count('|') > 0:
            n += 1
            basename = newObj.split('|')[-1]
            newName = '_'.join(basename.split('_')[0:-1])+'_'+str(n).zfill(padding)
            newObj = cmds.rename(newObj,newName)
        print 'renamed %s to %s' % (key,newObj)
        count = count+1
    if count < 1:
        return 'No duplicate names found.'
    else:
        return 'Found and renamed '+str(count)+' objects with duplicate names. Check script editor for details.'
       
    
#Enfocar en esa camara
def camLook():
    global camListBox
    selectLook = cmds.textScrollList(camListBox, q=True, selectItem=True)
    sel= cmds.ls(selectLook[0])
    if len(sel) >= 2:
        cmds.warning('HAY DOS OBJETOS CON EL MISMO NOMBRE OJO:' + str(sel)+'.\nPORFAVOR RENOMBRAR BIEN.')
        DupUI()
    else:
        cmds.select(selectLook[0])
        cmds.lookThru(selectLook[0]) # looks through the camera I specify
        lookThroughSelectedCamera()
        padreSrc = cmds.listRelatives(selectLook[0],type='transform', parent=True, fullPath=True)
        #selecciono el control del rig
        cnts=[]
        if '|' in padreSrc[0]:
            childrenS = cmds.listRelatives(padreSrc[0].split('|')[1], path=True)
            if len(childrenS) > 0:
                for cnt in childrenS:
                    if 'Control' or 'CNT' in cnt:
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
def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        # Si esta lo agrego
        if value not in seen:
            output.append(value)
            seen.add(value)
def initGui():
    global trfCams
    #lista de camaras en scena
    trfCams = cmds.ls('C_E*_P*','SCAM_*',type='transform')
    #trfCams=remove_duplicates(trfCams)
    excludeListB=['_Control','control','Control','__CNT','__CNTSH','TRF','HCNS','_HCNS','CAMSH','CAMShape','_SCAM']
    if trfCams!=[]:
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
    else:
        cmds.warning(('No se reconoce ninguna camara con nombres aceptables.').upper())

def refreshGui():
    # remove all existing items from the textScrollList, then repopulate it with initGui()
    cmds.textScrollList(camListTrf, edit=True, removeAll=True)
    cmds.textScrollList(camListBox, edit=True, removeAll=True)
    cmds.textScrollList(dupliname, edit=True, removeAll=True)
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
def cameraS():
    pm.SequenceEditor('CameraSequencer')
def makeWindow():

    version=' v1.0'
    winName='PH_MANAGERCAM'
    winD='FIX->THAT'
    if cmds.window(winName, exists=True):
        cmds.deleteUI(winName)
    if cmds.window(winD, exists=True):
        cmds.deleteUI(winD)
        
    cmds.window( winName,title=winName+version,s=0)
    rl1=cmds.rowLayout( numberOfColumns=3,columnWidth3=(350, 10, 50),columnAlign3=["left", "center", "center"])
    cl1=cmds.columnLayout(parent=rl1,adjustableColumn = True,columnOffset=['left',10])
    tx1=cmds.text(parent=cl1,label='GRUPOS\n')
    tslTRF=cmds.textScrollList(camListTrf,parent=cl1, deleteKeyCommand="delSelected()", allowMultiSelection=True, selectCommand="selectTrf()",h=350)
    tx4=cmds.text(parent=rl1,label='>\n\n>\n\n>\n')
    cl2=cmds.columnLayout(parent=rl1,adjustableColumn = True,columnOffset=['both',15])
    tx3=cmds.text(parent=cl2,label='CAMARAS\n')
    tslBOX=cmds.textScrollList(camListBox, parent=cl2, allowMultiSelection=False, selectCommand="selectChanged()",h=220)
    b1=cmds.button(parent=cl2, label='VER CAMARA', command="camLook()", bgc=(0.5,0.1,0.5),annotation='-Te lleva a la camara seleccionada y te pone los key en el timeline.\n-Si tiene animacion la seleccion hace un fill del timeline.')
    b0=cmds.button(parent=cl2, label='LOCK/UNLOCK CAMARAS', command="lockcams()", bgc=(0.2,0.8,0.0),annotation='Desbloquea y bloquea atributos de las camaras por seguridad.')
    cl3=cmds.columnLayout(parent=cl2,adjustableColumn = True,columnOffset=['both',15])
    rl2=cmds.rowLayout( parent=cl3,numberOfColumns=4)
    #b2=cmds.button(parent=rl2, label='TIMERANGE', command="_rangeTimeLine()", bgc=(0.2,0.8,0.0))
    b3=cmds.button(parent=rl2, label='CREAR SEQ', command="sequence()",bgc=(0.3,0.7,1),annotation='Crea Secuencia con las camaras de la escena.' )
    b3a=cmds.button(parent=rl2, label='SHOW', command='cameraS()',bgc=(0.3,0.7,1),annotation='Muestra la ventana de Camera Sequencer.' )
    b4=cmds.button(parent=rl2, label='IMPORTCAM', command="importrig()", bgc=(0.9,0.5,0.0) ,annotation='Seleciona la camara la cual remplazar para importar el rig nuevo.')
    b5=cmds.button(parent=rl2, label='ACTUALIZAR', command="refreshGui()", bgc=(0.5,0.2,0.0) ,annotation='Si hay algun cambio de camaras, es neceasrio actualizar.')
    tx4=cmds.text(parent=cl3,label='HELP: Mantene puntero del raton arriba de cada\n boton para ver mas info.')
    cmds.showWindow()
    #fill gui with cameras
    initGui()

makeWindow()