#COPY LA ANIMACION DE UN BLENDSHAPE A OTRO (FRAME 0 A 10000)
#PRIMERO SE DEBE SELECCIONAR EL ORIGEN, SEGUNDO EL DESTINO

import maya.cmds as mc
import re

if len(mc.ls(sl=1))==2:

	blendShapeOrigen = ( mc.ls(sl=1)[0] ).split(":")
	blendShapeDestino = ( mc.ls(sl=1)[1] ).split(":")
	rutaBlendOrigen = ""
	rutaBlendDestino = ""
	for i in range ( len(blendShapeOrigen)-1):
		rutaBlendOrigen = rutaBlendOrigen + blendShapeOrigen[i]+":"
	for i in range ( len(blendShapeDestino)-1):
		rutaBlendDestino = rutaBlendDestino + blendShapeDestino[i]+":"

	mc.copyKey ( rutaBlendOrigen + ":Face_Blend" , time= (0,10000) )
	mc.pasteKey( rutaBlendDestino + ":Face_Blend")
else:
	mc.warning ("DEBES SELECCIONAR 2 OBJETOS. PRIMERO EL ORIGEN, SEGUNDO EL DESTINO. PODES SELECCIONAR CUALQUIER COSA DEL RIG.")
