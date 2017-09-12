import maya.cmds as c

def offsetKeysMain(*args):
    if c.window ('offsetVentanaPrincipal',ex=1)==True:
        c.deleteUI ('offsetVentanaPrincipal')
    # calcula rango de animacion
    s=c.ls(sl=1)
    frameInicial= 99999
    frameFinal=0
    for i in range (len(s)):
        #conecciones = c.listConnections (source=1)

    	if c.keyframe (s[i] , q=1 , keyframeCount=1 ) != 0:
    		keysQ = c.keyframe (s[i] , q=1)
    		keysQ.sort()
    		if keysQ[0] < frameInicial:
    			frameInicial = keysQ[0]
    		if keysQ[-1] > frameFinal:
    			frameFinal = keysQ[-1]
    if frameInicial== 99999 and frameFinal==0:
        frameInicial=0
        frameFinal=0

    # UI
    c.window ('offsetVentanaPrincipal',t="PH_OFFSET ANIMACION v1.0" , s=0,resizeToFitChildren=1)
    col_01 = c.columnLayout(bgc=[0.23,0.23,0.23],p='offsetVentanaPrincipal',cw=300,columnAlign="center",columnAttach=["both",1 ])
    c.separator(style="none",h=15)
    c.rowLayout(numberOfColumns=10,p='offsetVentanaPrincipal')
    c.separator(style="none",w=5)
    c.text (" IN: ")
    c.intField( 'in' , value=frameInicial ,w=60 )
    c.text (" OUT: ")
    c.intField( 'out' ,  value=frameFinal  ,w=60 )
    c.text (" OFFSET: ")
    c.intField( 'offset' , value=0  ,w=60 )
    c.separator(style="none",w=20)
    col_02 = c.columnLayout(bgc=[0.2,0.2,0.2],p='offsetVentanaPrincipal',cw=300,columnAlign="center",columnAttach=["both",1 ])
    row_02 = c.rowLayout(numberOfColumns=10,p=col_02)
    c.separator(style="none",w=15)
    c.iconTextButton ('b_selJerarquia',bgc=[0.15,0.15,0.15], w=70,style="textOnly",c="cmds.select(hierarchy=1)",ann="SELECCIONA LA JERARQUIA",l="JERARQUIA",p=row_02)
    c.separator(style="none",w=22)
    c.iconTextButton ('b_calcularRango',bgc=[0.15,0.15,0.15],w=70,c=calculaRango,style="textOnly",l="RANGO",ann="CALCULA IN/OUT",p=row_02)
    c.separator(style="none",w=22,p=row_02)
    c.iconTextButton ('b_offset',bgc=[0.15,0.15,0.15],w=70,c=offset,style="textOnly",l="OFFSET",ann="CORRE EL SCRIPT",p=row_02)

    c.window ('offsetVentanaPrincipal',e=1,resizeToFitChildren=1)
    c.showWindow ('offsetVentanaPrincipal')

def calculaRango(*args):
    s=c.ls(sl=1)
    frameInicial= 99999
    frameFinal=0
    for i in range (len(s)):
    	if c.keyframe (s[i] , q=1 , keyframeCount=1 ) != 0:
    		keysQ = c.keyframe (s[i] , q=1)
    		keysQ.sort()
    		if keysQ[0] < frameInicial:
    			frameInicial = keysQ[0]
    		if keysQ[-1] > frameFinal:
    			frameFinal = keysQ[-1]
    if frameInicial== 99999 and frameFinal==0:
        frameInicial=0
        frameFinal=0
    c.intField( 'in' , e=1 , value=frameInicial)
    c.intField( 'out' , e=1 , value=frameFinal)

def offset(*args):
    frameIn = c.intField( 'in' , q=1 , value=1)
    frameOut = c.intField( 'out' , q=1 , value=1)
    frameOffset = c.intField( 'offset' , q=1 , value=1)
    seleccion = c.ls (sl=1,long=1,r=1)
    c.keyframe(edit=True,relative=True,timeChange=frameOffset,time=(frameIn,frameOut))
