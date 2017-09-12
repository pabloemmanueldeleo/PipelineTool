# -*- encoding: utf-8 -*-
import maya.cmds as cmds
import os
import sys
path='M:\PH_SCRIPTS\SCRIPTS\PACO'
if not path in sys.path:
    sys.path.append(path)
import PS.MM.cache
#reload(PS.MM.cache)
sys.path.remove(path)

#automatica export
def automaticExport():
    PS.MM.cache.exportSelectedAssets()

#Cambia elijiendo un transform entre el cache y el rig, apagando la refe.
def changebetweencache():
    PS.MM.cache.switchSelectedRigCache()

#select dirs
def repathUI():

    global eloadNameSpace
    global epathShader
    global epathAlembic
    global ibaseNameSpace
    global iloadNameSpace
    global ipathShader
    global ipathAlembic
    global uloadNameSpace
    global upathAlembic
    global tabs

    tabs='tabs'
    wPathUI='EXPORPACO v1.70 - 17-08-2015'
    if cmds.window(wPathUI, exists=True):
        cmds.deleteUI(wPathUI)
    if cmds.window(tabs, exists=True):
        cmds.deleteUI(tabs)

    wPathUI=cmds.window(wPathUI,title=wPathUI,resizeToFitChildren=True,s=1,titleBarMenu=True)
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
    eloadBtnShd=cmds.button(w=100,label="SELECT FILE",c=handleSelectSHDFileForExport,parent=efl2)
    efl3=cmds.rowLayout(numberOfColumns=3,columnWidth3=[90,100,70],parent=ecl2)
    etx3=cmds.text("SAVE ALEMBIC->",h=25,parent=efl3)
    epathAlembic=cmds.textField(w=250,h=25,parent=efl3)
    eloadBtnAbc=cmds.button(w=100,label="SAVE .ABC ",c=handleSelectABCFileForExport,parent=efl3)
    cmds.setParent( '..' )
    efixit=cmds.button(l="CREATE ALEMBIC", c=handleExport,w=70,h=80,bgc=(0.8,0.6,0),parent=ecl1)
    etextHelp=cmds.text('''
    *-HELP-*
    IMPORTANTE: -EXPORTA EL TIMELINE QUE ESTAs VIENDO EN LA BARRA-

    NAMESPACE:
        Es todo nombre de namespace del personaje.
        Ejemplo = UD16_E109_004A_ARTURO_3:arturo004A

    FILE SHADER:
        Archivo de maya que contiene el personaje con UV y SHD.
        Ejemplo = M:/MAYA/01_CHAR/04A_ARTURO/04A_ARTURO_SHD_v039.ma

    SAVE ALEMBIC:
        Ruta y nombre del archivo que tendra el cache del alembic.
        Si lo guardan local primero mejor.
        Ejemplo = D:/test_eman.abc , D:/CACHE/E109_P05_ARTURO.abc

    ''',align='left')

    #Creo columna de Import
    icl1=cmds.columnLayout(parent=tabs,adjustableColumn=True,columnOffset=['both',5],rowSpacing=5 )
    itx1=cmds.text("IMPORT ALEMBIC!!",parent=icl1,bgc=(0.5,0.8,1))
    icl2=cmds.columnLayout(parent=icl1)
    ifl0=cmds.rowLayout(numberOfColumns=3,columnWidth3=[100,100,70],parent=icl2)
    cmds.text("REF NAMESPACE->",h=25,parent=ifl0)
    ibaseNameSpace=cmds.textField(w=250,h=25,parent=ifl0,text=":")
    ifl1=cmds.rowLayout(numberOfColumns=3,columnWidth3=[100,100,70],parent=icl2)
    itx0=cmds.text("NAMESPACE->",h=25,parent=ifl1)
    iloadNameSpace=cmds.textField(w=250,h=25,parent=ifl1)
    ifl2=cmds.rowLayout(numberOfColumns=3,columnWidth3=[100,100,70],parent=icl2)
    itx2=cmds.text("FILE SHADER->",h=25,parent=ifl2)
    ipathShader=cmds.textField(w=250,h=25,parent=ifl2)
    iloadBtnShd=cmds.button(w=100,label="SELECT FILE",c=handleSelectSHDFileForImport,parent=ifl2)
    ifl3=cmds.rowLayout(numberOfColumns=3,columnWidth3=[100,100,70],parent=icl2)
    itx3=cmds.text("FILE ALEMBIC->",h=25,parent=ifl3)
    ipathAlembic=cmds.textField(w=250,h=25,parent=ifl3)
    iloadBtnAbc=cmds.button(w=100,label="SELECT .ABC",c=handleSelectABCFileForImport,parent=ifl3)
    ifixit=cmds.button(l="IMPORT ALEMBIC", c=handleImport,w=70,h=80,bgc=(0.5,0.8,1),parent=icl1)
    cmds.setParent( '..' )
    itextHelp=cmds.text('''
    *-HELP-*

    REF NAMESPACE:
        El namespace de la referencia. Si asignan este valor pueden dejar el segundo en blanco.
        Esto sirve en caso de que quieran importar el mismo asset mas de una vez en la escena
        como suelen pasar con los caballos.
        Ejemplo = arturo004A ,Ejemplo = CaballoA , Ejemplo = CaballoB

    NAMESPACE:
        Nombre del personaje a importar.
        Ejemplo = arturo004A , Ejemplo = pilar, Ejemplo = h1a

    FILE SHADER:
        Archivo de maya que contiene el personaje con UV y SHD.
        Ejemplo = M:/MAYA/01_CHAR/04A_ARTURO/04A_ARTURO_SHD_v039.ma
        Ejemplo = M:/MAYA/01_CHAR/04A_ARTURO/04A_ARTURO_GAMMA_SHD.ma

    FILE ALEMBIC:
        Cargar la ruta y archivo del cache de alembic.
        Ejemplo = D:/test_eman.abc , D:/CACHE/E109_P05_ARTURO.abc

    ''',align='left')
    cmds.setParent( '..' )
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
    uloadBtnAbc=cmds.button(w=100,label="SELECT .ABC ",c=handleSelectABCFileForUpdate,parent=ufl3)
    ufixit=cmds.button(l="UPDATE ALEMBIC", c=handleUpdate,w=70,h=80,bgc=(0.29,0.87,0.35),parent=ucl1)
    cmds.setParent( '..' )
    utextHelp=cmds.text('''
    *-HELP-*

    Esto sirve para que puedan actualizar el alembic referenciado existente.

    NAMESPACE:
        Namespace del personaje a actualizar.
        Ejemplo = :UD16_E109_004A_ARTURO_3:arturo004A

    FILE ALEMBIC:
        Cargar la ruta y archivo del cache de alembic.
        Ejemplo = D:/test_eman.abc , D:/CACHE/E109_P05_ARTURO.abc

    ''',align='left')
    #Creo los Tabs
    tabs=cmds.tabLayout( tabs, edit=True, tabLabel=((ecl1, 'CREATE ALEMBIC'),(icl1, 'IMPORT ALEMBIC'),(ucl1, 'UPDATE ALEMBIC')))
    cmds.showWindow(wPathUI)

def handleExport( args ):

	global eloadNameSpace
	global epathShader
	global epathAlembic
    #tico:Asset
    #D:/PH_SCRIPTS/SCENES_RIG/PACOTEST/CHAR/TICO/03_TICO_SHD.ma
    #D:/PH_SCRIPTS/SCENES_RIG/PACOTEST/ALEMBIC
	rigNamespace = cmds.textField( eloadNameSpace, edit=False, text=True, q=1 )
	assetSHDPath = cmds.textField( epathShader, edit=False, text=True, q=1 )
	cachePath    = cmds.textField( epathAlembic, edit=False, text=True, q=1 )
	PS.MM.cache.exportAssetCache( rigNamespace, assetSHDPath, cachePath )

def handleSelectSHDFileForExport( args ):

	file = selectFile( " - ELIJE ARCHIVO SHADER - ", "M:/MAYA/01_CHAR", "Maya Files (*.ma *.mb)" )

	if file:
		cmds.textField( epathShader, edit=True, text=file )

def handleSelectABCFileForExport( args ):

	file = selectFile( " - NOMBRAR Y GUARDAR EL ALEMBIC- ", "M:/", "*.abc", fm=5 )

	if file:
		cmds.textField( epathAlembic, edit=True, text=file )

def handleImport( args ):

	global ibaseNameSpace
	global iloadNameSpace
	global ipathShader
	global ipathAlembic

	baseNameSpace  = cmds.textField(ibaseNameSpace, edit=False, text=True, q=1)
	assetNamespace = cmds.textField(iloadNameSpace, edit=False, text=True, q=1)
	assetSHDPath   = cmds.textField(ipathShader, edit=False, text=True, q=1)
	cachePath      = cmds.textField(ipathAlembic, edit=False, text=True, q=1)

	PS.MM.cache.referenceAssetWithCache( assetNamespace, assetSHDPath, cachePath, baseNameSpace )

def handleSelectSHDFileForImport( args ):

	file = selectFile( " - ELIJE ARCHIVO SHADER- ", 'M:/MAYA/01_CHAR', "Maya Files (*.ma *.mb)", fm=4 )

	if file:
		cmds.textField( ipathShader, edit=True, text=file )

def handleSelectABCFileForImport( args ):

	file = selectFile( " - ELIJE ARCHIVO ALEMBIC - ", 'M:/MAYA/01_CHAR', "*.abc", fm=4 )

	if file:
		cmds.textField( ipathAlembic, edit=True, text=file )

def handleUpdate( args ):

	global uloadNameSpace
	global upathAlembic
	assetNamespace = cmds.textField(uloadNameSpace, edit=False, text=True, q=1)
	cachePath      = cmds.textField(upathAlembic, edit=False, text=True, q=1)

	try:
		cmds.refresh( su=True )
		PS.MM.cache.updateAssetCache( assetNamespace, cachePath )
	finally:
		cmds.refresh( su=False )

def handleSelectABCFileForUpdate( args ):

	file = selectFile( " - ELIJE ARCHIVO ALEMBIC - ", 'M:/MAYA/01_CHAR', "*.abc", fm=4 )

	if file:
		cmds.textField( upathAlembic, edit=True, text=file )

def selectFile( cap, dir, types,fm=4 ):

	ifolder = cmds.fileDialog2(cap=cap,startingDirectory=dir,fm=fm,ff=types)

	if ifolder:
		return str(str(ifolder[0]).replace('\\','/'))
	else:
		return None
