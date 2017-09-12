import maya.cmds as mc

def conexionConAOV():
    aov_list=0
    #Name nodes variables
    AOVOBJECTID='aiAOV_OBJECT_ID'
    AOVOCCLUSION='aiAOV_OCCLUSION'
    AOSHD='AO__SHD'
    IDSHD='ID__SHD'
    #Creacion de nodos
    if not mc.objExists(AOVOBJECTID):
        mc.createNode('aiAOV', name=AOVOBJECTID)
        print "Se creo aiAOV_OBJECT_ID \n"
    else:
        print "Ya existe aiAOV_OBJECT_ID"

    if not mc.objExists( AOVOCCLUSION ):
        mc.createNode('aiAOV',name=AOVOCCLUSION)
        print "Se creo aiAOV_OCCLUSION \n"
    else:
        print "Ya existe aiAOV_OCCLUSION"


    if not mc.objExists(AOSHD):
        mc.createNode('aiAmbientOcclusion',name=AOSHD)
        print 'Se creo el AO__SHD \n'
    else:
        print 'Ya existe AO__SHD'

    if not mc.objExists(IDSHD):
        mc.createNode('aiUtility',name=IDSHD)
        mc.setAttr(IDSHD+'.shadeMode', 2)
        mc.setAttr(IDSHD+'.colorMode', 21)
        print 'Se creo el ID__SHD \n'
    else:
        print 'Ya existe ID__SHD'
    mc.select(cl=1)
    aov_list = mc.getAttr('defaultArnoldRenderOptions.aovList',size=True)

    someInListID=0
    for aov in range(aov_list):
        #mc.listConnections('defaultArnoldDriver.message')
         if mc.isConnected(AOVOBJECTID+'.message','defaultArnoldRenderOptions.aovList[' + str(aov) + ']'):
            someInListID+=1
    #Conexion con ID
    if  someInListID<=0:
        mc.connectAttr( AOVOBJECTID+'.message','defaultArnoldRenderOptions.aovList[' + str(aov_list) + ']', force=True)
        mc.setAttr( AOVOBJECTID+'.type',5)
        mc.setAttr( AOVOBJECTID+'.name','OBJECT_ID', type='string')
        mc.connectAttr('defaultArnoldDriver.message', AOVOBJECTID+'.outputs[0].driver',force=True)
        mc.connectAttr('defaultArnoldFilter.message', AOVOBJECTID+'.outputs[0].filter',force=True)
        mc.connectAttr( IDSHD+'.outColor', AOVOBJECTID+'.defaultValue',force=True)
        mc.select(cl=1)
    else:
        print 'Ya existe la conexion entre AOV y ID'


    aov_list = mc.getAttr('defaultArnoldRenderOptions.aovList',size=True)
    someInListAO=0
    for aov in range(aov_list):
        #mc.listConnections('defaultArnoldDriver.message')
         if mc.isConnected(AOVOCCLUSION+'.message','defaultArnoldRenderOptions.aovList[' + str(aov) + ']'):
            someInListAO+=1
    #Conexion con AO
    if  someInListAO<=0:
        mc.connectAttr( AOVOCCLUSION+'.message','defaultArnoldRenderOptions.aovList[' + str(aov_list) + ']', force=True)
        mc.setAttr(AOVOCCLUSION+'.type',5)
        mc.setAttr(AOVOCCLUSION+'.name','OCCLUSION', type='string')
        mc.connectAttr('defaultArnoldDriver.message', AOVOCCLUSION+'.outputs[0].driver',force=True)
        mc.connectAttr('defaultArnoldFilter.message', AOVOCCLUSION+'.outputs[0].filter',force=True)
        mc.connectAttr(AOSHD+'.outColor', AOVOCCLUSION+'.defaultValue',force=True)
        mc.select(cl=1)
    else:
        print 'Ya existe la conexion entre AOV y AO'
#Cargo el pluging de arnold si no esta cargado
if mc.pluginInfo('mtoa.mll',q=True, l=True ):
    mc.setAttr('defaultRenderGlobals'+'.currentRenderer', 'arnold', type='string')
    print 'Arnold it is ON'
else:
    mc.loadPlugin( 'mtoa.mll' )
    print 'Arnold ON'

if not mc.getAttr('defaultRenderGlobals'+'.currentRenderer') == 'arnold':
    #Pongo como render el arnold
    mc.setAttr('defaultRenderGlobals'+'.currentRenderer', 'arnold', type='string')
    print 'Arnold se puse como render predefinido'

#get aov defauld
if mc.getAttr('defaultRenderGlobals'+'.currentRenderer') == 'arnold':
    try:
        aov_list = mc.getAttr('defaultArnoldRenderOptions.aovList',size=True)
    except:
        mc.setAttr('defaultRenderGlobals'+'.currentRenderer', 'arnold', type='string')
else:
    print 'Primero hay que setear arnold como motor principal de render'
mc.select(cl=1)

conexionConAOV()
