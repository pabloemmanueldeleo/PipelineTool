###################################
'''			IMPORTS				'''
###################################

import maya.cmds as cmds
try:
	import mtoa.aovs as aovs
except:
	cmds.warning('No se pude importar el modulo de arnold')

###################################
'''		FUCNIONES UTILES		'''
###################################

#Crea el tipo de nodo que quieras
def createSHD(nodo='',SHDname=''):
	if nodo and SHDname:
		if not cmds.objExists(SHDname):
			SHD=cmds.createNode( nodo, shared=True, n=SHDname )
			print "Se creo el tipo de nodo "+str(nodo)+'con el nombre '+SHDname
		else:
			cmds.warning('Nodo '+str(nodo)+' ya creado.')
	else:
		print 'Los argumentos estan mal.'
#CREA CONECTA COSAS
def conectar(nodo1=None,nodo2=None,ouput='',input=''):
	if not cmds.isConnected ( str(nodo1)+'.'+str(ouput), str(nodo2)+'.'+str(input) ):
		cmds.connectAttr( str(nodo1)+'.'+str(ouput), str(nodo2)+'.'+str(input), f=1 )
	else:
		cmds.warning("YA EXISTE UNA CONECCION CON"+str(nodo1)+'.'+str(ouput), str(nodo2)+'.'+str(input))

#CREO LOS AOVS QUE QUIERA
def crearAOV( AOVNAME ):
	#Name nodes variables
	aov='aiAOV_'+AOVNAME
	#Creacion de nodos
	if not cmds.objExists(aov):
		node=cmds.createNode('aiAOV', name=aov)
		return node
		print "Se creo " + aov
	else:
	    print "Ya existe " + aov

#CONECADOR DE AOV CON SHADER
def conectarAOVconShader(nodoAOV=None,nameAOV='',shd=None):
	if cmds.objExists(nodoAOV):
		aov_list=0
		cmds.select(cl=1)
		aov_list = cmds.getAttr('defaultArnoldRenderOptions.aovList',size=True)
		someInListID=0
		for aov in range(aov_list):
		     if cmds.isConnected(nodoAOV+'.message','defaultArnoldRenderOptions.aovList[' + str(aov) + ']'):
		        someInListID+=1
		#Conexion con AOV
		if  someInListID<=0:
		    cmds.connectAttr( nodoAOV+'.message','defaultArnoldRenderOptions.aovList[' + str(aov_list) + ']', force=True)
		    cmds.setAttr( nodoAOV+'.type',5)
		    if nameAOV=='':
				nameAOV=str(nodoAOV)
		    cmds.setAttr( nodoAOV+'.name',nameAOV, type='string')
		    cmds.connectAttr('defaultArnoldDriver.message', nodoAOV+'.outputs[0].driver',force=True)
		    cmds.connectAttr('defaultArnoldFilter.message', nodoAOV+'.outputs[0].filter',force=True)
		else:
			print 'Ya existe la conexion entre '+str(nodoAOV)
		if shd!=None:
			try:
				cmds.connectAttr( str(shd)+'.outColor', str(nodoAOV)+'.defaultValue',force=True)
				print 'Se conecto '+ str(shd)
			except:
				pass
		cmds.select(cl=1)
	else:
		print 'No existe el aov '+str(nodoAOV)

###################################################
'''			FUNCIONES DE CREACION Y SETEO		'''
###################################################

#CREO UN ALSURFACE
def crearShaderALSurface( SHD='', specS=None, nodo1R=0, nodo1G=0, nodo1B=0,*args ):
	#SHD='COCO',nodo1R=0, nodo1G=0, nodo1B=0
	if not cmds.objExists( SHD ):
		createSHD('alSurface',SHD)
	if not cmds.objExists(SHD+'GRP'):
		createSHD('shadingEngine',SHD+'GRP')
	if cmds.objExists(SHD) and cmds.objExists(SHD+'GRP'):
		conectar( SHD, SHD+'GRP', 'outColor', 'surfaceShader')
	try:
		if nodo1R or nodo1G or nodo1B !=0:
			cmds.setAttr(SHD+'.outColor', nodo1R, nodo1G, nodo1B, type='double3' )
		if specularStrength != None:
			cmds.setAttr(SHD+'.specular1Strength', specS )
	except:
		pass
#crear ShaderUtility
def crearShaderUtility(SHD='',shadeMode=2,colorMode=1):
	if not cmds.objExists(SHD):
		createSHD('aiUtility',SHD)
	if not cmds.objExists(SHD+'GRP'):
		createSHD('shadingEngine',SHD+'GRP')
	if cmds.objExists(SHD) and cmds.objExists(SHD+'GRP'):
		try:
			conectar( SHD, SHD+'GRP', 'outColor', 'surfaceShader')
			cmds.setAttr(SHD+'.shadeMode', shadeMode)
			cmds.setAttr(SHD+'.colorMode', colorMode)
		except:
			pass
#CREO UN AO
def crearShaderAO(SHD='', samples=1, farClip=75):
	if not cmds.objExists(SHD):
		createSHD('aiAmbientOcclusion',SHD)
	if not cmds.objExists(SHD+'GRP'):
		createSHD('shadingEngine',SHD+'GRP')
	if cmds.objExists(SHD) and cmds.objExists(SHD+'GRP'):
		conectar( SHD, SHD+'GRP', 'outColor', 'surfaceShader')
		try:
			cmds.setAttr( SHD+'.samples', 6  )
			cmds.setAttr( SHD+'.farClip', 75 )
		except:
			pass
def setArnoldSettings(*args):
	cmds.setAttr('defaultArnoldDriver.mergeAOVs', 1)
	print 'Se activo el Merge AOV.'

###########################################
'''			USO DE FUNCIONES			'''
###########################################

def packShaders():
	#SETEO DE ARNOLD PREVIO
	setArnoldSettings()

	#SHADERS DESEADOS ID
	crearShaderALSurface( 'RED__SHD'  , 1 , 0, 0 )
	crearShaderALSurface( 'GREEN__SHD', 0 , 1, 0 )
	crearShaderALSurface( 'BLUE__SHD' , 0 , 0, 1 )

	#SHADER DESADO SHADOW
	crearShaderALSurface( 'SHADOW__SHD' , specS=0)

	#SHADER DESEADO UTILITY
	crearShaderUtility( 'ID__SHD'   , 2 , 21 )
	crearShaderUtility( 'NORMAL__SHD',2 , 3 )

	#SHADER DESEADO AO
	crearShaderAO( 'AO__SHD', 6, 75 )

	#AOVS DECIADOS
	AOVS=['NORMAL', 'P', 'Z', 'direct_diffuse', 'direct_specular',
		  'reflection', 'refraction', 'sss','shadow_group_1','OCCLUSION','OBJECT_ID']

	#CONEXION AOV SIN SHADER
	for aov in AOVS:
		crearAOV(aov)
		conectarAOVconShader('aiAOV_'+str(aov),str(aov))

	#CONEXION AOV CON SHADER
	conectarAOVconShader('aiAOV_OBJECT_ID','OBJECT_ID','ID__SHD')
	conectarAOVconShader('aiAOV_OCCLUSION','OCCLUSION','AO__SHD')
	conectarAOVconShader('aiAOV_NORMAL','NORMAL','NORMAL__SHD')

def buttonPackShaders():
	if cmds.getAttr('defaultRenderGlobals.currentRenderer') == 'arnold':
		packShaders()
	else:
		cmds.warning('Necesitas configurar arnold como motor de render predeterminadoy pararte en la solapa de AOV.')
