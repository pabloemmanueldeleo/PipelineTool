# -*- encoding: utf-8 -*-
import maya.cmds as mc
import maya.mel as mel

#Busco el shaderGroup de un material
def obtenerSG(shader=None):
	if shader:
		if mc.objExists(shader):
			sgq = mc.listConnections(shader, d=True, et=True, t='shadingEngine')
		if sgq:
			return sgq[0]
	return None

#Asigna material a una lista de objetos.
def asignarSHDaListaObjetos(objList=None, shader=None):
	shaderSG = obtenerSG(shader)
	if objList:
		if shaderSG:
			try:
				mc.sets(objList, e=True, forceElement=shaderSG)
			except:
				pass
		else:
			print 'NO ENCONTRO EL SHADING GROUP.'
	else:
		print 'CHABON SELECCIONA UNO O MAS OBJETOS.'

#Override de render layer pasandole solo un material.
def renderLayerConTodoUnMaterial(layerName=None,mat=None):
    mel.eval('hookShaderOverride('+'"'+layerName+'"'+',"",'+'"'+str(mat)+'"'+');')

#Seteo y hace Override de atributos del render options de arnold
def overrideArnoldRenderOptions(renderLayer=None,attr=None,value=None):
    mc.editRenderLayerAdjustment('defaultArnoldRenderOptions.'+str(attr), layer=renderLayer)
    mc.setAttr('defaultArnoldRenderOptions.'+str(attr), value)


def createAov(nameNodoAov=None,nombreAOV=None):
	aovLGRP=cmds.createNode('aiAOV',name=nombreAOV)
	cmds.setAttr(aovLGRP)

	aov_list = mc.getAttr('defaultArnoldRenderOptions.aovList',size=True)

	someInListID=0
	for aov in range(aov_list):
		#mc.listConnections('defaultArnoldDriver.message')
		 if mc.isConnected(aovLGRP+'.message','defaultArnoldRenderOptions.aovList[' + str(aov) + ']'):
		    someInListID+=1
	#Conexion con ID
	if  someInListID<=0:
	    mc.connectAttr( aovLGRP+'.message','defaultArnoldRenderOptions.aovList[' + str(aov_list) + ']', force=True)
	    mc.setAttr( aovLGRP+'.type',5 )
	    mc.setAttr( aovLGRP+'.name',nombreAOV, type='string' )
	    mc.connectAttr('defaultArnoldDriver.message', aovLGRP+'.outputs[0].driver',force=True)
	    mc.connectAttr('defaultArnoldFilter.message', aovLGRP+'.outputs[0].filter',force=True)
	    #mc.connectAttr( IDSHD+'.outColor', nameNodoAov+'.defaultValue',force=True)
	    mc.select(cl=1)
	else:
	    print 'Ya existe la conexion entre '+nombreAOV

def crearShadowShd():
	msg='Si no existe el SHADOW__SHD no podras seguir.\n¿Quieres que lo cree por ti?'
	mc.warning(msg)
	configButtom=mc.confirmDialog(title='SHADOW__SHD',message=msg, button=['Sipi','No'], defaultButton='Sipi', cancelButton='No', dismissString='No',icon='icon')
	if configButtom == 'Sipi':
	    nombreNodoaiaov = mc.createNode( "alSurface", n= 'SHADOW__SHD')
	    mc.setAttr(nombreNodoaiaov+'.specular1Strength',0)
	if configButtom =='No':
	    mc.warning('Se cancelo la creacion del SHADOW__SHD')
	return configButtom


def renderLayerShadow(*args):

	mat="SHADOW__SHD"
	layerName="CHARS_SHADOWS_"
	states=[False,False,False,False,False,False]

	if mc.objExists(mat):
		mc.setAttr(mat+'.specular1Strength',0)
		states[0]=True

		listaSTANDIN=mc.ls(type='aiStandIn')
		listaMESH=mc.ls(type='mesh')
		listAOVs=mc.ls(type='aiAOV')

		if mc.objExists(layerName):
			mc.warning('Ya se creo el renderLayer '+layerName)
			mc.editRenderLayerGlobals( currentRenderLayer=layerName )
			states[1]=True
		else:
			#creo el renderLayer con mesh y standin de toda la escena.
			mc.select(listaSTANDIN,listaMESH)
			RLAY=mc.createRenderLayer( name=layerName,g=False)
			mc.select(cl=1)
			mc.warning('Ahi te cree un renderLayer llamado ' + layerName)
			mc.editRenderLayerGlobals( currentRenderLayer=layerName )
			states[1]=True

		#seteo que el mesh no emita sombras ni reciba
		if listaMESH:
			for MSH in listaMESH:
			    mc.setAttr(str(MSH)+'.castsShadows',0)
			    mc.setAttr(str(MSH)+'.receiveShadows',1)
			    mc.setAttr(str(MSH)+'.primaryVisibility',1)
			states[2]=True

		#seteoque le de bola a los shaders del mismo standing, que no genere sombras
		if listaSTANDIN:
			for STANDIN in listaSTANDIN:
			    mc.setAttr(str(STANDIN)+'.overrideShaders', 1)
			    mc.setAttr(str(STANDIN)+'.castsShadows', 0)
			    mc.setAttr(str(STANDIN)+'.overrideCastsShadows', 1)
			states[3]=True

		if listAOVs:
			copado1=False
			copado2=False
			#Set AOVS visibility
			for AOV in listAOVs:
			    mc.setAttr(str(AOV)+'.enabled',0)
			for AOV in listAOVs:
				if 'shadow' in AOV:
					mc.setAttr(str(AOV)+'.enabled',1)
					copado1=True
				if 'OCCLUSION' in AOV:
					mc.setAttr(str(AOV)+'.enabled',1)
					copado2=True
			if copado1 and copado2 == False:
				mc.warning('No encontre un aov con el nombre de shadow')
			states[4]=True
		else:
			mc.warning('No existe ningun aov creado.')

		if mc.objExists(layerName):
			#set Arnold Render Options
			overrideArnoldRenderOptions(layerName,'GIRefractionSamples',0)
			overrideArnoldRenderOptions(layerName,'GIDiffuseSamples',0)
			overrideArnoldRenderOptions(layerName,'GIGlossySamples',0)
			overrideArnoldRenderOptions(layerName,'GITotalDepth',0)
			overrideArnoldRenderOptions(layerName,'GIDiffuseDepth',0)
			overrideArnoldRenderOptions(layerName,'GIGlossyDepth',0)
			overrideArnoldRenderOptions(layerName,'GIReflectionDepth',0)
			overrideArnoldRenderOptions(layerName,'GIDiffuseDepth',0)
			overrideArnoldRenderOptions(layerName,'GIRefractionDepth',0)
			overrideArnoldRenderOptions(layerName,'GITotalDepth',0)
			states[5]=True
		else:
			mc.warning('No existe el layer '+layerName)

		#SI NO SE CUMPLEN TODAS LAS CONDICIONES NO SE AGREGARAN LOS ITEMS AL LAYER
		if states==[True,True,True,True,True,True]:
			#Aplico material a los standins
			asignarSHDaListaObjetos(listaSTANDIN,mat)
			#Aplico material a los meshes
			asignarSHDaListaObjetos(listaMESH,mat)
			#por las dudas hago un override al renderlayer con el material
			renderLayerConTodoUnMaterial(layerName,mat)
		else:
			states=[False,False,False,False,False,False]
	else:
		coco=crearShadowShd()
		if coco=='Sipi':
			renderLayerShadow()

def renderLayerLighting(*args):

	mat="SHADOW__SHD"
	layerName="CHARS_LIGHTS_"
	states=[False,False,False,False,False,False]

	if mc.objExists(mat):
		mc.setAttr(mat+'.specular1Strength',0)
		states[0]=True

		listaSTANDIN=mc.ls(type='aiStandIn')
		listaMESH=mc.ls(type='mesh')
		listAOVs=mc.ls(type='aiAOV')

		if mc.objExists(layerName):
			mc.warning('Ya se creo el renderLayer '+layerName)
			mc.editRenderLayerGlobals( currentRenderLayer=layerName )
			states[1]=True
		else:
			#creo el renderLayer con mesh y standin de toda la escena.
			mc.select(listaSTANDIN,listaMESH)
			RLAY=mc.createRenderLayer( name=layerName,g=False)
			mc.select(cl=1)
			mc.warning('Ahi te cree un renderLayer llamado ' + layerName)
			mc.editRenderLayerGlobals( currentRenderLayer=layerName )
			states[1]=True

		#seteo que el mesh no emita sombras ni reciba
		if listaMESH:
			for MSH in listaMESH:
			    mc.setAttr(str(MSH)+'.castsShadows',1)
			    mc.setAttr(str(MSH)+'.receiveShadows',1)
			    mc.setAttr(str(MSH)+'.primaryVisibility',1)
			states[2]=True

		#seteoque le de bola a los shaders del mismo standing, que no genere sombras
		if listaSTANDIN:
			for STANDIN in listaSTANDIN:
			    mc.setAttr(str(STANDIN)+'.overrideShaders', 1)
			    mc.setAttr(str(STANDIN)+'.castsShadows', 1)
			    mc.setAttr(str(STANDIN)+'.overrideCastsShadows', 1)
			states[3]=True

		if listAOVs:
			copado1=False

			#Set AOVS visibility
			for AOV in listAOVs:
			    mc.setAttr(str(AOV)+'.enabled',0)
			for AOV in listAOVs:
				if 'light_group' in AOV:
					mc.setAttr(str(AOV)+'.enabled',1)
					copado1=True
			if copado1 == False:
				mc.warning('No encontre un aov con el nombre de shadow')
			states[4]=True
		else:
			mc.warning('No existe ningun aov creado.')

		if mc.objExists(layerName):
			#set Arnold Render Options
			overrideArnoldRenderOptions(layerName,'GIRefractionSamples',0)
			overrideArnoldRenderOptions(layerName,'GIDiffuseSamples',0)
			overrideArnoldRenderOptions(layerName,'GIGlossySamples',0)
			overrideArnoldRenderOptions(layerName,'GITotalDepth',0)
			overrideArnoldRenderOptions(layerName,'GIDiffuseDepth',0)
			overrideArnoldRenderOptions(layerName,'GIGlossyDepth',0)
			overrideArnoldRenderOptions(layerName,'GIReflectionDepth',0)
			overrideArnoldRenderOptions(layerName,'GIDiffuseDepth',0)
			overrideArnoldRenderOptions(layerName,'GIRefractionDepth',0)
			overrideArnoldRenderOptions(layerName,'GITotalDepth',0)
			states[5]=True
		else:
			mc.warning('No existe el layer '+layerName)

		#SI NO SE CUMPLEN TODAS LAS CONDICIONES NO SE AGREGARAN LOS ITEMS AL LAYER
		if states==[True,True,True,True,True,True]:
			#Aplico material a los standins
			asignarSHDaListaObjetos(listaSTANDIN,mat)
			#Aplico material a los meshes
			asignarSHDaListaObjetos(listaMESH,mat)
			#por las dudas hago un override al renderlayer con el material
			renderLayerConTodoUnMaterial(layerName,mat)
		else:
			states=[False,False,False,False,False,False]
	else:
		coco=crearShadowShd()
		if coco=='Sipi':
			renderLayerLighting()


#selecciono la hiearchy dentro de la seleccion
def selectH(*args):
	geoH=[]
	listSel=[]
	objs=mc.ls(sl=1)
	for obj in objs:
		geos=mc.listRelatives(mc.listRelatives(obj,allParents=True,fullPath=True)[0],parent=True)
		for g in geos:
			chld=mc.listRelatives(g, allDescendents=True)
			for c in chld:
				geoH.append(c)
	mc.select(geoH)
	return geoH

#seteo los atributos shadow
def reciveS(*args):
	global switch
	sel=mc.ls(sl=1)
	if sel:
		for o in sel:
			mc.setAttr(o+'.castsShadows',1)
			mc.setAttr(o+'.receiveShadows',1)
			mc.setAttr(o+'.primaryVisibility',0)

#seteo los atributos shadow
def primaryV(*args):
	global switch
	sel=mc.ls(sl=1)
	if sel:
		for o in sel:
			mc.setAttr(o+'.castsShadows',1)
			mc.setAttr(o+'.receiveShadows',1)
			mc.setAttr(o+'.primaryVisibility',1)

def crearAttr(name=None,defauld=None,obj=None):
	if obj==None:
		sel=mc.ls(sl=1)
	else:
		sel=obj
	for s in sel:
		if mc.objectType(s) == 'directionalLight' or mc.objectType(s)=='pointLight' or mc.objectType(s)=='spotLight':
			attrNew=mc.addAttr(ln=name,at='long',dv=defauld)
			print 'Se creo un atributo nuevo para la luz llamado ' + attrNew
		else:
			mc.warning('Funciona si elegi el shape de una luz o varias')

def attr(*args):
	crearAttr('mtoa_constant_lightGroup',1)

#ventana de PH_MANAGER_RENDERLAYER
def winLayer():
	winRenderLayer='PH_MANAGER_RENDERLAYER'
	v=' v1.0'

	if mc.window(winRenderLayer, q=True, exists=True):
		mc.deleteUI(winRenderLayer)
	boxB=150
	boxB2=80
	boxB3=30
	verdemarino=(0.24,0.75,0.5)
	azul=(0.15,0.27,0.49)
	mc.window(winRenderLayer, title=winRenderLayer + v)
	mc.rowColumnLayout(numberOfRows=1)
	mc.rowColumnLayout(numberOfColumns=1)
	mc.separator(height=10, style='singleDash')
	mc.text(label='RENDER LAYERS')
	mc.separator(height=10, style='singleDash')
	mc.button(label='(CREAR) CHARS_SHADOW',c=renderLayerShadow,width=boxB,height=boxB2,backgroundColor=verdemarino)
	mc.button(label='(CREAR) CHARS_LIGHTS',c=renderLayerLighting,width=boxB,height=boxB2,backgroundColor=azul)
	mc.separator(height=10, style='singleDash')
	mc.text(label='SET GEO')
	mc.separator(height=10, style='singleDash')
	mc.button(label='SELECT HIEARCHY',c=selectH,annotation='Selecciona toda la jerarquía de la seleccion.',width=boxB2,height=boxB3)
	mc.separator(height=10, style='singleDash')
	mc.text(label='ATTRIBUTE SPREAD SHEET')
	mc.separator(height=10, style='singleDash')
	mc.button(label='RECEIVE SHADOW',c=reciveS,annotation='Prende: castsShadows,receiveShadows\nApaga: primaryVisibility',width=boxB2,height=boxB3)
	mc.button(label='PRIMARY VISIBILITY',c=primaryV,annotation='Prende: castsShadows,receiveShadows,primaryVisibility',width=boxB2,height=boxB3)
	mc.button(label='ADD ATTRIBUTE',c=attr,annotation='Te crea un atributo nuevo en las luces seleccionadas.',width=boxB2,height=boxB3)
	mc.showWindow(winRenderLayer)
