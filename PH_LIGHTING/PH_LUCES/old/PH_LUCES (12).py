import maya.cmds as cmds
from functools import partial
from operator import itemgetter
global grupoVG
global orden
global ultimoOrden
global grupoVCreacion
global ultimoGrupoCreadoPorUsuario
global aiColorTemperatureSlider
def add_light(kind):
	global contSpot
	global contDir
	global contPoint
	global contArea
	global contAmb
	global grupoVCreacion

	primerGrupoCreado = ""
	if(not cmds.ls('ROOT_LGRP')):
		root = cmds.group(name='ROOT_LGRP', em=True, w=True)
		rootAts = cmds.listAttr (root , k=1 )
		for at in rootAts:
			cmds.setAttr (root+"."+at,lock=1,k=0,channelBox=0)

	if len(cmds.ls ('*_LGRP'))==1:
		cmds.confirmDialog ( title='AVISO', message='NO HAY GRUPOS DE LUCES EN LA ESCENA. CREEMOS UNO.', button=['OKI'], defaultButton='OKI' )
		primerGrupoCreado = crearGrupo()
	if cmds.window('crearLuzV',exists=True):
		cmds.deleteUI ('crearLuzV')
	ventanaCreacionLuz = cmds.window ('crearLuzV' , menuBar=0,w=250,title = "CREAR LUZ" )
	col_ventanaCrearLuz = cmds.columnLayout( adjustableColumn = True , p = ventanaCreacionLuz )
	cmds.textField ('nombreLuzCreacion' , pht='NOMBRE' ,  p=col_ventanaCrearLuz )
	grupoVCreacion = cmds.optionMenuGrp ( 'oM_grupoVCreacion',    bgc = [0.1,0.1,0.1] , p = col_ventanaCrearLuz)
	clearOptionMenu (grupoVCreacion)
	gruposDeLuces = cmds.ls ( '*_LGRP' , type='transform' )
	for grp in gruposDeLuces:
		if grp !="ROOT_LGRP":
			cmds.menuItem(parent=(grupoVCreacion +'|OptionMenu'), label=grp[:-5] )
	try:
		cmds.optionMenuGrp ( 'oM_grupoVCreacion', e=1 , v = ultimoGrupoCreadoPorUsuario.split("_LGRP")[0])

	except :
		cmds.optionMenuGrp ( 'oM_grupoVCreacion', e=1 , sl = 1 )

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
	lucesSeleccionadas = cmds.textScrollList('listaLuces1' ,q=1, si=1)
	for luz in lucesSeleccionadas:
		shapeLuz = cmds.listRelatives (luz, s=1)[0]
		tipoLuz = cmds.nodeType (shapeLuz)
    	if tipoLuz=="spotLight":
    		tipoLuz="spot"
    	elif tipoLuz=="directionalLight":
    		tipoLuz="dir"
    	elif tipoLuz=="areaLight":
    		tipoLuz="area"
    	elif tipoLuz=="pointLight":
    		tipoLuz="point"
    	crearLuz(kind=tipoLuz,nombre=luz)

def crearLuz(kind="",primerGrupoCreado='' , nombre=''):
    if nombre=="" or nombre==False:
        nombreLuz = cmds.textField('nombreLuzCreacion',q=1,text=1)+"_"+cmds.radioCollection('coleccionTodo',q=1,select=1)+"_"
        grupoDeLaLuzCreada = cmds.optionMenu ('oM_grupoVCreacion|OptionMenu',q=1,value=1)
        if nombreLuz=="_"+cmds.radioCollection('coleccionTodo',q=1,select=1)+"_": #si no puso ningun nombre
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
        if cmds.objExists (nombreSinSuff+str(nroLuz).zfill(3)+'_LSPO'):
            while cmds.objExists (nombreSinSuff+str(nroLuz).zfill(3)+'_LSPO'):
                nroLuz +=1
            nombreSinSuff = cmds.rename(  nombreSinSuff , nombreSinSuff + str(nroLuz).zfill(3) )
            nombreConSuff = cmds.rename(  nombreSinSuff , nombreSinSuff + '_LSPO' )
        else:
            nombreConSuff=cmds.rename(  nombreSinSuff , nombreSinSuff + str(nroLuz).zfill(3) + '_LSPO')
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
    clearOptionMenu (grupoVG)
    gruposDeLuces = cmds.ls ( '*_LGRP' , type='transform' )
    for grp in gruposDeLuces:
        if grp !="ROOT_LGRP":
            cmds.menuItem(parent=(grupoVG +'|OptionMenu'), label=grp[:-5] )
    if cmds.window('crearLuzV',q=1,ex=1):
        cmds.deleteUI ('crearLuzV')
    cmds.textScrollList ('listaLuces1',e=1,da=1)
    cmds.textScrollList ('listaLuces1',e=1,si=nombreConSuff)
    ordenarLuz()


def clearOptionMenu (optionMenu):
	optionMenuFullName = None
	try:
		menuItems = cmds.optionMenuGrp ( grupoVG , q=1 , ill=1 )
		if menuItems != None and menuItems !=[]:
			cmds.deleteUI ( menuItems )
		firstItem = menuItems[0]
		optionMenuFullName = firstItem [:-len(firstItem.split ("|")[1])-1]
	except:
		pass
	return optionMenuFullName

def borrarBuscador(args):
	cmds.textField ('buscador' , e=1 , text="")
	cmds.warning ("~~~~~~~~~ borrarBuscador() ~~~~~~~~~")


def seleccionarLuces():
    shapesSeleccionado = cmds.listRelatives (cmds.textScrollList ('listaLuces1',q=1, si=1) , shapes=1)

    cmds.select ( shapesSeleccionado )

def tglTodos():
	botonesFiltros = ['LDIR','LSPO','LPNT','LARE',]
	imagenEstado = int(cmds.iconTextButton ('b_filtroLSPO',q=1, i1=1)[-5])
	for boton in botonesFiltros:
		cmds.iconTextButton ("b_filtro"+boton,e=1,i1="M:\PH_SCRIPTS\ICONS\\"+boton+"_"+str(int(not(imagenEstado)))+".png")
	filtradoRefresh()

def filtrado(luzTipo):
	imagen = cmds.iconTextButton ('b_filtro'+luzTipo,q=1, i1=1)
	if int(imagen[-5])==1:
		cmds.iconTextButton ('b_filtro'+luzTipo , e=1 , i1="M:\PH_SCRIPTS\ICONS\\"+luzTipo+"_0.png")
	if int(imagen[-5])==0:
		cmds.iconTextButton ('b_filtro'+luzTipo , e=1 , i1="M:\PH_SCRIPTS\ICONS\\"+luzTipo+"_1.png")
	filtradoRefresh()

def filtradoRefresh():
	#  QUERY DE FILTROS ACTIVADOS.
	filtros = ['b_filtroLPNT','b_filtroLDIR','b_filtroLSPO','b_filtroLARE']
	filtrosActivos=[]

	for filtro in filtros:
		estadoFiltro = int  ((cmds.iconTextButton (filtro , q = 1 , i1=1))[-5])
		if estadoFiltro==1:
			filtrosActivos.append ( "*"+ filtro[-4:] + "SH" )

	ordenarTipo( arraySufijos =filtrosActivos)

def refreshui(refrescarPor="",*args):
	global grupoVG
	global aiColorTemperatureSlider

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
	clearOptionMenu (grupoVG)
	gruposDeLuces = cmds.ls ( '*_LGRP' , type='transform' )
	for grp in gruposDeLuces:
		if grp !="ROOT_LGRP":
			cmds.menuItem(parent=(grupoVG +'|OptionMenu'), label=grp[:-5] )

	# REFRESH DE ATRIBUTOS.
	lucesSeleccionadas = cmds.textScrollList('listaLuces1' ,q=1, si=1)
	if lucesSeleccionadas != None:
		camposAtributos       = { "on_off":0, "aiExposure":0 , "aiRadius":0, "aiColorTemperature":0, "color":0, "intensity":0, "aiAngle":0, "aiSamples":0,"emitDiffuse":0,"emitSpecular":0 }
		camposAtributosV      = { "on_off":0, "aiExposure":0 , "aiRadius":0, "aiColorTemperature":None, "color":None, "intensity":0, "aiAngle":0, "aiSamples":0,"emitDiffuse":0,"emitSpecular":0 }
		camposAtributosDif    = { "on_off":0, "aiExposure":0 , "aiRadius":0, "aiColorTemperature":0, "color":0, "intensity":0, "aiAngle":0, "aiSamples":0,"emitDiffuse":0,"emitSpecular":0 }

		# hide / unhide
		for luz in lucesSeleccionadas: #VALORES
			if cmds.getAttr (luz+".visibility"):
				camposAtributosV["on_off"] = cmds.getAttr ( luz + ".visibility" )
		for luz in lucesSeleccionadas: # TIENEN EL MISMO VALOR TODOS?
			if cmds.getAttr (luz+".visibility") != camposAtributosV["on_off"] :
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
				if campo=="color" or campo=="aiColorTemperature":
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
					#print campo
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
					print "TIENEN VALORES DIF", campo
					cmds.checkBox ( campo , e=1 ,  en=1 , bgc=[0.863,0.808,0.529])
				except:
					pass
				if campo=="color" :
					cmds.colorSliderGrp( campo , e=1 , en=1  , bgc = [0.863,0.808,0.529])
				elif campo=='aiColorTemperature':
					cmds.colorSliderGrp( campo , e=1 , en=1  )
					print "tienen valores diferentes colorTemp" , campo

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

		lucesSeleccionadas = cmds.textScrollList('listaLuces1' ,q=1, si=1)
		for luz in lucesSeleccionadas:
			if cmds.getAttr (luz+".visibility"):
				cmds.textScrollList ("listaLuces1",e=1,da=1)
				cmds.textScrollList ("listaLuces1",e=1,si=luz)
				index= cmds.textScrollList ("listaLuces1",q=1,sii=1)[0]
				cmds.textScrollList ("listaLuces1", e=1, lf=[index,"boldLabelFont"])
			else:
				cmds.textScrollList ("listaLuces1",e=1,da=1)
				cmds.textScrollList ("listaLuces1",e=1,si=luz)
				index= cmds.textScrollList ("listaLuces1",q=1,sii=1)[0]
				cmds.textScrollList ("listaLuces1", e=1, lf=[index,"obliqueLabelFont"])

		cmds.textScrollList ("listaLuces1",e=1,si=lucesSeleccionadas)

		dropListas()

def enableCampos(camposAtributos={}):
	# HABILITAR DESHABILITAR
	lucesSeleccionadas=cmds.textScrollList ('listaLuces1',q=1,si=1)
	if len(lucesSeleccionadas)!=0:
		for campo in camposAtributos.keys():
			if camposAtributos[campo] != len(lucesSeleccionadas):
				try:
					cmds.floatField ( campo , e=1 , en=0)
				except:
					pass
				try:
					cmds.checkBox ( campo , e=1  , en=0 )
				except:
					pass
				if campo=="color" or campo=="aiColorTemperature":
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
				if campo=="color" or campo=="aiColorTemperature":
					try:
						cmds.colorSliderGrp( campo , e=1 , en=1 )
					except:
						pass


def maxmin():
	#variables
	lucesSeleccionadas = cmds.textScrollList('listaLuces1' ,q=1, si=1)
	camposAtributosMin   = {"aiExposure":0 , "aiRadius":0, "intensity":0, "aiAngle":0, "aiSamples":0 }
	camposAtributosMax   = {"aiExposure":0 , "aiRadius":0, "intensity":0, "aiAngle":0, "aiSamples":0 }
	for luz in lucesSeleccionadas:
		for key in camposAtributosMin.keys(): # CAPTURO VALORES
			if (cmds.attributeQuery (key , node=luz+"SH" , ex=1)):
				camposAtributosMin[key]= [luz, cmds.getAttr ( luz+"SH."+key ) ]
				camposAtributosMax[key]= [luz, cmds.getAttr ( luz+"SH."+key ) ]
	for luz in lucesSeleccionadas:
		for key in camposAtributosMin.keys():
			if (cmds.attributeQuery ( key , node = luz+"SH" , ex=1)):
				if cmds.getAttr(luz+"."+key)<camposAtributosMin[key][1]:
					camposAtributosMin[key][1]=cmds.getAttr(luz+"."+key)
					camposAtributosMin[key][0]=luz
	for luz in lucesSeleccionadas:
		for key in camposAtributosMax.keys():
			if (cmds.attributeQuery ( key , node = luz+"SH" , ex=1)):
				if cmds.getAttr(luz+"."+key)>camposAtributosMax[key][1]:
					camposAtributosMax[key][1]=cmds.getAttr(luz+"."+key)
					camposAtributosMax[key][0]=luz

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


def dropListas():
	lucesSeleccionadas = cmds.textScrollList ( 'listaLuces1' , q=1 , ai=1 )
	for luz in lucesSeleccionadas:
		pop = cmds.popupMenu(p='listaLuces1')#|textScrollList
		cmds.menuItem(l="DUPLICAR" , c=duplicarLuz , p=pop)
		cmds.menuItem(l="CREAR PRESET" , c='print "crearPreset()"', en=0 , p=pop)
		cmds.menuItem(l="VER A TRAVES DE ESTA LUZ" , c='print "ver()"',  en=0 ,p=pop)

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
                cmds.setAttr (luz+'SH.color',rgbSet[0],rgbSet[1],rgbSet[2],type='double3' )
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
	lucesTodas = cmds.ls(['*_LPNTSH','*_LDIRSH','*_LARESH','*_LAMBSH','*_LSPOSH'],lights = True)
	if len(lucesTodas)!=0:
		datosOrdenados =  ordenarDatos(ordenarPor='luz' , filtrado='')
		if orden["luz"]%2 == 1:
			datosOrdenados[0].reverse()
			datosOrdenados[1].reverse()
			datosOrdenados[2].reverse()
		listas = ['listaLuces1','listaLuces2','listaLuces3']
		try:
			seleccionar = cmds.textScrollList ('listaLuces1' , q=1 , si=1 )
		except:
			pass
		for lista in listas:
			cmds.textScrollList (lista, e=1 ,ra=1)
		try:
			cmds.textScrollList ('listaLuces1' , e=1  ,  a=datosOrdenados[0] , numberOfRows = len(datosOrdenados[0])+2 , si=seleccionar)
		except:
			pass
		try:
			indiceSeleccionLista1 = cmds.textScrollList ('listaLuces1' , q=1 , sii=1 )
		except:
			pass
		try:
			cmds.textScrollList ('listaLuces2' , e=1  ,  a=datosOrdenados[1] , numberOfRows = len(datosOrdenados[0])+2, sii= indiceSeleccionLista1)
		except:
			pass
		try:
			cmds.textScrollList ('listaLuces3' , e=1  ,  a=datosOrdenados[2] , numberOfRows = len(datosOrdenados[0])+2, sii=indiceSeleccionLista1)
		except:
			pass
	  	orden["luz"] +=1
	else:
		cmds.textScrollList('listaLuces1',e=1,ra=1)
		cmds.textScrollList('listaLuces2',e=1,ra=1)
		cmds.textScrollList('listaLuces3',e=1,ra=1)
		cmds.warning ("---- NO SE DETECTARON LUCES ADMITIDAS ----")

#..................................................................................................................................
def ordenarTipo( arraySufijos =[],seleccionar=1):
	global orden
	if filtrado =='':
		datosOrdenados =  ordenarDatos(ordenarPor='tipo' , filtrado='')
	else:
		datosOrdenados = ordenarDatos(ordenarPor='tipo' , filtrado=arraySufijos)
	if orden["tipo"]%2 == 1:
		datosOrdenados[0].reverse()
		datosOrdenados[1].reverse()
		datosOrdenados[2].reverse()
	listas = ['listaLuces1','listaLuces2','listaLuces3']
	try:# items seleccionados
		seleccionar = cmds.textScrollList ('listaLuces1' , q=1 , si=1 )
	except:
		pass
	for lista in listas:#limpio listas
		cmds.textScrollList (lista, e=1 ,ra=1)

	try:
		cmds.textScrollList ('listaLuces1' , e=1  ,  a=datosOrdenados[0] , numberOfRows = len(datosOrdenados[0])+2, si=seleccionar ) #lleno lista1
		indiceSeleccionLista1 = cmds.textScrollList ('listaLuces1' , q=1 , sii=1 ) # obtengo indices de items1
		cmds.textScrollList ('listaLuces2' , e=1  ,  a=datosOrdenados[1] , numberOfRows = len(datosOrdenados[0])+2, sii=indiceSeleccionLista1)
		cmds.textScrollList ('listaLuces3' , e=1  ,  a=datosOrdenados[2] , numberOfRows = len(datosOrdenados[0])+2, sii=indiceSeleccionLista1)
	except:
		pass
	orden["tipo"] +=1
	ultimoOrden="tipo"


def ordenarTipo2(*args): ################################################################################################
	global orden
	lucesShapes=[]
	tipos_de_Luces=[]
	filtro_tipos=[]
	tipo_de_Luz=""
	lucesTodas = cmds.ls(['*_LPNTSH','*_LDIRSH','*_LARESH','*_LAMBSH','*_LSPOSH'],lights = True)
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
				filtro_tipos.append("*_LSPOSH")
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
			orden["tipo"]+=1
			ultimoOrden="tipo"
	else:
		cmds.textScrollList('listaLuces1',e=1,ra=1)
		cmds.textScrollList('listaLuces2',e=1,ra=1)
		cmds.textScrollList('listaLuces3',e=1,ra=1)
		cmds.warning ("---- NO SE DETECTARON LUCES ADMITIDAS ----")

def ordenarGrupo(seleccionar=1):
	global orden
	lucesTodas = cmds.ls(['*_LPNTSH','*_LDIRSH','*_LARESH','*_LAMBSH','*_LSPOSH'],lights = True)
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
		orden["grupo"]+=1
		ultimoOrden="grupo"
	else:
		cmds.textScrollList('listaLuces1',e=1,ra=1)
		cmds.textScrollList('listaLuces2',e=1,ra=1)
		cmds.textScrollList('listaLuces3',e=1,ra=1)
		cmds.warning ("---- NO SE DETECTARON LUCES ADMITIDAS ----")
def cambiarGrupo(*args):
	global orden
	if cmds.textScrollList('listaLuces1',q=1,si=1)!=None:
		lucesSeleccionadas = cmds.textScrollList('listaLuces1' ,q=1, si=1)
		lucesSeleccionadasInd = cmds.textScrollList('listaLuces1' ,q=1, sii=1)
		grupoSeleccionado = cmds.optionMenu ( (grupoVG +'|OptionMenu')  , q=1 , value=1)
		for luz in lucesSeleccionadas:
		    try:
		        cmds.parent ( luz , grupoSeleccionado+"_LGRP" )
		    except:
				cmds.warning( "NO SE PUDO EMPARENTAR")
				pass
		if ultimoOrden=="luz":
			orden["luz"]+=1
			ordenarLuz(seleccionar=lucesSeleccionadasInd)
		if ultimoOrden=="tipo":
			orden["tipo"]+=1
			ordenarTipo()
		if ultimoOrden=="grupo":
			orden["grupo"]+=1
			ordenarGrupo()
	else:
		cmds.warning('NO HAY LUZ/LUCES SELECCIONADA/S')

def crearGrupo(*args):
	global ultimoGrupoCreadoPorUsuario

	if(not cmds.ls('ROOT_LGRP')):
		cmds.group(name='ROOT_LGRP', em=True, w=True)
	pideNombreGrupo = 'OK'
	arrancaConNumero=1
	while pideNombreGrupo=='OK' and arrancaConNumero==1:
		pideNombreGrupo = cmds.promptDialog(title='NOMBRAR',message='NOMBRE DE GRUPO:',button=['OK', 'CANCELAR'],defaultButton='OK',cancelButton='CANCELAR',dismissString='Cancel')
		if pideNombreGrupo == 'OK' and str(cmds.promptDialog(query=True, text=True))[0].isdigit()==False:
			arrancaConNumero=0
			qNombreGrupo = cmds.promptDialog(query=True, text=True)
			nombreDelGrupoCreado=cmds.group(name = qNombreGrupo.upper() + '_LGRP', em=True, w=True)
			cmds.parent ( qNombreGrupo.upper() + '_LGRP' , 'ROOT_LGRP' )
			#ACTUALIZO GRUPOS
			clearOptionMenu (grupoVG)
			gruposDeLuces = cmds.ls ( '*_LGRP' , type='transform' )
			for grp in gruposDeLuces:
				if grp != "ROOT_LGRP":
					cmds.menuItem(parent=(grupoVG +'|OptionMenu'), label=grp[:-5] )
		elif pideNombreGrupo == 'OK' and str(cmds.promptDialog(query=True, text=True))[0].isdigit()==True:
			cmds.warning ( "EL NOMBRE NO PUEDE COMENZAR CON UN NUMERO." )
		else:
			cmds.warning ( "USUARIO CANCELA" )
	if pideNombreGrupo=='OK':
		ultimoGrupoCreadoPorUsuario=nombreDelGrupoCreado
		return nombreDelGrupoCreado

def ordenarDatos(ordenarPor , filtrado=''):
    if filtrado=='':
	    luces = cmds.ls(['*_LPNTSH','*_LDIRSH','*_LARESH','*_LAMBSH','*_LSPOSH'],lights = True)
    else:
    	luces = cmds.ls( filtrado , lights = True)
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
	lightList = cmds.ls(['*_LPNTSH','*_LDIRSH','*_LARESH','*_LAMBSH','*_LSPOSH'],lights = True)
	dicLuces={}
	for l in lightList:
		name = cmds.listRelatives(l,type='transform',p=True)[0]
		grupo = cmds.listRelatives(name,type='transform',p=True)[0]
		lightType = cmds.nodeType(l)
		dicLuces[name]= [lightType,l,grupo]
	r_00 = cmds.rowLayout ('r_00', nc = 4 , p = 'row1' , h = 30 , cw4= [ 308 , 81 , 100 , 20] , ct4= ["both", "both", "both", "both"  ])
	cmds.button ( l = 'LUZ' ,   align = "center" ,  bgc=[0.3,0.3,0.3],c = ordenarLuz   , p = r_00 )
	cmds.button ( l = 'TIPO' ,  align = "center" ,  bgc=[0.3,0.3,0.3],c = ordenarTipo2  , p = r_00 )
	cmds.button ( l = 'GRUPO' , align = "center" ,  bgc=[0.3,0.3,0.3], c = ordenarGrupo ,  p = r_00 )
	b_isolate = cmds.iconTextButton  ('b_isolate',ann='AISLAR LUZ', en =0, style='iconOnly',image1='M:\PH_SCRIPTS\ICONS\PH_LUCES_ISOLATE.png', c = 'print "lkdsklsadklsadl"' ,width=15,height=25,p=r_00 )
	r_01 = cmds.rowLayout ( nc = 3 , cw3 = [ 305 , 80 , 100 ] ,  p = emparentarA )
	c_01 = cmds.columnLayout ('c_01', p = r_01 , adjustableColumn=1 )
	c_02 = cmds.columnLayout ( p = r_01 , adjustableColumn=1)
	c_03 = cmds.columnLayout ( p = r_01 , adjustableColumn=1)
	cmds.textScrollList('listaLuces1' , w = 300 , allowMultiSelection=1, p = c_01 , deleteKeyCommand=borrarSeleccion)
	cmds.textScrollList('listaLuces2' , w = 100 , allowMultiSelection = 1 , p = c_02 , bgc = [0.24,0.24,0.24] , dcc=tipoSel ,deleteKeyCommand=borrarSeleccion )
	cmds.textScrollList('listaLuces3' , w = 100 , allowMultiSelection = 1 , p = c_03 , bgc = [0.24,0.24,0.24] , dcc=grpSel ,deleteKeyCommand=borrarSeleccion)
	datosOrdenados = ordenarDatos(ordenarPor='luz' , filtrado='')
	cmds.textScrollList ('listaLuces1' , e=1 ,allowMultiSelection=1, a=datosOrdenados[0] , sc=partial(refreshui,'luz') ,  enable=1 ,h = (len(datosOrdenados[0])+2)*50)
	cmds.textScrollList ('listaLuces2' , e=1 ,allowMultiSelection=1, a=datosOrdenados[1] , sc=partial(refreshui,'tipo')  , enable=1 , h = (len(datosOrdenados[0])+2)*50 )
	cmds.textScrollList ('listaLuces3' , e=1 ,allowMultiSelection=1, a=datosOrdenados[2] , sc=partial(refreshui,'grupo')   , enable=1 ,h = (len(datosOrdenados[0])+2)*50 )
	cmds.textField ( 'buscador' , e=1 , aie= 1 , changeCommand = buscar, rfc= buscar, pht="Buscador" )

	lucesSeleccionadas = cmds.textScrollList('listaLuces1' ,q=1, ai=1)
	if lucesSeleccionadas!=None:
		for luz in lucesSeleccionadas:
			if cmds.getAttr (luz+".visibility"):
				cmds.textScrollList ("listaLuces1",e=1,da=1)
				cmds.textScrollList ("listaLuces1",e=1,si=luz)
				index= cmds.textScrollList ("listaLuces1",q=1,sii=1)[0]
				cmds.textScrollList ("listaLuces1", e=1, lf=[index,"boldLabelFont"])
			else:
				cmds.textScrollList ("listaLuces1",e=1,da=1)
				cmds.textScrollList ("listaLuces1",e=1,si=luz)
				index= cmds.textScrollList ("listaLuces1",q=1,sii=1)[0]
				cmds.textScrollList ("listaLuces1", e=1, lf=[index,"obliqueLabelFont"])

def buscar(*args):
	try:
		textoBuscador = cmds.textField ( 'buscador' , q=1 , text=True)
		if str(textoBuscador[0]).isdigit() ==1:
			recolectorBusqueda= cmds.ls("*"+textoBuscador,"*"+textoBuscador+"*", type='light')
		else:
			recolectorBusqueda= cmds.ls(textoBuscador+"*","*"+textoBuscador,"*"+textoBuscador+"*",textoBuscador , textoBuscador.upper()+"*","*"+textoBuscador.upper(),"*"+textoBuscador.upper()+"*",textoBuscador.upper() , type='light')
		recolectorBusqueda=list(set(recolectorBusqueda))
		resultadoBusqueda=[]
		for luz in recolectorBusqueda:
			if cmds.nodeType (luz)== "spotLight" or cmds.nodeType (luz)== "areaLight" or cmds.nodeType (luz)== "directionalLight" or cmds.nodeType (luz)== "pointLight":
				if ("_LPNT" in luz) or ( "_LSPO" in luz) or ( "_LDIR" in luz) or ( "_LAMB" in luz) or ( "_LARE" in luz):
					resultadoBusqueda.append(luz[:-2])

		cmds.textScrollList ('listaLuces1' , e=1 , da= 1)
		cmds.textScrollList ('listaLuces2' , e=1 , da= 1)
		cmds.textScrollList ('listaLuces3' , e=1 , da= 1)
		if len(resultadoBusqueda)!=0:
			cmds.textScrollList ('listaLuces1' , e=1 , si= resultadoBusqueda)
			indice = cmds.textScrollList ('listaLuces1' , q=1 , sii=1)
			cmds.textScrollList ('listaLuces2' , e=1 , sii=indice)
			cmds.textScrollList ('listaLuces3' , e=1 , sii=indice)
		else:
			cmds.warning('--- NO SE HA ENCONTRADO ---')
	except:
		if len(cmds.textField ( 'buscador' , q=1 , text=True))==0:
			pass
		else:
			cmds.warning ("NO SE HA PODIDO BUSCAR")

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


#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

def lightListPanel():
	global dicLuces
	global orden
	global grupoVG
	global aiColorTemperatureSlider
	try:
		import UTILITIES
		UTILITIES.arnoldON()
	except:
		cmds.warning ("NO SE PUDO IMPORTAR UTILITIES")
		cmds.warning ("NO SE PUDO PRENDER ARNOLD")
	lightList = cmds.ls(['*_LPNTSH','*_LDIRSH','*_LARESH','*_LAMBSH','*_LSPOSH'],lights = True)
	arnoldLightList = []
	dicLuces={}
	if cmds.window('winMLuces',exists=True):
		cmds.deleteUI('winMLuces')
	win = cmds.window('winMLuces', title="PH_LUCES! v1.1 BETA - COMPATIBLE CON ARNOLD -", menuBar=0 , w=100 , s=0, height= 100)
	col_0 = cmds.columnLayout('col_0', p=win)
	cmds.separator(h=5,w=10,hr=0,p=col_0,st="none")
	row_0 = cmds.rowLayout ('row_0',numberOfColumns = 16 , height= 30, p=col_0 )
	cmds.separator(w=3,p=row_0,st="none")
	b_sel = cmds.iconTextButton ('b_sel',ann='(.)SELECCIONAR - (..)DESELECCIONAR',style='iconOnly',image1='selectObject.png', c = seleccionarLuces , dcc= 'cmds.select(cl=True)', width=25,height=25,p=row_0, bgc=(0.4,0.4,0.4),font= "fixedWidthFont")
	cmds.separator(w=20,p=row_0,st="none")
	b_filtroSpot = cmds.iconTextButton  ('b_filtroLSPO',ann='SPOT',style='iconOnly',image1='M:\PH_SCRIPTS\ICONS\LSPO_1.png', c = partial(filtrado,"LSPO") ,width=25,height=25,p=row_0, dcc=partial(add_light,"spot") ,bgc=(0.2,0.2,0.2),font= "fixedWidthFont")
	b_filtroPoint = cmds.iconTextButton ('b_filtroLPNT',ann='POINT',style='iconOnly',image1='M:\PH_SCRIPTS\ICONS\LPNT_1.png', c = partial(filtrado,"LPNT") , width=25,height=25,p=row_0, dcc=partial(add_light,"point") ,bgc=(0.2,0.2,0.2),font= "fixedWidthFont")
	b_filtroArea = cmds.iconTextButton  ('b_filtroLARE',ann='AREA',style='iconOnly',image1='M:\PH_SCRIPTS\ICONS\LARE_1.png', c = partial(filtrado,"LARE") ,width=25,height=25,p=row_0, dcc=partial(add_light,"area") ,bgc=(0.2,0.2,0.2),font= "fixedWidthFont")
	b_filtroDir = cmds.iconTextButton   ('b_filtroLDIR',ann='DIRECTIONAL',style='iconOnly',image1='M:\PH_SCRIPTS\ICONS\LDIR_1.png', c = partial(filtrado,"LDIR") ,width=25,height=25,p=row_0, dcc=partial(add_light,"dir") ,bgc=(0.2,0.2,0.2),font= "fixedWidthFont")
	b_all = cmds.iconTextButton         ('b_filtrotodos',ann='TOGGLE FILTROS TODOS',style='iconOnly', image1='M:\PH_SCRIPTS\ICONS\TODAS_1.png',width=25,height=25,p=row_0,c=tglTodos )
	cmds.separator ( hr=0 , w=20 , p = row_0 )
	grupo_crear = cmds.button ( l="CREAR GRP" , c=crearGrupo , ann="CREA UN GRUPO DE LUZ CON EL NOMBRE ESPECIFICADO", bgc=[0.7,0.7,0.7] , p = row_0 )
	grupoVG = cmds.optionMenuGrp ( 'oM_grupo',    bgc = [0.1,0.1,0.1] , w=60 , changeCommand = cambiarGrupo , p = row_0)
	cmds.separator ( hr=0 , w=10 , p = row_0 )
	buscador = cmds.textField ( 'buscador' , p = row_0  )
	col = cmds.columnLayout(p=win,h=30)
	row1 = cmds.rowLayout ( 'row1' , parent = col, numberOfColumns = 2 , columnWidth = [(1,200),(2,100)], height = 30  )
	cmds.separator ( p = col )
	scroll = cmds.scrollLayout( 'scroll',parent = win , childResizable = 1, width = 520 , h=200)
	columnScroll = cmds.rowLayout( 'columnScroll', rowAttach = [2, "top", 0]  , numberOfColumns = 4 ,p=scroll, nbg = 1)
	for l in lightList:
		name = cmds.listRelatives(l,type='transform',p=True)[0]
		grupo = cmds.listRelatives(name,type='transform',p=True)[0]
		lightType = cmds.nodeType(l)
		dicLuces[name]= [lightType,l,grupo]
	construirScrollsConBotones ( emparentarA=scroll )
	frame_1 = cmds.frameLayout('frame_1', label='ATRIBUTOS', borderStyle='in',collapsable=1,p=win , h=110 , w=520 )
	clearOptionMenu (grupoVG)
	gruposDeLuces = cmds.ls ( '*_LGRP' , type='transform' )
	for grp in gruposDeLuces:
		if grp !="ROOT_LGRP":
			cmds.menuItem(parent=(grupoVG +'|OptionMenu'), label=grp[:-5] )
	row_3 = cmds.rowLayout ( p=frame_1 , numberOfColumns=20 , h=10 )
	cmds.separator(p=row_3 ,w=20 , st= "none")
	cmds.text(label='On' , p = row_3 , ann="ON / OFF")
	cmds.text(label='          Int       ' , p = row_3 , ann="INTENSITY")
	cmds.text(label='     Exp    ' , p = row_3 , ann="EXPOSURE")
	cmds.text(label='      Rad     ' , p = row_3 , ann="aiRADIUS")
	cmds.text(label='     Ang   ' , p = row_3 , ann="aiANGLE")
	cmds.text(label='      Samp    ' , p = row_3, ann="aiSAMPLES")
	cmds.separator(w=10,st= "none", p=row_3 )
	cmds.text('col',label='  Col ' , p=row_3 , ann="COLOR")
	cmds.separator(w=7,st= "none", p=row_3 )
	cmds.text(label='  iDef ' , p=row_3 , ann="ILLUMINATES BY DEFAULT")
	cmds.separator(w=2,st= "none", p=row_3 )
	cmds.text(label=' eDif  ' , p=row_3, ann="EMIT DIFFUSE")
	cmds.text(label='  eSpe  ' , p=row_3 , ann="EMIT SPECULAR" )
	cmds.text(label=' ColT ' , ann="COLOR TEMPERATURE", p=row_3)
	row_2 = cmds.rowLayout ( 'rowCambiaColor',p=frame_1  , numberOfColumns=18 , h=30 ,bgc=[0.5,0.5,0.5])
	cmds.separator(p=row_2 ,w=20, st= "none")
	cmds.checkBox ('on_off' ,en=1, l='' , w=13 ,h=20 , changeCommand = onoff  , p=row_2  )
	cmds.separator(p=row_2 ,w=10, st= "none")
	cmds.floatField( 'intensity' ,  en = 0 , precision = 1,  w = 50 , changeCommand = setInt  ,  p = row_2 )
	cmds.floatField('aiExposure' , en=0, precision = 2, w=50 , changeCommand = setExp  , p = row_2 )
	cmds.floatField('aiRadius' , en=0,precision = 2,  w=50 , changeCommand = setRad , p = row_2 )
	cmds.floatField('aiAngle' , en=0,precision = 2, w=50 , changeCommand = setAng , p= row_2 )
	cmds.floatField('aiSamples' , en=0,precision = 2,  w=50 , changeCommand = setSamp  , p = row_2  )
	cmds.separator(w=12,st= "none", p=row_2 )
	cmds.colorSliderGrp( 'color' , en=1,  cw2 = (22, 0),co2=[5, 0],ct2=["both", "both"], changeCommand = setColor , p=row_2)
	cmds.separator(w=7,st= "none", p=row_2 )
	cmds.checkBox ('C_ilumDef' ,en=0, l='' , w=13 ,h=20 , changeCommand = setilumDef  , p=row_2  )
	cmds.separator(w=16,st= "none", p=row_2 )
	cmds.checkBox ('emitDiffuse' ,en=0, l='' , w=13 ,h=20 , changeCommand = setDif  , p=row_2 )
	cmds.separator(w=17,st= "none", p=row_2 )
	cmds.checkBox ('emitSpecular' ,en=0, l='' , w=13 ,h=20  , changeCommand = setSpec   , p=row_2 )
	cmds.separator(w=13,st= "none", p=row_2 )
	aiColorTemperatureSlider = cmds.colorSliderGrp( 'aiColorTemperature' , en=1, cw2 = (20, 0), changeCommand = setSamp , p=row_2)
	row_5 = cmds.rowLayout ( p=frame_1  , numberOfColumns=1 , h=1, cal=[1,"center"])
	cmds.radioCollection('radioAbsRel')
	rowDeColumnas=cmds.rowLayout (nc=2,co2=[170,0],ct2=["left", "left"], p=row_5 ,h=30)
	row_AbsRel = cmds.columnLayout( p = rowDeColumnas)
	cmds.radioCollection('absrelRadio')
	cmds.radioButton( 'A',label='ABSOLUTO',sl=1,ann="ABSOLUTO",cl='radioAbsRel',onc='cmds.rowLayout("rowCambiaColor",e=1,bgc=[0.5,0.5,0.5])')
	row_ventanaCrearLuz = cmds.columnLayout( p = rowDeColumnas )
	cmds.radioCollection()
	cmds.radioButton('R', label='RELATIVO', ann="RELATIVO",cl='radioAbsRel', onc='cmds.rowLayout("rowCambiaColor",e=1,bgc=[0.18,0.65,0.72])')
	cmds.window('winMLuces', e=1 , height= 370, w=500)
	cmds.showWindow(win)
ultimoOrden="luz" #VARIABLE LOCAL PARA EL SWITCH DEL ORDEN DE LAS LUCES
orden = {"luz":0,"tipo":0,"grupo":0} #DICCIONARIO PARA SABER SI LAS VECES DE TOCAR EL BOTON SON PARES O INPARES
