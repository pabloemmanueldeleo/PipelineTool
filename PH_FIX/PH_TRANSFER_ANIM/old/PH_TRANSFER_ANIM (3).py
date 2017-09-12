#COPY LA ANIMACION DE UN BLENDSHAPE A OTRO (FRAME 0 A 10000)
#PRIMERO SE DEBE SELECCIONAR EL ORIGEN, SEGUNDO EL DESTINO
import maya.cmds as mc
import maya.mel as mel
import re
import pymel.core as pCore
def borrarDuplicados (aConDuplicados):
    a = set(aConDuplicados)
    result = []
    for item in a:
        result.append(item)
    return result
def transferAllMain():
	if len(mc.ls(sl=1))==2:
		blendsCopiados=0
		keysCopiados=0
		blendShapeOrigen = ( mc.ls(sl=1)[0] ).split(":")
		blendShapeDestino = ( mc.ls(sl=1)[1] ).split(":")
		rutaBlendOrigen = ""
		rutaBlendDestino = ""
		for i in range ( len(blendShapeOrigen)-1):
			rutaBlendOrigen = rutaBlendOrigen + blendShapeOrigen[i]+":"
		for i in range ( len(blendShapeDestino)-1):
			rutaBlendDestino = rutaBlendDestino + blendShapeDestino[i]+":"
		nsOrigen = rutaBlendOrigen
		nsDestino = rutaBlendDestino
		#busco char ............................................................................
		nombreCharO= mc.ls(nsOrigen+"Character?",nsOrigen+"Character")
		if len(nombreCharO)==1:
			charOrigen = nombreCharO[0]
			print charOrigen
		else:
			charOrigen=""
		nombreCharD= mc.ls(nsDestino+"Character?",nsDestino+"Character")
		if len(nombreCharD)==1:
			charDestino = nombreCharD[0]
			print charDestino
		else:
			charDestino=""
		# copio blends ...........................................................................
		rutaBlendOrigen = rutaBlendOrigen + "Face_Blend"
		rutaBlendDestino = rutaBlendDestino + "Face_Blend"
			# copio attrs ...........................................................................
		Sizemorphs = mc.getAttr (rutaBlendOrigen+".weight" , s=1 )
		for i in range(Sizemorphs):
			blendshape=mc.listAttr(rutaBlendOrigen+'.weight'+'['+str(i)+']')[0]
			vAtt = mc.getAttr(rutaBlendOrigen+".weight"+"["+str(i)+"]")
			print blendshape, vAtt
			mc.setAttr ( rutaBlendDestino +"."+ blendshape, vAtt )
		print mc.keyframe (rutaBlendOrigen , q=1)
		if mc.keyframe (rutaBlendOrigen , q=1) != None:
			mc.copyKey ( rutaBlendOrigen , time= (0,10000) )
			mc.pasteKey( rutaBlendDestino)
		# copio animacion HIK ....................................................................
		# saco rango de animacion: frameInicial ----> frameFinal
		if charOrigen!="" and charDestino!="":
			controles_huesos = mc.ls(nsOrigen+"Ctrl*")
			frameInicial= 99999
			frameFinal=0
			for item in mc.ls(nsOrigen+"*" , type = "joint"):
				controles_huesos.append (item)
			controles_huesos = borrarDuplicados (controles_huesos)
			controles_huesos.sort()
			controles_huesos.reverse()
		i=0
		for i in range (len(controles_huesos)):
			if mc.keyframe (controles_huesos[i] , q=1 , keyframeCount=1 ) != 0:
				keysQ = mc.keyframe (controles_huesos[i] , q=1)
				keysQ.sort()
				if keysQ[0] < frameInicial:
					frameInicial = keysQ[0]
				if keysQ[-1] > frameFinal:
					frameFinal = keysQ[-1]
		pCore.melGlobals['gHIKCurrentCharacter'] = charDestino
		mel.eval('mayaHIKsetCharacterInput("'+charDestino + '","' + charOrigen+'");')
		mc.HIKCharacterControlsTool()
		pCore.mel.hikUpdateCharacterControlsUI(True)
		tipoPanelQ = mc.getPanel ( type="modelPanel")
		for panel_ in tipoPanelQ:
			mc.modelEditor ( panel_ , e=1 , activeView=1 )
			mc.isolateSelect (panel_ , state=1)
		mel.eval ('hikBakeToControlRig 1;')
		if frameInicial==99999 and frameFinal==0:
			mc.headsUpMessage ("NO SE HA PODIDO DETECTAR EL RANGO DE ANIMACION. INGRESA LOS LOS VALORES.",verticalOffset=-330)
		else:
			mc.headsUpMessage ("RANGO DE ANIMACION DETECTADO (FRAMES) : "+ str(int(frameInicial)) +" A "+ str(int(frameFinal)) ,verticalOffset=-330 )
		mc.HIKCharacterControlsTool()
		pCore.mel.hikUpdateCharacterControlsUI(True)
	else:
		mc.warning ("DEBES SELECCIONAR 2 OBJETOS. PRIMERO EL ORIGEN, SEGUNDO EL DESTINO. PODES SELECCIONAR CUALQUIER COSA DEL RIG.")

#COPIA LA ANIMACION DE UN BLENDSHAPE A OTRO (FRAME 0 A 10000)
#PRIMERO SE DEBE SELECCIONAR EL ORIGEN, SEGUNDO EL DESTINO
def transferBlendsMain():
	if len(mc.ls(sl=1))==2:
		blendShapeOrigen = ( mc.ls(sl=1)[0] ).split(":")
		blendShapeDestino = ( mc.ls(sl=1)[1] ).split(":")
		rutaBlendOrigen = ""
		rutaBlendDestino = ""
		for i in range ( len(blendShapeOrigen)-1):
			rutaBlendOrigen = rutaBlendOrigen + blendShapeOrigen[i]+":"
		for i in range ( len(blendShapeDestino)-1):
			rutaBlendDestino = rutaBlendDestino + blendShapeDestino[i]+":"
		Sizemorphs = mc.getAttr (rutaBlendOrigen+"Face_Blend.weight" , s=1 )
		for i in range(Sizemorphs):
			blendshape=mc.listAttr(rutaBlendOrigen+'Face_Blend.weight'+'['+str(i)+']')[0]
			vAtt = mc.getAttr(rutaBlendOrigen+"Face_Blend.weight"+"["+str(i)+"]")
			print blendshape, vAtt
			mc.setAttr ( rutaBlendDestino +"Face_Blend."+ blendshape, vAtt )
		mc.copyKey ( rutaBlendOrigen + ":Face_Blend" , time= (0,10000) )
		mc.pasteKey( rutaBlendDestino + ":Face_Blend")
	else:
		mc.warning ("DEBES SELECCIONAR 2 OBJETOS. PRIMERO EL ORIGEN, SEGUNDO EL DESTINO. PODES SELECCIONAR CUALQUIER COSA DEL RIG.")
