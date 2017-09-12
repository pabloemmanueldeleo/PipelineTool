'''
Ejemplo de utilidad de clases.
'''
import maya.cmds as cmds
class standinTools(object):
	def __init__(self):
		self._wDock='STANDIN_TOOLS'
		self._wWin='_STANDIN_TOOLS_WIN'
		#check to see if our window exists
		if mc.dockControl(self._wDock, exists=True):
			mc.deleteUI(self._wDock)
		# window
		self._wWin=mc.window(t=self._wWin,width=100)
		# layout
		mc.columnLayout( adjustableColumn=True)
		""" controls """
		mc.button(l='SELECCIONAR', c=self.seleccionarTodos,bgc=[8,4,1],width=100,height=100)
		mc.button(l='VIEWPORT WIREFRAME', c=self.wireframe)
		mc.button(l='VIEWPORT BOUNDING_BOX', c=self.boundingBox)
		mc.button(l='OVER STANDIN SHD', c=self.boundingBox,bgc=[8,4,1])
		mc.setParent('..')
		mc.columnLayout( adjustableColumn=True )
		mc.checkBox( label='Primary Visibility' )
		#mc.checkBox( label='Cast Shadows',offCommand=self.castsShadows(onOff=0),onCommand=self.castsShadows(onOff=1) )
		mc.checkBox( label='Receive Shadows' )
		#show dock con window
		allowedAreas = ['right', 'left']
		mc.dockControl( self._wDock, area='left', content=self._wWin, allowedArea=allowedAreas,width=100 )

	def boundingBox(self,*args):
		seleccion=mc.ls(selection=1)
		for sel in seleccion:
			mc.setAttr(sel+'.mode', 0)

	def wireframe(self,*args):
		seleccion=mc.ls(selection=1)
		for sel in seleccion:
			mc.setAttr(sel+'.mode', 3)

	def seleccionarTodos(self,*args):
		seleccion=mc.ls(type='aiStandIn')
		mc.select(seleccion)


	def castsShadows(self,onOff=1):
		seleccion=mc.ls(type='aiStandIn')
		if onOff==1:
			for sel in seleccion:
				mc.setAttr(sel+'.castsShadows', 1)
		if onOff==0:
			for sel in seleccion:
				mc.setAttr(sel+'.castsShadows', 0)
standinTools()
