import maya.cmds
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
#AOV NECESARIO
listNameMSK={'aiAOV_MSK_ECO'    : 'MSK_ECO',
			 'aiAOV_MSK_BOULDER': 'MSK_BOULDER',
			 'aiAOV_MSK_BUSH'   : 'MSK_BUSH',
			 'aiAOV_MSK_GRASS'  : 'MSK_GRASS',
			 'aiAOV_MSK_LEAVES' : 'MSK_LEAVES',
			 'aiAOV_MSK_PLANTS' : 'MSK_PLANTS',
			 'aiAOV_MSK_ROCKS'  : 'MSK_ROCKS',
			 'aiAOV_MSK_STICKS' : 'MSK_STICKS',
			 'aiAOV_MSK_TREES'  : 'MSK_TREES'}

crearAovMsk(listNameMSK)

def crearAovMsk(listNameMSK={None}):

IDSHD='ID__SHD'
if not cmds.objExists(IDSHD):
	node=cmds.createNode("aiUtility",name=IDSHD)
	cmds.setAttr(node+'.shadeMode', 2)
	cmds.setAttr(node+'.colorMode', 21)
	print "Ya existe el nodo "+ node
else:
	print "Ya existe el nodo "+ node

for AOV,NAMEAOV in listNameMSK.items():
	cmds.select(cl=1)
    try:
        currentAOV = cmds.getAttr( 'defaultArnoldRenderOptions.aovList',size=True)
    except:
        currentAOV = currentAOV+1
	if not cmds.objExists(str(AOV)):
		node = cmds.createNode('aiAOV',name=AOV)
		cmds.connectAttr( AOV+'.message','defaultArnoldRenderOptions.aovList['+ str(currentAOV) +']', f=True)
		cmds.setAttr ( AOV+'.type', 5)
		cmds.setAttr ( AOV+'.name', NAMEAOV, type='string')
		cmds.connectAttr ('defaultArnoldDriver.message' , AOV+'.outputs[0].driver',f=True)
		cmds.connectAttr ('defaultArnoldFilter.message' , AOV+'.outputs[0].filter',f=True)
		cmds.select(cl=1)
	else:
		print 'Ya existe el nodo' + AOV
