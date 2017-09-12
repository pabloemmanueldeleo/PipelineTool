import maya.cmds
import os
import re
import shutil

#Size cant ej: V000, V00
cantDeZeros = 3
#oldnum = oldnum[0]
oldnum=[]
#get the current scene name
mafilename = cmds.file(query=True,sceneName=True)
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
#save the this scene with the new filename
result = cmds.file(rename=newfilename)
cmds.file(f=True, save=True)
cmds.warning('QUE BUENO CHE TENES BACKUP ;) ' + newFileName)
cmds.headsUpMessage('QUE BUENO CHE TENES BACKUP ;) ' + newFileName, time=3.0,verticalOffset=150)