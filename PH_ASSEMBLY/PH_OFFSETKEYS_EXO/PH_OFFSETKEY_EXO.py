import maya.cmds as cmds
global UI
UI={}
UI['win']='PH_OFFSET_KEY_EXO'
v=' v0.5'
if cmds.window (UI['win'],ex=1)==True:
    cmds.deleteUI (UI['win'])

# UI
cmds.window (UI['win'],t=UI['win']+v , s=0,resizeToFitChildren=1)
cmds.columnLayout(bgc=[0.23,0.23,0.23],cw=300,columnAlign="center",columnAttach=["both",1 ])
cmds.text (" LISTA EXOCORTEX ",align='left')
UI['scroll'] = cmds.textScrollList( numberOfRows=5, allowMultiSelection=True, showIndexedItem=8 )
cmds.separator(style="none",h=15)
cmds.rowLayout(numberOfColumns=10)
cmds.separator(style="none",w=5)
cmds.text (" IN: ")
UI['in']=cmds.intField( 'in',w=60 )
cmds.text (" OUT: ")
UI['out']=cmds.intField( 'out' ,w=60 )
cmds.text (" OFFSET: ")
UI['offset']=cmds.intField( 'offset' , value=0  ,w=60 )
cmds.button (l='offset')
cmds.window (UI['win'],e=1,resizeToFitChildren=1)
cmds.showWindow (UI['win'])
refreshExo()

def listaExocortex():
	global UI
	dicc={}
	listNodeExo=[]
	exoAfile=cmds.ls(type='ExocortexAlembicFile')
	for exo in exoAfile:

		listC=cmds.listConnections(exo,connections=True)
		fileName=cmds.getAttr(exo+'.fileName')
		for n in listC:
			if cmds.nodeType(n)=='ExocortexAlembicTimeControl':
				listNodeExo.append(n)
				dicc[exo]=[n,fileName]
		return dicc

def refreshExo(*args):
	global UI
	cmds.textScrollList(UI['scroll'],edit=True,append=listaExocortex().keys())
	nameFile=cmds.listAttr(n)
	inTime=cmds.getAttr(n+'.inTime')
	timeUnit=cmds.getAttr(n+'.timeUnit')
	factor=cmds.getAttr(n+'.factor')
	offset=cmds.getAttr(n+'.offset')
	factor=cmds.getAttr(n+'.loopStart')
	factor=cmds.getAttr(n+'.loopEnd')

def refreshTimeLine():
	cmds.get


frameInicial= 99999
frameFinal=0
for i in range (len(s)):
	#conecciones = cmds.listConnections (source=1)
	if cmds.keyframe (s[i] , q=1 , keyframeCount=1 ) != 0:
		keysQ = cmds.keyframe (s[i] , q=1)
		keysQ.sort()
		if keysQ[0] < frameInicial:
			frameInicial = keysQ[0]
		if keysQ[-1] > frameFinal:
			frameFinal = keysQ[-1]
if frameInicial== 99999 and frameFinal==0:
	frameInicial=0
	frameFinal=0


def calculaRango(*args):
    s=cmds.ls(sl=1)
    frameInicial= 99999
    frameFinal=0
    for i in range (len(s)):
		keysQ = cmds.keyframe (s[i] , q=1)
		keysQ.sort()
		if keysQ[0] < frameInicial:
			frameInicial = keysQ[0]
		if keysQ[-1] > frameFinal:
			frameFinal = keysQ[-1]
    if frameInicial== 99999 and frameFinal==0:
        frameInicial=0
        frameFinal=0
    cmds.intField( 'in' , e=1 , value=frameInicial)
    cmds.intField( 'out' , e=1 , value=frameFinal)

def offset(*args):
    frameIn = cmds.intField( 'in' , q=1 , value=1)
    frameOut = cmds.intField( 'out' , q=1 , value=1)
    frameOffset = cmds.intField( 'offset' , q=1 , value=1)
    seleccion = cmds.ls (sl=1,long=1,r=1)
    cmds.keyframe(edit=True,relative=True,timeChange=frameOffset,time=(frameIn,frameOut))
