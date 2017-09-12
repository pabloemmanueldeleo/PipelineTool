import maya.cmds as mc
'''
#AOV NECESARIOS
listNameMSK={'aiAOV_MSK_ECO'    : 'MSK_ECO',
			 'aiAOV_MSK_BOULDER': 'MSK_BOULDER',
			 'aiAOV_MSK_BUSH'   : 'MSK_BUSH',
			 'aiAOV_MSK_GRASS'  : 'MSK_GRASS',
			 'aiAOV_MSK_LEAVES' : 'MSK_LEAVES',
			 'aiAOV_MSK_PLANTS' : 'MSK_PLANTS',
			 'aiAOV_MSK_ROCKS'  : 'MSK_ROCKS',
			 'aiAOV_MSK_STICKS' : 'MSK_STICKS',
			 'aiAOV_MSK_TREES'  : 'MSK_TREES'
			 }
#Se le pasa un array
crearAovMsk(listNameMSK)
'''

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

def crearAovMsk(listNameMSK={None}):
	mc.select(cl=1)
	IDSHD='ID__SHD'
	if not mc.objExists(IDSHD):
		node=mc.createNode("aiUtility",name=IDSHD)
		mc.setAttr(node+'.shadeMode', 2)
		mc.setAttr(node+'.colorMode', 21)
		print "Ya existe el nodo "+ IDSHD
	else:
		print "Ya existe el nodo "+ IDSHD

	for AOV,NAMEAOV in listNameMSK.items():
		mc.select(cl=1)
		currentAOV = mc.getAttr( 'defaultArnoldRenderOptions.aovList',size=True)
		#currentAOV = currentAOV+1
		if not mc.objExists(str(AOV)):
			node=''
			node = mc.createNode('aiAOV',name=AOV)
			if node:
				print 'Se creo el aov ' + node
				mc.connectAttr( AOV+'.message','defaultArnoldRenderOptions.aovList['+ str(currentAOV) +']', f=True)
				mc.setAttr ( AOV+'.type', 5)
				mc.setAttr ( AOV+'.name', NAMEAOV, type='string')
				mc.connectAttr ('defaultArnoldDriver.message' , AOV+'.outputs[0].driver',f=True)
				mc.connectAttr ('defaultArnoldFilter.message' , AOV+'.outputs[0].filter',f=True)
			if not mc.objExists(NAMEAOV+'__AIWTC'):
				nodeWTC=''
				nodeWTC=mc.createNode( 'aiWriteColor', n=NAMEAOV+'__AIWTC' )
				print 'Se creo el aov ' + nodeWTC
				mc.setAttr( nodeWTC+'.blend',1)
				mc.setAttr( str(nodeWTC)+'.aovName', NAMEAOV, type='string')
				if not mc.isConnected(nodeWTC+'.outColor',AOV+'.defaultValue'):
					mc.connectAttr(nodeWTC+'.outColor',AOV+'.defaultValue', f=True)
				mc.select(cl=1)
		else:
			print 'Ya existe el nodo ' + AOV
