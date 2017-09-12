import maya.cmds as mc
import mtoa.aovs as aovs
'''
shaderType=''
shrArnold=cmds.listNodeTypes( 'rendernode/Arnold', ex='shader' )
for type in shrArnold:
    shaderType+=str(type)+','
shaderArnold=mc.ls(type=[shaderType[:-1]])
'''
#arg1=name ShaderGroup
#arg2=name Shading
#arg3=name AOV
#funcion= conecta el outColor del shader con el aov name.
def connectSHDtoAOV(SHDG=None,SHDIN=None,AOV=None):
    #Nodos contemplados de arnold
    shaderArnold=mc.ls(type=['aiAmbientOcclusion','aiUtility','aiWriteColor','aiStandard','alSurface'])
    SHD=''

    for shd in shaderArnold:
        if str(shd) == SHDIN:
            SHD=SHDIN

    if SHD:
        shadingGroup = SHDG
        numOfCustomAOVs = mc.getAttr(shadingGroup+'.aiCustomAOVs', size=1)
        #Conecto si existen
        for aov in range(numOfCustomAOVs):
            AOVNAME=cmds.getAttr(shadingGroup+'.aiCustomAOVs['+str(aov)+'].aovName')

            if not mc.isConnected(str(SHD)+'.outColor',shadingGroup+'.aiCustomAOVs['+str(aov)+'].aovInput')==True:
                if AOV in AOVNAME:
                    if not mc.isConnected(str(SHD)+'.outColor',shadingGroup+'.aiCustomAOVs['+str(aov)+'].aovInput')==False:
                        mc.connectAttr(str(SHD)+'.outColor', shadingGroup+'.aiCustomAOVs['+str(aov)+'].aovInput')
                        print 'Se conecto "'+str(SHD)+'" con el aov "'+ str(AOV)+'".'
                    else:
                        print 'Ya existe una conexion con "'+str(SHD)+'" y el aov "'+ str(AOV)+'".'
            else:
                mc.warning('YA EXISTE UNA CONEXION CON EL AOV "'+str(AOV)+'".')
    else:
        mc.warning('No se encontro el ' +str(SHDIN))

objs=[]
objs=mc.ls(sl=1)
#Conecta los objetos seleccionados segun su shdGroup creando un MASK y luego conecto los AOV
if objs:
    for obj in objs:
        myShapeNode = mc.listRelatives(obj, children=True, shapes=True)
        if not myShapeNode==None:
            mySGs = mc.listConnections(myShapeNode,type='shadingEngine')
            for sg in mySGs:
                surfaceShader = mc.listConnections(str(sg) + '.surfaceShader')[0]
                if mc.connectionInfo(str(surfaceShader)+'.opacity',sourceFromDestination=True):
                    alpha=mc.connectionInfo(str(surfaceShader)+'.opacity',sourceFromDestination=True)
                    #Conexion OCCLUSION__SHD
                    if mc.objExists('OCCLUSION__SHD'):
                        #Creacion de nodos
                        NAMENODE=str(obj)+'_AOMSK'+'__AIWC'
                        if not mc.objExists(NAMENODE):
                            #Creo nodo nuevo para AO
                            AIWCNODE=mc.createNode('aiWriteColor', name=NAMENODE)
                            print 'Se creo el '+ str(AIWCNODE)+'\n'
                        else:
                            print 'Ya existe '+str(NAMENODE)
                        if not mc.isConnected(str(alpha),str(AIWCNODE)+'.input')==True:
                            mc.connectAttr(str(alpha),str(AIWCNODE)+'.input')
                        else:
                            print 'Ya tiene una conexion con '+str(alpha)+' entre '+ str(AIWCNODE)+'.input'
                        if not mc.isConnected('OCCLUSION__SHD.outColor',str(AIWCNODE)+'.beauty'):
                            mc.connectAttr('OCCLUSION__SHD.outColor',str(AIWCNODE)+'.beauty')
                        else:
                            print 'Ya tiene una conexion con OCCLUSION__SHD.outColor'+' entre '+ str(AIWCNODE)+'.beauty'
                        mc.setAttr( AIWCNODE+'.blend', 1)
                        mc.setAttr( AIWCNODE+'.aovName','OCCLUSION', type='string')
                        #conect to aov
                        connectSHDtoAOV(sg,AIWCNODE,'OCCLUSION')
                    else:
                        mc.warning('Fijate el shader con el nombre OCCLUSION__SHD por que no lo vi por aqui.')

                    #Conexion ID__SHD
                    if mc.objExists('ID__SHD'):
                        #Creacion de nodos
                        NAMENODEID=str(obj)+'_IDMSK'+'__AIWC'
                        if not mc.objExists(NAMENODEID):
                            #Creo nodo nuevo para ID
                            AIWCNODEID=mc.createNode('aiWriteColor', name=NAMENODEID)
                            print 'Se creo el '+ str(AIWCNODEID)+'\n'
                        else:
                            print 'Ya existe '+str(AIWCNODEID)
                        if not mc.isConnected(str(alpha),str(AIWCNODEID)+'.input'):
                            mc.connectAttr(str(alpha),AIWCNODEID+'.input')
                        else:
                            print 'Ya tiene una conexion con '+str(alpha)+' entre '+ str(AIWCNODEID)+'.input'
                        if not mc.isConnected('ID__SHD.outColor',str(AIWCNODEID)+'.beauty'):
                            mc.connectAttr('ID__SHD.outColor',str(AIWCNODEID)+'.beauty')
                        else:
                            print 'Ya tiene una conexion con OCCLUSION__SHD.outColor'+' entre '+ str(AIWCNODEID)+'.beauty'
                        mc.setAttr( AIWCNODEID+'.blend', 1)
                        mc.setAttr( AIWCNODEID+'.aovName','OBJECT_ID', type='string')
                        #conect to aov
                        connectSHDtoAOV(sg,str(AIWCNODEID),'OBJECT_ID')
                    else:
                        mc.warning('Fijate el shader con el nombre OBJECT_ID por que no lo vi por aqui.')
                else:
                    mc.warning('El '+str(surfaceShader[0])+' no contiene informacion en el alpha channel.')
        else:
            mc.warning('La seleccion: '+str(obj)+' no contiene ShapeNode. Selecciona geometrias')
else:
    mc.warning('Selecciona un objeto.')
