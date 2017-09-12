import maya.cmds as cmds

def menuImport():

	if cmds.menu('CustomMenu',q=1,ex=1):
		print 'menu loaded'
	else:
		import trb_MayaMenu
		trb_MayaMenu.customMayaMenu()


scriptJobNum = cmds.scriptJob(event=["NewSceneOpened",menuImport])