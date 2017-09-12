#COPY LA ANIMACION DE UN BLENDSHAPE A OTRO (FRAME 0 A 10000)
#PRIMERO SE DEBE SELECCIONAR EL ORIGEN, SEGUNDO EL DESTINO
import maya.cmds as mc
import maya.mel as mel
import re
import pymel.core as pCore
#version 1.0.1
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
		pCore.melGlobals['gHIKCurrentCharacter'] = charDestino
		mel.eval('mayaHIKsetCharacterInput("'+charDestino + '","' + charOrigen+'");')
		mc.HIKCharacterControlsTool()
		pCore.mel.hikUpdateCharacterControlsUI(True)
		tipoPanelQ = mc.getPanel ( type="modelPanel")
		for panel_ in tipoPanelQ:
			mc.modelEditor ( panel_ , e=1 , activeView=1 )
			mc.isolateSelect (panel_ , state=1)
		mel.eval ('hikBakeToControlRig 1;')
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
