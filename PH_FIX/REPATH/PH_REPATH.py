import maya.cmds as cmds
import os

def renameTex():
    global newName
    tex=cmds.ls(sl=True,type='file')
    for item in tex:
        fullpath = cmds.getAttr(str(item)+'.fileTextureName')
        fileName= str(fullpath.split("/")[-1])
        newPath= os.path.join(fullpath,newName+'/'+fileName)
        result=cmds.setAttr(item+'.fileTextureName', newPath,type="string")
        print 'RE PATH DEL NODO:' + str(item) +' A:\n'+ str(newPath)

def selectDir():
    global pathT
    folder=cmds.fileDialog2(cap=" -ELIJE LA RUTA NUEVA- ",fm=3)
    filePath=str(str(folder[0]).replace('\\','/'))
    cmds.textField(pathT, edit=True,text=filePath)
    global newName
    newName=str(filePath)

def repathUI():
    global pathT
    winPathUI='PH_RE-PATH'
    if cmds.window(winPathUI, exists=True):
        cmds.deleteUI(winPathUI)
    winPathUI=cmds.window('PH_RE-PATH',title="PH_RE-PATH v1.0 (ONLY NODE FILE)",resizeToFitChildren=True,toolbox=1,s=0)
    cl1=cmds.columnLayout(parent=winPathUI,adjustableColumn=True,columnOffset=['both',5],rowSpacing=5 )
    tx1=cmds.text("PRIMERO QUE TODO SELECCIONA LOS NODO FILE!!",parent=cl1,bgc=(1,8,0))
    fl1=cmds.rowLayout(numberOfColumns=4,parent=cl1)
    tx2=cmds.text("RUTA NUEVA->",h=25,parent=fl1)
    pathT=cmds.textField(w=250,h=25,parent=fl1)
    loadBtn=cmds.button(w=100,label="ELEJIR",c="PH_REPATH.selectDir()",parent=fl1)
    cmds.setParent( '..' )
    fixit=cmds.button(l="RE PATH NOW", c="PH_REPATH.renameTex()",w=70,h=80,bgc=(0.8,0.6,0),parent=cl1)
    cmds.setParent( '..' )
    cmds.showWindow(winPathUI)
