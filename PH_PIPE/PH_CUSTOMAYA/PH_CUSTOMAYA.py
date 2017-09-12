import maya.cmds as cmds
class BOTONERA(object):
	def __init__(self):
		cmds.setParent("MayaWindow|toolBar1|MainStatusLineLayout|formLayout5|flowLayout1")
		self.myButton0 = cmds.iconTextButton ( style='iconOnly',image1='M:/PH_SCRIPTS/ICONS/OUTLINER.png',c=self.outLinerW)
		self.myButton2 = cmds.iconTextButton ( style='iconOnly',image1='M:/PH_SCRIPTS/ICONS/NODEEDITOR.png',c=self.nodeEditorW)
		self.myButton3 = cmds.iconTextButton ( style='iconOnly', image1='M:/PH_SCRIPTS/ICONS/GRAPHEDITOR.png', c=self.GraphEditorW)
		self.myButton4 = cmds.iconTextButton ( style='iconOnly',image1='M:/PH_SCRIPTS/ICONS/CAMERASEQUENCER.png',c=self.SequenceEditorW)
		self.myButton5 = cmds.iconTextButton ( style='iconOnly',image1='M:/PH_SCRIPTS/ICONS/NAMESPACEEDITOR.png', c=self.NamespaceEditorW)
		self.myButton6 = cmds.iconTextButton ( style='iconOnly', image1='M:/PH_SCRIPTS/ICONS/PLUGINMANAGER.png', c=self.PluginManagerW)
		self.myButton = cmds.iconTextButton ( style='iconOnly',image1='hypergraph.png', c=self.HypershadeWindowW)

	def outLinerW(self,*args):
		cmds.OutlinerWindow()

	def nodeEditorW(self,*args):
		cmds.NodeEditorWindow()

	def GraphEditorW(self,*args):
		cmds.GraphEditor()

	def SequenceEditorW(self,*args):
		cmds.SequenceEditor()

	def NamespaceEditorW(self,*args):
		cmds.NamespaceEditor()

	def PluginManagerW(self,*args):
		cmds.PluginManager()

	def HypershadeWindowW(self,*args):
		cmds.HypershadeWindow()
B=BOTONERA()
