import maya.cmds as cmds
from functools import partial
from operator import itemgetter
global grupoVG,grupoVCreacion,dock,dockLuces
global orden,ultimoOrden
global ultimoGrupoCreadoPorUsuario
global aiColorTemperatureSlider

deactivateSUB = False
global buscarPor_Grupo_Luz
buscarPor_Grupo_Luz = "luz"
global copiarValor
global isolate
deactivateSSS = False
deactivateDisplacement = False
myLights = cmds.ls(type='light')
myLightsOn = cmds.ls(type='light', visible=True)
mySelection = cmds.ls (selection = True)
global seleccionLista1

def add_light(kind):
	global contSpot
	global contDir
	global contPoint
	global contArea
	global contAmb
	global grupoVCreacion,dock

	primerGrupoCreado = ""
	descripcionDelRootOK=""
	if(not cmds.ls('ROOT_*_LGRP')):
		descripcionDelRootOK = cmds.promptDialog(
		title='DESCRIPCION ROOT',
		message='INGRESA DESCRIPCION DEL ROOT NUEVO:',
		button=['OK', 'Cancelar'],
		defaultButton='OK',
		cancelButton='Cancelar',
		dismissString='Cancelar')
	else:
	    descripcionDelRootOK='YA HAY ROOT'

	if descripcionDelRootOK=='OK':
		root = cmds.group(name='ROOT_'+ cmds.promptDialog(query=True, text=True) +'_LGRP', em=True, w=True)
		rootAts = cmds.listAttr (root , k=1 )
		for at in rootAts:
			cmds.setAttr (root+"."+at,lock=1,k=0,channelBox=0)
	else:
	    descripcionDelRootOK='YA HAY ROOT'

	grupos_LGRP = cmds.ls ('*_LGRP')
	if  ( descripcionDelRootOK=='OK' and len(grupos_LGRP)==1  ) or ( descripcionDelRootOK=='YA HAY ROOT' and len(grupos_LGRP)==1 ) :# or len(cmds.ls('ROOT*_LGRP'))==1
		cmds.confirmDialog ( title='AVISO', message='NO HAY GRUPOS DE LUCES EN LA ESCENA. CREEMOS UNO.', button=['OKI'], defaultButton='OKI' )
		primerGrupoCreado = crearGrupo()

	roots_LGRP = cmds.ls ('ROOT_*_LGRP')

	if ((len(grupos_LGRP)>=1 and len(roots_LGRP)==1) and primerGrupoCreado != "") or descripcionDelRootOK=='YA HAY ROOT' and len(grupos_LGRP)>1 :
		if cmds.window('crearLuzV',exists=True):
			cmds.deleteUI ('crearLuzV')
		ventanaCreacionLuz = cmds.window ('crearLuzV' , menuBar=0,w=250,title = "CREAR LUZ" )
		col_ventanaCrearLuz = cmds.columnLayout( adjustableColumn = True , p = ventanaCreacionLuz )
		cmds.textField ('nombreLuzCreacion' , pht='NOMBRE' ,  p=col_ventanaCrearLuz )
		grupoVCreacion = cmds.optionMenu ( 'oM_grupoVCreacion',    bgc = [0.1,0.1,0.1] , p = col_ventanaCrearLuz)
		clearOptionMenu ( grupoVCreacion )
		gruposDeLuces = cmds.ls ( '*_LGRP' , type='transform',referencedNodes=0 )
		rootDeLaEscena = cmds.ls ( 'ROOT_*_LGRP' , type='transform' ,referencedNodes=0)
		gruposDeLuces = list ( set ( gruposDeLuces ) - set ( rootDeLaEscena  ) )
		for grp in gruposDeLuces:
			cmds.menuItem(parent=grupoVCreacion, label=grp[:-5] )
		try:
			cmds.optionMenu ( grupoVCreacion, e=1 , v = ultimoGrupoCreadoPorUsuario.split ("_LGRP")[0] )
		except :
			pass
		cmds.radioCollection('coleccionTodo')
		rowDeColumnas=cmds.rowLayout (nc=3,co3=[25,0,0],ct3=["left", "both","both"], p=col_ventanaCrearLuz)
		row_ventanaCrearLuz = cmds.columnLayout( p = rowDeColumnas )
		cmds.radioCollection()
		cmds.radioButton( 'K',label='KEY', sl=1,cl='coleccionTodo')
		row_ventanaCrearLuz = cmds.columnLayout( p = rowDeColumnas )
		cmds.radioCollection()
		cmds.radioButton('F', label='FILL', cl='coleccionTodo')
		row_ventanaCrearLuz = cmds.columnLayout( p = rowDeColumnas )
		cmds.radioCollection()
		cmds.radioButton( 'R',label='RIM', cl='coleccionTodo')
		cmds.button ('b_crearLuz' , l='CREAR', c=  partial(crearLuz,kind,primerGrupoCreado) , p=col_ventanaCrearLuz)
		cmds.button ('b_cancelarCrearLuz' , l='CANCELAR' , c="cmds.deleteUI('crearLuzV')" , p=col_ventanaCrearLuz)
		cmds.showWindow ('crearLuzV')

def duplicarLuz(*args):
    lucesSeleccionadas = cmds.textScrollList('listaLuces1',q=1, si=1)
    copiasDeLuces = []
    for luz in lucesSeleccionadas:
        nombreLuzTRF = luz[:-8]+ str(int(luz[-8:-5])+1).zfill(3)  + luz[-5:]
        while cmds.objExists (nombreLuzTRF)==1:
            nombreLuzTRF = luz[:-8]+ str(int(nombreLuzTRF[-8:-5])+1).zfill(3)  + luz[-5:]
        cmds.duplicate ( luz , rr=1 , ic=1 , n=nombreLuzTRF )
        copiasDeLuces.append(nombreLuzTRF)
    ordenarLuz()
    ordenarLuz()
    cmds.textScrollList('listaLuces1',e=1, da=1)
    cmds.textScrollList('listaLuces2',e=1, da=1)
    cmds.textScrollList('listaLuces3',e=1, da=1)
    cmds.textScrollList('listaLuces1',e=1, si=copiasDeLuces)
    indexSeleccionLista1 = cmds.textScrollList('listaLuces1',q=1, sii=1)
    cmds.textScrollList('listaLuces2',e=1, sii=indexSeleccionLista1)
    cmds.textScrollList('listaLuces3',e=1, sii=indexSeleccionLista1)
    cmds.warning (" - - - DUPLICADO: SE HAN SELECCIONADO LAS LUCES NUEVAS - - - ")

def crearLuz(kind="",primerGrupoCreado='' , nombre=''):

    global grupoVG
    global grupoVCreacion,dock,dockLuces
    if nombre=="" or nombre==False:
        nombreLuz = cmds.textField('nombreLuzCreacion',q=1,text=1)+"_"+cmds.radioCollection('coleccionTodo',q=1,select=1)+"_"
        grupoDeLaLuzCreada = cmds.optionMenu (grupoVCreacion,q=1,value=1)
        if nombreLuz=="_"+cmds.radioCollection('coleccionTodo',q=1,select=1)+"_" or nombreLuz[0] in "0123456789": #si no puso ningun nombre
            nombreLuz = 'RENAMEMEPLEASE'+"_"+cmds.radioCollection('coleccionTodo',q=1,select=1)+"_"
    else:
        nombreLuz=nombre
        grupoDeLaLuzCreada = (cmds.listRelatives (nombreLuz,parent=1))[0][:-5]
        nombreLuz=nombre[:-8]

    if kind == 'spot':
        nameLight = cmds.spotLight(name=nombreLuz)
        nameLight = cmds.rename (nameLight, nameLight.split("Shape")[0]+"SH")
        nombreSinSuff = cmds.listRelatives(nameLight, shapes=True, children= True, allParents=True)[0]
        nroLuz=1
        if cmds.objExists (nombreSinSuff+str(nroLuz).zfill(3)+'_LSPT'):
            while cmds.objExists (nombreSinSuff+str(nroLuz).zfill(3)+'_LSPT'):
                nroLuz +=1
            nombreSinSuff = cmds.rename(  nombreSinSuff , nombreSinSuff + str(nroLuz).zfill(3) )
            nombreConSuff = cmds.rename(  nombreSinSuff , nombreSinSuff + '_LSPT' )
        else:
            nombreConSuff=cmds.rename(  nombreSinSuff , nombreSinSuff + str(nroLuz).zfill(3) + '_LSPT')
        cmds.select(nombreConSuff)
        cmds.parent(nombreConSuff, grupoDeLaLuzCreada+'_LGRP')

    elif kind == 'dir':
        nameLight = cmds.directionalLight(name=nombreLuz)
        nameLight = cmds.rename (nameLight, nameLight.split("Shape")[0]+"SH")
        nombreSinSuff = cmds.listRelatives(nameLight, shapes=True, children= True, allParents=True)[0]
        nroLuz=1
        if cmds.objExists (nombreSinSuff+str(nroLuz).zfill(3)+'_LDIR'):
            while cmds.objExists (nombreSinSuff+str(nroLuz).zfill(3)+'_LDIR'):
                nroLuz +=1
            nombreSinSuff = cmds.rename(  nombreSinSuff , nombreSinSuff + str(nroLuz).zfill(3) )
            nombreConSuff = cmds.rename(  nombreSinSuff , nombreSinSuff + '_LDIR' )
        else:
            nombreConSuff=cmds.rename(  nombreSinSuff , nombreSinSuff + str(nroLuz).zfill(3) + '_LDIR')
        cmds.select(nombreConSuff)
        cmds.parent(nombreConSuff, grupoDeLaLuzCreada+'_LGRP')

    elif kind == 'point':
        nameLight = cmds.pointLight(name=nombreLuz)
        nameLight = cmds.rename (nameLight, nameLight.split("Shape")[0]+"SH")
        nombreSinSuff = cmds.listRelatives(nameLight, shapes=True, children= True, allParents=True)[0]
        nroLuz=1
        if cmds.objExists (nombreSinSuff+str(nroLuz).zfill(3)+'_LPNT'):
            while cmds.objExists (nombreSinSuff+str(nroLuz).zfill(3)+'_LPNT'):
                nroLuz +=1
            nombreSinSuff = cmds.rename(  nombreSinSuff , nombreSinSuff + str(nroLuz).zfill(3) )
            nombreConSuff = cmds.rename(  nombreSinSuff , nombreSinSuff + '_LPNT' )
        else:
            nombreConSuff=cmds.rename(  nombreSinSuff , nombreSinSuff + str(nroLuz).zfill(3) + '_LPNT')
        cmds.select(nombreConSuff)
        cmds.parent(nombreConSuff, grupoDeLaLuzCreada+'_LGRP')

    elif kind == 'area':
        nombreLuz = cmds.group(name = nombreLuz, em=True, w=True)
        nameLight = cmds.shadingNode('areaLight',name=nombreLuz+"SH",p=nombreLuz,asLight=True).encode("utf-8")
        nameLightSH = nombreLuz
        nombreSinSuff = cmds.listRelatives(nameLight, shapes=True, children= True)[0]
        nroLuz=1
        if cmds.objExists (nombreLuz+str(nroLuz).zfill(3)+'_LARE'):
            while cmds.objExists (nombreLuz+str(nroLuz).zfill(3)+'_LARE'):
                nroLuz +=1
            nombreLuz = cmds.rename(  nombreLuz , nombreLuz + str(nroLuz).zfill(3) )
            nombreConSuff = cmds.rename(  nombreLuz , nombreLuz + '_LARE' )
        else:
            nombreConSuff=cmds.rename(  nombreLuz , nombreLuz + str(nroLuz).zfill(3) + '_LARE')
        cmds.select(nombreConSuff)
        cmds.parent(nombreConSuff, grupoDeLaLuzCreada+'_LGRP')

    ordenarLuz()
    rutaOM = clearOptionMenu (grupoVG)
    gruposDeLuces = cmds.ls ( '*_LGRP' , type='transform' )
    rootDeLaEscena = ""
    roots = cmds.ls('ROOT_*_LGRP',r=1)
    listaDeRootsNoReferenciados=[]

    for root in roots:
        if cmds.referenceQuery( root ,isNodeReferenced=1 ) == False:
            listaDeRootsNoReferenciados.append (root)
    if len(listaDeRootsNoReferenciados)==1:
        rootDeLaEscena = listaDeRootsNoReferenciados[0]
    for grp in gruposDeLuces:
        if grp !=rootDeLaEscena and cmds.referenceQuery( grp ,isNodeReferenced=1 ) == False :
            cmds.menuItem( parent = dock +  grupoVG.split("winMLuces")[1] , label = grp[:-5] )
    if cmds.window('crearLuzV',q=1,ex=1):
        cmds.deleteUI ('crearLuzV')
    cmds.textScrollList ('listaLuces1',e=1,da=1)
    cmds.textScrollList ('listaLuces1',e=1,si=nombreConSuff)
    ordenarLuz()
    ordenarLuz()
    refreshui()
    return nombreConSuff

def clearOptionMenu (optionMenu):
	optionMenuFullName = None
	try:
		menuItems = cmds.optionMenu ( optionMenu , q=1 , ill=1 )
		if menuItems != None and menuItems !=[]:
			cmds.deleteUI ( menuItems )
		firstItem = menuItems[0]
		optionMenuFullName = firstItem [:-len(firstItem.split ("|")[1])-1]
	except:
		pass
	return optionMenuFullName

def verAtraves(*args):
	# VER A TRAVES . . .
	if cmds.window ('v_Ver',ex=1):
		cmds.deleteUI ('v_Ver')
	if cmds.modelPanel ('mp_ver',ex=1):
		cmds.deleteUI ('mp_ver', panel=1)
	luzSeleccionada = cmds.textScrollList ('listaLuces1', q=1 , si=1 )[0]
	cmds.window( 'v_Ver' , title='VIENDO: '+luzSeleccionada)
	frameLayout_1 = cmds.frameLayout( lv=0 ,w=500 , h=500 , p='v_Ver' , collapsable=1 )
	cmds.modelPanel( 'mp_ver' , l='' ,menuBarVisible=0 , p=frameLayout_1)
	nombreEditor = cmds.modelPanel( 'mp_ver' , q=1 , modelEditor=1)
	cmds.modelEditor (nombreEditor  , e =1 ,displayAppearance="smoothShaded",
	 	polymeshes=1,
	 	nurbsSurfaces=1,
	 	planes=1,
	 	lights=1,
	 	cameras=0,
	 	controlVertices=0,
	 	grid=0,
	 	hulls=0,
	 	joints=0,
	 	ikHandles=0,
	 	nurbsCurves=0,
	 	deformers=0,
	 	dynamics=1,
	 	fluids=0,
	 	hairSystems=0,
	 	follicles=0,
	 	nCloths=1,
	 	nParticles=1,
	 	nRigids=1,
	 	dynamicConstraints=0,
	 	locators=0,
	 	manipulators=0,
	 	dimensions=0,
	 	handles=0,
	 	pivots=1,
	 	textures=0,
	 	strokes=0,
	 	pluginShapes=1,
	 	queryPluginObjects=1,
	 	)
	cmds.lookThru( luzSeleccionada , 'mp_ver' )
	cmds.showWindow()

def borrarBuscador(args):
	cmds.textField ('buscador' , e=1 , text="")
	cmds.warning ("~~~~~~~~~ borrarBuscador() ~~~~~~~~~")

def seleccionarLuces():
    shapesSeleccionado = cmds.listRelatives (cmds.textScrollList ('listaLuces1',q=1, si=1) , shapes=1)
    cmds.select ( shapesSeleccionado )

def tglTodos():
	botonesFiltros = ['LDIR','LSPT','LPNT','LARE',]
	imagenEstado = int(cmds.iconTextButton ('b_filtroLSPT',q=1, i1=1)[-5])
	for boton in botonesFiltros:
		cmds.iconTextButton ("b_filtro"+boton,e=1,i1="M:\PH_SCRIPTS\ICONS\\"+boton+"_"+str(int(not(imagenEstado)))+".png")
	filtradoRefresh()

def filtrado(luzTipo):
    # CAMBIA EL ICONO A ON / OFF
	global seleccion

	imagen = cmds.iconTextButton ('b_filtro'+luzTipo,q=1, i1=1)
	seleccion = cmds.textScrollList ('listaLuces1',q=1,si=1)
	if int(imagen[-5])==1:
		cmds.iconTextButton ('b_filtro'+luzTipo , e=1 , i1="M:\PH_SCRIPTS\ICONS\\"+luzTipo+"_0.png")
	if int(imagen[-5])==0:
		cmds.iconTextButton ('b_filtro'+luzTipo , e=1 , i1="M:\PH_SCRIPTS\ICONS\\"+luzTipo+"_1.png")
	filtradoRefresh()

def filtradoRefresh():
    filtros = ['b_filtroLPNT','b_filtroLDIR','b_filtroLSPT','b_filtroLARE']
    filtrosActivos=[]
    for filtro in filtros:
        estadoFiltro = int  ((cmds.iconTextButton (filtro , q = 1 , i1=1))[-5])
        if estadoFiltro==1:
            filtrosActivos.append ( "*"+ filtro[-4:] + "SH" )
    try:
        ordenarTipo( arraySufijos = filtrosActivos )
        boldOblique()
        enableDropParent()
    except:
        pass

def ordenarDatos(ordenarPor , filtrado=''):
    if filtrado=='':
	    luces = cmds.ls(['*_LPNTSH','*_LDIRSH','*_LARESH','*_LAMBSH','*_LSPTSH'],r=1,lights = True)
    else:
    	luces = cmds.ls( filtrado ,r=1, lights = True)
    datos_Dic={}
    for l in luces:
        name = cmds.listRelatives(l,type='transform',p=True)[0]
        grupo = cmds.listRelatives(name,type='transform',p=True)[0]
        lightType = cmds.nodeType(l)
        datos_Dic[name] = [lightType,l,grupo]
    lucesOrdenadas_=[]
    tiposOrdenados_=[]
    gruposOrdenados_=[]
    lucesTuplas=[]
    dicLuces_xTipo={}
    dicLuces_xGrupo={}
    # ORDENA POR NOMBRE
    if ordenarPor=='luz':
        lucesTuplas = sorted(datos_Dic.items(), key=itemgetter(0))
        for tupla in lucesTuplas:
            lucesOrdenadas_.append (tupla[0])
            tiposOrdenados_.append (tupla[1][0])
            gruposOrdenados_.append (tupla[1][2][:-5])
    ##########
    # ORDENA POR TIPO
    elif ordenarPor=='tipo':
        for key in datos_Dic.keys():
            dicLuces_xTipo[key] = datos_Dic [key][0]
            dicLuces_xGrupo[key] = datos_Dic [key][2]
        tuplas = sorted(dicLuces_xTipo.items(), key=itemgetter(1))
        for tupla in tuplas:
            lucesOrdenadas_.append (tupla[0])
            tiposOrdenados_.append (tupla[1])
            gruposOrdenados_.append (dicLuces_xGrupo [ tupla[0] ][:-5] )
    ##########
    # ORDENA POR GRUPO
    elif ordenarPor=='grupo':
        for key in datos_Dic.keys():
            dicLuces_xTipo[key] = datos_Dic [key][0]
            dicLuces_xGrupo[key] = datos_Dic [key][2]
        tuplas = sorted(dicLuces_xGrupo.items(), key=itemgetter(1))
        for tupla in tuplas:
            lucesOrdenadas_.append (tupla[0])
            gruposOrdenados_.append (tupla[1] [:-5])
            tiposOrdenados_.append (dicLuces_xTipo [ tupla[0] ] )
    return [lucesOrdenadas_,tiposOrdenados_,gruposOrdenados_]

def ordenarTipo( arraySufijos =[],seleccionar=1):
    global seleccion
    global orden
    if arraySufijos =='':
        datosOrdenados =  ordenarDatos(ordenarPor='tipo' , filtrado='')
    else:
        datosOrdenados = ordenarDatos(ordenarPor='tipo' , filtrado=arraySufijos)
    if orden["tipo"]%2 == 1:
        datosOrdenados[0].reverse()
        datosOrdenados[1].reverse()
        datosOrdenados[2].reverse()
    listas = ['listaLuces1','listaLuces2','listaLuces3']
    for lista in listas:#limpio listas
        cmds.textScrollList (lista, e=1 ,ra=1)
    if datosOrdenados:
        try:
            cmds.textScrollList ('listaLuces1' , e=1  ,  a=datosOrdenados[0] , numberOfRows = len(datosOrdenados[0])+2) #lleno lista1
            cmds.textScrollList ('listaLuces2' , e=1  ,  a=datosOrdenados[1] , numberOfRows = len(datosOrdenados[0])+2)
            cmds.textScrollList ('listaLuces3' , e=1  ,  a=datosOrdenados[2] , numberOfRows = len(datosOrdenados[0])+2)
            indiceSeleccionLista1 = cmds.textScrollList ('listaLuces1' , q=1 , sii=1 ) # obtengo indices de items1
            boldOblique()
            if seleccion!=None:
                cmds.textScrollList ('listaLuces1' , e=1 , si=seleccion )
                cmds.textScrollList ('listaLuces2' , e=1  ,  sii= cmds.textScrollList ('listaLuces1' , q=1 , sii=1 ))
                cmds.textScrollList ('listaLuces3' , e=1  ,  sii= cmds.textScrollList ('listaLuces1' , q=1 , sii=1 ))
        except:
            pass
        orden["tipo"] +=1
        ultimoOrden="tipo"

def qVisibilidadAbsoluta(luz,*args):
    visibilidadAbsoluta =1
    print "\n\n"
    if cmds.objExists(luz+"SH"):
        luzFullPath = cmds.ls (luz+"SH",long=1)[0]
        luzFullPathSPLIT = luzFullPath.split("|")[1:]
        for p in luzFullPathSPLIT:
            if visibilidadAbsoluta:
                visibilidad=cmds.getAttr(p+".visibility")
                print p,visibilidad
                if not visibilidad:
                    visibilidadAbsoluta=0
    return visibilidadAbsoluta

def visibilidadDeRuta( *args):
    if cmds.window('visibilidad' , q=1 , ex=1):
        cmds.deleteUI ( 'visibilidad' )
        try:
            cmds.deleteUI (filtroLuces)
        except:
            pass
    global outliner
    global filtroLuces
    seleccionLista1 = cmds.textScrollList ('listaLuces1' , q=1 , si=1)[0]
    pV=[]# visibilidad de parents
    if seleccionLista1:
        ruta = cmds.ls(seleccionLista1,long=1)[0]
        parents = ruta.split("|")[1:]
    for p in parents:
        if cmds.getAttr(p+".visibility"):
            pV.append(1)
        else:
            pV.append(0)
    cmds.select (parents)

    cmds.window('visibilidad' , t='VISIBILIDAD')
    cmds.frameLayout( labelVisible=False )
    panel = cmds.outlinerPanel()
    outliner = cmds.outlinerPanel(panel, query=True,outlinerEditor=True)
    cmds.outlinerEditor( outliner, edit=1, mainListConnection='worldList', selectionConnection='modelList', showShapes=0, showReferenceNodes=0, showReferenceMembers=0, showAttributes=0, showConnected=0, showAnimCurvesOnly=0, autoExpand=1, expandObjects=1,showDagOnly=1, ignoreDagHierarchy=0, expandConnections=0, showNamespace=1, showCompounds=1, showNumericAttrsOnly=0, highlightActive=1, autoSelectNewObjects=0, doNotSelectNewObjects=0, transmitFilters=0, showSetMembers=1, setFilter='defaultSetFilter', ignoreHiddenAttribute=0 )

    inputList =cmds.selectionConnection (worldList=1)
    selecCon = cmds.selectionConnection()
    filtroLuces = cmds.itemFilter ( byType= ("spotLight" , "directionalLight" , "pointLight" , "areaLight") )
    cmds.outlinerEditor ( outliner , e=1 , mainListConnection=inputList)
    cmds.outlinerEditor ( outliner , e=1 , selectionConnection = selecCon , filter = filtroLuces )
    cmds.showWindow()

def visibilidadDeRutaCerrar (*args):
    global outliner
    global filtroLuces
    cmds.delete ( filtroLuces )
    cmds.deleteUI ('visibilidad')

def dropListas():
	pop = cmds.popupMenu(p='listaLuces1')#|textScrollList
	cmds.menuItem(l="DUPLICAR" , c=duplicarLuz , p=pop)
	cmds.menuItem(l="VER A TRAVES DE ESTA LUZ" , c= verAtraves,  en=1 ,p=pop)
	cmds.menuItem(l="CREAR PRESET" , c='print "crearPreset()"', en=0 , p=pop)
	pop = cmds.popupMenu(p='listaLuces2')#|textScrollList
	cmds.menuItem(l="DUPLICAR" , c=duplicarLuz , p=pop)
	cmds.menuItem(l="CREAR PRESET" , c='print "crearPreset()"', en=0 , p=pop)
	cmds.menuItem(l="VER A TRAVES DE ESTA LUZ" , c=verAtraves,  en=0 ,p=pop)
	pop = cmds.popupMenu(p='listaLuces3')#|textScrollList
	cmds.menuItem(l="RENOMBRAR GRUPO" , c=renombrarGrupo, p=pop)
	cmds.menuItem( divider=1 , p=pop )
	cmds.menuItem( l="VISIBILIDAD" , c=visibilidadDeRuta, p=pop)
	cmds.menuItem( divider=1 , p=pop )
	cmds.menuItem( l="CERRAR VISIBILIDAD" , c=visibilidadDeRutaCerrar, p=pop)

def refreshui(refrescarPor="",*args):
	global aiColorTemperatureSlider
	global haySeleccionEnLista
	global grupoVG
	global win
	refreshOverride()
	if refrescarPor=='luz':
		lucesSeleccionadasIndices = cmds.textScrollList('listaLuces1' ,q=1, sii=1)
		cmds.textScrollList ('listaLuces2' , e=1 ,da=1)
		cmds.textScrollList ('listaLuces3' , e=1 ,da=1)
		try:
			cmds.textScrollList ('listaLuces2' , e=1 ,sii=lucesSeleccionadasIndices)
			cmds.textScrollList ('listaLuces3' , e=1 ,sii=lucesSeleccionadasIndices)
		except:
			pass
	if refrescarPor=='tipo':
		lucesSeleccionadasIndices = cmds.textScrollList('listaLuces2' ,q=1, sii=1)
		cmds.textScrollList ('listaLuces1' , e=1 ,da=1)
		cmds.textScrollList ('listaLuces3' , e=1 ,da=1)
		try:
			cmds.textScrollList ('listaLuces1' , e=1 ,sii=lucesSeleccionadasIndices)
			cmds.textScrollList ('listaLuces3' , e=1 ,sii=lucesSeleccionadasIndices)
		except:
			pass
	if refrescarPor=='grupo':
		lucesSeleccionadasIndices = cmds.textScrollList('listaLuces3' ,q=1, sii=1)
		cmds.textScrollList ('listaLuces1' , e=1 ,da=1)
		cmds.textScrollList ('listaLuces2' , e=1 ,da=1)
		try:
			cmds.textScrollList ('listaLuces1' , e=1 ,sii=lucesSeleccionadasIndices)
			cmds.textScrollList ('listaLuces2' , e=1 ,sii=lucesSeleccionadasIndices)
		except:
			pass
	#ACTUALIZO GRUPOS
	rootDeLaEscena = ""
	roots = cmds.ls('ROOT_*_LGRP',r=1)
	listaDeRootsNoReferenciados=[]
	for root in roots:
		if cmds.referenceQuery( root ,isNodeReferenced=1 ) == False:
			listaDeRootsNoReferenciados.append (root)

	if len(listaDeRootsNoReferenciados)==1:
		rootDeLaEscena = listaDeRootsNoReferenciados[0]
	clearOptionMenu (grupoVG)
	gruposDeLuces = cmds.ls ( '*_LGRP' , type='transform' )
	for grp in gruposDeLuces:
		if grp !=rootDeLaEscena and cmds.referenceQuery( grp ,isNodeReferenced=1 ) == False :
			cmds.menuItem(parent=grupoVG , label=grp[:-5] )
	clearOptionMenu (grupoCParent)
	for grp in gruposDeLuces:
		if grp != rootDeLaEscena and cmds.referenceQuery( grp ,isNodeReferenced=1 ) == False:
			cmds.menuItem(parent=dock +  grupoCParent.split("winMLuces")[1] , label=grp[:-5] )

	# REFRESH DE ATRIBUTOS.
	lucesSeleccionadas = cmds.textScrollList('listaLuces1' ,q=1, si=1)

	if lucesSeleccionadas!=None:
	    haySeleccionEnLista=True
	else:
	    haySeleccionEnLista=False

	if lucesSeleccionadas != None:
		camposAtributos       = { "on_off":0, "aiExposure":0 , "aiRadius":0, "aiColorTemperature":0, "color":0, "intensity":0, "aiAngle":0, "aiSamples":0,"emitDiffuse":0,"emitSpecular":0,"coneAngle":0 ,"penumbraAngle":0 ,"dropoff":0 , "aiShadowDensity":0 }
		camposAtributosV      = { "on_off":0, "aiExposure":0 , "aiRadius":0, "aiColorTemperature":0, "color":None, "intensity":0, "aiAngle":0, "aiSamples":0,"emitDiffuse":0,"emitSpecular":0 ,"coneAngle":0  ,"penumbraAngle":0 ,"dropoff":0 , "aiShadowDensity":0 }
		camposAtributosDif    = { "on_off":0, "aiExposure":0 , "aiRadius":0, "aiColorTemperature":0, "color":0, "intensity":0, "aiAngle":0, "aiSamples":0,"emitDiffuse":0,"emitSpecular":0 , "coneAngle":0  ,"penumbraAngle":0 ,"dropoff":0 , "aiShadowDensity":0 }
		# hide / unhide
		for luz in lucesSeleccionadas: #VALORES
			if qVisibilidadAbsoluta(luz):
				camposAtributosV["on_off"] = qVisibilidadAbsoluta(luz)

		for luz in lucesSeleccionadas: # TIENEN EL MISMO VALOR TODOS?
			if qVisibilidadAbsoluta(luz) != camposAtributosV["on_off"] :
				camposAtributosDif["on_off"]=1


		# todos los atts menos el hide / unhide
		for luz in lucesSeleccionadas:
			for key in camposAtributos.keys(): # CAPTURO VALORES
				if (cmds.attributeQuery (key , node=luz+"SH" , ex=1)):
					camposAtributosV[key]=cmds.getAttr ( luz+"SH."+key )
			for key in camposAtributos.keys(): # TIENEN EL ATRIBUTO TODOS?
				if (cmds.attributeQuery (key , node=luz+"SH" , ex=1)):
					camposAtributos[key] += 1
		for luz in lucesSeleccionadas:
			for key in camposAtributos.keys(): # TIENEN EL MISMO VALOR TODOS?
				if (cmds.attributeQuery (key , node=luz+"SH" , ex=1)):
					if cmds.getAttr ( luz+"SH."+key ) != camposAtributosV[key]:
						camposAtributosDif[key]=1
		# VALORES
		for campo in camposAtributosV.keys():
			if camposAtributos[campo] == len (lucesSeleccionadas) and camposAtributosDif[campo]!=1:
				try:
					cmds.floatField ( campo , e=1 , v = camposAtributosV[campo] )
				except:
					pass
				try:
					cmds.checkBox ( campo , e=1 , v = camposAtributosV[campo] )
				except:
					pass
				if campo=="color" :
					try:
						cmds.colorSliderGrp( campo , e=1 , rgbValue = camposAtributosV[campo][0] )
					except:
						pass
	    # PINTAR BEIGE
		for campo in camposAtributos.keys():
			if camposAtributosDif [campo] ==0 and len(lucesSeleccionadas)==camposAtributos[campo]: #tienen valores iguales
				try:
					cmds.floatField ( campo , e=1 , en=1 , bgc=[0.3,0.3,0.3])
				except:
					pass
				try:
					cmds.checkBox ( campo , e=1 , en=1  , bgc=[0.3,0.3,0.3] )
				except:
					pass
				try:
					cmds.colorSliderGrp( campo , e = 1 , en = 1  , ebg=0)
				except:
					pass
			elif camposAtributosDif [campo] !=0 and len(lucesSeleccionadas)== camposAtributos[campo]:#tienen valores diferentes
				try:
					cmds.floatField ( campo , e=1 , en=1, bgc=[0.863,0.808,0.529] )
				except:
					pass
				try:
					cmds.checkBox ( campo , e=1 ,  en=1 , bgc=[0.863,0.808,0.529])
				except:
					pass
				if campo=="color" :
					cmds.colorSliderGrp( campo , e=1 , en=1  , bgc = [0.863,0.808,0.529])

		maxmin()
		enableCampos(camposAtributos)
		if camposAtributosDif ["on_off"] ==0 : #tienen valores iguales
			try:
				cmds.checkBox ( "on_off" , e=1 , en=1  , v=camposAtributosV["on_off"] ,  bgc=[0.3,0.3,0.3] )
			except:
				pass
		elif camposAtributosDif ["on_off"] !=0 :#tienen valores diferentes
			try:
				cmds.checkBox ( "on_off" , e=1 ,  en=1 , bgc=[0.863,0.808,0.529])
			except:
				pass
		dropListas()
		boldOblique()
		enableDropParent()
		enableTempColor ()
		enableAbsRel()
		#cmds.window(win, e=1 , resizeToFitChildren=1)

def enableAbsRel(*args):
    global abs
    global rel
    global haySeleccionEnLista
    if haySeleccionEnLista:
        cmds.radioButton( abs,e=1,en=1 )
        cmds.radioButton( rel,e=1,en=1 )

def deseleccionar(*args):
    global abs
    global rel
    cmds.textScrollList ('listaLuces1' , e=1  ,da=1)
    cmds.textScrollList ('listaLuces2' , e=1  ,da=1)
    cmds.textScrollList ('listaLuces3' , e=1  ,da=1)
    cmds.select(cl=True)
    cmds.radioButton( abs,e=1,en=0 )
    cmds.radioButton( rel,e=1,en=0 )
    enableDropParent()
    cmds.warning('AHORA PODES EDITAR LOS GRUPOS.')
    refreshui()

def enableDropParent():
	global grupoCParent
	global grupo_borrar
	global grupo_renombrar
	if cmds.textScrollList('listaLuces1',q=1,si=1)==None:
		cmds.optionMenu (grupoCParent,e=1,en=1,ann="ACA ELEGIS EL PARENT DEL GRUPO ELEGIDO A LA IZQUIERDA.")
		cmds.iconTextButton(grupo_borrar,e=1,en=1)
		cmds.iconTextButton(grupo_renombrar,e=1,en=1)
	else:
		cmds.optionMenu (grupoCParent,e=1,en=0,ann="DESELECCIONA LAS LUCES DE LA LISTA PARA HABILITAR ESTA OPCION.")
		cmds.iconTextButton(grupo_borrar,e=1,en=0)
		cmds.iconTextButton(grupo_renombrar,e=1,en=0)

def boldOblique():
	luces = cmds.textScrollList('listaLuces1' ,q=1, ai=1)
	seleccionLista1 = cmds.textScrollList ("listaLuces1",q=1,sii=1)

	if luces!=None:
		for luz in luces:
			cmds.textScrollList ("listaLuces1",e=1,da=1)
			cmds.textScrollList ("listaLuces2",e=1,da=1)
			cmds.textScrollList ("listaLuces3",e=1,da=1)
			if qVisibilidadAbsoluta(luz) and cmds.referenceQuery( luz ,isNodeReferenced=1 )==True: #referenciada y activa
				cmds.textScrollList ("listaLuces1",e=1,si=luz)
				index= cmds.textScrollList ("listaLuces1",q=1,sii=1)[0]
				cmds.textScrollList ("listaLuces1", e=1, lf=[index,"smallObliqueLabelFont"])
				cmds.textScrollList ("listaLuces2", e=1, lf=[index,"smallObliqueLabelFont"])
				cmds.textScrollList ("listaLuces3", e=1, lf=[index,"smallObliqueLabelFont"])
			elif qVisibilidadAbsoluta(luz)==False and cmds.referenceQuery( luz ,isNodeReferenced=1 )==True: #referenciada e inactiva
				cmds.textScrollList ("listaLuces1",e=1,si=luz)
				index= cmds.textScrollList ("listaLuces1",q=1,sii=1)[0]
				cmds.textScrollList ("listaLuces1", e=1, lf=[index,"tinyBoldLabelFont"])
				cmds.textScrollList ("listaLuces2", e=1, lf=[index,"tinyBoldLabelFont"])
				cmds.textScrollList ("listaLuces3", e=1, lf=[index,"tinyBoldLabelFont"])
			elif qVisibilidadAbsoluta(luz)==False and cmds.referenceQuery( luz ,isNodeReferenced=1 )==False: #referenciada e inactiva
				cmds.textScrollList ("listaLuces1",e=1,si=luz)
				index= cmds.textScrollList ("listaLuces1",q=1,sii=1)[0]
				cmds.textScrollList ("listaLuces1", e=1, lf=[index,"boldLabelFont"])
				cmds.textScrollList ("listaLuces2", e=1, lf=[index,"boldLabelFont"])
				cmds.textScrollList ("listaLuces3", e=1, lf=[index,"boldLabelFont"])
			elif qVisibilidadAbsoluta(luz)==True and cmds.referenceQuery( luz ,isNodeReferenced=1 )==False: #referenciada e inactiva
				cmds.textScrollList ("listaLuces1",e=1,si=luz)
				index= cmds.textScrollList ("listaLuces1",q=1,sii=1)[0]
				cmds.textScrollList ("listaLuces1", e=1, lf=[index,"plainLabelFont"])
				cmds.textScrollList ("listaLuces2", e=1, lf=[index,"plainLabelFont"])
				cmds.textScrollList ("listaLuces3", e=1, lf=[index,"plainLabelFont"])
			cmds.textScrollList ("listaLuces1",e=1,da=1)
			cmds.textScrollList ("listaLuces2",e=1,da=1)
			cmds.textScrollList ("listaLuces3",e=1,da=1)
	try:
		cmds.textScrollList ("listaLuces1",e=1,sii=seleccionLista1)
		cmds.textScrollList ("listaLuces2",e=1,sii=seleccionLista1)
		cmds.textScrollList ("listaLuces3",e=1,sii=seleccionLista1)
	except:
		pass

def enableCampos(camposAtributos={}):
	# HABILITAR DESHABILITAR
	lucesSeleccionadas=cmds.textScrollList ('listaLuces1',q=1,si=1)
	if len(lucesSeleccionadas)!=0:
		for campo in camposAtributos.keys():
			if camposAtributos[campo] != len(lucesSeleccionadas) and camposAtributos!="aiColorTemperature":
				try:
					cmds.floatField ( campo , e=1 , en=0)
				except:
					pass
				try:
					cmds.checkBox ( campo , e=1  , en=0 )
				except:
					pass
				if campo=="color":
					try:
						cmds.colorSliderGrp( campo , e=1 , en=0 )
					except:
						pass
			else:
				try:
					cmds.floatField ( campo , e=1 , en=1)
				except:
					pass
				try:
					cmds.checkBox ( campo , e=1  , en=1 )
				except:
					pass
				if campo=="color":
					try:
						cmds.colorSliderGrp( campo , e=1 , en=1 )
					except:
						pass

def enableTempColor (*args):
	lucesSeleccionadas = cmds.textScrollList ('listaLuces1',q=1,si=1)
	tienenTempColorOn=[]
	tienenTempColorOff=[]
	if lucesSeleccionadas!=None:
		for l in lucesSeleccionadas:
			if cmds.getAttr( l+"SH.aiUseColorTemperature")==0:
				tienenTempColorOff.append(l)
			elif cmds.getAttr( l+"SH.aiUseColorTemperature")==1:
				tienenTempColorOn.append(l)

		if len(tienenTempColorOn) == len(lucesSeleccionadas) :
			cmds.floatField ("aiColorTemperature" , e=1 , en=1 )
		elif len(tienenTempColorOff) == len(lucesSeleccionadas) :
			cmds.floatField ("aiColorTemperature" , e=1 , en=0 , v=0 , bgc=[0.1,0.1,0.1])
		elif tienenTempColorOff==[] and tienenTempColorOn==[] and lucesSeleccionadas==None:
			cmds.floatField ("aiColorTemperature" , e=1 , en=0 , v=0 , bgc=[0.1,0.1,0.1])

		else:
			cmds.floatField ("aiColorTemperature" , e=1 , en=1)

		cmds.iconTextButton('b_masCalido',e=1 , en=1)
		cmds.iconTextButton('b_masFrio',  e=1 , en=1)
	else:
		cmds.iconTextButton('b_masCalido',e=1 , en=0)
		cmds.iconTextButton('b_masFrio',  e=1 , en=0)








def maxmin():
	#variables
	lucesSeleccionadas = cmds.textScrollList('listaLuces1' ,q=1, si=1)
	camposAtributosMin   = {"aiExposure":0 , "aiRadius":0, "intensity":0, "aiAngle":0, "aiSamples":0, "aiColorTemperature":0, "aiShadowDensity":0 }
	camposAtributosMax   = {"aiExposure":0 , "aiRadius":0, "intensity":0, "aiAngle":0, "aiSamples":0, "aiColorTemperature":0, "aiShadowDensity":0  }
	for luz in lucesSeleccionadas:
		for key in camposAtributosMin.keys(): # CAPTURO VALORES
			if (cmds.attributeQuery (key , node=luz+"SH" , ex=1)):
				camposAtributosMin[key]= [luz, cmds.getAttr ( luz+"SH."+key ) ]
				camposAtributosMax[key]= [luz, cmds.getAttr ( luz+"SH."+key ) ]
	for luz in lucesSeleccionadas:
		for key in camposAtributosMin.keys():
			if (cmds.attributeQuery ( key , node = luz+"SH" , ex=1)):
				try:
					if cmds.getAttr(luz+"."+key)<camposAtributosMin[key][1]:
						camposAtributosMin[key][1]=cmds.getAttr(luz+"."+key)
						camposAtributosMin[key][0]=luz
				except:
					pass
	for luz in lucesSeleccionadas:
		for key in camposAtributosMax.keys():
			if (cmds.attributeQuery ( key , node = luz+"SH" , ex=1)):
				try:
					if cmds.getAttr(luz+"."+key)>camposAtributosMax[key][1]:
						camposAtributosMax[key][1]=cmds.getAttr(luz+"."+key)
						camposAtributosMax[key][0]=luz
				except:
					pass
	if len(lucesSeleccionadas)>1 :
		for campo in camposAtributosMin.keys():
			try:
				cmds.floatField (campo  , e=1 , ann= "MIN: " + camposAtributosMin[campo][0]+"  "+ str(camposAtributosMin[campo][1]) +"\n"+"MAX: " + camposAtributosMax[campo][0]+ "  " + str(camposAtributosMax[campo][1])+"\n"+"PROMEDIO: "+ str( (camposAtributosMax[campo][1]- camposAtributosMin[campo][1])/2+camposAtributosMin[campo][1] ))
			except:
				pass
	else:
		cmds.floatField ('intensity'  , e=1 , ann= "")
		cmds.floatField ('aiExposure' , e=1 , ann= "")
		cmds.floatField ('aiRadius'   , e=1 , ann= "")
		cmds.floatField ('aiAngle'    , e=1 , ann= "")
		cmds.floatField ('aiSamples'  , e=1 , ann= "")
		cmds.floatField ('aiColorTemperature'  , e=1 , ann= "")




def mirarPorLuz(*args):
	try:
		cmds.lookThru(cmds.textScrollList ( 'listaLuces1' , q=1 , si=1 )[0] )
	except:
		pass

def setInt(*args):
    try:
        lucesSeleccionadas = cmds.textScrollList ('listaLuces1', q=1 , si=1)
        for luz in lucesSeleccionadas:
            try:
                if cmds.radioCollection('radioAbsRel',q=1,sl=1)=='A':
                    cmds.setAttr (luz+'SH.intensity', cmds.floatField ('intensity',q=1,v=1) )
                else:
                    cmds.setAttr (luz+'SH.intensity',  cmds.getAttr ( luz+'SH.intensity' ) +   cmds.floatField ('intensity',q=1,v=1) )
            except:
                pass
        cmds.textScrollList ('listaLuces1',e=1,si=lucesSeleccionadas)
    except:
        pass
    refreshui()

def setExp(*args):
    try:
        lucesSeleccionadas = cmds.textScrollList ('listaLuces1', q=1 , si=1)
        for luz in lucesSeleccionadas:
            try:
                if cmds.radioCollection('radioAbsRel',q=1,sl=1)=='A':
                    cmds.setAttr (luz+'SH.aiExposure', cmds.floatField ('aiExposure',q=1,v=1) )
                else:
                    cmds.setAttr (luz+'SH.aiExposure',  cmds.getAttr ( luz+'SH.aiExposure' ) +   cmds.floatField ('aiExposure',q=1,v=1) )
            except:
                pass
        cmds.textScrollList ('listaLuces1',e=1,si=lucesSeleccionadas)
    except:
        pass
    refreshui()

def setRad(*args):
    try:
        lucesSeleccionadas = cmds.textScrollList ('listaLuces1', q=1 , si=1)
        for luz in lucesSeleccionadas:
            try:
                if cmds.radioCollection('radioAbsRel',q=1,sl=1)=='A':
                    cmds.setAttr (luz+'SH.aiRadius', cmds.floatField ('aiRadius',q=1,v=1) )
                else:
                    cmds.setAttr (luz+'SH.aiRadius',  cmds.getAttr ( luz+'SH.aiRadius' ) +   cmds.floatField ('aiRadius',q=1,v=1) )
            except:
                pass
    except:
        pass
    refreshui()

def setAng(*args):
    try:
        lucesSeleccionadas = cmds.textScrollList ('listaLuces1', q=1 , si=1)
        for luz in lucesSeleccionadas:
            try:
                if cmds.radioCollection('radioAbsRel',q=1,sl=1)=='A':
                    cmds.setAttr (luz+'SH.aiAngle', cmds.floatField ('aiAngle',q=1,v=1) )
                else:
                    cmds.setAttr (luz+'SH.aiAngle',  cmds.getAttr ( luz+'SH.aiAngle' ) +   cmds.floatField ('aiAngle',q=1,v=1) )
            except:
                pass
    except:
        pass
    refreshui()

def setShadowDensity(*args):
    try:
        lucesSeleccionadas = cmds.textScrollList ('listaLuces1', q=1 , si=1)
        for luz in lucesSeleccionadas:
            try:
                if cmds.radioCollection('radioAbsRel',q=1,sl=1)=='A':
                    cmds.setAttr (luz+'SH.aiShadowDensity', cmds.floatField ('aiShadowDensity',q=1,v=1) )
                else:
                    cmds.setAttr (luz+'SH.aiShadowDensity',  cmds.getAttr ( luz+'SH.aiShadowDensity' ) +   cmds.floatField ('aiShadowDensity',q=1,v=1) )
            except:
                pass
    except:
        pass
    refreshui()


def setSamp(*args):
    try:
        lucesSeleccionadas = cmds.textScrollList ('listaLuces1', q=1 , si=1)
        for luz in lucesSeleccionadas:
            try:
                if cmds.radioCollection('radioAbsRel',q=1,sl=1)=='A':
                    cmds.setAttr (luz+'SH.aiSamples', cmds.floatField ('aiSamples',q=1,v=1) )
                else:
                    cmds.setAttr (luz+'SH.aiSamples',  cmds.getAttr ( luz+'SH.aiSamples' ) +   cmds.floatField ('aiSamples',q=1,v=1) )
            except:
                pass
    except:
        pass
    refreshui()

def setColor(*args):
	try:
		lucesSeleccionadas = cmds.textScrollList ('listaLuces1', q=1 , si=1)
		rgbSet=cmds.colorSliderGrp ('color',q=1,rgb=1)
		for luz in lucesSeleccionadas:
			try:
				cmds.setAttr (luz+".aiUseColorTemperature",0)
				cmds.setAttr (luz+'SH.color',rgbSet[0],rgbSet[1],rgbSet[2],type='double3' )
			except:
				pass
	except:
		pass
	refreshui()

def setTempColor(*args):
	try:
		lucesSeleccionadas = cmds.textScrollList ('listaLuces1', q=1 , si=1)
		for luz in lucesSeleccionadas:
			try:
				cmds.setAttr (luz+".aiUseColorTemperature",1)
				if cmds.radioCollection('radioAbsRel',q=1,sl=1)=='A':
					cmds.setAttr (luz+'SH.aiColorTemperature', cmds.floatField ('aiColorTemperature',q=1,v=1) )
				else:
					cmds.setAttr (luz+'SH.aiColorTemperature',  cmds.getAttr ( luz+'SH.aiColorTemperature' ) +   cmds.floatField ('aiColorTemperature',q=1,v=1) )
			except:
				pass
	except:
		pass
	refreshui()

def setilumDef(*args):
	cmds.warning ("-")

def setDif(*args):
    try:
        lucesSeleccionadas = cmds.textScrollList ('listaLuces1', q=1 , si=1)
        for luz in lucesSeleccionadas:
            try:
                cmds.setAttr (luz+'SH.emitDiffuse', cmds.checkBox ('emitDiffuse',q=1,v=1) )
            except:
                pass
    except:
        pass
    refreshui()

def setSpec(*args):
    try:
        lucesSeleccionadas = cmds.textScrollList ('listaLuces1', q=1 , si=1)
        for luz in lucesSeleccionadas:
            try:
                cmds.setAttr (luz+'SH.emitSpecular', cmds.checkBox ('emitSpecular',q=1,v=1) )
            except:
                pass
    except:
        pass
    refreshui()

def setconeangle(*args):
    try:
        lucesSeleccionadas = cmds.textScrollList ('listaLuces1', q=1 , si=1)
        for luz in lucesSeleccionadas:
            try:
                if cmds.radioCollection('radioAbsRel',q=1,sl=1)=='A':
                    cmds.setAttr (luz+'SH.coneAngle', cmds.floatField ('coneAngle',q=1,v=1) )
                else:
                    cmds.setAttr (luz+'SH.coneAngle',  cmds.getAttr ( luz+'SH.coneAngle' ) +   cmds.floatField ('coneAngle',q=1,v=1) )
            except:
                pass
    except:
        pass
    refreshui()

def setpenumbraAngle(*args):
	try:
	    lucesSeleccionadas = cmds.textScrollList ('listaLuces1', q=1 , si=1)
	    for luz in lucesSeleccionadas:
	        try:
	            if cmds.radioCollection('radioAbsRel',q=1,sl=1)=='A':
	                cmds.setAttr (luz+'SH.penumbraAngle', cmds.floatField ('penumbraAngle',q=1,v=1) )
	            else:
	                cmds.setAttr (luz+'SH.penumbraAngle',  cmds.getAttr ( luz+'SH.penumbraAngle' ) +   cmds.floatField ('penumbraAngle',q=1,v=1) )
	        except:
	            pass
	except:
	    pass
	refreshui()

def setdropoff(*args):
    try:
        lucesSeleccionadas = cmds.textScrollList ('listaLuces1', q=1 , si=1)
        for luz in lucesSeleccionadas:
            try:
                if cmds.radioCollection('radioAbsRel',q=1,sl=1)=='A':
                    cmds.setAttr (luz+'SH.dropoff', cmds.floatField ('dropoff',q=1,v=1) )
                else:
                    cmds.setAttr (luz+'SH.dropoff',  cmds.getAttr ( luz+'SH.dropoff' ) +   cmds.floatField ('dropoff',q=1,v=1) )
            except:
                pass
    except:
        pass
    refreshui()



def borrarSeleccion():
	try:
		lucesSeleccionadas = cmds.textScrollList ( 'listaLuces1' , q=1 , si=1 )
		for luz in lucesSeleccionadas:
			cmds.delete(luz)
		cmds.textScrollList ( 'listaLuces1' , e=1 , da=1 )
		ordenarLuz()
	except:
		pass

def ordenarLuz(seleccionar=1):
	global orden
	lucesTodas = cmds.ls(['*_LPNTSH','*_LDIRSH','*_LARESH','*_LAMBSH','*_LSPTSH'],r=1,lights = True)
	if len(lucesTodas)!=0:
		datosOrdenados =  ordenarDatos(ordenarPor='luz' , filtrado='')
		if orden["luz"]%2 == 1:
			datosOrdenados[0].reverse()
			datosOrdenados[1].reverse()
			datosOrdenados[2].reverse()
		listas = ['listaLuces1','listaLuces2','listaLuces3']
		seleccionar = cmds.textScrollList ('listaLuces1' , q=1 , si=1 )
		for lista in listas:
			cmds.textScrollList (lista, e=1 ,ra=1)
		cmds.textScrollList ('listaLuces1' , e=1  ,  a=datosOrdenados[0] , numberOfRows = len(datosOrdenados[0])+2 , si=seleccionar)
		cmds.textScrollList ('listaLuces2' , e=1  ,  a=datosOrdenados[1] , numberOfRows = len(datosOrdenados[0])+2)
		cmds.textScrollList ('listaLuces3' , e=1  ,  a=datosOrdenados[2] , numberOfRows = len(datosOrdenados[0])+2)
		orden["luz"] +=1
		boldOblique()
		cmds.textScrollList ('listaLuces1' , e=1  ,  da=1)
		cmds.textScrollList ('listaLuces1' , e=1 , si=seleccionar )
		cmds.textScrollList ('listaLuces2' , e=1  ,  da=1)
		try:
			cmds.textScrollList ('listaLuces2' , e=1  ,  sii= cmds.textScrollList ('listaLuces1' , q=1 , sii=1 ))
			cmds.textScrollList ('listaLuces3' , e=1  ,  da=1)
			cmds.textScrollList ('listaLuces3' , e=1  ,  sii= cmds.textScrollList ('listaLuces1' , q=1 , sii=1 ))
		except:
			pass
	else:
		cmds.textScrollList('listaLuces1',e=1,ra=1)
		cmds.textScrollList('listaLuces2',e=1,ra=1)
		cmds.textScrollList('listaLuces3',e=1,ra=1)
		cmds.warning ("---- NO SE DETECTARON LUCES ADMITIDAS ----")

def ordenarTipo2(*args):
	global orden
	lucesShapes=[]
	tipos_de_Luces=[]
	filtro_tipos=[]
	tipo_de_Luz=""
	lucesTodas = cmds.ls(['*_LPNTSH','*_LDIRSH','*_LARESH','*_LAMBSH','*_LSPTSH'],r=1,lights = True)
	try:
		items= cmds.textScrollList ('listaLuces1' , q=1, allItems=1) #items en la lista
		seleccionar = cmds.textScrollList ('listaLuces1' , q=1 , si=1 ) # seleccion de la lista
	except:
		seleccionar=1
		pass
	if len(lucesTodas)!=0:
		if len(items)!=0:
			for item in items:
				tipo_de_Luz=  cmds.nodeType( cmds.listRelatives(item,type='light')[0] )
				tipos_de_Luces.append (tipo_de_Luz)
			if "spotLight" in tipos_de_Luces:
				filtro_tipos.append("*_LSPTSH")
			if "pointLight" in tipos_de_Luces:
				filtro_tipos.append("*_LPNTSH")
			if "areaLight" in tipos_de_Luces:
				filtro_tipos.append("*_LARESH")
			if "directionalLight" in tipos_de_Luces:
				filtro_tipos.append("*_LDIRSH")
			datosOrdenados = ordenarDatos(ordenarPor='tipo', filtrado=filtro_tipos )
			listas = ['listaLuces1','listaLuces2','listaLuces3']
			if orden["tipo"]%2 == 1:
				datosOrdenados[0].reverse()
				datosOrdenados[1].reverse()
				datosOrdenados[2].reverse()
			for lista in listas:
				cmds.textScrollList (lista, e=1 ,ra=1)
			cmds.textScrollList ('listaLuces1' , e=1  ,  a= datosOrdenados[0] , numberOfRows = len(datosOrdenados[0])+2, si=seleccionar)
			indiceSeleccionLista1 = cmds.textScrollList ('listaLuces1' , q=1 , sii=1 )
			cmds.textScrollList ('listaLuces2' , e=1  ,  a=datosOrdenados[1] , numberOfRows = len(datosOrdenados[0])+2, sii=indiceSeleccionLista1)
			cmds.textScrollList ('listaLuces3' , e=1  ,  a=datosOrdenados[2] , numberOfRows = len(datosOrdenados[0])+2, sii=indiceSeleccionLista1)
			boldOblique()
			cmds.textScrollList ('listaLuces1' , e=1  ,  da=1)
			cmds.textScrollList ('listaLuces1' , e=1 , si=seleccionar )
			cmds.textScrollList ('listaLuces2' , e=1  ,  da=1)
			cmds.textScrollList ('listaLuces2' , e=1  ,  sii= cmds.textScrollList ('listaLuces1' , q=1 , sii=1 ))
			cmds.textScrollList ('listaLuces3' , e=1  ,  da=1)
			cmds.textScrollList ('listaLuces3' , e=1  ,  sii= cmds.textScrollList ('listaLuces1' , q=1 , sii=1 ))
			orden["tipo"]+=1
			ultimoOrden="tipo"
	else:
		cmds.textScrollList('listaLuces1',e=1,ra=1)
		cmds.textScrollList('listaLuces2',e=1,ra=1)
		cmds.textScrollList('listaLuces3',e=1,ra=1)
		cmds.warning ("---- NO SE DETECTARON LUCES ADMITIDAS ----")

def ordenarGrupo(seleccionar=1):
	global orden
	lucesTodas = cmds.ls(['*_LPNTSH','*_LDIRSH','*_LARESH','*_LAMBSH','*_LSPTSH'],r=1,lights = True)
	if len(lucesTodas)!=0:
		datosOrdenados = ordenarDatos(ordenarPor='grupo', filtrado='' )
		listas = ['listaLuces1','listaLuces2','listaLuces3']
		if orden["grupo"]%2 == 1:
			datosOrdenados[0].reverse()
			datosOrdenados[1].reverse()
			datosOrdenados[2].reverse()
		try:
			seleccionar = cmds.textScrollList ('listaLuces1' , q=1 , si=1 )
		except:
			pass
		for lista in listas:
			cmds.textScrollList (lista, e=1 ,ra=1)
		cmds.textScrollList ('listaLuces1' , e=1  ,  a= datosOrdenados[0] , numberOfRows = len(datosOrdenados[0])+2, si=seleccionar)
		indiceSeleccionLista1 = cmds.textScrollList ('listaLuces1' , q=1 , sii=1 )
		cmds.textScrollList ('listaLuces2' , e=1  ,  a=datosOrdenados[1] , numberOfRows = len(datosOrdenados[0])+2, sii=indiceSeleccionLista1)
		cmds.textScrollList ('listaLuces3' , e=1  ,  a=datosOrdenados[2] , numberOfRows = len(datosOrdenados[0])+2, sii=indiceSeleccionLista1)
		boldOblique()
		cmds.textScrollList ('listaLuces1' , e=1  ,  da=1)
		cmds.textScrollList ('listaLuces1' , e=1 , si=seleccionar )
		cmds.textScrollList ('listaLuces2' , e=1  ,  da=1)
		cmds.textScrollList ('listaLuces2' , e=1  ,  sii= cmds.textScrollList ('listaLuces1' , q=1 , sii=1 ))
		cmds.textScrollList ('listaLuces3' , e=1  ,  da=1)
		cmds.textScrollList ('listaLuces3' , e=1  ,  sii= cmds.textScrollList ('listaLuces1' , q=1 , sii=1 ))
		orden["grupo"]+=1
		ultimoOrden="grupo"
	else:
		cmds.textScrollList('listaLuces1',e=1,ra=1)
		cmds.textScrollList('listaLuces2',e=1,ra=1)
		cmds.textScrollList('listaLuces3',e=1,ra=1)
		cmds.warning ("---- NO SE DETECTARON LUCES ADMITIDAS ----")

def cambiarGrupo(grupoParaMoverA=""):
    global seleccionLista1
    global orden
    seleccion1=cmds.textScrollList('listaLuces1',q=1,si=1)
    seleccion2=cmds.textScrollList('listaLuces2',q=1,si=1)
    lucesSeleccionadas = cmds.textScrollList('listaLuces1',q=1,si=1)
    if lucesSeleccionadas !=None:
        if len(cmds.textScrollList('listaLuces1',q=1,si=1))!=0:
            lucesSeleccionadas = cmds.textScrollList('listaLuces1' ,q=1, si=1)
            lucesSeleccionadasInd = cmds.textScrollList('listaLuces1' ,q=1, sii=1)
            if grupoParaMoverA=="":
                grupoSeleccionado = cmds.optionMenu ( (grupoVG +'|OptionMenu')  , q=1 , value=1)
            else:
                grupoSeleccionado = grupoParaMoverA[:-5]

            if "_LGRP" in grupoParaMoverA:
                for luz in lucesSeleccionadas:
                    try:
                        cmds.parent ( luz ,grupoParaMoverA )
                    except:
                        pass
                refrescar()
            else:
                for luz in lucesSeleccionadas:
                    try:
                        if cmds.listRelatives ( luz ,p=1 )[0]!= grupoParaMoverA+'_LGRP':
                            cmds.parent ( luz ,grupoParaMoverA  + '_LGRP' )
                    except:
                        pass
            seleccion3=cmds.textScrollList('listaLuces3',q=1,si=1)
            cmds.textScrollList('listaLuces1',e=1,si=seleccion1)
            cmds.textScrollList('listaLuces2',e=1,si=seleccion2)
            cmds.textScrollList('listaLuces3',e=1,si=seleccion3)
            ordenarLuz()
            refreshui()


    else:
        cmds.warning(' - - - AHORA PODES EDITAR LOS GRUPOS - - - ')


def crearGrupo(*args):
	global ultimoGrupoCreadoPorUsuario
	global seleccionLista1
	global grupoVG
	global dock
	seleccionLista1 = cmds.textScrollList ('listaLuces1',q=1,si=1)

	pideNombreGrupo = 'OK'
	arrancaConNumero=1
	rootDeEscena = ""
	roots = cmds.ls('ROOT_*_LGRP',r=1)
	listaDeRootsNoReferenciados=[]
	if len( roots ) == 1:
		rootDeEscena = roots [0]
	elif len( roots ) > 1:
		for root in roots:
			if cmds.referenceQuery( root ,isNodeReferenced=1 ) == False:
				listaDeRootsNoReferenciados.append (root)
	else:
		rootDeEscena = ""
	if rootDeEscena != "" or len(listaDeRootsNoReferenciados)==1:
		while pideNombreGrupo=='OK' and arrancaConNumero==1:
			pideNombreGrupo = cmds.promptDialog(title='NOMBRAR',message='NOMBRE DE GRUPO:',button=['OK', 'CANCELAR'],defaultButton='OK',cancelButton='CANCELAR',dismissString='Cancel')
			if cmds.promptDialog(query=True, text=True)!="" and pideNombreGrupo != "CANCELAR":
				if pideNombreGrupo == 'OK' and str(cmds.promptDialog(query=True, text=True))[0].isdigit()==False:
				    if not cmds.objExists( cmds.promptDialog(query=True, text=True) ):
				        arrancaConNumero=0
				        qNombreGrupo = cmds.promptDialog(query=True, text=True)
				        nombreDelGrupoCreado=cmds.group(name = qNombreGrupo.upper() + '_LGRP', em=True, w=True)
				        cmds.parent ( qNombreGrupo.upper() + '_LGRP' , cmds.ls('ROOT_*_LGRP')[0] )
				        rootAts = cmds.listAttr (qNombreGrupo.upper() + '_LGRP' , k=1 )
				        for at in rootAts:
				            if at != "visibility":
				                cmds.setAttr (qNombreGrupo.upper() + '_LGRP'+"."+at,lock=1,k=0,channelBox=0)
				            else:
				                cmds.setAttr (qNombreGrupo.upper() + '_LGRP'+"."+at,lock=0,k=0,channelBox=1)
				        #ACTUALIZO GRUPOS
				        clearOptionMenu (grupoVG)
				        gruposDeLuces = cmds.ls ( '*_LGRP' , type='transform' )
				        rootDeLaEscena= cmds.ls ( 'ROOT_*_LGRP' , type='transform' )
				        for grp in gruposDeLuces:
				            if grp != rootDeLaEscena[0]:
				                cmds.menuItem(parent=( dock +  grupoVG.split("winMLuces")[1] ), label=grp[:-5] ) #########################
				        clearOptionMenu (grupoCParent)
				        gruposDeLuces = cmds.ls ( '*_LGRP' , type='transform' )
				        for grp in gruposDeLuces:
				            if grp != rootDeLaEscena[0]:
				                cmds.menuItem ( parent= dock +  grupoCParent.split("winMLuces")[1] , label=grp[:-5] )
        				else:
        				    cmds.warning (" - - - YA EXISTE UN GRUPO CON ESE NOMBRE. - - - ")
        			elif pideNombreGrupo == 'OK' and str(cmds.promptDialog(query=True, text=True))[0].isdigit()==True:
        			    cmds.warning ( " - - - EL NOMBRE NO PUEDE COMENZAR CON UN NUMERO. - - - " )
        			else:
        			    cmds.warning ( " - - - USUARIO CANCELA - - - " )
        			    return ""
            	else:
            		cmds.warning (" - - - CANCELADO - - - ")
            		return ""
        	if pideNombreGrupo=='OK':
        	    ultimoGrupoCreadoPorUsuario=nombreDelGrupoCreado
        	    cambiarGrupo(grupoParaMoverA=nombreDelGrupoCreado)
        	    return nombreDelGrupoCreado
	else:
	    cmds.warning ("NO HAY UN ROOT UNICO.")

def refrescar(*args):
	seleccionEnLaEscena = cmds.ls(sl=1)
	cmds.textScrollList ('listaLuces1',e=1,da=1)
	for o in seleccionEnLaEscena:
		try:
			cmds.textScrollList ('listaLuces1',e=1,si=o)
		except:
			pass
	ordenarLuz()
	refreshui()

def tipoSel():
	cmds.textScrollList ('listaLuces2',e=1,si= cmds.textScrollList ('listaLuces2',q=1,si=1  ) )
	cmds.textScrollList ('listaLuces1',e=1,sii=cmds.textScrollList ('listaLuces2',q=1,sii=1  ) )
	cmds.textScrollList ('listaLuces3',e=1,sii=cmds.textScrollList ('listaLuces2',q=1,sii=1  ) )

def grpSel():
	cmds.textScrollList ('listaLuces3',e=1,si= cmds.textScrollList ('listaLuces3',q=1,si=1  ) )
	cmds.textScrollList ('listaLuces1',e=1,sii=cmds.textScrollList ('listaLuces3',q=1,sii=1  ) )
	cmds.textScrollList ('listaLuces2',e=1,sii=cmds.textScrollList ('listaLuces3',q=1,sii=1  ) )

def construirScrollsConBotones( emparentarA='') :
	# ordenarPor puede ser 'luz' o 'tipo'.
	# emparentarA es el string del layout al que se quiere emparentar.
	lightList = cmds.ls(['*_LPNTSH','*_LDIRSH','*_LARESH','*_LAMBSH','*_LSPTSH'],r=1,lights = True)
	dicLuces={}
	for l in lightList:
		name = cmds.listRelatives(l,type='transform',p=True)[0]
		grupo = cmds.listRelatives(name,type='transform',p=True)[0]
		lightType = cmds.nodeType(l)
		dicLuces[name]= [lightType,l,grupo]
	r_00 = cmds.rowLayout ('r_00', nc = 5 , p = 'row1' ,bgc=(0.27,0.27,0.27), h = 30 , cw5= [ 50 , 250 , 85 , 100 , 25 ] , ct5= ["both", "both", "both", "both" , "both"])
	cmds.iconTextButton  (ann='REFRESCAR GUI',  style='iconOnly',image1='refresh.png', c = refrescar ,width=15,height=20,p=r_00 )

	#cmds.button ( l = 'LUZ' ,   align = "center" ,  bgc=[0.3,0.3,0.3],c = ordenarLuz   , p = r_00 )
	#cmds.button ( l = 'TIPO' ,  align = "center" ,  bgc=[0.3,0.3,0.3],c = ordenarTipo2  , p = r_00 )
	#cmds.button ( l = 'GRUPO' , align = "center" ,  bgc=[0.3,0.3,0.3], c = ordenarGrupo ,  p = r_00 )

	cmds.iconTextButton  (l ='LUZ',ann='LUZ',style='textOnly',image1='M:\PH_SCRIPTS\ICONS\LSPT_1.png', c = ordenarLuz     ,p=r_00 ,bgc=(0.27,0.27,0.27) ,font= "plainLabelFont")
	cmds.iconTextButton (l ='TIPO',ann='TIPO',style='textOnly',image1='M:\PH_SCRIPTS\ICONS\LPNT_1.png', c = ordenarTipo2    ,p=r_00 ,bgc=(0.27,0.27,0.27) ,font= "plainLabelFont")
	cmds.iconTextButton  (l ='GRUPO',ann='GRUPO',style='textOnly',image1='M:\PH_SCRIPTS\ICONS\LARE_1.png', c = ordenarGrupo ,p=r_00 ,bgc=(0.27,0.27,0.27) ,font= "plainLabelFont")

	b_isolate = cmds.iconTextButton  ('b_isolate',ann='AISLAR LUZ', en=0, style='iconOnly',image1='M:\PH_SCRIPTS\ICONS\PH_LUCES_ISOLATE.png', c = aislarLuz ,width=15,height=25,p=r_00 )
	r_01 = cmds.rowLayout ( nc = 3 , cw3 = [ 305 , 80 , 100 ] ,  p = emparentarA )
	c_01 = cmds.columnLayout ('c_01', p = r_01 , adjustableColumn=1)
	c_02 = cmds.columnLayout (        p = r_01 , adjustableColumn=1)
	c_03 = cmds.columnLayout (        p = r_01 , adjustableColumn=1)
	cmds.textScrollList('listaLuces1' , w = 300 , allowMultiSelection=1, p = c_01 , deleteKeyCommand=borrarSeleccion)
	cmds.textScrollList('listaLuces2' , w = 100 , allowMultiSelection = 1 , p = c_02 , bgc = [0.24,0.24,0.24] , dcc=tipoSel ,deleteKeyCommand=borrarSeleccion )
	cmds.textScrollList('listaLuces3' , w = 100 , allowMultiSelection = 1 , p = c_03 , bgc = [0.24,0.24,0.24] , dcc=grpSel ,deleteKeyCommand=borrarSeleccion)
	datosOrdenados = ordenarDatos(ordenarPor='luz' , filtrado='')
	cmds.textScrollList ('listaLuces1' , e=1 ,allowMultiSelection=1, a=datosOrdenados[0] , sc=partial(refreshui,'luz') ,  enable=1 ,h = (len(datosOrdenados[0])+2)*100)
	cmds.textScrollList ('listaLuces2' , e=1 ,allowMultiSelection=1, a=datosOrdenados[1] , sc=partial(refreshui,'tipo')  , enable=1 , h = (len(datosOrdenados[0])+2)*100 )
	cmds.textScrollList ('listaLuces3' , e=1 ,allowMultiSelection=1, a=datosOrdenados[2] , sc=partial(refreshui,'grupo')   , enable=1 ,h = (len(datosOrdenados[0])+2)*100 )
	cmds.textField ( 'buscador' , e=1 , aie= 1 , changeCommand = buscar,  pht="Buscar luces" )
	boldOblique()

def buscar(*args):
	global buscarPor_Grupo_Luz
	recolectorBusqueda=[]
	try:
		textoBuscador = cmds.textField ( 'buscador' , q=1 , text=True)
		if len(textoBuscador)!=0:
			if buscarPor_Grupo_Luz=='luz':
				if str(textoBuscador[0]).isdigit() ==1:
					recolectorBusqueda= cmds.ls("*"+textoBuscador,"*"+textoBuscador+"*", type='light')
				else:
					recolectorBusqueda= cmds.ls(textoBuscador+"*","*"+textoBuscador,"*"+textoBuscador+"*",textoBuscador , textoBuscador.upper()+"*","*"+textoBuscador.upper(),"*"+textoBuscador.upper()+"*",textoBuscador.upper() , type='light')
			elif buscarPor_Grupo_Luz=='grupo':
				if str(textoBuscador[0]).isdigit() ==1:
					gruposRecolectados= cmds.ls("*"+textoBuscador,"*"+textoBuscador+"*", type='transform')
					gruposRecolectados=list(set(gruposRecolectados))
				else:
					gruposRecolectados= cmds.ls(textoBuscador+"*","*"+textoBuscador,"*"+textoBuscador+"*",textoBuscador , textoBuscador.upper()+"*","*"+textoBuscador.upper(),"*"+textoBuscador.upper()+"*",textoBuscador.upper() , type='transform')
					gruposRecolectados=list(set(gruposRecolectados))
					for trf in gruposRecolectados:
						if 'ROOT' in trf:
							gruposRecolectados.remove(trf)
					luces = cmds.ls(type='light')
					for l in luces:
						if cmds.listRelatives(cmds.listRelatives(l,p=1)[0] ,p=1)[0]  in gruposRecolectados:
							recolectorBusqueda.append (l)

			recolectorBusqueda=list(set(recolectorBusqueda))
			datos_Dic={}
			for l in recolectorBusqueda:
				name = cmds.listRelatives(l,type='transform',p=True)[0]
				grupo = cmds.listRelatives(name,type='transform',p=True)[0]
				lightType = cmds.nodeType(l)
				datos_Dic[name] = [lightType,l,grupo]

			lucesOrdenadas_=[]
			tiposOrdenados_=[]
			gruposOrdenados_=[]
			lucesTuplas=[]
			lucesTuplas = sorted(datos_Dic.items(), key=itemgetter(0))

			for tupla in lucesTuplas:
				lucesOrdenadas_.append (tupla[0])
				tiposOrdenados_.append (tupla[1][0])
				gruposOrdenados_.append (tupla[1][2][:-5])
			cmds.textScrollList ('listaLuces1' , e=1 , ra= 1)
			cmds.textScrollList ('listaLuces2' , e=1 , ra= 1)
			cmds.textScrollList ('listaLuces3' , e=1 , ra= 1)
			cmds.textScrollList ('listaLuces1' , e=1 , a= lucesOrdenadas_)
			cmds.textScrollList ('listaLuces2' , e=1 , a= tiposOrdenados_)
			cmds.textScrollList ('listaLuces3' , e=1 , a= gruposOrdenados_)
		else:
			refrescar()
	except:
		print " - - - NO SE HA PODIDO BUSCAR. REPORTAR ESTE ERROR - - - "

def onoff(*args):
	try:
		lucesSeleccionadas = cmds.textScrollList ('listaLuces1', q=1 , si=1)
		for luz in lucesSeleccionadas:
			if cmds.checkBox ('on_off',q=1,v=1):
				cmds.showHidden ( luz )
			else:
				cmds.hide ( luz )
	except:
	    pass
	refreshui()

def cambiarGrupoParent(*args):
	global grupoCParent
	global grupoVG
	if cmds.optionMenu (grupoVG,q=1,v=1)!=cmds.optionMenu (grupoCParent,q=1,v=1):
		try:
			cmds.parent (cmds.optionMenu (grupoVG,q=1,v=1)+"_LGRP",cmds.optionMenu (grupoCParent,q=1,v=1)+"_LGRP" )
		except:
			pass
	refreshui()

def borrarGrupo(*args):
	global grupoVG
	if cmds.optionMenu (grupoVG,q=1,v=1)!="":
		confirma=cmds.confirmDialog( title='BORRAR GRUPO', message='BORRAR '+cmds.optionMenu (grupoVG,q=1,v=1)+'?', button=['SI','NO'], defaultButton='SI', cancelButton='NO', dismissString='NO' )
		if confirma=="SI":
			cmds.delete (cmds.optionMenu (grupoVG,q=1,v=1)+'_LGRP')
		else:
			cmds.warning ("  ELIMINACION DE GRUPO CANCELADA  ")
	refreshui()

def renombrarGrupo(*args):
	global grupoVG
	grupoARenombrar = cmds.optionMenu (grupoVG,q=1,v=1)
	if cmds.optionMenu (grupoVG,q=1,v=1)!="":
		result = cmds.promptDialog(
				title='RENOMBRA '+cmds.optionMenu (grupoVG,q=1,v=1),
				message='Nuevo nombre:',
				button=['OK', 'Cancel'],text=cmds.optionMenu (grupoVG,q=1,v=1),
				defaultButton='OK',
				cancelButton='Cancel',
				dismissString='Cancel')
		if result == 'OK':
			if cmds.promptDialog(query=True, text=True)!="":
				nombreNuevoGrupo = cmds.promptDialog(query=True, text=True)
				if cmds.objExists(nombreNuevoGrupo+"_LGRP" )!=True:
					cmds.rename ( cmds.optionMenu(grupoVG, q=1 , v=1)+"_LGRP" , nombreNuevoGrupo.upper()+"_LGRP")
				else:
					cmds.warning("YA EXISTE UN GRUPO CON EL NOMBRE DADO.")
			else:
				cmds.warning("NOMBRE INVALIDO")
		else:
			cmds.warning("RENOMBRADO CANCELADO")
	ordenarGrupo()
	refreshui()

#myLightsOn=[]

def aislarLuz(*args):
	global isolate
	global myLights
	global myLightsOn
	global mySelection
	mySelection = cmds.textScrollList ('listaLuces1',q=1,si=1)
	if isolate == True:
		isolate = False
		cmds.iconTextButton  ('b_isolate' , e=1 , image1='M:\PH_SCRIPTS\ICONS\PH_LUCES_ISOLATE.png')
		for light in myLightsOn:
			cmds.showHidden( light , b = True)
		cmds.textScrollList ('listaLuces1',e=1,si=mySelection)
	else:
		isolate = True
		myLights = cmds.ls(type='light')
		myLightsOnShapes = cmds.ls(type='light', visible=True)
		for l in myLightsOnShapes:
			myLightsOn.append(cmds.listRelatives (l,p=1)[0])
		mySelection = cmds.ls (selection = True)

		cmds.iconTextButton  ('b_isolate' , e=1 , image1='M:\PH_SCRIPTS\ICONS\PH_LUCES_ISOLATE_ON.png')
		cmds.hide(myLights)
		cmds.showHidden( mySelection , a = True, b = True)

def sss(*args):
    global deactivateSSS
    verde= [0.3,1,0.3]
    rojo = [1,0.3,0.3]
    if deactivateSSS == True:
        deactivateSSS = False
        cmds.iconTextButton  ('b_sss' , e=1 , bgc=verde)
        cmds.setAttr ( 'defaultArnoldRenderOptions.ignoreSss', 0)
    else:
        deactivateSSS = True
        cmds.iconTextButton  ('b_sss' , e=1 , bgc=rojo)
        cmds.setAttr ( 'defaultArnoldRenderOptions.ignoreSss', 1)

def disp(*args):
    global deactivateDisplacement
    verde= [0.3,1,0.3]
    rojo = [1,0.3,0.3]
    if deactivateDisplacement == True:
        deactivateDisplacement = False
        cmds.iconTextButton  ('b_disp' , e=1 , bgc=verde)
        cmds.setAttr ( 'defaultArnoldRenderOptions.ignoreDisplacement', 0)
    else:
        deactivateDisplacement = True
        cmds.iconTextButton  ('b_disp' , e=1 , bgc=rojo)
        cmds.setAttr ( 'defaultArnoldRenderOptions.ignoreDisplacement', 1)

def sub(*args):
    global deactivateSUB
    verde= [0.3,1,0.3]
    rojo = [1,0.3,0.3]
    if deactivateSUB == True:
        deactivateSUB = False
        cmds.iconTextButton  ('b_sub' , e=1 , bgc=verde)
        cmds.setAttr ( 'defaultArnoldRenderOptions.ignoreSubdivision', 0)
    else:
        deactivateSUB = True
        cmds.iconTextButton  ('b_sub' , e=1 , bgc=rojo)
        cmds.setAttr ( 'defaultArnoldRenderOptions.ignoreSubdivision', 1)

def refreshOverride (*args):
	global deactivateSSS
	global deactivateDisplacement
	global deactivateSUB
	verde= [0.3,1,0.3]
	rojo = [1,0.3,0.3]
	if cmds.getAttr ('defaultArnoldRenderOptions.ignoreSss') == 0:
		cmds.iconTextButton  ('b_sss' , e=1  ,bgc= verde)
		deactivateSSS = False
	else:
		cmds.iconTextButton  ('b_sss' , e=1 , bgc= rojo)
		deactivateSSS = True

	if cmds.getAttr ('defaultArnoldRenderOptions.ignoreDisplacement') == 0:
		cmds.iconTextButton  ('b_disp' , e=1 , bgc=verde)
		deactivateDisplacement = False
	else:
		cmds.iconTextButton  ('b_disp' , e=1 , bgc=rojo)
		deactivateDisplacement = True

	if cmds.getAttr ('defaultArnoldRenderOptions.ignoreSubdivision') == 0:
		cmds.iconTextButton  ('b_sub' , e=1 , bgc=verde)
		deactivateSUB = False
	else:
		cmds.iconTextButton  ('b_sub' , e=1 , bgc=rojo)
		deactivateSUB = True

def asignarFiltro(*args):
	print "asignarFiltro"

def setBusquedaPorLuz(*args):
	global buscarPor_Grupo_Luz
	buscarPor_Grupo_Luz='luz'
	cmds.textField ( 'buscador' , e=1 , aie= 1 , changeCommand = buscar,  pht="Buscar luces" )

def setBusquedaPorGrupo(*args):
	global buscarPor_Grupo_Luz
	buscarPor_Grupo_Luz='grupo'
	cmds.textField ( 'buscador' , e=1 , aie= 1 , changeCommand = buscar,  pht="Buscar grupo" )

def copiarValorGet(control_,*args):
	global copiarValor
	copiarValor = cmds.floatField ( control_ ,q=1, v=1 )

def pegarValorGet(control_,*args):
	global copiarValor
	cmds.floatField ( control_ ,e=1, v=copiarValor )

def restaurarDefault (control_,*args):
	lucesSel = cmds.textScrollList ('listaLuces1' , q=1 , si=1)
	for l in lucesSel :
		valorDefault = cmds.attributeQuery( control_ , n=l+"SH",ld=1)[0]
		cmds.setAttr( l+"SH."+control_ , valorDefault)
		cmds.floatField ( control_ ,e=1, v=valorDefault )

def crearDropCopiarPegar (parent_=''):
	pop = cmds.popupMenu(p=parent_)
	cmds.menuItem(l="COPIAR VALOR"   , c = partial (copiarValorGet,parent_)   , p=pop)
	cmds.menuItem(l="PEGAR VALOR" , c = partial (pegarValorGet,parent_) ,p=pop)
	cmds.menuItem(l="RESTAURAR DEFAULT" , c = partial (restaurarDefault,parent_) ,p=pop)

def setTemperaturaColor (temperaturaColor ,*args):
	luces = cmds.textScrollList ('listaLuces1',q=1,si=1)
	try:
		for l in luces:
			cmds.setAttr (l+".aiUseColorTemperature",1)
			cmds.setAttr (l+'.aiColorTemperature',temperaturaColor)
			cmds.floatField('aiColorTemperature',e=1, v=temperaturaColor)
	except:
		print "HUBO PROBLEMAS AL AJUSTAR LA TEMPERATURA COLOR"
	refreshui()

def masFrio (*args):
	luces = cmds.textScrollList ('listaLuces1',q=1,si=1)
	temperaturaMas= cmds.floatField('aiColorTemperature',q=1, v=1  ) +100
	cmds.floatField('aiColorTemperature',e=1, v = temperaturaMas  )
	try:
		for l in luces:
			cmds.setAttr (l+"SH.aiUseColorTemperature",1)
			cmds.setAttr (l+'SH.aiColorTemperature',temperaturaMas)
	except:
		print "HUBO PROBLEMAS AL AJUSTAR LA TEMPERATURA COLOR"
	refreshui()

def masCalido (*args):
	luces = cmds.textScrollList ('listaLuces1',q=1,si=1)
	temperaturaMenos= cmds.floatField('aiColorTemperature',q=1, v=1  ) - 100
	cmds.floatField('aiColorTemperature',e=1, v = temperaturaMenos  )
	try:
		for l in luces:
			cmds.setAttr (l+"SH.aiUseColorTemperature",1)
			cmds.setAttr (l+'SH.aiColorTemperature',temperaturaMenos)
	except:
		print "HUBO PROBLEMAS AL AJUSTAR LA TEMPERATURA COLOR"
	refreshui()

def seleccionarTempColor(on=1,*args):

	luces = cmds.textScrollList ('listaLuces1',q=1,si=1)
	lucesConTempColor=[]
	if luces!=None:
		for l in luces:
			if cmds.getAttr (l+"SH.aiUseColorTemperature")==on:
				lucesConTempColor.append (l)
		cmds.textScrollList ('listaLuces1', e=1,da=1)
		cmds.textScrollList ('listaLuces2', e=1,da=1)
		cmds.textScrollList ('listaLuces3', e=1,da=1)
		cmds.textScrollList ('listaLuces1', e=1,si=lucesConTempColor)
		indexLista1 = cmds.textScrollList ('listaLuces1', q=1,sii=1)
		cmds.textScrollList ('listaLuces2', e=1,sii=indexLista1)
		cmds.textScrollList ('listaLuces3', e=1,sii=indexLista1)

def usarTcACtual(*args):
	luces = cmds.textScrollList ('listaLuces1',q=1,si=1)
	if luces != None:
		for l in luces:
			cmds.setAttr (l+"SH.aiUseColorTemperature",1)
	refreshui()

def crearPopTempColor (parent_,*args):
	popTempColor = cmds.popupMenu(p=parent_)
	cmds.menuItem(l="1K"  , p=popTempColor , c=partial (setTemperaturaColor, 1000) )
	cmds.menuItem(l="3K"  , p=popTempColor , c=partial (setTemperaturaColor, 3000) )
	cmds.menuItem(l="5K5 - NEUTRO " , p=popTempColor , c=partial (setTemperaturaColor, 5500) )
	cmds.menuItem(l="10K" , p=popTempColor , c=partial (setTemperaturaColor, 10000) )
	cmds.menuItem(l="15K" , p=popTempColor , c=partial (setTemperaturaColor, 15000) )
	cmds.menuItem (divider=1, p=popTempColor )
	cmds.menuItem(l="ACTIVAR EL USO DE TC" , p=popTempColor , c=usarTcACtual )

def lightListPanel():
	global dicLuces,orden,grupoVG,aiColorTemperatureSlider,grupoCParent,grupo_borrar,grupo_renombrar,buscarPor_Grupo_Luz,myLights,myLightsOnShapes,myLightsOn
	global isolate,vecesEjecutado,abs,rel,win,dockLuces
	global dock,placeHolder
	try:
		import UTILITIES
		UTILITIES.arnoldON()
		refreshOverride()
	except:
		cmds.warning ("NO SE PUDO IMPORTAR UTILITIES")
		cmds.warning ("NO SE PUDO PRENDER ARNOLD")
	lightList = cmds.ls(['*_LPNTSH','*_LDIRSH','*_LARESH','*_LAMBSH','*_LSPTSH'],r=1,lights = True)
	arnoldLightList = []
	dicLuces={}
	if cmds.window('winMLuces',exists=True):
		cmds.deleteUI('winMLuces')
	if cmds.dockControl('dockLucesUI',ex=1)==True:
		cmds.deleteUI('dockLucesUI')
	win = cmds.window('winMLuces', title="PH_LUCES! v1.7 - COMPATIBLE CON ARNOLD -", menuBar=0 , w=100 , s=1, height= 100)
	col_0 = cmds.columnLayout('col_0', p=win)
	cmds.separator(h=5,w=10,hr=0,p=col_0,st="none")
	row_0 = cmds.rowLayout ('row_0',numberOfColumns = 16 , height= 30, p=col_0 )
	cmds.separator(w=3,p=row_0,st="none")
	b_sel = cmds.iconTextButton ('b_sel',ann='(.)SELECCIONAR - (..)DESELECCIONAR',style='iconOnly',image1='selectObject.png', c = seleccionarLuces , dcc= deseleccionar, width=25,height=25,p=row_0, bgc=(0.4,0.4,0.4),font= "fixedWidthFont")
	cmds.separator(w=20,p=row_0,st="none")
	b_filtroSpot = cmds.iconTextButton  ('b_filtroLSPT',ann='SPOT',style='iconOnly',image1='M:\PH_SCRIPTS\ICONS\LSPT_1.png', c = partial(filtrado,"LSPT") ,width=25,height=25,p=row_0, dcc=partial(add_light,"spot") ,bgc=(0.2,0.2,0.2),font= "fixedWidthFont")
	b_filtroPoint = cmds.iconTextButton ('b_filtroLPNT',ann='POINT',style='iconOnly',image1='M:\PH_SCRIPTS\ICONS\LPNT_1.png', c = partial(filtrado,"LPNT") , width=25,height=25,p=row_0, dcc=partial(add_light,"point") ,bgc=(0.2,0.2,0.2),font= "fixedWidthFont")
	b_filtroArea = cmds.iconTextButton  ('b_filtroLARE',ann='AREA',style='iconOnly',image1='M:\PH_SCRIPTS\ICONS\LARE_1.png', c = partial(filtrado,"LARE") ,width=25,height=25,p=row_0, dcc=partial(add_light,"area") ,bgc=(0.2,0.2,0.2),font= "fixedWidthFont")
	b_filtroDir = cmds.iconTextButton   ('b_filtroLDIR',ann='DIRECTIONAL',style='iconOnly',image1='M:\PH_SCRIPTS\ICONS\LDIR_1.png', c = partial(filtrado,"LDIR") ,width=25,height=25,p=row_0, dcc=partial(add_light,"dir") ,bgc=(0.2,0.2,0.2),font= "fixedWidthFont")
	b_all = cmds.iconTextButton         ('b_filtrotodos',ann='TOGGLE FILTROS TODOS',style='iconOnly', image1='M:\PH_SCRIPTS\ICONS\TODAS_1.png',width=25,height=25,p=row_0,c=tglTodos )
	cmds.separator ( hr=0 , w=10 , p = row_0 )
	grupo_crear = cmds.iconTextButton   (style='iconOnly', image1 = 'M:\PH_SCRIPTS\ICONS\PH_LUCES_CARPETA.png' ,width=25,height=25, c=crearGrupo , ann="CREA UN GRUPO DE LUZ CON EL NOMBRE ESPECIFICADO",  p = row_0 )
	grupo_renombrar = cmds.iconTextButton   (style='iconOnly', image1 = 'M:\PH_SCRIPTS\ICONS\PH_LUCES_CARPETA_RENOMBRAR.png',width=25,height=25, c=renombrarGrupo , ann="RENOMBRA EL GRUPO ELEGIDO EN EL DROP.\nDESELECCIONA LAS LUCES DE LA LISTA PARA HABILITAR ESTA OPCION.",  p = row_0 )
	grupo_borrar = cmds.iconTextButton   (style='iconOnly', image1 = 'M:\PH_SCRIPTS\ICONS\PH_LUCES_CARPETA_BORRAR.png' ,width=25,height=25, c=borrarGrupo , ann="BORRA EL GRUPO ELEGIDO EN EL DROP.\nDESELECCIONA LAS LUCES DE LA LISTA PARA HABILITAR ESTA OPCION.",  p = row_0 )
	grupoVG = cmds.optionMenu (    bgc = [0.1,0.1,0.1] , w=70 , changeCommand = cambiarGrupo , p = row_0)
	grupoCParent = cmds.optionMenu ( en=0,ann="DESELECCIONA LAS LUCES DE LA LISTA PARA HABILITAR ESTA OPCION.",bgc = [0.27,0.27,0.27] , w=70 , changeCommand = cambiarGrupoParent , p = row_0)
	buscador = cmds.textField ( 'buscador' , w=100,p = row_0  )
	pop = cmds.popupMenu(p='buscador')#|textScrollList
	cmds.menuItem(l="BUSCAR POR LUZ"   , c = setBusquedaPorLuz   , p=pop)
	cmds.menuItem(l="BUSCAR POR GRUPO" , c = setBusquedaPorGrupo ,p=pop)
	col = cmds.columnLayout(p=win,h=30)
	row1 = cmds.rowLayout ( 'row1' , parent = col, numberOfColumns = 2 , columnWidth = [(1,200),(2,100)], height = 30  )
	cmds.separator ( p = col )
	scroll = cmds.scrollLayout( 'scroll',parent = win , childResizable = 1, width = 520 , h=500)
	columnScroll = cmds.rowLayout( 'columnScroll', rowAttach = [2, "top", 0]  , numberOfColumns = 4 ,p=scroll, nbg = 1)
	for l in lightList:
		name = cmds.listRelatives(l,type='transform',p=True)[0]
		grupo = cmds.listRelatives(name,type='transform',p=True)[0]
		lightType = cmds.nodeType(l)
		dicLuces[name]= [lightType,l,grupo]
	construirScrollsConBotones ( emparentarA=scroll )
	frame_1 = cmds.frameLayout('frame_1' , h=120, expandCommand= "cmds.frameLayout('frame_1', e=1 , height= cmds.frameLayout('frame_1', q=1 , height= 1)+102 )" , collapseCommand = "cmds.frameLayout('frame_1', e=1 , height= cmds.frameLayout('frame_1', q=1 , height= 1)-102 )\ncmds.dockControl('dockLucesUI', e=1 , h=cmds.dockControl('dockLucesUI', q=1 , height= 1)-20 )" , label='ATRIBUTOS', borderStyle='in',collapsable=1,p=win , w=520 )
	rootDeLaEscena = ""
	roots = cmds.ls('ROOT_*_LGRP',r=1)
	listaDeRootsNoReferenciados=[]
	for root in roots:
		if cmds.referenceQuery( root ,isNodeReferenced=1 ) == False:
			listaDeRootsNoReferenciados.append (root)
	if len(listaDeRootsNoReferenciados)==1:
		rootDeLaEscena = listaDeRootsNoReferenciados[0]
	clearOptionMenu (grupoVG)
	gruposDeLuces = cmds.ls ( '*_LGRP' , type='transform' )
	for grp in gruposDeLuces:
		if grp !=rootDeLaEscena and cmds.referenceQuery( grp ,isNodeReferenced=1 ) == False :
			cmds.menuItem(parent=grupoVG , label=grp[:-5] )
	clearOptionMenu (grupoCParent)
	for grp in gruposDeLuces:
		if grp != rootDeLaEscena and cmds.referenceQuery( grp ,isNodeReferenced=1 ) == False:
			cmds.menuItem(parent=grupoCParent , label=grp[:-5] )
	row_3 = cmds.rowLayout ( p=frame_1 , numberOfColumns=21 , h=10 )
	cmds.separator(p=row_3 ,w=11 , st= "none")
	cmds.text(label='On' , p = row_3 , ann="ON / OFF")
	cmds.text(label='         Int     ' , p = row_3 , ann="INTENSITY")
	cmds.text(label='   Exp ' , p = row_3 , ann="EXPOSURE")
	cmds.text(label='       Rad   ' , p = row_3 , ann="aiRADIUS")
	cmds.text(label='    Ang  ' , p = row_3 , ann="aiANGLE")
	cmds.text(label='   ConeA' , p = row_3 , ann="CONE ANGLE")
	cmds.separator(w=6,st= "none", p=row_3 )
	cmds.text(label='PenuA' , p = row_3 , ann="PENUMBRA ANGLE")
	cmds.separator(w=4,st= "none", p=row_3 )
	cmds.text(label='Dropoff' , p = row_3 , ann="DROPOFF")
	cmds.separator(w=5,st= "none", p=row_3 )
	cmds.text('col',label=' Col   ' , p=row_3 , ann="COLOR")
	cmds.text(label='iDef ' , p=row_3 , ann="ILLUMINATES BY DEFAULT")
	cmds.text(label='eD ' , p=row_3, ann="EMIT DIFFUSE")
	cmds.text(label=' eS' , p=row_3 , ann="EMIT SPECULAR" )
	cmds.separator(w=5,st= "none", p=row_3 )
	cmds.text(label='Samp  ' , p = row_3, ann="aiSAMPLES")
	cmds.text(label=' ShDens  ' , p = row_3, ann="SHADOW DENSITY")
	row_2 = cmds.rowLayout ( 'rowCambiaColor',p=frame_1  , numberOfColumns=25 , h=30 ,bgc=[0.5,0.5,0.5])
	cmds.separator(p=row_2 ,w=10, st= "none")
	cmds.checkBox ('on_off' ,en=0, l='' , w=13 ,h=20 , changeCommand = onoff  , p=row_2  )
	cmds.separator(p=row_2 ,w=5, st= "none")
	cmds.floatField( 'intensity' ,  en = 0 , precision = 3,  w = 50 , changeCommand = setInt  ,  p = row_2 )
	crearDropCopiarPegar ('intensity')
	cmds.floatField('aiExposure' , en=0, precision = 3, w=40 , changeCommand = setExp  , p = row_2 )
	crearDropCopiarPegar ('aiExposure')
	cmds.floatField('aiRadius' , en=0,precision = 2,  w=40 , changeCommand = setRad , p = row_2 )
	crearDropCopiarPegar ('aiRadius')
	cmds.floatField('aiAngle' , en=0,precision = 2, w=40 , changeCommand = setAng , p= row_2 )
	crearDropCopiarPegar ('aiAngle')
	cmds.floatField('coneAngle' ,en=0, w=40 ,h=20 ,pre=2, cc = setconeangle  , p=row_2 )
	crearDropCopiarPegar ('coneAngle')
	cmds.floatField('penumbraAngle' ,en=0,w=40 ,h=20 ,pre=2, cc = setpenumbraAngle , p=row_2 )
	crearDropCopiarPegar ('penumbraAngle')
	cmds.floatField('dropoff' ,en=0, w=40 ,h=20 ,pre=2, cc = setdropoff  , p=row_2 )
	crearDropCopiarPegar ('dropoff')
	cmds.separator(w=2,st= "none", p=row_2 )
	cmds.colorSliderGrp( 'color' , en=0,  cw2 = (23, 0),co2=[5, 0],ct2=["both", "both"], changeCommand = setColor , p=row_2)
	cmds.checkBox ('C_ilumDef' ,en=0, l='' , w=13 ,h=20 , changeCommand = setilumDef  , p=row_2  )
	cmds.separator(w=4,st= "none", p=row_2 )
	cmds.checkBox ('emitDiffuse' ,en=0, l='' , w=13 ,h=20 , changeCommand = setDif  , p=row_2 )
	cmds.separator(w=4,st= "none", p=row_2 )
	cmds.checkBox ('emitSpecular' ,en=0, l='' , w=13 ,h=20  , changeCommand = setSpec   , p=row_2 )
	cmds.separator(w=4,st= "none", p=row_2 )
	cmds.floatField('aiSamples' , en=0,precision = 0,  w=32 , changeCommand = setSamp  , p = row_2  )
	cmds.separator(w=4,st= "none", p=row_2 )
	cmds.floatField('aiShadowDensity' , en=0,precision = 2,  w=32 , changeCommand = setShadowDensity  , p = row_2  )
	row_5 = cmds.rowLayout ( 'rowSegundoRowAtts' , p=frame_1  , numberOfColumns=11 , h=1, cal=[1,"center"]  , rat= [1, "top", 0]	 )
	cmds.radioCollection('radioAbsRel')
	rowDeColumnas=cmds.rowLayout (nc=3,co3=[170,0,50],ct3=["left", "left", "both"], p=row_5 ,h=20)
	row_AbsRel = cmds.columnLayout( p = rowDeColumnas)
	cmds.radioCollection('absrelRadio')
	abs = cmds.radioButton( 'A',label='ABSOLUTO',en=0,sl=1,ann="ABSOLUTO",cl='radioAbsRel',onc='cmds.rowLayout("rowCambiaColor",e=1,bgc=[0.5,0.5,0.5]) ')
	row_ventanaCrearLuz = cmds.columnLayout( p = rowDeColumnas )
	cmds.radioCollection()
	rel = cmds.radioButton('R', label='RELATIVO',en=0, ann="RELATIVO",cl='radioAbsRel', onc='cmds.rowLayout("rowCambiaColor",e=1,bgc=[0.18,0.65,0.72]) ')
	row_filtros = cmds.rowLayout( p = rowDeColumnas ,nc=21)
	cmds.text(label='               CT ' , ann="COLOR TEMPERATURE", p=row_filtros)
	cmds.iconTextButton  ('b_masCalido', en=0,ann='-100',style='iconOnly',image1='arrowDown', c = masCalido ,width=15,height=15,p=row_filtros,bgc=(1,0.2,0.2))
	crearPopTempColor ('b_masCalido')
	tempColor = cmds.floatField('aiColorTemperature' ,w=40 ,  bgc=(1,0.2,0.2) , en=0 , pre=0 ,h=15 ,cc = setTempColor, p=row_filtros )
	popTempColor = cmds.popupMenu(p=tempColor)
	cmds.menuItem(l="SELECCIONAR POR TEMPERATURA COLOR ON" , p=popTempColor , c=partial(seleccionarTempColor,1) )
	cmds.menuItem(l="SELECCIONAR POR TEMPERATURA COLOR OFF" , p=popTempColor , c=partial(seleccionarTempColor,0)  )
	cmds.iconTextButton  ('b_masFrio', en=0 ,ann='+100',style='iconOnly',image1='arrowUp', c = masFrio ,width=15,height=15,p=row_filtros,bgc=(0.2,0.2,1))
	crearPopTempColor ('b_masFrio')

	#ESTO ESTA DESHABILITADO HASTA QUE ESTE FUNCIONAL
	#filtrosDropMenu = cmds.optionMenu('oM_filtros',annotation="FILTROS",bgc = [0.7,0.7,0.7],w=70,en=0,changeCommand=asignarFiltro,p=row_filtros)
	#clearOptionMenu (filtrosDropMenu)
	#filtros = cmds.ls ( type='aiLightDecay' )
	#for filtro in filtros:
	#	cmds.menuItem(parent=(filtrosDropMenu +'|OptionMenu'), label=filtro)

	cmds.textScrollList ('listaLuces1' , e=1  ,da=1)
	cmds.textScrollList ('listaLuces2' , e=1  ,da=1)
	cmds.textScrollList ('listaLuces3' , e=1  ,da=1)
	cmds.columnLayout (h=5,p=win)
	frame_2 = cmds.frameLayout('frame_2', label='EXTRAS ARNOLD SETTINGS', borderStyle='in', expandCommand= "cmds.frameLayout('frame_2', e=1 , height= cmds.frameLayout('frame_2', q=1 , height= 1)+20 )" , collapseCommand = "cmds.frameLayout('frame_2', e=1 , height= cmds.frameLayout('frame_2', q=1 , height= 1)-20 )\ncmds.dockControl('dockLucesUI', e=1 , h=cmds.dockControl('dockLucesUI', q=1 , height= 1)-20 )"   ,collapsable=1,p=win , h=50 , w=520 )
	row_6 = cmds.rowLayout ( p=frame_2 , numberOfColumns=21 , h=30 )
	b_sss = cmds.iconTextButton  ('b_sss',l='SSS',style='textOnly',image1='M:\PH_SCRIPTS\ICONS\PH_LUCES_SSS.png', c = sss ,width=90,height=25,p=row_6 ,bgc=(0.2,0.2,0.2))
	b_disp = cmds.iconTextButton  ('b_disp',l='DISPLACEMENT',style='textOnly',image1='M:\PH_SCRIPTS\ICONS\PH_LUCES_DISP.png', c = disp ,width=90,height=25,p=row_6 ,bgc=(0.2,0.2,0.2))
	b_sub = cmds.iconTextButton  ('b_sub',l='SUBDIVISION',style='textOnly',image1='M:\PH_SCRIPTS\ICONS\PH_LUCES_DISP.png', c = sub ,width=90,height=25,p=row_6 ,bgc=(0.4,0.4,0.4))
	b_flush = cmds.iconTextButton  ('b_flush',l='FLUSH CACHE',style='textOnly',image1='M:\PH_SCRIPTS\ICONS\PH_LUCES_DISP.png', c = "cmds.arnoldFlushCache(flushall=True)" ,width=90,height=25,p=row_6 ,bgc=(0.4,0.4,0.4))
	refreshOverride()
	enableDropParent()
	cmds.window('winMLuces', e=1 , resizeToFitChildren=1 )
	allowedAreas = ['right', 'left']
	placeHolder = cmds.menuItem ( p = grupoVG , l="placeholder")
	dockLuces = cmds.dockControl( 'dockLucesUI' , label= "PH_LUCES! v1.6 - COMPATIBLE CON ARNOLD -",area='left', content=win, allowedArea=allowedAreas )
	dock = cmds.optionMenu ( grupoVG , q=1 , ill=1 )[0].split("|")[0]
	cmds.deleteUI (dock + placeHolder.split("winMLuces")[1] )


ultimoOrden="luz" #VARIABLE LOCAL PARA EL SWITCH DEL ORDEN DE LAS LUCES
orden = {"luz":0,"tipo":0,"grupo":0} #DICCIONARIO PARA SABER SI LAS VECES DE TOCAR EL BOTON SON PARES O INPARES
