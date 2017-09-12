import maya.cmds as mc
import os
import re
import shutil

#Global Variable---------------
global cantDeZeros#Size cant ej: V000, V00
global infoD#info global
global infoM#info global
#set variable inicial--------------
cantDeZeros = 3
infoD='DIRECTORIO LOCAL'
infoM='DIRECTORIO COPIA'


#funcion para salvar en D
def saveD():
    global cantDeZeros
    cantDeZeros = 3
    #oldnum = oldnum[0]
    oldnum=[]
    #get the current scene name
    mafilename = mc.file(query=True,sceneName=True)
    #iterative save file name generator
    sPN = os.path.split(mafilename)
    oldnum = re.findall(r'V[0-9]+', sPN[1])
    if oldnum==[]:
        pad = len(oldnum)
        num = str(int(pad)+1).zfill(cantDeZeros)
        newFileName = sPN[1].replace(sPN[1],sPN[1].split('.')[0].upper()+'_V' + str(num)+'.ma')
    else:
        oldnum=int(max(oldnum).split('V')[1])
        num = str(int(oldnum)+1).zfill(cantDeZeros)
        newFileName = sPN[1].replace(str(int(oldnum)).zfill(cantDeZeros),str(num))
    save(newFileName)
#funcion para salvar en M
def saveM():
    global cantDeZeros
    #oldnum = oldnum[0]
    oldnum=[]
    #get the current scene name
    mafilename = mc.file(query=True,sceneName=True)
    #iterative save file name generator
    sPN = os.path.split(mafilename)
    oldnum = re.findall(r'V[0-9]+', sPN[1])
    #save the this scene with the new filename
    if 'D:' in newfilename:
        newDirFile=maNewFileName.replace('D:', 'M:')
        mc.sysFile( os.path.split(newDirFile)[0], makeDir=True )
        #Copia el archivo local D a unidad M
        mc.sysFile( maNewFileName, copy= newDirFile )
        mc.warning('EN TU COMPU TAMBIEN UNIDAD D: ;) ' + newDirFile)
        save(newFileName)
    else:
        mc.warning('No se pudo guardar en tu disco D por alguna razon')
    
#funcion para salvar
def save(newFileName):
    maNewFileName = sPN[0] + '/' + newFileName
    #create the new filename
    newfilename = maNewFileName
    result = mc.file(rename=newfilename,f=True, save=True)
    mc.warning('QUE BUENO CHE TENES BACKUP ;) ' + newFileName)
    mc.headsUpMessage('QUE BUENO CHE TENES BACKUP ;) ' + newFileName, verticalOffset=120)

#funcion UISAVE
def saveUI():
    global infoD
    global infoM
    winSaveUI='SAVE-ME'
    version=' v1.0'
    h=50
    w=200
    if mc.window(winSaveUI, exists=True):
        mc.deleteUI(winSaveUI)
    winSaveUI=mc.window(winSaveUI,title=winSaveUI+version,w=w,h=h, toolbox=1)
    cl0=mc.columnLayout(parent=winSaveUI,rowSpacing=1,adjustableColumn = True,columnOffset=['both',5])
    tx0=mc.text(parent=cl0,label='\n¿Donde vas a guardarlo?\n')
    rcl0=mc.rowColumnLayout( parent=cl0,numberOfColumns=2, columnAttach=(1, 'both', 0), columnWidth=[(1, 200), (2, 100)],rowSpacing=[2,5], columnSpacing=[2,5])
    tx1=mc.text(parent=rcl0,label=infoD,align='left')
    bt0=mc.button(parent=rcl0,label='D:',bgc=(0.3,0.7,1),command='saveD()')
    tx1=mc.text(parent=rcl0,label=infoM,align='left')
    bt1=mc.button(parent=rcl0,label='D->M:',bgc=(0.7,0.2,0.1),command='saveM()')
    mc.showWindow(winSaveUI)
saveUI()