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
		nombreCharO= mc.ls(rutaBlendOrigen+"Character?",rutaBlendOrigen+"Character")
		if len(nombreCharO)==1:
			charOrigen = nombreCharO[0]
			print charOrigen
		else:
			charOrigen=""

		nombreCharD= mc.ls(rutaBlendDestino+"Character?",rutaBlendDestino+"Character")
		if len(nombreCharD)==1:
			charDestino = nombreCharD[0]
			print charDestino
		else:
			charDestino=""
		# copio blends ...........................................................................
		rutaBlendOrigen = rutaBlendOrigen + "Face_Blend"
		rutaBlendDestino = rutaBlendDestino + "Face_Blend"
			# copio attrs ...........................................................................
		morphs = mc.listConnections (rutaBlendOrigen , p=1 , type="mesh" , exactType=1)
		for i in range( len (morphs)):
			vAtt = mc.getAttr(rutaBlendOrigen+".weight"+"["+str(i)+"]")
			print vAtt
			mc.setAttr ( rutaBlendDestino+"."+([morphs[i].split('Shape.worldMesh')][0][0]).split(nsOrigen)[1] , vAtt )
		print mc.keyframe (rutaBlendOrigen , q=1)
		if mc.keyframe (rutaBlendOrigen , q=1) != None:
			mc.copyKey ( rutaBlendOrigen , time= (0,10000) )
			mc.pasteKey( rutaBlendDestino)

		# copio animacion HIK ....................................................................
		# saco rango de animacion: frameInicial ----> frameFinal
		if charOrigen!="" and charDestino!="":
			controles_huesos = mc.ls(nsOrigen+"Ctrl*")
			frameInicial= 0
			frameFinal=0
			for item in mc.ls(nsOrigen+"*" , type = "joint"):
				controles_huesos.append (item)
			controles_huesos = borrarDuplicados (controles_huesos)
			controles_huesos.sort()
		i=0
		for item in controles_huesos:
			if mc.keyframe (item , q=1 , keyframeCount=1 ) != 0:
				keysQ = mc.keyframe (item , q=1)
				keysQ.sort()
				if i==0:
					i+=1
					frameInicial = keysQ[0]
				else:
					if keysQ[0] < frameInicial:
						frameInicial = keysQ[0]
					if keysQ[-1] > frameFinal:
						frameFinal = keysQ[-1]
						print item
		pCore.melGlobals['gHIKCurrentCharacter'] = charDestino
		mel.eval('mayaHIKsetCharacterInput("'+charDestino + '","' + charOrigen+'");')
		mc.HIKCharacterControlsTool()
		pCore.mel.hikUpdateCharacterControlsUI(True)
		tipoPanelQ = mc.getPanel ( type="modelPanel")
		for panel_ in tipoPanelQ:
			mc.modelEditor ( panel_ , e=1 , activeView=1 )
			mc.isolateSelect (panel_ , state=1)
		mel.eval ('hikBakeToControlRig 1;')
		mc.headsUpMessage ("         RANGO DE ANIMACION DETECTADO (FRAMES) : "+ str(int(frameInicial)) +" A "+ str(int(frameFinal)) ,verticalOffset=-330 )
		print ("         RANGO DE ANIMACION DETECTADO (FRAMES) : "+ str(int(frameInicial)) +" A "+ str(int(frameFinal))  )
		mc.HIKCharacterControlsTool()
		pCore.mel.hikUpdateCharacterControlsUI(True)
		# FALTA desactivar viewport
	else:
		mc.warning ("DEBES SELECCIONAR 2 OBJETOS. PRIMERO EL ORIGEN, SEGUNDO EL DESTINO. PODES SELECCIONAR CUALQUIER COSA DEL RIG.")

		
