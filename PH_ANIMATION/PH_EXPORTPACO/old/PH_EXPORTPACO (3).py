import maya.cmds as cmds
import os
import sys
path='M:\PH_SCRIPTS\SCRIPTS\PACO'
if not path in sys.path:
    sys.path.append(path)
import PS.MM.cache
#reload(PS.MM.cache)
sys.path.remove(path)

#export
def alembic():
    global tabs
    global tabState
    tabState=cmds.tabLayout(tabs,q=1,selectTabIndex=1)#en que tab estoy?
    if tabState==1:#tab de export
        global eloadNameSpace
        global epathShader
        global epathAlembic
        #tico:Asset
        #D:/PH_SCRIPTS/SCENES_RIG/PACOTEST/CHAR/TICO/03_TICO_SHD.ma
        #D:/PH_SCRIPTS/SCENES_RIG/PACOTEST/ALEMBIC
        rigNamespace = cmds.textField(eloadNameSpace, edit=False, text=True, q=1)
        assetSHDPath = cmds.textField(epathShader, edit=False, text=True, q=1)
        cachePath    = cmds.textField(epathAlembic, edit=False, text=True, q=1)
        PS.MM.cache.exportAssetCache( rigNamespace, assetSHDPath, cachePath )
    elif tabState==2:#tab de import
        global iloadNameSpace
        global ipathShader
        global ipathAlembic
        assetNamespace = cmds.textField(iloadNameSpace, edit=False, text=True, q=1)
        assetSHDPath = cmds.textField(ipathShader, edit=False, text=True, q=1)
        cachePath    = cmds.textField(ipathAlembic, edit=False, text=True, q=1)
        PS.MM.cache.referenceAssetWithCache( assetNamespace, assetSHDPath, cachePath )
    elif tabState==3:#tab de update
        global uloadNameSpace
        global upathAlembic
        assetNamespace = cmds.textField(uloadNameSpace, edit=False, text=True, q=1)
        cachePath    = cmds.textField(upathAlembic, edit=False, text=True, q=1)
        PS.MM.cache.updateAssetCache( assetNamespace, cachePath )

#automatica export
def automaticExport():
    PS.MM.cache.exportSelectedAssets()

#Cambia elijiendo un transform entre el cache y el rig, apagando la refe.
def changebetweencache():
    PS.MM.cache.switchSelectedRigCache()

#select dirs
def selectDir(F=True):
    global tabs
    global tabState
    tabState=cmds.tabLayout(tabs,q=1,selectTabIndex=2)#en que tab estoy?
    if tabState==1:#tab de export
        global epathShader
        global epathAlembic
        if F:
            emultifilter="Maya Files (*.ma *.mb)"
            efolder=cmds.fileDialog2(cap=" - ELIJE ARCHIVO SHADER - ",startingDirectory='M:/MAYA/01_CHAR',fm=4,ff=emultifilter)#selecciona Archivo
            if efolder:
                efilePath=str(str(efolder[0]).replace('\\','/'))
                cmds.textField(epathShader, edit=True,text=efilePath)
            else:
                print 'No se busco nada.'
        else:
            emultifilter="*.abc"
            efolder=cmds.fileDialog2(cap=" - NOMBRAR Y GUARDAR EL ALEMBIC- ",startingDirectory='M:/',fm=5,ff=emultifilter)#seleccionar Carpeta
            if efolder:
                efilePath=str(str(efolder[0]).replace('\\','/'))
                cmds.textField(epathAlembic, edit=True,text=efilePath)
            else:
                print 'No se busco nada.'
    if tabState==2:#tab de import
        global ipathShader
        global ipathAlembic
        if F:
            imultifilter="Maya Files (*.ma *.mb)"
            ifolder=cmds.fileDialog2(cap=" - ELIJE ARCHIVO SHADER- ",startingDirectory='M:/MAYA/01_CHAR',fm=4,ff=imultifilter)#selecciona Archivo
            if ifolder:
                ifilePath=str(str(ifolder[0]).replace('\\','/'))
                cmds.textField(ipathShader, edit=True,text=ifilePath)
            else:
                print 'No se busco nada.'
        else:
            imultifilter="*.abc"
            ifolder=cmds.fileDialog2(cap=" - ELIJE ARCHIVO ALEMBIC - ",startingDirectory='M:/MAYA/01_CHAR',fm=4,ff=imultifilter)#selecciona Archivo
            if ifolder:
                ifilePath=str(str(ifolder[0]).replace('\\','/'))
                cmds.textField(ipathAlembic, edit=True,text=ifilePath)
            else:
                print 'No se busco nada.'
    if tabState==3:#tab de update
        global upathAlembic
        if F:
            umultifilter="*.abc"
            ufolder=cmds.fileDialog2(cap=" - ELIJE ARCHIVO ALEMBIC - ",startingDirectory='M:/MAYA/01_CHAR',fm=4,ff=umultifilter)#selecciona Archivo
            if ufolder:
                ufilePath=str(str(ufolder[0]).replace('\\','/'))
                cmds.textField(upathAlembic, edit=True,text=ufilePath)
            else:
                print 'No se busco nada.'
def repathUI():

    global eloadNameSpace
    global epathShader
    global epathAlembic
    global iloadNameSpace
    global ipathShader
    global ipathAlembic
    global uloadNameSpace
    global upathShader
    global upathAlembic
    global tabs
    global F

    tabs='tabs'
    wPathUI='EXPORPACO v1.6'
    if cmds.window(wPathUI, exists=True):
        cmds.deleteUI(wPathUI)
    if cmds.window(tabs, exists=True):
        cmds.deleteUI(tabs)

    wPathUI=cmds.window(wPathUI,title=wPathUI,resizeToFitChildren=True,s=1)
    tabs = cmds.tabLayout('tabs',innerMarginWidth=100, innerMarginHeight=5)

    #Creo columna de Export
    ecl1=cmds.columnLayout(parent=tabs,adjustableColumn=True,columnOffset=['both',5],rowSpacing=5 )
    etx1=cmds.text("EXPORT ALEMBIC!!",parent=ecl1,bgc=(1,8,0))
    ecl2=cmds.columnLayout(parent=ecl1)
    efl1=cmds.rowLayout(numberOfColumns=3,columnWidth3=[90,100,70],parent=ecl2)
    etx0=cmds.text("NAMESPACE->",h=25,parent=efl1)
    eloadNameSpace=cmds.textField(w=250,h=25,parent=efl1)
    efl2=cmds.rowLayout(numberOfColumns=3,columnWidth3=[90,100,70],parent=ecl2)
    etx2=cmds.text("FILE SHADER->",h=25,parent=efl2)
    epathShader=cmds.textField(w=250,h=25,parent=efl2)
    eloadBtnShd=cmds.button(w=100,label="SELECT FILE",c="PH_EXPORTPACO.selectDir()",parent=efl2)
    efl3=cmds.rowLayout(numberOfColumns=3,columnWidth3=[90,100,70],parent=ecl2)
    etx3=cmds.text("SAVE ALEMBIC->",h=25,parent=efl3)
    epathAlembic=cmds.textField(w=250,h=25,parent=efl3)
    eloadBtnAbc=cmds.button(w=100,label="SAVE .ABC ",c="PH_EXPORTPACO.selectDir(F=False)",parent=efl3)
    cmds.setParent( '..' )
    efixit=cmds.button(l="MANUEAL CREATE ALEMBIC", c="PH_EXPORTPACO.alembic()",w=70,h=80,bgc=(0.8,0.6,0),parent=ecl1)
    #autoExport=cmds.button(l="AUTO CREATE ALEMBIC", c="PH_EXPORTPACO.automaticExport()",w=70,h=80,bgc=(0.8,0.6,0),parent=ecl1)
    #autoSwitch=cmds.button(l="SWITCH CACHE/RIG", c="PH_EXPORTPACO.changebetweencache()",w=70,h=80,bgc=(0.8,0.6,0),parent=ecl1)
    cmds.setParent( '..' )

    #Creo columna de Import
    icl1=cmds.columnLayout(parent=tabs,adjustableColumn=True,columnOffset=['both',5],rowSpacing=5 )
    itx1=cmds.text("IMPORT ALEMBIC!!",parent=icl1,bgc=(0.5,0.8,1))
    icl2=cmds.columnLayout(parent=icl1)
    ifl1=cmds.rowLayout(numberOfColumns=3,columnWidth3=[90,100,70],parent=icl2)
    itx0=cmds.text("NAMESPACE->",h=25,parent=ifl1)
    iloadNameSpace=cmds.textField(w=250,h=25,parent=ifl1)
    ifl2=cmds.rowLayout(numberOfColumns=3,columnWidth3=[90,100,70],parent=icl2)
    itx2=cmds.text("FILE SHADER->",h=25,parent=ifl2)
    ipathShader=cmds.textField(w=250,h=25,parent=ifl2)
    iloadBtnShd=cmds.button(w=100,label="SELECT FILE",c="PH_EXPORTPACO.selectDir(True)",parent=ifl2)
    ifl3=cmds.rowLayout(numberOfColumns=3,columnWidth3=[90,100,70],parent=icl2)
    itx3=cmds.text("FILE ALEMBIC->",h=25,parent=ifl3)
    ipathAlembic=cmds.textField(w=250,h=25,parent=ifl3)
    iloadBtnAbc=cmds.button(w=100,label="SELECT .ABC",c="PH_EXPORTPACO.selectDir(F=False)",parent=ifl3)
    ifixit=cmds.button(l="IMPORT ALEMBIC", c="PH_EXPORTPACO.alembic()",w=70,h=80,bgc=(0.5,0.8,1),parent=icl1)


    #Creo columna de Update
    ucl1=cmds.columnLayout(parent=tabs,adjustableColumn=True,columnOffset=['both',5],rowSpacing=5 )
    utx1=cmds.text("UPDATE ALEMBIC!!",parent=ucl1,bgc=(0.29,0.87,0.35))
    ucl2=cmds.columnLayout(parent=ucl1)
    ufl1=cmds.rowLayout(numberOfColumns=3,columnWidth3=[90,100,70],parent=ucl2)
    utx0=cmds.text("NAMESPACE->",h=25,parent=ufl1)
    uloadNameSpace=cmds.textField(w=250,h=25,parent=ufl1)
    ufl2=cmds.rowLayout(numberOfColumns=3,columnWidth3=[90,100,70],parent=ucl2)
    ufl3=cmds.rowLayout(numberOfColumns=3,columnWidth3=[90,100,70],parent=ucl2)
    utx3=cmds.text("FILE ALEMBIC->",h=25,parent=ufl3)
    upathAlembic=cmds.textField(w=250,h=25,parent=ufl3)
    uloadBtnAbc=cmds.button(w=100,label="SELECT .ABC ",c="PH_EXPORTPACO.selectDir()",parent=ufl3)

    fixit=cmds.button(l="UPDATE ALEMBIC", c="PH_EXPORTPACO.alembic()",w=70,h=80,bgc=(0.29,0.87,0.35),parent=ucl1)

    #Creo los Tabs
    tabs=cmds.tabLayout( tabs, edit=True, tabLabel=((ecl1, 'CREATE ALEMBIC'),(icl1, 'IMPORT ALEMBIC'),(ucl1, 'UPDATE ALEMBIC')))
    cmds.showWindow(wPathUI)
