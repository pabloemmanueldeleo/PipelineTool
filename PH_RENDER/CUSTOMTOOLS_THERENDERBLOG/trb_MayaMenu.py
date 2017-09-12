import maya.cmds as cmds
import maya.mel as mel


def customMayaMenu():
	gMainWindow = mel.eval('$temp1 = $gMainWindow')

	CustomMenu = cmds.menu('CustomMenu',parent=gMainWindow, label='Custom Tools',to=1)
	ToolBar = cmds.menuItem(parent=CustomMenu, label= 'Toolbar Tools',c=callTools)
	#vprender = cmds.menuItem(parent=CustomMenu, label= 'Viewport Render',c=viewportRender)


def callTools(*args):
	import customTools_therenderblog
	reload(customTools_therenderblog)
	customTools_therenderblog.UI()

"""
def viewportRender(*args):

	if cmds.pluginInfo("viewportRender.mll",q=1,l=1) == False:
		cmds.loadPlugin("viewportRender.mll")

	if cmds.contextInfo('ViewportRenderContext1',ex=1) == False:
		cmds.ViewportRenderContext()

	cmds.setToolTo('ViewportRenderContext1')
"""