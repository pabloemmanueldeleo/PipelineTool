import maya.cmds as cmds
def GUI():
  winName="myWindow"

  if ( cmds.window(winName,exists=True)):
  cmds.deleteUI(winName)

  cmds.window(winName,title='mesh/shader connector',w=200,h=500)
  cmds.window(winName,q=True,wh=True)

  cmds.rowLayout("obj,shd",nc=2,w=200,h=200)
  cmds.columnLayout( adj=True, columnAttach=('left', 5), rowSpacing=10, columnWidth=250 )
  cmds.textScrollList('obj')
  cmds.textScrollList('shd')
  cmds.textFieldButtonGrp('obj',bl='Import Object', text='Select Object',ed=False, bc='selMultipleObjects()')
  cmds.textFieldButtonGrp('shd',bl='Refresh Shaders', text='Refresh Shaders',ed=False, bc='shadeGrps()')
  cmds.button('Connect()',l='Connect')
  cmds.showWindow()

GUI()
def selectSHD():
    objName=cmds.ls(sl=1)
    myShapeNode = cmds.listRelatives(objName, children=True, shapes=True)
    mySGs = cmds.listConnections(myShapeNode,type='shadingEngine')
    surfaceShader = cmds.listConnections(mySGs[0] + '.surfaceShader')
    cmds.select(surfaceShader)

def selObjName():
  sel=cmds.ls(sl=True)[0]
  cmds.textFieldButtonGrp('obj',e=True,text=sel)


def selMultipleObjects():
  sel=cmds.ls(sl=True)
  cmds.textScrollList('obj',e=True,ra=True)
  cmds.textScrollList('obj',e=True,numberOfRows=len(sel)+10, allowMultiSelection=True,
       append=sel)

def shadeGrps():
  Shader=cmds.ls(mat=True)
  cmds.textScrollList('shd',e=True,ra=True)
  cmds.textScrollList('shd',e=True,numberOfRows=10,append=Shader)

def Connect():
  cmds.shadingConnection( 'shd', e=True, cs=0 )
  cmds.shadingConnection( 'obj', q=True, cs=True )
