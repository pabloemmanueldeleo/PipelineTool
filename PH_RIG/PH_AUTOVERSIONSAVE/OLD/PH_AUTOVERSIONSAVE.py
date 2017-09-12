import maya.cmds as mc
import os
import re
import shutil

#Size cant ej: V000, V00
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

maNewFileName = sPN[0] + '/' + newFileName
#create the new filename
newfilename = maNewFileName
result = mc.file(rename=newfilename)
mc.file(f=True, save=True, defaultExtensions=True)
try:
    #save the this scene with the new filename
    if 'M:' in newfilename:
        newDirFile=maNewFileName.replace('M:', 'D:')
        mc.sysFile( os.path.split(newDirFile)[0], makeDir=True )
        #Copia el archivo local tambien en la unidad D
        mc.sysFile( maNewFileName, copy= newDirFile )
        mc.warning('EN TU COMPU TAMBIEN UNIDAD D: ;) ' + newDirFile)
except:
    mc.warning('No se pudo guardar en tu disco D por alguna razon')
mc.warning('QUE BUENO CHE TENES BACKUP ;) ' + newFileName)
mc.headsUpMessage('QUE BUENO CHE TENES BACKUP ;) ' + newFileName, verticalOffset=120)